"""Assemble a sharded render: concat silent video segments, mux the narration at -14 LUFS, decoded peak <= -1 dBFS.
Usage: assemble.py <segments_dir> <narration.wav> <out.mp4>
Segments are named seg-<NNN>.mp4 and are concatenated in numeric order."""
import glob, os, subprocess, sys

seg_dir, wav, out = sys.argv[1], sys.argv[2], sys.argv[3]
segs = sorted(glob.glob(os.path.join(seg_dir, "**", "seg-*.mp4"), recursive=True),
              key=lambda p: int(os.path.basename(p)[4:-4]))
if not segs: sys.exit("no segments found")
lst = os.path.join(seg_dir, "concat.txt")
open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
video = os.path.join(seg_dir, "video.mp4")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video], check=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit.audio import mux  # noqa: E402

# exact gain to -14 LUFS + look-ahead limiter; decoded peak verified <= -1 dBFS on the encoded file
m = mux(video, wav, out)
print(f"loudness {m['lufs']:.1f} LUFS, decoded peak {m['peak_dbfs']:.2f} dBFS")
dur =subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
print(f"assembled {len(segs)} segments -> {out} ({float(dur):.1f}s)")
