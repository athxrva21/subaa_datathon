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
CO_DIMS = {k: round(per_emp[k].mean(), 3) for k in DIMS}

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

# ---------------------------------------------------------------- the gap
# The headline finding, recomputed here on the same constants cost_model.py
# uses, so the chart in the file cannot drift from the chart in the deck.
vol_exits = exits[exits.exit_type == "voluntary"]
flagged = vol_exits[vol_exits.regrettable_flag]
counted = {
    "flagN": int(len(flagged)),
    "flagCost": round(replacement_cost(flagged) / 1e6, 1),
    "hvN": int(len(hi_val)),
    "hvCost": round(replacement_cost(hi_val) / 1e6, 1),
    "missedN": int((~hi_val.regrettable_flag).sum()),
    "volN": int(len(vol_exits)),
    "volCost": round(replacement_cost(vol_exits) / 1e6, 1),
}
counted["gapCost"] = round(counted["hvCost"] - counted["flagCost"], 1)

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
    "companyDims": CO_DIMS,
    "dimOrder": DIMS,
    "cohorts": cohorts,
    "entities": entities,
    "depts": depts,
    "fairness": fairness,
    "counted": counted,
    "addressable": counted["hvCost"],
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
/* ---------------------------------------------------------------- tokens
   Status colours carry good / warning / critical and never anything else.
   They are validated for colour-vision deficiency separation against the
   #FCFCFB surface, and every one of them is paired with a written band name,
   so nothing in this file is encoded by colour alone. */
:root{
 --p:#A100FF; --pd:#5B0091; --pl:#C9A0F5;
 --crit:#B3253A; --warn:#B07A00; --good:#00979E; --sup:#9A9AA6;
 --ink:#1A1A22; --ink2:#454552; --mut:#767684;
 --line:#E4E4EC; --hair:#EFEFF4;
 --bg:#FCFCFB; --surf:#fff; --tint:#F8F6FB;
 --nav:58px;
 --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
 font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;
 font-feature-settings:"kern" 1}
h1,h2,h3{margin:0;font-weight:600}
a{color:inherit}

/* ---------------------------------------------------------------- top bar */
.topbar{position:sticky;top:0;z-index:60;background:rgba(252,252,251,.86);
 -webkit-backdrop-filter:saturate(180%) blur(10px);backdrop-filter:saturate(180%) blur(10px);
 border-bottom:1px solid var(--line);transition:box-shadow .18s ease}
.topbar.stuck{box-shadow:0 1px 14px rgba(26,26,34,.08)}
.tbin{display:flex;align-items:center;gap:20px;height:var(--nav);
 padding:0 24px;max-width:1560px;margin:0 auto}
.brand{display:flex;align-items:baseline;gap:9px;white-space:nowrap;flex:none}
.glyph{display:inline-flex;align-items:flex-end;gap:2px;height:15px;transform:translateY(1px)}
.glyph i{width:3px;background:var(--pl);border-radius:1px}
.glyph i:nth-child(1){height:7px}
.glyph i:nth-child(2){height:11px;background:var(--p)}
.glyph i:nth-child(3){height:15px;background:var(--pd)}
.bn{font-weight:650;letter-spacing:-.015em;font-size:15px}
.bs{font-size:12.5px;color:var(--mut);letter-spacing:.01em}

.tabs{display:flex;gap:2px;flex:1;min-width:0;overflow-x:auto;scrollbar-width:none;
 align-self:stretch;align-items:center}
.tabs::-webkit-scrollbar{display:none}
.tab{position:relative;display:inline-flex;align-items:center;gap:7px;flex:none;
 height:calc(var(--nav) - 1px);padding:0 13px;border:0;background:none;cursor:pointer;
 font:550 13px inherit;color:var(--mut);letter-spacing:-.005em}
.tab:hover{color:var(--ink)}
.tab.on{color:var(--ink);font-weight:650}
.tab::after{content:"";position:absolute;left:11px;right:11px;bottom:0;height:2px;
 background:var(--p);border-radius:2px 2px 0 0;transform:scaleX(0);transition:transform .16s ease}
.tab.on::after{transform:scaleX(1)}
.tab kbd{font:500 9.5px var(--mono);color:var(--mut);border:1px solid var(--line);
 border-radius:3px;padding:1px 3.5px;opacity:.55;background:var(--surf)}
.tab.on kbd{opacity:.9;border-color:var(--pl);color:var(--pd)}

.tbmeta{display:flex;align-items:center;gap:14px;flex:none;margin-left:auto}
.shield{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:600;
 color:#0A6E73;background:rgba(0,151,158,.08);border:1px solid rgba(0,151,158,.28);
 padding:4px 10px 4px 8px;border-radius:100px;cursor:help;white-space:nowrap}
.shield svg{flex:none}
.vr{width:1px;height:20px;background:var(--line)}
.team{font-size:11.5px;color:var(--mut);white-space:nowrap;letter-spacing:.01em}
.team b{color:var(--ink2);font-weight:600}

/* ---------------------------------------------------------------- layout */
.wrap{max-width:1560px;margin:0 auto;padding:22px 24px 40px}
.eyebrow{display:flex;align-items:center;gap:11px;margin:26px 0 13px}
.eyebrow:first-child{margin-top:4px}
.eyebrow .ix{font:600 10.5px var(--mono);color:var(--p);letter-spacing:.06em}
.eyebrow h2{font-size:11.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--ink2)}
.eyebrow .fill{flex:1;height:1px;background:var(--line)}
.eyebrow .aside{font-size:11.5px;color:var(--mut)}

.panel{background:var(--surf);border:1px solid var(--line);border-radius:7px;padding:18px 20px}
.panel + .panel{margin-top:14px}
.panel h3{font-size:13.5px;margin-bottom:9px;letter-spacing:-.01em}
.panel.vc{display:flex;flex-direction:column;justify-content:center}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.gridA{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:14px}
/* without this a wide table sets its column's min-content and the grid pushes
   past the viewport instead of letting the table scroll in its own card */
.grid2>*,.gridA>*{min-width:0}
@media(max-width:980px){.grid2,.gridA{grid-template-columns:1fr}}
.note{font-size:11.5px;color:var(--mut);margin-top:9px;line-height:1.5}
.lede{font-size:14.5px;line-height:1.6}
.lede b{font-weight:650}

/* ------------------------------------------------------------- stat rail */
.rail{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));
 background:var(--surf);border:1px solid var(--line);border-radius:7px;overflow:hidden}
.stat{padding:13px 16px 14px;border-left:1px solid var(--hair)}
.stat:first-child{border-left:0}
.stat .k{font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--mut)}
.stat .v{font-size:27px;font-weight:600;letter-spacing:-.025em;line-height:1.15;margin-top:5px;
 font-variant-numeric:proportional-nums}
.stat .n{font-size:11px;color:var(--mut);margin-top:3px}
.stat .d{font-size:11px;font-weight:600;margin-top:3px}
.d.up{color:var(--crit)} .d.dn{color:var(--good)} .d.flat{color:var(--mut)}

/* ---------------------------------------------------------------- tables */
table{width:100%;border-collapse:collapse;font-size:12.5px;
 font-variant-numeric:tabular-nums}
th{text-align:left;font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
 color:var(--mut);padding:0 10px 7px;border-bottom:1px solid var(--ink);white-space:nowrap;
 background:var(--surf)}
