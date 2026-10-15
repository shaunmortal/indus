"""Phase 1 baseline: reproduce well-known corpus statistics on each open corpus."""
import csv, sys, math
from collections import Counter

def load(path):
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    seqs = [r['sign_sequence'].split() for r in rows if r.get('sign_sequence','').strip()]
    return rows, seqs

def entropy(counter):
    n = sum(counter.values())
    return -sum(c/n*math.log2(c/n) for c in counter.values())

def cond_entropy(seqs):
    big = Counter(); uni = Counter()
    for s in seqs:
        for a, b in zip(s, s[1:]):
            big[(a,b)] += 1; uni[a] += 1
    n = sum(big.values())
    return -sum(c/n*math.log2(c/uni[a]) for (a,_),c in big.items())

for path in sys.argv[1:]:
    rows, seqs = load(path)
    toks = [t for s in seqs for t in s]
    signs = Counter(toks)
    lens = Counter(len(s) for s in seqs)
    first = Counter(s[0] for s in seqs if s)
    last = Counter(s[-1] for s in seqs if s)
    hapax = sum(1 for c in signs.values() if c == 1)
    print(f"\n=== {path.split('/')[-1]} ===")
    print(f"inscriptions={len(seqs)} tokens={len(toks)} unique_signs={len(signs)} hapax={hapax} ({hapax/len(signs):.0%})")
    print(f"mean_len={len(toks)/len(seqs):.2f} max_len={max(lens)} len_dist(1..10)={[lens.get(i,0) for i in range(1,11)]}")
    print(f"unigram_entropy={entropy(signs):.2f} bits  conditional_entropy={cond_entropy(seqs):.2f} bits")
    top = signs.most_common(10)
    print("top10 signs:", ", ".join(f"{s}:{c}" for s,c in top))
    print("top5 FIRST:", ", ".join(f"{s}:{c}" for s,c in first.most_common(5)))
    print("top5 LAST :", ", ".join(f"{s}:{c}" for s,c in last.most_common(5)))
    # how concentrated is the terminal position?
    print(f"top1 last sign covers {last.most_common(1)[0][1]/len(seqs):.0%} of inscriptions")
    sites = Counter(r.get('site','?') for r in rows)
    print("sites:", ", ".join(f"{s}:{c}" for s,c in sites.most_common(6)))
    dirs = Counter(r.get('reading_direction','?') for r in rows)
    print("direction:", dict(dirs))
