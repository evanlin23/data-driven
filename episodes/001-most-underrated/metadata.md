# Upload package — Episode 001

## Titles (Test & Compare: upload all 3; YouTube picks by watch time)
1. I Built a Model to Find the Most Underrated Game on Steam
2. I Scored 51,897 Steam Games to Find the Most Underrated One
3. This Game Launched the Same Day as Dying Light. It Got Buried.

(Playbook check: first person ✓, big exact number ✓ (#2), superlative ✓, no year, no parentheses, all ≤ 60 chars except #3 (61), so trim #3 if Studio truncates.)

## Thumbnails (render with `npx remotion still src/index.ts Thumbnail` + props in thumbnails/*.json)
- **A `dot` (PRIMARY, owner pick)**: scatter cloud, one red-circled dot, arrow, "ROBBED." No game art (never spoil #1).
- B `number` (test variant): "302" huge + "REVIEWS. 96% LOVED IT." + the red dot.
- C `versus` (test variant): "?" card vs Dying Light art, "SAME DAY." The mystery game is never shown.

## Description
I scored 51,897 Steam games to find the ones that got robbed: games players loved that almost nobody showed up for. The model predicts how many reviews a game *should* have from its rating and release year, then ranks games by how far short they landed.

{{CHAPTERS}}

How it works
• Popularity = Steam review count (Steam doesn't publish sales; SteamSpy owner estimates suggest ~1 review per 100 owners for these games).
• Rating = % positive, shrunk toward the Steam average so tiny games can't top the list on 20 reviews.
• Model = gradient-boosted median regression on rating + release era, trained on every game with 10+ reviews (out-of-fold predictions).
• Rules: released 2014+, no re-releases of older games, no DLC/software, one game per studio. Full exclusion list in the sources link.

Games in this video: Gravity Ghost · SHENZHEN SOLITAIRE · Blackwell Epiphany · Supipara - Chapter 1 · Escape Goat 2 · Marvin's Mittens · Copy Kitty · Paint it Back · Bullet Heaven 2 · Quell · Tadpole Treble · Voidspire Tactics · The Lands of Dream · The Journey Down: Chapter Two · Home Sheep Home: Farmageddon Party Edition

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
- [ ] Every claim traceable to facts.json / traits.json / data.json (see sources.md)
- [ ] At least one genuine surprise the narrator reacts to (timing theory was wrong)
- [ ] Structure differs from previous uploads (n/a: first upload)
- [ ] No static frame > 6 s
- [ ] Thumbnail promise paid off (red dot = #1, revealed at the end)
- [ ] A person watched the final cut at 1.5x
