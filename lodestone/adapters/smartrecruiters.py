"""SmartRecruiters public Posting API (official): api.smartrecruiters.com/v1/companies/{id}/postings."""
from __future__ import annotations

from ..http import HttpError, get_json
from ..models import Posting


class SmartRecruitersAdapter:
    type = "smartrecruiters"
    label = "SmartRecruiters"
    host = "api.smartrecruiters.com"

    def fetch(self, slug: str) -> list:
        items, offset = [], 0
        while True:
            page = get_json(f"https://{self.host}/v1/companies/{slug}/postings?limit=100&offset={offset}")
            content = page.get("content") or []
            items += content
            offset += len(content)
            if not content or offset >= (page.get("totalFound") or 0) or offset >= 2000:
                return items

    def parse(self, payload: list, company: str, slug: str) -> list[Posting]:
        out = []
        for j in payload or []:
            loc = j.get("location") or {}
            parts = [loc.get("city"), loc.get("region"), (loc.get("country") or "").upper()]
            cid = (j.get("company") or {}).get("identifier") or slug
            out.append(Posting(
                source=self.type, company=company, slug=slug,
                source_job_id=str(j.get("id")),
                title=(j.get("name") or "").strip(),
                url=f"https://jobs.smartrecruiters.com/{cid}/{j.get('id')}",
                location_raw=", ".join(p for p in parts if p),
                country_hint=(loc.get("country") or None),
                remote_hint=loc.get("remote"),
                workplace="remote" if loc.get("remote") else ("hybrid" if loc.get("hybrid") else None),
                department=((j.get("department") or {}).get("label") or ""),
                posted_at=j.get("releasedDate"),
                description="",   # list endpoint has no description; fetched per job when scoring
                extra={"detail_api": j.get("ref")},
            ))
        return out

    def exists(self, slug: str) -> int | None:
        try:
            data = get_json(f"https://{self.host}/v1/companies/{slug}/postings?limit=1", retries=0)
        except HttpError:
            return None
        total = data.get("totalFound") if isinstance(data, dict) else None
        # Unknown company IDs return 200 with zero results, so require at least one posting.
        return total if isinstance(total, int) and total > 0 else None

    def list_jobs(self, company: str, slug: str) -> list[Posting]:
        return self.parse(self.fetch(slug), company, slug)
