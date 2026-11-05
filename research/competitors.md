# Competitor deep-dive: data stories about video games (2026-11-05)

Our lane: "I built a model / analyzed / simulated" data stories about video games, made for **players**
(not developers). AI narration, motion-graphics charts. Read with `gap-analysis.md` and `packaging-playbook.md`.

## Method and caveats
- **Video lists** come from `yt-dlp --flat-playlist -J --playlist-end 300` on each channel's /videos tab, plus
  `--extractor-args youtubetab:approximate_date` for upload dates. These dates are YouTube's relative labels
  ("3 months ago", "1 year ago"), so they are exact to the month under a year and to the **year** beyond that.
  Water CS2 was refetched in full (1,104 videos).
- **Subscriber counts** are `channel_follower_count` from yt-dlp. I did not open any watch pages, and I did not
  try anything that bot checks block.
- **"x median"** is a video's views divided by its channel's median. The median leaves out the 3 newest videos
  because their views are still coming in. This is the same method as the packaging playbook.
- **Discovery:** 52 search queries through `tools/youtube_niche_scan.py` (gaming data, Steam, sales, Metacritic,
  console war, achievements, speedruns, CS2 stats, Minecraft stats, and others).
- **Format and style notes** are inferred from titles, durations and search snippets. I watched no videos.
- **Limits:** "No results" means no data-format title in the top ~20 search results for that query. It does not
  prove a topic is untouched anywhere on YouTube.

---

## Summary table

| Channel | Subs | Videos | Median views | Max views (x median) | Cadence (recent) | Audience |
|---|---|---|---|---|---|---|
| Newbie Indie Game Dev (@NewbieIndieGameDev) | 36.6K | 22 in ~5 yrs | 9.3K | 1.5M (162x) | ~2 in last 12 months; none in the last ~8 months | Devs plus curious players |
| Water CS2 (@watercs) | 75.7K | 1,104 | 39K (last 300) | 1.7M (44x) | ~1.5/week now, ~1.5/day 3 years ago | Valve/Steam news |
| Data Time (@DataTime27) | 146K | 48 in ~5 yrs | 8.1K | 968K (120x) | ~4 in last 12 months | General curiosity, YouTube-creator corpora |
| i am a dot. (@i_am_a_dot) | 113K | 39 in ~2-3 yrs | 100K | 4.4M (44x) | ~monthly (13 in last 12 months) | Game-essay viewers |
| Game Oracle (@Game-Oracle) | 6.3K | 18 in ~1 yr | 1.1K | 283K (257x) | ~1.5/month | Indie devs (Steam market research) |
| Data Is Beautiful (@DataIsBeautifulOfficial) | 1.41M | 119 | 486K (lifetime) | 38M | ~1/week in 2026 | General; bar-chart races |
| Super Bunnyhop (@bunnyhopshow) | 432K | 300+ | 183K | 2.2M (12x) | ~1/month | Essay/critique |
| How To Market A Game (@howtomarketagame) | 20.1K | 64 | 3.1K | 41K (13x) | ~3/month | Indie devs |
| forrest yaps (@forrestyaps) | 3.6K | 15 in ~2-3 months | 19K | 210K (11x) | ~1.5/week | CS2 / Balatro players |
| fakeduck (@fakeduck-yt) | 2.8K | 7 | 13.5K | 26K (1.9x) | none in last ~12 months | CS2 esports fans |
| vindalol (@vindalolz) | 5.5K | 5 in ~2-3 months | 10K | 717K (72x) | ~2/month | Gen-Z internet culture |
| David makes games (@DavidReidChannel) | 3.0K | 15 | 3.7K | 46K (13x) | ~monthly | Devlog |
| GameDevIntel (@GameDevIntel) | 18 | 2 | 458 | 462 | new | Devs (Steam sales) |
| Captain Cabinetz (@captaincabinetz) | 70.7K | 300+ in ~8 months | 9K | 339K (38x) | **~1.2/day** | Gacha/League reaction (one data video) |

