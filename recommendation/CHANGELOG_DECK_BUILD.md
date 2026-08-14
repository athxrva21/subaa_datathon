# Deck build changelog

*Running record of every change made during the deck build, grouped by whose work it touches. Kept so nobody discovers their own numbers moved without being told, and so anything can be reverted per-person if someone disagrees.*

**Maintained by:** Aryan · **Branch:** `recommendation-workstream` · **Started:** 14 Aug 2026

---

## Why anything changed at all

Two audits ran before the deck build started.

**Audit 1, the dollar trace.** Every figure quoted in the storyboard was traced back to the script that produces it. 22 reconciled exactly. Three did not, and are written up as flags A14-1, A14-2 and A14-3 in `APPENDIX_A14_number_reconciliation.md`.

**Audit 2, the denominator check.** The deck quoted attrition on one convention while its own limitations slide criticised the Annual Report for using that same convention. Restating fixes the contradiction and does not change any conclusion.

Everything below flows from those two. **No finding changed. No recommendation changed. No conclusion reversed.** What changed is which denominator sits under a rate, and which of two already-known figures gets quoted.

---

## Changes to Atharva's work — Part 1

| File | What changed | Why |
|---|---|---|
| `findings.md` | Entity attrition spread restated from **7.5–15.0%** to **3.6–7.0% per year**. Company-average multiple moved 1.4x to 1.5x. Dated note added under the paragraph. | A14-1. The old figures were total exits including involuntary over the full roster. The deck now quotes annualised voluntary on active everywhere. |

**Nothing else in Part 1 was touched.** `explore_part1.py` and all 21 charts in `figures/` are untouched.

**Still open, needs Atharva's call:**
- A12 §4 says two Part 1 findings are wrong as written, not merely cut: the *"68% of exits are push, therefore preventable"* claim (push includes 267 involuntary exits, so it is not a disengagement measure) and the *"employees go silent before they quit"* claim (there is no pre-exit decay, leavers go 67.1% → 66.1% and were quieter from wave 1). Both are still live in `findings.md`. Neither is on a slide, so neither blocks the deck, but the repo contradicts the deck until they are fixed.
- `figures/03_attrition_by_legacy_entity.png` still plots the old roster-based rates. **Slide 6 uses the Part 2 version instead**, so this is not blocking, but the Part 1 chart and the Part 1 text now disagree.

---

## Changes to Keya's work — Part 2

| File | What changed | Why |
|---|---|---|
| `explore_part2.py:23` | `DATA_DIR` now derives from the script's own location instead of the hardcoded `/mnt/project`. | The script would not run for anyone who cloned the repo. This is what blocked slides 7 and 8. |
| `explore_part2.py` §7a | Entity attrition restated to annualised voluntary over active headcount. Added `WINDOW_YEARS`, `vol_exit` and `is_active`. | A14-1. |
| `explore_part2.py` §7a | Chi-square contingency table now built explicitly rather than by `crosstab`. | The crosstab folded involuntary leavers in as non-events, so the test population did not match the rate printed directly above it. p moves 3.2×10⁻⁸ → 8.0×10⁻⁹, now matching A8 and `cost_model.py`. |
| `explore_part2.py` §7a chart | Y-axis relabelled to per-year, denominator footnote added. | Style checklist in A12 §5, every rate carries its denominator. |
| `explore_part2.py:923` | Slide 7 chart, x-axis padded so p-value labels stop overprinting the y-axis tick labels. Added n for both entities. | `p=2.6e-25` was printing straight through the words "purpose meaning". Unreadable, on the chart A12 calls the most important visual in the deck. |
| `explore_part2.py:798` | Slide 8 chart, both panels share one y-scale, x-ticks forced to integers, legend moved outside the axes, footnote added on cohort join timing. | Independent y-scales made the same Entity_B gap look different on the left panel than the right. Half-numbered survey waves are meaningless. |
| `explore_part2.py:1113` | Hardcoded summary line 5 restated to 7.0% vs 3.6%. | The only place in the script where these rates were typed rather than computed. |

**Effect on Keya's findings:** all 18 still hold. Findings 138 and 180 now print the restated rates automatically because they interpolate from the computed table. The Entity_A vs Entity_C null moves p = 0.106 → 0.101, still null.

**Deliberately not changed:**
- Finding 124, HIPO staff leaving at 15.0% vs 10.0%, still uses roster-based rates. It is a different comparison to the entity one and does not appear on a slide.
- Finding 264, the Annual Report reconciliation, deliberately uses all-exits because that is what reproduces the Annual Report's own number. Correct as written.
- The other 15 uses of `departed` across the script. Restating all of them would touch findings well outside what the deck quotes. Scoped to the entity section only.

---

## Changes to Mokshith's work — ethics & financial quantification

| File | What changed | Why |
|---|---|---|
| `cost_model.py` §3 | Early attrition now measured on **in-window hires only**. Added `WINDOW_START`. | A14-2. The old version divided early exits by all hires of a source, most hired years before the window opened, so it measured who we can observe rather than who leaves early. This is the same error A7 documents. |
| `cost_model.py` §3 | Now prints both retracted claims explicitly as retractions. | The engine was still emitting *"91% of early exits are acquisition-sourced"* and *"agency hires have the second-LOWEST early-exit rate"*, the two claims A7 says to delete. Anyone rerunning the source of truth was being handed dead claims. |
| `cost_model.py` §5 | Early-tenure lever now computed as excess over the NovaCorp-Origin new-joiner baseline. **$29.6M → $7.9M.** Added disengagement and the Entity_B split so the table matches slide 11 line for line. | A14-2. Only the excess over baseline churn is addressable. Reproduces `cost_fix2.py` to the dollar. |
| `cost_model.py` | New §6 `entity_rates()`, prints both the restated and superseded conventions side by side. | A14-1, so slide 6's rates are traceable to the engine like everything else. |
| `cost_model.py` | New helpers `disengaged_pool()` and `early_tenure_addressable()`. | The lever table was recomputing methods that already existed elsewhere in the file. Now single-sourced. |
| `SLIDES.md` slide D | Early-exit table restated to in-window voluntary. Both retracted claims removed from the body. Retraction note added. | Handover instruction, carried through. |
| `SLIDES.md` slide E | Lever table restated: early-tenure **$7.9M / $1.6M / $3.2M**, Entity_B split added, disengagement row added. | Handover instruction, carried through. |
| `SLIDES.md` | Entity_B worst rate 15.0% → 7.0%/yr. Monday answer reworded off the 91% claim. Cheat-sheet row replaced. | A14-1 and A14-2. |

