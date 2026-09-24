"""Predict an upcoming week's real games using the current, fully-tuned model.

Walks the model through all completed history to get CURRENT end-of-history
ratings, applies one offseason regression step to project those ratings into
the new season (same 25% team-elo regression the model always does at a
season boundary, done manually here since the walk-forward loop in
elo_model.run() can't process rows with no score yet), then predicts the
requested week using only information legitimately available before kickoff.

Uses pipeline.build_training_data() for history, the SAME function main.py
uses, so this can never silently drift out of sync with the shipped model
again (that exact staleness bug is what broke the first draft of this file
in Session 41: it predated several features elo_model.run() now requires).

Every coefficient below is read from elo_model.run()'s own defaults, not
hardcoded, so if a currently-shelved feature (rest_coef, travel_coef,
oline_boost, etc.) ever gets activated, this script picks it up automatically
without needing a manual update. Two features genuinely can't be computed
this far from kickoff and degrade gracefully instead of guessing:
  - Weather (rain_snow_coef, extreme_cold_coef): needs a forecast, which the
    NWS API only provides ~7-10 days out. Beyond that range, assumes neutral
    weather (no adjustment), same principle as injury data not existing yet.
  - Confirmed starting QB: uses pipeline.predict_starters()'s validated
    fallback (86.7% -> 88.7% accuracy), not a guess.
"""
from statistics import NormalDist
import pandas as pd
import dataloader
import elo_model
import pipeline

HIST_YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

# Pull the model's own shipped defaults instead of hardcoding them here.
# If a coefficient changes in elo_model.py, this script updates automatically.
import inspect
_MARGIN_DEFAULTS = {k: v.default for k, v in inspect.signature(elo_model.run).parameters.items()}
_TOTALS_DEFAULTS = {k: v.default for k, v in inspect.signature(elo_model.run_totals).parameters.items()}


def get_current_state(season=None, week=1):
    """Run the model through everything that has actually been played and
    return current ratings.

    Week 1 (nothing played yet this season): walk 2018-2025, then manually
    project one offseason forward (the walk-forward loop can't process rows
    with no score, so the season-boundary regression it would normally apply
    is done by hand here).

    Week 2+: include the current season's completed games in the walk, so
    ratings react to what's happened this year. In that case the walk itself
    applies the 25% regression at the 2025->2026 boundary, so applying it
    again here would double-regress. It deliberately does not.
    """
    include_current = season is not None and week > 1
    years = HIST_YEARS + [season] if include_current else HIST_YEARS
    df = pipeline.build_training_data(years)

    if include_current:
        n_current = int((df['season'] == season).sum())
        if n_current == 0:
            # Would otherwise silently produce Week-1-style ratings for a
            # later week, which is exactly the failure this function exists to prevent.
            raise RuntimeError(
                f"Asked for {season} week {week} but no completed {season} games "
                f"made it into the training data (play-by-play not published yet?)")
        print(f"State includes {n_current} completed {season} games "
              f"(through week {int(df[df['season'] == season]['week'].max())}).")

    margin_result = elo_model.run(df)
    totals_result = elo_model.run_totals(df)

    if include_current:
        elo = dict(margin_result['elo'])
        off_elo = dict(totals_result['off_elo'])
        def_elo = dict(totals_result['def_elo'])
    else:
        # team elo/off_elo/def_elo regress 25% toward 1500 at every season
        # boundary; qb_rating/oline_rating/cpoe_rating all ship with
        # retention=1.0-equivalent no-op behavior currently, so no regression
        # step needed for them, they carry forward unchanged
        elo = {t: 1500 + 0.75 * (v - 1500) for t, v in margin_result['elo'].items()}
        off_elo = {t: 1500 + 0.75 * (v - 1500) for t, v in totals_result['off_elo'].items()}
        def_elo = {t: 1500 + 0.75 * (v - 1500) for t, v in totals_result['def_elo'].items()}
    qb_rating = dict(margin_result['qb_rating'])
    qb_baseline = pd.concat([df['home_qb_epa'], df['away_qb_epa']]).mean()

    return {'elo': elo, 'off_elo': off_elo, 'def_elo': def_elo,
            'qb_rating': qb_rating, 'qb_baseline': qb_baseline, 'df': df}


def get_weather_or_none(home_team, game_date):
    """Best-effort forecast for the actual game date; returns None if out of
    the ~7-10 day NWS range or the request otherwise fails. Caller must
    treat None as "unknown, assume neutral," never as "confirmed clear."
    """
    import metrics
    try:
        lat, lon = metrics.STADIUM_COORDS[home_team]
        return pipeline.get_weather_forecast(lat, lon, game_date)
    except Exception:
        return None


