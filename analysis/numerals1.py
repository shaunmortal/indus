"""Numerals in the Mahadevan (IM77) corpus: what gets counted, where, how much.
Short strokes: 97/98=1, 99/100=2(connective, excluded), 102/103=3, 104/105=4, 106/107=5, 108/109=6, 110/112=7
Tall strokes: 86=1, 87=2, 89=3
Sequences are in reading order (first read first). Sign 0 = lost/illegible -> break."""
import csv, collections
SHORT={'97':1,'98':1,'102':3,'103':3,'104':4,'105':4,'106':5,'107':5,'108':6,'109':6,'110':7,'112':7}
TALL={'86':1,'87':2,'89':3}
NUM={**SHORT,**TALL}
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seqs=[]
for r in rows:
    s=r['signs_clean'].split()
    if not s or s==['0']: continue
    seqs.append((r,s))
print("lines with text:",len(seqs))
by_obj=collections.Counter(); num_by_obj=collections.Counter()
after=collections.Counter(); before=collections.Counter(); pos=collections.Counter(); vals=collections.Counter()
tall_after=collections.Counter(); short_after=collections.Counter()
for r,s in seqs:
    by_obj[r['object_type']]+=1
    has=False
    for i,t in enumerate(s):
        if t in NUM:
            has=True; vals[(('T' if t in TALL else 'S'),NUM[t])]+=1
            nxt=s[i+1] if i+1<len(s) else 'END'
            prv=s[i-1] if i>0 else 'START'
            if nxt!='0': after[nxt]+=1; (tall_after if t in TALL else short_after)[nxt]+=1
            if prv!='0': before[prv]+=1
            pos['first' if i==0 else 'last' if i==len(s)-1 else 'mid']+=1
    if has: num_by_obj[r['object_type']]+=1
print("\nnumeral values (T=tall,S=short):",sorted(vals.items()))
print("numeral position:",dict(pos))
print("\nobject type: lines / lines with numeral / share")
for o,c in by_obj.most_common(): print(f"  {o:20} {c:5} {num_by_obj[o]:5} {num_by_obj[o]/c:5.0%}")
print("\nTOP signs AFTER a numeral (the 'counted item' slot):",after.most_common(12))
print("  after SHORT strokes:",short_after.most_common(8))
print("  after TALL strokes :",tall_after.most_common(8))
print("TOP signs BEFORE a numeral:",before.most_common(10))
# Which signs are almost ALWAYS preceded by a numeral? (candidate units of measure)
tot=collections.Counter(t for _,s in seqs for t in s if t!='0')
print("\nsigns most dependent on a preceding numeral (count>=20):")
dep=[(after[t]/tot[t],t,after[t],tot[t]) for t in tot if tot[t]>=20 and after[t]>0]
for share,t,a,n in sorted(dep,reverse=True)[:12]: print(f"  sign {t:>4}: {a:3}/{n:3} = {share:4.0%} preceded by numeral")
# two-numeral stacks (e.g. 3 then 4) = multi-digit? 
stack=sum(1 for _,s in seqs for a,b in zip(s,s[1:]) if a in NUM and b in NUM)
print("\nadjacent numeral pairs (possible compound numbers):",stack)
