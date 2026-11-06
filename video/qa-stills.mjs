// QA: render the first, middle and last frame of every scene in an episode spec (one bundle, many stills).
// Usage: node qa-stills.mjs src/episodes/<slug>.json out/qa/<slug>
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'fs';
import path from 'path';

const [specPath, outDir] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
fs.mkdirSync(outDir, {recursive: true});
const local = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const browserExecutable = fs.existsSync(local) ? local : undefined;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const inputProps = {spec};
const composition = await selectComposition({serveUrl, id: 'Episode', inputProps, browserExecutable});
const jobs = [];
spec.scenes.forEach((s, i) => {
  const a = Math.round(s.from * spec.fps), n = Math.max(1, Math.round(s.dur * spec.fps));
  [['a', a + 8], ['m', a + Math.floor(n / 2)], ['z', a + n - 6]].forEach(([k, f]) => jobs.push({i, k, f, type: s.type}));
});
for (const j of jobs) {
  await renderStill({composition, serveUrl, inputProps, browserExecutable, chromiumOptions: {gl: 'angle'},
    frame: j.f, output: path.join(outDir, `s${String(j.i).padStart(2, '0')}${j.k}_${j.type}.png`), scale: 0.5});
}
console.log(`rendered ${jobs.length} stills to ${outDir}`);
