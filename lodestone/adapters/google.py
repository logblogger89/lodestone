"""Google Careers (google.com/about/careers). No public API: the results page embeds its data as
JSON (AF_initDataCallback 'ds:1'), 20 jobs per page. Feed params: location (default "Canada")."""
from __future__ import annotations

import json
import re
import time
import urllib.parse

from ..http import get_text
from ..models import Posting
from ..text import html_to_text

BASE = "https://www.google.com/about/careers/applications/jobs/results"
_DS1 = re.compile(r"AF_initDataCallback\(\{key: 'ds:1'.*?data:(.*?), sideChannel: \{\}\}\);</script>", re.S)


def _slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _html(v) -> str:
    return html_to_text(v[1]) if isinstance(v, list) and len(v) > 1 and v[1] else ""


class GoogleAdapter:
    type = "google"
    label = "Google Careers"
    host = "www.google.com"

    def _page(self, location: str, page: int) -> list:
        q = urllib.parse.urlencode({"location": location, "page": page})
        m = _DS1.search(get_text(f"{BASE}?{q}", retries=2))
        if not m:
            raise ValueError("Google careers page layout changed: job data block not found")
        return json.loads(m.group(1))

    def list_feed(self, company: str, feed: dict) -> list[Posting]:
        location = feed.get("location", "Canada")
        out, page = [], 1
        while page <= 100:
            data = self._page(location, page)
            jobs = data[0] or []
            for j in jobs:
                locs = [l[0] for l in (j[9] or []) if l]
                countries = {l[5] for l in (j[9] or []) if l and len(l) > 5}
                desc = "\n\n".join(x for x in (_html(j[10]), _html(j[3]), _html(j[4]), _html(j[19])) if x)
                out.append(Posting(
                    source=self.type, company=company, slug="google", source_job_id=str(j[0]),
                    title=(j[1] or "").strip(), url=f"{BASE}/{j[0]}-{_slug(j[1] or '')}",
                    location_raw="; ".join(locs), country_hint="CA" if countries == {"CA"} else None,
                    posted_at=str(j[12][0]) if j[12] else None, description=desc,
                    extra={"all_countries": sorted(c for c in countries if c)},
                ))
            total = data[2] if len(data) > 2 and isinstance(data[2], int) else 0
            if not jobs or len(out) >= total:
                break
            page += 1
            time.sleep(0.5)
        return out
