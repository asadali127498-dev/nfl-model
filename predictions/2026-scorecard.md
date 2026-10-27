# 2026 Scorecard

Updated 2026-10-27T17:33:54 (local time). I graded every number here from the prediction files exactly as I posted them, not from a re-run of the model. The Vegas numbers are the closing line from nflverse, and the Vegas win % is the moneyline with the vig taken out.

Each cell is model / Vegas, and lower is better for MAE and Brier. For reference, my margin MAE over the 2023-2025 test seasons was 10.17 and Vegas was 9.74. I don't think a couple of weeks says much of anything yet, so I'm treating this as a running tally.

| Games | n | Straight up | Margin MAE | Brier | Total MAE | Closer than Vegas |
|---|---|---|---|---|---|---|
| Pre-registered only | 77 | 46-31 / 49-28 | 9.28 / 9.40 | 0.219 / 0.226 | 11.19 / 10.58 | 38 of 77 |
| All graded games | 92 | 54-38 / 59-33 | 9.83 / 9.88 | 0.223 / 0.228 | 10.97 / 10.52 | 47 of 92 |
| Week 1 | 16 | 10-6 / 12-4 | 11.82 / 11.28 | 0.232 / 0.214 | 12.24 / 11.69 | 6 of 16 |
| Week 2 (not pre-registered) | 15 | 8-7 / 10-5 | 12.63 / 12.33 | 0.242 / 0.239 | 9.87 / 10.23 | 9 of 15 |
| Week 3 | 16 | 9-7 / 9-7 | 7.96 / 8.09 | 0.218 / 0.254 | 11.04 / 10.94 | 8 of 16 |
| Week 4 | 16 | 10-6 / 9-7 | 6.22 / 7.31 | 0.200 / 0.219 | 12.14 / 9.62 | 11 of 16 |
| Week 5 | 15 | 10-5 / 9-6 | 9.65 / 10.40 | 0.194 / 0.212 | 10.67 / 10.17 | 8 of 15 |
| Week 7 | 14 | 7-7 / 10-4 | 11.01 / 10.07 | 0.253 / 0.231 | 9.59 / 10.43 | 5 of 14 |

Pre-registered means I committed that week's file before the game kicked off. I pushed the Week 2 file after its games were already played, so I'm still grading it to keep the record complete, but it doesn't count toward the top row.

## Week 1

File first committed 2026-09-09 07:02 UTC-04:00.

| Game | Final | Model margin | Vegas line | Result | Model err | Vegas err | Model win % | Vegas win % | SU pick |
|---|---|---|---|---|---|---|---|---|---|
| NE @ SEA | NE 10 - 13 SEA | +2.1 | +3.0 | +3 | 0.9 | 0.0 | 55.2% | 60.0% | SEA (yes) |
| SF @ LA | SF 27 - 7 LA | +2.6 | +3.5 | -20 | 22.6 | 23.5 | 56.4% | 65.7% | LA (no) |
| NYJ @ TEN | NYJ 23 - 10 TEN | +3.5 | +1.5 | -13 | 16.5 | 14.5 | 58.8% | 51.7% | TEN (no) |
| ATL @ PIT | ATL 13 - 20 PIT | +3.0 | +6.5 | +7 | 4.0 | 0.5 | 57.4% | 71.8% | PIT (yes) |
| BAL @ IND | BAL 41 - 23 IND | -1.5 | -3.0 | -18 | 16.5 | 15.0 | 46.2% | 40.7% | BAL (yes) |
| BUF @ HOU | BUF 36 - 31 HOU | +0.4 | -1.5 | -5 | 5.4 | 3.5 | 51.0% | 49.6% | HOU (no) |
| NO @ DET | NO 30 - 31 DET | +7.0 | +7.0 | +1 | 6.0 | 6.0 | 67.0% | 73.4% | DET (yes) |
| TB @ CIN | TB 27 - 33 CIN | +3.0 | +3.5 | +6 | 3.0 | 2.5 | 57.6% | 64.5% | CIN (yes) |
| CHI @ CAR | CHI 59 - 37 CAR | -2.9 | -3.0 | -22 | 19.1 | 19.0 | 42.7% | 40.0% | CHI (yes) |
| CLE @ JAX | CLE 10 - 34 JAX | +10.3 | +8.5 | +24 | 13.7 | 15.5 | 74.0% | 79.1% | JAX (yes) |
| WAS @ PHI | WAS 22 - 24 PHI | +3.5 | +6.0 | +2 | 1.5 | 4.0 | 58.7% | 68.1% | PHI (yes) |
| GB @ MIN | GB 22 - 39 MIN | +2.7 | +1.5 | +17 | 14.3 | 15.5 | 56.7% | 53.2% | MIN (yes) |
| ARI @ LAC | ARI 26 - 14 LAC | +5.8 | +8.5 | -12 | 17.8 | 20.5 | 64.1% | 78.7% | LAC (no) |
| MIA @ LV | MIA 13 - 27 LV | -3.2 | +3.0 | +14 | 17.2 | 11.0 | 42.0% | 60.4% | MIA (no) |
| DAL @ NYG | DAL 20 - 28 NYG | +1.3 | -3.0 | +8 | 6.7 | 11.0 | 53.2% | 40.0% | NYG (yes) |
| DEN @ KC | DEN 10 - 31 KC | -2.9 | +2.5 | +21 | 23.9 | 18.5 | 42.7% | 54.3% | DEN (no) |

