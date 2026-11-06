import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display, hand} from '../theme';
import {ease, fmt, pop} from '../anim';

export type LaunchCollisionProps = {
  dateLabel: string;          // e.g. "January 2015"
  small: {title: string; image: string; day: number; reviews: number};
  big: {title: string; image: string; day: number; reviews: number}[];
  daysInWindow?: number;      // width of the calendar strip, default 21
  caption?: string;
};

const BASE = 860, TOP = 330, CARD_W = 230, CARD_H = Math.round(230 * 215 / 460);

/** A calendar strip: our game launches, and a mega-hit lands next to it. Bar height ~ log(lifetime reviews). */
export const LaunchCollision: React.FC<LaunchCollisionProps> = ({dateLabel, small, big, daysInWindow = 21, caption}) => {
  const f = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const L = 160, R = width - 160;
  const x = (d: number) => L + ((d - 1) / (daysInWindow - 1)) * (R - L);
  const lo = 2, hi = 6.3; // log10 range: 100 .. 2M reviews
  const barH = (n: number) => ((Math.min(Math.max(Math.log10(Math.max(n, 10)), lo), hi) - lo) / (hi - lo)) * (BASE - TOP - 20) + 20;
  // games in draw order; nudge cards apart horizontally if two launches are within a card's width
  const items = [{...small, isSmall: true}, ...big.map((b) => ({...b, isSmall: false}))].map((g) => ({...g, cx: x(g.day)}));
  const sorted = [...items].sort((a, b) => a.cx - b.cx);
  for (let i = 1; i < sorted.length; i++) {
    if (sorted[i].cx - sorted[i - 1].cx < CARD_W + 30) sorted[i].cx = sorted[i - 1].cx + CARD_W + 30;
  }
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <div style={{position: 'absolute', top: 56, left: L, fontFamily: display, fontSize: 64, color: C.text}}>{dateLabel}</div>
      <div style={{position: 'absolute', top: 140, left: L, fontFamily: body, fontSize: 32, color: C.sub}}>launch day · bar height = lifetime Steam reviews</div>
      <svg width={width} height={1080} style={{position: 'absolute'}}>
        <line x1={L} x2={R} y1={BASE} y2={BASE} stroke={C.grid} strokeWidth={4} />
        {Array.from({length: daysInWindow}, (_, d) => (
          <line key={d} x1={x(d + 1)} x2={x(d + 1)} y1={BASE} y2={BASE + (d % 7 === 0 ? 22 : 10)} stroke={C.muted} strokeWidth={2} />
        ))}
        {items.map((g, i) => {
          const s = pop(f, fps, g.isSmall ? 4 : 26 + i * 10);
          const h = barH(g.reviews) * s;
          return (
            <g key={g.title}>
              {/* thin leader from the true launch day to the (possibly nudged) bar */}
              {Math.abs(g.cx - x(g.day)) > 2 && <line x1={x(g.day)} x2={g.cx} y1={BASE} y2={BASE - 8} stroke={C.muted} strokeWidth={2} />}
              <rect x={g.cx - 14} y={BASE - h} width={28} height={h} rx={10} fill={g.isSmall ? C.accent : C.muted} />
            </g>
          );
        })}
      </svg>
      {items.map((g, i) => {
        const s = pop(f, fps, g.isSmall ? 4 : 26 + i * 10);
        const top = BASE - barH(g.reviews) * s - CARD_H - 60;
        return (
          <div key={g.title} style={{position: 'absolute', left: g.cx - CARD_W / 2, top, width: CARD_W, opacity: s,
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
            <div style={{fontFamily: display, fontSize: 40, color: g.isSmall ? C.accent : C.text}}>{fmt(g.reviews, 'compact')}</div>
            <Img src={staticFile(g.image)} style={{width: CARD_W, borderRadius: 10, border: `4px solid ${g.isSmall ? C.accent : C.panel}`}} />
          </div>
        );
      })}
      {caption && (
        <div style={{position: 'absolute', bottom: 60, left: L, fontFamily: hand, fontSize: 54, color: C.gold, opacity: ease(f, 50, 70)}}>{caption}</div>
      )}
    </AbsoluteFill>
  );
};
