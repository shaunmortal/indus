"""Does ICONOGRAPHY (animal) predict seal size, controlling for text length? And does G741's effect survive controlling for animal too?"""
import csv, json, collections, random, statistics as st
exec(open('analysis/size1.py').read().split("# text length vs area")[0])
for r in sq: r['seq']=r['seq'][::-1]
random.seed(4)
def strat_perm(items,has,keyf,n_perm=3000):
    strata=collections.defaultdict(list)
    for i,r in enumerate(items): strata[keyf(r)].append(i)
    strata={k:v for k,v in strata.items() if len(v)>=5}
    keep=[i for v in strata.values() for i in v]
    med={k:st.median(items[i]['area'] for i in v) for k,v in strata.items()}
    resid={i:items[i]['area']-med[keyf(items[i])] for i in keep}
    w=[i for i in keep if has(items[i])]; wo=[i for i in keep if not has(items[i])]
    if len(w)<10 or len(wo)<10: return None
    obs=st.mean(resid[i] for i in w)-st.mean(resid[i] for i in wo); cnt=0
    for _ in range(n_perm):
        ph=set()
        for k,idx in strata.items():
            m=sum(1 for i in idx if has(items[i])); ph.update(random.sample(idx,m))
        d=st.mean(resid[i] for i in ph)-st.mean(resid[i] for i in keep if i not in ph)
        if abs(d)>=abs(obs): cnt+=1
    return len(w),obs,cnt/n_perm
fam=lambda r: (r['icon'].split(':')[0] or 'none')
print("iconography families:",collections.Counter(fam(r) for r in sq).most_common(8))
print("\nanimal vs area, site x length controlled:")
for a in ['Bull1','Bull2','Gaur','Zebu','Elephant','Rhino','Buffalo','Tiger','none']:
    res=strat_perm(sq,lambda r,a=a:fam(r)==a,lambda r:(r['site'],min(len(r['seq']),8)))
    if res: print(f"  {a:9} n={res[0]:3} delta={res[1]:+7.1f} p={res[2]:.4f}")
print("\nG741 effect controlling for site x length x animal family:")
res=strat_perm(sq,lambda r:741 in r['seq'],lambda r:(r['site'],min(len(r['seq']),8),fam(r)))
print("  n=%d delta=%+.1f p=%.4f"%res if res else "  too few")
print("G390 same control:"); res=strat_perm(sq,lambda r:390 in r['seq'],lambda r:(r['site'],min(len(r['seq']),8),fam(r))); print("  n=%d delta=%+.1f p=%.4f"%res if res else "  too few")
