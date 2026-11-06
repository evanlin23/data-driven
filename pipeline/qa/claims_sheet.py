"""List every checkable claim in an episode for the fact-check loop (see .claude/skills/fact-check-loop).

Usage: python3 pipeline/qa/claims_sheet.py episodes/<slug>  > claims.md
Prints, per scene: the on-screen text/numbers (inline props + every numeric field merged from data.json refs) and each
narration sentence that contains a number, a spelled-out number, or a comparative/superlative word. Every line of the
output must be traceable to facts.json / data.json / robustness.json, with the word choice matching the number
("half" means <= 0.5x, "most" means > 50%, "every" means all, ...).
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from script_parse import parse  # noqa: E402

ep = sys.argv[1]
blocks = parse(os.path.join(ep, "script.md"))
data = json.load(open(os.path.join(ep, "data.json"))) if os.path.exists(os.path.join(ep, "data.json")) else {}
NUM = r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|" \
      r"seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|" \
      r"half|third|quarter|twice|percent)\b"
COMP = r"\b(most|least|best|worst|highest|lowest|biggest|smallest|every|all|always|never|only|none|almost|about|" \
       r"around|roughly|nearly|over|under|more|less|fewer|past|same|exact|exactly|first|last|usually|typically)\b"

def scalars(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("points", "values", "trend", "xTicks", "yTicks", "cloud"): continue  # chart geometry
            yield from scalars(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj): yield from scalars(v, f"{path}[{i}]")
    elif isinstance(obj, (int, float, str)) and not (isinstance(obj, str) and obj.endswith((".jpg", ".png"))):
        yield path, obj

for n, b in enumerate(blocks):
    print(f"\n## scene {n}: {b['type']} {' '.join('@' + r for r in b['refs'])}")
    props = {}
    for r in b["refs"]:
        if r not in data: print(f"  !! missing data ref {r}")
        props.update(data.get(r, {}))
    props.update(b["props"])
    for k, v in scalars(props):
        print(f"  screen  {k} = {v}")
    for line in b["lines"]:
        for sent in re.split(r"(?<=[.?!])\s+", line):
            if re.search(NUM, sent, re.I) or re.search(COMP, sent, re.I):
                print(f"  spoken  {sent}")
