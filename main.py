import dataloader
import metrics
import elo_model

YEARS = [2021, 2022, 2023, 2024]

df = dataloader.load_schedules(YEARS)
pbp = dataloader.load_pbp(YEARS)
df = metrics.add_epa_margin(df, pbp)

print(f"{'K':>4} | {'result MAE':>10} {'result Brier':>12} | {'EPA MAE':>9} {'EPA Brier':>9}")
print("-" * 55)
for K in [1, 1.5, 2, 3, 4, 6, 8]:
    r = elo_model.run(df, K=K, signal='result')
    e = elo_model.run(df, K=K, signal='epa_margin')
    print(f"{K:>4} | {r['mae']:>10.4f} {r['brier']:>12.4f} | {e['mae']:>9.4f} {e['brier']:>9.4f}")

print(f"\nVegas MAE benchmark: {elo_model.run(df)['vegas_mae']:.4f}")


best = elo_model.run(df, K=2, signal='result')
counts, wins = elo_model.calibration_table(best['winprobs'], best['homewins'])
print(f"\nCalibration (result, K=2):")
for b in range(10):
    if counts[b] > 0:
        print(f"  bucket {b}: {wins[b]:>3}/{counts[b]:>3} = {wins[b]/counts[b]:.2f}")
