"""
Appendix pages A1 to A14, appended after the 15-slide main deck.

Content is transcribed from the appendix markdown files and ASSUMPTIONS.md.
Nothing is calculated here. Where a page carries a figure, that figure traces
to cost_model.py, ethics_audit.py or explore_part2.py.

Imported and called by build_deck.py. Not run on its own.
"""
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from build_deck import (blank, rect, textbox, para, bullets, table, picture,
                        callout, W, H, MARGIN, BODY_W,
                        PURPLE, DEEP, TEAL, CORAL, GOLD, INK, GREY, WHITE,
                        EFIG, FIG, P2FIG, SHOW_SOURCE_FOOTNOTES)


def ap_chrome(slide, tag, title, subtitle=None, footnote=None):
    """Appendix furniture. Deliberately quieter than the main deck."""
    rect(slide, 0, 0, W, Inches(0.075), fill=GREY)

    tf = textbox(slide, MARGIN, Inches(0.38), BODY_W, Inches(0.26))
    para(tf, f"APPENDIX {tag}", 11, PURPLE, bold=True, first=True, space_after=0)

    tf = textbox(slide, MARGIN, Inches(0.68), BODY_W, Inches(0.5))
    para(tf, title, 23, DEEP, bold=True, first=True, space_after=0)

    y = Inches(1.15)
    if subtitle:
        tf = textbox(slide, MARGIN, y, Inches(11.6), Inches(0.42))
        para(tf, subtitle, 11.5, GREY, italic=True, first=True, space_after=0,
             line_spacing=1.15)

    if footnote and SHOW_SOURCE_FOOTNOTES:
        tf = textbox(slide, MARGIN, Inches(6.95), Inches(11.2), Inches(0.4))
        para(tf, footnote, 8, GREY, italic=True, first=True, space_after=0)

    tf = textbox(slide, W - MARGIN - Inches(0.8), Inches(6.95), Inches(0.8), Inches(0.25))
    para(tf, tag, 10, GREY, bold=True, first=True, space_after=0, align=PP_ALIGN.RIGHT)


def divider(prs):
    s = blank(prs)
    rect(s, 0, 0, W, H, fill=DEEP)
    rect(s, MARGIN, Inches(3.30), Inches(1.5), Inches(0.07), fill=PURPLE)
    tf = textbox(s, MARGIN, Inches(3.62), Inches(11.4), Inches(1.0))
    para(tf, "Appendix", 44, WHITE, bold=True, first=True, space_after=6)
    para(tf, "A1 to A14. Method, assumptions, every test, and where each number comes from.",
         15, RGBColor_light(), space_after=0)


def RGBColor_light():
    from pptx.dml.color import RGBColor
    return RGBColor(0xC9, 0xA8, 0xEA)


# ---------------------------------------------------------------- A1
def a1(prs):
    s = blank(prs)
    ap_chrome(s, "A1", "Constants",
              "Every constant below is published by Finance in the case brief §6. "
              "Nothing outside this table is used as a benchmark.")
    rows = [
        ["Constant", "Value", "Used for"],
        ["Replacement cost multiplier", "1.50 × annual base salary", "attrition buckets"],
        ["Backfill rate", "85% of vacated roles", "attrition buckets"],
        ["Superannuation on-cost", "12.0% of base", "all salary figures grossed up"],
        ["Disengagement productivity loss", "15% of base salary/yr", "disengagement bucket"],
        ["Agency fee rate", "18% of first-year base", "hiring bucket"],
        ["Direct hire benchmark", "$5,500 fully loaded", "hiring bucket"],
    ]
    table(s, MARGIN, Inches(1.85), Inches(12.1), rows,
          [Inches(4.3), Inches(3.6), Inches(4.2)], row_h=Inches(0.44))

    callout(s, MARGIN, Inches(5.05), Inches(12.0), Inches(1.15),
            "The only numbers we introduce beyond this table are the 20% and 40% "
            "intervention-effectiveness rates on slide 11. Those are labelled as assumptions "
            "on the slide itself and shown at both ends, so no conclusion depends on the "
            "optimistic one.")


# ---------------------------------------------------------------- A2
def a2(prs):
    s = blank(prs)
    ap_chrome(s, "A2", "Population decisions",
              "The brief asks explicitly that these be documented. Each choice is stated "
              "with the reason it was made.")
    rows = [
        ["Decision", "Choice", "Why"],
        ["Observation window", "1 Jan 2024 – 31 Dec 2025 = 2.0 years",
         "Stated in brief §4. Every rate divided by 2 to annualise."],
        ["Attrition denominator", "Active headcount (12,003)",
         "A rate quoted against a roster that still contains leavers understates it."],
        ["Which exits count as cost", "Voluntary only (1,133 of 1,400)",
         "An involuntary exit is a decision the company made, not a loss it suffered."],
        ["“High value”", "Band at exit ∈ {Outstanding, High Performer}",
         "The only value proxy available at the point of exit."],
        ["Disengaged", "Index < 2.5 over the 2 most recent responded waves",
         "“Persistently”, per the brief. Single-wave dips are noise."],
        ["Non-responders", "Retained, not dropped",
         "Brief §4 warns these rows are intentional. They carry the silence signal."],
        ["Early-tenure population", "Hired on/after 1 Jan 2024 only",
         "Removes the left-truncation bias documented in A6 §1.1."],
    ]
    table(s, MARGIN, Inches(1.80), Inches(12.1), rows,
          [Inches(2.9), Inches(3.9), Inches(5.3)], row_h=Inches(0.52), size=11,
          left_cols=(1, 2))


