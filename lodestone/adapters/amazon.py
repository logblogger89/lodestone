"""Amazon Jobs (amazon.jobs/en/search.json): the JSON API behind the public search page.
Feed params: country (ISO-3, default "CAN")."""
from __future__ import annotations

import time
import urllib.parse

from ..http import get_json
from ..models import Posting
from ..text import html_to_text

PAGE = 100


class AmazonAdapter:
    type = "amazon"
    label = "Amazon Jobs"
    host = "www.amazon.jobs"

    def list_feed(self, company: str, feed: dict) -> list[Posting]:
        country = feed.get("country", "CAN")
        out, offset = [], 0
        while offset < 5000:
            q = urllib.parse.urlencode({"normalized_country_code[]": country, "result_limit": PAGE,
                                        "offset": offset, "sort": "recent"})
            d = get_json(f"https://{self.host}/en/search.json?{q}", retries=2)
            jobs = d.get("jobs") or []
            for j in jobs:
                desc = "\n\n".join(html_to_text(j.get(k) or "") for k in
                                   ("description", "basic_qualifications", "preferred_qualifications"))
                out.append(Posting(
                    source=self.type, company=company, slug="amazon", source_job_id=str(j.get("id_icims") or j.get("id")),
                    title=(j.get("title") or "").strip(), url=f"https://{self.host}{j.get('job_path', '')}",
                    location_raw=j.get("normalized_location") or j.get("location") or "",
                    country_hint="CA" if j.get("country_code") == "CAN" else j.get("country_code"),
                    department=j.get("job_category") or "", posted_at=j.get("posted_date"),
                    description=desc.strip(),
                    extra={"business": j.get("business_category"), "company_name": j.get("company_name")},
                ))
            offset += PAGE
            if not jobs or offset >= (d.get("hits") or 0):
                break
            time.sleep(0.5)
        return out
