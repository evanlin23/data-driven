"""Sound design from an episode spec, using CC0 samples in video/public/sfx (credits: video/public/sfx/CREDITS.md).

Events, all quiet (a bed under the voice, never over it):
  scene cut         -> page flip (rotating variants)
  number count-up   -> ticks that follow the count's easing (bigNumber, gapBars bars)
  stamp / callout   -> pencil scratch (gapBars "x short", scatter callout)
  highlight         -> pen tap (scatter red dot)
Usage: python3 pipeline/kit/sfx.py <spec.json> <out.wav>       (48 kHz mono float)
       python3 pipeline/kit/sfx.py <spec.json> <voice.wav> --mix <out.wav>   (voice + sfx, ducked)
Timings mirror the scene components (video/src/scenes/*.tsx defaults); keep them in sync when those change.
"""
import json, sys
import numpy as np

SR = 48000
rng = np.random.default_rng(3)


import glob, os
SFX_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "video", "public", "sfx")
_cache = {}


def _sample(prefix, i, level):
    """i-th variant (rotating) of video/public/sfx/<prefix>*.wav, scaled to `level` peak."""
    if prefix not in _cache:
        import soundfile as sf
        files = sorted(glob.glob(os.path.join(SFX_DIR, f"{prefix}*.wav")))
        if not files: raise SystemExit(f"sfx: no samples for '{prefix}' in {SFX_DIR}")
        _cache[prefix] = []
        for f in files:
            x, sr = sf.read(f, dtype="float32")
            if x.ndim > 1: x = x.mean(1)
            if sr != SR: x = np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x).astype(np.float32)
            _cache[prefix].append(x / (np.abs(x).max() + 1e-9))
    v = _cache[prefix]
    return v[i % len(v)] * level


_n = {"slide": 0, "tick": 0, "scratch": 0}
def slide():
    _n["slide"] += 1; return _sample("page_flip", _n["slide"], 0.09)


def tick(freq=None):  # freq kept for call compatibility: the higher "actual" bar uses the second tick variant
    return _sample("tick", 1 if (freq or 0) > 2400 else 0, 0.10)


def tap():
    return _sample("click", 0, 0.18)


def scratch(dur=None):
    _n["scratch"] += 1; return _sample("pencil_stroke", _n["scratch"], 0.12)


def _ease_inout(u):  # remotion Easing.inOut(Easing.cubic)-like, for tick spacing
    return np.where(u < 0.5, 4 * u ** 3, 1 - (-2 * u + 2) ** 3 / 2)


def count_ticks(t0, dur, n=14):
    """n ticks placed where the eased count crosses equal steps (dense mid-count, sparse at the ends)."""
    u = np.linspace(0, 1, 2000)
    v = _ease_inout(u)
    return [t0 + dur * u[np.searchsorted(v, k / n)] for k in range(1, n)]


def events(spec):
    ev = []
    for i, s in enumerate(spec["scenes"]):
        t0, p = s["from"], s.get("props", {})
        if i > 0:
            ev.append((t0, slide()))
        if s["type"] == "bigNumber":
            for t in count_ticks(t0, p.get("countSeconds", 1.2)):
                ev.append((t, tick()))
        elif s["type"] == "gapBars":   # GapBars.tsx: expected 0.2-1.4 s, actual 0.9-1.7 s, stamp at 2.0 s
            for t in count_ticks(t0 + 0.2, 1.2, 10): ev.append((t, tick(2100)))
            for t in count_ticks(t0 + 0.9, 0.8, 6): ev.append((t, tick(2600)))
            ev.append((t0 + 2.0, scratch()))
        elif s["type"] == "scatter" and "highlight" in p:   # Scatter.tsx: ring at highlightAt, callout +0.5 s
            h = t0 + p.get("highlightAt", 3)
            ev.append((h, tap()))
            if p.get("callout"): ev.append((h + 0.5, scratch(0.32)))
    return ev


def render(spec, dur=None):
    dur = dur or spec["durationSec"]
    out = np.zeros(int(dur * SR) + SR, np.float32)
    for t, x in events(spec):
        a = int(t * SR)
        if a < len(out):
            out[a:a + len(x)] += x[:len(out) - a]
    return out[:int(dur * SR)]


def mix(voice, sfx, duck_db=-6.0):
    """voice + sfx, with sfx ducked while the voice is loud (100 ms envelope)."""
    n = max(len(voice), len(sfx))
    v = np.pad(voice, (0, n - len(voice))); s = np.pad(sfx, (0, n - len(sfx)))
    w = int(0.1 * SR)
    env = np.sqrt(np.convolve(v ** 2, np.ones(w) / w, "same"))
    duck = np.where(env > 0.02, 10 ** (duck_db / 20), 1.0)
    duck = np.convolve(duck, np.ones(w) / w, "same")
    return (v + s * duck).astype(np.float32)


if __name__ == "__main__":
    import soundfile as sf
    spec = json.load(open(sys.argv[1]))
    if "--mix" in sys.argv:
        voice, sr = sf.read(sys.argv[2], dtype="float32")
        if voice.ndim > 1: voice = voice.mean(1)
        if sr != SR: voice = np.interp(np.arange(0, len(voice), sr / SR), np.arange(len(voice)), voice).astype(np.float32)
        sf.write(sys.argv[-1], mix(voice, render(spec, len(voice) / SR)), SR)
    else:
        sf.write(sys.argv[2], render(spec), SR)
    print(f"sfx: {len(events(spec))} events -> {sys.argv[-1]}")
