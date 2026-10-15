"""Proof protocol rule 2: seal a 30% hold-out of distinct texts, stratified by site x object type, fixed seed.
Writes data/holdout/{work,holdout}.json and holdout.sha256. The hash goes public (git commit / Zenodo) BEFORE any reading is claimed.
Nothing in analysis/ may read holdout.json after this point except the final validator."""
import json, hashlib, random, collections, os
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
seen={}; 
for i,r in enumerate(mc):
    k=tuple(r['seq'])
    if k and k not in seen: seen[k]={'idx':i,'cisi':r['cisi'],'site':r['site'],'type':r['type'],'seq':list(k)}
recs=list(seen.values())
strata=collections.defaultdict(list)
for r in recs: strata[(r['site'],r['type'].split(':')[0])].append(r)
rng=random.Random(20261015)
hold=[]; work=[]
for key,items in sorted(strata.items()):
    items=sorted(items,key=lambda r:r['idx']); rng.shuffle(items)
    n=round(len(items)*0.3)
    hold+=items[:n]; work+=items[n:]
os.makedirs('data/holdout',exist_ok=True)
json.dump(work,open('data/holdout/work.json','w'),indent=0)
hj=json.dumps(sorted(hold,key=lambda r:r['idx']),indent=0,sort_keys=True)
open('data/holdout/holdout.json','w').write(hj)
h=hashlib.sha256(hj.encode()).hexdigest()
open('data/holdout/holdout.sha256','w').write(h+"  holdout.json  sealed 2026-10-15 seed=20261015 stratified site x type 30%\n")
print("distinct texts:",len(recs)," work:",len(work)," holdout:",len(hold))
print("SHA-256 of holdout.json:",h)
print("holdout by site:",collections.Counter(r['site'] for r in hold).most_common(6))
