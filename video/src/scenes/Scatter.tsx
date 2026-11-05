import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, body, hand} from '../theme';
import {clamp, ease} from '../anim';

export type ScatterPoint = {x: number; y: number; label?: string};
export type ScatterProps = {
  points: ScatterPoint[];
  xLabel: string;
  yLabel: string;
  xLog?: boolean;
  yLog?: boolean;
  xDomain?: [number, number];
  yDomain?: [number, number];
  xTicks?: {v: number; t: string}[];
  yTicks?: {v: number; t: string}[];
  /** index of the point to call out; the "which one is it?" moment */
  highlight?: number;
  highlightAt?: number; // seconds
  callout?: string;
  revealSeconds?: number;
  /** optional trend line y = f(x) sampled as points in data space */
  trend?: ScatterPoint[];
  trendAt?: number;
};

const PAD = {l: 190, r: 90, t: 90, b: 150};

export const Scatter: React.FC<ScatterProps> = (p) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const tx = (v: number) => (p.xLog ? Math.log10(Math.max(v, 1e-9)) : v);
  const ty = (v: number) => (p.yLog ? Math.log10(Math.max(v, 1e-9)) : v);
  const xs = p.points.map((d) => tx(d.x));
  const ys = p.points.map((d) => ty(d.y));
  const xd = p.xDomain ? p.xDomain.map(tx) : [Math.min(...xs), Math.max(...xs)];
  const yd = p.yDomain ? p.yDomain.map(ty) : [Math.min(...ys), Math.max(...ys)];
  const sx = (v: number) => PAD.l + ((tx(v) - xd[0]) / (xd[1] - xd[0])) * (width - PAD.l - PAD.r);
  const sy = (v: number) => height - PAD.b - ((ty(v) - yd[0]) / (yd[1] - yd[0])) * (height - PAD.t - PAD.b);

  // stable pseudo-random reveal order so dots "rain in" rather than appear in data order
  const order = useMemo(() => p.points.map((_, i) => ((i * 2654435761) % 1000) / 1000), [p.points]);
  const reveal = (p.revealSeconds ?? 2) * fps;
  const hi = p.highlight;
  const hAt = (p.highlightAt ?? 3) * fps;
  const dim = hi !== undefined ? interpolate(f, [hAt, hAt + 15], [1, 0.25], clamp) : 1;
  const ring = ease(f, hAt, hAt + 20);
  const hp = hi !== undefined ? p.points[hi] : undefined;
  const trendT = p.trend ? ease(f, (p.trendAt ?? 2.5) * fps, (p.trendAt ?? 2.5) * fps + 30) : 0;

  return (
    <AbsoluteFill style={{background: C.bg}}>
      <svg width={width} height={height}>
        {(p.yTicks ?? []).map((t) => (
          <g key={`y${t.v}`}>
            <line x1={PAD.l} x2={width - PAD.r} y1={sy(t.v)} y2={sy(t.v)} stroke={C.grid} strokeWidth={2} />
            <text x={PAD.l - 24} y={sy(t.v) + 12} fill={C.muted} fontSize={34} fontFamily={body} textAnchor="end">{t.t}</text>
          </g>
        ))}
        {(p.xTicks ?? []).map((t) => (
          <text key={`x${t.v}`} x={sx(t.v)} y={height - PAD.b + 56} fill={C.muted} fontSize={34} fontFamily={body} textAnchor="middle">{t.t}</text>
        ))}
        <text x={(PAD.l + width - PAD.r) / 2} y={height - 36} fill={C.sub} fontSize={40} fontFamily={body} fontWeight={600} textAnchor="middle">{p.xLabel}</text>
        <text transform={`translate(56 ${(PAD.t + height - PAD.b) / 2}) rotate(-90)`} fill={C.sub} fontSize={40} fontFamily={body} fontWeight={600} textAnchor="middle">{p.yLabel}</text>
        {p.points.map((d, i) => {
          if (i === hi) return null;
          const a = interpolate(f, [order[i] * reveal, order[i] * reveal + 8], [0, 1], clamp);
          return <circle key={i} cx={sx(d.x)} cy={sy(d.y)} r={5} fill={C.text} opacity={0.55 * a * dim} />;
        })}
        {p.trend && (
          <polyline
            points={p.trend.map((d) => `${sx(d.x)},${sy(d.y)}`).join(' ')}
            fill="none" stroke={C.gold} strokeWidth={6} strokeLinecap="round"
            strokeDasharray={4000} strokeDashoffset={4000 * (1 - trendT)} opacity={0.9}
          />
        )}
        {hp && (
          <g>
            <circle cx={sx(hp.x)} cy={sy(hp.y)} r={11} fill={C.accent} opacity={interpolate(f, [hAt - 10, hAt], [0, 1], clamp)} />
            {/* hand-drawn style ring: slightly elliptical, drawn on with a stroke animation */}
            <ellipse cx={sx(hp.x)} cy={sy(hp.y)} rx={52} ry={44} fill="none" stroke={C.accent} strokeWidth={7}
              strokeDasharray={320} strokeDashoffset={320 * (1 - ring)} transform={`rotate(-12 ${sx(hp.x)} ${sy(hp.y)})`} />
          </g>
        )}
      </svg>
      {hp && p.callout && (
        <div style={{
          position: 'absolute', left: Math.min(sx(hp.x) + 70, width - 700), top: Math.max(sy(hp.y) - 150, 40),
          fontFamily: hand, fontSize: 64, color: C.accent, opacity: ease(f, hAt + 15, hAt + 30), transform: 'rotate(-4deg)',
        }}>
          {p.callout}
        </div>
      )}
    </AbsoluteFill>
  );
};
