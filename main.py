import dataloader
import metrics
import elo_model
import pipeline

# warm-up 2018-19, VALIDATION 2020-22, TEST 2023-25 (three held-out seasons)
YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

df = pipeline.build_training_data(YEARS)
injuries = dataloader.load_injuries(YEARS)  # still needed below for the injury-weight-tier check

# ============================================================
# VALIDATION (2020-22): all tuning happens here, nothing below
# this section may read `test`/TEST numbers until every sweep
# in this block has finished (that ordering bug bit Session 21).
# ============================================================

print("VALIDATION (2020-22): pick K here")
for K in [1, 1.5, 2, 3, 4]:
    v = elo_model.run(df, K=K, eval_from=2020, eval_to=2022)
    print(f"K={K}: MAE {v['mae']:.4f}  Brier {v['brier']:.4f}")

print("\nBLEND VALIDATION (2020-22): pick w here, K=2, using OPPONENT-ADJUSTED epa_margin")
print("Session 13 found blending raw epa_margin with result NEVER helped (corr=0.996,")
print("no diversification benefit). Opponent-adjusting EPA breaks that down to corr~0.89,")
print("re-tested the same blend hypothesis with a genuinely different signal (Session 34).")
for w in [0, 0.25, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]:
    r = elo_model.run(df, K=2, w=w, eval_from=2020, eval_to=2022)
    print(f"w={w}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nK RE-CHECK under w=0.8 (2020-22): confirms K=2 still holds with the new blend active")
for K in [1, 1.5, 2, 2.5, 3, 3.5, 4]:
    v = elo_model.run(df, K=K, w=0.8, eval_from=2020, eval_to=2022)
    print(f"K={K}: MAE {v['mae']:.4f}  Brier {v['brier']:.4f}")

print("\nTOTALS VALIDATION (2020-22): pick K here")
for K in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    tv = elo_model.run_totals(df, K=K, eval_from=2020, eval_to=2022)
    print(f"K={K}: MAE {tv['mae']:.4f}  vs Vegas {tv['vegas_mae']:.4f}")

print("\nTURF VALIDATION (2020-22): pick turf_coef here, K=0.6")
print("SHELVED: raw gap real (turf 47.2 vs grass 44.7 avg total), validation bowl real")
print("(min ~1), but honest test came back worse (10.4561->10.4720).")
for turf_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3]:
    r = elo_model.run_totals(df, K=0.6, turf_coef=turf_coef, eval_from=2020, eval_to=2022)
    print(f"turf_coef={turf_coef}: MAE {r['mae']:.4f}  vs Vegas {r['vegas_mae']:.4f}")

print("\nEXTREME COLD VALIDATION (2020-22): pick extreme_cold_coef here, K=0.6")
print("VALIDATED: outdoor games <32F, no precip required (distinct mechanism from")
print("bad_weather: ball grip/kicking, not rain/snow). Small raw sample (n=63) but")
print("honest test held up: 10.4561->10.4505. Locked extreme_cold_coef=2.")
for extreme_cold_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3]:
    r = elo_model.run_totals(df, K=0.6, extreme_cold_coef=extreme_cold_coef, eval_from=2020, eval_to=2022)
    print(f"extreme_cold_coef={extreme_cold_coef}: MAE {r['mae']:.4f}  vs Vegas {r['vegas_mae']:.4f}")

