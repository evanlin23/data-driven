import json,glob,re,statistics,math
rows=[]
for f in glob.glob('*.json'):
    e=[x for x in json.load(open(f))['entries'] if x.get('view_count') and x.get('title')]
    if len(e)<8: continue
    e=e[3:]  # drop 3 newest (views still accruing)
    med=statistics.median(x['view_count'] for x in e)
    for x in e: rows.append(dict(ch=f[:-5],t=x['title'],v=x['view_count'],r=x['view_count']/med,d=x.get('duration') or 0,id=x['id']))
F={
 'first-person "I "':lambda t:bool(re.match(r"^(I|I'm|I've|We)\b",t)),
 'contains a number':lambda t:bool(re.search(r'\d',t)),
 'big number (>=1,000)':lambda t:bool(re.search(r'\d{1,3}(,\d{3})+|\d{4,}|million|billion',t,re.I)) and not re.search(r'\b(19|20)\d\d\b',t),
 'year in title':lambda t:bool(re.search(r'\b(19|20)\d\d\b',t)),
 'model/sim/data words':lambda t:bool(re.search(r'model|simulat|data|analy[sz]|statistic|graph|scraped|math',t,re.I)),
 'superlative (most/best/worst/-est/ever)':lambda t:bool(re.search(r'\b(most|best|worst|greatest|ever|of all time|strongest|unluckiest|luckiest|hardest|biggest)\b',t,re.I)),
 'question mark':lambda t:'?' in t,
 'curiosity/conflict word':lambda t:bool(re.search(r'\b(lie|lying|wrong|truth|actually|really|myth|overrated|underrated|secret|nobody|everyone|insane|broke|problem|why)\b',t,re.I)),
 'ALL-CAPS word':lambda t:bool(re.search(r'\b[A-Z]{3,}\b',t)),
 '"Here\'s / What I found"':lambda t:bool(re.search(r"here's|here is|what i found|what happened",t,re.I)),
 'parentheses/brackets':lambda t:bool(re.search(r'[\(\[]',t)),
 'title <= 50 chars':lambda t:len(t)<=50,
}
print(f"n={len(rows)} videos, {len(set(r['ch'] for r in rows))} channels\n")
print(f"{'feature':<42}{'n_with':>7}{'median x (with)':>17}{'median x (without)':>20}")
for k,fn in F.items():
    a=[r['r'] for r in rows if fn(r['t'])]; b=[r['r'] for r in rows if not fn(r['t'])]
    if len(a)<10 or len(b)<10: continue
    print(f"{k:<42}{len(a):>7}{statistics.median(a):>17.2f}{statistics.median(b):>20.2f}")
print("\nduration buckets:")
for lo,hi in [(0,300),(300,600),(600,900),(900,1200),(1200,1800),(1800,99999)]:
    a=[r['r'] for r in rows if lo<=r['d']<hi]
    if a: print(f"  {lo//60:>3}-{hi//60 if hi<99999 else '+':>4} min  n={len(a):>4}  median x={statistics.median(a):.2f}  share>=2x={sum(1 for x in a if x>=2)/len(a):.0%}")
json.dump(rows,open('../rows.json','w'))
print("\nTop outliers (>=3x channel median):")
for r in sorted(rows,key=lambda r:-r['r'])[:45]:
    print(f"  {r['r']:>6.1f}x {r['v']:>10,} {r['ch'][:22]:<22} {r['t'][:85]}")
