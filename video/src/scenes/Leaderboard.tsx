import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display} from '../theme';
import {ease, pop} from '../anim';

export type LeaderboardProps = {
  title: string;
  rows: {rank: number; title: string; image?: string; value: string; hidden?: boolean}[];
  /** rank currently being revealed (gets the accent); rows below it are already known */
  focusRank?: number;
};

/** Running countdown board. Hidden rows show "???" to keep the loop open. */
export const Leaderboard: React.FC<LeaderboardProps> = ({title, rows, focusRank}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: C.bg, padding: '60px 140px'}}>
      <div style={{fontFamily: display, fontSize: 60, color: C.text, marginBottom: 30}}>{title}</div>
      {rows.map((r, i) => {
        const s = pop(f, fps, i * 3);
        const focus = r.rank === focusRank;
        return (
          <div key={r.rank} style={{display: 'flex', alignItems: 'center', gap: 28, height: 82, marginBottom: 6,
            background: focus ? C.panel : 'transparent', borderLeft: `8px solid ${focus ? C.accent : 'transparent'}`,
            paddingLeft: 20, opacity: s, transform: `translateY(${(1 - s) * 20}px)`}}>
            <div style={{fontFamily: display, fontSize: 44, width: 70, color: focus ? C.accent : C.muted}}>{r.rank}</div>
            {r.image && !r.hidden ? <Img src={staticFile(r.image)} style={{height: 64, borderRadius: 6}} /> : <div style={{width: 137, height: 64, background: C.grid, borderRadius: 6}} />}
            <div style={{fontFamily: body, fontWeight: 800, fontSize: 40, color: r.hidden ? C.muted : C.text, flex: 1}}>{r.hidden ? '???' : r.title}</div>
            <div style={{fontFamily: display, fontSize: 40, color: focus ? C.gold : C.sub, opacity: r.hidden ? 0 : ease(f, 10 + i * 3, 25 + i * 3)}}>{r.value}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
