# Team note — read before we lock the deck structure

Three things in `findings.md` (Part 1) don't survive contact with the raw data. I've re-run all of
them; scripts are in this folder. Flagging now because two of them are load-bearing for the current
narrative.

## 1. "68% of exits are push, therefore preventable" — unsafe as written

The brief defines `pathway` as **push = involuntary *or managed* exit**, pull = employee-initiated.
It does **not** mean "disengagement-driven".

- 267 of the 955 push exits are literally involuntary (196 of those are "Involuntary – performance").
- HR flags **3.7%** of push exits as regrettable, vs **26.5%** of pull exits.

So the current headline — *"we're pushing our best people out, 68% is preventable, $24–48M
addressable"* — is contradicted by NovaCorp's own regrettable flag. First question from the CHRO:
*"you say 68% is preventable loss, but my data says those are people we managed out — which is it?"*

**What to do:** don't drop the finding, re-aim it. The interesting thing isn't that 68% is push. It's
that **the two fields disagree**, and the reason they disagree is that the regrettable flag is
broken (see below). That's a stronger story and it's defensible.

## 2. "People go silent before they quit" — the decay doesn't exist

Leavers respond **67.1%** on their first pre-exit survey wave and **66.1%** on their last. There is
no pre-exit decay. They were always quieter than stayers (82.5%), from wave 1.

Good news: the 5.4x attrition spread across response bands is **real and clean** — I checked, there
are zero survey rows dated after anyone's exit date, so it isn't a mechanical artifact.

**What to do:** claim it as a **stable segmentation signal available from wave 1**, not an early
warning that fires as people disengage. That's actually a better recommendation (you can act on day
one, no trend needed). But if we say "scores decay before exit" a judge will check and we lose the
rigour marks.

⚠️ **Also**: as an *individual* flight-risk score this thing fails badly — 23% precision, 901 false
positives, and it fails the four-fifths fairness test on age by 12x. It has to be pitched at team
level. See `SLIDES.md` slide C. This is currently our #1 recommendation and it's the most
attackable thing in the deck.

## 3. Every attrition % needs its denominator stated

The AR's "10.4% voluntary attrition" = 1,400 ÷ 13,403 — that's *total* attrition (includes 267
involuntary) over the *full 2-year window*, on the total roster. Annualised voluntary on active
headcount is **4.7%**. Both are defensible; quoting one while the CHRO is thinking of the other is
not. Pick one, put it in a footnote on every slide. I've standardised on annualised-voluntary-on-active.

---

## What I'm taking

Ethics & Responsible Practice (20%) + Financial Impact Quantification (15%). Concretely:

- **The cost model.** One engine, `cost_model.py`, brief's constants only. Send me any finding and
  I'll return the dollar figure, the sensitivity range and the ROI. Please don't hand-calculate
  costs on your own slides — that's how decks contradict themselves in Q&A.
- **Slides A–D + F** (see `SLIDES.md`): the broken-metric finding, the restated buckets, the
  responsible-use rules for the risk score, and limitations.
- **The appendix** (`ASSUMPTIONS.md`): constants, population decisions, formulas, fairness method.

## The headline I'd like the deck built around

> NovaCorp counts **$14.3M** of regrettable attrition. The real figure is **$45.1M**. The gap exists
> because the `regrettable_flag` never fires for High Performers — **0 out of the 168** who were
> managed out were recorded as a loss. Finance then sized a $22–25M budget line on that flag.

It costs **$0** to fix (it's a definition change), it reframes the entire $42M, and it hits ethics,
rigour and financial quantification at once.
