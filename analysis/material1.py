"""Phase 2C: sign x MATERIAL (steatite vs faience vs clay vs copper) and square vs round seals, ICIT, site x length strata, permutation, Bonferroni."""
import csv, json, collections, random
exec(open('analysis/size1.py').read().split("# text length vs area")[0])
random.seed(31)
bridge={int(k):v['M'] for k,v in json.load(open('data/bridge_WM.json')).items()}
# rows = ICIT seals with dims+text; but material test should use ALL ICIT objects with text, not only those with dims
corp2=[]; seen=set()
for r in corp:
    sid=r['inscription_id'][1:]; s=seals.get(sid)
    if not s: continue
    seq=tuple(int(x[1:]) for x in r['sign_sequence'].split() if x[1:].isdigit())[::-1]
    if not seq: continue
    typ=type_by_cisi.get(s['CISI'] or '','?'); mat=s['MATERIAL'] or '?'
    k=(seq,typ,mat,sites.get(s['SITEID'],'?'))
    if k in seen: continue
    seen.add(k); corp2.append(dict(seq=seq,typ=typ,mat=mat,site=sites.get(s['SITEID'],'?')))
def test(items,labelf,name,min_group=40,min_sign=20,n_perm=2000):
    gc=collections.Counter(labelf(r) for r in items); groups=[g for g,c in gc.items() if c>=min_group and g]
    items=[r for r in items if labelf(r) in groups]
    strata=collections.defaultdict(list)
    for i,r in enumerate(items): strata[(r['site'],min(len(r['seq']),7))].append(i)
    strata={k:v for k,v in strata.items() if len(v)>=5}; keep=[i for v in strata.values() for i in v]
    signs=collections.Counter(w for i in keep for w in set(items[i]['seq']))
    print(f"\n=== {name}: {len(keep)} objects; groups {dict(collections.Counter(labelf(items[i]) for i in keep))}")
    tests=[]
    for g in groups:
        isG={i:labelf(items[i])==g for i in keep}
        for w,n in signs.items():
            if n<min_sign: continue
            has={i:(w in items[i]['seq']) for i in keep}
            obs=sum(1 for i in keep if has[i] and isG[i])
            if obs<5: continue
            cnt=0; exp=0
            for _ in range(n_perm):
                ph=set()
                for k,idx in strata.items():
                    m=sum(1 for i in idx if has[i]); ph.update(random.sample(idx,m))
                d=sum(1 for i in ph if isG[i]); exp+=d
                if d>=obs: cnt+=1
            tests.append((cnt/n_perm,g,w,n,obs,exp/n_perm))
    tests.sort(); bon=0.05/max(1,len(tests))
    print(f"  {len(tests)} tests, Bonferroni {bon:.5f}")
    for p,g,w,n,obs,exp in tests[:8]: print(f"  {'*' if p<bon else ' '} p={p:.4f} {g:10} W{w}(M{bridge.get(w,['?'])[0]}) n={n:3} obs={obs:3} exp={exp:5.1f} ratio={obs/exp:.2f}")
sq=[r for r in corp2 if r['typ'] in ('SEAL:S','SEAL:R')]
test(sq,lambda r:r['mat'],'seal MATERIAL')
test(sq,lambda r:r['typ'],'seal SHAPE square vs round')
tabs=[r for r in corp2 if r['typ'].startswith('TAB')]
test(tabs,lambda r:r['typ'],'tablet type (TAB:B bas-relief / TAB:I incised / TAB:C copper)')
