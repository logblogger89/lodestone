"""Immigration-pathway signals (R10, DR-3, CR-3/3a): employer-level evidence from ESDC's positive-LMIA employer
lists (open.canada.ca, quarterly), combined with what the posting itself says. Signals, not immigration advice.

  lodestone signals load   -> parse data/external/esdc/*.xlsx into data/state/signals.json (per watchlist company)

A positive LMIA means ESDC approved that employer to hire a foreign worker for a role. "Global Talent" is the fast
two-week stream for in-demand tech occupations. Not every employer that hires from abroad appears here: intra-company
transfers and other LMIA-exempt routes don't need an LMIA.
"""
from __future__ import annotations

import collections
import glob
import html
import json
import re
import zipfile

from . import pipeline, store
from .text import ascii_fold

DATASET_URL = "https://open.canada.ca/data/en/dataset/90fed587-1364-4f33-a9ee-208181dc0b97"
_LEGAL = {"inc", "incorporated", "ltd", "limited", "ltee", "ltée", "corp", "corporation", "co", "company", "ulc",
          "llc", "lp", "the", "canada", "canadian", "of", "and", "cie", "compagnie", "ltd.", "s.e.c", "sec", "lp."}
# NOC 2021 codes for professional, managerial and tech work (the kind of role Ayush applies to).
TECH_NOC = re.compile(r"^(0\d{4}|10\d{3}|11\d{3}|20\d{3}|21\d{3}|22\d{3}|41\d{3})")


def norm(name: str) -> str:
    s = ascii_fold(html.unescape(name or "")).lower().replace("&", " and ")
    s = re.sub(r"\(.*?\)", " ", s)
    words = re.findall(r"[a-z0-9]+", s)
    return " ".join(w for w in words if w not in _LEGAL)


def _rows(path: str):
    z = zipfile.ZipFile(path)
    ss = [html.unescape(re.sub(r"<[^>]+>", "", m)) for m in
          re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode("utf8"), re.S)]
    sheet = z.read("xl/worksheets/sheet1.xml").decode("utf8")
    for r in re.findall(r"<row[^>]*>(.*?)</row>", sheet, re.S):
        out = []
        for m in re.finditer(r'<c r="[A-Z]+\d+"([^>]*?)(?:/>|>(?:<f>[^<]*</f>)?(?:<v>([^<]*)</v>|<is><t[^>]*>([^<]*)</t></is>)?</c>)', r):
            v = m.group(2) or m.group(3) or ""
            if 't="s"' in m.group(1) and v:
                v = ss[int(v)]
            out.append(v.strip())
        yield out


# Brand names that are also ordinary words or other businesses' names: these match only through an alias.
GENERIC = {"apple", "block", "square", "later", "float", "zip", "maple", "league", "flare", "hopper", "jane app",
           "fable", "ada", "bell", "porter", "rogers", "solace", "mila", "karoo", "signal 1", "element", "wave",
           "propel holdings", "constellation software", "national bank", "visa", "intact", "indeed", "unity", "snap"}
# Words a legal name may add after the brand ("Snowflake Computing Canada ULC", "Salesforce.com Canada Corp.").
SUFFIXES = {"technologies", "technology", "tech", "computing", "com", "software", "systems", "labs", "payments",
            "platforms", "financial", "services", "solutions", "digital", "global", "international", "group", "hq",
            "operations", "development", "centre", "center", "research"}


def _match(emp_core: str, keys: dict[str, str], prefixes: dict[str, str]) -> str | None:
    if emp_core in keys:
        return keys[emp_core]
    words = emp_core.split()
    for n in range(len(words) - 1, 0, -1):               # longest brand prefix followed only by suffix words
        head, tail = " ".join(words[:n]), words[n:]
        if head in prefixes and all(w in SUFFIXES for w in tail):
            return prefixes[head]
    return None


