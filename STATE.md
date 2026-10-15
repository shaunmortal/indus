# Indus Script Decipherment — Project State

**Owner:** Ayush Kumar (India). Credit goes to Ayush. Claude assists.
**Locked:** 2026-10-15
**Goal (final, no compromise):** Read the Indus script in a way archaeologists accept.
Milestones (sign grammar, corpus tools, papers) are steps, never the goal.

## Rules
- DEDUPLICATE FIRST. Harappa miniature tablets and sealings repeat one text dozens of times. Every count must be reported on distinct texts as well as tokens, or it is not a result. (Learned the hard way on F7, 2026-10-15.)
- No alternate goal. No pivot. If stuck, go deeper, not sideways.
- Every claim must be reproducible from the corpus. No hand-waving.
- Always track what was tried and why it failed (see Failures).

## Status
- [x] Phase 0: Download open corpora (done 2026-10-15, see Data inventory)
- [x] Phase 0: Map attempts -> attempts.md (v0)
- [x] Phase 1: Reproduce known results -> analysis/stats0.py (entropy, terminal sign, lengths all match literature)
- [ ] Phase 0b: Build M <-> G <-> P sign concordance (upstream blocker; paragorth bridge covers 143 signs only)
- [ ] Phase 0c: Normalize reading direction (website corpus is stored L-R as seen; M77 is in reading order R-L; G740 appears FIRST in website corpus but its equivalent M342 appears LAST in M77 -> reverse website sequences)
- [x] Phase 0d: paragorth key files fetched (34 files, data/raw/paragorth/). Full Mahadevan corpus WITH site/object/level/direction: data/raw/paragorth/data/im77/im77_corpus_lines.csv (3916 lines, 2906 texts). Use THIS as the master corpus.
- [x] Phase 2: 30% hold-out sealed (analysis/holdout.py, seed 20261015, stratified site x type): 966 of 3241 distinct texts. SHA-256 950c22bd56781dd60f9f00347e360fb3cc961d71b4712074b66973407fbab1ec. PUBLIC TIMESTAMP DONE 2026-10-15: https://github.com/shaunmortal/indus commit e332532 (merge f52df84) holds data/holdout/holdout.sha256. Do NOT read holdout.json in any analysis.

## Done
- Problem chosen, explained to Ayush with real-world analogy.
- 2026-10-15: corpora downloaded, baseline stats reproduced, attempts map written.

## Data inventory (data/raw/)
| File | Source | Inscriptions | Signs | Scheme | Notes |
|---|---|---|---|---|---|
| joyboseroy_csv/m77_indusscript_real_corpus.csv | Mahadevan 1977 via indusscript.in | 3573 lines | 418 | MSg### | R-L reading order; no site info; M342 (jar) terminal in 27% |
| joyboseroy_csv/indus_website_real_corpus.csv | ICIT via yajnadevam dump | 2543 | 592 | G### | has site, object, cisi_number; stored L-R (needs reversal) |
| joyboseroy_csv/cisi_real_corpus.csv | Parpola CISI via mayig | 179 | 182 | P### | Mohenjo-daro unicorn seals only |
| joyboseroy/ | full repo (MIT) | | | | falsification toolkit, null models, converters |
| mayig/ | full repo | | | | CISI hand digitization, Rust tooling, per-sign feature JSON |

Baseline numbers (stats0.py): M77 cond. entropy 3.37 bits, ICIT 3.74 bits; mean length ~4; hapax 27-34%; longest 19.

## Failures / dead ends
- git clone of paragorth/Indus- fails (early EOF). Use zip archive instead.
- (inherited, from literature) statistics-only arguments for language: refuted by Raghavendra 2026 SIGIL. Do not pursue.
- (inherited, paragorth 2026) dictionary-hit maximization with partial key: wrong keys beat true key. Do not pursue without key-stability test.