One-off data videos from other channels that show demand (search results; age approximate):
Shwep "Completing All 6,280 Minecraft Statistics" 1.78M (~1y) · FitMC "The Shocking Data Behind Minecraft's 2b2t" 1.53M (~5y) ·
Orrnery "I played and Ranked EVERY Game of the Year" 1.37M (~9mo, played rather than data) ·
STYKO "We Analyzed 10,000 Rounds to Find the Strongest Positions" 215K (~1mo) ·
Leverage In Action "I Tried Using Data Science to Profit in a Video Game Economy" 75K ·
Captain Cabinetz "I Simulated 2 Million Pulls to Compare Every Gacha System" 18K ·
YUTZYtv "Exploring Steam's Strange Achievement Stats" 5.5K ·
FrBlank "Why Are Games So Expensive? (I Did the Math)" 314 · Tobys Data Digest "I Analysed 120,000 Steam Games… Here's Why Some Go Viral" 303 ·
Arcadelytics "I Simulated Steam… and Found the MOST Profitable Game" 164 · Dima G "I Analyzed 7,437 Steam Games — … Capsules Is Wrong" 74.

---

## 1. Newbie Indie Game Dev (@NewbieIndieGameDev): the direct threat
**36.6K subs · 22 videos over ~5 years · median 9.3K · videos run 4-16 min (median 9.7 min).**
Cadence is bursty: 8 videos landed in a single "1 year ago" batch, which produced all the hits. The most recent
uploads are about 10 and 8 months old (one is a collab whose view count is hidden). Nothing has come out in the
last ~8 months. The channel is **semi-dormant**.

| # | Views | x median | Title |
|---|---|---|---|
| 1 | 1,500,000 | 162x | I Scraped the Entire Steam Catalog, Here's the Data |
| 2 | 284,000 | 31x | I Downloaded EVERY Silksong Review, Here's the Data |
| 3 | 252,000 | 27x | I Made a Soft-Body Tetris That's Actually Playable |
| 4 | 126,000 | 14x | Mario is (NP-) Hard |
| 5 | 95,000 | 10x | Can a Single Screenshot Predict a Game's Success? |
| 6 | 89,000 | 10x | The Code Behind My 30,000 Pokémon Card Mosaic |
| 7 | 63,000 | 7x | I Merged Pac-Man and Snake |
| 8 | 61,000 | 7x | I Counted Every Box in Baldur's Gate 3 |
| 9 | 38,000 | 4x | I Rebuilt Monument Valley, Here's How |
| 10 | 17,000 | 2x | How I made Getting Over Goombas |

- **Topics covered:** the whole Steam catalog (prices, tags, releases, reviews); every Silksong review; whether a
  screenshot predicts success; counting boxes in BG3; NP-hardness of Mario; Perlin noise; plus devlogs and remakes.
- **Format:** a developer on camera or narrating, showing code and charts. Programming appears in about half the videos.
- **What the top titles share:** "I [scraped/downloaded/counted] EVERY/the Entire X, Here's the Data". These combine
  completeness and effort with a famous subject (Steam, Silksong, BG3, Mario).
- **What it doesn't do (our openings):** no recurring series or regular cadence; no models or simulations that settle
  player debates; no "best/worst/most underrated ever" answers; no cross-platform or console work; almost nothing
  about review scores across all of gaming; developer framing ("success" means sales).

## 2. Water CS2 (@watercs): Steam news, not a data channel
**75.7K subs · 1,104 videos · median of last 300 = 39K · ~7 min · no Shorts in the /videos tab.**

| # | Views | x median | Title |
|---|---|---|---|
| 1 | 1,700,000 | 44x | Who Owns North Korea's Steam Account? |
| 2 | 1,200,000 | 31x | SteamOS Just Came to Mobile (And It Changes Everything) |
| 3 | 879,000 | 23x | Gabe Newell's Opening Speech at The International 2026 |
| 4 | 658,000 | 17x | Visa Responds To Censoring Steam Games |
| 5 | 621,000 | 16x | Collective Shout Now Wants Gamers Arrested |
| 6 | 619,000 | 16x | Steam's New Codec Uses 10x Bandwidth |
| 7 | 606,000 | 16x | The 13TB Steam Leak Is Bigger Than You Think |
| 8 | 597,000 | 15x | Valve Responds To PayPal Banning Steam |
| 9 | 579,000 | 15x | Valve REVEALS Mastercard LIED About Censoring Games |
| 10 | 568,000 | 15x | The Real Reason Valve Made The Steam Machine "WEAK" |

