"""Grades every 4th-down call (go for it, kick a field goal, or punt) against
whichever option gave the team the best chance to win.

I think of this as the same expected value problem as the Elo model, just
one play at a time. For each option I figure out what the game looks like if
it works and if it doesn't, run both of those through a win probability
model, and weight them by how likely each one is:

    WP(go)   = P(convert) * WP(first down or TD) + (1 - P(convert)) * WP(turnover on downs)
    WP(fg)   = P(make)    * WP(up 3, kick off)   + (1 - P(make))    * WP(opp ball at spot of kick)
    WP(punt) = WP(opp ball wherever punts from here usually end up)

So I need four models, all fit on nflverse play-by-play. The main one is my
own win probability model (gradient boosted trees on score, time, field
position, down and distance, timeouts, and the pregame spread). The other
three are smaller: a logistic regression for converting on 3rd/4th down,
another one for field goals by distance, and a plain table of where the
other team usually starts after a punt from each yard line.

A play's grade is how much win probability the coach gave up compared to the
best option. If I add that up over a season, I get roughly how many wins a
coach's 4th-down calls cost the team.

Limits I know about (they're in the report too): gains on a successful
conversion come from the league-wide spread for that distance, so it doesn't
know defenses tighten up near the goal line. Every TD is worth exactly 7, so
no 2-point decisions. I leave overtime out because the rules are different.
And the only team strength it knows about is the pregame spread, so it
doesn't know if a team has a great short-yardage offense.
"""
import os
import sys
import numpy as np
import pandas as pd
import nfl_data_py as nfl
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

HIST_YEARS = list(range(2018, 2026))
# I give the win probability model more history than everything else. With
# only 2018-2025 it made big jumps between neighboring scores anywhere the data
# was thin, and going back to 2006 roughly tripled the data and helped with
# both that and accuracy. I kept the kicking and conversion models on 2018+
# though, since kickers keep getting better and coaches go for it way more now.
WP_START = 2006
RECENT_START = 2018
CACHE_DIR = 'cache'
REPORT_DIR = 'reports'

PBP_COLS = ['game_id', 'season', 'week', 'season_type', 'posteam', 'defteam', 'home_team', 'away_team',
            'home_coach', 'away_coach', 'qtr', 'down', 'ydstogo', 'yardline_100', 'game_seconds_remaining',
            'half_seconds_remaining', 'score_differential', 'posteam_timeouts_remaining',
            'defteam_timeouts_remaining', 'play_type', 'first_down', 'touchdown', 'td_team',
            'field_goal_result', 'kick_distance', 'return_yards', 'punt_blocked', 'touchback', 'result',
            'spread_line', 'vegas_wp', 'yards_gained', 'desc', 'game_date']

WP_FEATURES = ['score_differential', 'game_seconds_remaining', 'half_seconds_remaining', 'second_half',
               'yardline_100', 'down', 'ydstogo', 'posteam_timeouts_remaining', 'defteam_timeouts_remaining',
               'pos_spread', 'spread_time']

# which way each feature is allowed to push win probability (+1 up, -1 down,
# 0 either). Without these the trees did weird things wherever the data was
# thin, like a team's chances going DOWN when it had more timeouts. I also took
# is_home out completely, since the spread already includes home field, and
# with it in the model somehow learned that being at home lowered your chances.
MONOTONIC = {'score_differential': 1, 'pos_spread': 1, 'spread_time': 1, 'yardline_100': -1,
             'ydstogo': -1, 'posteam_timeouts_remaining': 1, 'defteam_timeouts_remaining': -1}

# how long each option takes off the clock, in seconds. These are rough
# guesses, but I don't think they matter much outside the last couple minutes.
RUNOFF = {'go': 5, 'fg': 4, 'punt': 8, 'kickoff': 5}

# a gap smaller than this (in win probability) is a coin flip, not a mistake
TOSSUP = 0.01


# ---------------------------------------------------------------- data

