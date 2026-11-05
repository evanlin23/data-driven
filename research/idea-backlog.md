# Video idea backlog: data stories about video games (2026-11-05)

Channel formula (from `packaging-playbook.md` and `gap-analysis.md`): **a model or dataset settles an
argument players already have, told as a story.** The subject must be bigger than one game's fanbase,
or be one of the very biggest games. The title should be first person, with a superlative or extreme
answer and a big exact number. Avoid team or local interest and time-bound takes.

## How this was built
- **Brainstorm:** 119 candidate ideas, merged into about 95 distinct premises.
- **Competition and demand scan:** 286 YouTube searches through `tools/youtube_niche_scan.py`:
  - 236 searches in round 1, pairing a data-format query with a plain debate query for each idea;
  - 40 targeted "I analyzed / by metacritic / simulated" queries in round 2;
  - 10 competitor-channel checks in round 3.
  - Raw JSON is in the session scratchpad and was not committed:
    `/tmp/claude-0/-home-user-data-driven/111e2ec2-3c2d-5c60-a5e7-30cf2038f82a/scratchpad/scan/`.
  - Limit: the scan reads only the top ~20 search results. "0 data versions" means none surfaced in
    those results, not that none exists anywhere.
- **Data sources checked by curl from this machine today** (on top of the sources already verified):

| Code | Source | What it gives | Status |
|---|---|---|---|
| **SS** | SteamSpy `request=all` | 1,000 apps per page: owners range, positive/negative counts, CCU, price | Works. **Playtime fields now return 0**, so no playtime data from SteamSpy. |
| **SA** | Steam appdetails | Genres, release date, Metacritic score, price, achievement list | Works |
| **SH** | Steam `appreviewhistogram/{appid}` | **Monthly positive and negative review counts over a game's whole life** | 200, verified on Cyberpunk 2077. Replaces the blocked reviews endpoint for time series. The store page also shows the "last 30 days" share and the "off-topic review activity" (review-bomb) flag. |
| **ACH** | Steam `GetGlobalAchievementPercentagesForApp` (no key needed) plus the community stats page | % of owners who unlocked each achievement. The page embeds the names, e.g. "Defeated Godfrey, First Elden Lord". | 200, verified |
| **MC** | Metacritic browse pages | Critic and user scores embedded in page JSON | 200, verified |
| **SC** | steamcharts.com | Monthly average and peak players per game since 2012 | 200 |
| **SR** | speedrun.com REST API | Games, leaderboards, full run history | 200 |
| **EE** | esportsearnings.com | Player and tournament prize money | 200 |
| **CPI** | FRED CPI CSV | Inflation series | 200 |
| **HLTB** | HowLongToBeat | Game lengths | Site returns 200, but its search API needs a rotating token, so plan on a Kaggle HLTB dump as fallback. |
| **VGC / WP / KG** | VGChartz, Wikipedia, Kaggle | Sales figures, lists, datasets | Reachable |
| (blocked) | pro-football-reference, Liquipedia | | 403 and 429 |

- **Scoring:** each idea gets 1-5 on six dimensions, for a maximum total of 30:

| Code | Dimension | 1 means | 5 means |
|---|---|---|---|
| **D** | Debate size | Nobody argues about it | People already argue about it everywhere |
| **A** | Audience size | Niche | All gamers, or one of the very biggest games |
| **C** | Competition | Data versions already exist and get views | Nobody has made the data version |
| **F** | Data feasibility | Hard to get the data | Sources above, verified |
| **E** | Evergreen | Expires soon | Lasts for years |
| **T** | Thumbnail-ability | No clear image | One striking chart or icon |

  The scores are deliberately not inflated. Most ideas land at 23-27, and only 3 reach 29.
- **Numbers in titles are placeholders.** Replace each with the exact count from the final dataset,
  per the playbook rule to use exact, odd numbers.

