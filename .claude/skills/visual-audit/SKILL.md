---
name: visual-audit
description: Audit a rendered episode frame by frame (contact sheets, scene hold times, loudness, true peak, silences, A/V length) and its thumbnails. Use after every local or CI render, before sending a preview or uploading.
---

# Visual audit

1. `python3 pipeline/qa/audit_video.py <film.mp4> episodes/<ep> <scratch dir>`
   - It checks automatically:
     - film length matches the spec;
     - no scene holds over 12.5 s (charts get 14 s);
     - loudness −15 ±1 LUFS and true peak ≤ −1 dBFS;
     - no silence of 1.2 s or more.
   - It writes `sheet_N.png`, one frame every 3 s with timestamps.
2. **Open every sheet with the Read tool** and look for:
   - cut-off, wrapped or overlapping text (long titles wrapped into the chart in ep001);
   - multi-word `*highlight*` spans rendered in the accent colour (they once stayed white);
   - numbers on the last frame of each scene showing their final value (count-ups finish within about 1.7 s);
   - chart artefacts (low-count games once drew curved streaks: fixed with a 30-review floor plus display jitter);
   - #1's art or name appearing before the reveal;
   - captions or fine print that contradict the narration, or labels that never render (LaunchCollision shows
     no titles);
   - any stretch where one picture holds and nothing moves.
3. To check one changed scene without re-rendering everything:
   ```
   python3 -c "import json;s=json.load(open('video/src/episodes/<ep>.json'));json.dump({'spec':s},open('/tmp/p.json','w'))"
   cd video && npx remotion still src/index.ts Episode /tmp/f.png --props=/tmp/p.json --frame=<sceneFrom*30+60> --scale=0.5
   ```
4. Thumbnails: `python3 pipeline/render_thumbnails.py episodes/<ep>`. Put the three side by side
   (`ffmpeg ... hstack=3`) and check: legible at small size, no #1 art, the numbers match facts.json.
5. Fix at the source (script, data, or scene component), re-render or re-still, re-audit, then commit and push.

Headless Chromium can't reach Google Fonts or remote images: fonts are bundled, and game art must exist in
`video/public/games/` (`pipeline/fetch_art.py` checks the files really are images).
