"""Pay ranges (R5, D-045): read every range a posting states, and pick the Canadian one.

Sources, in order of trust: a structured salary field from the job system, else ranges written in the
description text (common since Ontario's pay-transparency rules, Jan 2026). Postings often state several
ranges (e.g. NYC, other US, Ontario); all are kept, each with its region label and the sentence it came
from, and `canada` marks the one to feature. Lodestone never converts currencies (B8: pay shown as posted).

Result shape: {"ranges": [{min, max, currency, interval, label, canada, quote}], "primary": index|None,
               "source": "field"|"text"}   or None when nothing was found.
"""
from __future__ import annotations

import re

_NUM = r"\d{1,3}(?:[,\s.]\d{3})+(?:\.\d{2})?|\d+(?:\.\d+)?\s?[kK]|\d{2,7}(?:\.\d{2})?"
_CUR = r"US\$|USD\s?\$?|C\$|CA\$|CAD\s?\$?|CDN\s?\$?|\$|£|€"
_RANGE = re.compile(
    rf"(?P<c1>{_CUR})?\s?(?P<a>{_NUM})\s?(?P<c2>USD|CAD|CDN)?\s*(?:-|–|—|to|and)\s*"
    rf"(?P<c3>{_CUR})?\s?(?P<b>{_NUM})\s?(?P<c4>USD|CAD|CDN)?(?![\d%])", re.I)

CANADA = ["canada", "canadian", "ontario", "toronto", "waterloo", "ottawa", "british columbia", "vancouver",
          "quebec", "québec", "montreal", "montréal", "alberta", "calgary", "edmonton", "nova scotia",
          "manitoba", "winnipeg", "saskatchewan", "new brunswick", "newfoundland", " gta"]
US = ["united states", "u.s.", " us ", "usa", "new york", "nyc", "san francisco", "california", "seattle",
      "washington", "texas", "austin", "boston", "chicago", "colorado", "los angeles", "irvine", "mclean",
      "virginia", "illinois", "massachusetts", "us-based", "us location", "eligible us"]


def _amount(s: str) -> float | None:
    s = s.strip().replace(" ", "")
    k = s[-1:].lower() == "k"
    s = s.rstrip("kK")
    if re.fullmatch(r"\d{1,3}(?:[,.]\d{3})+(?:\.\d{2})?", s):
        if re.search(r"\.\d{2}$", s) and s.count(".") == 1 and "," in s:
            s = s.replace(",", "")
        else:
            s = re.sub(r"[,.](?=\d{3}(\D|$))", "", s)
    try:
        v = float(s.replace(",", ""))
    except ValueError:
        return None
    return v * 1000 if k else v


def _currency(*tags: str | None, sentence: str = "") -> str | None:
    t = " ".join(x or "" for x in tags).upper()
    if "US" in t:
        return "USD"
    if any(x in t for x in ("CAD", "C$", "CA$", "CDN")):
        return "CAD"
    low = f" {sentence.lower()} "
    if any(w in low for w in CANADA):
        return "CAD"
    if any(w in low for w in US):
        return "USD"
    return None


def _label(sentence: str) -> tuple[str | None, bool | None]:
    """A short region label from the sentence, and whether it is Canadian (None = no region named)."""
    low = f" {sentence.lower()} "
    m = re.search(r"\b(?:for|in)\s+((?:[A-Z][\w.'-]*(?:,?\s+(?:and/or\s+|and\s+)?)?){1,8})", sentence)
    named = m.group(1).strip(" ,") if m else None
    if any(w in low for w in CANADA):
        hit = next((w.strip() for w in CANADA if w in low and w.strip() not in ("canada", "canadian")), None)
        label = named if named and any(w in named.lower() for w in CANADA) else (hit.title() + ", Canada" if hit else "Canada")
        return label, True
    if any(w in low for w in US):
        if re.search(r"\bany\b|\bother\b|unless", low):
            return "Other US locations", False
        cities = [c for c in US_CITIES if c.lower() in low]
        if cities:
            return ", ".join(cities[:3]) + (" +" + str(len(cities) - 3) if len(cities) > 3 else ""), False
        if named and len(named) <= 60:
            return named, False
        return "United States", False
    return None, None


US_CITIES = ["New York", "San Francisco", "Seattle", "Los Angeles", "Irvine", "McLean", "Washington",
             "Boston", "Chicago", "Austin", "Denver", "Atlanta", "Dallas", "Bellevue", "Sunnyvale", "Mountain View"]


def _interval(sentence: str, lo: float) -> str:
    low = sentence.lower()
    if re.search(r"per hour|/\s?h(ou)?r|hourly|an hour", low) or lo < 300:
        return "hour"
    if re.search(r"per month|/\s?mo|monthly", low):
        return "month"
    return "year"


