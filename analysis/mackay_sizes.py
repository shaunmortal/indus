"""Parse Mackay 1938 FEM vol I seal tables (OCR, one token per line): serial, type, W x H x D (in), material, block, house, room, level ft, field no.
Join: IM77 text_no = 2000 + FEM serial (hypothesis), validated by level. Then replicate F12 on FEM seals."""
import re, csv, json, statistics as st, random, collections
txt=open('data/raw/books/Mackay1938_vol1_text.txt',encoding='utf-8',errors='replace').read().split('\n')
toks=[t.strip() for t in txt[64300:74500] if t.strip()]
def num(s):
    s=s.replace('-','.').replace('°','.').replace(':','.').replace("'",'.').replace('•','.').replace('·','.').replace('o','0').replace('O','0').replace('l','1').replace('I','1')
    s=re.sub(r'^r','1',s)
    if re.fullmatch(r'[12]\d\d',s): s=s[0]+'.'+s[1:]      # OCR dropped the decimal: 105 -> 1.05, 132 -> 1.32
    elif re.fullmatch(r'0\d\d?',s): s='0.'+s[1:]
    elif re.fullmatch(r'[1-9]\d',s): s=s[0]+'.'+s[1:]        # 94 -> 9.4? no: 2-digit without leading 0 is ambiguous; treat as x.y
    try:
        v=float(s); return v if 0.2<=v<=3 else None
    except: return None
rows={}; i=0; n=len(toks)
dimre=re.compile(r"^([oO0-9rIl.:°'•·\-]{1,5})\s*[xX×]?$")
while i<n-6:
    t=toks[i]
    if re.fullmatch(r'\d{1,3}',t) and 1<=int(t)<=1200:
        ser=int(t)
        # look ahead up to 8 tokens for pattern W, X, H (X H may be split or joined)
        win=toks[i+1:i+10]; joined=' '.join(win)
        m=re.search(r"([oO0-9rIl.:°'•·\-]{1,5})\s*[xX×]\s*([oO0-9rIl.:°'•·\-]{1,5})(?:\s*[xX×]\s*([oO0-9rIl.:°'•·\-]{1,5}))?",joined)
        if m:
            w=num(m.group(1)); h=num(m.group(2))
            if w and h:
                # level: first token like "Surface" or a number followed by ft within next 25 tokens; field no: DK/HR + number
                seg=' '.join(toks[i+1:i+30])
                lv=re.search(r'\b(\d{1,2})\s*[-–]?\s*\d?\b(?=[^|]*?(?:DK|HR|VS|SD|L|C|E|B|D)\s*\d{3,5})',seg)
                fn=re.search(r'\b(DK|HR|VS|SD|L|C|E|B|D)\.?\s*(\d{3,5})',seg)
                if ser not in rows: rows[ser]={'w':w,'h':h,'find':(fn.group(1)+' '+fn.group(2)) if fn else '', 'level_raw':seg[:60]}
                i+=3; continue
    i+=1
print("parsed FEM serials:",len(rows),"range",min(rows),max(rows))
print("sample:",[(k,rows[k]['w'],rows[k]['h'],rows[k]['find']) for k in sorted(rows)[:8]])
json.dump({str(k):v for k,v in rows.items()},open('data/mackay_seal_sizes.json','w'),indent=0)
im=list(csv.DictReader(open('data/raw/paragorth/data/im77/im77_corpus_lines.csv',encoding='utf-8')))
im_by={}
for r in im:
    t=int(r['text_no'])
    if 2001<=t<=2952 and r['signs_clean'].strip() not in ('','0'): im_by.setdefault(t,r)
# validation via 'Surface' vs level 0? use field-number presence in IM77 'locus'? IM77 locus is a code. Validate via FEM 'Block' ~ IM77 locus? Try correlation of level: extract 'ft' number right before field no
def level_ft(seg):
    if 'Surface' in seg: return 0
    m=re.search(r'-\s?(\d{1,2})[-.](\d)\s*(?:ft|tt|ff|\'|»|>)?',seg)
    return int(m.group(1)) if m else None
pairs=[]
for ser,v in rows.items():
    r=im_by.get(2000+ser)
    if not r: continue
    ft=level_ft(v['level_raw'])
    if ft is not None and r['level'].lstrip('-').isdigit(): pairs.append((ft,-int(r['level'])))
print("depth pairs:",len(pairs)," exact match share:",round(sum(1 for a,b in pairs if a==b)/max(1,len(pairs)),2))
print("cross-tab:",{k:collections.Counter(b for a,b in pairs if a==k).most_common(3) for k in sorted(set(a for a,_ in pairs))[:10]})
# F12 replication
random.seed(8); recs=[]
for ser,v in rows.items():
    r=im_by.get(2000+ser)
    if not r or r['object_type']!='seal': continue
    recs.append(([int(t) for t in r['signs_clean'].split()], v['w']*v['h']*645.16))
print("\nFEM seals with size+text:",len(recs),"median area mm2:",round(st.median(a for _,a in recs)))
L=lambda s:min(len(s),8); strata={}
for i,(s_,a) in enumerate(recs): strata.setdefault(L(s_),[]).append(i)
med={k:st.median(recs[i][1] for i in v) for k,v in strata.items()}
resid=[recs[i][1]-med[L(recs[i][0])] for i in range(len(recs))]
for sign,name in [(343,'M343 handled jar'),(342,'M342 plain jar'),(161,'M161 tree'),(176,'M176'),(169,'M169'),(387,'M387')]:
    w=[resid[i] for i in range(len(recs)) if sign in recs[i][0]]; wo=[resid[i] for i in range(len(recs)) if sign not in recs[i][0]]
    if len(w)<5: print(f"{name}: n={len(w)} too few"); continue
    obs=st.mean(w)-st.mean(wo); cnt=0
    for _ in range(4000):
        ph=set()
        for k,idx in strata.items():
            m=sum(1 for i in idx if sign in recs[i][0]); ph.update(random.sample(idx,m))
        d=st.mean(resid[i] for i in ph)-st.mean(resid[i] for i in range(len(recs)) if i not in ph)
        if abs(d)>=abs(obs): cnt+=1
    print(f"{name}: n_with={len(w)} delta={obs:+.0f} mm2 ({obs/st.median(a for _,a in recs):+.0%}) perm p={cnt/4000:.4f}")
