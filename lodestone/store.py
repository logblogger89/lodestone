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


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def today() -> str:
    """Today's date in New York time: the day the scheduled runs and the app's daily caps count against."""
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("America/New_York")).date().isoformat()
    except Exception:                                    # no time-zone data: UTC is close enough for a cap
        return dt.datetime.now(dt.timezone.utc).date().isoformat()


def count_today(name: str) -> int:
    """How many items a daily log holds for today (each log: {date: [ids]}, last 14 days kept)."""
    return len(load(name, {}).get(today(), []))


def log_today(name: str, item: str) -> int:
    log = load(name, {})
    day = log.setdefault(today(), [])
    if item not in day:
        day.append(item)
    save(name, {d: v for d, v in sorted(log.items())[-14:]})
    return len(day)


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


def mark_fresh(component: str, **info) -> None:
    """Freshness indicator (R11a): last-updated time per component."""
    runs = load("runs", {"components": {}, "history": []})
    runs["components"][component] = {"at": now(), **info}
    runs["history"] = (runs["history"] + [{"component": component, "at": now(), **info}])[-50:]
    save("runs", runs)
