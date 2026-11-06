# Upload package — Episode 001

## Titles (Test & Compare: upload all 3; YouTube picks by watch time)
1. I Built a Model to Find the Most Underrated Game on Steam
2. I Scored 51,897 Steam Games to Find the Most Underrated One
3. This Game Launched the Same Day as Dying Light

(Playbook check: first person ✓, big exact number ✓ (#2), superlative ✓, no year, no parentheses, all ≤ 60 chars. #3 deliberately makes no causal claim: the video finds timing isn't the pattern.)

## Thumbnails (render with `npx remotion still src/index.ts Thumbnail` + props in thumbnails/*.json)
- **A `dot` (PRIMARY, owner pick)**: scatter cloud, one red-circled dot, arrow, "ROBBED." No game art (never spoil #1).
- B `number` (test variant): "302" huge + "REVIEWS. 97% LOVED IT." + the red dot.
- C `versus` (test variant): "?" card vs Dying Light art, "SAME DAY." The mystery game is never shown.

## Description
I scored 51,897 Steam games to find the great ones that got overlooked. For every game, the model looks at the 150 most similar games (same rating, same launch window) and asks how many reviews it should have had. Only games that launched on Steam first count.

{{CHAPTERS}}

How it works
• Popularity = Steam review count (Steam doesn't publish sales; SteamSpy owner estimates suggest roughly 1 review per 130 owners for the games in this video).
• Rating = % positive, shrunk toward the Steam average so tiny games can't top the list on 20 reviews.
• Model = for each game, the median review count of the 150 most similar games (rating + launch window). Typical miss on a single game: about 2.7x. Re-run 7 different ways; the same 7 games made the top 10 every time.
• Rules: released 2014+, 200+ reviews, launched on Steam first (51 release histories checked by hand), no DLC/software, one game per studio.

Games in this video (A-Z, so the list doesn't spoil #1): Blackwell Epiphany · Escape Goat 2 · Gravity Ghost · I and Me · Nelly Cootalot: The Fowl Fleet · Starlight Vega · Stardust Galaxy Warriors: Stellar Climax · The Journey Down: Chapter Two · Voidspire Tactics · Wand Wars

Data: Steam store & review data (Valve), SteamSpy (owner/review counts; owner figures are estimates). Not affiliated with or endorsed by Valve or any developer shown. Game art is used for commentary and identification.

Which game did my model miss? Tell me in the comments.

#steam #indiegames #hiddengems

## Tags (limited role; misspellings and variants)
underrated games, underrated steam games, hidden gems steam, best indie games, steam hidden gems, most underrated game, gravity ghost, indie games you missed, steam data, games nobody played

## Pinned comment
Which game should've made the list? I'll run the ones you suggest through the model and show the results in a future video. Next up: the most OVERRATED game on Steam.

## End screen
Next video (Overrated) + subscribe. Last 20 s of narration is the hand-off line.

## Quality gate (human-feel-guide §7) — fill in before publishing
- [ ] script_lint PASS (zero hard hits, soft penalty ≤ 5)
- [ ] Every claim traceable to facts.json / robustness.json / data.json (see sources.md)
- [ ] At least one genuine surprise the narrator reacts to (timing theory: 66% vs 72%, if anything slightly fewer)
- [ ] Structure differs from previous uploads (n/a: first upload)
- [x] No single picture held > ~13 s; long explanations split into beats (audit 2026-11-06)
- [ ] Thumbnail promise paid off (red dot = #1, revealed at the end)
- [ ] A person watched the final cut at 1.5x
