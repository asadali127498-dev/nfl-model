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

## Week 7 predictions (2026)

Generated 2026-10-20, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder, and each file's git commit timestamp is the actual proof of when I
posted it.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-10-22 | NE | CHI | NE 23.7 - 23.7 CHI | -0.0 | 49.9% | 47.4 | CHI |
| 2026-10-25 | LA | LV | LA 24.0 - 20.8 LV | -3.3 | 41.9% | 44.8 | LA |
| 2026-10-25 | KC | SEA | KC 18.4 - 20.5 SEA | +2.1 | 55.2% | 38.9 | SEA |
| 2026-10-25 | DEN | ARI | DEN 26.2 - 21.5 ARI | -4.7 | 38.6% | 47.7 | DEN |
| 2026-10-25 | CLE | TEN | CLE 19.7 - 18.2 TEN | -1.5 | 46.2% | 37.8 | CLE |
| 2026-10-25 | MIA | NYJ | MIA 21.6 - 24.6 NYJ | +3.0 | 57.4% | 46.2 | NYJ |
| 2026-10-25 | GB | DET | GB 25.2 - 28.5 DET | +3.2 | 58.0% | 53.7 | DET |
| 2026-10-25 | NYG | HOU | NYG 19.7 - 25.6 HOU | +5.9 | 64.4% | 45.2 | HOU |
| 2026-10-25 | TB | CAR | TB 21.1 - 25.1 CAR | +4.0 | 59.8% | 46.3 | CAR |
| 2026-10-25 | CIN | BAL | CIN 26.0 - 27.8 BAL | +1.8 | 54.4% | 53.8 | BAL |
| 2026-10-25 | SF | ATL | SF 28.3 - 22.9 ATL | -5.4 | 36.7% | 51.2 | SF |
| 2026-10-25 | PIT | NO | PIT 23.1 - 20.0 NO | -3.1 | 42.3% | 43.0 | PIT |
| 2026-10-25 | IND | MIN | IND 18.9 - 24.0 MIN | +5.1 | 62.6% | 42.9 | MIN |
| 2026-10-26 | DAL | PHI | DAL 25.3 - 25.9 PHI | +0.6 | 51.5% | 51.2 | PHI |

All 14 games posted before kickoff, including Thursday night's NE @ CHI (BUF, JAX, LAC, and WAS are on bye).
One heads up: PIT @ NO is in Paris, and my model doesn't handle neutral sites,
so it still gives NO the normal home field bump. Without it, it would be about
NO -4.4 instead of -3.1. I'm keeping the model locked for the rest of the season
so the record stays clean, and I'll fix this in the offseason.

### Previous weeks

- Week 6: I didn't post predictions for week 6 before the games, so there's nothing to grade. I'm not going to post them after the fact.
- [Week 5](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week05.md): all 15 games posted before kickoff.
- [Week 4](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week04.md): all 16 games posted before kickoff.
- [Week 3](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week03.md): all 16 games posted before kickoff.
- [Week 2](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week02.md): I generated this before kickoff but didn't push it until after the games, so it doesn't count as pre-registered. I also never predicted DET @ BUF.
- [Week 1](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week01.md): all 16 games posted before kickoff.

## Source

[github.com/asadali127498-dev/nfl-model](https://github.com/asadali127498-dev/nfl-model)

<script data-goatcounter="https://drakemayefan123.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
