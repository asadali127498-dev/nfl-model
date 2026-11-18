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
| Pre-registered (Weeks 1, 3-5, 7-10) | 120 | 80-40 / 83-37 | 9.56 / 9.60 | 0.207 / 0.203 | 11.24 / 10.34 |
| All graded (Weeks 1-5, 7-10) | 135 | 88-47 / 93-42 | 9.90 / 9.91 | 0.211 / 0.207 | 11.08 / 10.33 |

Week 10 was close again. Vegas and I both went 9-5 straight up. I edged them on margin error (10.32 vs 10.36) and they beat me on Brier (0.184 vs my 0.208). Totals were my closest week yet (8.51 vs 8.36), even with SF @ DAL going for 86. Across everything I pre-registered I'm still basically tied with Vegas on margin (9.56 vs 9.60) and a hair behind on Brier (0.207 vs 0.203), about three games behind straight up, and a point behind on totals (11.24 vs 10.34). I need to take back something I said last week. I'd pointed out that dropping the home field bump would've helped in all three international games so far. The Munich game (NE @ DET) went DET by 25, and dropping the bump would've made my miss a little worse (22.85 vs 21.6), so it's 3 of 4 now. That's not much of a pattern anymore.

## Week 11 predictions (2026)

Generated 2026-11-18, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder, and each file's git commit timestamp is the actual proof of when I
posted it.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-11-19 | IND | HOU | IND 18.1 - 24.4 HOU | +6.4 | 65.5% | 42.5 | HOU |
| 2026-11-22 | NYJ | LAC | NYJ 20.1 - 22.5 LAC | +2.4 | 55.9% | 42.6 | LAC |
| 2026-11-22 | MIN | SF | MIN 15.6 - 20.5 SF | +5.0 | 62.2% | 36.1 | SF |
| 2026-11-22 | PIT | PHI | PIT 20.8 - 16.7 PHI | -4.1 | 39.8% | 37.5 | PIT |
| 2026-11-22 | LV | DEN | LV 16.4 - 25.4 DEN | +9.1 | 71.5% | 41.8 | DEN |
| 2026-11-22 | JAX | NYG | JAX 23.8 - 15.9 NYG | -7.9 | 31.1% | 39.7 | JAX |
| 2026-11-22 | MIA | BUF | MIA 14.0 - 27.6 BUF | +13.5 | 80.1% | 41.6 | BUF |
| 2026-11-22 | TB | DET | TB 20.5 - 26.6 DET | +6.1 | 64.9% | 47.1 | DET |
| 2026-11-22 | TEN | DAL | TEN 22.0 - 29.3 DAL | +7.4 | 67.7% | 51.3 | DAL |
| 2026-11-22 | NO | CHI | NO 12.4 - 22.3 CHI | +10.0 | 73.3% | 34.7 | CHI |
| 2026-11-22 | BAL | CAR | BAL 19.3 - 20.5 CAR | +1.3 | 53.1% | 39.8 | CAR |
| 2026-11-22 | ARI | KC | ARI 15.0 - 26.2 KC | +11.2 | 75.8% | 41.2 | KC |
| 2026-11-23 | CIN | WAS | CIN 25.7 - 20.0 WAS | -5.8 | 35.9% | 45.7 | CIN |

All 13 games posted before kickoff, including Thursday night's IND @ HOU (ATL, CLE, GB, LA, NE, and SEA are on bye).
Two heads ups. MIN @ SF is in Mexico City, and my model gets that wrong twice:
it still gives SF home field, and it used the forecast for the Bay Area, not
Mexico City, so a "Light Rain Likely" in Santa Clara took 8 points off the total.
It also doesn't know about the altitude. And eight totals this week have my full
8 point rain penalty because the forecast mentions rain, but only Chicago's is a
real rain forecast. The rest say "chance" or "slight chance," which my model
treats the same as actual rain, so I think most of my totals this week are too
low. That penalty only touches totals, so my margins and win probabilities
aren't affected. The details are in the
[week 11 file](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week11.md).

### Previous weeks

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