**Net effect, and it is a good one:** every dollar *and* every rate on the face of the deck now comes from `cost_model.py` alone. The carve-out for `cost_fix2.py` is no longer needed. `cost_fix2.py` is retained as an independent cross-check, which is worth more as corroboration than as a second source of truth.

**Not changed:** `ethics_audit.py`, `verify.py`, `verify2.py`, `make_figures.py`, and all six E-charts. The fairness work, the four-fifths results and the sensitivity grid are untouched.

---

## Changes to Suman's work — recommendation & appendices

| File | What changed | Why |
|---|---|---|
| `DECK_STORYBOARD.md` slide 6 | Rates restated to **4.5 / 3.6 / 7.0 / 4.6 %/yr**. p = 2×10⁻¹³ → 8×10⁻⁹. Entity_B sized as **1,601** not 1,884. Denominator footnote added. | A14-1 and A14-3. |
| `DECK_STORYBOARD.md` slide 9 | Headline restated to *"Entity_A is at 3.6%, below NovaCorp's own 4.5%"*. Entity_C 9.3% → 4.6%. p = 0.106 → 0.101. | A14-1. |
| `DECK_STORYBOARD.md` cheat-sheet | Entity_B vs Entity_A row restated. | A14-1. |
| `DECK_STORYBOARD.md` Q&A | *"Entity_B is only 1,884 people"* → 1,601. | A14-3. 283 of the 1,884 have already left, so it is not a population you can act on. |
| `APPENDIX_A8` tests 1 and 2 | Restated to voluntary-on-active. n 13,403 → 12,003 and 1,884/1,950 → 1,601/1,804. Dated note added explaining the change. | A14-1. |
| `APPENDIX_A8` null register | Entity_A vs Entity_C p = 0.106 → 0.101. | Recomputed on the restated construction. Still null. |
| `APPENDIX_A13` | Entity_A precedent 7.5% → 3.6%/yr. | A14-1. |
| `EARLY_TENURE_CORRECTION.md` (A7) | Hire-source table restated to voluntary-only: 9.6 / 7.7 / 5.4 / 3.4. Note added. | A7's cohort table counted voluntary only while its hire-source table counted all exits. Internal inconsistency inside one appendix. Same ordering and conclusion either way. |

**New files added by the deck build:**

| File | What it is |
|---|---|
| `APPENDIX_A14_number_reconciliation.md` | The dollar trace. 22 figures verified against source, three flags with what was done about each, and the four-population table explaining why four different denominators are legitimately in play. |
| `reconcile_deck_numbers.py` | Reproduces the denominator audit and the survives-restatement test. Read only. |
| `CHANGELOG_DECK_BUILD.md` | This file. |

**Not changed:** A6, A9, A10, A11, A12, `survival_fix.py`, `cost_fix2.py`, `HANDOVER_ARYAN.md`.

---

## Changes to shared repo files

| File | What changed | Why |
|---|---|---|
| `.gitignore` | Created. Ignores `.venv/`, `__pycache__/`, `.DS_Store`, scratch files. | The repo had none. A stray `git add .` would have committed a 200MB virtualenv. |

---

## Verification after every change

All three engines run clean and agree:

```
cost_model.py     early-tenure $7.9M / $1.6M / $3.2M, Entity_B $6.2M
cost_fix2.py      $7.9M/yr, 92 excess exits, Entity_B $6.2M
explore_part2.py  4.5 / 3.6 / 7.0 / 4.6 %/yr, p = 6.7e-09 overall, 8.0e-09 pairwise
reconcile_deck_numbers.py   same rates, same p values
```

Two independent implementations of the early-tenure method agree to the dollar. Three independent implementations of the entity rate agree to the decimal.

Reproduce everything:

```bash
python3 -m venv .venv && .venv/bin/pip install pandas numpy matplotlib seaborn scipy
cd ethics_finance   && ../.venv/bin/python cost_model.py
cd ../recommendation && ../.venv/bin/python cost_fix2.py && ../.venv/bin/python reconcile_deck_numbers.py
cd ../explore_pt2    && ../.venv/bin/python explore_part2.py
```

---

## Open items nobody has ruled on

| # | Item | Owner | Blocking? |
|---|---|---|---|
| 1 | Two Part 1 findings that A12 calls wrong as written, not just cut | Atharva | No, neither is on a slide |
| 2 | `figures/03_attrition_by_legacy_entity.png` still plots roster-based rates | Atharva | No, slide 6 uses the Part 2 chart |
| 3 | A8's remaining tests still use roster denominators (HIPO, response rate, compa-ratio) | Suman | No, none appear on a slide |
| 4 | `.venv` pinned at pandas 3.0.5 / scipy 1.18.0, much newer than these scripts were written against | anyone | No, but reproducibility is nominal not real until pinned |