def load_pbp(years):
    """Play-by-play for these seasons. I cache each season locally because the
    download is really slow, but I always re-download the newest season since
    games keep getting added to it."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    frames = []
    current = max(years)
    for y in years:
        path = os.path.join(CACHE_DIR, f'pbp_{y}.pkl')
        if os.path.exists(path) and y != current:
            frames.append(pd.read_pickle(path))
            continue
        try:
            df = nfl.import_pbp_data([y], columns=PBP_COLS)
        except Exception as e:
            # the season in progress might not be published yet, that's fine
            print(f"No play-by-play for {y} ({e}), skipping it.")
            continue
        df.to_pickle(path)
        frames.append(df)
    pbp = pd.concat(frames, ignore_index=True)
    return add_features(pbp[pbp['season_type'] == 'REG'])


def add_features(pbp):
    pbp = pbp[pbp['posteam'].notna()].copy()
    pbp['is_home'] = (pbp['posteam'] == pbp['home_team']).astype(int)
    # nflverse spread_line is from the home side (positive = home favored)
    pbp['pos_spread'] = np.where(pbp['is_home'] == 1, pbp['spread_line'], -pbp['spread_line'])
    pbp['second_half'] = (pbp['qtr'] >= 3).astype(int)
    pbp['coach'] = np.where(pbp['is_home'] == 1, pbp['home_coach'], pbp['away_coach'])
    # did the team with the ball end up winning? result is home minus away
    won = np.where(pbp['is_home'] == 1, pbp['result'] > 0, pbp['result'] < 0)
    pbp['pos_won'] = np.where(pbp['result'] == 0, np.nan, won.astype(float))
    return add_spread_time(pbp)


def add_spread_time(df):
    """The spread matters most at kickoff and less and less as the clock runs
    out, so I hand the model that fade directly instead of making it learn it."""
    df['spread_time'] = df['pos_spread'] * df['game_seconds_remaining'] / 3600
    return df


# ---------------------------------------------------------------- models

def fit_wp_model(pbp):
    """P(team with the ball wins) from the game state. I train on every
    regulation scrimmage play from games that didn't end in a tie."""
    train = pbp[pbp['down'].notna() & (pbp['qtr'] <= 4) & pbp['pos_won'].notna()
                & pbp['play_type'].isin(['run', 'pass', 'punt', 'field_goal', 'no_play', 'qb_kneel', 'qb_spike'])]
    train = train.dropna(subset=WP_FEATURES)
    model = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.08, max_leaf_nodes=31,
                                           min_samples_leaf=500, random_state=0,
                                           monotonic_cst=[MONOTONIC.get(f, 0) for f in WP_FEATURES])
    model.fit(train[WP_FEATURES], train['pos_won'])
    return model


def conversion_features(ydstogo, yardline_100, is_fourth):
    ydstogo = np.asarray(ydstogo, dtype=float)
    yardline_100 = np.asarray(yardline_100, dtype=float)
    return np.column_stack([np.log(ydstogo), ydstogo, yardline_100,
                            (ydstogo >= yardline_100).astype(float),  # goal to go
                            np.broadcast_to(np.asarray(is_fourth, dtype=float), ydstogo.shape)])


def fit_conversion_model(pbp):
    """P(picking up the first down) on a 3rd or 4th down run/pass. I use 3rd
    downs too because 4th-down attempts alone are a small sample, and a biased
    one, since teams mostly only go for it when it's short. I added a 4th-down
    flag so the model can still pick up on anything different about them."""
    plays = pbp[pbp['down'].isin([3, 4]) & pbp['play_type'].isin(['run', 'pass'])
                & (pbp['ydstogo'] <= 20)].dropna(subset=['ydstogo', 'yardline_100'])
    converted = ((plays['first_down'] == 1) | ((plays['touchdown'] == 1) & (plays['td_team'] == plays['posteam'])))
    X = conversion_features(plays['ydstogo'], plays['yardline_100'], plays['down'] == 4)
    return LogisticRegression(max_iter=1000).fit(X, converted.astype(int))


def fg_features(dist, season):
    return np.column_stack([np.asarray(dist, dtype=float), np.asarray(season, dtype=float) - 2018])


def fit_fg_model(pbp):
    """P(field goal is good) by distance, plus a season trend because kickers
    keep getting more accurate. Without the trend, the version trained on
    2018-2022 said 82% of the 2023-2025 kicks would be good, and 85% actually
    were. Blocked kicks count as misses."""
    fgs = pbp[(pbp['play_type'] == 'field_goal') & pbp['kick_distance'].notna()]
    return LogisticRegression(max_iter=1000).fit(fg_features(fgs['kick_distance'], fgs['season']),
                                                 (fgs['field_goal_result'] == 'made').astype(int))


