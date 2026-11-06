"""Every number episode 001 states, computed in one place -> episodes/001-most-underrated/facts.json.
Run after: underrated.py, finalists.py, collisions.py. Nothing in the script may come from anywhere else."""
import json, os, glob, datetime as dt
import numpy as np, pandas as pd

EP = "episodes/001-most-underrated"
u = pd.read_csv("data/derived/underrated.csv")              # candidates >= 200 reviews
allg = pd.read_csv("data/derived/all_scored.csv")
fin = pd.read_csv("data/derived/finalists_ok.csv")           # filtered, one per developer, ranked by gap
coll = json.load(open("data/derived/collisions.json"))

def store(a):
    p = f"data/raw/store_details/{a}.json"
    return ((json.load(open(p)) or {}).get("data") or {}) if os.path.exists(p) else {}
def rdate(a):
    s = (store(a).get("release_date") or {}).get("date", "")
    for fmt in ("%b %d, %Y", "%d %b, %Y", "%B %d, %Y"):
        try: return dt.datetime.strptime(s, fmt).date()
        except ValueError: pass
F = {}
F["games_scored"] = int(len(allg))
F["candidates_min200"] = int(len(u))
MI = json.load(open("data/derived/model_info.json"))
F["model"] = MI  # method, K, scales, typical_miss_x, prior_mean
F["prior_mean_positive"] = MI["prior_mean"]
F["model_typical_miss_x"] = MI["typical_miss_x"]

def game(r, rank):
    d = store(int(r.appid))
    return {"rank": rank, "appid": int(r.appid), "name": r["name"], "developer": r.developer, "release": str(r.release),
            "reviews": int(r.n), "liked_adj": round(float(r.q), 4), "liked_raw": round(float(r.positive / r.n), 4),
            "expected": int(round(r.expected_n)), "times_short": round(float(r.gap), 1),
            "list_price_usd": float(r.price_usd), "metacritic": (d.get("metacritic") or {}).get("score"),
            "short_description": d.get("short_description", ""),
            "collisions": [h for h in coll.get(str(int(r.appid)), {}).get("hits", []) if abs(h["delta_days"]) <= 10][:2]}
F["top10"] = [game(r, i + 1) for i, (_, r) in enumerate(fin.head(10).iterrows())]
F["next5"] = [game(r, i + 11) for i, (_, r) in enumerate(fin.iloc[10:15].iterrows())]
F["highest_rated_in_top10"] = max(F["top10"], key=lambda g: g["liked_adj"])["name"]

# Model check: games released in 2015 rated 95-97% (adjusted): median actual vs median model expectation
u["rel"] = u.appid.map(rdate)
band = u[(u.q >= 0.95) & (u.q < 0.97) & u.rel.map(lambda d: d is not None and d.year == 2015)]
F["model_check"] = {"group": "released in 2015, rated 95-97% (adjusted), >=200 reviews, release date known",
                    "n_games": int(len(band)), "median_actual": int(band.n.median()), "median_expected": int(band.expected_n.median())}

# Traits: top 100 most underrated (status ok, >=93%) vs comparison groups
f_all = pd.read_csv("data/derived/finalists.csv")
# comparison group: the 100 top-rated (>=93%) games most short of expectation that pass the basic rules
# (2014+, no DLC/software/adult/classic re-releases), BEFORE the Steam-first check (which only gates the final list)
basic = f_all[f_all.status.isin(["ok", "unverified release history"]) | f_all.status.str.startswith("released before Steam")]
top100 = basic.sort_values("gap", ascending=False).head(100)
met = u[(u.q >= 0.93) & (u.gap <= 1)]
F["price"] = {"top100_median": float(top100.price_usd.median()), "met_expectations_median": float(met.price_usd.median()),
              "top100_share_20plus": round(float((top100.price_usd >= 20).mean()), 3),
              "met_share_20plus": round(float((met.price_usd >= 20).mean()), 3), "met_n": int(len(met))}
sample = [int(l) for l in open("data/derived/sample_ids.txt")]
def prof(ids):
    g = {}; c = {}; n = 0
    for a in ids:
        d = store(a)
        if not d or d.get("type") != "game": continue
        n += 1
        for x in d.get("genres", []): g[x["description"]] = g.get(x["description"], 0) + 1
        for x in d.get("categories", []): c[x["description"]] = c.get(x["description"], 0) + 1
    return n, {k: round(v / n, 3) for k, v in g.items()}, {k: round(v / n, 3) for k, v in c.items()}
nt, gt, ct = prof(top100.appid); ns, gs, cs = prof(sample)
keys_g = ["Casual", "Strategy", "Simulation", "RPG"]; keys_c = ["Single-player", "Multi-player", "Online PvP"]
F["genres"] = {"underrated_n": nt, "random_n": ns, **{k: [gt.get(k, 0), gs.get(k, 0)] for k in keys_g}}
F["categories"] = {k: [ct.get(k, 0), cs.get(k, 0)] for k in keys_c}
mega = [int(l) for l in open("data/derived/mega_hits_ids.txt")]
md = [d for d in (rdate(a) for a in mega) if d]
def near(ids):
    ds = [d for d in (rdate(a) for a in ids) if d and d.year >= 2014]
    return len(ds), round(float(np.mean([any(abs((m - d).days) <= 7 for m in md) for d in ds])), 3)
F["timing"] = {"definition": "launched within 7 days of one of the 400 most-reviewed Steam games",
               "random": dict(zip(["n", "share"], near(sample))), "top100": dict(zip(["n", "share"], near(top100.appid)))}
F["robustness"] = "see robustness.json (rank stability across K / rating-scale / era-scale settings)"
json.dump(F, open(f"{EP}/facts.json", "w"), indent=1, default=str)
print(json.dumps({k: F[k] for k in ["games_scored", "candidates_min200", "model_check", "price", "genres", "categories", "timing", "highest_rated_in_top10"]}, indent=1))
for g in F["top10"] + F["next5"]:
    print(f"#{g['rank']:>2} {g['name'][:30]:<30} {g['liked_adj']:.1%} rev {g['reviews']:>4} exp {g['expected']:>5} x{g['times_short']:<4} ${g['list_price_usd']:<5} mc={g['metacritic']} {g['release']} coll={[h['name'][:18]+' '+str(h['delta_days']) for h in g['collisions']]}")
