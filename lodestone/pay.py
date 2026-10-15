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


def pay_kind(sentence: str) -> str:
    """What a range covers, from the posting's own words: base | base_bonus | ote | total | unspecified."""
    low = sentence.lower()
    if re.search(r"on[- ]target|\bote\b|including commission|incl\.? commission|plus commission", low):
        return "ote"
    if re.search(r"total (target )?(cash|compensation)|inclusive of (an? )?(annual )?(performance )?bonus|"
                 r"includ(es|ing) (an? )?(annual )?(performance )?bonus|base (salary )?(plus|\+|and) (target )?bonus|"
                 r"salary and bonus|incl\.? bonus", low):
        return "total" if re.search(r"equity|stock|rsu", low) and "total" in low else "base_bonus"
    if re.search(r"\bbase\b|salary range|annual salary|base pay|hiring range|starting salary", low):
        return "base"
    return "unspecified"


def _kind_in_context(sentence: str, context: str) -> str:
    k = pay_kind(sentence)
    return k if k != "unspecified" or not context else pay_kind(context)


def _estimated(sentence: str) -> bool:
    return bool(re.search(r"\bestimated\b|\bexpected\b|approximate|anticipated", sentence, re.I))


# ---------- equity ----------
_DEI = re.compile(r"(diversity|inclusion|employment|pay|gender|racial|health|social|home|brand)[, ]+(and |& )?equity|"
                  r"equity[, ]+(diversity|inclusion|and inclusion|& inclusion)|\bequity[- ]deserving|\bpay equity|"
                  r"private equity|equity (research|markets?|capital markets|trading|derivatives|analyst|portfolio|investor|fund)|"
                  r"fixed income and equit|home equity|internal equity|equity (and|&) fairness|equitabl\\w*", re.I)
_EQ_WORD = re.compile(r"\b(equity|stock options?|share options?|rsus?|restricted stock|esop|employee stock|stock grants?|"
                      r"ownership stake|options? grant)\b", re.I)
_PCT = re.compile(r"(\d+(?:\.\d+)?)\s?%\s*(?:-|–|—|to)\s*(\d+(?:\.\d+)?)\s?%")
_SHARES = re.compile(r"(\d{1,3}(?:,\d{3})+|\d{3,7})\s*(?:-|–|—|to)\s*(\d{1,3}(?:,\d{3})+|\d{3,7})\s+(?:stock options|options|shares|rsus)", re.I)


def equity_from_text(text: str) -> dict | None:
    """Equity on offer: amounts when the posting states them, else just that it is offered.
    Diversity statements ("diversity, equity and inclusion", "pay equity") and finance jargon don't count."""
    found, amounts = None, []
    for s in _sentences(text or ""):
        clean = _DEI.sub(" ", s)
        if not _EQ_WORD.search(clean):
            continue
        if re.search(r"\b(no|not eligible for|does not include|excluding)\b[^.]{0,30}(equity|stock|options)", clean, re.I):
            continue
        if found is None or (not re.search(r"\bmay\b|eligible|applicable|potential", s, re.I)
                             and re.search(r"\bmay\b|eligible|applicable|potential", found, re.I)):
            found = s[:400]                                   # prefer a definite statement over a hedged one
        for m in _PCT.finditer(clean):
            a, b = float(m.group(1)), float(m.group(2))
            if 0 < a <= b <= 10:
                amounts.append({"min": a, "max": b, "unit": "percent", "quote": s[:400]})
        for m in _SHARES.finditer(clean):
            a, b = _amount(m.group(1)), _amount(m.group(2))
            if a and b and a <= b:
                amounts.append({"min": a, "max": b, "unit": "shares", "quote": s[:400]})
        if re.search(r"equity|rsu|stock|grant", clean, re.I) and not re.search(r"salary|base pay|base compensation|pay range", clean, re.I):
            for m in _RANGE.finditer(clean):
                if not any(m.group(g) for g in ("c1", "c2", "c3", "c4")):
                    continue
                a, b = _amount(m.group("a")), _amount(m.group("b"))
                if a and b and 1000 <= a <= b and re.search(r"(equity|rsu|stock|grant)[^.]{0,60}" + re.escape(m.group(0)[:6])
                                                          + r"|" + re.escape(m.group(0)[-6:]) + r"[^.]{0,40}(equity|rsu|stock|grant)",
                                                          clean, re.I):
                    amounts.append({"min": round(a), "max": round(b), "unit": "currency",
                                    "currency": _currency(m.group("c1"), m.group("c2"), m.group("c3"), m.group("c4"), sentence=s),
                                    "quote": s[:400]})
    if not found:
        return None
    maybe = bool(re.search(r"\bmay\b|eligible|where applicable|as applicable|potential", found, re.I)) and not amounts
    return {"offered": True, "certainty": "possible" if maybe else "offered", "amounts": amounts, "quote": found}


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
    recent: list[str] = []                                    # the lines just above: headings like "Base pay range"
    for s in _sentences(text or ""):
        context = " ".join(recent[-2:])
        recent.append(s)
        here = _label(s)
        if not re.search(r"\d", s) or not re.search(r"\$|USD|CAD|salary|compensation|pay|range|rate|wage", s, re.I):
            prev = here if here[0] else prev
            continue
        label, canada = here
        if re.search(r"\b(rsus?|restricted stock|stock options?|equity grant|share grant|shares)\b", s, re.I) and \
                not re.search(r"salary|base pay|base compensation", s, re.I):
            prev = here if here[0] else prev
            continue                                             # an equity grant, not cash pay
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
                        "label": label, "canada": is_ca, "kind": _kind_in_context(s, context),
                        "estimated": _estimated(s) or _estimated(context),
                        "quote": s[:400]})
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
    q = r.get("quote") or r.get("summary") or ""
    return {"min": r.get("min"), "max": r.get("max"), "currency": cur, "interval": iv, "label": label,
            "canada": canada, "kind": r.get("kind") or ("base" if re.search(r"base", q, re.I) else "unspecified"),
            "estimated": False, "quote": q}


def resolve(structured: dict | None, description: str, location: str, region: str | None) -> dict | None:
    """Structured salary fields win; otherwise ranges read from the description text. Equity comes from
    the job system's equity field when present, else from the text."""
    out = None
    if structured:
        raw = structured.get("ranges") or ([structured] if (structured.get("min") or structured.get("max")) else [])
        ranges = [_norm_field(r, location) for r in raw if r.get("min") or r.get("max")]
        if ranges:
            out = {"ranges": ranges, "primary": choose_primary(ranges, region), "source": "field"}
    if out is None:
        ranges = from_text(description)
        if ranges:
            out = {"ranges": ranges, "primary": choose_primary(ranges, region), "source": "text"}
    equity = (structured or {}).get("equity") or equity_from_text(description)
    if equity:
        out = out or {"ranges": [], "primary": None, "source": None}
        out["equity"] = equity
    return out
