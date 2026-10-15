"""CLI: python3 -m lodestone {detect,refresh,stats}. Used by the /refresh-jobs skill."""
from __future__ import annotations

import argparse
import json
import sys

from . import pipeline


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="lodestone")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect", help="auto-detect hosted job boards for companies not yet in the source index")
    d.add_argument("--redo", action="store_true", help="re-probe companies already detected")
    r = sub.add_parser("refresh", help="pull all sources, keep Canadian roles, dedup, update liveness")
    r.add_argument("--only", help="limit to one company name or one platform (for testing a source)")
    sub.add_parser("stats", help="print current counts and freshness")
    pg = sub.add_parser("pages", help="careers-page reader: fetch pages, or save the jobs read from one")
    pg.add_argument("action", choices=["fetch", "save"])
    pg.add_argument("company", nargs="?")
    pg.add_argument("file", nargs="?", help="JSON list of {title, url, location}")
    sub.add_parser("index", help="rewrite data/sources/README.md, the readable source index")
    a = ap.parse_args(argv)
    log = lambda m: print(m, file=sys.stderr)
    if a.cmd == "detect":
        out = pipeline.detect(redo=a.redo, log=log)
    elif a.cmd == "refresh":
        out = pipeline.refresh(only=a.only, log=log)
    elif a.cmd == "pages":
        from . import pagereader
        if a.action == "fetch":
            out = pagereader.fetch_all(log=log)
        else:
            if not (a.company and a.file):
                ap.error("pages save needs a company and a JSON file")
            out = pagereader.save(a.company, json.load(open(a.file)))
    elif a.cmd == "index":
        from . import sources, store
        path = sources.INDEX.parent / "README.md"
        path.write_text(sources.render_markdown(sources.load(), pipeline.employers()))
        out = {"written": str(path.relative_to(sources.ROOT))}
    else:
        out = pipeline.stats()
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
