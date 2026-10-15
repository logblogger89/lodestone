"""Oracle Recruiting Cloud (Oracle HCM "Candidate Experience") careers sites: {host}/hcmRestApi.
Feed params: host, siteNumber, location (default "Canada"). The location search is radius-based and
can include US rows, so the Canada filter still runs on our side."""
from __future__ import annotations

import time
import urllib.parse

from ..http import get_json
from ..models import Posting
from ..text import html_to_text

PAGE = 25


class OracleHcmAdapter:
    type = "oracle_hcm"
    label = "Oracle Recruiting"
    host = "oraclecloud.com"

    def list_feed(self, company: str, feed: dict) -> list[Posting]:
        host, site = feed["host"], feed["siteNumber"]
        loc = feed.get("location", "Canada")
        out, offset = [], 0
        while offset < 2000:
            finder = (f"findReqs;siteNumber={site},limit={PAGE},offset={offset},"
                      f"location={urllib.parse.quote(loc)},sortBy=POSTING_DATES_DESC")
            url = (f"https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true"
                   f"&expand=requisitionList.secondaryLocations&finder={finder}")
            items = (get_json(url, retries=2).get("items") or [{}])[0]
            reqs = items.get("requisitionList") or []
            for r in reqs:
                locs = [r.get("PrimaryLocation")] + [s.get("Name") for s in r.get("secondaryLocations") or []]
                out.append(Posting(
                    source=self.type, company=company, slug=f"{host.split('.')[0]}/{site}", source_job_id=str(r["Id"]),
                    title=(r.get("Title") or "").strip(),
                    url=f"https://{host}/hcmUI/CandidateExperience/en/sites/{site}/job/{r['Id']}",
                    location_raw="; ".join(l for l in locs if l),
                    workplace=(r.get("WorkplaceType") or None), posted_at=r.get("PostedDate"),
                    extra={"detail_api": f"https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails"
                                         f"?expand=all&onlyData=true&finder=ById;Id=%22{r['Id']}%22,siteNumber={site}"},
                ))
            offset += PAGE
            if not reqs or offset >= (items.get("TotalJobsCount") or 0):
                break
            time.sleep(0.3)
        return out

    def detail(self, p: Posting) -> dict:
        it = (get_json(p.extra["detail_api"], retries=2).get("items") or [{}])[0]
        parts = (it.get("ExternalDescriptionStr"), it.get("ExternalResponsibilitiesStr"), it.get("ExternalQualificationsStr"))
        return {"description": "\n\n".join(html_to_text(x) for x in parts if x)}
