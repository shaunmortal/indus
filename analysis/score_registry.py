"""Score a NEW lot of inscriptions against the frozen registries (prereg/predictions-1..4). Usage:
  python analysis/score_registry.py LOT.json [--out prereg/results-<name>.md]
LOT.json = list of objects: {"id": str, "seq": [Wells codes in READING order], "type": "SEAL:S"|"SEAL:R"|"TAB:B"|"TAB:I"|"TAB:C"|"POT"|"TAG"|..., "site": str,
  optional "side": 1|2 with "object": str for two-sided objects, optional "animal": str, optional "area_mm2": float}
Transcribe the lot into Wells v3 codes WITHOUT re-reading the registry numbers; then run this once. Output is written whatever it says.
--smoke draws a pseudo-lot from the work set (NOT new data; only checks that the code runs and the stats are computed as registered)."""
import json, sys, math, collections, random
B='/Users/Happy/Desktop/plugins/indus'
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
cl=json.load(open(f'{B}/data/model1b_consensus_classes.json'))['classes']; CLOSER=set(cl['0']); OPENER=set(cl['1'])
SS=json.load(open(f'{B}/data/stroke_signs.json')); SHORTM={int(k):v for k,v in SS['short'].items()}
TALL={31:1,32:2,33:3,34:4,35:5,36:6,37:7}; CUP=700; HJAR={741}; M169={407}; M387={803,806}
work=json.load(open(f'{B}/data/holdout/work.json'))
def norm(seq): return [Wm.get(int(g),int(g)) for g in seq]
def shortval(w): m=bridge.get(w); return SHORTM.get(m) if m else None
# bigram model on the work set, same form as analysis/model2.py (absolute discounting D=0.75, add-0.5 unigram, <unk>)
class Bigram:
    def __init__(s,train):
        s.Vs={w for t in train for w in t}; s.END='</s>'
        s.uni=collections.Counter(w for t in train for w in t); s.uni[s.END]=len(train); s.uni['<unk>']=1; s.N=sum(s.uni.values()); s.VV=len(s.uni)
        s.big=collections.defaultdict(collections.Counter)
        for t in train:
            q=('<s>',)+tuple(t)+(s.END,)
            for i in range(1,len(q)): s.big[q[i-1]][q[i]]+=1
    def p1(s,w): return (s.uni[w]+0.5)/(s.N+0.5*s.VV)
    def p2(s,p,w,D=0.75):
        c=s.big[p]; tot=sum(c.values())
        if not tot: return s.p1(w)
        return max(c[w]-D,0)/tot + (D*len(c)/tot)*s.p1(w)
    def ppl(s,texts):
        ll=0;m=0
        for t in texts:
            q=('<s>',)+tuple(w if w in s.Vs else '<unk>' for w in t)+(s.END,)
            for i in range(1,len(q)): ll+=math.log(s.p2(q[i-1],q[i])); m+=1
        return math.exp(-ll/m) if m else None
MODEL=Bigram([norm(r['seq']) for r in work])
def ppl(texts): return MODEL.ppl(texts)
published={tuple(norm(r['seq'])) for r in work}
def score(lot):
    for o in lot: o['s']=norm(o['seq'])
    sq=[o for o in lot if o['type']=='SEAL:S' and len(o['s'])>=3]; rd=[o for o in lot if o['type']=='SEAL:R' and len(o['s'])>=3]
    seals=[o for o in lot if o['type'].startswith('SEAL')]
    R=[]
    def add(pid,n,value,verdict,note=''): R.append((pid,n,value,verdict,note))
    # P1 P2
    if sq:
        add('P1',len(sq),round(sum(o['s'][-1] in CLOSER for o in sq)/len(sq),3),None,'pred 0.676; falsified < 0.45 on >=20')
        add('P2',len(sq),round(sum(o['s'][0] in OPENER for o in sq)/len(sq),3),None,'pred 0.318; falsified < 0.10 or > 0.50 on >=20')
    # P3 P4 P13 P10 P9
    sqa=[o for o in lot if o['type']=='SEAL:S']; rda=[o for o in lot if o['type']=='SEAL:R']
    if rda and sqa: add('P3',len(rda),{'round':round(sum(any(g in HJAR for g in o['s']) for o in rda)/len(rda),3),'square':round(sum(any(g in HJAR for g in o['s']) for o in sqa)/len(sqa),3)},None,'pred round 0.059 < square 0.157; falsified round >= square on >=15 round')
    if rda:
        add('P4',len(rda),round(sum(any(g in M169|M387 for g in o['s']) for o in rda)/len(rda),3),None,'pred 0.168; falsified < 0.08 on >=15 round')
        if all('animal' in o for o in rda): add('P13',len(rda),round(sum((o.get('animal') in (None,'','none')) for o in rda)/len(rda),3),None,'pred >= 0.85; falsified < 0.60')
    lotseqs=collections.Counter(tuple(o['s']) for o in seals)
    for pid,grp in (('P9',sq),('P10',rd)):
        if grp: add(pid,len(grp),round(sum(lotseqs[tuple(o['s'])]==1 and tuple(o['s']) not in published for o in grp)/len(grp),3),None,'pred 0.955 (P9) / 0.99 (P10); falsified < 0.80')
    # P5 short-stroke values 4-7
    vals=collections.Counter(v for o in lot for g in o['s'] for v in [shortval(g)] if v in (4,5,6,7))
    if sum(vals.values()): 
        t=sum(vals.values()); sh={k:round(vals[k]/t,3) for k in (4,5,6,7)}
        add('P5',t,sh,None,'pred non-monotone, share(7) >= share(5) and (6); falsified if share7 < share5 and share7 < share6 on >=60')
    # P7 perplexity
    texts=[o['s'] for o in lot if len(o['s'])>=1]
    if texts: add('P7',len(texts),round(ppl(texts),1),None,'pred 25-45 per sign; falsified outside 20-60 on >=30 texts. Calibration, out-of-sample 20% of the work set: square seals 33, round 31, moulded tablets 34, incised 30, POTTERY 62 (pottery graffiti fall outside the band already; score P7 on seal and tablet texts)')
    # P14 P15 P16
    def tallshare(grp):
        toks=[TALL[g] for o in grp for g in o['s'] if g in TALL and len(o['s'])>=2 and any(x not in TALL and shortval(x) is None for x in o['s'])]
        return (len(toks), round(sum(v>=4 for v in toks)/len(toks),3)) if toks else (0,None)
    n,v=tallshare([o for o in lot if o['type'].startswith('POT')]); 
    if n: add('P14',n,v,None,'pred 0.098; falsified <= seal share or < 0.06 on >=25 tokens')
    n,v=tallshare(seals)
    if n: add('P15',n,v,None,'pred 0.034; falsified >= 0.12 on >=40 tokens')
    pairs=collections.Counter()
    for o in lot:
        if o['type'].startswith('TAB'):
            s=o['s']
            for i,g in enumerate(s):
                if g in TALL and ((i>0 and s[i-1]==CUP) or (i<len(s)-1 and s[i+1]==CUP)): pairs[TALL[g]]+=1
    if pairs: add('P16',sum(pairs.values()),max(pairs,key=pairs.get),None,'pred modal 3; falsified modal 1 or >=4 on >=15 pairs')
    if pairs:
        t=sum(pairs.values()); add('P17',t,{'value5':round(pairs[5]/t,3),'value1':round(pairs[1]/t,3),'values_2_3_4':round((pairs[2]+pairs[3]+pairs[4])/t,3)},None,'pred value5 0.0, value1 0.115, values 2-4 0.846; falsified on >=20 pairs if value5 >= 0.10 or values 2-4 < 0.60')
    # P6, P8, P12 need side/animal/area fields
    for pid,field in (('P6','side'),('P8','animal'),('P12','area_mm2')):
        if not any(field in o for o in lot): add(pid,0,None,'not scorable','lot lacks field '+field)
    return R
