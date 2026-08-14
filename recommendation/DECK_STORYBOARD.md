# NovaCorp — deck storyboard (15 slides + appendix)

**Owner of this doc:** Suman · **Builds from:** `findings.md` (Pt 1), `findings_part2.md` (Pt 2), `ethics_finance/SLIDES.md` (Moksh), `EARLY_TENURE_CORRECTION.md`
**Audience:** CHRO (primary), CFO (secondary). HR leader, not a data scientist.
**Status:** copy is near-final. Aryan builds design, charts and PDF from here — build spec at the end.

---

## The spine

> NovaCorp cannot fix what it refuses to count. The metric that defines "a departure we regret" never fires for High Performers, so the most expensive problem in the business is invisible on the CHRO's own dashboard — and the $42M was budgeted on top of that blind spot. Once you count properly, the loss concentrates in one place: an acquisition that was never finished. And NovaCorp has already proved it knows how to fix that, because it did it once before.

Three beats: **you're measuring the wrong thing → here's what it was hiding → you've already solved this once.**

---

# SLIDE 1 — Title

**NovaCorp People Analytics Challenge**
*What's driving the $42M — and where to act first*
Team name · 15 August 2026

---

# SLIDE 2 — The question you asked us

**Headline:** *You asked what's driving $42M. We found you're counting $14M of it.*

- Finance sized the annual people cost at **~$42M** across three buckets: regrettable attrition ($22–25M), disengagement ($12–15M), hiring inefficiency ($4–6M).
- We did not set out to re-litigate that number. We set out to find which parts are **tractable**.
- What we found first was a **measurement problem** — and it changes the shape of everything underneath it.

**Say:** "We'll show you three things: what your data is hiding, where the loss actually sits, and what it's worth if you act. All of it uses your own numbers and Finance's own formulas."

---

# SLIDE 3 — ⭐ The headline

**Headline:** *You count $14.3M of regrettable attrition. The real figure is $45.1M.*

**Figure:** `E1_regrettable_gap.png`

- HR's `regrettable_flag` fires on **153 departures** over two years → **$14.3M/yr**.
- Apply a value-based definition — every High Performer or Outstanding employee who **chose** to leave — and it is **499 departures → $45.1M/yr**.
- **371 high-performing people** walked out and were never recorded as a loss.

**Say:** "This isn't an estimate we're arguing with. It's the same replacement-cost formula Finance gave us, applied to a population your flag excludes."

*Source: `attrition_log.csv`; brief §6 constants. Defensible range $34–56M — appendix A5.*

---

# SLIDE 4 — Why the flag misses them

**Headline:** *The flag is a synonym for "Outstanding", not a measure of value lost.*

**Figure:** `E2_flag_never_fires.png`

- Flag rate by rating: **Outstanding 61–72%**. High Performer **15% (pull) / 0% (push)**. Meets Expectations 12% / 1%.
- Of the **168 High Performers who were managed out, zero** were flagged regrettable. Not a low rate — zero.
- The flag is applied **after** the exit, by the same function that approved the exit. It records whether a departure was **convenient**, not whether it was **costly**.

**Say:** "We're not suggesting bad faith. This flag was almost certainly built to spot top-talent loss, and it does — for 'Outstanding'. The failure is that it was then used as a **cost** metric, which it was never designed to be."

*This slide carries the ethics dimension as much as the finance one — a retrospective, self-assessed metric that structurally exonerates the decision-maker is a justification, not a measurement.*

---

# SLIDE 5 — The $42M, restated

**Headline:** *It isn't $42M. On your own formulas it's $65M — and the shape is different too.*

**Figure:** `E6_buckets_restated.png`

| Bucket | Finance | On the data | Why it moved |
|---|---|---|---|
| Regrettable attrition | $22–25M | **$45.1M** | flag excludes High Performers |
| Disengagement productivity | $12–15M | **$17.8M** | 813 staff persistently below 2.5 |
| Hiring inefficiency | $4–6M | **$2.3M** | agency premium is genuinely small |
| **Total** | **$38–46M** | **$65.2M** | |

