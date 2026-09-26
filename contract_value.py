"""Which players are actually worth their contracts?

I set this up the same way you'd price an asset. First I figure out what the
open market pays for production at each position, then for every player I
compare what their production would cost on that market to what their team
is really paying them. The difference is surplus value, so positive means a
bargain and negative means overpaid.

For production I use EPA above replacement, which is a player's total EPA
(passing, rushing, and receiving) minus what a backup would have put up on
the same number of plays. That's what lets me compare a 600-dropback QB to a
90-target TE, since both are just "points added over a guy you could sign
off the street."

For pay I use the contract's average per year as a share of the salary cap
when it was signed. The cap went up about 60% from 2018 to 2025, so raw
dollars would make every old deal look cheap.

The market price comes from ranks. If a player is the 10th most productive
WR that season, I say their production is worth what the 10th highest-paid
veteran WR makes that season. Anything at or below replacement is worth the
league minimum, since that's basically the definition of replacement level.
Only veteran deals go into the pay ladder, because rookie deals are set by
draft slot and not by the market, but rookies still get graded against it.

My first version fit a curve of pay against production instead, and it said
a replacement-level WR was worth $10.9M, which made every minimum-salary
rookie look like a $13M bargain. I'm pretty sure the problem is that
production is really noisy (a WR's EPA per play only correlates 0.23 from
one year to the next) and teams pay for what they EXPECT, so pay barely
follows any one season and the curve comes out flat with a high floor. Ranks
don't have that problem, and since every season gets its own ladder, it also
keeps up if the market for a position changes.

I only do QB, RB, WR, and TE. Public play-by-play doesn't have a fair
per-player stat for linemen or defenders, and I'd rather leave them out than
grade them on something I made up.
"""
import os
import sys
import numpy as np
import pandas as pd
import nfl_data_py as nfl

YEARS = list(range(2018, 2026))
CACHE_DIR = 'cache'
REPORT_DIR = 'reports'
POSITIONS = ['QB', 'RB', 'WR', 'TE']

# salary cap by season, in $M, so a cap share can be turned back into dollars
CAP = {2018: 177.2, 2019: 188.2, 2020: 198.2, 2021: 182.5, 2022: 208.2, 2023: 224.8,
       2024: 255.4, 2025: 279.2}

# league minimum salary for a rookie, in $M. The contract data has some weird
# tiny deals below this (I'm assuming practice squad stuff), so I floor at the
# real minimum instead of trusting the bottom of the pay ladder.
MIN_SALARY = {2018: 0.48, 2019: 0.495, 2020: 0.61, 2021: 0.66, 2022: 0.705, 2023: 0.75,
              2024: 0.795, 2025: 0.84}

# how many players at each position I count as "starters" in a season, which
# is 1 QB per team, about 1.5 RBs, 3 WRs, and 1.5 TEs. Everyone below that line
# (by volume) is who sets replacement level.
STARTERS = {'QB': 32, 'RB': 48, 'WR': 96, 'TE': 48}

# with too few plays the EPA is mostly noise. This is roughly 4-5 games as a starter.
MIN_PLAYS = {'QB': 150, 'RB': 80, 'WR': 40, 'TE': 30}

PBP_COLS = ['game_id', 'play_id', 'season', 'season_type', 'play_type', 'passer_player_id',
            'passer_player_name', 'rusher_player_id', 'rusher_player_name', 'receiver_player_id',
            'receiver_player_name', 'epa', 'qb_epa', 'pass_attempt', 'rush_attempt']


# ---------------------------------------------------------------- data

def load_pbp(years):
    os.makedirs(CACHE_DIR, exist_ok=True)
    frames = []
    for y in years:
        path = os.path.join(CACHE_DIR, f'pbp_players_{y}.pkl')
        if os.path.exists(path):
            frames.append(pd.read_pickle(path))
            continue
        df = nfl.import_pbp_data([y], columns=PBP_COLS)
        df.to_pickle(path)
        frames.append(df)
    pbp = pd.concat(frames, ignore_index=True)
    return pbp[(pbp['season_type'] == 'REG') & pbp['epa'].notna()]