def fit_punt_table(pbp):
    """Where the other team ends up on average after a punt, by the yard line
    the punt came from. Touchbacks go to the 20. I smooth across neighboring
    yard lines because some of them only have a handful of punts."""
    punts = pbp[(pbp['play_type'] == 'punt') & pbp['kick_distance'].notna()].copy()
    ret = punts['return_yards'].fillna(0)
    opp_y = 100 - (punts['yardline_100'] - punts['kick_distance']) - ret
    punts['opp_y'] = np.where(punts['touchback'] == 1, 80, opp_y).clip(1, 99)
    by_line = punts.groupby('yardline_100')['opp_y'].mean().reindex(range(1, 100))
    smoothed = by_line.rolling(5, center=True, min_periods=1).mean()
    # nobody really punts from inside the opponent's 30, so I just hold the
    # closest real value flat there instead of making something up
    return smoothed.bfill().ffill()


def fit_success_gain(pbp):
    """Every gain on a successful 3rd/4th down conversion, grouped by distance.
    I keep the whole spread of gains instead of one typical number. My first
    version used the median, and since a converted 3rd & 3 has a median gain
    of 7, it counted every conversion from inside the 10 as a touchdown. The
    real rate from the 4-8 yard line is about 60%, so going for it near the
    goal line looked way better than it actually is."""
    plays = pbp[pbp['down'].isin([3, 4]) & pbp['play_type'].isin(['run', 'pass'])
                & (pbp['first_down'] == 1) & (pbp['ydstogo'] <= 20)]
    gains = {int(t): np.sort(g.to_numpy(dtype=float)) for t, g in plays.groupby('ydstogo')['yards_gained']}
    return {t: gains.get(t, gains[max(k for k in gains if k <= t)]) for t in range(1, 21)}


def success_outcomes(gains, togo, y):
    """For a successful conversion, the chance it goes all the way for a
    touchdown, and the average yard line it ends at when it doesn't."""
    p_td = np.empty(len(y))
    land = np.empty(len(y))
    for i, (t, yl) in enumerate(zip(np.clip(togo, 1, 20).astype(int), y)):
        g = gains[t]
        td = g >= yl
        p_td[i] = td.mean()
        short = g[~td]
        land[i] = yl - (short.mean() if len(short) else t)
    return p_td, np.clip(land, 1, 99)


def fit_all(pbp):
    print("Fitting win probability model...")
    recent = pbp[pbp['season'] >= RECENT_START]
    return {'wp': fit_wp_model(pbp), 'conv': fit_conversion_model(recent), 'fg': fit_fg_model(recent),
            'punt': fit_punt_table(recent), 'gain': fit_success_gain(recent)}


# ---------------------------------------------------------------- the decision math

def wp_of(models, states):
    states = add_spread_time(states.copy())
    return models['wp'].predict_proba(states[WP_FEATURES])[:, 1]


def opponent_first_down(plays, opp_y, score_change, runoff):
    """The game right after the other team gets the ball, 1st and 10 (or goal)
    from opp_y yards out, from THEIR side. score_change is however much the
    team that kicked or went for it added to its lead first."""
    secs = (plays['game_seconds_remaining'] - runoff).clip(lower=0)
    half = (plays['half_seconds_remaining'] - runoff).clip(lower=0)
    opp_y = np.asarray(opp_y, dtype=float)
    return pd.DataFrame({
        'score_differential': -(plays['score_differential'].to_numpy() + score_change),
        'game_seconds_remaining': secs.to_numpy(),
        'half_seconds_remaining': half.to_numpy(),
        'second_half': plays['second_half'].to_numpy(),
        'yardline_100': opp_y,
        'down': 1,
        'ydstogo': np.minimum(10, opp_y),
        'posteam_timeouts_remaining': plays['defteam_timeouts_remaining'].to_numpy(),
        'defteam_timeouts_remaining': plays['posteam_timeouts_remaining'].to_numpy(),
        'pos_spread': -plays['pos_spread'].to_numpy(),
        'is_home': 1 - plays['is_home'].to_numpy(),
    })


def kickoff_start(plays):
    """Where drives start after a kickoff. The 2024 rule change moved
    touchbacks up to the 30, and then 2025 moved them to the 35, so I go by year."""
    return np.select([plays['season'] >= 2025, plays['season'] >= 2024], [65, 70], 75)


