"""Complete stroke-sign inventory (read from Mahadevan drawings, analysis/img/signs_80_135.png) and three tests:
 A. value distributions, short 1-12 and tall 1-5
 B. are one-tier and two-tier forms of the same value allographs? (compare what follows them)
 C. is short-2 (M99/M100) really a connective, or a numeral like 1 and 3?"""
import csv, json, collections, math
SHORT={97:1,98:1,99:2,100:2,101:2,102:3,103:3,104:4,105:4,106:5,107:5,108:6,109:6,110:7,111:7,112:7,
       114:8,115:9,116:9,117:9,118:10,121:12,122:5}
TIER={97:1,98:1,99:1,100:1,101:2,102:1,103:2,104:1,105:2,106:1,107:2,108:1,109:2,110:1,111:1,112:2,
      114:2,115:1,116:2,117:2,118:2,121:3,122:1}
TALL={86:1,87:2,88:3,89:3,92:3,93:3,94:3,95:4,96:5}
CHEV={119:3,120:4}
json.dump({'short':SHORT,'short_tiers':TIER,'tall':TALL,'chevron':CHEV,
           'note':'read from Mahadevan 1977 sign drawings on 2026-10-15; 113 and 123 excluded (unclear)'},
          open('data/stroke_signs.json','w'),indent=1)
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
seqs=[[int(t) for t in r['signs_clean'].split()] for r in rows if r['signs_clean'].strip() and r['signs_clean'].strip()!='0']
tok=collections.Counter(t for s in seqs for t in s)
# A
print("A. SHORT value -> tokens (by sign):")
byval=collections.defaultdict(list)
for m,v in SHORT.items(): byval[v].append((m,tok[m],TIER[m]))
for v in sorted(byval): print(f"  {v:>2}: "+", ".join(f"M{m}={c}(tier{t})" for m,c,t in byval[v])+f"   total={sum(c for _,c,_ in byval[v])}")
print("   TALL:", {v:sum(tok[m] for m,vv in TALL.items() if vv==v) for v in range(1,6)}, " CHEVRON:",{v:tok[m] for m,v in CHEV.items()})
# B & C: following-sign distribution per numeral sign
foll=collections.defaultdict(collections.Counter)
for s in seqs:
    for a,b in zip(s,s[1:]):
        if b!=0: foll[a][b]+=1
def cos(c1,c2):
    keys=set(c1)|set(c2); n1=math.sqrt(sum(v*v for v in c1.values())); n2=math.sqrt(sum(v*v for v in c2.values()))
    return sum(c1[k]*c2[k] for k in keys)/(n1*n2) if n1 and n2 else float('nan')
print("\nB. one-tier vs two-tier forms of the same value: cosine similarity of what follows them (n=tokens)")
pairs=[(102,103),(104,105),(106,107),(108,109),(110,112),(97,98),(99,100),(99,101),(115,116)]
for a,b in pairs: print(f"  M{a}(n={tok[a]}) vs M{b}(n={tok[b]}): cos={cos(foll[a],foll[b]):.2f}  top after M{a}: {foll[a].most_common(3)}  | after M{b}: {foll[b].most_common(3)}")
print("\n  control: unrelated numerals  M97 vs M102:", f"{cos(foll[97],foll[102]):.2f}", " M86 vs M87:", f"{cos(foll[86],foll[87]):.2f}", " M87 vs M89:", f"{cos(foll[87],foll[89]):.2f}")
print("\nC. is short-2 a connective? similarity of what follows M99 to what follows other short numerals:")
for m in [97,102,104,106,110]: print(f"  M99 vs M{m}: cos={cos(foll[99],foll[m]):.2f}")
print("  after M99 top10:",foll[99].most_common(10))
print("  after M102 top10:",foll[102].most_common(10))
# where does M99 sit? position
pos=collections.Counter()
for s in seqs:
    for i,t in enumerate(s):
        if t==99: pos['first' if i==0 else 'last' if i==len(s)-1 else 'mid']+=1
print("  M99 position:",dict(pos))
