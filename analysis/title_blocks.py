"""Title-block inventory (deliverable named in paper v0.4 section 6; basis F28).
Unique square-seal texts >= 5 signs (merged corpus, Wells v3 codes). Opener/closer classes from M1b (K=3).
core = text with leading opener-class signs and trailing closer-class signs stripped.
A title block = the last 3 signs of a core shared by >= 3 unique texts. For each block: count, closers that follow it,
sites, and the individual parts (the core before the block). Writes data/title_blocks_v1.json."""
import json, collections
B='/Users/Happy/Desktop/plugins/indus'
Wm={int(k):v for k,v in json.load(open(f'{B}/data/model5_merges_wells_v3.json')).items()}
bridge={int(k):v['M'][0] for k,v in json.load(open(f'{B}/data/bridge_WM.json')).items() if v['M']}
cl=json.load(open(f'{B}/data/model1b_consensus_classes.json'))['classes']
CLOSER=set(cl['0']); OPENER=set(cl['1'])
mc=json.load(open(f'{B}/data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
objs=collections.defaultdict(list)
for r in mc:
    if r['type']=='SEAL:S' and len(r['seq'])>=3: objs[tuple(Wm.get(w,w) for w in r['seq'])].append(r['site'])
uniq={t:s for t,s in objs.items() if len(s)==1 and len(t)>=5}
def split(t):
    i=0
    while i<len(t)-1 and t[i] in OPENER: i+=1
    j=len(t)
    while j>i+1 and t[j-1] in CLOSER: j-=1
    return t[:i],t[i:j],t[j:]
blocks=collections.defaultdict(list)
for t,s in uniq.items():
    op,core,clo=split(t)
    if len(core)>=3: blocks[core[-3:]].append(dict(text=list(t),individual=list(core[:-3]),closer=list(clo),site=s[0]))
inv=[]
for b,items in blocks.items():
    if len(items)<3: continue
    inv.append(dict(block_W=list(b),block_M=[bridge.get(w) for w in b],n_names=len(items),
        closers=collections.Counter(tuple(i['closer']) for i in items).most_common(3),
        sites=sorted(collections.Counter(i['site'] for i in items).items(),key=lambda x:-x[1]),
        individual_parts=[i['individual'] for i in items],
        distinct_individuals=len({tuple(i['individual']) for i in items})))
inv.sort(key=lambda x:-x['n_names'])
json.dump(dict(basis='F28; unique square-seal texts >=5 signs; Wells v3; M1b classes; min 3 names per block',
    n_unique_texts=len(uniq),n_blocks=len(inv),blocks=inv),open(f'{B}/data/title_blocks_v1.json','w'),indent=1)
print('unique texts',len(uniq),'blocks',len(inv),'names covered',sum(x['n_names'] for x in inv))
for x in inv[:12]: print(x['block_W'],x['block_M'],'n',x['n_names'],'closers',x['closers'][:2],'sites',x['sites'][:3],'indiv distinct',x['distinct_individuals'])