def verdicts(R):
    out=[]
    for pid,n,v,verdict,note in R:
        if verdict: out.append((pid,n,v,verdict,note)); continue
        f='pending (n below the registered minimum or needs judgement)'
        if pid=='P1' and n>=20: f='FALSIFIED' if v<0.45 else 'passed'
        if pid=='P2' and n>=20: f='FALSIFIED' if (v<0.10 or v>0.50) else 'passed'
        if pid=='P3' and n>=15: f='FALSIFIED' if v['round']>=v['square'] else 'passed'
        if pid=='P4' and n>=15: f='FALSIFIED' if v<0.08 else 'passed'
        if pid=='P13': f='FALSIFIED' if v<0.60 else 'passed'
        if pid in('P9','P10') and n>=(50 if pid=='P9' else 20): f='FALSIFIED' if v<0.80 else 'passed'
        if pid=='P5' and n>=60: f='FALSIFIED' if (v[7]<v[5] and v[7]<v[6]) else 'passed'
        if pid=='P7' and n>=30: f='FALSIFIED' if (v<20 or v>60) else 'passed'
        if pid=='P15' and n>=40: f='FALSIFIED' if v>=0.12 else 'passed'
        if pid=='P16' and n>=15: f='FALSIFIED' if (v==1 or v>=4) else 'passed'
        if pid=='P17' and n>=20: f='FALSIFIED' if (v['value5']>=0.10 or v['values_2_3_4']<0.60) else 'passed'
        if pid=='P14' and n>=25:
            sealv=next((x[2] for x in R if x[0]=='P15'),None); f='FALSIFIED' if (v<0.06 or (sealv is not None and v<=sealv)) else 'passed'
        out.append((pid,n,v,f,note))
    return out
if __name__=='__main__':
    args=sys.argv[1:]
    if '--smoke' in args:
        rng=random.Random(1); _pick=rng.sample(range(len(work)),300); lot=[dict(id=f'w{i}',seq=work[i]['seq'],type=work[i]['type'],site=work[i]['site']) for i in _pick]; name='smoke'
        for o in lot: published.discard(tuple(norm(o['seq'])))   # the pseudo-lot is itself 'published'; drop it for the uniqueness stat
        _ids={o['id'] for o in lot}; MODEL=Bigram([norm(r['seq']) for i,r in enumerate(work) if f'w{i}' not in _ids])   # out-of-sample model for the smoke lot
    else:
        lot=json.load(open(args[0])); name=args[0].rsplit('/',1)[-1].rsplit('.',1)[0]
    R=verdicts(score(lot))
    lines=[f'# Registry scoring: lot `{name}` ({len(lot)} objects)',"",'| id | n | observed | verdict | registered |','|---|---|---|---|---|']+[f'| {p} | {n} | {v} | {f} | {note} |' for p,n,v,f,note in R]
    out=next((a.split('=',1)[1] for a in args if a.startswith('--out=')),f'{B}/prereg/results-{name}.md')
    if name!='smoke': open(out,'w').write('\n'.join(lines)+'\n')
    print('\n'.join(lines))
    if name=='smoke': assert all(f!='FALSIFIED' for _,_,_,f,_ in R), 'smoke lot from the work set must not falsify anything'
