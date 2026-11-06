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
- Stability: re-run with 7 settings (K = 100/150/300; rating and era scales halved/doubled). The same 7 games are in the
  top 10 every time. Final order = geometric mean of "times short" across the 7 runs (`robustness.json`).
  #1: Gravity Ghost in 4 of 7 settings, Escape Goat 2 in 3.

## Rules
- Released 2014 or later (Steam user reviews launched in November 2013).
- At least 200 reviews; no DLC, software or adult-flagged games; one game per developer (`pipeline/finalists.py`).
- Launched on Steam first: release histories checked by hand with sources for 51 candidates;
  34 had been released elsewhere first (browser/Flash, mobile, older PC versions, Japan), 1 is delisted.
  Verdicts and source URLs: `release_history.json`.

## Final list
1. Gravity Ghost: 96.3% positive, 302 reviews, expected 2,005, 6.6x short (range 5.17-7.99x); Gravity Ghost: first released 2015-01-26 on PC (wikipedia Gravity_Ghost)
2. Escape Goat 2: 95.5% positive, 441 reviews, expected 2,889, 6.5x short (range 5.68-7.61x); Escape Goat 2: same-day Steam/GOG/Humble 2014-03-24 (engadget)
3. Voidspire Tactics: 96.2% positive, 268 reviews, expected 1,426, 5.3x short (range 3.66-6.29x); Voidspire Tactics: launched Nov 2015 on Steam and direct same day (indierpgs.com)
4. Wand Wars: 95.8% positive, 218 reviews, expected 1,134, 5.2x short (range 3.97-6.7x); Wand Wars: PC 2016-04-13, consoles later (dekudeals)
5. The Journey Down: Chapter Two: 95.2% positive, 537 reviews, expected 2,314, 4.3x short (range 3.36-5.0x); The Journey Down Ch.2: launched 2014-08-25 Steam+Humble same day (gamingonlinux)
6. Nelly Cootalot: The Fowl Fleet: 94.5% positive, 291 reviews, expected 928, 3.2x short (range 2.42-3.7x); Nelly Cootalot: The Fowl Fleet: Steam + direct same day 2016-03-22 (gamingonlinux)
7. Stardust Galaxy Warriors: Stellar Climax: 93.4% positive, 226 reviews, expected 696, 3.1x short (range 2.64-3.71x); Stardust Galaxy Warriors: Steam 2015-11-10 first (steamdb)
8. Blackwell Epiphany: 97.6% positive, 934 reviews, expected 2,737, 2.9x short (range 2.56-3.4x); Blackwell Epiphany: same-day Steam/GOG/site 2014-04-24 (gogdb, pcgamer)
9. Starlight Vega: 93.4% positive, 255 reviews, expected 724, 2.8x short (range 2.56-3.12x); Starlight Vega: Steam+itch.io 2016-04-14, demos only before (opencritic)
10. I and Me: 95.8% positive, 358 reviews, expected 934, 2.6x short (range 2.07-3.96x); I and Me: Steam May 2016, Switch 2017 (wikipedia)

## Comparisons (correlations, not causes)
- Underrated-looking group: 44 games rated 93%+ (adjusted) with at least 1.5x fewer reviews than expected, released 2014+,
  no DLC/software/adult/re-releases, one per developer, leaving out games known to have launched elsewhere first
  (15 verified Steam-first, 29 not checked). Store data exists for all but one game at 1.5x+.
- Popular Steam games: random sample of games released 2014 or later with 300+ reviews (n=141). Not matched on rating
  or release year (the underrated group skews 2014-16 and higher-rated), so differences may partly reflect era.
- Timing: launched within 7 days (Steam store dates) of one of Steam's 400 most-reviewed games, never itself: 72% vs 66%.
- Genres: Casual 41% vs 25%; Strategy 16% vs 31%; Simulation 14% vs 34%; RPG 14% vs 30%.
- Online PvP (Steam store category) 4.5% vs 23%. Price $20+ (current SteamSpy list price): 1 of 44 (2%) vs 22%.
- Owners per review for the top 10: median 129 (SteamSpy owner-range midpoints).
- Displayed "expected" = reviews x consensus "times short" (geometric mean of the 7 runs). In the default run alone
  (K=150) Escape Goat 2 is #1 and Gravity Ghost #2; the video says the order is the average of all seven.
- The 7-run stability check ranks the hand-verified Steam-first pool; in the default run no unverified game would
  enter the top 10 (best 2.39x).
- Ratings shown are the adjusted score (e.g. Gravity Ghost 96.3% adjusted; 96.7% of its reviews are positive).
- Release dates are Steam store dates (e.g. Dying Light Jan 26, 2015 on Steam; Jan 27 in some regions).
- Review-history chart: English-language reviews only (138 of Gravity Ghost's 302).

## Known limitations
- Reviews are a proxy for players; the owners-per-review ratio varies widely.
- Ranks 6-10 are about 3x short, close to the model's typical error ("probably overlooked").
- Genre/price/timing comparisons are small samples and correlations.
- Neighbours of a 96%+ game are necessarily games with ~30+ reviews (shrinkage), which partly builds in the rising trend at the top.
- Sequels and later chapters (Escape Goat 2, Blackwell Epiphany, The Journey Down: Chapter Two) may get fewer reviews for structural reasons; the model compares them with all games.