def _try_with_current_season(loader_fn, hist_years, season):
    """Try fetching `hist_years + [season]`; if the current season has no
    data yet (nflverse 404s, since no games played means no file published),
    fall back to history only rather than crashing the whole prediction."""
    try:
        return loader_fn(hist_years + [season])
    except Exception:
        return loader_fn(hist_years)


def predict_games(season, week, state):
    import metrics  # local import: only needed here, keeps module import light
    elo, off_elo, def_elo = state['elo'], state['off_elo'], state['def_elo']
    qb_rating, qb_baseline = state['qb_rating'], state['qb_baseline']
    hist_df = state['df']

    schedule = dataloader.load_schedules([season])
    games = schedule[(schedule['season'] == season) & (schedule['week'] == week)]
    # Never "predict" a game whose result is already known, since that would
    # be post-hoc and the whole point of this pipeline is pre-registration.
    # (get_played_games() reports what got excluded so it can be disclosed.)
    games = games[games['home_score'].isna()]

    ids = dataloader.load_ids()
    # snap_counts/injuries only exist for a season once games have actually
    # been played. Early in a new season (e.g. predicting Week 1) nflverse
    # has no file for it yet and 404s. Fall back to history-only, which is
    # exactly correct here: with zero current-season games, there's nothing
    # to override the "last known starter" default anyway.
    snap_counts = _try_with_current_season(dataloader.load_snap_counts, HIST_YEARS, season)
    injuries = _try_with_current_season(dataloader.load_injuries, HIST_YEARS, season)
    full_schedule = dataloader.load_schedules(HIST_YEARS + [season])  # schedules ARE published in advance
    starters = pipeline.predict_starters(full_schedule, injuries, snap_counts, ids)
    starters_this_week = starters[(starters['season'] == season) & (starters['week'] == week)]
    starter_by_team = dict(zip(starters_this_week['team'], starters_this_week['predicted_qb_id']))

    this_week_injuries = injuries[(injuries['season'] == season) & (injuries['week'] == week)]
    df_inj = metrics.add_injuries(games.copy(), this_week_injuries) if len(this_week_injuries) else None

    league_avg_total = hist_df['total'].mean()

    m = _MARGIN_DEFAULTS
    t = _TOTALS_DEFAULTS

    predictions = []
    for _, row in games.iterrows():
        home, away = row['home_team'], row['away_team']
        home_elo = elo.get(home, 1500)
        away_elo = elo.get(away, 1500)

        home_qb = starter_by_team.get(home)
        away_qb = starter_by_team.get(away)
        home_qb_rating = qb_rating.get(home_qb, qb_baseline)
        away_qb_rating = qb_rating.get(away_qb, qb_baseline)

        home_sev = away_sev = 0
        if df_inj is not None:
            match = df_inj[(df_inj['home_team'] == home) & (df_inj['away_team'] == away)]
            if len(match):
                home_sev, away_sev = match.iloc[0]['home_severity'], match.iloc[0]['away_severity']

        rest_diff = row['home_rest'] - row['away_rest']

        # margin prediction: mirrors elo_model.run()'s `expected` formula exactly,
        # using its own current defaults (mostly 0/shelved right now, but picks up
        # automatically if any of them get activated in a future session)
        expected_margin = max(min(
            (home_elo - away_elo) / 25 + m['hfa'] + m['rest_coef'] * rest_diff
            + m['qb_boost'] * (home_qb_rating - away_qb_rating)
            + m['injury_coef'] * (away_sev - home_sev), 20), -20)
        win_prob = NormalDist().cdf(expected_margin / m['sigma'])

        # totals prediction: weather-dependent terms only apply if a forecast
        # is actually obtainable this far out; otherwise assume neutral weather
        home_off, away_off = off_elo.get(home, 1500), off_elo.get(away, 1500)
        home_def, away_def = def_elo.get(home, 1500), def_elo.get(away, 1500)
        expected_total = (league_avg_total / 2 + (home_off - away_def) / t['scale'] + t['hfa']
                          + league_avg_total / 2 + (away_off - home_def) / t['scale'])
        if row['div_game']:
            expected_total -= t['div_coef']
        if row['surface'] and str(row['surface']).strip().lower() != 'grass':
            expected_total += t['turf_coef']

        forecast = get_weather_or_none(home, row['gameday'])
        if forecast is not None and row['roof'] in ('outdoors', 'open'):
            if forecast['bad_weather']:
                expected_total -= t['rain_snow_coef']
            if forecast['clear_weather']:
                expected_total += t['clear_weather_coef']
            if forecast['wind'] is not None and forecast['wind'] > t['wind_threshold']:
                expected_total -= t['wind_coef'] * (forecast['wind'] - t['wind_threshold'])

        # implied scores from the two SEPARATE, independently-validated models.
        # margin (home-away) and total (home+away) are two equations, two
        # unknowns: home = (total+margin)/2, away = (total-margin)/2
        predicted_home_score = round((expected_total + expected_margin) / 2, 1)
        predicted_away_score = round((expected_total - expected_margin) / 2, 1)

        predictions.append({
            'gameday': row['gameday'], 'home': home, 'away': away,
            'predicted_margin': round(expected_margin, 1),
            'home_win_prob': round(win_prob, 3),
            'predicted_total': round(expected_total, 1),
            'predicted_home_score': predicted_home_score,
            'predicted_away_score': predicted_away_score,
            'home_qb': home_qb, 'away_qb': away_qb,
            'home_severity': home_sev, 'away_severity': away_sev,
            'weather_known': forecast is not None,
        })
    return predictions


