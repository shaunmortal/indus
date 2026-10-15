"""Seal size vs sign, controlling for SITE x TEXT LENGTH (stratified permutation). Sequences reversed to reading order."""
import csv, json, collections, random, statistics as st
exec(open('analysis/size1.py').read().split("# text length vs area")[0])
for r in sq: r['seq']=r['seq'][::-1]
random.seed(3)
key=lambda r:(r['site'],min(len(r['seq']),8))
strata=collections.defaultdict(list)
for i,r in enumerate(sq): strata[key(r)].append(i)
strata={k:v for k,v in strata.items() if len(v)>=5}
keep=sorted(i for v in strata.values() for i in v)
areas={i:sq[i]['area'] for i in keep}
med={k:st.median(areas[i] for i in v) for k,v in strata.items()}
resid={i:areas[i]-med[key(sq[i])] for i in keep}
print("sites:",collections.Counter(sq[i]['site'] for i in keep).most_common(4)," median area MD vs H:",
      st.median(areas[i] for i in keep if sq[i]['site']=='Mohenjo-daro'),st.median(areas[i] for i in keep if sq[i]['site']=='Harappa'))
def strat_perm(has,n_perm=4000):
    w=[i for i in keep if has[i]]; wo=[i for i in keep if not has[i]]
    obs=st.mean(resid[i] for i in w)-st.mean(resid[i] for i in wo); cnt=0
    for _ in range(n_perm):
        ph=set()
        for k,idx in strata.items():
            m=sum(1 for i in idx if has[i])
            ph.update(random.sample(idx,m))
        d=st.mean(resid[i] for i in ph)-st.mean(resid[i] for i in keep if i not in ph)
        if abs(d)>=abs(obs): cnt+=1
    return obs,cnt/n_perm
bridge=json.load(open('data/bridge_WM.json')); desc={}
try:
    for w,v in json.load(open('data/raw/paragorth/data/repro/repro/data/bridge.json')).items(): desc[int(w)]=v.get('desc','')
except Exception: pass
signs=collections.Counter(g for i in keep for g in set(sq[i]['seq']))
res=[]
for g,n in signs.items():
    if n<30: continue
    has={i:(g in sq[i]['seq']) for i in keep}
    obs,p=strat_perm(has); res.append((p,obs,g,n))
res.sort()
print("\nsite x length controlled, n=%d seals, %d signs tested, Bonferroni=%.4f"%(len(keep),len(res),0.05/len(res)))
print("  sign   M        n   delta_mm2   p      shape")
for p,obs,g,n in res[:12]:
    m=bridge.get(str(g),{}).get('M',['?']); print(f"  G{g:<4} M{str(m[0]):<5} {n:4}  {obs:+8.1f}  {p:.4f}  {desc.get(g,'')[:45]}")
for name,grp,pos in [("opener 817/820/861 first",{817,820,861},0),("jar 740 last",{740},-1),("person 90/91 first",{90,91},0),("741 last",{741},-1)]:
    has={i:(sq[i]['seq'][pos] in grp) for i in keep}
    if sum(has.values())>=20:
        obs,p=strat_perm(has,3000); print(f"{name}: n={sum(has.values())} delta={obs:+.1f} p={p:.4f}")
