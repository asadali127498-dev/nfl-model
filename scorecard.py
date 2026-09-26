"""Grades my published predictions against what actually happened.

I pull the numbers straight out of the markdown files in predictions/
instead of re-running the model. If I re-ran it, the ratings would have
already seen the results, so I'd be grading something I never actually
posted. The file on GitHub is the record, so the file is what gets graded.

I compare every game against the Vegas closing line from nflverse on margin
(my margin vs spread_line), on win probability (my Brier score vs the
market's, where I get the market's number from the moneylines with the vig
taken out), and on totals (my total vs total_line).

I also check whether each game was really pre-registered, which I'm counting
as the file's first git commit landing before that game kicked off. Week 2
fails that (I pushed it after the games), so it still gets graded but I keep
it out of the headline row. The commit time comes from my own clock and the
GitHub push time is the actual proof, but for Weeks 1 and 2 I checked and
the two line up.
"""
import glob
import os
import re
import subprocess
import datetime
import pandas as pd
import dataloader

PRED_DIR = 'predictions'


def parse_prediction_file(path):
    """Pull the game rows out of one published week file."""
    rows = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) != 8 or not re.match(r'\d{4}-\d{2}-\d{2}', cells[0]):
                continue
            gameday, away, home, _, margin, win_pct, total, _ = cells
            rows.append({
                'gameday': gameday, 'away_team': away, 'home_team': home,
                'pred_margin': float(margin),
                'pred_home_wp': float(win_pct.rstrip('%')) / 100,
                # the total column can carry a "*(weather TBD)*" tag
                'pred_total': float(total.split()[0]),
            })
    return pd.DataFrame(rows)


def first_commit_time(path):
    """When this file first entered git history, or None if it never has."""
    out = subprocess.run(['git', 'log', '--diff-filter=A', '--follow', '--format=%aI', '--', path],
                         capture_output=True, text=True).stdout.split()
    return datetime.datetime.fromisoformat(out[-1]) if out else None


def market_home_wp(home_ml, away_ml):
    """Home win probability from the moneylines with the vig taken out. The
    raw implied probabilities add up to a little over 1 (the extra is the
    sportsbook's cut), so I scale both down until they add up to exactly 1."""
    def implied(ml):
        return 100 / (ml + 100) if ml > 0 else -ml / (-ml + 100)
    h, a = implied(home_ml), implied(away_ml)
    return h / (h + a)


def load_graded(season):
    files = sorted(glob.glob(os.path.join(PRED_DIR, f'{season}-week*.md')))
    sched = dataloader.load_schedules([season])
    # nflverse gametime is Eastern; git gives me an offset-aware time, so I
    # attach Eastern to the kickoff to compare them properly
    from zoneinfo import ZoneInfo
    sched['kickoff'] = pd.to_datetime(sched['gameday'] + ' ' + sched['gametime']).dt.tz_localize(
        ZoneInfo('America/New_York'))

    graded = []
    for path in files:
        week = int(re.search(r'week(\d+)', path).group(1))
        preds = parse_prediction_file(path)
        committed = first_commit_time(path)
        df = preds.merge(sched, on=['gameday', 'away_team', 'home_team'], how='left')
        missing = df['week'].isna()
        if missing.any():
            raise ValueError(f"{path}: couldn't match {df[missing][['away_team', 'home_team']].values.tolist()} to the schedule")
        df['file_week'] = week
        df['committed_at'] = committed
        df['pre_registered'] = df['kickoff'].apply(lambda k: committed is not None and committed < k)
        # I only grade a week once every game in it is final, otherwise a week
        # where only Thursday night is done would show up as a 1-game tally
        if df['result'].isna().any():
            print(f"Skipping week {week}: {int(df['result'].isna().sum())} game(s) not played yet.")
            continue
        graded.append(df)

    df = pd.concat(graded, ignore_index=True)
    df['home_won'] = (df['result'] > 0).astype(float)
    df.loc[df['result'] == 0, 'home_won'] = 0.5
    df['vegas_home_wp'] = [market_home_wp(h, a) for h, a in zip(df['home_moneyline'], df['away_moneyline'])]
    df['model_margin_err'] = (df['pred_margin'] - df['result']).abs()
    df['vegas_margin_err'] = (df['spread_line'] - df['result']).abs()
    df['model_total_err'] = (df['pred_total'] - df['total']).abs()
    df['vegas_total_err'] = (df['total_line'] - df['total']).abs()
    # straight-up pick: whoever the predicted margin favors. A 0.0 margin is no pick.
    df['model_correct'] = (df['pred_margin'] * df['result'] > 0)
    df['vegas_correct'] = (df['spread_line'] * df['result'] > 0)
    return df


