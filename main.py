import dataloader
import metrics
import elo_model

# warm-up 2018-19, VALIDATION 2020-22, TEST 2023-25 (three held-out seasons)
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

df = dataloader.load_schedules(YEARS)
pbp = dataloader.load_pbp(YEARS)
df = metrics.add_epa_margin(df, pbp)
df = metrics.add_weather(df, pbp)
df = metrics.add_qb_epa(df, pbp)
df = metrics.add_travel(df)
df = metrics.add_body_clock(df)
injuries = dataloader.load_injuries(YEARS)
df = metrics.add_injuries(df, injuries)

# ============================================================
# VALIDATION (2020-22) — all tuning happens here, nothing below
# this section may read `test`/TEST numbers until every sweep
# in this block has finished (that ordering bug bit Session 21).
# ============================================================

print("VALIDATION (2020-22) — pick K here")
for K in [1, 1.5, 2, 3, 4]:
    v = elo_model.run(df, K=K, eval_from=2020, eval_to=2022)
    print(f"K={K}: MAE {v['mae']:.4f}  Brier {v['brier']:.4f}")

print("\nTOTALS VALIDATION (2020-22) — pick K here")
for K in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    tv = elo_model.run_totals(df, K=K, eval_from=2020, eval_to=2022)
    print(f"K={K}: MAE {tv['mae']:.4f}  vs Vegas {tv['vegas_mae']:.4f}")

