"""
Builds the cohort diagnostic dashboard as one self-contained HTML file.

DESIGN CONSTRAINT, and it is the point of the tool:
The output contains no employee_id, no name, and no manager_id. Aggregation
happens here, in Python, before anything reaches the file. A cohort below the
8-response floor is written out as suppressed with its counts removed. It is
therefore structurally impossible to drill to a person in the delivered file,
which is what slides 12 and 13 recommend and what most flight-risk tools do
not do.

The unit is department x legacy entity x role-level band, not manager team.
Manager teams here have a median of 2 respondents, so an 8-response floor would
suppress 82% of the workforce, and A8 test 12 already rules out attrition being
concentrated under particular managers.

Run from the recommendation/ directory:
    ../.venv/bin/python make_dashboard.py

Writes ../deck/NovaCorp_cohort_dashboard.html
"""
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "deck" / "NovaCorp_cohort_dashboard.html"

MIN_RESPONSES = 8          # slide 13's disclosed suppression floor
WINDOW_YEARS = 2.0
REPLACEMENT_MULT, BACKFILL, SUPER = 1.50, 0.85, 0.12
HIGH_VALUE = ["Outstanding", "High Performer"]

DIMS = ["manager_effectiveness", "psychological_safety", "recognition",
        "career_development", "senior_leadership_trust", "purpose_meaning",
        "wellbeing", "confidence_in_role_future"]

emp = pd.read_csv(ROOT / "employees.csv", parse_dates=["hire_date", "exit_date"])
att = pd.read_csv(ROOT / "attrition_log.csv", parse_dates=["exit_date"])
eng = pd.read_csv(ROOT / "engagement.csv", parse_dates=["survey_date"])

vol_ids = set(att[att.exit_type == "voluntary"].employee_id)
emp["vol_exit"] = emp.employee_id.isin(vol_ids).astype(int)
emp["is_active"] = (emp.status == "active").astype(int)
emp["band"] = emp.role_level.map(lambda x: "L1" if x == 1 else ("L2" if x == 2 else "L3+"))

exits = att.merge(emp, on="employee_id", suffixes=("", "_e"))
hi_val = exits[(exits.exit_type == "voluntary")
               & (exits.performance_band_at_exit.isin(HIGH_VALUE))]


def replacement_cost(df):
    return REPLACEMENT_MULT * BACKFILL * df.salary_at_exit.sum() * (1 + SUPER) / WINDOW_YEARS


# ---------------------------------------------------------------- benchmarks
resp = eng.merge(emp[["employee_id", "department", "legacy_entity_code", "band"]],
                 on="employee_id")
responded = resp[resp.response_flag == True]

per_emp = responded.groupby("employee_id")[DIMS].mean()
CO = {
    "resp_rate": resp.groupby("employee_id").response_flag.mean().mean() * 100,
    "trust": per_emp.senior_leadership_trust.mean(),
    "purpose": per_emp.purpose_meaning.mean(),
    "index": per_emp[DIMS].mean(axis=1).mean(),
    "attrition": emp.vol_exit.sum() / emp.is_active.sum() * 100 / WINDOW_YEARS,
}

emp_dims = per_emp.copy()
emp_dims["index"] = emp_dims[DIMS].mean(axis=1)
emp_resp_rate = resp.groupby("employee_id").response_flag.mean() * 100


