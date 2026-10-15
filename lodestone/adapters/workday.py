"""Workday careers sites: {tenant}.wd{N}.myworkdayjobs.com (the JSON API behind each site, no key).

Feed params: host, tenant, site, and optionally canada_facet ({facetParameter: [ids]}) and search
(keyword, for sites with no location filter). We ask Workday for Canada-only postings using its location-country
filter, read titles, and fetch the full posting (description, all locations) only for jobs that pass
the role rules (see pipeline.enrich), which keeps requests low for big employers.
"""
from __future__ import annotations

import time

from ..http import HttpError, get_json
from ..models import Posting
from ..text import html_to_text

PAGE = 20                      # Workday's maximum page size
MAX_JOBS = 3000


class WorkdayAdapter:
    type = "workday"
    label = "Workday"
    host = "myworkdayjobs.com"

    @staticmethod
    def _api(feed: dict) -> str:
        return f"https://{feed['host']}/wday/cxs/{feed['tenant']}/{feed['site']}"

    @staticmethod
    def _canada_facet(facets: list) -> tuple[str, str] | None:
        """Find (facetParameter, id) for Canada. Country facets are sometimes nested in a group."""
        stack = list(facets or [])
        while stack:
            f = stack.pop()
            param = f.get("facetParameter") or ""
            for v in f.get("values") or []:
                if "values" in v:                       # nested group, e.g. locationMainGroup
                    stack.append(v)
                elif (v.get("descriptor") or "").strip().lower() == "canada" and "country" in param.lower():
                    return param, v.get("id")
        return None

    def _page(self, feed, facets, offset, search=""):
        return get_json(self._api(feed) + "/jobs", retries=2, body={
            "appliedFacets": facets, "limit": PAGE, "offset": offset, "searchText": search})

    def list_feed(self, company: str, feed: dict) -> list[Posting]:
        first = self._page(feed, {}, 0, feed.get("search", ""))
        if feed.get("canada_facet"):          # set in the source index (country or Canadian city ids)
            facets = feed["canada_facet"]
        else:
            ca = self._canada_facet(first.get("facets"))
            facets = {ca[0]: [ca[1]]} if ca else {}
        country_known = bool(facets)          # every result of a Canada filter is in Canada
        items, offset, total = [], 0, None
        while True:
            page = self._page(feed, facets, offset, feed.get("search", "")) if (offset or facets) else first
            posts = page.get("jobPostings") or []
            if total is None:
                total = page.get("total") or 0
            items += posts
            offset += PAGE
            if not posts or offset >= min(total, MAX_JOBS):
                break
            time.sleep(0.3)
        key = f"{feed['tenant']}/{feed['site']}"
        out = []
        for j in items:
            path = j.get("externalPath") or ""
            jid = (j.get("bulletFields") or [path.rsplit("_", 1)[-1]])[0]
            out.append(Posting(
                source=self.type, company=company, slug=key, source_job_id=str(jid or path),
                title=(j.get("title") or "").strip(),
                url=f"https://{feed['host']}/en-US/{feed['site']}{path}",
                location_raw=j.get("locationsText") or "",
                country_hint="CA" if country_known else None,
                remote_hint=True if (j.get("remoteType") or "").lower() == "remote" else None,
                posted_at=j.get("postedOn"),
                extra={"detail_api": self._api(feed) + path},
            ))
        return out

    def detail(self, p: Posting) -> dict:
        info = get_json(p.extra["detail_api"], retries=2).get("jobPostingInfo") or {}
        locs = [info.get("location")] + list(info.get("additionalLocations") or [])
        return {"description": html_to_text(info.get("jobDescription") or ""),
                "location_raw": "; ".join(l for l in locs if l) or p.location_raw,
                "posted_at": info.get("startDate") or p.posted_at}

    def exists(self, feed: dict) -> int | None:
        try:
            return self._page(feed, {}, 0).get("total")
        except HttpError:
            return None