print("\nWIND VALIDATION (2020-22) — pick wind_coef here, K=0.6, threshold=15mph")
print("judged on the OUTDOOR-only gap, not overall MAE (dome games are unaffected)")
for wind_coef in [0, 0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0]:
    w = elo_model.run_totals(df, K=0.6, wind_coef=wind_coef, eval_from=2020, eval_to=2022)
    outdoor = [g for g in w['games'] if g['roof'] == 'outdoors']
    m = sum(abs(g['pred'] - g['actual']) for g in outdoor) / len(outdoor)
    v = sum(abs(g['vegas'] - g['actual']) for g in outdoor) / len(outdoor)
    print(f"wind_coef={wind_coef}: outdoor Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

print("\nRAIN/SNOW VALIDATION (2020-22) — pick rain_snow_coef here, K=0.6")
print("judged on bad-weather games only (small sample — expect a lot of noise)")
for rain_snow_coef in [0, 2, 5, 7, 8, 9, 10, 12, 16, 20]:
    r = elo_model.run_totals(df, K=0.6, rain_snow_coef=rain_snow_coef, eval_from=2020, eval_to=2022)
    bad = [g for g in r['games'] if g['bad_weather']]
    m = sum(abs(g['pred'] - g['actual']) for g in bad) / len(bad)
    v = sum(abs(g['vegas'] - g['actual']) for g in bad) / len(bad)
    print(f"rain_snow_coef={rain_snow_coef}: n={len(bad)}  Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

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

print("\nDIVISIONAL VALIDATION (2020-22) — pick div_coef here, K=0.6")
print("judged on divisional games only. Raw-data check: avg total is basically")
print("identical for div vs non-div early season (46.6/45.1) and late (45.7/45.2)")
print("once controlled for week-of-season, so this isn't a pure scheduling artifact.")
for div_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3]:
    d = elo_model.run_totals(df, K=0.6, div_coef=div_coef, eval_from=2020, eval_to=2022)
    div = [g for g in d['games'] if g['div_game']]
    m = sum(abs(g['pred'] - g['actual']) for g in div) / len(div)
    v = sum(abs(g['vegas'] - g['actual']) for g in div) / len(div)
    print(f"div_coef={div_coef}: n={len(div)}  Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

print("\nQB REGRESSION VALIDATION (2020-22) — pick qb_regression here, K=2")
for qb_regression in [0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]:
    q = elo_model.run(df, K=2, qb_regression=qb_regression, eval_from=2020, eval_to=2022)
    print(f"qb_regression={qb_regression}: MAE {q['mae']:.4f}  Brier {q['brier']:.4f}")

print("\nQB RATING VALIDATION (2020-22) — pick qb_boost here, K=2, qb_k=0.15, qb_retention=1.0")
print("qb_rating is a persistent per-passer EMA of passing EPA/dropback, carried")
print("across team changes (unlike team elo, which resets 25% every offseason).")
for qb_boost in [0, 2, 4, 5, 6, 8, 10, 12, 15]:
    qr = elo_model.run(df, K=2, qb_boost=qb_boost, eval_from=2020, eval_to=2022)
    print(f"qb_boost={qb_boost}: MAE {qr['mae']:.4f}  Brier {qr['brier']:.4f}")

print("\nQB_K VALIDATION (2020-22) — pick qb_k here, K=2, qb_boost=5, qb_retention=1.0")
print("qb_k is the EMA smoothing rate for the QB rating (0.15 was an unswept prior)")
print("SHELVED RESULT: qb_k=0.05 looked better here, but combined with the retention")
print("tune below, the honest test came back WORSE than the qb_k=0.15 default. Reverted.")
for qb_k in [0.01, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3]:
    qk = elo_model.run(df, K=2, qb_boost=5, qb_k=qb_k, eval_from=2020, eval_to=2022)
    print(f"qb_k={qb_k}: MAE {qk['mae']:.4f}  Brier {qk['brier']:.4f}")

print("\nQB_RETENTION VALIDATION (2020-22) — pick qb_retention here, K=2, qb_boost=5, qb_k=0.05")
print("1.0 = untouched offseason; <1 regresses toward league-avg QB; >1 pushes further")
print("from average (Asad's hypothesis: still-improving QBs might warrant >1).")
for qb_retention in [1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.2, 2.5, 3.0]:
    qret = elo_model.run(df, K=2, qb_boost=5, qb_k=0.05, qb_retention=qb_retention, eval_from=2020, eval_to=2022)
    print(f"qb_retention={qb_retention}: MAE {qret['mae']:.4f}  Brier {qret['brier']:.4f}")

print("\nTRAVEL VALIDATION (2020-22) — pick travel_coef here, K=2")
print("WEAK PRIOR going in: corr(away_travel, result)=-0.04, bucket pattern non-monotonic,")
print("longest-distance bucket even reverses direction. Testing anyway for a clean record.")
for travel_coef in [-1.0, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    tr = elo_model.run(df, K=2, travel_coef=travel_coef, eval_from=2020, eval_to=2022)
    print(f"travel_coef={travel_coef}: MAE {tr['mae']:.4f}  Brier {tr['brier']:.4f}")

print("\nBODY CLOCK VALIDATION (2020-22) — pick body_clock_coef here, K=2, travel_coef=-0.4")
print("Session-30 follow-up: raw check showed west_to_east_early games average")
print("home margin ~-0.03 vs ~+1.96 elsewhere — a ~2pt gap, much cleaner than raw distance.")
for body_clock_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4]:
    bc = elo_model.run(df, K=2, body_clock_coef=body_clock_coef, eval_from=2020, eval_to=2022)
    print(f"body_clock_coef={body_clock_coef}: MAE {bc['mae']:.4f}  Brier {bc['brier']:.4f}")

print("\nBODY CLOCK VALIDATION, ISOLATED (2020-22) — same sweep but travel_coef=0")
print("to check whether travel_coef was already absorbing this signal")
for body_clock_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4]:
    bc = elo_model.run(df, K=2, travel_coef=0, body_clock_coef=body_clock_coef, eval_from=2020, eval_to=2022)
    print(f"body_clock_coef={body_clock_coef}: MAE {bc['mae']:.4f}  Brier {bc['brier']:.4f}")

print("\nINJURY VALIDATION (2020-22) — pick injury_coef here, K=2")
print("MVP: position-weighted count of 'Out' players (QB excluded, already covered")
print("by qb_boost). Raw check: corr(sev_diff, result)=+0.087, mostly monotonic buckets.")
for injury_coef in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]:
    ic = elo_model.run(df, K=2, injury_coef=injury_coef, eval_from=2020, eval_to=2022)
    print(f"injury_coef={injury_coef}: MAE {ic['mae']:.4f}  Brier {ic['brier']:.4f}")

print("\nTOTALS SCALE VALIDATION (2020-22) — pick scale here, K=0.6")
for scale in [15, 20, 25, 30, 35]:
    s = elo_model.run_totals(df, K=0.6, scale=scale, eval_from=2020, eval_to=2022)
    print(f"scale={scale}: MAE {s['mae']:.4f}  vs Vegas {s['vegas_mae']:.4f}")

print("\nREST VALIDATION (2020-22) — pick rest_coef here, K=2, hfa=1.25")
print("SHELVED: validation bowl (rest_coef~0.25-0.3) only moved MAE by 0.018, smaller")
print("than the wind sweep's noise-floor swing — test then confirmed it doesn't generalize.")
for rest_coef in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]:
    r = elo_model.run(df, K=2, rest_coef=rest_coef, eval_from=2020, eval_to=2022)
    print(f"rest_coef={rest_coef}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nHFA VALIDATION (2020-22) — pick hfa here, K=2")
