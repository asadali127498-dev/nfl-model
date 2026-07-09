import nfl_data_py as nfl
pbp = nfl.import_pbp_data([2024])
print(pbp.shape)
print((pbp[['game_id', 'posteam', 'epa']]).head(20).to_string())

pbp = pbp[pbp['posteam'].notna()]                      
game_epa = pbp.groupby(['game_id', 'posteam'])['epa'].sum()
print(game_epa.head(10))