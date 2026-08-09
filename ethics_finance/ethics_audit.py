"""
Ethics & Responsible Practice audit — NovaCorp People Analytics Challenge.

Answers three questions a judge will ask:
  1. Is HR's `regrettable_flag` applied consistently, or does it encode a bias?
  2. Does that bias fall along protected characteristics (adverse impact)?
  3. If NovaCorp deploys a survey-silence flight-risk flag, WHO gets flagged?

Run:  python ethics_audit.py
"""
import pandas as pd, numpy as np

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 40)

emp = pd.read_csv("../employees.csv", parse_dates=["hire_date", "exit_date"])
att = pd.read_csv("../attrition_log.csv", parse_dates=["exit_date"])
eng = pd.read_csv("../engagement.csv", parse_dates=["survey_date"])

HIGH = ["Outstanding", "High Performer"]
PROTECTED = ["gender", "cultural_background", "age_band", "contract_type"]
a = att.merge(emp, on="employee_id", suffixes=("", "_e"))


def hr(series_flagged, series_ref):
    """Impact ratio (selection rate of group / selection rate of most-favoured group)."""
    return series_flagged / series_ref if series_ref else np.nan


def four_fifths(tbl, col="rate"):
    """EEOC four-fifths rule: flag groups whose rate < 80% of the highest-rate group."""
    top = tbl[col].max()
    tbl = tbl.copy()
    tbl["impact_ratio"] = (tbl[col] / top).round(2)
    tbl["fails_4/5"] = np.where(tbl["impact_ratio"] < 0.80, "<-- FAIL", "")
    return tbl


print("#" * 78)
print("# 1. IS THE `regrettable_flag` APPLIED CONSISTENTLY?")
print("#" * 78)
tbl = a.pivot_table(index="performance_band_at_exit", columns="pathway",
                    values="regrettable_flag", aggfunc=["mean", "size"])
tbl.columns = [f"{s}_{p}" for s, p in tbl.columns]
for c in ["mean_pull", "mean_push"]:
    tbl[c] = (tbl[c] * 100).round(1)
print(tbl.rename(columns={"mean_pull": "regrettable%_pull", "mean_push": "regrettable%_push",
                          "size_pull": "n_pull", "size_push": "n_push"}))

hp = a[a.performance_band_at_exit == "High Performer"]
out = a[a.performance_band_at_exit == "Outstanding"]
print(f"\n  'Outstanding' leavers flagged regrettable : {out.regrettable_flag.mean()*100:5.1f}%  (n={len(out)})")
print(f"  'High Performer' leavers flagged         : {hp.regrettable_flag.mean()*100:5.1f}%  (n={len(hp)})")
print(f"     ...of which PUSH pathway              : {hp[hp.pathway=='push'].regrettable_flag.mean()*100:5.1f}%"
      f"  (n={len(hp[hp.pathway=='push'])})")
vol_hp = a[(a.exit_type == "voluntary") & a.performance_band_at_exit.isin(HIGH)]
missed = int((~vol_hp.regrettable_flag).sum())
print(f"\n  => {missed} high-performing VOLUNTARY leavers were not counted as a regrettable loss.")
print("     The flag is effectively a synonym for 'Outstanding', not a measure of value lost.")

print("\n" + "#" * 78)
print("# 2. ADVERSE IMPACT — does the flag fall unevenly on protected groups?")
print("#" * 78)
print("Population: voluntary leavers rated High Performer or Outstanding (like-for-like value).")
print("If the flag were neutral, every group should be flagged at a similar rate.\n")
for col in PROTECTED:
    g = vol_hp.groupby(col).agg(n=("regrettable_flag", "size"),
                                rate=("regrettable_flag", "mean"))
    g = g[g.n >= 20]
    if g.empty:
        continue
    g["rate"] = (g["rate"] * 100).round(1)
    print(f"--- {col} (groups with n>=20) ---")
    print(four_fifths(g))
    print()

print("Stratified check — flag rate within performance band x gender (controls for merit):")
strat = vol_hp.pivot_table(index="performance_band_at_exit", columns="gender",
                           values="regrettable_flag", aggfunc=["mean", "size"])
print((strat * 1).round(3))

print("\n" + "#" * 78)
print("# 3. IF WE DEPLOY A SURVEY-SILENCE RISK FLAG, WHO GETS FLAGGED?")
print("#" * 78)
rr = eng.groupby("employee_id").response_flag.mean().rename("resp_rate")
act = emp[emp.status == "active"].merge(rr, on="employee_id", how="left")
act["flagged"] = act.resp_rate < 0.50          # the proposed "going quiet" rule
print(f"Rule: flag any active employee answering <50% of survey waves.")
print(f"Flagged: {int(act.flagged.sum())} of {len(act)} active staff "
      f"({act.flagged.mean()*100:.1f}%)\n")
for col in PROTECTED + ["role_level", "legacy_entity_code"]:
    g = act.groupby(col).agg(n=("flagged", "size"), rate=("flagged", "mean"))
    g = g[g.n >= 50]
    if g.empty:
        continue
    g["rate"] = (g["rate"] * 100).round(1)
    print(f"--- flag rate by {col} ---")
    print(four_fifths(g))
    print()

print("=" * 78)
print("PRECISION OF THE FLAG (does it actually work, and what is the false-positive cost?)")
print("=" * 78)
all_emp = emp.merge(rr, on="employee_id", how="left")
all_emp["left"] = (all_emp.status == "departed").astype(int)
all_emp["flagged"] = all_emp.resp_rate < 0.50
tp = int(((all_emp.flagged == 1) & (all_emp.left == 1)).sum())
fp = int(((all_emp.flagged == 1) & (all_emp.left == 0)).sum())
fn = int(((all_emp.flagged == 0) & (all_emp.left == 1)).sum())
print(f"  flagged & left    (true positive) : {tp}")
print(f"  flagged & stayed  (false positive): {fp}")
print(f"  not flagged & left (missed)       : {fn}")
print(f"  precision {tp/(tp+fp)*100:.1f}%   recall {tp/(tp+fn)*100:.1f}%")
print(f"\n  => {fp} people would be labelled a flight risk who never leave.")
print(f"     At {fp/(tp+fp)*100:.0f}% false-positive rate, this cannot be a list of names")
print("     handed to managers. It is a team-level diagnostic, not an individual score.")
