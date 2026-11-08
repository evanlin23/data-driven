# Handoff: data-driven channel (as of 2026-11-08 04:05 UTC)

You're picking up a faceless, automated YouTube channel about video games: "I built a model to find X" data stories,
narrated by a Gemini TTS voice, animated in Remotion and rendered on GitHub Actions. Episode 1 is nearly ready to
upload. The production kit is built and documented. Episode 2 has not started.

## 0. Read first (in this order)
1. `CLAUDE.md`: owner decisions (don't revisit them), the pipeline map, where everything lives.
2. `docs/KIT.md`: the reusable parts and the rules they enforce.
3. `.claude/skills/*/SKILL.md`: `new-episode`, `fact-check-loop`, `release-history-check`, `visual-audit`,
   `voice-render-run`. Follow these for any episode work; they encode the mistakes already made.
4. `research/`: why the channel looks the way it does (`packaging-playbook.md`, `human-feel-guide.md`,
   `copyright-risk.md`, `idea-backlog.md`).

## 1. Repo, branch, access
- Repo `evanlin23/data-driven` (public). Work branch: **`claude/awesome-pasteur-y6c7lv`**. Everything is committed and
  pushed there (HEAD `46ed2b0` plus this file). `main` is 34 commits behind; **merge only when the owner asks.**
- If you work on your own branch, branch from `claude/awesome-pasteur-y6c7lv`, not from `main`.
- Renders: `.github/workflows/render.yml`, **manual dispatch only** (`episode=<folder>`, ref = your branch). Only the
  owner's GitHub account can trigger it, so you dispatch through the owner's GitHub connection.
- Secrets live only in GitHub repo secrets: `GEMINI_API_KEY` (set), `MUSIC_URL` (not set yet), later
  `YT_CLIENT_ID/SECRET/REFRESH_TOKEN`. Never put a secret in chat, a file or a commit.

## 2. Coordination rule: the voice quota is shared
Gemini TTS free tier: **10 requests per day per model**, reset at midnight Pacific (08:00 UTC in winter). Every render
uses the same `GEMINI_API_KEY`, so two workers share one daily quota. Before any render that needs new narration,
check with the owner that nobody else is voicing that day. Renders that only reuse cached narration cost **0
requests**: the pace, scene splits, style, sfx and music can all change freely, but narration *words* can't.
Each narration chunk (about 250 words) is one request. `pipeline/qa/test_voice_guards.py episodes/<ep>` prints the
chunk count; it's 7 for episode 1. **Never enable billing or add a fallback voice or model** (owner's rule).

## 3. Episode 1 status (`episodes/001-most-underrated/`)
"I Built a Model to Find the Most Underrated Game on Steam". #1 is Gravity Ghost.
- **Script:** final. It went through 9 independent fact-check rounds; the last 2 were clean. Don't change narration
  words without running the `fact-check-loop` skill again and accepting a re-voice.
- **Voice:** Achird, voiced 2026-11-07; all 7 chunks passed the guards first take. The cached raw takes are in the
  Actions cache (`tts-001-most-underrated-*`).
- **Look:** `look.json` = Blueprint style + sound design (owner approved). The scene layouts were reworked
  2026-11-07 (BigNumber, TextBeat, GapBars, CompareBars).
- **Last delivered preview:** run 42357995853 (Achird, Blueprint, synthesized sfx, 9:32, voice at ~159 wpm).
- **In flight:** run **42445296598** (started 04:04 UTC). It has CC0 sample sound effects, the voice evened out to
  172 wpm (owner said it was too slow) and two extra scene splits; expect about 8:50. **Your first task:** when it
  finishes, follow `voice-render-run`:
  1. Download the `film-001-most-underrated` artifact and the `voice-001-most-underrated` artifact.
  2. Run `python3 pipeline/qa/audit_video.py <film> episodes/001-most-underrated <out>` against the **CI spec** from
     the voice artifact (copy it over `video/src/episodes/001-most-underrated.json` temporarily, then
     `git checkout` it back).
  3. Look at every contact sheet.
  4. Transcribe the narration. If the base model flags a line, re-check it with `small.en`: base.en dropped 12 words
     of a correct line last time.
  5. Send the owner a 720p preview.

