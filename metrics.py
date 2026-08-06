from math import radians, sin, cos, asin, sqrt
import pandas as pd

# Stadium coordinates (lat, lon) for every team abbreviation seen in the
# 2018-2025 data. LV/OAK are the same franchise (relocated 2020) — kept as
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


# Rough position-importance tiers for injury severity, excluding QB (already
# covered by the separate persistent QB rating — including it here would
# double-count the same signal, same trap as travel_coef/body_clock_coef).
POSITION_WEIGHT = {
    'WR': 2, 'T': 2, 'CB': 2, 'DE': 2,
    'TE': 1, 'G': 1, 'C': 1, 'DT': 1, 'LB': 1, 'S': 1,
    'RB': 0.5, 'FB': 0.5, 'K': 0.5, 'P': 0.5, 'LS': 0.5,
}


def add_injuries(df, injuries):
    out = injuries[(injuries['report_status'] == 'Out') & (injuries['position'] != 'QB')].copy()
    out['weight'] = out['position'].map(POSITION_WEIGHT).fillna(0)
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
    (trailing snap share > 0.5) before going Out — filters out the noise of
    backup 'Out' designations that the simpler add_injuries() MVP counts equally.

    Two real data-linking gotchas solved here (see PROGRESS.md Session 32):
    - snap_counts uses pfr_player_id, injuries uses gsis_id — different ID
      systems, linked via nfl.import_ids()'s crosswalk (only ~81% coverage,
      an accepted imprecision like several other features in this project).
    - An 'Out' player has NO snap-count row for that week (they didn't play),
      so matching on the same week is impossible by construction. Needs
      merge_asof to find each player's most recent PRIOR game instead.
    - Both dtype traps: pandas 3.0's nullable 'string' dtype vs plain 'object'
      breaks merge_asof outright (raises) and silently returns near-zero
      matches with a plain .merge() — .astype(object) on both sides required.
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
