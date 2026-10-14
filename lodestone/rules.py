"""Role-family rules (config/role_taxonomy.json). Cheap, transparent first filter before any AI scoring."""
from __future__ import annotations

import json
import pathlib
import re
from dataclasses import dataclass
from functools import lru_cache

from .text import norm_title

CONFIG = pathlib.Path(__file__).resolve().parent.parent / "config" / "role_taxonomy.json"


@dataclass
class RoleResult:
    tier: str | None        # Core | Adjacent | Stretch | None
    excluded: bool
    people_mgmt_hint: bool
    reason: str


@lru_cache(maxsize=1)
def _cfg() -> dict:
    raw = json.loads(CONFIG.read_text())
    comp = lambda xs: [re.compile(x) for x in xs]
    return {"exclude": comp(raw["exclude"]), "tiers": {k: comp(v) for k, v in raw["tiers"].items()},
            "people": comp(raw["people_management_hints"])}


def classify_title(title: str) -> RoleResult:
    t = norm_title(title)
    cfg = _cfg()
    people = any(p.search(t) for p in cfg["people"])
    for p in cfg["exclude"]:
        if p.search(t):
            return RoleResult(None, True, people, f"excluded by /{p.pattern}/")
    for tier, pats in cfg["tiers"].items():
        for p in pats:
            if p.search(t):
                return RoleResult(tier, False, people, f"{tier} via /{p.pattern}/")
    return RoleResult(None, False, people, "no role-family match")
