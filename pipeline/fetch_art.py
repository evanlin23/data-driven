"""Download Steam header art for appids into video/public/games/, following redirects and verifying each file
is a real image (a redirect page saved as .jpg breaks the render). Usage: fetch_art.py APPID [APPID ...]"""
import os, sys, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "video", "public", "games")
os.makedirs(OUT, exist_ok=True)
MAGIC = (b"\xff\xd8\xff", b"\x89PNG")

def ok(path):
    try:
        with open(path, "rb") as f:
            return f.read(4).startswith(MAGIC)
    except OSError:
        return False

bad = []
for a in sys.argv[1:]:
    p = os.path.join(OUT, f"{a}_header.jpg")
    if ok(p):
        continue
    for url in (f"https://cdn.akamai.steamstatic.com/steam/apps/{a}/header.jpg",
                f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{a}/header.jpg"):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "data-driven-research/0.1"})
            with urllib.request.urlopen(req, timeout=60) as r:
                open(p, "wb").write(r.read())
            if ok(p):
                break
        except Exception:
            pass
    if not ok(p):
        bad.append(a)
print(f"art ok for {len(sys.argv) - 1 - len(bad)} apps" + (f"; FAILED: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
