"""Phase 2A/2B: sign x AREA and sign x PERIOD at Mohenjo-daro and Harappa (merged corpus, reading order).
Distinct (text, area) objects; strata = object class x text length; permutation of group labels within strata; Bonferroni."""
import json, collections, random, re
mc=json.load(open('data/raw/paragorth/data/derived/merged-corpus-reading-order.json'))
bridge={int(k):v['M'] for k,v in json.load(open('data/bridge_WM.json')).items()}
random.seed(21)
def norm_area(site,r):
    a=str(r.get('area-section','')).strip()
    if site=='Mohenjo-daro':
        M={'DKG. (S)':'DK-G South','DKG. (N)':'DK-G North','DKG':'DK-G','DKC':'DK-C','DKE':'DK-E','DKB':'DK-B','DKA':'DK-A','DKD':'DK-D','DKH':'DK-H',
           'HRB':'HR','HRA':'HR','HR-':'HR','HRC':'HR','VSA':'VS','VS-':'VS','VSB':'VS','SD-':'SD','L-':'L','LB':'L','LC':'L','LD':'L'}
        return M.get(a)
    if site=='Harappa':
        if a in ('--','-',''): return None
        if a.startswith('ET'): return 'Mound ET'
        if a.startswith('EC') or a.startswith('EB'): return 'Mound E'
        if a.startswith('E'): return 'Mound E'
        if a.startswith('F'): return 'Mound F'
        if a.startswith('AB'): return 'Mound AB'
        if a.startswith('D'): return 'Mound D'
        return None
    return None
def norm_period(site,r):
    if site=='Mohenjo-daro':
        p=str(r.get('period','-')).strip()
        return p if p in ('Early','Intermediate','Late') else None
    if site=='Harappa':
        t=str(r.get('time','-'))
        m=re.search(r'Period (3B|3C|3B/C)',t)
        return m.group(1) if m and m.group(1)!='3B/C' else None
    return None
def run(site,labelf,name,min_group=60,min_sign=20,n_perm=2000):
    items=[]; seen=set()
    for r in mc:
        if r['site']!=site or not r['seq']: continue
        g=labelf(site,r)
        if not g: continue
        k=(tuple(r['seq']),g,r['type'].split(':')[0])
        if k in seen: continue
        seen.add(k); items.append((tuple(r['seq']),g,r['type'].split(':')[0]))
    gc=collections.Counter(g for _,g,_ in items); groups=[g for g,c in gc.items() if c>=min_group]
    items=[it for it in items if it[1] in groups]
    print(f"\n=== {site} x {name}: {len(items)} distinct objects; groups {dict(collections.Counter(g for _,g,_ in items))}")
    strata=collections.defaultdict(list)
    for i,(s,g,t) in enumerate(items): strata[(t,min(len(s),7))].append(i)
    strata={k:v for k,v in strata.items() if len(v)>=5}; keep=[i for v in strata.values() for i in v]
    signs=collections.Counter(w for i in keep for w in set(items[i][0]))
    tests=[]
    for g in groups:
        isG={i:items[i][1]==g for i in keep}
        for w,n in signs.items():
            if n<min_sign: continue
            has={i:(w in items[i][0]) for i in keep}
            obs=sum(1 for i in keep if has[i] and isG[i])
            if obs<5: continue
            cnt=0; exp=0
            for _ in range(n_perm):
                ph=set()
                for k,idx in strata.items():
                    m=sum(1 for i in idx if has[i]); ph.update(random.sample(idx,m))
                d=sum(1 for i in ph if isG[i]); exp+=d
                if d>=obs: cnt+=1
            tests.append((cnt/n_perm,g,w,n,obs,exp/n_perm))
    tests.sort(); bon=0.05/max(1,len(tests))
    print(f"  {len(tests)} tests, Bonferroni {bon:.5f}; survivors marked *")
    for p,g,w,n,obs,exp in tests[:10]:
        print(f"  {'*' if p<bon else ' '} p={p:.4f}  {g:14} W{w}(M{bridge.get(w,['?'])[0]})  sign n={n:3}  in group obs={obs:3} exp={exp:5.1f}  ratio={obs/exp:.2f}")
run('Mohenjo-daro',lambda s,r:norm_area(s,r),'AREA')
run('Harappa',lambda s,r:norm_area(s,r),'MOUND')
