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
# at -16.5), then gain, then a look-ahead limiter, all at 48 kHz. Do NOT oversample: limiting at 192 kHz and resampling
# down left near-Nyquist energy that AAC's lowpass turned into ~3 dB of overshoot (0.35 dB at 48 kHz; measured).
COMP = "acompressor=threshold=0.063:ratio=4:attack=5:release=80:knee=4"


def mux(video, audio, out, target=-15.0, max_peak=-1.0, tol=1.0, extra_args=()):
    """video (its own video stream is copied) + audio -> out.mp4 at `target` LUFS (+-tol) with decoded peak <= max_peak,
    Target -15 LUFS (spoken-word range; YouTube only turns DOWN louder audio): on the Achird voice -14 needed a ceiling
    that left no room for AAC overshoot, and pushing harder only crushed the voice.
    measured on the ENCODED file. Re-aims the gain per limiter ceiling; lowers the ceiling if AAC overshoots."""
    def run(gain, ceiling_db):
        af = (f"aresample=48000,{COMP},volume={gain:.2f}dB,"
              f"alimiter=limit={10 ** (ceiling_db / 20):.4f}:attack=5:release=80:level=false")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(audio), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                        "-movflags", "+faststart", *extra_args, str(out)], check=True)
        return decoded_peak_dbfs(out), lufs(out)

    # Converge gain and ceiling together: AAC overshoot over the limiter ceiling varies by take (0.5-3 dB seen), so
    # measure it each pass and pull the ceiling down by exactly that much, while re-aiming the gain at the target.
    _, li0 = run(0.0, -2.0)
    gain, ceiling_db, best = target - li0, -2.0, None
    for _ in range(10):
        pk, li = run(gain, ceiling_db)
        print(f"  audio: compressor + gain {gain:+.2f} dB + limiter {ceiling_db:.2f} dB -> decoded peak {pk:.2f} dBFS, {li:.1f} LUFS")
        ok_pk, ok_li = pk <= max_peak, abs(li - target) <= tol
        if ok_pk and ok_li:
            return {"lufs": li, "peak_dbfs": pk}
        if ok_pk and (best is None or abs(li - target) < best[0]): best = (round(abs(li - target), 2), li, pk)
        if not ok_pk: ceiling_db -= (pk - max_peak) + 0.3
        if not ok_li: gain += target - li
        ceiling_db = max(ceiling_db, -9.0)
    raise SystemExit(f"audio: no setting reached {target} LUFS with decoded peak <= {max_peak} dBFS (closest {best})")
