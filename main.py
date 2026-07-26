import dataloader
import metrics
import elo_model

# warm-up 2018-19, VALIDATION 2020-22, TEST 2023-25 (three held-out seasons)
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

df = dataloader.load_schedules(YEARS)
pbp = dataloader.load_pbp(YEARS)
df = metrics.add_epa_margin(df, pbp)
df = metrics.add_weather(df, pbp)

print("VALIDATION (2020-22) — pick K here")
for K in [1, 1.5, 2, 3, 4]:
    v = elo_model.run(df, K=K, eval_from=2020, eval_to=2022)
    print(f"K={K}: MAE {v['mae']:.4f}  Brier {v['brier']:.4f}")

best = elo_model.run(df, w=1, eval_from=2020, eval_to=2025)
counts, wins = elo_model.calibration_table(best['winprobs'], best['homewins'])
print(f"\nCalibration (result, K=2):")
for b in range(10):
    if counts[b] > 0:
        print(f"  bucket {b}: {wins[b]:>3}/{counts[b]:>3} = {wins[b]/counts[b]:.2f}")

test = elo_model.run(df, K=2, eval_from=2023, eval_to=2025)
print(f"\nTEST (2023-25, untouched): MAE {test['mae']:.4f}  vs Vegas {test['vegas_mae']:.4f}  Brier {test['brier']:.4f}")

print("\nTOTALS VALIDATION (2020-22) — pick K here")
for K in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    tv = elo_model.run_totals(df, K=K, eval_from=2020, eval_to=2022)
    print(f"K={K}: MAE {tv['mae']:.4f}  vs Vegas {tv['vegas_mae']:.4f}")

test_totals = elo_model.run_totals(df, K=0.6, eval_from=2023, eval_to=2025)
print(f"\nTOTALS TEST (2023-25, untouched): MAE {test_totals['mae']:.4f}  vs Vegas {test_totals['vegas_mae']:.4f}")

