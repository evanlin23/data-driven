"""Fetch Steam store appdetails (release date, genres, description, metacritic, images) for a list of appids.
Usage: fetch_store_details.py ids.txt out_dir   (throttled ~1 req/1.6s to respect store rate limits)"""
import json, os, sys, time, urllib.request
ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for i in ids:
    p = f"{out}/{i}.json"
    if os.path.exists(p): continue
    for attempt in range(3):
        try:
            req = urllib.request.Request(f"https://store.steampowered.com/api/appdetails?appids={i}&cc=us&l=en",
                                         headers={"User-Agent": "data-driven-research/0.1"})
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
            json.dump(d.get(str(i), {}), open(p, "w")); break
        except Exception as e:
            print("err", i, e, flush=True); time.sleep(30 * (attempt + 1))
    time.sleep(1.6)
print("done", len(os.listdir(out)))
