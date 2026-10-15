# Indus Script Project

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23399794.svg)](https://doi.org/10.5281/zenodo.23399794)  Cite as: Ayush Kumar (2026), v0.4.0, doi:10.5281/zenodo.23399794 (all versions: 10.5281/zenodo.23396757; v0.3.1 = 10.5281/zenodo.23396758, superseded by the F23 correction)

**Ayush Kumar (India)** — an open, data-first attempt at the Indus Valley script, with computational assistance from Claude.
Started 15 October 2026. Goal: read the script in a way archaeologists accept. No pivots, no compromise.

## What is here

| Path | What |
|---|---|
| `STATE.md` | Running state: rules, status, findings F1-F11, failures, next steps. Read this first. |
| `attempts.md` | Map of 100 years of attempts and why each failed to convince. |
| `research/` | Six research sweeps (India finds, Gulf/Iran sealings, Mesopotamian seals, numerals and weights, online sources, odd objects, hybrid seals) and the first draft note. |
| `analysis/` | All code. `stats0.py` baseline stats; `numerals1-7` the stroke-sign tests; `diachronic1.py`; `concord1-2.py` sign concordance; `holdout.py` the sealed test set. |
| `data/stroke_signs.json` | Complete stroke-sign inventory read from Mahadevan's drawings. |
| `data/title_blocks_v1.json` | Title-block inventory (F28): 18 three-sign blocks shared by >=3 unique square-seal texts, with closers, sites and individual parts (85 names); replicated on Mahadevan 1977 in `data/title_blocks_v1_mahadevan.json` (38 blocks, 169 names). `analysis/title_blocks.py`. |
| `data/bridge_WM.json` | Mahadevan <-> Wells/ICIT sign concordance, 176 signs (88.6% of ICIT tokens), with provenance per pair (paragorth; text-alignment voting; glyph-similarity matches verified by eye, `analysis/concord3_image.py`). |
| `data/holdout/holdout.sha256` | SHA-256 of the sealed 30% hold-out (966 texts). `holdout.json` itself is never read by analysis code. |
| `data/raw/` | Corpora and books (not committed; see Sources). |

## Results so far (15 Oct 2026)

- 2026-10-16 additions: results robust to dropping doubtful readings (F32); tall strokes on pottery suggestive only (F33, registry P14-P16); stroke-class collocation tables agree across transcriptions (F34); anchor drill: one title block unlocks <4% of texts, the jar closer 49% (F35); ICIT seal dimensions for Mohenjo-daro/Harappa are the 1930s catalogue measurements, so the size results rest on one measurement set (F36, F37); the cup formula on tablets takes values 2-4, never 5, rarely 1 (F38, P17), and its value follows the side-1 identity (F39). See STATE.md and research/search_map.md.
- The short and tall vertical-stroke signs do not behave as a number system: not concentrated on accounting objects, value distribution peaks at 7 and 12, no place-value order, tall and short strokes have disjoint complements. Replicated on two independent transcriptions (Mahadevan 1977; ICIT/Wells). Draft: `research/note1_numerals_draft.md`.
- Stroke-group layout is lexical for at least one value: three strokes in a row (M102) is productive; three strokes as 2-over-1 (M103) is bound to M403 in 27 of 28 cases across sites and object types.
- No published object anywhere carries Indus signs together with a readable script. Six sweeps, documented in `research/`.
- Two-sided tablets and sealings divide labour: side 1 carries the varied, jar-final, seal-like text; side 2 carries the short repetitive formula tall-strokes + cup (M328). Tall strokes are the administrative class, short strokes the onomastic one.
- Seal size: after controlling for site and text length, one mid-text sign (Wells 741 = Mahadevan 343, the jar with handles) sits on seals about 25% smaller (p = 0.0003, stratified permutation, Bonferroni-corrected). The common jar closer has no size effect. First sign tied to a physical, non-textual variable. Code: `analysis/size1-4.py`.

- Round vs square seals carry partly different sign sets at every site (M169, M387 round; M343, M161, M402 square). Animal emblem, excavation area, period and material show no sign association after correction. Draft: `research/note2_physical_correlates_draft.md`.

- Our own models (Phase 4): sequential structure is bigram-deep (trigram and class models add nothing on held-out texts); an unsupervised function-class model, selected for cross-resample stability, supports exactly three reproducible classes (openers, core, closers; K = 3, ARI 0.59) and no finer grammar; an allograph algorithm (drawing similarity x distributional similarity) finds that graphic resemblance carries no information about function overall (r = 0.05), and separates true allographs (fish variants, handled-jar variants, M97/M98) from look-alikes that are different signs (plain jar vs handled jar; tall vs short strokes). Merging the allograph pairs lowers held-out perplexity from 29.0 to 26.3, while merging look-alike-but-distinct pairs or random pairs does not (28.5; 28.6 +/- 0.3). Replicated on the Wells/ICIT list (perplexity 37.7 to 32.0 vs 36.9 random). A merge-adoption rule based on that test yields a corrected Mahadevan list of 404 signs (`data/model4_merges_v2.json`). Draft: `research/note3_allographs_draft.md`. Code: `analysis/model1-4*.py`.

- What the texts are (F23-F30): 96% of square-seal texts occur on one seal only (unique identifiers); repeated texts are short title strings and sit on seals 14% smaller; final-sign alternation on shared stems is at chance level (an earlier '11 sd fewer than chance' figure was a deduplication bug and is retracted); identical texts recur across cities above chance, but the cases are moulded tablets and title formulae, not shipments; shared 'blocks' cover no more of the texts than a bigram process would. The defensible picture: seal text = opener formula + individual element + title block + closer, with identity carried combinatorially.
- Two Ur excavation volumes (UE X 1951, UE III 1936) read page by page: no impression of an Indus-sign seal on any tablet or bulla; Ur is exhausted in print.
- Frozen, hashed registries of falsifiable predictions for the next inscriptions to be published: `prereg/predictions-1.json` (P1-P8), `predictions-2.json` (P9-P13, P11 withdrawn), `predictions-3.json` (P14-P16, tall-stroke values by object class), `predictions-4.json` (P17, cup-formula values on tablets); all computed on the work set only. `analysis/score_registry.py LOT.json` scores a new lot against every registered prediction and writes `prereg/results-<lot>.md` (format of the lot file in the script header; `--smoke` self-check).

- Tamil Nadu graffiti (tngraffiti.in, 42 base signs, 5,163 occurrences): 30 of 42 signs have an Indus look-alike, but the pairs of signs that co-occur on Tamil sherds do not correspond to pairs that co-occur in Indus texts any more than random frequency-matched signs do (p = 0.51). The 'parallels' are shapes, not behaviour. Code: `analysis/tn1_lookalikes.py`, `tn2_behaviour.py`.

## Proof protocol (never relaxed)

1. One sign, one value, everywhere.
2. 30% hold-out sealed before any reading is claimed; hash published.
3. Any key must beat 10,000 random keys on the same scoring.
4. Language plausible for 2600-1900 BCE.
5. Readings must fit object context.
6. Code and data fully open.
7. Written predictions for unseen inscriptions before seeing them.
8. Final bar: peer review that survives.

Also: deduplicate first. Identical texts (mass-produced tablets, sealings) are counted once.

## Reproduce

```
python3 -m venv .venv && .venv/bin/pip install pillow openpyxl pypdf
.venv/bin/python -I analysis/stats0.py data/raw/joyboseroy_csv/*.csv
.venv/bin/python -I analysis/numerals6.py
```

## Sources

- Mahadevan 1977 corpus, machine-readable export from indusscript.in (Roja Muthiah Research Library), via github.com/paragorth/Indus- (MIT, with attribution).
- ICIT/Wells corpus via the yajnadevam/indus-website open database; CISI (Parpola et al.) partial digitization via github.com/mayig/indus-valley-script-corpus; toolkit by github.com/joyboseroy/indus_decipher (MIT).
- Scans: Mahadevan 1977 and CISI vols 1-2 on archive.org; Gadd 1932 on archive.org.

## Credit

Work and credit: Ayush Kumar. Computational assistance: Claude (Anthropic). Every number here is computed from the open data; nothing is narrated.
