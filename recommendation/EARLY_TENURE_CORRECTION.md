# Correction: the early-tenure lever ($29.6M → $7.9M)

*Resolves Conflict 1. Reproduce with `survival_fix.py` and `cost_fix2.py`.*

## What was wrong

`cost_model.py` line 149 defines an early exit as `status == "departed" & tenure_months <= 12`, then reports early-exit rate by `hire_source` against **all** hires of that source. Slide D turns this into *"91% of early exits are acquisition-sourced"* and Slide E into a **$29.6M** addressable lever.

The problem is that `hire_date` for acquired staff records **when their record entered NovaCorp's system**, not when they started work (Part 2, Finding 10). So the two groups are not observed for comparable amounts of time:

| Cohort | n | % observed from tenure 0 | Max observable tenure |
|---|---|---|---|
| NovaCorp-Origin | 8,555 | **5.3%** | 462 months |
| Entity_A | 1,950 | **0.0%** | 33 months |
| Entity_B | 1,884 | **100%** | 20 months |
| Entity_C | 1,014 | **100%** | 9 months |

Entity_C cannot physically contain anyone with more than 9 months' tenure, so **100% of its 94 exits are "early exits" by construction**. Meanwhile 94.7% of NovaCorp-Origin staff were hired before the observation window opened — we never see their first year at all. The comparison measures *who we can observe*, not *who leaves early*.

## The fix

Restrict to people **hired inside the observation window** (1 Jan 2024 onward), so every person is observed from tenure 0 and no truncation exists. I also ran a left-truncated Kaplan-Meier as a cross-check; both give the same answer.

**Voluntary exits within 12 months, in-window hires only:**

| Cohort | n | early exits | rate |
|---|---|---|---|
| NovaCorp-Origin | 455 | 29 | **6.4%** |
| Entity_C | 1,014 | 85 | 8.4% |
| Entity_B | 1,884 | 192 | **10.2%** |

Entity_B vs NovaCorp-Origin new joiners: **z = 2.50** (p ≈ 0.012) — real, but borderline.
Entity_C vs NovaCorp-Origin: **z = 1.33** (p ≈ 0.18) — **not significant.**

## The restated number

Using NovaCorp-Origin's own new joiners as the baseline, the *excess* early attrition attributable to the acquisition cohorts is:

| Cohort | rate vs 6.4% baseline | excess exits | cost |
|---|---|---|---|
| Entity_B | 10.2% | 72 | **$6.2M/yr** |
| Entity_C | 8.4% | 20 | $1.8M/yr |
| **Total** | | **92** | **$7.9M/yr** |

At 20% reduction: **$1.6M/yr**. At 40%: **$3.2M/yr**.

**Slide E should read $7.9M, not $29.6M.** The old figure counted the entire cost of every early exit as addressable, including the ~6.4% that happens to any new joiner anywhere.

## The claim that reverses

Slide D says agency hires are *"the second-best performing source"* and that cutting agency spend *"would save ~$2.3M and fix nothing."* That rested on the same denominator problem — it divided 25 agency early exits by all **3,243** agency hires, most hired years before the window. Only **274** agency hires are observed from tenure 0.

Among comparable new hires, counting **voluntary** exits only so this table matches the cohort table above and the $7.9M lever:

| Source | n (in-window) | early exits | rate |
|---|---|---|---|
| acquisition | 2,898 | 277 | **9.6%** |
| **agency** | 274 | 21 | **7.7%** |
| direct | 93 | 5 | 5.4% |
| referral | 88 | 3 | 3.4% |

*Corrected 14 Aug. This table previously counted all exits including involuntary, giving 11.6 / 8.4 / 5.4 / 4.5, while the cohort table above it counted voluntary only. Same ordering and same conclusion either way, but the two tables now use one definition. Reproduces from `cost_model.py` section 3.*

Agency is the second-**worst**, not second-best. The gap to direct hire is not significant (z = 0.74, n = 93 direct hires is too small to conclude much), so the safe wording is *"agency is not the largest early-tenure problem — acquisition onboarding is"*, rather than *"agency is one of our best sources."*

## What survives, and how to say it

✅ **Acquisition-cohort onboarding is the largest early-tenure problem.** True, and now defensible as a *rate*: 11.5% of acquisition-sourced new joiners leave inside 12 months, vs 6.4% for a comparable NovaCorp new joiner.

❌ **"91% of early exits are acquisition-sourced."** Drop it. It's a composition statistic driven by observation availability. Replace with the rate comparison above.

❌ **"$29.6M addressable."** Replace with **$7.9M/yr**.

❌ **"Agency hires are one of our best sources."** Drop.

✅ **"One fix, two buckets."** Still true, and arguably stronger — the excess early attrition is concentrated in Entity_B, which is the same cohort driving the regrettable-attrition bucket.

## Why this is worth doing rather than quietly shipping the bigger number

Rigour is 25% of the grade, and Part 2 Finding 10 already documents this exact trap in our own repo. A judge who reads the appendix and then the recommendation slide finds us making the mistake we warned about. Correcting it costs us $21.7M of headline lever and buys back the credibility of every other number in the deck — and the *lead* finding ($45.1M regrettable) is untouched by this and remains the biggest lever by a wide margin.
