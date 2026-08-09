"""Figures for the ethics + financial-quantification slides. Writes to figures_ethics/."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path

OUT = Path("figures_ethics"); OUT.mkdir(exist_ok=True)
PURPLE, DEEP, TEAL, CORAL, GOLD, GREY = "#A100FF", "#460073", "#00B7C3", "#FF6B6B", "#FFB300", "#5A5A66"
plt.rcParams.update({
    "figure.dpi": 120, "savefig.dpi": 160, "savefig.bbox": "tight",
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlecolor": DEEP,
    "axes.edgecolor": "#DDDDE3", "axes.labelcolor": "#33333A",
    "axes.grid": True, "grid.color": "#ECECF1", "axes.axisbelow": True,
    "legend.frameon": False, "figure.facecolor": "white",
})
emp = pd.read_csv("../employees.csv", parse_dates=["hire_date", "exit_date"])
att = pd.read_csv("../attrition_log.csv", parse_dates=["exit_date"])
eng = pd.read_csv("../engagement.csv", parse_dates=["survey_date"])
exits = att.merge(emp, on="employee_id", suffixes=("", "_e"))
HIGH = ["Outstanding", "High Performer"]
W, SUPER = 2.0, 0.12
cost = lambda d: 1.5 * 0.85 * d.salary_at_exit.sum() * (1 + SUPER) / W / 1e6   # $M per year


def save(fig, name):
    fig.savefig(OUT / name); plt.close(fig); print("  ->", name)


# 1 --------------------------------------------------------------- the gap
vol = exits[exits.exit_type == "voluntary"]
a, c = cost(vol[vol.regrettable_flag]), cost(vol[vol.performance_band_at_exit.isin(HIGH)])
fig, ax = plt.subplots(figsize=(9, 4.6))
ypos = np.arange(3)
ax.barh(ypos, [a, 23.5, c], color=[GREY, "#C9C9D2", PURPLE], height=.62)
ax.set_yticks(ypos)
ax.set_yticklabels(["What NovaCorp\ncounts today", "Finance's\nstated bucket",
                    "Every high performer\nwho chose to leave"])
for y, v, n in zip(ypos, [a, 23.5, c], ["153 people", "assumption", "499 people"]):
    ax.text(v + 1.2, y, f"${v:.1f}M   ({n})", va="center", fontweight="bold", color=DEEP)
ax.set_xlim(0, 60); ax.set_xlabel("Replacement cost, $M per year")
ax.set_title("NovaCorp under-counts its most expensive problem by 3x")
ax.annotate("", xy=(c, 2.42), xytext=(a, 2.42), arrowprops=dict(arrowstyle="<->", color=CORAL, lw=2))
ax.text((a + c) / 2, 2.55, f"${c-a:.0f}M invisible to the current metric",
        ha="center", color=CORAL, fontweight="bold")
ax.set_ylim(-.6, 2.85); save(fig, "E1_regrettable_gap.png")

# 2 ------------------------------------------------- the flag never fires
order = ["Outstanding", "High Performer", "Meets Expectations", "Below Expectations"]
p = (exits.pivot_table(index="performance_band_at_exit", columns="pathway",
                       values="regrettable_flag", aggfunc="mean") * 100).reindex(order)
n = exits.pivot_table(index="performance_band_at_exit", columns="pathway",
                      values="regrettable_flag", aggfunc="size").reindex(order)
fig, ax = plt.subplots(figsize=(9.8, 5.0))
x = np.arange(len(p)); w = .38
ax.bar(x - w/2, p["pull"], w, label="Left for an opportunity (pull)", color=PURPLE)
ax.bar(x + w/2, p["push"], w, label="Managed / pushed out (push)", color=TEAL)
for i in range(len(p)):
    for off, col in [(-w/2, "pull"), (w/2, "push")]:
        v = p[col].iloc[i]
        ax.text(i + off, v + 2.2, f"{v:.0f}%", ha="center", fontsize=9.5,
                fontweight="bold", color=DEEP)
        ax.text(i + off, -5.5, f"n={int(n[col].iloc[i])}", ha="center", fontsize=8, color=GREY)
ax.set_xticks(x); ax.set_xticklabels([t.replace(" ", "\n") for t in p.index])
ax.set_ylabel("% of exits flagged 'regrettable' by HR")
ax.set_ylim(-9, 96); ax.legend(loc="upper right", fontsize=10)
ax.set_title("The flag is a synonym for 'Outstanding' — not a measure of value lost")
ax.annotate("Not one of the 168 High Performers\nmanaged out was counted as a loss",
            xy=(1 + w/2 + .02, 1.5), xytext=(1.62, 44), color=CORAL, fontweight="bold",
            fontsize=10.5, ha="left",
            arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.9,
                            connectionstyle="arc3,rad=-0.25"))
ax.axhline(0, color="#DDDDE3", lw=1)
save(fig, "E2_flag_never_fires.png")

# 3 ------------------------------------------- adverse impact of the silence flag
rr = eng.groupby("employee_id").response_flag.mean().rename("rr")
act = emp[emp.status == "active"].merge(rr, on="employee_id", how="left")
act["flag"] = act.rr < .5
g = act.groupby("age_band").flag.mean() * 100
fig, ax = plt.subplots(figsize=(9.5, 4.6))
cols = [CORAL if v >= 9 else (GOLD if v >= 4 else TEAL) for v in g.values]
xpos = np.arange(len(g))
ax.bar(xpos, g.values, color=cols, width=.66)
ax.set_xticks(xpos); ax.set_xticklabels(g.index)
for i, v in enumerate(g.values):
    ax.text(i, v + .45, f"{v:.1f}%", ha="center", fontweight="bold", fontsize=9, color=DEEP)
ax.axhline(g.max() * .8, ls="--", color=GREY, lw=1.4)
ax.text(len(g) - .65, g.max() * .8 + .5, "four-fifths\nthreshold", ha="right", fontsize=9, color=GREY)
ax.set_ylabel("% flagged as a flight risk"); ax.set_xlabel("Age band")
ax.set_title("A 'who stopped answering' flag is an age proxy — 16.6% vs 1.4%")
save(fig, "E3_adverse_impact_age.png")

# 4 --------------------------------------------------- precision of the flag
al = emp.merge(rr, on="employee_id", how="left")
al["left"] = al.status == "departed"; al["flag"] = al.rr < .5
tp = int((al.flag & al.left).sum()); fp = int((al.flag & ~al.left).sum()); fn = int((~al.flag & al.left).sum())
fig, ax = plt.subplots(figsize=(8.6, 4.4))
ax.barh([1], [tp], color=PURPLE, height=.5, label=f"actually left ({tp})")
ax.barh([1], [fp], left=[tp], color="#E4E4EA", height=.5, label=f"never left ({fp})")
ax.barh([0], [fn], color=CORAL, height=.5, label=f"missed ({fn})")
ax.set_yticks([0, 1]); ax.set_yticklabels(["Left but was\nnever flagged", "Flagged as\na flight risk"])
ax.set_xlabel("People"); ax.legend(loc="lower right"); ax.set_xlim(0, (tp + fp) * 1.32)
ax.set_title("Right 23% of the time, catches 19% of leavers — not a list of names")
ax.text(tp + fp + 30, 1, f"{fp/(tp+fp)*100:.0f}% false positives", va="center",
        color=DEEP, fontweight="bold")
save(fig, "E4_flag_precision.png")

# 5 ------------------------------------------------------------- sensitivity
hv = vol[vol.performance_band_at_exit.isin(HIGH)]
mults, fills = [1.0, 1.25, 1.5, 1.75, 2.0], [1.00, .85, .70]
M = np.array([[1.5*0 + mu*f*hv.salary_at_exit.sum()*(1+SUPER)/W/1e6 for mu in mults] for f in fills])
fig, ax = plt.subplots(figsize=(8.6, 3.9))
im = ax.imshow(M, cmap="Purples", aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax.text(j, i, f"${M[i,j]:.0f}M", ha="center", va="center", fontsize=11,
                color="white" if M[i, j] > M.max()*.62 else DEEP, fontweight="bold")
ax.set_xticks(range(len(mults))); ax.set_xticklabels([f"{x}x" for x in mults])
ax.set_yticks(range(len(fills))); ax.set_yticklabels([f"{int(f*100)}%" for f in fills])
ax.set_xlabel("Replacement cost multiplier"); ax.set_ylabel("Backfill rate")
ax.grid(False); ax.set_title("Our number under every assumption we don't control")
ax.add_patch(plt.Rectangle((1.5, .5), 1, 1, fill=False, edgecolor=CORAL, lw=3))
ax.text(2.62, 1.02, "brief's\nconstants", color=CORAL, fontweight="bold", fontsize=9, va="center")
save(fig, "E5_sensitivity.png")

# 6 -------------------------------------------------- the three buckets restated
fig, ax = plt.subplots(figsize=(9.6, 4.4))
labels = ["Regrettable\nattrition", "Disengagement\nproductivity", "Hiring\ninefficiency"]
brief_lo, brief_hi = np.array([22, 12, 4]), np.array([25, 15, 6])
ours = np.array([45.1, 17.8, 2.3])
x = np.arange(3); w = .34
ax.bar(x - w/2, brief_hi - brief_lo, w, bottom=brief_lo, color="#C9C9D2", label="Finance's estimate")
ax.bar(x + w/2, ours, w, color=PURPLE, label="Restated on the data")
for i, v in enumerate(ours):
    ax.text(i + w/2, v + 1, f"${v:.1f}M", ha="center", fontweight="bold", color=DEEP)
for i, (lo, hi) in enumerate(zip(brief_lo, brief_hi)):
    ax.text(i - w/2, hi + 1, f"${lo}-{hi}M", ha="center", fontsize=9, color=GREY)
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylabel("$M per year")
ax.set_ylim(0, 54); ax.legend(loc="upper right")
ax.set_title("The $42M is mis-apportioned: the big bucket is bigger, the small one smaller")
save(fig, "E6_buckets_restated.png")
print("\nDone -> figures_ethics/")
