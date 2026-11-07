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

/** One line on screen, revealed word by word, set left like a magazine pull quote under an accent rule
 *  (a centered line on an empty frame reads as a slide). Use sparingly: for the claim, the twist, the question. */
export const TextBeat: React.FC<TextBeatProps> = ({text, sub, size = 96}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lines = text.split('|').map((l) => l.trim().split(' ').filter(Boolean));
  const total = lines.reduce((n, l) => n + l.length, 0);
  const per = Math.min(5, (1.2 * fps) / total);
  let k = 0;
  let inHot = false; // *spans* may cover several words
  return (
    <AbsoluteFill style={{background: C.bg, justifyContent: 'center', padding: '0 200px', flexDirection: 'column'}}>
      <div style={{width: 120 * ease(f, 0, 10), height: 10, background: C.accent, borderRadius: 5, marginBottom: 46}} />
      <div style={{fontFamily: display, fontSize: size, color: C.text, textAlign: 'left', lineHeight: 1.1}}>
        {lines.map((words, li) => (
          <div key={li} style={{whiteSpace: 'nowrap'}}>
            {words.map((w, i) => {
              const j = k++;
              const opens = w.startsWith('*');
              const closes = /\*[^\w]*$/.test(w) && (!opens || w.length > 1 && w.replace(/[^*]/g, '').length >= 2);
              const hot = inHot || opens;
              if (opens && !closes) inHot = true;
              if (closes) inHot = false;
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
      {sub && <div style={{fontFamily: body, fontSize: 38, color: C.sub, marginTop: 40, textAlign: 'left', maxWidth: 1300, opacity: ease(f, total * per + 6, total * per + 20)}}>{sub}</div>}
    </AbsoluteFill>
  );
};
