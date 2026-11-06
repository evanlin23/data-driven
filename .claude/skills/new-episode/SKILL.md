---
name: new-episode
description: Make a new episode of the video-game data channel end to end, from picking an idea through data, model, facts, script, QA and render to the upload package. Use when starting episode NNN or turning an idea from research/idea-backlog.md into a video.
---

# New episode, start to finish

Worked example: `episodes/001-most-underrated/`. Copy its shape. Each step lists what bit us before.

## 1. Pick and frame (research/)
- Take the next idea from `research/idea-backlog.md`. The title formula is in `packaging-playbook.md`: first person, a
  superlative, a big exact number, 60 characters or fewer, three variants for Test & Compare.
- Decide the **one question** the model answers and the **reveal** saved for the end (the cold open teases it).
- Check `copyright-risk.md`: game header art is OK for commentary and identification; no trailers or gameplay footage.

## 2. Data
- Fetchers in `pipeline/fetch_*.py` resume where they stopped. The Steam store API allows about 5 requests/min, so
  queue only the apps you need and run detached (containers restart). Snapshot the raw data into `data/snapshots/`
  (data/raw is gitignored).
- Fetch store details for **every** candidate the comparison groups could draw on, not just the top ones. Missing
  details silently shrink groups (ep001's "top 100" filled up with games that beat expectations).

## 3. Model and rules
- Model code is reusable (`underrated_knn.py`). Write the rules down in `finalists.py` and the episode's
  `exclusions.json` (one reason per entry).
- Apply the Steam-first rule to every finalist with the `release-history-check` skill. It removed 34 of 51 candidates
  in ep001; it matters more than the model.
- Run `robustness.py` and report the stable core, not the fragile order.

## 4. Facts, then data
- Copy `ep001_facts.py` to `epNNN_facts.py`. **Every number the video says or shows** gets computed here, into
  `facts.json`. Round from unrounded values.
- Copy `ep001_data.py` to `epNNN_data.py`. Charts, cards and boards are built from facts.json, never hand-typed.
- Comparison groups follow the episode's own rules (see the fact-check-loop lessons).

## 5. Script (`episodes/<ep>/script.md`)
- Follow `research/human-feel-guide.md`: narrator presence ("I"), a genuine surprise, specific details, no AI tells.
- Format: `@chapter Title`, `@scene <type> @ref:<data key> {inline json}`, then narration lines (one spoken line each).
  `[pause 0.5]` is allowed. Scene types live in `video/src/scenes/`.
- **One picture should never hold more than about 12 s.** When a scene has 2+ sentences, give the second one its own
  beat (textBeat/bigNumber). Achird reads about 15% slower than the placeholder voice, so scenes grow.
- Spell out years and dates. Quote titles that read like words. Write abbreviations as words.
- `python3 pipeline/script_lint.py episodes/<ep>/script.md` must PASS.
- Write `sources.md` (generated sections from facts.json) and `metadata.md`: titles, description with chapters
  placeholder, games listed A-Z so #1 isn't spoiled, tags, pinned comment, thumbnail plan.

## 6. QA before spending voice quota
1. `fact-check-loop` skill until two clean rounds.
2. `python3 pipeline/qa/test_voice_guards.py episodes/<ep>`: must pass. The chunk count is the number of Gemini
   requests; keep it ≤ 7 so re-takes fit in the 10/day quota.
3. Local placeholder render: `env -u GEMINI_API_KEY python3 pipeline/build_episode.py episodes/<ep> --render`
   (Kokoro voice, about 40 min), then the `visual-audit` skill. Fix, then re-run what changed.
4. Thumbnails: `python3 pipeline/render_thumbnails.py episodes/<ep>`, then look at them (no #1 art, text legible small).

## 7. Real render
`voice-render-run` skill (CI dispatch after the quota reset, then verify).

## 8. Upload (not built yet)
Needs a YouTube upload workflow and the owner's OAuth secrets (`YT_CLIENT_ID`, `YT_CLIENT_SECRET`,
`YT_REFRESH_TOKEN`). Until then, hand the owner the `film-<ep>` artifact, thumbnails, `metadata.md` and `chapters.txt`.
