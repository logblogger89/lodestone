"""Ashby public Job Postings API (official, no key): api.ashbyhq.com/posting-api."""
from __future__ import annotations

from ..http import HttpError, get_json
from ..models import Posting
from ..text import html_to_text


class AshbyAdapter:
    type = "ashby"
    label = "Ashby"
    host = "api.ashbyhq.com"

    def fetch(self, slug: str) -> dict:
        return get_json(f"https://{self.host}/posting-api/job-board/{slug}?includeCompensation=true")

    @staticmethod
    def _pay(comp: dict | None) -> dict | None:
        """Every salary tier the employer lists (often one per country), so the Canadian one can be featured."""
        if not comp:
            return None
        ranges = []
        for t in comp.get("compensationTiers") or []:
            for c in t.get("components") or []:
                if (c.get("compensationType") or "").lower() == "salary" and (c.get("minValue") or c.get("maxValue")):
                    ranges.append({"min": c.get("minValue"), "max": c.get("maxValue"), "currency": c.get("currencyCode"),
                                   "interval": c.get("interval"), "label": t.get("title") or None,
                                   "quote": t.get("tierSummary") or ""})
        if not ranges:
            for c in comp.get("summaryComponents") or []:
                if (c.get("compensationType") or "").lower() == "salary" and (c.get("minValue") or c.get("maxValue")):
                    ranges.append({"min": c.get("minValue"), "max": c.get("maxValue"), "currency": c.get("currencyCode"),
                                   "interval": c.get("interval"), "label": None,
                                   "quote": comp.get("compensationTierSummary") or ""})
        return {"ranges": ranges, "posted": True} if ranges else None

    def parse(self, payload: dict, company: str, slug: str) -> list[Posting]:
        out = []
        for j in (payload or {}).get("jobs", []):
            if j.get("isListed") is False:
                continue
            locs = [j.get("location") or ""] + [
                (s.get("location") or "") for s in j.get("secondaryLocations") or []]
            addr = ((j.get("address") or {}).get("postalAddress") or {})
            wp = (j.get("workplaceType") or "").lower()
            out.append(Posting(
                source=self.type, company=company, slug=slug,
                source_job_id=str(j.get("id")),
                title=(j.get("title") or "").strip(),
                url=j.get("jobUrl") or "",
                location_raw="; ".join(l for l in locs if l),
                country_hint=addr.get("addressCountry") or None,
                remote_hint=j.get("isRemote"),
                workplace={"onsite": "onsite", "hybrid": "hybrid", "remote": "remote"}.get(wp),
                department=j.get("department") or j.get("team") or "",
                posted_at=j.get("publishedAt"),
                description=j.get("descriptionPlain") or html_to_text(j.get("descriptionHtml") or ""),
                pay=self._pay(j.get("compensation")),
            ))
        return out

    def exists(self, slug: str) -> int | None:
        try:
            data = get_json(f"https://{self.host}/posting-api/job-board/{slug}", retries=0)
        except HttpError:
            return None
        jobs = data.get("jobs") if isinstance(data, dict) else None
        return len(jobs) if isinstance(jobs, list) else None

    def list_jobs(self, company: str, slug: str) -> list[Posting]:
        return self.parse(self.fetch(slug), company, slug)
