import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, display, hand} from '../theme';
import {ease} from '../anim';

export type LineChartProps = {
  title?: string;
  /** x labels shown under the axis, e.g. years; values are indices into `values` */
  xTicks?: {i: number; t: string}[];
  values: number[];
  yMax?: number;
  yLabel?: string;
  /** annotate one index (e.g. "launch" or "the big sale") */
  mark?: {i: number; text: string};
  drawSeconds?: number;
  color?: 'accent' | 'gold' | 'good' | 'blue';
};

const PAD = {l: 150, r: 90, t: 170, b: 140};

/** A line that draws itself left-to-right: lifetime review history, player counts, prices over time. */
export const LineChart: React.FC<LineChartProps> = ({title, xTicks = [], values, yMax, yLabel, mark, drawSeconds = 2.5, color = 'gold'}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const max = yMax ?? Math.max(...values) * 1.1;
  const sx = (i: number) => PAD.l + (i / Math.max(values.length - 1, 1)) * (width - PAD.l - PAD.r);
  const sy = (v: number) => height - PAD.b - (v / max) * (height - PAD.t - PAD.b);
  const t = ease(f, 6, drawSeconds * fps);
  const shown = Math.max(2, Math.ceil(values.length * t));
  const pts = values.slice(0, shown).map((v, i) => `${sx(i)},${sy(v)}`).join(' ');
  const area = `${sx(0)},${sy(0)} ${pts} ${sx(shown - 1)},${sy(0)}`;
  const markIn = mark ? ease(f, drawSeconds * fps * (mark.i / values.length) + 6, drawSeconds * fps * (mark.i / values.length) + 24) : 0;
  return (
    <AbsoluteFill style={{background: C.bg}}>
      {title && <div style={{position: 'absolute', top: 60, left: PAD.l, fontFamily: display, fontSize: 64, color: C.text}}>{title}</div>}
      <svg width={width} height={height}>
        <line x1={PAD.l} x2={width - PAD.r} y1={sy(0)} y2={sy(0)} stroke={C.grid} strokeWidth={3} />
        {xTicks.map((x) => (
          <text key={x.i} x={sx(x.i)} y={height - PAD.b + 56} fill={C.muted} fontSize={34} fontFamily={body} textAnchor="middle">{x.t}</text>
        ))}
        <polygon points={area} fill={C[color]} opacity={0.12} />
        <polyline points={pts} fill="none" stroke={C[color]} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" />
        {mark && (
          <g opacity={markIn}>
            <line x1={sx(mark.i)} x2={sx(mark.i)} y1={PAD.t - 10} y2={sy(0)} stroke={C.accent} strokeWidth={4} strokeDasharray="12 10" />
          </g>
        )}
        {yLabel && <text x={PAD.l} y={PAD.t - 30} fill={C.sub} fontSize={36} fontFamily={body} fontWeight={600}>{yLabel}</text>}
      </svg>
      {mark && (
        <div style={{position: 'absolute', left: Math.min(sx(mark.i) + 24, width - 620), top: PAD.t + 10, fontFamily: hand, fontSize: 56,
          color: C.accent, opacity: markIn, transform: 'rotate(-3deg)'}}>{mark.text}</div>
      )}
    </AbsoluteFill>
  );
};
