from math import radians, sin, cos, asin, sqrt
import pandas as pd

# Stadium coordinates (lat, lon) for every team abbreviation seen in the
# 2018-2025 data. LV/OAK are the same franchise (relocated 2020), kept as
# separate entries since both abbreviations appear in the historical data.
STADIUM_COORDS = {
    'ARI': (33.5276, -112.2626), 'ATL': (33.7554, -84.4008), 'BAL': (39.2780, -76.6227),
    'BUF': (42.7738, -78.7870), 'CAR': (35.2258, -80.8528), 'CHI': (41.8623, -87.6167),
    'CIN': (39.0955, -84.5161), 'CLE': (41.5061, -81.6995), 'DAL': (32.7473, -97.0945),
    'DEN': (39.7439, -105.0201), 'DET': (42.3400, -83.0456), 'GB': (44.5013, -88.0622),
    'HOU': (29.6847, -95.4107), 'IND': (39.7601, -86.1639), 'JAX': (30.3239, -81.6373),
    'KC': (39.0489, -94.4839), 'LA': (33.9535, -118.3392), 'LAC': (33.9535, -118.3392),
    'LV': (36.0909, -115.1833), 'OAK': (37.7516, -122.2005), 'MIA': (25.9580, -80.2389),
    'MIN': (44.9738, -93.2575), 'NE': (42.0909, -71.2643), 'NO': (29.9511, -90.0812),
    'NYG': (40.8135, -74.0745), 'NYJ': (40.8135, -74.0745), 'PHI': (39.9008, -75.1675),
    'PIT': (40.4468, -80.0158), 'SEA': (47.5952, -122.3316), 'SF': (37.4032, -121.9698),
    'TB': (27.9759, -82.5033), 'TEN': (36.1665, -86.7713), 'WAS': (38.9078, -76.8645),
}


