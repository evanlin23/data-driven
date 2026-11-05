"""Fetch the SteamSpy 'all' catalog (1000 apps/page, rate limit ~1 req/min)."""
import json, os, sys, time, urllib.request
OUT = sys.argv[1] if len(sys.argv) > 1 else "data/raw/steamspy"
os.makedirs(OUT, exist_ok=True)
page = 0
while True:
    path = f"{OUT}/page_{page:03d}.json"
    if not os.path.exists(path):
        for attempt in range(5):
            try:
                with urllib.request.urlopen(f"https://steamspy.com/api.php?request=all&page={page}", timeout=90) as r:
                    data = json.load(r)
                break
            except Exception as e:
                print(f"page {page} attempt {attempt}: {e}", flush=True); time.sleep(30 * (attempt + 1))
        else:
            sys.exit(f"giving up on page {page}")
        if not data:
            print(f"page {page} empty -> done", flush=True); break
        json.dump(data, open(path, "w"))
        print(f"page {page}: {len(data)} apps", flush=True)
        time.sleep(61)
    else:
        data = json.load(open(path))
        if not data: break
    page += 1
