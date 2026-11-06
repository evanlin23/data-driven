"""Assemble a sharded render: concat silent video segments, mux the narration, loudness-normalise (two-pass -14 LUFS).
Usage: assemble.py <segments_dir> <narration.wav> <out.mp4>
Segments are named seg-<NNN>.mp4 and are concatenated in numeric order."""
import glob, json, os, subprocess, sys

seg_dir, wav, out = sys.argv[1], sys.argv[2], sys.argv[3]
segs = sorted(glob.glob(os.path.join(seg_dir, "**", "seg-*.mp4"), recursive=True),
              key=lambda p: int(os.path.basename(p)[4:-4]))
if not segs: sys.exit("no segments found")
lst = os.path.join(seg_dir, "concat.txt")
open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
video = os.path.join(seg_dir, "video.mp4")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video], check=True)

def mix(video, wav, out):
    probe = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
    j = json.loads(probe[probe.rfind("{"):probe.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", out], check=True)

mix(video, wav, out)

# Verify on the final file (AAC encode can shift integrated loudness ~1 LU); correct with a plain gain if off by > 0.5.
def measure(path):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=framelog=quiet", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(e[e.rfind(" I:"):].split()[1])
li = measure(out)
if abs(li + 14) > 0.5:
    tmp = out + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", out, "-c:v", "copy", "-af", f"volume={-14 - li:.2f}dB,alimiter=limit=0.89:level=false",  # gain up, but never past -1 dBFS
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", tmp], check=True)
    os.replace(tmp, out)
    print(f"loudness corrected {li:.1f} -> {measure(out):.1f} LUFS")
else:
    print(f"loudness {li:.1f} LUFS")
dur =subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
print(f"assembled {len(segs)} segments -> {out} ({float(dur):.1f}s)")
