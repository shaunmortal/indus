"""Side-2 numerals (tablets+sealings) vs seal numerals: value distributions, unit signs, repetitiveness. Distinct texts."""
import csv, json, collections
SS=json.load(open('data/stroke_signs.json')); SHORT={int(k):v for k,v in SS['short'].items()}; TALL={int(k):v for k,v in SS['tall'].items()}
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
def vals(seq):
    out=[]
    for i,t in enumerate(seq):
        if t in TALL: out.append(('T',TALL[t],seq[i+1] if i+1<len(seq) else 'END'))
        elif t in SHORT and t not in (99,100,101): out.append(('S',SHORT[t],seq[i+1] if i+1<len(seq) else 'END'))
    return out
groups={'side2 of 2-sided tablets/sealings':[], 'side1 of 2-sided tablets/sealings':[], 'single-sided seals':[]}
obj=collections.defaultdict(dict)
for r in rows:
    s=r['signs_clean'].strip()
    if not s or s=='0': continue
    seq=[int(t) for t in s.split()]
    obj[(r['text_no'],r['object_type'])].setdefault(r['side'],[]).append(seq)
for (tn,typ),sides in obj.items():
    if typ in ('miniature tablet','sealing') and '1' in sides and '2' in sides:
        groups['side2 of 2-sided tablets/sealings']+=sides['2']; groups['side1 of 2-sided tablets/sealings']+=sides['1']
    elif typ=='seal' and list(sides)==['0']:
        groups['single-sided seals']+=sides['0']
for name,seqs in groups.items():
    seqs=[list(s) for s in {tuple(x) for x in seqs}]
    V=collections.Counter(); U=collections.Counter(); cls=collections.Counter()
    for s in seqs:
        for c,v,u in vals(s): V[(c,v)]+=1; U[u]+=1; cls[c]+=1
    print(f"\n== {name}: distinct texts={len(seqs)}, numeral tokens={sum(V.values())} (T {cls['T']}, S {cls['S']})")
    print("  short values:",[(v,V[('S',v)]) for v in [1,3,4,5,6,7,8,9,10,12] if V[('S',v)]],"  tall:",[(v,V[('T',v)]) for v in [1,2,3,4,5] if V[('T',v)]])
    print("  sign after numeral:",U.most_common(8))
    print("  example side texts:",[' '.join(map(str,s)) for s in seqs[:6]])