# ---------------------------------------------------------------- A3
def a3(prs):
    s = blank(prs)
    ap_chrome(s, "A3", "Cost formulas",
              "Three formulas produce every dollar figure in the deck. All are the brief's "
              "own, applied to the populations defined in A2.")

    formulas = [
        ("Replacement cost", "1.50 × 0.85 × Σ(salary_at_exit × 1.12) ÷ 2.0",
         "Applied to voluntary exits rated Outstanding or High Performer. Gives $45.1M/yr."),
        ("Disengagement", "Σ(salary_active × 1.12) × 0.15",
         "Applied to the 813 active staff whose index is below 2.5. Gives $17.8M/yr."),
        ("Agency premium", "Σ max(salary × 0.18 − 5,500, 0) ÷ 2.0",
         "Applied to the 274 agency hires made inside the window. Gives $2.3M/yr."),
    ]
    y = Inches(1.85)
    for name, f, note in formulas:
        rect(s, MARGIN, y, Inches(0.05), Inches(1.10), fill=PURPLE)
        tf = textbox(s, MARGIN + Inches(0.25), y, Inches(3.1), Inches(0.35))
        para(tf, name, 14, DEEP, bold=True, first=True, space_after=0)
        tf = textbox(s, MARGIN + Inches(0.25), y + Inches(0.34), Inches(11.4), Inches(0.35))
        p = para(tf, f, 12.5, INK, first=True, space_after=0)
        for r in p.runs:
            r.font.name = "Consolas"
        tf = textbox(s, MARGIN + Inches(0.25), y + Inches(0.70), Inches(11.4), Inches(0.35))
        para(tf, note, 11, GREY, italic=True, first=True, space_after=0)
        y += Inches(1.32)

    callout(s, MARGIN, Inches(6.00), Inches(12.0), Inches(0.75),
            "The early-tenure lever ($7.9M) uses the replacement-cost formula applied to the "
            "excess exits over a 6.4% NovaCorp-Origin new-joiner baseline, not to all early "
            "exits. Method in A7.", accent=GOLD, size=11.5)


# ---------------------------------------------------------------- A4
def a4(prs):
    s = blank(prs)
    ap_chrome(s, "A4", "Fairness method and results",
              "Four-fifths (80%) rule, the standard EEOC adverse-impact screen: a group's rate "
              "divided by the highest group's rate. Below 0.80 warrants investigation.",
              "All figures reproduce from ethics_audit.py. Groups below n = 20 (flag test) and "
              "n = 50 (silence test) are suppressed rather than reported.")
    rows = [
        ["Flag tested", "Dimension", "Worst ratio", "Detail", "Verdict"],
        ["Proposed silence flag", "Age band", "0.08",
         "18–24: 16.6% vs 45–49: 1.4%  (n = 1,253 / 1,017)", "Fails badly"],
        ["Proposed silence flag", "Role level", "0.15",
         "L1 9.2% vs L5 1.4%  (n = 6,931 / 74)", "Fails"],
        ["Proposed silence flag", "Acquisition cohort", "0.08",
         "Entity_C 31.7% vs NovaCorp-Origin 2.4%", "Fails"],
        ["HR regrettable_flag", "Gender, within Outstanding leavers", "0.60",
         "M 74.6% / F 59.4% / NB 44.4%  (n = 67 / 64 / 9)", "Under-powered"],
    ]
    table(s, MARGIN, Inches(1.92), Inches(12.1), rows,
          [Inches(2.5), Inches(2.9), Inches(1.3), Inches(3.8), Inches(1.6)],
          row_h=Inches(0.52), size=10.5, head_size=10.5, left_cols=(3,))

    bullets(s, MARGIN, Inches(4.65), Inches(12.0), Inches(2.0), [
        "**The silence flag result is unambiguous.** It fails on three dimensions at once, on "
        "groups of 900 to 1,900 people. This is why we recommend against individual-level "
        "deployment on slide 12.",
        "**The regrettable_flag result is suggestive but under-powered.** With 9 non-binary "
        "staff in the comparison we report it as a governance risk requiring audit, not as "
        "established discrimination. Saying more than the sample supports would be the same "
        "error we are criticising.",
    ], size=12, gap=12)


# ---------------------------------------------------------------- A5
def a5(prs):
    s = blank(prs)
    ap_chrome(s, "A5", "Sensitivity",
              "How the $45.1M headline moves across the two assumptions we do not control.",
              "Replacement multiplier 1.0–2.0×, backfill 70–100%. Brief's constants are "
              "1.50× and 85%.")
    picture(s, EFIG / "E5_sensitivity.png",
            Inches(0.7), Inches(1.75), Inches(7.2), Inches(4.6))
    bullets(s, Inches(8.25), Inches(2.00), Inches(4.5), Inches(4.2), [
        "Full range across the grid: **$24.8M to $70.8M**.",
        "We quote **$34–56M** as the defensible band, roughly ±25% around the brief's own "
        "constants.",
        "**Every cell in the grid exceeds the $14.3M currently counted.** The finding does "
        "not depend on the assumption. That is the point of showing the grid rather than a "
        "single number.",
    ], size=12.5, gap=14)


# ---------------------------------------------------------------- A6 (2 pages)
def a6_issues(prs):
    s = blank(prs)
    ap_chrome(s, "A6", "Data quality register — issues found",
              "The brief calls data preparation “a substantive analytical step, not a "
              "preprocessing formality”. This records every issue, and what we did about it.")
    rows = [
        ["#", "Issue", "What we did"],
        ["1.1", "hire_date is a system-entry date for acquired staff. Entity_C's whole roster "
                "reads as under 9 months tenure. Material.",
         "Restricted all early-tenure analysis to in-window hires, so everyone is observed "
         "from tenure 0. Changed the lever from $29.6M to $7.9M. See A7."],
        ["1.2", "The 2025-H2 performance cycle is absent, so band at exit can be up to 12 "
                "months stale.",
         "Used performance band as a value proxy at exit, not a current-state measure, and "
         "flagged staleness wherever it carries a dollar."],
        ["1.3", "307 employees have no engagement records. 171 were employed while surveys ran "
                "and were still never asked; 152 sit on Entity_B and Entity_C systems.",
         "Excluded from the silence-flag population, because “never issued” is not “issued and "
         "declined”. Reported separately as a data-fragmentation finding."],
        ["1.4", "10,264 rows have response_flag = False with null dimensions. Intentional, per "
                "the brief.",
         "Retained every row. Response rate used as a variable in its own right. Scores "
         "averaged per employee before any group comparison."],
        ["1.5", "“Push” does not mean disengagement-driven. 267 of 955 push exits are "
                "involuntary. Definitional.",
         "Removed any claim that 68% push implies 68% preventable. All cost figures use "
         "voluntary exits only."],
        ["1.6", "Small samples above Level 4: L5 78, L6 16, L7 8, L8 1.",
         "Report nothing above L4 as a finding. Where a senior gap appears, state the n and "
         "decline to conclude."],
        ["1.7", "The Annual Report's “voluntary attrition” is total attrition over two years "
                "on the full roster.",
         "Restated as annualised voluntary on active (4.7%/yr) and footnoted the denominator "
         "on every slide carrying a rate."],
    ]
    table(s, MARGIN, Inches(1.72), Inches(12.1), rows,
          [Inches(0.6), Inches(5.4), Inches(6.1)], row_h=Inches(0.56), size=9,
          head_size=10, left_cols=(1, 2))


