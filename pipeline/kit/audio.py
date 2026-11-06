"""Loudness-exact mux with a guaranteed decoded peak (approach from the Buh Simulates kit, evanlin23/niche compose.mux).

Single-pass loudnorm + AAC let decoded peaks reach +2.1 dBFS there. Here: exact gain to the target from a measured
integrated loudness, a look-ahead limiter, then the ENCODED file is decoded and measured, and the limiter ceiling
lowered until no decoded sample exceeds -1 dBFS. The final loudness is re-measured and trimmed once if it drifted.
"""
import re, subprocess


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


def mux(video, audio, out, target=-14.0, max_peak=-1.0, extra_args=()):
    """video (its own video stream is copied) + audio -> out.mp4 at `target` LUFS (+-0.4) with decoded peak <= max_peak.
    For each limiter ceiling, re-aim the gain (limiting eats loudness on peaky voices) up to 4 times; if the decoded
    peak is over, drop to a lower ceiling. Returns the measured result; raises if no setting meets both limits."""
    base = target - lufs(audio)
    best = None
    for ceiling_db in (-1.5, -2.0, -3.0, -4.0):
        gain = base
        for _ in range(4):
            af = f"aresample=48000,volume={gain:.2f}dB,alimiter=limit={10 ** (ceiling_db / 20):.4f}:attack=5:release=80:level=false"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(audio), "-map", "0:v", "-map", "1:a",
                            "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                            "-movflags", "+faststart", *extra_args, str(out)], check=True)
            pk, li = decoded_peak_dbfs(out), lufs(out)
            print(f"  audio: gain {gain:+.2f} dB, limiter {ceiling_db} dB -> decoded peak {pk:.2f} dBFS, {li:.1f} LUFS")
            if pk > max_peak:
                break                              # this ceiling overshoots after AAC: try a lower one
            if abs(li - target) <= 0.4:
                return {"lufs": li, "peak_dbfs": pk}
            best = (abs(li - target), li, pk)
            gain += target - li
    raise SystemExit(f"audio: no limiter setting reached {target} LUFS with decoded peak <= {max_peak} dBFS (closest {best})")
