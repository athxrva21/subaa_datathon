# Appendix A6 — Data quality register

*The brief states that data preparation is "a substantive analytical step, not a preprocessing formality" and that documenting these decisions "is part of demonstrating analytical rigour." This page records every quality issue we found, what we did about it, and what we checked that came back clean.*

---

## 1. Issues found, and how we handled them

### 1.1 `hire_date` is a system-entry date for acquired staff — **material**

For the three acquired cohorts, `hire_date` records when the employee's record entered NovaCorp's unified system after acquisition, **not** when they began working. The evidence is the clustering:

| Cohort | `hire_date` range | Max observable tenure |
|---|---|---|
| Entity_A | 2023-04-16 → 2023-10-13 | 33 months |
| Entity_B | 2024-05-10 → 2024-09-07 | 20 months |
| Entity_C | 2025-04-05 → 2025-06-04 | 9 months |
| NovaCorp-Origin | 1988-01-11 → 2025-12-17 | 462 months |

`tenure_months` inherits the same artifact (Entity_C mean tenure reads as 7.0 months).

**Impact:** any raw tenure comparison across cohorts measures how long a *record* has existed, not how long a *person* has worked. A naive "exits within 12 months" count makes 100% of Entity_C's exits early exits by construction.

**What we did:** all early-tenure analysis is restricted to employees hired inside the observation window, so every person is observed from tenure 0 and no truncation exists; cross-checked with a left-truncated Kaplan-Meier. This changed our early-tenure lever from $29.6M to **$7.9M** — see appendix A7. Cross-cohort retention over time uses survival curves, never a raw median tenure.

### 1.2 The 2025-H2 performance cycle is absent — **stated in the brief**

`performance.csv` contains only 2024-H1, 2024-H2 and 2025-H1. For employees who left in H2 2025, `performance_band_at_exit` may be up to 12 months stale.

**What we did:** used performance band as a *value proxy at the point of exit*, not as a current-state measure, and flagged the staleness wherever it carries a dollar figure.

### 1.3 307 employees have no engagement records at all — **material**

These employees were never issued a survey in any of the five waves.

- 89 are active and were all hired after wave 5 opened (2025-07-25) — mechanical, not meaningful.
- 218 departed. Of these, 47 left before wave 1 closed — also mechanical.
- **171 were employed while surveys were running and were still never asked.** 152 of them sit on the Entity_B (BambooHR) and Entity_C (PeopleSoft) legacy systems. 60 were rated High Performer or Outstanding.

**What we did:** excluded them from the silence-flag population, because "never issued" is not the same behaviour as "issued and declined" — including them inflates flag precision from 22.6% to 32.7% on a group whose non-response carries a different meaning. We report them separately as a **data-fragmentation finding**: the cohorts most at risk are partly invisible to the instrument used to monitor risk.

### 1.4 Survey non-response is intentional, not missing data — **stated in the brief**

10,264 rows have `response_flag = False` with all eight dimension scores null.

**What we did:** retained every row. Response rate is used as a variable in its own right. Dimension scores are averaged over responded waves only, and **per employee before any group comparison**, so nobody is counted five times (pseudo-replication).

### 1.5 "Push" does not mean "disengagement-driven" — **definitional**

The brief defines `pathway` as push = involuntary *or managed* exit; pull = employee-initiated. It does **not** mean disengagement. 267 of the 955 push exits are literally involuntary, 196 of those recorded as "Involuntary – performance."

**What we did:** removed any claim that 68% push implies 68% preventable. All cost figures use **voluntary exits only** (1,133 of 1,400).

### 1.6 Small samples above Level 4 — **structural**

Role level distribution: L1 7,759 · L2 3,997 · L3 1,265 · L4 279 · L5 78 · L6 16 · L7 8 · L8 1.

**What we did:** report nothing above L4 as a finding. Where a senior-level gap appears (e.g. pay equity at L5–L7), we state the n and decline to draw a conclusion.

### 1.7 The Annual Report's headline attrition metric does not match its label

The FY2025 report states 10.4% "voluntary attrition." That reproduces exactly as 1,400 ÷ 13,403 — **total** exits (including 267 involuntary) across the **full two-year** window, on the total roster. Every department figure matches our all-exits calculation to 0.1pp, which confirms the report was produced from this same export.

**What we did:** restated all rates as annualised voluntary-on-active (**4.7%/yr**) and footnoted the denominator on every slide carrying a rate. We flag the discrepancy for resolution; we do not use it as an accusation.

---

## 2. Integrity checks that came back clean

Documenting what we verified and found sound matters as much as what we found broken.

| Check | Result |
|---|---|
| Duplicate `employee_id` in `employees.csv` | 0 |
| `attrition_log` rows with no matching employee | 0 |
| Employees marked `departed` with no attrition record | 0 — exact 1:1 on all 1,400 |
| `exit_date` disagreement between the two files | 0 of 1,400 |
| `salary` vs `salary_at_exit` disagreement | 0 of 1,400 |
| Date formatting variation | None — all `YYYY-MM-DD` across all files |
| Negative or impossible tenure values | 0 |
| Survey rows dated after an employee's exit date | 0 — the response/attrition link is not a mechanical artifact |
| Nulls outside the two expected fields | None (`exit_date` for active staff; dimensions where `response_flag = False`) |

The data is materially cleaner than the brief's framing implies. **The substantive issues are semantic, not structural** — fields that are well-formed but do not mean what their names suggest (`hire_date`, `pathway`, the Annual Report's "voluntary attrition"). That is the harder failure mode to catch, and it is where our data-preparation effort went.

---

## 3. Population decisions

| Decision | Choice | Rationale |
|---|---|---|
| Observation window | 1 Jan 2024 – 31 Dec 2025 = **2.0 years** | Stated in brief §4. Every rate divided by 2 to annualise. |
| Attrition denominator | **Active headcount (12,003)** | A rate quoted against a roster that includes leavers understates it. |
| Which exits count as cost | **Voluntary only** (1,133) | An involuntary exit is a decision, not a loss. |
| "High value" | `performance_band_at_exit` ∈ {Outstanding, High Performer} | The only value proxy available at the point of exit. |
| Disengaged | Index < 2.5 averaged over the 2 most recent responded waves | "Persistently" per the brief; single-wave dips are noise. |
| Non-responders | **Retained** | Brief §4 warns these rows are intentional. |
| Early-tenure population | Hired on/after 1 Jan 2024 only | Removes the left-truncation bias in §1.1. |
