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

/** A number that counts up, with a label. The workhorse "stat beat". */
export const BigNumber: React.FC<BigNumberProps> = ({value, kind = 'int', label, sub, color = 'text', countSeconds = 1.2}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = ease(f, 0, countSeconds * fps);
  const s = pop(f, fps);
  const subIn = ease(f, countSeconds * fps, countSeconds * fps + 12);
  return (
    <AbsoluteFill style={{background: C.bg, alignItems: 'center', justifyContent: 'center', flexDirection: 'column', padding: '0 180px', textAlign: 'center'}}>
      <div style={{fontFamily: display, fontSize: 260, color: C[color], transform: `scale(${0.85 + 0.15 * s})`, letterSpacing: -4, lineHeight: 1}}>
        {fmt(value * t, kind)}
      </div>
      <div style={{fontFamily: body, fontWeight: 800, fontSize: label.length > 40 ? 52 : 64, color: C.text, marginTop: 30, opacity: s, maxWidth: 1500, lineHeight: 1.2}}>{label}</div>
      {sub && <div style={{fontFamily: body, fontSize: 36, color: C.sub, marginTop: 18, opacity: subIn, maxWidth: 1400, lineHeight: 1.3}}>{sub}</div>}
    </AbsoluteFill>
  );
};
