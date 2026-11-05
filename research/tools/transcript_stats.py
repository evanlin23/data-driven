"""Parse YouTube auto-caption VTTs and measure pacing. Usage: transcript_stats.py <dir> <cohort_videos.json> <out.json>"""
import re, sys, os, glob, json, statistics
D, COHORT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ratio = {r['id']: r for r in json.load(open(COHORT))}
def ts(s):
    h, m, rest = s.split(':'); return int(h)*3600 + int(m)*60 + float(rest)
def parse(path):
    """Return list of (t, word) from auto-caption VTT (uses <c> word timings when present)."""
    words, last_line = [], None
    txt = open(path, encoding='utf-8', errors='ignore').read()
    for block in txt.split('\n\n'):
        m = re.search(r'(\d\d:\d\d:\d\d\.\d+) --> (\d\d:\d\d:\d\d\.\d+)', block)
        if not m: continue
        start = ts(m.group(1))
        lines = [l for l in block.split('\n')[1:] if l.strip() and '-->' not in l]
        for l in lines:
            if '<' in l:  # word-timed line: first word at cue start, then <00:00:01.234><c> word</c>
                first = re.match(r'^([^<]*)', l).group(1).strip()
                if first: words += [(start, w) for w in first.split()]
                for t, w in re.findall(r'<(\d\d:\d\d:\d\d\.\d+)><c>\s*([^<]*)</c>', l):
                    words += [(ts(t), x) for x in w.split()]
            else:
                clean = re.sub(r'<[^>]+>', '', l).strip()
                if clean and clean != last_line and not any(clean == x for x in ()):
                    pass
                last_line = clean
    if not words:  # manual captions: no word timing; take unique lines
        seen = []
        for block in txt.split('\n\n'):
            m = re.search(r'(\d\d:\d\d:\d\d\.\d+) -->', block)
            if not m: continue
            for l in block.split('\n')[1:]:
                c = re.sub(r'<[^>]+>', '', l).strip()
                if c and '-->' not in c and (not seen or seen[-1][1] != c):
                    seen.append((ts(m.group(1)), c))
        for t, c in seen: words += [(t, w) for w in c.split()]
    return words
files = {}
for p in glob.glob(os.path.join(D, '**', '*.vtt'), recursive=True):
    vid = re.search(r'\[([\w-]{11})\]', p).group(1)
    pref = 0 if '.en-orig.' in p else 1   # original ASR track has word timings
    if vid not in files or pref < files[vid][0]: files[vid] = (pref, p)
rows = []
for vid, (_, p) in files.items():
    w = parse(p)
    if len(w) < 50: continue
    dur = w[-1][0]
    text = ' '.join(x for _, x in w)
    first = lambda s: [x for t, x in w if t < s]
    num_t = next((t for t, x in w if re.search(r'\d', x) or x.lower() in ('million','billion','thousand','hundred','percent')), None)
    you = sum(1 for _, x in w if x.lower().strip(',.?!') in ('you', "you're", 'your'))
    i_ = sum(1 for _, x in w if x.lower().strip(',.?!') in ('i', "i'm", "i've", 'my', 'me'))
    gaps = [b[0]-a[0] for a, b in zip(w, w[1:])]
    pauses = sum(1 for g in gaps if g > 0.7)
    meta = ratio.get(vid, {})
    rows.append(dict(id=vid, ch=meta.get('ch', os.path.basename(p).split(' - ')[0]), title=meta.get('t', os.path.basename(p)),
        x=round(meta.get('r', float('nan')), 2), dur_min=round(dur/60, 1), words=len(w),
        wpm=round(len(w)/(dur/60)), wpm_first60=len(first(60)), words_first30=len(first(30)),
        first_number_s=round(num_t, 1) if num_t is not None else None,
        you_per_1k=round(you*1000/len(w), 1), i_per_1k=round(i_*1000/len(w), 1),
        pauses_per_min=round(pauses/(dur/60), 1), opening=' '.join(first(45))))
json.dump(rows, open(OUT, 'w'), indent=1)
rows.sort(key=lambda r: -(r['x'] if r['x'] == r['x'] else -1))
print(f"{'x':>7} {'min':>5} {'wpm':>4} {'w@60s':>6} {'1st#':>5} {'you':>5} {'I':>5} {'pause/m':>7}  channel | title")
for r in rows:
    print(f"{r['x']:>7} {r['dur_min']:>5} {r['wpm']:>4} {r['wpm_first60']:>6} {str(r['first_number_s']):>5} {r['you_per_1k']:>5} {r['i_per_1k']:>5} {r['pauses_per_min']:>7}  {r['ch'][:18]} | {r['title'][:55]}")
