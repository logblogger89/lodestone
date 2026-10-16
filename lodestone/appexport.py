"""Package refresh results for the Lodestone app (the Artifact's `db`, P1-S2).

`python3 -m lodestone export` writes one JSON file per database document under
data/state/app_export/<collection>/<doc>.json and prints the list. Claude then writes them with one
ArtifactData `batch` (max 50 documents, 1 MiB), so jobs are packed into a few bucket documents
instead of one document per job. Triage, pipeline, settings and the paste inbox are written by the
app itself and never by this export.
"""
from __future__ import annotations

import hashlib
import json
import shutil

from . import pipeline, sources, store
from .experience import years_required

OUT = store.STATE / "app_export"
BUCKETS = 8                     # ~70 jobs per document, well under the 256 KiB document limit
DESC_BUCKETS = 32               # job descriptions (D-065): ~120 KB each, loaded only when a role is opened


def job_id(key: str) -> str:
    """Stable, path-safe id for a job (canonical keys can contain '/')."""
    return hashlib.sha1(key.encode()).hexdigest()[:12]


def _job(key: str, j: dict) -> dict:
    labels = sources.PLATFORM_LABELS
    return {
        "id": job_id(key), "company": j["company"], "title": j["title"], "location": j.get("location") or "",
        "region": j.get("region"), "remote": bool(j.get("remote")), "workplace": j.get("workplace"),
        "tier": j.get("role_tier"), "people_mgmt": bool(j.get("people_mgmt_hint")),
        "department": (j.get("department") or "")[:80], "pay": j.get("pay"), "pay_checked": bool(j.get("pay_checked")), "posted_at": j.get("posted_at"),
        "first_seen": j.get("first_seen"), "last_seen": j.get("last_seen"), "live": bool(j.get("live", True)),
        "closed_at": j.get("closed_at"),
        "captured": bool(j.get("captured")),
        "years": years_required(j.get("description") or ""),
        "sources": [{"label": s.get("label") or labels.get(s["source"], s["source"]), "url": s["url"], "live": s.get("live", True)}
                    for s in j["sightings"]],
    }


def build() -> dict[str, dict[str, dict]]:
    jobs = store.load("jobs", {"jobs": {}})["jobs"]
    scores = store.load("scores", {})
    from . import payest
    from . import signals as sigmod
    estimates = payest.build()
    market = store.load("market_checks", {})
    sigs = store.load("signals", {"companies": {}, "window": ""})
    from . import jdsections
    docs: dict[str, dict[str, dict]] = {"jobs": {}, "meta": {}, "desc": {f"d{i:02d}": {"jobs": {}} for i in range(DESC_BUCKETS)}}
    abouts: dict[str, list] = {}
    buckets = {f"b{i}": {} for i in range(BUCKETS)}
    for key, j in jobs.items():
        if not j.get("role_tier") or j.get("role_excluded"):
            continue
        rec = _job(key, j)
        sc = scores.get(rec["id"])
        if rec["id"] in estimates:
            rec["pay"] = {**(rec["pay"] or {"ranges": [], "primary": None, "source": None}), "estimate": estimates[rec["id"]]}
        if rec["id"] in market:
            rec["pay"] = {**(rec["pay"] or {"ranges": [], "primary": None, "source": None}), "market": market[rec["id"]]}
        rec["pathway"] = sigmod.pathway_for(j["company"], sc, sigs["companies"].get(j["company"]), sigs.get("window", ""))
        if sc:
            rec["fit"] = {k: sc[k] for k in ("subs", "reasons", "summary", "level_guess", "people_mgmt", "work_mode",
                                             "must_haves", "flags", "scored_at", "rubric")}
        buckets[f"b{int(rec['id'], 16) % BUCKETS}"][rec["id"]] = rec
        desc = j.get("description") or ""
        if j.get("live") and len(desc) > 200:
            app = jdsections.for_app(desc)
            team = jdsections.team_about(desc)
            docs["desc"][desc_bucket(rec["id"])]["jobs"][rec["id"]] = {
                "text": app["text"], "truncated": app["truncated"], "has_legal": bool(app["legal"]),
                "team": {"heading": team[0], "text": team[1]} if team else None, "read_at": j.get("last_seen")}
            abouts.setdefault(j["company"], []).append(jdsections.company_about(desc, j["company"]))
    for b, items in buckets.items():
        docs["jobs"][b] = {"jobs": items}

    runs = store.load("runs", {"components": {}})["components"]
    docs["meta"]["freshness"] = {"components": runs}

    seg = {r["company"].strip(): r.get("segment", "") for r in pipeline.employers()}
    rows = []
    for name, rs in sorted(sources.by_company(sources.load()).items(), key=lambda kv: kv[0].lower()):
        best = next((r for r in rs if r["status"] == "active"), rs[0])
        rows.append({"name": name, "segment": seg.get(name, ""),
                     "system": sources.PLATFORM_LABELS.get(best["platform"], best["platform"]),
                     "status": best["status"], "canada_jobs": best.get("canada_jobs") or None,
                     "careers_url": best.get("careers_url") or "", "note": (best.get("notes") or "")[:160]})
    docs["meta"]["companies"] = {"companies": rows}
    written = json.loads((store.ROOT / "data" / "companies" / "summaries.json").read_text())["companies"]
    profiles = {}
    for name in set(abouts) | set(written):
        own = jdsections.best_company_about(abouts.get(name, []), name)
        if own:
            profiles[name] = {"about": own, "source": "posting"}
        elif name in written:
            profiles[name] = {"about": written[name], "source": "claude"}
    docs["meta"]["company_profiles"] = {"companies": profiles}
    hist = store.load("eval_history", {"runs": []})["runs"]
    last = lambda k: next((r for r in reversed(hist) if r.get("kind") == k), None)
    docs["meta"]["eval"] = {"reading": last("reading"), "ranking": last("ranking"),
                            "history": [{k: r.get(k) for k in ("at", "kind", "pairwise", "interested_in_top25", "accuracy")}
                                        for r in hist[-30:]]}
    return docs


def desc_bucket(jid: str) -> str:
    return f"d{int(jid, 16) % DESC_BUCKETS:02d}"


def write() -> list[dict]:
    """Writes every document and marks which changed since the last export (`changed`), so a push can skip the large
    description documents that didn't change."""
    import hashlib
    docs = build()
    shutil.rmtree(OUT, ignore_errors=True)
    before = store.load("export_hashes", {})
    hashes, out = {}, []
    for coll, items in docs.items():
        (OUT / coll).mkdir(parents=True, exist_ok=True)
        for doc_id, body in items.items():
            path = OUT / coll / f"{doc_id}.json"
            text = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
            path.write_text(text)
            h = hashlib.sha1(text.encode()).hexdigest()[:16]
            hashes[f"{coll}/{doc_id}"] = h
            out.append({"collection": coll, "doc_id": doc_id, "file": str(path), "bytes": len(text.encode()),
                        "changed": before.get(f"{coll}/{doc_id}") != h})
    store.save("export_hashes", hashes)
    return out
