# Appendix — cost model assumptions & method

Put this in the appendix (unlimited slides). It exists so that when a judge asks "where did that
number come from", the answer is a page reference, not a recollection.

## 1. Constants — all published by Finance in the case brief §6

| Constant | Value | Used for |
|---|---|---|
| Replacement cost multiplier | 1.50 × annual base salary | attrition buckets |
| Backfill rate | 85% of vacated roles | attrition buckets |
| Superannuation on-cost | 12.0% of base | all salary figures grossed up |
| Disengagement productivity loss | 15% of base salary/yr | disengagement bucket |
| Agency fee rate | 18% of first-year base | hiring bucket |
| Direct hire benchmark | $5,500 fully loaded | hiring bucket |

**Nothing outside this table is used as a benchmark.** The only other numbers we introduce are the
20%/40% intervention-effectiveness rates, which are labelled as assumptions on the slide itself and
shown at both ends so no conclusion depends on the optimistic one.

## 2. Population decisions (the brief explicitly asks us to document these)

| Decision | Choice | Why |
|---|---|---|
| Observation window | 1 Jan 2024 – 31 Dec 2025 = **2.0 years** | stated in brief §4; every rate is divided by 2 to annualise |
| Attrition denominator | **active headcount (12,003)** | a rate quoted against a roster that includes leavers understates it |
| Which exits count as cost | **voluntary only** (1,133 of 1,400) | involuntary exits are a decision, not a loss; including them inflates the problem |
| "High value" | performance band at exit ∈ {Outstanding, High Performer} | the only value proxy available at the point of exit |
| Disengaged | engagement index < 2.5 averaged over the **2 most recent responded waves** | "persistently", per the brief's wording; single-wave dips are noise |
| Non-responders | **retained, not dropped** | brief §4 warns these rows are intentional; they carry the silence signal |

### The denominator that matters most

The FY2025 Annual Report headline is **"10.4% voluntary attrition"**. That figure reproduces exactly
as `1,400 departed / 13,403 total roster`. Two problems:

1. It includes **267 involuntary** exits, so it is not voluntary attrition.
2. It spans the **full two-year** window but is presented as an annual rate.

Like-for-like — voluntary only, annualised, on active headcount — the rate is **4.7%/yr**. Every
department rate in the AR table matches our data to 0.1pp, which confirms the AR was produced from
this same export. We restate the metric and flag the definition gap; we do not use it to attack the
company's reporting.

## 3. Formula

```
replacement_cost($/yr) = 1.50 × 0.85 × Σ(salary_at_exit × 1.12) ÷ 2.0
disengagement($/yr)    = Σ(salary_active × 1.12) × 0.15
agency_premium($/yr)   = Σ max(salary × 0.18 − 5500, 0) ÷ 2.0
```

## 4. Sensitivity

See `figures_ethics/E5_sensitivity.png`. Headline ($45.1M) varies **$24.8M – $70.8M** across
replacement multiplier 1.0–2.0× and backfill 70–100%. We quote **$34–56M** as the defensible band
(±25% around the brief's own constants). **Every cell in the grid exceeds the $14.3M currently
counted** — the finding does not depend on the assumption.

## 5. Fairness testing method

- **Four-fifths (80%) rule**, the standard EEOC adverse-impact screen: a group's selection rate
  divided by the highest group's rate; below 0.80 warrants investigation.
- Applied to (a) HR's `regrettable_flag` among voluntary high-value leavers, and (b) the proposed
  silence flag among all active staff.
- Groups with n < 20 (flag test) / n < 50 (silence test) are suppressed rather than reported.
- **Result (a)** — suggestive but under-powered: within Outstanding leavers the flag fires for 74.6%
  of men, 59.4% of women, 44.4% of non-binary staff (n = 67 / 64 / 9). Reported as a governance risk
  requiring audit, **not** as established discrimination.
- **Result (b)** — unambiguous: age impact ratios fall to **0.08** (18–24: 16.6% flagged vs 45–49:
  1.4%), role level to 0.15, acquisition cohort to 0.08, on groups of 900–1,900 people.

## 6. What we deliberately did not do

- **No demographic features in any risk model.** Gender, cultural background and age band appear in
  this analysis *only* as fairness-audit dimensions, never as predictors. Using them to predict
  attrition would be direct discrimination regardless of accuracy.
- **No individual employees or managers named** on any slide. Manager-level results are aggregated
  and suppressed below 8 reports.
- **No attempt to reverse-engineer the data generator**, per brief §5.
- **No causal language.** Association only.

## 7. Reproducibility

| Script | Produces |
|---|---|
| `cost_model.py` | every dollar figure in the deck, plus reconciliation and sensitivity |
| `ethics_audit.py` | flag-consistency, four-fifths tests, flag precision/recall |
| `make_figures.py` | the six `E*` charts |

All three read only the four supplied CSVs and are deterministic — no seeds, no sampling.
