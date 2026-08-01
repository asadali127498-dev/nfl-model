from statistics import NormalDist
import pandas as pd

def run_totals(df, K=0.6, hfa=1.25, scale=25, wind_coef=0, wind_threshold=15,
               rain_snow_coef=8, clear_weather_coef=0, div_coef=1.5, eval_from=2020, eval_to=2022):
    """Walk-forward offense/defense Elo, predicting game TOTAL (home+away score).

    Each team has two ratings: off_elo (scoring ability) and def_elo (points
    prevented). off_elo updates on the team's own EPA that game; def_elo
    updates on the opponent's EPA against them. Predictions are graded
    out-of-sample from `eval_from` through `eval_to`, against the real total
    and the Vegas total_line.

    For outdoor/open-roof games, wind above `wind_threshold` mph subtracts
    `wind_coef` points per mph over the threshold, and rain/snow (parsed from
    the play-by-play 'weather' text) subtracts a flat `rain_snow_coef` points.
    Both apply to the PREDICTION only — never the off_elo/def_elo rating
    updates, since weather is a one-game condition, not true team quality.
    `div_coef` subtracts a flat amount for divisional games (same
    prediction-only treatment — familiarity is a matchup trait, not a
    team-quality signal that should feed the ratings).
    """
    off_elo = {t: 1500 for t in df['home_team'].unique()}
    def_elo = {t: 1500 for t in df['home_team'].unique()}
    baseline = df['total'].mean() / 2
    current_season = None
    pred, act, veg, games = [], [], [], []

    for _, row in df.iterrows():
        if row['season'] != current_season:
            if current_season is not None:
                for t in off_elo:
                    off_elo[t] = 1500 + 0.75 * (off_elo[t] - 1500)
                for t in def_elo:
                    def_elo[t] = 1500 + 0.75 * (def_elo[t] - 1500)
            current_season = row['season']
        home, away = row['home_team'], row['away_team']

        expected_home_score = baseline + (off_elo[home] - def_elo[away]) / scale + hfa
        expected_away_score = baseline + (off_elo[away] - def_elo[home]) / scale
        expected_total = expected_home_score + expected_away_score

        wind = row['wind']
        if row['roof'] in ('outdoors', 'open') and wind > wind_threshold:
            expected_total -= wind_coef * (wind - wind_threshold)

        if row['roof'] in ('outdoors', 'open') and row['bad_weather']:
            expected_total -= rain_snow_coef

        if row['roof'] in ('outdoors', 'open') and row['clear_weather']:
            expected_total += clear_weather_coef

        if row['div_game']:
            expected_total -= div_coef

        if eval_from <= row['season'] <= eval_to:
            pred.append(expected_total)
            act.append(row['total'])
            veg.append(row['total_line'])
            games.append({'home': home, 'away': away, 'week': row['week'],
                          'roof': row['roof'], 'bad_weather': row['bad_weather'],
                          'clear_weather': row['clear_weather'], 'div_game': row['div_game'],
                          'pred': expected_total, 'actual': row['total'],
                          'vegas': row['total_line']})

        home_epa = row['home_epa']
        away_epa = row['away_epa']
        off_elo[home] += K * (home_epa - (off_elo[home] - def_elo[away]) / scale)
        def_elo[away] -= K * (home_epa - (off_elo[home] - def_elo[away]) / scale)
        off_elo[away] += K * (away_epa - (off_elo[away] - def_elo[home]) / scale)
        def_elo[home] -= K * (away_epa - (off_elo[away] - def_elo[home]) / scale)
    
    

    mae = sum(abs(p - a) for p, a in zip(pred, act)) / len(pred)
    vegas_mae = sum(abs(v - a) for v, a in zip(veg, act)) / len(veg)

    return {'mae': mae, 'vegas_mae': vegas_mae, 'games': games,
            'off_elo': off_elo, 'def_elo': def_elo, 'n': len(pred)}

