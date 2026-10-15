"""Apple Jobs (jobs.apple.com). The search page embeds its results as JSON (React Router hydration
data), 20 per page. Feed params: location (default "canada-CANC")."""
from __future__ import annotations

import json
import re
import time

from ..http import get_text
from ..models import Posting

_DATA = re.compile(r'window.__staticRouterHydrationData = JSON.parse\((".*?")\);', re.S)


class AppleAdapter:
    type = "apple"
    label = "Apple Jobs"
    host = "jobs.apple.com"

    def list_feed(self, company: str, feed: dict) -> list[Posting]:
        loc = feed.get("location", "canada-CANC")
        out, page = [], 1
        while page <= 50:
            m = _DATA.search(get_text(f"https://{self.host}/en-ca/search?location={loc}&page={page}", retries=2))
            if not m:
                raise ValueError("Apple jobs page layout changed: data block not found")
            s = json.loads(json.loads(m.group(1)))["loaderData"]["search"]
            rows = s.get("searchResults") or []
            for j in rows:
                locs = j.get("locations") or []
                out.append(Posting(
                    source=self.type, company=company, slug="apple", source_job_id=str(j.get("positionId") or j.get("id")),
                    title=(j.get("postingTitle") or "").strip(),
                    url=f"https://{self.host}/en-ca/details/{j.get('positionId')}/{j.get('transformedPostingTitle', '')}",
                    location_raw="; ".join(", ".join(x for x in (l.get("city"), l.get("stateProvince"), l.get("countryName")) if x) for l in locs),
                    country_hint="CA" if all(l.get("countryName") == "Canada" for l in locs) and locs else None,
                    remote_hint=j.get("homeOffice") is True, department=(j.get("team") or {}).get("teamName", ""),
                    posted_at=j.get("postDateInGMT"), description=j.get("jobSummary") or "",
                ))
            if not rows or len(out) >= (s.get("totalRecords") or 0):
                break
            page += 1
            time.sleep(0.5)
        return out
