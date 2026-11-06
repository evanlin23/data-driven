import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display} from '../theme';
import {ease} from '../anim';

export type TextBeatProps = {
  /** words wrapped in *asterisks* get the accent color; "|" forces a line break (no awkward orphan words) */
  text: string;
  sub?: string;
  size?: number;
};

/** One line on screen, revealed word by word. Use sparingly: for the claim, the twist, the question. */
export const TextBeat: React.FC<TextBeatProps> = ({text, sub, size = 96}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lines = text.split('|').map((l) => l.trim().split(' ').filter(Boolean));
  const total = lines.reduce((n, l) => n + l.length, 0);
  const per = Math.min(5, (1.2 * fps) / total);
  let k = 0;
  return (
    <AbsoluteFill style={{background: C.bg, alignItems: 'center', justifyContent: 'center', padding: 140, flexDirection: 'column'}}>
      <div style={{fontFamily: display, fontSize: size, color: C.text, textAlign: 'center', lineHeight: 1.12}}>
        {lines.map((words, li) => (
          <div key={li} style={{whiteSpace: 'nowrap'}}>
            {words.map((w, i) => {
              const j = k++;
              const hot = w.startsWith('*') && w.replace(/[^*]/g, '').length >= 2;
              const a = ease(f, j * per, j * per + 8);
              return (
                <span key={i} style={{opacity: a, color: hot ? C.accent : C.text, display: 'inline-block', transform: `translateY(${(1 - a) * 18}px)`}}>
                  {w.replace(/\*/g, '')}{i < words.length - 1 ? ' ' : ''}
                </span>
              );
            })}
          </div>
        ))}
      </div>
      {sub && <div style={{fontFamily: body, fontSize: 40, color: C.sub, marginTop: 36, textAlign: 'center', opacity: ease(f, total * per + 6, total * per + 20)}}>{sub}</div>}
    </AbsoluteFill>
  );
};