th.s{cursor:pointer;user-select:none}
th.s:hover{color:var(--ink)}
th .ar{opacity:0;margin-left:3px}
th.s:hover .ar{opacity:.35}
th.act{color:var(--ink)} th.act .ar{opacity:1;color:var(--p)}
td{padding:7px 10px;border-bottom:1px solid var(--hair);vertical-align:middle}
tbody tr:hover td{background:var(--tint)}
tr.sup td{color:#9A9AA6}
td.num,th.num{text-align:right}
.tw{max-height:calc(100vh - 232px);overflow:auto;border:1px solid var(--line);
 border-radius:7px;background:var(--surf)}
.tw thead th{position:sticky;top:0;z-index:2}
.tw table{font-size:12.5px}
.tw td:first-child,.tw th:first-child{padding-left:14px;white-space:nowrap}
.flat-t{border:1px solid var(--line);border-radius:7px;background:var(--surf);padding:4px 0 0;
 overflow-x:auto}
.flat-t td:first-child,.flat-t th:first-child{padding-left:14px}
.flat-t tr:last-child td{border-bottom:0}
.ck{font-weight:600}

/* The band colour rides the square, not the type: a status hue light enough to
   read as a mark is not necessarily legible as 11px text, and the band name or
   number beside it is what carries the meaning anyway. */
.pill{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:650;
 white-space:nowrap;color:var(--ink)}
.pill::before{content:"";width:7px;height:7px;border-radius:2px;flex:none;
 background:var(--bc,var(--mut))}
.Priority{--bc:var(--crit)} .Elevated{--bc:var(--warn)}
.Stable{--bc:var(--good)} .Suppressed{--bc:var(--sup);color:var(--mut)}

/* --------------------------------------------------------------- filters */
.filters{background:var(--surf);border:1px solid var(--line);border-radius:7px;margin-bottom:12px}
.frow{display:flex;align-items:center;gap:9px 18px;padding:10px 14px;flex-wrap:wrap}
.frow + .frow{border-top:1px solid var(--hair)}
.fgroup{display:inline-flex;align-items:center;gap:9px;white-space:nowrap;max-width:100%}
.flab{font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
 color:var(--mut);flex:none}
.seg{display:inline-flex;background:var(--tint);border:1px solid var(--line);border-radius:6px;
 padding:2px;gap:2px;max-width:100%;overflow-x:auto;scrollbar-width:none}
.seg::-webkit-scrollbar{display:none}
.seg button{border:0;background:none;cursor:pointer;font:600 12px inherit;color:var(--ink2);
 padding:4px 11px;border-radius:4px;white-space:nowrap;transition:background .12s,color .12s}
.seg button:hover{color:var(--ink)}
.seg button.on{background:var(--surf);color:var(--pd);
 box-shadow:0 1px 2px rgba(26,26,34,.10),0 0 0 1px rgba(91,0,145,.10)}
.seg.bands button.on[data-b=Priority]{color:var(--crit)}
.seg.bands button.on[data-b=Elevated]{color:var(--warn)}
.seg.bands button.on[data-b=Stable]{color:var(--good)}
.sel{position:relative;display:inline-flex}
.sel select{appearance:none;-webkit-appearance:none;font:600 12px inherit;color:var(--ink2);
 background:var(--surf);border:1px solid var(--line);border-radius:6px;
 padding:6px 28px 6px 10px;cursor:pointer;max-width:230px}
.sel select:hover{border-color:#CFCFDA}
.sel select:focus-visible{outline:2px solid var(--pl);outline-offset:1px}
.sel::after{content:"";position:absolute;right:10px;top:50%;width:7px;height:7px;
 border-right:1.5px solid var(--mut);border-bottom:1.5px solid var(--mut);
 transform:translateY(-70%) rotate(45deg);pointer-events:none}
.search{position:relative;display:inline-flex;align-items:center}
.search svg{position:absolute;left:9px;pointer-events:none}
.search input{font:inherit;font-size:12.5px;border:1px solid var(--line);border-radius:6px;
 padding:6px 26px 6px 28px;background:var(--surf);width:196px;color:var(--ink)}
.search input::placeholder{color:var(--mut)}
.search input:focus-visible{outline:2px solid var(--pl);outline-offset:1px;border-color:var(--pl)}
.search .x{position:absolute;right:5px;border:0;background:none;cursor:pointer;color:var(--mut);
 font-size:15px;line-height:1;padding:2px 5px;border-radius:4px}
.search .x:hover{background:var(--tint);color:var(--ink)}
.tog{display:inline-flex;align-items:center;gap:8px;cursor:pointer;font-size:12px;
 font-weight:600;color:var(--ink2);user-select:none}
.tog input{position:absolute;opacity:0;width:0;height:0}
.tog .tr{width:34px;height:19px;border-radius:100px;background:#DBDBE4;position:relative;
 transition:background .16s ease;flex:none}
.tog .tr::after{content:"";position:absolute;top:2px;left:2px;width:15px;height:15px;
 border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(26,26,34,.28);
 transition:transform .16s cubic-bezier(.3,.8,.4,1)}
.tog input:checked + .tr{background:var(--p)}
.tog input:checked + .tr::after{transform:translateX(15px)}
.tog input:focus-visible + .tr{outline:2px solid var(--pl);outline-offset:2px}
.btn{display:inline-flex;align-items:center;gap:6px;font:600 12px inherit;color:var(--ink2);
 background:var(--surf);border:1px solid var(--line);border-radius:6px;padding:6px 11px;
 cursor:pointer;transition:border-color .12s,color .12s}
.btn:hover{border-color:var(--pl);color:var(--pd);background:var(--tint)}
.spacer{flex:1}
.count{font-size:11.5px;color:var(--mut);font-variant-numeric:tabular-nums}
.count b{color:var(--ink);font-weight:650}

/* ---------------------------------------------------------------- charts */
figure{margin:0}
figcaption{font-size:11.5px;color:var(--mut);margin-top:8px;line-height:1.5}
/* Charts only — inline icons keep their own intrinsic size. Each chart also
   carries a max-width equal to its own viewBox width: an SVG stretched past it
   scales the type up with the geometry, which is how a chart ends up with
   16px axis labels in a wide panel. */
svg.ch{display:block;width:100%;height:auto;margin:0 auto;overflow:visible}
.dot{display:inline-block;width:7px;height:7px;border-radius:2px;margin-right:6px}
.legend{display:flex;gap:14px;flex-wrap:wrap;align-items:center;font-size:11.5px;
 color:var(--ink2);margin-bottom:10px}
.legend i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:6px;
 vertical-align:-1px}
.hit{cursor:crosshair}
#tip{position:fixed;z-index:90;pointer-events:none;opacity:0;transition:opacity .1s;
 background:#1A1A22;color:#fff;font-size:11.5px;line-height:1.45;padding:8px 10px;
 border-radius:6px;box-shadow:0 6px 22px rgba(26,26,34,.28);max-width:260px}
#tip b{font-weight:650} #tip .t2{color:#B9B9C8}

/* inline component bar inside the cohort table */
.cbar{display:inline-flex;align-items:center;height:9px;width:104px;vertical-align:-1px}
.cbar span{height:9px;display:block}
.cbar span:first-child{border-radius:2px 0 0 2px}
.cbar span:last-child{border-radius:0 2px 2px 0}

/* --------------------------------------------------------------- slider */
.range{display:flex;align-items:center;gap:14px;margin:6px 0 2px}
input[type=range]{-webkit-appearance:none;appearance:none;background:none;flex:1;max-width:520px;
 height:22px;cursor:pointer}