def haversine_miles(coord1, coord2):
    lat1, lon1, lat2, lon2 = map(radians, [*coord1, *coord2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 3956 * asin(sqrt(a))


def add_travel(df):
    df = df.copy()
    df['away_travel'] = df.apply(
        lambda row: haversine_miles(STADIUM_COORDS[row['away_team']], STADIUM_COORDS[row['home_team']]),
        axis=1)
    return df


# Hours behind Eastern time, by team. Used to flag the "circadian rhythm"
# case: an away team from a more-western timezone playing an early (<=1pm ET)
# kickoff, whose body clock is still on morning time relative to the home team.
TZ_OFFSET = {
    'BAL': 0, 'BUF': 0, 'CAR': 0, 'CIN': 0, 'CLE': 0, 'DET': 0, 'IND': 0, 'JAX': 0,
    'MIA': 0, 'NE': 0, 'NYG': 0, 'NYJ': 0, 'PHI': 0, 'PIT': 0, 'TB': 0, 'WAS': 0, 'ATL': 0,
    'CHI': -1, 'DAL': -1, 'GB': -1, 'HOU': -1, 'KC': -1, 'MIN': -1, 'NO': -1, 'TEN': -1,
    'DEN': -2, 'ARI': -2,
    'LA': -3, 'LAC': -3, 'LV': -3, 'SF': -3, 'SEA': -3, 'OAK': -3,
}


def add_body_clock(df):
    df = df.copy()
    away_tz = df['away_team'].map(TZ_OFFSET)
    home_tz = df['home_team'].map(TZ_OFFSET)
    kickoff_hour = df['gametime'].str.split(':').str[0].astype(int)
    df['west_to_east_early'] = (away_tz < home_tz) & (kickoff_hour <= 13)
    return df


def add_primetime(df):
    """Games kicking off at/after 7pm ET (SNF/MNF/TNF-type windows). Real
    confound risk: national TV disproportionately picks marquee matchups
    between good teams, so any effect here could be team-quality selection,
    not a genuine primetime performance difference. Untested causally, only
    empirically. See Session 36.
    """
    df = df.copy()
    df['primetime'] = df['gametime'].str.split(':').str[0].astype(int) >= 19
    return df


def add_turnover_margin(df, pbp):
    """Net turnover margin (home takeaways - home giveaways) per game. Used
    to discount the TRAINING signal, not the prediction, since turnover margin
    strongly explains THIS game's result (corr 0.54) but barely predicts a
    team's own future turnover margin (corr 0.08, essentially random). That's
    the classic signature of luck, not skill. See Session 36.
    """
    giveaway = ((pbp['interception'] == 1) | (pbp['fumble_lost'] == 1)).astype(int)
    tov = pbp.assign(giveaway=giveaway).groupby(['game_id', 'posteam'])['giveaway'].sum().reset_index()

    df = df.merge(tov, left_on=['game_id', 'home_team'], right_on=['game_id', 'posteam'], how='left')
    df = df.rename(columns={'giveaway': 'home_giveaways'}).drop(columns=['posteam'])
    df = df.merge(tov, left_on=['game_id', 'away_team'], right_on=['game_id', 'posteam'], how='left')
    df = df.rename(columns={'giveaway': 'away_giveaways'}).drop(columns=['posteam'])
    df['home_giveaways'] = df['home_giveaways'].fillna(0)
    df['away_giveaways'] = df['away_giveaways'].fillna(0)
    df['turnover_margin'] = df['away_giveaways'] - df['home_giveaways']
    return df


def add_sack_rate(df, pbp):
    """Sack rate allowed on dropbacks, an O-line/pass-protection proxy.
    corr(sack_rate_diff, result)=+0.36 raw, but real redundancy risk: sacks
    are already negative-EPA plays baked into home_epa/away_epa and qb_epa,
    so this may double-count the same signal those already capture (same
    trap as the totals opponent-adjustment). Untested for that yet, see
    Session 36's honest test for the answer.
    """
    dropbacks = pbp[pbp['qb_dropback'] == 1]
    sack_rate = dropbacks.groupby(['game_id', 'posteam'])['sack'].mean().reset_index().rename(
        columns={'sack': 'sack_rate'})
    df = df.merge(sack_rate, left_on=['game_id', 'home_team'], right_on=['game_id', 'posteam'], how='left')
    df = df.rename(columns={'sack_rate': 'home_sack_rate'}).drop(columns=['posteam'])
    df = df.merge(sack_rate, left_on=['game_id', 'away_team'], right_on=['game_id', 'posteam'], how='left')
    df = df.rename(columns={'sack_rate': 'away_sack_rate'}).drop(columns=['posteam'])
    return df


def add_oline_fault_sack_rate(df, pbp, ftn):
    """Refined O-line signal: sack rate EXCLUDING sacks charted as the QB's
    own fault (held the ball too long), only sacks attributable to
    protection/scheme. FTN charting data only exists from 2022 onward, so
    this is NaN (gracefully skipped by the update mechanism) for 2018-2021,
    meaning the validation window (2020-22) effectively only reflects 2022's
    signal. Session 39, testing whether this fixes why raw sack rate
    (add_sack_rate) failed in Session 36, possibly conflating QB pocket
    presence with O-line quality.
    """
    merged = pbp.merge(ftn, left_on=['game_id', 'play_id'],
                       right_on=['nflverse_game_id', 'nflverse_play_id'], how='inner')
    dropbacks = merged[merged['qb_dropback'] == 1]
    oline_sack = (dropbacks['sack'] == 1) & (dropbacks['is_qb_fault_sack'] == False)
    rate = dropbacks.assign(oline_sack=oline_sack).groupby(
        ['game_id', 'posteam'])['oline_sack'].mean().reset_index().rename(
        columns={'oline_sack': 'oline_sack_rate'})

    df = df.merge(rate, left_on=['game_id', 'home_team'], right_on=['game_id', 'posteam'], how='left')
    df = df.rename(columns={'oline_sack_rate': 'home_oline_sack_rate'}).drop(columns=['posteam'])
    df = df.merge(rate, left_on=['game_id', 'away_team'], right_on=['game_id', 'posteam'], how='left')
    df = df.rename(columns={'oline_sack_rate': 'away_oline_sack_rate'}).drop(columns=['posteam'])
    return df


def add_epa_margin(df, pbp):
    game_epa = pbp.groupby(['game_id', 'posteam'])['epa'].sum().reset_index()

    df = df.merge(game_epa, left_on=['game_id', 'home_team'],
                  right_on=['game_id', 'posteam'])
    df = df.rename(columns={'epa': 'home_epa'})
    df = df.merge(game_epa, left_on=['game_id', 'away_team'],
                  right_on=['game_id', 'posteam'])
    df = df.rename(columns={'epa': 'away_epa'})

    df['epa_margin'] = df['home_epa'] - df['away_epa']

    df = df.sort_values('gameday')
    return df


def add_success_rate(df, pbp):
    """Success rate: a play "succeeds" if it gains >=40% of yards-to-go on
    1st down, >=60% on 2nd, or the full distance on 3rd/4th. Genuinely
    different information from EPA (corr=0.52, much lower than opponent-
    adjustment's 0.90). It measures CONSISTENCY, not point value, so an
    explosive-play offense and a consistent-chain-mover can have very
    different success rates at the same EPA level. Session 40.
    """
    plays = pbp[pbp['down'].notna() & pbp['ydstogo'].notna() & pbp['yards_gained'].notna()].copy()
    thresh = plays['down'].map({1: 0.4, 2: 0.6, 3: 1.0, 4: 1.0})
    plays['success'] = (plays['yards_gained'] >= thresh * plays['ydstogo']).astype(int)
    succ = plays.groupby(['game_id', 'posteam'])['success'].mean().reset_index()

    df = df.merge(succ, left_on=['game_id', 'home_team'], right_on=['game_id', 'posteam'], how='left')
    df = df.rename(columns={'success': 'home_success'}).drop(columns=['posteam'])
    df = df.merge(succ, left_on=['game_id', 'away_team'], right_on=['game_id', 'posteam'], how='left')
    df = df.rename(columns={'success': 'away_success'}).drop(columns=['posteam'])
    df['success_diff'] = df['home_success'] - df['away_success']
    return df


def add_adjusted_epa_margin(df):
    """Opponent-adjusted EPA margin. Corrects each team's game EPA for how
    good/bad the opponent's defense typically is (trailing, no lookahead),
    unlike raw epa_margin which treats a big game against a bad defense the
    same as a big game against a good one.

    def_strength[team] = trailing avg EPA ALLOWED by that team's defense.
    A team is adjusted UP if their opponent's defense was tougher than
    average, DOWN if it was weaker than average. Requires `home_epa`/
    `away_epa` (from add_epa_margin) to already be present.

    Falls back to raw epa_margin for early-season games with no trailing
    defensive history yet (season openers, first ~2 games of a team's year).
    """
    home_allowed = df[['season', 'week', 'home_team', 'away_epa']].rename(
        columns={'home_team': 'team', 'away_epa': 'epa_allowed'})
    away_allowed = df[['season', 'week', 'away_team', 'home_epa']].rename(
        columns={'away_team': 'team', 'home_epa': 'epa_allowed'})
    allowed = pd.concat([home_allowed, away_allowed]).sort_values(['team', 'season', 'week'])
    allowed['def_strength'] = allowed.groupby('team')['epa_allowed'].transform(
        lambda s: s.shift(1).rolling(8, min_periods=3).mean())
    league_avg = df['home_epa'].mean()

    df = df.merge(allowed[['team', 'season', 'week', 'def_strength']].rename(
        columns={'team': 'home_team', 'def_strength': 'home_def_strength'}),
        on=['season', 'week', 'home_team'], how='left')
    df = df.merge(allowed[['team', 'season', 'week', 'def_strength']].rename(
        columns={'team': 'away_team', 'def_strength': 'away_def_strength'}),
        on=['season', 'week', 'away_team'], how='left')

    df['adj_home_epa'] = df['home_epa'] - df['away_def_strength'] + league_avg
    df['adj_away_epa'] = df['away_epa'] - df['home_def_strength'] + league_avg
    df['adj_epa_margin'] = df['adj_home_epa'] - df['adj_away_epa']
    df['adj_epa_margin'] = df['adj_epa_margin'].fillna(df['epa_margin'])
    df = df.drop(columns=['adj_home_epa', 'adj_away_epa', 'home_def_strength', 'away_def_strength'])
    return df


def add_qb_epa(df, pbp):
    dropbacks = pbp[pbp['qb_dropback'] == 1]
    qb_epa = dropbacks.groupby(['game_id', 'passer_id'])['epa'].mean().reset_index()

    df = df.merge(qb_epa, left_on=['game_id', 'home_qb_id'],
                  right_on=['game_id', 'passer_id'], how='left')
    df = df.rename(columns={'epa': 'home_qb_epa'})
    df = df.drop(columns=['passer_id'])
    df = df.merge(qb_epa, left_on=['game_id', 'away_qb_id'],
                  right_on=['game_id', 'passer_id'], how='left')
    df = df.rename(columns={'epa': 'away_qb_epa'})
    df = df.drop(columns=['passer_id'])

    df = df.sort_values('gameday')
    return df


def add_cpoe(df, ngs_passing):
    """Completion % above expectation, a Next Gen Stats QB accuracy metric,
    genuinely distinct from EPA/dropback (isolates throw accuracy specifically,
    not tangled with pass-rush/scheme effects the way EPA is). Session 38.
    """
    ngs = ngs_passing[ngs_passing['week'] > 0][
        ['season', 'week', 'player_gsis_id', 'completion_percentage_above_expectation']
    ].rename(columns={'completion_percentage_above_expectation': 'cpoe'})

    df = df.merge(ngs, left_on=['season', 'week', 'home_qb_id'],
                  right_on=['season', 'week', 'player_gsis_id'], how='left')
    df = df.rename(columns={'cpoe': 'home_cpoe'}).drop(columns=['player_gsis_id'])
    df = df.merge(ngs, left_on=['season', 'week', 'away_qb_id'],
                  right_on=['season', 'week', 'player_gsis_id'], how='left')
    df = df.rename(columns={'cpoe': 'away_cpoe'}).drop(columns=['player_gsis_id'])
    return df


# Rough position-importance tiers for injury severity, excluding QB (already
# covered by the separate persistent QB rating; including it here would
# double-count the same signal, same trap as travel_coef/body_clock_coef).
POSITION_WEIGHT = {
    'WR': 2, 'T': 2, 'CB': 2, 'DE': 2,
    'TE': 1, 'G': 1, 'C': 1, 'DT': 1, 'LB': 1, 'S': 1,
    'RB': 0.5, 'FB': 0.5, 'K': 0.5, 'P': 0.5, 'LS': 0.5,
}


def add_injuries(df, injuries, doubtful_mult=0.0, questionable_mult=0.0):
    """doubtful_mult/questionable_mult give partial credit to Doubtful/
    Questionable statuses on top of the always-full-weight 'Out'. Both
    default to 0 (original MVP behavior: only Out counts) since a
    Questionable player usually DOES play. See Session 37 for the test.
    """
    out = injuries[(injuries['position'] != 'QB') &
                   (injuries['report_status'].isin(['Out', 'Doubtful', 'Questionable']))].copy()
    status_mult = {'Out': 1.0, 'Doubtful': doubtful_mult, 'Questionable': questionable_mult}
    out['weight'] = out['position'].map(POSITION_WEIGHT).fillna(0) * out['report_status'].map(status_mult)
    severity = out.groupby(['season', 'week', 'team'])['weight'].sum().reset_index()
    severity = severity.rename(columns={'weight': 'severity'})

    df = df.merge(severity, left_on=['season', 'week', 'home_team'],
                  right_on=['season', 'week', 'team'], how='left')
    df = df.rename(columns={'severity': 'home_severity'}).drop(columns=['team'])
    df = df.merge(severity, left_on=['season', 'week', 'away_team'],
                  right_on=['season', 'week', 'team'], how='left')
    df = df.rename(columns={'severity': 'away_severity'}).drop(columns=['team'])
    df['home_severity'] = df['home_severity'].fillna(0)
    df['away_severity'] = df['away_severity'].fillna(0)
    return df


def add_injuries_starters(df, injuries, snap_counts, ids):
    """Refined injury severity, restricted to players who were recently STARTING
    (trailing snap share > 0.5) before going Out. Filters out the noise of
    backup 'Out' designations that the simpler add_injuries() MVP counts equally.

    Two real data-linking gotchas solved here (see PROGRESS.md Session 32):
    - snap_counts uses pfr_player_id, injuries uses gsis_id. Different ID
      systems, linked via nfl.import_ids()'s crosswalk (only ~81% coverage,
      an accepted imprecision like several other features in this project).
    - An 'Out' player has NO snap-count row for that week (they didn't play),
      so matching on the same week is impossible by construction. Needs
      merge_asof to find each player's most recent PRIOR game instead.
    - Both dtype traps: pandas 3.0's nullable 'string' dtype vs plain 'object'
      breaks merge_asof outright (raises) and silently returns near-zero
      matches with a plain .merge(). .astype(object) on both sides required.
    """
    crosswalk = ids[['pfr_id', 'gsis_id']].dropna()
    crosswalk = crosswalk[crosswalk['gsis_id'].str.match(r'^\d{2}-\d{7}$')]
    crosswalk = crosswalk.drop_duplicates('pfr_id')
    crosswalk['gsis_id'] = crosswalk['gsis_id'].astype(object)

    snaps = snap_counts.merge(crosswalk, left_on='pfr_player_id', right_on='pfr_id', how='left')
    snaps = snaps.dropna(subset=['gsis_id']).copy()
    snaps['gsis_id'] = snaps['gsis_id'].astype(object)
    snaps['snap_pct'] = snaps[['offense_pct', 'defense_pct']].max(axis=1)
    snaps = snaps.sort_values(['gsis_id', 'season', 'week'])
    snaps['recent_pct'] = snaps.groupby('gsis_id')['snap_pct'].transform(
        lambda s: s.rolling(3, min_periods=1).mean())

    out = injuries[(injuries['report_status'] == 'Out') & (injuries['position'] != 'QB')].copy()
    out = out.dropna(subset=['gsis_id']).copy()
    out['gsis_id'] = out['gsis_id'].astype(object)
    out['week'] = out['week'].astype('int64')
    snaps['week'] = snaps['week'].astype('int64')
    out_sorted = out.sort_values('week')
    snaps_sorted = snaps[['gsis_id', 'week', 'recent_pct']].sort_values('week')

    matched = pd.merge_asof(out_sorted, snaps_sorted, by='gsis_id', left_on='week', right_on='week',
                             direction='backward', allow_exact_matches=False)
    starters_out = matched[matched['recent_pct'] > 0.5].copy()
    starters_out['weight'] = starters_out['position'].map(POSITION_WEIGHT).fillna(0)

    severity = starters_out.groupby(['season', 'week', 'team'])['weight'].sum().reset_index()
    severity = severity.rename(columns={'weight': 'severity_v2'})

    df = df.merge(severity, left_on=['season', 'week', 'home_team'],
                  right_on=['season', 'week', 'team'], how='left')
    df = df.rename(columns={'severity_v2': 'home_severity_v2'}).drop(columns=['team'])
    df = df.merge(severity, left_on=['season', 'week', 'away_team'],
                  right_on=['season', 'week', 'team'], how='left')
    df = df.rename(columns={'severity_v2': 'away_severity_v2'}).drop(columns=['team'])
    df['home_severity_v2'] = df['home_severity_v2'].fillna(0)
    df['away_severity_v2'] = df['away_severity_v2'].fillna(0)
    return df


def add_weather(df, pbp):
    game_weather = pbp.groupby('game_id')['weather'].first().reset_index()
    df = df.merge(game_weather, on='game_id')
    df['bad_weather'] = (df['weather'].str.contains('rain', case=False, na=False) |
                          df['weather'].str.contains('snow', case=False, na=False))
    df['clear_weather'] = (df['weather'].str.contains('sunny', case=False, na=False) |
                            df['weather'].str.contains('clear', case=False, na=False))
    return df


def add_surface(df):
    """Turf vs grass. Raw check: turf averages 47.2 total pts vs grass 44.7
    (~2.5pt gap), real and physically plausible (turf is a faster surface).
    Session 40.
    """
    df = df.copy()
    df['surface_clean'] = df['surface'].str.strip().str.lower()
    df['is_turf'] = ~df['surface_clean'].isin(['grass'])
    return df


def add_extreme_cold(df):
    """Outdoor games below 32F, no precipitation required. A different
    mechanism than bad_weather (ball grip/kicking distance in the cold,
    not precip). Raw check: 42.9 vs 45.0 avg total (~2.1pt gap, n=63,
    small sample, treat cautiously). Session 40.
    """
    df = df.copy()
    df['extreme_cold'] = (df['roof'].isin(['outdoors', 'open'])) & (df['temp'] < 32)
    return df
