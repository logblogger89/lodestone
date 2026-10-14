"""Sprint 1 pipeline: detect each company's job system, then refresh.

refresh = pull every feed -> keep Canada -> role rules -> dedup -> liveness -> candidates to score.
"""
from __future__ import annotations

import concurrent.futures as cf
from collections import Counter

from . import dedup, store
from .adapters import ADAPTERS, DETECT_ORDER
from .geo import classify
from .models import Company
from .rules import classify_title
from .text import slug_candidates

WORKERS = 8
MISSES_BEFORE_DEAD = 2          # missing from 2 successful pulls in a row -> "no longer live" (F25)


# ---------- detection ----------

def _detect_one(name: str) -> tuple[str | None, str | None, str]:
    """Try likely slugs on each job system; accept only a board that has jobs.

    Returns (ats, slug, confidence). A match on just the first word of a multi-word name
    ("royal" for "Royal Bank of Canada") is marked low confidence for review.
    """
    for slug in slug_candidates(name):
        for ats in DETECT_ORDER:
            try:
                n = ADAPTERS[ats].exists(slug)
            except Exception:
                n = None
            if n:
                return ats, slug, _confidence(name, slug)
    return None, None, "none"


def _confidence(name: str, slug: str | None) -> str:
    """High only when the board name is the full company name ("canadalife"), not a shortened
    form ("life" for "Canada Life", "air" for "Air Canada"), which may be a different company."""
    if not slug:
        return "none"
    return "high" if slug in slug_candidates(name)[:2] else "low"


def detect(redo: bool = False, log=print) -> dict:
    seed = store.read_seed()
    overrides = store.read_overrides()
    known = {c["name"]: c for c in store.load("companies", {"companies": []})["companies"]}
    todo, companies = [], []
    for row in seed:
        if "not employers" in row.get("segment", "").lower() or row.get("discovery_source") == "discovery":
            continue          # discovery orgs (VCs, accelerators) are sources of companies, not employers
        c = Company(name=row["company"].strip(), segment=row.get("segment", ""),
                    canada_locations=row.get("canada_locations", ""), fit_tier=row.get("fit_tier", ""),
                    why_relevant=row.get("why_relevant", ""), discovery_source=row.get("discovery_source", ""))
        d = c.to_dict()
        prev = known.get(c.name)
        if c.name in overrides:
            o = overrides[c.name]
            d.update(ats=None if o["ats"] == "none" else o["ats"], slug=o["slug"],
                     ats_checked_at=store.now(), confidence="override")
        elif prev and not redo and prev.get("ats_checked_at"):
            d.update({k: prev.get(k) for k in ("ats", "slug", "ats_checked_at", "status")})
            d["confidence"] = _confidence(c.name, d["slug"])
        else:
            todo.append(d)
        companies.append(d)
    log(f"Detecting job systems for {len(todo)} companies ({len(companies) - len(todo)} already known)...")
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        futs = {ex.submit(_detect_one, d["name"]): d for d in todo}
        for f in cf.as_completed(futs):
            d = futs[f]
            d["ats"], d["slug"], d["confidence"] = f.result()
            d["ats_checked_at"] = store.now()
    store.save("companies", {"updated_at": store.now(), "companies": companies})
    found = Counter(d["ats"] or "none" for d in companies)
    store.mark_fresh("ats_detection", companies=len(companies), matched=len(companies) - found["none"])
    return {"companies": len(companies), "by_ats": dict(found),
            "low_confidence": [d["name"] for d in companies if d.get("confidence") == "low"]}


# ---------- refresh ----------

def _pull(d: dict):
    try:
        return d, ADAPTERS[d["ats"]].list_jobs(d["name"], d["slug"]), None
    except Exception as e:  # one broken feed never stops the run
        return d, [], f"{type(e).__name__}: {e}"


