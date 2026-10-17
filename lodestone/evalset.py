"""Score quality check (P1-S5, ENG_DESIGN §9, R7). Two checks, both re-run whenever the scoring rules change:

1. Ranking: does Lodestone rank the roles the user marked Interested above the ones marked Later or Not for me?
   Uses the app's own fit formula (same weights, freshness, pay targets and work-permit routes as the app), so the
   numbers match what the user sees.
     python3 -m lodestone eval ranking <triage folder> [--prefs <file>] [--profile <file>]
2. Reading: does Lodestone read postings correctly (pay, level, people management, location)? Compared with a
   hand-checked set in data/eval/reading_gold.json.
     python3 -m lodestone eval reading

Results append to data/state/eval_history.json; `export` puts the latest into the app (meta/eval).
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

from . import rules
from . import scoring, store

GOLD = store.ROOT / "data" / "eval" / "reading_gold.json"
SUBS = ["role", "level", "domain", "pathway", "pay", "skills", "freshness"]
DEFAULT_W = {"role": 22, "level": 18, "domain": 18, "pathway": 14, "pay": 9, "skills": 9, "freshness": 10}
DEFAULT_CHECKS = {"pay_green": 190000, "pay_yellow": 160000}
LABEL = {"interested": 1.0, "later": 0.5, "not": 0.0}
DAY = 86400.0


# ---------- the app's fit formula, in Python ----------
def _when(v, base=None):
    if v in (None, ""):
        return None
    s = str(v).strip()
    if re.fullmatch(r"\d{9,13}", s):
        n = int(s)
        return n / 1000 if n > 1e12 else n
    m = re.search(r"posted\s+(today|yesterday|(\d+)\+?\s+days?\s+ago)", s, re.I)
    if m:
        d = 0 if m.group(1).lower() == "today" else 1 if m.group(1).lower() == "yesterday" else int(m.group(2))
        return (base or dt.datetime.now(dt.timezone.utc).timestamp()) - d * DAY
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d", "%B %d, %Y"):
        try:
            t = dt.datetime.strptime(s.replace("Z", "+00:00") if "T" in s else s, fmt)
            return (t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)).timestamp()
        except ValueError:
            continue
    return None


def freshness(j, now):
    posted = _when(j.get("posted_at"), _when(j.get("last_seen")))
    ms = posted if posted is not None else _when(j.get("first_seen"))
    if ms is None:
        return 50
    d = max(0, round((now - ms) / DAY))
    v = 100 if d <= 14 else 85 if d <= 30 else 60 if d <= 45 else 30 if d <= 60 else 15 if d <= 90 else 5
    return min(v, 70) if posted is None else v


def _co(x):
    x = re.sub(r"\b(inc|ltd|llc|corp|corporation|company|co|ulc|canada)\b", "", str(x or "").lower().replace("&", " and "))
    return re.sub(r"[^a-z0-9]", "", x)


def pathway(j, profile):
    base = j.get("pathway") or {"score": 45, "signals": []}
    profile = profile or {}
    if profile.get("work_status") == "open_permit":
        lim = next((s for s in base["signals"] if s["label"].startswith("Posting limits")), None)
        return 15 if lim and re.search(r"citizen|permanent resident|clearance", lim.get("detail") or "", re.I) else 95
    emp = ((profile.get("current") or {}).get("employer") or "").strip()
    if emp and _co(emp) and _co(emp) == _co(j["company"]):
        return 95
    return base["score"]


def _pay_score(top, kind, checks):
    g, y = checks["pay_green"], checks["pay_yellow"]
    v = 95 if top >= g * 1.2 else 80 if top >= g else 60 if top >= y else 40 if top >= y * 0.8 else 20
    return v if kind in ("base", "unspecified", None) else max(20, v - 10)


def _role_from_types(j, prefs):
    """Same as the app (D-077): once Claude has read a job's type scores, the role factor is its relevance to you."""
    from . import affinity
    if j.get("aff_src") != "read" or not j.get("aff"):
        return None
    prefs = prefs or {}
    mine = prefs.get("families") or rules.default_families()
    return round(affinity.relevance(j["aff"], mine, prefs.get("families_shown"))[0])


