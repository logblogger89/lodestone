"""Role-family rules (config/role_taxonomy.json, D-076). Cheap, transparent first filter before any AI scoring.

Every job gets one absolute family ("Business analysis" is the same for everyone). How close that family is to a
person is relative to the families they picked: their own (Core), a related one (Adjacent) or a stretch (Stretch).
`role_tier` on stored jobs is that closeness for the default families (the first user's), kept for older readers."""
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
    tier: str | None        # Core | Adjacent | Stretch | None, relative to the default families
    excluded: bool
    people_mgmt_hint: bool
    reason: str
    family: str | None = None   # absolute family id, e.g. "ba"


@lru_cache(maxsize=1)
def _cfg() -> dict:
    raw = json.loads(CONFIG.read_text())
    comp = lambda xs: [re.compile(x) for x in xs]
    return {"exclude": comp(raw["exclude"]), "families": [(f["id"], comp(f["patterns"])) for f in raw["families"]],
            "people": comp(raw["people_management_hints"]), "raw": raw}


def families() -> list[dict]:
    """The family list as configured (id, label, tag, what, onboard, patterns, related, stretch, pay)."""
    return [dict(f) for f in _cfg()["raw"]["families"]]


def groups() -> list[str]:
    """Headings the app groups role types under (setup cards, Profile)."""
    return list(_cfg()["raw"].get("groups") or [])


def default_families() -> list[str]:
    return list(_cfg()["raw"].get("default_families") or ["pm"])


def closeness(family: str | None, mine: list[str] | None = None) -> str | None:
    """Core if the family is one of `mine`, Adjacent if related to one of them, Stretch if a stretch, else None."""
    if not family:
        return None
    mine = list(mine or default_families())
    if family in mine:
        return "Core"
    fams = {f["id"]: f for f in _cfg()["raw"]["families"]}
    if any(family in fams.get(m, {}).get("related", []) for m in mine):
        return "Adjacent"
    if any(family in fams.get(m, {}).get("stretch", []) for m in mine):
        return "Stretch"
    return None


def family_of(title: str) -> tuple[str | None, str]:
    t = norm_title(title)
    for fid, pats in _cfg()["families"]:
        for p in pats:
            if p.search(t):
                return fid, p.pattern
    return None, ""


def classify_title(title: str) -> RoleResult:
    t = norm_title(title)
    cfg = _cfg()
    people = any(p.search(t) for p in cfg["people"])
    fam, pat = family_of(title)
    for p in cfg["exclude"]:
        if p.search(t):
            return RoleResult(None, True, people, f"excluded by /{p.pattern}/", fam)
    if not fam:
        return RoleResult(None, False, people, "no role-family match")
    return RoleResult(closeness(fam) or "Other", False, people, f"{fam} via /{pat}/", fam)
