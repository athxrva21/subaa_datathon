# Ethics + Financial Quantification — slide pack

**Owner:** Moksh · **Covers:** Ethics & Responsible Practice (20%) + Financial Impact Quantification (15%) = **35% of total marks**

Every dollar figure in the team deck should come from `cost_model.py` so we cannot contradict
ourselves in Q&A. If someone wants a finding priced, send it to me and I'll run it through the
same engine.

Figures referenced live in `../figures_ethics/`. Numbers regenerate with:

```
python cost_model.py      # every table below
python ethics_audit.py    # the fairness tests
python make_figures.py    # the charts
```

---

## The through-line

> NovaCorp cannot fix what it refuses to count. The metric that defines "a departure we regret"
> never fires for High Performers — so the single most expensive problem in the business is
> invisible on the CHRO's own dashboard, and the $42M was budgeted on top of that blind spot.

That one sentence carries both of my dimensions: it is a **measurement-ethics failure** that causes
a **costing failure**. Fixing it costs nothing and is the highest-return action available.

---

# SLIDE A — "You are not measuring what you think you're measuring"

**Headline:** *NovaCorp counts $14M of regrettable attrition. The real figure is $45M.*

**Figure:** `E1_regrettable_gap.png`

**Body (3 bullets max):**
- HR's `regrettable_flag` fires on **153 departures** over two years → **$14.3M/yr**.
- Apply a value-based definition — *every High Performer or Outstanding employee who chose to
  leave* — and it is **499 departures → $45.1M/yr**.
- **371 high-performing people** walked out and were never recorded as a loss.

**Say out loud:** "This isn't an estimate we're arguing with. It's the same replacement-cost formula
Finance gave us, applied to a population their flag excludes."

---

# SLIDE B — "Here's why the flag misses them"

**Headline:** *The flag is a synonym for 'Outstanding', not a measure of value lost.*

**Figure:** `E2_flag_never_fires.png`

**Body:**
- Regrettable-flag rate by rating: **Outstanding 61–72%**, High Performer **15% / 0%**,
  Meets Expectations **12% / 1%**.
- Split by pathway, it collapses: of the **168 High Performers who were managed out, zero** were
  flagged regrettable. Not a low rate — **zero**.
- The flag is applied *after* the exit by the same function that approved the exit. It records
  whether the departure was **convenient**, not whether it was **costly**.

**This is the ethics core.** A retrospective, self-assessed metric that structurally exonerates the
decision-maker is not a measurement — it's a justification. And Finance sized a $22–25M budget line
on it.

---

# SLIDE C — "Before you deploy a flight-risk score, look who it flags"

**Headline:** *A 'who stopped answering' flag is an age proxy — it flags 16.6% of under-25s and 1.4% of 45–49s.*

**Figure:** `E3_adverse_impact_age.png` (pair with `E4_flag_precision.png` if space allows)

**Body:**
- The proposed silence flag (answers <50% of survey waves) selects **901 of 12,003 active staff**.
- Under the **four-fifths rule** it fails on age (impact ratio down to **0.08**), role level
  (L1 9.2% vs L5 1.4%) and acquisition cohort (**Entity_C 31.7%, Entity_B 23.2% vs NovaCorp-Origin 2.4%**).
- It is also **wrong 77% of the time**: 263 flagged people left, **901 flagged people didn't**, and
  it misses 1,137 leavers entirely (precision 23%, recall 19%).

**The recommendation this forces:**
1. **Never** as an individual score handed to a manager. 77% false positives means the dominant
   outcome is a career conversation about someone who was never leaving.
2. Report it **at team level** (≥8 responses) as a *diagnostic*, not a *prediction*.
3. Tell employees the participation metric exists. If engagement surveys were sold as confidential,
   quietly re-using non-response as a personal risk score breaks that promise — and once staff work
   it out, response rates collapse and the instrument is gone.

**Caveat to state, not hide:** low response is heavily concentrated in the acquisition cohorts, so
this flag is substantially measuring **integration failure**, not individual intent. That is a
better problem to solve anyway — and it points at the same Entity_B/C fix as the rest of the deck.

---

# SLIDE D — "The $42M is real, but mis-apportioned"

**Headline:** *Same $42M, different shape — the big bucket is bigger and the small one is smaller.*

**Figure:** `E6_buckets_restated.png`

| Bucket | Finance | Restated on the data | Why it moved |
|---|---|---|---|
| Regrettable attrition | $22–25M | **$45.1M** | flag excludes High Performers |
| Disengagement productivity | $12–15M | **$17.8M** | 813 persistently disengaged (index <2.5) |
| Hiring inefficiency | $4–6M | **$2.3M** | agency premium is small — and agency isn't the problem |

**The hiring-bucket reversal is a strong Q&A moment.** The brief frames this bucket as agency
hiring. Early-exit rate (left within 12 months) by source:

