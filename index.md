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
| Pre-registered (Weeks 1, 3-5, 7-11) | 133 | 89-44 / 92-41 | 9.49 / 9.42 | 0.206 / 0.201 | 11.11 / 10.39 |
| All graded (Weeks 1-5, 7-11) | 148 | 97-51 / 102-46 | 9.81 / 9.72 | 0.209 / 0.205 | 10.98 / 10.37 |

Week 11 was a mixed one. Vegas and I both went 9-4 straight up. They beat me on margin error (7.77 vs my 8.78) and on Brier (0.183 vs 0.194), but I beat them on totals (9.91 vs 10.81). Across everything I pre-registered I'm now slightly behind Vegas on all four, including margin for the first time since early in the season (9.49 vs 9.42). The gaps are small, but I'm not going to pretend I'm ahead. Two corrections from last week too. I said the rain penalty was probably making most of my totals too low. In the eight games that got it, I actually missed less with the penalty (6.51) than I would have without it (10.19), so I was wrong, at least for that week. And the Mexico City game (MIN @ SF) went SF by 25, so dropping the home field bump would've made it worse. That's now 3 of 5 international games where it would've helped, which is basically a coin flip.

## Week 12 predictions (2026)

Generated 2026-11-24, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder, and each file's git commit timestamp is the actual proof of when I
posted it.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-11-25 | GB | LA | GB 21.7 - 26.3 LA | +4.6 | 61.3% | 47.9 | LA |
| 2026-11-26 | PHI | DAL | PHI 21.6 - 28.3 DAL | +6.7 | 66.2% | 49.9 | DAL |
| 2026-11-26 | CHI | DET | CHI 22.6 - 25.1 DET | +2.6 | 56.4% | 47.7 | DET |
| 2026-11-26 | KC | BUF | KC 20.1 - 23.7 BUF | +3.5 | 58.7% | 43.8 | BUF |
| 2026-11-27 | DEN | PIT | DEN 19.1 - 17.5 PIT | -1.6 | 46.0% | 36.6 | DEN |
| 2026-11-29 | NO | CIN | NO 14.8 - 25.0 CIN | +10.2 | 73.8% | 39.8 | CIN |
| 2026-11-29 | LV | CLE | LV 14.2 - 16.4 CLE | +2.2 | 55.6% | 30.6 | CLE |
| 2026-11-29 | WAS | ARI | WAS 27.2 - 23.3 ARI | -4.0 | 40.2% | 50.5 | WAS |
| 2026-11-29 | NE | LAC | NE 24.1 - 19.5 LAC | -4.6 | 38.6% | 43.6 | NE |
| 2026-11-29 | ATL | MIN | ATL 16.1 - 22.4 MIN | +6.3 | 65.4% | 38.5 | MIN |
| 2026-11-29 | SEA | SF | SEA 17.1 - 22.3 SF | +5.3 | 62.9% | 39.4 | SF |
| 2026-11-29 | TEN | JAX | TEN 11.9 - 26.2 JAX | +14.3 | 81.5% | 38.0 | JAX |
| 2026-11-29 | NYG | IND | NYG 23.4 - 20.9 IND | -2.5 | 43.9% | 44.4 | NYG |
| 2026-11-29 | BAL | HOU | BAL 19.3 - 26.5 HOU | +7.1 | 67.2% | 45.8 | HOU |
| 2026-11-29 | NYJ | MIA | NYJ 18.0 - 19.3 MIA | +1.3 | 53.3% | 37.4 | MIA |
| 2026-11-30 | CAR | TB | CAR 16.0 - 19.8 TB | +3.8 | 59.4% | 35.8 | TB |

All 16 games posted before kickoff, including Wednesday night's GB @ LA and the Thanksgiving games.
TEN @ JAX at 81.5% is the most confident I've been about any game this season.
Eight totals have my full 8 point rain penalty because the forecast mentions
rain (KC @ BUF, DEN @ PIT, SEA @ SF, CAR @ TB, NO @ CIN, LV @ CLE, NYJ @ MIA,
and TEN @ JAX). That only affects totals, not margins. The details are in the
[week 12 file](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week12.md).

### Previous weeks

- [Week 11](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week11.md): all 13 games posted before kickoff.
- [Week 10](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week10.md): all 14 games posted before kickoff.
- [Week 9](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week09.md): all 15 games posted before kickoff.
- [Week 8](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week08.md): all 14 games posted before kickoff.
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
