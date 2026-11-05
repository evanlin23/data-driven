"""Build an episode: script.md -> lint -> narration (Kokoro) -> timed render spec -> (optional) render.

script.md format: blocks that start with a scene directive, followed by narration lines (one spoken line each).

    @scene textBeat {"text": "*84,302* games on Steam"}
    There are eighty-four thousand games on Steam.
    I scored every single one of them. [pause]

    @scene scatter @ref:scatter_main {"highlight": 1, "callout": "..."}
    ...

- `@ref:NAME` merges props from episode data file `data.json` (key NAME) under the inline JSON.
- A scene lasts exactly as long as its narration lines (+ optional `@hold 1.5` extra seconds).
- Lines starting with `#` are comments.

Usage: python3 pipeline/build_episode.py episodes/001-most-underrated [--render] [--skip-lint]
"""
import json, os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(__file__))
from script_lint import lint  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ep = os.path.abspath(sys.argv[1]); slug = os.path.basename(ep)
flags = set(sys.argv[2:])

def parse(path):
    blocks, cur, pending_chapter = [], None, [None]
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("@chapter"):
            pending_chapter[0] = line[len("@chapter"):].strip(); continue
        if line.startswith("@scene"):
            m = re.match(r"@scene\s+(\w+)((?:\s+@ref:\w+)*)\s*(\{.*\})?\s*$", line)
            if not m: sys.exit(f"bad scene line: {line}")
            cur = {"chapter": pending_chapter[0], "type": m.group(1), "refs": re.findall(r"@ref:(\w+)", m.group(2) or ""),
                   "props": json.loads(m.group(3)) if m.group(3) else {}, "lines": [], "hold": 0.0}
            pending_chapter[0] = None
            blocks.append(cur)
        elif line.startswith("@hold"):
            cur["hold"] = float(line.split()[1])
        else:
            if cur is None: sys.exit("narration before first @scene")
            cur["lines"].append(line.strip())
    return blocks

blocks = parse(os.path.join(ep, "script.md"))
data = json.load(open(os.path.join(ep, "data.json"))) if os.path.exists(os.path.join(ep, "data.json")) else {}
spoken = "\n".join(l for b in blocks for l in b["lines"])

r = lint(spoken)
print(f"lint: {r['words']} words ≈ {r['minutes_at_175wpm']} min | hard {r['hard']} | soft {r['penalty']}")
for i in r["issues"]: print("   ", i)
if not r["passed"] and "--skip-lint" not in flags:
    sys.exit("script failed lint (use --skip-lint only for drafts)")

from voice import say_script  # noqa: E402  (slow import; after lint)
audio_dir = os.path.join(ROOT, "video", "public", "episodes", slug); os.makedirs(audio_dir, exist_ok=True)
lines = [l for b in blocks for l in b["lines"]]
timing = say_script(lines, os.path.join(audio_dir, "narration.wav"))

scenes, li, t_shift, chapters = [], 0, 0.0, []
for b in blocks:
    n = len(b["lines"])
    if n == 0: sys.exit(f"scene {b['type']} has no narration")
    start = timing[li]["start"] + t_shift
    end = timing[li + n - 1]["end"] + t_shift + 0.28
    li += n
    props = {}
    for ref in b["refs"]: props.update(data[ref])
    props.update(b["props"])
    if b.get("chapter"): chapters.append((start, b["chapter"]))
    scenes.append({"type": b["type"], "from": round(start, 3), "dur": round(end - start + b["hold"], 3), "props": props})
    if b["hold"]:
        t_shift += b["hold"]  # NOTE: holds extend visuals only; narration audio is continuous, so keep holds on the last scene

dur = scenes[-1]["from"] + scenes[-1]["dur"] + 0.5
spec = {"fps": 30, "durationSec": round(dur, 2), "audio": f"episodes/{slug}/narration.wav", "scenes": scenes}
spec_path = os.path.join(ROOT, "video", "src", "episodes", f"{slug}.json"); os.makedirs(os.path.dirname(spec_path), exist_ok=True)
json.dump(spec, open(spec_path, "w"), indent=1)
json.dump(timing, open(os.path.join(ep, "timing.json"), "w"), indent=1)
if chapters:
    fmt = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
    chapters[0] = (0.0, chapters[0][1])  # YouTube requires the first chapter at 0:00
    open(os.path.join(ep, "chapters.txt"), "w").write("\n".join(f"{fmt(t)} {c}" for t, c in chapters) + "\n")
    print("chapters:", "; ".join(f"{fmt(t)} {c}" for t, c in chapters))
long = [s for s in scenes if s["dur"] > 14]
print(f"spec: {len(scenes)} scenes, {dur/60:.1f} min -> {spec_path}")
if long: print(f"  note: {len(long)} scenes longer than 14 s (consider splitting): {[round(s['dur']) for s in long]}")

if "--render" in flags:
    out = os.path.join(ROOT, "video", "out", f"{slug}.mp4")
    props_file = os.path.join(audio_dir, "props.json"); json.dump({"spec": spec}, open(props_file, "w"))
    subprocess.run(["npx", "remotion", "render", "src/index.ts", "Episode", out, f"--props={props_file}", "--log=error"],
                   cwd=os.path.join(ROOT, "video"), check=True)
    # loudness-normalise the final mix only (two-pass loudnorm to -14 LUFS), per channel voice settings
    final = out.replace(".mp4", ".final.mp4")
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", out, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(m[m.rfind("{"):m.rfind("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", out, "-c:v", "copy", "-af", af, "-ar", "48000", final], check=True)
    print("rendered:", final)