def run(df, K=2, w=1.0, cap=20, hfa=1.25, sigma=16, qb_regression=1.0, rest_coef=0.0,
        qb_k=0.15, qb_boost=5.0, qb_retention=1.0, travel_coef=-0.4, eval_from=2020, eval_to=2024):
    """Walk-forward Elo over the date order.

    Ratings train on a blend of the two signals: w * result + (1 - w) * epa_margin,
    capped at +/-cap to balance blowout games. w=1 is pure scoreboard, w=0 is pure EPA.
    Predictions are graded out-of-sample from season 2022-2024, always
    against the real scoreboard (`result`). Returns a dict of metrics.

    qb_rating is a SEPARATE, persistent rating per passer_id (not per team),
    tracked as an exponential moving average of the QB's own passing EPA/dropback,
    in EPA units (not Elo points). It carries across team changes since it's keyed
    by player, not team. `qb_boost` blends the rating gap into the prediction
    (prediction-only surface, but the QB rating itself updates every game like
    any other rating). `qb_retention` controls how much of the rating survives
    each offseason (1.0 = untouched, <1 regresses toward the league-average QB,
    >1 pushes further from average — for QBs who are still improving). Retention
    only applies to QBs who played in the season that just ended — an inactive/
    retired QB's rating is left frozen rather than compounded every offseason
    with nothing (no games) to ever correct it back.

    qb_k=0.05/qb_retention=1.8 were tuned in Session 28 and looked better on
    validation, but the combined honest test (2023-25) came back WORSE
    (MAE 10.2421) than these Session 27 defaults (MAE 10.2107) — reverted
    intentionally, not carried forward. See PROGRESS.md Session 28.

    `travel_coef` boosts the home team's expected margin based on how far
    (in thousands of miles) the AWAY team traveled from its own stadium —
    prediction-only, home team's own rating/travel is always 0 by definition.
    """
    last_qb = {}
    qb_last_season = {}
    elo = {t: 1500 for t in df['home_team'].unique()}
    qb_rating = {}
    qb_baseline = pd.concat([df['home_qb_epa'], df['away_qb_epa']]).mean()
    current_season = None
    pred, act, veg, winprobs, homewins, games = [], [], [], [], [], []

    for _, row in df.iterrows():
        if row['season'] != current_season:
            if current_season is not None:
                for t in elo:
                    elo[t] = 1500 + 0.75 * (elo[t] - 1500)
                for qb in qb_rating:
                    if qb_last_season.get(qb) == current_season:
                        qb_rating[qb] = qb_baseline + qb_retention * (qb_rating[qb] - qb_baseline)
            current_season = row['season']
        home_qb = row['home_qb_id']
        away_qb = row['away_qb_id']
        home, away = row['home_team'], row['away_team']
        home_qb_changed = home in last_qb and home_qb != last_qb[home] and row['week'] != 18
        away_qb_changed = away in last_qb and away_qb != last_qb[away] and row['week'] != 18
        if home_qb_changed:
            elo[home] = 1500 + qb_regression * (elo[home] - 1500)
        if away_qb_changed:
            elo[away] = 1500 + qb_regression * (elo[away] - 1500)
        blended = w * row['result'] + (1 - w) * row['epa_margin']
        actual = max(min(blended, cap), -cap)
        rest_diff = row['home_rest'] - row['away_rest']
        home_qb_rating = qb_rating.get(home_qb, qb_baseline)
        away_qb_rating = qb_rating.get(away_qb, qb_baseline)
        expected = max(min((elo[home] - elo[away]) / 25 + hfa + rest_coef * rest_diff
                            + qb_boost * (home_qb_rating - away_qb_rating)
                            + travel_coef * (row['away_travel'] / 1000), 20), -20)
        win_prob = NormalDist().cdf(expected / sigma)

        if eval_from <= row['season'] <= eval_to:
            pred.append(expected)
            act.append(row['result'])
            veg.append(row['spread_line'])
            winprobs.append(win_prob)
            homewins.append(1 if row['result'] > 0 else 0)
            games.append({'home': home, 'away': away, 'week': row['week'],
                          'error': abs(expected - row['result']),
                          'vegas': row['spread_line'], 'actual': row['result']})

        if pd.notna(row['home_qb_epa']):
            qb_rating[home_qb] = home_qb_rating + qb_k * (row['home_qb_epa'] - home_qb_rating)
        if pd.notna(row['away_qb_epa']):
            qb_rating[away_qb] = away_qb_rating + qb_k * (row['away_qb_epa'] - away_qb_rating)

        elo[home] += K * (actual - expected)
        elo[away] -= K * (actual - expected)
        last_qb[home] = home_qb
        last_qb[away] = away_qb
        qb_last_season[home_qb] = row['season']
        qb_last_season[away_qb] = row['season']
    mae = sum(abs(p - a) for p, a in zip(pred, act)) / len(pred)
    vegas_mae = sum(abs(v - a) for v, a in zip(veg, act)) / len(veg)
    brier = sum((p - hw) ** 2 for p, hw in zip(winprobs, homewins)) / len(winprobs)

    return {'mae': mae, 'vegas_mae': vegas_mae, 'brier': brier,
            'elo': elo, 'qb_rating': qb_rating, 'winprobs': winprobs, 'homewins': homewins,
            'games': games, 'n': len(pred)}


def bucket_rate(winprobs, homewins, lo, hi):
    """Actual home win rate for games with predicted win_prob in [lo, hi)."""
    pairs = [(p, hw) for p, hw in zip(winprobs, homewins) if lo <= p < hi]
    if not pairs:
        return 0, None
    return len(pairs), sum(hw for _, hw in pairs) / len(pairs)


def calibration_table(winprobs, homewins):
    """Bucket predictions into 0.0-0.1 ... 0.9-1.0 and return (counts, wins)."""
    counts = {b: 0 for b in range(10)}
    wins = {b: 0 for b in range(10)}
    for p, hw in zip(winprobs, homewins):
        b = int(p * 10)
        counts[b] += 1
        wins[b] += hw
    return counts, wins