def player_production(pbp):
    """Total EPA and play count per player-season, across every role. A QB
    gets credit for every dropback, sacks included (I use qb_epa here so a QB
    doesn't get blamed when a receiver fumbles after the catch), plus their
    own runs and scrambles. A receiver gets the EPA of every pass thrown their
    way, caught or not, and a back gets credit for both runs and targets."""
    passing = pbp[pbp['pass_attempt'] == 1]
    roles = [
        passing[['season', 'passer_player_id', 'passer_player_name', 'qb_epa']].set_axis(
            ['season', 'gsis_id', 'name', 'epa'], axis=1),
        pbp[pbp['rush_attempt'] == 1][['season', 'rusher_player_id', 'rusher_player_name', 'epa']].set_axis(
            ['season', 'gsis_id', 'name', 'epa'], axis=1),
        passing[['season', 'receiver_player_id', 'receiver_player_name', 'epa']].set_axis(
            ['season', 'gsis_id', 'name', 'epa'], axis=1),
    ]
    credits = pd.concat(roles, ignore_index=True).dropna(subset=['gsis_id'])
    return credits.groupby(['season', 'gsis_id']).agg(
        name=('name', 'last'), plays=('epa', 'size'), epa=('epa', 'sum')).reset_index()


def load_contracts():
    c = nfl.import_contracts()
    c = c[c['gsis_id'].notna() & c['position'].isin(POSITIONS) & c['apy_cap_pct'].notna()].copy()
    c['years'] = c['years'].fillna(1).clip(lower=1)
    # a rookie deal is the one signed the same year the player was drafted.
    # Undrafted rookies sign for about the minimum, so I count those too.
    c['rookie_deal'] = (c['year_signed'] == c['draft_year']) | (c['draft_year'].isna() & (c['apy'] <= 1.2))
    return c


def contract_for_season(contracts, season):
    """The deal each player was playing under in a given season, which I take
    as the most recent one signed on or before that season that still has
    years left. One problem with this is that an extension signed during a
    season counts for that season, even if the new money doesn't start until
    the next year."""
    live = contracts[(contracts['year_signed'] <= season)
                     & (contracts['year_signed'] + contracts['years'] > season)]
    live = live.sort_values(['year_signed', 'apy']).groupby('gsis_id').tail(1).copy()
    live['season'] = season
    live['contract_year'] = season - live['year_signed'] + 1
    return live


# ---------------------------------------------------------------- the value math

def add_replacement(df):
    """EPA above replacement, per position and season. Replacement level is
    the EPA per play of everyone outside the top N by volume at that position
    (so basically the backups), weighted by how much each of them played."""
    out = []
    for (season, pos), g in df.groupby(['season', 'position']):
        g = g.sort_values('plays', ascending=False).copy()
        bench = g.iloc[STARTERS[pos]:]
        repl = bench['epa'].sum() / bench['plays'].sum() if len(bench) else 0.0
        g['repl_per_play'] = repl
        g['epar'] = g['epa'] - repl * g['plays']
        out.append(g)
    return pd.concat(out, ignore_index=True)


def build_table(years=YEARS):
    """Returns the player-season table, plus every contract in force each
    season, since that's what I build the pay ladders from."""
    prod = player_production(load_pbp(years))
    contracts = load_contracts()
    deals = pd.concat([contract_for_season(contracts, s) for s in years], ignore_index=True)
    df = prod.merge(deals[['season', 'gsis_id', 'player', 'position', 'team', 'year_signed', 'years', 'apy',
                           'apy_cap_pct', 'guaranteed', 'rookie_deal', 'contract_year']],
                    on=['season', 'gsis_id'], how='inner')
    # replacement level uses everyone who played, before the volume cutoff
    df = add_replacement(df)
    df = df[df['plays'] >= df['position'].map(MIN_PLAYS)].copy()
    print(f"{len(df):,} player-seasons with a matched contract (of {len(prod):,} with any plays).")
    return df, deals


def fit_market(deals):
    """The pay ladder, which is every veteran contract in force at a position
    that season sorted from highest cap share down, so index 0 is the
    highest-paid player."""
    vets = deals[~deals['rookie_deal']]
    return {key: np.sort(g['apy_cap_pct'].to_numpy())[::-1]
            for key, g in vets.groupby(['season', 'position'])}