## Where the problem stands after Phase 0 (2026-10-15)
Reduced to one sentence: **find one physical object that ties an Indus sign-string to a word in a readable script (cuneiform, Linear Elamite, Proto-Elamite) or to a countable quantity.**
Everything else (entropy, key search, dictionary fitting) has been tried in 2026 by solo+AI teams and shown not to work (paragorth: statistical key-fitting fails even on a planted known language).
Our edge must be an anchor, not statistics. Candidate places to look:
- Indian museum/ASI reserve collections: unpublished inscribed objects, bilingual-context finds (Lothal, Dholavira, Rakhigarhi 2011-17, Kalibangan storerooms).
- Pakistan/Oman/Bahrain/Iran excavation reports for Indus seals found in sealed archive contexts.
- Indus weights + stroke-numerals on tablets as a numeric anchor (paragorth flagged, not resolved).
- Sign-identity work (allographs) using sign IMAGES not hand lists: indusscript.in holds a drawing per sign; CISI photos. A better sign list changes every downstream count.

## Findings log
### F1 (2026-10-15) Numerals are NOT concentrated on accounting objects — analysis/numerals1.py
Share of lines containing a numeral sign: seals 36%, sealings 31%, miniature tablets 38%, copper tablets 42%, pottery 31%. Flat across object types.
If strokes were quantities of goods, they should pile up on sealings/tablets, not on personal seals. They do not. => numerals on seals behave like parts of names/titles ("number-names"), consistent with Parpola; now shown from data.
### F2 (2026-10-15) Tall and short strokes count DIFFERENT things
After TALL strokes (M86/87/89): M328 (209x), M59, M211, M342. After SHORT strokes: M162, M169, M59, M287, M194. Two separate systems. M328 is preceded by a numeral 65% of the time, M190 95% (n=22): best "unit/measure-word" candidates. Tall strokes attest only 1,2,3; short attest 1,3-7 (2-short = M99/100 is a connective, 728 tokens, excluded).
Open question: are tall strokes numerals at all, or classifiers? Test: do tall-stroke counts vary while the following sign stays fixed, per site?

### F3 (2026-10-15) India 2010-2026 sweep: no bilingual, no inscribed weight, no sealing with known contents (research/india_finds_2010-2026.md)
Best leads: Dholavira Bisht 2015 report (~150 inscriptions, many first-published -> natural hold-out set); Kanmer 3 tablets with same seal + different incised texts (fixed identity + variable field).

### F4 (2026-10-15) Gulf/Iran/Central Asia sweep: no sealed document with an Indus-sign seal impression exists in print (research/gulf_iran_sealings.md)
Only Indus-seal impression on a container abroad: Salut ST1 jar sherd (Oman). Authoritative unseen checklist: Parpola 1994 in Qala'at al-Bahrain vol.1 (library only).

### F5 (2026-10-15) Wells' "tall stroke = 10, short = 1" hypothesis fails three data tests — analysis/numerals2.py
1. Compound numeral pairs have no fixed order: tall-then-short 18, short-then-tall 7, tall-tall 15, short-short 21. Place-value numbers would show one order and no TT/SS compounds (T3-T3 occurs 7x, S1-S4 5x).
2. Short-stroke values are not a quantity distribution: 1=179, 3=181, 4=72, 5=44, 6=41, 7=76. Peaks at 3 and 7 = "favourite numbers", typical of names/formulae, not counts. Tall: 1=149, 2=365, 3=314 (2 and 3 beat 1).
3. Complementary distribution: M328 is counted ONLY by tall strokes (209 vs 0), M287/M25/M190 ONLY by short. If tall were tens of the same unit, M328 would also appear with ones.
=> Tall and short strokes are two different sign classes, not two digit positions. Numerals on seals are formulaic/onomastic. The agent's literature sweep confirms nobody has published tests 1-3 (research/numerals_weights_lit.md, gaps list).
Caveat: two-tier short-stroke signs (8-12) and semicircle "tens" not yet included; add before publishing.