Its one data-shaped hit was **"Steam's New Data Just Made $70 Games Look Pathetic" (333K, 8.5x, ~10 months ago)**.
Others in that style: "CS2 Lost 250,000 'Players' After New Update" (0.4x) and "New VAC Bans & CS2 Cheat Stats" (0.5x).
- **Topics:** Valve and Steam news, payment-processor censorship, Steam Machine and Deck, Half-Life 3 leaks, lawsuits, CS2 updates.
- **What the titles share:** conflict between named actors (Valve vs Visa/Epic/PayPal), "Just", "REVEALS", "Bigger Than You Think".
- **What it doesn't do:** original analysis. It reacts to Valve's own numbers. Our opening is the deeper data story
  behind its headlines (for example, what $70 games actually do on Steam over the long run).
- **Cadence lesson:** see §4 below.

## 3. Data Time (@DataTime27): format twin, but not about games
**146K subs · 48 videos over ~5 years · median 8.1K · ~11 min, newer ones 23-27 min.**

| # | Views | x median | Title |
|---|---|---|---|
| 1 | 968,000 | 120x | I analyzed all words on the Mr Beast channel |
| 2 | 850,000 | 105x | I used AI to analyze presidential speeches... I was surprised |
| 3 | 583,000 | 72x | Disaster in California: I went to the San Andreas Fault |
| 4 | 440,000 | 54x | I analyzed all writers on Game Theory |
| 5 | 350,000 | 43x | I downloaded every word from Jet Lag The Game |
| 6 | 325,000 | 40x | I downloaded every Game Theory word |
| 7 | 214,000 | 26x | I analyzed all Vsauce words using AI |
| 8 | 204,000 | 25x | I used AI to analyze Trump and Harris's words... |
| 9 | 151,000 | 19x | 100 prisoners riddle: Can I demonstrate if Veritasium is right? |
| 10 | 131,000 | 16x | Can I prove Neil deGrasse Tyson is wrong |

- **Topics:** word and transcript analysis of big YouTubers (MrBeast, Game Theory, Vsauce, Veritasium, Markiplier,
  Jet Lag, Taskmaster), political speeches, flat-earth experiments.
- **Format:** a personal on-camera presenter running experiments. Long runtimes, and about 4 uploads a year lately.
- **What the titles share:** "I analyzed / downloaded ALL/every [words] of [famous creator]". The subject's fandom
  carries the views. Off-format videos (vlogs, travel) get 0.1-0.4x.
- **What it doesn't do:** video games themselves (Game Theory and Markiplier are about creators, not games). There
  is no collision as long as we don't analyze game-YouTuber transcripts.

## 4. i am a dot. (@i_am_a_dot): essay channel, tried data once
**113K subs · 39 videos over ~2-3 years · median 100K · ~22 min · about monthly.**

| # | Views | x median | Title |
|---|---|---|---|
| 1 | 4,400,000 | 44x | Games Where You're NOT the Main Character |
| 2 | 977,000 | 9.8x | When a Sequel is SO GOOD it RUINS its Series |
| 3 | 805,000 | 8.1x | How Do Humongous Entertainment's Adventure Games Actually Work? |
| 4 | 620,000 | 6.2x | Night in the Woods' Most Profound Question |
| 5 | 341,000 | 3.4x | What Does Dispatch Gain From Being Interactive? |
| 6 | 320,000 | 3.2x | Is This the Strangest Remake Ever? |
| 7 | 290,000 | 2.9x | My Brief Obsession with the Worst RPG Ever Made |
| 8 | 280,000 | 2.8x | The Horror Game That Hates Horror Games |
| 9 | 201,000 | 2.0x | Super Metroid's Greatest Moment |
| 10 | 198,000 | 2.0x | The Game That's IMPOSSIBLE to Master |

