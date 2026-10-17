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

from . import rules, store
from .appexport import job_id

INBOX = store.STATE / "score_inbox"
SUBS = ["role", "level", "domain", "pathway", "pay", "skills"]
_BOILER = re.compile(r"(equal opportunity|accommodation|we are committed to (diversity|creating)|privacy (notice|policy)|"
                     r"benefits include|what we offer|perks|about us\b|who we are\b|e-?verify|land acknowledg)", re.I)


def config() -> dict:
    return json.loads((store.ROOT / "config" / "scoring.json").read_text())


PROFILE_KEYS = ("headline", "summary", "domains", "skills", "scope_signals", "roles", "current", "experience_years",
                "preferences", "work_status")


# Profile parts the app applies itself, instantly, without re-scoring (D-077): where you want to work, people
# management, which other families you see (and their labels), work status (pathway is computed in the app).
APP_SIDE_PREFS = ("families_shown", "role_families", "locations", "people_management", "updated")


def profile_key(profile: dict | None) -> str | None:
    """Short hash of the parts of a profile that Claude's fit scores depend on (experience, domains, skills, target
    level, field). Changes the app applies itself (APP_SIDE_PREFS, work status) don't change it, so they cost no
    re-scoring."""
    if not profile:
        return None
    profile = profile.get("data", profile)
    part = {k: profile.get(k) for k in PROFILE_KEYS if k != "work_status"}
    pref = {k: v for k, v in (part.get("preferences") or {}).items() if k not in APP_SIDE_PREFS}
    if pref.get("families") in (None, [], rules.default_families()):
        pref.pop("families", None)            # the default field: same scores as before families existed
    if part.get("preferences") is not None:
        part["preferences"] = pref
    return hashlib.sha1(json.dumps({"v": 2, **part}, sort_keys=True, default=str).encode()).hexdigest()[:12]


def legacy_key(profile: dict | None) -> str | None:
    """The key before D-077, so scores already made for this exact profile still count as current."""
    if not profile:
        return None
    profile = profile.get("data", profile)
    part = {k: profile.get(k) for k in PROFILE_KEYS}
    pref = dict(part.get("preferences") or {})
    pref.pop("families_shown", None)          # which other families you see changes what is scored, not how
    pref.pop("role_families", None)           # labels mirroring `families`
    if pref.get("families") in (None, [], rules.default_families()):
        pref.pop("families", None)            # the default field: same scores as before families existed
    if part.get("preferences") is not None:
        part["preferences"] = pref
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


def in_scope(key: str, j: dict, profile: dict | None, stored_aff: dict | None = None) -> bool:
    """Worth a scoring call for this person (D-077): the job's type scores make it relevant to the families they do or
    asked to see (affinity.relevance >= affinity.SHOWN_AT). Roles you added yourself always count."""
    from . import affinity
    if j.get("captured"):
        return True
    pref = ((profile or {}).get("data", profile or {}).get("preferences") or {})
    mine = [f for f in (pref.get("families") or []) if f] or rules.default_families()
    aff, _ = affinity.for_job(key, j, stored_aff)
    if not aff and "role_family" not in j:
        return True           # older stored jobs not yet classified: keep the old behaviour
    return affinity.relevance(aff, mine, pref.get("families_shown"))[0] >= affinity.SHOWN_AT


def family_scope(profile: dict | None) -> set[str]:
    """Role families worth scoring for this person (D-076): the families they do (`preferences.families`) plus the
    ones they asked to see too (`preferences.families_shown`). Older profiles without families: the default
    families plus everything related or a stretch, which is what was scored before."""
    pref = ((profile or {}).get("data", profile or {}).get("preferences") or {})
    mine = [f for f in (pref.get("families") or []) if f] or rules.default_families()
    shown = pref.get("families_shown")
    if shown is None:
        fams = {f["id"]: f for f in rules.families()}
        shown = [x for m in mine for x in fams.get(m, {}).get("related", []) + fams.get(m, {}).get("stretch", [])]
    return set(mine) | set(shown)


def pending_batches() -> list[str]:
    """Roles in the current batch files that haven't been ingested yet (a scorer may still be working on them)."""
    scores = store.load("scores", {})
    left = []
    for f in sorted(INBOX.glob("batch_*.json")) if INBOX.exists() else []:
        for r in json.loads(f.read_text()):
            have = scores.get(r["id"], {})
            if have.get("fingerprint") != r.get("fingerprint") or have.get("profile_key") != r.get("profile_key"):
                left.append(r["id"])
    return left


