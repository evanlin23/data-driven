import {Config} from '@remotion/cli/config';
import {existsSync} from 'fs';

// In the Claude cloud container a headless Chromium is preinstalled; elsewhere (GitHub Actions, laptops)
// Remotion downloads its own chrome-headless-shell automatically.
const local = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
if (existsSync(local)) Config.setBrowserExecutable(local);
// 'angle' renders ~3x faster than 'swangle' on CPU-only machines (benchmarked: 30 s clip 50 s vs 165 s).
Config.setChromiumOpenGlRenderer('angle');
Config.setConcurrency(Number(process.env.REMOTION_CONCURRENCY) || 4);
