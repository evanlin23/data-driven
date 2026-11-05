import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {BigNumber, BigNumberProps} from './scenes/BigNumber';
import {Scatter, ScatterProps} from './scenes/Scatter';
import {GameCard, GameCardProps} from './scenes/GameCard';
import {LineChart, LineChartProps} from './scenes/LineChart';
import {LaunchCollision, LaunchCollisionProps} from './scenes/LaunchCollision';
import {Leaderboard, LeaderboardProps} from './scenes/Leaderboard';
import {TextBeat, TextBeatProps} from './scenes/TextBeat';
import {ReviewQuote, ReviewQuoteProps} from './scenes/ReviewQuote';
import {C} from './theme';

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
);

export type EpisodeSpec = {fps: number; durationSec: number; audio?: string; music?: string; musicVolume?: number; scenes: Scene[]};

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
  }
};

/** Slow push-in + quick fade so nothing is ever a static slide; alternates direction per scene. */
const Camera: React.FC<{children: React.ReactNode; dur: number; i: number}> = ({children, dur, i}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = dur * fps;
  const z = interpolate(f, [0, n], i % 2 ? [1.0, 1.035] : [1.035, 1.0]);
  const o = interpolate(f, [0, 5, n - 4, n], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{transform: `scale(${z})`, opacity: o}}>{children}</AbsoluteFill>;
};

/** Renders an episode from a JSON spec. Scene timing (seconds) comes from the narration timing file. */
export const Episode: React.FC<{spec: EpisodeSpec}> = ({spec}) => (
  <AbsoluteFill style={{background: C.bg}}>
    {spec.audio && <Audio src={staticFile(spec.audio)} />}
    {spec.music && <Audio src={staticFile(spec.music)} volume={spec.musicVolume ?? 0.08} loop />}
    {spec.scenes.map((s, i) => (
      <Sequence key={i} from={Math.round(s.from * spec.fps)} durationInFrames={Math.max(1, Math.round(s.dur * spec.fps))}>
        <Camera dur={s.dur} i={i}>{render(s)}</Camera>
      </Sequence>
    ))}
  </AbsoluteFill>
);
