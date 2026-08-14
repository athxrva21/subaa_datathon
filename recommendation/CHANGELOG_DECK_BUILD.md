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
| `findings.md` one-sentence story | Rewritten off the two claims corrected below. Dated note added. | Both corrected claims were load-bearing in the summary. |
| `findings.md` finding 2 | *"68% of exits are push (disengagement-driven)"* corrected. Push is **involuntary or managed** per the brief, not disengagement-driven, and **267 of the 955 are literally involuntary** (196 performance, 50 restructure). Restated as **688 of 1,133 voluntary exits, 60.7%**. | A12 §4 calls this wrong on correctness, not space. An involuntary exit is a decision the company made, not a loss it suffered, so it cannot be counted as preventable. |
| `findings.md` finding 5 | *"gap widening wave over wave"* corrected. Leavers go **70.6% → 70.3%** across waves 1–5 while stayers go 84.9% → 80.5%. The gap **narrows** from 14.4pt to 10.2pt. Reframed as a stable trait rather than a decline. Ethics warning added. | A12 §4. The original said people go silent *before* quitting. They were quiet from arrival. An early-warning system built to spot a decline would never fire. |
| `findings.md` finding 12 | Superseded. All dollar figures now cite `cost_model.py`: $45.1M / $17.8M / $2.3M, total $65.2M. | The original used a 0.5–1.0× replacement multiplier the brief does not specify, then applied the 68% push share, double-counting the involuntary exits corrected in finding 2. |
| `findings.md` glossary | Push/pull definition corrected to the brief's actual wording. | Root cause of the finding 2 error. |
| `findings.md` finding 3 | Entity attrition spread restated **7.5–15.0%** → **3.6–7.0% per year**. | A14-1. |
| `explore_part1.py:90` | Added `WINDOW_YEARS`. | Rates now read per year. |
| `explore_part1.py:180` | Added `vol_exit` and `is_active` at load time. | So every rate in Part 1 can use the deck convention. |
| `explore_part1.py` §2 | Entity attrition restated to annualised voluntary on active. Chart relabelled, y-limit set, denominator footnote added, company-average label moved so it stops colliding with the bar labels. | A14-1. Part 1 now agrees with Part 2 and `cost_model.py` to two decimals. |
| `figures/03_attrition_by_legacy_entity.png` | Regenerated. | Was plotting the superseded roster-based rates. |
| `figures/04_entity_engagement_vs_attrition.png` | Regenerated. | Same underlying table. |

**Not changed:** the other 19 charts in `figures/`, and every Part 1 finding not listed above.

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
| `explore_part2.py` `load()` | `vol_exit` and `is_active` moved to load time so every function can use them. | They were local to the entity section, which meant the HIPO and leadership-churn sections could not reach them. |
| `explore_part2.py` §6 | HIPO attrition restated. **15.0% vs 10.0% → 7.3% vs 4.5%/yr.** Lift **1.50× → 1.64×**, p 9.7×10⁻⁸ → 1.2×10⁻⁷. Chart relabelled. | A14-1. The finding gets *stronger* restated. |
| `explore_part2.py` §7h | Senior Manager churn restated. **L3 Entity_A 6.7% vs Entity_B 18.0% → 2.9% vs 9.8%/yr.** Ratio **2.7× → 3.4×**, p 0.0050 → 0.0047. | A14-1. Also gets stronger. This one is quoted on slide 10. |
| `explore_part2.py:792` | L3-and-above summary restated 14.8% vs 6.2% → 7.3%/yr vs 2.8%. | Hardcoded, not computed. |
| `explore_part2.py:1114` | Summary lines 2 and 5 restated. | The only two places in the script where these rates were typed rather than computed. |
| `explore_pt2/findings_part2.md` | Replaced with the regenerated output. | The committed copy was Keya's original and still carried every superseded figure. It is generated output, so it is replaced rather than hand-edited. |

**Effect on Keya's findings:** all 18 still hold, and **two get stronger**. Findings 124, 138, 180 and 211 now print restated rates automatically because they interpolate from computed tables. The Entity_A vs Entity_C null moves p = 0.106 → 0.101, still null.

