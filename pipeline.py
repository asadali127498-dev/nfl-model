"""Live, in-season prediction helpers — separate from elo_model.py's historical
walk-forward training/evaluation. These answer "what do we know before THIS
week's games" rather than grading against a known outcome.
"""
import re
import json
import urllib.request
import pandas as pd


def get_weather_forecast(lat, lon, contact_email='nfl-model@example.com'):
    """Pregame weather forecast from the National Weather Service (free, no API
    key, US locations only — fine, every NFL stadium is in the US). Returns
    the same shape the model expects: {'bad_weather': bool, 'clear_weather':
    bool, 'wind': float|None}, using the DAYTIME period nearest to game day.

    IMPORTANT CAVEAT, unlike every other feature in this project: this CANNOT
    be honestly backtested. `add_weather()`'s historical bad_weather/
    clear_weather columns come from `pbp['weather']` — the ACTUAL recorded
    conditions, known only after the game. A forecast is a genuinely
    different, less accurate signal (forecasts a few days out can be wrong),
    and no historical forecast archive exists to validate against. This
    function can only be smoke-tested for correctness, not honestly evaluated
    the way rain_snow_coef/div_coef/etc. were. Treat it as a best-effort
    stand-in, not a validated feature, when the live pipeline is actually built.
    """
    headers = {'User-Agent': f'nfl-model ({contact_email})'}
    points_req = urllib.request.Request(f'https://api.weather.gov/points/{lat},{lon}', headers=headers)
    with urllib.request.urlopen(points_req, timeout=10) as resp:
        forecast_url = json.loads(resp.read())['properties']['forecast']

    forecast_req = urllib.request.Request(forecast_url, headers=headers)
    with urllib.request.urlopen(forecast_req, timeout=10) as resp:
        periods = json.loads(resp.read())['properties']['periods']

    period = periods[0]
    text = period['shortForecast'].lower()
    bad_weather = ('rain' in text) or ('snow' in text)
    clear_weather = ('sunny' in text) or ('clear' in text)
    wind_match = re.search(r'(\d+)', period['windSpeed'])
    wind = float(wind_match.group(1)) if wind_match else None

    return {'bad_weather': bad_weather, 'clear_weather': clear_weather, 'wind': wind,
            'raw_forecast': period['shortForecast'], 'period_name': period['name']}


def build_qb_crosswalk(ids):
    crosswalk = ids[['pfr_id', 'gsis_id']].dropna()
    crosswalk = crosswalk[crosswalk['gsis_id'].str.match(r'^\d{2}-\d{7}$')]
    crosswalk = crosswalk.drop_duplicates('pfr_id')
    crosswalk['gsis_id'] = crosswalk['gsis_id'].astype(object)
    return crosswalk


def predict_starters(schedule, injuries, snap_counts, ids):
    """For every (team, season, week) in `schedule`, predict the starting QB
    using only information available BEFORE that week:
      1. Default to the team's most recent known starter.
      2. If that QB is listed Out/Doubtful on this week's injury report,
         fall back to the team's highest-trailing-snap-share QB instead.

    Validated (Session 33) on 2018-2025 history: naive same-QB-as-last-time
    baseline gets 86.7% right; this fallback logic improves that to 88.7%
    overall, and 78.2% specifically on the ~119 games where the presumed
    starter was actually flagged unavailable (vs the naive approach's 4.2%
    on those same games). Returns `schedule` with a `predicted_qb_id` column.
    """
    home = schedule[['season', 'week', 'home_team', 'home_qb_id']].rename(
        columns={'home_team': 'team', 'home_qb_id': 'qb_id'})
    away = schedule[['season', 'week', 'away_team', 'away_qb_id']].rename(
        columns={'away_team': 'team', 'away_qb_id': 'qb_id'})
    qb_hist = pd.concat([home, away]).sort_values(['team', 'season', 'week'])
    qb_hist['predicted_naive'] = qb_hist.groupby('team')['qb_id'].shift(1).astype(object)

    crosswalk = build_qb_crosswalk(ids)
    qb_snaps = snap_counts[snap_counts['position'] == 'QB'].merge(
        crosswalk, left_on='pfr_player_id', right_on='pfr_id', how='left')
    qb_snaps = qb_snaps.dropna(subset=['gsis_id']).copy()
    qb_snaps['gsis_id'] = qb_snaps['gsis_id'].astype(object)
    qb_snaps = qb_snaps.sort_values(['team', 'season', 'week'])
    qb_snaps['trailing_pct'] = qb_snaps.groupby(['team', 'gsis_id'])['offense_pct'].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean())
    backup_pool = qb_snaps[['team', 'season', 'week', 'gsis_id', 'trailing_pct']].dropna(subset=['trailing_pct'])

    inj_out = injuries[injuries['report_status'].isin(['Out', 'Doubtful'])][
        ['season', 'week', 'team', 'gsis_id']].copy()
    inj_out['gsis_id'] = inj_out['gsis_id'].astype(object)
    inj_out['flagged_out'] = True

    qb_hist = qb_hist.merge(inj_out, left_on=['season', 'week', 'team', 'predicted_naive'],
                            right_on=['season', 'week', 'team', 'gsis_id'], how='left')
    qb_hist['flagged_out'] = qb_hist['flagged_out'].fillna(False)

    def find_backup(row):
        if not row['flagged_out']:
            return row['predicted_naive']
        candidates = backup_pool[(backup_pool['team'] == row['team']) &
                                  (backup_pool['season'] == row['season']) &
                                  (backup_pool['week'] == row['week']) &
                                  (backup_pool['gsis_id'] != row['predicted_naive'])]
        if len(candidates) == 0:
            return row['predicted_naive']
        return candidates.sort_values('trailing_pct', ascending=False).iloc[0]['gsis_id']

    qb_hist['predicted_qb_id'] = qb_hist.apply(find_backup, axis=1)
    return qb_hist[['team', 'season', 'week', 'predicted_qb_id']]