## Week 2

File first committed 2026-09-24 19:17 UTC-04:00.

| Game | Final | Model margin | Vegas line | Result | Model err | Vegas err | Model win % | Vegas win % | SU pick |
|---|---|---|---|---|---|---|---|---|---|
| PHI @ TEN | PHI 24 - 20 TEN | -5.9 | -7.0 | -4 | 1.9 | 3.0 | 35.5% | 26.6% | PHI (yes) |
| MIN @ CHI | MIN 9 - 3 CHI | +2.7 | +4.5 | -6 | 8.7 | 10.5 | 56.8% | 65.7% | CHI (no) |
| GB @ NYJ | GB 20 - 17 NYJ | -5.3 | -3.5 | -3 | 2.3 | 0.5 | 37.0% | 37.8% | GB (yes) |
| PIT @ NE | PIT 3 - 20 NE | +4.7 | +4.5 | +17 | 12.3 | 12.5 | 61.6% | 66.4% | NE (yes) |
| CIN @ HOU | CIN 20 - 6 HOU | +1.4 | +3.0 | -14 | 15.4 | 17.0 | 53.5% | 57.2% | HOU (no) |
| NO @ BAL | NO 24 - 17 BAL | +7.0 | +8.5 | -7 | 14.0 | 15.5 | 67.0% | 75.7% | BAL (no) |
| CAR @ ATL | CAR 34 - 3 ATL | +2.5 | -2.5 | -31 | 33.5 | 28.5 | 56.1% | 41.7% | ATL (no) |
| CLE @ TB | CLE 23 - 19 TB | +4.9 | +8.5 | -4 | 8.9 | 12.5 | 62.0% | 77.7% | TB (no) |
| JAX @ DEN | JAX 13 - 20 DEN | -4.1 | +2.5 | +7 | 11.1 | 4.5 | 39.9% | 57.2% | JAX (no) |
| LV @ LAC | LV 26 - 14 LAC | +4.4 | +6.5 | -12 | 16.4 | 18.5 | 60.8% | 73.4% | LAC (no) |
| MIA @ SF | MIA 13 - 35 SF | +10.9 | +12.5 | +22 | 11.1 | 9.5 | 75.1% | 86.3% | SF (yes) |
| WAS @ DAL | WAS 20 - 37 DAL | +0.4 | +3.5 | +17 | 16.6 | 13.5 | 51.0% | 65.7% | DAL (yes) |
| SEA @ ARI | SEA 31 - 7 ARI | -6.1 | -3.5 | -24 | 17.9 | 20.5 | 35.1% | 34.3% | SEA (yes) |
| IND @ KC | IND 30 - 33 KC | +4.5 | +6.0 | +3 | 1.5 | 3.0 | 61.1% | 69.6% | KC (yes) |
| NYG @ LA | NYG 6 - 28 LA | +4.1 | +6.5 | +22 | 17.9 | 15.5 | 60.0% | 71.8% | LA (yes) |

