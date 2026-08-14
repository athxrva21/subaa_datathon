"""
Charts built specifically for the deck, where no existing figure makes the point
cleanly. Writes to deck/figures/.

Run from the recommendation/ directory:
    ../.venv/bin/python make_deck_figures.py
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "deck" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

PURPLE, DEEP, TEAL, CORAL, GOLD, GREY = \
    "#A100FF", "#460073", "#00B7C3", "#FF6B6B", "#FFB300", "#5A5A66"

plt.rcParams.update({
    "figure.dpi": 120, "savefig.dpi": 160, "savefig.bbox": "tight",
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlecolor": DEEP,
    "axes.edgecolor": "#DDDDE3", "axes.labelcolor": "#33333A",
    "axes.grid": True, "grid.color": "#ECECF1", "axes.axisbelow": True,
    "legend.frameon": False, "figure.facecolor": "white",
})

WINDOW_YEARS = 2.0
ORDER = ["Entity_A", "NovaCorp-Origin", "Entity_C", "Entity_B"]

emp = pd.read_csv(ROOT / "employees.csv", parse_dates=["hire_date", "exit_date"])
att = pd.read_csv(ROOT / "attrition_log.csv", parse_dates=["exit_date"])
eng = pd.read_csv(ROOT / "engagement.csv", parse_dates=["survey_date"])

emp["vol_exit"] = emp.employee_id.isin(
    set(att[att.exit_type == "voluntary"].employee_id)).astype(int)
emp["is_active"] = (emp.status == "active").astype(int)


def entity_recovery():
    """
    Slide 9. Entity_A is the proof integration works.

    Deliberately NOT a Kaplan-Meier survival curve. NovaCorp-Origin's survival
    curve is dominated by long-tenure staff we only start observing in 2024,
    while the acquired entities are observed from acquisition, so the curve
    makes NovaCorp-Origin look far healthier than its attrition rate actually
    is. That is the left-truncation trap documented in A7, and putting it on
    this slide would contradict the slide's own headline.
    """
    # Response rate is the mean of each employee's own rate, not the pooled rate
    # across all surveys. That matches A8 test 8 and the figures quoted on the
    # slide. Pooling instead would read about 0.4pt higher and contradict them.
    resp = eng.merge(emp[["employee_id", "legacy_entity_code"]], on="employee_id")
    per_emp = resp.groupby(["employee_id", "legacy_entity_code"]).response_flag.mean()
    per_emp = per_emp.reset_index()

    att_rate, resp_rate = {}, {}
    for c in ORDER:
        s = emp[emp.legacy_entity_code == c]
        att_rate[c] = s.vol_exit.sum() / s.is_active.sum() * 100 / WINDOW_YEARS
        resp_rate[c] = per_emp[per_emp.legacy_entity_code == c].response_flag.mean() * 100

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.5))

    def panel(ax, data, title, ylabel, ref_key, better_low):
        vals = [data[c] for c in ORDER]
        ref = data[ref_key]
        colors = []
        for c in ORDER:
            if c == "Entity_A":
                colors.append(TEAL)
            elif c == "Entity_B":
                colors.append(CORAL)
            elif c == ref_key:
                colors.append(GREY)
            else:
                colors.append(PURPLE)
        bars = ax.bar(range(len(ORDER)), vals, color=colors, width=0.66)
        ax.axhline(ref, color=DEEP, ls="--", lw=1.4)
        ax.set_xticks(range(len(ORDER)))
        ax.set_xticklabels([c.replace("NovaCorp-Origin", "NovaCorp\nOrigin") for c in ORDER],
                           fontsize=9.5)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(title)
        ax.set_ylim(0, max(vals) * 1.22)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.03,
                    f"{v:.1f}%", ha="center", fontweight="bold", fontsize=10)
        # Reference label sits just under the line at the far right, clear of
        # the bar-top value labels.
        ax.text(len(ORDER) - 0.35, ref - max(vals) * 0.055,
                "NovaCorp-Origin", color=DEEP, ha="right", va="top", fontsize=8.5,
                fontweight="bold")

    panel(axes[0], att_rate, "Voluntary attrition, per year",
          "% per year", "NovaCorp-Origin", True)
    panel(axes[1], resp_rate, "Survey response rate",
          "% of surveys issued", "NovaCorp-Origin", False)

    fig.suptitle("Attrition and survey response, by legacy entity",
                 fontsize=13.5, fontweight="bold", color=DEEP, y=1.03)
    fig.text(0.5, -0.06,
             "Attrition is annualised voluntary exits over active headcount (n=12,003). "
             "Response rate is the mean of each employee's own rate across five waves "
             "(n=13,096 employees).",
             ha="center", fontsize=7.5, color=GREY)
    fig.savefig(OUT / "S9_entity_recovery.png")
    plt.close(fig)
    print("  -> S9_entity_recovery.png")
    for c in ORDER:
        print(f"     {c:<18} attrition {att_rate[c]:.1f}%/yr   response {resp_rate[c]:.1f}%")


if __name__ == "__main__":
    entity_recovery()
