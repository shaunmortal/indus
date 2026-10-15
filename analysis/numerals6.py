"""Re-run F1/F2/F5 on DISTINCT texts only (identical sequences collapsed to one), because Harappa miniature tablets
and sealings repeat the same text dozens of times and inflate every count."""
import csv, collections, json
SS=json.load(open('data/stroke_signs.json'))
SHORT={int(k):v for k,v in SS['short'].items()}; TALL={int(k):v for k,v in SS['tall'].items()}
NUM={**SHORT,**TALL}
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seen=set(); uniq=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k!='0' and k not in seen: seen.add(k); uniq.append((r,[int(t) for t in k.split()]))
print("distinct texts:",len(uniq),"of",sum(1 for r in rows if r['signs_clean'].strip() and r['signs_clean'].strip()!='0'))
# F1: share with numeral per object type (first occurrence's object type)
by=collections.Counter(); nb=collections.Counter()
for r,s in uniq:
    by[r['object_type']]+=1
    if any(t in NUM for t in s): nb[r['object_type']]+=1
print("\nF1 dedup — share of distinct texts with a numeral:")
for o,c in by.most_common(5): print(f"  {o:18} {nb[o]:4}/{c:4} = {nb[o]/c:.0%}")
# F5.2 value distributions
vs=collections.Counter(); vt=collections.Counter()
for _,s in uniq:
    for t in s:
        if t in SHORT and t not in (99,100,101): vs[SHORT[t]]+=1
        if t in TALL: vt[TALL[t]]+=1
print("\nF5 dedup — short values 1,3..12:",[(v,vs[v]) for v in sorted(vs)]," tall 1..5:",[(v,vt[v]) for v in sorted(vt)])
# F5.1 compound order
order=collections.Counter()
for _,s in uniq:
    for a,b in zip(s,s[1:]):
        if a in NUM and b in NUM and a not in (99,100,101) and b not in (99,100,101):
            order[('T' if a in TALL else 'S')+('T' if b in TALL else 'S')]+=1
print("F5 dedup — compound numeral orders:",dict(order))
# F2/F5.3 complements of tall vs short (excluding connective 2)
after=collections.defaultdict(collections.Counter)
for _,s in uniq:
    for a,b in zip(s,s[1:]):
        if a in NUM and a not in (99,100,101) and b not in NUM and b!=0: after[b]['T' if a in TALL else 'S']+=1
print("\nF2 dedup — counted item: tall / short (n>=10)")
for b,c in sorted(after.items(),key=lambda x:-(x[1]['T']+x[1]['S'])):
    if c['T']+c['S']>=10: print(f"  M{b:>4}: T={c['T']:3} S={c['S']:3}")
