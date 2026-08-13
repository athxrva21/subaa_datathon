# Appendix A8 — Statistical test register

*Every comparison in this deck, the test behind it, and the result. Tests run with `scipy.stats`. Where a comparison uses survey data, each employee's scores are averaged across waves **before** the comparison, so no person is counted more than once (pseudo-replication avoided). Conventional threshold: p < 0.05.*

---

## Findings we rely on

| # | Claim | Test | Result | p | n |
|---|---|---|---|---|---|
| 1 | Entity_B attrition differs from other cohorts | Chi-square, 4 groups | 10.3 / 7.5 / **15.0** / 9.3 % | **1.9×10⁻¹³** | 13,403 |
| 2 | Entity_B vs Entity_A specifically | Chi-square, pairwise | 15.0% vs 7.5% | **2×10⁻¹³** | 1,884 / 1,950 |
| 3 | Senior leadership trust collapsed in Entity_B | Welch's t | 3.352 → 3.051 (**−0.301**) | **1.5×10⁻²⁵** | 1,938 / 1,697 |
| 4 | Purpose & meaning collapsed in Entity_B | Welch's t | 3.358 → 3.058 (**−0.300**) | **2.6×10⁻²⁵** | 1,938 / 1,697 |
| 5 | …and holds among **active** staff only (not a leaver artifact) | Welch's t | same direction | **4.6×10⁻²⁵** | active only |
| 6 | Manager effectiveness is **not** different | Welch's t | 3.344 vs 3.371 | 0.35 — **null** | 1,938 / 1,697 |
| 7 | Psychological safety is **not** different | Welch's t | 3.351 vs 3.354 | 0.91 — **null** | 1,938 / 1,697 |
| 8 | Entity_B response rate is lower | One-way ANOVA | 83.6 / 83.8 / **62.6** / 68.6 % | **7.0×10⁻³⁰⁴** | 13,096 |
| 9 | Entity_B is paid *above* NovaCorp-Origin | One-way ANOVA | 0.937 / 0.959 / **0.961** / 0.962 | **2.2×10⁻⁷¹** | 13,403 |
| 10 | Entity_B loses Senior Managers (L3) at ~3× | Chi-square | 6.7% vs **18.0%** | **0.0050** | 150 / 150 |
| 11 | HIPO staff leave at 1.5× | Chi-square | 15.0% vs 10.0% | **9.7×10⁻⁸** | 13,403 |
| 12 | Attrition is **not** concentrated under bad managers | Chi-square goodness-of-fit vs team size | worst 10% hold 18.4% of exits | **0.9957 — null** | 1,196 managers |
| 13 | HR's regrettable flag ≠ a value-based definition | Chi-square | 97 of 312 overlap | **<10⁻⁶** | 1,400 |
| 14 | Entity_B new joiners leave early more often | Two-proportion z | 10.2% vs 6.4% | **0.012** (z = 2.50) | 1,884 / 455 |
| 15 | Composite engagement barely differs by entity | One-way ANOVA | 3.377 / 3.366 / 3.280 / 3.346 | 2.5×10⁻⁹ — *significant but trivial* | 13,096 |

**Row 15 is deliberately included.** A significant p-value on a 0.085-point gap is the clearest illustration in this analysis of why statistical significance is not the same as importance — and why the composite index hid the problem.

---

## Findings we tested and did **not** rely on

Reported so the record is complete, not because they carry the argument.

| Claim | Test | Result | p | Why we set it aside |
|---|---|---|---|---|
| Pay compression among high-performing leavers, L1 | Welch's t | 0.962 vs 0.942 | 0.0006 | Real, but narrow — see below |
| …L2 | Welch's t | 0.913 vs 0.915 | 0.81 — null | Not significant |
| …L3 | Welch's t | 0.948 vs 0.917 | 0.040 | n = 34 leavers |
| …L4 | Welch's t | 0.961 vs 0.964 | 0.90 — null | n = 7 leavers |
| Push/pull mix differs by entity | Chi-square | 68 / 68 / 73 / 59 % | 0.061 | Borderline; directionally supportive only |
| Purpose separates leavers from stayers *within* Entity_B | Welch's t | 2.929 vs 3.070 | 0.084 — null | **Load-bearing null:** rules out individual targeting on purpose scores |
| Entity_A vs Entity_C attrition | Chi-square | 7.5% vs 9.3% | 0.106 — null | Entity_C is not a second Entity_B |
| Entity_C new joiners leave early more often | Two-proportion z | 8.4% vs 6.4% | 0.18 — null | Not significant; excluded from the headline |
| Disengagement cutoff at 2.5 separates leavers | Chi-square | 7.4% vs 5.9% | 0.100 | Threshold is a judgement call — see A5 |
| Agency vs direct early-exit rate | Two-proportion z | 8.4% vs 5.4% | 0.46 — null | n = 93 direct hires; no conclusion drawn |

**On pay:** only 2 of 4 levels show a real gap, and across the whole workforce leavers and stayers differ by 0.94 vs 0.95 — practically nothing. Treated as a narrow, targeted fix, never as a driver.

---

## Fairness tests (four-fifths / EEOC adverse-impact screen)

A group's selection rate ÷ the highest group's rate. Below 0.80 warrants investigation. Groups below n = 50 suppressed.

| Flag | Dimension | Worst ratio | Detail | Verdict |
|---|---|---|---|---|
| Proposed silence flag | **Age band** | **0.15** | 18–24: 21.6% flagged vs 45–49: 3.3% | **Fails badly** |
| Proposed silence flag | Role level | 0.15 | L1 9.2% vs L5 1.4% | Fails |
| Proposed silence flag | Acquisition cohort | 0.15 | Entity_C 36.9%, Entity_B 28.2% vs Entity_A 4.1% | Fails |
| HR `regrettable_flag` | Gender (within Outstanding leavers) | 0.60 | M 74.6% / F 59.4% / NB 44.4% | **Under-powered** — n = 67/64/9. Reported as governance risk requiring audit, **not** as established discrimination |

**Silence flag predictive performance:** 901 active staff flagged; precision **22.6%**, recall 18.8%. Wrong roughly three times in four.

---

## Not statistical tests

| Item | Method |
|---|---|
| $42M reconciliation ($43.7M over two years) | Arithmetic on the brief's constants, employee by employee |
| `hire_date` system-entry artifact | Range inspection per cohort (A6 §1.1) |
| Purpose/trust by survey wave | Descriptive; no trend test — the point is the *level on arrival*, not a slope |
| Annual Report reconciliation | Exact numerical match across seven departments (A10) |

---

## Two honest caveats on this page

**Multiple comparisons.** We ran roughly 40 tests. At p < 0.05 you would expect ~2 false positives by chance alone. Our load-bearing findings sit at p < 10⁻¹³, far beyond anything multiplicity could manufacture — but the borderline results (rows 14, and the L3 pay gap at p = 0.040) should be read with that in mind.

**Significance is not size.** With 12,000 employees almost any real difference reaches significance. We report the size of every gap alongside its p-value, and row 15 is included specifically to show a case where the p-value is impressive and the finding is not.
