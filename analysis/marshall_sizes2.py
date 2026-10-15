"""Second-pass Marshall parser: higher recall. Strategy: find every 'serial  W x H' occurrence anywhere on a line
(two table columns per OCR line), with a permissive size token class; keep the first size seen per serial; sanity-filter sizes."""
import re, json, csv, statistics as st
txt=open('data/raw/books/Marshall1931_vol2_text.txt',encoding='utf-8',errors='replace').read().split('\n')
starts=[i for i,l in enumerate(txt) if 'TABULATION OF SEALS' in l.upper()]
lines=txt[starts[1]-3:starts[1]+1400]
TOK=r"[oOœ0-9rIl.:°•'·\-]{1,6}"
def fix(s):
    s=s.replace('œ','0.').replace('-','.').replace('°','.').replace(':','.').replace("'",'.').replace('•','.').replace('·','.')
    s=s.replace('o','0').replace('O','0').replace('I','1').replace('l','1')
    s=re.sub(r'^r0?s$','1.05',s); s=re.sub(r'^r','1',s); s=s.replace('..','.')
    if re.fullmatch(r'[12]\d\d',s): s=s[0]+'.'+s[1:]
    elif re.fullmatch(r'0\d\d?',s): s='0.'+s[1:]
    elif re.fullmatch(r'\d\d',s): s=s[0]+'.'+s[1:]
    elif re.fullmatch(r'\d',s): s='1.0' if s=='1' else '0.'+s
    try:
        v=float(s); return round(v,2) if 0.4<=v<=2.0 else None
    except: return None
pat=re.compile(r'(?<![\d.])(\d{1,3})\s*[|\[\]Il!]?\s*('+TOK+r')\s*[xX×]\s*('+TOK+r'|\?)')
rows={}
for l in lines:
    for m in pat.finditer(l):
        ser=int(m.group(1))
        if not 1<=ser<=600: continue
        w=fix(m.group(2)); h=None if m.group(3)=='?' else fix(m.group(3))
        if w and ser not in rows: rows[ser]={'w':w,'h':h}
print("serials parsed:",len(rows)," (first pass had 116)")
# sanity: square seals should have w~h; report share within 15%
sq=[(v['w'],v['h']) for v in rows.values() if v['h']]
print("share with |w-h|/w <= 0.15:",round(sum(1 for w,h in sq if abs(w-h)/w<=0.15)/len(sq),2)," median w:",st.median(v['w'] for v in rows.values()))
old=json.load(open('data/marshall_seal_sizes.json'))
agree=[(k,old[k]['w'],rows[int(k)]['w']) for k in old if int(k) in rows]
print("overlap with first pass:",len(agree)," agreeing on w:",sum(1 for k,a,b in agree if abs(a-b)<0.03))
json.dump({str(k):v for k,v in rows.items()},open('data/marshall_seal_sizes.json','w'),indent=0)
