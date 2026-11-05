import React, {useMemo} from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {C, display, hand} from './theme';

export type ThumbnailProps = {
  variant: 'dot' | 'number' | 'versus';
  /** background cloud: [quality 0-1, log10 reviews] pairs, sampled from the real data */
  cloud: [number, number][];
  hero: [number, number];       // the highlighted game in the same space
  words?: string;               // <= 3 words
  bigNumber?: string;           // for 'number' variant, e.g. "302"
  image?: string;               // small game art (secondary), under public/
  versusImage?: string;         // for 'versus': the mega-hit it launched against
};

const TW = 1280, TH = 720;

/** YouTube thumbnail. Readable at 160px: one chart, one red mark, <=3 words. */
export const Thumbnail: React.FC<ThumbnailProps> = ({variant, cloud, hero, words, bigNumber, image, versusImage}) => {
  const L = 60, R = TW - 60, T = 60, B = TH - 60;
  const sx = (q: number) => L + ((q - 0.35) / 0.65) * (R - L);
  const sy = (lg: number) => B - ((lg - 1.0) / 5.2) * (B - T);
  const pts = useMemo(() => cloud.map(([q, lg], i) => <circle key={i} cx={sx(q)} cy={sy(lg)} r={3.2} fill={C.text} opacity={0.33} />), [cloud]);
  const hx = sx(hero[0]), hy = sy(hero[1]);
  return (
    <AbsoluteFill style={{background: C.bg}}>
      <svg width={TW} height={TH}>
        {pts}
        <circle cx={hx} cy={hy} r={13} fill={C.accent} />
        <ellipse cx={hx} cy={hy} rx={62} ry={50} fill="none" stroke={C.accent} strokeWidth={9} transform={`rotate(-12 ${hx} ${hy})`} />
        {variant !== 'number' && (
          <path d={`M ${hx - 330} ${hy - 210} Q ${hx - 160} ${hy - 230} ${hx - 70} ${hy - 62}`} fill="none" stroke={C.accent} strokeWidth={10} strokeLinecap="round" />
        )}
      </svg>
      {variant === 'number' && bigNumber && (
        <div style={{position: 'absolute', left: 70, top: 70, fontFamily: display, fontSize: 250, color: C.text, lineHeight: 0.9}}>
          {bigNumber}
          <div style={{fontFamily: display, fontSize: 64, color: C.accent, marginTop: 18}}>{words}</div>
        </div>
      )}
      {variant !== 'number' && words && (
        <div style={{position: 'absolute', left: 60, ...(variant === 'versus' ? {bottom: 60} : {top: 70}), fontFamily: display, fontSize: 104, color: C.text, lineHeight: 0.95, maxWidth: 700,
          textShadow: '0 6px 30px rgba(0,0,0,.8)'}}>
          {words}
        </div>
      )}
      {image && variant !== 'versus' && (
        <Img src={staticFile(image)} style={{position: 'absolute', right: 50, top: 50, width: 360, borderRadius: 12, border: `5px solid ${C.accent}`}} />
      )}
      {variant === 'versus' && versusImage && (
        <div style={{position: 'absolute', right: 40, top: 40, display: 'flex', alignItems: 'center', gap: 16}}>
          {image ? <Img src={staticFile(image)} style={{width: 300, borderRadius: 12, border: `5px solid ${C.accent}`}} /> : (
            // the mystery game: never show the answer on the thumbnail
            <div style={{width: 300, height: 140, borderRadius: 12, border: `5px solid ${C.accent}`, background: C.panel,
              display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: display, fontSize: 110, color: C.accent}}>?</div>
          )}
          <div style={{fontFamily: hand, fontSize: 64, color: C.gold}}>vs</div>
          <Img src={staticFile(versusImage)} style={{width: 300, borderRadius: 12, opacity: 0.9}} />
        </div>
      )}
    </AbsoluteFill>
  );
};
