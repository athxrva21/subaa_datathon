import pandas as pd, numpy as np
from math import sqrt
D="../"
emp=pd.read_csv(D+"employees.csv",parse_dates=["hire_date","exit_date"])
att=pd.read_csv(D+"attrition_log.csv",parse_dates=["exit_date"])
W0=pd.Timestamp("2024-01-01"); SUP,MULT,BACK,YRS=1.12,1.50,0.85,2.0
x=att.merge(emp,on="employee_id",suffixes=("","_e"))
base=emp[emp.hire_date>=W0]                      # everyone observed from tenure 0
vol=x[(x.exit_type=="voluntary")&(x.hire_date>=W0)&(x.tenure_months<=12)]

print("VOLUNTARY early exit (<=12mo), in-window hires only, by cohort:")
print(f"{'cohort':<18}{'n':>7}{'exits':>7}{'rate':>8}")
print("-"*40)
r={}
for c in ["NovaCorp-Origin","Entity_A","Entity_B","Entity_C"]:
    n=(base.legacy_entity_code==c).sum(); k=(vol.legacy_entity_code==c).sum()
    if n: r[c]=(k,n); print(f"{c:<18}{n:>7}{k:>7}{100*k/n:>7.1f}%")

def z2(a,na,b,nb):
    p=(a+b)/(na+nb); se=sqrt(p*(1-p)*(1/na+1/nb)); return (a/na-b/nb)/se
ka,na=r["Entity_B"]; kb,nb=r["NovaCorp-Origin"]
print(f"\nEntity_B vs NovaCorp-Origin new joiners: z=%.2f  (p<0.01 if |z|>2.58)"%z2(ka,na,kb,nb))
kc,nc=r["Entity_C"]
print(f"Entity_C vs NovaCorp-Origin new joiners: z=%.2f"%z2(kc,nc,kb,nb))

print("\n--- ADDRESSABLE, using NovaCorp-Origin new joiners as the baseline ---")
BASE=kb/nb
tot_excess=0; tot_cost=0
for c in ["Entity_B","Entity_C"]:
    k,n=r[c]; rate=k/n; ex=max(rate-BASE,0)*n
    sal=vol[vol.legacy_entity_code==c].salary_at_exit.mean()
    cst=MULT*BACK*ex*sal*SUP/YRS/1e6
    tot_excess+=ex; tot_cost+=cst
    print(f"  {c:<12} rate {100*rate:.1f}% vs baseline {100*BASE:.1f}%  -> {ex:.0f} excess exits  ${cst:.1f}M/yr")
print(f"\n  TOTAL addressable early-tenure cost: ${tot_cost:.1f}M/yr  ({tot_excess:.0f} excess exits)")
print(f"    @20% reduction ${tot_cost*0.2:.1f}M/yr   @40% ${tot_cost*0.4:.1f}M/yr")
print(f"\n  vs Moksh's Slide E figure of $29.6M addressable / $5.9M @20% / $11.8M @40%")
