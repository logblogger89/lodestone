"""Smaller hosted job systems whose public feeds are a single simple request. One class per system;
feed params come from the source index. Descriptions are included when the feed carries them."""
from __future__ import annotations

import threading
import time
import urllib.parse
import xml.etree.ElementTree as ET

from ..http import fetch, get_json
from ..models import Posting
from ..text import html_to_text

UA = {"User-Agent": "Mozilla/5.0"}
# Workable's bot filter rate-limits short user agents from cloud IPs.
CHROME_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}


def _p(adapter, company, key, jid, title, url, loc, **kw) -> Posting:
    return Posting(source=adapter.type, company=company, slug=key, source_job_id=str(jid),
                   title=(title or "").strip(), url=url or "", location_raw=loc or "", **kw)


class GemAdapter:
    """Gem job boards (jobs.gem.com/{slug}); Greenhouse-like schema."""
    type, label, host = "gem", "Gem", "api.gem.com"

    def list_feed(self, company, feed):
        out = []
        for j in get_json(f"https://{self.host}/job_board/v0/{feed['slug']}/job_posts/", retries=2) or []:
            locs = [(j.get("location") or {}).get("name")] + [(o.get("location") or {}).get("name") for o in j.get("offices") or []]
            out.append(_p(self, company, feed["slug"], j["id"], j.get("title"), j.get("absolute_url"),
                          "; ".join(dict.fromkeys(l for l in locs if l)), workplace=j.get("location_type"),
                          posted_at=j.get("first_published_at"),
                          description=j.get("content_plain") or html_to_text(j.get("content") or "")))
        return out


class RipplingAdapter:
    """Rippling ATS boards (ats.rippling.com/{slug})."""
    type, label, host = "rippling", "Rippling ATS", "api.rippling.com"

    def list_feed(self, company, feed):
        rows = get_json(f"https://{self.host}/platform/api/ats/v1/board/{feed['slug']}/jobs", retries=2) or []
        return [_p(self, company, feed["slug"], j["uuid"], j.get("name"), j.get("url"),
                   (j.get("workLocation") or {}).get("label"), department=(j.get("department") or {}).get("label", ""))
                for j in rows]


class BambooHRAdapter:
    """BambooHR careers pages ({sub}.bamboohr.com/careers)."""
    type, label, host = "bamboohr", "BambooHR", "bamboohr.com"

    def list_feed(self, company, feed):
        sub = feed["subdomain"]
        rows = (get_json(f"https://{sub}.bamboohr.com/careers/list", retries=2) or {}).get("result") or []
        out = []
        for j in rows:
            loc = j.get("location") or {}
            ats = j.get("atsLocation") or {}
            where = ", ".join(x for x in (loc.get("city") or ats.get("city"), loc.get("state") or ats.get("province") or ats.get("state"), ats.get("country")) if x)
            out.append(_p(self, company, sub, j["id"], j.get("jobOpeningName"), f"https://{sub}.bamboohr.com/careers/{j['id']}",
                          where, remote_hint=bool(j.get("isRemote")) or None, department=j.get("departmentLabel") or ""))
        return out


class JazzHRAdapter:
    """JazzHR ({sub}.applytojob.com) XML job feed."""
    type, label, host = "jazzhr", "JazzHR", "app.jazz.co"

    def list_feed(self, company, feed):
        root = ET.fromstring(fetch(f"https://{self.host}/feeds/export/jobs/{feed['subdomain']}", retries=2))
        out = []
        for j in root.iter("job"):
            g = lambda t: (j.findtext(t) or "").strip()
            if g("status") and g("status").lower() != "open":
                continue
            out.append(_p(self, company, feed["subdomain"], g("id"), g("title"), g("url"),
                          ", ".join(x for x in (g("city"), g("state"), g("country")) if x),
                          department=g("department"), description=html_to_text(g("description"))))
        return out


