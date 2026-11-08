"""Loudness-exact mux with a guaranteed decoded peak (approach from the Buh Simulates kit, evanlin23/niche compose.mux).

Single-pass loudnorm + AAC let decoded peaks reach +2.1 dBFS there. Here: exact gain to the target from a measured
integrated loudness, a look-ahead limiter, then the ENCODED file is decoded and measured, and the limiter ceiling
lowered until no decoded sample exceeds -1 dBFS. The final loudness is re-measured and trimmed once if it drifted.
"""
import re, subprocess
import numpy as np


def lufs(path):
    e = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1])


def decoded_peak_dbfs(path):
    """Highest absolute decoded sample, in dBFS (what a player actually outputs, after AAC)."""
    e = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(path), "-af", "astats=measure_perchannel=none:measure_overall=Peak_level",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    v = re.findall(r"Peak level dB:\s+(-?[\d.]+|-inf)", e)
    return float(v[-1]) if v and v[-1] != "-inf" else -120.0


# Voice-over chain: compressor evens out syllable peaks (TTS voices peak near full scale on every syllable, so a limiter
# alone can't reach -14 LUFS: on the ep001 Achird take +10 dB into a limiter added ~1 LU, and dynamic loudnorm stopped
# at -16.5), then gain, then a look-ahead limiter, all at 48 kHz. Do NOT oversample: limiting at 192 kHz and resampling
# down left near-Nyquist energy that AAC's lowpass turned into ~3 dB of overshoot (0.35 dB at 48 kHz; measured).
COMP = "acompressor=threshold=0.063:ratio=4:attack=5:release=80:knee=4"


def _render(audio_path, af):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(audio_path), "-af", af, "-ac", "1", "-ar", "48000",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def _lufs_arr(x):
    p = subprocess.run(["ffmpeg", "-nostats", "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", "-", "-af",
                        "ebur128=framelog=quiet", "-f", "null", "-"], input=x.astype(np.float32).tobytes(),
                       capture_output=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr.decode())[-1])


def _encode(video, x, out, extra_args=()):
    p = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-f", "f32le", "-ar", "48000", "-ac", "1",
                        "-i", "-", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-ar", "48000", "-shortest", "-movflags", "+faststart", *extra_args, str(out)],
                       input=x.astype(np.float32).tobytes(), capture_output=True)
    if p.returncode: raise SystemExit(p.stderr.decode()[-500:])
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(out), "-vn", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def mux(video, audio, out, target=-15.0, max_peak=-1.0, tol=1.0, extra_args=()):
    """video (its video stream copied) + audio -> out.mp4 at `target` LUFS (+-tol), decoded peak <= max_peak.

    1. Loudness on the PCM: compressor + gain + limiter (-2 dB ceiling) at 48 kHz, gain re-aimed until on target.
    2. Peaks on the ENCODED file: AAC overshoot depends on the take (0.3-4 dB seen, at chunk joins and transients),
       so encode, decode, find the samples over max_peak and dip the gain smoothly (20 ms raised cosine) at exactly
       those spots, then re-encode. Local dips leave the loudness unchanged. Repeat until clean.
    Target -15 LUFS: spoken-word range; YouTube only turns DOWN audio louder than -14."""
    lim = 10 ** (-2.0 / 20)
    gain = target - lufs(audio)
    for _ in range(6):
        x = _render(audio, f"aresample=48000,{COMP},volume={gain:.2f}dB,alimiter=limit={lim:.4f}:attack=5:release=80:level=false")
        li = _lufs_arr(x)
        if abs(li - target) <= 0.3: break
        gain += target - li
    print(f"  audio: compressor + gain {gain:+.2f} dB + limiter -2 dB -> {li:.1f} LUFS (PCM)")
    w = int(0.010 * 48000)
    win = 0.5 - 0.5 * np.cos(np.linspace(0, 2 * np.pi, 2 * w + 1))
    for it in range(8):
        dec = _encode(video, x, out, extra_args)
        n = min(len(dec), len(x))
        over = np.where(np.abs(dec[:n]) > 10 ** ((max_peak - 0.1) / 20))[0]
        pk = 20 * np.log10(np.abs(dec).max() + 1e-12)
        if not len(over):
            li = lufs(out)
            print(f"  audio: {it} spot repair pass(es) -> decoded peak {pk:.2f} dBFS, {li:.1f} LUFS")
            if abs(li - target) > tol:
                raise SystemExit(f"audio: loudness {li:.1f} LUFS outside {target} +-{tol}")
            return {"lufs": li, "peak_dbfs": float(pk)}
        g = np.ones(len(x), np.float32)
        for i in over:
            need = 10 ** ((max_peak - 0.4) / 20) / abs(dec[i])          # gain that brings this sample under, with margin
            a, b = max(0, i - w), min(len(x), i + w + 1)
            dip = 1 - (1 - need) * win[(a - i + w):(b - i + w)]
            g[a:b] = np.minimum(g[a:b], dip)
        x = x * g
        print(f"  audio: pass {it + 1}: {len(over)} samples over {max_peak} dBFS after AAC (peak {pk:.2f}); dipped locally")
    raise SystemExit(f"audio: decoded peaks still over {max_peak} dBFS after 8 spot-repair passes")
