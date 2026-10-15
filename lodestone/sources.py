"""The source index (data/sources/source_index.csv): where every watched company's jobs come from.

One row per company per source. `feed` holds the adapter's parameters as JSON (a board slug, or a
Workday host/tenant/site, ...). status: active (pulled on refresh) | no_feed (nothing machine-readable;
use paste capture) | paused. Rows are added by auto-detection or by research, and edited by hand.
"""
from __future__ import annotations

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "sources" / "source_index.csv"
FIELDS = ["company", "platform", "feed", "careers_url", "status", "canada_jobs", "total_jobs",
          "verified_at", "found_by", "notes"]


def load(path: pathlib.Path | None = None) -> list[dict]:
    path = path or INDEX
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["feed"] = json.loads(r["feed"]) if r.get("feed") else {}
    return rows


def save(rows: list[dict], path: pathlib.Path | None = None) -> None:
    path = path or INDEX
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda r: (r["status"] != "active", r["company"].lower(), r["platform"]))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({**{k: "" for k in FIELDS}, **r,
                        "feed": json.dumps(r.get("feed") or {}, separators=(",", ":"), sort_keys=True)})


def by_company(rows: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for r in rows:
        out.setdefault(r["company"], []).append(r)
    return out