def _avoid_hit(j, prefs, checks):
    avoid = (prefs or {}).get("avoid_types") or []
    if not avoid:
        return False
    types = json.loads((store.ROOT / "config" / "company_types.json").read_text())["types"]
    if not any(j.get("company") in types.get(t, {}).get("companies", []) for t in avoid):
        return False
    p = j.get("pay") or {}
    m = p["ranges"][p["primary"]] if p.get("ranges") and p.get("primary") is not None else None
    return not (m and m.get("max") and m.get("currency") != "USD" and m["max"] >= checks["pay_green"])


def sub(j, k, now, checks, profile, prefs=None):
    if k == "role" and (v := _role_from_types(j, prefs)) is not None:
        return float(v)
    if k == "domain" and _avoid_hit(j, prefs, checks):
        return float(min(35, ((j.get("fit") or {}).get("subs") or {}).get("domain") or 35))
    if k == "freshness":
        return freshness(j, now)
    if k == "pathway":
        return pathway(j, profile)
    if k == "pay":
        p = j.get("pay") or {}
        m = p["ranges"][p["primary"]] if p.get("ranges") and p.get("primary") is not None else None
        if m and m.get("max") and m.get("currency") != "USD":
            return _pay_score(m["max"] * 2000 if m.get("interval") == "hour" else m["max"], m.get("kind"), checks)
        if (p.get("estimate") or {}).get("max"):
            return min(_pay_score(p["estimate"]["max"], "base", checks), 75)
    return float(((j.get("fit") or {}).get("subs") or {}).get(k) or 0)


def fit(j, prefs=None, profile=None, now=None):
    if not (j.get("fit") or {}).get("subs"):
        return None
    prefs = prefs or {}
    W = {**DEFAULT_W, **(prefs.get("weights") or {})}
    checks = {**DEFAULT_CHECKS, **(prefs.get("checks") or {})}
    now = now or dt.datetime.now(dt.timezone.utc).timestamp()
    t = sum(W[k] for k in SUBS)
    return round(sum(W[k] * sub(j, k, now, checks, profile, prefs) for k in SUBS) / t) if t else None


# ---------- 1. ranking ----------
def _load_dir(folder) -> dict[str, dict]:
    out = {}
    for f in Path(folder).rglob("*.json"):
        d = json.loads(f.read_text())
        out[f.stem] = d.get("data", d) if isinstance(d, dict) else {}
    return out


def _app_jobs() -> dict[str, dict]:
    jobs = {}
    for f in (store.STATE / "app_export" / "jobs").glob("*.json"):
        jobs.update(json.loads(f.read_text())["jobs"])
    return jobs


def ranking(triage: dict[str, dict], jobs: dict[str, dict], prefs=None, profile=None, now=None) -> dict:
    scored = {i: fit(j, prefs, profile, now) for i, j in jobs.items() if j.get("live")}
    scored = {i: s for i, s in scored.items() if s is not None}
    order = sorted(scored, key=lambda i: -scored[i])
    rank = {i: n + 1 for n, i in enumerate(order)}
    lab = {i: LABEL[t["status"]] for i, t in triage.items() if t.get("status") in LABEL and i in scored}
    pos = [i for i, v in lab.items() if v == 1.0]
    neg = [i for i, v in lab.items() if v < 1.0]
    pairs = [(p, n) for p in pos for n in neg]
    pairwise = sum(1.0 if scored[p] > scored[n] else 0.5 if scored[p] == scored[n] else 0.0 for p, n in pairs) / len(pairs) if pairs else None
    top10 = [i for i in order[:10] if i in lab]
    mean = lambda xs: round(sum(xs) / len(xs), 1) if xs else None
    return {
        "labels": {"interested": len(pos), "later": sum(1 for v in lab.values() if v == 0.5), "not": sum(1 for v in lab.values() if v == 0.0)},
        "pairwise": round(pairwise, 3) if pairwise is not None else None,
        "interested_in_top25": sum(1 for i in pos if rank[i] <= 25),
        "precision_at_10": round(sum(lab[i] == 1.0 for i in top10) / len(top10), 2) if top10 else None,
        "labelled_in_top10": len(top10),
        "mean_fit": {"interested": mean([scored[i] for i in pos]),
                     "later": mean([scored[i] for i, v in lab.items() if v == 0.5]),
                     "not": mean([scored[i] for i, v in lab.items() if v == 0.0])},
        "roles_ranked": len(order),
        "misses": [{"id": i, "title": jobs[i]["title"], "company": jobs[i]["company"], "rank": rank[i], "fit": scored[i]}
                   for i in sorted(pos, key=lambda i: rank[i]) if rank[i] > 25][:5],
        "enough_labels": len(pos) >= 10 and len(neg) >= 10,
    }


