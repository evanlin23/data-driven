"""Audit a rendered episode: contact sheets, scene lengths, loudness, peaks, silences, A/V length.

Usage: python3 pipeline/qa/audit_video.py <film.mp4> episodes/<slug> [out_dir]
Writes out_dir/sheet_N.png (one frame every 3 s with timestamps; LOOK AT EVERY SHEET) and prints a pass/fail list.
Thresholds come from research/human-feel-guide.md and the channel's audio spec (-14 LUFS, true peak <= -1 dBTP).
"""
import glob, json, os, re, shutil, subprocess, sys

film, ep = sys.argv[1], sys.argv[2].rstrip("/")
slug = os.path.basename(ep)
out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.environ.get("TMPDIR", "/tmp"), f"audit-{slug}")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
spec = json.load(open(os.path.join(ROOT, "video", "src", "episodes", f"{slug}.json")))
shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
run = lambda *a: subprocess.run(a, capture_output=True, text=True)
fails = []

dur = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", film).stdout)
print(f"duration {dur // 60:.0f}:{dur % 60:04.1f} (spec {spec['durationSec']:.1f}s)")
if abs(dur - spec["durationSec"]) > 1.5: fails.append(f"film length {dur:.1f}s != spec {spec['durationSec']:.1f}s")
if dur < 8 * 60: print("  note: under 8 minutes (mid-roll ads need 8:00+)")

# scenes that hold one picture too long (static > ~12 s reads as dead air; animated scatter/line charts get more slack)
for i, s in enumerate(spec["scenes"]):
    lim = 14 if s["type"] in ("scatter", "lineChart", "launchCollision", "compareBars") else 12.5
    if s["dur"] > lim:
        fails.append(f"scene {i} {s['type']} holds {s['dur']:.1f}s (> {lim}s): split it into more beats")
print(f"{len(spec['scenes'])} scenes, longest {max(s['dur'] for s in spec['scenes']):.1f}s")

# audio
e = run("ffmpeg", "-nostats", "-i", film, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
li = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]); tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
print(f"loudness {li:.1f} LUFS, true peak {tp:.1f} dBFS")
if abs(li + 14) > 0.7: fails.append(f"loudness {li:.1f} LUFS (target -14)")
if tp > -0.9: fails.append(f"true peak {tp:.1f} dBFS (max -1)")
sil = re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_duration: ([\d.]+)",
                 run("ffmpeg", "-nostats", "-i", film, "-af", "silencedetect=n=-45dB:d=1.2", "-f", "null", "-").stderr)
for s0, d in sil:
    if float(s0) < dur - 3: fails.append(f"silence {float(d):.1f}s at {float(s0):.0f}s")

# pixel gate (as in the Buh Simulates kit): black frames, and 1-2 frame brightness flashes/dips (a frame that jumps
# away from both neighbours and comes straight back reads as a glitch; real cuts change level and stay there)
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", film, "-vf", "scale=96:54,format=gray", "-f", "rawvideo", "-"],
                     capture_output=True).stdout
import numpy as np  # noqa: E402
Y = np.frombuffer(raw, np.uint8).reshape(-1, 54, 96).astype(np.float32)
fps_v = len(Y) / dur
lum = Y.mean(axis=(1, 2))
# blank = a uniform frame (nothing drawn). A fade-through-background cut is <= ~4 blank frames; longer runs mean a
# gap between scenes, a missing scene or a black frame (in any style: Remotion renders full range).
blank = Y.std(axis=(1, 2)) < 2
run, start = 0, 0
for i, bl in enumerate(list(blank) + [False]):
    if bl:
        start = i if run == 0 else start; run += 1
    else:
        if run > 6: fails.append(f"blank picture for {run} frames at {start / fps_v:.2f}s (gap or missing scene)")
        run = 0
for k in (1, 2):  # spike of width k frames
    a, mid, b = lum[:-k - 1], np.array([lum[i + 1:i + 1 + k].mean() for i in range(len(lum) - k - 1)]), lum[k + 1:]
    jump = np.minimum(np.abs(mid - a), np.abs(mid - b))
    back = np.abs(a - b)
    for i in np.where((jump > 25) & (back < 6))[0][:5]:
        fails.append(f"{k}-frame flash/dip at {(i + 1) / fps_v:.2f}s (luma {a[i]:.0f} -> {mid[i]:.0f} -> {b[i]:.0f})")
print(f"pixel gate: {len(Y)} frames checked")

# contact sheets: a frame every 3 s, 8x6 per sheet
run("ffmpeg", "-loglevel", "error", "-i", film, "-vf",
    "fps=1/3,scale=480:-1,drawtext=text='%{pts\\:hms}':x=5:y=5:fontsize=18:fontcolor=yellow", os.path.join(out, "f_%04d.png"))
frames = sorted(glob.glob(os.path.join(out, "f_*.png")))
for k in range(0, len(frames), 48):
    run("ffmpeg", "-loglevel", "error", "-y", "-pattern_type", "glob", "-i", os.path.join(out, "f_*.png"), "-vf",
        f"select='between(n,{k},{k + 47})',tile=8x6", "-frames:v", "1", os.path.join(out, f"sheet_{k // 48}.png"))
for f in frames: os.remove(f)
print(f"contact sheets: {sorted(glob.glob(os.path.join(out, 'sheet_*.png')))}")
print("  look for: cut-off/overlapping text, wrapped titles, wrong or mid-count numbers on the LAST frame of a scene,")
print("  missing art, spoilers before the reveal, captions that contradict the narration")

print("\n" + ("PASS (automatic checks) - now review the sheets" if not fails else "FAIL:\n  " + "\n  ".join(fails)))
sys.exit(1 if fails else 0)
