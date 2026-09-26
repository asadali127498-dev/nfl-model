# 4th Down Decision Grader

I graded every regulation 4th down since 2018 against whichever option (go for it, field goal, or punt) had the highest win probability. WP lost is how much win probability a call gave up compared to the best option, and if you add it up over a season it's roughly how many games a coach's 4th-down calls cost the team.

If the options were within 1% of each other I count the call as fine. Those are basically coin flips, and I don't think my model is precise enough to call them either way.

## How good are the models?

I trained on seasons through 2022 and tested on 2023-2025. The win probability model uses 2006-2022, and everything else uses 2018-2022.

- Win probability, on 117,772 test plays: Brier 0.1501, compared to 0.1484 for nflfastR's model (lower is better). So mine is a little worse than theirs, but close.
- Conversions, on 2,414 real 4th-down attempts in the test seasons: it predicted 54.0% would convert and 55.3% did.
- Field goals, on 3,263 test kicks: it predicted 85.5% would be good and 85.2% were.
- Consistency check, on the test seasons' 4th downs: I compared the average win probability I predicted for whatever the coach chose to the win probability on the next snap. Going for it 35.2% predicted vs 35.3% on the next snap (2,369 plays); field goals 56.7% predicted vs 56.7% on the next snap (2,860 plays); punts 47.1% predicted vs 47.3% on the next snap (6,202 plays). Those basically match, so I don't think the decision math is biased toward any one option.

Calibration on the test seasons, meaning when my model says a team has an X% chance, how often that team actually wins:

| Predicted | Actual | Plays |
|---|---|---|
| 3.4% | 3.8% | 16,704 |
| 15.0% | 15.9% | 10,063 |
| 24.9% | 25.1% | 11,311 |
| 34.9% | 34.7% | 10,037 |
| 44.9% | 44.9% | 9,683 |
| 55.1% | 55.0% | 9,177 |
| 65.1% | 64.8% | 10,803 |
| 74.9% | 75.1% | 11,466 |
| 85.0% | 82.1% | 10,745 |
| 96.4% | 96.8% | 17,783 |

4th-down conversion rate by distance in the test seasons:

| Yards to go | Predicted | Actual | Attempts |
|---|---|---|---|
| 1 | 67.6% | 68.9% | 960 |
| 2 | 59.0% | 60.2% | 367 |
| 3 | 53.1% | 54.5% | 266 |
| 4 | 48.1% | 52.4% | 189 |
| 5 | 44.2% | 50.3% | 145 |
| 6+ | 28.9% | 27.7% | 487 |

## Are coaches getting more aggressive?

These are the spots where going for it was clearly the better call (by more than the 1% toss-up margin), and how often coaches actually went for it. The go rate climbs pretty steadily, but the wins lost per team doesn't really drop, which I think is because there are more clear go spots every year too.

| Season | Clear 'go' spots | Went for it | WP lost per team |
|---|---|---|---|
| 2018 | 812 | 32.6% | 0.57 |
| 2019 | 838 | 35.6% | 0.55 |
| 2020 | 813 | 41.9% | 0.49 |
| 2021 | 873 | 44.4% | 0.53 |
| 2022 | 948 | 39.5% | 0.61 |
| 2023 | 915 | 42.7% | 0.55 |
| 2024 | 904 | 45.6% | 0.53 |
| 2025 | 1,036 | 45.8% | 0.59 |

## 2025 coaches, best to worst

| Coach | Team | 4th downs | Clear 'go' spots | Went | Too conservative | Too aggressive | Wins lost |
|---|---|---|---|---|---|---|---|
| Jonathan Gannon | ARI | 116 | 20 | 8 | 13 | 0 | 0.34 |
| Dan Campbell | DET | 116 | 29 | 18 | 12 | 1 | 0.34 |
| Nick Sirianni | PHI | 117 | 20 | 11 | 9 | 2 | 0.36 |
| Sean McDermott | BUF | 101 | 30 | 17 | 13 | 3 | 0.41 |
| Liam Coen | JAX | 116 | 33 | 19 | 14 | 0 | 0.41 |
| Mike McDaniel | MIA | 113 | 28 | 11 | 17 | 0 | 0.44 |
| Zac Taylor | CIN | 111 | 25 | 11 | 15 | 0 | 0.44 |
| Sean McVay | LA | 104 | 31 | 18 | 13 | 2 | 0.47 |
| Brian Callahan | TEN | 145 | 20 | 6 | 14 | 0 | 0.47 |
| Mike Vrabel | NE | 102 | 30 | 14 | 16 | 0 | 0.47 |
| Brian Schottenheimer | DAL | 109 | 39 | 18 | 21 | 2 | 0.48 |
| Matt LaFleur | GB | 99 | 28 | 15 | 13 | 2 | 0.49 |
| Pete Carroll | LV | 130 | 27 | 13 | 14 | 2 | 0.50 |
| Mike Macdonald | SEA | 106 | 22 | 8 | 14 | 0 | 0.53 |
| Dan Quinn | WAS | 104 | 36 | 15 | 22 | 1 | 0.55 |
| Todd Bowles | TB | 126 | 35 | 19 | 16 | 1 | 0.55 |
| Raheem Morris | ATL | 127 | 36 | 19 | 18 | 0 | 0.55 |
| Sean Payton | DEN | 124 | 31 | 12 | 19 | 0 | 0.56 |
| John Harbaugh | BAL | 108 | 26 | 13 | 13 | 1 | 0.57 |
| Aaron Glenn | NYJ | 139 | 33 | 12 | 22 | 1 | 0.57 |
| Kellen Moore | NO | 130 | 41 | 17 | 24 | 2 | 0.60 |
| Ben Johnson | CHI | 126 | 36 | 20 | 17 | 2 | 0.64 |
| Kyle Shanahan | SF | 96 | 29 | 12 | 17 | 1 | 0.67 |
| Shane Steichen | IND | 102 | 35 | 17 | 19 | 1 | 0.68 |
| Dave Canales | CAR | 120 | 41 | 24 | 17 | 2 | 0.71 |
| Brian Daboll | NYG | 121 | 43 | 22 | 21 | 1 | 0.72 |
| Andy Reid | KC | 123 | 45 | 24 | 21 | 2 | 0.77 |
| Kevin O'Connell | MIN | 122 | 38 | 15 | 24 | 1 | 0.79 |
| DeMeco Ryans | HOU | 139 | 38 | 14 | 24 | 1 | 0.84 |
| Mike Tomlin | PIT | 116 | 40 | 14 | 26 | 3 | 0.97 |
| Jim Harbaugh | LAC | 118 | 35 | 6 | 29 | 0 | 0.97 |
| Kevin Stefanski | CLE | 147 | 36 | 12 | 26 | 2 | 0.98 |

