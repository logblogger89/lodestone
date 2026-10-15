"""Jobs that Claude read from a careers page with no feed (see lodestone/pagereader.py).
Feed params: url. A page not read in the last day counts as a failed source, so its jobs are not
marked closed just because nobody read the page this time."""
from __future__ import annotations

import datetime as dt
import hashlib

from .. import store
from ..models import Posting

MAX_AGE = dt.timedelta(hours=24)


class PageAdapter:
    type, label, host = "page", "Careers page (read by Claude)", "page"

    def list_feed(self, company, feed):
        read = store.load("page_reads", {}).get(company)
        if not read:
            raise ValueError("careers page not read yet: run `lodestone pages fetch` and record the jobs")
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(read["read_at"])
        if age > MAX_AGE:
            raise ValueError(f"careers page last read {age.days}d ago: read it again this refresh")
        return [Posting(source=self.type, company=company, slug=company.lower().replace(" ", "-"),
                        source_job_id=hashlib.sha1(j["url"].encode()).hexdigest()[:12],
                        title=j["title"], url=j["url"], location_raw=j.get("location", ""))
                for j in read["jobs"]]
