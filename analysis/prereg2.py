"""Prediction registry v2: adds predictions from F26/F27/F19/F23 computed on the WORK set (hold-out untouched). Frozen with SHA-256."""
import json, collections, hashlib, datetime, random, statistics as st
B='/Users/Happy/Desktop/plugins/indus'
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
cls=json.load(open(f'{B}/data/model1b_consensus_classes.json'))['classes']; OPEN=set(cls['1']); CLOSE=set(cls['0'])
work=json.load(open(f'{B}/data/holdout/work.json'))
W=[(tuple(Wm.get(w,w) for w in r['seq']),r['type'],r['site']) for r in work if r['seq']]
sq=[s for s,t,_ in W if t=='SEAL:S' and len(s)>=3]; rd=[s for s,t,_ in W if t=='SEAL:R' and len(s)>=3]
cnt=collections.Counter(sq); uniq_share=sum(1 for s in sq if cnt[s]==1)/len(sq)
cntr=collections.Counter(rd); uniq_r=sum(1 for s in rd if cntr[s]==1)/len(rd)
# P11: no-inflection: stems with >=2 different finals vs shuffled null, on work set square seals len>=3
def altern(seqs):
    d=collections.defaultdict(set)
    for s in seqs: d[s[:-1]].add(s[-1])
    return sum(1 for v in d.values() if len(v)>=2)
dist=list(set(sq)); obs=altern(dist)
rng=random.Random(1); null=[]
byL=collections.defaultdict(list)
for s in dist: byL[len(s)].append(s)
for _ in range(30):
    S=[]
    for L,ts in byL.items():
        fin=[t[-1] for t in ts]; rng.shuffle(fin); S+=[t[:-1]+(f,) for t,f in zip(ts,fin)]
    null.append(altern(S))
ratio=obs/st.mean(null)
P=[]
P.append(dict(id='P9',scope='new SQUARE seals (>=3 signs), any lot of >=50',stat='share of seals whose text occurs on no other seal in the lot plus the published corpus',predicted=round(uniq_share,3),n_work=len(sq),falsifier='share < 0.80'))
P.append(dict(id='P10',scope='new ROUND seals (>=3 signs), lot of >=20',stat='same uniqueness share',predicted=round(uniq_r,3),n_work=len(rd),falsifier='share < 0.80'))
P.append(dict(id='P11',scope='new square seals, lot of >=100 distinct texts',stat='stems (text minus last sign) attested with >=2 different final signs, as a ratio to the within-length shuffle null',predicted=round(ratio,2),n_work=len(dist),falsifier='ratio >= 1.0 (i.e. alternation at or above chance would indicate inflection-like variation we claim is absent)'))
P.append(dict(id='P12',scope='new square seals with measured faces, lot of >=60 (steatite), within site x length strata',stat='residual face area of seals whose text repeats another seal, minus unique-text seals',predicted='negative (title-like texts on smaller seals); work-set estimate -97 mm2 (-14%)',falsifier='positive difference with p < 0.05 on the new lot'))
P.append(dict(id='P13',scope='new ROUND seals',stat='share without an animal emblem',predicted='>= 0.85 (work set: 346/365 = 0.95 at home sites)',falsifier='share < 0.60'))
reg=json.load(open(f'{B}/prereg/predictions-1.json'))
reg2={'frozen':datetime.date.today().isoformat(),'supersedes':'predictions-1 (kept; P1-P8 unchanged)','author':'Ayush Kumar (India), with Claude','basis':'work set only; hold-out untouched','predictions':reg['predictions']+P}
js=json.dumps(reg2,indent=1,sort_keys=True); open(f'{B}/prereg/predictions-2.json','w').write(js)
h=hashlib.sha256(js.encode()).hexdigest(); open(f'{B}/prereg/predictions-2.sha256','w').write(h+'  predictions-2.json\n')
for p in P: print(p['id'],p['stat'][:70],'->',p['predicted'])
print('SHA-256',h)
