"""Careers sites with no JSON feed, read from their public search-result pages (Avature, iCIMS,
Radancy TalentBrew) plus two company-specific search APIs (IBM, Coveo). Page layouts can change;
a parse that finds nothing raises an error so the refresh report flags it."""
from __future__ import annotations

import html
import re
import time
import urllib.parse

from ..http import get_json, get_text
from ..models import Posting

UA = {"User-Agent": "Mozilla/5.0"}


def _p(adapter, company, key, jid, title, url, loc, **kw) -> Posting:
    return Posting(source=adapter.type, company=company, slug=key, source_job_id=str(jid),
                   title=html.unescape(title or "").strip(), url=url or "", location_raw=html.unescape(loc or "").strip(), **kw)


def _clean(s: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s or "")).split())


class AvatureAdapter:
    """Avature portals (…/careers/SearchJobs). Feed params: search_url (with any country filter),
    page_size (default 10). Portals use different templates (cards or a table), so each job is the
    stretch of page between one JobDetail link and the next, and the location is the first
    location-like element in it."""
    type, label, host = "avature", "Avature", "avature"
    _LINK = re.compile(r'<a [^>]*href="([^"]*/JobDetail/[^"]*?/(\d+))"[^>]*>(.*?)</a>', re.S)
    _LOCS = (re.compile(r'class="list-item-location"[^>]*>(.*?)</span>', re.S),
             re.compile(r'article__header__text__subtitle">(.*?)</div>', re.S),
             re.compile(r"<td[^>]*>(.*?)</td>", re.S))

    def _location(self, chunk: str, url: str) -> str:
        loc = ""
        for rx in self._LOCS:
            m = rx.search(chunk)
            if m and _clean(m.group(1)):
                loc = _clean(m.group(1))
                break
        parts = [x.strip() for x in loc.split("·") if x.strip()]
        if len(parts) > 1 and parts[0].lower() == "canada":       # "Canada · Ontario · Toronto"
            loc = ", ".join(reversed(parts))
        if "canada" not in loc.lower() and "-Canada-" in url:     # NBC: "Montreal" + ".../Montr-al-Quebec-Canada-..."
            loc = f"{loc}, Canada" if loc else "Canada"
        return loc

    def list_feed(self, company, feed):
        base, size = feed["search_url"], int(feed.get("page_size", 10))
        out, seen, offset = [], set(), 0
        while offset < 3000:
            sep = "&" if "?" in base else "?"
            page = get_text(f"{base}{sep}jobRecordsPerPage={size}&jobOffset={offset}", retries=2, headers=UA)
            links = [m for m in self._LINK.finditer(page) if _clean(m.group(3))]
            if not links and offset == 0:
                raise ValueError("Avature page layout changed: no job links found")
            new = 0
            for i, m in enumerate(links):
                jid = m.group(2)
                if jid in seen:
                    continue
                seen.add(jid)
                new += 1
                end = next((n.start() for n in links[i + 1:] if n.group(2) != jid), len(page))
                out.append(_p(self, company, urllib.parse.urlparse(base).netloc, jid, _clean(m.group(3)), m.group(1),
                              self._location(page[m.end():end], m.group(1))))
            if new == 0:
                break
            offset += size
            time.sleep(0.4)
        return out


