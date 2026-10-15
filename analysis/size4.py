"""Robustness of the G741 (M343) small-seal effect: per-site, position, relation to plain jar G740, material, thickness."""
import csv, json, collections, statistics as st, random
exec(open('analysis/size1.py').read().split("# text length vs area")[0])
for r in sq: r['seq']=r['seq'][::-1]
def med(xs): return round(st.median(xs)) if xs else None
print("G741 position in text (reading order):",collections.Counter('last' if r['seq'][-1]==741 else 'first' if r['seq'][0]==741 else 'mid' for r in sq if 741 in r['seq']))
print("co-occurrence: seals with 741 that also have 740:",sum(1 for r in sq if 741 in r['seq'] and 740 in r['seq']),"of",sum(1 for r in sq if 741 in r['seq']))
print("\nper site, same text length band, median area with vs without G741:")
for site in ['Mohenjo-daro','Harappa','Chanhujo-daro']:
    for lo,hi in [(2,4),(5,6),(7,20)]:
        w=[r['area'] for r in sq if r['site']==site and lo<=len(r['seq'])<=hi and 741 in r['seq']]
        wo=[r['area'] for r in sq if r['site']==site and lo<=len(r['seq'])<=hi and 741 not in r['seq']]
        if len(w)>=4: print(f"  {site:14} len {lo}-{hi}: with741 n={len(w):3} median={med(w)}   without n={len(wo):3} median={med(wo)}")
print("\nsame for G740 (plain jar) as the LAST sign vs not, Mohenjo-daro:")
for lo,hi in [(2,4),(5,6),(7,20)]:
    w=[r['area'] for r in sq if r['site']=='Mohenjo-daro' and lo<=len(r['seq'])<=hi and r['seq'][-1]==740]
    wo=[r['area'] for r in sq if r['site']=='Mohenjo-daro' and lo<=len(r['seq'])<=hi and r['seq'][-1]!=740]
    print(f"  len {lo}-{hi}: jar-final n={len(w):3} median={med(w)}   other n={len(wo):3} median={med(wo)}")
print("\nthickness: with 741",med([r['t'] for r in sq if 741 in r['seq'] and r['t']>0])," without",med([r['t'] for r in sq if 741 not in r['seq'] and r['t']>0]))
print("iconography with 741:",collections.Counter(r['icon'] for r in sq if 741 in r['seq']).most_common(4)," overall:",collections.Counter(r['icon'] for r in sq).most_common(4))
# what precedes 741 vs 740 (do they take the same 'title' slot?)
pre741=collections.Counter(r['seq'][i-1] for r in sq for i,g in enumerate(r['seq']) if g==741 and i>0)
pre740=collections.Counter(r['seq'][i-1] for r in sq for i,g in enumerate(r['seq']) if g==740 and i>0)
print("\nsign before 741:",pre741.most_common(6)); print("sign before 740:",pre740.most_common(6))
