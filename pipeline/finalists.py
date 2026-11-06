"""Filter underrated candidates with store details: real games only, no DLC/soundtracks/adult content,
flag re-releases of old games, attach release date/genres/description. -> data/derived/finalists.csv"""
import json, os, re
import pandas as pd
c = pd.read_csv("data/derived/underrated.csv")
c = c[c.q >= 0.93]
rows = []
for _, r in c.iterrows():
    p = f"data/raw/store_details/{int(r.appid)}.json"
    if not os.path.exists(p): continue
    d = (json.load(open(p)) or {}).get("data")
    if not d: rows.append({**r, "status": "store page gone"}); continue
    rd = (d.get("release_date") or {}).get("date", "")
    yr = re.search(r"(19|20)\d\d", rd)
    desc = re.sub(r"<[^>]+>", " ", d.get("about_the_game") or "")
    blob = (d.get("short_description", "") + " " + desc).lower()
    cd = (d.get("content_descriptors") or {}).get("ids") or []
    genres = ", ".join(g["description"] for g in d.get("genres", []))
    status = "ok"
    if d.get("type") != "game": status = f"type={d.get('type')}"
    elif any(i in cd for i in (3, 4)): status = "adult content"
    elif re.search(r"\b(originally released|classic (19|20)\d\d|remaster|re-?release|(199\d|200\d) classic|first released in (19|200))", blob):
        status = "re-release of older game"
    elif re.search(r"\b(19[89]\d|200[0-6])\b", blob) and re.search(r"\b(classic|original|retro|back in)\b", blob):
        status = "possible re-release (check)"
    rows.append({**r, "status": status, "release": rd, "year": int(yr.group(0)) if yr else None, "genres": genres,
                 "short": d.get("short_description", "")[:160], "metacritic": (d.get("metacritic") or {}).get("score")})
f = pd.DataFrame(rows)
import sys
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    ex = {int(k): v for k, v in json.load(open(sys.argv[1])).items() if k.isdigit()}
    f.loc[f.appid.isin(ex), "status"] = f.loc[f.appid.isin(ex), "appid"].map(lambda a: "editorial: " + ex[a])
# Steam user reviews launched Nov 2013: games released earlier missed reviews from their launch window.
f.loc[(f.status == "ok") & (f.year < 2014), "status"] = "released before Steam reviews existed (pre-2014)"
# Steam-first rule: verified release histories (episodes/<ep>/release_history.json). PRIOR = released anywhere before
# Steam (browser/Flash, mobile, Japan, older PC, inside another game) -> excluded; candidates not yet verified are
# marked "unverified" and can't be finalists until checked.
hist_path = os.path.join(os.path.dirname(sys.argv[1]) if len(sys.argv) > 1 else ".", "release_history.json")
if os.path.exists(hist_path):
    H = {int(k): v for k, v in json.load(open(hist_path)).items()}
    for i, r in f.iterrows():
        if r.status != "ok": continue
        verdict = H.get(int(r.appid))
        if verdict is None: f.at[i, "status"] = "unverified release history"
        elif verdict[0] == "PRIOR": f.at[i, "status"] = "released before Steam: " + verdict[1]
f.to_csv("data/derived/finalists.csv", index=False)  # after ALL status rules
ok = f[f.status == "ok"].copy()
ok["one_per_dev"] = ~ok.developer.duplicated()
ok = ok[ok.one_per_dev]
ok.to_csv("data/derived/finalists_ok.csv", index=False)
print(f"checked {len(f)} | ok {len(ok)} | excluded: {f[f.status != 'ok'].status.value_counts().to_dict()}")
for _, r in ok.head(30).iterrows():
    print(f"x{r.gap:5.1f} {r.q:5.1%} {int(r.n):>6,}rev exp{int(r.expected_n):>7,} {str(r.release):>13} mc={r.metacritic if r.metacritic==r.metacritic else '-':>4} {str(r['name'])[:34]:<34} | {r.genres[:30]}")