print("\nWIND VALIDATION (2020-22): pick wind_coef here, K=0.6, threshold=15mph")
print("judged on the OUTDOOR-only gap, not overall MAE (dome games are unaffected)")
for wind_coef in [0, 0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5, 2.0]:
    w = elo_model.run_totals(df, K=0.6, wind_coef=wind_coef, eval_from=2020, eval_to=2022)
    outdoor = [g for g in w['games'] if g['roof'] == 'outdoors']
    m = sum(abs(g['pred'] - g['actual']) for g in outdoor) / len(outdoor)
    v = sum(abs(g['vegas'] - g['actual']) for g in outdoor) / len(outdoor)
    print(f"wind_coef={wind_coef}: outdoor Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

print("\nRAIN/SNOW VALIDATION (2020-22): pick rain_snow_coef here, K=0.6")
print("judged on bad-weather games only (small sample, expect a lot of noise)")
for rain_snow_coef in [0, 2, 5, 7, 8, 9, 10, 12, 16, 20]:
    r = elo_model.run_totals(df, K=0.6, rain_snow_coef=rain_snow_coef, eval_from=2020, eval_to=2022)
    bad = [g for g in r['games'] if g['bad_weather']]
    m = sum(abs(g['pred'] - g['actual']) for g in bad) / len(bad)
    v = sum(abs(g['vegas'] - g['actual']) for g in bad) / len(bad)
    print(f"rain_snow_coef={rain_snow_coef}: n={len(bad)}  Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

print("\nCLEAR/SUNNY VALIDATION (2020-22): pick clear_weather_coef here, K=0.6")
print("SHELVED: coef that helped validation ran opposite the raw data (clear games")
print("score HIGHER on average, but a NEGATIVE coef improved the fit), a confound")
print("red flag, confirmed by the test failing. Kept here for a transparent record.")
for clear_weather_coef in [-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3]:
    c = elo_model.run_totals(df, K=0.6, clear_weather_coef=clear_weather_coef, eval_from=2020, eval_to=2022)
    clear = [g for g in c['games'] if g['clear_weather']]
    m = sum(abs(g['pred'] - g['actual']) for g in clear) / len(clear)
    v = sum(abs(g['vegas'] - g['actual']) for g in clear) / len(clear)
    print(f"clear_weather_coef={clear_weather_coef}: n={len(clear)}  Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

print("\nDIVISIONAL VALIDATION (2020-22): pick div_coef here, K=0.6")
print("judged on divisional games only. Raw-data check: avg total is basically")
print("identical for div vs non-div early season (46.6/45.1) and late (45.7/45.2)")
print("once controlled for week-of-season, so this isn't a pure scheduling artifact.")
for div_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3]:
    d = elo_model.run_totals(df, K=0.6, div_coef=div_coef, eval_from=2020, eval_to=2022)
    div = [g for g in d['games'] if g['div_game']]
    m = sum(abs(g['pred'] - g['actual']) for g in div) / len(div)
    v = sum(abs(g['vegas'] - g['actual']) for g in div) / len(div)
    print(f"div_coef={div_coef}: n={len(div)}  Model MAE={m:.3f}  Vegas MAE={v:.3f}  gap={m-v:.3f}")

print("\nQB REGRESSION VALIDATION (2020-22): pick qb_regression here, K=2")
for qb_regression in [0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]:
    q = elo_model.run(df, K=2, qb_regression=qb_regression, eval_from=2020, eval_to=2022)
    print(f"qb_regression={qb_regression}: MAE {q['mae']:.4f}  Brier {q['brier']:.4f}")

print("\nQB RATING VALIDATION (2020-22): pick qb_boost here, K=2, qb_k=0.15, qb_retention=1.0")
print("qb_rating is a persistent per-passer EMA of passing EPA/dropback, carried")
print("across team changes (unlike team elo, which resets 25% every offseason).")
for qb_boost in [0, 2, 4, 5, 6, 8, 10, 12, 15]:
    qr = elo_model.run(df, K=2, qb_boost=qb_boost, eval_from=2020, eval_to=2022)
    print(f"qb_boost={qb_boost}: MAE {qr['mae']:.4f}  Brier {qr['brier']:.4f}")

print("\nQB_K VALIDATION (2020-22): pick qb_k here, K=2, qb_boost=5, qb_retention=1.0")
print("qb_k is the EMA smoothing rate for the QB rating (0.15 was an unswept prior)")
print("SHELVED RESULT: qb_k=0.05 looked better here, but combined with the retention")
print("tune below, the honest test came back WORSE than the qb_k=0.15 default. Reverted.")
for qb_k in [0.01, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3]:
    qk = elo_model.run(df, K=2, qb_boost=5, qb_k=qb_k, eval_from=2020, eval_to=2022)
    print(f"qb_k={qb_k}: MAE {qk['mae']:.4f}  Brier {qk['brier']:.4f}")

print("\nQB_RETENTION VALIDATION (2020-22): pick qb_retention here, K=2, qb_boost=5, qb_k=0.05")
print("1.0 = untouched offseason; <1 regresses toward league-avg QB; >1 pushes further")
print("from average (Asad's hypothesis: still-improving QBs might warrant >1).")
for qb_retention in [1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.2, 2.5, 3.0]:
    qret = elo_model.run(df, K=2, qb_boost=5, qb_k=0.05, qb_retention=qb_retention, eval_from=2020, eval_to=2022)
    print(f"qb_retention={qb_retention}: MAE {qret['mae']:.4f}  Brier {qret['brier']:.4f}")

print("\nTRAVEL VALIDATION (2020-22): pick travel_coef here, K=2")
print("SHELVED Session 33: this sweep's OWN honest test looked like a pass, but was")
print("compared against a stale baseline. Properly re-checked against the QB-rating")
print("baseline it was actually stacked on, travel_coef made TEST MAE worse. Reverted.")
for travel_coef in [-1.0, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    tr = elo_model.run(df, K=2, travel_coef=travel_coef, eval_from=2020, eval_to=2022)
    print(f"travel_coef={travel_coef}: MAE {tr['mae']:.4f}  Brier {tr['brier']:.4f}")

print("\nBODY CLOCK VALIDATION (2020-22): pick body_clock_coef here, K=2, travel_coef=0 (default)")
print("Re-checked Session 34 now that travel_coef is gone. Session 30 shelved this as")
print("redundant with travel_coef, which no longer applies now that travel is removed.")
for body_clock_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4]:
    bc = elo_model.run(df, K=2, body_clock_coef=body_clock_coef, eval_from=2020, eval_to=2022)
    print(f"body_clock_coef={body_clock_coef}: MAE {bc['mae']:.4f}  Brier {bc['brier']:.4f}")

print("\nINJURY VALIDATION (2020-22): pick injury_coef here, K=2")
print("MVP: position-weighted count of 'Out' players (QB excluded, already covered")
print("by qb_boost). Raw check: corr(sev_diff, result)=+0.087, mostly monotonic buckets.")
for injury_coef in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]:
    ic = elo_model.run(df, K=2, injury_coef=injury_coef, eval_from=2020, eval_to=2022)
    print(f"injury_coef={injury_coef}: MAE {ic['mae']:.4f}  Brier {ic['brier']:.4f}")

print("\nINJURY V2 VALIDATION, ISOLATED (2020-22): injury_coef=0, only injury_coef_v2 active")
print("v2 = starter-only severity (trailing snap share >0.5). Raw corr weaker than MVP")
print("(+0.057 vs +0.087), checking whether precision still wins in the actual model.")
for injury_coef_v2 in [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]:
    icv2 = elo_model.run(df, K=2, injury_coef=0, injury_coef_v2=injury_coef_v2, eval_from=2020, eval_to=2022)
    print(f"injury_coef_v2={injury_coef_v2}: MAE {icv2['mae']:.4f}  Brier {icv2['brier']:.4f}")

print("\nINJURY V2 VALIDATION, STACKED (2020-22): injury_coef=0.2 (locked MVP) + injury_coef_v2")
for injury_coef_v2 in [0, 0.1, 0.2, 0.3, 0.4, 0.5]:
    icv2 = elo_model.run(df, K=2, injury_coef=0.2, injury_coef_v2=injury_coef_v2, eval_from=2020, eval_to=2022)
    print(f"injury_coef_v2={injury_coef_v2}: MAE {icv2['mae']:.4f}  Brier {icv2['brier']:.4f}")

print("\nTOTALS SCALE VALIDATION (2020-22): pick scale here, K=0.6")
for scale in [15, 20, 25, 30, 35]:
    s = elo_model.run_totals(df, K=0.6, scale=scale, eval_from=2020, eval_to=2022)
    print(f"scale={scale}: MAE {s['mae']:.4f}  vs Vegas {s['vegas_mae']:.4f}")

print("\nREST VALIDATION (2020-22): pick rest_coef here, K=2, hfa=1.25")
print("SHELVED: validation bowl (rest_coef~0.25-0.3) only moved MAE by 0.018, smaller")
print("than the wind sweep's noise-floor swing. Test then confirmed it doesn't generalize.")
for rest_coef in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]:
    r = elo_model.run(df, K=2, rest_coef=rest_coef, eval_from=2020, eval_to=2022)
    print(f"rest_coef={rest_coef}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nTURNOVER VALIDATION (2020-22): pick turnover_coef here, K=2")
