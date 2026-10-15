"""Daily run report (D-057): one document per day, shown in the app (Digest banner and Reports > Archive) and
committed under data/state/reports/ so GitHub keeps the history too.

  python3 -m lodestone report save <report.json>   -> validates, writes data/state/reports/<date>.json, prints the
                                                     db document to write and the old dates to delete from the db
Report shape (written by Claude at the end of the daily run):
  {"date": "YYYY-MM-DD", "headline": "...", "stats": {"new": 0, "closed": 0, "scored": 0, "unscored": 0,
   "open_roles": 0, "failed_sources": 0}, "top": [{"id", "company", "title", "fit", "pay", "why"}],
   "sections": [{"title": "...", "items": ["..."]}], "actions": ["what Ayush needs to do"]}
"""
from __future__ import annotations

import datetime as dt
import json
import re

from . import store

DIR = store.STATE / "reports"
KEEP_DAYS = 90                      # in the app's db; the app shows the last N days (Settings)
STATS = ("new", "closed", "scored", "unscored", "open_roles", "failed_sources")


def validate(r: dict) -> list[str]:
    errs = []
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r.get("date", ""))):
        errs.append("date must be YYYY-MM-DD")
    if not str(r.get("headline", "")).strip():
        errs.append("headline is required")
    for k, v in (r.get("stats") or {}).items():
        if k not in STATS or not isinstance(v, int):
            errs.append(f"stats.{k}: unknown or not a whole number")
    for t in r.get("top") or []:
        if not {"company", "title"} <= set(t):
            errs.append("each top match needs company and title")
    for s in r.get("sections") or []:
        if not (s.get("title") and isinstance(s.get("items"), list)):
            errs.append("each section needs a title and a list of items")
    return errs


def save(r: dict, today: dt.date | None = None) -> dict:
    errs = validate(r)
    if errs:
        return {"status": "invalid", "errors": errs}
    doc = {"date": r["date"], "ran_at": r.get("ran_at") or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
           "headline": r["headline"].strip(), "stats": {k: r.get("stats", {}).get(k) for k in STATS if k in r.get("stats", {})},
           "top": [{k: t.get(k) for k in ("id", "company", "title", "fit", "pay", "why")} for t in (r.get("top") or [])[:5]],
           "sections": [{"title": s["title"], "items": [str(i) for i in s["items"]][:30]} for s in r.get("sections") or []],
           "actions": [str(a) for a in r.get("actions") or []][:10]}
    DIR.mkdir(parents=True, exist_ok=True)
    path = DIR / f"{doc['date']}.json"
    path.write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    cutoff = ((today or dt.date.today()) - dt.timedelta(days=KEEP_DAYS)).isoformat()
    old = sorted(p.stem for p in DIR.glob("*.json") if p.stem < cutoff)
    return {"status": "saved", "file": str(path), "db_doc": f"reports/{doc['date']}", "delete_from_db": [f"reports/{d}" for d in old]}
