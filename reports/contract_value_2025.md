# Contract Value Analyzer

Who's outplaying their contract in 2025 and who isn't. I only did QB, RB, WR, and TE, since public play-by-play doesn't have a fair per-player stat for linemen or defenders.

How to read the tables: EPA over repl. is the expected points a player added above what a backup would have put up on the same number of plays. Paid is the contract's average per year as a share of the cap when it was signed, turned into 2025 dollars. Market value comes from ranks, so if a player was 10th in production at their position, it's what the 10th highest-paid veteran at that position makes (and the league minimum if they were at or below replacement). Surplus is market value minus pay, so positive means a bargain.

## What the market pays

The 2025 veteran pay ladder at each position, by average per year:

| Position | Highest paid | 5th | 16th | 32nd | Minimum |
|---|---|---|---|---|---|
| QB | $68.4M | $63.4M | $46.6M | $4.2M | $0.8M |
| RB | $20.7M | $13.4M | $7.8M | $2.0M | $0.8M |
| WR | $40.2M | $32.9M | $26.5M | $10.9M | $0.8M |
| TE | $20.4M | $18.4M | $9.8M | $4.5M | $0.8M |

## How much of this is luck?

This is how much the same player's numbers carry over from one season to the next, 2018-2025. Close to 0 means a great year mostly doesn't repeat, so a big surplus is closer to a lucky season than a smart signing. QBs hold up the best, and for everyone else I'd take a single great season with a grain of salt.

| Position | EPA over repl. per play | Surplus | Player pairs |
|---|---|---|---|
| QB | 0.40 | 0.30 | 188 |
| RB | 0.24 | 0.38 | 294 |
| TE | 0.26 | 0.35 | 207 |
| WR | 0.23 | 0.37 | 479 |

## 2025 QBs

Best value:

| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |
|---|---|---|---|---|---|---|---|
| Drake Maye | Patriots | 645 | +242.5 | $10.1M | $68.4M | $58.4M | rookie |
| Bo Nix | Broncos | 723 | +145.7 | $5.0M | $61.7M | $56.7M | rookie |
| Caleb Williams | Bears | 675 | +122.4 | $10.9M | $58.1M | $47.2M | rookie |
| Daniel Jones | Colts | 456 | +128.4 | $14.0M | $60.0M | $46.1M | yr 1 of 1 |
| C.J. Stroud | Texans | 497 | +113.8 | $11.2M | $55.0M | $43.8M | rookie |
| Jaxson Dart | Giants | 462 | +89.1 | $4.2M | $37.4M | $33.2M | rookie |
| Matt Stafford | Rams | 649 | +185.4 | $39.9M | $65.6M | $25.7M | yr 1 of 2 |
| Sam Darnold | Seahawks | 541 | +117.3 | $33.5M | $58.1M | $24.6M | yr 1 of 3 |
| Aaron Rodgers | Steelers | 551 | +79.0 | $13.7M | $33.5M | $19.8M | yr 1 of 1 |
| Mac Jones | 49ers | 343 | +74.7 | $3.6M | $20.1M | $16.5M | yr 1 of 2 |

Most overpaid:

| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |
|---|---|---|---|---|---|---|---|
| Kyler Murray | Cardinals | 206 | +31.0 | $61.7M | $5.9M | -$55.8M | yr 4 of 5 |
| Joe Burrow | Bengals | 292 | +70.2 | $68.4M | $14.0M | -$54.4M | yr 3 of 5 |
| Tua Tagovailoa | Dolphins | 437 | +51.9 | $58.1M | $10.6M | -$47.5M | yr 2 of 4 |
| Kirk Cousins | Falcons | 298 | +27.2 | $49.1M | $5.9M | -$43.3M | yr 2 of 4 |
| Geno Smith | Raiders | 546 | -18.4 | $37.4M | $0.8M | -$36.6M | yr 1 of 2 |
| Lamar Jackson | Ravens | 407 | +80.6 | $64.5M | $36.6M | -$27.9M | yr 3 of 5 |
| Justin Herbert | Chargers | 650 | +98.9 | $65.3M | $39.9M | -$25.4M | yr 3 of 5 |
| Justin Fields | Jets | 309 | +17.3 | $20.1M | $3.9M | -$16.2M | yr 1 of 2 |
| Jalen Hurts | Eagles | 593 | +112.0 | $63.4M | $49.1M | -$14.2M | yr 3 of 5 |
| Cam Ward | Titans | 634 | -35.4 | $12.3M | $0.8M | -$11.4M | rookie |

## 2025 RBs

Best value:

| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |
|---|---|---|---|---|---|---|---|
| Bijan Robinson | Falcons | 391 | +48.7 | $6.7M | $17.3M | $10.6M | rookie |
| Devon Achane | Dolphins | 323 | +32.2 | $1.7M | $10.3M | $8.7M | rookie |
| Kareem Hunt | Chiefs | 188 | +27.6 | $1.4M | $10.1M | $8.7M | yr 1 of 1 |
| Rachaad White | Buccaneers | 178 | +24.3 | $1.7M | $9.8M | $8.1M | rookie |
| Jahmyr Gibbs | Lions | 337 | +44.7 | $5.6M | $13.4M | $7.8M | rookie |
| TreVeyon Henderson | Patriots | 222 | +30.6 | $2.8M | $10.1M | $7.3M | rookie |
| Blake Corum | Rams | 159 | +24.0 | $1.7M | $8.9M | $7.3M | rookie |
| Rico Dowdle | Panthers | 287 | +22.0 | $2.8M | $8.7M | $5.9M | yr 1 of 1 |
| Ty Johnson | Bills | 83 | +21.5 | $2.5M | $7.8M | $5.3M | yr 1 of 2 |
| Jaylen Warren | Steelers | 256 | +32.6 | $5.9M | $10.9M | $5.0M | yr 1 of 2 |

Most overpaid:

| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |
|---|---|---|---|---|---|---|---|
| Saquon Barkley | Eagles | 332 | +0.1 | $20.7M | $1.4M | -$19.3M | yr 1 of 2 |
| Alvin Kamara | Saints | 170 | -25.5 | $13.4M | $0.8M | -$12.6M | yr 2 of 2 |
| Aaron Jones | Vikings | 173 | +5.3 | $10.1M | $1.7M | -$8.4M | yr 1 of 2 |
| Rhamondre Stevenson | Patriots | 169 | +9.7 | $9.8M | $1.7M | -$8.1M | yr 2 of 4 |
| Ashton Jeanty | Raiders | 340 | -47.2 | $8.9M | $0.8M | -$8.1M | rookie |
| Chuba Hubbard | Panthers | 174 | +4.2 | $8.9M | $1.4M | -$7.5M | yr 2 of 4 |
| Josh Jacobs | Packers | 278 | +21.4 | $13.1M | $6.1M | -$7.0M | yr 2 of 4 |
| Tony Pollard | Titans | 283 | -8.7 | $7.8M | $0.8M | -$7.0M | yr 2 of 3 |
| David Montgomery | HOU/DET | 191 | +18.6 | $10.1M | $5.3M | -$4.7M | yr 2 of 2 |
| Derrick Henry | Ravens | 329 | +34.7 | $15.1M | $10.9M | -$4.2M | yr 1 of 2 |

## 2025 WRs

Best value:

| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |
|---|---|---|---|---|---|---|---|
| Puka Nacua | Rams | 176 | +97.7 | $1.4M | $40.2M | $38.8M | rookie |
| George Pickens | PIT/DAL | 138 | +67.3 | $2.2M | $38.3M | $36.0M | rookie |
| Jaxon Smith-Njigba | Seahawks | 170 | +64.4 | $4.5M | $37.1M | $32.7M | rookie |
| Kayshon Boutte | NE/HOU | 46 | +29.7 | $1.1M | $32.7M | $31.5M | rookie |
| Alec Pierce | Colts | 84 | +42.8 | $2.2M | $32.9M | $30.7M | rookie |
| Zay Flowers | Ravens | 129 | +28.9 | $4.5M | $31.0M | $26.5M | rookie |
| Romeo Doubs | Packers | 86 | +21.3 | $1.4M | $26.5M | $25.1M | rookie |
| Luther Burden | Bears | 66 | +22.1 | $2.8M | $27.4M | $24.6M | rookie |
| Ryan Flournoy | Cowboys | 60 | +19.8 | $1.1M | $24.0M | $22.9M | yr 1 of 2 |
| Demario Douglas | Patriots | 53 | +19.0 | $1.1M | $22.3M | $21.2M | rookie |

Most overpaid:

| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |
|---|---|---|---|---|---|---|---|
| Justin Jefferson | Vikings | 144 | -36.2 | $38.3M | $0.8M | -$37.4M | yr 2 of 4 |
| Garrett Wilson | Jets | 60 | -11.4 | $32.4M | $0.8M | -$31.5M | yr 1 of 4 |
| CeeDee Lamb | Cowboys | 118 | +10.4 | $37.1M | $10.1M | -$27.1M | yr 2 of 4 |
| D.J. Moore | CHI/BUF | 101 | +6.0 | $30.2M | $3.4M | -$26.8M | yr 2 of 4 |
| Ja'Marr Chase | Bengals | 188 | +12.3 | $40.2M | $14.2M | -$26.0M | yr 1 of 4 |
| Christian Kirk | JAX/HOU | 53 | -29.4 | $24.0M | $0.8M | -$23.2M | yr 4 of 4 |
| Michael Pittman, Jr. | IND/PIT | 114 | +4.6 | $25.4M | $2.8M | -$22.6M | yr 2 of 3 |
| Mike Evans | Buccaneers | 62 | -4.3 | $22.3M | $0.8M | -$21.5M | yr 2 of 2 |
| Jakobi Meyers | Jaguars | 115 | -8.2 | $20.1M | $0.8M | -$19.3M | yr 1 of 3 |
| Jerry Jeudy | Browns | 107 | -46.2 | $19.3M | $0.8M | -$18.4M | yr 2 of 3 |

