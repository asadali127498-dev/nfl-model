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
| Pre-registered (Weeks 1, 3-5, 7) | 77 | 46-31 / 49-28 | 9.28 / 9.40 | 0.219 / 0.226 | 11.19 / 10.58 |
| All graded (Weeks 1-5, 7) | 92 | 54-38 / 59-33 | 9.83 / 9.88 | 0.223 / 0.228 | 10.97 / 10.52 |

Week 7 was my first rough week since week 1. I went 7-7 straight up to Vegas's 10-4, with a margin error of 11.01 vs 10.07 and a Brier of 0.253 vs 0.231. TB @ CAR (I missed by 34) and CIN @ BAL (missed by 24) did most of the damage, but Vegas missed both of those badly too. The good news is it was my first week beating Vegas on totals (9.59 vs 10.43). Overall I'm still a little ahead on margin and win probability across everything I pre-registered, and still behind on totals.

## Week 8 predictions (2026)

Generated 2026-10-27, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder, and each file's git commit timestamp is the actual proof of when I
posted it.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-10-29 | CAR | GB | CAR 22.8 - 27.9 GB | +5.1 | 62.5% | 50.8 | GB |
| 2026-11-01 | PHI | WAS | PHI 23.5 - 26.1 WAS | +2.6 | 56.4% | 49.6 | WAS |
| 2026-11-01 | NE | MIA | NE 27.8 - 20.4 MIA | -7.3 | 32.3% | 48.2 | NE |
| 2026-11-01 | LAC | LA | LAC 17.9 - 26.1 LA | +8.2 | 69.5% | 43.9 | LA |
| 2026-11-01 | ATL | TB | ATL 22.2 - 22.3 TB | +0.1 | 50.2% | 44.5 | TB |
| 2026-11-01 | CLE | PIT | CLE 12.2 - 18.1 PIT | +5.9 | 64.3% | 30.4 | PIT |
| 2026-11-01 | KC | DEN | KC 17.8 - 20.2 DEN | +2.4 | 56.0% | 38.0 | DEN |
| 2026-11-01 | IND | JAX | IND 17.3 - 24.6 JAX | +7.4 | 67.7% | 41.9 | JAX |
| 2026-11-01 | MIN | DET | MIN 20.6 - 23.2 DET | +2.6 | 56.4% | 43.7 | DET |
| 2026-11-01 | ARI | DAL | ARI 25.0 - 31.6 DAL | +6.6 | 65.9% | 56.5 | DAL |
| 2026-11-01 | TEN | CIN | TEN 16.0 - 27.2 CIN | +11.2 | 75.7% | 43.1 | CIN |
| 2026-11-01 | BAL | BUF | BAL 26.0 - 31.7 BUF | +5.7 | 63.9% | 57.7 | BUF |
| 2026-11-01 | LV | NYJ | LV 21.5 - 22.6 NYJ | +1.2 | 53.0% | 44.1 | NYJ |
| 2026-11-02 | CHI | SEA | CHI 21.5 - 24.0 SEA | +2.5 | 56.2% | 45.5 | SEA |

All 14 games posted before kickoff, including Thursday night's CAR @ GB (HOU, NO, NYG, and SF are on bye).
One heads up: the 30.4 total for CLE @ PIT includes my full 8 point rain penalty
because the forecast says there's a chance of showers. That penalty was trained
on games where it actually rained, so I think it's too low here. Without it, it
would be about 38.4. I'm keeping the model locked for the season and fixing this
in the offseason.

### Previous weeks

- [Week 7](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week07.md): all 14 games posted before kickoff.
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
