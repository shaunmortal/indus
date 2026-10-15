# Indus Script Project

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
| `data/bridge_WM.json` | Mahadevan <-> Wells/ICIT sign concordance, 165 signs, with provenance. |
| `data/holdout/holdout.sha256` | SHA-256 of the sealed 30% hold-out (966 texts). `holdout.json` itself is never read by analysis code. |
| `data/raw/` | Corpora and books (not committed; see Sources). |

## Results so far (15 Oct 2026)

- The short and tall vertical-stroke signs do not behave as a number system: not concentrated on accounting objects, value distribution peaks at 7 and 12, no place-value order, tall and short strokes have disjoint complements. Replicated on two independent transcriptions (Mahadevan 1977; ICIT/Wells). Draft: `research/note1_numerals_draft.md`.
- Stroke-group layout is lexical for at least one value: three strokes in a row (M102) is productive; three strokes as 2-over-1 (M103) is bound to M403 in 27 of 28 cases across sites and object types.
- No published object anywhere carries Indus signs together with a readable script. Six sweeps, documented in `research/`.
- Two-sided tablets and sealings divide labour: side 1 carries the varied, jar-final, seal-like text; side 2 carries the short repetitive formula tall-strokes + cup (M328). Tall strokes are the administrative class, short strokes the onomastic one.
- Seal size: after controlling for site and text length, one mid-text sign (Wells 741 = Mahadevan 343, the jar with handles) sits on seals about 25% smaller (p = 0.0003, stratified permutation, Bonferroni-corrected). The common jar closer has no size effect. First sign tied to a physical, non-textual variable. Code: `analysis/size1-4.py`.

- Round vs square seals carry partly different sign sets at every site (M169, M387 round; M343, M161, M402 square). Animal emblem, excavation area, period and material show no sign association after correction. Draft: `research/note2_physical_correlates_draft.md`.

- Our own models (Phase 4): sequential structure is bigram-deep (trigram and class models add nothing on held-out texts); an unsupervised function-class model recovers openers, closers, connectives and the docket slot; an allograph algorithm (drawing similarity x distributional similarity) finds that graphic resemblance carries no information about function overall (r = 0.05), and separates true allographs (fish variants, handled-jar variants, M97/M98) from look-alikes that are different signs (plain jar vs handled jar; tall vs short strokes). Merging the allograph pairs lowers held-out perplexity from 29.0 to 26.3, while merging look-alike-but-distinct pairs or random pairs does not (28.5; 28.6 +/- 0.3). A merge-adoption rule based on that test yields a corrected list of 404 signs (`data/model4_merges_v2.json`). Draft: `research/note3_allographs_draft.md`. Code: `analysis/model1-4*.py`.

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