### F6 (2026-10-15) Umma 2017 seal = surface find, 2 Indus signs, no cuneiform. Paris BnF seal = cuneiform only ("servant of Nin-ildum son of Ur-gi"), no Indus signs. (research/umma_paris_seals.md)
=> After four sweeps (India, Gulf/Iran/C.Asia, Mesopotamia, numerals/weights): NO published object on Earth carries Indus signs together with a readable script. The bilingual does not exist in print. Confirmed independently of paragorth.

### F7 (2026-10-15) Stroke-group LAYOUT matters more than stroke COUNT — analysis/numerals3.py, numerals4.py
Complete stroke inventory read from Mahadevan's drawings: data/stroke_signs.json (short 1-12 incl. two- and three-tier forms; tall 1-5; chevrons).
- Two-tier forms are NOT allographs of one-row forms of the same count. M103 (3 as 2-over-1) is followed by M403 in 27/28 cases (96%); M102 (3 in a row) spreads over M59/M162/M190 (top 15%). M112 (7 as 4-over-3) -> M194/M197; M110 (7 in a row) -> M342. Cosine of follower distributions: 0.00-0.33, vs 0.64 for the DIFFERENT tall counts M87 vs M89.
- Null check: cos<=0.05 occurs in 45% of random sign pairs, so the allograph claim rests on the fixed-compound evidence, not on cosine alone.
- Tall-stroke gradient: share followed by M328 rises with count: 1 tall 9%, 2 tall 23%, 3 tall 44%, 4 tall (M95) 97%. 4-tall + M328 is a fixed compound (58/60).
- Short-2 (M99, 649 tokens, 96% mid-text) is a connective, not a numeral: follower similarity to 3/4/5/7-strokes is 0.00-0.10.
- 12 (M121, 4-4-4) has 70 tokens, more than 8+9+10 combined (12). A favoured fixed sign, not a count.
CORRECTION after replication (analysis/numerals5.py, per site / per object / distinct texts):
- M103->M403 HOLDS: Mohenjo-daro 6/6, Harappa 18/18, seals 9/10, sealings 4/4, tablets 12/12; distinct texts 11/12. Real fixed compound.
- M95->M328 (4 tall) and the tall-stroke gradient are a DUPLICATION ARTIFACT: 45/46 of M95->M328 are Harappa miniature tablets repeating one text. On distinct texts M89->M328 drops 44% -> 6%, M87->M328 23% -> 2%. Withdrawn.
- M112->M194 is object-specific (copper tablets 10/10, seals 34%). Moderate.
=> Surviving claim: layout carries information for at least one value (3 one-row vs 3 two-tier are different signs: M102 productive, M103 bound to M403). Smaller than first stated, but solid. Mahadevan's separate numbering is vindicated for 102/103.

### Dedup confirmation (2026-10-15, analysis/numerals6.py; 2409 distinct texts of 3548 lines)
- F1 HOLDS and strengthens: distinct texts with a numeral: seals 56%, sealings 40%, miniature tablets 41%, pottery 46%, copper tablets 48%. Personal seals carry MORE numerals than accounting objects.
- F5 HOLDS: short values 1=153, 3=114, 4=54, 5=34, 6=30, 7=64, 8=7, 9=4, 10=1, 12=52 (peaks at 7 and 12); tall 1=134, 2=249, 3=182. Compound orders TT12 ST9 SS32 TS17 (no fixed order).
- F2 HOLDS: complementary counted items on distinct texts: tall-only M211 (42/2), M328 (20/0), M60 (13/0), M244 (11/0), M284 (11/0), M249 (18/2); short-only M287 (0/25), M25 (0/10), M190 (1/13), M162 (6/38), M169 (5/36), M194 (2/19). Shared: M59, M342, M15.
### F8 (2026-10-15) Independent replication on ICIT/Wells corpus (1918 distinct texts, G-signs via bridge) — analysis/numerals7_icit.py
Test 2: short 1=140, 3=116, 4=55, 5=30, 6=28, 7=46, 8=6, 12=36 (peaks at 7 and 12 again); tall 1=131, 2=227, 3=151.
Test 3: compound orders SS27 TT21 TS21 ST8 (no fixed order).
Test 4: tall-only G520/M211 40 vs 3, G226/M60 13 vs 1, G590/M249 17 vs 3; short-only G900/M287 0 vs 23, G390/M161 3 vs 47, G407/M169 1 vs 16, G575/M197 1 vs 13. Same split, independent transcription.
Numeral note drafted: research/note1_numerals_draft.md (F8 added).
Semicircle 'tens' signs: not in M362-417 (those are leaf/oval signs, contact sheet analysis/img/signs_362_417.png). Still to locate in M192-361.