**Say:** "Only one of these moves in your favour, and it's the smallest one. The agency bucket you were worried about is the least of your problems. The two that moved against you are the two that are hardest to see, which is not a coincidence — both were sized using a definition that excluded the expensive cases."

*Same constants Finance published, same replacement-cost formula. The gap is definitional, not methodological.*

*⚠️ Do **not** claim "91% of early exits are acquisition-sourced" or "agency is one of our best sources" — both were artifacts. See `EARLY_TENURE_CORRECTION.md`.*

---

# SLIDE 6 — Where the loss concentrates

**Headline:** *One acquisition accounts for double the attrition of another — and it's the one still on its own HR system.*

**Figure:** `03_attrition_by_legacy_entity.png` (Pt 1) or Pt 2's entity chart

- Attrition by origin: NovaCorp-Origin **4.5%** · Entity_A **3.6%** · **Entity_B 7.0%** · Entity_C 4.6%.
- Entity_B vs Entity_A: **p = 8×10⁻⁹** on 1,601 and 1,804 active staff. This is the most statistically solid finding in the analysis.
- Entity_B was acquired in FY2023 and **still runs on BambooHR**, two years on. Entity_A was absorbed onto the core system and is now the healthiest cohort in the company.

**Say:** "Entity_B has the worst rate. It is not where the most dollars sit — NovaCorp-Origin holds $29.2M of the $45.1M purely on headcount. Entity_B is where the **leverage** is: $8.4M concentrated in 1,601 people you already know how to fix."

*Footnote on slide: annualised voluntary exits ÷ active headcount, the same convention used on every rate in this deck. An earlier draft quoted 10.3 / 7.5 / 15.0 / 9.3, which was total exits including involuntary over the full roster — the construction we criticise on slide 14. The ratio is 1.9× restated against 2.0× as first drafted, so the finding is unchanged. See A14.*

---

# SLIDE 7 — It isn't pay, and it isn't their managers

**Headline:** *Six of eight engagement dimensions are fine. Two collapsed.*

**Figure:** Pt 2 eight-dimension comparison *(⚠️ needs extracting — see build spec)*

- **Manager effectiveness**: 3.344 vs 3.371 — **no difference** (p = 0.35).
- **Psychological safety**: 3.351 vs 3.354 — **no difference** (p = 0.91).
- **Senior leadership trust**: −0.301 (p = 1.5×10⁻²⁵). **Purpose & meaning**: −0.300 (p = 2.6×10⁻²⁵).
- And it isn't money: Entity_B staff sit at **0.961** compa-ratio vs NovaCorp-Origin's **0.937**. They are paid *better* and leaving anyway.

**Say:** "This rules out the two most expensive things you might have done: a manager training programme, and a retention pay round. Neither would have touched this. What broke is their belief in NovaCorp — not their experience of their own team."

**Why it never showed on your dashboard:** the composite index averages all eight dimensions, so two collapsed scores get diluted by six healthy ones — Entity_B reads 3.280 vs Entity_A's 3.366. A gap of 0.085 that looks like nothing.

---

# SLIDE 8 — They arrived this way, and then went quiet

**Headline:** *There was no decline to detect. Entity_B's first-ever survey was already broken.*

**Figure:** Pt 2 purpose/trust by wave *(needs extracting)*

- Entity_B's **first** measurement: purpose 2.975, trust 3.060 — against NovaCorp-Origin's steady 3.38. A year later: 3.067. **Flat.**
- Survey response rate: Entity_B **62.6%** vs Entity_A **83.8%** — 21 points lower.
- **307 employees were never issued a survey at all** — 152 of the mid-window leavers among them sit on the Entity_B and Entity_C legacy systems. They weren't silent; **they were never asked.**

**Say:** "This matters for what you build. Any early-warning system designed to spot a **decline** will never catch this, because there was no decline. Acquired cohorts have to be measured against the company baseline from their very first survey."

---

# SLIDE 9 — You've already solved this once

**Headline:** *Entity_A is at 3.6% — below NovaCorp's own 4.5%. Integration works; you've proved it.*

