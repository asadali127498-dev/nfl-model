import dataloader
import metrics
import elo_model

YEARS = [2021, 2022, 2023, 2024]

df = dataloader.load_schedules(YEARS)
pbp = dataloader.load_pbp(YEARS)
df = metrics.add_epa_margin(df, pbp)


print("VALIDATION (2022-23) — pick K here")
for K in [1, 1.5, 2, 3, 4]:
    v = elo_model.run(df, K=K, eval_from=2022, eval_to=2023)
    print(f"K={K}: MAE {v['mae']:.4f}  Brier {v['brier']:.4f}")
    




best = elo_model.run(df, w=1)
counts, wins = elo_model.calibration_table(best['winprobs'], best['homewins'])
print(f"\nCalibration (result, K=2):")
for b in range(10):
    if counts[b] > 0:
        print(f"  bucket {b}: {wins[b]:>3}/{counts[b]:>3} = {wins[b]/counts[b]:.2f}")

test = elo_model.run(df, K=2, eval_from=2024, eval_to=2024)
print(f"\nTEST (2024, untouched): MAE {test['mae']:.4f}  vs Vegas {test['vegas_mae']:.4f}  Brier {test['brier']:.4f}")