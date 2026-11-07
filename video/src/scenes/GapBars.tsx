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
  const maxW = 1240;
  const te = ease(f, 6, 6 + 1.2 * fps), ta = ease(f, 0.9 * fps, 0.9 * fps + 0.8 * fps), tx = ease(f, 2.0 * fps, 2.0 * fps + 12);
  const bar = (label: string, n: number, t: number, color: string) => (
    <div style={{display: 'flex', alignItems: 'center'}}>
      <div style={{width: 260, fontFamily: body, fontWeight: 800, fontSize: 44, color: C.sub}}>{label}</div>
      <div style={{width: Math.max(8, (n / expected) * maxW * t), height: 120, background: color, borderRadius: 12}} />
      <div style={{fontFamily: display, fontSize: 76, color, marginLeft: 30, opacity: t, fontVariantNumeric: 'tabular-nums'}}>{fmt(n * t)}</div>
    </div>
  );
  // one block, vertically centred: header, two bars, the "x short" stamp (no empty lower half)
  return (
    <AbsoluteFill style={{background: C.bg, padding: '0 140px', justifyContent: 'center', gap: 56}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 36}}>
        {image && <Img src={staticFile(image)} style={{height: 150, borderRadius: 12}} />}
        <div>
          <div style={{fontFamily: display, fontSize: title.length > 30 ? 60 : 76, color: C.text, lineHeight: 1.05}}>{title}</div>
          {liked !== undefined && <div style={{fontFamily: body, fontSize: 40, color: C.good, marginTop: 8}}>{Math.round(liked * 100)}% positive reviews</div>}
        </div>
      </div>
      <div style={{display: 'flex', flexDirection: 'column', gap: 34}}>
        {bar('expected', expected, te, C.gold)}
        {bar('actual', actual, ta, C.accent)}
      </div>
      <div style={{fontFamily: hand, fontSize: 112, color: C.accent, opacity: tx, marginLeft: 260,
        transform: `rotate(-3deg) scale(${0.8 + 0.2 * tx})`, transformOrigin: 'left center', lineHeight: 1}}>
        {timesShort.toFixed(1)}x short
      </div>
    </AbsoluteFill>
  );
};
