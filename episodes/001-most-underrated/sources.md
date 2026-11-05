# Sources and method: Episode 001

Every number in the script traces to a file in this folder or in `data/derived/` (rebuild with the commands below).

| Claim in script | Source |
|---|---|
| 51,897 games scored | `pipeline/underrated.py` training set: SteamSpy catalogue, games with ≥10 reviews, appid 220k–3.0M (≈2013–mid 2025) |
| ~15,000 games judged | candidates with ≥200 reviews (15,452) |
| Per-game reviews, % positive, expected reviews, "times short" | `data/derived/underrated.csv` → `facts.json` |
| ~1 review per 100 owners | SteamSpy owner-range midpoints vs review counts for the top-30 finalists (0.6–4.4%, typically ~1%) |
| Launch dates and collisions (Dying Light, Witcher 3, Rainbow Six Siege, Geometry Dash, Fallout 4) | Steam store `release_date` for finalists and for the 400 most-reviewed games → `data/derived/collisions.json` |
| 74% vs 62% launched within 7 days of a top-400 hit | `traits.json` (random sample n=141 with 2014+ dates; top-100 underrated n=84 with store data) |
| Median price $6.99 vs $11.99; 4% vs 17% at $20+ | SteamSpy `initialprice`; top-100 underrated (≥93% adj.) vs top-rated games with gap ≤ 1 (n=2,325) |
| Genre and multiplayer differences | Steam store genres/categories: 90 most-underrated games with store data vs 160 random games with ≥300 reviews |
| Supipara: 34% of English reviews in the last 2 years | Steam review histogram (English, monthly), `data/raw/histograms/496350.json` |
| Gravity Ghost monthly reviews chart | same, appid 251490 (English reviews only, shape only) |
| Metacritic scores (Gravity Ghost 75, Tadpole Treble 90) | Steam store `metacritic` field |
| Model check: same-era 95–97% games, median actual 4,748 vs model 4,588 | ad-hoc validation, see conversation log / rerun snippet in `pipeline/underrated.py` notes |

## Method choices (and why)
- **Reviews as the popularity proxy**: Steam doesn't publish sales. SteamSpy owner estimates exist only as wide ranges.
- **Bayesian shrinkage of ratings**: Beta prior fit on games with ≥200 reviews (mean 80%), so small samples get pulled toward the average.
- **Train on ≥10 reviews, crown only ≥200**: training only on ≥200 would truncate the low tail and inflate expectations.
- **Era via appid**: monotone with store-page date (calibrated against 160 release dates).
- **Exclusions**: pre-2014 releases (Steam reviews launched Nov 2013), re-releases and ports of older games, DLC and software, one game per developer. Full list with reasons: `exclusions.json`.

## Known limitations (said on screen where it matters)
- Reviews ≠ players; bundles inflate ownership without engagement.
- "Underrated" here = relative to games of similar rating and era, not relative to genre.
- Genre and price comparisons are correlations against a small random sample, not causes.

## Rebuild
```
python3 pipeline/underrated.py 200
python3 pipeline/finalists.py episodes/001-most-underrated/exclusions.json
python3 pipeline/collisions.py 10
python3 pipeline/ep001_traits.py
python3 pipeline/ep001_data.py
python3 pipeline/build_episode.py episodes/001-most-underrated --render
```