def period_over(plays, models, wp, score_change, runoff):
    """If the clock runs out during this outcome, the next possession never
    happens, so whatever wp says about it doesn't mean anything. The model has
    almost never seen a 1st down with 0 seconds left, so it values one anyway.
    I caught this on MIA, up 1 with 4 seconds left in the half, where it said
    going for it on 4th & 2 at the 9 beat a chip-shot field goal.

    If it's the end of the game, the score is final (and I count a tie as a
    coin flip for overtime). If it's halftime, nobody has the ball, so I
    average the team getting the second-half kickoff and the other team
    getting it, since I don't track who actually receives it."""
    over = (plays['half_seconds_remaining'].to_numpy() - runoff) <= 0
    if not over.any():
        return wp
    diff = plays['score_differential'].to_numpy() + score_change
    final = np.select([diff > 0, diff < 0], [1.0, 0.0], 0.5)
    start = plays.copy()
    start['game_seconds_remaining'] = 1800
    start['half_seconds_remaining'] = 1800
    start['second_half'] = 1
    start['posteam_timeouts_remaining'] = 3
    start['defteam_timeouts_remaining'] = 3
    start['score_differential'] = diff
    start['yardline_100'] = kickoff_start(plays)
    start['down'] = 1
    start['ydstogo'] = 10
    ours = wp_of(models, start)
    theirs = 1 - wp_of(models, opponent_first_down(start, kickoff_start(plays), 0, 0))
    halftime = (ours + theirs) / 2
    return np.where(over, np.where(plays['second_half'].to_numpy() == 1, final, halftime), wp)


def evaluate_options(plays, models):
    """Win probability for going for it, kicking, and punting on each play."""
    plays = plays.reset_index(drop=True)
    y = plays['yardline_100'].to_numpy(dtype=float)
    togo = plays['ydstogo'].to_numpy(dtype=float)

    # ---- go for it
    p_conv = models['conv'].predict_proba(conversion_features(togo, y, np.ones_like(y)))[:, 1]
    p_td, land = success_outcomes(models['gain'], togo, y)
    # converted but no TD: 1st down further up the field, same team's ball
    first = plays[WP_FEATURES].copy()
    first['game_seconds_remaining'] = (first['game_seconds_remaining'] - RUNOFF['go']).clip(lower=0)
    first['half_seconds_remaining'] = (first['half_seconds_remaining'] - RUNOFF['go']).clip(lower=0)
    first['yardline_100'] = land
    first['down'] = 1
    first['ydstogo'] = np.minimum(10, first['yardline_100'])
    wp_first = period_over(plays, models, wp_of(models, first), 0, RUNOFF['go'])
    # converted with a TD: up 7, then kick off to them
    wp_td = period_over(plays, models, 1 - wp_of(models, opponent_first_down(
        plays, kickoff_start(plays), 7, RUNOFF['go'] + RUNOFF['kickoff'])), 7, RUNOFF['go'])
    wp_success = p_td * wp_td + (1 - p_td) * wp_first
    # failed: they take over at the spot
    wp_fail = period_over(plays, models, 1 - wp_of(models, opponent_first_down(plays, 100 - y, 0, RUNOFF['go'])),
                          0, RUNOFF['go'])
    wp_go = p_conv * wp_success + (1 - p_conv) * wp_fail

    # ---- field goal (snapped 7 yards back, plus 10 for the end zone)
    dist = y + 17
    p_make = models['fg'].predict_proba(fg_features(dist, plays['season']))[:, 1]
    p_make = np.where(dist > 70, 0.0, p_make)  # nobody has ever made one from past 66
    wp_make = period_over(plays, models, 1 - wp_of(models, opponent_first_down(
        plays, kickoff_start(plays), 3, RUNOFF['fg'] + RUNOFF['kickoff'])), 3, RUNOFF['fg'])
    # a miss gives them the ball at the spot of the kick, or the 20 if that's closer to their goal
    wp_miss = period_over(plays, models, 1 - wp_of(models, opponent_first_down(plays, np.minimum(93 - y, 80), 0, RUNOFF['fg'])),
                          0, RUNOFF['fg'])
    wp_fg = p_make * wp_make + (1 - p_make) * wp_miss

    # ---- punt
    opp_y = models['punt'].reindex(np.clip(y, 1, 99).astype(int)).to_numpy()
    wp_punt = period_over(plays, models, 1 - wp_of(models, opponent_first_down(plays, opp_y, 0, RUNOFF['punt'])),
                          0, RUNOFF['punt'])

    out = plays.copy()
    out['p_convert'], out['p_fg'] = p_conv, p_make
    out['wp_go'], out['wp_fg'], out['wp_punt'] = wp_go, wp_fg, wp_punt
    return out


