"""Assemble chart/scene data for episode 001 (most underrated game on Steam) from pipeline outputs."""
import json, datetime as dt
import numpy as np, pandas as pd
EP = "episodes/001-most-underrated"
allg = pd.read_csv("data/derived/all_scored.csv")
fin15 = pd.read_csv("data/derived/finalists_ok.csv").head(15).reset_index(drop=True)
fin = fin15.head(10)
coll = json.load(open("data/derived/collisions.json"))
rng = np.random.default_rng(7)
cloud = allg[allg.n >= 10].sample(2600, random_state=7)
img = lambda a: f"games/{int(a)}_header.jpg"
gg = fin.iloc[0]

def pts(df):
    return [{"x": round(float(q), 4), "y": int(n)} for q, n in zip(df.q, df.n)]
cloud_pts = pts(cloud)
# model's expectation curve: median expected reviews by quality bin
bins = np.linspace(0.35, 0.99, 30)
allg["qb"] = pd.cut(allg.q, bins)
trend = [{"x": round(float(iv.mid), 3), "y": int(g.expected_n.median())} for iv, g in allg.groupby("qb", observed=True) if len(g) > 30]
axes = {"xLabel": "players who liked it (adjusted % positive)", "yLabel": "Steam reviews", "yLog": True,
        "xDomain": [0.35, 1.0], "yDomain": [10, 3000000],
        "xTicks": [{"v": v / 100, "t": f"{v}%"} for v in range(40, 101, 10)],
        "yTicks": [{"v": v, "t": t} for v, t in [(10, "10"), (100, "100"), (1000, "1K"), (10000, "10K"), (100000, "100K"), (1000000, "1M")]]}
D = {}
D["scatter_cloud"] = {**axes, "points": cloud_pts, "revealSeconds": 2.5}
D["scatter_trend"] = {**axes, "points": cloud_pts, "revealSeconds": 0.6, "trend": trend, "trendAt": 0.8}
D["scatter_gg"] = {**axes, "points": cloud_pts + [{"x": round(float(gg.q), 4), "y": int(gg.n)}], "highlight": len(cloud_pts),
                   "highlightAt": 1.2, "revealSeconds": 0.5, "callout": f"{gg.q:.0%} liked it. {int(gg.n)} reviews."}
D["scatter_gg_trend"] = {**D["scatter_gg"], "trend": trend, "trendAt": 0.3, "highlightAt": 0.4, "callout": f"expected: {int(round(gg.expected_n, -2)):,}"}
for i, r in fin.iterrows():
    rank = 10 - i if i else 1  # fin is sorted by gap: row0 = #1
for i, r in fin15.iterrows():
    D[f"card_{int(r.appid)}"] = {"rank": i + 1, "title": r["name"].split(" - ")[0], "image": img(r.appid), "year": int(r.year),
        "stats": [{"label": "Steam reviews", "value": int(r.n)},
                  {"label": "Players who liked it", "value": round(float(r.q), 3), "kind": "pct", "color": "good"},
                  {"label": "Model expected", "value": int(round(r.expected_n, -1)), "color": "gold"},
                  {"label": "Times short", "value": round(float(r.gap), 1), "color": "accent"}]}
def board(revealed_upto):
    rows = []
    for i, r in fin.iterrows():
        rank = i + 1
        rows.append({"rank": rank, "title": r["name"].split(" - ")[0], "image": img(r.appid), "value": f"{r.gap:.1f}x short",
                     "hidden": rank < revealed_upto})
    return {"title": "Most underrated on Steam (since 2014)", "rows": rows, "focusRank": revealed_upto}
for k in range(10, 0, -1): D[f"board_{k}"] = board(k)
# launch collisions
def collision(appid, label):
    c = coll[str(int(appid))]; d0 = dt.date.fromisoformat(c["date"]); h = c["hits"][0]; d1 = dt.date.fromisoformat(h["date"])
    start = min(d0, d1) - dt.timedelta(days=3)
    small = fin15[fin15.appid == appid].iloc[0]
    return {"dateLabel": label, "daysInWindow": 21,
            "small": {"title": small["name"], "image": img(appid), "day": (d0 - start).days + 1, "reviews": int(small.n)},
            "big": [{"title": h["name"], "image": f"games/{h['appid']}_header.jpg", "day": (d1 - start).days + 1, "reviews": int(h["reviews"])}]}
for a, lab in [(251490, "January 2015"), (344480, "May 2015"), (412670, "December 2015"), (333260, "December 2014"), (415920, "November 2015")]:
    if coll.get(str(a), {}).get("hits"): D[f"collision_{a}"] = collision(a, lab)
# Gravity Ghost lifetime review history (shape only: English-language reviews by month)
ro = json.load(open("data/raw/histograms/251490.json"))["results"]["rollups"]
vals = [x["recommendations_up"] + x["recommendations_down"] for x in ro]
yrs = [dt.date.fromtimestamp(x["date"]).year for x in ro]
ticks = [{"i": i, "t": str(y)} for i, y in enumerate(yrs) if i == 0 or y != yrs[i - 1]][::2]
D["gg_history"] = {"title": "Gravity Ghost: reviews per month", "values": vals, "xTicks": ticks, "drawSeconds": 3, "color": "gold",
                   "mark": {"i": 0, "text": "launch week"}}
D["board_hm"] = {"title": "Honorable mentions", "rows": [{"rank": i + 1, "title": r["name"].split(" - ")[0].split(":")[0] if len(r["name"]) > 34 else r["name"],
                  "image": img(r.appid), "value": f"{r.gap:.1f}x short"} for i, r in fin15.iterrows() if i >= 10], "focusRank": 0}
json.dump(D, open(f"{EP}/data.json", "w"))
facts = {"games_scored": int(len(allg)), "candidates": int((allg.n >= 200).sum()), "finalists": fin[["appid", "name", "n", "q", "expected_n", "gap", "release", "developer"]].to_dict("records"),
         "collisions": {k: v for k, v in coll.items() if v["hits"]}}
json.dump(facts, open(f"{EP}/facts.json", "w"), indent=1, default=str)
print("scenes data keys:", len(D), "| games scored:", facts["games_scored"], "| candidates:", facts["candidates"])
for h in [c for c in coll.values() if c["hits"]]:
    for x in h["hits"][:1]:
        print("collision:", h["name"], "vs", x["name"], x["delta_days"], "days")
