import nfl_data_py as nfl
pbp = nfl.import_pbp_data([2024])
df = nfl.import_schedules([2024])
df = df[df['game_type'] == 'REG']

print(pbp.shape)
print((pbp[['game_id', 'posteam', 'epa']]).head(20).to_string())

pbp = pbp[pbp['posteam'].notna()]                      
game_epa = pbp.groupby(['game_id', 'posteam'])['epa'].sum()
print(game_epa.head(10))
game_epa = game_epa.reset_index()
print(game_epa.head(10))
df = df.merge(
    game_epa,
    left_on=['game_id', 'home_team'],
    right_on=['game_id', 'posteam']
)
df = df.rename(columns={'epa': 'home_epa'})
print(df[['game_id', 'home_team', 'away_team', 'home_epa']].head())
df = df.merge(
    game_epa,
    left_on=['game_id', 'away_team'],
    right_on=['game_id', 'posteam']
)
df = df.rename(columns={'epa': 'away_epa'})
print(df[['game_id', 'home_team', 'away_team', 'home_epa', 'away_epa']].head())

df['epa_margin'] = df['home_epa'] - df['away_epa']
print(df[['game_id', 'result', 'epa_margin']].head())
