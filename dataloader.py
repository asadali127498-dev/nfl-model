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

def load_injuries(years):
    return nfl.import_injuries(years)

def load_snap_counts(years):
    return nfl.import_snap_counts(years)

def load_ids():
    return nfl.import_ids()