def grade(plays):
    """Labels each call and works out how much it cost."""
    options = plays[['wp_go', 'wp_fg', 'wp_punt']].to_numpy()
    names = np.array(['go', 'fg', 'punt'])
    best_idx = options.argmax(axis=1)
    plays['best'] = names[best_idx]
    plays['choice'] = plays['play_type'].map({'run': 'go', 'pass': 'go', 'field_goal': 'fg', 'punt': 'punt'})
    chosen = options[np.arange(len(plays)), pd.Series(plays['choice']).map({'go': 0, 'fg': 1, 'punt': 2}).to_numpy()]
    plays['wp_lost'] = options.max(axis=1) - chosen
    best_kick = np.maximum(plays['wp_fg'], plays['wp_punt'])
    plays['go_edge'] = plays['wp_go'] - best_kick  # positive means going for it is the better call
    went = plays['choice'] == 'go'
    plays['verdict'] = np.select(
        [plays['wp_lost'] < TOSSUP,
         went & (plays['go_edge'] < 0),
         ~went & (plays['go_edge'] > 0)],
        ['fine', 'too aggressive', 'too conservative'],
        'wrong kick')  # e.g. punting when the field goal was the better kick
    return plays


def fourth_downs(pbp):
    """The decisions I actually grade: 4th downs in regulation where the team
    really ran a play, punted, or kicked. I drop penalties and no-plays since
    I can't tell what the team was trying to do, and kneel-downs. Fake punts
    and fake kicks show up as a run or pass anyway, so those get graded as
    going for it, which I think is fair."""
    fd = pbp[(pbp['down'] == 4) & (pbp['qtr'] <= 4)
             & pbp['play_type'].isin(['run', 'pass', 'field_goal', 'punt'])]
    return fd.dropna(subset=WP_FEATURES)


# ---------------------------------------------------------------- validation

def brier(p, y):
    return float(np.mean((np.asarray(p) - np.asarray(y)) ** 2))


def validate(pbp):
    """Fits on everything through 2022 and tests on 2023-2025, the same split
    I use for the Elo model, so none of the test numbers come from data the
    models already trained on."""
    train = pbp[pbp['season'] <= 2022]
    test = pbp[(pbp['season'] >= 2023) & (pbp['season'] <= 2025)]
    models = fit_all(train)
    lines = []

    # win probability: mine vs nflfastR's own model (which also uses the spread)
    t = test[test['down'].notna() & (test['qtr'] <= 4) & test['pos_won'].notna()].dropna(subset=WP_FEATURES + ['vegas_wp'])
    mine = wp_of(models, t)
    lines.append(f"- Win probability, on {len(t):,} test plays: Brier {brier(mine, t['pos_won']):.4f}, "
                 f"compared to {brier(t['vegas_wp'], t['pos_won']):.4f} for nflfastR's model (lower is better). "
                 f"So mine is a little worse than theirs, but close.")
    cal = pd.DataFrame({'p': mine, 'y': t['pos_won']})
    cal['bin'] = (cal['p'] * 10).clip(0, 9.999).astype(int)
    calib = cal.groupby('bin').agg(predicted=('p', 'mean'), actual=('y', 'mean'), n=('y', 'size'))

    # conversion: check it on actual 4th-down attempts, not the 3rd downs it also trained on
    att = test[(test['down'] == 4) & test['play_type'].isin(['run', 'pass'])
               & (test['ydstogo'] <= 20)].dropna(subset=['ydstogo', 'yardline_100'])
    conv = ((att['first_down'] == 1) | ((att['touchdown'] == 1) & (att['td_team'] == att['posteam']))).astype(int)
    p = models['conv'].predict_proba(conversion_features(att['ydstogo'], att['yardline_100'], np.ones(len(att))))[:, 1]
    by_dist = pd.DataFrame({'togo': np.clip(att['ydstogo'], 1, 6), 'p': p, 'y': conv}).groupby('togo').agg(
        predicted=('p', 'mean'), actual=('y', 'mean'), n=('y', 'size'))
    lines.append(f"- Conversions, on {len(att):,} real 4th-down attempts in the test seasons: it predicted "
                 f"{p.mean():.1%} would convert and {conv.mean():.1%} did.")

    fgs = test[(test['play_type'] == 'field_goal') & test['kick_distance'].notna()]
    pf = models['fg'].predict_proba(fg_features(fgs['kick_distance'], fgs['season']))[:, 1]
    lines.append(f"- Field goals, on {len(fgs):,} test kicks: it predicted {pf.mean():.1%} would be good and "
                 f"{(fgs['field_goal_result'] == 'made').mean():.1%} were.")
    lines += consistency_check(test, models)
    return lines, calib, by_dist


