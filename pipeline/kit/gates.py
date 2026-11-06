"""Video gates shared by every channel (see docs/KIT.md). Each returns a list of human-readable failures."""
import subprocess
import numpy as np


def pixel_gate(film, max_blank_frames=6):
    """Blank-picture runs (gaps, missing scenes, black) longer than a fade cut, and 1-2 frame flashes or dips:
    a frame that jumps away from both neighbours and comes straight back reads as a glitch (a real cut changes
    level and stays there). From the Buh Simulates kit's pixel gate."""
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(film), "-vf", "scale=96:54,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    Y = np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.float32)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(film)],
                               capture_output=True, text=True).stdout)
    fps = len(Y) / dur
    fails = []
    blank = Y.std(axis=(1, 2)) < 2
    run = start = 0
    for i, bl in enumerate(list(blank) + [False]):
        if bl:
            start = i if run == 0 else start
            run += 1
        else:
            if run > max_blank_frames:
                fails.append(f"blank picture for {run} frames at {start / fps:.2f}s (gap, missing scene or black)")
            run = 0
    lum = Y.mean(axis=(1, 2))
    for k in (1, 2):
        a, b = lum[:-k - 1], lum[k + 1:]
        mid = np.array([lum[i + 1:i + 1 + k].mean() for i in range(len(lum) - k - 1)])
        jump = np.minimum(np.abs(mid - a), np.abs(mid - b))
        for i in np.where((jump > 25) & (np.abs(a - b) < 6))[0][:5]:
            fails.append(f"{k}-frame flash/dip at {(i + 1) / fps:.2f}s (luma {a[i]:.0f} -> {mid[i]:.0f} -> {b[i]:.0f})")
    return fails
