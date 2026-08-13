"""Re-derive the early-tenure lever with a left-truncated survival model."""
import pandas as pd, numpy as np
D="../"
emp=pd.read_csv(D+"employees.csv",parse_dates=["hire_date","exit_date"])
att=pd.read_csv(D+"attrition_log.csv",parse_dates=["exit_date"])
W0,W1=pd.Timestamp("2024-01-01"),pd.Timestamp("2025-12-31")
SUP,MULT,BACK,YRS=1.12,1.50,0.85,2.0

def mo(a,b): return (b.dt.year-a.dt.year)*12+(b.dt.month-a.dt.month)

e=emp.copy()
e["obs_start"]=e.hire_date.clip(lower=W0)
e["obs_end"]=e.exit_date.fillna(W1)
e["entry_t"]=mo(e.hire_date,e.obs_start).clip(lower=0)     # tenure when observation begins
e["exit_t"]=mo(e.hire_date,e.obs_end).clip(lower=0)
e["event"]=(e.status=="departed").astype(int)
e=e[e.exit_t>=e.entry_t]

print("="*78);print("THE BIAS, STATED PLAINLY");print("="*78)
print("Naive 'early exit' counts everyone with tenure_months<=12 as an early exit.")
print("But whether we can OBSERVE someone's first 12 months depends entirely on")
print("when their record entered the system:\n")
obs=e.assign(observed_from_0=e.entry_t==0).groupby("legacy_entity_code").agg(
    n=("event","size"), pct_observed_from_hire=("observed_from_0","mean"))
obs["pct_observed_from_hire"]=(obs.pct_observed_from_hire*100).round(1)
print(obs.to_string())
print("\n-> Acquired cohorts are 100% observed from tenure 0. NovaCorp-Origin is barely")
print("   observed there at all. Comparing raw counts compares availability, not risk.\n")

def km(df,horizon=12):
    """Left-truncated Kaplan-Meier. Risk set at t = entry_t < t <= exit_t."""
    ev=np.sort(df.loc[df.event==1,"exit_t"].unique())
    S=1.0; out=[]
    for t in ev:
        if t>horizon: break
        at_risk=((df.entry_t<t)&(df.exit_t>=t)).sum()
        d=((df.exit_t==t)&(df.event==1)).sum()
        if at_risk>0:
            S*=(1-d/at_risk); out.append((t,at_risk,d,S))
    return S,out

print("="*78);print("LEFT-TRUNCATED KM: probability of leaving within 12 months of joining");print("="*78)
print(f"{'group':<20}{'n obs from t=0':>16}{'exits<=12mo':>13}{'P(exit<=12mo)':>15}")
print("-"*64)
rows={}
for col,groups in [("hire_source",None),("legacy_entity_code",None)]:
    print(f"\n  by {col}:")
    for gname,sub in e.groupby(col):
        s,_=km(sub,12)
        n0=(sub.entry_t==0).sum(); ex=((sub.exit_t<=12)&(sub.event==1)).sum()
        rows[gname]=1-s
        print(f"  {gname:<18}{n0:>16}{ex:>13}{(1-s)*100:>14.1f}%")

print("\n"+"="*78);print("APPLES-TO-APPLES: restrict to people hired INSIDE the window");print("="*78)
print("(everyone here is observed from tenure 0, so no truncation problem at all)\n")
inw=e[e.hire_date>=W0].copy()
print(f"{'hire_source':<16}{'n':>7}{'exits<=12mo':>13}{'rate':>9}")
print("-"*45)
for gname,sub in inw.groupby("hire_source"):
    ex=((sub.exit_t<=12)&(sub.event==1)).sum()
    print(f"{gname:<16}{len(sub):>7}{ex:>13}{100*ex/len(sub):>8.1f}%")
print(f"\n{'entity':<18}{'n':>7}{'exits<=12mo':>13}{'rate':>9}{'max obs':>9}")
print("-"*56)
for gname,sub in inw.groupby("legacy_entity_code"):
    ex=((sub.exit_t<=12)&(sub.event==1)).sum()
    print(f"{gname:<18}{len(sub):>7}{ex:>13}{100*ex/len(sub):>8.1f}%{sub.exit_t.max():>9.0f}")

print("\n"+"="*78);print("COMMON-HORIZON TEST: 9 months (the most Entity_C can ever show)");print("="*78)
for gname,sub in inw.groupby("legacy_entity_code"):
    ex=((sub.exit_t<=9)&(sub.event==1)).sum()
    print(f"  {gname:<18} {100*ex/len(sub):>6.1f}%   ({ex}/{len(sub)})")
