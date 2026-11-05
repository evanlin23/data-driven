import {Easing, interpolate, spring} from 'remotion';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** 0→1 ease between two frames */
export const ease = (f: number, from: number, to: number) =>
  interpolate(f, [from, to], [0, 1], {...clamp, easing: Easing.bezier(0.22, 1, 0.36, 1)});

export const pop = (f: number, fps: number, delay = 0) =>
  spring({frame: f - delay, fps, config: {damping: 14, stiffness: 160, mass: 0.6}});

/** Format numbers for screen: 1914 -> "1,914", 0.981 -> "98%" */
export type NumKind = 'int' | 'pct' | 'compact' | 'x1' | 'usd';
export const fmt = (n: number, kind: NumKind = 'int') => {
  if (kind === 'pct') return `${Math.round(n * 100)}%`;
  if (kind === 'x1') return `${n.toFixed(1)}x`;
  if (kind === 'usd') return '$' + n.toFixed(2);
  if (kind === 'compact') {
    if (n >= 1e6) return `${(n / 1e6).toFixed(n >= 1e7 ? 0 : 1)}M`;
    if (n >= 1e3) return `${(n / 1e3).toFixed(n >= 1e4 ? 0 : 1)}K`;
    return `${Math.round(n)}`;
  }
  return Math.round(n).toLocaleString('en-US');
};