## Week 3

File first committed 2026-09-24 19:17 UTC-04:00.

| Game | Final | Model margin | Vegas line | Result | Model err | Vegas err | Model win % | Vegas win % | SU pick |
|---|---|---|---|---|---|---|---|---|---|
| ATL @ GB | ATL 35 - 14 GB | +3.3 | +4.5 | -21 | 24.3 | 25.5 | 58.1% | 66.9% | GB (no) |
| SEA @ WAS | SEA 31 - 33 WAS | -6.9 | -8.5 | +2 | 8.9 | 10.5 | 33.4% | 22.8% | SEA (no) |
| CIN @ PIT | CIN 27 - 30 PIT | -1.0 | -3.5 | +3 | 4.0 | 6.5 | 47.4% | 38.4% | CIN (no) |
| NYJ @ DET | NYJ 24 - 31 DET | +8.7 | +7.0 | +7 | 1.7 | 0.0 | 70.6% | 73.4% | DET (yes) |
| KC @ MIA | KC 24 - 10 MIA | -5.5 | -10.0 | -14 | 8.5 | 4.0 | 36.5% | 17.8% | KC (yes) |
| NE @ JAX | NE 6 - 35 JAX | +0.8 | +3.0 | +29 | 28.2 | 26.0 | 52.0% | 59.3% | JAX (yes) |
| HOU @ IND | HOU 17 - 19 IND | -0.2 | -1.5 | +2 | 2.2 | 3.5 | 49.4% | 46.8% | HOU (no) |
| CAR @ CLE | CAR 18 - 21 CLE | -1.5 | -2.5 | +3 | 4.5 | 5.5 | 46.3% | 44.9% | CAR (no) |
| LAC @ BUF | LAC 16 - 24 BUF | +9.4 | +7.0 | +8 | 1.4 | 1.0 | 72.1% | 73.4% | BUF (yes) |
| TEN @ NYG | TEN 7 - 12 NYG | +5.2 | +2.5 | +5 | 0.2 | 2.5 | 62.7% | 54.3% | NYG (yes) |
| MIN @ TB | MIN 23 - 16 TB | -3.8 | -1.5 | -7 | 3.2 | 5.5 | 40.7% | 49.6% | MIN (yes) |
| ARI @ SF | ARI 30 - 36 SF | +11.7 | +7.5 | +6 | 5.7 | 1.5 | 76.8% | 76.6% | SF (yes) |
| LV @ NO | LV 35 - 27 NO | +3.6 | +3.5 | -8 | 11.6 | 11.5 | 58.8% | 63.1% | NO (no) |
| BAL @ DAL | BAL 34 - 31 DAL | -1.7 | -3.0 | -3 | 1.3 | 0.0 | 45.7% | 39.6% | BAL (yes) |
| LA @ DEN | LA 26 - 30 DEN | -0.6 | +1.5 | +4 | 4.6 | 2.5 | 48.5% | 50.4% | LA (no) |
| PHI @ CHI | PHI 7 - 27 CHI | +2.9 | -3.5 | +20 | 17.1 | 23.5 | 57.3% | 36.3% | CHI (yes) |

## Week 4

File first committed 2026-09-30 20:36 UTC-04:00.

