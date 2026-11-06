---
name: fact-check-loop
description: Independent fact-check rounds on an episode script, on-screen text, sources and metadata until two consecutive rounds find nothing wrong. Use before every real-voice render and after any script or data change.
---

# Fact-check loop

Episode 001 needed 9 rounds. Rounds 1-3 found method flaws, 4-7 found about one wrong number each, and 8-9 were clean.
A single review pass is never enough, and the author can't see their own anchoring, so reviewers must be fresh.

## Loop
1. Generate the claim list: `python3 pipeline/qa/claims_sheet.py episodes/<ep> > /tmp/claims.md` (give it to the reviewer).
2. Spawn a **fresh** general-purpose agent with the prompt below. Don't pass earlier findings: that anchors it.
   Run it in the background, and in parallel with a render if one is needed.
3. For every issue it reports:
   - **Verify it yourself against the data before changing anything.** Reviewers were wrong several times, e.g.
     "same top four every time" and "same top two every time" were false; 340 was really 360.
   - The same applies to any new claim a reviewer *suggests*: check it in robustness.json/facts.json before using it.
   - Fix at the source: facts/data scripts, then regenerate. Never hand-edit facts.json or data.json.
4. Re-run `script_lint.py`, `claims_sheet.py` and `test_voice_guards.py` (chunk count changes with words).
5. Commit and push, then start the next round.
6. **Stop after two consecutive rounds with nothing above "nit".** Fix the nits that cost nothing.

## Reviewer prompt (fill in <ep>)
> Fact-check a YouTube video script before publication. Repo: /home/user/data-driven. Read-only: do NOT edit, commit, or
> run renders/builds. Script: episodes/<ep>/script.md (@scene lines hold on-screen text as JSON; other lines are
> narration; @ref:NAME pulls props from episodes/<ep>/data.json; video/src/scenes/*.tsx show how values render).
> Sources of truth: episodes/<ep>/facts.json, robustness.json, release_history.json, exclusions.json, sources.md,
> data.json; the pipeline/*.py that build them; data/raw/store_details/<appid>.json; data/derived/*.csv. Also
> metadata.md and thumbnails/*.json. Verify every factual claim, spoken or on screen. Check every comparative or
> superlative word literally against the numbers; spoken and on-screen figures must agree. Check the fine print
> describes comparison groups exactly as the code builds them. Flag what a sharp, skeptical commenter would call out,
> and lines a TTS narrator would misread. Don't re-raise limitations sources.md documents unless the video states
> something false about them. If you use outside knowledge, say so and rate your confidence. Report: issues with
> severity (wrong / misleading / unclear / nit), line, evidence, fix; then a verified-OK list. If nothing is above
> nit, say so in the first line.

## Lessons from episode 001 (check these first)
- **Ratio words:** "half as often" must mean ≤ 0.5×. RPGs at 0.59× broke that, and so did "past the typical miss" for a
  game at 2.6× against a 2.7× miss. Re-check every "about / almost / most / every / only / half / twice / highest" after
  each edit, because edits introduce new ones.
- **Rounding:** round from unrounded values. 6.55 stored, then rounded again, became 6.5 instead of 6.6. Spoken and
  on-screen numbers must come from the same field.
- **Raw vs adjusted:** show the real % positive that Steam shows. Shrunk/adjusted scores are model internals only.
- **Comparison groups** must obey the episode's own rules: no excluded re-releases, a real shortfall threshold, one per
  studio, same years. Say in the fine print what isn't matched (rating, year) and how many weren't hand-checked.
- **Small samples:** test differences (Fisher exact). Don't claim one at p ≈ 0.2. Say "small sample".
- **Model error:** state the typical miss for the population it was measured on. For a selected group (200+ reviews)
  the model is biased, so give the rarity instead ("fewer than 1 in 100 are this far short").
- **Robustness claims** must name the pool they were computed on ("of the sixteen games that passed every check").
- **Dates:** say "on Steam" and use Steam store dates. Commonly cited dates are often a day later; list both in sources.md.
- **Superlatives over partial data:** "highest Metacritic" failed because Steam's page lacked one game's score. Avoid
  superlatives unless every item has the field.
- **Lifetime reviews of now-free games** overstate their launch size; label them.
- **TTS:** spell out years and dates in narration. Quote titles that read like words ("a game called 'I and Me'"),
  and write "player-versus-player", not "PvP".
