"""For each finalist, find mega-hits (top-400 most-reviewed Steam games) released within +/-WINDOW days."""
import json, os, sys, datetime as dt
import pandas as pd
WINDOW = int(sys.argv[1]) if len(sys.argv) > 1 else 10
def date(appid):
    p = f"data/raw/store_details/{appid}.json"
    if not os.path.exists(p): return None, None
    d = (json.load(open(p)) or {}).get("data") or {}
    s = (d.get("release_date") or {}).get("date", "")
    for fmt in ("%b %d, %Y", "%d %b, %Y", "%B %d, %Y"):
        try: return dt.datetime.strptime(s, fmt).date(), d.get("name")
        except ValueError: pass
    return None, d.get("name")
scored = pd.read_csv("data/derived/all_scored.csv").set_index("appid")
mega = [int(l) for l in open("data/derived/mega_hits_ids.txt")]
mega_dates = {a: date(a) for a in mega}
have = sum(1 for v in mega_dates.values() if v[0])
print(f"mega-hits with dates: {have}/{len(mega)}")
fin = pd.read_csv("data/derived/finalists_ok.csv").head(14)
out = {}
for _, r in fin.iterrows():
    d0, _ = date(int(r.appid))
    hits = []
    for a, (d, name) in mega_dates.items():
        if d and d0 and abs((d - d0).days) <= WINDOW:
            n = int(scored.loc[a, "n"]) if a in scored.index else None
            hits.append({"appid": a, "name": name, "date": str(d), "delta_days": (d - d0).days, "reviews": n})
    hits.sort(key=lambda h: -(h["reviews"] or 0))
    out[int(r.appid)] = {"name": r["name"], "date": str(d0), "hits": hits}
    print(f"{r['name'][:30]:<30} {d0}  ->  " + "; ".join(f"{h['name'][:28]} ({h['delta_days']:+d}d, {h['reviews']:,} rev)" for h in hits[:3]))
json.dump(out, open("data/derived/collisions.json", "w"), indent=1)