**Its data video, "I Analyzed 20+ Years of Video Game Awards Data. Here's What I Learned..." (51K), got 0.5x**, one of
the channel's weaker results.
- **Topics:** design essays on single games (Night in the Woods, Firewatch, Control, Uncharted, Persona 5, Pikmin, Paper Mario).
- **What the titles share:** a category concept stated simply ("Games Where You're NOT the Main Character",
  "When a Sequel is SO GOOD it RUINS its Series").
- **Takeaway:** essay audiences don't reward data for its own sake. The **sequel-vs-original** idea did 977K as an
  essay, and nobody has answered it with data (whitespace).

## 5. Game Oracle (@Game-Oracle): closest in method, aimed at developers
**6.3K subs · 18 videos in ~1 year · median 1.1K · ~11 min.**

| # | Views | x median | Title |
|---|---|---|---|
| 1 | 283,000 | 257x | I Analysed 62,000 Indie Developers. Here's What Actually Predicts Success |
| 2 | 96,000 | 87x | The Developers Making Successful Games You've Never Heard Of |
| 3 | 4,300 | 3.9x | The Steam Map |
| 4 | 3,500 | 3.2x | The Hidden AI Boom on Steam |
| 5 | 3,200 | 2.9x | The Steam Algorithm Isn't Your Marketing Plan… This Is |
| 6 | 2,600 | 2.4x | Why You Might Not Need Thousands of Steam Wishlists |
| 7 | 2,100 | 1.9x | We Made a Map of Every Game on Steam… but Why? |
| 8 | 1,600 | 1.5x | Why Survival Games Are Getting on Trains |
| 9 | 1,600 | 1.5x | Why Indie Devs Keep Abandoning Brewing Sims |
| 10 | 1,200 | 1.1x | The 5 Eras of Steam Every Indie Dev MUST Understand |

- **Topics:** predictors of indie success, a map or clustering of every Steam game, 12 years of Steam releases,
  AI-made games on Steam, niche genre trends, Christmas games, wishlists. These are market-research videos for devs.
- **Lesson:** the 2 breakouts (Steam-wide scope, big exact number, "what actually predicts") cleared 1,000x the
  dev-jargon titles. Wishlists, the algorithm and market research all cap at about 3K.
- **What it doesn't do:** player questions (best, worst, underrated, value for money), consoles, review scores.

## 6. Other channels
- **Data Is Beautiful (1.41M):** animated bar-chart races. Its 2019-2020 gaming races were huge: "Best-Selling Video
  Game Consoles 2004-2019" 7.8M, "Most Popular Streamed Games" 5.9M, "Most Sold Video Games of All Time" 4.6M,
  "Most Popular Android Games" 3.9M, "Console Wars 2001-2022" 1.2M, "Most Popular Games on Steam 2012-2019" 1.2M.
  **2026 uploads get about 50K median on 1.4M subs**, and "Most Popular Gaming Consoles 1985-2025" got 428K (0.9x).
  Narration-free race charts are in steep decline. **Taken:** console sales and best-selling-games races. Don't
  make a race chart. Make a story or model about the same data.
- **Super Bunnyhop (432K):** critique and history. Data-adjacent: "Statistically Speaking: Metacritic's 'Best Games
  of All Time'" (233K, 1.3x, ~6 years ago) and "Global Warming, as Depicted by 30 Years of Strategy Games" (216K).
  Its top video is business: "How Telltale Went Broke" (2.2M, 12x). Industry money stories travel.
- **How To Market A Game (Chris Zukowski, 20.1K):** Steam data for devs in 30-130 min streams. Owns Steam Next Fest,
  wishlists and "were there too many games in 2024". Best is 41K. Proves dev-facing Steam data has a low ceiling.