def a6_clean(prs):
    s = blank(prs)
    ap_chrome(s, "A6", "Data quality register — checks that came back clean",
              "Nine integrity checks across the four files, and what each returned.")
    rows = [
        ["Check", "Result"],
        ["Duplicate employee_id in employees.csv", "0"],
        ["attrition_log rows with no matching employee", "0"],
        ["Employees marked departed with no attrition record", "0 — exact 1:1 on all 1,400"],
        ["exit_date disagreement between the two files", "0 of 1,400"],
        ["salary vs salary_at_exit disagreement", "0 of 1,400"],
        ["Date formatting variation", "None — all YYYY-MM-DD across all files"],
        ["Negative or impossible tenure values", "0"],
        ["Survey rows dated after an employee's exit date", "0 — the link is not an artifact"],
        ["Nulls outside the two expected fields", "None"],
    ]
    table(s, MARGIN, Inches(1.80), Inches(7.4), rows,
          [Inches(4.6), Inches(2.8)], row_h=Inches(0.40), size=11, left_cols=(1,))

    x = Inches(8.45)
    rect(s, x, Inches(1.80), Inches(4.25), Inches(4.05), fill=RGBColor_lightbg())
    tf = textbox(s, x + Inches(0.35), Inches(2.10), Inches(3.55), Inches(3.5))
    para(tf, "WHAT THIS MEANS", 10, GREY, bold=True, first=True, space_after=14)
    para(tf, "The data is materially cleaner than the brief's framing implies.", 13, DEEP,
         bold=True, space_after=10, line_spacing=1.15)
    para(tf, "The substantive issues are semantic, not structural. Fields that are well-formed "
             "but do not mean what their names suggest: hire_date, pathway, and the Annual "
             "Report's “voluntary attrition”.", 11.5, INK, space_after=10, line_spacing=1.2)
    para(tf, "That is the harder failure mode to catch, and it is where our data-preparation "
             "effort went.", 11.5, INK, space_after=0, line_spacing=1.2)


def RGBColor_lightbg():
    from pptx.dml.color import RGBColor
    return RGBColor(0xF7, 0xF3, 0xFC)


# ---------------------------------------------------------------- A7
def a7(prs):
    s = blank(prs)
    ap_chrome(s, "A7", "Early-tenure correction: $29.6M → $7.9M",
              "The largest single correction we made to our own work. Reproduces with "
              "cost_model.py §3 and §5, cross-checked independently by cost_fix2.py.")

    tf = textbox(s, MARGIN, Inches(1.68), Inches(5.7), Inches(0.3))
    para(tf, "WHAT WAS WRONG", 10, CORAL, bold=True, first=True, space_after=8)
    bullets(s, MARGIN, Inches(2.00), Inches(5.7), Inches(2.2), [
        "The original defined an early exit as anyone departed with tenure ≤ 12 months, "
        "measured against **all** hires of that source.",
        "But 94.7% of NovaCorp-Origin staff were hired before the window opened, so we never "
        "see their first year. Entity_C cannot contain anyone above 9 months' tenure, so "
        "**100% of its exits are early exits by construction**.",
        "The comparison measured **who we can observe**, not who leaves early.",
    ], size=11.5, gap=11)

    tf = textbox(s, Inches(7.0), Inches(1.68), Inches(5.7), Inches(0.3))
    para(tf, "THE FIX", 10, TEAL, bold=True, first=True, space_after=8)
    rows = [
        ["Cohort", "n", "early exits", "rate"],
        ["NovaCorp-Origin", "455", "29", "6.4%"],
        ["Entity_C", "1,014", "85", "8.4%"],
        ["Entity_B", "1,884", "192", "10.2%"],
    ]
    table(s, Inches(7.0), Inches(2.00), Inches(5.7), rows,
          [Inches(2.3), Inches(1.0), Inches(1.3), Inches(1.1)], row_h=Inches(0.38), size=11)

    tf = textbox(s, Inches(7.0), Inches(3.65), Inches(5.7), Inches(0.7))
    para(tf, "Restricted to people hired inside the window, so everyone is observed from "
             "tenure 0. Cross-checked with a left-truncated Kaplan-Meier.", 11, INK,
         first=True, space_after=0, line_spacing=1.18)

    rows2 = [
        ["Cohort", "rate vs 6.4% baseline", "excess exits", "cost"],
        ["Entity_B", "10.2%", "72", "$6.2M/yr"],
        ["Entity_C", "8.4%", "20", "$1.8M/yr"],
        ["Total", "", "92", "$7.9M/yr"],
    ]
    table(s, MARGIN, Inches(4.50), Inches(12.1), rows2,
          [Inches(3.0), Inches(3.4), Inches(2.7), Inches(3.0)], row_h=Inches(0.42),
          emphasis_rows=(3,))

    callout(s, MARGIN, Inches(6.30), Inches(12.0), Inches(0.62),
            "Only the excess over baseline is addressable. The old figure counted the ~6.4% "
            "early attrition every employer carries. Two claims were retracted with it: see A12.",
            accent=CORAL, size=11)


