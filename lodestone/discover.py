"""Company discovery (P1-S5, ENG_DESIGN §6, DR-5). Finds employers that aren't on the watchlist, proves each with
evidence, and suggests them to Ayush in the app. Nothing joins the watchlist until he approves it.

Routes (each candidate keeps every route that found it):
  lmia     ESDC positive-LMIA lists: employers with tech/product hires (>= MIN_TECH positions or any Global Talent Stream)
  capture  companies of jobs Ayush pasted into the inbox
  search   web search for Canadian role-family postings on hosted job boards (Claude runs the searches)
  vc       Canadian VC / ecosystem portfolio boards (Claude reads the boards)

  python3 -m lodestone discover harvest                 -> lmia + capture candidates into data/state/discovery.json
  python3 -m lodestone discover add <candidates.json>   -> search/vc candidates found by Claude: [{name, route, evidence, url?}]
  python3 -m lodestone discover probe [--limit N]       -> find each candidate's job board, count open Canadian role matches
  python3 -m lodestone discover review <reviews.json>   -> Claude's verdicts: [{key, name?, segment, kind, verdict, why}]
  python3 -m lodestone discover export                  -> meta/suggestions for the app
  python3 -m lodestone discover apply <decisions dir>   -> Ayush's approvals join the watchlist (+ source index)
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import csv
import glob
import json
import re

from . import adapters, pipeline, signals, sources, store
from .adapters import ADAPTERS
from .geo import classify
from .rules import classify_title

STATE = "discovery"
GETRO_API = "https://api.getro.com/api/v2/collections/{id}/search/companies"
CANADA = re.compile(r"\b(canada|ontario|quebec|québec|british columbia|alberta|nova scotia|manitoba|saskatchewan|new brunswick|"
                    r"toronto|waterloo|kitchener|ottawa|montr[eé]al|vancouver|calgary|edmonton|halifax|winnipeg)\b|, (ON|QC|BC|AB|NS|MB|SK|NB)\b", re.I)


SIZE = {1: "1–10 staff", 2: "11–50 staff", 3: "51–200 staff", 4: "201–1,000 staff", 5: "1,000+ staff"}


def settings() -> dict:
    return json.loads((store.ROOT / "config" / "discovery.json").read_text())


MIN_TECH = settings()["lmia_min_tech_hires"]
MIN_GTS = settings()["lmia_min_global_talent"]
# NOC 2021 codes where product, program and engineering hires land (PMs are often filed as 20012 or 21221).
PRODUCT_NOC = re.compile(r"^(20012|21211|21221|21222|21223|21231|21232|21233|21234|21311|10019|10022|11202)")
VERDICTS = ("suggest", "skip")          # skip: IT staffing / consultancy body shop, government, not a product employer


def key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", signals.norm(name)).strip("-")


def _load() -> dict:
    return store.load(STATE, {"candidates": {}, "updated_at": None})


def _save(d: dict) -> None:
    d["updated_at"] = store.now()
    store.save(STATE, d)


def _matcher():
    """Same name matching as the pathway signals: aliases, and legal names that add suffix words
    ("Snowflake Computing Canada ULC" is Snowflake)."""
    names = [r["company"].strip() for r in store.read_seed()]
    aliases = json.loads((store.ROOT / "config" / "employer_aliases.json").read_text())
    keys, prefixes = {}, {}
    for n in names:
        for v in (n, n.split(" (")[0]):
            core = signals.norm(v)
            if core:
                keys[core] = n
                if len(core) >= 4 and core not in signals.GENERIC:
                    prefixes[core] = n
        for a in aliases.get(n, []):
            keys[signals.norm(a)] = n
    return lambda name: signals._match(signals.norm(name), keys, prefixes)


def on_watchlist(name: str, _m=[]) -> str | None:
    if not _m:
        _m.append(_matcher())
    return _m[0](name)


def _merge(d: dict, name: str, route: str, evidence: str, **extra) -> None:
    k = key(name)
    if not k or on_watchlist(name):
        return
    c = d["candidates"].setdefault(k, {"name": name, "routes": {}, "status": "new", "first_found": store.now()})
    c["routes"][route] = evidence
    for f, v in extra.items():
        if v is not None:
            c[f] = v


def _lmia() -> dict[str, dict]:
    """Employers on the positive-LMIA lists that aren't on the watchlist, with product-relevant tech hires."""
    agg = collections.defaultdict(lambda: {"tech": 0, "gts": 0, "prov": collections.Counter(), "occ": collections.Counter(),
                                           "q": set(), "legal": collections.Counter()})
    for f in sorted(glob.glob(str(store.ROOT / "data" / "external" / "esdc" / "tfwp_*_pos_en.xlsx"))):
        quarter = re.search(r"(\d{4}q\d)", f).group(1).upper()
        h = None
        for row in signals._rows(f):
            if h is None:
                if "Employer" in row:
                    h = {k: i for i, k in enumerate(row)}
                continue
            if len(row) < len(h):
                continue
            emp, occ = row[h["Employer"]], row[h["Occupation"]]
            if not PRODUCT_NOC.match(occ.split("-")[0].strip()):
                continue
            k = key(emp)
            if not k or on_watchlist(emp):
                continue
            try:
                pos = int(float(row[h.get("Approved Positions", 0)] or 0))
            except ValueError:
                pos = 0
            a = agg[k]
            a["tech"] += pos
            a["occ"][occ.split("-", 1)[-1].strip()] += pos
            a["q"].add(quarter)
            a["legal"][emp.strip()] += pos
            a["gts"] += pos if "talent" in row[h["Program Stream"]].lower() else 0
            a["prov"][row[h["Province/Territory"]].strip()] += pos
    out = {}
    for k, a in agg.items():
        if a["tech"] >= MIN_TECH or a["gts"] >= MIN_GTS:
            legal = a["legal"].most_common(1)[0][0]
            prov = ", ".join(p for p, _ in a["prov"].most_common(2))
            out[k] = {"name": legal, "provinces": [p for p, _ in a["prov"].most_common(3)],
                      "evidence": f"{a['tech']} approved tech/product hires {min(a['q'])}–{max(a['q'])}"
                                  + (f" ({a['gts']} via Global Talent Stream)" if a["gts"] else "") + f"; {prov}; "
                                  f"top roles: {', '.join(o for o, _ in a['occ'].most_common(2))}",
                      "lmia_tech": a["tech"], "lmia_gts": a["gts"]}
    return out


