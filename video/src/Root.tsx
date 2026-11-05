import React from 'react';
import {Composition, Still} from 'remotion';
import {Thumbnail, ThumbnailProps} from './Thumbnail';
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
    <Still id="Thumbnail" component={Thumbnail} width={1280} height={720}
      defaultProps={{variant: 'dot', cloud: [], hero: [0.96, 2.5], words: 'NOBODY PLAYED IT'} as ThumbnailProps} />
  </>
);
