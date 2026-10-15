"""Test Wells' hypothesis (tall stroke = 10, short = 1) on compound numeral pairs in IM77.
If tall=tens and short=ones, compounds should be ordered consistently (tall then short, or always the reverse),
and the stroke-count distribution should NOT look like a 'favourite numbers' distribution."""
import csv, collections
SHORT={'97':1,'98':1,'102':3,'103':3,'104':4,'105':4,'106':5,'107':5,'108':6,'109':6,'110':7,'112':7}
TALL={'86':1,'87':2,'89':3}
NUM={**SHORT,**TALL}
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seqs=[r['signs_clean'].split() for r in rows if r['signs_clean'].strip() and r['signs_clean'].strip()!='0']
order=collections.Counter(); pairs=collections.Counter()
for s in seqs:
    for a,b in zip(s,s[1:]):
        if a in NUM and b in NUM:
            ka='T' if a in TALL else 'S'; kb='T' if b in TALL else 'S'
            order[ka+kb]+=1
            pairs[(ka+str(NUM[a]), kb+str(NUM[b]))]+=1
print("compound numeral pair orders (first,second):",dict(order))
print("most common compounds:",pairs.most_common(12))
# distribution of short values vs what a 'quantity' distribution would look like (monotone decreasing, Benford-ish)
vals=collections.Counter()
for s in seqs:
    for t in s:
        if t in SHORT: vals[SHORT[t]]+=1
        if t in TALL: vals['T'+str(TALL[t])]+=1
print("short-stroke values 1..7 (2 excluded as connective):",[vals.get(i,0) for i in range(1,8)])
print("tall-stroke values 1..3:",[vals.get('T'+str(i),0) for i in range(1,4)])
# Do the same counted item take BOTH tall and short numerals? (if tall=10s, a commodity counted in tens should also be counted in ones)
after=collections.defaultdict(collections.Counter)
for s in seqs:
    for a,b in zip(s,s[1:]):
        if a in NUM and b not in NUM and b!='0': after[b]['T' if a in TALL else 'S']+=1
both=[(b,c['T'],c['S']) for b,c in after.items() if c['T']+c['S']>=15]
print("\ncounted item: tall-count / short-count")
for b,t,s_ in sorted(both,key=lambda x:-(x[1]+x[2])): print(f"  M{b:>4}: T={t:3} S={s_:3}  {'MIXED' if t>=3 and s_>=3 else 'ONE SYSTEM ONLY'}")
