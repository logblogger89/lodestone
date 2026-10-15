"""Careers-page reader: the fallback for companies with no job feed (D-043).

Two steps, so no paid API is needed:
1. `lodestone pages fetch` downloads each "page" source and saves a plain-text copy, keeping links
   as [text](url), under data/state/page_inbox/ (not committed).
2. Claude, in the /refresh-jobs session, reads each text file and records the open jobs with
   `lodestone pages save <company> <file.json>`. The `page` adapter then feeds them into the refresh
   like any other source.
"""
from __future__ import annotations

import html
import json
import re
import urllib.parse

from . import sources, store
from .http import get_text

INBOX = store.STATE / "page_inbox"
READS = "page_reads"
BROWSER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"}


def page_text(raw: str, base: str) -> str:
    """HTML -> readable text with absolute links, scripts and styles removed."""
    s = re.sub(r"(?is)<(script|style|noscript|svg|head)[^>]*>.*?</\1>", " ", raw)

    def link(m):
        href, label = m.group(1), re.sub(r"<[^>]+>", " ", m.group(2))
        label = " ".join(html.unescape(label).split())
        label = label.split('{"')[0].strip()             # drop embedded animation JSON
        if not label or href.startswith(("#", "javascript:", "mailto:")):
            return f" {label} "
        return f" [{label}]({urllib.parse.urljoin(base, html.unescape(href))}) "

    # Clickable cards often keep their link in a data attribute instead of an <a> tag.
    s = re.sub(r"""(?is)<[a-z]+\b[^>]*?\bdata-[a-z-]*url=["']([^"']+)["'][^>]*>""",
               lambda m: f" [link]({urllib.parse.urljoin(base, html.unescape(m.group(1)))}) ", s)
    s = re.sub(r"""(?is)<a\b[^>]*?href=(?:"([^"]*)"|'([^']*)'|([^\s>]+))[^>]*>(.*?)</a>""",
               lambda m: link(_M(m.group(1) or m.group(2) or m.group(3) or "", m.group(4))), s)
    s = re.sub(r"(?i)<\s*(br|/p|/li|/h\d|/div|/tr|/section|/article)\s*/?>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    lines = [" ".join(l.split()) for l in s.splitlines()]
    return "\n".join(l for l in lines if l and not (l.startswith('{"') and len(l) > 200))   # drop embedded JSON


class _M:
    """Adapter so link() can take (href, label) from either regex."""
    def __init__(self, href, label):
        self._g = (None, href, label)

    def group(self, i):
        return self._g[i]


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def fetch_all(log=print) -> list[dict]:
    INBOX.mkdir(parents=True, exist_ok=True)
    out = []
    for r in sources.load():
        if r["platform"] != "page" or r["status"] != "active":
            continue
        url = r["feed"]["url"]
        try:
            text = page_text(get_text(url, retries=1, headers=BROWSER), url)
            path = INBOX / f"{_slug(r['company'])}.txt"
            path.write_text(f"COMPANY: {r['company']}\nURL: {url}\n\n{text}\n")
            out.append({"company": r["company"], "file": str(path.relative_to(store.ROOT)), "chars": len(text)})
        except Exception as e:
            out.append({"company": r["company"], "error": f"{type(e).__name__}: {e}"[:200]})
    return out


def save(company: str, jobs: list[dict]) -> dict:
    """Record the jobs Claude read from a company's careers page. Each job: title, url, location."""
    clean = []
    for j in jobs:
        if not (j.get("title") and j.get("url")):
            raise ValueError(f"every job needs a title and url: {j}")
        clean.append({"title": j["title"].strip(), "url": j["url"].strip(), "location": (j.get("location") or "").strip()})
    reads = store.load(READS, {})
    reads[company] = {"read_at": store.now(), "jobs": clean}
    store.save(READS, reads)
    return {"company": company, "jobs": len(clean)}


_JSON_DESC = re.compile(r'"(?:description|jobDescription|content)"\s*:\s*"((?:[^"\\]|\\.){300,})"')
NO_DETAIL = {"meta", "workable", "shopify", "bamboohr", "page"}     # pages that need a browser or a login


def posting_text(url: str, platform: str) -> str:
    """Full text of one job posting, for job systems whose list view has no description.
    Prefers a description embedded as JSON in the page (Phenom, Coveo, Rippling), else the page text."""
    if platform in NO_DETAIL:
        return ""
    if platform == "icims" and "in_iframe" not in url:
        url += ("&" if "?" in url else "?") + "in_iframe=1"
    # CGI's Njoyn site challenges browser-like clients but serves plain requests.
    raw = get_text(url, retries=1, headers=False if platform == "njoyn" else BROWSER)
    best = ""
    for m in _JSON_DESC.finditer(raw):
        try:
            txt = json.loads('"' + m.group(1) + '"')
        except ValueError:
            continue
        from .text import html_to_text
        txt = html_to_text(txt)
        if len(txt) > len(best):
            best = txt
    if len(best) < 500:
        page = page_text(raw, url)
        best = page if len(page) > len(best) else best
    return "" if is_bot_check(best) else best[:30000]


_BOT = re.compile(r"you are a bot|are you a robot|verify you are human|just a moment|enable javascript and cookies|"
                  r"access denied|captcha", re.I)


def is_bot_check(text: str) -> bool:
    """A challenge or block page instead of the posting: never store it as a description."""
    return len(text) < 3000 and bool(_BOT.search(text))