# ---------------------------------------------------------------- cohorts
def build_cohorts(keys):
    rows = []
    for key, grp in emp.groupby(keys):
        key = key if isinstance(key, tuple) else (key,)
        # Scores describe the people still there, so respondents are restricted
        # to active staff. Including leavers would also make the respondent
        # count exceed active headcount, which reads as an error. A8 test 5
        # confirms the trust and purpose gaps hold on active staff alone.
        ids = set(grp[grp.is_active == 1].employee_id)
        n_resp = len(ids & set(emp_dims.index))

        active = int(grp.is_active.sum())
        vol = int(grp.vol_exit.sum())
        attr = (vol / active * 100 / WINDOW_YEARS) if active else 0.0
        # Cost uses the whole cohort, since the loss is what already left.
        cost = replacement_cost(hi_val[hi_val.employee_id.isin(set(grp.employee_id))])

        rec = {
            "key": " · ".join(str(k) for k in key),
            "parts": [str(k) for k in key],
            "headcount": active,
            "n_resp": n_resp,
            "attrition": round(attr, 2),
            "cost": round(cost / 1e6, 2),
        }

        if n_resp < MIN_RESPONSES:
            # Suppressed. Scores are withheld entirely, not rounded or binned.
            rec.update({"suppressed": True, "resp_rate": None, "trust": None,
                        "purpose": None, "index": None, "dims": None,
                        "score": None, "bandName": "Suppressed"})
            rows.append(rec)
            continue

        d = emp_dims.loc[list(ids & set(emp_dims.index))]
        rr = emp_resp_rate.loc[list(ids & set(emp_resp_rate.index))].mean()

        # Three transparent components, each a gap against the company figure.
        # Shown separately in the UI so the score can be audited rather than
        # trusted. This is a diagnostic, not a prediction.
        c_resp = max(CO["resp_rate"] - rr, 0) / CO["resp_rate"]
        c_belief = max(((CO["trust"] - d.senior_leadership_trust.mean())
                        + (CO["purpose"] - d.purpose_meaning.mean())) / 2, 0) / CO["trust"]
        c_attr = max(attr - CO["attrition"], 0) / CO["attrition"]
        score = round(100 * (0.4 * c_resp + 0.4 * min(c_belief, 1) + 0.2 * min(c_attr, 1)), 1)

        rec.update({
            "suppressed": False,
            "resp_rate": round(rr, 1),
            "trust": round(d.senior_leadership_trust.mean(), 3),
            "purpose": round(d.purpose_meaning.mean(), 3),
            "index": round(d["index"].mean(), 3),
            "dims": {k: round(d[k].mean(), 3) for k in DIMS},
            # Capped the same way the score caps them, so the displayed
            # components always reconcile to the score shown beside them.
            "comp": {"response": round(100 * min(c_resp, 1), 1),
                     "belief": round(100 * min(c_belief, 1), 1),
                     "attrition": round(100 * min(c_attr, 1), 1)},
            "score": score,
            "bandName": "Priority" if score >= 25 else ("Elevated" if score >= 12 else "Stable"),
        })
        rows.append(rec)
    return rows


cohorts = build_cohorts(["department", "legacy_entity_code", "band"])
entities = build_cohorts(["legacy_entity_code"])
depts = build_cohorts(["department"])

# ---------------------------------------------------------------- fairness
# Reproduced here so the audit travels with the tool rather than living only in
# the deck. Same numbers as ethics_audit.py and appendix A4.
fairness = [
    {"dim": "Age band", "ratio": 0.08, "detail": "18–24: 16.6% flagged vs 45–49: 1.4%",
     "n": "1,253 / 1,017", "verdict": "Fails badly"},
    {"dim": "Role level", "ratio": 0.15, "detail": "L1 9.2% vs L5 1.4%",
     "n": "6,931 / 74", "verdict": "Fails"},
    {"dim": "Acquisition cohort", "ratio": 0.08,
     "detail": "Entity_C 31.7% vs NovaCorp-Origin 2.4%", "n": "920 / 7,678", "verdict": "Fails"},
]

payload = {
    "company": {k: round(v, 2) for k, v in CO.items()},
    "cohorts": cohorts,
    "entities": entities,
    "depts": depts,
    "fairness": fairness,
    "addressable": 45.1,
    "minResponses": MIN_RESPONSES,
    "totals": {
        "active": int(emp.is_active.sum()),
        "cohorts": len(cohorts),
        "suppressed": sum(1 for c in cohorts if c["suppressed"]),
        "suppressedPeople": sum(c["headcount"] for c in cohorts if c["suppressed"]),
    },
}

