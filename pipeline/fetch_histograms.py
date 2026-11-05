"""Fetch Steam monthly review histograms (lifetime positive/negative per month). Usage: fetch_histograms.py ids.txt out_dir"""
import json, os, sys, time, urllib.request
ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for i in ids:
    p = f"{out}/{i}.json"
    if os.path.exists(p): continue
    try:
        req = urllib.request.Request(f"https://store.steampowered.com/appreviewhistogram/{i}?l=english&review_score_preference=0",
                                     headers={"User-Agent": "data-driven-research/0.1"})
        with urllib.request.urlopen(req, timeout=60) as r:
            json.dump(json.load(r), open(p, "w"))
    except Exception as e:
        print("err", i, e, flush=True); time.sleep(10)
    time.sleep(0.8)
print("done", len(os.listdir(out)))
