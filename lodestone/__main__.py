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
    sc = sub.add_parser("score", help="fit scoring: prepare batches for Claude, or ingest Claude's results")
    sc.add_argument("action", choices=["prepare", "ingest"])
    sc.add_argument("file", nargs="?", help="results JSON (a list) for ingest")
    sc.add_argument("--batch", type=int, default=70)
    sg = sub.add_parser("signals", help="load ESDC positive-LMIA lists into per-company pathway signals")
    sg.add_argument("action", choices=["load"])
    ib = sub.add_parser("inbox", help="paste inbox: prepare pasted items for Claude, or add the jobs Claude read")
    ib.add_argument("action", choices=["prepare", "add"])
    ib.add_argument("file", help="inbox items (prepare) or job records (add), JSON list")
    mk = sub.add_parser("market", help="on-request levels.fyi pay check for one role (never during refresh)")
    mk.add_argument("action", choices=["fetch", "add", "pending"])
    mk.add_argument("target", help="job id, or words from company + title (fetch); folder of saved requests (pending)")
    mk.add_argument("level", nargs="?", help="company level that matches the role (add)")
    mk.add_argument("note", nargs="?", default="", help="why this level (add)")
    sub.add_parser("export", help="package jobs, companies and freshness for the app's database")
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
    elif a.cmd == "score":
        from . import scoring
        if a.action == "prepare":
            out = scoring.prepare(a.batch)
        else:
            if not a.file:
                ap.error("score ingest needs a results file")
            out = scoring.ingest(json.load(open(a.file)))
    elif a.cmd == "signals":
        from . import signals
        out = signals.load(log=log)
    elif a.cmd == "market":
        from . import market
        if a.action == "fetch":
            out = market.fetch(a.target)
        elif a.action == "pending":
            out = market.pending(a.target)
        else:
            if not a.level:
                ap.error("market add needs a job id and a level")
            out = market.add(a.target, a.level, a.note)
    elif a.cmd == "inbox":
        from . import capture
        data = json.load(open(a.file))
        out = capture.prepare(data) if a.action == "prepare" else capture.add(data)
    elif a.cmd == "export":
        from . import appexport
        out = appexport.write()
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
