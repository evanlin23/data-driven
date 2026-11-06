import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {BigNumber, BigNumberProps} from './scenes/BigNumber';
import {Scatter, ScatterProps} from './scenes/Scatter';
import {GameCard, GameCardProps} from './scenes/GameCard';
import {LineChart, LineChartProps} from './scenes/LineChart';
import {LaunchCollision, LaunchCollisionProps} from './scenes/LaunchCollision';
import {Leaderboard, LeaderboardProps} from './scenes/Leaderboard';
import {TextBeat, TextBeatProps} from './scenes/TextBeat';
import {ReviewQuote, ReviewQuoteProps} from './scenes/ReviewQuote';
import {CompareBars, CompareBarsProps} from './scenes/CompareBars';
import {GapBars, GapBarsProps} from './scenes/GapBars';
import {C, setStyle, texture, transition} from './theme';
import {TextureOverlay} from './Texture';

type Base = {from: number; dur: number};
export type Scene = Base & (
  | {type: 'bigNumber'; props: BigNumberProps}
  | {type: 'scatter'; props: ScatterProps}
  | {type: 'gameCard'; props: GameCardProps}
  | {type: 'lineChart'; props: LineChartProps}
  | {type: 'launchCollision'; props: LaunchCollisionProps}
  | {type: 'leaderboard'; props: LeaderboardProps}
  | {type: 'textBeat'; props: TextBeatProps}
  | {type: 'reviewQuote'; props: ReviewQuoteProps}
  | {type: 'compareBars'; props: CompareBarsProps}
  | {type: 'gapBars'; props: GapBarsProps}
);

export type EpisodeSpec = {fps: number; durationSec: number; style?: string; audio?: string; music?: string; musicVolume?: number; scenes: Scene[]};

const render = (s: Scene) => {
  switch (s.type) {
    case 'bigNumber': return <BigNumber {...s.props} />;
    case 'scatter': return <Scatter {...s.props} />;
    case 'gameCard': return <GameCard {...s.props} />;
    case 'lineChart': return <LineChart {...s.props} />;
    case 'launchCollision': return <LaunchCollision {...s.props} />;
    case 'leaderboard': return <Leaderboard {...s.props} />;
    case 'textBeat': return <TextBeat {...s.props} />;
    case 'reviewQuote': return <ReviewQuote {...s.props} />;
    case 'compareBars': return <CompareBars {...s.props} />;
    case 'gapBars': return <GapBars {...s.props} />;
  }
};

/** Slow push-in so nothing is ever a static slide (direction alternates per scene). Entry: a quick fade, or for
 *  'slide' styles a short eased slide from the right (the sheet texture travels with it, see SheetTexture). */
const SLIDE_FRAMES = 10, SLIDE_PX = 160;
const Camera: React.FC<{children: React.ReactNode; dur: number; i: number}> = ({children, dur, i}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = dur * fps;
  const z = interpolate(f, [0, n], i % 2 ? [1.0, 1.035] : [1.035, 1.0]);
  if (transition === 'slide') {
    const t = interpolate(f, [0, SLIDE_FRAMES], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
    const o = interpolate(f, [0, 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return <AbsoluteFill style={{transform: `translateX(${(1 - t) * SLIDE_PX}px) scale(${z})`, opacity: o}}>{children}</AbsoluteFill>;
  }
  const e = Math.min(5, n / 3);  // very short scenes: shorter fades (input range must stay increasing)
  const o = n > 3 ? interpolate(f, [0, e, n - e, n], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
  return <AbsoluteFill style={{transform: `scale(${z})`, opacity: o}}>{children}</AbsoluteFill>;
};

/** Texture that moves with the cuts in 'slide' styles: one continuous sheet panned scene to scene. */
const SheetTexture: React.FC<{spec: EpisodeSpec}> = ({spec}) => {
  const f = useCurrentFrame();
  let idx = 0;
  spec.scenes.forEach((s, i) => { if (f >= Math.round(s.from * spec.fps)) idx = i; });
  const local = f - Math.round((spec.scenes[idx]?.from ?? 0) * spec.fps);
  const t = transition === 'slide' ? interpolate(local, [0, SLIDE_FRAMES], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}) : 1;
  return <TextureOverlay kind={texture} offsetX={-(idx - 1 + t) * SLIDE_PX} />;
};

/** Renders an episode from a JSON spec. Scene timing (seconds) comes from the narration timing file. */
export const Episode: React.FC<{spec: EpisodeSpec; style?: string}> = ({spec, style}) => {
  setStyle(style ?? spec.style);  // before any scene renders: scenes read the live palette/fonts
  return (
  <AbsoluteFill style={{background: C.bg}}>
    {spec.audio && <Audio src={staticFile(spec.audio)} />}
    {spec.music && <Audio src={staticFile(spec.music)} volume={spec.musicVolume ?? 0.08} loop />}
    {spec.scenes.map((s, i) => (
      <Sequence key={i} from={Math.round(s.from * spec.fps)} durationInFrames={Math.max(1, Math.round(s.dur * spec.fps))}>
        <Camera dur={s.dur} i={i}>{render(s)}</Camera>
      </Sequence>
    ))}
    <SheetTexture spec={spec} />
  </AbsoluteFill>
  );
};