- **forrest yaps (3.6K, ~2-3 months old):** "A PowerPoint About Counter-Strike and [Bayesian Statistics / Information
  Theory / Game Theory / Expected Value / Markov Chains / Goodhart's Law / Prisoner's Dilemma …]" and "Balatro and
  Search Theory". The first video hit 210K. Later ones fell to about 10K at ~1.5 uploads a week. **Taken:** math
  concepts applied to CS2, and Balatro search theory. Lesson: a strong series hook can wear out quickly when every
  episode is the same game.
- **fakeduck (2.8K):** CS2 pro-player data ("most (in)consistent CS2 player" 26K, "10 Million CS Kills" 9.3K). Flat
  performance and dormant. Esports-stat topics alone don't break out.
- **vindalol (5.5K):** "i graphed the ENTIRE Minecraft community" got 618K on its 4th video. Together with Shwep
  (1.78M) and FitMC (1.53M), this marks **Minecraft as the single game big enough** to carry a data video.
- **David makes games / GameDevIntel / Tobys / Arcadelytics / Dima G:** a crowd of tiny "I analyzed N,000 Steam games"
  videos for devs (74-13K views). They show that the "N Steam games for indie success" angle is saturated and
  low-ceiling.
- **Captain Cabinetz (70.7K):** a daily gacha and League reaction channel. Its one data video, "I Simulated 2 Million
  Pulls to Compare Every Gacha System", got 18K (2x). The topic is taken but not well exploited.

---

## Conclusions

### (1) Taken topics: avoid, or clearly beat
| Topic | Owner (views) | Verdict |
|---|---|---|
| Scraped the whole Steam catalog (general overview) | Newbie 1.5M | Don't redo it generically. Only do it with a sharp player question (for example "best game per dollar on Steam") |
| Every review of one hyped game (Silksong) | Newbie 284K | Allowed for the next mega-launch (GTA VI), but must be framed as "the data" |
| Screenshot predicts success | Newbie 95K | Avoid |
| What predicts indie success / 62,000 developers / map of every Steam game | Game Oracle 283K / 96K | Avoid; dev-facing |
| Steam Next Fest, wishlists, "too many games", what sold in H1 | HTMAG, GameDevIntel, David | Avoid; dev-facing and low ceiling |
| $70 games vs cheaper games (Steam data) | Water CS2 333K | Beat it only with real analysis (price vs playtime/reviews/regret) |
| 20+ years of game-awards data | i am a dot 51K (weak) | Beatable. A GOTY **predictor model** is open and timely (The Game Awards in December) |
| Played and ranked every GOTY | Orrnery 1.37M | Different format; our version must be data-ranked, not played |
| Metacritic "best games of all time" statistics | Super Bunnyhop 233K (~6y ago) | Old; OK to redo with a modern critic-vs-player model |
| Console sales, best-selling games, most popular Steam/streamed games over time | Data Is Beautiful (1-8M, 2019-22) | Avoid race charts; use only as context inside a story |
| Math concepts applied to CS2; Balatro search theory | forrest yaps | Avoid CS2-plus-theory framing |
| CS2 pro consistency, kills, strongest positions | fakeduck, STYKO 215K | Avoid |
| Minecraft community graph, all Minecraft stats, 2b2t data | vindalol, Shwep, FitMC | Avoid those angles; Minecraft itself is still open |
| Pokémon battle simulations | Astroid, SmithPlays, Gym Leader Matt | Saturated (per gap-analysis) |
| Gacha pull simulation | Captain Cabinetz 18K | Beatable, but niche |
| Data science in a game economy | Leverage In Action 75K | Avoid |
| Word analysis of game-YouTuber transcripts | Data Time | Avoid |

### (2) Whitespace: no data-format results for the query (top ~20 search results)
1. **Critic vs player divergence:** "most overrated / most underrated video game ever (data)". Zero results.
   Data: Metacritic/OpenCritic vs Steam user reviews.
2. **"How many players actually finish games?"** from Steam global achievement rates for the biggest games, plus
   HowLongToBeat length. Achievement queries returned only 1 small video (5.5K); `howlongtobeat data` returned nothing.
3. **"Are video games getting longer / worse / more expensive?"** Zero data results for the first two. Price history
   adjusted for inflation has only one 314-view video.
