import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display} from '../theme';
import {ease} from '../anim';

export type TextBeatProps = {
  /** words wrapped in *asterisks* get the accent color */
  text: string;
  sub?: string;
  size?: number;
};

/** One line on screen, revealed word by word. Use sparingly: for the claim, the twist, the question. */
export const TextBeat: React.FC<TextBeatProps> = ({text, sub, size = 96}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const words = text.split(' ');
  const per = Math.min(5, (1.2 * fps) / words.length);
  return (
    <AbsoluteFill style={{background: C.bg, alignItems: 'center', justifyContent: 'center', padding: 160, flexDirection: 'column'}}>
      <div style={{fontFamily: display, fontSize: size, color: C.text, textAlign: 'center', lineHeight: 1.12}}>
        {words.map((w, i) => {
          const hot = w.startsWith('*') && w.replace(/[^*]/g, '').length >= 2;
          const a = ease(f, i * per, i * per + 8);
          return (
            <span key={i} style={{opacity: a, color: hot ? C.accent : C.text, display: 'inline-block', transform: `translateY(${(1 - a) * 18}px)`}}>
              {w.replace(/\*/g, '')}{i < words.length - 1 ? ' ' : ''}
            </span>
          );
        })}
      </div>
      {sub && <div style={{fontFamily: body, fontSize: 40, color: C.sub, marginTop: 36, opacity: ease(f, words.length * per + 6, words.length * per + 20)}}>{sub}</div>}
    </AbsoluteFill>
  );
};