# ---------- 1b. role types (D-077) ----------
def types() -> dict:
    """Top type score vs the hand-checked main type (data/eval/type_gold.json), and the title guess for comparison."""
    from .appexport import job_id
    gold = json.loads((store.ROOT / "data" / "eval" / "type_gold.json").read_text())["postings"]
    jobs = {job_id(k): j for k, j in store.load("jobs", {"jobs": {}})["jobs"].items()}
    aff = store.load("affinity", {})
    read = [g for g in gold if (aff.get(g["id"]) or {}).get("aff")]
    top = lambda a: max(a, key=a.get)
    ok_read = [g for g in read if top(aff[g["id"]]["aff"]) in g["main"]]
    ok_title = [g for g in gold if (jobs.get(g["id"]) or {}).get("role_family") in g["main"]]
    pct = lambda a, b: round(len(a) / len(b), 3) if b else None
    return {"postings": len(gold), "read": len(read), "type_scores_accuracy": pct(ok_read, read), "title_guess_accuracy": pct(ok_title, gold),
            "misses": [{"title": g["title"], "company": g["company"], "main": g["main"], "got": top(aff[g["id"]]["aff"])}
                       for g in read if g not in ok_read][:5]}


# ---------- 2. reading ----------
def reading() -> dict:
    """Compare what Lodestone read from each hand-checked posting with the gold answer."""
    gold = json.loads(GOLD.read_text())["postings"] if GOLD.exists() else []
    from .appexport import job_id
    jobs = {job_id(k): j for k, j in store.load("jobs", {"jobs": {}})["jobs"].items()}
    scores = store.load("scores", {})
    from .experience import years_required
    fields = {"pay": [0, 0], "pay_kind": [0, 0], "region": [0, 0], "people_mgmt": [0, 0], "level": [0, 0], "years": [0, 0], "excluded": [0, 0]}
    errors = []
    for g in gold:
        j = jobs.get(g["id"])
        if not j:
            continue
        p = j.get("pay") or {}
        m = p["ranges"][p["primary"]] if p.get("ranges") and p.get("primary") is not None else None
        got = {"pay": [m["min"], m["max"], m.get("currency")] if m else None, "pay_kind": (m or {}).get("kind"),
               "region": j.get("region"), "people_mgmt": (scores.get(g["id"]) or {}).get("people_mgmt"),
               "level": _lv((scores.get(g["id"]) or {}).get("level_guess")),
               "years": (years_required(j.get("description") or "") or {}).get("min"),
               "excluded": bool(j.get("role_excluded"))}
        for f in fields:
            if f not in g:
                continue
            fields[f][1] += 1
            ok = got[f] == g[f] if f != "level" else (g[f] is None or (got[f] is not None and abs(got[f] - g[f]) <= 0.5))
            fields[f][0] += ok
            if not ok:
                errors.append({"id": g["id"], "field": f, "expected": g[f], "got": got[f], "title": j["title"], "company": j["company"]})
    acc = {f: round(a / n, 2) if n else None for f, (a, n) in fields.items()}
    return {"postings": len(gold), "accuracy": acc, "errors": errors}


def _lv(guess):
    ns = [int(x) for x in re.findall(r"L(\d)", guess or "")]
    return sum(ns) / len(ns) if ns else None


def record(kind: str, result: dict) -> dict:
    hist = store.load("eval_history", {"runs": []})
    entry = {"at": store.now(), "kind": kind, "rubric": scoring.config()["rubric_version"], **result}
    hist["runs"].append(entry)
    hist["runs"] = hist["runs"][-200:]
    store.save("eval_history", hist)
    return entry