def prepare(batch_size: int = 70, profile: dict | None = None, max_rescore: int = 150, force: bool = False) -> list[dict]:
    """Writes new batch files. Refuses while earlier batches are still being scored (their files would be replaced
    under the scorer, and results would be matched to the wrong roles: 2026-10-16), unless force=True."""
    if not force and (left := pending_batches()):
        raise RuntimeError(f"{len(left)} roles in the current batches aren't ingested yet; ingest their results first, "
                           "or pass --force if those scorers have stopped")
    rubric = config()["rubric_version"]
    pkey, lkey = profile_key(profile), legacy_key(profile)
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    scores = store.load("scores", {})
    stored_aff = store.load("affinity", {})
    todo, stale = [], []
    migrated = 0
    if pkey:   # remember which field each profile version was scored for, so the app can tell when it no longer matches
        fields = store.load("profile_fields", {})
        pref = ((profile or {}).get("data", profile or {}).get("preferences") or {})
        fields[pkey] = sorted(f for f in (pref.get("families") or rules.default_families()) if f)
        store.save("profile_fields", fields)
    for key, j in jobs.items():
        if not (j.get("live") and j.get("role_tier") and not j.get("role_excluded")):
            continue
        if not in_scope(key, j, profile, stored_aff):
            continue          # not the kind of work this person looks at: not worth a scoring call
        fp = _fingerprint(j, rubric)
        have = scores.get(job_id(key), {})
        if have.get("fingerprint") == fp:
            if pkey and lkey and have.get("profile_key") == lkey and lkey != pkey:
                have["profile_key"] = pkey     # scored for this same profile under the old key: still current
                migrated += 1
            if not pkey or have.get("profile_key") == pkey:
                continue
            subs = have.get("subs") or {}      # same job, older profile: re-score within the daily cap, best first
            stale.append((sum(subs.values()) / len(subs) if subs else 0, j.get("first_seen") or "", key, fp))
            continue
        todo.append((key, fp))
    if migrated:
        store.save("scores", scores)
    stale.sort(reverse=True)
    max_rescore = max(0, max_rescore - store.count_today("rescore_log"))   # the cap is per day, across all runs
    todo += [(k, fp) for _, _, k, fp in stale[:max_rescore]]
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
    store.mark_fresh("rescore", waiting=max(0, len(stale) - max_rescore), cap=150, this_run=min(len(stale), max_rescore))
    return out


def _packet(key: str, j: dict, fp: str, pkey: str | None) -> dict:
    return {"id": job_id(key), "fingerprint": fp, "profile_key": pkey, "title": j["title"], "company": j["company"],
                     "location": j.get("location"), "region": j.get("region"), "family": _family_label(j.get("role_family")),
            "pay": _pay_summary(j.get("pay")), "description": trim(j.get("description") or "") or "(no description available)"}


def _family_label(fid: str | None) -> str:
    return next((f["label"] for f in rules.families() if f["id"] == fid), "Other (added by you)")


_STOP = set("the and for with own lead drive its from that this their role product manager senior staff principal".split())


def _words(t: str) -> set:
    return {w for w in re.findall(r"[a-z]{4,}", (t or "").lower()) if w not in _STOP}


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
        prev = scores.get(r["id"]) or {}
        if prev.get("fingerprint") == r.get("fingerprint") and prev.get("profile_key") != r.get("profile_key"):
            store.log_today("rescore_log", r["id"])    # a re-score against a changed profile
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
    # Sanity check: a summary that shares few words with its own posting was probably written for another role.
    jobs = {job_id(k): j for k, j in store.load("jobs", {"jobs": {}})["jobs"].items()}
    suspect = []
    for r in results:
        j, sw = jobs.get(r.get("id")), _words(r.get("summary"))
        if j and j["company"].split(" (")[0].lower() not in (r.get("summary") or "").lower() and len(sw) >= 4 and len(sw & _words(f"{j['title']} {j['company']} {(j.get('description') or '')[:6000]}")) / len(sw) < 0.4:
            suspect.append({"id": r["id"], "company": j["company"], "title": j["title"], "summary": r.get("summary", "")[:100]})
    return {"stored": ok, "rejected": bad, "total_scored": len(scores), "suspect_mismatch": suspect}
