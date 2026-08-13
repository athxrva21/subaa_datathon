# Handover → Aryan

**You own:** the appendix assembly and the pitch deck build. Everything below is written content — your job is to get it into slides and out as a PDF, not to write it from scratch.

**Deadline:** 15 Aug, 11:59pm, uploaded to the shared Google Drive.

---

## What you're getting

| File | What it is |
|---|---|
| `DECK_STORYBOARD.md` | 15 slides, near-final copy. Headline, bullets, figure, source and speaker note for each. |
| `EARLY_TENURE_CORRECTION.md` | Why the $29.6M lever became $7.9M. Becomes appendix A7. |
| `APPENDIX_A6_data_quality.md` | Data quality register. Drop in as-is. |
| `APPENDIX_A13_risk_compliance.md` | R&C + department breakdown. Drop in as-is. |
| `survival_fix.py`, `cost_fix2.py` | Reproduce the corrected numbers. |
| `ethics_finance/` (Moksh) | `SLIDES.md`, `ASSUMPTIONS.md`, `cost_model.py`, six E-charts. |

---

## 🔴 Do these two first — everything else is blocked on them

**1. Merge the branch safely.**
`ethics-finance-workstream` was cut from `0e234fa`, *before* Keya's Part 2 commit. A naive merge deletes `explore_pt2/` — 2,600 lines of her work. Rebase the branch onto `main` first, or merge `main` into it, then verify `explore_pt2/` still exists before you push anything.

**2. Extract the Part 2 charts.**
They're base64-embedded inside `findings_part2.md` — they exist as pixels in a markdown file, not as image files. Two slides have no figure until this is fixed, and **slide 7 is the diagnostic core of the whole deck.**

To regenerate: open `explore_pt2/explore_part2.py`, change `DATA_DIR = Path("/mnt/project")` to the repo root, `pip install scipy`, then run it. Charts land in `explore_pt2/part2b_outputs/figures/`.

The two you must have:
- **Entity_A vs Entity_B across all eight engagement dimensions** → slide 7. This is the picture that proves it's not a manager problem.
- **Purpose/trust by survey wave, by cohort** → slide 8. This is the picture that proves it was broken on arrival.

---

## Appendix — 13 pages

| # | Content | Status |
|---|---|---|
| A1 | Constants table | ✅ `ASSUMPTIONS.md` §1 |
| A2 | Population decisions | ✅ `ASSUMPTIONS.md` §2 (also A6 §3) |
| A3 | Cost formulas | ✅ `ASSUMPTIONS.md` §3 |
| A4 | Fairness method + four-fifths results | ✅ `ASSUMPTIONS.md` §5 |
| A5 | Sensitivity grid $24.8–70.8M | ✅ `E5_sensitivity.png` |
| A6 | Data quality register | ✅ written |
| A7 | Early-tenure correction | ✅ written |
| A8 | **Statistical test appendix — 18 Pt 2 findings with p-values** | ⚠️ **you extract** |
| A9 | Glossary | 🟡 lift verbatim from `findings_part2.md` → "How to read this report" |
| A10 | Annual Report reconciliation by department | 🟡 in Pt 2 finding 18, needs a table |
| A11 | Script inventory / reproducibility | ✅ `ASSUMPTIONS.md` §7 |
| A12 | Chart index | ⚠️ you build once figures are final |
| A13 | Risk & Compliance + department breakdown | ✅ written |

**A8 is the one that matters.** Rigour is 25% of the grade and Part 2 is our strongest rigour evidence — 18 findings, every one with a real significance test — and right now it's the least visible work in the project. It doesn't need to be pretty: a table of finding / test used / result / p-value / n is enough.

---

## Build notes

- **15 slides is a hard cap.** Appendix is unlimited — push detail there aggressively.
- **Palette** is already consistent across Pt 1 and Pt 2: `#A100FF` purple, `#00B7C3` teal, `#FF6B6B` coral, `#FFB300` gold, `#460073` deep. Check E1–E6 match.
- **Headlines are sentences, not labels.** "The flag is a synonym for Outstanding" — not "Regrettable flag analysis."
- **Audience is an HR leader.** No p-values on the face of a slide except slides 6 and 7, where they're doing real work. Everything else to the appendix.
- **Every dollar comes from `cost_model.py`** — except the $7.9M early-tenure figure, which comes from `cost_fix2.py`. Don't hand-calculate on a slide; that's how decks contradict themselves in Q&A.

**Changes to Moksh's slides you must carry through** (his `SLIDES.md` predates the correction):
- Slide E: early-tenure lever is **$7.9M**, not $29.6M. @20% = $1.6M, @40% = $3.2M.
- Slide D: **delete** "91% of early exits are acquisition-sourced" and **delete** "agency hires are the second-best performing source." Both were artifacts. Replace with the rate comparison in `EARLY_TENURE_CORRECTION.md`.

---

## Before you export

- [ ] Every rate carries its denominator in a footnote
- [ ] No individual employee or manager named anywhere
- [ ] Limitations slide present (slide 14) — the brief says decks without one get scrutinised *more*
- [ ] Team name on the title slide
- [ ] Exactly 15 slides in the main deck
- [ ] Exported as PDF
- [ ] Uploaded to the shared Drive, and someone other than you has confirmed it opens