# ---------------------------------------------------------------- A8 (2 pages)
def a8_main(prs):
    s = blank(prs)
    ap_chrome(s, "A8", "Statistical test register — findings we rely on",
              "Every comparison in this deck, the test behind it, and the result. Run with "
              "scipy.stats, threshold p < 0.05. Survey comparisons average each employee "
              "across waves first, so nobody is counted five times. Attrition rates are "
              "annualised voluntary on active headcount.")
    rows = [
        ["#", "Claim", "Test", "Result", "p", "n"],
        ["1", "Attrition differs by legacy entity", "Chi-square, 4 groups",
         "4.5 / 3.6 / 7.0 / 4.6 %/yr", "6.7×10⁻⁹", "12,003"],
        ["2", "Entity_B vs Entity_A specifically", "Chi-square, pairwise",
         "7.0% vs 3.6%/yr", "8.0×10⁻⁹", "1,601 / 1,804"],
        ["3", "Senior leadership trust collapsed", "Welch's t", "3.352 → 3.051 (−0.301)",
         "1.5×10⁻²⁵", "1,938 / 1,697"],
        ["4", "Purpose & meaning collapsed", "Welch's t", "3.358 → 3.058 (−0.300)",
         "2.6×10⁻²⁵", "1,938 / 1,697"],
        ["5", "…and holds among active staff only", "Welch's t", "same direction",
         "4.6×10⁻²⁵", "active only"],
        ["6", "Manager effectiveness is NOT different", "Welch's t", "3.344 vs 3.371",
         "0.35 — null", "1,938 / 1,697"],
        ["7", "Psychological safety is NOT different", "Welch's t", "3.351 vs 3.354",
         "0.91 — null", "1,938 / 1,697"],
        ["8", "Entity_B response rate is lower", "One-way ANOVA",
         "83.6 / 83.8 / 62.6 / 68.6 %", "7.0×10⁻³⁰⁴", "13,096"],
        ["9", "Entity_B is paid above NovaCorp-Origin", "One-way ANOVA",
         "0.937 / 0.959 / 0.961 / 0.962", "2.2×10⁻⁷¹", "13,403"],
        ["10", "Entity_B loses Senior Managers (L3)", "Chi-square", "2.9% vs 9.8%/yr",
         "0.0047", "140 / 123"],
        ["11", "HIPO staff leave at 1.6×", "Chi-square", "7.3% vs 4.5%/yr",
         "1.2×10⁻⁷", "12,003"],
        ["12", "Attrition NOT concentrated under bad managers", "Chi-square goodness-of-fit",
         "worst 10% hold 18.4% of exits", "0.9957 — null", "1,196 mgrs"],
        ["13", "Regrettable flag ≠ value-based definition", "Chi-square", "97 of 312 overlap",
         "<10⁻⁶", "1,400"],
        ["14", "Entity_B new joiners leave early more", "Two-proportion z", "10.2% vs 6.4%",
         "0.012 (z=2.50)", "1,884 / 455"],
        ["15", "Composite engagement barely differs", "One-way ANOVA",
         "3.377 / 3.366 / 3.280 / 3.346", "2.5×10⁻⁹ — trivial", "13,096"],
    ]
    table(s, MARGIN, Inches(1.88), Inches(12.1), rows,
          [Inches(0.42), Inches(4.15), Inches(2.45), Inches(2.55), Inches(1.35), Inches(1.18)],
          row_h=Inches(0.275), size=8.5, head_size=9, left_cols=(1, 2))

    callout(s, MARGIN, Inches(6.62), Inches(12.0), Inches(0.42),
            "Row 15 is deliberately included. A significant p-value on a 0.085-point gap is the "
            "clearest illustration of why significance is not importance.", accent=GOLD, size=10)


def a8_nulls(prs):
    s = blank(prs)
    ap_chrome(s, "A8", "Statistical test register — the nulls that matter",
              "Findings that came back null. Each one rules out an expensive intervention, "
              "which makes them as load-bearing as the positives.")
    rows = [
        ["Claim tested", "Test", "Result", "p", "Why the null matters"],
        ["Manager effectiveness differs in Entity_B", "Welch's t", "3.344 vs 3.371",
         "0.35", "Rules out a manager training programme, the most expensive obvious response"],
        ["Psychological safety differs in Entity_B", "Welch's t", "3.351 vs 3.354",
         "0.91", "Rules out a team-climate intervention"],
        ["Entity_B is underpaid", "One-way ANOVA", "0.961 vs 0.937 — paid above",
         "2.2×10⁻⁷¹", "Rules out a retention pay round. They are paid better and leave anyway"],
        ["Attrition concentrates under bad managers", "Chi-square GoF",
         "worst 10% hold 18.4%", "0.9957", "Rules out performance-managing a manager tail"],
        ["Purpose separates leavers within Entity_B", "Welch's t", "2.929 vs 3.070",
         "0.084", "Rules out individual targeting on purpose scores"],
        ["Entity_A vs Entity_C attrition", "Chi-square", "3.6% vs 4.6%/yr",
         "0.101", "Entity_C is not a second Entity_B — yet"],
    ]
    table(s, MARGIN, Inches(1.90), Inches(12.1), rows,
          [Inches(3.3), Inches(1.7), Inches(2.4), Inches(1.0), Inches(3.7)],
          row_h=Inches(0.62), size=10, head_size=10.5, left_cols=(1, 4))

    callout(s, MARGIN, Inches(6.05), Inches(12.0), Inches(0.72),
            "Three of the six nulls each rule out a seven-figure programme. Slide 10's "
            "“notice what's not on this list” rests entirely on this page.", size=11.5)


# ---------------------------------------------------------------- A9
def a9(prs):
    s = blank(prs)
    ap_chrome(s, "A9", "Glossary",
              "No statistics background assumed. Every term used in this deck, in plain English.")
    left = [
        ("p-value", "If there were no real difference between two groups, how surprising would "
                    "a gap this big be from luck alone? Below 0.05 by convention. It is not the "
                    "size of an effect."),
        ("Statistically significant", "Shorthand for “unlikely to be a coincidence”. It does "
                                      "not mean big or important."),
        ("Chi-square test", "Used when comparing rates or categories between groups."),
        ("Welch's t-test", "Used when comparing the average of a number between two groups."),
        ("Left truncation", "When people only become visible partway through their tenure. "
                            "Ignoring it makes newer cohorts look like they leave faster. See A6 §1.1."),
        ("Pseudo-replication", "Counting the same person once per survey wave, which makes "
                               "results look more certain than they are. Avoided here."),
        ("Four-fifths rule", "The standard EEOC adverse-impact screen. Below 0.80 warrants "
                             "investigation."),
        ("Precision / recall", "Of everyone a flag identifies, precision is the share who "
                               "actually leave. Recall is the share of leavers it catches."),
    ]
    right = [
        ("Compa-ratio", "Salary divided by the midpoint of the pay range for that role and "
                        "level. 1.00 = paid exactly at midpoint."),
        ("HIPO", "“High potential.” A talent-review tag marking a likely future leader. "
                 "Separate from a performance rating."),
        ("Push vs pull", "Push = the organisation drove or managed the exit. Pull = an outside "
                         "opportunity drew them away. Push includes genuinely involuntary "
                         "exits and does not mean disengagement-driven."),
        ("Regrettable attrition", "HR's label for a departure the company didn't want. Here it "
                                  "is a retrospective judgement recorded after the exit, not a "
                                  "measurement. That is the subject of slides 3 and 4."),
        ("Composite index", "One number made by averaging several scores. It can hide a serious "
                            "problem in one component by averaging it against healthy ones, "
                            "which is what happened to Entity_B."),
        ("Backfill rate", "The share of vacated roles actually refilled, 85% per the brief. "
                          "Unfilled roles incur no replacement cost."),
        ("FAR", "Financial Accountability Regime. Australian legislation effective March 2024 "
                "imposing personal accountability on senior financial executives. Named in "
                "NovaCorp's Annual Report as a driver of Risk & Compliance attrition."),
    ]

    for items, x in [(left, MARGIN), (right, Inches(7.0))]:
        tf = textbox(s, x, Inches(1.70), Inches(5.75), Inches(5.1))
        for i, (t, b) in enumerate(items):
            para(tf, t, 11.5, DEEP, bold=True, first=(i == 0), space_after=1)
            para(tf, b, 9.5, INK, space_after=8, line_spacing=1.12)


