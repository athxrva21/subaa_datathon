# Appendix A14 — Number reconciliation

*Every figure quoted in the deck traced back to the script that produces it. Reproduce with `reconcile_deck_numbers.py`, `../ethics_finance/cost_model.py` and `cost_fix2.py`.*

The build rule was that every dollar comes from `cost_model.py`, except the corrected early-tenure figure which comes from `cost_fix2.py`. This page is the audit of that rule.

Three items did not reconcile on the first pass. **All three were fixed on 14 Aug** and the fixes are recorded in §3 below. `cost_model.py` is now the single engine for every dollar and every rate on the face of the deck, including the corrected early-tenure lever, so the exception for `cost_fix2.py` is no longer needed. `cost_fix2.py` is retained as the independent cross-check that produced the correction.

---

## 1. Verified against `cost_model.py`

| Slide | Figure | Deck | Script | |
|---|---|---|---|---|
| 3 | Regrettable as counted | $14.3M | $14.3M, n=153 | ok |
| 3 | Regrettable, value based | $45.1M | $45.1M, n=499 | ok |
| 3 | High performers not counted | 371 | 371 | ok |
| 3 | Defensible range | $34–56M | $34–56M | ok |
| 5 | Disengagement | $17.8M | $17.8M, n=813 | ok |
| 5 | Hiring inefficiency | $2.3M | $2.3M | ok |
| 6 | Entity_B regrettable cost | $8.4M | $8.4M | ok |
| 6 | NovaCorp-Origin share | $29.2M | $29.2M | ok |
| 11 | Regrettable @20% / @40% | $9.0M / $18.1M | $9.0M / $18.1M | ok |
| 11 | Disengagement @20% / @40% | $3.6M / $7.1M | $3.56M / $7.12M | ok |
| 11 | Total addressable | $71M | $70.8M | ok |
| 14 | Annualised voluntary rate | 4.7%/yr | 1,133 / 2 / 12,003 = 4.7% | ok |
| 14 | Annual Report reconciliation | 1,400 / 13,403 = 10.4% | reproduces exactly | ok |
| 14 | Involuntary exits | 267 | 267 | ok |
| A5 | Sensitivity grid | $24.8–70.8M | $24.8–70.8M | ok |
| Q&A | Risk & Compliance | $8.0M | $8.0M | ok |

## 2. Verified against `cost_fix2.py`

| Slide | Figure | Deck | Script | |
|---|---|---|---|---|
| 11 | Early-tenure addressable | $7.9M | $7.9M, 92 excess exits | ok |
| 11 | @20% / @40% | $1.6M / $3.2M | $1.6M / $3.2M | ok |
| 11 | Entity_B share | $6.2M | $6.2M, 72 excess exits | ok |
| 11 | Entity_B @20% / @40% | $1.2M / $2.5M | derived, 6.2 × 0.2 and × 0.4 | ok |
| A7 | Entity_B new joiner rate | 10.2% vs 6.4% | 192/1,884 vs 29/455 | ok |
| A8 | Test 14, z score | z = 2.50 | z = 2.50 | ok |

---

## 3. Flags, and what was done about them

All three are closed. Each entry states what was wrong, what changed, and where to reproduce it.

### ✅ A14-1 — Slides 6 and 9 used the denominator slide 14 criticises

**Material. Affects slides 6 and 9, and A8 tests 1 and 2.**

Slide 6 quotes attrition as NovaCorp-Origin 10.3% · Entity_A 7.5% · Entity_B 15.0% · Entity_C 9.3%. Those reproduce only as **total exits including involuntary, over the full two years, on the full roster of 13,403**.

That is the identical construction the deck attacks elsewhere. A6 §"decisions" records our chosen denominator as **active headcount (12,003)** and our chosen numerator as **voluntary only (1,133)**. Slide 14 tells the CHRO their Annual Report's 10.4% is misleading because it is "total exits including 267 involuntary, across the full two-year window, on the total roster." Slide 6 then uses that same construction as the deck's own headline entity comparison.

All five constructions, from `reconcile_deck_numbers.py`:

| entity | all/roster | vol/roster | all/active | vol/active | vol/active/yr |
|---|---|---|---|---|---|
| NovaCorp-Origin | **10.3%** | 8.1% | 11.4% | 9.0% | 4.5% |
| Entity_A | **7.5%** | 6.7% | 8.1% | 7.2% | 3.6% |
| Entity_B | **15.0%** | 11.9% | 17.7% | 14.0% | 7.0% |
| Entity_C | **9.3%** | 8.4% | 10.2% | 9.2% | 4.6% |

Bold column is what the deck quotes. Last column is what A6 says we adopted.

**The finding is not at risk.** Entity_B is worst on every construction and the effect barely moves:

| | as published | restated |
|---|---|---|
| Entity_B vs Entity_A ratio | 2.0× | 1.9× |
| Chi-square, four groups | p = 1.9×10⁻¹³ | p = 6.7×10⁻⁹ |
| Entity_B vs Entity_A pairwise | p = 2.0×10⁻¹³ | p = 8.0×10⁻⁹ |

