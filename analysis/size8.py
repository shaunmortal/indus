"""Does multiplicity explain the M343 (W741) small-seal effect? Rerun F12 restricted to UNIQUE-text seals, and with multiplicity as an extra stratum."""
import csv, json, collections, random, statistics as st
exec(open('analysis/size1.py').read().split("# text length vs area")[0])
for r in sq: r['seq']=r['seq'][::-1]
Wm={int(k):v for k,v in json.load(open('data/model5_merges_wells_v3.json')).items()}
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
cnt=collections.Counter(tuple(Wm.get(w,w) for w in r['seq']) for r in mc if r['type']=='SEAL:S' and r['seq'])
for r in sq: r['mult']=cnt.get(tuple(Wm.get(w,w) for w in r['seq']),1)
def test(items,keyf,has,n_perm=4000):
    random.seed(13); strata=collections.defaultdict(list)
    for i,r in enumerate(items): strata[keyf(r)].append(i)
    strata={k:v for k,v in strata.items() if len(v)>=5}; keep=[i for v in strata.values() for i in v]
    med={k:st.median(items[i]['area'] for i in v) for k,v in strata.items()}
    resid={i:items[i]['area']-med[keyf(items[i])] for i in keep}
    w=[i for i in keep if has(items[i])]; wo=[i for i in keep if not has(items[i])]
    obs=st.mean(resid[i] for i in w)-st.mean(resid[i] for i in wo); c=0
    for _ in range(n_perm):
        ph=set()
        for k,idx in strata.items():
            m=sum(1 for i in idx if has(items[i])); ph.update(random.sample(idx,m))
        d=st.mean(resid[i] for i in ph)-st.mean(resid[i] for i in keep if i not in ph)
        if abs(d)>=abs(obs): c+=1
    return len(keep),len(w),obs,c/n_perm
uniq=[r for r in sq if r['mult']==1]
n,k,obs,p=test(uniq,lambda r:(r['site'],min(len(r['seq']),8)),lambda r:741 in r['seq'])
print(f"UNIQUE-text seals only: n={n}, with M343={k}, delta={obs:+.0f} mm2, p={p:.4f}")
n,k,obs,p=test(sq,lambda r:(r['site'],min(len(r['seq']),8),r['mult']>=2),lambda r:741 in r['seq'])
print(f"ALL seals, strata site x length x multiplicity: n={n}, with M343={k}, delta={obs:+.0f} mm2, p={p:.4f}")
