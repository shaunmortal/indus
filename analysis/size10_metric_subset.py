"""F37: F12/F27 size effects re-tested on the only measurements independent of the 1930s catalogues: ICIT steatite square
seals from sites measured metrically in post-1950 reports (Lothal, Kalibangan, Nausharo, Allahdino, Banawali, Dholavira...).
Mohenjo-daro, Harappa and Chanhu-daro (Marshall/Mackay/Vats, inches) excluded. Site x length strata, residual area, permutation."""
import csv,json,collections,random,statistics as st
B='/Users/Happy/Desktop/plugins/indus'
seals={r['SEALID']:r for r in csv.DictReader(open(f'{B}/data/icit_seal.csv'))}; sites={r['SITEID']:r for r in csv.DictReader(open(f'{B}/data/icit_site.csv'))}
sitename={k:(v.get('NAME') or v.get('SITE') or list(v.values())[1]) for k,v in sites.items()}
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
mc={r['cisi']:r for r in json.load(open(f'{B}/data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))}
EXCL={'Mohenjo-daro','Harappa','Chanhu-daro','Chanhujo-daro'}
rows=[]
for r in csv.DictReader(open(f'{B}/data/raw/joyboseroy_csv/indus_website_real_corpus.csv')):
    s=seals.get(r['inscription_id'][1:])
    if not s: continue
    w,h=float(s['WIDTH'] or 0),float(s['HEIGHT'] or 0); site=sitename.get(s['SITEID'],'?')
    if not(5<w<100 and 5<h<100) or site in EXCL: continue
    m=mc.get(s['CISI'])
    if not m or m['type']!='SEAL:S' or s['MATERIAL']!='Steatite': continue
    seq=tuple(Wm.get(int(x[1:]),int(x[1:])) for x in r['sign_sequence'].split())
    if seq: rows.append(dict(site=site,area=w*h,L=min(len(seq),7),hj=741 in seq,seq=seq))
print('metric-site steatite square seals:',len(rows),collections.Counter(r['site'] for r in rows).most_common(8))
strata=collections.defaultdict(list)
for i,r in enumerate(rows): strata[(r['site'],r['L'])].append(i)
strata={k:v for k,v in strata.items() if len(v)>=3}; keep=[i for v in strata.values() for i in v]
med={k:st.median(rows[i]['area'] for i in v) for k,v in strata.items()}
res={i:rows[i]['area']-med[(rows[i]['site'],rows[i]['L'])] for i in keep}; medarea=st.median(rows[i]['area'] for i in keep)
def stat(flag):
    a=[res[i] for i in keep if flag[i]]; b=[res[i] for i in keep if not flag[i]]; return (st.mean(a)-st.mean(b)) if a and b else None, len(a)
def perm(flag,label,N=4000):
    obs,n=stat(flag); rng=random.Random(3); cnt=0
    for _ in range(N):
        vals=[flag[i] for i in keep]; rng.shuffle(vals); d,_=stat(dict(zip(keep,vals)))
        if d is not None and d<=obs: cnt+=1
    print(f'{label}: n={n} of {len(keep)}; residual area diff {obs:+.0f} mm2 ({obs/medarea:+.0%} of median {medarea:.0f}); one-sided (smaller) perm p={cnt/N:.3f}')
perm({i:rows[i]['hj'] for i in keep},'handled jar W741/M343 (F12)')
cnts=collections.Counter(r['seq'] for r in rows); perm({i:cnts[rows[i]['seq']]>=2 for i in keep},'repeated text (F27)')
