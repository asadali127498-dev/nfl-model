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
| Pre-registered (Weeks 1, 3-5, 7-9) | 106 | 71-35 / 74-32 | 9.46 / 9.50 | 0.207 / 0.205 | 11.60 / 10.60 |
| All graded (Weeks 1-5, 7-9) | 121 | 79-42 / 84-37 | 9.86 / 9.86 | 0.211 / 0.209 | 11.38 / 10.56 |

Week 9 was the best week for both of us. Vegas and I each went 14-1 straight up. Vegas was more confident on the ones it got right though, so it won on Brier (0.121 vs my 0.164) and edged me on margin error (8.80 vs 9.36). GB @ NE going for 72 and HOU @ LAC for 66 wrecked the totals again. Across everything I pre-registered I'm now basically tied with Vegas on margin (9.46 vs 9.50) and Brier (0.207 vs 0.205), which is down from being ahead on both a few weeks ago. I'm still about a point behind on totals (11.60 vs 10.60). The Madrid game (CIN @ ATL) went ATL by -17, and without the home field bump I flagged, my miss would've been 12.35 instead of 13.6. That's three international games in a row where dropping the bump would've helped.

## Week 10 predictions (2026)

Generated 2026-11-10, before kickoff of every game listed. Every week's file
lives in the repo's
[`predictions/`](https://github.com/asadali127498-dev/nfl-model/tree/main/predictions)
folder, and each file's git commit timestamp is the actual proof of when I
posted it.

| Date | Away | Home | Predicted Score | Margin | Home Win % | Total | Favorite |
|---|---|---|---|---|---|---|---|
| 2026-11-12 | WAS | NYG | WAS 19.9 - 21.1 NYG | +1.3 | 53.1% | 41.0 | NYG |
| 2026-11-15 | PIT | CIN | PIT 24.0 - 27.5 CIN | +3.5 | 58.6% | 51.5 | CIN |
| 2026-11-15 | SF | DAL | SF 31.4 - 27.1 DAL | -4.3 | 39.5% | 58.5 | SF |
| 2026-11-15 | SEA | LV | SEA 25.1 - 18.1 LV | -7.0 | 33.1% | 43.1 | SEA |
| 2026-11-15 | JAX | TEN | JAX 28.8 - 17.6 TEN | -11.2 | 24.2% | 46.4 | JAX |
| 2026-11-15 | BUF | NYJ | BUF 31.8 - 20.5 NYJ | -11.3 | 24.0% | 52.2 | BUF |
| 2026-11-15 | LA | ARI | LA 27.3 - 20.8 ARI | -6.5 | 34.2% | 48.1 | LA |
| 2026-11-15 | MIA | IND | MIA 23.0 - 26.1 IND | +3.1 | 57.7% | 49.2 | IND |
| 2026-11-15 | MIN | GB | MIN 17.4 - 23.2 GB | +5.8 | 64.1% | 40.6 | GB |
| 2026-11-15 | HOU | CLE | HOU 18.2 - 12.5 CLE | -5.7 | 36.2% | 30.7 | HOU |
| 2026-11-15 | KC | ATL | KC 26.3 - 22.3 ATL | -4.1 | 40.0% | 48.6 | KC |
| 2026-11-15 | NE | DET | NE 24.3 - 27.7 DET | +3.4 | 58.5% | 52.0 | DET |
| 2026-11-15 | CAR | NO | CAR 21.7 - 21.7 NO | +0.0 | 50.1% | 43.4 | NO |
| 2026-11-16 | LAC | BAL | LAC 20.1 - 25.0 BAL | +4.9 | 61.9% | 45.1 | BAL |

All 14 games posted before kickoff, including Thursday night's WAS @ NYG (CHI, DEN, PHI, and TB are on bye).
Two heads ups. NE @ DET is in Munich, and my model still gives DET home field,
so without it that one would be about DET +2.2 instead of +3.4. And two totals
(WAS @ NYG and HOU @ CLE) have my full 8 point rain penalty because the forecast
mentions rain, though Cleveland's is only a "slight chance." The details are in
the [week 10 file](https://github.com/asadali127498-dev/nfl-model/blob/main/predictions/2026-week10.md).

### Previous weeks

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
