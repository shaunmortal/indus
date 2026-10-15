"""Prediction registry 3 (F33): computed on the WORK set only (data/holdout/work.json); hold-out untouched."""
import json, collections, hashlib
B='/Users/Happy/Desktop/plugins/indus'
work=json.load(open(f'{B}/data/holdout/work.json'))
TALL={31:1,32:2,33:3,34:4,35:5}; CUP=700
def cls3(t): return {'SEAL:S':'seal','SEAL:R':'seal','TAB:B':'tablet','TAB:I':'tablet','POT:T:g':'pot','POT:T:s':'pot'}.get(t)
rec=collections.defaultdict(collections.Counter); cupN=collections.Counter()
for r in work:
    s=tuple(r['seq']); c=cls3(r['type'])
    if not c or len(s)<2: continue
    for g in set(s):
        if g in TALL: rec[c][TALL[g]]+=1
    if c=='tablet':
        for i,g in enumerate(s):
            if g in TALL and ((i>0 and s[i-1]==CUP) or (i<len(s)-1 and s[i+1]==CUP)): cupN[TALL[g]]+=1
share={c:round((k[4]+k[5])/sum(k.values()),3) for c,k in rec.items()}
n={c:sum(k.values()) for c,k in rec.items()}
print('work-set tall-N by class',{c:[k[x] for x in range(1,6)] for c,k in rec.items()}); print('share N>=4',share,'n',n); print('tablet cup+tall N',dict(cupN))
reg={"author":"Ayush Kumar (India), with Claude","basis":"work set only; hold-out untouched","frozen":"2026-10-15",
 "source":"F33, analysis/numerals9_volumetric.py; numbers here from analysis/prereg3.py on the work set",
 "predictions":[
  {"id":"P14","scope":"new POTTERY graffiti with >=2 signs and at least one tall stroke (W31-W35 / M86-M96)","stat":"share of tall-stroke tokens with value >= 4",
   "predicted":share.get('pot'),"n_work":n.get('pot'),"falsifier":"observed share <= the seal share on the same new lot, or < 0.08, on >= 25 tall-stroke tokens"},
  {"id":"P15","scope":"new SEALS (any shape) with >=2 signs and at least one tall stroke","stat":"share of tall-stroke tokens with value >= 4",
   "predicted":share.get('seal'),"n_work":n.get('seal'),"falsifier":"observed share >= 0.12 on >= 40 tall-stroke tokens"},
  {"id":"P16","scope":"new TABLETS carrying the cup W700/M328 adjacent to a tall stroke","stat":"modal tall value in that pair",
   "predicted":max(cupN,key=cupN.get) if cupN else None,"n_work":sum(cupN.values()),"falsifier":"modal value is 1 or >= 4 on >= 15 pairs"}]}
js=json.dumps(reg,indent=1,sort_keys=True); open(f'{B}/prereg/predictions-3.json','w').write(js)
h=hashlib.sha256(open(f'{B}/prereg/predictions-3.json','rb').read()).hexdigest()
open(f'{B}/prereg/predictions-3.sha256','w').write(h+'  predictions-3.json\n'); print('SHA-256',h)