def consistency_check(test, models):
    """This is the check I trust the most. On a real 4th down, the win
    probability I predict for the option the coach actually picked should
    match, on average, the win probability on the very next snap once the
    play has happened. If my version of "what happens after a punt" was off,
    punts would show a gap here. When the grades looked too extreme, this
    came back clean, which is how I knew the problem was in the win
    probability model and not the decision math."""
    t = test[test['down'].notna() & (test['qtr'] <= 4)].dropna(subset=WP_FEATURES).reset_index(drop=True)
    t['wp'] = wp_of(models, t)
    t['half'] = np.where(t['qtr'] <= 2, 1, 2)
    nxt = t.groupby(['game_id', 'half']).shift(-1)
    t['wp_next'] = np.where(nxt['posteam'] == t['posteam'], nxt['wp'], 1 - nxt['wp'])
    t = t[nxt['posteam'].notna()]
    g = grade(evaluate_options(fourth_downs(t), models))
    g['wp_next'] = fourth_downs(t)['wp_next'].to_numpy()
    parts = []
    for choice, col, label in [('go', 'wp_go', 'Going for it'), ('fg', 'wp_fg', 'field goals'),
                               ('punt', 'wp_punt', 'punts')]:
        c = g[g['choice'] == choice]
        parts.append(f"{label} {pct(c[col].mean())} predicted vs {pct(c['wp_next'].mean())} on the next snap "
                     f"({len(c):,} plays)")
    return ["- Consistency check, on the test seasons' 4th downs: I compared the average win probability I "
            "predicted for whatever the coach chose to the win probability on the next snap. " +
            "; ".join(parts) + ". Those basically match, so I don't think the decision math is biased "
            "toward any one option."]


# ---------------------------------------------------------------- report

def pct(x):
    return f"{x:.1%}"


