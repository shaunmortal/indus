"""Do specific signs predict SEAL SIZE? Join ICIT seal dimensions to sign sequences.
For each sign with >=30 distinct square-seal texts: mean seal face area with vs without the sign; permutation p-value (10,000 shuffles).
Also: text length vs area; opener/closer classes vs area."""
import csv, json, collections, random, statistics as st
seals={r['SEALID']:r for r in csv.DictReader(open('data/icit_seal.csv'))}
sites={r['SITEID']:r['NAME'] for r in csv.DictReader(open('data/icit_site.csv'))}
icon={r['SEALID']:r['DESCRIPTION'] for r in csv.DictReader(open('data/icit_iconography.csv'))}
corp=list(csv.DictReader(open('data/raw/joyboseroy_csv/indus_website_real_corpus.csv')))
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
type_by_cisi={r['cisi']:r['type'] for r in mc if r.get('cisi') and r['cisi']!='-'}
# sanity: inscription_id S<n> == SEALID n ? check cisi agreement
agree=sum(1 for r in corp if seals.get(r['inscription_id'][1:],{}).get('CISI')==r['cisi_number']); print("cisi agreement S<n>==SEALID:",agree,"of",len(corp))
rows=[]; seen=set()
for r in corp:
    sid=r['inscription_id'][1:]; s=seals.get(sid)
    if not s: continue
    w,h,t=float(s['WIDTH'] or 0),float(s['HEIGHT'] or 0),float(s['THICKNESS'] or 0)
    if w<=0 or h<=0: continue
    seq=tuple(int(x[1:]) for x in r['sign_sequence'].split() if x[1:].isdigit())
    if not seq or (seq,sid) in seen: continue
    seen.add((seq,sid))
    rows.append(dict(sid=sid,seq=seq,area=w*h,w=w,h=h,t=t,site=sites.get(s['SITEID'],'?'),mat=s['MATERIAL'],obj=type_by_cisi.get(s['CISI'] or '','?'),icon=icon.get(sid,'')))
print("seals with dims+text:",len(rows)," object types:",collections.Counter(r['obj'] for r in rows).most_common(5))
sq=[r for r in rows if r['obj']=='SEAL:S' and r['mat']=='Steatite']
print("steatite seals:",len(sq)," median area mm2:",st.median(r['area'] for r in sq)," median w,h:",st.median(r['w'] for r in sq),st.median(r['h'] for r in sq))
# text length vs area
byl=collections.defaultdict(list)
for r in sq: byl[min(len(r['seq']),8)].append(r['area'])
print("\ntext length -> median area (n):",{l:(round(st.median(v)),len(v)) for l,v in sorted(byl.items())})
# per-sign test
random.seed(1)
areas=[r['area'] for r in sq]
def perm_p(idx_with,n_perm=10000):
    obs=st.mean(areas[i] for i in idx_with)-st.mean(areas[i] for i in range(len(areas)) if i not in idx_with)
    k=len(idx_with); cnt=0; ids=list(range(len(areas)))
    for _ in range(n_perm):
        random.shuffle(ids); a=ids[:k]; sa=set(a)
        d=st.mean(areas[i] for i in a)-st.mean(areas[i] for i in ids[k:])
        if abs(d)>=abs(obs): cnt+=1
    return obs,cnt/n_perm
signs=collections.Counter(g for r in sq for g in set(r['seq']))
res=[]
for g,n in signs.items():
    if n<30: continue
    idx=set(i for i,r in enumerate(sq) if g in r['seq'])
    obs,p=perm_p(idx,2000)
    res.append((p,obs,g,n))
res.sort()
print("\nsigns whose presence shifts mean seal area (steatite square seals), sorted by permutation p (2000 perms):")
print("  sign  n   delta_area_mm2   p")
for p,obs,g,n in res[:15]: print(f"  G{g:<4} {n:4}  {obs:+8.1f}   {p:.3f}")
print("  ... least:"); 
for p,obs,g,n in res[-3:]: print(f"  G{g:<4} {n:4}  {obs:+8.1f}   {p:.3f}")
print("\nBonferroni threshold for",len(res),"signs:",round(0.05/len(res),4))
