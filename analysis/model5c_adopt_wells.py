"""Adoption rule (M4b) for Wells merges on ICIT: adopt a candidate merge only if the 5-split held-out perplexity drop beats a single-random-merge null by 2 sd."""
import csv, json, collections, math, random, statistics as st
exec(open('analysis/model5b_validate.py').read().split("# union-find")[0])   # loads base, ppl, apply
res=json.load(open(f'{B}/data/model5_wells_allographs.json'))
tok=collections.Counter(t for s in base for t in s)
cur={}; seqs=list(base); p0=ppl(seqs); print(f"start: ppl {p0:.2f}")
freq=[g for g,c in tok.items() if c>=15]; rng=random.Random(17); null=[]
for _ in range(40):
    a,b=rng.sample(freq,2); null.append(ppl(apply(seqs,{a:b}))-p0)
mu,sd=st.mean(null),st.stdev(null); thr=mu-2*sd; print(f"null delta {mu:+.3f} +- {sd:.3f}; threshold {thr:+.3f}")
def root(x):
    while x in cur: x=cur[x]
    return x
cands=sorted(res['allograph_candidates'],key=lambda p:-(p[2]+p[3]))
for a,b,i_,d_ in cands:
    ra,rb=root(a),root(b)
    if ra==rb: print(f"  W{a}~W{b}: already merged"); continue
    keep,drop=(ra,rb) if tok[ra]>=tok[rb] else (rb,ra)
    d=ppl(apply(seqs,{drop:keep}))-p0; v='ADOPT' if d<thr else 'reject'
    print(f"  W{drop}->W{keep}: delta {d:+.3f} {v}")
    if v=='ADOPT': cur[drop]=keep; seqs=apply(base,{x:root(x) for x in cur}); p0=ppl(seqs)
json.dump({str(k):root(k) for k in cur},open(f'{B}/data/model5_merges_wells_v2.json','w'),indent=0)
print(f"final: {len(set(t for s in seqs for t in s))} signs, ppl {p0:.2f}, merges adopted {len(cur)}")