### Open items for episode 1, in priority order
1. **Music:** waiting on the owner. They'll pick a YouTube Audio Library track ("Attribution not required"), host it
   privately and set the `MUSIC_URL` secret. Then add `"music": "bed"` to `look.json` and re-render (0 quota).
   The pipeline is `pipeline/kit/music.py`: −20 dB under speech, ducked a further 8 dB while speaking, with fades.
   Log the track name and licence in `look.json`. Never use "royalty-free" tracks from random sites
   (`research/copyright-risk.md` section 5).
2. **Long holds:** at Achird pace, about 12 scenes hold 12.6–17 s (target ≤ 12.5 s; charts ≤ 14 s). The 172 wpm
   pace shortens them. What's left is mostly single long narration lines, which can only be split by re-voicing
   their chunks (costs quota). Show the owner, and only do this if they ask.
3. **One-frame overlap at some cuts** (seen at 8:00 in run 42357995853): the outgoing and incoming scenes both draw
   for one frame. Probably `Math.round(from*fps)` + `Math.round(dur*fps)` overlap in `video/src/Episode.tsx`.
   Compute each Sequence's end from the next scene's start instead.
4. **Pronunciation:** nobody has listened yet. Check "Cootalot", "Wadjet Eye" and "co-op" by ear.
5. **Packaging:** `metadata.md` alt title 2 ("I Scored 51,897 Steam Games…") is the number-first pattern another
   channel measured at a median of 58 views. Suggest replacing it. Thumbnails: `thumbnails/*.json`, rendered in the
   episode's style.
6. **Upload:** no upload workflow yet. It needs the owner's YouTube OAuth secrets. Until then, the owner uploads the
   film artifact, the thumbnail, `metadata.md` and `chapters.txt` by hand. The research says to keep a human review
   before each publish.

## 4. Next: episode 2 ("Most Overrated", the end card promises it)
Not started. Use the `new-episode` skill.
- Store-details fetch for ep 2 candidates: `data/derived/ep002_store_ids.txt` and `fetch_queue.txt`; about
  1,833 of 2,077 were done when the last fetch died on a container restart. The fetchers resume
  (`pipeline/fetch_store_details.py`, about 5 requests/min).
- Copy `pipeline/ep001_facts.py` and `ep001_data.py` to `ep002_*`. The script may only state numbers that exist in
  `facts.json`.
- Design lessons for ep 2: fewer centered text cards (ep 1 has about 20), and give layouts real visuals rather than
  text on an empty frame. Style is per episode via `look.json`; preview looks with `video/style-gallery.mjs`.

## 5. Gotchas that already cost time
- **Rendering:**
  - Headless Chromium can't fetch Google Fonts or remote images: fonts are bundled in `video/public/fonts`, and game
    art must be in `video/public/games` (`pipeline/fetch_art.py` checks the files really are images).
  - Use `--gl=angle` locally; it's 3× faster than swangle.
- **Audio:**
  - Gemini audio runs near full scale and once clipped. Narration is written as float with 6 dB headroom.
  - `pipeline/kit/audio.py` mux: compressor → gain → 4× oversampled limiter, then the *decoded* file is measured. A
    plain limiter or loudnorm couldn't reach −15 LUFS on this voice. The tolerance is ±1 LU.
- **Data and claims:**
  - Comparison groups must obey the episode's own rules (re-releases, one per studio, a real shortfall threshold).
  - Ratio words must be literally true ("half" means ≤ 0.5×).
  - Round from unrounded values: 6.55 double-rounded to 6.5.
  - Reviewers' suggested claims were false 3 times; verify everything against the data before using it.
- **Narration guards:** a chunk is rejected when it's cut off, skips or repeats a line, adds words, or reads under
  125 wpm. Rejected chunks are re-voiced within the day's spare requests. Only passing chunks are cached.
- **CI:**
  - `kit-ci.yml` runs on every pipeline/video change (gate self-tests, guard simulation, typecheck, every scene in
    every style). Keep it green.
  - Installs are time-boxed, and JS deps are pinned exactly.
- **Sandbox:** the container is ephemeral. Commit and push often; `data/raw` is gitignored, and a snapshot is in
  `data/snapshots/`.

## 6. Owner preferences
- Wants daily posting, with no filler, 8+ minutes, high effort, and nothing that "looks AI".
- Picked the Achird voice, the Blueprint look and the "ROBBED." thumbnail style.
- Doesn't want to spend money (free tiers only).
- Likes being told what's running and when results arrive; send previews as files.
- Said earlier "don't ask me questions, just do it". Still ask for anything that spends voice quota or publishes.
