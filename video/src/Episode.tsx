import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {BigNumber, BigNumberProps} from './scenes/BigNumber';
import {Scatter, ScatterProps} from './scenes/Scatter';
import {GameCard, GameCardProps} from './scenes/GameCard';
import {C} from './theme';

export type Scene =
  | {type: 'bigNumber'; from: number; dur: number; props: BigNumberProps}
  | {type: 'scatter'; from: number; dur: number; props: ScatterProps}
  | {type: 'gameCard'; from: number; dur: number; props: GameCardProps};

export type EpisodeSpec = {fps: number; durationSec: number; audio?: string; scenes: Scene[]};

const render = (s: Scene) => {
  switch (s.type) {
    case 'bigNumber': return <BigNumber {...s.props} />;
    case 'scatter': return <Scatter {...s.props} />;
    case 'gameCard': return <GameCard {...s.props} />;
  }
};

/** Renders an episode from a JSON spec. Scene timing (seconds) comes from the voiceover's word timestamps. */
export const Episode: React.FC<{spec: EpisodeSpec}> = ({spec}) => (
  <AbsoluteFill style={{background: C.bg}}>
    {spec.audio && <Audio src={staticFile(spec.audio)} />}
    {spec.scenes.map((s, i) => (
      <Sequence key={i} from={Math.round(s.from * spec.fps)} durationInFrames={Math.max(1, Math.round(s.dur * spec.fps))}>
        {render(s)}
      </Sequence>
    ))}
  </AbsoluteFill>
);
