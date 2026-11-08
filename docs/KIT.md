# Production kit

Everything here exists so the next episode, or the next channel, starts from parts that already passed QA, rather than
from a blank Remotion project. Lessons from our own episode 1 and from the Buh Simulates kit (`evanlin23/niche`:
`docs/scene-kit.md`, `docs/LESSONS.md`) are built into the gates rather than left as advice.

## What's generic and what's channel-specific

| piece | where | generic? |
|---|---|---|
| Voice-over mux: −15 LUFS ±1, decoded peak ≤ −1 dBFS (compressor → gain → limiter at 48 kHz → measure the decoded file) | `pipeline/kit/audio.py` | yes |
| Pixel gate: blank runs, 1–2 frame flashes/dips | `pipeline/kit/gates.py` | yes |
| Kit self-tests (each gate fires on a known-bad input) | `pipeline/kit/test_kit.py` | yes |
| Synthesized sound design from the scene timeline (no licensing) | `pipeline/kit/sfx.py` | yes (event map per scene type) |
| Gemini TTS with Whisper guards: re-takes within the daily quota, word-level coverage, cut-off, repeat, pace | `pipeline/voice_gemini.py`, `pipeline/align.py` | yes |
| Guard simulation on the real chunks | `pipeline/qa/test_voice_guards.py` | yes |
| Script linter for AI-writing tells | `pipeline/script_lint.py` | yes |
| Script format, parser, build (lint → voice → timed spec → chapters) | `pipeline/script_parse.py`, `build_episode.py` | yes |
| Sharded GitHub Actions render (voice once → N draw shards → assemble) | `.github/workflows/render.yml` | yes |
| Kit CI (gates + guard sims + typecheck + every scene × every style) | `.github/workflows/kit-ci.yml` | yes |
| Video audit: length, hold times, loudness, pixel gate, contact sheets | `pipeline/qa/audit_video.py` | yes |
| Claims sheet for the fact-check loop | `pipeline/qa/claims_sheet.py` | yes (for data channels) |
| Style system: palettes, fonts, textures, transitions (+ gallery renderer) | `video/src/theme.ts`, `Texture.tsx`, `style-gallery.mjs` | yes |
| Data-story scene library: scatter, bars, cards, boards, line chart, launch collision, big number, text beat | `video/src/scenes/` | yes for data stories |
| Steam data fetchers, underrated model, release-history rule | `pipeline/fetch_*`, `underrated_knn.py`, `finalists.py` | Steam-specific |
| `epNNN_facts.py` / `epNNN_data.py` | `pipeline/` | per episode |

## Rules the kit enforces (and why)
- **Every number comes from a facts file**; charts are generated from it, never typed (ep001: hand-typed chart values
  were wrong twice).
- **Nothing ships unmeasured.** The mux measures the decoded file, the pixel gate checks every frame, the voice guards
  transcribe every chunk. The other kit's single-pass loudnorm let peaks reach +2.1 dBFS; ours overshot by 2.5 dB
  until resampling moved in front of the limiter.
- **A failing gate is fixed at the source, never waived.** If a rule is wrong, fix the rule and add a case to
  `test_kit.py`.
- **Pin and time-box everything in CI.** Exact package versions, a lockfile, and `timeout` on apt/pip/npm. In the
  other kit a caret range broke every render, and a hung apt stalled jobs for 40+ minutes.
- **Build the kit before the episode.** Fixing the same glitch by hand in several episodes is how both projects lost
  days.

## Starting a new channel from this kit
1. Copy `pipeline/kit/`, `pipeline/{voice_gemini,align,script_lint,script_parse,build_episode,assemble,render_thumbnails}.py`,
   `pipeline/qa/`, `video/` (minus `public/games`, `src/episodes`), `.github/workflows/{render,kit-ci}.yml`,
   `.claude/skills/{fact-check-loop,visual-audit,voice-render-run}`, and this file.
2. Add the channel's look to `STYLES` in `theme.ts` and preview it with `style-gallery.mjs`.
3. Write the channel's `CLAUDE.md` (owner decisions, voice, formula) and a `new-episode` skill for its format.
4. Make `kit-ci` green before episode 1.

Later, if a third channel needs it: split `pipeline/kit` (+ voice, align, lint, assemble) into a small pip package,
and `video/src/{theme,Texture,anim}.ts` + `scenes/` into an npm package. That's the other kit's recommendation too.
Until then, copying keeps each channel free to diverge.