### Key competitors to know
- **Data-format channels:**
  - **Newbie Indie Game Dev**, "I Scraped the Entire Steam Catalog" (1.6M). A whole-catalog,
    developer-angle video.
  - **adef**, math of Pokémon and Ocarina of Time luck (1.6M, 1.0M; an OoT video got 239K in 1 day).
    Owns "math behind luck" for Pokémon.
  - **Astroid, Gym Leader Matt and SmithPlays**, Pokémon battle sims (3.1M, 811K, 244K). Own Pokémon
    simulation.
  - **Shortcat**, Mario Kart mechanics (13.2M, 5.0M). Owns Mario Kart.
  - **Summoning Salt**, histories of single-game world records (up to 8.9M). Owns that format.
  - **Global Stats and Data Is Beautiful**, sales and console bar-chart races (2.0M, 4.7M).
    Sales rankings are fully covered.
  - **Thomas Game Docs**, "LEAST popular Mario game?" (4.65M) and Zelda (1.19M). These are fan
    surveys, not models.
  - **Super Bunnyhop**, "Statistically Speaking: Metacritic's Best Games" (234K, 6 years old).
  - **i am a dot.**, "I Analyzed 20+ Years of Video Game Awards Data" (51K).
  - **WelfareWalrus**, "Exposing BIAS in Game Review Scores" (2.1M, 6 years old).
  - **OrangeJuiceJaz**, "Ranking the Hardest Fromsoft Bosses with DATA" (325K).
