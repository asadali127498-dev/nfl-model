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
| Pre-registered (Weeks 1, 3-5, 7-8) | 91 | 57-34 / 60-31 | 9.48 / 9.62 | 0.214 / 0.219 | 11.46 / 10.69 |
| All graded (Weeks 1-5, 7-8) | 106 | 65-41 / 70-36 | 9.93 / 10.00 | 0.218 / 0.222 | 11.24 / 10.62 |

Week 8 was close. Vegas and I both went 11-3 straight up, I beat them on margin error (10.56 vs 10.82), and they beat me on Brier (0.181 vs 0.187) and totals (11.29 vs 12.99). TEN @ CIN going for 79 and LV @ NYJ going for 71 didn't help anyone's totals. The CLE @ PIT game I flagged last week ended up at 33 total, so my 30.4 with the rain penalty actually beat Vegas's 38.5. That's one game though. Across everything I pre-registered I'm still a little ahead on margin and win probability and behind on totals.

## Week 9 predictions (2026)

Generated 2026-11-03, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder, and each file's git commit timestamp is the actual proof of when I
posted it.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-11-05 | JAX | BAL | JAX 24.1 - 19.4 BAL | -4.7 | 38.4% | 43.6 | JAX |
| 2026-11-08 | GB | NE | GB 19.1 - 22.6 NE | +3.5 | 58.6% | 41.8 | NE |
| 2026-11-08 | LV | SF | LV 20.6 - 29.7 SF | +9.2 | 71.7% | 50.3 | SF |
| 2026-11-08 | HOU | LAC | HOU 22.7 - 18.2 LAC | -4.4 | 39.1% | 40.9 | HOU |
| 2026-11-08 | LA | WAS | LA 26.7 - 24.2 WAS | -2.5 | 43.7% | 50.9 | LA |
| 2026-11-08 | NYG | PHI | NYG 23.6 - 22.1 PHI | -1.5 | 46.2% | 45.6 | NYG |
| 2026-11-08 | DAL | IND | DAL 28.2 - 26.6 IND | -1.6 | 46.1% | 54.8 | DAL |
| 2026-11-08 | DET | MIA | DET 29.9 - 23.5 MIA | -6.4 | 34.5% | 53.4 | DET |
| 2026-11-08 | NYJ | KC | NYJ 21.9 - 29.0 KC | +7.2 | 67.3% | 50.9 | KC |
| 2026-11-08 | DEN | CAR | DEN 25.6 - 21.0 CAR | -4.6 | 38.6% | 46.6 | DEN |
| 2026-11-08 | CIN | ATL | CIN 27.3 - 23.9 ATL | -3.4 | 41.6% | 51.2 | CIN |
| 2026-11-08 | ARI | SEA | ARI 14.6 - 23.3 SEA | +8.7 | 70.6% | 37.9 | SEA |
| 2026-11-08 | CLE | NO | CLE 16.8 - 19.1 NO | +2.3 | 55.7% | 35.9 | NO |
| 2026-11-08 | TB | CHI | TB 15.7 - 22.8 CHI | +7.0 | 67.0% | 38.5 | CHI |
| 2026-11-09 | BUF | MIN | BUF 25.0 - 21.7 MIN | -3.2 | 42.0% | 46.7 | BUF |

All 15 games posted before kickoff, including Thursday night's JAX @ BAL (PIT and TEN are on bye).
Two heads ups. CIN @ ATL is in Madrid, and my model still gives ATL home field,
so without it that one would be about ATL -4.7 instead of -3.4. And four totals
(ARI @ SEA, JAX @ BAL, GB @ NE, TB @ CHI) have my full 8 point rain penalty because
the forecast mentions rain, even the "slight chance" ones. The details are in
the [week 9 file](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week09.md).

### Previous weeks

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
