"""Paste inbox (R3, A3a/b/c): links or job-description text Ayush pastes in the app's "Add job".

Two steps, so no paid API is needed:
  lodestone inbox prepare <inbox.json>  -> for each pasted item: find links, recognise known jobs, fetch readable
                                           pages, and write work packets to data/state/capture_inbox/
  (Claude reads each packet and writes the job details: title, company, location, url, description)
  lodestone inbox add <records.json>    -> adds the jobs (dedup against everything known), returns per-item status

Statuses written back to the app's inbox: already_known, added, needs_text, not_canada, not_a_role, failed.
LinkedIn, Indeed, Glassdoor and Wellfound pages are never fetched (A3): for those Lodestone asks for the
job-description text instead, unless it was pasted along with the link.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import urllib.parse

from . import dedup, pagereader, pay, store
from .appexport import job_id
from .geo import classify
from .models import Posting
from .rules import classify_title

INBOX = store.STATE / "capture_inbox"
URL = re.compile(r"https?://[^\s<>\"')\]]+", re.I)
NO_FETCH = ("linkedin.com", "indeed.com", "indeed.ca", "glassdoor.", "wellfound.com", "angel.co")
LABELS = {"linkedin.com": "LinkedIn (pasted)", "indeed.": "Indeed (pasted)", "glassdoor.": "Glassdoor (pasted)",
          "wellfound.com": "Wellfound (pasted)"}


def _canon(url: str) -> str:
    """Comparable form of a posting URL: no query string, fragment or trailing slash."""
    p = urllib.parse.urlparse(url.strip())
    return f"{p.netloc.lower().removeprefix('www.')}{p.path.rstrip('/')}"


def _known_urls(jobs: dict) -> dict[str, str]:
    out = {}
    for key, j in jobs.items():
        for s in j["sightings"]:
            out[_canon(s["url"])] = key
    return out


def prepare(items: list[dict]) -> list[dict]:
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    known = _known_urls(jobs)
    shutil.rmtree(INBOX, ignore_errors=True)
    INBOX.mkdir(parents=True)
    out = []
    for it in items:
        if it.get("status") not in (None, "new"):
            continue
        text = (it.get("text") or "").strip()
        urls = list(dict.fromkeys(u.rstrip(".,;") for u in URL.findall(text)))
        jd_text = URL.sub(" ", text).strip()
        packet = {"doc_id": it["id"], "pasted_text": jd_text[:20000], "links": []}
        for u in urls:
            host = urllib.parse.urlparse(u).netloc.lower()
            hit = known.get(_canon(u))
            link = {"url": u, "host": host}
            if hit:
                link.update(kind="already_known", job_id=job_id(hit), title=jobs[hit]["title"], company=jobs[hit]["company"])
            elif any(b in host for b in NO_FETCH):
                link.update(kind="no_fetch")              # use pasted text if any, else ask for it
            else:
                try:
                    link.update(kind="page", page_text=pagereader.posting_text(u, "capture")[:15000])
                except Exception as e:
                    link.update(kind="fetch_failed", error=f"{type(e).__name__}: {e}"[:160])
            packet["links"].append(link)
        if not urls:
            packet["links"].append({"url": None, "host": None, "kind": "text_only"})
        path = INBOX / f"{it['id']}.json"
        path.write_text(json.dumps(packet, ensure_ascii=False, indent=1))
        out.append({"doc_id": it["id"], "file": str(path), "links": [(l["kind"], l.get("url")) for l in packet["links"]]})
    return out


def _label(url: str | None) -> str:
    host = urllib.parse.urlparse(url or "").netloc.lower()
    for k, v in LABELS.items():
        if k in host:
            return v
    return (host.removeprefix("www.") or "Pasted text") + (" (pasted)" if host else "")


def add(records: list[dict]) -> list[dict]:
    """Records from Claude, one per pasted job: {doc_id, url, title, company, location, description,
    status?, note?}. status may preset already_known / needs_text / not_a_role / failed."""
    data = store.load("jobs", {"jobs": {}, "updated_at": None})
    jobs = data["jobs"]
    now = store.now()
    results = []
    for r in records:
        if r.get("status") in ("already_known", "needs_text", "not_a_role", "failed"):
            results.append({"doc_id": r["doc_id"], "status": r["status"], "result": r.get("note", "")})
            continue
        url = r.get("url") or ""
        src_key = hashlib.sha1((url or r.get("title", "") + r.get("company", "")).encode()).hexdigest()[:12]
        p = Posting(source="capture", company=(r.get("company") or "").strip(), slug=_label(url),
                    source_job_id=src_key, title=(r.get("title") or "").strip(), url=url,
                    location_raw=r.get("location") or "", description=r.get("description") or "")
        geo = classify(p)
        if not geo.in_canada:
            results.append({"doc_id": r["doc_id"], "status": "not_canada",
                            "result": f"{p.title} at {p.company}: location '{p.location_raw}' isn't in Canada, so it wasn't added."})
            continue
        role = classify_title(p.title)
        rec = {"key": p.canonical_key, "source": "capture", "url": url or "", "seen_at": now,
               "group": dedup.group_key(p.company, p.title, geo.region), "company": p.company, "title": p.title,
               "location": p.location_raw, "region": geo.region, "remote": geo.remote, "cec_credit": geo.cec_credit,
               "workplace": r.get("workplace"), "department": "", "posted_at": r.get("posted_at"),
               "pay": pay.resolve(None, p.description, p.location_raw, geo.region), "pay_field": None,
               "pay_checked": bool(p.description), "role_tier": role.tier or "Other", "role_family": role.family,   # you chose it: keep it
               "role_excluded": False, "people_mgmt_hint": role.people_mgmt_hint,
               "role_reason": role.reason if role.tier else "added by you", "description": p.description,
               "captured": True, "label": _label(url)}
        before = len(jobs)
        jid = dedup.merge(jobs, rec)
        job = jobs[jid]
        job.setdefault("first_seen", now)
        job.setdefault("live", True)
        job["last_seen"] = max(job.get("last_seen") or now, now)
        for s in job["sightings"]:
            if s["key"] == p.canonical_key:
                s["label"] = rec["label"]
        merged = len(jobs) == before
        results.append({"doc_id": r["doc_id"], "status": "added", "job_id": job_id(jid),
                        "result": (f"Matched an existing role: {job['title']} at {job['company']}." if merged
                                   else f"Added {p.title} at {p.company}. It's scored at this refresh.")})
    store.save("jobs", data)
    return results
