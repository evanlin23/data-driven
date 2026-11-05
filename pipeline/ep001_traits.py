"""What do underrated games have in common? Launch timing vs mega-hits, release month, price.
Compares the 100 most-underrated top-rated games with a random sample of games (store dates fetched for both)."""
import json, os, datetime as dt
import numpy as np, pandas as pd

def date(a):
    p = f"data/raw/store_details/{a}.json"
    if not os.path.exists(p): return None
    d = (json.load(open(p)) or {}).get("data") or {}
    s = (d.get("release_date") or {}).get("date", "")
    for fmt in ("%b %d, %Y", "%d %b, %Y", "%B %d, %Y"):
        try: return dt.datetime.strptime(s, fmt).date()
        except ValueError: pass
    return None

mega = [int(l) for l in open("data/derived/mega_hits_ids.txt")]
md = sorted(d for d in (date(a) for a in mega) if d)
print(f"mega-hit dates known: {len(md)}/{len(mega)}")

def near_mega(d, days=7):
    return any(abs((m - d).days) <= days for m in md)

u = pd.read_csv("data/derived/underrated.csv")
top = u[u.q >= 0.93].sort_values("gap", ascending=False).head(100)
sample = [int(l) for l in open(os.environ.get("SAMPLE_IDS", "data/derived/sample_ids.txt"))]
groups = {"top-100 underrated": list(top.appid), "random games (>=300 reviews)": sample}
res = {}
for name, ids in groups.items():
    ds = [d for d in (date(a) for a in ids) if d and d.year >= 2014]
    if not ds: continue
    near = np.mean([near_mega(d) for d in ds])
    dec = np.mean([d.month in (10, 11, 12) for d in ds])
    res[name] = {"n": len(ds), "within_7d_of_mega_hit": round(float(near), 3), "oct_dec_launch": round(float(dec), 3)}
    print(f"{name:<30} n={len(ds):>3} | launched within 7 days of a top-400 hit: {near:5.1%} | Oct-Dec launch: {dec:5.1%}")
json.dump(res, open("episodes/001-most-underrated/traits.json", "w"), indent=1)
