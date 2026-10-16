"""On-request market pay checks from levels.fyi (D-054, Q-22).

levels.fyi's terms forbid automated reading and compiling datasets; its robots.txt allows fetches a person asks
for at that moment ("Claude-User"). So this module only runs when Ayush asks about a specific role in chat, reads
that one company page, and keeps the one level that matches the role (plus its neighbours for context). It never
runs during /refresh-jobs. Every figure is shown with the source, location, date and a link back (their
attribution rule).

  python3 -m lodestone market fetch "<job id, or words from company + title>"   -> reads the page, prints levels
  python3 -m lodestone market add <job id> <level> ["why this level"]          -> attaches the check to the role
  python3 -m lodestone market pending <folder>                                  -> app requests to answer (max daily_cap)
"""
from __future__ import annotations

import datetime as dt
import gzip
import json
import re
import urllib.request

from . import store
from .appexport import job_id

CONFIG = store.ROOT / "config" / "market.json"
FETCHED = store.STATE / "market_inbox"          # gitignored: their page text is read, not kept in the repo


def config() -> dict:
    return json.loads(CONFIG.read_text())


def slug(company: str, cfg: dict | None = None) -> str:
    cfg = cfg or config()
    if company in cfg.get("company_slugs", {}):
        return cfg["company_slugs"][company]
    return re.sub(r"[^a-z0-9]+", "-", company.lower().replace("&", "and")).strip("-")


def family(title: str, cfg: dict | None = None) -> str:
    cfg = cfg or config()
    for pat, fam in cfg["families"]:
        if re.search(pat, title or "", re.I):
            return fam
    return "product-manager"


def parse(md: str) -> dict:
    """Read a levels.fyi salary .md page: location, currency, date and the per-level median total pay."""
    get = lambda pat: (m.group(1).strip() if (m := re.search(pat, md)) else None)
    levels = []
    for name, val in re.findall(r"^\|\s*([^|]+?)\s*\|\s*(?:CA)?\$([\d,]+)\s*\|\s*$", md, re.M):
        levels.append({"level": name, "median_total": int(val.replace(",", ""))})
    cur = get(r"\*\*Currency:\*\*\s*(\w+)")
    return {"location": get(r"\*\*Location:\*\*\s*(.+)"), "currency": cur, "updated": get(r"Last Updated:\s*(.+)"),
            "page_url": get(r"\*\*URL:\*\*\s*(\S+)"), "levels": levels}


def _get(url: str, ua: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=30) as r:
        b = r.read()
    try:
        b = gzip.decompress(b)
    except OSError:
        pass
    return b.decode("utf-8", "replace")


def find(query: str) -> list[tuple[str, dict]]:
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    if re.fullmatch(r"[0-9a-f]{12}", query):
        return [(job_id(k), j) for k, j in jobs.items() if job_id(k) == query]
    words = query.lower().split()
    return [(job_id(k), j) for k, j in jobs.items() if j.get("live") and j.get("role_tier")
            and all(w in f"{j['company']} {j['title']}".lower() for w in words)]


def fetch(query: str, *, getter=_get) -> dict:
    hits = find(query)
    if len(hits) != 1:
        return {"status": "pick_one" if hits else "not_found",
                "matches": [{"id": i, "company": j["company"], "title": j["title"], "location": j.get("location")} for i, j in hits[:15]]}
    jid, j = hits[0]
    cfg = config()
    store.log_today("market_log", jid)               # counts toward the daily cap, whatever the answer
    locs = [cfg["locations"].get(j.get("region") or "", cfg["locations"]["default"]), cfg["locations"]["default"]]
    tried = []
    for loc in dict.fromkeys(locs):
        url = cfg["url"].format(company=slug(j["company"], cfg), family=family(j["title"], cfg), location=loc)
        try:
            page = parse(getter(url, cfg["user_agent"]))
        except Exception as e:                       # 404: company or family not on levels.fyi
            tried.append({"url": url, "result": str(e)[:80]})
            continue
        if page["currency"] != "CAD" or not page["levels"]:
            tried.append({"url": url, "result": "no Canadian data (levels.fyi showed US figures)"})
            continue
        FETCHED.mkdir(parents=True, exist_ok=True)
        (FETCHED / f"{jid}.json").write_text(json.dumps({**page, "fetched_at": _now()}, indent=1))
        return {"status": "ok", "id": jid, "company": j["company"], "title": j["title"], "job_location": j.get("location"),
                "level_guess": store.load("scores", {}).get(jid, {}).get("level_guess"), **page}
    return {"status": "no_data", "id": jid, "tried": tried}


def add(jid: str, level: str, note: str = "") -> dict:
    """Attach the chosen level (and its neighbours) from the page fetched for this role."""
    p = FETCHED / f"{jid}.json"
    if not p.exists():
        return {"status": "fetch_first"}
    page = json.loads(p.read_text())
    names = [x["level"] for x in page["levels"]]
    if level not in names:
        return {"status": "unknown_level", "levels": names}
    i = names.index(level)
    checks = store.load("market_checks", {})
    checks[jid] = {"source": "levels.fyi", "page_url": page["page_url"], "location": page["location"],
                   "currency": page["currency"], "metric": "median total pay (base + stock + bonus)",
                   "updated": page["updated"], "checked_at": page["fetched_at"], "level": level,
                   "median_total": page["levels"][i]["median_total"],
                   "neighbours": page["levels"][max(0, i - 1):i] + page["levels"][i + 1:i + 2], "note": note}
    store.save("market_checks", checks)
    return {"status": "added", "id": jid, **checks[jid]}


def pending(folder: str) -> dict:
    """Requests saved from the app (`ArtifactData list market_req` with out_dir), oldest first. The cap is per day
    (New York time) across all runs: roles already read today count against it."""
    from pathlib import Path
    reqs = []
    for f in sorted(Path(folder).rglob("*.json")):
        d = json.loads(f.read_text())
        d = d.get("data", d) if isinstance(d, dict) else {}
        if d.get("status") == "requested":
            reqs.append({"id": f.stem, **{k: d.get(k) for k in ("company", "title", "requested_at")}})
    reqs.sort(key=lambda r: r.get("requested_at") or "")
    done = store.count_today("market_log")
    cap = max(0, config().get("daily_cap", 20) - done)
    return {"process": reqs[:cap], "deferred": [r["id"] for r in reqs[cap:]], "read_today": done}


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