def add_value(df, market):
    df = df.copy()
    df['prod_rank'] = df.groupby(['season', 'position'])['epar'].rank(ascending=False, method='first').astype(int)
    values = []
    for season, pos, rank, epar in zip(df['season'], df['position'], df['prod_rank'], df['epar']):
        ladder = market[(season, pos)]
        floor = MIN_SALARY[season] / CAP[season]
        values.append(floor if epar <= 0 or rank > len(ladder) else max(ladder[rank - 1], floor))
    df['market_cap_pct'] = values
    df['surplus_cap_pct'] = df['market_cap_pct'] - df['apy_cap_pct']
    df['surplus_m'] = df['surplus_cap_pct'] * df['season'].map(CAP)
    df['market_m'] = df['market_cap_pct'] * df['season'].map(CAP)
    df['paid_m'] = df['apy_cap_pct'] * df['season'].map(CAP)
    return df


def validate(df):
    """Does this season's production say anything about next season's? If a
    "bargain" is really just a lucky year, then surplus value is mostly noise
    and I shouldn't read the rankings as much more than a box score. So I
    check how well EPA above replacement per play carries over from one year
    to the next, and whether the same player's surplus does too."""
    rate = df.assign(rate=df['epar'] / df['plays'])[['gsis_id', 'season', 'position', 'rate']]
    nxt = rate.assign(season=rate['season'] - 1)
    pairs = rate.merge(nxt, on=['gsis_id', 'season', 'position'], suffixes=('', '_next'))
    sur = df[['gsis_id', 'season', 'surplus_m']]
    sur_pairs = sur.merge(sur.assign(season=sur['season'] - 1), on=['gsis_id', 'season'], suffixes=('', '_next'))
    pairs = pairs.merge(sur_pairs, on=['gsis_id', 'season'], how='left')
    return pairs.groupby('position').apply(
        lambda g: pd.Series({'pairs': len(g), 'corr': g['rate'].corr(g['rate_next']),
                             'surplus_corr': g['surplus_m'].corr(g['surplus_m_next'])}), include_groups=False)


# ---------------------------------------------------------------- report

def money(x):
    return f"-${-x:.1f}M" if x < 0 else f"${x:.1f}M"


def player_rows(g):
    return [f"| {r.player} | {r.team} | {r.plays} | {r.epar:+.1f} | {money(r.paid_m)} | {money(r.market_m)} | "
            f"{money(r.surplus_m)} | {'rookie' if r.rookie_deal else f'yr {r.contract_year} of {int(r.years)}'} |"
            for r in g.itertuples()]


HEADER = ["| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |",
          "|---|---|---|---|---|---|---|---|"]