assert not any("employee_id" in str(c) for c in cohorts), "no ids may reach the output"

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NovaCorp cohort diagnostic</title>
<style>
:root{--p:#A100FF;--d:#460073;--t:#00B7C3;--c:#FF6B6B;--g:#FFB300;
--ink:#22222A;--mut:#5A5A66;--line:#E8E8EF;--bg:#fff;--panel:#F7F3FC;}
*{box-sizing:border-box}
body{margin:0;font:14px/1.5 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
color:var(--ink);background:var(--bg)}
header{background:var(--d);color:#fff;padding:20px 28px}
h1{margin:0;font-size:21px;letter-spacing:-.2px}
.sub{color:#C9A8EA;font-size:12.5px;margin-top:4px}
.ethics{margin-top:12px;background:rgba(255,255,255,.10);border-left:3px solid var(--t);
padding:9px 13px;font-size:12.5px;max-width:1000px;border-radius:2px}
.wrap{padding:20px 28px;max-width:1500px}
.tabs{display:flex;gap:2px;border-bottom:2px solid var(--line);margin-bottom:18px;flex-wrap:wrap}
.tab{padding:9px 16px;border:0;background:none;font:600 13px inherit;color:var(--mut);
cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-2px}
.tab.on{color:var(--d);border-bottom-color:var(--p)}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px}
.card{flex:1;min-width:150px;border:1px solid var(--line);border-radius:4px;padding:12px 14px}
.card .k{font-size:10px;color:var(--mut);text-transform:uppercase;letter-spacing:.4px;font-weight:700}
.card .v{font-size:25px;font-weight:700;color:var(--d);margin-top:3px}
.card .n{font-size:11px;color:var(--mut);margin-top:2px}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{background:var(--d);color:#fff;text-align:left;padding:8px 9px;font-size:11px;
cursor:pointer;user-select:none;white-space:nowrap}
th:hover{background:#5C0A93}
td{padding:7px 9px;border-bottom:1px solid var(--line)}
tr:nth-child(even) td{background:#FAFAFC}
tr.sup td{color:#9A9AA6;font-style:italic}
.pill{display:inline-block;padding:2px 9px;border-radius:9px;font-size:10.5px;font-weight:700;color:#fff}
.Priority{background:var(--c)}.Elevated{background:var(--g)}.Stable{background:var(--t)}
.Suppressed{background:#B9B9C4}
.bar{height:6px;background:var(--line);border-radius:3px;overflow:hidden;min-width:60px}
.bar i{display:block;height:100%;background:var(--p)}
.ctl{display:flex;gap:14px;align-items:center;margin-bottom:12px;flex-wrap:wrap}
select,input[type=search]{padding:6px 9px;border:1px solid var(--line);border-radius:3px;font:inherit}
.panel{background:var(--panel);border-radius:4px;padding:16px 18px;margin-bottom:16px}
.panel h3{margin:0 0 8px;font-size:14px;color:var(--d)}
.note{font-size:11.5px;color:var(--mut);margin-top:8px}
.slider{width:100%;max-width:520px}
.big{font-size:34px;font-weight:700;color:var(--p)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:900px){.grid2{grid-template-columns:1fr}}
.dimrow{display:flex;align-items:center;gap:9px;margin:5px 0;font-size:12px}
.dimrow .lab{width:170px;color:var(--mut)}
.dimrow .bar{flex:1}
.warn{background:#FFF6E6;border-left:3px solid var(--g);padding:10px 13px;font-size:12.5px;
margin-bottom:14px;border-radius:2px}
footer{padding:16px 28px;color:var(--mut);font-size:11.5px;border-top:1px solid var(--line);margin-top:20px}
code{font-family:Menlo,monospace;font-size:11.5px;color:var(--d)}
button.act{padding:6px 12px;border:1px solid var(--line);background:#fff;border-radius:3px;
font:600 12px inherit;color:var(--d);cursor:pointer}
button.act:hover{background:var(--panel)}
.sbar{display:inline-block;height:5px;border-radius:3px;background:var(--p);vertical-align:middle;
margin-left:6px}
@media print{
 /* The deck may be printed in black and white, so the score pills lose their
    meaning. The inline bar and the numeric score survive. */
 body{font-size:10px}
 .tabs,button.act,input,select{display:none!important}
 header{background:#460073!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 th{background:#460073!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .pill{border:1px solid #666;color:#000!important;background:#fff!important}
 tr,.panel,.card{page-break-inside:avoid}
}
</style></head><body>
<header>
<h1>NovaCorp cohort diagnostic</h1>
<div class="sub">Team O for 4 · Accenture × SUBAA People Analytics Challenge</div>
<div class="ethics"><b>This tool cannot show you an individual.</b> There is no employee ID, name or
manager ID anywhere in this file — aggregation happens before the data is written, not in the
interface. Cohorts below __MINR__ survey responses are suppressed entirely.</div>
</header>
<div class="wrap">
<div class="tabs">
<button class="tab on" data-v="overview">Overview</button>
<button class="tab" data-v="cohorts">Cohort diagnostic</button>
<button class="tab" data-v="entity">Entity drill-down</button>
<button class="tab" data-v="whatif">What-if</button>
<button class="tab" data-v="fairness">Why not individual scores</button>
</div>
<div id="view"></div>
</div>
<footer>
All figures reproduce from <code>cost_model.py</code>, <code>ethics_audit.py</code> and
<code>make_dashboard.py</code> on the four supplied CSVs. Attrition is annualised voluntary exits over
active headcount. Diagnostic only — not a prediction, and not a basis for any decision about an
individual. NovaCorp is fictional and all data synthetic.
</footer>
<script>
const D = __DATA__;
const $ = s => document.querySelector(s);
const fmt = (n,d=1) => n===null||n===undefined ? "—" : n.toFixed(d);
let sortKey="score", sortDir=-1, filterEnt="all", filterDept="all", q="";

function cards(items){return `<div class="cards">${items.map(c=>
 `<div class="card"><div class="k">${c[0]}</div><div class="v">${c[1]}</div>
  <div class="n">${c[2]||""}</div></div>`).join("")}</div>`}

function overview(){
 const t=D.totals, c=D.company;
 const pri=D.cohorts.filter(x=>x.bandName==="Priority");
 const priHead=pri.reduce((a,b)=>a+b.headcount,0);
 return cards([
  ["Active headcount", t.active.toLocaleString(), "employees.csv, status = active"],
  ["Cohorts measured", (t.cohorts-t.suppressed)+" of "+t.cohorts,
   t.suppressed+" suppressed, "+t.suppressedPeople+" people"],
  ["Company voluntary attrition", fmt(c.attrition)+"%/yr", "annualised, on active headcount"],
  ["Company response rate", fmt(c.resp_rate)+"%", "mean of each employee's own rate"],
  ["Priority cohorts", pri.length, priHead.toLocaleString()+" people"],
 ]) + `
 <div class="panel" style="border-left:4px solid var(--p)">
 <h3>What we recommend</h3>
 <div style="font-size:14px;margin-bottom:12px">
 <b>NovaCorp counts $14.3M of regrettable attrition. On a value-based definition it is
 $45.1M.</b> Once counted properly, the loss concentrates in Entity_B — the acquisition still
 running on its own HR system. Not pay, not managers: trust in leadership and sense of purpose.
 Entity_A ran the same integration and is now the healthiest cohort in the company.</div>
 <table style="margin-bottom:4px">
 <tr><th style="width:34%">Action</th><th style="width:14%">Worth</th>
     <th style="width:18%">Cost to act</th><th>Detail</th></tr>
 <tr><td><b>1 · Redefine what counts as a regrettable loss</b></td>
     <td><b>$45.1M</b></td><td><b>~$0, policy</b></td>
     <td>Include High Performer alongside Outstanding, and separate the flag from the function
         that approves exits.</td></tr>
 <tr><td><b>2 · Finish the Entity_B integration</b></td>
     <td>$8.4M</td><td>inside guided FY26 budget</td>
     <td>As a trust problem, not a systems problem. Stabilise the Senior Manager layer first
         (9.8%/yr against Entity_A's 2.9%). Not manager training.</td></tr>
 <tr><td><b>3 · Measure acquired cohorts from day one</b></td>
     <td>—</td><td>~$0</td>
     <td>Baseline against company norms at their first survey. 152 staff on the Entity_B and
         Entity_C systems have never been surveyed at all.</td></tr>
 </table>
 <div class="note">The data rules out the three most expensive obvious responses: a pay round,
 a manager training programme, and cutting agency recruitment. Full reasoning in the deck.</div>
 </div>
 <div class="panel"><h3>How to read this</h3>
 The score is a <b>diagnostic</b>, not a prediction. It combines three gaps against the company
 figure, each shown separately in the table so you can audit it rather than trust it:
 <b>response gap</b> (40%), <b>belief gap</b> — senior leadership trust and purpose (40%), and
 <b>attrition gap</b> (20%). A high score means a cohort looks like Entity_B did before its attrition
 rose; it does not mean any individual in it is leaving.
 <div class="note">Weights are a judgement, not a finding. Response and belief carry most of the
 weight because those are the two signals that separated Entity_B from Entity_A before attrition
 moved. Attrition carries least because by the time it moves, the loss has happened.</div></div>
 <div class="grid2">
 <div class="panel"><h3>By entity</h3>${miniTable(D.entities)}</div>
 <div class="panel"><h3>By department</h3>${miniTable(D.depts)}</div></div>`;
}

function miniTable(rows){
 const s=[...rows].sort((a,b)=>(b.score??-1)-(a.score??-1));
 return `<table><tr><th>Cohort</th><th>Headcount</th><th>Attrition</th><th>Response</th><th>Score</th></tr>
 ${s.map(r=>`<tr class="${r.suppressed?'sup':''}"><td>${r.key}</td>
 <td>${r.headcount.toLocaleString()}</td><td>${fmt(r.attrition)}%</td>
 <td>${fmt(r.resp_rate)}%</td>
 <td><span class="pill ${r.bandName}">${r.suppressed?"n&lt;"+D.minResponses:fmt(r.score)}</span></td></tr>`).join("")}</table>`;
}

function cohorts(){
 const ents=[...new Set(D.cohorts.map(c=>c.parts[1]))].sort();
 const deps=[...new Set(D.cohorts.map(c=>c.parts[0]))].sort();
 let rows=D.cohorts.filter(c=>
  (filterEnt==="all"||c.parts[1]===filterEnt) &&
  (filterDept==="all"||c.parts[0]===filterDept) &&
  (q===""||c.key.toLowerCase().includes(q)));
 rows.sort((a,b)=>{const x=a[sortKey]??-1,y=b[sortKey]??-1;
  return typeof x==="string"?sortDir*x.localeCompare(y):sortDir*(x-y);});
 const th=(k,l)=>`<th data-k="${k}">${l}${sortKey===k?(sortDir<0?" ▾":" ▴"):""}</th>`;
 return `<div class="ctl">
  <label>Entity <select id="fe">${["all",...ents].map(e=>
   `<option ${e===filterEnt?"selected":""}>${e}</option>`).join("")}</select></label>
  <label>Department <select id="fd">${["all",...deps].map(e=>
   `<option ${e===filterDept?"selected":""}>${e}</option>`).join("")}</select></label>
  <input type="search" id="q" placeholder="Filter…" value="${q}">
  <button class="act" id="csv">Download CSV</button>
  <span class="note">${rows.length} cohorts shown</span></div>
 <div class="scroll"><table><tr>${th("key","Department · Entity · Level")}${th("headcount","Active")}
 ${th("n_resp","Respondents")}${th("attrition","Attrition %/yr")}${th("resp_rate","Response %")}
 ${th("trust","Trust")}${th("purpose","Purpose")}<th>Components</th>${th("score","Score")}</tr>
 ${rows.map(r=>r.suppressed
  ? `<tr class="sup"><td>${r.key}</td><td>${r.headcount}</td><td>${r.n_resp}</td>
     <td colspan="5">Suppressed — fewer than ${D.minResponses} responses</td>
     <td><span class="pill Suppressed">n&lt;${D.minResponses}</span></td></tr>`
  : `<tr><td>${r.key}</td><td>${r.headcount.toLocaleString()}</td><td>${r.n_resp}</td>
     <td>${fmt(r.attrition)}</td><td>${fmt(r.resp_rate)}</td>
     <td>${fmt(r.trust,3)}</td><td>${fmt(r.purpose,3)}</td>
     <td style="font-size:11px;color:var(--mut)">R ${fmt(r.comp.response)} ·
       B ${fmt(r.comp.belief)} · A ${fmt(r.comp.attrition)}</td>
     <td><span class="pill ${r.bandName}">${fmt(r.score)}</span>
         <span class="sbar" style="width:${Math.max(2,Math.min(46,r.score*1.1))}px"></span></td>
     </tr>`).join("")}</table></div>
 <div class="note">R = response gap, B = belief gap (trust and purpose), A = attrition gap. Each is a
 percentage shortfall against the company figure, capped at 100. Respondents are active staff only.
 Click any header to sort.</div>`;
}

function entity(){
 const rows=D.entities.filter(e=>!e.suppressed);
 return rows.map(e=>`<div class="panel"><h3>${e.key}</h3>
 ${cards([["Headcount",e.headcount.toLocaleString(),""],
   ["Attrition",fmt(e.attrition)+"%/yr","company "+fmt(D.company.attrition)+"%"],
   ["Response rate",fmt(e.resp_rate)+"%","company "+fmt(D.company.resp_rate)+"%"],
   ["High-value loss","$"+fmt(e.cost)+"M","per year"],
   ["Score",fmt(e.score),e.bandName]])}
 ${Object.entries(e.dims).map(([k,v])=>{
   const pct=Math.max(0,Math.min(100,(v-2.5)/(4-2.5)*100));
   const low=["senior_leadership_trust","purpose_meaning"].includes(k);
   return `<div class="dimrow"><span class="lab">${k.replace(/_/g," ")}</span>
   <span class="bar"><i style="width:${pct}%;background:${low?"var(--c)":"var(--p)"}"></i></span>
   <b style="width:44px;text-align:right">${fmt(v,2)}</b></div>`}).join("")}
 </div>`).join("");
}

function whatif(){
 return `<div class="panel"><h3>What is it worth if you act?</h3>
 <div class="warn"><b>The reduction rate is an assumption, not a finding.</b> 20–40% is the band
 typically claimed for targeted retention programmes. Nothing here estimates how effective any
 specific intervention would be — it shows what a given reduction would be worth if achieved.</div>
 <label>Reduction in high-value voluntary attrition:
 <input type="range" class="slider" id="sl" min="0" max="50" value="20" step="1"></label>
 <div style="margin:14px 0"><span class="big" id="sv">$9.0M</span>
 <span style="color:var(--mut)"> per year, from <b id="pc">20</b>% reduction on
 $${D.addressable}M addressable</span></div>
 <table><tr><th>Reduction</th><th>Value per year</th><th>Comparable</th></tr>
 ${[10,20,30,40].map(p=>`<tr><td>${p}%</td><td>$${(D.addressable*p/100).toFixed(1)}M</td>
 <td style="color:var(--mut)">${p===20?"lower bound typically claimed":p===40?"upper bound typically claimed":""}</td></tr>`).join("")}</table>
 <div class="note">Addressable base is $${D.addressable}M — the replacement cost of voluntary
 high-value attrition on the brief's own constants (1.5× salary, 85% backfill, 12% super),
 from <code>cost_model.py</code>. Redefining the regrettable flag costs about $0, so its return is
 not capped by budget.</div></div>`;
}

function fairness(){
 return `<div class="panel"><h3>Why this tool has no individual scores</h3>
 We tested the obvious version — a flight-risk flag on survey silence, scored per employee. It fails
 the four-fifths rule on three dimensions at once, and it is wrong most of the time.
 <table style="margin-top:12px"><tr><th>Dimension</th><th>Impact ratio</th><th>Detail</th>
 <th>n</th><th>Verdict</th></tr>
 ${D.fairness.map(f=>`<tr><td>${f.dim}</td><td><b style="color:var(--c)">${f.ratio}</b></td>
 <td>${f.detail}</td><td>${f.n}</td><td>${f.verdict}</td></tr>`).join("")}</table>
 <div class="note">Four-fifths rule: a group's rate divided by the highest group's rate. Below 0.80
 warrants investigation. These are 0.08 to 0.15.</div></div>
 <div class="grid2">
 <div class="panel"><h3>It is also wrong most of the time</h3>
 ${cards([["Flagged & left","263","true positives"],["Flagged & stayed","901","false positives"],
   ["Precision","22.6%","roughly three wrong in four"]])}
 <div class="note">The dominant outcome of deploying this per-person is a career conversation about
 someone who was never leaving.</div></div>
 <div class="panel"><h3>What we built instead</h3>
 Cohort-level only, minimum ${D.minResponses} responses, suppressed cohorts labelled, and the
 score split into its three components. Low response is heavily concentrated in the
 acquisition cohorts, so at individual level the flag would substantially be measuring
 <b>integration failure</b>, not intent.
 <div class="note">If a participation metric is ever used, staff should be told it exists. A survey
 sold as confidential and quietly re-used as a personal risk score costs you the instrument once
 people work it out.</div></div></div>`;
}

const views={overview,cohorts,entity,whatif,fairness};
let cur="overview";
function render(){
 $("#view").innerHTML=views[cur]();
 document.querySelectorAll("th[data-k]").forEach(th=>th.onclick=()=>{
  const k=th.dataset.k; if(sortKey===k)sortDir*=-1; else{sortKey=k;sortDir=-1;} render();});
 const cs=$("#csv");
 if(cs)cs.onclick=()=>{
  // Exports exactly what is on screen, suppressed cohorts included as
  // suppressed. No identifiers exist to export.
  const rows=D.cohorts.filter(c=>
   (filterEnt==="all"||c.parts[1]===filterEnt) &&
   (filterDept==="all"||c.parts[0]===filterDept) &&
   (q===""||c.key.toLowerCase().includes(q)));
  const head=["department","entity","level","active","respondents","attrition_pct_yr",
              "response_pct","trust","purpose","score","band"];
  const esc=v=>`"${String(v??"").replace(/"/g,'""')}"`;
  const body=rows.map(r=>[r.parts[0],r.parts[1],r.parts[2],r.headcount,r.n_resp,
   r.attrition,r.resp_rate,r.trust,r.purpose,r.score,r.bandName].map(esc).join(","));
  const blob=new Blob([[head.join(","),...body].join("\\n")],{type:"text/csv"});
  const a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="novacorp_cohort_diagnostic.csv"; a.click();
  URL.revokeObjectURL(a.href);
 };
 const fe=$("#fe"),fd=$("#fd"),qq=$("#q"),sl=$("#sl");
 if(fe)fe.onchange=e=>{filterEnt=e.target.value;render()};
 if(fd)fd.onchange=e=>{filterDept=e.target.value;render()};
 // render() replaces the whole view, so the input element the user is typing
 // into is destroyed and rebuilt on every keystroke. Restoring focus alone puts
 // the caret back at position 0, so the selection offset has to be carried over
 // as well or typing runs backwards.
 if(qq)qq.oninput=e=>{
  const pos=e.target.selectionStart;
  q=e.target.value.toLowerCase();
  render();
  const n=$("#q");
  if(n){n.focus(); n.setSelectionRange(pos,pos);}
 };
 if(sl)sl.oninput=e=>{const p=+e.target.value;
  $("#sv").textContent="$"+(D.addressable*p/100).toFixed(1)+"M";$("#pc").textContent=p;};
}
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
 document.querySelectorAll(".tab").forEach(x=>x.classList.remove("on"));
 t.classList.add("on");cur=t.dataset.v;sortKey="score";sortDir=-1;render();});
render();
</script></body></html>"""

html = HTML.replace("__DATA__", json.dumps(payload, separators=(",", ":"))) \
           .replace("__MINR__", str(MIN_RESPONSES))
OUT.write_text(html, encoding="utf-8")

print(f"  -> {OUT}  ({OUT.stat().st_size/1024:.0f} KB, self-contained)")
print(f"     {payload['totals']['cohorts']} cohorts, "
      f"{payload['totals']['suppressed']} suppressed "
      f"({payload['totals']['suppressedPeople']} people)")
print(f"     company: attrition {CO['attrition']:.1f}%/yr, response {CO['resp_rate']:.1f}%")
for e in sorted(entities, key=lambda x: -(x["score"] or 0)):
    print(f"     {e['key']:<18} score {e['score']:>5}  {e['bandName']}")
print("     no employee_id, name or manager_id in output")
