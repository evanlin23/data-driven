"""Render every thumbnail variant in episodes/<slug>/thumbnails/*.json to video/out/<slug>/thumb_<name>.png."""
import glob, os, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ep = os.path.abspath(sys.argv[1]); slug = os.path.basename(ep)
out = os.path.join(ROOT, "video", "out", slug); os.makedirs(out, exist_ok=True)
import json, tempfile
look = json.load(open(os.path.join(ep, "look.json"))) if os.path.exists(os.path.join(ep, "look.json")) else {}
for f in sorted(glob.glob(os.path.join(ep, "thumbnails", "*.json"))):
    if look.get("style"):  # thumbnails wear the episode's look
        props = json.load(open(f)); props.setdefault("style", look["style"])
        f = os.path.join(tempfile.mkdtemp(), os.path.basename(f)); json.dump(props, open(f, "w"))
    name = os.path.splitext(os.path.basename(f))[0]
    dst = os.path.join(out, f"thumb_{name}.png")
    subprocess.run(["npx", "remotion", "still", "src/index.ts", "Thumbnail", dst, f"--props={f}", "--log=error"],
                   cwd=os.path.join(ROOT, "video"), check=True)
    print("thumbnail:", dst)