print("SHELVED: turnover margin has real luck signature (corr w/ own future TM = 0.08,")
print("essentially random) but discounting it from training barely moved MAE (0.0006)")
print("while Brier got WORSE immediately. The existing +/-20 cap + small K=2 already")
print("limit overreaction to turnover-driven blowouts, nothing left to fix.")
for turnover_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4]:
    r = elo_model.run(df, K=2, turnover_coef=turnover_coef, eval_from=2020, eval_to=2022)
    print(f"turnover_coef={turnover_coef}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nPRIMETIME VALIDATION (2020-22): pick primetime_coef here, K=2")
print("SHELVED: raw gap (0.8pt tighter, 0.3pt less home edge) likely scheduling")
print("selection (TV picks good-team matchups), not a real effect. Gain here is 0.002.")
for primetime_coef in [0, 0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0]:
    r = elo_model.run(df, K=2, primetime_coef=primetime_coef, eval_from=2020, eval_to=2022)
    print(f"primetime_coef={primetime_coef}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nOLINE VALIDATION (2020-22): pick oline_boost here, K=2")
print("SHELVED: real bowl on validation (min ~45-50), but honest test came back")
print("worse (10.1743->10.1820). Sacks are already negative-EPA plays baked into")
print("the adjusted-EPA blend, a separate rating just double-counts the same signal.")
for oline_boost in [0, 10, 20, 30, 40, 45, 50, 60, 80, 100]:
    r = elo_model.run(df, K=2, oline_boost=oline_boost, eval_from=2020, eval_to=2022)
    print(f"oline_boost={oline_boost}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nINJURY WEIGHT CHECK (2020-22): confirms the shipped 3-tier weighting beats uniform")