- **Opinion and list giants** (demand signal; they don't compete on data): gameranx, TripleJump,
  WatchMojo, penguinz0, Scott The Woz, The Act Man. Their 1-5M view counts on the same debates
  measure demand.

---

## Top 50, ranked

Format: CD = countdown, MY = mystery or reveal, HH = head-to-head, SIM = simulation or counterfactual.

| # | Title draft | Premise (format) | Data | D | A | C | F | E | T | **Tot** | Existing competition (views) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | I Built a Model to Find the Most Overrated Game Ever | Overrated = acclaim (critic score, hype, GOTY noms) minus what players later said and did (user score, Steam review %, retention). Top 10 countdown to #1. (CD) | MC, SH, SS, SC | 5 | 5 | 5 | 4 | 5 | 5 | **29** | 0 data versions. Opinion only: gameranx "Overhyped" 2.2M, "Witcher 3 most overrated" 320K, JonTron 399K. |
| 2 | I Analyzed 31 Million Players to Find FromSoft's Hardest Boss | Steam achievement % for every boss in Dark Souls 1-3, Sekiro and Elden Ring (incl. DLC). The "wall" is the biggest drop-off between consecutive mandatory bosses. (MY) | ACH, SS | 5 | 5 | 4 | 5 | 5 | 5 | **29** | OrangeJuiceJaz "with DATA" 325K (2 yrs). The rest are opinion or challenge videos: ToweringPants 4.2M, Ember 2.6M. "I analyzed every fromsoftware boss" returned 0. |
| 3 | I Found the Boss That Made the Most Gamers Quit | Across ~2,000 Steam games with boss achievements, the largest single-boss player drop-off in all of gaming. (MY) | ACH, SS | 5 | 5 | 5 | 4 | 5 | 5 | **29** | 0 data versions. Lists only: WatchMojo hardest bosses 1.4M, gameranx 858K. F=4 because mapping achievements to bosses needs parsing "Defeat X" descriptions. |
| 4 | I Ranked Every Console Ever by Its Games, Not Its Sales | Library quality (Metacritic depth: # of 85+ games, median score) plus breadth per console. A bracket ends on the best console ever. (HH) | MC, WP, VGC | 5 | 5 | 4 | 4 | 5 | 5 | **28** | Sales races: Data Is Beautiful 429K, Global Stats 2.1M. Opinion tier lists: Linus 3.8M, TripleJump 4.4M. "console generations ranked by metacritic" returned 0. |
| 5 | I Checked 1,000 Games. Here's the One Nobody Finishes | Completion achievement % across Steam's top 1,000 games, and which hit has the lowest finish rate. (MY) | ACH, SS | 4 | 5 | 5 | 5 | 5 | 4 | **28** | 0 data versions. Essays: Razbuten 1.1M, Soup Box 384K, "Why 90% of gamers never finish" 192K. |
| 6 | I Analyzed 61,000 Games to Find the Worst Publisher Ever | Weighted Steam review %, Metacritic, review-bomb incidents and dead live-service games by publisher. Logos make the thumbnail. (CD) | SS, MC, SH, SC | 5 | 5 | 5 | 4 | 4 | 5 | **28** | 0 data versions. Opinion: penguinz0 "Worst Publisher Ever" 1.5M, "Ubisoft is sinking" 1.9M. |
| 7 | I Ranked 3,000 Game Studios to Find the Best One Ever | Developer-level career quality (hit rate and consistency), with a curve per studio. (CD) | MC, SS | 5 | 4 | 5 | 4 | 5 | 5 | **28** | 0 data versions. EthanOnEverything tier list 139K, WatchMojo 336K. |
| 8 | I Found the Greatest Comeback in Gaming History | Biggest swing from launch review % to the present, using monthly review history (No Man's Sky, Cyberpunk, FFXIV-style arcs). (MY) | SH, SC | 4 | 5 | 5 | 5 | 5 | 4 | **28** | Single-game stories only: "Engoodening of No Man's Sky" 26.5M, Cyberpunk redemption 2.5M. No cross-game data version. |
| 9 | I Built a Model to Find the Most Underrated Game on Steam | High positive % and quality signals versus tiny owner counts. Countdown to the best game nobody bought. (CD) | SS, SA, MC | 4 | 5 | 4 | 5 | 5 | 4 | **27** | Newbie Indie Game Dev catalog video 1.6M (developer angle, not this question). Lists: Rye Games 617K, gameranx 514K. "steam hidden gems algorithm" returned 0. |
| 10 | Games Aren't Getting Worse. I Checked 24,000 of Them. | Scores and user reception by release year, controlling for volume and survivorship. Write the claim from the result: if the data says "worse", flip it. (HH: eras) | MC, SH, SS | 5 | 5 | 5 | 4 | 4 | 4 | **27** | 0 data versions. Opinion: Act Man "Why are AAA games getting worse" 3.4M, Self Deficient 3.5M. |
| 11 | Critics vs Gamers: I Checked Who Was Right 14,000 Times | Who predicted a game's long-run reception (review % years later, player retention) better: critics or users? (HH) | MC, SH, SC | 5 | 4 | 5 | 4 | 5 | 4 | **27** | WelfareWalrus "Exposing bias" 2.1M (6 yrs), dunkey "Game Critics" 17.7M (essay). "games critics loved but players hated" has 0 data versions; lists ~400K. |
| 12 | I Combined 4 Datasets to Find the Greatest Game Ever Made | Composite of critics, users, sales and longevity (players still on it years later). A counterpoint to sales-only bar races. (CD) | MC, SH, SC, WP | 5 | 5 | 4 | 4 | 5 | 4 | **27** | Super Bunnyhop Metacritic stats 234K (6 yrs). Sales races: Data Is Beautiful 4.7M, Global Stats 2.0M. IGN Top 100 1.3M. |
| 13 | I Found the Hardest Game on Steam, by Data | Final-boss and credits achievement % divided by early-game %, which removes people who never started. (CD) | ACH, SS | 5 | 5 | 4 | 4 | 5 | 4 | **27** | Lists and challenges: RNG Gamer "hardest game every console" 2.3M, WatchMojo achievements 5.1M. No dataset version. Shares the dataset with #3 and #5, so it is cheap to make. |
| 14 | Games Have Never Been Cheaper. I Ran the Numbers. | Launch prices 1985-now adjusted with CPI, plus hours per dollar. Addresses the $70/$80 debate. (HH: then vs now) | WP, CPI, HLTB | 5 | 4 | 4 | 5 | 4 | 4 | **26** | Scott The Woz "Game Prices" 1.9M (comedy/history), Extra Credits 678K (8 yrs), NintenDeen inflation 73K, "I did the math" 314. |
| 15 | I Calculated the Best Value Game Ever Made | Price per hour (HLTB) times quality. Finds the best and the worst dollar-per-fun game. (CD) | HLTB, SA, MC | 4 | 4 | 5 | 4 | 5 | 4 | **26** | 0 data versions. dunkey "Video Game Pricing" 8.6M (essay), gameranx "worth full money" 2.0M. |
| 16 | I Compared Every Remake to Its Original. One Side Wins. | ~300 remake/remaster vs original pairs: critic and user deltas. (HH) | MC, WP, SH | 4 | 4 | 5 | 4 | 5 | 4 | **26** | 0 data versions. Single-series videos: RE remakes 228K, Pyrocynical essay 5.2M. |
| 17 | I Analyzed 24,000 Games to Find Gaming's Greatest Year | Depth of acclaimed releases per year (98? 2004? 2017? 2023?). (CD) | MC, WP | 5 | 4 | 4 | 5 | 5 | 3 | **26** | DynamiteNunchucks "I Analyzed 500 Games to Settle Gaming's Best Year" **687 views** (exists, tiny). TripleJump every-year ranking 1.2M. |
| 18 | I Tracked 200 Franchises to Find Gaming's Biggest Fall | The steepest decline in quality and players across sequels (AC? Sonic? Halo? CoD?). (MY) | MC, SH, SC | 4 | 4 | 5 | 4 | 5 | 4 | **26** | 0 data versions. Opinion: gameranx franchise lists 0.9-2.2M, "Downfall of Assassin's Creed" 1.5M. |
| 19 | I Built a Model to Find the Worst Game Ever Made | Bottom of the distribution with minimum-attention thresholds, so it's not just 0-review shovelware. (CD) | MC, SS, SH | 4 | 5 | 4 | 4 | 5 | 4 | **26** | Huge opinion and playthrough demand: gameranx 5.0M, Great Big Story 4.4M, TripleJump "101 worst" 2.8M. No model. |
| 20 | I Ranked All 87,000 Steam Games. #1 Surprised Me. | Bayesian-adjusted Steam rating, so 50-review games don't top it. Steam's real #1. (CD) | SS, SH | 4 | 5 | 3 | 5 | 5 | 4 | **26** | Newbie Indie catalog 1.6M. Recap "Highest Rated Steam Games" 2.3M (playthrough), Get To It "God Tier Steam Games" 3.0M. Overlaps with #9. |
| 21 | The Data Says This Is the Best Pokémon Game Ever | Every mainline Pokémon game by critic and user score, sales and longevity. Pokémon passes the "biggest games" test. (CD) | MC, VGC, WP | 5 | 5 | 3 | 4 | 5 | 4 | **26** | Opinion rankings saturate it: WolfeyVGC 2.1M, StrawHatMidas 1.8M/1.2M. Pokémon data space is crowded (Astroid, adef, Gym Leader Matt). |
| 22 | I Ranked Every Call of Duty Using 20 Years of Data | Critic and user scores, sales and multiplayer survival curves (steamcharts for PC-era titles). (CD) | MC, SC, VGC | 5 | 5 | 4 | 4 | 4 | 4 | **26** | Opinion only: Ali-A 1.7M, ghost explains 2.1M, Ranton 885K. 0 data versions. |
| 23 | I Tracked 312 Live Service Games. Most Died Fast. | Survival curve: median months from launch to 90% player loss, and the fastest death (Concord?). (SIM: survival model) | SC, SS, WP | 4 | 4 | 5 | 4 | 4 | 4 | **25** | 0 data versions. Concord documentary 1.8M, Rocket Sloth "dead live service" 769K, Act Man 2.4M. |
| 24 | Review Bombs Don't Work. I Checked 500 of Them. | Month-by-month histograms around flagged review-bomb events: does the score recover, and do sales/CCU dip? Claim follows the result. (HH: before/after) | SH, SC | 4 | 4 | 5 | 4 | 4 | 4 | **25** | 0 data versions. News/essays: IGN short 1.26M, War Thunder documentary 573K, Extra Credits 192K. |
| 25 | I Compared 600 Sequels to Their Originals | Do sequels beat originals? Biggest upgrade and biggest flop. (HH) | MC, WP | 4 | 4 | 5 | 4 | 5 | 3 | **25** | "sequels review scores data" returned 0. Opinion: Act Man 2.1M, gameranx 2.0M. |
| 26 | Great Games Don't Sell. I Checked 9,000 of Them. | Quality vs sales correlation, and the best game that flopped hardest. Claim follows the result. (MY) | MC, SS, VGC | 4 | 4 | 5 | 4 | 5 | 3 | **25** | Lists only: gameranx "Good Games That Flopped" 4.0M / 1.7M. 0 data versions. |
| 27 | I Built a Model to Find the Most Average Game Ever | A direct riff on the 5,800x "most average NBA player" outlier: the game closest to the median on every metric. (MY) | SS, MC, HLTB | 2 | 4 | 5 | 5 | 5 | 4 | **25** | Nothing (Linus "Most Average Gaming PC" 6.0M is hardware). Low debate, proven hook. |
| 28 | Bigger Budgets Don't Make Better Games. I Checked. | ~150 games with known budgets vs quality and sales: best and worst money ever spent. (HH) | WP, MC, VGC | 4 | 4 | 5 | 3 | 5 | 4 | **25** | 0 data versions. Essays: CircleToonsHD 2.7M, Grant Wisler "low-budget masterpiece" 2.0M. Budget list is ~150 games (F=3). |
| 29 | I Ranked Every Soulslike on Steam. Only 3 Beat Dark Souls. | ~1,500 Souls-like-tagged games: how many are good, and does the "fatigue" hold up? (CD) | SS (tags), SH | 4 | 4 | 5 | 5 | 4 | 3 | **25** | Opinion: penguinz0 "Soulslike Fatigue" 2.2M, Nasu 3.2M. 0 data versions. |
| 30 | I Measured 100 Open Worlds. Bigger Maps Score Worse. | Map area vs quality and completion rate (does anyone finish a giant map?). Claim follows the result. (HH) | WP/fandom map sizes, MC, ACH | 4 | 4 | 4 | 3 | 5 | 5 | **25** | Size comparisons are saturated (RED SIDE 28M, Horizon 6.3M) but none link size to quality. Open-world fatigue essays 1.9M. |
| 31 | I Found the Best Horror Game Ever Made, With Data | Composite score plus Steam review sentiment within the horror tag. Seasonal bump every October. (CD) | SS, MC, SH | 3 | 4 | 5 | 4 | 5 | 4 | **25** | Opinion lists: gameranx 1.4M, IGN 289K, WatchMojo 232K. No data versions. |
| 32 | I Found the Rarest Achievement on Steam | Lowest global % across ~50,000 games with achievements, filtered for real games. (MY) | ACH, SS | 3 | 4 | 4 | 5 | 5 | 4 | **25** | Snamwiches single achievements 3.9M; gameranx impossible trophies 1.2M; ItsJabo Fallout 1.6M. No all-Steam scan surfaced. |
| 33 | I Searched 90,000 Steam Games for the One Nobody Owns | Owner ranges plus 0 reviews plus CCU 0. The loneliest game on Steam. (MY) | SS, SA | 2 | 5 | 4 | 5 | 5 | 4 | **25** | Playthroughs: Joeseppi "Steam Games That Nobody Plays" 13.8M, Ludwig "no reviews" 2.2M. No data version. Low debate. |
| 34 | I Tested the Madden Curse on Every Cover Athlete | ~25 covers: next-season games and stats vs the player's baseline and position peers. (HH) | WP (stats), ESPN/WP tables | 5 | 4 | 4 | 3 | 5 | 4 | **25** | REBOUND "Madden Curse" 7.4M (narrative). BenchwarmerBran "isn't real" 315K (light analysis). PFR is blocked (403), so stats need Wikipedia/ESPN (F=3). |
| 35 | I Traced 60,000 Games to Find the Most Copied Game Ever | Tag/genre explosions after a release (Dark Souls, Minecraft, PUBG, Vampire Survivors, Slay the Spire). (MY) | SS tags, SA dates | 4 | 4 | 5 | 3 | 5 | 4 | **25** | "Most influential" lists: WatchMojo 560K, Max Derrat 231K. 0 data versions. |
| 36 | I Ranked Every Resident Evil Using 30 Years of Data | Mainline, remakes and spinoffs by critics, users, sales and player retention. (CD) | MC, SH, VGC | 4 | 4 | 4 | 4 | 5 | 4 | **25** | penguinz0 "All 29 RE games" 3.3M, GmanLives 1.0M, Orrnery 549K (all opinion). |
| 37 | I Ranked Every GTA Game Using 25 Years of Data | Critics, sales, longevity (GTA V's player decade). Ride the GTA 6 launch wave but keep an evergreen title. (CD) | MC, VGC, SC, WP | 4 | 5 | 4 | 4 | 4 | 4 | **25** | penguinz0 "All 11 GTA" 1.6M (60 days), GmanLives 712K, ZacCoxTV 3.7M. "every gta game ranked data" returned 0. |
| 38 | The Data Says This Is the Best Mario Game Ever | Every mainline and spinoff Mario by score, sales, legs. (CD) | MC, VGC, WP | 4 | 5 | 3 | 4 | 5 | 4 | **25** | Thomas Game Docs "LEAST popular Mario game?" 4.65M (survey-based, close), Nathaniel Bandy 5.7M. |
| 39 | The Data Says This Is the Best Zelda Game Ever | Same method for Zelda (BotW vs OoT vs TotK). (CD) | MC, VGC, WP | 5 | 4 | 3 | 4 | 5 | 4 | **25** | Many "I ranked": BeatEmUps 1.1M, Player 2 678K, Orrnery 350K. Thomas Game Docs "least popular Zelda" 1.19M. |
| 40 | I Built a Model to Find the Unluckiest Game Ever Released | A great game buried by its release week (vs a GTA/Zelda launch), studio shutdown or platform. Counterfactual: reassign its release date. (SIM) | MC, SS, VGC, SA | 3 | 4 | 5 | 3 | 5 | 4 | **24** | 0 data versions. Lists: "Most Poorly Timed Nintendo Games" 1.9M, "Failed at launch" 3.1M. Proven "unluckiest" model hook (98x / 286K in other sports). |
| 41 | I Re-Judged Every Game of the Year With Hindsight Data | Did the right game win? Winners vs nominees by long-run reception. Publish in the Game Awards window (early Dec). (HH) | MC, SH, SC, WP | 5 | 4 | 3 | 4 | 4 | 4 | **24** | i am a dot. "20+ Years of Awards Data" 51K. Played-and-ranked: Orrnery 1.37M, SpongeDidTheMath 1.56M, Zenkai Goose 1.67M. "Robbed" lists 1.2M. |
| 42 | I Analyzed 3,000,000 Speedruns to Find the Unbreakable Record | Fit improvement curves to all speedrun.com leaderboards and simulate which record is closest to the human limit. (SIM) | SR | 3 | 4 | 4 | 5 | 5 | 3 | **24** | Summoning Salt owns single-game histories (up to 8.9M). "I analyzed every speedrun" returned 0 data versions. adef "Math Behind Unluckiest OoT Moments" 239K in 1 day (adjacent). |
| 43 | Indie Games Are Better Than AAA. I Checked 80,000. | Quality distributions by price/publisher tier: hit rate vs ceiling. Claim follows the result. (HH) | SS, SA, MC | 4 | 4 | 4 | 4 | 5 | 3 | **24** | CircleToonsHD 4.3M, Going Indie 2.2M, Viva La Dirt League 1.3M (skits/essays). Newbie Indie touches it from the developer side. |
| 44 | Delayed Games Turn Out Better. I Checked 400. | Delay length vs final reception (compiled from Wikipedia release histories). (HH) | WP, MC | 4 | 4 | 5 | 3 | 5 | 3 | **24** | Scott The Woz "To Delay a Game" 2.1M (essay). 0 data versions. Delay dataset is manual (F=3). |
| 45 | I Analyzed 18,625 IGN Reviews to Find Their Worst Take | Largest deviation of IGN from the consensus: the "too much water" hall of fame. (CD) | KG (IGN dataset), MC | 4 | 4 | 5 | 3 | 4 | 4 | **24** | Opinion: penguinz0 "Worst IGN Reviews Ever" 5.9M, "Most Disliked IGN Reviews" 1.1M. 0 data versions. Kaggle IGN set may stop around 2016 (F=3). |
| 46 | A 7/10 Is Now a Bad Score. I Analyzed 300,000 Reviews. | Critic score inflation over time: the drift of the 50th percentile. Claim follows the result. (MY) | MC | 4 | 3 | 5 | 4 | 5 | 3 | **24** | 0 game data versions. "Why are review scores so inflated?" 21K, Vox on Rotten Tomatoes 2.3M (film). |
| 47 | I Built a Model to Find the Biggest Surprise Hit Ever | Expected success (studio size, price, hype) vs actual owners and CCU (Palworld, Lethal Company, Among Us, Vampire Survivors). (MY) | SS, SC, SA | 3 | 4 | 5 | 3 | 5 | 4 | **24** | 0 relevant results (search noise). Mortismal personal list 316K. |
| 48 | I Ranked Every Assassin's Creed Using 18 Years of Data | Critics, users, sales, completion %. Ties into "fall of Ubisoft". (CD) | MC, SH, ACH, VGC | 4 | 4 | 3 | 4 | 5 | 4 | **24** | Crowded "I ranked": bizlychannel 2.0M, jayvee 2.8M, Ironside George 1.2M, The Hidden One (several). |
| 49 | I Measured Every Sequel Gap. Half-Life 3 Isn't the Worst. | The longest waits (Half-Life, Elder Scrolls 6, GTA, Hollow Knight to Silksong), ranked and projected. (CD) | WP, SA | 3 | 4 | 4 | 4 | 4 | 4 | **23** | gameranx "Waited LONGEST" 466K, Rocket Sloth dev time 381K, Larry Bundy 473K. "What the data says" 3.5K. |
| 50 | I Simulated 10,000,000 Gacha Pulls to Find the Cruelest Game | Published pity rates across Genshin, Honkai Star Rail, Wuthering Waves, FGO and others: expected cost of a limited 5-star. (SIM) | Published rates (pure simulation) | 4 | 4 | 4 | 5 | 3 | 3 | **23** | "I simulated gacha pulls" returned 0 data versions. Genshin pity guides 1.5M, 550K. Fine as a simulation-format slot. |

Notes on the bottom of the table:
- #49 and #50 are tied at 23 with about 10 backups. They were picked over the others for audience
  breadth (#49) and to keep a second pure simulation format (#50).
- The 23-point backups: Ubisoft decline, esports GOAT, most addictive game (CCU/owners proxy),
  Final Fantasy ranked, genre rise and fall, Skyrim re-releases, Japan vs West, one-hit-wonder
  studios.
- Scored lower: FIFA/EA FC pack simulation (22; ChrisMD real packs 6.8M, and a yearly game kills
  evergreen-ness) and early access completion (22).

---

## First 14 uploads

Rules applied:
- Open with the broadest and highest-scoring ideas.
- Alternate the four formats, and never put two from the same dataset back-to-back. The Metacritic
  "acclaim" set and the Steam achievement set each appear at least two slots apart.
- Spread the single-franchise videos (FromSoft, GTA) out.
- Put the one simulation built on a famous hook early.

| Slot | Video (# above) | Format | Main dataset | Why here |
|---|---|---|---|---|
| 1 | I Built a Model to Find the Most Overrated Game Ever (#1) | CD | MC + SH | Biggest debate with zero data competition. Sets the channel's identity. |
| 2 | I Analyzed 31 Million Players to Find FromSoft's Hardest Boss (#2) | MY | ACH | One of the biggest game families. The achievement chart is striking. |
| 3 | I Ranked Every Console Ever by Its Games, Not Its Sales (#4) | HH | MC + WP | Every gamer has a console opinion. Icon-friendly thumbnail. |
| 4 | I Built a Model to Find the Unluckiest Game Ever Released (#40) | SIM | MC + SS | Reuses the proven "unluckiest" model hook. The first simulation. |
| 5 | I Found the Greatest Comeback in Gaming History (#8) | MY | SH | Narrative arc built into the data (No Man's Sky / Cyberpunk curves). |
| 6 | I Analyzed 61,000 Games to Find the Worst Publisher Ever (#6) | CD | SS + MC | Anger-driven comments. Logo thumbnail. |
| 7 | I Checked 1,000 Games. Here's the One Nobody Finishes (#5) | MY | ACH | Relatable and universal. Five slots after the last achievement video. |
| 8 | I Compared Every Remake to Its Original. One Side Wins. (#16) | HH | MC | A clean two-sided debate. |
| 9 | I Built a Model to Find the Most Underrated Game on Steam (#9) | CD | SS | Companion-site bait: viewers look up their game. |
| 10 | I Analyzed 3,000,000 Speedruns to Find the Unbreakable Record (#42) | SIM | SR | A new audience (speedrunning). A different data source keeps the look fresh. |
| 11 | Games Aren't Getting Worse. I Checked 24,000 of Them. (#10) | HH (eras) | MC + SH | The largest general debate. Comes once the channel has some credibility. |
| 12 | I Found the Boss That Made the Most Gamers Quit (#3) | MY | ACH | The all-of-gaming sequel to slot 2, 10 slots later. |
| 13 | Critics vs Gamers: I Checked Who Was Right 14,000 Times (#11) | HH | MC + SH | Follows up slot 1's audience with a different question. |
| 14 | I Calculated the Best Value Game Ever Made (#15) | CD | HLTB + SA | Lighter, practical, very shareable. Validates the HLTB pipeline for #14 and #17 later. |

Timing swaps:
- **The Game Awards (early Dec 2026):** if uploads are weekly, slot 5 lands about then. Swap in #41,
  "I Re-Judged Every Game of the Year", for that week and push the rest back one.
- **GTA 6 launch window:** if GTA 6 launches in this window, #37 ("I Ranked Every GTA Game") can take
  the next free slot. Keep the title evergreen, with no "GTA 6" in it.

---

## Ideas rejected and why

| Idea | Reason |
|---|---|
| Best-selling / most-played games ever; console sales war; Switch vs PS2 race; esports prize money | **Saturated by bar-chart races.** Data Is Beautiful 4.7M / 1.3M, Global Stats 2.0M / 2.1M, Zorion 2.7M, Captain Gizmo, TierLine. Sales rankings are not a debate with an answer. |
| Pokémon battle sims, best starter, best type, most popular Pokémon, Pokémon luck math | **Taken.** Astroid 3.1M, Gym Leader Matt 811K (21 days), SmithPlays, adef 1.6M, MandJTV 6.3M, Wolfey 4.3M, UnlistedLeaf "official data" 4.5M. Only the game ranking (#21) survives. |
| Mario Kart best combo / item odds | **Shortcat owns it** (13.2M, 5.0M, 2.3M). |
| Speedrun history of one game, Tetris records | **Summoning Salt and aGameScout own it** (up to 20M). Kept only the cross-game data angle (#42). |
| "Steam is flooded / how many games make money" | **Developer-angle and done:** Newbie Indie Game Dev 1.6M plus many developer revenue videos. Fails the "for players" filter. |
| Most played Roblox / Roblox stats; Minecraft world/seed analysis | Data not reachable from the verified sources (Roblox API untested, no Minecraft telemetry). Minecraft "simulate" results are dominated by 1000-player civilization videos (56M), which is a different format. |
| CS2 skin market; Smash tier lists by results; esports GOAT | Niche or blocked data: the Steam market is untested, Liquipedia returns 429, and Smash results are unverified. Esports GOAT scored 23 and is a backup. |
| Game Pass effect, "Xbox losing the war", Starfield failure, battle royale dying, Ubisoft decline as its own video | **Time-bound or one-company news takes** (playbook losers). Their data angles fold into #6 (worst publisher) and #18 (fall from grace). |
| GTA 6 sales prediction; Game Awards 2026 predictor | **Time-bound.** E=1, and the playbook warns against putting a year in the title. GTA 6 enters only through the evergreen #37. |
| Steam sale timing / Nintendo never discounts | Needs price-history data (SteamDB / DekuDeals not verified). It's shopping advice, not a debate. |
| "What gamers hate" from review text | The Steam reviews endpoint redirects (302). Only aggregate histograms are available. Kaggle review dumps are old. |
| Most addictive game (playtime) | **SteamSpy playtime fields now return 0** (verified on CS and Cyberpunk). The only proxy is the CCU-to-owners ratio. Scored 23 and kept as a backup. |
| Best handheld; worst-selling consoles; console exclusives matter | Hardware opinion space (Linus 5M, Mrwhosetheboss 16M). There is no quality dataset for handheld libraries beyond #4's method, and exclusives data is weak. |
| Video game movies ranked | Off-niche (film data). Opinion lists already cover it (100-485K). |
| Easy mode debate | Big debate (Act Man 1.8M), but there is no data that answers "should". |
| Delisted / lost games | Low debate, and the data needs manual compilation. Covered by list channels (1.4-3.6M). |
| Generic "I simulated X 1 million times" (loot boxes, Monopoly-style) | `gap-analysis.md` found likely automated channels getting 1-19K views. A simulation without a fandom debate does not get views. |
