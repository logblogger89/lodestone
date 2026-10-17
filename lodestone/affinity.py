"""Type scores (D-077): how much of each job is each kind of work, 0-100 per role family.

A job can be more than one type: "Program Manager, Payments" may be Program 80, Product 70. Type scores are a fact
about the job, the same for everyone, so they are worked out once per job (and again only if its title or
description changes). Claude reads the description in the refresh run (like fit scoring, but a much shorter task):

  lodestone affinity prepare   -> data/state/affinity_inbox/batch_XX.json (jobs that need type scores, best first)
  lodestone affinity ingest <file.json>

Until Claude has read a job, its title gives a first guess (`prior`): 85 for the family its title names. How well a
job fits a *person* is `relevance`: the best type score among the families they do and the ones they asked to see,
the related and stretch ones counting a little less. The app computes the same thing (lodestone.html).
"""
from __future__ import annotations

import hashlib
import json
import shutil

from . import rules, store

INBOX = store.STATE / "affinity_inbox"
DAILY_CAP = 400          # Claude reads at most this many jobs a day for type scores (catch-up spreads over runs)
PRIOR = 85               # title-only guess for the family the title names
SHOWN_AT = 50            # a job is shown to, and scored for, someone when its relevance reaches this
WEIGHT = {"Core": 1.0, "Adjacent": 0.85, "Stretch": 0.7, "Other": 0.7}


def fingerprint(j: dict) -> str:
    return hashlib.sha1(f"aff1|{j['title']}|{(j.get('description') or '')[:20000]}".encode()).hexdigest()[:16]


def prior(title: str, family: str | None = None) -> dict:
    fam = family or rules.classify_title(title).family
    return {fam: PRIOR} if fam else {}


def for_job(key: str, j: dict, stored: dict | None = None) -> tuple[dict, str]:
    """(type scores, source): "read" when Claude has read this version of the posting, else the title guess."""
    from .appexport import job_id
    stored = store.load("affinity", {}) if stored is None else stored
    have = stored.get(job_id(key)) or {}
    if have.get("fingerprint") == fingerprint(j) and have.get("aff"):
        return have["aff"], "read"
    return prior(j["title"], j.get("role_family")), "title"


def relevance(aff: dict, mine: list[str], shown: list[str] | None) -> tuple[float, str | None]:
    """Best weighted type score over the person's families, and the family that gave it."""
    mine = list(mine or rules.default_families())
    if shown is None:
        fams = {f["id"]: f for f in rules.families()}
        shown = [x for m in mine for x in fams.get(m, {}).get("related", []) + fams.get(m, {}).get("stretch", [])]
    best, via = 0.0, None
    for f in set(mine) | set(shown):
        w = WEIGHT[rules.closeness(f, mine) or "Other"]
        v = (aff.get(f) or 0) * w
        if v > best:
            best, via = v, f
    return best, via


def _rank_hint(jid: str, scores: dict) -> float:
    s = (scores.get(jid) or {}).get("subs") or {}
    return sum(s.values()) / len(s) if s else -1


def pending_batches() -> list[str]:
    stored = store.load("affinity", {})
    left = []
    for f in sorted(INBOX.glob("batch_*.json")) if INBOX.exists() else []:
        for r in json.loads(f.read_text()):
            if (stored.get(r["id"]) or {}).get("fingerprint") != r["fingerprint"]:
                left.append(r["id"])
    return left


def prepare(batch_size: int = 60, cap: int = DAILY_CAP, force: bool = False) -> list[dict]:
    """Batches of live roles with no type scores for their current posting: the best-scored first (the top of people's
    lists), then the newest, within the daily cap. Once caught up, each run reads only the day's new roles. Refuses while earlier batches are still being read (see scoring.prepare)."""
    from .appexport import job_id
    if not force and (left := pending_batches()):
        raise RuntimeError(f"{len(left)} roles in the current type-score batches aren't ingested yet; ingest them first, "
                           "or pass --force if those readers have stopped")
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    stored, scores = store.load("affinity", {}), store.load("scores", {})
    todo = []
    for key, j in jobs.items():
        if not (j.get("live") and j.get("role_tier") and not j.get("role_excluded")):
            continue
        jid, fp = job_id(key), fingerprint(j)
        if (stored.get(jid) or {}).get("fingerprint") == fp:
            continue
        todo.append(((j.get("first_seen") or "")[:10], _rank_hint(jid, scores), jid, fp, key))
    todo.sort(key=lambda t: (t[1], t[0]), reverse=True)        # best-scored roles first (the top of lists), then newest
    room = max(0, cap - store.count_today("affinity_log"))
    take = todo[:room]
    shutil.rmtree(INBOX, ignore_errors=True)
    INBOX.mkdir(parents=True)
    fams = [{"id": f["id"], "label": f["label"], "what": f.get("what", "")} for f in rules.families()]
    out = []
    for n in range(0, len(take), batch_size):
        part = [{"id": jid, "fingerprint": fp, "title": jobs[key]["title"], "company": jobs[key]["company"],
                 "title_guess": jobs[key].get("role_family"),
                 "description": (jobs[key].get("description") or "")[:3000] or "(no description: judge from the title)"}
                for _, _, jid, fp, key in take[n:n + batch_size]]
        path = INBOX / f"batch_{n // batch_size:02d}.json"
        path.write_text(json.dumps({"families": fams, "jobs": part}, ensure_ascii=False, indent=1))
        out.append({"file": str(path), "jobs": len(part)})
    if len(todo) > room:
        out.append({"waiting": len(todo) - room})
    store.mark_fresh("affinity", read=len(stored), waiting=max(0, len(todo) - room))
    return out


def ingest(results: list[dict]) -> dict:
    """Each result: {id, fingerprint, aff: {family id: 0-100}, why}. Unknown families and bad numbers are rejected."""
    ids = {f["id"] for f in rules.families()}
    stored = store.load("affinity", {})
    ok, bad = 0, []
    for r in results:
        aff = r.get("aff") or {}
        if not r.get("id") or not r.get("fingerprint") or not aff or set(aff) - ids or \
                not all(isinstance(v, (int, float)) and 0 <= v <= 100 for v in aff.values()):
            bad.append(r.get("id"))
            continue
        stored[r["id"]] = {"fingerprint": r["fingerprint"], "aff": {k: int(round(v)) for k, v in aff.items() if v >= 5},
                           "why": str(r.get("why") or "")[:160], "at": store.now()}
        store.log_today("affinity_log", r["id"])
        ok += 1
    store.save("affinity", stored)
    return {"stored": ok, "rejected": bad, "total": len(stored)}
