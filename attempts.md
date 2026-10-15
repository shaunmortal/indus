# 100 years of Indus script attempts — map (v0, 2026-10-15)

Purpose: know what was tried, why it did not convince, so we never repeat a dead end unknowingly.

## Foundational data work (not decipherments)
| Who | Year | What | Status |
|---|---|---|---|
| Mahadevan (M77) | 1977 | Concordance, 417 signs, ~2900 texts, 14k tokens. ASI publication. | Standard reference; scan on archive.org; digitized copies on GitHub |
| Parpola et al. (CISI) | 1987-2010 | Corpus of Indus Seals and Inscriptions, photo volumes, ~398 P-signs | Images; partial hand digitization (mayig repo) |
| Wells (ICIT) | 2006-2011 | Interactive Corpus of Indus Texts, ~676 signs, 5500+ texts, hosted TU Berlin / indus.epigraphica.de | Access by request (Fuls). Partial dump via yajnadevam/indus-website, 2543 texts, 592 G-signs |
| Fuls | 2022 | Corpus of Indus Inscriptions (book, 5500+ texts) | Not open |

Problem: three incompatible sign lists (M, P, G). No full public concordance. paragorth repo claims a bridge of 143 signs only.

## Structural / statistical claims
| Who | Year | Claim | Why not decisive |
|---|---|---|---|
| Rao, Yadav, Vahia et al. | 2009 (Science) | Conditional entropy of sign sequences sits in the range of natural languages, not of non-linguistic systems | Sproat, Farmer et al. showed non-linguistic systems can mimic it; measure is non-specific |
| Yadav et al. | 2010 | n-gram / Markov model, segmentation, some predictability | Shows structure, not language |
| Sinha et al. | 2010 | Network analysis of sign co-occurrence shows syntactic-like organization | Same objection |
| Farmer, Sproat, Witzel | 2004 | "Collapse of the Indus-script thesis": texts too short, too many rare signs, no long texts, no scribal equipment -> not writing | Influential but contested; proposes nonlinguistic symbol system |
| Nair | 2026 (arXiv 2604.17828) | Synthetic heraldic & administrative baselines; Indus sits between them, matches neither cleanly | Discrimination test, not verdict |
| Raghavendra | 2026 (arXiv 2608.02999) | SIGIL: a generated emblem system with no phonology reproduces all "Indus-like" statistics | Kills statistics-only arguments for language; demands grouped held-out + key-stability tests |
| Kriger & Hunt (with Claude) | 2026 | Positional entropy -> "structured registration code, not writing" | Preprint |

Takeaway: entropy / Zipf / positional stats CANNOT prove language. Any proof must be prediction on held-out texts.

## Decipherment claims
| Who | Language | Core idea | Why rejected / unresolved |
|---|---|---|---|
| Parpola | Dravidian | Rebus readings (fish = min = star), astral names | Internally rich, but unfalsifiable; few signs, no hold-out test |
| Mahadevan | Dravidian | Similar, Old Tamil affinities | Same |
| Rao (S.R.) | Indo-Aryan | Alphabet-like, Sanskrit | Late, dismissed |
| Yajnadevam (B. Rao) | Sanskrit | Treat corpus as cryptogram, search mapping maximizing dictionary hits (Monier-Williams) vs ICIT | Not peer-reviewed; "mathematical proof" disputed; author later conceded errors; another 2026 preprint agrees with 0/34 of his readings |
| Pierson | Proto-Dravidian | 185 computational phonetic readings, two corpora | Preprint May 2026; author retracted 3 claims after finding pipeline bugs; awaits Dravidianist review |
| paragorth (anon, solo + AI) | unknown | Open DB, preregistered predictions (Jul & Sep 2026), validator on unseen texts | Honest; records failures. KEY NEGATIVE RESULT: when only common signs are decoded, wrong keys beat the true key under every objective tested; only a small (~80-sign) syllabary makes the true key optimal |
| Lengyel | n/a | Transformer to predict pronunciations (self-published) | Proposal only |

## Directly relevant 2026 theory to engage (found 2026-10-15 while locating Frenez)
- Frenez, D. 2026, 'Branding Authority: Further Considerations on the Oligopolistic Nature of the Indus Seal-Based Administrative System', Archaeologies (WAC), SSRN 6103846 (Jan 2026; author listed as Independent; also Subject Expert, Univ. Bologna DISCI; lecturer Padua 2026-27). Thesis: seals = institutional branding instruments within a heterarchy; extreme standardisation; unicorn dominance = stable unbalanced oligopoly; seals are 'procedural instruments of institutional recognition' rather than emblematic identities. OUR DATA SPEAK TO THIS: F26 (96% of seal texts unique = individual recognition), F14 (no sign-motif coupling = text and brand are separate channels), F19 (round seals = a second tradition), F27 (repeated title strings on smaller seals). Cite and discuss in paper v0.4; this is the right reader.
- Frenez talk, Oct 2026 (YouTube): 'Ongoing decipherments: Writing in the Indus Civilization'.

## Lessons we must bake in
1. Statistics prove structure, not language. Do not spend time re-proving entropy.
2. Dictionary-hit maximization (Yajnadevam-style) is a trap: with a big dictionary and partial key, wrong keys win. Need key-stability + grouped hold-out.
3. Sign list identity is itself unsolved (417 vs 592 vs 676). Allograph merging decisions change every downstream result. This is upstream of everything.
4. External anchors are the only route to a Ventris moment. CORRECTION 2026-10-15: Parag Garg (paragorth, Sept 2026) already pulled 214 CDLI Meluhha attestations and the Gulf/Ur/Failaka seals. Findings: Meluhhan people in cuneiform carry Mesopotamian names; at Ur no tablet with an Indus seal impression is published; ~40 foreign-found Indus texts break home grammar. Anchor not found, but the search space is mapped.
6. paragorth planted-language test (S113-S121): statistical key-fitting cannot recover even a KNOWN planted language on this corpus. Readings can only come sign by sign from outside. This is the single most important constraint on our plan.
5. The field in 2025-26 is crowded with solo+AI statistical attempts. Being unique requires a new HANDLE, not better statistics.
