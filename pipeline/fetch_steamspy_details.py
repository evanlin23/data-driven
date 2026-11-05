"""Fetch SteamSpy appdetails (tags, genre, languages) for apps with >= MIN reviews, most-reviewed first.
Re-reads the catalog each pass so it picks up pages fetched later. Rate: ~1 req/s."""
import json, os, sys, time, glob, urllib.request
CAT, OUT, MIN = sys.argv[1], sys.argv[2], int(sys.argv[3])
os.makedirs(OUT, exist_ok=True)
while True:
    apps = {}
    for f in glob.glob(f"{CAT}/page_*.json"):
        for a in json.load(open(f)).values():
            apps[a["appid"]] = a["positive"] + a["negative"]
    todo = sorted((n, i) for i, n in apps.items() if n >= MIN and not os.path.exists(f"{OUT}/{i}.json"))
    todo.reverse()
    if not todo:
        if os.path.exists(f"{CAT}/DONE"): break
        time.sleep(120); continue
    for n, i in todo[:500]:
        try:
            with urllib.request.urlopen(f"https://steamspy.com/api.php?request=appdetails&appid={i}", timeout=60) as r:
                d = json.load(r)
            json.dump(d, open(f"{OUT}/{i}.json", "w"))
        except Exception as e:
            print("err", i, e, flush=True); time.sleep(10)
        time.sleep(1.05)
    print(f"{len(os.listdir(OUT))} details fetched; remaining >= {MIN}: {len(todo) - min(500, len(todo))}", flush=True)