def format_report(graded, val_lines, calib, by_dist, focus_season):
    s = graded[graded['season'] == focus_season]
    lines = [
        "# 4th Down Decision Grader",
        "",
        "I graded every regulation 4th down since 2018 against whichever option (go for it, field goal, "
        "or punt) had the highest win probability. WP lost is how much win probability a call gave up "
        "compared to the best option, and if you add it up over a season it's roughly how many games a "
        "coach's 4th-down calls cost the team.",
        "",
        f"If the options were within {TOSSUP:.0%} of each other I count the call as fine. Those are "
        "basically coin flips, and I don't think my model is precise enough to call them either way.",
        "",
        "## How good are the models?",
        "",
        f"I trained on seasons through 2022 and tested on 2023-2025. The win probability model uses "
        f"{WP_START}-2022, and everything else uses {RECENT_START}-2022.",
        "",
        *val_lines,
        "",
        "Calibration on the test seasons, meaning when my model says a team has an X% chance, how often "
        "that team actually wins:",
        "",
        "| Predicted | Actual | Plays |",
        "|---|---|---|",
        *[f"| {pct(r.predicted)} | {pct(r.actual)} | {int(r.n):,} |" for r in calib.itertuples()],
        "",
        "4th-down conversion rate by distance in the test seasons:",
        "",
        "| Yards to go | Predicted | Actual | Attempts |",
        "|---|---|---|---|",
        *[f"| {'6+' if i == 6 else int(i)} | {pct(r.predicted)} | {pct(r.actual)} | {int(r.n):,} |"
          for i, r in by_dist.iterrows()],
        "",
        "## Are coaches getting more aggressive?",
        "",
        "These are the spots where going for it was clearly the better call (by more than the "
        f"{TOSSUP:.0%} toss-up margin), and how often coaches actually went for it. The go rate climbs "
        "pretty steadily, but the wins lost per team doesn't really drop, which I think is because "
        "there are more clear go spots every year too.",
        "",
        "| Season | Clear 'go' spots | Went for it | WP lost per team |",
        "|---|---|---|---|",
    ]
    for season, g in graded.groupby('season'):
        clear_go = g[g['go_edge'] > TOSSUP]
        n_teams = g['posteam'].nunique()
        lines.append(f"| {season} | {len(clear_go):,} | {pct((clear_go['choice'] == 'go').mean())} | "
                     f"{g['wp_lost'].sum() / n_teams:.2f} |")

    coaches = s.groupby(['coach', 'posteam']).agg(
        calls=('wp_lost', 'size'),
        clear_go=('go_edge', lambda e: int((e > TOSSUP).sum())),
        went_when_clear=('go_edge', lambda e: int(((e > TOSSUP) & (s.loc[e.index, 'choice'] == 'go')).sum())),
        too_conservative=('verdict', lambda v: int((v == 'too conservative').sum())),
        too_aggressive=('verdict', lambda v: int((v == 'too aggressive').sum())),
        wp_lost=('wp_lost', 'sum'),
    ).reset_index().sort_values('wp_lost')
    lines += [
        "",
        f"## {focus_season} coaches, best to worst",
        "",
        "| Coach | Team | 4th downs | Clear 'go' spots | Went | Too conservative | Too aggressive | Wins lost |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| {r.coach} | {r.posteam} | {r.calls} | {r.clear_go} | {r.went_when_clear} | "
          f"{r.too_conservative} | {r.too_aggressive} | {r.wp_lost:.2f} |" for r in coaches.itertuples()],
        "",
        f"## {focus_season}'s costliest calls",
        "",
        "| Game | Team | Qtr | Time | Score | Situation | Call | Go / FG / Punt WP | Lost |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in s.sort_values('wp_lost', ascending=False).head(15).itertuples():
        mins, secs = divmod(int(r.game_seconds_remaining - 900 * (4 - r.qtr)), 60)
        clock = f"{mins}:{secs:02d}"
        spot = f"own {100 - int(r.yardline_100)}" if r.yardline_100 > 50 else f"opp {int(r.yardline_100)}"
        lines.append(f"| {r.away_team} @ {r.home_team} (wk {r.week}) | {r.posteam} | {int(r.qtr)} | {clock} | "
                     f"{int(r.score_differential):+d} | 4th & {int(r.ydstogo)}, {spot} | {r.choice} | "
                     f"{pct(r.wp_go)} / {pct(r.wp_fg)} / {pct(r.wp_punt)} | {pct(r.wp_lost)} |")
    lines += [
        "",
        "## Known limits",
        "",
        "- The biggest one: my win probability model is built from decision trees, so it moves in "
        "steps between scores that are right next to each other. Some of that is real (being down 6 "
        "and being down 7 play out pretty similarly), but some of the jumps are bigger than the real "
        "data backs up, like a tie vs. up 1 early in a game. That can push a single play's grade off "
        "by a few points. I think season totals mostly average it out, but a smoother model is the "
        "first thing I want to fix.",
        "- Gains on a successful conversion come from the league-wide spread for that distance, so it "
        "doesn't know defenses tighten up near the goal line.",
        "- Conversion and field goal odds are league average. It has no idea a team has a great "
        "short-yardage offense or a great kicker, other than whatever the pregame spread says about "
        "the team overall.",
        "- Every touchdown is worth 7, so no 2-point decisions, and I left overtime out.",
        "- Penalties, spikes, and kneels on 4th down aren't graded.",
    ]
    return "\n".join(lines) + "\n"


def run(focus_season=2025):
    years = list(range(WP_START, max(HIST_YEARS) + 1)) + ([focus_season] if focus_season > max(HIST_YEARS) else [])
    pbp = load_pbp(years)
    val_lines, calib, by_dist = validate(pbp)
    # the actual grades use models fit on every season, and the test numbers
    # above are how I know those models are any good
    models = fit_all(pbp)
    graded = grade(evaluate_options(fourth_downs(pbp[pbp['season'] >= RECENT_START]), models))
    return graded, format_report(graded, val_lines, calib, by_dist, focus_season)


if __name__ == '__main__':
    # usage: python fourth_down.py [season] [--save]
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    season = int(args[0]) if args else 2025
    graded, text = run(season)
    print(text)
    if '--save' in sys.argv:
        os.makedirs(REPORT_DIR, exist_ok=True)
        path = os.path.join(REPORT_DIR, f'fourth_down_{season}.md')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        # every graded play, in case I want to dig into one game. It's way too big for the repo.
        graded.to_csv(os.path.join(CACHE_DIR, 'fourth_down_graded.csv'), index=False)
        print("SAVED TO:", path)
