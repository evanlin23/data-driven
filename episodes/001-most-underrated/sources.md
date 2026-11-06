# Sources and method: Episode 001 (final)

Every number in the script comes from `facts.json` (built by `pipeline/ep001_facts.py`) or `robustness.json`.

## Data
- SteamSpy catalogue (positive/negative review counts, list price, owner ranges); 87 pages, fetched 2026-11-05.
- Steam store pages (release date, genres, categories, Metacritic, description) via the store appdetails endpoint.
- Steam monthly review histograms (English-language reviews only, used for the review-history chart).
- Snapshot: `data/snapshots/raw-2026-11-05.tgz`.

## Model (`pipeline/underrated_knn.py`)
- Rating = % positive, shrunk toward the Steam average (80%), weighted by review count.
- Expected reviews = median review count of the 150 most similar other games (same rating, same launch window).
  The launch window uses the release date when known, otherwise the store-page age (appid).
- Typical miss on a single game: 2.68x.
- Stability: re-run with 7 settings (K = 100/150/300; rating scale 0.10/0.25 around 0.15; era scale halved/doubled). The same 7 games are in the
  top 10 every time. Final order = geometric mean of "times short" across the 7 runs (`robustness.json`).
  #1: Gravity Ghost in 4 of 7 settings, Escape Goat 2 in 3.

## Rules
- Released 2014 or later (Steam user reviews launched in November 2013).
- At least 200 reviews; no DLC, software or adult-flagged games; one game per developer (`pipeline/finalists.py`).
- Launched on Steam first: release histories checked by hand with sources for 51 candidates;
  34 had been released elsewhere first (browser/Flash, mobile, older PC versions, Japan), 1 is delisted.
  Verdicts and source URLs: `release_history.json`.

## Final list (from facts.json; % = real share of positive reviews)
1. Gravity Ghost: 96.7% positive, 302 reviews, expected 2,006, 6.6x short (range 5.17-7.99x); Gravity Ghost: first released 2015-01-26 on PC (wikipedia Gravity_Ghost)
2. Escape Goat 2: 95.7% positive, 441 reviews, expected 2,890, 6.6x short (range 5.68-7.61x); Escape Goat 2: same-day Steam/GOG/Humble 2014-03-24 (engadget)
3. Voidspire Tactics: 96.6% positive, 268 reviews, expected 1,426, 5.3x short (range 3.66-6.29x); Voidspire Tactics: launched Nov 2015 on Steam and direct same day (indierpgs.com)
4. Wand Wars: 96.3% positive, 218 reviews, expected 1,133, 5.2x short (range 3.97-6.7x); Wand Wars: PC 2016-04-13, consoles later (dekudeals)
5. The Journey Down: Chapter Two: 95.3% positive, 537 reviews, expected 2,314, 4.3x short (range 3.36-5.0x); The Journey Down Ch.2: launched 2014-08-25 Steam+Humble same day (gamingonlinux)
6. Nelly Cootalot: The Fowl Fleet: 94.8% positive, 291 reviews, expected 928, 3.2x short (range 2.42-3.7x); Nelly Cootalot: The Fowl Fleet: Steam + direct same day 2016-03-22 (gamingonlinux)
7. Stardust Galaxy Warriors: Stellar Climax: 93.8% positive, 226 reviews, expected 696, 3.1x short (range 2.64-3.71x); Stardust Galaxy Warriors: Steam 2015-11-10 first (steamdb)
8. Blackwell Epiphany: 97.8% positive, 934 reviews, expected 2,735, 2.9x short (range 2.56-3.4x); Blackwell Epiphany: same-day Steam/GOG/site 2014-04-24 (gogdb, pcgamer)
9. Starlight Vega: 93.7% positive, 255 reviews, expected 725, 2.8x short (range 2.56-3.12x); Starlight Vega: Steam+itch.io 2016-04-14, demos only before (opencritic)
10. I and Me: 96.1% positive, 358 reviews, expected 935, 2.6x short (range 2.07-3.96x); I and Me: Steam May 2016, Switch 2017 (wikipedia)

