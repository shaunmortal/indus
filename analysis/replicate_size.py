"""Pooled independent replication of F12 on Marshall 1931 (MIC) + Mackay 1938 (FEM) seal measurements,
joined to IM77 by text_no = 1000+MIC serial / 2000+FEM serial (confirmed by Mahadevan Appendix V).
Strata: source x text length. 10,000 permutations. One-sided test in the pre-specified direction (smaller), since F12 fixed the direction."""
import json, csv, random, statistics as st, collections
mar={int(k):v for k,v in json.load(open('data/marshall_seal_sizes.json')).items()}
mac={int(k):v for k,v in json.load(open('data/mackay_seal_sizes.json')).items()}
im=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
im_by={}
for r in im:
    if r['signs_clean'].strip() not in ('','0') and r['object_type']=='seal': im_by.setdefault(int(r['text_no']),r)
recs=[]
for ser,v in mar.items():
    r=im_by.get(1000+ser)
    if r: recs.append(('MIC',[int(t) for t in r['signs_clean'].split()],v['w']*(v['h'] or v['w'])*645.16))
for ser,v in mac.items():
    r=im_by.get(2000+ser)
    if r: recs.append(('FEM',[int(t) for t in r['signs_clean'].split()],v['w']*v['h']*645.16))
print("pooled seals:",len(recs),collections.Counter(s for s,_,_ in recs),"median area",round(st.median(a for _,_,a in recs)))
random.seed(11)
key=lambda i:(recs[i][0],min(len(recs[i][1]),8))
strata=collections.defaultdict(list)
for i in range(len(recs)): strata[key(i)].append(i)
strata={k:v for k,v in strata.items() if len(v)>=4}; keep=[i for v in strata.values() for i in v]
med={k:st.median(recs[i][2] for i in v) for k,v in strata.items()}
resid={i:recs[i][2]-med[key(i)] for i in keep}
def test(sign,one_sided_smaller=True,n=10000):
    w=[i for i in keep if sign in recs[i][1]]; wo=[i for i in keep if sign not in recs[i][1]]
    if len(w)<8: return None
    obs=st.mean(resid[i] for i in w)-st.mean(resid[i] for i in wo); cnt=0
    for _ in range(n):
        ph=set()
        for k,idx in strata.items():
            m=sum(1 for i in idx if sign in recs[i][1]); ph.update(random.sample(idx,m))
        d=st.mean(resid[i] for i in ph)-st.mean(resid[i] for i in keep if i not in ph)
        if (d<=obs) if one_sided_smaller else (abs(d)>=abs(obs)): cnt+=1
    return len(w),obs,cnt/n
for sign,name,os in [(343,'M343 handled jar (pre-specified: smaller)',True),(342,'M342 plain jar (two-sided)',False),(169,'M169 (two-sided)',False),(176,'M176 (two-sided)',False),(161,'M161 (two-sided)',False)]:
    r=test(sign,os); print(f"{name}: "+(f"n={r[0]} delta={r[1]:+.0f} mm2 ({r[1]/st.median(a for _,_,a in recs):+.0%}) p={r[2]:.4f}" if r else "too few"))
# per-source for M343
for src in ['MIC','FEM']:
    w=[resid[i] for i in keep if recs[i][0]==src and 343 in recs[i][1]]; wo=[resid[i] for i in keep if recs[i][0]==src and 343 not in recs[i][1]]
    print(f"  {src}: M343 n={len(w)} mean resid with={st.mean(w):+.0f} without={st.mean(wo):+.0f}")
