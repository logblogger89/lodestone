"""File-backed state under data/state/ (Phase 1). The Artifact db is the app's copy; these files let
each fresh Claude Code session pick up where the last one left off (liveness needs history)."""
from __future__ import annotations

import csv
import datetime as dt
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "state"
SEED = ROOT / "data" / "seed" / "watchlist_seed.csv"
OVERRIDES = ROOT / "config" / "ats_overrides.csv"


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load(name: str, default):
    path = STATE / f"{name}.json"
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save(name: str, data) -> pathlib.Path:
    STATE.mkdir(parents=True, exist_ok=True)
    path = STATE / f"{name}.json"
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=False) + "\n")
    return path


def read_seed(path: pathlib.Path = SEED) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_overrides(path: pathlib.Path = OVERRIDES) -> dict[str, dict]:
    """company -> {"ats": ..., "slug": ...}. ats 'none' means: don't probe, no public feed."""
    if not path.exists():
        return {}
    out = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(line for line in f if not line.startswith("#")):
            if row.get("company"):
                out[row["company"].strip()] = {"ats": (row.get("ats") or "").strip() or None,
                                               "slug": (row.get("slug") or "").strip() or None}
    return out


def mark_fresh(component: str, **info) -> None:
    """Freshness indicator (R11a): last-updated time per component."""
    runs = load("runs", {"components": {}, "history": []})
    runs["components"][component] = {"at": now(), **info}
    runs["history"] = (runs["history"] + [{"component": component, "at": now(), **info}])[-50:]
    save("runs", runs)
