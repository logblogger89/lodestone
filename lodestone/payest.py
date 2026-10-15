"""Pay estimates for roles with no posted Canadian range (R5, B8, DR-2 §3). Always labelled "est.", with basis,
confidence and the postings it came from. Uses only Lodestone's own corpus of posted Canadian base ranges:

  1. Same company, same role family and level            -> high confidence
  2. Same company, same family, one level away (±15%)    -> medium
  3. Similar companies (same segment), same family/level -> medium-low (needs 3+ postings)
  4. All companies, same family and level                -> low (needs 5+ postings)

Caveat shown in the app: Ontario exempts roles paying over $200K from posting a range (DR-4), so posted ranges
under-represent senior pay and estimates for senior roles may run low.
"""
from __future__ import annotations

import re
import statistics

from . import pipeline, scoring, store
from .appexport import job_id

LEVEL_STEP = 0.15


def level_of(title: str, guess: str | None) -> int | None:
    m = re.findall(r"L(\d)", guess or "")
    if m:
        return round(sum(int(x) for x in m) / len(m))
    t = (title or "").lower()
    for pat, lv in ((r"\b(vp|vice president)\b", 8), (r"\b(director|head of)\b", 7), (r"\b(principal|group product)\b", 6),
                    (r"\bstaff\b", 6), (r"\b(senior|sr\.?|lead)\b", 5), (r"\b(associate|junior|jr\.?)\b", 3)):
        if re.search(pat, t):
            return lv
    return 4 if re.search(r"\b(ii|2)\b", t) else None


def _round5k(v: float) -> int:
    return int(round(v / 5000.0) * 5000)


def _canadian_base(pay: dict | None) -> dict | None:
    if not pay or pay.get("primary") is None:
        return None
    r = pay["ranges"][pay["primary"]]
    if r.get("interval") != "year" or r.get("currency") == "USD" or r.get("kind") not in ("base", "unspecified", None):
        return None
    if not (r.get("min") and r.get("max")) or r["max"] / max(r["min"], 1) > 3:
        return None                               # one-sided or absurdly wide (e.g. $100K–300K) ranges teach little
    return r


def _band_score(top: float) -> int:
    b = scoring.config()["pay_target_cad"]
    return 95 if top >= b["excellent"] else 80 if top >= b["good"] else 60 if top >= b["ok"] else 40 if top >= b["low"] else 20


def build() -> dict[str, dict]:
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    scores = store.load("scores", {})
    seg = {r["company"].strip(): r.get("segment", "") for r in pipeline.employers()}
    rows = []
    for key, j in jobs.items():
        if not (j.get("live") and j.get("role_tier") and not j.get("role_excluded")):
            continue
        jid = job_id(key)
        rows.append({"id": jid, "company": j["company"], "title": j["title"], "family": j["role_tier"],
                     "segment": seg.get(j["company"], ""), "level": level_of(j["title"], scores.get(jid, {}).get("level_guess")),
                     "base": _canadian_base(j.get("pay")), "has_canadian": bool((j.get("pay") or {}).get("primary") is not None)})
    pool = [r for r in rows if r["base"] and r["level"]]
    out = {}
    for r in rows:
        if r["has_canadian"] or not r["level"]:
            continue
        tiers = [
            ("Same company, same level", "high", 1,
             [p for p in pool if p["company"] == r["company"] and p["family"] == r["family"] and p["level"] == r["level"]], 0),
            ("Same company, adjusted one level", "medium", 1,
             [p for p in pool if p["company"] == r["company"] and p["family"] == r["family"] and abs(p["level"] - r["level"]) == 1], None),
            (f"Similar companies ({r['segment'] or 'same segment'}), same level", "medium-low", 3,
             [p for p in pool if r["segment"] and p["segment"] == r["segment"] and p["family"] == r["family"] and p["level"] == r["level"]], 0),
            ("All watched companies, same level", "low", 5,
             [p for p in pool if p["family"] == r["family"] and p["level"] == r["level"]], 0),
        ]
        for basis, conf, need, comps, _ in tiers:
            if len(comps) < need:
                continue
            adj = lambda p: (1 + LEVEL_STEP) ** (r["level"] - p["level"])
            lo = statistics.median(p["base"]["min"] * adj(p) for p in comps)
            hi = statistics.median(p["base"]["max"] * adj(p) for p in comps)
            if hi < lo:
                lo, hi = hi, lo
            est = {"min": _round5k(lo), "max": _round5k(hi), "currency": "CAD", "interval": "year", "kind": "base",
                   "basis": basis, "confidence": conf, "n": len(comps),
                   "examples": [f"{p['company']}: {p['title']} ({p['base']['min']:,.0f}–{p['base']['max']:,.0f})" for p in comps[:3]]}
            est["score"] = _band_score(est["max"])
            out[r["id"]] = est
            break
    return out
