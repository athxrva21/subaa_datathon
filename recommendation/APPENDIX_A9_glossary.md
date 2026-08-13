# Appendix A9 — Glossary

*No statistics background assumed. Every term used in this deck, in plain English.*

---

## Statistical terms

**p-value** — a number between 0 and 1 answering: *"if there were actually no real difference between these two groups, how surprising would it be to see a gap this big just from random luck?"* A small p-value (below **0.05** by convention) means the gap is unlikely to be a fluke. A large one (say 0.5) means it could easily be noise. **A p-value is not the size of an effect** — a tiny, unimportant gap can still have a small p-value if the sample is large, so we report the size of the gap and its p-value together, every time.

**Statistically significant** — shorthand for "this gap is unlikely to be a coincidence." It does **not** mean "big" or "important" — only "probably real."

**Chi-square test** — used whenever we compare *rates* or *categories* between groups ("does attrition differ by legacy entity?").

**t-test (Welch's)** — used when comparing the *average* of a number (like compa-ratio or an engagement score) between two groups.

**ANOVA / Kruskal-Wallis** — like a t-test, but comparing an average across *more than two* groups at once (used here for the four legacy entities).

**Two-proportion z-test** — compares two percentages directly (used for the early-tenure rates).

**Kaplan-Meier / survival curve** — the probability an employee is still present at a given tenure. It correctly handles the fact that different groups have been observable for different lengths of time, which a raw average tenure cannot.

**Left truncation** — when people only become visible in the data partway through their tenure. Most NovaCorp-Origin staff were hired before the observation window, so we never see their first year. Ignoring this makes newer cohorts look like they leave faster. See A6 §1.1.

**Pseudo-replication** — a common mistake where the same person is counted several times (once per survey wave), making results look more certain than they are. Avoided here by averaging each person to a single value before comparing groups.

**Four-fifths rule** — the standard EEOC adverse-impact screen. A group's selection rate divided by the highest group's rate; below 0.80 warrants investigation.

**Precision / recall** — of everyone a flag identifies, precision is the share who actually leave; recall is the share of all leavers the flag catches. A flag can have high recall and terrible precision by simply flagging everyone.

## HR and business terms

**Compa-ratio** — an employee's salary divided by the midpoint of the standard pay range for their role and level. 1.00 = paid exactly at the market midpoint; 0.90 = paid 10% below it.

**HIPO** — "high-potential." A formal tag from NovaCorp's talent-review process marking someone as a likely future leader. Separate from their performance rating.

**Push vs. pull** — how an exit is classified. **Push** = the organisation drove or managed the exit. **Pull** = an outside opportunity drew the person away. ⚠️ Note that "push" includes genuinely involuntary exits — it does *not* mean "disengagement-driven." See A6 §1.5.

**Regrettable attrition** — HR's label for a departure the company genuinely didn't want. In NovaCorp's data this is a retrospective judgement recorded after the exit, not a measurement — which is the subject of slides 3 and 4.

**Legacy entity** — which company an employee originally worked for. NovaCorp-Origin = always part of NovaCorp. Entity_A / B / C = acquired companies, folded in at different times (Entity_A FY2022, Entity_B FY2023, Entity_C late FY2024).

**Role level (L1–L8)** — seniority tier. L1 = Analyst / junior individual contributor. L2 = Manager. L3 = Senior Manager. L4 = Director. L5+ = Managing Director and above.

**Layer / tier** — a level in the org chart treated as a group. "The Senior Manager layer" = everyone at Level 3.

**Cohort** — a group treated together because they share something. Here it usually means everyone who came from the same acquired company.

**Churn** — people leaving and needing replacing. Same idea as attrition or turnover.

**Composite / index score** — one number made by averaging several separate scores. Useful for a dashboard, but it can hide a serious problem in one component by averaging it against healthy ones — which is exactly what happened to Entity_B. See slide 7.

**Engagement index** — the mean of the eight pulse-survey dimensions, responded waves only.

**Backfill rate** — the share of vacated roles actually refilled (85% per the brief). Roles left unfilled don't incur a replacement cost.

**Superannuation on-cost** — Australia's compulsory employer retirement contribution, 12.0% of base salary from 1 July 2025. Applied on top of every salary figure in the cost model.

**FAR (Financial Accountability Regime)** — Australian legislation effective March 2024 imposing personal accountability obligations on senior executives at regulated financial institutions. Referenced in NovaCorp's Annual Report as a driver of Risk & Compliance attrition.
