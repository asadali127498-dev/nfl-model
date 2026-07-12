

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