def _plausible(lo: float, hi: float, interval: str) -> bool:
    if hi < lo:
        return False
    if interval == "hour":
        return 15 <= lo <= 400 and hi <= 600
    if interval == "month":
        return 2000 <= lo <= 60000
    return 30000 <= lo <= 1500000 and hi <= 2500000 and hi / lo < 4


def _sentences(text: str):
    for line in text.splitlines():
        for s in re.split(r"(?<=\.)\s+(?=[A-Z])", line):
            if s.strip():
                yield s.strip()


def from_text(text: str) -> list[dict]:
    out, seen = [], set()
    prev = (None, None)
    for s in _sentences(text or ""):
        here = _label(s)
        if not re.search(r"\d", s) or not re.search(r"\$|USD|CAD|salary|compensation|pay|range|rate|wage", s, re.I):
            prev = here if here[0] else prev
            continue
        label, canada = here
        if label is None and re.search(r"\b(those|these|above|listed)\b", s, re.I):
            label, canada = prev                                  # "...in any of those locations"
        prev = here if here[0] else prev
        for m in _RANGE.finditer(s):
            lo, hi = _amount(m.group("a")), _amount(m.group("b"))
            if lo is None or hi is None:
                continue
            if m.group("a").lower().endswith("k") is False and m.group("b").lower().endswith("k") and lo < 1000:
                lo *= 1000                                          # "$140-175K"
            has_cur = any(m.group(g) for g in ("c1", "c2", "c3", "c4"))
            if not has_cur and not re.search(r"salary|compensation|pay|wage|base", s, re.I):
                continue                                            # bare number pairs (years, team sizes)
            iv = _interval(s, lo)
            if not _plausible(lo, hi, iv):
                continue
            cur = _currency(m.group("c1"), m.group("c2"), m.group("c3"), m.group("c4"), sentence=s)
            key = (lo, hi, cur, label)
            if key in seen:
                continue
            seen.add(key)
            is_ca = canada if canada is not None else (True if cur == "CAD" else None)
            if is_ca and not label:
                label = "Canada"
            out.append({"min": round(lo), "max": round(hi), "currency": cur, "interval": iv,
                        "label": label, "canada": is_ca, "quote": s[:300]})
    return out


PLACE_WORDS = {"GTA": ["toronto", "gta", "ontario"], "Waterloo Region": ["waterloo", "kitchener", "ontario"],
               "Ottawa": ["ottawa", "ontario"], "Montreal": ["montreal", "montréal", "quebec", "québec"],
               "Vancouver": ["vancouver", "british columbia"], "Calgary": ["calgary", "alberta"],
               "Edmonton": ["edmonton", "alberta"]}


def choose_primary(ranges: list[dict], region: str | None, in_canada: bool = True) -> int | None:
    """The range to feature: the job's own province, else any Canadian range, else an unlabeled
    non-USD range on a Canadian job. US-only postings have no primary (shown as 'US range only')."""
    if not ranges:
        return None
    for word in PLACE_WORDS.get(region or "", []):           # most specific place first
        for i, r in enumerate(ranges):
            if r.get("canada") and word in (r.get("label") or "").lower():
                return i
    for i, r in enumerate(ranges):
        if r.get("canada"):
            return i
    if in_canada:
        for i, r in enumerate(ranges):
            if r.get("canada") is None and r.get("currency") != "USD":
                return i
    return None


def _norm_field(r: dict, location: str) -> dict:
    cur = (r.get("currency") or "").upper() or None
    iv = str(r.get("interval") or "year").lower()
    iv = "hour" if "hour" in iv else "month" if "month" in iv else "year"
    label = r.get("label")
    low = f" {(label or '').lower()} "
    canada = True if (cur == "CAD" or any(w in low for w in CANADA)) else (False if cur == "USD" or any(w in low for w in US) else None)
    if canada and not label:
        label = "Canada"
    return {"min": r.get("min"), "max": r.get("max"), "currency": cur, "interval": iv, "label": label,
            "canada": canada, "quote": r.get("quote") or r.get("summary") or ""}


def resolve(structured: dict | None, description: str, location: str, region: str | None) -> dict | None:
    """Structured salary fields win; otherwise ranges read from the description text."""
    if structured:
        raw = structured.get("ranges") or ([structured] if (structured.get("min") or structured.get("max")) else [])
        ranges = [_norm_field(r, location) for r in raw if r.get("min") or r.get("max")]
        if ranges:
            return {"ranges": ranges, "primary": choose_primary(ranges, region), "source": "field"}
    ranges = from_text(description)
    if not ranges:
        return None
    return {"ranges": ranges, "primary": choose_primary(ranges, region), "source": "text"}
