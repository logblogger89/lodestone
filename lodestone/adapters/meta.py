"""Meta Careers (metacareers.com). The site loads jobs through its GraphQL endpoint. The query's
document id changes when Meta ships new front-end code, so we look it up from the page's scripts
each run instead of hard-coding it. One call returns every open job; we keep the Canadian ones."""
from __future__ import annotations

import json
import re

from ..http import BROWSER_UA, fetch, get_text
from ..models import Posting

PAGE = "https://www.metacareers.com/jobsearch/"
QUERY = "CareersJobSearchResultsDataQuery_candidate_portalRelayOperation"


class MetaAdapter:
    type = "meta"
    label = "Meta Careers"
    host = "www.metacareers.com"

    def _session(self) -> tuple[str, str]:
        html = get_text(PAGE, retries=2)
        lsd = re.search(r'"LSD",\[\],\{"token":"([^"]+)"', html)
        if not lsd:
            raise ValueError("Meta careers page layout changed: token not found")
        for js in sorted(set(re.findall(r'https://static\.xx\.fbcdn\.net/rsrc\.php/[^"]+\.js', html))):
            try:
                body = get_text(js, retries=0)
            except Exception:
                continue
            m = re.search(re.escape(QUERY) + r'",\[\],\(function\([^)]*\)\{a\.exports="(\d+)"', body)
            if m:
                return lsd.group(1), m.group(1)
        raise ValueError("Meta careers: job-search query id not found in page scripts")

    def list_feed(self, company: str, feed: dict) -> list[Posting]:
        lsd, doc_id = self._session()
        variables = {"isLoggedIn": False, "viewasUserID": None, "search_input": {
            "q": "", "divisions": [], "offices": [], "roles": [], "leadership_levels": [], "saved_jobs": [],
            "saved_searches": [], "sub_teams": [], "teams": [], "is_leadership": False,
            "is_remote_only": False, "sort_by_new": False, "results_per_page": None}}
        raw = fetch(f"https://{self.host}/graphql", retries=2,
                    headers={"User-Agent": BROWSER_UA, "x-fb-lsd": lsd},
                    form={"lsd": lsd, "doc_id": doc_id, "variables": json.dumps(variables)})
        jobs = json.loads(raw)["data"]["job_search_with_featured_jobs"]["all_jobs"]
        out = []
        for j in jobs:
            locs = j.get("locations") or []
            if not any(l.endswith(", Canada") for l in locs):
                continue                                   # keep the payload small: Canada only
            out.append(Posting(
                source=self.type, company=company, slug="meta", source_job_id=str(j["id"]),
                title=(j.get("title") or "").split(" | ")[0].strip(),   # drop the French title
                url=f"https://{self.host}/jobs/{j['id']}/", location_raw="; ".join(locs),
                department=", ".join(j.get("teams") or []),
            ))
        return out
