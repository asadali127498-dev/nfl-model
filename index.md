---
title: NFL Elo Prediction Model
---

# NFL Elo Prediction Model

A from-scratch NFL prediction model, built in Python, evaluated honestly against
Vegas closing lines over the 2026 season. Predictions are posted here **before**
each week's games — timestamped by the git commit history, not editable after
the fact.

- **Margin model:** MAE 10.17 vs Vegas 9.74 on 3 held-out seasons (2023-2025).
- **Totals model:** MAE 10.45 vs Vegas 10.12 on the same held-out seasons.
- Full methodology, every parameter, and every tested idea that *didn't* work
  (a real record of the negative results, not just the wins) is in
  [`PROGRESS.md`](https://github.com/asadali127498-dev/nfl-model/blob/main/PROGRESS.md)
  in the repo.

## How it's doing so far

I graded these straight from the files I posted, against the Vegas closing
line (model / Vegas, and lower is better). The game-by-game breakdown is in the
[scorecard](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-scorecard.md).

| Games | n | Straight up | Margin MAE | Brier | Total MAE |
|---|---|---|---|---|---|
| Pre-registered (Weeks 1, 3-5) | 63 | 39-24 / 39-24 | 8.90 / 9.25 | 0.211 / 0.225 | 11.54 / 10.61 |
| All graded (Weeks 1-5) | 78 | 47-31 / 49-29 | 9.62 / 9.85 | 0.217 / 0.228 | 11.22 / 10.54 |

Week 5 was the third week in a row I beat Vegas. I went 10-5 straight up to their 9-6, with a margin error of 9.65 vs 10.40 and a Brier of 0.194 vs 0.212 (NYG @ WAS ended in a tie, which counts as a miss for both of us straight up). Across everything I pre-registered, I'm now tied with Vegas straight up and ahead on margin and win probability. Totals are still my weak spot (11.54 vs 10.61), and I'm looking at a fix for that. The London game (PHI @ JAX) went JAX by 2, and without the home field bump I talked about, my miss on it would've been 5.25 points instead of 6.5.

## Week 5 predictions (2026)

Generated 2026-10-06, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder, and each file's git commit timestamp is the actual proof of when I
posted it.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-10-08 | TB | DAL | TB 24.4 - 29.5 DAL | +5.1 | 62.5% | 54.0 | DAL |
| 2026-10-11 | NYG | WAS | NYG 20.8 - 20.4 WAS | -0.4 | 49.0% | 41.3 | NYG |
| 2026-10-11 | BAL | ATL | BAL 25.3 - 24.8 ATL | -0.4 | 48.9% | 50.1 | BAL |
| 2026-10-11 | SF | SEA | SF 25.0 - 24.2 SEA | -0.8 | 48.0% | 49.3 | SF |
| 2026-10-11 | DET | ARI | DET 29.6 - 25.0 ARI | -4.6 | 38.7% | 54.6 | DET |
| 2026-10-11 | DEN | LAC | DEN 22.8 - 19.2 LAC | -3.6 | 41.2% | 42.1 | DEN |
| 2026-10-11 | HOU | TEN | HOU 22.8 - 18.9 TEN | -3.9 | 40.3% | 41.7 | HOU |
| 2026-10-11 | CIN | MIA | CIN 29.4 - 23.5 MIA | -5.9 | 35.7% | 53.0 | CIN |
| 2026-10-11 | CLE | NYJ | CLE 20.3 - 19.9 NYJ | -0.4 | 49.1% | 40.2 | CLE |
| 2026-10-11 | MIN | NO | MIN 21.4 - 16.9 NO | -4.4 | 39.1% | 38.3 | MIN |
| 2026-10-11 | LV | NE | LV 17.7 - 24.5 NE | +6.8 | 66.5% | 42.3 | NE |
| 2026-10-11 | IND | PIT | IND 20.1 - 20.8 PIT | +0.7 | 51.7% | 40.9 | PIT |
| 2026-10-11 | CHI | GB | CHI 26.6 - 23.8 GB | -2.8 | 43.1% | 50.5 | CHI |
| 2026-10-11 | PHI | JAX | PHI 19.9 - 28.5 JAX | +8.5 | 70.3% | 48.4 | JAX |
| 2026-10-12 | BUF | LA | BUF 26.5 - 27.1 LA | +0.6 | 51.4% | 53.6 | LA |

All 15 games posted before kickoff, including Thursday night's TB @ DAL (CAR and KC are on bye).
One heads up: PHI @ JAX is in London, and my model doesn't handle neutral sites
yet, so it still gives JAX the normal home field bump. Without it, it would be
about JAX +7.3 instead of +8.5.

### Previous weeks

- [Week 4](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week04.md): all 16 games posted before kickoff.
- [Week 3](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week03.md): all 16 games posted before kickoff.
- [Week 2](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week02.md): I generated this before kickoff but didn't push it until after the games, so it doesn't count as pre-registered. I also never predicted DET @ BUF.
- [Week 1](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week01.md): all 16 games posted before kickoff.

## Source

[github.com/asadali127498-dev/nfl-model](https://github.com/asadali127498-dev/nfl-model)

<script data-goatcounter="https://drakemayefan123.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
