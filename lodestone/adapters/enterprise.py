"""Careers-site platforms used by banks, telecoms and large Canadian employers, plus Shopify.
Feed params come from the source index."""
from __future__ import annotations

import http.cookiejar
import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET

from ..http import USER_AGENT, fetch, get_json
from ..models import Posting
from ..text import html_to_text

UA = {"User-Agent": "Mozilla/5.0"}


def _p(adapter, company, key, jid, title, url, loc, **kw) -> Posting:
    return Posting(source=adapter.type, company=company, slug=key, source_job_id=str(jid),
                   title=(title or "").strip(), url=url or "", location_raw=loc or "", **kw)


def _slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", s or "").strip("-")


class PhenomAdapter:
    """Phenom People careers sites (POST {host}/widgets). Feed params: host, refNum, lang, site_country,
    country_value (how the site spells Canada, e.g. "Canada" or "CANADA")."""
    type, label, host = "phenom", "Phenom", "phenom"

    def list_feed(self, company, feed):
        host, out, start, size = feed["host"], [], 0, 50
        lang, sc = feed.get("lang", "en_ca"), feed.get("site_country", "ca")
        while start < 5000:
            body = {"lang": lang, "deviceType": "desktop", "country": sc, "pageName": "search-results",
                    "ddoKey": "refineSearch", "sortBy": "", "subsearch": "", "from": start, "jobs": True,
                    "counts": False, "all_fields": ["country"], "size": size, "clearAll": False,
                    "jdsource": "facets", "isSliderEnable": False, "keywords": "", "global": True,
                    "selected_fields": {"country": [feed.get("country_value", "Canada")]}, "refNum": feed["refNum"]}
            rs = get_json(f"https://{host}/widgets", retries=2, body=body, headers=UA).get("refineSearch") or {}
            jobs = (rs.get("data") or {}).get("jobs") or []
            for j in jobs:
                locs = j.get("multi_location") or [j.get("cityStateCountry") or j.get("location")]
                out.append(_p(self, company, feed["refNum"], j.get("jobId") or j.get("reqId"), j.get("title"),
                              f"https://{host}/{sc}/{lang.split('_')[0]}/job/{j.get('jobId')}/{_slug(j.get('title'))}",
                              "; ".join(l for l in locs if l), country_hint="CA" if (j.get("country") or "").lower() == "canada" else None,
                              department=j.get("category") or "", posted_at=j.get("postedDate"),
                              extra={"teaser": j.get("descriptionTeaser") or ""}))   # full text fetched for role matches
            start += len(jobs)
            if not jobs or start >= (rs.get("totalHits") or 0):
                break
            time.sleep(0.3)
        return out


class DayforceAdapter:
    """Dayforce candidate portals (jobs.dayforcehcm.com/{ns}/{board}). The search API needs the
    session cookie and anti-forgery token a browser gets from the portal page. Feed params: namespace, board."""
    type, label, host = "dayforce", "Dayforce", "jobs.dayforcehcm.com"

    def list_feed(self, company, feed):
        ns, board = feed["namespace"], feed.get("board", "CANDIDATEPORTAL")
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        hdr = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

        def call(url, body=None, extra=None):
            data = json.dumps(body).encode() if body is not None else None
            h = {**hdr, **(extra or {}), **({"Content-Type": "application/json"} if data else {})}
            with opener.open(urllib.request.Request(url, data=data, headers=h), timeout=30) as r:
                return r.read().decode("utf-8", "replace")

        call(f"https://{self.host}/en-US/{ns}/{board}", extra={"Accept": "text/html"})
        token = json.loads(call(f"https://{self.host}/api/auth/csrf"))["csrfToken"]
        out, start = [], 0
        while start < 2000:
            d = json.loads(call(f"https://{self.host}/api/geo/{ns}/jobposting/search",
                                {"clientNamespace": ns, "jobBoardCode": board, "cultureCode": "en-US",
                                 "distanceUnit": 0, "paginationStart": start}, {"X-CSRF-TOKEN": token}))
            rows = d.get("jobPostings") or []
            for j in rows:
                locs = j.get("postingLocations") or []
                codes = {l.get("isoCountryCode") for l in locs}
                out.append(_p(self, company, ns, j["jobPostingId"], j.get("jobTitle"),
                              f"https://{self.host}/en-US/{ns}/{board}/jobs/{j['jobPostingId']}",
                              "; ".join(l.get("formattedAddress") or "" for l in locs),
                              country_hint="CA" if codes == {"CA"} else None, remote_hint=j.get("hasVirtualLocation") or None,
                              posted_at=j.get("postingStartTimestampUTC"), description=html_to_text(j.get("jobDescription") or "")))
            start += len(rows)
            if not rows or start >= (d.get("maxCount") or 0):
                break
            time.sleep(1)
        return out


