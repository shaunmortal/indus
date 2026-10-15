"""Replication of F7 fixed compounds per site and per object type. A real structural fact should hold at Mohenjo-daro AND Harappa, on seals AND sealings."""
import csv, collections
rows=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
COMP=[(103,403),(95,328),(112,194),(89,328),(87,328),(102,59),(347,342),(8,342),(267,99)]
def stats(subset,label):
    foll=collections.defaultdict(collections.Counter)
    for r in subset:
        s=[int(t) for t in r['signs_clean'].split()] if r['signs_clean'].strip() else []
        for a,b in zip(s,s[1:]):
            if a and b: foll[a][b]+=1
    out=[]
    for a,b in COMP:
        n=sum(foll[a].values()); c=foll[a][b]
        out.append(f"M{a}->M{b} {c}/{n}" + (f"={c/n:.0%}" if n else ""))
    print(f"{label:28}", " | ".join(out))
print("compound: M103->403 (3 two-tier), M95->328 (4 tall), M112->194 (7 two-tier), M89->328 (3 tall), M87->328 (2 tall), M102->59 (3 one-row), + 3 known compounds as controls\n")
stats(rows,"ALL")
for site in ["Mohenjodaro","Harappa","Lothal","Kalibangan","Chanhudaro"]:
    stats([r for r in rows if r['site']==site],"site="+site)
print()
for ob in ["seal","sealing","miniature tablet","copper tablet","pottery graffito"]:
    stats([r for r in rows if r['object_type']==ob],"obj="+ob)
# dedupe check: identical sequences inflate counts (e.g. many sealings from one seal). Count DISTINCT sequences too.
print("\nDISTINCT sequences only (dedup identical texts):")
seen=set(); uniq=[]
for r in rows:
    k=r['signs_clean'].strip()
    if k and k not in seen: seen.add(k); uniq.append(r)
stats(uniq,"ALL distinct")
