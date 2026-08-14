# Appendix A14 — Number reconciliation

*Every figure quoted in the deck traced back to the script that produces it. Reproduce with `reconcile_deck_numbers.py`, `../ethics_finance/cost_model.py` and `cost_fix2.py`.*

The build rule was that every dollar comes from `cost_model.py`, except the corrected early-tenure figure which comes from `cost_fix2.py`. This page is the audit of that rule. Three items did not reconcile and are flagged at the bottom rather than rewritten, so the copy stays traceable.

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

## 3. Flags

### 🔴 A14-1 — Slides 6 and 9 use the denominator slide 14 criticises

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

**Recommended fix, for whoever owns the copy:** restate slide 6 to **7.0% vs 3.6%** annualised voluntary on active, keep the 1.9× framing, and footnote the denominator. This costs the argument nothing and removes a contradiction a judge can find by reading two of our own slides against each other. A8 tests 1 and 2 need the same treatment.

Not applied here, per the instruction to flag rather than rewrite.

### 🔴 A14-2 — `cost_model.py` still emits the pre-correction numbers

**Material. Affects the reproducibility claim in A11.**

`cost_model.py` is named as the deck's single costing engine, but running it today prints:

- Early-tenure lever **$29.6M addressable, $5.9M @20%, $11.8M @40%**. The deck says $7.9M / $1.6M / $3.2M.
- `"91% of them are ACQUISITION-sourced, not agency"` — the exact claim A7 says to delete.
- `"agency hires have the second-LOWEST early-exit rate"` — the other claim A7 says to delete.

So the stated rule cannot be satisfied as written for the early-tenure line. The correction lives only in `cost_fix2.py`, and the engine of record still contradicts it. Anyone who reruns the named source of truth, including a judge who asks us to, gets the superseded answer along with two claims we have publicly retracted.

**Options:** either patch `cost_model.py` section 3 to call the in-window method and have it print the retraction, or state plainly in A11 that section 3 of `cost_model.py` is superseded by `cost_fix2.py`. The second is a ten-minute fix and is probably right given the deadline.

### 🟡 A14-3 — Three different Entity_B headcounts on adjacent slides

**Minor, but it is the kind of thing that gets picked up in Q&A.**

| Number | What it is | Where it appears |
|---|---|---|
| 1,884 | full roster, active and departed | slides 6 and 11, A8 test 2 |
| 1,601 | active headcount | not quoted, but is the A6 denominator |
| 1,697 | survey responders | slide 7 chart footnote, A8 tests 3 and 4 |

All three are correct for their own purpose. Slide 6 says "$8.4M concentrated in 1,884 people you already know how to fix", which reads as a headcount you could act on, but 283 of those 1,884 have already left. The actionable population is 1,601.

**Recommended fix:** slide 6 reads "1,601 people still there". Footnote the others where they appear.

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