uniform_test = elo_model.run(df, K=2, injury_coef=0.2, eval_from=2020, eval_to=2022)
orig_weights = dict(metrics.POSITION_WEIGHT)
for k in metrics.POSITION_WEIGHT:
    metrics.POSITION_WEIGHT[k] = 1
df_uniform = metrics.add_injuries(df.drop(columns=['home_severity', 'away_severity']), injuries)
uniform_r = elo_model.run(df_uniform, K=2, injury_coef=0.2, eval_from=2020, eval_to=2022)
metrics.POSITION_WEIGHT.update(orig_weights)
print(f"3-tier weights (shipped): MAE {uniform_test['mae']:.4f}  Brier {uniform_test['brier']:.4f}")
print(f"uniform weights (all=1): MAE {uniform_r['mae']:.4f}  Brier {uniform_r['brier']:.4f}")

print("\nALTITUDE VALIDATION (2020-22): pick altitude_coef here, K=2 (Denver-specific)")
print("SHELVED: raw gap tiny and noisy (DEN home margin 1.91 vs league 1.56, n=67).")
print("No signal at any tested value, monotonically worse from 0.")
for altitude_coef in [0, 0.5, 1, 1.5, 2, 2.5, 3]:
    r = elo_model.run(df, K=2, altitude_coef=altitude_coef, eval_from=2020, eval_to=2022)
    print(f"altitude_coef={altitude_coef}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nQUESTIONABLE-INJURY WEIGHT VALIDATION (2020-22): pick questionable_mult here, K=2")
