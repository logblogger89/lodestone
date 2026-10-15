"""Eightfold-powered careers sites (e.g. Microsoft: apply.careers.microsoft.com). JSON 'pcsx' API.
Feed params: host, domain, location (default "Canada"). The site rate-limits, so we go slowly."""
from __future__ import annotations

import time
import urllib.parse

from ..http import get_json

# Eightfold turns away requests whose user agent names a tool, so use a plain browser one.
UA = {"User-Agent": "Mozilla/5.0"}
from ..models import Posting
from ..text import html_to_text


class EightfoldAdapter:
    type = "eightfold"
    label = "Eightfold"
    host = "eightfold.ai"

    def list_feed(self, company: str, feed: dict) -> list[Posting]:
        host, domain = feed["host"], feed["domain"]
        out, start = [], 0
        while start < 3000:
            q = urllib.parse.urlencode({"domain": domain, "query": feed.get("query", ""),
                                        "location": feed.get("location", "Canada"), "start": start})
            d = (get_json(f"https://{host}/api/pcsx/search?{q}", retries=3, headers=UA) or {}).get("data") or {}
            pos = d.get("positions") or []
            for j in pos:
                out.append(Posting(
                    source=self.type, company=company, slug=domain, source_job_id=str(j.get("id")),
                    title=(j.get("name") or "").strip(),
                    url=f"https://{host}{j.get('positionUrl') or '/careers/job/' + str(j.get('id'))}",
                    location_raw="; ".join(j.get("locations") or []),
                    workplace=j.get("workLocationOption"), department=j.get("department") or "",
                    posted_at=str(j.get("postedTs") or ""),
                    extra={"detail_api": f"https://{host}/api/pcsx/position_details?"
                                         + urllib.parse.urlencode({"position_id": j.get("id"), "domain": domain})},
                ))
            start += len(pos)
            if not pos or start >= (d.get("count") or 0):
                break
            time.sleep(2)
        return out

    def detail(self, p: Posting) -> dict:
        time.sleep(1)
        d = (get_json(p.extra["detail_api"], retries=3, headers=UA) or {}).get("data") or {}
        return {"description": html_to_text(d.get("jobDescription") or "")}
