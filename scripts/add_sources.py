"""Add verified sources to the source index and the watchlist seed in one step (D-080).

Only for companies Ayush asked to add directly (the wide net); everything else goes through discovery and his
approval in the app. Input: the output of verify_sources.py, filtered to the rows to add, plus
{company: [segment, one-line why]}. Companies already on the watchlist are skipped.
Usage: python3 scripts/add_sources.py <verified.json> <segments.json>
"""
import csv, json, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
from lodestone import sources, store

ver, seg = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
rows, seed = sources.load(), store.read_seed()
have = {r["company"].lower() for r in rows} | {r["company"].lower() for r in seed}
added = []
for r in ver:
    name = r["company"]
    if name not in seg or name.lower() in have:
        continue
    s, why = seg[name]
    rows.append({"company": name, "platform": r["platform"], "feed": r["feed"], "careers_url": r.get("careers_url") or "",
                 "status": "active", "canada_jobs": r.get("ca") if r.get("ca") is not None else "",
                 "total_jobs": r.get("total") if r.get("total") is not None else "", "verified_at": store.now()[:10],
                 "found_by": "research", "notes": ("Wide net wave 2 (D-080). " + (r.get("notes") or ""))[:300]})
    seed.append({"company": name, "segment": s, "canada_locations": "", "fit_tier": "B", "why_relevant": why[:120],
                 "discovery_source": "wide-net-D080"})
    have.add(name.lower()); added.append(name)
with store.SEED.open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(seed[0].keys())); w.writeheader(); w.writerows(seed)
sources.save(rows)
print(len(added), added)
