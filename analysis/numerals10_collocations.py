"""Right-adjacent collocations of stroke signs (the layout of Wells 2015 tables 5.1-5.3), computed on both corpora so
the two readings can be compared sign by sign once the book is in hand. 'Right-adjacent' = the next sign in reading order.
Classes: short linear (one tier), short stacked (two/three tiers), long/tall. Distinct texts, Wells v3 / Mahadevan v3.
Writes data/stroke_collocations_v1.json."""
import json, csv, collections
B='/Users/Happy/Desktop/plugins/indus'
SS=json.load(open(f'{B}/data/stroke_signs.json'))
SHORT={int(k):v for k,v in SS['short'].items()}; TIER={int(k):v for k,v in SS['short_tiers'].items()}; TALL={int(k):v for k,v in SS['tall'].items()}
Mm={int(k):v for k,v in json.load(open(f'{B}/data/model4_merges_v3.json')).items()}
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
def mclass(m):
    if m in TALL: return 'tall'
    if m in SHORT: return 'short_stacked' if TIER.get(m,1)>=2 else 'short_linear'
    return None
# Mahadevan
rows=list(csv.DictReader(open(f'{B}/data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
TM={tuple(Mm.get(int(t),int(t)) for t in r['signs_clean'].split() if t!='0') for r in rows if r['signs_clean'].strip() not in ('','0')}
# Wells, mapped to M codes where bridged (unbridged kept as 'W<n>')
TW={tuple(Wm.get(int(x[1:]),int(x[1:])) for x in r['sign_sequence'].split())[::-1] for r in csv.DictReader(open(f'{B}/data/raw/joyboseroy_csv/indus_website_real_corpus.csv'))}  # CSV is written order; reversed to reading order
def colloc(T,tok2m,label):
    out={c:collections.Counter() for c in ('short_linear','short_stacked','tall')}; nfinal=collections.Counter(); ntok=collections.Counter()
    for t in T:
        for i,g in enumerate(t):
            m=tok2m(g); c=mclass(m) if isinstance(m,int) else None
            if not c: continue
            ntok[c]+=1
            if i==len(t)-1: nfinal[c]+=1
            else:
                r=tok2m(t[i+1]); out[c][r if isinstance(r,int) else f'W{t[i+1]}']+=1
    res={}
    for c in out:
        tot=sum(out[c].values()); top=out[c].most_common(12)
        res[c]=dict(tokens=ntok[c],final=nfinal[c],right_neighbours_total=tot,top=[(f'M{k}' if isinstance(k,int) else k,n,round(n/tot,3)) for k,n in top])
        print(f'{label} {c:14s} tokens {ntok[c]:4d} final {nfinal[c]:3d} ({nfinal[c]/max(1,ntok[c]):.0%})  top right: '+', '.join(f'{("M"+str(k)) if isinstance(k,int) else k}:{n}' for k,n in top[:8]))
    return res
R={'mahadevan':colloc(TM,lambda g:g,'IM77 '),'icit':colloc(TW,lambda g:bridge.get(g,f'W{g}'),'ICIT ')}
# overlap of top-8 right neighbours between corpora per class
for c in ('short_linear','short_stacked','tall'):
    a={k for k,_,_ in R['mahadevan'][c]['top'][:8]}; b={k for k,_,_ in R['icit'][c]['top'][:8]}
    print(c,'top-8 overlap between corpora:',len(a&b),'of 8 ->',sorted(a&b))
json.dump(R,open(f'{B}/data/stroke_collocations_v1.json','w'),indent=1)
