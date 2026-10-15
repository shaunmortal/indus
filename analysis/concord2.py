"""Bootstrap the concordance: add accepted pairs, re-align, repeat until no growth. Output data/bridge_WM.json (W -> [M]) with provenance."""
import csv, json, collections
seed={int(k):v for k,v in json.load(open('data/raw/paragorth/data/derived/bridge_extended.json')).items()}
W2M={w:set(ms) for w,ms in seed.items() if ms}
prov={w:'paragorth' for w in W2M}
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
SITE={'Mohenjodaro':'Mohenjo-daro','Harappa':'Harappa','Lothal':'Lothal','Kalibangan':'Kalibangan','Chanhudaro':'Chanhu-daro'}
icit=collections.defaultdict(set)
for r in mc:
    if r['seq']: icit[(r['site'],len(r['seq']))].add(tuple(r['seq']))
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
texts=[]; seen=set()
for r in rows:
    s=r['signs_clean'].strip()
    if s and s not in seen and SITE.get(r['site']):
        seen.add(s); m=[int(t) for t in s.split()]
        if 0 not in m and len(m)>=3: texts.append((SITE[r['site']],m))
for it in range(6):
    M2W=collections.defaultdict(set)
    for w,ms in W2M.items():
        for m in ms: M2W[m].add(w)
    votes=collections.Counter(); matched=0
    for site,m in texts:
        cands=[]
        for w in icit.get((site,len(m)),()):
            ok=True; known=0
            for mi,wi in zip(m,w):
                if wi in W2M:
                    if mi in W2M[wi]: known+=1
                    else: ok=False; break
                elif mi in M2W: ok=False; break
            if ok and known>=2: cands.append(w)
        if len(cands)==1:
            matched+=1
            for mi,wi in zip(m,cands[0]):
                if wi not in W2M: votes[(mi,wi)]+=1
    byw=collections.defaultdict(collections.Counter)
    for (mi,wi),c in votes.items(): byw[wi][mi]+=c
    added=0
    for wi,cnt in byw.items():
        (m1,c1),*_=cnt.most_common(); tot=sum(cnt.values())
        if c1>=3 and c1/tot>=0.8: W2M[wi]={m1}; prov[wi]=f'align-iter{it+1} {c1}/{tot}'; added+=1
    print(f"iter {it+1}: matched texts={matched} new pairs={added} bridge size={len(W2M)}")
    if not added: break
json.dump({str(w):{'M':sorted(ms),'source':prov[w]} for w,ms in sorted(W2M.items())},open('data/bridge_WM.json','w'),indent=0)
print("saved data/bridge_WM.json")
# coverage: share of ICIT tokens whose W sign now has an M mapping
tok=collections.Counter(w for r in mc for w in r['seq'])
cov=sum(c for w,c in tok.items() if w in W2M)/sum(tok.values())
print(f"ICIT token coverage by bridge: {cov:.1%}  (signs mapped {len(W2M)} of {len(tok)} distinct W signs)")
