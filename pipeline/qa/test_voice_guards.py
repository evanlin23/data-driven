"""Simulate the narration guards (voice_gemini._check / _say) on an episode's real chunks, without calling Gemini.

Usage: python3 pipeline/qa/test_voice_guards.py episodes/<slug>
Exit 1 if a bad take would be accepted, or clean takes get falsely rejected too often (costs daily requests).
Run it after editing the script (chunk boundaries move) or the guard code.
"""
import os, random, re, sys, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import align, voice_gemini as vg  # noqa: E402
from script_parse import spoken_lines  # noqa: E402

ep = sys.argv[1]
lines = spoken_lines(os.path.join(ep, "script.md"))
clean = [re.sub(r"\s*\[pause(?: [\d.]+)?\]\s*", "... ", l).strip() for l in lines]
chunks = list(vg._chunks(clean))
print(f"{len(lines)} lines -> {len(chunks)} Gemini requests (free tier: 10/day): words per chunk "
      f"{[sum(len(clean[i].split()) for i in c) for c in chunks]}")


def fake(cl, drop=(), half=(), cut_last=None, wps=155 / 60, repeat=None, noise=0.0, seed=0):
    """Word timestamps Whisper would return for a take with the given defect."""
    rnd = random.Random(seed); out, t = [], 0.0
    for li, l in enumerate(cl):
        ws = l.split()
        if cut_last is not None and li == len(cl) - 1: ws = ws[:max(1, int(len(ws) * cut_last))]
        for _ in range(2 if li == repeat else 1):
            for wi, w in enumerate(ws):
                if li in drop or (li in half and wi >= len(ws) // 2): continue
                for tok in align._tok(w):
                    out.append(("zzz" if rnd.random() < noise else tok, t, t + 1 / wps))
                t += 1 / wps
    return out, t


def verdict(cl, words, dur):
    try:
        vg._check(cl, "\n".join(cl), np.zeros(int(dur * 24000), np.float32), words); return "ok"
    except vg.BadChunk:
        return "REJ"


bad_cases = {"last line cut at 30%": {"cut_last": .3}, "middle line skipped": {"drop": (2,)},
             "second half of a line skipped": {"half": (1,)}, "line spoken twice": {"repeat": 1}, "slow 118 wpm": {"wps": 118 / 60}}
fail = False
for name, kw in {"clean": {}, **bad_cases}.items():
    res = []
    for ci, idx in enumerate(chunks):
        cl = [clean[i] for i in idx]
        res.append(verdict(cl, *fake(cl, seed=ci, **kw)))
    want = "ok" if name == "clean" else "REJ"
    bad = [i for i, r in enumerate(res) if r != want]
    fail |= bool(bad)
    print(f"  {name:32s} {'PASS' if not bad else 'FAIL on chunks ' + str(bad)}")

for nz in (0.03, 0.05):
    rej = n = 0
    for seed in range(30):
        for ci, idx in enumerate(chunks):
            cl = [clean[i] for i in idx]; n += 1
            rej += verdict(cl, *fake(cl, noise=nz, seed=seed * 10 + ci)) == "REJ"
    print(f"  clean take, {nz:.0%} ASR noise: false rejects {rej}/{n} ({rej / n:.1%})")
    if nz == 0.03 and rej / n > 0.05: fail = True

# re-take loop: first take of chunk 0 repeats a line -> re-voiced; other chunks cached once
os.environ["TTS_CACHE"] = vg.CACHE = tempfile.mkdtemp()
cur, calls = {}, [0]
def synth(text):
    calls[0] += 1; cl = text.split("\n")
    w, d = fake(cl, repeat=1 if calls[0] == 1 else None); cur["w"] = w
    return np.zeros(int(d * 24000), np.float32)
align.transcribe_words = lambda a: cur["w"]
vg._say(lines, os.path.join(vg.CACHE, "o.wav"), 0.35, "Achird", synth, "m")
ok = calls[0] == len(chunks) + 1
fail |= not ok
print(f"  re-take loop: {calls[0]} requests for {len(chunks)} chunks ({'PASS' if ok else 'FAIL'})")
sys.exit(1 if fail else 0)
