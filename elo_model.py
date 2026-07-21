from statistics import NormalDist

def run_totals(df, K=2, hfa=1.5, scale=25, eval_from=2022, eval_to=2023):
    """Walk-forward offense/defense Elo, predicting game TOTAL (home+away score).

    Each team has two ratings: off_elo (scoring ability) and def_elo (points
    prevented). off_elo updates on the team's own EPA that game; def_elo
    updates on the opponent's EPA against them. Predictions are graded
    out-of-sample from `eval_from` through `eval_to`, against the real total
    and the Vegas total_line.
    """
    off_elo = {t: 1500 for t in df['home_team'].unique()}
    def_elo = {t: 1500 for t in df['home_team'].unique()}
    baseline = df['total'].mean() / 2
    current_season = None
    pred, act, veg = [], [], []

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

        if eval_from <= row['season'] <= eval_to:
            pred.append(expected_total)
            act.append(row['total'])
            veg.append(row['total_line'])

        home_epa = row['home_epa']
        away_epa = row['away_epa']
        off_elo[home] += K * (home_epa - (off_elo[home] - def_elo[away]) / scale)
        def_elo[away] -= K * (home_epa - (off_elo[home] - def_elo[away]) / scale)
        off_elo[away] += K * (away_epa - (off_elo[away] - def_elo[home]) / scale)
        def_elo[home] -= K * (away_epa - (off_elo[away] - def_elo[home]) / scale)
    
    

    mae = sum(abs(p - a) for p, a in zip(pred, act)) / len(pred)
    vegas_mae = sum(abs(v - a) for v, a in zip(veg, act)) / len(veg)

    return {'mae': mae, 'vegas_mae': vegas_mae,
            'off_elo': off_elo, 'def_elo': def_elo, 'n': len(pred)}

def run(df, K=2, w=1.0, cap=20, hfa=1.5, sigma=16, qb_regression=1.0, eval_from=2022, eval_to=2024):
    """Walk-forward Elo over the date order.

    Ratings train on a blend of the two signals: w * result + (1 - w) * epa_margin,
    capped at +/-cap to balance blowout games. w=1 is pure scoreboard, w=0 is pure EPA.
    Predictions are graded out-of-sample from season 2022-2024, always
    against the real scoreboard (`result`). Returns a dict of metrics.
    """
    last_qb = {}
    elo = {t: 1500 for t in df['home_team'].unique()}
    current_season = None
    pred, act, veg, winprobs, homewins, games = [], [], [], [], [], []

    for _, row in df.iterrows():
        if row['season'] != current_season:
            if current_season is not None:
                for t in elo:
                    elo[t] = 1500 + 0.75 * (elo[t] - 1500)
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
        expected = max(min((elo[home] - elo[away]) / 25 + hfa, 20), -20)
        win_prob = NormalDist().cdf(expected / sigma)

        if eval_from <= row['season'] <= eval_to:
            pred.append(expected)
            act.append(row['result'])
            veg.append(row['spread_line'])
            winprobs.append(win_prob)
            homewins.append(1 if row['result'] > 0 else 0)
            games.append({'home': home, 'away': away, 'week': row['week'],
                          'error': abs(expected - row['result'])})

        elo[home] += K * (actual - expected)
        elo[away] -= K * (actual - expected)
        last_qb[home] = home_qb
        last_qb[away] = away_qb
    mae = sum(abs(p - a) for p, a in zip(pred, act)) / len(pred)
    vegas_mae = sum(abs(v - a) for v, a in zip(veg, act)) / len(veg)
    brier = sum((p - hw) ** 2 for p, hw in zip(winprobs, homewins)) / len(winprobs)

    return {'mae': mae, 'vegas_mae': vegas_mae, 'brier': brier,
            'elo': elo, 'winprobs': winprobs, 'homewins': homewins,
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
