import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display, hand} from '../theme';
import {ease, fmt} from '../anim';

export type GapBarsProps = {
  title: string;
  image?: string;
  expected: number;
  actual: number;
  timesShort: number;
  liked?: number; // 0-1
};

/** Expected vs actual reviews as two bars (linear), then the "times short" stamp. One per countdown entry. */
export const GapBars: React.FC<GapBarsProps> = ({title, image, expected, actual, timesShort, liked}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const L = 380, maxW = 1200;
  const te = ease(f, 6, 6 + 1.2 * fps), ta = ease(f, 0.9 * fps, 0.9 * fps + 0.8 * fps), tx = ease(f, 2.0 * fps, 2.0 * fps + 12);
  const bar = (label: string, n: number, t: number, color: string, y: number) => (
    <div style={{position: 'absolute', left: 140, top: y, display: 'flex', alignItems: 'center'}}>
      <div style={{width: L - 140, fontFamily: body, fontWeight: 800, fontSize: 40, color: C.sub}}>{label}</div>
      <div style={{width: Math.max(8, (n / expected) * maxW * t), height: 96, background: color, borderRadius: 10}} />
      <div style={{fontFamily: display, fontSize: 64, color, marginLeft: 26, opacity: t}}>{fmt(n * t)}</div>
    </div>
  );
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <div style={{position: 'absolute', top: 70, left: 140, display: 'flex', alignItems: 'center', gap: 30}}>
        {image && <Img src={staticFile(image)} style={{height: 110, borderRadius: 10}} />}
        <div>
          <div style={{fontFamily: display, fontSize: 64, color: C.text}}>{title}</div>
          {liked !== undefined && <div style={{fontFamily: body, fontSize: 38, color: C.good}}>{Math.round(liked * 100)}% positive reviews</div>}
        </div>
      </div>
      {bar('expected', expected, te, C.gold, 360)}
      {bar('actual', actual, ta, C.accent, 520)}
      <div style={{position: 'absolute', left: 140, top: 740, fontFamily: hand, fontSize: 96, color: C.accent, opacity: tx,
        transform: `rotate(-3deg) scale(${0.8 + 0.2 * tx})`, transformOrigin: 'left center'}}>
        {timesShort.toFixed(1)}x short
      </div>
    </AbsoluteFill>
  );
};
