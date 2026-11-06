---
name: voice-render-run
description: Produce the final film with the Achird voice on GitHub Actions under the Gemini free-tier quota, then verify it (length, loudness, transcript vs script, pace, frames) and deliver a preview. Use when an episode has passed the fact-check loop and visual audit with the placeholder voice.
---

# Real-voice render (GitHub Actions)

## Quota rules (Gemini free tier, `gemini-3.8-flash-tts`)
- 10 requests/day per model, reset at **midnight Pacific** (08:00 UTC in winter, 07:00 UTC in summer). Requests made
  earlier the same Pacific day count against it, including voice-test runs and failed runs.
- One request per narration chunk of about 250 words. `python3 pipeline/qa/test_voice_guards.py episodes/<ep>` prints
  the chunk count. Spare = 10 − chunks, and those spare requests go on re-takes of rejected chunks.
- Chunks that pass every check are cached (`.tts-cache`, actions cache key per run and attempt), so a rerun only
  voices what's missing. Changing a line's words, the STYLE prompt, the voice or the model re-voices that chunk.
- Never enable billing and never add a fallback model or voice (owner's decision). A missing key or ffmpeg fails the
  job on purpose.

## Dispatch
- After the reset, trigger workflow `render` with input `episode=<ep>` **on the working branch**
  (`mcp__github__actions_run_trigger`, ref = the branch). `main` may be behind.
- Only the repo owner's account can trigger it (manual `workflow_dispatch`, no push trigger).
- Watch the run (`mcp__github__actions_get` / `get_job_logs`). The voice job log shows per chunk: pace, anchored lines,
  and "rejected: ..." / "re-voicing" lines.
- If the voice job fails:
  - quota: wait for the reset; the cached chunks persist;
  - "kept failing the checks": read the reason. A real repeat or cut-off means just re-run tomorrow. A false reject
    (a correct take) means fix the guard and add the case to `test_voice_guards.py`.

## Verify the film (artifact `film-<ep>`: mp4, thumbnails, metadata.md, chapters.txt)
1. Download the artifact (`gh run download <id> -n film-<ep>`, or the GitHub MCP).
2. `python3 pipeline/qa/audit_video.py dist/<ep>.mp4 episodes/<ep> <scratch>`, then inspect the sheets
   (`visual-audit` skill). Use the CI spec from the `voice-<ep>` artifact (`video/src/episodes/<ep>.json`): Achird
   timing differs from the local placeholder spec.
3. Transcribe the whole narration (faster-whisper base.en, `vad_filter=True`) and run `align.inserted_speech` and
   `novel_words` against all script lines. Nothing added, repeated or skipped.
4. Pace: spoken words ÷ minutes of narration should be about 145–160 wpm. Listen for proper names (Cootalot, Wadjet
   Eye, Voidspire), "co-op", titles in quotes, and spelled-out dates.
5. Make a 720p preview (`ffmpeg -vf scale=1280:-2 -crf 28`) and send it with a short QA summary.
