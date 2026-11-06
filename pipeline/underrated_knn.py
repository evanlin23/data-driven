"""Underrated model v2: "games like it" median (k nearest neighbours), replacing the gradient-boosted model whose
5 fold-versions disagreed 2-3x on the very games at the top of the list (ranking by max gap then rewards noise).

Expected reviews for a game = median review count of the K most similar OTHER games:
  - similar rating (logit of shrunk % positive), and
  - released at about the same time (store-page appid rank; replaced by the release-date era where known).
Easy to say on screen: "games released around then with almost the same rating usually got X reviews".

Usage: python3 pipeline/underrated_knn.py [K] [RATING_SCALE] [ERA_SCALE]  -> data/derived/underrated.csv (same columns)
"""
import glob, json, os, sys, datetime as dt
import numpy as np, pandas as pd
from sklearn.neighbors import NearestNeighbors

K = int(sys.argv[1]) if len(sys.argv) > 1 else 150
RS = float(sys.argv[2]) if len(sys.argv) > 2 else 0.15     # logit units ~ +/-1.5 rating points near 97%
ES = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01     # 1% of catalogue in store-page order ~ a few weeks
MIN = 200
rows = {}
for f in glob.glob("data/raw/steamspy/page_*.json"):
    for a in json.load(open(f)).values(): rows[a["appid"]] = a
df = pd.DataFrame(rows.values())
df["n"] = df.positive + df.negative
df = df[(df.n >= 10) & (df.appid >= 220000) & (df.appid < 3000000)].copy().reset_index(drop=True)
df["price_usd"] = pd.to_numeric(df.initialprice, errors="coerce").fillna(0) / 100
raw = (df.positive / df.n)[df.n >= 200]; m, v = raw.mean(), raw.var(); k = m * (1 - m) / v - 1
a0, b0 = m * k, (1 - m) * k
df["q"] = (df.positive + a0) / (df.n + a0 + b0)
df["lq"] = np.log(df.q / (1 - df.q))

# era: appid, moved LATER to the typical new-page appid of its release month when the release date is known
rel = {}
for f in glob.glob("data/raw/store_details/*.json"):
    d = (json.load(open(f)) or {}).get("data") or {}
    s = (d.get("release_date") or {}).get("date", "")
    for fmt in ("%b %d, %Y", "%d %b, %Y", "%B %d, %Y"):
        try: rel[d["steam_appid"]] = dt.datetime.strptime(s, fmt).date(); break
        except Exception: pass
ym = pd.Series({a: d.year * 12 + d.month - 1 for a, d in rel.items()})
def era_appid(mo):
    near = ym[(ym >= mo - 2) & (ym <= mo + 2)]
    return float(np.quantile(near.index.values, 0.8)) if len(near) >= 15 else None
df["era_appid"] = [max(a, era_appid(ym[a]) or a) if a in ym.index else a for a in df.appid]
df["era_source"] = np.where(df.appid.isin(ym.index), "release date", "store page (appid)")
df["release_date"] = df.appid.map(lambda a: str(rel.get(a, "")))
# era coordinate = rank of era_appid within the catalogue's appid distribution (0..1)
sorted_ids = np.sort(df.appid.to_numpy())
df["era_rank"] = np.searchsorted(sorted_ids, df.era_appid.to_numpy()) / len(sorted_ids)

Z = np.column_stack([df.lq / RS, df.era_rank / ES])
nn = NearestNeighbors(n_neighbors=K + 1).fit(Z)
dist, idx = nn.kneighbors(Z)
logn = np.log10(df.n.to_numpy())
exp_log = np.array([np.median(logn[ix[ix != i][:K]]) for i, ix in enumerate(idx)])  # exclude the game itself
df["expected_n"] = 10 ** exp_log
df["gap"] = df.expected_n / df.n
err = np.median(np.abs(exp_log - logn))
print(f"K={K} RS={RS} ES={ES} | games {len(df):,} | typical miss x{10 ** err:.1f} | release-date era for {(df.era_source == 'release date').sum():,}")
os.makedirs("data/derived", exist_ok=True)
df[["appid", "name", "n", "q", "expected_n", "gap"]].to_csv("data/derived/all_scored.csv", index=False)
out = df[df.n >= MIN].sort_values("gap", ascending=False)
out[["appid", "name", "developer", "publisher", "positive", "negative", "n", "q", "price_usd", "owners", "release_date",
     "era_source", "era_appid", "expected_n", "gap"]].to_csv("data/derived/underrated.csv", index=False)
json.dump({"method": "knn-median", "K": K, "rating_scale_logit": RS, "era_scale_rank": ES, "typical_miss_x": round(10 ** err, 2),
           "prior_mean": round(float(m), 3)}, open("data/derived/model_info.json", "w"))
