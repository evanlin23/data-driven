import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Fonts are bundled in public/fonts (the render browser can't fetch Google Fonts through the proxy,
// and bundling keeps renders deterministic). All OFL-1.1 (free for commercial video).
const FONTS: [string, string, string][] = [
  ['Archivo Black', 'ArchivoBlack-400.woff2', '400'],
  ['Inter', 'Inter-400.woff2', '100 900'],
  ['Permanent Marker', 'PermanentMarker-400.woff2', '400'],
  ['DM Serif Display', 'DMSerifDisplay-400.woff2', '400'],
  ['IBM Plex Sans', 'IBMPlexSans-400.woff2', '100 600'],
  ['IBM Plex Sans', 'IBMPlexSans-700.woff2', '700 900'],
  ['Caveat', 'Caveat-700.woff2', '400 900'],
  ['VT323', 'VT323-400.woff2', '400 900'],
  ['JetBrains Mono', 'JetBrainsMono-400.woff2', '100 600'],
  ['JetBrains Mono', 'JetBrainsMono-800.woff2', '700 900'],
  ['Bungee', 'Bungee-400.woff2', '400 900'],
  ['Space Grotesk', 'SpaceGrotesk-400.woff2', '100 600'],
  ['Space Grotesk', 'SpaceGrotesk-700.woff2', '700 900'],
  ['Space Grotesk Display', 'SpaceGrotesk-700.woff2', '400 900'],
  ['Anton', 'Anton-400.woff2', '400 900'],
  ['Oswald', 'Oswald-500.woff2', '100 900'],
  ['Fraunces', 'Fraunces-900.woff2', '400 900'],
];
for (const [family, file, weight] of FONTS) loadFont({family, url: staticFile(`fonts/${file}`), weight});

export type Palette = {bg: string; panel: string; grid: string; muted: string; text: string; sub: string;
  accent: string; gold: string; good: string; blue: string};
export type Texture = 'none' | 'grain' | 'paper' | 'scanlines' | 'halftone' | 'graph' | 'stripes';
export type Transition = 'fade' | 'slide';
export type Style = {label: string; palette: Palette; display: string; body: string; hand: string; texture: Texture;
  transition?: Transition};

/** Channel looks. "accent" is reserved for THE answer / the highlighted dot; "gold" = the model / expected. */
export const STYLES: Record<string, Style> = {
  midnight: {label: 'Midnight (current)', display: 'Archivo Black', body: 'Inter', hand: 'Permanent Marker', texture: 'none',
    palette: {bg: '#0c0e13', panel: '#151922', grid: '#232838', muted: '#5d6478', text: '#eef0f5', sub: '#a7adbd',
      accent: '#ff3d3d', gold: '#ffc642', good: '#3ddc84', blue: '#4c8dff'}},
  editorial: {label: 'Editorial (newspaper)', display: 'DM Serif Display', body: 'IBM Plex Sans', hand: 'Caveat', texture: 'paper',
    palette: {bg: '#f3eee4', panel: '#e9e2d4', grid: '#d8cfbd', muted: '#9b927f', text: '#16140f', sub: '#5b5547',
      accent: '#d1262a', gold: '#b07800', good: '#1f7a45', blue: '#1f56b3'}},
  terminal: {label: 'Terminal (retro CRT)', display: 'VT323', body: 'JetBrains Mono', hand: 'VT323', texture: 'scanlines',
    palette: {bg: '#040904', panel: '#0a160c', grid: '#123019', muted: '#2f6e3c', text: '#c9ffd2', sub: '#72d58b',
      accent: '#ff5252', gold: '#ffb000', good: '#39ff6a', blue: '#4fd6ff'}},
  arcade: {label: 'Arcade (neon pop)', display: 'Bungee', body: 'Space Grotesk', hand: 'Bungee', texture: 'halftone',
    palette: {bg: '#170a36', panel: '#24124f', grid: '#34206f', muted: '#7a69b3', text: '#ffffff', sub: '#c8b8ff',
      accent: '#ff2e88', gold: '#ffd400', good: '#00e5a0', blue: '#29b6ff'}},
  swiss: {label: 'Swiss (clean light)', display: 'Space Grotesk Display', body: 'Space Grotesk', hand: 'Space Grotesk Display', texture: 'none',
    palette: {bg: '#fafafa', panel: '#efefef', grid: '#e2e2e2', muted: '#a3a3a3', text: '#111111', sub: '#575757',
      accent: '#ff3b00', gold: '#2952ff', good: '#0a8f4f', blue: '#2952ff'}},
  broadcast: {label: 'Broadcast (sports-TV)', display: 'Anton', body: 'Oswald', hand: 'Anton', texture: 'stripes',
    palette: {bg: '#111214', panel: '#1d1f23', grid: '#2b2e34', muted: '#6d717b', text: '#ffffff', sub: '#b9bcc4',
      accent: '#ff3131', gold: '#ffd60a', good: '#2ee59d', blue: '#3aa0ff'}},
  blueprint: {label: 'Blueprint (engineering drawing)', display: 'Fraunces', body: 'JetBrains Mono', hand: 'Caveat', texture: 'graph',
    transition: 'slide',
    // cyanotype sheet: chalk-white linework, red-pencil answer, warm chalk-yellow for the model
    palette: {bg: '#123c70', panel: '#184886', grid: '#3a6aa6', muted: '#86a8d4', text: '#f3f7ff', sub: '#c2d4ee',
      accent: '#ff5b3d', gold: '#ffd76e', good: '#9bf5c8', blue: '#bfe2ff'}},
};

// Live bindings: scenes import these; setStyle() swaps them before a composition renders.
export const C: Palette = {...STYLES.midnight.palette};
export let display = STYLES.midnight.display;
export let body = STYLES.midnight.body;
export let hand = STYLES.midnight.hand;
export let texture: Texture = 'none';
export let transition: Transition = 'fade';

export const setStyle = (name?: string) => {
  const s = STYLES[name ?? 'midnight'] ?? STYLES.midnight;
  Object.assign(C, s.palette);
  display = s.display; body = s.body; hand = s.hand; texture = s.texture; transition = s.transition ?? 'fade';
};

export const W = 1920;
export const H = 1080;
export const FPS = 30;