def load(log=print) -> dict:
    aliases = json.loads((store.ROOT / "config" / "employer_aliases.json").read_text())
    names = [r["company"].strip() for r in pipeline.employers()]
    keys: dict[str, str] = {}
    prefixes: dict[str, str] = {}
    for n in names:
        core = norm(n)
        if core and core not in GENERIC and norm(n.split(" (")[0]) not in GENERIC:
            keys[core] = n
            if len(core) >= 4:
                prefixes[core] = n
        for a in aliases.get(n, []):
            keys[norm(a)] = n
    agg: dict[str, dict] = {}
    files = sorted(glob.glob(str(store.ROOT / "data" / "external" / "esdc" / "tfwp_*_pos_en.xlsx")))
    for f in files:
        quarter = re.search(r"tfwp_(\d{4}q\d)", f).group(1).upper()
        header = None
        for row in _rows(f):
            if header is None:
                if "Employer" in row:
                    header = {k: i for i, k in enumerate(row)}
                continue
            if len(row) < len(header):
                continue
            emp = row[header["Employer"]]
            company = _match(norm(emp), keys, prefixes)
            if not company:
                continue
            occ = row[header["Occupation"]]
            code = occ.split("-")[0].strip()
            try:
                pos = int(float(row[header.get("Approved Positions", header.get("Approved Positions ", 0))] or 0))
            except ValueError:
                pos = 0
            a = agg.setdefault(company, {"positions": 0, "tech_positions": 0, "streams": collections.Counter(),
                                         "quarters": set(), "occupations": collections.Counter(), "legal_names": set(),
                                         "provinces": set()})
            a["positions"] += pos
            if TECH_NOC.match(code):
                a["tech_positions"] += pos
                a["occupations"][occ] += pos
            a["streams"][re.sub(r"\s+", " ", row[header["Program Stream"]]).strip()] += pos
            a["quarters"].add(quarter)
            a["legal_names"].add(emp.strip())
            a["provinces"].add(row[header["Province/Territory"]].strip())
    quarters = [re.search(r"(\d{4}q\d)", f).group(1) for f in files]
    out = {"source": DATASET_URL, "files": [f.rsplit("/", 1)[-1] for f in files],
           "window": f"{min(quarters).upper()}–{max(quarters).upper()}" if files else "",
           "loaded_at": store.now(), "companies": {}}
    for c, a in agg.items():
        out["companies"][c] = {"positions": a["positions"], "tech_positions": a["tech_positions"],
                               "streams": dict(a["streams"]), "quarters": sorted(a["quarters"]),
                               "top_occupations": [o for o, _ in a["occupations"].most_common(4)],
                               "legal_names": sorted(a["legal_names"])[:5], "provinces": sorted(a["provinces"])}
    store.save("signals", out)
    store.mark_fresh("signals", window=out["window"], companies_with_lmias=len(out["companies"]))
    return {"window": out["window"], "companies_matched": len(out["companies"]),
            "with_tech_roles": sum(1 for v in out["companies"].values() if v["tech_positions"])}


ICT_COMPANIES = {"Google"}          # Ayush's current employer: intra-company transfer is LMIA-exempt (DR-3)
_NO_SPONSOR = re.compile(r"no sponsorship|without sponsorship|must be (legally )?(eligible|authori[sz]ed)|"
                         r"eligib\w* to work|work authori[sz]ation (is )?required|clearance", re.I)


def pathway_for(company: str, fit: dict | None, sig: dict | None, window: str) -> dict:
    """Combine what the posting says (from scoring) with employer evidence (ESDC). Returns the pathway
    sub-score used in the fit score and the signals shown in the app, each with status and source."""
    signals, score = [], None
    reason = ((fit or {}).get("reasons") or {}).get("pathway", "")
    claude = ((fit or {}).get("subs") or {}).get("pathway")
    if company in ICT_COMPANIES:
        signals.append({"label": "Intra-company transfer", "status": "Strong route",
                        "detail": "You work at Google today, so a transfer to Google Canada is LMIA-exempt (DR-3).",
                        "url": "https://www.canada.ca/en/immigration-refugees-citizenship/services/work-canada/hire-temporary-foreign/international-mobility-program/framework/intra-company-transferees.html"})
        score = 95
    if claude is not None and claude <= 20:
        signals.append({"label": "Posting limits who can apply", "status": "Stated", "detail": reason, "url": None})
        score = 15 if company not in ICT_COMPANIES else score
    elif claude is not None and claude >= 85 and "stated" in reason.lower():
        signals.append({"label": "Sponsorship or relocation offered", "status": "Stated", "detail": reason, "url": None})
        score = max(score or 0, 85)
    if sig:
        gts = sig["streams"].get("Global Talent Stream", 0)
        tech = sig["tech_positions"]
        detail = (f"{sig['positions']} position{'s' if sig['positions'] != 1 else ''} approved {window}"
                  f"{f', {gts} through the Global Talent Stream' if gts else ''}"
                  f"{'; tech roles include ' + ', '.join(o.split('-', 1)[1] for o in sig['top_occupations'][:2]) if sig['top_occupations'] else ''}.")
        signals.append({"label": "Hires from abroad (positive LMIAs)", "status": "Inferred", "detail": detail,
                        "url": DATASET_URL})
        esdc = 80 if (tech >= 10 or gts >= 5) else 70 if tech >= 1 else 55
        if score is None or (score not in (15,) and esdc > score):
            score = max(score or 0, esdc)
    if not signals:
        signals.append({"label": "No public signal", "status": "Unknown",
                        "detail": "Not on ESDC's positive-LMIA lists for " + window + ", and the posting doesn't mention sponsorship.",
                        "url": DATASET_URL})
    if score is None:
        score = 45          # no evidence either way (replaces the scorer's "large multinational" guess)
    return {"score": int(score), "signals": signals}