# ---------------------------------------------------------------- A10
def a10(prs):
    s = blank(prs)
    ap_chrome(s, "A10", "Annual Report reconciliation",
              "We cross-checked against NovaCorp's published FY2025 Annual Report to confirm we "
              "describe the same workforce. Headcounts matched exactly. The attrition metric "
              "did not match its label.",
              "Seven independent exact matches on the attrition column is not coincidence. The "
              "published metric is total attrition, including the 267 involuntary exits.")
    rows = [
        ["Department", "AR “voluntary attrition”", "Our total attrition", "Our voluntary only",
         "Annualised voluntary on active"],
        ["Retail Banking", "9.3%", "9.3%", "7.7%", "4.2%"],
        ["Technology", "10.4%", "10.4%", "8.5%", "4.7%"],
        ["Risk & Compliance", "11.8%", "11.8%", "9.6%", "5.5%"],
        ["Insurance", "10.3%", "10.3%", "8.0%", "4.5%"],
        ["Wealth Management", "10.5%", "10.5%", "7.9%", "4.4%"],
        ["Corporate Operations", "11.6%", "11.6%", "9.7%", "5.5%"],
        ["Executive Leadership", "8.3%", "8.3%", "7.4%", "4.0%"],
        ["Group", "10.4%", "10.4%", "8.5%", "4.7%"],
    ]
    table(s, MARGIN, Inches(2.05), Inches(12.1), rows,
          [Inches(3.0), Inches(2.4), Inches(2.2), Inches(2.1), Inches(2.4)],
          row_h=Inches(0.42), size=11, emphasis_rows=(8,))

    callout(s, MARGIN, Inches(5.90), Inches(12.0), Inches(0.85),
            "Active employees, departures and all seven department headcounts matched the "
            "Annual Report exactly, which is what makes the attrition column meaningful. "
            "We restate the metric and flag the definition gap. We do not use it as an "
            "accusation.", size=11.5)


# ---------------------------------------------------------------- A11
def a11(prs):
    s = blank(prs)
    ap_chrome(s, "A11", "Reproducibility",
              "Every figure in this deck regenerates from the four supplied CSVs. No seeds, no "
              "sampling, no external benchmarks.")
    rows = [
        ["Script", "Produces"],
        ["ethics_finance/cost_model.py",
         "Every dollar figure in the deck, the Annual Report reconciliation, the sensitivity "
         "grid and the entity attrition table"],
        ["ethics_finance/ethics_audit.py",
         "Flag consistency, all four-fifths tests, flag precision and recall"],
        ["ethics_finance/make_figures.py", "The six E-charts, including E6 on slide 5"],
        ["explore_part1.py", "Part 1's 21 charts, including slide 6's entity chart"],
        ["explore_pt2/explore_part2.py",
         "Part 2's 15 charts and 18 findings, including slides 7 and 8"],
        ["recommendation/cost_fix2.py",
         "Independent cross-check of the corrected early-tenure lever"],
        ["recommendation/reconcile_deck_numbers.py",
         "The denominator audit and population table behind A2 and A14"],
        ["recommendation/make_deck_figures.py", "Slide 9's entity recovery chart"],
        ["recommendation/build_deck.py", "This deck"],
    ]
    table(s, MARGIN, Inches(1.85), Inches(12.1), rows,
          [Inches(4.2), Inches(7.9)], row_h=Inches(0.44), size=10.5, left_cols=(1,))

    callout(s, MARGIN, Inches(6.05), Inches(12.0), Inches(0.72),
            "Dependencies are pinned in requirements.txt. From a clean clone: create the venv, "
            "install, then run each script from its own directory. Two independent "
            "implementations agree on the early-tenure lever; four agree on the entity rates.",
            accent=TEAL, size=11)


# ---------------------------------------------------------------- A12
def a12(prs):
    s = blank(prs)
    ap_chrome(s, "A12", "What we cut, and why",
              "Decided deliberately, not by running out of room. All remain in the repo and "
              "are defensible if raised.")
    rows = [
        ["Finding", "Why it is not in the deck"],
        ["Recognition gap — under-recognised high performers leave at 9.6% vs 8.1%",
         "A 1.2× lift is weak next to Entity_B's 1.9×. Doesn't survive a “how big is that "
         "really?” question."],
        ["Pay equity by level and gender",
         "Gaps are ≤1.0pt where samples are large, and only appear at L5–L7 where n < 80. "
         "Leading with pay also contradicts slide 7, where Entity_B is paid above "
         "NovaCorp-Origin and leaves anyway."],
        ["“Frozen middle” — attrition flat across L1–L4",
         "A null result. Useful for ruling out a middle-management framing, but no "
         "recommendation attaches to it."],
        ["Manager Pareto and psychological safety by team",
         "The manager finding is now a negative. It appears on slide 10 as something we rule "
         "out, so it does not need its own slide."],
        ["“68% of exits are push, therefore preventable”",
         "Cut on correctness, not space. Push includes 267 involuntary exits; the brief defines "
         "it as involuntary-or-managed, not disengagement-driven. See A6 §1.5."],
        ["“Employees go silent before they quit”",
         "Cut on correctness. There is no pre-exit decay. Leavers respond at 70.6% in wave 1 "
         "and 70.3% in wave 5, and the gap to stayers narrows. Reframed on slide 8 as a stable "
         "signal available from arrival."],
        ["“91% of early exits are acquisition-sourced” and “agency is one of our best sources”",
         "Both retracted. Artifacts of the left-truncation problem in A6 §1.1. On a "
         "like-for-like population agency is the second-worst source, not the second-best. "
         "See A7."],
    ]
    table(s, MARGIN, Inches(1.80), Inches(12.1), rows,
          [Inches(4.4), Inches(7.7)], row_h=Inches(0.56), size=9.5, head_size=10.5,
          left_cols=(1,))


