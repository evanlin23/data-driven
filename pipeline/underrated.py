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
for tr, te in KFold(5, shuffle=True, random_state=0).split(X):
    mdl = HistGradientBoostingRegressor(loss="quantile", quantile=0.5, max_iter=300, learning_rate=0.05,
                                        min_samples_leaf=80, monotonic_cst=[1, 0, 0], random_state=0)
    mdl.fit(X[tr], y[tr])
    pred[te] = mdl.predict(X[te])
df["expected_n"] = 10 ** pred
df["gap"] = df.expected_n / df.n          # >1 = fewer players than a game this good "should" have
df["pct_rank_quality"] = df.q.rank(pct=True)
n_trained = len(df)
df = df[df.n >= MIN].copy()

os.makedirs("data/derived", exist_ok=True)
out = df.sort_values("gap", ascending=False)
out[["appid", "name", "developer", "publisher", "positive", "negative", "n", "q", "price_usd", "owners",
     "expected_n", "gap", "pct_rank_quality"]].to_csv("data/derived/underrated.csv", index=False)

print(f"trained on {n_trained:,} games (>= {TRAIN_MIN} reviews); candidates {len(df):,} (>= {MIN}) | prior a={a0:.1f} b={b0:.1f} mean={m:.3f}")
print(f"median |log error| (all trained) = {np.median(np.abs(pred - y)):.2f} dex (x{10**np.median(np.abs(pred - y)):.1f})")
top = out[out.q >= 0.93]
print(f"\nTop-rated (>=93% adj.) games, biggest gap between expected and actual reviews ({len(top):,} candidates):")
for _, r in top.head(40).iterrows():
    print(f"  x{r.gap:5.1f}  {r.q:5.1%}  {int(r.n):>7,} rev  exp {int(r.expected_n):>7,}  ${r.price_usd:>5.2f}  {r.appid:>8}  {str(r['name'])[:42]:<42} | {str(r.developer)[:25]}")