4. **Sequel vs original, remake vs original, by the numbers.** The essay version did 977K; no data version exists.
5. **Console war, settled with a model** (not a race chart). `console war data` returned zero data-format titles
   while general results had a 108K median.
6. **Franchise-wide analyses:** every Zelda, Mario, Nintendo, PlayStation or Elden Ring game analyzed. All zero.
7. **Speedrun world-record progressions** (speedrun.com API). Zero.
8. **Review bombing data.** Zero results that were actual analysis.
9. **Live-service death model:** which games die and when, from SteamCharts concurrent players. Only tutorials appeared.
10. **GOTY predictor and "biggest GOTY robbery ever"** model. Only one weak awards-data video exists, and The Game
    Awards in December makes this timely. Keep the year out of the title.
11. **Minecraft beyond the community graph** (for example "I simulated 1,000,000 Minecraft worlds").
    Minecraft is proven to carry data videos.

### (3) What gaming-data audiences respond to
- **Gaming-wide or mega-game subjects beat single games and niches.** Newbie: whole catalog 1.5M, then Silksong 284K,
  then BG3 boxes 61K. Game Oracle: 62,000 developers 283K vs genre niches ~1.5K. The exceptions are only the biggest
  games (Minecraft 618K-1.78M, Silksong, CS2).
- **Players beat developers.** Every dev-facing title (wishlists, algorithm, Next Fest, capsules, "what sold")
  tops out around 1-40K. The dev-channel breakouts were the ones with player-readable framing ("What Actually
  Predicts Success", "Games You've Never Heard Of").
- **Money and drama beat review scores in general, but reviews win when tied to a hyped game.** Examples:
  "Telltale Went Broke" 2.2M; "$70 Games Look Pathetic" 333K; Valve vs payment processors at 500-650K each.
  Review-score topics: Silksong reviews 284K, Metacritic stats 233K (1.3x), awards data 0.5x.
  Best bet: a review or score question with stakes ("overrated", "robbed", "worth the money").
- **Pure chart animation is fading.** Data Is Beautiful went from 4-8M gaming races (2019) to about 50K median
  in 2026. Narrative plus a model is the differentiator.
- **Data framing doesn't help essay audiences** (i am a dot's data video got 0.5x). We need a question that grabs
  people who didn't come for data.
- **Titles that win:** "I [Scraped/Downloaded/Analysed] [EVERY / big exact number] X, Here's [the Data / What Actually …]".
  Examples: 62,000; 10,000 rounds; "Entire Steam Catalog"; "EVERY Silksong Review". This matches the packaging playbook.

### (4) Cadence: does anyone post daily, and does it work?
- **No gaming data-story channel posts daily.** The breakout data channels post rarely: Newbie made 22 videos in
  ~5 years (1.5M hit), Data Time ~4 a year (146K subs), vindalol 5 videos with two over 600K, Game Oracle ~1.5 a month.
- **Water CS2** is the only big gaming channel that ran near-daily: ~544 uploads in the "3 years ago" year
  (~1.5/day) at a ~10K median per video. It then cut to 109 in the "1 year ago" year (~49K median) and to 79 in the
  last 12 months (~1.5/week, monthly medians 43K-546K, most of them above 80K). Per-video views rose about 10x as cadence fell.
  This is confounded by subscriber growth, and older videos had more time to gain views, which makes the rise
  understated if anything. Daily volume may have built the base, but its news format can be churned out; ours can't.
- **Captain Cabinetz** (~1.2/day, 9K median, 70.7K subs) shows daily works for cheap reaction streams, not for produced analysis.
- **forrest yaps** at ~1.5/week on a single topic decayed from 210K to about 10K per video in 2 months.
- **Reference: Spreadsheet Sports** posts daily NBA videos, but its views come from a few model-settles-a-debate hits.
- **Recommendation:** 1-2 well-packaged long-form videos per week beats daily. Gap-analysis also warns that daily
  "I simulated X" channels look automated and get 1-19K views. If we want daily output, Shorts cut from each
  long-form video are a lower-risk way to do it.
