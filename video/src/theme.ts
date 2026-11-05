import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Fonts are bundled in public/fonts (the render browser can't fetch Google Fonts through the proxy,
// and bundling keeps renders deterministic).
export const display = 'Archivo Black';
export const body = 'Inter';
export const hand = 'Permanent Marker';
loadFont({family: display, url: staticFile('fonts/ArchivoBlack-400.woff2'), weight: '400'});
loadFont({family: body, url: staticFile('fonts/Inter-400.woff2'), weight: '100 900'});
loadFont({family: hand, url: staticFile('fonts/PermanentMarker-400.woff2'), weight: '400'});

// One palette for the whole channel. "accent" is reserved for THE answer / the highlighted dot.
export const C = {
  bg: '#0c0e13',
  panel: '#151922',
  grid: '#232838',
  muted: '#5d6478',
  text: '#eef0f5',
  sub: '#a7adbd',
  accent: '#ff3d3d',
  gold: '#ffc642',
  good: '#3ddc84',
  blue: '#4c8dff',
};

export const W = 1920;
export const H = 1080;
export const FPS = 30;
