"""Deduplication (R2): one job, many sightings.

* Exact: the same posting on the same source has the same canonical key (source:slug:job_id).
* Fuzzy: the same role posted on two *different* sources (e.g. a company's Greenhouse board and a
  pasted LinkedIn link) shares a group key built from company + normalized title + place.
  Two postings on the *same* source with different IDs are kept apart: companies often post the
  same title twice for different teams.
"""
from __future__ import annotations

import re

from .text import ascii_fold, norm_title

_CO_NOISE = {"inc", "ltd", "corp", "co", "the", "llc", "limited", "canada"}


def norm_company(name: str) -> str:
    words = re.findall(r"[a-z0-9]+", ascii_fold(name).lower())
    return " ".join(w for w in words if w not in _CO_NOISE)


def group_key(company: str, title: str, place: str | None) -> str:
    return f"{norm_company(company)}|{norm_title(title)}|{(place or '').lower()}"


def merge(jobs: dict, posting_rec: dict) -> str:
    """Merge one posting record into the jobs index (keyed by job id). Returns the job id used.

    posting_rec must carry: key (canonical), group, source, url, seen_at, plus job fields.
    """
    key, group, src = posting_rec["key"], posting_rec["group"], posting_rec["source"]
    # 1) Exact sighting already known.
    for jid, job in jobs.items():
        if any(s["key"] == key for s in job["sightings"]):
            return jid
    # 2) Same role on a different source.
    for jid, job in jobs.items():
        if job["group"] == group and all(s["source"] != src for s in job["sightings"]):
            job["sightings"].append(_sighting(posting_rec))
            return jid
    # 3) New job.
    jobs[key] = {k: v for k, v in posting_rec.items() if k not in ("key", "source", "url", "seen_at")}
    jobs[key]["sightings"] = [_sighting(posting_rec)]
    return key


def _sighting(rec: dict) -> dict:
    return {"key": rec["key"], "source": rec["source"], "url": rec["url"],
            "first_seen": rec["seen_at"], "last_seen": rec["seen_at"], "live": True, "missed_runs": 0}