**Applied.** Slide 6 now reads **7.0% vs 3.6%** annualised voluntary on active, keeps the 1.9× framing, and carries the denominator in a footnote. Changed in the same pass:

| File | Change |
|---|---|
| `DECK_STORYBOARD.md` slide 6 | rates restated, denominator footnote added |
| `DECK_STORYBOARD.md` slide 9 | headline restated to 3.6% below 4.5%, Entity_C to 4.6% |
| `DECK_STORYBOARD.md` cheat-sheet + Q&A | 7.0% vs 3.6%, p = 8×10⁻⁹, Entity_B sized as 1,601 |
| `APPENDIX_A8` tests 1 and 2 | restated, with a dated note on why |
| `APPENDIX_A13` | Entity_A precedent restated to 3.6%/yr |
| `ethics_finance/SLIDES.md` | Entity_B worst rate restated to 7.0%/yr |
| `findings.md` | Part 1 spread restated to 3.6–7.0%, note added |
| `cost_model.py` | new `entity_rates()` section prints both conventions side by side |

### ✅ A14-2 — `cost_model.py` emitted the pre-correction numbers

**Material. Affects the reproducibility claim in A11.**

`cost_model.py` is named as the deck's single costing engine, but running it today prints:

- Early-tenure lever **$29.6M addressable, $5.9M @20%, $11.8M @40%**. The deck says $7.9M / $1.6M / $3.2M.
- `"91% of them are ACQUISITION-sourced, not agency"` — the exact claim A7 says to delete.
- `"agency hires have the second-LOWEST early-exit rate"` — the other claim A7 says to delete.

So the stated rule cannot be satisfied as written for the early-tenure line. The correction lives only in `cost_fix2.py`, and the engine of record still contradicts it. Anyone who reruns the named source of truth, including a judge who asks us to, gets the superseded answer along with two claims we have publicly retracted.

**Applied.** `cost_model.py` section 3 now measures early attrition on in-window hires only, and section 5 computes the early-tenure lever as excess over the NovaCorp-Origin new-joiner baseline. It reproduces `cost_fix2.py` exactly:

```
Early-tenure / acquisition onboarding    $7.9M    $1.6M    $3.2M
  of which Entity_B                      $6.2M    $1.2M    $2.5M
```

Section 3 also now prints both retractions explicitly, so anyone rerunning the engine is told which claims are dead rather than being handed them:

```
RETRACTED, do not quote either of these:
   - '91% of early exits are acquisition-sourced' was a composition
     statistic driven by observation availability.
   - 'agency hires are one of our best sources' reversed once the
     denominator was corrected.
```

Moksh's `SLIDES.md` slide D and slide E were updated to match, with both retracted claims removed from the body, the Q&A answer and the cheat-sheet.

One residual difference, stated so it does not read as a fresh contradiction: `cost_model.py` counts **voluntary** early exits, matching A6's convention and the $7.9M lever. A7's hire-source table counts **all** early exits and so reads about 2pt higher per source (acquisition 11.6% against 9.6%). Same ordering, same conclusion, different numerator. A7's own cohort table is voluntary-only, so the inconsistency is internal to A7 and worth a one-line fix if anyone has time.

### ✅ A14-3 — Three different Entity_B headcounts on adjacent slides

**Minor, but it is the kind of thing that gets picked up in Q&A.**

| Number | What it is | Where it appears |
|---|---|---|
| 1,884 | full roster, active and departed | slides 6 and 11, A8 test 2 |
| 1,601 | active headcount | not quoted, but is the A6 denominator |
| 1,697 | survey responders | slide 7 chart footnote, A8 tests 3 and 4 |

All three are correct for their own purpose. Slide 6 says "$8.4M concentrated in 1,884 people you already know how to fix", which reads as a headcount you could act on, but 283 of those 1,884 have already left. The actionable population is 1,601.

**Applied.** Slide 6 and the Q&A prep now say **1,601**, the population that can actually be acted on. The slide 7 chart carries its own responder n in the footnote. Where 1,884 remains correct, as in A7's in-window comparison, it is left alone.

---

## 4. Populations used across the deck

Kept here because four different denominators are in play and each is right for a different question.

| | roster | active | in-window hires | survey responders |
|---|---|---|---|---|
| NovaCorp-Origin | 8,555 | 7,678 | 455 | 8,315 |
| Entity_A | 1,950 | 1,804 | 0 | 1,938 |
| Entity_B | 1,884 | 1,601 | 1,884 | 1,697 |
| Entity_C | 1,014 | 920 | 1,014 | 640 |
| **total** | **13,403** | **12,003** | **3,353** | **12,590** |

Entity_A has zero in-window hires and Entity_B and Entity_C have their entire roster in-window. That is the `hire_date` system-entry artifact documented in A6 and Part 2 finding 10, and it is why `cost_fix2.py` restricts to in-window hires before comparing early attrition.
