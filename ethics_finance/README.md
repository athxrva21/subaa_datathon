# Ethics & Financial Quantification workstream

**Owner:** Moksh — covers 35% of the marking rubric (Ethics & Responsible Practice 20%,
Financial Impact Quantification 15%).

## Start here

| File | What it is |
|---|---|
| **`TEAM_NOTE.md`** | ⚠️ Read first — three findings in `../findings.md` that don't hold up, and what to do instead |
| **`SLIDES.md`** | Slide-by-slide content for slides A–F, with Q&A prep and a numbers cheat-sheet |
| **`ASSUMPTIONS.md`** | Appendix: constants, population decisions, formulas, fairness method |

## Scripts

Run from inside this folder — they read the CSVs from `../`.

```
python cost_model.py      # every dollar figure in the deck + reconciliation + sensitivity
python ethics_audit.py    # flag-consistency, four-fifths adverse-impact tests, flag precision
python make_figures.py    # the six E* charts -> figures_ethics/
python verify.py          # stress-tests the Part-1 findings (push/pull, silence decay)
python verify2.py         # regrettable-flag bias, segment costs, AR reconciliation
```

Deterministic — no seeds, no sampling. Only dependencies are `pandas`, `numpy`, `matplotlib`.

## Figures

| File | Used on |
|---|---|
| `E1_regrettable_gap.png` | Slide A — $14.3M counted vs $45.1M real |
| `E2_flag_never_fires.png` | Slide B — flag rate by performance band × pathway |
| `E3_adverse_impact_age.png` | Slide C — silence flag is an age proxy |
| `E4_flag_precision.png` | Slide C — 23% precision, 901 false positives |
| `E5_sensitivity.png` | Appendix / Q&A — $25–71M grid |
| `E6_buckets_restated.png` | Slide D — the $42M re-apportioned |

## The one number

**$14.3M counted → $45.1M real.** 371 high-performing voluntary leavers NovaCorp never recorded as a
loss, because the `regrettable_flag` fires for "Outstanding" and almost never for "High Performer" —
**0 out of the 168** who were managed out. Fixing it is a definition change, cost ~$0.
