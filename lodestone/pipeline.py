"""Sprint 1 pipeline: detect each company's job system, then refresh.

refresh = pull every feed -> keep Canada -> role rules -> dedup -> liveness -> candidates to score.
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import re
from collections import Counter

from . import adapters, dedup, pagereader, pay, sources, store
from .adapters import ADAPTERS, DETECT_ORDER
from .geo import classify
from .rules import classify_title
from .text import slug_candidates

WORKERS = 8
MISSES_BEFORE_DEAD = 2          # missing from 2 successful pulls in a row -> "no longer live" (F25)
_MULTI = re.compile(r"^\d+ locations?$", re.I)


# ---------- detection ----------

def _detect_one(name: str) -> tuple[str | None, str | None, str]:
    """Try likely slugs on each hosted job board; accept only a board that has jobs."""
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


def employers() -> list[dict]:
    """Seed watchlist minus discovery orgs (VCs, accelerators): those are sources of companies."""
    return [r for r in store.read_seed()
            if "not employers" not in r.get("segment", "").lower() and r.get("discovery_source") != "discovery"]


def detect(redo: bool = False, log=print) -> dict:
    """Auto-detect hosted job boards for companies that have no row in the source index yet."""
    rows = sources.load()
    have = sources.by_company(rows)
    names = [r["company"].strip() for r in employers()]
    todo = [n for n in names if redo or n not in have]
    if redo:
        rows = [r for r in rows if r.get("found_by") != "auto-detect"]
    log(f"Auto-detecting job boards for {len(todo)} companies ({len(names) - len(todo)} already indexed)...")
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        for name, (ats, slug, conf) in zip(todo, ex.map(_detect_one, todo)):
            if not ats:
                continue          # left for research: it will get a careers-site row or a no_feed row
            rows.append({"company": name, "platform": ats, "feed": {"slug": slug},
                         "status": "active" if conf == "high" else "paused", "verified_at": store.now()[:10],
                         "found_by": "auto-detect",
                         "notes": "" if conf == "high" else "matched on a shortened name: confirm before activating"})
    sources.save(rows)
    have = sources.by_company(rows)
    missing = [n for n in names if n not in have]
    store.mark_fresh("source_index", companies=len(names), indexed=len(names) - len(missing))
    return {"companies": len(names), "indexed": len(names) - len(missing),
            "active_sources": sum(1 for r in rows if r["status"] == "active"),
            "by_platform": dict(Counter(r["platform"] for r in rows if r["status"] == "active")),
            "not_indexed": missing}


# ---------- refresh ----------

def _pull(row: dict):
    try:
        return row, adapters.pull(row["platform"], row["company"], row["feed"]), None
    except Exception as e:  # one broken feed never stops the run
        return row, [], f"{type(e).__name__}: {e}"[:300]


def _low_hourly(p: dict | None) -> bool:
    """A Canadian hourly rate below the config threshold (retail and support jobs with product-sounding titles)."""
    limit = json.loads((store.ROOT / "config" / "role_taxonomy.json").read_text()).get("exclude_hourly_below_cad")
    if not (p and limit and p.get("primary") is not None):
        return False
    r = p["ranges"][p["primary"]]
    return r.get("interval") == "hour" and r.get("currency") != "USD" and (r.get("max") or 0) < limit


def _is_candidate(role) -> bool:
    return bool(role.tier) and not role.excluded


def _enrich(p, jobs: dict):
    """Fetch the full posting when the list view has no description, once per job: the adapter's own
    detail call (Workday, Eightfold, Oracle), else the posting page itself."""
    a = ADAPTERS[p.source]
    if p.description:
        return p, None
    known = jobs.get(p.canonical_key)
    if known and len(known.get("description") or "") > 600 and not pagereader.is_bot_check(known["description"]):
        p.description, p.location_raw = known["description"], known.get("location") or p.location_raw
        return p, None
    try:
        if hasattr(a, "detail"):
            d = a.detail(p)
        else:
            d = {"description": pagereader.posting_text(p.url, p.source)}
    except Exception as e:
        return p, f"{type(e).__name__}: {e}"[:200]
    p.description = d.get("description") or ""
    p.location_raw = d.get("location_raw") or p.location_raw
    p.posted_at = d.get("posted_at") or p.posted_at
    return p, None


def refresh(only: str | None = None, log=print) -> dict:
    rows = sources.load()
    active = [r for r in rows if r["status"] == "active" and (not only or r["company"] == only or r["platform"] == only)]
    if not active:
        raise SystemExit("No active sources. Run: python3 -m lodestone detect")
    jobs: dict = store.load("jobs", {"jobs": {}})["jobs"]
    seen_at = store.now()
    stats = Counter()
    errors, per_source = {}, Counter()
    ok_companies, seen_keys = set(), set()

    log(f"Pulling {len(active)} sources...")
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        results = list(ex.map(_pull, active))

    # Canada + role rules first; then fetch full postings only for the role matches that need it.
    keep = []
    for row, postings, err in results:
        if err:
            errors[f"{row['company']} ({row['platform']})"] = err
            continue
        ok_companies.add(row["company"])
        per_source[row["platform"]] += len(postings)
        stats["pulled"] += len(postings)
        row["total_jobs"], canada = len(postings), 0
        for p in postings:
            if classify(p).in_canada:
                canada += 1
                keep.append(p)
            elif _MULTI.match(p.location_raw) and hasattr(ADAPTERS[p.source], "detail"):
                keep.append(p)            # "3 Locations": decide after fetching the full posting
        row["canada_jobs"], row["verified_at"] = canada, seen_at[:10]
    need = [p for p in keep if _is_candidate(classify_title(p.title))]
    log(f"Fetching full postings where needed ({len(need)} role matches)...")
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        for p, err in ex.map(lambda p: _enrich(p, jobs), need):
            if err:
                stats["detail_errors"] += 1

    for p in keep:
        geo = classify(p)
        if not geo.in_canada:
            continue
        stats["canada"] += 1
        role = classify_title(p.title)
        if not _is_candidate(role) and p.canonical_key not in jobs:
            continue          # only role-family matches are stored; the rest are counted, not kept
        rec = {
            "key": p.canonical_key, "source": p.source, "url": p.url, "seen_at": seen_at,
            "group": dedup.group_key(p.company, p.title, geo.region),
            "company": p.company, "title": p.title, "location": p.location_raw,
            "region": geo.region, "remote": geo.remote, "cec_credit": geo.cec_credit,
            "workplace": p.workplace, "department": p.department, "posted_at": p.posted_at,
            "pay": pay.resolve(p.pay, p.description, p.location_raw, geo.region),
            "pay_field": p.pay,               # raw salary data from the job system, kept so pay can be re-read
            "pay_checked": bool(p.description or p.pay),
            "role_tier": role.tier, "role_excluded": role.excluded,
            "people_mgmt_hint": role.people_mgmt_hint, "role_reason": role.reason,
            "description": p.description if _is_candidate(role) else "",
            "detail_api": p.extra.get("detail_api"),
        }
        if not rec["role_excluded"] and _low_hourly(rec["pay"]):
            rec["role_excluded"], rec["role_reason"] = True, "Hourly pay below the professional range (store or support job)"
        before = len(jobs)
        jid = dedup.merge(jobs, rec)
        seen_keys.add(p.canonical_key)
        job = jobs[jid]
        if len(jobs) > before:
            job["first_seen"] = seen_at
            stats["new"] += 1
        for k in ("title", "location", "region", "remote", "pay", "pay_field", "pay_checked", "role_tier", "role_excluded",
                  "people_mgmt_hint", "role_reason", "workplace", "posted_at"):
            job[k] = rec[k]
        if rec["description"]:
            job["description"] = rec["description"]
        for s in job["sightings"]:
            if s["key"] == p.canonical_key:
                s.update(last_seen=seen_at, live=True, missed_runs=0, url=p.url)

    # Sources that failed this run keep their stored descriptions; re-read pay from them so a parsing
    # improvement reaches every job, not only the ones pulled this time.
    for key, job in jobs.items():
        if key not in seen_keys and job.get("role_tier") and job.get("description"):
            if pagereader.is_bot_check(job["description"]):
                job["description"] = ""
                continue
            job["pay"] = pay.resolve(job.get("pay_field"), job["description"], job.get("location", ""), job.get("region"))
            job["pay_checked"] = True

    # Liveness: only count a miss when that company's sources were pulled successfully this run.
    pulled = {r["company"] for r in active}
    for job in jobs.values():
        for s in job["sightings"]:
            if s["key"] in seen_keys or job["company"] not in pulled or s.get("source") == "capture":
                continue
            if job["company"] in ok_companies:
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
    sources.save(rows)
    for src, n in per_source.items():
        store.mark_fresh(f"jobs:{src}", postings=n)
    summary = {
        "sources_ok": len(active) - len(errors), "sources_failed": len(errors),
        "companies_ok": len(ok_companies), "postings_pulled": stats["pulled"],
        "canada_postings": stats["canada"], "jobs_tracked": sum(1 for j in jobs.values() if j["live"]),
        "new_jobs": stats["new"], "went_dead": stats["went_dead"], "detail_errors": stats["detail_errors"],
        "multi_source_jobs": sum(1 for j in jobs.values() if len(j["sightings"]) > 1),
        "candidates": len(candidates),
        "pay_found": sum(1 for j in jobs.values() if j["live"] and j.get("role_tier") and not j.get("role_excluded")
                         and (j.get("pay") or {}).get("ranges")),
        "equity_mentioned": sum(1 for j in jobs.values() if j["live"] and j.get("role_tier") and not j.get("role_excluded")
                                and (j.get("pay") or {}).get("equity")),
        "pay_canada": sum(1 for j in jobs.values() if j["live"] and j.get("role_tier") and not j.get("role_excluded")
                          and j.get("pay") and j["pay"].get("primary") is not None),
        "by_tier": dict(Counter(c["role_tier"] for c in candidates)),
        "by_region": dict(Counter(c["region"] for c in candidates)), "errors": errors,
    }
    store.mark_fresh("jobs", **{k: summary[k] for k in ("sources_ok", "sources_failed", "canada_postings", "candidates")})
    return summary


def stats() -> dict:
    rows = sources.load()
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    live = [j for j in jobs.values() if j.get("live")]
    cands = [j for j in live if j.get("role_tier") and not j.get("role_excluded")]
    return {
        "sources": dict(Counter(r["status"] for r in rows)),
        "active_by_platform": dict(Counter(r["platform"] for r in rows if r["status"] == "active")),
        "jobs_live": len(live), "candidates": len(cands),
        "by_tier": dict(Counter(j["role_tier"] for j in cands)),
        "by_region": dict(Counter(j["region"] for j in cands)),
        "by_company": dict(Counter(j["company"] for j in cands).most_common()),
        "freshness": store.load("runs", {"components": {}})["components"],
    }
