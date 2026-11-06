// Render the same representative moments of an episode in every channel style (theme.ts STYLES), one bundle.
// Usage: node style-gallery.mjs src/episodes/<slug>.json ../episodes/<slug>/thumbnails/A_dot.json out/styles [style ...]
// Writes out/styles/<style>/<nn>_<type>.png (960x540) and thumb.png; compose sheets with ffmpeg afterwards.
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'fs';
import path from 'path';

const [specPath, thumbPath, outDir, ...only] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const thumb = JSON.parse(fs.readFileSync(thumbPath, 'utf8'));
const local = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const browserExecutable = fs.existsSync(local) ? local : undefined;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const styles = only.length ? only : ['midnight', 'editorial', 'terminal', 'arcade', 'swiss', 'broadcast', 'blueprint'];

// one frame per scene type that defines the look, ~70% into the scene so entry animations have finished
const want = ['scatter', 'bigNumber', 'leaderboard', 'gapBars', 'gameCard', 'launchCollision', 'compareBars', 'textBeat', 'lineChart'];
const picks = [];
for (const t of want) {
  const cands = spec.scenes.map((s, i) => ({s, i})).filter(({s}) => s.type === t);
  if (!cands.length) continue;
  const {s, i} = t === 'scatter' ? cands[cands.length - 1] : (cands[Math.floor(cands.length * 0.75)] ?? cands[0]);  // later scenes are richer; last scatter has the red dot
  picks.push({i, t, f: Math.round((s.from + s.dur * 0.7) * spec.fps)});
}
for (const style of styles) {
  const dir = path.join(outDir, style); fs.mkdirSync(dir, {recursive: true});
  const inputProps = {spec, style};
  const composition = await selectComposition({serveUrl, id: 'Episode', inputProps, browserExecutable});
  for (const [k, p] of picks.entries()) {
    await renderStill({composition, serveUrl, inputProps, browserExecutable, chromiumOptions: {gl: 'angle'},
      frame: p.f, output: path.join(dir, `${k}_${p.t}.png`), scale: 0.5});
  }
  const tprops = {...thumb, style};
  const tc = await selectComposition({serveUrl, id: 'Thumbnail', inputProps: tprops, browserExecutable});
  await renderStill({composition: tc, serveUrl, inputProps: tprops, browserExecutable, output: path.join(dir, 'thumb.png'), scale: 0.75});
  console.log(`${style}: ${picks.length} frames + thumbnail`);
}
