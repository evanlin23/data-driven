import React from 'react';
import {Composition} from 'remotion';
import {Episode, EpisodeSpec} from './Episode';
import {FPS, H, W} from './theme';
import demo from './demo-spec.json';

export const Root: React.FC = () => (
  <>
    <Composition
      id="Episode"
      component={Episode}
      width={W}
      height={H}
      fps={FPS}
      durationInFrames={Math.round((demo as EpisodeSpec).durationSec * FPS)}
      defaultProps={{spec: demo as EpisodeSpec}}
      calculateMetadata={({props}) => ({durationInFrames: Math.round(props.spec.durationSec * props.spec.fps)})}
    />
  </>
);
