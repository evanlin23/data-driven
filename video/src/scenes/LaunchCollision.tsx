import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display, hand} from '../theme';
import {ease, fmt, pop} from '../anim';

export type LaunchCollisionProps = {
  dateLabel: string;          // e.g. "January 2015"
  small: {title: string; image: string; day: number; reviews: number};
  big: {title: string; image: string; day: number; reviews: number}[];
  daysInWindow?: number;      // width of the calendar strip, default 31
  caption?: string;
};

/** A calendar strip: our game launches, and a mega-hit lands next to it. Card height ~ log(reviews). */
export const LaunchCollision: React.FC<LaunchCollisionProps> = ({dateLabel, small, big, daysInWindow = 31, caption}) => {
  const f = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const L = 140, R = width - 140, base = 820;
  const x = (d: number) => L + ((d - 1) / (daysInWindow - 1)) * (R - L);
  const h = (n: number) => 70 + Math.log10(Math.max(n, 10)) * 95;
  const card = (g: LaunchCollisionProps['small'], i: number, isSmall: boolean) => {
    const s = pop(f, fps, isSmall ? 6 : 30 + i * 10);
    const ht = h(g.reviews) * s;
    return (
      <div key={g.title} style={{position: 'absolute', left: x(g.day) - 120, top: base - ht, width: 240, height: ht,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', gap: 10}}>
        <Img src={staticFile(g.image)} style={{width: 240, borderRadius: 10, border: `4px solid ${isSmall ? C.accent : C.panel}`}} />
        <div style={{fontFamily: display, fontSize: 40, color: isSmall ? C.accent : C.text}}>{fmt(g.reviews, 'compact')}</div>
        <div style={{flex: 1, width: 18, background: isSmall ? C.accent : C.muted, borderRadius: 9}} />
      </div>
    );
  };
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <div style={{position: 'absolute', top: 60, left: L, fontFamily: display, fontSize: 64, color: C.text}}>{dateLabel}</div>
      <div style={{position: 'absolute', top: 140, left: L, fontFamily: body, fontSize: 34, color: C.sub}}>Steam reviews (lifetime)</div>
      <svg width={width} height={1080} style={{position: 'absolute'}}>
        <line x1={L} x2={R} y1={base} y2={base} stroke={C.grid} strokeWidth={4} />
        {Array.from({length: daysInWindow}, (_, d) => (
          <g key={d}>
            <line x1={x(d + 1)} x2={x(d + 1)} y1={base} y2={base + (d % 7 === 0 ? 26 : 12)} stroke={C.muted} strokeWidth={2} />
            {d % 7 === 0 && <text x={x(d + 1)} y={base + 64} fill={C.muted} fontSize={30} fontFamily={body} textAnchor="middle">{d + 1}</text>}
          </g>
        ))}
      </svg>
      {big.map((g, i) => card(g, i, false))}
      {card(small, 0, true)}
      {caption && (
        <div style={{position: 'absolute', bottom: 60, left: L, fontFamily: hand, fontSize: 54, color: C.gold, opacity: ease(f, 60, 80)}}>{caption}</div>
      )}
    </AbsoluteFill>
  );
};