class HiBobAdapter:
    """HiBob careers sites ({sub}.careers.hibob.com)."""
    type, label, host = "hibob", "HiBob", "careers.hibob.com"

    _lock = threading.Lock()                 # one Workable request at a time, spaced out

    def list_feed(self, company, feed):
        sub = feed["subdomain"]
        with self._lock:
            time.sleep(8)
            d = get_json(f"https://{sub}.{self.host}/api/job-ad", retries=2, headers={"companyidentifier": sub})
        out = []
        for j in d.get("jobAdDetails") or []:
            pay = None
            if j.get("payTransparencyMinSalary"):
                pay = {"min": j.get("payTransparencyMinSalary"), "max": j.get("payTransparencyMaxSalary"),
                       "currency": j.get("payTransparencySalaryCurrency"), "interval": j.get("payTransparencySalaryPayPeriod"), "posted": True}
            out.append(_p(self, company, sub, j["id"], j.get("title"), f"https://{sub}.{self.host}/jobs/{j['id']}",
                          ", ".join(x for x in (j.get("site"), j.get("country")) if x),
                          workplace=(j.get("workspaceTypeId") or None), department=j.get("department") or "",
                          posted_at=j.get("publishedAt"), pay=pay, description=html_to_text(j.get("description") or "")))
        return out


class ADPAdapter:
    """ADP Workforce Now career centers. Feed params: cid, ccId."""
    type, label, host = "adp", "ADP Workforce Now", "workforcenow.adp.com"

    def list_feed(self, company, feed):
        base = f"https://{self.host}/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions"
        out, skip = [], 0
        while skip < 1000:
            q = urllib.parse.urlencode({"cid": feed["cid"], "ccId": feed.get("ccId", "19000101_000001"),
                                        "lang": "en_CA", "locale": "en_CA", "$top": 50, "$skip": skip})
            d = get_json(f"{base}?{q}", retries=2)
            rows = d.get("jobRequisitions") or []
            for j in rows:
                locs = [(l.get("nameCode") or {}).get("shortName", "").strip() for l in j.get("requisitionLocations") or []]
                pr = j.get("payGradeRange") or {}
                pay = None
                if (pr.get("minimumRate") or {}).get("amountValue"):
                    pay = {"min": pr["minimumRate"]["amountValue"], "max": (pr.get("maximumRate") or {}).get("amountValue"),
                           "currency": pr["minimumRate"].get("currencyCode"), "interval": "year", "posted": True}
                url = (f"https://{self.host}/mascsr/default/mdf/recruitment/recruitment.html?"
                       + urllib.parse.urlencode({"cid": feed["cid"], "ccId": feed.get("ccId", "19000101_000001"),
                                                 "jobId": j["itemID"], "lang": "en_CA"}))
                out.append(_p(self, company, feed["cid"][:8], j["itemID"], j.get("requisitionTitle"), url,
                              "; ".join(l for l in locs if l), posted_at=j.get("postDate"), pay=pay))
            skip += len(rows)
            if not rows or skip >= ((d.get("meta") or {}).get("totalNumber") or 0):
                break
        return out


class DoverAdapter:
    """Dover careers pages. Feed params: client_id, apply_base (public job page prefix)."""
    type, label, host = "dover", "Dover", "app.dover.com"

    def list_feed(self, company, feed):
        url, out = f"https://{self.host}/api/v1/careers-page/{feed['client_id']}/jobs", []
        while url:
            d = get_json(url, retries=2)
            for j in d.get("results") or []:
                if not j.get("is_published", True):
                    continue
                locs = [(l.get("location_option") or {}).get("display_name") or l.get("name") for l in j.get("locations") or []]
                out.append(_p(self, company, feed["client_id"][:8], j["id"], j.get("title"),
                              f"{feed.get('apply_base', 'https://app.dover.com/jobs/' + feed['client_id'])}/{j['id']}",
                              "; ".join(l for l in locs if l), workplace=(j.get("workplace_type") or "").lower() or None))
            url = d.get("next")
        return out


class JibeAdapter:
    """iCIMS Jibe careers sites ({host}/api/jobs), e.g. AMD. Feed params: host, location, path."""
    type, label, host = "jibe", "Jibe (iCIMS)", "jibe"

    def list_feed(self, company, feed):
        host, out, page = feed["host"], [], 1
        while page <= 50:
            q = urllib.parse.urlencode({"location": feed.get("location", "Canada"), "limit": 100, "page": page})
            d = get_json(f"https://{host}/api/jobs?{q}", retries=2, headers=UA)
            rows = d.get("jobs") or []
            for r in rows:
                j = r.get("data") or {}
                out.append(_p(self, company, host.split(".")[1] if host.count(".") > 1 else host, j.get("req_id") or j.get("slug"),
                              j.get("title"), f"https://{host}{feed.get('path', '/careers-home/jobs')}/{j.get('slug')}",
                              ", ".join(x for x in (j.get("city", "").title(), j.get("state"), j.get("country")) if x),
                              country_hint=j.get("country_code"), posted_at=j.get("posted_date"),
                              description=html_to_text(j.get("description") or "")))
            if not rows or len(out) >= (d.get("totalCount") or 0):
                break
            page += 1
        return out


