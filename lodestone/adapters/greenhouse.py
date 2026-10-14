"""Greenhouse public Job Board API: boards-api.greenhouse.io (no key needed)."""
from __future__ import annotations

from ..http import HttpError, get_json
from ..models import Posting
from ..text import html_to_text


class GreenhouseAdapter:
    type = "greenhouse"
    label = "Greenhouse"
    host = "boards-api.greenhouse.io"

    def fetch(self, slug: str) -> dict:
        return get_json(f"https://{self.host}/v1/boards/{slug}/jobs?content=true")

    def parse(self, payload: dict, company: str, slug: str) -> list[Posting]:
        out = []
        for j in payload.get("jobs", []):
            out.append(Posting(
                source=self.type, company=company, slug=slug,
                source_job_id=str(j.get("id")),
                title=(j.get("title") or "").strip(),
                url=j.get("absolute_url") or "",
                location_raw=((j.get("location") or {}).get("name") or "").strip(),
                department=", ".join(d.get("name", "") for d in j.get("departments") or []),
                posted_at=j.get("first_published") or j.get("updated_at"),
                description=html_to_text(j.get("content") or ""),
                extra={"offices": [o.get("name") for o in j.get("offices") or []]},
            ))
        return out

    def exists(self, slug: str) -> int | None:
        try:
            data = get_json(f"https://{self.host}/v1/boards/{slug}/jobs", retries=0)
        except HttpError:
            return None
        jobs = data.get("jobs") if isinstance(data, dict) else None
        return len(jobs) if isinstance(jobs, list) else None

    def list_jobs(self, company: str, slug: str) -> list[Posting]:
        return self.parse(self.fetch(slug), company, slug)
