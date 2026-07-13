from statistics import NormalDist


def run(df, K=2, w=1.0, cap=20, hfa=2.5, sigma=16, eval_from=2022):
    """Walk-forward Elo over the date order.

    Ratings train on a blend of the two signals: w * result + (1 - w) * epa_margin,
    capped at +/-cap to balance blowout games. w=1 is pure scoreboard, w=0 is pure EPA.
    Predictions are graded out-of-sample from season `eval_from` onward, always
    against the real scoreboard (`result`). Returns a dict of metrics.
    """
    elo = {t: 1500 for t in df['home_team'].unique()}
    current_season = None
    pred, act, veg, winprobs, homewins = [], [], [], [], []

    for _, row in df.iterrows():
        if row['season'] != current_season:
            if current_season is not None:
                for t in elo:
                    elo[t] = 1500 + 0.75 * (elo[t] - 1500)
            current_season = row['season']

        home, away = row['home_team'], row['away_team']
        blended = w * row['result'] + (1 - w) * row['epa_margin']
        actual = max(min(blended, cap), -cap)
        expected = max(min((elo[home] - elo[away]) / 25 + hfa, 20), -20)
        win_prob = NormalDist().cdf(expected / sigma)

        if row['season'] >= eval_from:                         
            pred.append(expected)
            act.append(row['result'])                          
            veg.append(row['spread_line'])
            winprobs.append(win_prob)
            homewins.append(1 if row['result'] > 0 else 0)

        elo[home] += K * (actual - expected)
        elo[away] -= K * (actual - expected)

    mae = sum(abs(p - a) for p, a in zip(pred, act)) / len(pred)
    vegas_mae = sum(abs(v - a) for v, a in zip(veg, act)) / len(veg)
    brier = sum((p - hw) ** 2 for p, hw in zip(winprobs, homewins)) / len(winprobs)

    return {'mae': mae, 'vegas_mae': vegas_mae, 'brier': brier,
            'elo': elo, 'winprobs': winprobs, 'homewins': homewins,
            'n': len(pred)}


def calibration_table(winprobs, homewins):
    """Bucket predictions into 0.0-0.1 ... 0.9-1.0 and return (counts, wins)."""
    counts = {b: 0 for b in range(10)}
    wins = {b: 0 for b in range(10)}
    for p, hw in zip(winprobs, homewins):
        b = int(p * 10)
        counts[b] += 1
        wins[b] += hw
    return counts, wins