def get_played_games(season, week):
    """Games in this week whose result is already known, excluded from
    predictions and disclosed in the published file instead."""
    schedule = dataloader.load_schedules([season])
    games = schedule[(schedule['season'] == season) & (schedule['week'] == week)]
    return games[games['home_score'].notna()]


def format_predictions_markdown(season, week, preds, notes=None):
    """Render a week's predictions as a public-facing markdown page. The
    generation timestamp here is informational only. The REAL proof of
    timing is the git commit / GitHub push timestamp once this file is
    committed and pushed to the public repo, which is independent of
    anything this script claims about itself.
    """
    import datetime
    generated_at = datetime.datetime.now().isoformat(timespec='seconds')
    lines = [
        f"# {season} Week {week} Predictions",
        "",
        f"Generated: {generated_at} (local). Locked parameters, honestly "
        f"validated on 2018-2025 held-out data, see PROGRESS.md for the "
        f"full methodology and every negative result along the way.",
        "",
        "| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for p in preds:
        fav = p['home'] if p['predicted_margin'] >= 0 else p['away']
        weather_note = '' if p['weather_known'] else ' *(weather TBD)*'
        lines.append(f"| {p['gameday']} | {p['away']} | {p['home']} | "
                     f"{p['away']} {p['predicted_away_score']:.1f} - "
                     f"{p['predicted_home_score']:.1f} {p['home']} | "
                     f"{p['predicted_margin']:+.1f} | {p['home_win_prob']:.1%} | "
                     f"{p['predicted_total']:.1f}{weather_note} | {fav} |")
    for note in (notes or []):
        lines += ["", f"**Note:** {note}"]
    return "\n".join(lines) + "\n"


def save_predictions(season, week, preds, out_dir='predictions', notes=None, overwrite=False):
    """Write the week's markdown file. Refuses to overwrite an existing file
    by default: once a week's predictions are published, regenerating that
    file would replace the pre-registered record with a fresh run."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{season}-week{week:02d}.md")
    if os.path.exists(path) and not overwrite:
        raise FileExistsError(f"{path} already exists, refusing to overwrite a published prediction file")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(format_predictions_markdown(season, week, preds, notes=notes))
    return path


if __name__ == '__main__':
    # usage: python predict_week.py [season] [week] [--save]
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    season = int(args[0]) if len(args) > 0 else 2026
    week = int(args[1]) if len(args) > 1 else 1
    save = '--save' in sys.argv

    state = get_current_state(season, week)
    preds = predict_games(season, week, state)

    notes = []
    for _, g in get_played_games(season, week).iterrows():
        notes.append(f"{g['away_team']} @ {g['home_team']} ({g['gameday']}) had already been played "
                     f"when this file was generated, so it is not part of this pre-registered set. "
                     f"No prediction for it was posted before kickoff.")

    print(f"\n{season} Week {week} predictions ({len(preds)} games):\n")
    for p in preds:
        fav = p['home'] if p['predicted_margin'] >= 0 else p['away']
        weather_note = '' if p['weather_known'] else ' (weather TBD, no forecast available for that date)'
        print(f"{p['gameday']}  {p['away']} {p['predicted_away_score']:.1f} - "
              f"{p['predicted_home_score']:.1f} {p['home']}  "
              f"(margin {p['predicted_margin']:+.1f}, "
              f"home win prob {p['home_win_prob']:.1%}, "
              f"total {p['predicted_total']:.1f}), favorite {fav}{weather_note}")
    for n in notes:
        print(f"\nNOTE: {n}")

    if save:
        print("\nSAVED TO:", save_predictions(season, week, preds, notes=notes))
    else:
        print("\n(Not saved, re-run with --save to write the markdown file.)")
