import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display} from '../theme';
import {ease, fmt, NumKind, pop} from '../anim';

export type GameCardProps = {
  rank?: number;
  title: string;
  image: string; // path under public/ (download assets first; the render browser can't fetch remote images)
  year?: number;
  stats: {label: string; value: number; kind?: NumKind; color?: 'text' | 'accent' | 'gold' | 'good'}[];
  note?: string;
};

/** "Model card" for one game: art + the numbers that put it on the list. */
export const GameCard: React.FC<GameCardProps> = ({rank, title, image, year, stats, note}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = pop(f, fps);
  return (
    <AbsoluteFill style={{background: C.bg, padding: 90, flexDirection: 'row', alignItems: 'center', gap: 80}}>
      <div style={{position: 'relative', width: 920, transform: `translateX(${(1 - s) * -80}px)`, opacity: s}}>
        <Img src={staticFile(image)} style={{width: 920, borderRadius: 18, boxShadow: '0 30px 80px rgba(0,0,0,.6)'}} />
        {rank !== undefined && (
          <div style={{position: 'absolute', top: -46, left: -46, width: 140, height: 140, borderRadius: 70, background: C.accent,
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: display, fontSize: 72, color: C.text}}>
            {rank}
          </div>
        )}
      </div>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 26}}>
        <div style={{fontFamily: display, fontSize: 76, color: C.text, lineHeight: 1.05}}>{title}</div>
        {year && <div style={{fontFamily: body, fontSize: 38, color: C.sub}}>{year}</div>}
        {stats.map((st, i) => {
          const t = ease(f, 12 + i * 10, 40 + i * 10);
          return (
            <div key={st.label} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline',
              borderBottom: `2px solid ${C.grid}`, paddingBottom: 12, opacity: t}}>
              <span style={{fontFamily: body, fontSize: 38, color: C.sub}}>{st.label}</span>
              <span style={{fontFamily: display, fontSize: 60, color: C[st.color ?? 'text']}}>{fmt(st.value * t, st.kind)}</span>
            </div>
          );
        })}
        {note && <div style={{fontFamily: body, fontSize: 34, color: C.gold, opacity: ease(f, 60, 75)}}>{note}</div>}
      </div>
    </AbsoluteFill>
  );
};
