import nfl_data_py as nfl
from statistics import NormalDist

df = nfl.import_schedules([2021, 2022, 2023, 2024])
df = df[df['game_type'] == 'REG']
df = df.sort_values('gameday')
print(df.shape)
print(df.columns)
print(df.head())
print(df[['home_team', 'away_team', 'home_score', 'away_score', 'result']].head(10).to_string())
df = df.sort_values('gameday')

philly_margins = []

for index, row in df.iterrows():
    if row['home_team'] == 'PHI':
        philly_margins.append(row['result'])
    elif row['away_team'] == 'PHI':
        philly_margins.append(-row['result'])

print(sum(philly_margins))
print(len(philly_margins))
average_margin = sum(philly_margins) / len(philly_margins)
print(average_margin)
print(df['home_team'].unique())
team_avg = {}

for team in df['home_team'].unique():
    margins = []
    for index, row in df.iterrows():
        if row['home_team'] == team:
            margins.append(row['result'])
        elif row['away_team'] == team:
            margins.append(-row['result'])
    team_avg[team] = sum(margins) / len(margins)

print(team_avg)
sorted_teams = sorted(team_avg.items(), key=lambda x: x[1], reverse=True)
for team, avg in sorted_teams:
    print(f"{team}: {avg:.2f}")
pbp = nfl.import_pbp_data([2021, 2022, 2023, 2024])
  
 
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
  
elo = {}
for team in df['home_team'].unique():
    elo[team] = 1500
current_season = None

predictedmargins = []
actualmargins = []
Vegasmargins = []
winprobs = []
homewins = []
K = 4
hfa = 2.5
sigma = 16
for index, row in df.iterrows():
    if row['season'] != current_season:
        if current_season is not None:
            for team in elo:
                elo[team] = 1500 + 0.75 * (elo[team] - 1500)
        current_season = row['season']
    home = row['home_team']
    away = row['away_team']
    actual = max(min(row['result'], 20), -20)  
    expected = max(min((elo[home] - elo[away]) / 25 + hfa, 20), -20)
    win_prob = NormalDist().cdf(expected / sigma)
    if row['season'] >= 2022:
        predictedmargins.append(expected)
        actualmargins.append(row['result'])
        Vegasmargins.append(row['spread_line'])
        winprobs.append(win_prob)
        homewins.append(1 if row['result'] > 0 else 0)
    elo[home] = elo[home] + K * (actual - expected)
    elo[away] = elo[away] - K * (actual - expected)
brier = sum((p - w)**2  for p, w in zip(winprobs, homewins) ) / len(winprobs)
print(f"Brier: {brier:.4f}")
model_mae = sum( abs(p - a) for p, a, in zip(predictedmargins, actualmargins) ) / len(predictedmargins)
vegas_mae = sum( abs(v - a) for v, a, in zip(Vegasmargins, actualmargins) ) / len(Vegasmargins)
sorted_elo = sorted(elo.items(), key=lambda x: x[1], reverse=True)

bucket_count = {}
bucket_wins = {}
for b in range(10):
    bucket_count[b] = 0
    bucket_wins[b]  = 0
for prob, won in zip(winprobs, homewins):
    bucket = int(prob * 10)
    bucket_count[bucket] += 1
    bucket_wins[bucket] += won
print(f"Model MAE: {model_mae:.2f}")
print(f"Vegas MAE: {vegas_mae:.2f}")
for team, rating in sorted_elo:
    print(f"{team}: {rating:.1f}")
for b in range(10):
    if bucket_count[b] > 0:
        print(f"Bucket {b}: {bucket_wins[b]} wins out of {bucket_count[b]} games, win rate: {bucket_wins[b]/bucket_count[b]:.2f}")

print(df[['gameday', 'home_team', 'away_team', 'result', 'epa_margin']].head())