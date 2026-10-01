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
| Pre-registered (Weeks 1 and 3) | 32 | 19-13 / 21-11 | 9.89 / 9.69 | 0.225 / 0.234 | 11.64 / 11.31 |
| All graded (Weeks 1-3) | 47 | 27-20 / 31-16 | 10.77 / 10.53 | 0.231 / 0.235 | 11.08 / 10.97 |

Week 3 was my best week so far. I beat Vegas on margin error (7.96 vs 8.09) and on Brier (0.218 vs 0.254), and we both went 9-7 straight up. I'm still a little behind on margin overall, but my win probabilities are actually ahead of the market's now. Three weeks is still a small sample though, so I'm not reading too much into it yet.

## Week 4 predictions (2026)

Generated 2026-09-30, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder, and each file's git commit timestamp is the actual proof of when I
posted it.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-10-01 | PIT | CLE | PIT 20.1 - 17.5 CLE | -2.6 | 43.5% | 37.5 | PIT |
| 2026-10-04 | DET | CAR | DET 23.6 - 20.5 CAR | -3.1 | 42.2% | 44.1 | DET |
| 2026-10-04 | DEN | SF | DEN 22.8 - 28.0 SF | +5.2 | 62.7% | 50.7 | SF |
| 2026-10-04 | LAC | SEA | LAC 16.7 - 26.0 SEA | +9.3 | 71.9% | 42.8 | SEA |
| 2026-10-04 | KC | LV | KC 23.3 - 19.8 LV | -3.4 | 41.5% | 43.1 | KC |
| 2026-10-04 | MIA | MIN | MIA 16.8 - 26.5 MIN | +9.7 | 72.7% | 43.3 | MIN |
| 2026-10-04 | GB | TB | GB 25.7 - 25.9 TB | +0.3 | 50.6% | 51.6 | TB |
| 2026-10-04 | LA | PHI | LA 21.7 - 18.4 PHI | -3.3 | 41.9% | 40.1 | LA |
| 2026-10-04 | ARI | NYG | ARI 24.2 - 26.2 NYG | +2.0 | 54.9% | 50.3 | NYG |
| 2026-10-04 | JAX | CIN | JAX 24.1 - 21.0 CIN | -3.1 | 42.3% | 45.1 | JAX |
| 2026-10-04 | NYJ | CHI | NYJ 19.8 - 28.2 CHI | +8.4 | 70.1% | 48.0 | CHI |
| 2026-10-04 | NE | BUF | NE 23.5 - 26.6 BUF | +3.1 | 57.7% | 50.2 | BUF |
| 2026-10-04 | TEN | BAL | TEN 15.4 - 25.9 BAL | +10.6 | 74.5% | 41.3 | BAL |
| 2026-10-04 | IND | WAS | IND 26.2 - 27.3 WAS | +1.1 | 52.8% | 53.5 | WAS |
| 2026-10-04 | DAL | HOU | DAL 24.4 - 25.3 HOU | +0.9 | 52.2% | 49.7 | HOU |
| 2026-10-05 | ATL | NO | ATL 20.7 - 20.1 NO | -0.6 | 48.4% | 40.8 | ATL |

All 16 games posted before kickoff, including Thursday night's PIT @ CLE.

### Previous weeks

- [Week 3](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week03.md): all 16 games posted before kickoff.
- [Week 2](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week02.md): I generated this before kickoff but didn't push it until after the games, so it doesn't count as pre-registered. I also never predicted DET @ BUF.
- [Week 1](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week01.md): all 16 games posted before kickoff.

## Source

[github.com/asadali127498-dev/nfl-model](https://github.com/asadali127498-dev/nfl-model)

<script data-goatcounter="https://drakemayefan123.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
