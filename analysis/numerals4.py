"""Null check for F7: how unusual is cos~0 between two signs' following-distributions?
Baseline = all pairs of signs with >=30 tokens each. Also: how often is a sign's top follower >=80% of its tokens (fixed compound)?"""
import csv, collections, math, itertools
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seqs=[[int(t) for t in r['signs_clean'].split()] for r in rows if r['signs_clean'].strip() and r['signs_clean'].strip()!='0']
tok=collections.Counter(t for s in seqs for t in s)
foll=collections.defaultdict(collections.Counter)
for s in seqs:
    for a,b in zip(s,s[1:]):
        if b!=0 and a!=0: foll[a][b]+=1
def cos(c1,c2):
    n1=math.sqrt(sum(v*v for v in c1.values())); n2=math.sqrt(sum(v*v for v in c2.values()))
    return sum(c1[k]*c2[k] for k in set(c1)&set(c2))/(n1*n2) if n1 and n2 else float('nan')
signs=[m for m in tok if tok[m]>=30 and sum(foll[m].values())>=15]
vals=sorted(cos(foll[a],foll[b]) for a,b in itertools.combinations(signs,2))
import statistics
print(f"baseline pairs={len(vals)} median cos={statistics.median(vals):.2f}  share<=0.05: {sum(v<=0.05 for v in vals)/len(vals):.0%}  share>=0.40: {sum(v>=0.40 for v in vals)/len(vals):.0%}")
print("=> cos 0.00 between M102 and M103 is NOT rare by itself; the finding rests on the FIXED-COMPOUND behaviour below.")
print("\nsigns (n>=20 followers) whose single top follower takes >=70% of their followers (fixed compounds):")
fx=[]
for m in foll:
    n=sum(foll[m].values())
    if n>=20:
        b,c=foll[m].most_common(1)[0]
        if c/n>=0.7: fx.append((c/n,m,b,c,n))
for sh,m,b,c,n in sorted(fx,reverse=True): print(f"  M{m:>3} -> M{b:>3}: {c:3}/{n:3} = {sh:.0%}")
print("\nfor comparison, one-row stroke signs: top follower share")
for m in [97,98,99,102,104,106,108,110,86,87,89,95]:
    n=sum(foll[m].values()); b,c=foll[m].most_common(1)[0] if n else (None,0)
    print(f"  M{m:>3} (n={n:3}) top M{b}: {c/n if n else 0:.0%}")
