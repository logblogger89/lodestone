"""Lever public Postings API: api.lever.co/v0/postings (no key needed)."""
from __future__ import annotations

from datetime import datetime, timezone

from ..http import HttpError, get_json
from ..models import Posting


class LeverAdapter:
    type = "lever"
    label = "Lever"
    host = "api.lever.co"

    def fetch(self, slug: str) -> list:
        return get_json(f"https://{self.host}/v0/postings/{slug}?mode=json")

    def parse(self, payload: list, company: str, slug: str) -> list[Posting]:
        out = []
        for j in payload or []:
            cats = j.get("categories") or {}
            created = j.get("createdAt")
            posted = datetime.fromtimestamp(created / 1000, tz=timezone.utc).isoformat() if created else None
            sr = j.get("salaryRange") or None
            pay = None
            if sr and (sr.get("min") or sr.get("max")):
                pay = {"min": sr.get("min"), "max": sr.get("max"), "currency": sr.get("currency"),
                       "interval": sr.get("interval"), "posted": True}
            locs = cats.get("allLocations") or ([cats.get("location")] if cats.get("location") else [])
            wp = (j.get("workplaceType") or "").lower() or None
            out.append(Posting(
                source=self.type, company=company, slug=slug,
                source_job_id=str(j.get("id")),
                title=(j.get("text") or "").strip(),
                url=j.get("hostedUrl") or "",
                location_raw="; ".join(l for l in locs if l),
                country_hint=(j.get("country") or None),
                remote_hint=(wp == "remote") if wp else None,
                workplace={"on-site": "onsite", "onsite": "onsite", "hybrid": "hybrid", "remote": "remote"}.get(wp or ""),
                department=cats.get("team") or cats.get("department") or "",
                posted_at=posted,
                description=(j.get("descriptionPlain") or "") + "\n" + "\n".join(
                    (l.get("text", "") + ":\n" + (l.get("content") or "")) for l in j.get("lists") or []),
                pay=pay,
            ))
        return out

    def exists(self, slug: str) -> int | None:
        try:
            data = get_json(f"https://{self.host}/v0/postings/{slug}?mode=json&limit=1", retries=0)
        except HttpError:
            return None
        if not isinstance(data, list):
            return None
        if not data:
            return 0
        full = get_json(f"https://{self.host}/v0/postings/{slug}?mode=json", retries=0)
        return len(full) if isinstance(full, list) else None

    def list_jobs(self, company: str, slug: str) -> list[Posting]:
        return self.parse(self.fetch(slug), company, slug)
