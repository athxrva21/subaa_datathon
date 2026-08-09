"""Stress-test the Part-1 findings against the raw data."""
import pandas as pd, numpy as np
pd.set_option("display.width", 200)

emp = pd.read_csv("../employees.csv", parse_dates=["hire_date", "exit_date"])
att = pd.read_csv("../attrition_log.csv", parse_dates=["exit_date"])
eng = pd.read_csv("../engagement.csv", parse_dates=["survey_date"])
perf = pd.read_csv("../performance.csv", parse_dates=["review_date"])

print("=" * 70)
print("A. PATHWAY vs EXIT_TYPE  — is 'push' really disengagement?")
print("=" * 70)
print(pd.crosstab(att.pathway, att.exit_type, margins=True))
print("\nrow % within pathway:")
print(pd.crosstab(att.pathway, att.exit_type, normalize="index").round(3) * 100)
print("\npathway share:", att.pathway.value_counts(normalize=True).round(3).to_dict())
print("\nregrettable by pathway:")
print(att.groupby("pathway").regrettable_flag.mean().round(3))
print("\nstated reason x pathway:")
print(pd.crosstab(att.stated_exit_reason, att.pathway))

print("\n" + "=" * 70)
print("B. EXIT VOLUME — does the data reconcile with the Annual Report?")
print("=" * 70)
att["yr"] = att.exit_date.dt.year
print("exits by calendar year:\n", att.yr.value_counts().sort_index())
print("\nexits by FY (Jul-Jun):")
fy = att.exit_date.dt.to_period("Q-JUN").dt.qyear
print(fy.value_counts().sort_index())
vol = att[att.exit_type == "voluntary"]
print(f"\ntotal exits {len(att)},  voluntary {len(vol)},  involuntary {len(att)-len(vol)}")
active = (emp.status == "active").sum()
print(f"active employees in file: {active}  (AR claims 12,003)")
print(f"AR claims 10.4% voluntary attrition => ~{0.104*12003:.0f} voluntary exits/yr")
print(f"data shows ~{len(vol)/2:.0f} voluntary exits/yr  => {len(vol)/2/active*100:.1f}%")

print("\n" + "=" * 70)
print("C. THE BIG ONE — is non-response CONFOUNDED by having already left?")
print("=" * 70)
e = eng.merge(emp[["employee_id", "exit_date", "status"]], on="employee_id", how="left")
e["after_exit"] = e.exit_date.notna() & (e.survey_date > e.exit_date)
print("survey rows dated AFTER the employee's exit_date:", int(e.after_exit.sum()))
print("  of those, response_flag=False:", int((e.after_exit & ~e.response_flag).sum()))
print("\nresponse rate by wave, leavers vs stayers:")
e["grp"] = np.where(e.exit_date.notna(), "leaver", "stayer")
print(e.pivot_table(index="wave_number", columns="grp", values="response_flag", aggfunc="mean").round(3))

# rebuild the response-band -> attrition finding, but ONLY on pre-exit waves
pre = e[~e.after_exit]
rr_all = e.groupby("employee_id").response_flag.mean()
rr_pre = pre.groupby("employee_id").response_flag.mean()
d = emp[["employee_id", "status"]].copy()
d["left"] = (d.status == "departed").astype(int)
for name, rr in [("ALL waves (what findings.md did)", rr_all), ("PRE-EXIT waves only", rr_pre)]:
    t = d.merge(rr.rename("rr"), on="employee_id")
    t["band"] = pd.cut(t.rr, [-.01, .25, .5, .75, 1.01], labels=["0-25%", "25-50%", "50-75%", "75-100%"])
    g = t.groupby("band", observed=True).agg(n=("left", "size"), attrition=("left", "mean"))
    g["attrition"] = (g.attrition * 100).round(1)
    lo, hi = g.attrition.iloc[0], g.attrition.iloc[-1]
    print(f"\n--- {name} ---")
    print(g)
    print(f"    spread lowest-vs-highest band: {lo/hi:.1f}x")

print("\n" + "=" * 70)
print("D. Does silence lead the exit? (response in the LAST wave before leaving)")
print("=" * 70)
lv = pre[pre.grp == "leaver"].sort_values(["employee_id", "wave_number"])
last = lv.groupby("employee_id").tail(1)
first = lv.groupby("employee_id").head(1)
print(f"leavers with >=1 pre-exit wave: {lv.employee_id.nunique()}")
print(f"  responded on their FIRST pre-exit wave : {first.response_flag.mean()*100:.1f}%")
print(f"  responded on their LAST  pre-exit wave : {last.response_flag.mean()*100:.1f}%")
st = pre[pre.grp == "stayer"]
print(f"stayers overall pre-exit response rate  : {st.response_flag.mean()*100:.1f}%")
print(f"AR claims survey response rate 81.7%; data overall: {eng.response_flag.mean()*100:.1f}%")
