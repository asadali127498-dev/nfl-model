"""Live, in-season prediction helpers, separate from elo_model.py's historical
walk-forward training/evaluation. These answer "what do we know before THIS
week's games" rather than grading against a known outcome.
"""
import re
import json
import urllib.request
import pandas as pd
import dataloader
import metrics


def build_training_data(years):
    """The FULL historical feature pipeline, shared by main.py and
    predict_week.py so they can never silently drift apart. This is the
    exact bug that broke the first draft of predict_week.py (Session 41):
    it predated several shipped features, and elo_model.run() now
    unconditionally reads columns that draft never built. One source of
    truth from here on; add new metrics.add_*() calls here ONLY.
    """
    df = dataloader.load_schedules(years)
    # Core play-by-play is deliberately NOT given a fallback. If it's missing
    # for a season we asked for, that season's games would silently vanish
    # from the ratings (add_epa_margin inner-joins on it), so this fails loudly.
    pbp = dataloader.load_pbp(years)
    df = metrics.add_epa_margin(df, pbp)
    df = metrics.add_adjusted_epa_margin(df)
    df = metrics.add_turnover_margin(df, pbp)
    df = metrics.add_sack_rate(df, pbp)
    df = metrics.add_success_rate(df, pbp)
    df = metrics.add_weather(df, pbp)
    df = metrics.add_surface(df)
    df = metrics.add_extreme_cold(df)
    df = metrics.add_qb_epa(df, pbp)
    # Optional/secondary data can lag pbp for a season still in progress, or
    # not exist yet. Every merge below is a left join though, so a missing
    # tail year just leaves NaN/0 for those rows instead of breaking anything.
    ngs_passing = _load_allow_missing_tail(dataloader.load_ngs_passing, years)
    df = metrics.add_cpoe(df, ngs_passing)
    df = metrics.add_travel(df)
    df = metrics.add_body_clock(df)
    df = metrics.add_primetime(df)
    injuries = _load_allow_missing_tail(dataloader.load_injuries, years)
    df = metrics.add_injuries(df, injuries)
    snap_counts = _load_allow_missing_tail(dataloader.load_snap_counts, years)
    ids = dataloader.load_ids()
    df = metrics.add_injuries_starters(df, injuries, snap_counts, ids)
    ftn = _load_allow_missing_tail(dataloader.load_ftn, [y for y in years if y >= 2022])  # FTN only exists from 2022
    df = metrics.add_oline_fault_sack_rate(df, pbp, ftn)
    return df


def _load_allow_missing_tail(loader, years):
    """Load `years`; if that fails (nflverse 404s for a season with no
    published file yet), retry once without the most recent year. Only for
    secondary data; see build_training_data for why pbp doesn't use this."""
    try:
        return loader(years)
    except Exception:
        if len(years) <= 1:
            raise
        return loader([y for y in years if y != max(years)])


def get_weather_forecast(lat, lon, game_date, contact_email='nfl-model@example.com'):
    """Pregame weather forecast from the National Weather Service (free, no API
    key, US locations only, fine since every NFL stadium is in the US) for the
    DAYTIME period actually covering `game_date` (a date object or 'YYYY-MM-DD'
    string), NOT just whatever period happens to come first in the response.
    Returns None if no period in the forecast covers that date (NWS only
    publishes ~7-10 days out, so a game a month away has no real forecast yet.
    An earlier version of this function silently returned TODAY's weather
    for ANY game date, a real bug caught in Session 41 by checking the raw
    NWS response instead of trusting the wrapped output).

    Returns the same shape the model expects: {'bad_weather': bool,
    'clear_weather': bool, 'wind': float|None}.

    IMPORTANT CAVEAT, unlike every other feature in this project: this CANNOT
    be honestly backtested. `add_weather()`'s historical bad_weather/
    clear_weather columns come from `pbp['weather']`, the ACTUAL recorded
    conditions, known only after the game. A forecast is a genuinely
    different, less accurate signal (forecasts a few days out can be wrong),
    and no historical forecast archive exists to validate against. This
    function can only be smoke-tested for correctness, not honestly evaluated
    the way rain_snow_coef/div_coef/etc. were. Treat it as a best-effort
    stand-in, not a validated feature.
    """
    import datetime
    if isinstance(game_date, str):
        game_date = datetime.date.fromisoformat(game_date)

    headers = {'User-Agent': f'nfl-model ({contact_email})'}
    points_req = urllib.request.Request(f'https://api.weather.gov/points/{lat},{lon}', headers=headers)
    with urllib.request.urlopen(points_req, timeout=10) as resp:
        forecast_url = json.loads(resp.read())['properties']['forecast']

    forecast_req = urllib.request.Request(forecast_url, headers=headers)
    with urllib.request.urlopen(forecast_req, timeout=10) as resp:
        periods = json.loads(resp.read())['properties']['periods']

    period = None
    for p in periods:
        start = datetime.date.fromisoformat(p['startTime'][:10])
        end = datetime.date.fromisoformat(p['endTime'][:10])
        if start <= game_date <= end and p['isDaytime']:
            period = p
            break
    if period is None:
        return None  # game_date is outside the ~7-10 day forecast range

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