def format_report(df, market, stability, season, top=10):
    s = df[df['season'] == season]
    lines = [
        "# Contract Value Analyzer",
        "",
        f"Who's outplaying their contract in {season} and who isn't. I only did QB, RB, WR, and TE, "
        "since public play-by-play doesn't have a fair per-player stat for linemen or defenders.",
        "",
        "How to read the tables: EPA over repl. is the expected points a player added above what a backup "
        "would have put up on the same number of plays. Paid is the contract's average per year as a share "
        f"of the cap when it was signed, turned into {season} dollars. Market value comes from ranks, so if "
        "a player was 10th in production at their position, it's what the 10th highest-paid veteran at "
        "that position makes (and the league minimum if they were at or below replacement). Surplus is "
        "market value minus pay, so positive means a bargain.",
        "",
        "## What the market pays",
        "",
        f"The {season} veteran pay ladder at each position, by average per year:",
        "",
        "| Position | Highest paid | 5th | 16th | 32nd | Minimum |",
        "|---|---|---|---|---|---|",
    ]
    for pos in POSITIONS:
        ladder = market[(season, pos)] * CAP[season]
        picks = [ladder[i] if i < len(ladder) else ladder[-1] for i in (0, 4, 15, 31)] + [MIN_SALARY[season]]
        lines.append(f"| {pos} | " + " | ".join(money(v) for v in picks) + " |")
    lines += [
        "",
        "## How much of this is luck?",
        "",
        "This is how much the same player's numbers carry over from one season to the next, 2018-2025. "
        "Close to 0 means a great year mostly doesn't repeat, so a big surplus is closer to a lucky season "
        "than a smart signing. QBs hold up the best, and for everyone else I'd take a single great season "
        "with a grain of salt.",
        "",
        "| Position | EPA over repl. per play | Surplus | Player pairs |",
        "|---|---|---|---|",
        *[f"| {pos} | {r['corr']:.2f} | {r['surplus_corr']:.2f} | {int(r['pairs'])} |"
          for pos, r in stability.iterrows()],
    ]
    for pos in POSITIONS:
        g = s[s['position'] == pos]
        lines += ["", f"## {season} {pos}s", "", "Best value:", "", *HEADER,
                  *player_rows(g.sort_values('surplus_m', ascending=False).head(top)),
                  "", "Most overpaid:", "", *HEADER,
                  *player_rows(g.sort_values('surplus_m').head(top))]
    vet = df[~df['rookie_deal'] & (df['years'] >= 3)]
    by_year = vet.groupby('contract_year').agg(players=('surplus_m', 'size'),
                                               surplus=('surplus_cap_pct', 'mean')).head(5)
    lines += [
        "",
        "## Do veteran deals age well?",
        "",
        f"Average surplus by year of the contract, for veteran deals of 3+ years, in {season} dollars. "
        "I expected this to get worse every year as players age, but it's negative from year 1 and just "
        "kind of stays there. My guess is that teams mostly overpay at signing (the market is paying for "
        "the season that earned the deal), not that deals fall apart later.",
        "",
        "| Contract year | Player-seasons | Average surplus |",
        "|---|---|---|",
        *[f"| {int(y)} | {int(r.players)} | {money(r.surplus * CAP[season])} |" for y, r in by_year.iterrows()],
        "",
        "## Known limits",
        "",
        "- Pay is the average per year, not the actual cap hit that season. Most deals are back-loaded, "
        "so early years really cost less than what's shown here and later years cost more.",
        "- An extension signed during a season counts for that season, even if the new money starts later.",
        "- A receiver gets credit for every pass thrown their way and a QB for every dropback, so a good "
        "QB and WR share credit for the same plays. That's part of why I only compare players to their "
        "own position.",
        "- EPA says nothing about blocking, which matters a lot for TEs and some RBs.",
        "- Rank pricing tells you what the Nth best producer would cost, not what that player will do "
        "next year, so a one-year spike still ranks high even if it won't repeat (see the luck table).",
        "- Players who missed games rank lower, since EPA over replacement is a season total. That's a "
        "big part of why Burrow and Murray show up as overpaid.",
    ]
    return "\n".join(lines) + "\n"


def query(df, season, pos=None, max_apy=None, min_apy=None, sort='surplus', top=15):
    """For questions like "best value QBs under $5M" or "most overpaid WRs"."""
    q = df[df['season'] == season]
    if pos:
        q = q[q['position'] == pos]
    if max_apy is not None:
        q = q[q['paid_m'] <= max_apy]
    if min_apy is not None:
        q = q[q['paid_m'] >= min_apy]
    q = q.sort_values('surplus_m', ascending=(sort == 'overpaid')).head(top)
    return "\n".join(HEADER + player_rows(q))


def run(season=2025):
    df, deals = build_table()
    market = fit_market(deals)
    return add_value(df, market), market


if __name__ == '__main__':
    # usage:
    #   python contract_value.py [season] [--save]                full report
    #   python contract_value.py 2025 --pos WR --overpaid          most overpaid WRs
    #   python contract_value.py 2025 --pos QB --max-apy 5         best value QBs under $5M
    args = sys.argv[1:]
    def opt(name):
        return args[args.index(name) + 1] if name in args else None
    positional = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or not args[i - 1].startswith('--'))]
    season = int(positional[0]) if positional else 2025

    df, market = run(season)
    if any(a in args for a in ('--pos', '--max-apy', '--min-apy', '--overpaid')):
        print(query(df, season, pos=opt('--pos'),
                    max_apy=float(opt('--max-apy')) if opt('--max-apy') else None,
                    min_apy=float(opt('--min-apy')) if opt('--min-apy') else None,
                    sort='overpaid' if '--overpaid' in args else 'surplus'))
    else:
        text = format_report(df, market, validate(df), season)
        print(text)
        if '--save' in args:
            os.makedirs(REPORT_DIR, exist_ok=True)
            path = os.path.join(REPORT_DIR, f'contract_value_{season}.md')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            print("SAVED TO:", path)