### Data (2026-10-15 evening): ICIT open database extracted
From paragorth repro package (yajnadevam/indus-website SQL): data/icit_seal.csv (2543 seals: site, material, CISI number for 2375, museum for 299, dimensions for 2305), icit_site.csv (52 sites), icit_iconography.csv (1622), icit_inscription.csv (direction/completeness), icit_glyph.csv (G-sign -> font PUA codepoint). CISI numbers = the key for aligning ICIT texts with M77 and with CISI photos.

### Sources map (research/sources_online.md)
Downloading to data/raw/books/: Mahadevan 1977 full book (36 MB), Gadd 1932 Ur seals. CISI vol.1 & 2 photo PDFs available at same archive.org item (not yet pulled). Parpola 1994 QAB catalogue: library only. Laursen 2010 / Crawford 2001 / Pittman 2013: need browser (harappa.com, academia.edu, ADS).
Merged corpus (paragorth data/derived/merged-corpus-reading-order.json): 5369 objects keyed by CISI number with site, type, material, Wells seq — the cross-corpus backbone.

### F9 (2026-10-15) No diachronic trend — analysis/diachronic1.py
Harappa distinct texts with a stroke sign by period: 3B 31% (n=71), 3B/C 31% (n=372), 3C 38% (n=310). Stable. Period samples too small for the tall/short split; 3C shows W520/M211 T8/S1 and W900/M287 T0/S8, same direction as corpus-wide.
### Lead closed: Dholavira hold-out
ICIT/merged corpus already holds 203 Dholavira objects (190 distinct texts: 79 square seals, 53 tags, 31 round seals, 15 tablets). Bisht 2015's "scores published for first time" are mostly already transcribed by Wells. A hold-out must come from post-2015 finds or from the sealed 30% split, not from Dholavira.

### Books on disk (data/raw/books/)
Mahadevan1977.pdf (36 MB), Gadd1932_Ur_seals.pdf (3 MB), CISI_vol1_India.pdf, CISI_vol2_Pakistan.pdf (photo volumes; use for sign-image / allograph work).

### F10 (2026-10-15) Three odd objects resolved (research/odd_objects.md)
Lothal L-56 = stylus wedges, Indus-only. Failaka "bilingual" = fringe, object never identified. Susa text O (Louvre Sb 9382) = unknown/aberrant Linear Elamite, 43 signs, only 2 read, Indus link unverified. ONE cheap computational lead: shape-compare text O's 43 signs with our 418 Mahadevan drawings (Louvre has 5 downloadable hi-res images).

### F11 (2026-10-15) Museum collections + 2018-2026 finds abroad: nothing (research/hybrid_seals_new_finds.md)
Six sweeps complete. Zero objects on Earth, published, with Indus signs + readable script. Zero new Indus-inscribed objects abroad since 2018. Bahrain 2026 tokens (Kanmer-like shape, cuneiform legends) show the admin technology crossed the Gulf; the script did not.
Watch list: Failaka F6 2025 temple seals (unpublished); Konar Sandal resumed 2023; Rakhigarhi ASI 2022-24 seals (unpublished).