# ---------------------------------------------------------------- A13
def a13(prs):
    s = blank(prs)
    ap_chrome(s, "A13", "Risk & Compliance, and the department view",
              "NovaCorp's Annual Report singles out Risk & Compliance. We looked, and it is "
              "real — but it is not where we would act first.")
    # Deliberately not using Part 1's 20_business_impact_sizing.png here. That
    # chart sizes the loss with a 0.5-1.0x multiplier the brief does not specify
    # and carries a "'push' / preventable" bar, which is the 68% claim retracted
    # in A6 §1.5. It would contradict slide 5 on the same page as the trace table.
    rows = [
        ["Department", "High-value exits", "Cost/yr", "Roster", "High-value loss rate"],
        ["Corporate Operations", "82", "$7.7M", "1,509", "5.4%"],
        ["Risk & Compliance", "83", "$8.0M", "2,022", "4.1%"],
        ["Wealth Management", "59", "$5.5M", "1,549", "3.8%"],
        ["Insurance", "67", "$6.1M", "1,781", "3.8%"],
        ["Retail Banking", "107", "$9.3M", "3,280", "3.3%"],
        ["Technology", "96", "$8.0M", "3,032", "3.2%"],
        ["Executive Leadership", "5", "$0.5M", "230", "2.2%"],
    ]
    table(s, MARGIN, Inches(1.72), Inches(6.5), rows,
          [Inches(2.15), Inches(1.15), Inches(0.95), Inches(0.9), Inches(1.35)],
          row_h=Inches(0.37), size=10, head_size=9.5, emphasis_rows=(1, 2))

    bullets(s, Inches(7.5), Inches(1.72), Inches(5.25), Inches(4.6), [
        "**The Annual Report is right to be concerned.** R&C loses high-value people at a "
        "materially higher **rate** than the large divisions. Technology carries 50% more "
        "headcount and loses the same dollars.",
        "**Corporate Operations is worse still, at 5.4%**, and appears nowhere in the Annual "
        "Report's commentary. We raise it as a finding requiring follow-up, not a "
        "recommendation, because we have not established a mechanism.",
        "**Why we didn't lead with R&C.** FAR imposes personal liability on senior regulatory "
        "staff from March 2024. That is a **pull** problem in a tight external market, and the "
        "classic response is compensation benchmarking, which the Annual Report already "
        "commits to. We would be recommending what NovaCorp has already decided to do.",
    ], size=10.5, gap=11)

    callout(s, MARGIN, Inches(4.90), Inches(6.5), Inches(1.35),
            "Entity_A is the proven precedent. It ran the same integration and now sits at "
            "3.6%/yr, below NovaCorp-Origin's own rate. There is no equivalent proof that a "
            "compensation response fixes FAR-driven regulatory attrition.", accent=TEAL,
            size=10.5)

    callout(s, MARGIN, Inches(6.42), Inches(12.0), Inches(0.5),
            "Both cuts are in the data and both are correct. We chose the one with an "
            "identified cause, a proven fix and a guided budget already attached.", size=11)


# ---------------------------------------------------------------- A14
def a14(prs):
    s = blank(prs)
    ap_chrome(s, "A14", "Where every number comes from",
              "Each figure quoted on a slide, traced to the script that produces it. Run the "
              "script, get the number. Two independent implementations agree on the "
              "early-tenure lever; four agree on the entity attrition rates.")
    rows = [
        ["Slide", "Figure", "Value", "Source"],
        ["3", "Regrettable as counted / value-based", "$14.3M → $45.1M", "cost_model.py §1"],
        ["3", "High performers never counted", "371", "cost_model.py §1"],
        ["5", "Three buckets restated", "$45.1M · $17.8M · $2.3M", "cost_model.py §1–3"],
        ["5", "Restated total against Finance's $42M", "$65.2M", "cost_model.py"],
        ["6", "Attrition by legacy entity", "4.5 / 3.6 / 7.0 / 4.6 %/yr", "cost_model.py §6"],
        ["6", "Entity_B concentration", "$8.4M in 1,601 active", "cost_model.py §5"],
        ["7", "Trust and purpose gaps", "−0.301 and −0.300", "explore_part2.py §7g"],
        ["7", "Compa-ratio", "0.961 vs 0.937", "explore_part2.py §7f"],
        ["8", "Entity_B first survey", "purpose 2.975, trust 3.060", "explore_part2.py §7i"],
        ["9", "Entity_A recovery", "3.6%/yr, 83.8% response", "make_deck_figures.py"],
        ["10", "Senior Manager gap", "9.8%/yr vs 2.9%", "explore_part2.py §7h"],
        ["11", "Lever table, all rows", "$45.1M / $17.8M / $7.9M / $6.2M", "cost_model.py §5"],
        ["12", "Four-fifths ratios", "0.08 age · 0.15 level · 0.08 cohort", "ethics_audit.py §3"],
        ["12", "Flag precision", "263 true / 901 false, 22.6%", "ethics_audit.py §4"],
        ["14", "Annualised voluntary rate", "4.7%/yr", "cost_model.py §0"],
        ["14", "Annual Report reconciliation", "1,400 / 13,403 = 10.4%", "cost_model.py §0"],
    ]
    table(s, MARGIN, Inches(1.85), Inches(12.1), rows,
          [Inches(0.85), Inches(4.5), Inches(3.85), Inches(2.9)],
          row_h=Inches(0.275), size=9, head_size=9.5, left_cols=(1, 3))

    callout(s, MARGIN, Inches(6.58), Inches(12.0), Inches(0.45),
            "Method notes for the figures restated during the build are in A6 §1.5, §1.7 "
            "and A7.", size=10)


