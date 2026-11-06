# data-driven: faceless video-game data-story channel

Goal: a daily, fully automated YouTube channel. Format: "I built a model to find X", where a dataset settles an argument
players already have. The same formula repeats every episode: first person, a superlative, a big exact number, a reveal
at the end, no filler, 8+ minutes. Research behind every choice is in `research/`. Read `packaging-playbook.md`,
`human-feel-guide.md` and `copyright-risk.md` before writing a new episode. `idea-backlog.md` is the queue.

## Owner decisions (don't revisit without being asked)
- Voice: Gemini TTS **Achird**, structured AUDIO PROFILE / DIRECTOR'S NOTES / TRANSCRIPT prompt (`pipeline/voice_gemini.py`).
  Free tier only (10 requests/day per model, resets midnight Pacific). **No fallback voice or model.** Never enable billing.
- Rendering happens on GitHub Actions (`.github/workflows/render.yml`), manual dispatch only, 12 shards, like blocky-stories.
- Thumbnails never spoil the #1 answer (no #1 game art; A "ROBBED." style was the owner's pick).
- Secrets live only in GitHub repo secrets (`GEMINI_API_KEY`; later `YT_CLIENT_ID/SECRET/REFRESH_TOKEN`), never in chat or files.
- Don't bypass YouTube bot checks; ask the owner to run yt-dlp locally if transcripts are needed.

## Pipeline (episode 001 is the worked example)
| step | code | output |
|---|---|---|
| fetch catalog/store/histograms | `pipeline/fetch_*.py` (resumable; store API ~5/min) | `data/raw/` (gitignored; snapshot in `data/snapshots/`) |
| model | `pipeline/underrated_knn.py` (KNN "games like it" median) | `data/derived/*.csv`, `model_info.json` |
| rules + exclusions | `pipeline/finalists.py episodes/<ep>/exclusions.json` + `release_history.json` | `finalists.csv`, `finalists_ok.csv` |
| robustness | `pipeline/robustness.py` (7 settings, consensus = geometric mean) | `episodes/<ep>/robustness.json` |
| facts | `pipeline/ep001_facts.py`: **every number the video states**, computed in one place | `episodes/<ep>/facts.json` |
| scene data | `pipeline/ep001_data.py`: charts and cards **generated from facts**, never hand-typed | `episodes/<ep>/data.json` |
| script | `episodes/<ep>/script.md` (`@chapter`, `@scene type @ref:key {json}`, narration lines) | |
| build | `pipeline/build_episode.py episodes/<ep>`: lint, voice, timed spec, chapters | `video/src/episodes/<ep>.json` |
| render | dispatch `render` workflow with `episode=<ep>` on the working branch | artifact `film-<ep>` (90 days) |

For a new episode, copy `ep001_facts.py` / `ep001_data.py` to `epNNN_*.py` and keep the same contract: the script may
only state numbers that exist in facts.json, and data.json is generated from facts.json.

## Skills (use them, they encode what went wrong before)
- `new-episode`: idea to finished upload package, in order.
- `fact-check-loop`: independent reviewer rounds until two clean rounds. **Mandatory before any render with the real voice.**
- `release-history-check`: the Steam-first rule; how to verify and record a game's first release.
- `visual-audit`: contact sheets, scene lengths, audio levels, thumbnails.
- `voice-render-run`: dispatching the CI render under the daily TTS quota, and verifying the film.

## QA tools
- `pipeline/script_lint.py`: AI-writing tells (also runs inside build_episode).
- `pipeline/qa/claims_sheet.py episodes/<ep>`: every checkable claim, per scene (input for the fact-check loop).
- `pipeline/qa/test_voice_guards.py episodes/<ep>`: simulates the narration guards on the real chunks; run after
  script edits (chunk count = daily requests) or guard edits.
- `pipeline/qa/audit_video.py <film.mp4> episodes/<ep> [out]`: automatic checks plus contact sheets to inspect.

## Git
Work on the session's feature branch, commit and push often (containers are ephemeral). `main` exists; merge only when asked.
