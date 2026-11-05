import re,json,sys,urllib.parse,subprocess,statistics,concurrent.futures as cf
def walk(o,key):
    if isinstance(o,dict):
        for k,v in o.items():
            if k==key: yield v
            yield from walk(v,key)
    elif isinstance(o,list):
        for x in o: yield from walk(x,key)
def num(s):
    s=s.replace(',','').split(' ')[0]
    return int(s) if s.isdigit() else 0
def age_days(p):
    m=re.search(r'(\d+)\s*(mo|y|w|d|h|min|s)',p or '')
    if not m: return None
    n=int(m.group(1)); u=m.group(2)
    return n*{'s':0,'min':0,'h':0,'d':1,'w':7,'mo':30,'y':365}[u]
FMT=re.compile(r'\b(model|analy[sz]ed|data|simulat|statistic|stats|ranked every|every single|math|numbers|algorithm|spreadsheet|i measured|i tracked|i graphed|i calculated)',re.I)
def search(q):
    url='https://www.youtube.com/results?search_query='+urllib.parse.quote(q)
    h=subprocess.run(['curl','-sS','-L','-m','30','-A','Mozilla/5.0','-H','Accept-Language: en-US','-b','CONSENT=YES+1',url],capture_output=True,text=True).stdout
    m=re.search(r'var ytInitialData = (\{.*?\});</script>',h,re.S)
    if not m: return q,[]
    d=json.loads(m.group(1)); rows=[]
    for v in walk(d,'videoRenderer'):
        rows.append(dict(t=v['title']['runs'][0]['text'],ch=v.get('ownerText',{}).get('runs',[{}])[0].get('text',''),
          v=num(v.get('viewCountText',{}).get('simpleText','0')),age=age_days(v.get('publishedTimeText',{}).get('simpleText',''))))
    return q,rows[:20]
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
out={}
with cf.ThreadPoolExecutor(6) as ex:
    for q,rows in ex.map(search,qs): out[q]=rows
json.dump(out,open(sys.argv[2],'w'))
print(f"{'query':<52}{'fmt#':>5}{'fmtMed':>9}{'fmtMax':>10}{'fmtChans':>9}{'fmt<1y':>7}{'allMed':>9}")
for q,rows in out.items():
    f=[r for r in rows if FMT.search(r['t'])]
    fv=[r['v'] for r in f]; av=[r['v'] for r in rows]
    rec=sum(1 for r in f if r['age'] is not None and r['age']<365)
    print(f"{q[:51]:<52}{len(f):>5}{int(statistics.median(fv)) if fv else 0:>9,}{max(fv) if fv else 0:>10,}{len(set(r['ch'] for r in f)):>9}{rec:>7}{int(statistics.median(av)) if av else 0:>9,}")

if len(sys.argv)>3:
  for q,rows in out.items():
    f=sorted([r for r in rows if FMT.search(r['t'])],key=lambda r:-r['v'])[:int(sys.argv[3])]
    print('##',q)
    for r in f: print(f"   {r['v']:>10,} {str(r['age'])+'d':>6} {r['ch'][:22]:<22} {r['t'][:80]}")
