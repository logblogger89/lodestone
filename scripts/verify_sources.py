"""Verify researched careers sites before adding them (D-080 wide net).

Each input file is a JSON list of {"company", "platform", "feed", "careers_url", "skip"} from source research.
Every entry is pulled with its adapter and counted: total postings, Canadian ones, and Canadian ones in a role family.
Usage: python3 scripts/verify_sources.py <out.json> <research.json> [...]
Then: python3 scripts/add_sources.py <out.json> <segments.json>
"""
import json, sys, concurrent.futures as cf
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
from lodestone import adapters, geo, rules, sources

def norm(r):
    p, f = r["platform"], dict(r.get("feed") or {})
    if p in ("bamboohr", "hibob", "workable") and "slug" in f and "subdomain" not in f:
        f["subdomain"] = f.pop("slug")
    if p == "ultipro" and "board_url" not in f:
        if f.get("tenant") and f.get("board"):
            f = {"board_url": f"https://{f.get('host','recruiting.ultipro.ca')}/{f['tenant']}/JobBoard/{f['board']}"}
        elif f.get("ukg"):
            f = {"board_url": f["ukg"]}
    if p == "page" and f.get("ukg"):
        p, f = "ultipro", {"board_url": f["ukg"]}
    return p, f

def check(r):
    p, f = norm(r)
    if p not in adapters.ADAPTERS or (p == "page" and not r.get("careers_url")):
        return r, p, f, None, None, None, "unsupported"
    if p == "page":
        return r, p, f, None, None, None, "page"
    try:
        posts = adapters.pull(p, r["company"], f)
    except Exception as e:
        return r, p, f, None, None, None, f"{type(e).__name__}: {str(e)[:120]}"
    ca = [x for x in posts if geo.classify(x).in_canada]
    biz = [x for x in ca if (c := rules.classify_title(x.title)) and c.family and not getattr(c, "excluded", False)]
    return r, p, f, len(posts), len(ca), len(biz), "ok"

rows = [r for fn in sys.argv[2:] for r in json.load(open(fn)) if not r.get("skip")]
have = {x["company"].lower() for x in sources.load()}
out = []
with cf.ThreadPoolExecutor(6) as ex:
    for r, p, f, tot, ca, biz, st in ex.map(check, rows):
        dup = r["company"].lower() in have
        print(f"{r['company'][:24]:24} {p:14} tot={tot} ca={ca} biz={biz} {st}{' DUP' if dup else ''}")
        out.append({**r, "platform": p, "feed": f, "total": tot, "ca": ca, "biz": biz, "status": st, "dup": dup})
json.dump(out, open(sys.argv[1], "w"), indent=1)
