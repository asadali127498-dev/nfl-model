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

print("\nTOTALS VALIDATION (2022-23) — pick K here")
for K in [0.5, 0.6,0.7,0.8,0.9]:
    tv = elo_model.run_totals(df, K=K, eval_from=2022, eval_to=2023)
    print(f"K={K}: MAE {tv['mae']:.4f}  vs Vegas {tv['vegas_mae']:.4f}")

test_totals = elo_model.run_totals(df, K=0.8, eval_from=2024, eval_to=2024)
print(f"\nTOTALS TEST (2024, untouched): MAE {test_totals['mae']:.4f}  vs Vegas {test_totals['vegas_mae']:.4f}")

print("\nQB REGRESSION VALIDATION (2022-23) — pick qb_regression here, K=2")
for qb_regression in [0, 0.1, 0.2, 0.3, 0.5,0.6,0.7,0.8,0.9,1.0,1.1]:
    q = elo_model.run(df, K=2, qb_regression=qb_regression, eval_from=2022, eval_to=2023)
    print(f"qb_regression={qb_regression}: MAE {q['mae']:.4f}  Brier {q['brier']:.4f}")

print("\nTOTALS SCALE VALIDATION (2022-23) — pick scale here, K=0.8")
for scale in [15, 20, 25, 30, 35]:
    s = elo_model.run_totals(df, K=0.8, scale=scale, eval_from=2022, eval_to=2023)
    print(f"scale={scale}: MAE {s['mae']:.4f}  vs Vegas {s['vegas_mae']:.4f}")

print("\nHFA VALIDATION (2022-23) — pick hfa here, K=2")
print("judged on Brier + calibration, not just MAE (MAE barely moves across this range)")
for hfa in [1.0, 1.5, 2.0, 2.5, 3.0]:
    h = elo_model.run(df, K=2, hfa=hfa, eval_from=2022, eval_to=2023)
    n1, r1 = elo_model.bucket_rate(h['winprobs'], h['homewins'], 0.4, 0.5)
    n2, r2 = elo_model.bucket_rate(h['winprobs'], h['homewins'], 0.5, 0.6)
    print(f"hfa={hfa}: MAE {h['mae']:.4f}  Brier {h['brier']:.4f}  "
          f"underdog(.4-.5)={r1:.3f} (n={n1})  favorite(.5-.6)={r2:.3f} (n={n2})")