input[type=range]::-webkit-slider-runnable-track{height:5px;border-radius:100px;
 background:linear-gradient(90deg,var(--p) var(--fill,40%),#E6E6EE var(--fill,40%))}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:17px;height:17px;
 border-radius:50%;background:#fff;border:2px solid var(--p);margin-top:-6px;
 box-shadow:0 1px 4px rgba(26,26,34,.25)}
input[type=range]::-moz-range-track{height:5px;border-radius:100px;background:#E6E6EE}
input[type=range]::-moz-range-progress{height:5px;border-radius:100px;background:var(--p)}
input[type=range]::-moz-range-thumb{width:15px;height:15px;border-radius:50%;background:#fff;
 border:2px solid var(--p)}
input[type=range]:focus-visible{outline:2px solid var(--pl);outline-offset:4px;border-radius:4px}
.hero{font-size:40px;font-weight:600;letter-spacing:-.03em;color:var(--pd);
 font-variant-numeric:proportional-nums}

.callout{border-left:2px solid var(--warn);background:rgba(176,122,0,.05);padding:10px 14px;
 font-size:12.5px;border-radius:0 5px 5px 0;margin-bottom:14px}
.callout b{font-weight:650}
.rec{border-left:2px solid var(--p)}
footer{border-top:1px solid var(--line);margin-top:34px;padding:18px 24px 30px;
 max-width:1560px;margin-left:auto;margin-right:auto;color:var(--mut);font-size:11.5px}
footer .fr{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;align-items:baseline}
footer code{font:11px var(--mono);color:var(--ink2)}
footer .cred b{color:var(--ink2);font-weight:600}

@media(max-width:1120px){
 .tbin{height:auto;padding:9px 16px;flex-wrap:wrap;row-gap:6px}
 .tabs{order:3;width:100%;flex-basis:100%}
 .tab{height:38px}
 .tab::after{bottom:-9px}
 .wrap{padding:18px 16px 34px}
 .tw{max-height:none}
}
@media(max-width:640px){.tab kbd{display:none} .bs{display:none} .shield span{display:none}}

@media print{
 /* The deck may be printed in black and white, so a status colour alone must
    never be the carrier: every band prints its written name beside the mark. */
 body{font-size:10px;background:#fff}
 .topbar{position:static;background:#fff;box-shadow:none}
 .tabs,.filters,#tip,.tab kbd,input[type=range]{display:none!important}
 .tw{max-height:none;overflow:visible;border:0}
 .panel,.rail,.tw{break-inside:avoid}
 tr,figure{break-inside:avoid}
 svg.ch{max-width:640px}
 *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style></head><body>

<div class="topbar" id="topbar"><div class="tbin">
 <div class="brand">
  <span class="glyph" aria-hidden="true"><i></i><i></i><i></i></span>
  <span class="bn">NovaCorp</span><span class="bs">cohort diagnostic</span>
 </div>
 <nav class="tabs" id="tabs">
  <button class="tab on" data-v="overview">Overview<kbd>1</kbd></button>
  <button class="tab" data-v="cohorts">Cohorts<kbd>2</kbd></button>
  <button class="tab" data-v="entity">Entities<kbd>3</kbd></button>
  <button class="tab" data-v="whatif">What-if<kbd>4</kbd></button>
  <button class="tab" data-v="fairness">Why no individual scores<kbd>5</kbd></button>
 </nav>
 <div class="tbmeta">
  <span class="shield" title="No employee ID, name or manager ID exists anywhere in this file. Aggregation happens in Python before the file is written, not in the interface, and cohorts below __MINR__ survey responses are suppressed entirely.">
   <svg width="12" height="13" viewBox="0 0 12 13" fill="none" aria-hidden="true">
    <path d="M6 .8 10.7 2.6v3.7c0 3-2 5.2-4.7 6-2.7-.8-4.7-3-4.7-6V2.6L6 .8Z"
     stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
    <path d="M3.9 6.4 5.4 8l2.8-3" stroke="currentColor" stroke-width="1.3"
     stroke-linecap="round" stroke-linejoin="round"/></svg><span>No individual data</span></span>
  <span class="vr"></span>
  <span class="team">Team <b>O for 4</b></span>
 </div>
</div></div>

<div class="wrap"><div id="view"></div></div>
<div id="tip"></div>

<footer><div class="fr">
 <div style="max-width:940px">All figures reproduce from <code>cost_model.py</code>,
 <code>ethics_audit.py</code> and <code>make_dashboard.py</code> on the four supplied CSVs.
 Attrition is annualised voluntary exits over active headcount. Diagnostic only — not a
 prediction, and not a basis for any decision about an individual. There is no employee ID,
 name or manager ID in this file. NovaCorp is fictional and all data synthetic.</div>
 <div class="cred">Accenture × SUBAA People Analytics Challenge<br>Team <b>O for 4</b></div>
</div></footer>

<script>
const D = __DATA__;
const $ = s => document.querySelector(s);
const fmt = (n,d=1) => n===null||n===undefined ? "—" : n.toFixed(d);
const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const C = {crit:"#B3253A",warn:"#B07A00",good:"#00979E",sup:"#9A9AA6",
           p:"#A100FF",pd:"#5B0091",pl:"#C9A0F5",ink:"#1A1A22",ink2:"#454552",
           mut:"#767684",line:"#E4E4EC",surf:"#FCFCFB"};
const sign = d => (d>=0?"+":"−")+Math.abs(d).toFixed(2);
const dimCol = d => d<-0.02?C.crit:(d>0.02?C.good:C.mut);
const dimLab = k => {const l=k.replace(/_/g," "); return l.charAt(0).toUpperCase()+l.slice(1);};
const BAND = {Priority:C.crit,Elevated:C.warn,Stable:C.good,Suppressed:C.sup};
// The three score components, in the order they are weighted. One hue, three
// steps: they are parts of one number, not four unrelated series.
const COMP = [["response","Response gap","#5B0091",0.4],
              ["belief","Belief gap","#A100FF",0.4],
              ["attrition","Attrition gap","#C9A0F5",0.2]];

let cur="overview", sortKey="score", sortDir=-1;
let filterEnt="all", filterDept="all", filterBand="all", showSup=true, q="";

/* ------------------------------------------------------------ svg helpers */
// Rounded at the data end, square at the baseline.
function hbar(x,y,w,h,fill,r=4){
 w=Math.max(w,0.6); r=Math.min(r,w,h/2);
 return `<path d="M${x},${y}h${w-r}a${r},${r} 0 0 1 ${r},${r}v${h-2*r}a${r},${r} 0 0 1 ${-r},${r}h${-(w-r)}z" fill="${fill}"/>`;
}
function niceTicks(min,max,n){
 const span=(max-min)||1, raw=span/n, mag=Math.pow(10,Math.floor(Math.log10(raw)));
 const step=[1,2,2.5,5,10].find(s=>s*mag>=raw)*mag;
 const out=[]; for(let v=Math.ceil(min/step)*step; v<=max+1e-9; v+=step) out.push(+v.toFixed(6));
 return out;
}
const gridline=(x1,y1,x2,y2)=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${C.line}" stroke-width="1"/>`;
const txt=(x,y,s,o={})=>`<text x="${x}" y="${y}" fill="${o.fill||C.mut}" font-size="${o.size||10.5}"
 text-anchor="${o.anchor||"start"}" font-weight="${o.weight||400}"
 ${o.mono?'font-family="ui-monospace,Menlo,monospace"':''}
 ${o.rotate?`transform="rotate(${o.rotate} ${x} ${y})"`:""}
 style="font-variant-numeric:tabular-nums">${s}</text>`;

/* --------------------------------------------------------------- tooltip */
const tipEl = () => $("#tip");
function bindTips(root){
 root.querySelectorAll("[data-tip]").forEach(el=>{
  el.addEventListener("mousemove",e=>{
   const t=tipEl(); t.innerHTML=el.dataset.tip; t.style.opacity=1;
   const b=t.getBoundingClientRect();
   let x=e.clientX+14, y=e.clientY-b.height-12;
   if(x+b.width>innerWidth-8) x=e.clientX-b.width-14;
   if(y<8) y=e.clientY+18;
   t.style.left=x+"px"; t.style.top=y+"px";
  });
  el.addEventListener("mouseleave",()=>{tipEl().style.opacity=0});
 });
}

/* ============================================================== CHART 1
   The measurement gap. One bar is a subset of the other, so the second bar
   redraws the first as its left segment and shows what the flag misses as the
   remainder. Anything else would ask the reader to subtract two bar lengths. */
function gapChart(){
 const k=D.counted, W=700, H=232, x0=0, w=616, BH=30, max=k.hvCost*1.06;
 const sc=v=>v/max*w;
 const rows=[
  {lab:"HR's regrettable_flag, as configured", n:k.flagN, val:k.flagCost, y:46},
  {lab:"Value-based definition — every voluntary High Performer and Outstanding exit",
   n:k.hvN, val:k.hvCost, y:150}
 ];
 let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" style="max-width:${W}px" role="img" aria-label="Cost of regrettable attrition under two definitions">`;
 s+=`<line x1="${x0}" y1="26" x2="${x0}" y2="${H-24}" stroke="${C.line}" stroke-width="1"/>`;
 rows.forEach((r,i)=>{
  const vy=r.y+BH/2+4.5;
  s+=txt(x0+2,r.y-9,esc(r.lab),{size:11.5,fill:C.ink2,weight:600});
  if(i===0){
   s+=hbar(x0,r.y,sc(r.val),BH,C.p);
  }else{
   const a=sc(k.flagCost), gap=sc(r.val)-a;
   s+=`<g data-tip="<b>Counted today</b><br>$${k.flagCost.toFixed(1)}M · ${k.flagN} exits">`
     + hbar(x0,r.y,a,BH,C.p) + `</g>`;
   s+=`<g data-tip="<b>Never counted as a loss</b><br>$${k.gapCost.toFixed(1)}M · ${k.missedN} high performers">`
     + hbar(x0+a+2,r.y,gap-2,BH,C.crit) + `</g>`;
   s+=txt(x0+a+10,r.y+BH+22,
        `${k.missedN} high performers left and were never recorded as a loss — $${k.gapCost.toFixed(1)}M a year`,
        {size:11.5,fill:C.crit,weight:600});
  }
  s+=txt(x0+sc(r.val)+11,vy,`$${r.val.toFixed(1)}M`,{size:14,weight:650,fill:C.ink});
  s+=txt(x0+sc(r.val)+11,vy+16,`${r.n} exits`,{size:11});
 });
 s+=`</svg>`;
 return `<div class="legend"><span><i style="background:${C.p}"></i>Counted today</span>
  <span><i style="background:${C.crit}"></i>Missed by the flag</span></div>
  <figure>${s}<figcaption>Replacement cost per year on the brief's own constants —
  1.5× salary, 85% backfill, 12% super, over the two-year window. The ceiling, all
  ${D.counted.volN} voluntary exits, is $${D.counted.volCost.toFixed(1)}M.</figcaption></figure>`;
}

/* ============================================================== CHART 2
   Where the risk sits: response rate against attrition, one dot per cohort.
   The table below is the same data, so nothing here is gated behind a hover. */
function scatter(rows){
 const pts=rows.filter(r=>!r.suppressed);
 if(!pts.length) return `<div class="note">No cohorts match the current filters.</div>`;
 const W=1200,H=360,L=54,R=18,T=16,B=44;
 const pw=W-L-R, ph=H-T-B;
 const xs=pts.map(p=>p.resp_rate), ys=pts.map(p=>p.attrition);
 const x1=Math.min(...xs,D.company.resp_rate)-4, x2=Math.max(...xs,D.company.resp_rate)+3;
 const y2=Math.max(...ys,D.company.attrition)*1.1;
 const X=v=>L+(v-x1)/(x2-x1)*pw, Y=v=>T+ph-(v/y2)*ph;
 const maxHead=Math.max(...pts.map(p=>p.headcount));
 const Rr=h=>4+Math.sqrt(h/maxHead)*13;

 let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" style="max-width:${W}px" role="img" aria-label="Survey response rate against voluntary attrition, one dot per cohort">`;
 niceTicks(0,y2,5).forEach(t=>{
  s+=gridline(L,Y(t),W-R,Y(t))+txt(L-9,Y(t)+3.5,fmt(t,0)+"%",{anchor:"end"});
 });
 niceTicks(x1,x2,6).forEach(t=>{
  s+=txt(X(t),H-B+18,fmt(t,0)+"%",{anchor:"middle"});
 });
 s+=gridline(L,T+ph,W-R,T+ph);
 // company reference crosshair
 s+=`<line x1="${X(D.company.resp_rate)}" y1="${T}" x2="${X(D.company.resp_rate)}" y2="${T+ph}" stroke="${C.ink}" stroke-width="1" opacity=".28"/>`;
 s+=`<line x1="${L}" y1="${Y(D.company.attrition)}" x2="${W-R}" y2="${Y(D.company.attrition)}" stroke="${C.ink}" stroke-width="1" opacity=".28"/>`;
 s+=txt(X(D.company.resp_rate)-6,T+10,`company ${fmt(D.company.resp_rate)}%`,{anchor:"end",size:10});
 s+=txt(W-R,Y(D.company.attrition)-6,`company ${fmt(D.company.attrition)}%/yr`,{anchor:"end",size:10});
 s+=txt(L+6,T+13,"↖ quieter and leaving faster",{size:10.5,fill:C.crit,weight:600});
 // marks, largest first so small cohorts stay clickable on top
 [...pts].sort((a,b)=>b.headcount-a.headcount).forEach(p=>{
  const cx=X(p.resp_rate), cy=Y(p.attrition), r=Rr(p.headcount);
  const tip=`<b>${esc(p.key)}</b><br><span class="t2">${p.headcount.toLocaleString()} active · `
   +`${p.n_resp} respondents</span><br>Response ${fmt(p.resp_rate)}% · Attrition ${fmt(p.attrition)}%/yr`
   +`<br>Trust ${fmt(p.trust,2)} · Purpose ${fmt(p.purpose,2)}<br>Score ${fmt(p.score)} — ${p.bandName}`;
  s+=`<g class="hit" data-tip="${tip.replace(/"/g,"&quot;")}">
   <circle cx="${cx}" cy="${cy}" r="${r}" fill="${BAND[p.bandName]}" fill-opacity=".72"
    stroke="${C.surf}" stroke-width="2"/>
   <circle cx="${cx}" cy="${cy}" r="${Math.max(r,13)}" fill="transparent"/></g>`;
 });
 s+=txt(L+pw/2,H-4,"Survey response rate",{anchor:"middle",size:11,fill:C.mut});
 s+=txt(13,T+ph/2,"Voluntary attrition (%/yr)",{anchor:"middle",size:11,fill:C.mut,rotate:-90});
 s+=`</svg>`;
 const nsup=rows.length-pts.length;
 return `<div class="legend">
   <span><i style="background:${C.crit}"></i>Priority</span>
   <span><i style="background:${C.warn}"></i>Elevated</span>
   <span><i style="background:${C.good}"></i>Stable</span>
   <span style="color:var(--mut)">Dot size = active headcount</span></div>
  <figure>${s}<figcaption>Each dot is one department × entity × level cohort${
   nsup?`. ${nsup} suppressed cohort${nsup>1?"s":""} cannot be plotted — they have no published scores`:""
  }. Every value is also in the table below.</figcaption></figure>`;
}

/* ============================================================== CHART 3
   Entity dimensions as deviations from the company average, not as absolute
   scores. On a 1–5 scale the absolute bars all look alike and hide the finding;
   the deviation is the finding. Shared scale and shared row order across
   entities, so the panels can be read against each other. */
function dimOrderGlobal(){
 const worst={};
 D.dimOrder.forEach(k=>{
  worst[k]=Math.min(...D.entities.filter(e=>!e.suppressed).map(e=>e.dims[k]-D.companyDims[k]));
 });
 return [...D.dimOrder].sort((a,b)=>worst[a]-worst[b]);
}
function deviation(e,order,dom){
 // Values live in their own right-hand column rather than beside each dot: a
 // dot sitting far from zero pushes its label into the dimension name, and
 // nudging labels off their marks reads as noise.
 const W=640,L=178,VC=56,ROW=25,H=order.length*ROW+34;
 const half=(W-L-VC-14)/2, zero=L+half;
 const X=d=>zero+(d/dom)*half;
 let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" style="max-width:${W}px" role="img" aria-label="${esc(e.key)} engagement dimensions versus the company average">`;
 s+=`<line x1="${zero}" y1="16" x2="${zero}" y2="${H-18}" stroke="${C.ink}" stroke-width="1" opacity=".35"/>`;
 s+=txt(zero,10,"company average",{anchor:"middle",size:9.5});
 order.forEach((k,i)=>{
  const y=26+i*ROW+ROW/2, d=e.dims[k]-D.companyDims[k];
  const col=dimCol(d);
  s+=txt(L-12,y+3.5,dimLab(k),{anchor:"end",size:11,fill:C.ink});
  s+=`<line x1="${zero}" y1="${y}" x2="${X(d)}" y2="${y}" stroke="${col}" stroke-width="1.5" opacity=".45"/>`;
  s+=`<g data-tip="<b>${esc(dimLab(k))}</b><br>${esc(e.key)} ${fmt(e.dims[k],2)} · company ${fmt(D.companyDims[k],2)}<br><span class='t2'>difference ${sign(d)}</span>">
   <circle cx="${X(d)}" cy="${y}" r="5" fill="${col}" stroke="${C.surf}" stroke-width="2"/>
   <circle cx="${X(d)}" cy="${y}" r="12" fill="transparent"/></g>`;
  s+=txt(W-6,y+3.5,sign(d),{anchor:"end",size:10.5,fill:C.ink2,weight:600});
 });
 s+=txt(zero-8,H-6,"worse than company ←",{anchor:"end",size:9.5});
 s+=txt(zero+8,H-6,"→ better",{size:9.5});
 s+=txt(W-6,20,"vs co.",{anchor:"end",size:9.5});
 s+=`</svg>`;
 return s;
}

/* ============================================================== CHART 4
   The score, decomposed. Segment widths are the weighted contributions
   0.4·R + 0.4·B + 0.2·A, so the three of them add up to exactly the number
   printed beside the bar. */
function compBar(r){
 const tot=45, px=104;
 const parts=COMP.map(([k,lab,col,w])=>({lab,col,v:r.comp[k]*w,raw:r.comp[k]}));
 const tip=parts.map(p=>`${p.lab} ${fmt(p.raw)} → ${fmt(p.v)}`).join("<br>");
 return `<span class="cbar" data-tip="<b>Score ${fmt(r.score)}</b><br><span class='t2'>gap → weighted contribution</span><br>${tip}">`
  + parts.map(p=>`<span style="width:${Math.max(p.v/tot*px,p.v>0?1.5:0)}px;background:${p.col};margin-right:${p.v>0?2:0}px"></span>`).join("")
  + `</span>`;
}

/* ============================================================== CHART 5 */
function whatifChart(pct){
 const W=620,H=210,L=44,R=14,T=14,B=34, pw=W-L-R, ph=H-T-B;
 const maxY=D.addressable*0.5*1.08;   // headroom, so the line ends inside the frame
 const X=p=>L+p/50*pw, Y=v=>T+ph-v/maxY*ph;
 let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" style="max-width:${W}px" role="img" aria-label="Value per year against reduction in high-value voluntary attrition">`;
 s+=`<rect x="${X(20)}" y="${T}" width="${X(40)-X(20)}" height="${ph}" fill="${C.p}" opacity=".06"/>`;
 s+=txt((X(20)+X(40))/2,T+12,"band typically claimed",{anchor:"middle",size:10});
 niceTicks(0,maxY,4).forEach(t=>{
  s+=gridline(L,Y(t),W-R,Y(t))+txt(L-8,Y(t)+3.5,"$"+fmt(t,0)+"M",{anchor:"end"});
 });
 [0,10,20,30,40,50].forEach(t=>s+=txt(X(t),H-B+18,t+"%",{anchor:"middle"}));
 s+=gridline(L,T+ph,W-R,T+ph);
 s+=`<path d="M${X(0)},${Y(0)}L${X(50)},${Y(D.addressable*0.5)}" stroke="${C.p}" stroke-width="2" fill="none" stroke-linecap="round"/>`;
 const v=D.addressable*pct/100;
 s+=`<line x1="${X(pct)}" y1="${Y(v)}" x2="${X(pct)}" y2="${T+ph}" stroke="${C.p}" stroke-width="1" opacity=".35"/>`;
 s+=`<circle cx="${X(pct)}" cy="${Y(v)}" r="6" fill="${C.p}" stroke="${C.surf}" stroke-width="2"/>`;
 s+=txt(X(pct)+(pct>38?-12:12),Y(v)-9,"$"+v.toFixed(1)+"M",
       {anchor:pct>38?"end":"start",size:12.5,weight:650,fill:C.ink});
 s+=txt(L+pw/2,H-3,"Reduction in high-value voluntary attrition",{anchor:"middle",size:11});
 s+=`</svg>`;
 return s;
}

/* ============================================================== CHART 6 */
function fairnessChart(){
 const W=900,H=180,L=180,R=76,T=28, pw=W-L-R, ROW=36;
 const X=v=>L+v*pw;
 let s=`<svg class="ch" viewBox="0 0 ${W} ${H}" style="max-width:${W}px" role="img" aria-label="Four-fifths impact ratios against the 0.80 threshold">`;
 D.fairness.forEach((f,i)=>{
  const y=T+i*ROW;
  s+=txt(L-12,y+16,esc(f.dim),{anchor:"end",size:11.5,fill:C.ink});
  s+=`<rect x="${L}" y="${y+4}" width="${pw}" height="18" fill="${C.line}" opacity=".45" rx="2"/>`;
  s+=`<g data-tip="<b>${esc(f.dim)}</b><br>${esc(f.detail)}<br><span class='t2'>n = ${esc(f.n)}</span>">`
    + hbar(L,y+4,X(f.ratio)-L,18,C.crit,3)
    + `<rect x="${L}" y="${y}" width="${pw}" height="26" fill="transparent"/></g>`;
  s+=txt(X(f.ratio)+9,y+17,f.ratio.toFixed(2),{size:12,weight:650,fill:C.ink});
 });
 s+=`<line x1="${X(0.8)}" y1="12" x2="${X(0.8)}" y2="${T+3*ROW-4}" stroke="${C.ink}" stroke-width="1.5"/>`;
 s+=txt(X(0.8)-6,10,"0.80 four-fifths threshold",{anchor:"end",size:10.5,fill:C.ink,weight:600});
 s+=txt(L,H-6,"0.00",{size:10});
 s+=txt(L+pw,H-6,"1.00 — parity",{anchor:"end",size:10});
 s+=`</svg>`;
 return `<figure>${s}<figcaption>A group's flag rate divided by the highest group's rate.
  Below 0.80 warrants investigation. These are 0.08 to 0.15 — the per-employee version of
  this tool fails on three dimensions at once.</figcaption></figure>`;
}

/* ---------------------------------------------------------------- views */
function eyebrow(ix,label,aside=""){
 return `<div class="eyebrow"><span class="ix">${ix}</span><h2>${label}</h2>
  <span class="fill"></span>${aside?`<span class="aside">${aside}</span>`:""}</div>`;
}
function rail(items){
 return `<div class="rail">${items.map(c=>`<div class="stat"><div class="k">${c[0]}</div>
  <div class="v">${c[1]}</div>${c[3]?`<div class="d ${c[3][1]}">${c[3][0]}</div>`:""}
  <div class="n">${c[2]||""}</div></div>`).join("")}</div>`;
}

function overview(){
 const t=D.totals, c=D.company;
 const pri=D.cohorts.filter(x=>x.bandName==="Priority");
 const priHead=pri.reduce((a,b)=>a+b.headcount,0);
 return eyebrow("01","Where NovaCorp stands","two-year window, four supplied CSVs")
 + rail([
  ["Active headcount", t.active.toLocaleString(), "employees.csv · status = active"],
  ["Voluntary attrition", fmt(c.attrition)+"%/yr", "annualised, on active headcount"],
  ["Survey response", fmt(c.resp_rate)+"%", "mean of each employee's own rate"],
  ["Cohorts measured", (t.cohorts-t.suppressed)+" of "+t.cohorts,
   t.suppressed+" suppressed · "+t.suppressedPeople+" people"],
  ["Priority cohorts", pri.length, priHead.toLocaleString()+" people"],
 ])
 + eyebrow("02","The measurement gap")
 + `<div class="gridA">
   <div class="panel vc">${gapChart()}</div>
   <div class="panel rec"><h3>What we recommend</h3>
    <div class="lede" style="margin-bottom:12px">NovaCorp counts <b>$${D.counted.flagCost.toFixed(1)}M</b>
    of regrettable attrition. On a value-based definition it is <b>$${D.counted.hvCost.toFixed(1)}M</b>.
    Once counted properly the loss concentrates in Entity_B — the acquisition still running on its
    own HR system. Not pay, not managers: trust in leadership and sense of purpose. Entity_A ran the
    same integration and is now the healthiest cohort in the company.</div>
    <table><thead><tr><th style="width:38%">Action</th><th class="num">Worth</th>
      <th>Cost to act</th></tr></thead><tbody>
     <tr><td class="ck">1 · Redefine what counts as a regrettable loss</td>
      <td class="num ck">$${D.counted.hvCost.toFixed(1)}M</td><td>~$0, policy</td></tr>
     <tr><td class="ck">2 · Finish the Entity_B integration</td>
      <td class="num ck">$8.4M</td><td>inside guided FY26 budget</td></tr>
     <tr><td class="ck">3 · Measure acquired cohorts from day one</td>
      <td class="num">—</td><td>~$0</td></tr></tbody></table>
    <div class="note">1 · Include High Performer alongside Outstanding, and separate the flag from
    the function that approves exits. 2 · As a trust problem, not a systems problem — stabilise the
    Senior Manager layer first, 9.8%/yr against Entity_A's 2.9%. Not manager training.
    3 · Baseline acquired staff against company norms at their first survey; 152 people on the
    Entity_B and Entity_C systems have never been surveyed at all.</div>
    <div class="note">The data rules out the three most expensive obvious responses: a pay round, a
    manager training programme, and cutting agency recruitment. Full reasoning in the deck.</div>
   </div></div>`
 + eyebrow("03","The two cuts that matter","sorted by score")
 + `<div class="grid2">
   <div class="panel"><h3>By legacy entity</h3>${miniTable(D.entities)}</div>
   <div class="panel"><h3>By department</h3>${miniTable(D.depts)}</div></div>`
 + eyebrow("04","How to read the score")
 + `<div class="panel"><div class="lede">The score is a <b>diagnostic, not a prediction</b>. It is
   three gaps against the company figure, each shown separately in the cohort table so you can audit
   it rather than trust it.</div>
   <table style="margin-top:12px"><thead><tr><th style="width:150px">Component</th>
    <th class="num" style="width:70px">Weight</th><th>What it measures</th></tr></thead><tbody>
    <tr><td><span class="pill" style="--bc:#5B0091">Response gap</span></td><td class="num">40%</td>
     <td>How far the cohort's survey response rate falls below the company's ${fmt(D.company.resp_rate)}%.</td></tr>
    <tr><td><span class="pill" style="--bc:#A100FF">Belief gap</span></td><td class="num">40%</td>
     <td>Senior leadership trust and purpose, averaged, against company means of
      ${fmt(D.company.trust,2)} and ${fmt(D.company.purpose,2)}.</td></tr>
    <tr><td><span class="pill" style="--bc:#C9A0F5">Attrition gap</span></td><td class="num">20%</td>
     <td>Annualised voluntary attrition above the company's ${fmt(D.company.attrition)}%/yr.</td></tr>
   </tbody></table>
   <div class="note">A high score means a cohort looks like Entity_B did <em>before</em> its attrition
   rose. It does not mean any individual in it is leaving. Weights are a judgement, not a finding:
   response and belief carry most of the weight because those are the two signals that separated
   Entity_B from Entity_A before attrition moved; attrition carries least because by the time it
   moves, the loss has already happened.</div>
   <div class="note"><b>The floor is disclosed, not hidden.</b> Cohorts with fewer than
   ${D.minResponses} survey responses publish no scores at all — ${D.totals.suppressed} of
   ${D.totals.cohorts} cohorts, ${D.totals.suppressedPeople} people. They stay visible as rows so you
   can see that something was withheld.</div></div>`;
}

function miniTable(rows){
 const s=[...rows].sort((a,b)=>(b.score??-1)-(a.score??-1));
 const max=Math.max(...s.map(r=>r.score||0),1);
 return `<div class="flat-t"><table><thead><tr><th>Cohort</th><th class="num">Active</th>
  <th class="num">Attrition</th><th class="num">Response</th><th>Score</th></tr></thead><tbody>
 ${s.map(r=>`<tr class="${r.suppressed?'sup':''}"><td class="ck">${esc(r.key)}</td>
  <td class="num">${r.headcount.toLocaleString()}</td><td class="num">${fmt(r.attrition)}%</td>
  <td class="num">${fmt(r.resp_rate)}%</td>
  <td>${r.suppressed
   ? `<span class="pill Suppressed">n&lt;${D.minResponses}</span>`
   : `<span class="pill ${r.bandName}">${fmt(r.score)}</span>
      <span style="display:inline-block;height:4px;border-radius:2px;vertical-align:2px;
       margin-left:7px;width:${Math.max(3,r.score/max*54)}px;background:${BAND[r.bandName]};opacity:.35"></span>`}
  </td></tr>`).join("")}</tbody></table></div>`;
}

function currentRows(){
 return D.cohorts.filter(c=>
  (filterEnt==="all"||c.parts[1]===filterEnt) &&
  (filterDept==="all"||c.parts[0]===filterDept) &&
  (filterBand==="all"||c.bandName===filterBand) &&
  (showSup||!c.suppressed) &&
  (q===""||c.key.toLowerCase().includes(q)));
}

function cohortsView(){
 const ents=[...new Set(D.cohorts.map(c=>c.parts[1]))].sort();
 const deps=[...new Set(D.cohorts.map(c=>c.parts[0]))].sort();
 let rows=currentRows();
 rows.sort((a,b)=>{const x=a[sortKey]??-1,y=b[sortKey]??-1;
  return typeof x==="string"?sortDir*x.localeCompare(y):sortDir*(x-y);});
 const th=(k,l,cls="")=>`<th class="s ${cls} ${sortKey===k?"act":""}" data-k="${k}">${l}<span class="ar">${
  sortKey===k?(sortDir<0?"↓":"↑"):"↓"}</span></th>`;
 const seg=(id,vals,active)=>`<div class="seg" id="${id}">${vals.map(v=>
  `<button data-v="${v[0]}" data-b="${v[0]}" class="${v[0]===active?"on":""}">${v[1]}</button>`).join("")}</div>`;

 return `<div class="filters">
  <div class="frow">
   <span class="fgroup"><span class="flab">Entity</span>
    ${seg("segEnt",[["all","All"],...ents.map(e=>[e,e])],filterEnt)}</span>
   <span class="fgroup"><span class="flab">Band</span>
    ${seg("segBand",[["all","All"],["Priority","Priority"],["Elevated","Elevated"],["Stable","Stable"]],filterBand)}</span>
  </div>
  <div class="frow">
   <span class="fgroup"><span class="flab">Department</span>
    <span class="sel"><select id="fd">${["all",...deps].map(e=>
     `<option ${e===filterDept?"selected":""}>${esc(e)}</option>`).join("")}</select></span></span>
   <span class="search">
    <svg width="13" height="13" viewBox="0 0 14 14" fill="none" aria-hidden="true">
     <circle cx="6" cy="6" r="4.4" stroke="#767684" stroke-width="1.4"/>
     <path d="M9.4 9.4 12.6 12.6" stroke="#767684" stroke-width="1.4" stroke-linecap="round"/></svg>
    <input type="search" id="q" placeholder="Find a cohort…" value="${esc(q)}">
    ${q?`<button class="x" id="qx" title="Clear">×</button>`:""}</span>
   <label class="tog"><input type="checkbox" id="sup" ${showSup?"checked":""}>
    <span class="tr"></span>Show suppressed</label>
   <span class="spacer"></span>
   <span class="count"><b>${rows.length}</b> of ${D.cohorts.length} cohorts</span>
   <button class="btn" id="csv">
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
     <path d="M6 1v7m0 0L3.4 5.6M6 8l2.6-2.4M1.6 10.4h8.8" stroke="currentColor"
      stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>Download CSV</button>
  </div></div>

 <div class="panel" style="margin-bottom:12px">${scatter(rows)}</div>

 <div class="tw"><table><thead><tr>
  ${th("key","Department · Entity · Level")}${th("headcount","Active","num")}
  ${th("n_resp","Resp.","num")}${th("attrition","Attrition %/yr","num")}
  ${th("resp_rate","Response %","num")}${th("trust","Trust","num")}${th("purpose","Purpose","num")}
  <th>Score composition</th>${th("score","Score","num")}</tr></thead><tbody>
 ${rows.map(r=>r.suppressed
  ? `<tr class="sup"><td class="ck">${esc(r.key)}</td><td class="num">${r.headcount}</td>
     <td class="num">${r.n_resp}</td>
     <td colspan="5" style="font-style:italic">Suppressed — fewer than ${D.minResponses} responses</td>
     <td class="num"><span class="pill Suppressed">n&lt;${D.minResponses}</span></td></tr>`
  : `<tr><td class="ck">${esc(r.key)}</td><td class="num">${r.headcount.toLocaleString()}</td>
     <td class="num">${r.n_resp}</td><td class="num">${fmt(r.attrition)}</td>
     <td class="num">${fmt(r.resp_rate)}</td><td class="num">${fmt(r.trust,2)}</td>
     <td class="num">${fmt(r.purpose,2)}</td><td>${compBar(r)}</td>
     <td class="num"><span class="pill ${r.bandName}">${fmt(r.score)}</span></td></tr>`).join("")}
 </tbody></table></div>
 <div class="legend" style="margin:10px 0 0">
  ${COMP.map(([k,lab,col])=>`<span><i style="background:${col}"></i>${lab}</span>`).join("")}
  <span style="color:var(--mut)">Segment widths are the weighted contributions, so they add to the
  score. Click any column header to sort.</span></div>`;
}

function entity(){
 const rows=D.entities.filter(e=>!e.suppressed).sort((a,b)=>b.score-a.score);
 const order=dimOrderGlobal();
 const dom=Math.max(...rows.flatMap(e=>order.map(k=>Math.abs(e.dims[k]-D.companyDims[k]))))*1.15;
 return rows.map((e,i)=>{
  const dAtt=e.attrition-D.company.attrition, dRes=e.resp_rate-D.company.resp_rate;
  return eyebrow(String(i+1).padStart(2,"0"),e.key,
   `<span class="pill ${e.bandName}">${e.bandName} · score ${fmt(e.score)}</span>`)
  + rail([
   ["Headcount",e.headcount.toLocaleString(),"active"],
   ["Voluntary attrition",fmt(e.attrition)+"%/yr","company "+fmt(D.company.attrition)+"%",
    [(dAtt>=0?"+":"−")+Math.abs(dAtt).toFixed(1)+" pts vs company", dAtt>0.2?"up":(dAtt<-0.2?"dn":"flat")]],
   ["Survey response",fmt(e.resp_rate)+"%","company "+fmt(D.company.resp_rate)+"%",
    [(dRes>=0?"+":"−")+Math.abs(dRes).toFixed(1)+" pts vs company", dRes<-0.2?"up":(dRes>0.2?"dn":"flat")]],
   ["High-value loss","$"+fmt(e.cost)+"M","replacement cost per year"],
   ["Respondents",e.n_resp.toLocaleString(),"active staff who answered"],
  ])
  + `<div class="gridA" style="margin-top:12px">
     <div class="panel"><h3>Engagement against the company average</h3>
      ${deviation(e,order,dom)}
      <div class="note">Distance from the company mean on each dimension, on the same scale for every
      entity and in the same row order, so the panels read against each other. Absolute scores on a
      1–5 scale look alike across entities — the distance from the average is where the difference
      lives.</div></div>
     <div class="panel"><h3>The same figures, as numbers</h3>${dimTable(e,order)}
      <div class="note">Nothing in the chart is only reachable by hovering it.</div></div>
     </div>`;
 }).join("");
}

// Every chart in this file has a table twin. This is the deviation chart's.
function dimTable(e,order){
 return `<div class="flat-t"><table><thead><tr><th>Dimension</th>
  <th class="num">${esc(e.key)}</th><th class="num">Company</th>
  <th class="num">Difference</th></tr></thead><tbody>
  ${order.map(k=>{const d=e.dims[k]-D.companyDims[k];
   return `<tr><td class="ck">${dimLab(k)}</td><td class="num">${fmt(e.dims[k],2)}</td>
   <td class="num">${fmt(D.companyDims[k],2)}</td>
   <td class="num"><span class="dot" style="background:${dimCol(d)}"></span>${sign(d)}</td></tr>`;
  }).join("")}</tbody></table></div>`;
}

function whatif(){
 const p=20;
 return eyebrow("01","What is it worth if you act?")
 + `<div class="panel">
  <div class="callout"><b>The reduction rate is an assumption, not a finding.</b> 20–40% is the band
  typically claimed for targeted retention programmes. Nothing here estimates how effective any
  specific intervention would be — it shows what a given reduction would be worth if achieved.</div>
  <div class="gridA" style="align-items:start">
   <div>
    <div style="font-size:11.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--mut)">
     Reduction in high-value voluntary attrition</div>
    <div class="range"><input type="range" id="sl" min="0" max="50" value="${p}" step="1"
     style="--fill:${p/50*100}%" aria-label="Reduction in high-value voluntary attrition"></div>
    <div style="display:flex;align-items:baseline;gap:10px;margin:10px 0 2px">
     <span class="hero" id="sv">$${(D.addressable*p/100).toFixed(1)}M</span>
     <span style="color:var(--mut);font-size:12.5px">per year, from <b id="pc">${p}</b>% of the
     $${D.addressable.toFixed(1)}M addressable base</span></div>
    <div class="flat-t" style="margin-top:14px"><table><thead><tr><th>Reduction</th>
     <th class="num">Value per year</th><th>Comparable</th></tr></thead><tbody>
     ${[10,20,30,40].map(x=>`<tr><td class="ck">${x}%</td>
      <td class="num ck">$${(D.addressable*x/100).toFixed(1)}M</td>
      <td style="color:var(--mut)">${x===20?"lower bound typically claimed":x===40?"upper bound typically claimed":""}</td>
     </tr>`).join("")}</tbody></table></div>
   </div>
   <div id="wchart">${whatifChart(p)}</div>
  </div>
  <div class="note">Addressable base is $${D.addressable.toFixed(1)}M — the replacement cost of
  voluntary high-value attrition on the brief's own constants (1.5× salary, 85% backfill, 12% super),
  from <code>cost_model.py</code>. Redefining the regrettable flag costs about $0, so its return is
  not capped by budget.</div></div>`;
}

function fairness(){
 return eyebrow("01","Why this tool has no individual scores")
 + `<div class="panel"><div class="lede" style="margin-bottom:14px">We built the obvious version — a
  flight-risk flag on survey silence, scored per employee — tested it, and did not ship it. It fails
  the four-fifths rule on three dimensions at once, and it is wrong most of the time.</div>
  ${fairnessChart()}
  <div class="flat-t" style="margin-top:14px"><table><thead><tr><th>Dimension</th>
   <th class="num">Impact ratio</th><th>Detail</th><th class="num">n</th><th>Verdict</th></tr></thead><tbody>
  ${D.fairness.map(f=>`<tr><td class="ck">${esc(f.dim)}</td>
   <td class="num"><span class="pill Priority">${f.ratio.toFixed(2)}</span></td>
   <td>${esc(f.detail)}</td><td class="num">${esc(f.n)}</td><td>${esc(f.verdict)}</td></tr>`).join("")}
  </tbody></table></div></div>`
 + eyebrow("02","And it is wrong most of the time")
 + `<div class="grid2">
  <div class="panel">
   ${rail([["Flagged & left","263","true positives"],["Flagged & stayed","901","false positives"],
     ["Precision","22.6%","roughly three wrong in four"]])}
   <div class="note">The dominant outcome of deploying this per-person is a career conversation about
   someone who was never leaving. Low response is heavily concentrated in the acquisition cohorts, so
   at individual level the flag would substantially be measuring <b>integration failure</b>, not intent.</div></div>
  <div class="panel"><h3>What we built instead</h3>
   <div>Cohort level only, a minimum of ${D.minResponses} responses, suppressed cohorts labelled
   rather than dropped, and the score split into its three components. The file itself carries no
   employee ID, no name and no manager ID — aggregation happens in Python before the file is written,
   so there is no drill-down to disable.</div>
   <div class="note">If a participation metric is ever used, staff should be told it exists. A survey
   sold as confidential and quietly re-used as a personal risk score costs you the instrument once
   people work it out.</div></div></div>`;
}

/* ---------------------------------------------------------------- wiring */
const views={overview,cohorts:cohortsView,entity,whatif,fairness};

function render(){
 const v=$("#view");
 tipEl().style.opacity=0;      // the element it was anchored to is about to go
 v.innerHTML=views[cur]();
 bindTips(v);

 v.querySelectorAll("th[data-k]").forEach(th=>th.onclick=()=>{
  const k=th.dataset.k; if(sortKey===k)sortDir*=-1; else{sortKey=k;sortDir=-1;} render();});

 const segEnt=$("#segEnt"), segBand=$("#segBand");
 if(segEnt)segEnt.onclick=e=>{const b=e.target.closest("button");
  if(b){filterEnt=b.dataset.v;render();}};
 if(segBand)segBand.onclick=e=>{const b=e.target.closest("button");
  if(b){filterBand=b.dataset.v;render();}};
 const fd=$("#fd"); if(fd)fd.onchange=e=>{filterDept=e.target.value;render()};
 const sup=$("#sup"); if(sup)sup.onchange=e=>{showSup=e.target.checked;render()};
 const qx=$("#qx"); if(qx)qx.onclick=()=>{q="";render();$("#q")&&$("#q").focus()};

 // render() replaces the whole view, so the input the user is typing into is
 // destroyed and rebuilt on every keystroke. Restoring focus alone puts the
 // caret back at position 0, so the selection offset is carried over too or
 // typing runs backwards.
 const qq=$("#q");
 if(qq)qq.oninput=e=>{
  const pos=e.target.selectionStart;
  q=e.target.value.toLowerCase();
  render();
  const n=$("#q");
  if(n){n.focus(); n.setSelectionRange(pos,pos);}
 };

 const sl=$("#sl");
 if(sl)sl.oninput=e=>{
  const p=+e.target.value;
  e.target.style.setProperty("--fill",p/50*100+"%");
  $("#sv").textContent="$"+(D.addressable*p/100).toFixed(1)+"M";
  $("#pc").textContent=p;
  $("#wchart").innerHTML=whatifChart(p);
  bindTips($("#wchart"));
 };

 const cs=$("#csv");
 if(cs)cs.onclick=()=>{
  // Exports exactly what is on screen, suppressed cohorts included as
  // suppressed. No identifiers exist to export.
  const rows=currentRows();
  const head=["department","entity","level","active","respondents","attrition_pct_yr",
              "response_pct","trust","purpose","response_gap","belief_gap","attrition_gap",
              "score","band"];
  const q2=v=>`"${String(v??"").replace(/"/g,'""')}"`;
  const body=rows.map(r=>[r.parts[0],r.parts[1],r.parts[2],r.headcount,r.n_resp,
   r.attrition,r.resp_rate,r.trust,r.purpose,
   r.comp?r.comp.response:"",r.comp?r.comp.belief:"",r.comp?r.comp.attrition:"",
   r.score,r.bandName].map(q2).join(","));
  const blob=new Blob([[head.join(","),...body].join("\\n")],{type:"text/csv"});
  const a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="novacorp_cohort_diagnostic.csv"; a.click();
  URL.revokeObjectURL(a.href);
 };
}

function go(name){
 if(!views[name]) return;
 cur=name; sortKey="score"; sortDir=-1;
 document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("on",x.dataset.v===name));
 render();
 if(scrollY>0) scrollTo({top:0,behavior:"smooth"});
}
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>go(t.dataset.v));
addEventListener("keydown",e=>{
 if(e.metaKey||e.ctrlKey||e.altKey) return;
 if(/^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement.tagName)) return;
 const tabs=[...document.querySelectorAll(".tab")];
 const i=+e.key-1;
 if(i>=0&&i<tabs.length) go(tabs[i].dataset.v);
});
addEventListener("scroll",()=>{
 $("#topbar").classList.toggle("stuck",scrollY>4);
},{passive:true});
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
print(f"     gap: flag {counted['flagN']} exits ${counted['flagCost']}M -> "
      f"value-based {counted['hvN']} exits ${counted['hvCost']}M "
      f"({counted['missedN']} missed, ${counted['gapCost']}M)")
for e in sorted(entities, key=lambda x: -(x["score"] or 0)):
    print(f"     {e['key']:<18} score {e['score']:>5}  {e['bandName']}")
print("     no employee_id, name or manager_id in output")
