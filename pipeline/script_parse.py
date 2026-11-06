"""Parse episodes/<slug>/script.md into scene blocks (shared by build_episode.py and the QA tools)."""
import json, re, sys


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


def spoken_lines(path):
    return [l for b in parse(path) for l in b["lines"]]