**Figure:** `17_survival_by_entity.png` or a simple entity-over-time panel

- Entity_A (FY2022, fully integrated) is now the **safest cohort in the company** — better than NovaCorp-Origin itself.
- Its survey response rate has recovered to **83.8%**, indistinguishable from NovaCorp-Origin.
- Entity_C (late FY2024) is at 4.6% and statistically indistinguishable from Entity_A (p = 0.101) — it is **not** a second Entity_B yet.

**Say:** "This turns the recommendation from 'we hope this helps' into 'you have already done this once, in this company, with this workforce.' And it sets your success measure: track Entity_B against Entity_A's recovery, not against a generic benchmark."

---

# SLIDE 10 — What to do

**Headline:** *Three actions, in order. The first one is free.*

**1 · Redefine what counts as a regrettable loss** — *~$0, policy change, this quarter*
Include High Performer alongside Outstanding; separate the flag from the function that approved the exit; review quarterly. Restates your baseline immediately and fixes next year's $42M at source.

**2 · Finish the Entity_B integration — as a trust problem, not a systems problem** — *inside the guided $40–50M FY26 integration budget*
Migrate off BambooHR. Stabilise the Senior Manager layer first (Entity_B loses L3s at **9.8%/yr vs Entity_A's 2.9%**, a 3.4× gap) — there is otherwise nobody credible left to communicate the integration. Then senior-leadership visibility and honest communication about what the merger means for people personally. **Not** manager training.

**3 · Measure acquired cohorts from day one, at cohort level** — *~$0*
Baseline every acquired group against company norms at their first survey. Track response rate as a health metric in its own right. Fix the 307 who were never surveyed.

**Say:** "Notice what's not on this list: a pay round, a manager training programme, and cutting agency recruitment. The data rules out all three."

---

# SLIDE 11 — What it's worth

**Headline:** *$71M addressable. The cheapest lever is the largest.*

| Lever | Addressable | @20% | @40% | Cost to act |
|---|---|---|---|---|
| Redefine `regrettable_flag` + quarterly review | **$45.1M** | $9.0M | $18.1M | **~$0 (policy)** |
| Disengagement (813 staff below 2.5) | $17.8M | $3.6M | $7.1M | programme-dependent |
| Early-tenure / acquisition onboarding | **$7.9M** | $1.6M | $3.2M | ~$500–800/head |
| *of which Entity_B specifically* | *$6.2M* | *$1.2M* | *$2.5M* | |

**Say before anyone asks:** "The 20% and 40% are **assumptions**, not findings — that's the band typically claimed for targeted retention programmes. We show both so the decision doesn't depend on the optimistic one. The first lever is a definition change, so its return isn't capped by budget at all."

*⚠️ $7.9M is the corrected figure. An earlier draft said $29.6M — that counted the baseline early attrition every employer has. See appendix A7.*

---

# SLIDE 12 — ⚠️ How **not** to act on this

**Headline:** *A "who stopped answering" flag looks free. It flags 21.6% of under-25s and 3.3% of 45–49s.*

**Figure:** `E3_adverse_impact_age.png` (+ `E4_flag_precision.png` if space)

- The obvious move from our own analysis is a flight-risk score built on survey silence. **We recommend against deploying it at individual level.**
- Under the **four-fifths rule** it fails on age (impact ratio **0.15**), on role level (L1 9.2% vs L5 1.4%) and on acquisition cohort (**Entity_C 36.9%, Entity_B 28.2% vs Entity_A 4.1%**).
- It is also **wrong most of the time**: 901 active staff flagged, **precision 23%**. The dominant outcome is a career conversation about someone who was never leaving.
- Low response is heavily concentrated in the acquisition cohorts — so the flag is substantially measuring **integration failure**, not individual intent.

**Say:** "We're showing you the thing we decided not to recommend. If this ever surfaced in a performance or redundancy conversation, you'd have a discrimination exposure that costs more than the attrition does."

---

# SLIDE 13 — How to use it responsibly

**Headline:** *Team-level diagnostic, disclosed to staff, never an individual score.*

1. **Never as an individual score handed to a manager.** 23% precision.
2. **Team level only**, minimum 8 responses, reported as a *diagnostic* not a *prediction*.
3. **Tell employees the participation metric exists.** If the survey was sold as confidential, quietly re-using non-response as a personal risk score breaks that promise — and once staff work it out, response rates collapse and you lose the instrument entirely.

**What we deliberately did not do:**
- **No demographic features in any model.** Gender, age and cultural background appear *only* as fairness-audit dimensions, never as predictors.
- **No individual employees or managers named.** Manager results aggregated, suppressed below 8 reports.
- **No causal language.** Association only.

---

# SLIDE 14 — What we can't tell you

- **Two-year window, annualised.** All rates are voluntary exits ÷ 2 years ÷ active headcount = **4.7%/yr**. Your FY2025 Annual Report's "10.4% voluntary attrition" is actually *total* attrition including 267 involuntary exits, across the *full two years* — it reproduces exactly as 1,400/13,403. **We restate; we don't accuse.** It's worth resolving, because on a strict voluntary reading you have already met the FY2026 sub-9.5% target.
- **We cannot see pre-acquisition Entity_B.** They may have arrived unhappy from their previous employer. We genuinely cannot rule this out.
- **Association, not causation.** Senior Manager churn and collapsed trust move together; we cannot say which drives which.
- **Engagement is only observed for responders**, and leavers responded less — so every disengagement figure is a lower bound.
- **`regrettable_flag`, `performance_band_at_exit` and `stated_exit_reason` are retrospective HR judgements.** We use them as the *object* of analysis, not as ground truth.
- **The 2025-H2 review cycle is missing**, so performance data is up to 12 months stale for some leavers.
- **Small samples above Level 4.** Nothing above L4 is reliable — 279 people at L4, 103 above it.

**Say:** "We'd rather you heard these from us than found them in Q&A."

---

# SLIDE 15 — Close

**Headline:** *Start with the free one.*

- **This quarter:** redefine regrettable. Cost ~$0. It restates your baseline and stops you funding a budget line built on a blind spot.
- **This half:** finish Entity_B — Senior Manager layer first, then leadership visibility. $8.4M concentrated, inside a budget you've already guided.
- **Ongoing:** baseline every acquired cohort from day one. Entity_C is healthy today — it does not have to become the next Entity_B.

**Close on:** "You already have the money set aside — the Annual Report commits to a People Reinvention Programme three times. This is what we'd spend it on, and this is what we'd measure."

---

# APPENDIX (unlimited slides)

| # | Content | Source |
|---|---|---|
| A1 | Constants table — brief §6 only | `ASSUMPTIONS.md` §1 |
| A2 | Population decisions + rationale | `ASSUMPTIONS.md` §2 |
| A3 | Cost formulas | `ASSUMPTIONS.md` §3 |
| A4 | Fairness method + full four-fifths results | `ASSUMPTIONS.md` §5 |
| A5 | Sensitivity grid — $24.8–70.8M | `E5_sensitivity.png` |
| A6 | **Data-quality register** ⚠️ *to write* | see below |
| A7 | **Early-tenure correction — method + restated $7.9M** | `EARLY_TENURE_CORRECTION.md` |
| A8 | **Statistical test appendix — all 18 Pt 2 findings with p-values** ⚠️ *to extract* | `findings_part2.md` |
| A9 | Glossary — no stats background assumed | `findings_part2.md` §"How to read this report" |
| A10 | Annual Report reconciliation, department by department | Pt 2 finding 18 |
| A11 | Reproducibility — script inventory | `ASSUMPTIONS.md` §7 |
| A12 | Chart index | — |

**A6 must cover:** the `hire_date` / `tenure_months` system-entry artifact and how we handled it · the missing 2025-H2 review cycle · the 307 never-surveyed employees · nulls where `response_flag = False` (intentional, retained) · the 1:1 integrity check between `employees.csv` and `attrition_log.csv` · why we chose active headcount as the denominator.

---

# Numbers cheat-sheet — memorise these

| | |
|---|---|
| Counted vs real regrettable | **$14.3M → $45.1M** (range $34–56M) |
| High performers never counted | **371** |
| High Performers managed out, flagged regrettable | **0 of 168** |
| Entity_B vs Entity_A attrition | **7.0% vs 3.6%**/yr, p = 8×10⁻⁹ |
| What collapsed in Entity_B | trust **−0.301**, purpose **−0.300**; managers **no difference** |
| Entity_B pay | **0.961** vs NovaCorp-Origin **0.937** — paid *better* |
| Silence flag | 901 flagged, **23% precision**, four-fifths ratio **0.15** on age |
| Early-tenure addressable | **$7.9M/yr** (not $29.6M) |
| Annualised voluntary attrition | **4.7%** on active headcount |

---

# Q&A prep

**"Are you telling me my HR team is dishonest?"**
No. The flag was built to identify top-talent loss and it does that — for "Outstanding". The failure is that it was then used as a cost metric, which it was never designed to be. That's a governance gap, not a personnel matter.

**"Your number is double Finance's. Which is right?"**
Both, for different questions. Finance priced the departures HR flagged. We priced the departures that cost you money. The gap *is* the finding.

**"How confident are you in $45.1M?"**
Point estimate on Finance's own constants. Defensible range $34–56M, varying the replacement multiplier 1.0–2.0× and backfill 70–100%. **Every cell in that grid is above the $14.3M you currently count.**

**"Can't I just run the silence flag? It's free."**
At team level, yes. As an individual score it fails the four-fifths rule on age by a factor of seven and is wrong 77% of the time.

**"Entity_B is only 1,601 people. Why should I care?"**
You shouldn't care about it for the dollars — NovaCorp-Origin holds $29.2M of the $45.1M on headcount alone. You should care because it's the one place where the cause is identified, the fix is proven, and the budget is already guided.

**"Why didn't you look at Risk & Compliance?"** *(your Annual Report singles it out)*
We did — it's $8.0M of the $45.1M, third-largest by department, and the FAR pressure your report describes is consistent with what we see. We led with Entity_B because it's where the evidence is strongest and the intervention is proven. R&C is in the appendix.

**"What do I do Monday?"**
Redefine regrettable to include High Performer. Costs nothing, restates your baseline immediately, and stops the next budget cycle being built on the same blind spot.

---

# 🔧 BUILD SPEC — for Aryan

**You own:** design, chart production, layout, PDF export. Copy above is near-final — flag anything that doesn't fit rather than rewriting it, so the numbers stay traceable to `cost_model.py`.

**Do first (blocking):**
1. **Extract Part 2's charts.** They're base64-embedded in `findings_part2.md`. Re-run `explore_pt2/explore_part2.py` — **you must first change `DATA_DIR = Path("/mnt/project")` to point at the repo root**, and it needs `scipy` installed. Slides 7 and 8 have no figure until this is done, and slide 7 is the diagnostic core of the deck.
2. **Merge the branch.** `ethics-finance-workstream` was cut before Keya's Part 2 commit — rebase it onto `main` first or Part 2's 2,600 lines get deleted.

**Design notes:**
- Palette is already consistent across Pt 1 and Pt 2: `#A100FF` purple, `#00B7C3` teal, `#FF6B6B` coral, `#FFB300` gold, `#460073` deep. Check E1–E6 match.
- One message per slide, stated in the headline as a **sentence**, not a label. If a slide needs two sentences to explain, it's two slides.
- Audience is an HR leader — no p-values on the face of a slide except slides 6 and 7 where they're doing real work. Everything else goes in the appendix.
- 15 slides is a hard cap. Appendix is unlimited — push detail there aggressively.

**Every dollar figure must come from `cost_model.py`** — except the corrected $7.9M early-tenure figure, which comes from `cost_fix2.py`. Don't hand-calculate anything on a slide.

**Final checks before export:** every rate carries its denominator in a footnote · no individual named anywhere · limitations slide present · PDF under any size limit the Drive imposes · uploaded and confirmed readable by someone else on the team.
