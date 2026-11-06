"""Scene data for episode 001, built ONLY from facts.json + model outputs (so visuals and narration can't disagree)."""
import json, datetime as dt
import numpy as np, pandas as pd

EP = "episodes/001-most-underrated"
F = json.load(open(f"{EP}/facts.json"))
allg = pd.read_csv("data/derived/all_scored.csv")
img = lambda a: f"games/{int(a)}_header.jpg"
top, nxt = F["top10"], F["next5"]
hero = top[0]
short = lambda n: n.split(" - ")[0].replace(": Farmageddon Party Edition", "").replace(": The Siren`s Call", "")

def pts(df): return [{"x": round(float(q), 4), "y": int(n)} for q, n in zip(df.q, df.n)]
axes = {"xLabel": "players who liked it (adjusted % positive)", "yLabel": "Steam reviews", "yLog": True,
        "xDomain": [0.35, 1.0], "yDomain": [10, 3000000],
        "xTicks": [{"v": v / 100, "t": f"{v}%"} for v in range(40, 101, 10)],
        "yTicks": [{"v": v, "t": t} for v, t in [(10, "10"), (100, "100"), (1000, "1K"), (10000, "10K"), (100000, "100K"), (1000000, "1M")]]}
D = {}
cloud = allg[allg.n >= 10].sample(2600, random_state=7)
D["scatter_cloud"] = {**axes, "points": pts(cloud), "revealSeconds": 2.5}
# hero's era: games whose store pages date from the same period (hero's page ~= its release, Dec 2016)
era = allg[(allg.appid >= 450000) & (allg.appid <= 700000)].copy()
era_pts = pts(era.sample(min(2000, len(era)), random_state=7))
era["qb"] = pd.cut(era.q, np.linspace(0.55, 0.99, 14))
trend = [{"x": round(float(iv.mid), 3), "y": int(g.expected_n.median())} for iv, g in era.groupby("qb", observed=True) if len(g) > 15]
D["scatter_trend"] = {**axes, "points": era_pts, "revealSeconds": 0.6, "trend": trend, "trendAt": 0.8}
hp = {"x": round(hero["liked_adj"], 4), "y": hero["reviews"]}
D["scatter_hero"] = {**axes, "points": era_pts + [hp], "highlight": len(era_pts), "highlightAt": 1.2, "revealSeconds": 0.5,
                     "callout": f"{round(hero['liked_adj'] * 100)}% liked it. {hero['reviews']} reviews."}
D["scatter_hero_trend"] = {**D["scatter_hero"], "trend": trend, "trendAt": 0.3, "highlightAt": 0.4,
                           "callout": f"expected: {int(round(hero['expected'], -2)):,}"}
for g in top + nxt:
    D[f"card_{g['appid']}"] = {"rank": g["rank"], "title": short(g["name"]), "image": img(g["appid"]), "year": int(g["release"][-4:]),
        "stats": [{"label": "Players who liked it", "value": round(g["liked_adj"], 3), "kind": "pct", "color": "good"},
                  {"label": "Model expected", "value": g["expected"], "color": "gold"},
                  {"label": "Steam reviews", "value": g["reviews"]},
                  {"label": "Times short", "value": g["times_short"], "kind": "x1", "color": "accent"}]}
def board(reveal):
    return {"title": "Most underrated on Steam (since 2014)", "focusRank": reveal,
            "rows": [{"rank": g["rank"], "title": short(g["name"]), "image": img(g["appid"]), "value": f"{g['times_short']:.1f}x short",
                      "hidden": g["rank"] < reveal} for g in top]}
for k in range(10, 0, -1): D[f"board_{k}"] = board(k)
D["board_hm"] = {"title": "Just missed the top ten", "focusRank": 0,
                 "rows": [{"rank": g["rank"], "title": short(g["name"]), "image": img(g["appid"]), "value": f"{g['times_short']:.1f}x short"} for g in nxt]}

def collision(g, label, nbig=1):
    d0 = dt.date.fromisoformat(dt.datetime.strptime(g["release"], "%b %d, %Y").date().isoformat())
    hs = g["collisions"][:nbig]; ds = [dt.date.fromisoformat(h["date"]) for h in hs]
    start = min([d0] + ds) - dt.timedelta(days=3)
    return {"dateLabel": label, "daysInWindow": 21,
            "small": {"title": short(g["name"]), "image": img(g["appid"]), "day": (d0 - start).days + 1, "reviews": g["reviews"]},
            "big": [{"title": h["name"], "image": img(h["appid"]), "day": (d1 - start).days + 1, "reviews": int(h["reviews"])} for h, d1 in zip(hs, ds)]}
byname = {g["appid"]: g for g in top + nxt}
for a, lab in [(415920, "November 2015"), (412670, "December 2015"), (251490, "January 2015")]:
    if byname.get(a, {}).get("collisions"): D[f"collision_{a}"] = collision(byname[a], lab)

ro = json.load(open(f"data/raw/histograms/{hero['appid']}.json"))["results"]["rollups"]
vals = [x["recommendations_up"] + x["recommendations_down"] for x in ro]
yrs = [dt.date.fromtimestamp(x["date"]).year for x in ro]
D["hero_history"] = {"title": f"{short(hero['name'])}: English reviews per month", "values": vals, "yMax": 30,
                     "xTicks": [{"i": i, "t": str(y)} for i, y in enumerate(yrs) if i == 0 or y != yrs[i - 1]][::2],
                     "drawSeconds": 3, "color": "gold", "mark": {"i": 0, "text": "launch"}}
json.dump(D, open(f"{EP}/data.json", "w"))
ids = sorted({g["appid"] for g in top + nxt} | {h["appid"] for g in top + nxt for h in g["collisions"]})
open(f"{EP}/art_ids.txt", "w").write("\n".join(map(str, ids)) + "\n")
print("scene keys:", len(D), "| art ids:", len(ids))
