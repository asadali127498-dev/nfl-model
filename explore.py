import nfl_data_py as nfl

df = nfl.import_schedules([2021, 2022, 2023, 2024])
df = df[df['game_type'] == 'REG']
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
len(philly_margins)
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
   
   
elo = {}
for team in df['home_team'].unique():
    elo[team] = 1500
current_season = None

predictedmargins = []
actualmargins = []
Vegasmargins = []
hfa = 3
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
    if row['season'] == 2024:
        predictedmargins.append(expected)
        actualmargins.append(row['result'])
        Vegasmargins.append(row['spread_line'])
        elo[home] = elo[home] + 4 * (actual - expected)
        elo[away] = elo[away] - 4 * (actual - expected)
model_mae = sum( abs(p - a) for p, a, in zip(predictedmargins, actualmargins) ) / len(predictedmargins)
vegas_mae = sum( abs(v - a) for v, a, in zip(Vegasmargins, actualmargins) ) / len(Vegasmargins)
sorted_elo = sorted(elo.items(), key=lambda x: x[1], reverse=True)
print(f"Model MAE: {model_mae:.2f}")
print(f"Vegas MAE: {vegas_mae:.2f}")
for team, rating in sorted_elo:
    print(f"{team}: {rating:.1f}")

