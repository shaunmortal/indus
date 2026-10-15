"""Sign x ANIMAL association on ICIT seals, with site x text-length stratified permutation (Fisher-style), Bonferroni.
paragorth reported no sign-emblem pair in Mahadevan's coding; ICIT iconography is finer (1622 entries). Test the claim independently."""
import csv, json, collections, random
exec(open('analysis/size1.py').read().split("# text length vs area")[0])
random.seed(6)
seals_all=[r for r in rows if r['obj'] in ('SEAL:S','SEAL:R') and r['icon']]
for r in seals_all: r['seq']=r['seq'][::-1]
fam=lambda r: r['icon'].split(':')[0]
famc=collections.Counter(fam(r) for r in seals_all); print("seals with animal:",len(seals_all),famc.most_common(10))
key=lambda r:(r['site'],min(len(r['seq']),7))
strata=collections.defaultdict(list)
for i,r in enumerate(seals_all): strata[key(r)].append(i)
strata={k:v for k,v in strata.items() if len(v)>=5}; keep=[i for v in strata.values() for i in v]
signs=collections.Counter(g for i in keep for g in set(seals_all[i]['seq']))
animals=[a for a,c in famc.items() if c>=20 and a!='Bull1']   # test the rarer animals; unicorn is the default
tests=[]
for a in animals:
    isA={i:fam(seals_all[i])==a for i in keep}; nA=sum(isA.values())
    for g,n in signs.items():
        if n<15: continue
        has={i:(g in seals_all[i]['seq']) for i in keep}
        obs=sum(1 for i in keep if has[i] and isA[i])
        exp=0; cnt=0; N=2000
        for _ in range(N):
            ph=set()
            for k,idx in strata.items():
                m=sum(1 for i in idx if has[i]); ph.update(random.sample(idx,m))
            d=sum(1 for i in ph if isA[i]); exp+=d
            if d>=obs: cnt+=1
        exp/=N
        if obs>=5: tests.append((cnt/N,a,g,n,obs,exp))
tests.sort()
print(f"\n{len(tests)} animal x sign tests (obs>=5); Bonferroni = {0.05/max(1,len(tests)):.5f}")
bridge={int(k):v['M'] for k,v in json.load(open('data/bridge_WM.json')).items()}
print("  p       animal   sign(M)      n_sign  obs_with_animal  expected")
for p,a,g,n,obs,exp in tests[:12]: print(f"  {p:.4f}  {a:8} G{g}(M{bridge.get(g,['?'])[0]})  {n:4}   {obs:3}   {exp:5.1f}")
