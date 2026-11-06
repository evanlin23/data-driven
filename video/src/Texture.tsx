import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, Texture} from './theme';

/** Full-frame surface texture drawn over every scene (static, so it never flickers or costs much to render). */
export const TextureOverlay: React.FC<{kind: Texture; offsetX?: number}> = ({kind, offsetX = 0}) => {
  if (kind === 'none') return null;
  const noise = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.55 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`;
  const base: React.CSSProperties = {pointerEvents: 'none'};
  switch (kind) {
    case 'grain':
      return <AbsoluteFill style={{...base, backgroundImage: noise, opacity: 0.18, mixBlendMode: 'overlay'}} />;
    case 'paper':
      return <AbsoluteFill style={{...base, backgroundImage: noise, opacity: 0.35, mixBlendMode: 'multiply', backgroundPosition: `${offsetX}px 0`}} />;
    case 'scanlines':
      return (
        <>
          <AbsoluteFill style={{...base, backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.35) 0 2px, transparent 2px 5px)'}} />
          <AbsoluteFill style={{...base, background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.65) 100%)'}} />
        </>
      );
    case 'halftone':
      return <AbsoluteFill style={{...base, backgroundImage: `radial-gradient(${C.grid} 2px, transparent 2.5px)`, backgroundSize: '22px 22px', opacity: 0.55, mixBlendMode: 'screen'}} />;
    case 'graph':
      return (
        <AbsoluteFill style={{...base, opacity: 0.5, mixBlendMode: 'screen',
          backgroundImage: `linear-gradient(${C.grid} 1px, transparent 1px), linear-gradient(90deg, ${C.grid} 1px, transparent 1px),` +
            `linear-gradient(${C.grid} 2px, transparent 2px), linear-gradient(90deg, ${C.grid} 2px, transparent 2px)`,
          backgroundSize: '24px 24px, 24px 24px, 120px 120px, 120px 120px', backgroundPosition: `${offsetX}px 0`}} />
      );
    case 'stripes':
      return <AbsoluteFill style={{...base, backgroundImage: 'repeating-linear-gradient(135deg, rgba(255,255,255,0.025) 0 18px, transparent 18px 36px)'}} />;
  }
  return null;
};
