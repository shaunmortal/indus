"""Seal size vs sign, CONTROLLING for text length: permutation within length strata (shuffle sign presence only among seals with the same text length).
Also report per-sign: median area with vs without, within-length."""
import csv, json, collections, random, statistics as st
exec(open('analysis/size1.py').read().split("# text length vs area")[0])   # reuse loading -> sq
random.seed(2)
L=lambda r: min(len(r['seq']),8)
strata=collections.defaultdict(list)
for i,r in enumerate(sq): strata[L(r)].append(i)
areas=[r['area'] for r in sq]
# residual area = area - median area of its length stratum
med={l:st.median(areas[i] for i in idx) for l,idx in strata.items()}
resid=[areas[i]-med[L(sq[i])] for i in range(len(sq))]
def strat_perm(has,n_perm=4000):
    obs=st.mean(resid[i] for i in range(len(sq)) if has[i])-st.mean(resid[i] for i in range(len(sq)) if not has[i])
    cnt=0
    for _ in range(n_perm):
        ph=[False]*len(sq)
        for l,idx in strata.items():
            k=sum(1 for i in idx if has[i])
            for i in random.sample(idx,k): ph[i]=True
        d=st.mean(resid[i] for i in range(len(sq)) if ph[i])-st.mean(resid[i] for i in range(len(sq)) if not ph[i])
        if abs(d)>=abs(obs): cnt+=1
    return obs,cnt/n_perm
signs=collections.Counter(g for r in sq for g in set(r['seq']))
res=[]
for g,n in signs.items():
    if n<30: continue
    has=[g in r['seq'] for r in sq]
    obs,p=strat_perm(has)
    res.append((p,obs,g,n))
res.sort()
print("length-controlled: signs vs residual seal area (steatite square seals, n=%d), stratified permutation 4000"%len(sq))
print("  sign   n   delta_resid_mm2   p")
for p,obs,g,n in res[:12]: print(f"  G{g:<4} {n:4}   {obs:+8.1f}    {p:.4f}")
print("Bonferroni 0.05/%d = %.4f"%(len(res),0.05/len(res)))
# positional classes: does the FIRST sign or LAST sign class matter? test opener G820/G817/G861 and closer G740 (jar) as groups
for name,grp,pos in [("opener 817/820/861",{817,820,861},0),("jar-final 740",{740},-1),("twins/person-initial 90/91",{90,91},0)]:
    has=[r['seq'][pos] in grp for r in sq]
    if sum(has)>=20:
        obs,p=strat_perm(has,3000); print(f"{name}: n={sum(has)} delta_resid={obs:+.1f} p={p:.4f}")