class SuccessFactorsAdapter:
    """SAP SuccessFactors career sites. Feed params: host, mode.
    mode "feed": the site's full job feed (feed_path, e.g. /sitemap.xml or /googlefeed.xml), RSS with
    every posting and its description. mode "json": the newer search API (/services/recruiting/v1/jobs)."""
    type, label, host = "successfactors", "SAP SuccessFactors", "successfactors"

    def list_feed(self, company, feed):
        return self._json(company, feed) if feed.get("mode") == "json" else self._rss(company, feed)

    def _rss(self, company, feed):
        host = feed["host"]
        xml = fetch(f"https://{host}{feed.get('feed_path', '/sitemap.xml')}", timeout=120, retries=2,
                    headers={"Accept": "application/rss+xml, application/xml, */*"})
        root = ET.fromstring(xml.encode("utf-8"))
        g = "{http://base.google.com/ns/1.0}"
        out, seen = [], set()
        for it in root.iter("item"):
            title, link = (it.findtext("title") or "").strip(), (it.findtext("link") or "").strip()
            m = re.match(r"^(.*)\s+\(([^()]*)\)\s*$", title)        # "Senior PM (Toronto, ON, CA, M5J 2J5)"
            name, where = (m.group(1), m.group(2)) if m else (title, it.findtext(f"{g}location") or "")
            jid = it.findtext(f"{g}id") or link.rstrip("/").rsplit("/", 1)[-1]
            if jid in seen:
                continue                                               # EN/FR duplicates
            seen.add(jid)
            where = re.sub(r",\s*CA(,|$)", r", Canada\1", where)
            out.append(_p(self, company, host, jid, name, link, where,
                          description=html_to_text(it.findtext("description") or "")))
        return out

    def _json(self, company, feed):
        host, out, page = feed["host"], [], 0
        while page < 200:
            d = get_json(f"https://{host}/services/recruiting/v1/jobs", retries=2, headers=UA, body={
                "locale": "en_US", "pageNumber": page, "sortBy": "", "keywords": "", "location": "",
                "facetFilters": {}, "brand": "", "skills": [], "categoryId": 0, "alertId": "", "rcmCandidateId": ""})
            rows = d.get("jobSearchResult") or []
            for r in rows:
                j = r.get("response") or {}
                locs = [re.sub(r"<br/?>", "", l).strip() for l in j.get("jobLocationShort") or []]
                locs = [re.sub(r",\s*CAN(,|$)", r", Canada\1", l) for l in locs]
                out.append(_p(self, company, host, j.get("id"), j.get("unifiedStandardTitle"),
                              f"https://{host}/job/{j.get('unifiedUrlTitle')}/{j.get('id')}-en_US/", "; ".join(locs),
                              posted_at=j.get("unifiedStandardStart")))
            page += 1
            if not rows or len(out) >= (d.get("totalJobs") or 0):
                break
            time.sleep(0.3)
        return out


class ShopifyAdapter:
    """Shopify careers (shopify.com/careers). Jobs come from the site's own data route, a Remix
    'turbo-stream' (a flat JSON array where keys and values point at other array slots). Shopify's
    'Americas' roles are remote across the US and Canada, so they count as remote-Canada."""
    type, label, host = "shopify", "Shopify Careers", "www.shopify.com"

    def list_feed(self, company, feed):
        a = json.loads(fetch(f"https://{self.host}/careers.data", retries=2, headers=UA).split("\n")[0])

        def val(v, depth=0):
            if isinstance(v, int):
                return None if v < 0 else obj(a[v], depth + 1) if v < len(a) else None
            return v

        def obj(o, depth):
            if depth > 15:
                return None
            if isinstance(o, dict):
                return {(a[int(k[1:])] if k.startswith("_") else k): val(v, depth) for k, v in o.items()}
            if isinstance(o, list):
                return [val(x, depth) for x in o]
            return o

        out = []
        for o in a:
            if not isinstance(o, dict):
                continue
            keys = {a[int(k[1:])] for k in o if k.startswith("_") and k[1:].isdigit() and isinstance(a[int(k[1:])], str)}
            if not {"title", "externalLink", "locationName"} <= keys:
                continue
            j = obj(o, 0)
            if j.get("isListed") is False:
                continue
            loc = (j.get("locationName") or "").strip()
            if loc.lower() == "americas":
                loc = "Remote - Americas (US and Canada)"
            out.append(_p(self, company, "shopify", j.get("id"), j.get("title"), j.get("externalLink"), loc,
                          workplace=(j.get("workplaceType") or "").lower() or None, remote_hint=(j.get("workplaceType") == "Remote") or None,
                          department=j.get("teamName") or "", posted_at=j.get("publishedDate")))
        return out


ALL = [PhenomAdapter(), DayforceAdapter(), SuccessFactorsAdapter(), ShopifyAdapter()]
