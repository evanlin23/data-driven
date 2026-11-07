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


# Voice-over chain: compressor evens out syllable peaks (TTS voices peak near full scale on every syllable, so a limiter
# alone can't reach -14 LUFS: on the ep001 Achird take +10 dB into a limiter added ~1 LU, and dynamic loudnorm stopped
# at -16.5), then gain, then a look-ahead limiter at 4x rate (catches inter-sample peaks AAC turns into overshoot).
COMP = "acompressor=threshold=0.063:ratio=4:attack=5:release=80:knee=4"


def mux(video, audio, out, target=-14.0, max_peak=-1.0, tol=1.0, extra_args=()):
    """video (its own video stream is copied) + audio -> out.mp4 at `target` LUFS (+-tol) with decoded peak <= max_peak,
    measured on the ENCODED file. Re-aims the gain per limiter ceiling; lowers the ceiling if AAC overshoots."""
    def run(gain, ceiling_db):
        af = (f"aresample=192000,{COMP},volume={gain:.2f}dB,"
              f"alimiter=limit={10 ** (ceiling_db / 20):.4f}:attack=5:release=80:level=false,aresample=48000")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(audio), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                        "-movflags", "+faststart", *extra_args, str(out)], check=True)
        return decoded_peak_dbfs(out), lufs(out)

    gain, best = None, None
    for ceiling_db in (-2.0, -3.0, -4.0):
        if gain is None:  # first estimate: measure the compressed signal at unity gain
            _, li0 = run(0.0, ceiling_db)
            gain = target - li0
        for _ in range(5):
            pk, li = run(gain, ceiling_db)
            print(f"  audio: compressor + gain {gain:+.2f} dB + limiter {ceiling_db} dB -> decoded peak {pk:.2f} dBFS, {li:.1f} LUFS")
            if pk > max_peak:
                break
            if abs(li - target) <= tol:  # +-1 LU: inaudible; pushing harder crushes the voice (ep001 levelled at -14.6)
                return {"lufs": li, "peak_dbfs": pk}
            best = (round(abs(li - target), 2), li, pk)
            gain += target - li
    raise SystemExit(f"audio: no setting reached {target} LUFS with decoded peak <= {max_peak} dBFS (closest {best})")
