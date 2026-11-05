import re,json,sys,urllib.parse,subprocess,concurrent.futures as cf
def walk(o,key):
    if isinstance(o,dict):
        for k,v in o.items():
            if k==key: yield v
            yield from walk(v,key)
    elif isinstance(o,list):
        for x in o: yield from walk(x,key)
FMT=re.compile(r'\b(model|analy[sz]ed|simulat|statistic|i scraped|i measured|i tracked|i graphed|i calculated|i ranked every|data)',re.I)
def num(s):
    s=s.replace(',','').split(' ')[0]; return int(s) if s.isdigit() else 0
def search(q):
    url='https://www.youtube.com/results?search_query='+urllib.parse.quote(q)
    h=subprocess.run(['curl','-sS','-L','-m','30','-A','Mozilla/5.0','-H','Accept-Language: en-US','-b','CONSENT=YES+1',url],capture_output=True,text=True).stdout
    m=re.search(r'var ytInitialData = (\{.*?\});</script>',h,re.S)
    if not m: return []
    out=[]
    for v in walk(json.loads(m.group(1)),'videoRenderer'):
        t=v['title']['runs'][0]['text']; r=v.get('ownerText',{}).get('runs',[{}])[0]
        u=r.get('navigationEndpoint',{}).get('browseEndpoint',{})
        out.append((t,r.get('text'),u.get('canonicalBaseUrl') or ('/channel/'+u.get('browseId','')),num(v.get('viewCountText',{}).get('simpleText','0'))))
    return out
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
chans={}
with cf.ThreadPoolExecutor(6) as ex:
    for res in ex.map(search,qs):
        for t,name,url,v in res:
            if FMT.search(t) and v>=50000:
                chans.setdefault(url,[name,0,[]]); chans[url][1]+=1; chans[url][2].append((v,t))
for url,(n,c,vs) in sorted(chans.items(),key=lambda x:-max(v for v,_ in x[1][2])):
    print(url,'|',n,'|',max(vs)[0],'|',max(vs)[1][:70])
