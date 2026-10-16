"""Years of experience a posting asks for (D-064), read straight from the posting text.

Returns {"min": 8, "max": None, "quote": "...8+ years of product management experience..."} or None. When a posting
gives several numbers ("8+ years of product management", "3+ years leading teams"), the one about product work wins,
then the main requirement over "preferred" ones, then the largest.
"""
from __future__ import annotations

import re

_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
          "eleven": 11, "twelve": 12, "fifteen": 15}
_N = r"(\d{1,2}|" + "|".join(_WORDS) + r")"
_YEARS = re.compile(
    rf"(?:minimum of |at least |over |more than |)\b{_N}(?:\s*\(\d{{1,2}}\))?\s*(?:\+|plus)?\s*"
    rf"(?:(?:-|–|—|to)\s*{_N}\s*\+?\s*)?(?:or more\s+)?years?\b", re.I)
_EXPERIENCE = re.compile(r"experience|track record|background in|working (in|as|on)|in (a|an) .{0,40}role", re.I)
_NOT_REQ = re.compile(r"years? (old|ago|in business|history)|for (over |more than )?\d+ years|since \d{4}|"
                      r"founded|anniversary|warranty|\bage\b|contract", re.I)
_PRODUCT = re.compile(r"\bproduct\b|\bpm\b", re.I)
_PREFERRED = re.compile(r"prefer|nice to have|bonus|ideally|plus\b", re.I)


def _num(s: str | None) -> int | None:
    if not s:
        return None
    return int(s) if s.isdigit() else _WORDS.get(s.lower())


def _sentences(text: str):
    for line in (text or "").splitlines():
        for s in re.split(r"(?<=[.;])\s+", line):
            if s.strip():
                yield s.strip()


def years_required(text: str) -> dict | None:
    found = []
    for s in _sentences(text):
        if not re.search(r"years?", s, re.I):
            continue
        for m in _YEARS.finditer(s):
            after = s[m.end(): m.end() + 90]
            before = s[max(0, m.start() - 40): m.start()]
            lead_in = re.match(r"\s*(?:’|')?\s*(of|in|managing|leading|working|building|as|doing|across)\b", after, re.I)
            if not (_EXPERIENCE.search(after + " " + before) or lead_in) or _NOT_REQ.search(s[max(0, m.start() - 30): m.end() + 30]):
                continue
            lo, hi = _num(m.group(1)), _num(m.group(2))
            if not lo or lo > 25 or (hi and (hi < lo or hi > 30)):
                continue
            found.append({"min": lo, "max": hi, "quote": s[:300],
                          "_product": bool(_PRODUCT.search(after)), "_preferred": bool(_PREFERRED.search(s))})
    if not found:
        return None
    found.sort(key=lambda f: (not f["_product"], f["_preferred"], -f["min"]))
    best = found[0]
    return {"min": best["min"], "max": best["max"], "quote": best["quote"]}
