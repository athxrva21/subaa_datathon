# NovaCorp People Analytics Challenge

Accenture × SUBAA, August 2026. Team **O for 4** — Aryan, Atharva, Keya, Mokshith, Suman.

## Submission

Everything for submission is in [`deck/`](deck/):

| File | |
|---|---|
| `NovaCorp_executive_summary.pdf` | The argument on one page |
| `NovaCorp_deck.pdf` | 15 main slides + 22 appendix pages |
| `NovaCorp_cohort_dashboard.html` | Cohort diagnostic, single file, no install |
| `README.md` | Notes for the judges |

## The finding

NovaCorp's `regrettable_flag` fires on 153 departures ($14.3M/yr). A value-based definition —
every High Performer or Outstanding employee who chose to leave — gives 499 ($45.1M/yr).
371 high performers left and were never recorded as a loss, and of the 168 High Performers
managed out, zero were flagged.

Once counted properly, the loss concentrates in Entity_B, an acquisition still running on its
own HR system. Not pay, not managers: senior leadership trust and purpose, both diluted to
nothing by an eight-dimension composite index. Entity_A ran the same integration and is now the
healthiest cohort in the company.

## Repository layout

| Path | Owner | Contents |
|---|---|---|
| `explore_part1.py`, `findings.md`, `figures/` | Atharva | Part 1 exploration, 21 charts |
| `explore_pt2/` | Keya | Part 2 deep dive, 18 findings, 15 charts |
| `ethics_finance/` | Mokshith | Cost model, fairness audit, E1–E6 charts |
| `recommendation/` | Suman, Aryan | Storyboard, appendices A1–A18, deck and dashboard builders |
| `deck/` | Aryan | Built submission |

## Reproducing

Every figure comes from the four supplied CSVs. No seeds, no sampling, no external benchmarks.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/python explore_part1.py
cd explore_pt2    && ../.venv/bin/python explore_part2.py          && cd ..
cd ethics_finance && ../.venv/bin/python cost_model.py             \
                  && ../.venv/bin/python ethics_audit.py           \
                  && ../.venv/bin/python make_figures.py           && cd ..
cd recommendation && ../.venv/bin/python robustness_check.py       \
                  && ../.venv/bin/python reconcile_deck_numbers.py \
                  && ../.venv/bin/python make_deck_figures.py      \
                  && ../.venv/bin/python make_dashboard.py         \
                  && ../.venv/bin/python build_deck.py
```

Then export the PDF:

```bash
cd deck && soffice --headless --convert-to pdf --outdir . NovaCorp_deck.pptx
```

Appendix A14 traces every figure on a slide back to the script that produces it. The entity
attrition rates are computed independently in four places and the early-tenure lever in two.