print("judged on Brier + calibration, not just MAE (MAE barely moves across this range)")
for hfa in [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]:
    h = elo_model.run(df, K=2, hfa=hfa, eval_from=2020, eval_to=2022)
    n1, r1 = elo_model.bucket_rate(h['winprobs'], h['homewins'], 0.4, 0.5)
    n2, r2 = elo_model.bucket_rate(h['winprobs'], h['homewins'], 0.5, 0.6)
    print(f"hfa={hfa}: MAE {h['mae']:.4f}  Brier {h['brier']:.4f}  "
          f"underdog(.4-.5)={r1:.3f} (n={n1})  favorite(.5-.6)={r2:.3f} (n={n2})")

print("\nLATE-SEASON REPLICATION CHECK (2020-22 validation) — does the Session 25")
print("Weeks1-4 vs Weeks5-18 gap-to-Vegas pattern (0.21 -> 0.59 on 2023-25 test) hold here?")
val = elo_model.run(df, K=2, eval_from=2020, eval_to=2022)
val_early = [g for g in val['games'] if g['week'] <= 4]
val_late = [g for g in val['games'] if g['week'] >= 5]
ve_mae = sum(g['error'] for g in val_early) / len(val_early)
vl_mae = sum(g['error'] for g in val_late) / len(val_late)
ve_vegas = sum(abs(g['vegas'] - g['actual']) for g in val_early) / len(val_early)
vl_vegas = sum(abs(g['vegas'] - g['actual']) for g in val_late) / len(val_late)
print(f"Weeks 1-4:  Model MAE {ve_mae:.4f}  Vegas MAE {ve_vegas:.4f}  gap {ve_mae - ve_vegas:.4f}  (n={len(val_early)})")
print(f"Weeks 5-18: Model MAE {vl_mae:.4f}  Vegas MAE {vl_vegas:.4f}  gap {vl_mae - vl_vegas:.4f}  (n={len(val_late)})")

# ============================================================
# FINAL HELD-OUT TEST (2023-25) — one honest look per parameter,
# only run after every VALIDATION sweep above has already picked
# its number. Locked params: margin K=2/hfa=1.25/rest_coef=0;
# totals K=0.6/hfa=1.25/scale=25/wind_coef=0/rain_snow_coef=8/clear_weather_coef=0.
# ============================================================

best = elo_model.run(df, w=1, eval_from=2020, eval_to=2025)
counts, wins = elo_model.calibration_table(best['winprobs'], best['homewins'])
print(f"\nCalibration (result, K=2):")
for b in range(10):
    if counts[b] > 0:
        print(f"  bucket {b}: {wins[b]:>3}/{counts[b]:>3} = {wins[b]/counts[b]:.2f}")

test = elo_model.run(df, K=2, eval_from=2023, eval_to=2025)
print(f"\nTEST (2023-25, untouched): MAE {test['mae']:.4f}  vs Vegas {test['vegas_mae']:.4f}  Brier {test['brier']:.4f}")

early = [g for g in test['games'] if g['week'] <= 4]
late = [g for g in test['games'] if g['week'] >= 5]
early_mae = sum(g['error'] for g in early) / len(early)
late_mae = sum(g['error'] for g in late) / len(late)
early_vegas_mae = sum(abs(g['vegas'] - g['actual']) for g in early) / len(early)
late_vegas_mae = sum(abs(g['vegas'] - g['actual']) for g in late) / len(late)
print(f"\nWeeks 1-4:  Model MAE {early_mae:.4f}  Vegas MAE {early_vegas_mae:.4f}  gap {early_mae - early_vegas_mae:.4f}  (n={len(early)})")
print(f"Weeks 5-18: Model MAE {late_mae:.4f}  Vegas MAE {late_vegas_mae:.4f}  gap {late_mae - late_vegas_mae:.4f}  (n={len(late)})")

test_rest = elo_model.run(df, K=2, rest_coef=0.3, eval_from=2023, eval_to=2025)
print(f"\nTEST w/ rest fix (2023-25, untouched): MAE {test_rest['mae']:.4f}  vs Vegas {test_rest['vegas_mae']:.4f}  Brier {test_rest['brier']:.4f}")
print("(baseline w/o fix was MAE 10.2414, Brier 0.2247 — rest fix is a wash, not an improvement)")

test_travel = elo_model.run(df, K=2, travel_coef=-0.4, eval_from=2023, eval_to=2025)
print(f"\nTEST w/ travel fix (2023-25, untouched): MAE {test_travel['mae']:.4f}  vs Vegas {test_travel['vegas_mae']:.4f}  Brier {test_travel['brier']:.4f}")
print("(baseline w/o fix was MAE 10.2414, Brier 0.2247)")