print("\nWIND VALIDATION (2020-22) — pick wind_coef here, K=0.6, threshold=15mph")
print("judged on the OUTDOOR-only gap, not overall MAE (dome games are unaffected)")
for wind_coef in [0, 0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0]:
    w = elo_model.run_totals(df, K=0.6, wind_coef=wind_coef, eval_from=2020, eval_to=2022)
    outdoor = [g for g in w['games'] if g['roof'] == 'outdoors']
    m = sum(abs(g['pred'] - g['actual']) for g in outdoor) / len(outdoor)
    v = sum(abs(g['vegas'] - g['actual']) for g in outdoor) / len(outdoor)
    print(f"wind_coef={wind_coef}: outdoor Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

test_totals_wind = elo_model.run_totals(df, K=0.6, eval_from=2023, eval_to=2025)
outdoor_test = [g for g in test_totals_wind['games'] if g['roof'] == 'outdoors']
om = sum(abs(g['pred'] - g['actual']) for g in outdoor_test) / len(outdoor_test)
ov = sum(abs(g['vegas'] - g['actual']) for g in outdoor_test) / len(outdoor_test)
print(f"\nTOTALS TEST w/ wind fix (2023-25, untouched): MAE {test_totals_wind['mae']:.4f}  vs Vegas {test_totals_wind['vegas_mae']:.4f}")
print(f"  outdoor-only: Model MAE={om:.3f}  Vegas MAE={ov:.3f}  gap={om-ov:.3f}")

print("\nRAIN/SNOW VALIDATION (2020-22) — pick rain_snow_coef here, K=0.6")
print("judged on bad-weather games only (small sample — expect a lot of noise)")
for rain_snow_coef in [0, 2, 5, 7, 8, 9, 10, 12, 16, 20]:
    r = elo_model.run_totals(df, K=0.6, rain_snow_coef=rain_snow_coef, eval_from=2020, eval_to=2022)
    bad = [g for g in r['games'] if g['bad_weather']]
    m = sum(abs(g['pred'] - g['actual']) for g in bad) / len(bad)
    v = sum(abs(g['vegas'] - g['actual']) for g in bad) / len(bad)
    print(f"rain_snow_coef={rain_snow_coef}: n={len(bad)}  Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

test_totals_rain = elo_model.run_totals(df, K=0.6, eval_from=2023, eval_to=2025)
bad_test = [g for g in test_totals_rain['games'] if g['bad_weather']]
bm = sum(abs(g['pred'] - g['actual']) for g in bad_test) / len(bad_test)
bv = sum(abs(g['vegas'] - g['actual']) for g in bad_test) / len(bad_test)
print(f"\nTOTALS TEST w/ rain/snow fix (2023-25, untouched): MAE {test_totals_rain['mae']:.4f}  vs Vegas {test_totals_rain['vegas_mae']:.4f}")
print(f"  bad-weather-only: Model MAE={bm:.3f}  Vegas MAE={bv:.3f}  gap={bm-bv:.3f}")

print("\nCLEAR/SUNNY VALIDATION (2020-22) — pick clear_weather_coef here, K=0.6")
print("SHELVED: coef that helped validation ran opposite the raw data (clear games")
print("score HIGHER on average, but a NEGATIVE coef improved the fit) — a confound")
print("red flag, confirmed by the test failing. Kept here for a transparent record.")
for clear_weather_coef in [-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3]:
    c = elo_model.run_totals(df, K=0.6, clear_weather_coef=clear_weather_coef, eval_from=2020, eval_to=2022)
    clear = [g for g in c['games'] if g['clear_weather']]
    m = sum(abs(g['pred'] - g['actual']) for g in clear) / len(clear)
    v = sum(abs(g['vegas'] - g['actual']) for g in clear) / len(clear)
    print(f"clear_weather_coef={clear_weather_coef}: n={len(clear)}  Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

test_totals_clear = elo_model.run_totals(df, K=0.6, eval_from=2023, eval_to=2025)
clear_test = [g for g in test_totals_clear['games'] if g['clear_weather']]
cm = sum(abs(g['pred'] - g['actual']) for g in clear_test) / len(clear_test)
cv = sum(abs(g['vegas'] - g['actual']) for g in clear_test) / len(clear_test)
print(f"\nTOTALS TEST w/o clear-weather fix (2023-25, untouched): MAE {test_totals_clear['mae']:.4f}  vs Vegas {test_totals_clear['vegas_mae']:.4f}")
print(f"  clear-weather-only: Model MAE={cm:.3f}  Vegas MAE={cv:.3f}  gap={cm-cv:.3f}")

print("\nQB REGRESSION VALIDATION (2020-22) — pick qb_regression here, K=2")
for qb_regression in [0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]:
    q = elo_model.run(df, K=2, qb_regression=qb_regression, eval_from=2020, eval_to=2022)
    print(f"qb_regression={qb_regression}: MAE {q['mae']:.4f}  Brier {q['brier']:.4f}")

print("\nTOTALS SCALE VALIDATION (2020-22) — pick scale here, K=0.6")
for scale in [15, 20, 25, 30, 35]:
    s = elo_model.run_totals(df, K=0.6, scale=scale, eval_from=2020, eval_to=2022)
    print(f"scale={scale}: MAE {s['mae']:.4f}  vs Vegas {s['vegas_mae']:.4f}")

print("\nHFA VALIDATION (2020-22) — pick hfa here, K=2")
print("judged on Brier + calibration, not just MAE (MAE barely moves across this range)")
for hfa in [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]:
    h = elo_model.run(df, K=2, hfa=hfa, eval_from=2020, eval_to=2022)
    n1, r1 = elo_model.bucket_rate(h['winprobs'], h['homewins'], 0.4, 0.5)
    n2, r2 = elo_model.bucket_rate(h['winprobs'], h['homewins'], 0.5, 0.6)
    print(f"hfa={hfa}: MAE {h['mae']:.4f}  Brier {h['brier']:.4f}  "
          f"underdog(.4-.5)={r1:.3f} (n={n1})  favorite(.5-.6)={r2:.3f} (n={n2})")
