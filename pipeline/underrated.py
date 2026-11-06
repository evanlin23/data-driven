"""Underrated-game model.

Question: given how good a game is (player rating) and when it came out, how many players should it have had?
- Reach   = number of Steam reviews (the most precise public popularity signal; ~30-60 sales per review).
- Quality = % positive reviews, Bayesian-shrunk toward the catalogue average (so 20/20 doesn't beat 9,800/10,000).
- Era     = Steam appid (monotone with store-page date; calibrated against 160 release dates).
Model: gradient-boosted median regression  log10(reviews) ~ quality + era, trained on every game with >= MIN reviews,
with 5-fold out-of-fold predictions so no game predicts itself.
Underrated gap = predicted / actual reviews (how many times more players it "should" have had).

Usage: python3 pipeline/underrated.py [min_reviews]  -> data/derived/underrated.csv
"""
import glob, json, os, sys
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold

MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 200   # min reviews to be a *candidate*
TRAIN_MIN = 10  # train on (nearly) everything: training only on >=MIN would truncate the low tail and inflate expectations
rows = {}
for f in glob.glob("data/raw/steamspy/page_*.json"):
    for a in json.load(open(f)).values():
        rows[a["appid"]] = a
df = pd.DataFrame(rows.values())
df["n"] = df.positive + df.negative
df = df[df.n >= TRAIN_MIN].copy()
# Era window: appid >= 220k (~2013+; earlier the only well-reviewed games are famous classics, which skews
# expectations) and < 3.0M (~mid-2025; newer games are still accumulating reviews).
df = df[(df.appid >= 220000) & (df.appid < 3000000)].copy()
df["price_usd"] = pd.to_numeric(df.initialprice, errors="coerce").fillna(0) / 100
df["free"] = (df.price_usd == 0).astype(int)

# Bayesian shrinkage: Beta prior fit by method of moments on raw rates of well-reviewed games
raw = (df.positive / df.n)[df.n >= 200]   # fit prior on well-measured games only
m, v = raw.mean(), raw.var()
k = m * (1 - m) / v - 1
a0, b0 = m * k, (1 - m) * k
df["q"] = (df.positive + a0) / (df.n + a0 + b0)
df["logit_q"] = np.log(df.q / (1 - df.q))
df["log_n"] = np.log10(df.n)

X = df[["logit_q", "appid", "free"]].to_numpy()
y = df.log_n.to_numpy()
pred = np.zeros(len(df))
fold_of = np.zeros(len(df), int); models = []
for k, (tr, te) in enumerate(KFold(5, shuffle=True, random_state=0).split(X)):
    mdl = HistGradientBoostingRegressor(loss="quantile", quantile=0.5, max_iter=300, learning_rate=0.05,
                                        min_samples_leaf=80, monotonic_cst=[1, 0, 0], random_state=0)
    mdl.fit(X[tr], y[tr])
    pred[te] = mdl.predict(X[te]); fold_of[te] = k; models.append(mdl)
df["expected_n_appid_era"] = 10 ** pred

# --- Era by RELEASE DATE where we know it -------------------------------------------------------------------
# appid tracks when the store PAGE was created. Some games (Greenlight era, long early access) launched years
# later, and would be compared with an older, higher-review era (e.g. Gravity Ghost: page 2013, release 2015).
# For games with a known release date, use the appid typical of NEW store pages launching within +/-2 months
# (80th percentile: the sample of dated games is full of old pages released late, so the median skews old),
# and only ever move a game's era LATER (max with its own appid), never earlier.
import datetime as dt
rel = {}
for f in glob.glob("data/raw/store_details/*.json"):
    d = (json.load(open(f)) or {}).get("data") or {}
    s = (d.get("release_date") or {}).get("date", "")
    for fmt in ("%b %d, %Y", "%d %b, %Y", "%B %d, %Y"):
        try: rel[d["steam_appid"]] = dt.datetime.strptime(s, fmt).date(); break
        except Exception: pass
ym = pd.Series({a: d.year * 12 + d.month - 1 for a, d in rel.items()})
def era_appid(m):
    near = ym[(ym >= m - 2) & (ym <= m + 2)]
    return float(np.quantile(near.index.values, 0.8)) if len(near) >= 15 else None
eff = df.appid.map(lambda a: max(a, era_appid(ym[a]) or a) if a in ym.index else None).astype(float)
df["release_date"] = df.appid.map(lambda a: str(rel.get(a, "")))
has = eff.notna().to_numpy()
pred2 = pred.copy()
if has.any():
    X2 = X.copy(); X2[has, 1] = eff[has]
    for k, mdl in enumerate(models):
        idx = has & (fold_of == k)
        if idx.any(): pred2[idx] = mdl.predict(X2[idx])
df["era_source"] = np.where(has, "release date", "store page (appid)")
print(f"era from release date for {has.sum():,} games; from appid for the rest")
df["expected_n"] = 10 ** pred2
df["gap"] = df.expected_n / df.n          # >1 = fewer players than a game this good "should" have
df["pct_rank_quality"] = df.q.rank(pct=True)
n_trained = len(df)
os.makedirs("data/derived", exist_ok=True)
df[["appid", "name", "n", "q", "expected_n", "gap"]].to_csv("data/derived/all_scored.csv", index=False)
df = df[df.n >= MIN].copy()

os.makedirs("data/derived", exist_ok=True)
out = df.sort_values("gap", ascending=False)
out[["appid", "name", "developer", "publisher", "positive", "negative", "n", "q", "price_usd", "owners", "release_date", "era_source", "expected_n_appid_era",
     "expected_n", "gap", "pct_rank_quality"]].to_csv("data/derived/underrated.csv", index=False)

print(f"trained on {n_trained:,} games (>= {TRAIN_MIN} reviews); candidates {len(df):,} (>= {MIN}) | prior a={a0:.1f} b={b0:.1f} mean={m:.3f}")
print(f"median |log error| (all trained) = {np.median(np.abs(pred - y)):.2f} dex (x{10**np.median(np.abs(pred - y)):.1f})")
top = out[out.q >= 0.93]
print(f"\nTop-rated (>=93% adj.) games, biggest gap between expected and actual reviews ({len(top):,} candidates):")
for _, r in top.head(40).iterrows():
    print(f"  x{r.gap:5.1f}  {r.q:5.1%}  {int(r.n):>7,} rev  exp {int(r.expected_n):>7,}  ${r.price_usd:>5.2f}  {r.appid:>8}  {str(r['name'])[:42]:<42} | {str(r.developer)[:25]}")
