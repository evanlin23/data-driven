"""Background music bed under the narration: loop to length, fade in/out, sit ~20 dB under the voice and duck
another 8 dB while it speaks.

Licensing (research/copyright-risk.md section 5): use YouTube Audio Library tracks (never claimed via Content ID) or a
channel-whitelisted subscription library, and log every track in episodes/<ep>/look.json. Audio Library terms don't
allow redistributing the file, and this repo is public, so the track is NOT committed: CI downloads it from the
MUSIC_URL repo secret (a private direct-download link) into video/public/music/bed.<ext>.
"""
import numpy as np

SR = 48000


def load(path):
    import subprocess
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def bed(voice, music, level_db=-20.0, duck_db=-8.0, fade_in=2.0, fade_out=4.0):
    """voice: float32 mono @48k. Returns voice + music bed (music RMS `level_db` below the voice's speech RMS)."""
    n = len(voice)
    reps = int(np.ceil(n / max(1, len(music))))
    m = np.tile(music, reps)[:n].astype(np.float32)
    w = int(0.1 * SR)
    env = np.sqrt(np.convolve(voice ** 2, np.ones(w) / w, "same"))
    speech = env > 0.02
    v_rms = np.sqrt((voice[speech] ** 2).mean()) if speech.any() else 0.1
    m_rms = np.sqrt((m ** 2).mean()) + 1e-9
    m *= (v_rms * 10 ** (level_db / 20)) / m_rms
    duck = np.convolve(np.where(speech, 10 ** (duck_db / 20), 1.0), np.ones(4 * w) / (4 * w), "same")  # 400 ms glide
    t = np.arange(n) / SR
    fade = np.minimum(1, t / fade_in) * np.minimum(1, (n / SR - t) / fade_out)
    return (voice + m * duck * fade).astype(np.float32)
