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
if abs(li + 14) > 1.0: fails.append(f"loudness {li:.1f} LUFS (target -14)")
if tp > -0.9: fails.append(f"true peak {tp:.1f} dBFS (max -1)")
sil = re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_duration: ([\d.]+)",
                 run("ffmpeg", "-nostats", "-i", film, "-af", "silencedetect=n=-45dB:d=1.2", "-f", "null", "-").stderr)
for s0, d in sil:
    if float(s0) < dur - 3: fails.append(f"silence {float(d):.1f}s at {float(s0):.0f}s")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from kit.gates import pixel_gate  # noqa: E402
fails += pixel_gate(film)

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