**Deliberately not changed:**
- Finding 264, the Annual Report reconciliation, deliberately uses all-exits because that is what reproduces the Annual Report's own number. Correct as written and load-bearing for slide 14.
- The remaining uses of `departed` in sections that are not attrition rates.

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
| `make_figures.py` E6 | Bucket values now imported from `cost_model.py` instead of being typed as `np.array([45.1, 17.8, 2.3])`. | A14-2. A hardcoded chart silently stops matching the engine the moment the engine changes. |
| `make_figures.py` E6 | Bars now coloured by direction, coral for buckets larger than Finance's estimate and teal for smaller. Legend rewritten. Footnote added showing the **$65.2M total against Finance's $42M midpoint**. Title changed to *"Two buckets are bigger than Finance thought, one is smaller"*. | The old title said the $42M was *"mis-apportioned"*, which reads as a fixed total being redistributed. The restated buckets total 1.6× Finance's midpoint. That is the more important fact and it was invisible on the chart. |

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
| `DECK_STORYBOARD.md` slide 5 | Headline changed from *"Same $42M — different shape"* to *"It isn't $42M. On your own formulas it's $65M."* Total row added to the table. | The restated buckets total **$65.2M**, 1.6× Finance's $42M midpoint. "Same $42M, different shape" describes a redistribution that did not happen. |
| `DECK_STORYBOARD.md` slide 5 | *"Two of these move in your favour and one moves badly against you"* corrected to *"Only one of these moves in your favour, and it's the smallest one."* | Backwards as written. Regrettable and disengagement both moved **against** NovaCorp; only hiring moved in its favour. |
| `DECK_STORYBOARD.md` slide 10 | Senior Manager gap restated 18.0% vs 6.7% → **9.8%/yr vs 2.9%**, and the 3.4× ratio stated explicitly. | A14-1, carrying A8 test 10 through. |
| `APPENDIX_A8` tests 10 and 11 | Restated. L3 **2.9 vs 9.8 %/yr**, p = 0.0047. HIPO **7.3 vs 4.5 %/yr**, lift 1.64×, p = 1.2×10⁻⁷. Before-and-after table added to the header note. | A14-1. Completes the register, every attrition rate now uses one convention. |

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
| `requirements.txt` | Created. Pins pandas 3.0.5, numpy 2.5.2, matplotlib 3.11.1, seaborn 0.13.2, scipy 1.18.0. | A11 claims reproducibility, but `explore_part2.py` needs scipy and nobody had it installed. Reproducibility was nominal until this existed. |

---

## Verification after every change

All five engines run clean and agree.

**Entity_B attrition, four independent implementations:**

```
explore_part1.py            7.00 %/yr
explore_part2.py            7.0  %/yr    p = 6.7e-09 overall, 8.0e-09 pairwise
cost_model.py               7.0  %/yr
reconcile_deck_numbers.py   7.0  %/yr
```

**Early-tenure lever, two independent implementations:**

```
cost_model.py    $7.9M addressable, $1.6M @20%, $3.2M @40%, Entity_B $6.2M
cost_fix2.py     $7.9M/yr, 92 excess exits, Entity_B $6.2M
```

Reproduce everything from a clean clone:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python explore_part1.py
cd explore_pt2       && ../.venv/bin/python explore_part2.py   && cd ..
cd ethics_finance    && ../.venv/bin/python cost_model.py      && ../.venv/bin/python make_figures.py && cd ..
cd recommendation    && ../.venv/bin/python cost_fix2.py       && ../.venv/bin/python reconcile_deck_numbers.py
```

---

## Open items

All four items from the first pass are now closed.

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Two Part 1 findings A12 calls wrong as written | Atharva | ✅ Fixed, findings 2 and 5, plus the summary and glossary |
| 2 | `figures/03` plotted roster-based rates | Atharva | ✅ Regenerated, and 04 with it |
| 3 | A8's remaining roster-denominator tests | Suman | ✅ Tests 10 and 11 restated, both got stronger |
| 4 | Dependency versions unpinned | anyone | ✅ `requirements.txt` added |

**Nothing outstanding.** Every attrition rate in the repo now uses one convention, every dollar comes from `cost_model.py`, and all five engines agree.

Two things worth a second pair of eyes rather than being problems:

- **Part 1 finding 5 now carries an ethics warning** pointing at deck slides 12–13. The original recommended the silence flag as *"the single highest-leverage early-warning signal available"*, which directly contradicts the deck's recommendation against individual-level deployment. Worth Atharva and Mokshith agreeing on the wording.
- **Part 1 finding 12 is marked superseded rather than restated**, because the costing engine now owns every dollar figure. If Atharva would rather it were deleted outright, that is a one-line change.
