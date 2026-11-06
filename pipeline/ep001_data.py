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

def pts(df):
    # Display-only jitter (+/-12% reviews, +/-0.8 pt rating): small integer review counts with shrunk ratings otherwise
    # line up into visible curved streaks at the bottom of the chart. The hero dot is never jittered.
    r = np.random.default_rng(11)
    jy = 10 ** r.uniform(-0.05, 0.05, len(df)); jx = r.uniform(-0.008, 0.008, len(df))
    return [{"x": round(float(q + a), 4), "y": round(float(n * b), 1)} for q, n, a, b in zip(df.q, df.n, jx, jy)]
axes = {"xLabel": "positive reviews (adjusted %)", "yLabel": "Steam reviews", "yLog": True,
        "xDomain": [0.35, 1.0], "yDomain": [10, 3000000],
        "xTicks": [{"v": v / 100, "t": f"{v}%"} for v in range(40, 101, 10)],
        "yTicks": [{"v": v, "t": t} for v, t in [(10, "10"), (100, "100"), (1000, "1K"), (10000, "10K"), (100000, "100K"), (1000000, "1M")]]}
D = {}
cloud = allg[allg.n >= 30].sample(2600, random_state=7)  # under ~30 reviews the shrunk ratings fall on visible arcs
D["scatter_cloud"] = {**axes, "points": pts(cloud), "revealSeconds": 2.5}
# hero's era: games with nearly the same launch period (era rank +/- 0.02), and the model's own expectation curve there
er = pd.read_csv("data/derived/era_rank.csv").set_index("appid").era_rank
hero_er = float(er[hero["appid"]])
era_ids = er[(er >= hero_er - 0.02) & (er <= hero_er + 0.02)].index
era = allg[allg.appid.isin(era_ids)]
era_pts = pts(era.sample(min(2000, len(era)), random_state=7))
C = json.load(open("data/derived/model_curves.json"))
key = f"{round(round(hero_er / C['era_rank_step']) * C['era_rank_step'], 3):.3f}"
trend = [{"x": q, "y": v} for q, v in zip(C["q"], C["curves"][key]) if q >= 0.6]
D["scatter_trend"] = {**axes, "points": era_pts, "revealSeconds": 0.6, "trend": trend, "trendAt": 0.8}
hp = {"x": round(hero["liked_adj"], 4), "y": hero["reviews"]}
D["scatter_hero"] = {**axes, "points": era_pts + [hp], "highlight": len(era_pts), "highlightAt": 1.2, "revealSeconds": 0.5,
                     "callout": f"{round(hero['liked_raw'] * 100)}% positive. {hero['reviews']} reviews."}
D["scatter_hero_trend"] = {**D["scatter_hero"], "trend": trend, "trendAt": 0.3, "highlightAt": 0.4,
                           "expected": hero["expected"], "expectedAt": 1.4,
                           "callout": f"{hero['times_short']:.1f}x short"}
for g in top + nxt:
    D[f"card_{g['appid']}"] = {"rank": g["rank"], "title": short(g["name"]), "image": img(g["appid"]), "year": int(g["release"][-4:]),
        "stats": [{"label": "Positive reviews", "value": round(g["liked_raw"], 3), "kind": "pct", "color": "good"},
                  {"label": "Model expected", "value": g["expected"], "color": "gold"},
                  {"label": "Steam reviews", "value": g["reviews"]},
                  {"label": "Times short", "value": g["times_short"], "kind": "x1", "color": "accent"}]}
for g in top + nxt:
    D[f"gap_{g['appid']}"] = {"title": short(g["name"]), "image": img(g["appid"]), "expected": g["expected"],
                              "actual": g["reviews"], "timesShort": g["times_short"], "liked": round(g["liked_raw"], 3)}
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
            "big": [{"title": h["name"].replace("®", "").replace("™", "").replace(" - Episode 1", ""), "image": img(h["appid"]), "day": (d1 - start).days + 1, "reviews": int(h["reviews"])} for h, d1 in zip(hs, ds)]}
byname = {g["appid"]: g for g in top + nxt}
for a, lab in [(415920, "November 2015"), (412670, "December 2015"), (251490, "January 2015")]:
    if byname.get(a, {}).get("collisions"): D[f"collision_{a}"] = collision(byname[a], lab, 2)  # both nearby giants (the script names both)

ro = json.load(open(f"data/raw/histograms/{hero['appid']}.json"))["results"]["rollups"]
bym = {(dt.date.fromtimestamp(x["date"]).year, dt.date.fromtimestamp(x["date"]).month): x["recommendations_up"] + x["recommendations_down"] for x in ro}
(y0, m0), (y1, m1) = min(bym), max(bym)
months = [(y, m) for y in range(y0, y1 + 1) for m in range(1, 13) if (y, m) >= (y0, m0) and (y, m) <= (y1, m1)]
vals = [bym.get(k, 0) for k in months]
D["hero_history"] = {"title": f"{short(hero['name'])}: English reviews per month ({sum(vals)} of its {hero['reviews']})", "values": vals, "yMax": max(vals) * 1.15,
                     "xTicks": [{"i": i, "t": str(y)} for i, (y, mo) in enumerate(months) if mo == 1][::2],
                     "drawSeconds": 3, "color": "gold", "mark": {"i": 0, "text": "launch"}}
# comparison charts straight from facts.json (never hand-typed in the script)
G, Ca = F["genres"], F["categories"]
D["genres_chart"] = {"title": "What kind of games look overlooked?", "aLabel": f"{G['underrated_n']} underrated-looking games", "bLabel": "Popular Steam games (random sample)",
    "rows": [{"label": k, "a": G[k][0], "b": G[k][1]} for k in ["Casual", "Strategy", "Simulation", "RPG"]],
    "note": f"Steam store genres · {G['underrated_n']} games rated 93%+ with 1.5x+ fewer reviews than expected (one per studio, known earlier releases left out) vs a random sample of {G['random_n']} games from 2014 on with 300+ reviews · not matched on rating or year"}
D["players_chart"] = {"title": "Who do you play it with?", "aLabel": f"{G['underrated_n']} underrated-looking games", "bLabel": "Popular Steam games (random sample)",
    "rows": [{"label": k.replace("Multi-player", "Multiplayer"), "a": Ca[k][0], "b": Ca[k][1]} for k in ["Single-player", "Multi-player", "Online PvP"]],
    "note": "Steam store categories · same samples"}
json.dump(D, open(f"{EP}/data.json", "w"))
ids = sorted({g["appid"] for g in top + nxt} | {h["appid"] for g in top + nxt for h in g["collisions"]})
open(f"{EP}/art_ids.txt", "w").write("\n".join(map(str, ids)) + "\n")
print("scene keys:", len(D), "| art ids:", len(ids))
