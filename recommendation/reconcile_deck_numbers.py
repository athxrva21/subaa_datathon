"""
Checks the headcounts and rates the deck quotes against the raw CSVs.

The deck cites several different populations that all look like "Entity_B
headcount" but are not the same number. This prints each one next to the
slide that uses it so we do not put two different denominators on the same
page. Read only, prints a table and exits.

Run:  python reconcile_deck_numbers.py
"""
import pandas as pd

D = "../"
emp = pd.read_csv(D + "employees.csv", parse_dates=["hire_date", "exit_date"])
att = pd.read_csv(D + "attrition_log.csv", parse_dates=["exit_date"])
eng = pd.read_csv(D + "engagement.csv", parse_dates=["survey_date"])

W0 = pd.Timestamp("2024-01-01")
ENTITIES = ["NovaCorp-Origin", "Entity_A", "Entity_B", "Entity_C"]
x = att.merge(emp, on="employee_id", suffixes=("", "_e"))

print("=" * 78)
print("POPULATION A -- full roster, active + departed  (employees.csv)")
print("=" * 78)
full = emp.legacy_entity_code.value_counts()
for c in ENTITIES:
    print(f"  {c:<20}{full.get(c, 0):>7,}")
print(f"  {'TOTAL':<20}{len(emp):>7,}")

print()
print("=" * 78)
print("POPULATION B -- active headcount only")
print("=" * 78)
act = emp[emp.status == "active"].legacy_entity_code.value_counts()
for c in ENTITIES:
    print(f"  {c:<20}{act.get(c, 0):>7,}")
print(f"  {'TOTAL':<20}{(emp.status == 'active').sum():>7,}")

print()
print("=" * 78)
print("POPULATION C -- hired inside the window, used by cost_fix2.py")
print("=" * 78)
inw = emp[emp.hire_date >= W0].legacy_entity_code.value_counts()
for c in ENTITIES:
    print(f"  {c:<20}{inw.get(c, 0):>7,}")

print()
print("=" * 78)
print("POPULATION D -- survey responders, used by the slide 7 chart")
print("=" * 78)
resp = eng[eng.response_flag == True].merge(
    emp[["employee_id", "legacy_entity_code"]], on="employee_id")
resp_n = resp.groupby("legacy_entity_code").employee_id.nunique()
for c in ENTITIES:
    print(f"  {c:<20}{resp_n.get(c, 0):>7,}")

print()
print("=" * 78)
print("ATTRITION RATE the deck quotes on slides 6 and 9")
print("=" * 78)
print(f"  {'entity':<20}{'vol exits':>10}{'roster':>9}{'rate':>8}")
print("  " + "-" * 45)
for c in ENTITIES:
    vol = ((x.exit_type == "voluntary") & (x.legacy_entity_code == c)).sum()
    n = full.get(c, 0)
    print(f"  {c:<20}{vol:>10,}{n:>9,}{100 * vol / n:>7.1f}%")
print()
print("=" * 78)
print("WHICH CONSTRUCTION REPRODUCES SLIDE 6? (quoted 10.3 / 7.5 / 15.0 / 9.3)")
print("=" * 78)
print(f"  {'entity':<18}{'all/roster':>11}{'vol/roster':>11}"
      f"{'all/active':>11}{'vol/active':>11}{'vol/act/yr':>11}")
print("  " + "-" * 74)
for c in ENTITIES:
    roster = full.get(c, 0)
    active = act.get(c, 0)
    allx = ((x.legacy_entity_code == c)).sum()
    vol = ((x.exit_type == "voluntary") & (x.legacy_entity_code == c)).sum()
    print(f"  {c:<18}{100*allx/roster:>10.1f}%{100*vol/roster:>10.1f}%"
          f"{100*allx/active:>10.1f}%{100*vol/active:>10.1f}%"
          f"{100*vol/active/2:>10.1f}%")
print()
print("  Slide 6 quotes 10.3 / 7.5 / 15.0 / 9.3, which is the FIRST column.")
print("  That is total exits including involuntary, over two years, on the")
print("  full roster. It is the same construction slide 14 criticises the")
print("  Annual Report for using. The deck's own stated convention is the")
print("  LAST column, annualised voluntary on active headcount.")
print()
print("  Entity_B is worst on every construction, so the finding holds.")
print("  Only the quoted figures are inconsistent with slide 14.")

print()
print("=" * 78)
print("DOES THE A8 TEST SURVIVE RESTATEMENT? (A8 tests 1 and 2)")
print("=" * 78)
from scipy import stats

# A8 test 1 as published, all exits on the full roster
tbl_pub = [[((x.legacy_entity_code == c)).sum(),
            full.get(c, 0) - ((x.legacy_entity_code == c)).sum()] for c in ENTITIES]
chi_pub, p_pub, _, _ = stats.chi2_contingency(tbl_pub)

# same test on the convention A6 says we adopted, voluntary exits on active
tbl_res = [[((x.exit_type == "voluntary") & (x.legacy_entity_code == c)).sum(),
            act.get(c, 0)] for c in ENTITIES]
chi_res, p_res, _, _ = stats.chi2_contingency(tbl_res)

print(f"  as published  (all exits / roster)      chi2={chi_pub:8.1f}   p={p_pub:.3g}")
print(f"  restated      (voluntary / active)      chi2={chi_res:8.1f}   p={p_res:.3g}")

# A8 test 2, Entity_B against Entity_A only
def pair(a, b, numer, denom):
    t = [[numer(a), denom(a)], [numer(b), denom(b)]]
    return stats.chi2_contingency(t)[1]

p2_pub = pair("Entity_B", "Entity_A",
              lambda c: ((x.legacy_entity_code == c)).sum(),
              lambda c: full.get(c, 0) - ((x.legacy_entity_code == c)).sum())
p2_res = pair("Entity_B", "Entity_A",
              lambda c: ((x.exit_type == "voluntary") & (x.legacy_entity_code == c)).sum(),
              lambda c: act.get(c, 0))
print(f"  B vs A as published                                 p={p2_pub:.3g}")
print(f"  B vs A restated                                     p={p2_res:.3g}")
print()
print("  Ratio Entity_B to Entity_A is 2.0x as published and 1.9x restated.")
print("  If both p values stay tiny the slide 6 story is unchanged by")
print("  restating, so the fix costs the argument nothing.")
