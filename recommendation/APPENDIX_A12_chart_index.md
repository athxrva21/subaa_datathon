# Appendix A12 — Chart index & cut list

*Which figure goes where, which existing charts we're not using, and why.*

---

## 1. Charts in the main deck

| Slide | Chart | Source file | Status |
|---|---|---|---|
| 3 | Regrettable gap — $14.3M counted vs $45.1M real | `ethics_finance/figures_ethics/E1_regrettable_gap.png` | ✅ exists |
| 4 | Flag rate by performance band × pathway | `E2_flag_never_fires.png` | ✅ exists |
| 5 | The $42M re-apportioned | `E6_buckets_restated.png` | ⚠️ **regenerate** — hiring bucket text changes with the correction |
| 6 | Attrition by legacy entity | `figures/03_attrition_by_legacy_entity.png` | ✅ exists |
| 7 | **Entity_A vs Entity_B across all eight dimensions** | Part 2 script | 🔴 **must extract — highest priority** |
| 8 | Purpose & trust by survey wave, by cohort | Part 2 script | 🔴 **must extract** |
| 9 | Survival by entity | `figures/17_survival_by_entity.png` | ✅ exists |
| 11 | *(table, no chart)* | — | — |
| 12 | Silence flag — adverse impact by age | `E3_adverse_impact_age.png` | ✅ exists |
| 12 | Silence flag — precision | `E4_flag_precision.png` | ✅ exists, use if space |

**Slides 1, 2, 10, 13, 14, 15 are text/table only.** That's intentional — a chart on a recommendation slide competes with the recommendation.

## 2. Charts in the appendix

| Appendix | Chart | Source |
|---|---|---|
| A5 | Sensitivity grid, $24.8–70.8M | `E5_sensitivity.png` |
| A7 | Survival by hire source | `figures/16_survival_by_hire_source.png` |
| A13 | High-value loss by department | *build from A13 table* |
| — | Pre-exit engagement (shows the *absence* of decay) | `figures/05_preexit_engagement_decay.png` |
| — | Non-response, leavers vs stayers | `figures/07_nonresponse_leavers_vs_stayers.png` |
| — | Driver ranking | `figures/18_driver_univariate_strength.png` |

## 3. 🔴 The two that must be extracted

Both live as base64 inside `explore_pt2/findings_part2.md` — pixels in a text file, not image files.

```
1. edit explore_pt2/explore_part2.py -> change DATA_DIR = Path("/mnt/project") to the repo root
2. pip install scipy
3. python explore_part2.py
4. charts appear in explore_pt2/part2b_outputs/figures/
```

Slide 7's eight-dimension chart is the single most important visual in the deck — it is the picture that proves Entity_B's problem is not a manager problem. **Do not ship without it.**

---

## 4. Cut list — Part 1 findings not in the deck

Decided deliberately, not by running out of room. All remain in `findings.md` and are defensible if raised in Q&A.

| Finding | Why it's cut |
|---|---|
| **Recognition gap** (under-recognised high performers, 9.6% vs 8.1%) | 1.2× lift is weak next to Entity_B's 2.0×. Part 1 itself notes it's likely understated but can't quantify by how much. Doesn't survive a "how big is that really?" question. |
| **Pay equity by level / gender** | Gaps are ≤1.0pt where samples are large, and only appear at L5–L7 where n < 80. Leading with pay also contradicts slide 7, where Entity_B is paid *above* NovaCorp-Origin and leaves anyway. |
| **"Frozen middle"** (attrition flat 10.2–10.7% across L1–L4) | A null result. Useful for ruling out a middle-management framing, but there's no recommendation attached. |
| **Manager Pareto / psych safety by team** | The manager finding is now a *negative* — it's on slide 10 as something we rule out, so it doesn't need its own slide. |
| **"68% of exits are push, therefore preventable"** | **Cut on correctness, not space.** "Push" includes 267 involuntary exits; the brief defines it as involuntary-or-managed, not disengagement-driven. See A6 §1.5. |
| **"Employees go silent before they quit"** | **Cut on correctness.** There is no pre-exit decay — leavers go 67.1% → 66.1%. They were always quieter, from wave 1. Reframed on slide 8 as a stable signal available from arrival. |

The last two matter most: both are load-bearing in Part 1's current write-up, and both are wrong as written. `findings.md` should be updated so the repo doesn't contradict the deck.

## 5. Style checklist for every chart

- Palette: `#A100FF` purple · `#00B7C3` teal · `#FF6B6B` coral · `#FFB300` gold · `#460073` deep
- Title states the **finding**, not the variables — "Entity_B's managers are fine; its trust in leadership isn't", not "Engagement dimensions by entity"
- Axis units labelled; every rate carries its denominator
- No chart junk, no 3D, no dual axes unless genuinely necessary
- Readable when printed greyscale — judges may not see it in colour
- n stated on the chart wherever a group is under ~200 people