# ---------------------------------------------------------------- A15
def a15(prs):
    s = blank(prs)
    ap_chrome(s, "A15", "Does the Entity_B finding survive controls?",
              "The obvious challenge to slide 6 is that Entity_B might simply sit in "
              "departments or levels that lose people anyway. We tested it. It does not.",
              "Logistic model on voluntary exit, baseline Entity_A, n = 13,136 with 1,133 events. "
              "Reproduce with robustness_check.py.")

    rows = [
        ["Model", "Entity_B vs Entity_A", "95% CI", "p"],
        ["Controlling for department, role level, pay and high-potential status",
         "1.95×", "1.55 – 2.44", "8.4×10⁻⁹"],
        ["…and additionally for tenure", "1.92×", "1.53 – 2.41", "1.6×10⁻⁸"],
    ]
    table(s, MARGIN, Inches(1.92), Inches(12.1), rows,
          [Inches(6.1), Inches(2.2), Inches(2.0), Inches(1.8)],
          row_h=Inches(0.46), size=11.5, emphasis_rows=(1,), left_cols=())

    bullets(s, MARGIN, Inches(3.55), Inches(5.9), Inches(2.9), [
        "**The effect holds either way.** Slide 6 quotes a 1.9× rate ratio. The adjusted "
        "odds ratio is 1.95, so the headline is not an artifact of what Entity_B does or "
        "where it sits.",
        "**Department explains very little.** Only one of six department terms reaches "
        "p < 0.05, and every odds ratio sits between 0.77 and 1.00. Risk & Compliance is "
        "exactly 1.00 once entity is in the model.",
        "**High-potential status replicates independently.** OR 1.59 (p = 3.6×10⁻⁶) here, "
        "against the 1.64× lift in A8 test 11 computed a different way.",
    ], size=11.5, gap=12)

    x = Inches(7.0)
    rect(s, x, Inches(3.55), Inches(5.75), Inches(2.9), fill=RGBColor_lightbg())
    tf = textbox(s, x + Inches(0.38), Inches(3.82), Inches(5.0), Inches(2.5))
    para(tf, "WHY TENURE IS REPORTED SEPARATELY", 10, GREY, bold=True, first=True,
         space_after=12)
    para(tf, "tenure_months is the system-entry artifact from A6 §1.1, so for the acquired "
             "cohorts it is close to a restatement of entity itself:", 11, INK,
         space_after=9, line_spacing=1.16)
    para(tf, "Entity_C 0–9 months  ·  Entity_B 0–20  ·  Entity_A 7–33  ·  "
             "NovaCorp-Origin 0–462", 10.5, DEEP, bold=True, space_after=9)
    para(tf, "Controlling for it is close to controlling for the thing being measured, so we "
             "report both models rather than picking the flattering one. Baseline is Entity_A "
             "because that is the comparison the deck makes. NovaCorp-Origin is the worst "
             "choice of baseline here, since it is the cohort the artifact distorts most.",
         11, INK, space_after=0, line_spacing=1.16)

    callout(s, MARGIN, Inches(6.48), Inches(12.0), Inches(0.4),
            "This does not establish cause. It rules out the most likely confounders, which is "
            "a different and weaker claim, and the one we make.", accent=GOLD, size=10.5)


# ---------------------------------------------------------------- A16
def a16(prs):
    s = blank(prs)
    ap_chrome(s, "A16", "What to measure, and when you can actually read it",
              "Targets are Entity_A's current position. Milestones are paced to the survey "
              "cadence NovaCorp actually runs.",
              "Baselines from cost_model.py. Targets are Entity_A's present position.")
    rows = [
        ["Metric", "Entity_B today", "Target (Entity_A today)", "First readable", "Why this one"],
        ["Survey response rate", "62.6%", "83.8%", "Next wave",
         "Moves first and costs nothing to measure. The leading indicator."],
        ["Senior leadership trust", "3.051", "3.352", "Next wave",
         "One of the two dimensions that actually collapsed."],
        ["Purpose & meaning", "3.058", "3.358", "Next wave",
         "The other one."],
        ["Employees never surveyed", "152 on B and C systems", "0", "Next wave",
         "You cannot manage a cohort you are not asking. Fixable before the wave issues."],
        ["Senior Manager (L3) attrition", "9.8%/yr", "2.9%/yr", "2 quarters",
         "The layer that has to carry the integration message."],
        ["Voluntary attrition", "7.0%/yr", "3.6%/yr", "3–4 quarters",
         "The outcome. Moves last, so do not judge the programme on it early."],
    ]
    table(s, MARGIN, Inches(1.95), Inches(12.1), rows,
          [Inches(2.85), Inches(2.0), Inches(2.3), Inches(1.35), Inches(3.6)],
          row_h=Inches(0.44), size=10.5, head_size=10, left_cols=(4,))

    # Three columns rather than stacked rows. Stacked, these ran into the table
    # above and the footnote below.
    x = MARGIN
    for label, body, accent in [
        ("BEFORE THE NEXT WAVE", "Redefine the regrettable flag, separate it from the function "
                                 "that approves exits, restate the baseline, and add the 152 "
                                 "unsurveyed staff to the issue list. All policy, all ~$0.",
         PURPLE),
        ("AT THE NEXT WAVE", "The first real read. Response rate and the two collapsed "
                             "dimensions, against Entity_A's trajectory rather than Entity_B's "
                             "own past. Attrition will not have moved.", CORAL),
        ("THE WAVE AFTER", "Confirm direction rather than declare success. Two consecutive "
                           "wave-on-wave improvements in response rate is the earliest "
                           "defensible signal.", TEAL),
    ]:
        rect(s, x, Inches(5.30), Inches(3.87), Inches(0.05), fill=accent)
        tf = textbox(s, x, Inches(5.49), Inches(3.87), Inches(0.28))
        para(tf, label, 10.5, accent, bold=True, first=True, space_after=8)
        para(tf, body, 10.5, INK, space_after=0, line_spacing=1.18)
        x += Inches(4.11)

    callout(s, MARGIN, Inches(6.52), Inches(12.0), Inches(0.44),
            "Anchored to waves, not days: NovaCorp's ran 122, 92, 123 and 181 days apart, mean "
            "4.2 months and widening. A 90-day plan would promise a reading the cadence cannot "
            "deliver — and a leading indicator read twice a year is not a leading indicator.",
            accent=GOLD, size=10)


