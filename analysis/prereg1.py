"""Phase 5: frozen, falsifiable predictions for NEW inscriptions (Failaka 2025 seals, Rakhigarhi 2022-26 seals, any new find),
computed from the WORK set only (hold-out untouched). Each prediction states the statistic, the predicted value, and the falsifier.
Output: prereg/predictions-1.json + SHA-256, committed to the public repo before any new text is seen."""
import json, collections, hashlib, datetime
B='/Users/Happy/Desktop/plugins/indus'
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
cls=json.load(open(f'{B}/data/model1b_consensus_classes.json'))['classes']
OPEN=set(cls['1']); CLOSE=set(cls['0'])
work=json.load(open(f'{B}/data/holdout/work.json'))
W=[(tuple(Wm.get(w,w) for w in r['seq']),r['type'],r['site']) for r in work if r['seq']]
sq=[s for s,t,_ in W if t=='SEAL:S' and len(s)>=3]; rd=[s for s,t,_ in W if t=='SEAL:R' and len(s)>=2]
tabs=[s for s,t,_ in W if t.startswith('TAB')]
def share(seqs,f): return round(sum(1 for s in seqs if f(s))/len(seqs),3)
NUM={1,3,4,5,13,16,17,31,32,33,35,55}
P=[]
P.append(dict(id='P1',scope='new SQUARE seals, text >=3 signs',stat='share whose LAST sign is in the closer class (13 signs)',predicted=share(sq,lambda s:s[-1] in CLOSE),n_work=len(sq),falsifier='observed share < 0.45 on >=20 new seals'))
P.append(dict(id='P2',scope='new SQUARE seals, text >=3 signs',stat='share whose FIRST sign is in the opener class (9 signs)',predicted=share(sq,lambda s:s[0] in OPEN),n_work=len(sq),falsifier='observed share < 0.10 or > 0.50 on >=20 new seals'))
P.append(dict(id='P3',scope='new seals of any shape',stat='share containing the handled jar W741/M343 among ROUND seals vs SQUARE',predicted={'round':share(rd,lambda s:741 in s),'square':share(sq,lambda s:741 in s)},n_work={'round':len(rd),'square':len(sq)},falsifier='round share >= square share on >=15 round seals'))
P.append(dict(id='P4',scope='new ROUND seals',stat='share containing W407/M169 or W803/W806 (M387 family)',predicted=share(rd,lambda s:(407 in s) or (390 in s and False) or (803 in s)),n_work=len(rd),falsifier='observed share < 0.08 on >=15 round seals (square baseline %.3f)'%share(sq,lambda s:(407 in s) or (803 in s))))
P.append(dict(id='P5',scope='new texts with stroke signs',stat='short-stroke value distribution: share of value 7 among values 4-9',predicted=None,falsifier='see note 1 Test 2: if quantities, 4 > 5 > 6 > 7; we predict 7 > 4,5,6 combined share per value'))
v=collections.Counter()
for s,_,_ in W:
    for w in s:
        if w in (4,5,16,17): v[{4:4,5:5,16:6,17:7}[w]]+=1
tot=sum(v.values()); P[-1]['predicted']={k:round(v[k]/tot,3) for k in (4,5,6,7)}; P[-1]['n_work']=tot
P.append(dict(id='P6',scope='new two-sided TABLETS/SEALINGS from Harappa',stat='share of side-2 texts that end in the cup W700/M328 preceded by a tall stroke',predicted=None,falsifier='observed share < 0.25 on >=20 new two-sided tablets'))
t2=[s for s in tabs if len(s)>=2]; P[-1]['predicted']=share(t2,lambda s:s[-1]==700 and s[-2] in (31,32,33,35)); P[-1]['n_work']=len(t2)
P.append(dict(id='P7',scope='any new text',stat='bigram perplexity of the new texts under the work-set bigram model (sign list v3)',predicted='between 25 and 45 per sign if the texts are Indus-script seal texts; > 80 if they are not Indus texts or are a different tradition',falsifier='ppl outside 20-60 on >=30 new texts'))
P.append(dict(id='P8',scope='any new SQUARE seal with an animal',stat='no sign will be significantly enriched by animal (F14)',predicted='no sign x animal pair passes Bonferroni on the new set alone',falsifier='a pair with ratio > 3 and p < 0.001 on >= 100 new seals'))
reg={'frozen':datetime.date.today().isoformat(),'author':'Ayush Kumar (India), with Claude','basis':'work set only (data/holdout/work.json); hold-out untouched','sign_list':'Wells v3 (data/model5_merges_wells_v3.json); classes data/model1b_consensus_classes.json','predictions':P}
import os; os.makedirs(f'{B}/prereg',exist_ok=True)
js=json.dumps(reg,indent=1,sort_keys=True); open(f'{B}/prereg/predictions-1.json','w').write(js)
h=hashlib.sha256(js.encode()).hexdigest(); open(f'{B}/prereg/predictions-1.sha256','w').write(h+'  predictions-1.json\n')
for p in P: print(p['id'],p['stat'][:60],'->',p['predicted'],'| n=',p.get('n_work'))
print('SHA-256',h)