| Game | Final | Model margin | Vegas line | Result | Model err | Vegas err | Model win % | Vegas win % | SU pick |
|---|---|---|---|---|---|---|---|---|---|
| PIT @ CLE | PIT 24 - 27 CLE | -2.6 | -2.5 | +3 | 5.6 | 5.5 | 43.5% | 42.8% | PIT (no) |
| IND @ WAS | IND 30 - 13 WAS | +1.1 | -4.5 | -17 | 18.1 | 12.5 | 52.8% | 33.1% | WAS (no) |
| GB @ TB | GB 17 - 14 TB | +0.3 | -3.0 | -3 | 3.3 | 0.0 | 50.6% | 41.7% | TB (no) |
| LA @ PHI | LA 24 - 20 PHI | -3.3 | -3.5 | -4 | 0.7 | 0.5 | 41.9% | 36.3% | LA (yes) |
| ARI @ NYG | ARI 24 - 36 NYG | +2.0 | -2.5 | +12 | 10.0 | 14.5 | 54.9% | 44.9% | NYG (yes) |
| JAX @ CIN | JAX 22 - 17 CIN | -3.1 | +2.5 | -5 | 1.9 | 7.5 | 42.3% | 57.2% | JAX (yes) |
| NYJ @ CHI | NYJ 12 - 23 CHI | +8.4 | +3.5 | +11 | 2.6 | 7.5 | 70.1% | 63.1% | CHI (yes) |
| NE @ BUF | NE 29 - 26 BUF | +3.1 | +7.0 | -3 | 6.1 | 10.0 | 57.7% | 74.4% | BUF (no) |
| TEN @ BAL | TEN 18 - 24 BAL | +10.6 | +11.5 | +6 | 4.6 | 5.5 | 74.5% | 85.2% | BAL (yes) |
| DAL @ HOU | DAL 34 - 30 HOU | +0.9 | +3.0 | -4 | 4.9 | 7.0 | 52.2% | 58.3% | HOU (no) |
| MIA @ MIN | MIA 10 - 15 MIN | +9.7 | +10.0 | +5 | 4.7 | 5.0 | 72.7% | 80.8% | MIN (yes) |
| DEN @ SF | DEN 14 - 24 SF | +5.2 | +3.0 | +10 | 4.8 | 7.0 | 62.7% | 60.0% | SF (yes) |
| LAC @ SEA | LAC 23 - 30 SEA | +9.3 | +7.0 | +7 | 2.3 | 0.0 | 71.9% | 74.4% | SEA (yes) |
| KC @ LV | KC 30 - 27 LV | -3.4 | -4.5 | -3 | 0.4 | 1.5 | 41.5% | 33.6% | KC (yes) |
| DET @ CAR | DET 26 - 32 CAR | -3.1 | -4.5 | +6 | 9.1 | 10.5 | 42.2% | 33.6% | DET (no) |
| ATL @ NO | ATL 45 - 24 NO | -0.6 | +1.5 | -21 | 20.4 | 22.5 | 48.4% | 51.7% | ATL (yes) |

## Week 5

File first committed 2026-10-06 19:37 UTC-04:00.

| Game | Final | Model margin | Vegas line | Result | Model err | Vegas err | Model win % | Vegas win % | SU pick |
|---|---|---|---|---|---|---|---|---|---|
| TB @ DAL | TB 24 - 16 DAL | +5.1 | +9.5 | -8 | 13.1 | 17.5 | 62.5% | 80.8% | DAL (no) |
| PHI @ JAX | PHI 17 - 19 JAX | +8.5 | +7.5 | +2 | 6.5 | 5.5 | 70.3% | 76.0% | JAX (yes) |
| NYG @ WAS | NYG 27 - 27 WAS | -0.4 | +3.5 | +0 | 0.4 | 3.5 | 49.0% | 61.6% | NYG (no) |
| HOU @ TEN | HOU 26 - 3 TEN | -3.9 | -6.5 | -23 | 19.1 | 16.5 | 40.3% | 27.4% | HOU (yes) |
| CIN @ MIA | CIN 31 - 24 MIA | -5.9 | -7.0 | -7 | 1.1 | 0.0 | 35.7% | 25.2% | CIN (yes) |
| CLE @ NYJ | CLE 12 - 17 NYJ | -0.4 | +2.5 | +5 | 5.4 | 2.5 | 49.1% | 56.3% | CLE (no) |
| MIN @ NO | MIN 23 - 13 NO | -4.4 | -2.5 | -10 | 5.6 | 7.5 | 39.1% | 43.7% | MIN (yes) |
| LV @ NE | LV 17 - 45 NE | +6.8 | +3.5 | +28 | 21.2 | 24.5 | 66.5% | 61.6% | NE (yes) |
| IND @ PIT | IND 22 - 34 PIT | +0.7 | +3.0 | +12 | 11.3 | 9.0 | 51.7% | 59.3% | PIT (yes) |
| CHI @ GB | CHI 7 - 31 GB | -2.8 | -1.5 | +24 | 26.8 | 25.5 | 43.1% | 46.8% | CHI (no) |
| DEN @ LAC | DEN 23 - 17 LAC | -3.6 | -3.5 | -6 | 2.4 | 2.5 | 41.2% | 36.9% | DEN (yes) |
| SF @ SEA | SF 32 - 29 SEA | -0.8 | +3.0 | -3 | 2.2 | 6.0 | 48.0% | 60.0% | SF (yes) |
| DET @ ARI | DET 45 - 21 ARI | -4.6 | -5.5 | -24 | 19.4 | 18.5 | 38.7% | 30.4% | DET (yes) |
| BAL @ ATL | BAL 30 - 23 ATL | -0.4 | +3.5 | -7 | 6.6 | 10.5 | 48.9% | 60.9% | BAL (yes) |
| BUF @ LA | BUF 37 - 34 LA | +0.6 | +3.5 | -3 | 3.6 | 6.5 | 51.4% | 62.2% | LA (no) |