## Standing order (Ayush, 2026-10-15)
Do not stop. Every session: continue "Next". Final report must be "Badhai ho Ayush" (with proof passing the protocol) or "Sorry Ayush" (with the complete map of everything searched). No fake Badhai.

## Where we stand after Day 1 (2026-10-15)
Anchor routes closed in print: Ur archives, Bahrain/Failaka sealings, Umma, Paris, YBC 5447, Linear Elamite look-alikes.
Anchor routes still open: (1) unpublished Dholavira inscriptions as hold-out; (2) Kanmer same-seal/different-text tablets; (3) weights datasets (PNAS 408, Ascalone 900) joined to inscriptions; (4) Salut ST1 stamped jar; (5) Parpola 1994 QAB catalogue (library); (6) Lothal seal with cuneiform-style wedges (Frenez 2023 fig.12D).
Our own data results so far: F1, F2, F5 (numerals are formulaic, two stroke classes, Wells' tens hypothesis fails). None published elsewhere in this form.

## Next (in order)
1. Complete F5: add two-tier strokes and semicircle signs; run per-site. Write it up as a 2-page note under Ayush's name.
2. Download PNAS 2021 Dataset S1; test whether stroke-count sets match weight-denomination sets per commodity sign.
3. (done) Repo public: https://github.com/shaunmortal/indus. Commit after every session.
4. (started) M<->W concordance: analysis/concord1.py, concord2.py. Text-alignment voting (same site, same length, seed-consistent, unique match, >=3 unanimous votes) added 23 pairs to paragorth's 142 -> data/bridge_WM.json, 165 signs, 86.2% of ICIT tokens covered. Plateaus at iteration 2; to grow further relax to length>=2 texts or resolve ambiguous matches. P-signs: paragorth repro bridge.json gives W<->P<->M for 85 signs with shape descriptions (data/raw/paragorth/data/repro/repro/data/bridge.json). Merge into bridge_WM.json next.
5. Susa text O shape comparison. Plate downloaded (data/raw/susa/, Hinz 1969 Taf.15 photo + colour photo). Viewed: 8 ruled columns, boxed geometric signs (X-in-square, circle-dot, comb/rake, D-shape). Looks like its own script, Proto/Linear-Elamite layout; a few shapes superficially Indus-like. Low prior. Do the shape test only after items 1-4; needs a permutation baseline or it proves nothing.
6. Check CISI vol.1 entry L-56 (we have the PDF).

## Failures (Day 1 evening)
- ancientportsantiques.com "Dholavira-Bisht2015.pdf" is NOT the ASI report: it is a 115-page fringe commentary (rebus "cipher" blog) with excerpts. Real report: Scribd doc/262316120 (needs browser) or ASI. Do not cite the PDF we have.
- PNAS 2021 Dataset S1 (weights) download blocked by PMC JS proof-of-work interstitial; curl returns "Preparing to download". Use Chrome tool or manual download later. URL: https://pmc.ncbi.nlm.nih.gov/articles/instance/8271817/bin/pnas.2105873118.sd01.xlsx
- Tooling: system python3 lacks PIL; project venv at indus/.venv (pillow, openpyxl, pypdf). Always call /Users/Happy/Desktop/plugins/indus/.venv/bin/python with absolute paths.

## Open ideas (Ayush + Claude)
(none yet)

## Proof protocol (never relax these)
1. One sign = one value, everywhere. No convenience readings.
2. Train/test split: 70% work set, 30% sealed hold-out. Publish SHA-256 of hold-out + date before any reading is claimed.
3. Permutation test: our key must beat 10,000 random sign-value assignments on the same scoring.
4. Language must be plausible for ~2600-1900 BCE. No anachronistic vocabulary.
5. Readings must fit object context (seals -> names/titles, pots -> goods, etc.).
6. Code + data fully open and reproducible.
7. Written predictions for unexcavated / unseen inscriptions before seeing them (Ventris tripod test).
8. Final bar: peer-reviewed publication that survives scholarly attack. Prize requires archaeologist acceptance.