## Comparisons (correlations, not causes)
- Underrated-looking group: 34 games rated 93%+ (adjusted) with two-thirds or less of the expected reviews
  (default run gap >= 1.5x), released 2014+, no DLC/software/adult, known re-releases and earlier releases left out
  (exclusions.json), one per developer: 15 verified Steam-first, 19 not checked. Small sample.
- Popular Steam games: random sample of games released 2014 or later with 300+ reviews (n=141). Not matched on rating
  or release year (the underrated group skews 2014-16 and higher-rated), so differences may partly reflect era.
- Timing: launched within 7 days (Steam store dates) of one of Steam's 400 most-reviewed games, never itself:
  71.6% vs 67.6%. 63% of all calendar days 2014-2025 fall within a week of one of those 400 games.
- Genres (6 of 34 RPG, 5 strategy, 4 simulation): Casual 47% vs 25%; Strategy 15% vs 31%; Simulation 12% vs 34%; RPG 18% vs 30%.
- Online PvP (Steam store category) 2.9% vs 22.7%. Price $20+ (current SteamSpy list price): 2.9% vs 22.3%.
- Model error: typical miss 2.68x across all 51,897 scored games; among games with 200+ reviews
  only 0.9% are that far short (the model underpredicts most 200+ games, since lookalikes include tiny games).
- Owners per review for the top 10: median 129 (shown as 130) (SteamSpy owner-range midpoints).
- Displayed "expected" = reviews x consensus "times short" (geometric mean of the 7 runs). In the default run alone
  (K=150) Escape Goat 2 is #1 and Gravity Ghost #2; the video says the order is the average of all seven.
- The 7-run stability check ranks the hand-verified Steam-first pool (16 games). In the default run no unverified game
  would enter the top 10 (best 2.39x); in other settings some unverified games would (e.g. Unium, Mr. Massagy,
  Secret Sealing Travel), so the claim is about the checked finalists, as the video says.
- Ratings shown and spoken are the real share of positive reviews (e.g. Gravity Ghost 96.7% -> 97%); the adjusted
  (shrunk) score is used only for the model and the scatter's x axis (Gravity Ghost 96.3%).
- Release dates are Steam store dates, often a day earlier than commonly cited dates (Dying Light Jan 26 vs Jan 27;
  Life is Strange Ep. 1 Jan 29 vs Jan 30; Black Ops III Nov 5 vs Nov 6; Fallout 4 Nov 9 vs Nov 10). The video says 'on Steam'.
- RPG share in the underrated-looking group (6/34 vs 42/141) is not distinguishable from chance (Fisher p~0.2), so
  the video doesn't claim it; strategy (p~0.06), simulation (p~0.01), online PvP and $20+ (p~0.006) are.
- Review-history chart: English-language reviews only (138 of Gravity Ghost's 302).

## Known limitations
- Coverage: store-page appids 220000 to 3,000,000, i.e. games whose Steam page was created by about mid-2024; newer
  games (a few hundred with 200+ reviews) are not scored.
- Casual share among the 15 release-checked games in the comparison group is 5/15 (33%) vs 11/19 (58%) among the
  unchecked ones; the video says so.
- Reviews are a proxy for players; the owners-per-review ratio varies widely.
- Ranks 6-10 are about 3x short, close to the model's typical error ("probably overlooked").
- Genre/price/timing comparisons are small samples and correlations.
- Neighbours of a 96%+ game are necessarily games with ~30+ reviews (shrinkage), which partly builds in the rising trend at the top.
- Sequels and later chapters (Escape Goat 2, Blackwell Epiphany, The Journey Down: Chapter Two, Nelly Cootalot: The Fowl Fleet, a sequel to the 2007 freeware Spoonbeaks Ahoy!) may get fewer reviews for structural reasons; the model compares them with all games.
