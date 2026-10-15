"""Extend the M<->W (Mahadevan <-> Wells/ICIT) sign concordance by aligning whole texts.
Seed: paragorth bridge (W -> [M...]). Method: for each IM77 text (site known) find ICIT texts (merged corpus) of the same site
and same length whose seed-mapped signs all agree; if exactly one such match, record every position as an (M,W) vote.
New pairs with >=3 votes and no conflicting majority become bridge candidates. Pure counting, no model."""
import csv, json, collections
bridge={int(k):v for k,v in json.load(open('data/raw/paragorth/data/derived/bridge_extended.json')).items()}
W2M={w:set(ms) for w,ms in bridge.items() if ms}
M2W=collections.defaultdict(set)
for w,ms in W2M.items():
    for m in ms: M2W[m].add(w)
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
SITE={'Mohenjodaro':'Mohenjo-daro','Harappa':'Harappa','Lothal':'Lothal','Kalibangan':'Kalibangan','Chanhudaro':'Chanhu-daro'}
icit=collections.defaultdict(list)
for r in mc:
    if r['seq']: icit[(r['site'],len(r['seq']))].append(tuple(r['seq']))
for k in icit: icit[k]=list(set(icit[k]))
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
votes=collections.Counter(); matched=0; ambiguous=0; nomatch=0; seen=set()
for r in rows:
    s=r['signs_clean'].strip()
    if not s or s in seen: continue
    seen.add(s)
    m=[int(t) for t in s.split()]
    if 0 in m or len(m)<3: continue
    site=SITE.get(r['site'])
    if not site: continue
    cands=[]
    for w in icit.get((site,len(m)),[]):
        ok=True; known=0
        for mi,wi in zip(m,w):
            if wi in W2M:
                if mi in W2M[wi]: known+=1
                else: ok=False; break
            elif mi in M2W: ok=False; break   # M sign known to map elsewhere
        if ok and known>=2: cands.append(w)
    if len(cands)==1:
        matched+=1
        for mi,wi in zip(m,cands[0]):
            if wi not in W2M: votes[(mi,wi)]+=1
    elif len(cands)>1: ambiguous+=1
    else: nomatch+=1
print(f"IM77 distinct texts len>=3: matched uniquely={matched} ambiguous={ambiguous} nomatch={nomatch}")
# consolidate votes: for each W, the M with most votes if it dominates
byw=collections.defaultdict(collections.Counter)
for (mi,wi),c in votes.items(): byw[wi][mi]+=c
new={}
for wi,cnt in byw.items():
    (m1,c1),*rest=cnt.most_common()
    tot=sum(cnt.values())
    if c1>=3 and c1/tot>=0.8: new[wi]=(m1,c1,tot)
print(f"new W->M pairs with >=3 votes and >=80% agreement: {len(new)}  (seed bridge had {len(W2M)})")
for wi,(m1,c1,tot) in sorted(new.items(),key=lambda x:-x[1][1])[:25]: print(f"  W{wi} -> M{m1}  votes {c1}/{tot}")
json.dump({str(w):[m] for w,(m,_,_) in new.items()},open('data/bridge_new_candidates.json','w'),indent=0)