def refresh(log=print) -> dict:
    companies = [d for d in store.load("companies", {"companies": []})["companies"]
                 if d.get("ats") and d.get("slug") and d.get("status", "active") == "active"]
    if not companies:
        raise SystemExit("No companies with a detected job system. Run: python3 -m lodestone detect")
    jobs: dict = store.load("jobs", {"jobs": {}})["jobs"]
    seen_at = store.now()
    stats = Counter()
    errors, per_source = {}, Counter()
    ok_companies, seen_keys = set(), set()

    log(f"Pulling {len(companies)} job feeds...")
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        results = list(ex.map(_pull, companies))

    for d, postings, err in results:
        if err:
            errors[d["name"]] = err
            continue
        ok_companies.add(d["name"])
        per_source[d["ats"]] += len(postings)
        stats["pulled"] += len(postings)
        for p in postings:
            geo = classify(p)
            if not geo.in_canada:
                continue
            stats["canada"] += 1
            role = classify_title(p.title)
            rec = {
                "key": p.canonical_key, "source": p.source, "url": p.url, "seen_at": seen_at,
                "group": dedup.group_key(p.company, p.title, geo.region),
                "company": p.company, "title": p.title, "location": p.location_raw,
                "region": geo.region, "remote": geo.remote, "cec_credit": geo.cec_credit,
                "workplace": p.workplace, "department": p.department, "posted_at": p.posted_at,
                "pay": p.pay, "pay_posted": bool(p.pay),
                "role_tier": role.tier, "role_excluded": role.excluded,
                "people_mgmt_hint": role.people_mgmt_hint, "role_reason": role.reason,
                "description": p.description if (role.tier and not role.excluded) else "",
                "detail_api": p.extra.get("detail_api"),
            }
            before = len(jobs)
            jid = dedup.merge(jobs, rec)
            seen_keys.add(p.canonical_key)
            job = jobs[jid]
            if len(jobs) > before:
                job["first_seen"] = seen_at
                stats["new"] += 1
            # refresh fields that can change on the source
            for k in ("title", "location", "pay", "pay_posted", "role_tier", "role_excluded",
                      "people_mgmt_hint", "role_reason", "workplace", "posted_at"):
                job[k] = rec[k]
            if rec["description"]:
                job["description"] = rec["description"]
            for s in job["sightings"]:
                if s["key"] == p.canonical_key:
                    s.update(last_seen=seen_at, live=True, missed_runs=0, url=p.url)

    # Liveness: only count a miss when that company's feed was pulled successfully this run.
    for job in jobs.values():
        for s in job["sightings"]:
            if s["key"] in seen_keys:
                continue
            company_ok = job["company"] in ok_companies
            if company_ok:
                s["missed_runs"] = s.get("missed_runs", 0) + 1
                if s["missed_runs"] >= MISSES_BEFORE_DEAD:
                    s["live"] = False
        was_live = job.get("live", True)
        job["live"] = any(s["live"] for s in job["sightings"])
        job["last_seen"] = max(s["last_seen"] for s in job["sightings"])
        if was_live and not job["live"]:
            job["closed_at"] = seen_at
            stats["went_dead"] += 1

    candidates = [
        {"id": jid, **{k: j[k] for k in ("company", "title", "location", "region", "role_tier",
                                          "people_mgmt_hint", "pay", "first_seen")},
         "sources": [s["source"] for s in j["sightings"]], "urls": [s["url"] for s in j["sightings"]]}
        for jid, j in jobs.items()
        if j["live"] and j["role_tier"] and not j["role_excluded"]
    ]
    tier_rank = {"Core": 0, "Adjacent": 1, "Stretch": 2}
    candidates.sort(key=lambda c: (tier_rank.get(c["role_tier"], 9), c["company"], c["title"]))

    store.save("jobs", {"updated_at": seen_at, "jobs": jobs})
    store.save("candidates_to_score", {"updated_at": seen_at, "count": len(candidates), "candidates": candidates})
    for src, n in per_source.items():
        store.mark_fresh(f"jobs:{src}", postings=n)
    summary = {
        "feeds_ok": len(ok_companies), "feeds_failed": len(errors), "postings_pulled": stats["pulled"],
        "canada_postings": stats["canada"], "canada_jobs_tracked": sum(1 for j in jobs.values() if j["live"]),
        "new_jobs": stats["new"], "went_dead": stats["went_dead"],
        "multi_source_jobs": sum(1 for j in jobs.values() if len(j["sightings"]) > 1),
        "candidates": len(candidates), "by_tier": dict(Counter(c["role_tier"] for c in candidates)),
        "by_region": dict(Counter(c["region"] for c in candidates)), "errors": errors,
    }
    store.mark_fresh("jobs", **{k: summary[k] for k in ("feeds_ok", "feeds_failed", "canada_jobs_tracked", "candidates")})
    return summary


def stats() -> dict:
    comps = store.load("companies", {"companies": []})["companies"]
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    live = [j for j in jobs.values() if j.get("live")]
    cands = [j for j in live if j.get("role_tier") and not j.get("role_excluded")]
    return {
        "companies": len(comps), "by_ats": dict(Counter(c.get("ats") or "none" for c in comps)),
        "jobs_live": len(live), "candidates": len(cands),
        "by_tier": dict(Counter(j["role_tier"] for j in cands)),
        "by_region": dict(Counter(j["region"] for j in cands)),
        "freshness": store.load("runs", {"components": {}})["components"],
    }
