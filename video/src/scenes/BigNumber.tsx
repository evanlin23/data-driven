import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display} from '../theme';
import {ease, fmt, NumKind, pop} from '../anim';

export type BigNumberProps = {
  value: number;
  kind?: NumKind;
  label: string;
  sub?: string;
  color?: 'text' | 'accent' | 'gold' | 'good';
  countSeconds?: number;
};

/** A number that counts up, with its label beside it (spec-sheet layout, not a centered slide).
 *  Percentages also get a 0-100% meter across the bottom, so the space shows the size of the number. */
export const BigNumber: React.FC<BigNumberProps> = ({value, kind = 'int', label, sub, color = 'text', countSeconds = 1.2}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = ease(f, 0, countSeconds * fps);
  const s = pop(f, fps);
  const subIn = ease(f, countSeconds * fps, countSeconds * fps + 12);
  const text = fmt(value * t, kind);
  const numSize = fmt(value, kind).length > 4 ? 250 : 320;
  const meter = kind === 'pct';
  return (
    <AbsoluteFill style={{background: C.bg, padding: '0 160px', justifyContent: 'center'}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 70, marginTop: meter ? -90 : 0}}>
        <div style={{fontFamily: display, fontSize: numSize, color: C[color], transform: `scale(${0.9 + 0.1 * s})`, transformOrigin: 'left center',
          letterSpacing: -4, lineHeight: 1, whiteSpace: 'nowrap', fontVariantNumeric: 'tabular-nums'}}>{text}</div>
        <div style={{width: 6, alignSelf: 'stretch', background: C.grid, borderRadius: 3, opacity: s}} />
        <div style={{display: 'flex', flexDirection: 'column', gap: 18, maxWidth: 820}}>
          <div style={{fontFamily: body, fontWeight: 800, fontSize: label.length > 45 ? 48 : 58, color: C.text, opacity: s, lineHeight: 1.18}}>{label}</div>
          {sub && <div style={{fontFamily: body, fontSize: 30, color: C.sub, opacity: subIn, lineHeight: 1.35}}>{sub}</div>}
        </div>
      </div>
      {meter && (
        <div style={{position: 'absolute', left: 160, right: 160, bottom: 150, opacity: s}}>
          <div style={{height: 34, background: C.panel, borderRadius: 8, overflow: 'hidden'}}>
            <div style={{width: `${value * t * 100}%`, height: '100%', background: C[color === 'text' ? 'gold' : color]}} />
          </div>
          <div style={{display: 'flex', justifyContent: 'space-between', marginTop: 12, fontFamily: body, fontSize: 26, color: C.muted}}>
            {[0, 25, 50, 75, 100].map((v) => <span key={v}>{v}%</span>)}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
