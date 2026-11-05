import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, body, display} from '../theme';
import {ease} from '../anim';

export type CompareBarsProps = {
  title: string;
  aLabel: string;   // e.g. "100 most underrated"
  bLabel: string;   // e.g. "random Steam games"
  rows: {label: string; a: number; b: number}[]; // fractions 0-1
  note?: string;
};

/** Paired horizontal bars: our group (accent) vs the baseline (muted). */
export const CompareBars: React.FC<CompareBarsProps> = ({title, aLabel, bLabel, rows, note}) => {
  const f = useCurrentFrame();
  const maxW = 1000;
  return (
    <AbsoluteFill style={{background: C.bg, padding: '70px 150px'}}>
      <div style={{fontFamily: display, fontSize: 60, color: C.text}}>{title}</div>
      <div style={{display: 'flex', gap: 40, margin: '22px 0 40px', fontFamily: body, fontSize: 34, color: C.sub}}>
        <span><span style={{display: 'inline-block', width: 26, height: 26, background: C.accent, borderRadius: 4, marginRight: 12}} />{aLabel}</span>
        <span><span style={{display: 'inline-block', width: 26, height: 26, background: C.muted, borderRadius: 4, marginRight: 12}} />{bLabel}</span>
      </div>
      {rows.map((r, i) => {
        const t = ease(f, 8 + i * 8, 34 + i * 8);
        return (
          <div key={r.label} style={{display: 'flex', alignItems: 'center', marginBottom: 34}}>
            <div style={{width: 360, fontFamily: body, fontWeight: 800, fontSize: 40, color: C.text}}>{r.label}</div>
            <div style={{display: 'flex', flexDirection: 'column', gap: 8}}>
              {[{v: r.a, c: C.accent}, {v: r.b, c: C.muted}].map((x, j) => (
                <div key={j} style={{display: 'flex', alignItems: 'center', gap: 16}}>
                  <div style={{width: Math.max(4, x.v * maxW * t), height: 34, background: x.c, borderRadius: 6}} />
                  <div style={{fontFamily: display, fontSize: 32, color: j ? C.sub : C.text, opacity: t}}>{Math.round(x.v * 100)}%</div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
      {note && <div style={{position: 'absolute', bottom: 50, left: 150, fontFamily: body, fontSize: 30, color: C.muted}}>{note}</div>}
    </AbsoluteFill>
  );
};