class ICIMSAdapter:
    """iCIMS hosted career portals ({host}/jobs/search). Feed params: host. Locations look like
    'CA-ON-Ottawa' or 'CA-Remote' and are rewritten to 'Ottawa, ON, Canada'."""
    type, label, host = "icims", "iCIMS", "icims.com"
    _ITEM = re.compile(r'<li class="iCIMS_JobCardItem">(.*?)</li>', re.S)

    @staticmethod
    def _loc(code: str) -> str:
        parts = code.strip().split("-")
        if len(parts) >= 2 and parts[0] == "CA":
            rest = parts[1:]
            return ("Remote, Canada" if rest == ["Remote"] else ", ".join(reversed(rest)) + ", Canada")
        return code.strip()

    def list_feed(self, company, feed):
        host, out, page, pages = feed["host"], [], 0, 1
        while page < min(pages, 60):
            s = get_text(f"https://{host}/jobs/search?ss=1&in_iframe=1&pr={page}", retries=2, headers=UA)
            m = re.search(r"Page \d+ of (\d+)", s)
            pages = int(m.group(1)) if m else 1
            items = self._ITEM.findall(s)
            if not items and page == 0:
                raise ValueError("iCIMS page layout changed: no job cards found")
            for it in items:
                link = re.search(rf'href="(https://{re.escape(host)}/jobs/(\d+)/[^"]*?/job)[^"]*"', it)
                title = re.search(r"<h3[^>]*>(.*?)</h3>", it, re.S)
                locs = re.findall(r'field-label">(?:Location|Additional Locations)</span>.*?<span[^>]*>(.*?)</span>', it, re.S)
                if not link:
                    continue
                where = "; ".join(dict.fromkeys(self._loc(_clean(l)) for l in locs for l in _clean(l).split("|")))
                remote = re.search(r'Remote</dt>\s*<dd[^>]*><span[^>]*>\s*Yes', it) is not None
                out.append(_p(self, company, host.split(".")[0], link.group(2), _clean(title.group(1) if title else ""),
                              link.group(1), where, remote_hint=remote or None))
            page += 1
            time.sleep(0.4)
        return out


class TalentBrewAdapter:
    """Radancy TalentBrew career sites (…/search-jobs/results): JSON whose 'results' is HTML.
    Feed params: host, facet_id (GeoNames id of the country, Canada = 6251999)."""
    type, label, host = "talentbrew", "Radancy TalentBrew", "talentbrew"

    def list_feed(self, company, feed):
        host, fid, out, page = feed["host"], feed.get("facet_id", "6251999"), [], 1
        while page <= 30:
            q = urllib.parse.urlencode({
                "ActiveFacetID": fid, "CurrentPage": page, "RecordsPerPage": 100, "Distance": 50,
                "RadiusUnitType": 0, "ShowRadius": "False", "IsPagination": "True", "FacetType": 2,
                "FacetFilters[0].ID": fid, "FacetFilters[0].FacetType": 2, "FacetFilters[0].Count": 0,
                "FacetFilters[0].Display": feed.get("country", "Canada"), "FacetFilters[0].IsApplied": "true",
                "SearchResultsModuleName": "Search Results", "SearchFiltersModuleName": "Search Filters",
                "SortCriteria": 0, "SortDirection": 0, "SearchType": 5, "ResultsType": 0})
            h = get_json(f"https://{host}/search-jobs/results?{q}", retries=2,
                         headers={**UA, "X-Requested-With": "XMLHttpRequest"}).get("results") or ""
            rows = re.findall(r'<a href="(/job/[^"]+/(\d+))"[^>]*data-title="([^"]*)".*?class="job-location">(.*?)</span>', h, re.S)
            for path, jid, title, loc in rows:
                out.append(_p(self, company, host, jid, title, f"https://{host}{path}", _clean(loc)))
            total = re.search(r'data-total-results="(\d+)"', h)
            if not rows or len(out) >= int(total.group(1) if total else 0):
                break
            page += 1
        return out