class AtlassianAdapter:
    """Atlassian's careers listing endpoint (one request, every job)."""
    type, label, host = "atlassian", "Atlassian Careers", "www.atlassian.com"

    def list_feed(self, company, feed):
        rows = get_json(f"https://{self.host}/endpoint/careers/listings", retries=2, headers=UA) or []
        return [_p(self, company, "atlassian", j["id"], j.get("title"),
                   (j.get("portalJobPost") or {}).get("portalUrl") or f"https://www.atlassian.com/company/careers/details/{j['id']}",
                   "; ".join(j.get("locations") or []), department=j.get("category") or "",
                   description=html_to_text(j.get("overview") or ""))
                for j in rows]


class WorkableAdapter:
    """Workable accounts (apply.workable.com/{sub}). Workable rate-limits cloud IPs, so go slowly."""
    type, label, host = "workable", "Workable", "apply.workable.com"

    _lock = threading.Lock()                 # one Workable request at a time, spaced out

    def list_feed(self, company, feed):
        sub = feed["subdomain"]
        with self._lock:
            time.sleep(8)
            d = get_json(f"https://{self.host}/api/v1/widget/accounts/{sub}", retries=3, headers=CHROME_UA)
        return [_p(self, company, sub, j.get("shortcode"), j.get("title"), j.get("url") or j.get("application_url"),
                   ", ".join(x for x in (j.get("city"), j.get("state"), j.get("country")) if x),
                   remote_hint=j.get("telecommuting") or None, department=j.get("department") or "",
                   posted_at=j.get("published_on"))
                for j in d.get("jobs") or []]


class UltiProAdapter:
    """UKG Pro (UltiPro) recruiting boards. Feed params: board_url (…/JobBoard/{guid})."""
    type, label, host = "ultipro", "UKG Pro Recruiting", "ultipro"

    def list_feed(self, company, feed):
        base, out, skip = feed["board_url"].rstrip("/"), [], 0
        while skip < 2000:
            body = {"opportunitySearch": {"Top": 50, "Skip": skip, "QueryString": "", "Filters": [],
                                          "OrderBy": [{"Value": "postedDateDesc", "PropertyName": "PostedDate", "Ascending": False}]},
                    "matchCriteria": {"PreferredJobs": [], "Educations": [], "LicenseAndCertifications": [],
                                      "Skills": [], "hasNoLicenses": False, "SkippedSkills": []}}
            d = get_json(f"{base}/JobBoardView/LoadSearchResults", retries=2, body=body)
            rows = d.get("opportunities") or []
            for j in rows:
                locs, countries = [], set()
                for l in j.get("Locations") or []:
                    a = l.get("Address") or {}
                    countries.add((a.get("Country") or {}).get("Code"))
                    locs.append(", ".join(x for x in (a.get("City"), (a.get("State") or {}).get("Code"), (a.get("Country") or {}).get("Code")) if x))
                out.append(_p(self, company, base.split("/")[3], j["Id"], j.get("Title"),
                              f"{base}/OpportunityDetail?opportunityId={j['Id']}", "; ".join(l for l in locs if l),
                              country_hint="CA" if countries == {"CAN"} else None,
                              posted_at=j.get("PostedDate"), description=html_to_text(j.get("BriefDescription") or "")))
            skip += len(rows)
            if not rows or skip >= (d.get("totalCount") or 0):
                break
            time.sleep(0.3)
        return out


ALL = [GemAdapter(), RipplingAdapter(), BambooHRAdapter(), JazzHRAdapter(), HiBobAdapter(), ADPAdapter(),
       DoverAdapter(), JibeAdapter(), AtlassianAdapter(), WorkableAdapter(), UltiProAdapter()]