def harvest() -> dict:
    d = _load()
    before = len(d["candidates"])
    lm = _lmia()
    for k, v in lm.items():
        _merge(d, v["name"], "lmia", v["evidence"], provinces=v["provinces"], lmia_tech=v["lmia_tech"], lmia_gts=v["lmia_gts"])
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    for j in jobs.values():
        if j.get("captured"):
            _merge(d, j["company"], "capture", f"You pasted a role: {j['title']}")
    _save(d)
    return {"lmia_candidates": len(lm), "total_candidates": len(d["candidates"]), "new": len(d["candidates"]) - before}


def _getro(board: dict, log=print) -> list[dict]:
    """All companies on a Getro board, via the same public search the board page uses."""
    import time
    import urllib.request
    from . import http
    page = http.get_text(board["url"].rstrip("/") + "/companies")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S)
    cid = json.loads(m.group(1))["props"]["pageProps"]["network"]["id"]
    out, n = [], 0
    while True:
        req = urllib.request.Request(GETRO_API.format(id=cid), method="POST",
                                     data=json.dumps({"hitsPerPage": 20, "page": n, "filters": "", "query": ""}).encode(),
                                     headers={"Content-Type": "application/json", "Accept": "application/json",
                                              "User-Agent": http.BROWSER_UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.loads(r.read())["results"]
        out += res["companies"]
        n += 1
        if not res["companies"] or len(out) >= res.get("count", 0) or n >= 50:
            break
        time.sleep(1)                                   # the boards ask for a 1-second crawl delay
    log(f"{board['name']}: {len(out)} companies")
    return out


def harvest_vc(log=print) -> dict:
    cfg = settings()
    d = _load()
    before, kept, errors = len(d["candidates"]), 0, {}
    for b in cfg["vc_boards"]:
        try:
            comps = _getro(b, log)
        except Exception as e:
            errors[b["name"]] = str(e)[:120]
            continue
        for c in comps:
            locs = c.get("locations") or []
            if not any(CANADA.search(l) for l in locs) or (c.get("head_count") or 0) < cfg["vc_min_size_band"] \
                    or not c.get("active_jobs_count"):
                continue
            ca = [l for l in locs if CANADA.search(l)]
            _merge(d, c["name"], "vc", f"{b['name']} portfolio; {SIZE.get(c.get('head_count'), 'size unknown')}; {c['active_jobs_count']} open jobs; "
                                       f"{', '.join(ca[:2])}", careers_url=f"{b['url'].rstrip('/')}/companies/{c.get('slug')}",
                   domain=c.get("domain"), about=(c.get("description") or "")[:240])
            kept += 1
    _save(d)
    return {"vc_companies_kept": kept, "new_candidates": len(d["candidates"]) - before, "errors": errors}


def add(items: list[dict]) -> dict:
    d = _load()
    n = 0
    for it in items:
        if it.get("name") and it.get("route") in ("search", "vc", "capture", "lmia"):
            _merge(d, it["name"], it["route"], it.get("evidence", ""), careers_url=it.get("url"))
            n += 1
    _save(d)
    return {"added_or_updated": n, "total_candidates": len(d["candidates"])}


def _probe_one(c: dict) -> dict:
    """Find a hosted job board for this name and count its open Canadian role-family matches."""
    names = [c["name"], signals.norm(c["name"]).title()] + ([c["brand"]] if c.get("brand") else [])
    for n in dict.fromkeys(names):
        ats, slug, conf = pipeline._detect_one(n)
        if ats:
            break
    if not ats:
        return {"board": None}
    try:
        posts = adapters.pull(ats, c.get("brand") or c["name"], {"slug": slug})
    except Exception as e:
        return {"board": {"platform": ats, "slug": slug, "confidence": conf}, "probe_error": str(e)[:120]}
    ca = [p for p in posts if classify(p).in_canada]
    roles = [p for p in ca if (r := classify_title(p.title)).tier and not r.excluded]
    return {"board": {"platform": ats, "slug": slug, "confidence": conf}, "jobs_total": len(posts), "jobs_canada": len(ca),
            "roles_canada": len(roles), "sample_roles": [f"{p.title} ({p.location_raw})"[:90] for p in roles[:4]]}


def probe(limit: int | None = None, only_new: bool = True) -> dict:
    d = _load()
    todo = [(k, c) for k, c in d["candidates"].items() if c["status"] in ("new", "reviewed") and (not only_new or "probed_at" not in c)]
    todo.sort(key=lambda kc: -(kc[1].get("lmia_tech") or 0))
    todo = todo[:limit] if limit else todo
    with cf.ThreadPoolExecutor(pipeline.WORKERS) as ex:
        for (k, c), res in zip(todo, ex.map(lambda kc: _probe_one(kc[1]), todo)):
            c.update(res, probed_at=store.now())
    _save(d)
    found = [c for _, c in todo if c.get("board")]
    return {"probed": len(todo), "with_board": len(found), "with_canadian_roles": sum(1 for c in found if c.get("roles_canada"))}


def review(items: list[dict]) -> dict:
    d = _load()
    n = 0
    for it in items:
        c = d["candidates"].get(it.get("key"))
        if not c or it.get("verdict") not in VERDICTS:
            continue
        c.update({f: it[f] for f in ("segment", "kind", "why", "brand", "careers_url") if it.get(f)})
        c["verdict"], c["status"] = it["verdict"], "reviewed" if it["verdict"] == "suggest" else "skipped"
        if it.get("brand"):
            c["display"] = it["brand"]
        n += 1
    _save(d)
    return {"reviewed": n}


def suggestions() -> list[dict]:
    d = _load()
    out = []
    for k, c in d["candidates"].items():
        if c["status"] != "reviewed":
            continue
        out.append({"key": k, "name": c.get("display") or c["name"], "legal_name": c["name"], "segment": c.get("segment", ""),
                    "why": c.get("why", ""), "routes": c["routes"], "provinces": c.get("provinces", []),
                    "board": c.get("board"), "roles_canada": c.get("roles_canada"), "sample_roles": c.get("sample_roles", []),
                    "careers_url": c.get("careers_url") or ""})
    out.sort(key=lambda s: (-(s["roles_canada"] or 0), -len(s["routes"]), s["name"].lower()))
    return out


def export() -> dict:
    out = store.STATE / "app_export" / "meta"
    out.mkdir(parents=True, exist_ok=True)
    s = suggestions()
    (out / "suggestions.json").write_text(json.dumps({"suggestions": s, "updated_at": store.now()}, ensure_ascii=False))
    return {"suggestions": len(s), "file": str(out / "suggestions.json")}


def apply(folder: str) -> dict:
    """Ayush's decisions from the app (`company_decisions` docs saved with ArtifactData list out_dir)."""
    from pathlib import Path
    d = _load()
    seed_rows = store.read_seed()
    rows = sources.load()
    approved, dismissed = [], []
    for f in sorted(Path(folder).rglob("*.json")):
        dec = json.loads(f.read_text())
        dec = dec.get("data", dec) if isinstance(dec, dict) else {}
        c = d["candidates"].get(f.stem)
        if not c or c["status"] in ("approved", "dismissed"):
            continue
        if dec.get("decision") == "dismiss":
            c["status"] = "dismissed"
            dismissed.append(f.stem)
        elif dec.get("decision") == "approve":
            name = c.get("display") or c["name"]
            seed_rows.append({"company": name, "segment": c.get("segment") or "Discovered", "canada_locations": "; ".join(c.get("provinces", [])),
                              "fit_tier": "B", "why_relevant": (c.get("why") or "")[:120],
                              "discovery_source": "discover-" + "+".join(sorted(c["routes"]))})
            b = c.get("board")
            if b and b.get("confidence") == "high":
                rows.append({"company": name, "platform": b["platform"], "feed": {"slug": b["slug"]}, "status": "active",
                             "verified_at": store.now()[:10], "found_by": "discovery", "careers_url": c.get("careers_url") or "",
                             "notes": "Approved by Ayush from discovery"})
            c["status"] = "approved"
            approved.append(name)
    if approved:
        with store.SEED.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(seed_rows[0].keys()))
            w.writeheader()
            w.writerows(seed_rows)
        sources.save(rows)
    _save(d)
    return {"approved": approved, "dismissed": len(dismissed),
            "needs_source_research": [n for n in approved if not any(r["company"] == n for r in rows)]}
