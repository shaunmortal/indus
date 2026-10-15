"""Are repeated (title-like) seal texts on smaller or larger seals than unique (name-like) texts? Site x length strata, permutation."""
import csv, json, collections, random, statistics as st
exec(open('analysis/size1.py').read().split("# text length vs area")[0])
for r in sq: r['seq']=r['seq'][::-1]
Wm={int(k):v for k,v in json.load(open('data/model5_merges_wells_v3.json')).items()}
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
cnt=collections.Counter(tuple(Wm.get(w,w) for w in r['seq']) for r in mc if r['type']=='SEAL:S' and r['seq'])
for r in sq: r['mult']=cnt.get(tuple(Wm.get(w,w) for w in r['seq']),1)
random.seed(8)
key=lambda r:(r['site'],min(len(r['seq']),8))
strata=collections.defaultdict(list)
for i,r in enumerate(sq): strata[key(r)].append(i)
strata={k:v for k,v in strata.items() if len(v)>=5}; keep=[i for v in strata.values() for i in v]
med={k:st.median(sq[i]['area'] for i in v) for k,v in strata.items()}
resid={i:sq[i]['area']-med[key(sq[i])] for i in keep}
has={i:sq[i]['mult']>=2 for i in keep}
w=[i for i in keep if has[i]]; wo=[i for i in keep if not has[i]]
obs=st.mean(resid[i] for i in w)-st.mean(resid[i] for i in wo); cnt_=0
for _ in range(4000):
    ph=set()
    for k,idx in strata.items():
        m=sum(1 for i in idx if has[i]); ph.update(random.sample(idx,m))
    d=st.mean(resid[i] for i in ph)-st.mean(resid[i] for i in keep if i not in ph)
    if abs(d)>=abs(obs): cnt_+=1
print(f"steatite square seals with dims: {len(keep)}; repeated-text seals: {len(w)}; delta residual area = {obs:+.0f} mm2 ({obs/st.median(sq[i]['area'] for i in keep):+.0%}); perm p={cnt_/4000:.3f}")