| acquisition | agency | referral | graduate | direct |
|---|---|---|---|---|
| **7.0%** | 0.8% | 0.4% | 0.3% | 0.2% |

**91% of early exits are acquisition-sourced.** Agency hires are the second-*best* performing source.
Cutting agency spend would save ~$2.3M and fix nothing. The waste is acquisition-cohort onboarding —
the same root cause as the Entity_B concentration in bucket 1. **One fix, two buckets.**

---

# SLIDE E — "What it's worth if you act" *(shared with the recommendations owner)*

| Lever | Addressable | @20% reduction | @40% reduction | Cost to act |
|---|---|---|---|---|
| Redefine `regrettable_flag` + quarterly review | $45.1M | $9.0M | $18.1M | **~$0 (policy)** |
| Early-tenure / acquisition onboarding | $29.6M | $5.9M | $11.8M | ~$500–800/head |
| Entity_B integration + retention | $8.4M | $1.7M | $3.3M | inside the guided $40–50M FY26 integration budget |

**Say this before anyone asks:** "The 20% and 40% are **assumptions**, not findings — that's the band
typically claimed for targeted retention programmes. We show both so you can see the decision doesn't
depend on the optimistic one. The first lever is a definition change, so its return is effectively
uncapped by budget."

**Honest framing on Entity_B:** it has the worst *rate* (15.0%) but NovaCorp-Origin holds the most
*dollars* ($29.2M of the $45.1M) purely on headcount. Don't let the team claim Entity_B is where the
money is — it's where the **leverage** is.

---

# SLIDE F — Limitations *(the brief warns decks without this get scrutinised MORE)*

- **Two-year window, annualised.** All rates are voluntary exits ÷ 2 years ÷ active headcount. The
  FY2025 Annual Report's "10.4% voluntary attrition" is actually *total* attrition (includes 267
  involuntary exits) over the *full two years* against the total roster — it reproduces exactly as
  1,400/13,403. Like-for-like, the annualised voluntary rate is **4.7%**. We restate; we don't
  accuse.
- **Engagement is only observed for responders.** 441 active staff have no usable score. Every
  disengagement figure is a lower bound on a partially observed population.
- **`regrettable_flag`, `performance_band_at_exit` and `stated_exit_reason` are retrospective HR
  judgements**, not measurements. We use them as the *object* of analysis, not as ground truth.
- **The demographic skew in the regrettable flag is suggestive, not established.** Within
  Outstanding leavers the flag fires for 74.6% of men vs 59.4% of women vs 44.4% of non-binary
  staff, but group sizes are 9–67. We report it as a governance risk warranting audit — we do **not**
  claim proven discrimination. *(The age/level/entity skew on the silence flag is a different story —
  those groups are 900–1,900 people and the effect is unambiguous.)*
- **No causal claim.** Everything here is association. We cannot say fixing recognition *causes*
  retention; we can say the population is identifiable and the cost of ignoring it is sized.
- **2025-H2 review cycle is missing** from the data, so the most recent performance signal is up to
  12 months stale for some employees.

---

# Q&A — what the CHRO will actually ask

**"Are you telling me my HR team is dishonest?"**
No. The flag was almost certainly designed to identify top-talent loss, and it does that — for
"Outstanding". The failure is that it was then used as a *cost* metric, which it was never built to
be. That's a governance gap, not bad faith. The fix is a definition and a quarterly review, not a
personnel matter.

**"Your number is double Finance's. Which is right?"**
Both, for different questions. Finance priced the departures HR flagged. We priced the departures
that cost you money. The gap *is* the finding. And we're not re-litigating the $42M — the brief
didn't ask us to.

**"How confident are you in $45.1M?"**
Point estimate under the brief's own constants. The defensible range is **$34–56M** — see
`E5_sensitivity.png`, which varies the replacement multiplier 1.0–2.0x and backfill 70–100%. Every
cell in that grid is above what you're currently counting.

**"Can I just run the silence flag anyway? It's free."**
You can, at team level. As an individual score it fails the four-fifths rule on age by a factor of
twelve, and it's wrong 77% of the time. If it ever surfaces in a performance or redundancy
conversation you have a discrimination exposure that costs more than the attrition.

**"What do I do Monday?"**
Three things, in order: (1) redefine regrettable to include High Performer, cost ~$0, restates your
baseline immediately; (2) put a 90-day structured onboarding on acquisition-cohort hires, where 91%
of early exits sit; (3) run the flight-risk diagnostic at team level only, with the fairness audit
attached.

---

## Numbers cheat-sheet (memorise these five)

| | |
|---|---|
| Counted today vs real | **$14.3M → $45.1M** (range $34–56M) |
| High performers never counted | **371** |
| High Performers managed out, flagged regrettable | **0 of 168** |
| Silence flag: false positives / precision | **901 / 23%** |
| Early exits that are acquisition-sourced | **91%** |
