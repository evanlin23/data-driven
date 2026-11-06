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
# Final order = consensus across 7 model settings (robustness.json): geometric-mean "times short".
# Displayed "times short" and "expected" use that consensus so order and numbers always agree.
R = json.load(open(f"{EP}/robustness.json"))
byname = {r["name"]: r for _, r in fin.iterrows()}
ordered = [c for c in R["consensus"] if c["name"] in byname]
def cgame(c, rank):
    g = game(byname[c["name"]], rank)
    # recompute the geometric mean unrounded (robustness.json stores 2 decimals; 6.55 -> round(.,1) gave 6.5, not 6.6)
    gs = [x["gap"] for v in R["runs"].values() for x in v if x["name"] == c["name"]]
    gm = float(np.exp(np.mean(np.log(gs))))
    g["times_short"] = round(gm + 1e-9, 1); g["times_short_range"] = [c["min"], c["max"]]
    g["expected"] = int(round(g["reviews"] * gm))
    return g
F["top10"] = [cgame(c, i + 1) for i, c in enumerate(ordered[:10])]
F["next5"] = [cgame(c, i + 11) for i, c in enumerate(ordered[10:15])]
F["highest_rated_in_top10"] = max(F["top10"], key=lambda g: g["liked_adj"])["name"]

# Model check: games released in 2015 rated 95-97% (adjusted): median actual vs median model expectation
u["rel"] = u.appid.map(rdate)
band = u[(u.q >= 0.95) & (u.q < 0.97) & u.rel.map(lambda d: d is not None and d.year == 2015)]
F["model_check"] = {"group": "released in 2015, rated 95-97% (adjusted), >=200 reviews, release date known",
                    "n_games": int(len(band)), "median_actual": int(band.n.median()), "median_expected": int(band.expected_n.median())}

# Traits. Underrated-looking group: top-rated (>=93%) games at least 1.5x short of expectation that pass the rules
# the final list uses (2014+, no DLC/software/adult/re-releases) and are NOT known to have launched elsewhere first
# (status "ok" = verified Steam-first, "unverified release history" = not checked yet). Comparison group: random sample
# of Steam games with 300+ reviews, restricted to games released 2014 or later, so both groups cover the same years.
f_all = pd.read_csv("data/derived/finalists.csv")
# Only games really short of expectation (>= 1.5x; store data exists for all but one of them), one per developer.
basic = f_all[f_all.status.isin(["ok", "unverified release history"]) & (f_all.gap >= 1.5)]
top100 = basic.sort_values("gap", ascending=False).drop_duplicates("developer")
F["traits_group"] = {"n": int(len(top100)), "verified_steam_first": int((top100.status == "ok").sum()),
                     "unverified": int((top100.status != "ok").sum())}
sample_all = [int(l) for l in open("data/derived/sample_ids.txt")]
sample = [a for a in sample_all if store(a).get("type") == "game" and (rdate(a) is not None and rdate(a).year >= 2014)]
price = u.set_index("appid").price_usd
sp = price.reindex(sample).dropna()
F["price"] = {"top100_median": float(top100.price_usd.median()), "random_median": float(sp.median()),
              "top100_share_20plus": round(float((top100.price_usd >= 20).mean()), 3),
              "random_share_20plus": round(float((sp >= 20).mean()), 3), "random_n": int(len(sp))}
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
mega = {int(l): rdate(int(l)) for l in open("data/derived/mega_hits_ids.txt")}
def near(ids):
    out = []
    for a in ids:
        d = rdate(int(a))
        if not d or d.year < 2014: continue
        out.append(any(m and abs((m - d).days) <= 7 for k, m in mega.items() if k != int(a)))  # never match itself
    return len(out), round(float(np.mean(out)), 3)
F["timing"] = {"definition": "launched within 7 days of one of the 400 most-reviewed Steam games (other than itself)",
               "random": dict(zip(["n", "share"], near(sample))), "top100": dict(zip(["n", "share"], near(top100.appid)))}
F["robustness"] = "see robustness.json (rank stability across K / rating-scale / era-scale settings)"
# reviews per owner (SteamSpy owner-range midpoints) for the final top 10
ratios = []
for g in F["top10"]:
    lo, hi = [int(x.replace(",", "")) for x in u.set_index("appid").loc[g["appid"], "owners"].split("..")]
    if hi: ratios.append(g["reviews"] / ((lo + hi) / 2))
F["reviews_per_owner_top10"] = {"median": round(float(np.median(ratios)), 4), "min": round(min(ratios), 4), "max": round(max(ratios), 4)}
# release-history checks (Steam-first rule)
H = json.load(open(f"{EP}/release_history.json"))
F["release_history"] = {"checked": len(H), "prior_release": sum(v[0] == "PRIOR" for v in H.values()),
                        "steam_first": sum(v[0] == "STEAM-FIRST" for v in H.values()), "delisted": sum(v[0] == "DELISTED" for v in H.values())}
# how often each of the top two came out #1 across settings
F["top_spot"] = {n: sum(1 for v in R["runs"].values() if v and v[0]["name"] == n) for n in [g["name"] for g in F["top10"][:2]]}
F["settings_count"] = len(R["runs"])
F["verified_pool"] = int(len(fin))
F["share_200plus_at_typical_miss"] = round(float((u.gap >= MI["typical_miss_x"]).mean()), 4)  # games with 200+ reviews this far short
json.dump(F, open(f"{EP}/facts.json", "w"), indent=1, default=str)
print(json.dumps({k: F[k] for k in ["games_scored", "candidates_min200", "model_check", "traits_group", "price", "genres", "categories", "timing", "highest_rated_in_top10"]}, indent=1))
for g in F["top10"] + F["next5"]:
    print(f"#{g['rank']:>2} {g['name'][:30]:<30} {g['liked_adj']:.1%} rev {g['reviews']:>4} exp {g['expected']:>5} x{g['times_short']:<4} ${g['list_price_usd']:<5} mc={g['metacritic']} {g['release']} coll={[h['name'][:18]+' '+str(h['delta_days']) for h in g['collisions']]}")
