# Content gap analysis (2026-11-05)

Reference channel: **Spreadsheet Sports Analytics** (4.46K subs, 52 videos, daily NBA uploads).
Formula: *"a data model settles an argument fans already have, told like a story,"* plus a
companion site with the model's numbers.

## What works on the reference channel
| Format | Example | Views |
|---|---|---|
| Model settles a famous debate | Unluckiest NBA Player Ever | 286K |
| Rewriting history with one change | Would 75% FT Shaq Be the GOAT? | 192K |
| Model settles a famous debate | NBA's Most Underrated Player | 112K |
| Season simulation | Simulated 2027 Season 10,000x | 68K |
| Film breakdown / documentary | 76ers, Brunson | 1-2K |

Debates every fan already has an opinion on win by 10-100x. Film breakdowns and documentaries lose.

## Method
`tools/youtube_niche_scan.py` scrapes YouTube search results (top ~20 per query). It counts titles in
the data/model/simulation format, plus their views, channels and age. It ran 90+ queries across sports,
games, TV, music, history, finance and more. Raw results are in `raw/`.

## Findings
**Taken or saturating:** NBA (HQE, copycats), NFL (BlitzTalk: 421K on "Unluckiest NFL Team"),
Pokémon battle simulations (Astroid 3.1M, SmithPlays, Gym Leader Matt: 810K in 21 days),
world-war and history simulations (Geo Facts, RealityMargin, game-engine sims), chess (huge channels).

**Warning:** generic "I simulated X 100 million times" channels (casino, roulette, Connect 4,
Monopoly, Catan clones) appeared in the last ~2 weeks with 1-19K views. They are likely automated.
A simulation alone isn't enough to get views. The winners combine (a) a fandom with an existing
argument and (b) a narrative.

**Gaps (lots of demand, little or none of this format):**
1. **Video games, for players rather than developers.** "I Scraped the Entire Steam Catalog" got 1.6M,
   and "Every Silksong Review" got 284K, both from one developer-focused channel. "Most underrated
   video game ever data" returns 0 results. Data: Steam reviews, SteamSpy, HowLongToBeat, OpenCritic, IGDB.
2. **Reality TV and game shows** (Survivor, Jeopardy, Wheel of Fortune, Price is Right, Family Feud).
   General searches have a median of 90-170K views, and essentially no data-model videos exist.
   Data: the survivoR dataset (every vote and challenge), J! Archive (every Jeopardy clue).
3. College basketball / March Madness (the sports runner-up from round 1).
4. MLB history what-ifs.

## Recommendation
Primary: **video games** (largest audience, empty model-story lane, visuals can be fully generated from data).
Secondary or sister channel: **Survivor and game shows** (emptiest niche, ideal open datasets, passionate fandoms).