## 2025 TEs

Best value:

| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |
|---|---|---|---|---|---|---|---|
| Tucker Kraft | Packers | 45 | +31.1 | $1.7M | $18.4M | $16.8M | rookie |
| Dalton Kincaid | Bills | 50 | +31.2 | $4.2M | $18.7M | $14.5M | rookie |
| Sam LaPorta | Lions | 49 | +28.4 | $3.1M | $15.6M | $12.6M | rookie |
| Colston Loveland | Bears | 84 | +32.9 | $6.7M | $19.0M | $12.3M | rookie |
| A.J. Barner | Seahawks | 78 | +22.4 | $1.4M | $12.6M | $11.2M | rookie |
| Darren Waller | Dolphins | 36 | +22.7 | $2.0M | $13.1M | $11.2M | yr 1 of 1 |
| Brenton Strange | Jaguars | 60 | +21.6 | $2.0M | $12.0M | $10.1M | rookie |
| Greg Dulcich | Dolphins | 35 | +10.2 | $1.1M | $9.8M | $8.7M | yr 1 of 1 |
| Jake Tonges | 49ers | 46 | +6.7 | $1.1M | $7.8M | $6.7M | yr 1 of 1 |
| Darnell Washington | Steelers | 44 | +7.4 | $1.7M | $8.1M | $6.4M | rookie |

Most overpaid:

| Player | Team | Plays | EPA over repl. | Paid (APY) | Market value | Surplus | Deal |
|---|---|---|---|---|---|---|---|
| David Njoku | Browns | 48 | -11.5 | $18.4M | $0.8M | -$17.6M | yr 4 of 4 |
| T.J. Hockenson | Vikings | 67 | +2.0 | $20.4M | $5.3M | -$15.1M | yr 3 of 4 |
| Mark Andrews | Ravens | 80 | -5.0 | $13.1M | $0.8M | -$12.3M | yr 1 of 3 |
| Jonnu Smith | Steelers | 64 | -6.1 | $12.0M | $0.8M | -$11.2M | yr 1 of 1 |
| Evan Engram | Broncos | 78 | -9.0 | $11.4M | $0.8M | -$10.6M | yr 1 of 2 |
| Cole Kmet | Bears | 50 | +4.7 | $15.6M | $6.4M | -$9.2M | yr 3 of 4 |
| Jake Ferguson | Cowboys | 104 | +1.4 | $12.6M | $5.0M | -$7.5M | yr 1 of 4 |
| Mike Gesicki | Bengals | 43 | -2.6 | $8.4M | $0.8M | -$7.5M | yr 1 of 3 |
| Travis Kelce | Chiefs | 110 | +20.6 | $18.7M | $11.4M | -$7.3M | yr 2 of 2 |
| Noah Gray | Chiefs | 38 | -13.1 | $6.4M | $0.8M | -$5.6M | yr 2 of 3 |

## Do veteran deals age well?

Average surplus by year of the contract, for veteran deals of 3+ years, in 2025 dollars. I expected this to get worse every year as players age, but it's negative from year 1 and just kind of stays there. My guess is that teams mostly overpay at signing (the market is paying for the season that earned the deal), not that deals fall apart later.

| Contract year | Player-seasons | Average surplus |
|---|---|---|
| 1 | 209 | -$8.3M |
| 2 | 165 | -$7.9M |
| 3 | 99 | -$10.5M |
| 4 | 53 | -$8.3M |
| 5 | 13 | -$10.0M |

## Known limits

- Pay is the average per year, not the actual cap hit that season. Most deals are back-loaded, so early years really cost less than what's shown here and later years cost more.
- An extension signed during a season counts for that season, even if the new money starts later.
- A receiver gets credit for every pass thrown their way and a QB for every dropback, so a good QB and WR share credit for the same plays. That's part of why I only compare players to their own position.
- EPA says nothing about blocking, which matters a lot for TEs and some RBs.
- Rank pricing tells you what the Nth best producer would cost, not what that player will do next year, so a one-year spike still ranks high even if it won't repeat (see the luck table).
- Players who missed games rank lower, since EPA over replacement is a season total. That's a big part of why Burrow and Murray show up as overpaid.
