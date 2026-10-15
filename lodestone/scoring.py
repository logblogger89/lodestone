"""Fit scoring (P1-S3, PRD Appendix E). Claude does the scoring in the /refresh-jobs session, so there is no
API bill; this module prepares the work and stores the results.

  lodestone score prepare [--batch N]   -> data/state/score_inbox/batch_XX.json (jobs needing a score)
  lodestone score ingest <file.json>    -> merges results into data/state/scores.json

A job needs a (re)score when it is new, its title/description changed, or the rubric version changed. With
`--profile <file>` (the app's profile/main, saved to the scratchpad), roles scored against an older version of the
profile are re-scored too, at most `--max-rescore` a day (newest first) so a profile edit doesn't use a whole day's
usage at once (D-060). The candidate profile lives in the app's database, never in the repo.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil

from . import store
from .appexport import job_id

INBOX = store.STATE / "score_inbox"
SUBS = ["role", "level", "domain", "pathway", "pay", "skills"]
_BOILER = re.compile(r"(equal opportunity|accommodation|we are committed to (diversity|creating)|privacy (notice|policy)|"
                     r"benefits include|what we offer|perks|about us\b|who we are\b|e-?verify|land acknowledg)", re.I)


def config() -> dict:
    return json.loads((store.ROOT / "config" / "scoring.json").read_text())


PROFILE_KEYS = ("headline", "summary", "domains", "skills", "scope_signals", "roles", "current", "experience_years",
                "preferences", "work_status")


def profile_key(profile: dict | None) -> str | None:
    """Short hash of the parts of a profile that change scores (not the resume file or app settings)."""
    if not profile:
        return None
    profile = profile.get("data", profile)
    part = {k: profile.get(k) for k in PROFILE_KEYS}
    return hashlib.sha1(json.dumps(part, sort_keys=True, default=str).encode()).hexdigest()[:12]


def _fingerprint(j: dict, rubric: str) -> str:
    return hashlib.sha1(f"{rubric}|{j['title']}|{(j.get('description') or '')[:20000]}".encode()).hexdigest()[:16]


def trim(desc: str, limit: int = 6000) -> str:
    """Keep the parts that describe the job; drop boilerplate paragraphs (EEO, benefits, company blurb)."""
    paras = [p.strip() for p in re.split(r"\n\s*\n|\n(?=[-•*])", desc or "") if p.strip()]
    keep = [p for p in paras if not _BOILER.search(p[:200])]
    text = "\n".join(keep) or (desc or "")
    return text[:limit]


def _pay_summary(pay: dict | None) -> str:
    if not pay or not pay.get("ranges"):
        return "No pay range found"
    out = []
    for i, r in enumerate(pay["ranges"]):
        tag = " (featured Canadian)" if i == pay.get("primary") else ""
        out.append(f"{r.get('currency') or '$'} {r['min']}-{r['max']} {r.get('interval')} {r.get('kind')} [{r.get('label') or 'no region'}]{tag}")
    eq = pay.get("equity")
    if eq:
        out.append(f"Equity: {eq.get('certainty')}")
    return "; ".join(out)


def prepare(batch_size: int = 70, profile: dict | None = None, max_rescore: int = 150) -> list[dict]:
    rubric = config()["rubric_version"]
    pkey = profile_key(profile)
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    scores = store.load("scores", {})
    todo, stale = [], []
    for key, j in jobs.items():
        if not (j.get("live") and j.get("role_tier") and not j.get("role_excluded")):
            continue
        fp = _fingerprint(j, rubric)
        have = scores.get(job_id(key), {})
        if have.get("fingerprint") == fp:
            if not pkey or have.get("profile_key") == pkey:
                continue
            stale.append((j.get("first_seen") or "", key, fp))     # same job, older profile: re-score within the daily cap
            continue
        todo.append((key, fp))
    stale.sort(reverse=True)
    todo += [(k, fp) for _, k, fp in stale[:max_rescore]]
    todo = [_packet(key, jobs[key], fp, pkey) for key, fp in todo]
    shutil.rmtree(INBOX, ignore_errors=True)
    INBOX.mkdir(parents=True)
    out = []
    for n in range(0, len(todo), batch_size):
        path = INBOX / f"batch_{n // batch_size:02d}.json"
        path.write_text(json.dumps(todo[n:n + batch_size], ensure_ascii=False, indent=1))
        out.append({"file": str(path), "jobs": len(todo[n:n + batch_size])})
    if len(stale) > max_rescore:
        out.append({"profile_rescore_waiting": len(stale) - max_rescore})
    return out


def _packet(key: str, j: dict, fp: str, pkey: str | None) -> dict:
    return {"id": job_id(key), "fingerprint": fp, "profile_key": pkey, "title": j["title"], "company": j["company"],
                     "location": j.get("location"), "region": j.get("region"), "tier": j.get("role_tier"),
            "pay": _pay_summary(j.get("pay")), "description": trim(j.get("description") or "") or "(no description available)"}


def ingest(results: list[dict]) -> dict:
    """Validate and store scores. Each result: id, fingerprint, subs{6}, reasons{6}, summary, level_guess,
    people_mgmt, work_mode, must_haves, flags."""
    scores = store.load("scores", {})
    ok, bad = 0, []
    for r in results:
        subs = r.get("subs") or {}
        if not r.get("id") or set(SUBS) - set(subs) or not all(isinstance(subs[k], (int, float)) and 0 <= subs[k] <= 100 for k in SUBS):
            bad.append(r.get("id"))
            continue
        scores[r["id"]] = {
            "fingerprint": r.get("fingerprint"), "profile_key": r.get("profile_key"), "rubric": config()["rubric_version"], "scored_at": store.now(),
            "subs": {k: int(round(subs[k])) for k in SUBS},
            "reasons": {k: str((r.get("reasons") or {}).get(k, ""))[:160] for k in SUBS},
            "summary": str(r.get("summary") or "")[:220], "level_guess": str(r.get("level_guess") or "")[:60],
            "people_mgmt": bool(r.get("people_mgmt")), "work_mode": str(r.get("work_mode") or "")[:20],
            "must_haves": [str(x)[:80] for x in (r.get("must_haves") or [])][:4],
            "flags": [str(x)[:60] for x in (r.get("flags") or [])][:4],
        }
        ok += 1
    store.save("scores", scores)
    store.mark_fresh("scoring", rubric=config()["rubric_version"], scored=len(scores))
    return {"stored": ok, "rejected": bad, "total_scored": len(scores)}
