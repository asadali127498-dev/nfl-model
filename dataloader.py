import nfl_data_py as nfl
def load_schedules(years):
    df = nfl.import_schedules(years)
    df = df[df['game_type'] == 'REG']
    df = df.sort_values('gameday')
    return df

def load_pbp(years):
    pbp = nfl.import_pbp_data(years)
    pbp = pbp[pbp['posteam'].notna()]                      
    return pbp

