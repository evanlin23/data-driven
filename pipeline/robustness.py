"""Rank stability of the final (verified Steam-first) list across model settings -> <episode>/robustness.json.
Re-runs underrated_knn.py + finalists.py per setting, then restores the default."""
import json, subprocess, sys
import pandas as pd

EP = sys.argv[1] if len(sys.argv) > 1 else "episodes/001-most-underrated"
CFGS = [("150", "0.15", "0.01"), ("100", "0.15", "0.01"), ("300", "0.15", "0.01"), ("150", "0.10", "0.01"),
        ("150", "0.25", "0.01"), ("150", "0.15", "0.005"), ("150", "0.15", "0.02")]
runs = {}
for cfg in CFGS:
    subprocess.run(["python3", "-I", "pipeline/underrated_knn.py", *cfg], check=True, capture_output=True)
    subprocess.run(["python3", "-I", "pipeline/finalists.py", f"{EP}/exclusions.json"], check=True, capture_output=True)
    f = pd.read_csv("data/derived/finalists_ok.csv").head(15)
    runs["/".join(cfg)] = [{"name": n, "gap": round(float(g), 2)} for n, g in zip(f.name, f.gap)]
subprocess.run(["python3", "-I", "pipeline/underrated_knn.py", *CFGS[0]], check=True, capture_output=True)
subprocess.run(["python3", "-I", "pipeline/finalists.py", f"{EP}/exclusions.json"], check=True, capture_output=True)
default = [r["name"] for r in runs["/".join(CFGS[0])][:10]]
summary = {}
for name in default:
    ranks = [next((i + 1 for i, r in enumerate(v) if r["name"] == name), None) for v in runs.values()]
    summary[name] = {"ranks": ranks, "best": min(x for x in ranks if x), "worst": max((x or 99) for x in ranks),
                     "in_top10_all": all(x is not None and x <= 10 for x in ranks)}
json.dump({"settings": [list(c) for c in CFGS], "runs": runs, "default_top10": summary}, open(f"{EP}/robustness.json", "w"), indent=1)
for n, s in summary.items():
    print(f"{n[:34]:<34} ranks {s['ranks']}  {'TOP10 in all' if s['in_top10_all'] else ''}")
