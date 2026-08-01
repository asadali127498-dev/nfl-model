from math import radians, sin, cos, asin, sqrt

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


def add_weather(df, pbp):
    game_weather = pbp.groupby('game_id')['weather'].first().reset_index()
    df = df.merge(game_weather, on='game_id')
    df['bad_weather'] = (df['weather'].str.contains('rain', case=False, na=False) |
                          df['weather'].str.contains('snow', case=False, na=False))
    df['clear_weather'] = (df['weather'].str.contains('sunny', case=False, na=False) |
                            df['weather'].str.contains('clear', case=False, na=False))
    return df