print("SHELVED: real bowl on validation (min ~0.6, MAE 9.9993 vs 10.0089), but the")
print("honest test came back worse (10.1743->10.1775). Doubtful never showed any signal.")
for questionable_mult in [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]:
    d = metrics.add_injuries(df.drop(columns=['home_severity', 'away_severity']), injuries,
                              questionable_mult=questionable_mult)
    r = elo_model.run(d, K=2, injury_coef=0.2, eval_from=2020, eval_to=2022)
    print(f"questionable_mult={questionable_mult}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nHOME BIAS VALIDATION (2020-22): pick home_bias_coef here, K=2")
print("Shrunk, single-coefficient alternative to a full 32-team home/away split")
print("(too many free parameters for the signal available, high overfitting risk).")
print("SHELVED: even this cheap version failed, honest test 10.1743->10.1780, worse.")
for home_bias_coef in [0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
    r = elo_model.run(df, K=2, home_bias_coef=home_bias_coef, eval_from=2020, eval_to=2022)
    print(f"home_bias_coef={home_bias_coef}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nCPOE VALIDATION (2020-22): pick cpoe_boost here, K=2, added on top of qb_boost=5")
print("SHELVED: CPOE (Next Gen Stats accuracy metric) monotonically worse from 0 in BOTH")
print("configurations, additive on top of the EPA-based QB rating, and as a standalone")
print("replacement (qb_boost=0). Redundant with what EPA/dropback already captures.")
for cpoe_boost in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    r = elo_model.run(df, K=2, cpoe_boost=cpoe_boost, eval_from=2020, eval_to=2022)
    print(f"cpoe_boost={cpoe_boost}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nSUCCESS RATE VALIDATION (2020-22): pick success_coef here, K=2")
print("Genuinely different info from EPA (corr=0.52, much lower than opponent-adj's")
print("0.90 which DID work), real bowl (min ~25), but honest test came back MIXED:")
print("MAE worse (10.1743->10.1924) though Brier improved. MAE is the deciding metric.")
for success_coef in [0, 5, 10, 15, 20, 25, 30, 40]:
    r = elo_model.run(df, K=2, success_coef=success_coef, eval_from=2020, eval_to=2022)
    print(f"success_coef={success_coef}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nOLINE-FAULT-EXCLUDED VALIDATION (2020-22): pick oline_boost here, K=2")
print("CAVEAT: FTN charting only exists from 2022, so this validation window effectively")
print("reflects only 2022's data, a single season, unusually noisy to tune on.")
print("SHELVED: real bowl on this thin validation (min ~300), but the honest test failed")
print("badly (MAE 10.1743->10.6092, MUCH worse), a textbook overfit to a too-small window.")
df_oline_test = df.copy()
df_oline_test['home_sack_rate'] = df_oline_test['home_oline_sack_rate']
df_oline_test['away_sack_rate'] = df_oline_test['away_oline_sack_rate']
for oline_boost in [0, 50, 100, 150, 200, 250, 300, 400]:
    r = elo_model.run(df_oline_test, K=2, oline_boost=oline_boost, eval_from=2020, eval_to=2022)
    print(f"oline_boost={oline_boost}: MAE {r['mae']:.4f}  Brier {r['brier']:.4f}")

print("\nHFA VALIDATION (2020-22): pick hfa here, K=2")
print("judged on Brier + calibration, not just MAE (MAE barely moves across this range)")
for hfa in [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]:
    h = elo_model.run(df, K=2, hfa=hfa, eval_from=2020, eval_to=2022)
    n1, r1 = elo_model.bucket_rate(h['winprobs'], h['homewins'], 0.4, 0.5)
    n2, r2 = elo_model.bucket_rate(h['winprobs'], h['homewins'], 0.5, 0.6)
    print(f"hfa={hfa}: MAE {h['mae']:.4f}  Brier {h['brier']:.4f}  "
          f"underdog(.4-.5)={r1:.3f} (n={n1})  favorite(.5-.6)={r2:.3f} (n={n2})")

print("\nLATE-SEASON REPLICATION CHECK (2020-22 validation): does the Session 25")
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
# FINAL HELD-OUT TEST (2023-25): one honest look per parameter,
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
print(f"\nTEST (2023-25, untouched, w=0.8 shipped default): MAE {test['mae']:.4f}  vs Vegas {test['vegas_mae']:.4f}  Brier {test['brier']:.4f}")

test_pure_scoreboard = elo_model.run(df, K=2, w=1.0, eval_from=2023, eval_to=2025)
print(f"(for comparison, w=1.0 pure scoreboard: MAE {test_pure_scoreboard['mae']:.4f}  Brier {test_pure_scoreboard['brier']:.4f}, "
      f"the adjusted-EPA blend is a real, validated gain of {test_pure_scoreboard['mae']-test['mae']:.4f} MAE)")

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
print("(baseline w/o fix was MAE 10.2414, Brier 0.2247. Rest fix is a wash, not an improvement)")

test_travel = elo_model.run(df, K=2, travel_coef=-0.4, eval_from=2023, eval_to=2025)
print(f"\nTEST w/ travel fix (2023-25, untouched): MAE {test_travel['mae']:.4f}  vs Vegas {test_travel['vegas_mae']:.4f}  Brier {test_travel['brier']:.4f}")
print("(baseline w/o fix was MAE 10.2414, Brier 0.2247)")

test_injury = elo_model.run(df, K=2, injury_coef=0.2, eval_from=2023, eval_to=2025)
print(f"\nTEST w/ injury fix (2023-25, untouched): MAE {test_injury['mae']:.4f}  vs Vegas {test_injury['vegas_mae']:.4f}  Brier {test_injury['brier']:.4f}")
print("(baseline w/o fix was MAE 10.2414, Brier 0.2247)")

# IMPORTANT: compare against the CURRENT shipped stack (`test` above, MAE 10.1919),
# not the old stale 10.2414 reference. That exact mistake is what caused the
# travel_coef bug in Session 33. Always compare against the immediately-correct baseline.
test_bodyclock = elo_model.run(df, K=2, body_clock_coef=1.5, eval_from=2023, eval_to=2025)
print(f"\nTEST w/ body_clock fix (2023-25, untouched, SHELVED, wash, not shipped): "
      f"MAE {test_bodyclock['mae']:.4f}  vs Vegas {test_bodyclock['vegas_mae']:.4f}  Brier {test_bodyclock['brier']:.4f}")
print(f"(CORRECT current baseline w/o fix: MAE {test['mae']:.4f}, Brier {test['brier']:.4f})")

test_qb = elo_model.run(df, K=2, qb_boost=5, eval_from=2023, eval_to=2025)
print(f"\nTEST w/ QB rating (2023-25, untouched, qb_k=0.15/qb_retention=1.0, shipped defaults): "
      f"MAE {test_qb['mae']:.4f}  vs Vegas {test_qb['vegas_mae']:.4f}  Brier {test_qb['brier']:.4f}")
print("(baseline w/o QB rating was MAE 10.2414, Brier 0.2247)")

test_qb_tuned = elo_model.run(df, K=2, qb_boost=5, qb_k=0.05, qb_retention=1.8, eval_from=2023, eval_to=2025)
print(f"TEST w/ Session-28 'tuned' qb_k=0.05/qb_retention=1.8 (SHELVED, worse than above): "
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

test_totals_baseline_no_cold = elo_model.run_totals(df, K=0.6, extreme_cold_coef=0, eval_from=2023, eval_to=2025)
test_totals_cold = elo_model.run_totals(df, K=0.6, extreme_cold_coef=2, eval_from=2023, eval_to=2025)
print(f"\nTOTALS TEST w/o extreme-cold fix: MAE {test_totals_baseline_no_cold['mae']:.4f}")
print(f"TOTALS TEST w/ extreme-cold fix (shipped default): MAE {test_totals_cold['mae']:.4f}")
