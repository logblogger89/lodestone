"""Decide whether a posting is in Canada and which region it belongs to (driven by config/geo_canada.json)."""
from __future__ import annotations

import json
import pathlib
import re
from dataclasses import dataclass
from functools import lru_cache

from .models import Posting

CONFIG = pathlib.Path(__file__).resolve().parent.parent / "config" / "geo_canada.json"


@dataclass
class GeoResult:
    in_canada: bool
    region: str | None          # GTA | Waterloo Region | ... | Remote-Canada | None
    remote: bool
    cec_credit: bool            # work happens in Canada (DR-3 §2a)
    reason: str


@lru_cache(maxsize=1)
def _cfg() -> dict:
    return json.loads(CONFIG.read_text())


def _has(text: str, word: str) -> bool:
    return re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", text) is not None


def classify(p: Posting) -> GeoResult:
    cfg = _cfg()
    loc = p.location_raw.lower()
    remote = bool(p.remote_hint) or "remote" in loc or p.workplace == "remote"
    country = (p.country_hint or "").strip().lower()
    canada_named = any(_has(loc, n) for n in cfg["country_names"]) or country in cfg["country_codes"] + cfg["country_names"]
    province_hit = None
    for code, names in cfg["provinces"].items():
        if any(_has(loc, n) for n in names) or re.search(r",\s*" + code.lower() + r"\b", loc):
            province_hit = code
            break
    region = None
    for reg, cities in cfg["regions"].items():
        for c in cities:
            if _has(loc, c):
                bad = cfg["ambiguous_cities"].get(c.split(",")[0], [])
                if any(b in loc for b in bad) and not (canada_named or province_hit):
                    continue
                region = reg
                break
        if region:
            break
    in_canada = bool(canada_named or province_hit or region)
    # A city match alone is enough only when no other country is named.
    if region and not (canada_named or province_hit) and re.search(r"\b(usa|united states|uk|united kingdom|india|germany|australia)\b", loc):
        in_canada, region = False, None
    if in_canada and not region:
        region = "Remote-Canada" if remote else "Other Canada"
    if not in_canada:
        return GeoResult(False, None, remote, False, f"not Canada: '{p.location_raw}'")
    if remote and region not in (None,) and not any(_has(loc, c) for cs in cfg["regions"].values() for c in cs):
        region = "Remote-Canada"
    return GeoResult(True, region, remote, True, f"Canada ({region}) from '{p.location_raw}'")
