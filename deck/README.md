# NovaCorp People Analytics Challenge — Team O for 4

**Accenture × SUBAA, August 2026**

---

## What's in this submission

| File | What it is |
|---|---|
| `NovaCorp_executive_summary.pdf` | **Start here.** The whole argument on one page. |
| `NovaCorp_deck.pdf` | **Primary deliverable.** 15 main slides, then 22 appendix pages (A1–A18). |
| `NovaCorp_cohort_dashboard.html` | Interactive cohort diagnostic. Single file, no install, opens by double-click. |
| `NovaCorp_deck.pptx` | Editable source of the deck. |

The main deck is the first 15 pages. Everything from the "Appendix" divider onward is supporting detail, per §7's "no limit on appendix slides". **A18 is our own Q&A prep** — the questions we expect and the page that backs each answer.

---

## Before you open the dashboard

**It has no individual-level data, and that is deliberate.**

The obvious build here is a flight-risk score per employee. We built one, tested it, and did not ship it. On the four-fifths rule it returns impact ratios of **0.08 on age**, 0.15 on role level and 0.08 on acquisition cohort, and its precision is **22.6%** — 901 false positives against 263 true positives. Low survey response is heavily concentrated in the acquisition cohorts, so at individual level the flag would substantially be measuring integration failure rather than intent.

Slides 12 and 13 recommend against deploying it that way, so the dashboard works at cohort level only, with a minimum of 8 responses and suppressed cohorts labelled. There is no employee ID, name or manager ID anywhere in the file — aggregation happens before the data is written.

Appendix A17 is the model card. Appendix A4 has the full fairness results.

---

## The argument, in three beats

1. **You're measuring the wrong thing.** The `regrettable_flag` fires for 153 departures ($14.3M/yr). Applying a value-based definition gives 499 departures ($45.1M/yr). 371 high performers left and were never recorded as a loss.
2. **Here's what that hid.** The loss concentrates in Entity_B, an acquisition still running on its own HR system. Not pay, not managers — trust in leadership and sense of purpose, which collapsed and were diluted to nothing by an eight-dimension composite index.
3. **You've already solved this once.** Entity_A ran the same integration and is now the healthiest cohort in the company.

---

## Reproducing every figure

All numbers come from the four supplied CSVs. No seeds, no sampling, no external benchmarks.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/python explore_part1.py                              # Part 1 charts
cd explore_pt2    && ../.venv/bin/python explore_part2.py      # Part 2 charts + findings
cd ../ethics_finance && ../.venv/bin/python cost_model.py      # every dollar figure
                     && ../.venv/bin/python ethics_audit.py    # fairness tests
                     && ../.venv/bin/python make_figures.py    # E1–E6
cd ../recommendation && ../.venv/bin/python robustness_check.py        # A15
                     && ../.venv/bin/python reconcile_deck_numbers.py  # A14
                     && ../.venv/bin/python make_dashboard.py          # the dashboard
                     && ../.venv/bin/python build_deck.py              # the deck
```

**Appendix A14** traces every figure quoted on a slide back to the script that produces it.

Two figures are computed by two independent implementations that agree to the dollar; the entity attrition rates are computed by four that agree to the decimal.

---

## Corrections and nulls

- An early-tenure lever we originally sized at $29.6M is stated at **$7.9M**. The original counted the baseline early attrition every employer carries. Method in A7.
- Three load-bearing findings are nulls: manager effectiveness, psychological safety and pay each show no Entity_B effect. Each rules out a seven-figure programme. A8 page 2.
- The restated buckets total **$65.2M** against Finance's $42M.

---

*NovaCorp is a fictional organisation and all data is synthetic, per the case brief.*