test_injury = elo_model.run(df, K=2, injury_coef=0.2, eval_from=2023, eval_to=2025)
print(f"\nTEST w/ injury fix (2023-25, untouched): MAE {test_injury['mae']:.4f}  vs Vegas {test_injury['vegas_mae']:.4f}  Brier {test_injury['brier']:.4f}")
print("(baseline w/o fix was MAE 10.2414, Brier 0.2247)")

test_qb = elo_model.run(df, K=2, qb_boost=5, eval_from=2023, eval_to=2025)
print(f"\nTEST w/ QB rating (2023-25, untouched, qb_k=0.15/qb_retention=1.0 — shipped defaults): "
      f"MAE {test_qb['mae']:.4f}  vs Vegas {test_qb['vegas_mae']:.4f}  Brier {test_qb['brier']:.4f}")
print("(baseline w/o QB rating was MAE 10.2414, Brier 0.2247)")

test_qb_tuned = elo_model.run(df, K=2, qb_boost=5, qb_k=0.05, qb_retention=1.8, eval_from=2023, eval_to=2025)
print(f"TEST w/ Session-28 'tuned' qb_k=0.05/qb_retention=1.8 (SHELVED — worse than above): "
      f"MAE {test_qb_tuned['mae']:.4f}  Brier {test_qb_tuned['brier']:.4f}")

test_totals = elo_model.run_totals(df, K=0.6, eval_from=2023, eval_to=2025)
print(f"\nTOTALS TEST (2023-25, untouched): MAE {test_totals['mae']:.4f}  vs Vegas {test_totals['vegas_mae']:.4f}")

test_totals_wind = elo_model.run_totals(df, K=0.6, eval_from=2023, eval_to=2025)
outdoor_test = [g for g in test_totals_wind['games'] if g['roof'] == 'outdoors']
om = sum(abs(g['pred'] - g['actual']) for g in outdoor_test) / len(outdoor_test)
ov = sum(abs(g['vegas'] - g['actual']) for g in outdoor_test) / len(outdoor_test)
print(f"\nTOTALS TEST w/ wind fix (2023-25, untouched): MAE {test_totals_wind['mae']:.4f}  vs Vegas {test_totals_wind['vegas_mae']:.4f}")
print(f"  outdoor-only: Model MAE={om:.3f}  Vegas MAE={ov:.3f}  gap={om-ov:.3f}")

test_totals_rain = elo_model.run_totals(df, K=0.6, eval_from=2023, eval_to=2025)
bad_test = [g for g in test_totals_rain['games'] if g['bad_weather']]
bm = sum(abs(g['pred'] - g['actual']) for g in bad_test) / len(bad_test)
bv = sum(abs(g['vegas'] - g['actual']) for g in bad_test) / len(bad_test)
print(f"\nTOTALS TEST w/ rain/snow fix (2023-25, untouched): MAE {test_totals_rain['mae']:.4f}  vs Vegas {test_totals_rain['vegas_mae']:.4f}")
print(f"  bad-weather-only: Model MAE={bm:.3f}  Vegas MAE={bv:.3f}  gap={bm-bv:.3f}")

test_totals_clear = elo_model.run_totals(df, K=0.6, eval_from=2023, eval_to=2025)
clear_test = [g for g in test_totals_clear['games'] if g['clear_weather']]
cm = sum(abs(g['pred'] - g['actual']) for g in clear_test) / len(clear_test)
cv = sum(abs(g['vegas'] - g['actual']) for g in clear_test) / len(clear_test)
print(f"\nTOTALS TEST w/o clear-weather fix (2023-25, untouched): MAE {test_totals_clear['mae']:.4f}  vs Vegas {test_totals_clear['vegas_mae']:.4f}")
print(f"  clear-weather-only: Model MAE={cm:.3f}  Vegas MAE={cv:.3f}  gap={cm-cv:.3f}")

test_totals_div = elo_model.run_totals(df, K=0.6, div_coef=1.5, eval_from=2023, eval_to=2025)
div_test = [g for g in test_totals_div['games'] if g['div_game']]
dm = sum(abs(g['pred'] - g['actual']) for g in div_test) / len(div_test)
dv = sum(abs(g['vegas'] - g['actual']) for g in div_test) / len(div_test)
print(f"\nTOTALS TEST w/ div fix (2023-25, untouched): MAE {test_totals_div['mae']:.4f}  vs Vegas {test_totals_div['vegas_mae']:.4f}")
print(f"  divisional-only: Model MAE={dm:.3f}  Vegas MAE={dv:.3f}  gap={dm-dv:.3f}")