## Week 7

File first committed 2026-10-20 19:33 UTC-04:00.

| Game | Final | Model margin | Vegas line | Result | Model err | Vegas err | Model win % | Vegas win % | SU pick |
|---|---|---|---|---|---|---|---|---|---|
| NE @ CHI | NE 24 - 30 CHI | -0.0 | +3.0 | +6 | 6.0 | 3.0 | 49.9% | 58.3% | NE (no) |
| PIT @ NO | PIT 16 - 10 NO | -3.1 | -3.0 | -6 | 2.9 | 3.0 | 42.3% | 40.7% | PIT (yes) |
| CLE @ TEN | CLE 27 - 24 TEN | -1.5 | -1.5 | -3 | 1.5 | 1.5 | 46.2% | 45.7% | CLE (yes) |
| MIA @ NYJ | MIA 28 - 25 NYJ | +3.0 | +3.5 | -3 | 6.0 | 6.5 | 57.4% | 65.7% | NYJ (no) |
| NYG @ HOU | NYG 27 - 21 HOU | +5.9 | +10.0 | -6 | 11.9 | 16.0 | 64.4% | 80.4% | HOU (no) |
| TB @ CAR | TB 43 - 13 CAR | +4.0 | +3.0 | -30 | 34.0 | 33.0 | 59.8% | 60.0% | CAR (no) |
| CIN @ BAL | CIN 35 - 13 BAL | +1.8 | -3.0 | -22 | 23.8 | 19.0 | 54.4% | 40.7% | BAL (no) |
| SF @ ATL | SF 20 - 29 ATL | -5.4 | -2.5 | +9 | 14.4 | 11.5 | 36.7% | 41.7% | SF (no) |
| IND @ MIN | IND 10 - 16 MIN | +5.1 | +6.5 | +6 | 0.9 | 0.5 | 62.6% | 73.4% | MIN (yes) |
| DEN @ ARI | DEN 30 - 16 ARI | -4.7 | -4.5 | -14 | 9.3 | 9.5 | 38.6% | 33.1% | DEN (yes) |
| LA @ LV | LA 35 - 21 LV | -3.3 | -3.5 | -14 | 10.7 | 10.5 | 41.9% | 38.4% | LA (yes) |
| GB @ DET | GB 17 - 20 DET | +3.2 | +3.5 | +3 | 0.2 | 0.5 | 58.0% | 63.1% | DET (yes) |
| KC @ SEA | KC 3 - 20 SEA | +2.1 | +3.0 | +17 | 14.9 | 14.0 | 55.2% | 59.3% | SEA (yes) |
| DAL @ PHI | DAL 38 - 21 PHI | +0.6 | -4.5 | -17 | 17.6 | 12.5 | 51.5% | 33.6% | PHI (no) |

Margins, lines, and win % are all from the home team's side, so +3.0 means the home team by 3.
