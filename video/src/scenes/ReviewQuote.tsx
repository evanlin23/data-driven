import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body} from '../theme';
import {ease, pop} from '../anim';

export type ReviewQuoteProps = {
  quote: string;        // <= 2 sentences, per copyright guide
  hours?: number;       // "Steam reviewer, 41 hrs" — never usernames/avatars
  recommended?: boolean;
  game?: string;
};

/** Anonymized Steam review card. */
export const ReviewQuote: React.FC<ReviewQuoteProps> = ({quote, hours, recommended = true, game}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = pop(f, fps);
  return (
    <AbsoluteFill style={{background: C.bg, alignItems: 'center', justifyContent: 'center'}}>
      <div style={{width: 1300, background: C.panel, borderRadius: 22, padding: '56px 70px', transform: `scale(${0.92 + 0.08 * s})`, opacity: s,
        boxShadow: '0 30px 90px rgba(0,0,0,.55)'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 18, marginBottom: 30}}>
          <div style={{width: 64, height: 64, borderRadius: 12, background: recommended ? C.blue : C.accent, display: 'flex',
            alignItems: 'center', justifyContent: 'center', fontSize: 40, color: C.text}}>{recommended ? '👍' : '👎'}</div>
          <div style={{fontFamily: body, fontWeight: 800, fontSize: 38, color: C.text}}>{recommended ? 'Recommended' : 'Not Recommended'}</div>
          <div style={{fontFamily: body, fontSize: 32, color: C.sub, marginLeft: 'auto'}}>
            Steam reviewer{hours !== undefined ? ` · ${hours} hrs on record` : ''}
          </div>
        </div>
        <div style={{fontFamily: body, fontSize: 50, color: C.text, lineHeight: 1.35, opacity: ease(f, 8, 22)}}>“{quote}”</div>
        {game && <div style={{fontFamily: body, fontSize: 32, color: C.muted, marginTop: 26}}>— on {game}</div>}
      </div>
    </AbsoluteFill>
  );
};