# ---------------------------------------------------------------- A17
def a17(prs):
    s = blank(prs)
    ap_chrome(s, "A17", "Model card — cohort diagnostic",
              "Intended use, prohibited use, and known limits for the accompanying dashboard.")

    cols = [
        ("INTENDED USE", TEAL, [
            "Cohort-level diagnostic for HR and integration leads.",
            "Identifying which parts of the organisation resemble Entity_B before its attrition "
            "rose, so integration effort can be directed.",
            "Tracking cohorts against the A16 measures over time.",
        ]),
        ("PROHIBITED USE", CORAL, [
            "Any decision about an individual. The file contains no employee, manager or team "
            "identifier, so this is enforced by construction rather than by policy.",
            "Performance management, redundancy selection, or promotion input.",
            "Publishing cohort scores to managers without the fairness context in A4.",
        ]),
        ("KNOWN LIMITS", GOLD, [
            "Diagnostic, not predictive. It has no validated forward accuracy and none is claimed.",
            "Engagement is observed only for responders, so every score is a lower bound on a "
            "partially observed population.",
            "Component weights (40/40/20) are a judgement, not a finding. They are shown "
            "separately in the tool so the score can be audited.",
            "Eight cohorts covering 44 people are suppressed below the response floor.",
        ]),
    ]
    x = MARGIN
    for title, accent, items in cols:
        rect(s, x, Inches(1.78), Inches(3.87), Inches(0.05), fill=accent)
        tf = textbox(s, x, Inches(1.98), Inches(3.87), Inches(0.3))
        para(tf, title, 10.5, accent, bold=True, first=True, space_after=12)
        for it in items:
            para(tf, "•  " + it, 11, INK, space_after=10, line_spacing=1.18)
        x += Inches(4.11)

    rect(s, MARGIN, Inches(5.35), Inches(12.1), Inches(1.35), fill=RGBColor_lightbg())
    tf = textbox(s, MARGIN + Inches(0.4), Inches(5.60), Inches(11.3), Inches(1.0))
    para(tf, "Why there is no individual-level version", 12.5, DEEP, bold=True, first=True,
         space_after=6)
    para(tf, "We built and tested one. On the four-fifths rule it returns impact ratios of 0.08 "
             "on age, 0.15 on role level and 0.08 on acquisition cohort, and its precision is "
             "22.6% — 901 false positives against 263 true ones. Low response is concentrated in "
             "the acquisition cohorts, so at individual level the flag would substantially be "
             "measuring integration failure rather than intent, so we did not ship it.", 11, INK, space_after=0,
         line_spacing=1.18)

    callout(s, MARGIN, Inches(6.90), Inches(12.0), Inches(0.4),
            "If a participation metric is ever used, staff should be told it exists. A survey "
            "sold as confidential and quietly re-used as a risk score costs you the instrument.",
            size=10)


# ---------------------------------------------------------------- A18
def _qa_page(prs, tag, title, subtitle, pairs, footnote=None):
    s = blank(prs)
    ap_chrome(s, tag, title, subtitle, footnote)
    y = Inches(1.72)
    for q, a, ref in pairs:
        tf = textbox(s, MARGIN, y, Inches(11.9), Inches(0.28))
        para(tf, "“" + q + "”", 12.5, DEEP, bold=True, first=True, space_after=4)
        tf = textbox(s, MARGIN, y + Inches(0.30), Inches(10.3), Inches(0.62))
        para(tf, a, 11, INK, first=True, space_after=0, line_spacing=1.18)
        if ref:
            tf = textbox(s, Inches(11.1), y + Inches(0.30), Inches(1.6), Inches(0.3))
            para(tf, ref, 9.5, PURPLE, bold=True, first=True, space_after=0,
                 align=PP_ALIGN.RIGHT)
        y += Inches(1.05)
    return s


def a18_a(prs):
    _qa_page(prs, "A18", "Questions we expect — the number",
             "Prepared answers, with the page that backs each one. Anyone on the team can "
             "present from this.",
             [
              ("Your number is double Finance's. Which is right?",
               "Both, for different questions. Finance priced the departures HR flagged. We "
               "priced the departures that cost you money. The gap is the finding, not a "
               "disagreement about arithmetic — we used their formula and their constants.",
               "Slides 3–5"),
              ("Your buckets total $65M, not $42M. Haven't you just inflated the problem?",
               "Two of the three moved against you and one moved in your favour, and we show "
               "all three. The hiring bucket you were most worried about is the smallest thing "
               "here at $2.3M against Finance's $4–6M. If we were inflating, that is the number "
               "we would have left alone.",
               "Slide 5"),
              ("How confident are you in $45.1M?",
               "It is a point estimate on your own constants. The defensible range is $34–56M, "
               "varying the replacement multiplier 1.0–2.0× and backfill 70–100%. Every cell in "
               "that grid is above the $14.3M you currently count, so the finding does not "
               "depend on the assumption.",
               "A5"),
              ("You changed your own figure from $29.6M to $7.9M. Why trust the rest?",
               "Because we found it, said so, and showed the method. The original counted the "
               "baseline early attrition every employer carries as if it were addressable. "
               "Correcting it cost us $21.7M of headline and is the reason to believe the "
               "numbers we kept.",
               "A7"),
              ("How do we know any of these numbers are right?",
               "Every figure on a slide traces to the script that produces it, listed page by "
               "page. Two independent implementations agree on the early-tenure lever to the "
               "dollar; four agree on the entity attrition rates to the decimal. Run them "
               "yourself.",
               "A14, A11"),
             ])


def a18_b(prs):
    _qa_page(prs, "A18", "Questions we expect — the recommendation",
             "Continued.",
             [
              ("Are you telling me my HR team is dishonest?",
               "No. The flag was almost certainly built to spot top-talent loss, and it does "
               "that for Outstanding. The failure is that it was then used as a cost metric, "
               "which it was never designed to be. That is a governance gap, not a personnel "
               "matter.",
               "Slide 4"),
              ("Isn't Entity_B just sitting in your worst departments?",
               "No. Controlling for department, role level, pay and high-potential status, "
               "Entity_B still leaves at 1.95× Entity_A (95% CI 1.55–2.44). Only one of six "
               "department terms is significant, and Risk & Compliance comes out at exactly "
               "1.00 once entity is in the model.",
               "A15"),
              ("Entity_B is only 1,601 people. Why should I care?",
               "You shouldn't care about it for the dollars — NovaCorp-Origin holds $29.2M of "
               "the $45.1M on headcount alone. You should care because it is the one place "
               "where the cause is identified, the fix is proven inside your own company, and "
               "the budget is already guided.",
               "Slides 6, 9"),
              ("Can't I just run the silence flag? It's free.",
               "At team level, yes. As an individual score it fails the four-fifths rule on age "
               "by a factor of twelve and is wrong roughly three times in four. If it ever "
               "surfaced in a performance or redundancy conversation, the exposure would cost "
               "more than the attrition does.",
               "Slides 12–13, A4"),
              ("What would change your mind?",
               "Pre-acquisition Entity_B engagement data. If they arrived unhappy from their "
               "previous employer, the integration story weakens considerably and we cannot "
               "currently rule that out. A shorter survey cadence would also test it: if "
               "response rate does not move within two waves of the flag change, our leading "
               "indicator is wrong.",
               "Slide 14, A16"),
             ])


APPENDIX = [divider, a1, a2, a3, a4, a5, a6_issues, a6_clean, a7, a8_main,
            a8_nulls, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18_a, a18_b]