## 2025's costliest calls

| Game | Team | Qtr | Time | Score | Situation | Call | Go / FG / Punt WP | Lost |
|---|---|---|---|---|---|---|---|---|
| IND @ HOU (wk 18) | IND | 4 | 2:42 | -2 | 4th & 2, opp 4 | fg | 36.2% / 21.6% / 9.5% | 14.6% |
| CLE @ CIN (wk 18) | CLE | 4 | 2:50 | +5 | 4th & 1, own 18 | punt | 66.8% / 37.8% / 52.4% | 14.4% |
| PIT @ CLE (wk 17) | CLE | 4 | 2:24 | +4 | 4th & 1, own 19 | punt | 74.9% / 35.1% / 63.4% | 11.6% |
| KC @ BUF (wk 9) | KC | 2 | 0:06 | -11 | 4th & 1, opp 1 | fg | 27.5% / 16.5% / 14.9% | 11.0% |
| BAL @ MIN (wk 10) | BAL | 2 | 1:14 | -7 | 4th & 2, opp 10 | fg | 50.7% / 40.5% / 31.8% | 10.2% |
| CHI @ CIN (wk 9) | CHI | 2 | 1:33 | +1 | 4th & 2, opp 6 | fg | 77.0% / 67.3% / 58.5% | 9.7% |
| LA @ ATL (wk 17) | ATL | 4 | 7:34 | +7 | 4th & 1, opp 49 | punt | 78.2% / 66.8% / 69.2% | 9.0% |
| PHI @ LAC (wk 14) | LAC | 4 | 7:29 | -3 | 4th & 3, opp 13 | fg | 44.6% / 36.4% / 22.4% | 8.2% |
| DEN @ NYJ (wk 6) | NYJ | 4 | 10:23 | +1 | 4th & 1, own 30 | punt | 40.3% / 21.3% / 32.2% | 8.1% |
| JAX @ CIN (wk 2) | JAX | 4 | 6:09 | +3 | 4th & 2, opp 47 | punt | 69.4% / 56.9% / 61.3% | 8.1% |
| DAL @ NYG (wk 18) | NYG | 2 | 9:48 | -4 | 4th & 3, opp 4 | fg | 41.3% / 33.5% / 27.2% | 7.9% |
| PIT @ BAL (wk 14) | PIT | 2 | 10:41 | +4 | 4th & 3, opp 5 | fg | 57.1% / 49.3% / 42.2% | 7.8% |
| KC @ LV (wk 18) | LV | 2 | 1:56 | +0 | 4th & 2, opp 5 | fg | 56.8% / 49.3% / 40.0% | 7.6% |
| SF @ TB (wk 6) | SF | 3 | 7:30 | -4 | 4th & 6, opp 11 | fg | 38.2% / 30.9% / 25.5% | 7.3% |
| SEA @ PIT (wk 2) | SEA | 2 | 7:11 | +1 | 4th & 1, opp 49 | punt | 51.0% / 38.9% / 44.0% | 7.0% |

## Known limits

- The biggest one: my win probability model is built from decision trees, so it moves in steps between scores that are right next to each other. Some of that is real (being down 6 and being down 7 play out pretty similarly), but some of the jumps are bigger than the real data backs up, like a tie vs. up 1 early in a game. That can push a single play's grade off by a few points. I think season totals mostly average it out, but a smoother model is the first thing I want to fix.
- Gains on a successful conversion come from the league-wide spread for that distance, so it doesn't know defenses tighten up near the goal line.
- Conversion and field goal odds are league average. It has no idea a team has a great short-yardage offense or a great kicker, other than whatever the pregame spread says about the team overall.
- Every touchdown is worth 7, so no 2-point decisions, and I left overtime out.
- Penalties, spikes, and kneels on 4th down aren't graded.
