// Render one late frame (80% in) of every scene of the given types, in one style, for an overflow/layout check.
// Usage: node scene-check.mjs src/episodes/<slug>.json <style> <outDir> type1,type2,...
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'fs';
import path from 'path';
const [specPath, style, outDir, types] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const want = new Set((types || '').split(',').filter(Boolean));
fs.mkdirSync(outDir, {recursive: true});
const local = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const browserExecutable = fs.existsSync(local) ? local : undefined;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const inputProps = {spec, style};
const composition = await selectComposition({serveUrl, id: 'Episode', inputProps, browserExecutable});
let n = 0;
for (const [i, s] of spec.scenes.entries()) {
  if (want.size && !want.has(s.type)) continue;
  await renderStill({composition, serveUrl, inputProps, browserExecutable, chromiumOptions: browserExecutable ? {gl: 'angle'} : {},
    frame: Math.round((s.from + s.dur * 0.8) * spec.fps), output: path.join(outDir, `s${String(i).padStart(2, '0')}_${s.type}.png`), scale: 0.4});
  n++;
}
console.log(`${n} stills -> ${outDir}`);
