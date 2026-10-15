"""If stroke 'numerals' were rank numbers, seal size should vary with the value. Test: among steatite square seals, area vs numeral value
(tall 1/2/3; short 1/3/4/5/6/7/12), site x length controlled residuals. Also: any-numeral vs none."""
import csv, json, collections, random, statistics as st
exec(open('analysis/size1.py').read().split("# text length vs area")[0])
for r in sq: r['seq']=r['seq'][::-1]
bridge={int(k):v['M'] for k,v in json.load(open('data/bridge_WM.json')).items()}
SS=json.load(open('data/stroke_signs.json')); SHORT={int(k):v for k,v in SS['short'].items()}; TALL={int(k):v for k,v in SS['tall'].items()}
def val(g):
    for m in bridge.get(g,[]):
        if m in TALL: return ('T',TALL[m])
        if m in SHORT and m not in (99,100,101): return ('S',SHORT[m])
    return None
key=lambda r:(r['site'],min(len(r['seq']),8))
strata=collections.defaultdict(list)
for i,r in enumerate(sq): strata[key(r)].append(i)
strata={k:v for k,v in strata.items() if len(v)>=5}
med={k:st.median(sq[i]['area'] for i in v) for k,v in strata.items()}
resid={i:sq[i]['area']-med[key(sq[i])] for v in strata.values() for i in v}
byv=collections.defaultdict(list); anyn=[]; none=[]
for i,res in resid.items():
    vs=[val(g) for g in sq[i]['seq'] if val(g)]
    (anyn if vs else none).append(res)
    for v in set(vs): byv[v].append(res)
print("any numeral: n=%d mean resid=%+.1f | none: n=%d mean resid=%+.1f"%(len(anyn),st.mean(anyn),len(none),st.mean(none)))
print("\nresidual area by numeral value (n, mean, median):")
for v in sorted(byv): 
    if len(byv[v])>=8: print(f"  {v[0]}{v[1]:<3} n={len(byv[v]):3}  mean={st.mean(byv[v]):+7.1f}  median={st.median(byv[v]):+7.1f}")
# monotone trend test for tall 1,2,3 and short 1..7: Spearman via permutation
def spearman(xs,ys):
    def rank(a):
        s=sorted(range(len(a)),key=lambda i:a[i]); r=[0]*len(a)
        for k,i in enumerate(s): r[i]=k
        return r
    rx,ry=rank(xs),rank(ys); n=len(xs); mx,my=st.mean(rx),st.mean(ry)
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry)); den=(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))**0.5
    return num/den if den else 0
random.seed(5)
for cls in ['T','S']:
    xs=[];ys=[]
    for v,res in byv.items():
        if v[0]==cls: xs+= [v[1]]*len(res); ys+=res
    if len(xs)<20: continue
    obs=spearman(xs,ys); cnt=0
    for _ in range(3000):
        random.shuffle(ys)
        if abs(spearman(xs,ys))>=abs(obs): cnt+=1
    print(f"\n{cls}-strokes: value vs residual area, Spearman rho={obs:+.3f}, perm p={cnt/3000:.3f} (n={len(xs)})")