class NjoynAdapter:
    """Njoyn job listings (e.g. CGI: cgi.njoyn.com). HTML table, 50 rows per page.
    Feed params: host, path (…/xweb/xweb.asp), clid, form (country filter fields). Plain request headers:
    CGI's site shows a captcha to browser-like clients."""
    type, label, host = "njoyn", "Njoyn", "njoyn.com"
    _ROW = re.compile(r"<tr HasMultipleLocations='(\d)'[^>]*><td><a href='([^']*Jobid=([^&']+)[^']*)'>[^<]*</a></td>"
                      r"<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td[^>]*>(.*?)</td></tr>", re.S)

    def list_feed(self, company, feed):
        from ..http import fetch
        host, path, clid = feed["host"], feed.get("path", "/CORP/xweb/xweb.asp"), feed["clid"]
        url = f"https://{host}{path}?NTKN=c&clid={clid}&Page=joblisting&lang=1"
        out, page, pages = [], 1, 1
        while page <= min(pages, 40):
            s = fetch(url, form={**feed.get("form", {}), "pn": page}, retries=2)
            m = re.search(r"Page \d+ of (\d+)", s)
            pages = int(m.group(1)) if m else 1
            rows = self._ROW.findall(s)
            if not rows and page == 1:
                raise ValueError("Njoyn page layout changed: no job rows found")
            for multi, href, jid, title, cat, city, country in rows:
                link = f"https://{host}{path.rsplit('/', 1)[0]}/{html.unescape(href)}"
                out.append(_p(self, company, host.split(".")[0], jid, _clean(title), link,
                              ", ".join(x for x in (_clean(city), _clean(country)) if x), department=_clean(cat)))
            page += 1
            time.sleep(0.4)
        return out


class IBMAdapter:
    """IBM careers search API (www-api.ibm.com/search/api/v2, Elasticsearch-style). Feed params: country."""
    type, label, host = "ibm", "IBM Careers", "www-api.ibm.com"

    def list_feed(self, company, feed):
        out, start = [], 0
        while start < 3000:
            body = {"appId": "careers", "scopes": ["careers2"], "size": 100, "from": start, "lang": "zz",
                    "query": {"bool": {"must": [{"term": {"field_keyword_05": feed.get("country", "Canada")}}]}},
                    "_source": ["url", "title", "description", "dcdate", "field_keyword_05", "field_keyword_08",
                                "field_keyword_17", "field_keyword_19"]}
            hits = (get_json(f"https://{self.host}/search/api/v2", retries=2, body=body, headers=UA).get("hits") or {})
            rows = hits.get("hits") or []
            for h in rows:
                s = h.get("_source") or {}
                city = re.sub(r",\s*CA$", ", Canada", s.get("field_keyword_19") or "")
                jid = (re.search(r"jobId=(\d+)", s.get("url", "")) or [None, h.get("_id")])[1]
                out.append(_p(self, company, "ibm", jid, s.get("title"), s.get("url"), city or s.get("field_keyword_05"),
                              country_hint="CA" if s.get("field_keyword_05") == "Canada" else None,
                              workplace=(s.get("field_keyword_17") or "").lower() or None,
                              department=s.get("field_keyword_08") or "", posted_at=s.get("dcdate"),
                              description=s.get("description") or ""))
            start += len(rows)
            if not rows or start >= ((hits.get("total") or {}).get("value") or 0):
                break
        return out


class CoveoAdapter:
    """Coveo's careers search (it runs on Coveo's own search API). Jobs are indexed more than once,
    so we dedupe on the underlying job id."""
    type, label, host = "coveo", "Coveo Careers", "www.coveo.com"

    def list_feed(self, company, feed):
        d = get_json(f"https://{self.host}/coveo/rest/search/v2", retries=2, headers=UA, body={
            "q": "", "aq": "@iscareerjob==1 @culture==en", "numberOfResults": 500,
            "fieldsToInclude": ["maintitle", "joblocation", "jobofficehierarchical", "z95xname", "clickableuri"]})
        out, seen = [], set()
        for r in d.get("results") or []:
            raw = r.get("raw") or {}
            jid = raw.get("z95xname") or r.get("clickUri")
            if not jid or jid in seen:
                continue
            seen.add(jid)
            out.append(_p(self, company, "coveo", jid, raw.get("maintitle") or r.get("title"), r.get("clickUri"),
                          raw.get("joblocation") or "; ".join(raw.get("jobofficehierarchical") or [])))
        return out


ALL = [AvatureAdapter(), ICIMSAdapter(), NjoynAdapter(), TalentBrewAdapter(), IBMAdapter(), CoveoAdapter()]
