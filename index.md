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
| Pre-registered (Week 1) | 16 | 10-6 / 12-4 | 11.82 / 11.28 | 0.232 / 0.214 | 12.24 / 11.69 |
| All graded (Weeks 1-2) | 31 | 18-13 / 22-9 | 12.21 / 11.79 | 0.237 / 0.226 | 11.09 / 10.98 |

So far I'm a little behind Vegas, which is about the same gap I had in testing. Two weeks is way too small a sample to judge anything though, so I'm treating this as a running tally.

## Week 3 predictions (2026)

Generated 2026-09-24, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder — each file's git commit timestamp is the actual, unfakeable proof of
when it was posted.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-09-24 | ATL | GB | ATL 22.8 - 26.1 GB | +3.3 | 58.1% | 49.0 | GB |
| 2026-09-27 | SEA | WAS | SEA 24.3 - 17.4 WAS | -6.9 | 33.4% | 41.7 | SEA |
| 2026-09-27 | LA | DEN | LA 23.6 - 23.0 DEN | -0.6 | 48.5% | 46.6 | LA |
| 2026-09-27 | LV | NO | LV 17.4 - 21.0 NO | +3.6 | 58.8% | 38.5 | NO |
| 2026-09-27 | BAL | DAL | BAL 28.8 - 27.1 DAL | -1.7 | 45.7% | 55.9 | BAL |
| 2026-09-27 | MIN | TB | MIN 23.8 - 20.0 TB | -3.8 | 40.7% | 43.8 | MIN |
| 2026-09-27 | ARI | SF | ARI 19.9 - 31.6 SF | +11.7 | 76.8% | 51.5 | SF |
| 2026-09-27 | CIN | PIT | CIN 24.4 - 23.4 PIT | -1.0 | 47.4% | 47.8 | CIN |
| 2026-09-27 | NYJ | DET | NYJ 20.9 - 29.5 DET | +8.7 | 70.6% | 50.4 | DET |
| 2026-09-27 | KC | MIA | KC 28.2 - 22.7 MIA | -5.5 | 36.5% | 50.8 | KC |
| 2026-09-27 | NE | JAX | NE 23.5 - 24.3 JAX | +0.8 | 52.0% | 47.7 | JAX |
| 2026-09-27 | HOU | IND | HOU 22.4 - 22.2 IND | -0.2 | 49.4% | 44.7 | HOU |
| 2026-09-27 | CAR | CLE | CAR 20.9 - 19.5 CLE | -1.5 | 46.3% | 40.4 | CAR |
| 2026-09-27 | LAC | BUF | LAC 20.8 - 30.1 BUF | +9.4 | 72.1% | 50.9 | BUF |
| 2026-09-27 | TEN | NYG | TEN 17.0 - 22.2 NYG | +5.2 | 62.7% | 39.1 | NYG |
| 2026-09-28 | PHI | CHI | PHI 22.9 - 25.8 CHI | +2.9 | 57.3% | 48.7 | CHI |

All 16 games posted before kickoff, including tonight's ATL @ GB opener.

### Previous weeks

- [Week 2](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week02.md): I generated this before kickoff but didn't push it until after the games, so it doesn't count as pre-registered. I also never predicted DET @ BUF.
- [Week 1](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week01.md): all 16 games posted before kickoff.

## Source

[github.com/asadali127498-dev/nfl-model](https://github.com/asadali127498-dev/nfl-model)

<script data-goatcounter="https://drakemayefan123.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