def summarize(df):
    n = len(df)
    return {
        'games': n,
        'model_su': f"{int(df['model_correct'].sum())}-{n - int(df['model_correct'].sum())}",
        'vegas_su': f"{int(df['vegas_correct'].sum())}-{n - int(df['vegas_correct'].sum())}",
        'model_mae': df['model_margin_err'].mean(),
        'vegas_mae': df['vegas_margin_err'].mean(),
        'model_brier': ((df['pred_home_wp'] - df['home_won']) ** 2).mean(),
        'vegas_brier': ((df['vegas_home_wp'] - df['home_won']) ** 2).mean(),
        'model_total_mae': df['model_total_err'].mean(),
        'vegas_total_mae': df['vegas_total_err'].mean(),
        'closer_than_vegas': int((df['model_margin_err'] < df['vegas_margin_err']).sum()),
    }


def summary_rows(label, s):
    return [
        f"| {label} | {s['games']} | {s['model_su']} / {s['vegas_su']} | "
        f"{s['model_mae']:.2f} / {s['vegas_mae']:.2f} | "
        f"{s['model_brier']:.3f} / {s['vegas_brier']:.3f} | "
        f"{s['model_total_mae']:.2f} / {s['vegas_total_mae']:.2f} | "
        f"{s['closer_than_vegas']} of {s['games']} |"
    ]


def format_scorecard(season, df):
    generated = datetime.datetime.now().isoformat(timespec='seconds')
    lines = [
        f"# {season} Scorecard",
        "",
        f"Updated {generated} (local time). I graded every number here from the prediction files "
        f"exactly as I posted them, not from a re-run of the model. The Vegas numbers are the "
        f"closing line from nflverse, and the Vegas win % is the moneyline with the vig taken out.",
        "",
        "Each cell is model / Vegas, and lower is better for MAE and Brier. For reference, my "
        "margin MAE over the 2023-2025 test seasons was 10.17 and Vegas was 9.74. I don't think a "
        "couple of weeks says much of anything yet, so I'm treating this as a running tally.",
        "",
        "| Games | n | Straight up | Margin MAE | Brier | Total MAE | Closer than Vegas |",
        "|---|---|---|---|---|---|---|",
    ]
    pre = df[df['pre_registered']]
    lines += summary_rows("Pre-registered only", summarize(pre)) if len(pre) else []
    lines += summary_rows("All graded games", summarize(df))
    for week, wk in df.groupby('file_week'):
        tag = '' if wk['pre_registered'].all() else ' (not pre-registered)'
        lines += summary_rows(f"Week {week}{tag}", summarize(wk))

    lines += [
        "",
        "Pre-registered means I committed that week's file before the game kicked off. I pushed "
        "the Week 2 file after its games were already played, so I'm still grading it to keep the "
        "record complete, but it doesn't count toward the top row.",
    ]

    for week, wk in df.groupby('file_week'):
        committed = wk['committed_at'].iloc[0]
        lines += [
            "",
            f"## Week {week}",
            "",
            f"File first committed {committed:%Y-%m-%d %H:%M %Z}." if committed is not None else "File not committed yet.",
            "",
            "| Game | Final | Model margin | Vegas line | Result | Model err | Vegas err | Model win % | Vegas win % | SU pick |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for _, g in wk.sort_values('kickoff').iterrows():
            final = f"{g['away_team']} {int(g['away_score'])} - {int(g['home_score'])} {g['home_team']}"
            pick = g['home_team'] if g['pred_margin'] > 0 else g['away_team']
            mark = 'yes' if g['model_correct'] else 'no'
            lines.append(
                f"| {g['away_team']} @ {g['home_team']} | {final} | {g['pred_margin']:+.1f} | "
                f"{g['spread_line']:+.1f} | {g['result']:+.0f} | {g['model_margin_err']:.1f} | "
                f"{g['vegas_margin_err']:.1f} | {g['pred_home_wp']:.1%} | {g['vegas_home_wp']:.1%} | "
                f"{pick} ({mark}) |")
    lines += ["", "Margins, lines, and win % are all from the home team's side, so +3.0 means "
                  "the home team by 3."]
    return "\n".join(lines) + "\n"


if __name__ == '__main__':
    # usage: python scorecard.py [season] [--save]
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    season = int(args[0]) if args else 2026
    df = load_graded(season)
    text = format_scorecard(season, df)
    print(text)
    if '--save' in sys.argv:
        path = os.path.join(PRED_DIR, f'{season}-scorecard.md')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("SAVED TO:", path)
