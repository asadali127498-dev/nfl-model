# 2026 Scorecard

Updated 2026-09-25T21:31:12 (local time). I graded every number here from the prediction files exactly as I posted them, not from a re-run of the model. The Vegas numbers are the closing line from nflverse, and the Vegas win % is the moneyline with the vig taken out.

Each cell is model / Vegas, and lower is better for MAE and Brier. For reference, my margin MAE over the 2023-2025 test seasons was 10.17 and Vegas was 9.74. I don't think a couple of weeks says much of anything yet, so I'm treating this as a running tally.

| Games | n | Straight up | Margin MAE | Brier | Total MAE | Closer than Vegas |
|---|---|---|---|---|---|---|
| Pre-registered only | 16 | 10-6 / 12-4 | 11.82 / 11.28 | 0.232 / 0.214 | 12.24 / 11.69 | 6 of 16 |
| All graded games | 31 | 18-13 / 22-9 | 12.21 / 11.79 | 0.237 / 0.226 | 11.09 / 10.98 | 15 of 31 |
| Week 1 | 16 | 10-6 / 12-4 | 11.82 / 11.28 | 0.232 / 0.214 | 12.24 / 11.69 | 6 of 16 |
| Week 2 (not pre-registered) | 15 | 8-7 / 10-5 | 12.63 / 12.33 | 0.242 / 0.239 | 9.87 / 10.23 | 9 of 15 |

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

Margins, lines, and win % are all from the home team's side, so +3.0 means the home team by 3.
