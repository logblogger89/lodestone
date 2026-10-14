# DR-4 — Job-Source Inventory and Feasibility

| | |
|---|---|
| **Feeds** | PRD A1 (multi-source ingestion and dedup), A3 (paste URL), B8 (pay), CR-3a (pathway signals). Also an input to the Eng Design Doc |
| **Status** | v1, desk research 2026-10-14. Items marked *verify* get a hands-on check in the Eng Design phase |
| **Author** | Claude (research), for Ayush's review |

---

## 1. Summary

1. **Discover companies broadly, but ingest jobs from their source.** Most "job boards" (VC portfolio boards, Built In, startup.jobs, Eluta) re-host postings that actually live in a company's ATS. The robust, ToS-friendly design is: use boards and lists to **find companies and their ATS slugs**, then pull jobs from the **ATS's public JSON feed**. That gives structured data, a canonical job ID for dedup, and the freshest status for the liveness check (F25).
2. **Four ATS families have public, keyless, read-only feeds:** Greenhouse, Lever, Ashby (official docs, with optional compensation) and SmartRecruiters (official docs). Workable and Workday have endpoints that aren't documented; treat those as *verify*. Together these cover a large share of tech employers.
3. **Big aggregators are off-limits for automated access.** LinkedIn's User Agreement prohibits scraping. Indeed's free publisher API is closed to new developers. Wellfound uses bot mitigation, and its terms reportedly refuse scraping. All of these are covered through **A3, paste a URL**: Ayush pastes a link, Lodestone fetches that single page on his behalf, parses it, and scores it.
4. **Sources are a set, not a single value.** Every sighting of a job is kept, and the listing shows one icon per source (A1). Dedup uses the canonical ATS job ID or apply URL, with fuzzy matching on company, title and location as a fallback.
5. **Two policy findings change product requirements:**
   - **Ontario pay transparency (in force since 2026-01-01):** employers with 25 or more employees must post pay, and the range can be no wider than $50K. But roles **above $200K are exempt**. Many roles at Ayush's target level may therefore have *no posted range*, which makes the estimate in B8 a core feature rather than a nice-to-have. The same rules **ban "Canadian experience required"** in postings, which helps Ayush.
   - **ESDC publishes a quarterly list of employers that received a positive LMIA** (open data, XLSX). It's an official, employer-level sponsorship signal for CR-3a.

## 2. Source inventory

Tiers describe how Lodestone uses each source. **Ingest** means pulled automatically on a schedule. **Discover** means used to find companies and their ATS slugs, not scraped for jobs. **Manual** means only via A3 (paste URL). **Signal** means used to enrich listings, not as a source of listings.

### 2.1 ATS public feeds (Ingest; the backbone)

| Source | Access | Notes |
|---|---|---|
| **Greenhouse** | `GET boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true`, no key | Whole board in one response. No pay field in the schema; pay may appear in the JD text |
| **Lever** | `GET api.lever.co/v0/postings/{slug}?mode=json`, no key (EU variant exists) | Paginated (`skip`, `limit`). Some customers disable the feed (*verify* per company) |
| **Ashby** | `GET api.ashbyhq.com/posting-api/job-board/{name}?includeCompensation=true`, no key, **official docs** | Has structured pay when the employer opts in. Very common with startups and scale-ups |
| **SmartRecruiters** | `GET api.smartrecruiters.com/v1/companies/{id}/postings`, **official docs** | Public feed isn't enabled on every plan |
| **Workable** | Widget endpoint `apply.workable.com/api/v1/widget/accounts/{slug}?details=true` | Not documented; sources conflict on whether it needs auth (*verify*) |
| **Workday** | `POST {tenant}.wd{N}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs` | Not documented. 20 results per page. May sit behind Cloudflare. **Banks and big enterprises (RBC, TD, etc.) use it heavily.** Check ToS per employer (*verify*) |

### 2.2 Company career sites (Ingest where possible, otherwise Manual)

| Source | Notes |
|---|---|
| **Google Careers** (internal-transfer channel, D-012) | No documented public API. Options: Ayush pastes links (A3), a polite per-page fetch from the watchlist (*verify* ToS), or he browses Google's internal job site himself. Postings from Google get the internal-transfer badge (B10) |
| Custom career sites (some banks and enterprises) | Often a Workday or SuccessFactors front end. Otherwise A3 |

### 2.3 Discovery boards: VC portfolios and ecosystems (Discover, and Ingest when the board exposes its ATS)

| Board | Platform | Relevance |
|---|---|---|
| **a16z Portfolio Jobs** (portfoliojobs.a16z.com) | Consider | Global, includes Canadian and remote roles |
| **Inovia Capital** (careers.inovia.vc) | Getro | Top Canadian VC. Montréal and Toronto portfolio |
| **Communitech** (communitech.getro.com) | Getro | **Waterloo ecosystem**, and Communitech has absorbed the Prospect startup job board |
| **BDC Capital** and **Diagram** boards | Getro | Canadian portfolio companies |
| Other VC boards to add (*verify* each exists): Georgian, OMERS Ventures, Radical Ventures, Real Ventures, Portage, Golden Ventures, plus US firms with Canadian portfolios (Accel, Sequoia, Index, Lightspeed, Tiger) | Getro / Consider / custom | Breadth |
| **Y Combinator: Work at a Startup** | YC | Filter for Canada and remote |
| **Getro platform** | Network API v2 (bearer key, 30 req/min) | Key is for network operators, not the public. Use the boards for discovery, then ingest jobs from the companies' ATS |

### 2.4 Canadian and PM-focused aggregators (Discover; Manual for postings)

| Board | Notes |
|---|---|
| **Built In Toronto** | Toronto tech roles, tagged by seniority and industry |
| **Eluta.ca** | Canadian engine that crawls employer sites (run by the Canada's Top 100 Employers project). Has RSS and email alerts (*verify* ToS before using RSS) |
| **startup.jobs**, **Wellfound** | Startup roles. Wellfound is Manual only (bot mitigation, restrictive terms) |
| **WeLoveProduct / Mind the Product jobs**, **Product HQ** | PM-specific boards |
| **Himalayas**, **Remote100K** | Remote roles (useful for remote-in-Canada) |
| **CVCA job board** | Private-capital roles. Low relevance |
| **Job Bank (federal)** | Open data as **monthly CSV**. An XML feed exists, but it's mainly for inbound partners. Low relevance for senior PM, but it carries NOC codes and some LMIA-linked postings |
| **Hacker News "Who is hiring?"** | Official HN Firebase and Algolia APIs. Monthly thread, unstructured, so it needs LLM parsing. Good for remote and startup roles |

### 2.5 Manual only (A3, paste URL)

**LinkedIn, Indeed, Glassdoor, Wellfound.** Ayush pastes a link, and Lodestone fetches only that page, parses it, scores it, and records the source icon. No crawling and no bulk access.

### 2.6 Signal sources (enrichment, not listings)

| Source | Use |
|---|---|
| **ESDC Positive LMIA Employers List** (open.canada.ca, quarterly XLSX, back to 2014) | Employer-level "has sponsored before" signal for CR-3a. Caveats: it counts *positions approved*, not permits issued. PR-stream LMIAs were left out from Q1 2018 to Q3 2023 and are included again from Q4 2023 |
| **Global Talent Stream designated referral partners** (ESDC) | A Category A pathway signal. The list was cut from 58 to 41 partners in Sep 2026, so pull it live |
| **Ontario pay-transparency rules** | Explains why pay is missing (the >$200K exemption). Drives how B8 estimates are labelled |
| Company news (funding, layoffs) | A5 and B13 signals (V1) |

## 3. Dedup and source attribution design (input to the Eng Design Doc)

1. **Canonical key:** the ATS job ID plus the ATS host, when known. Otherwise the normalized apply URL.
2. **Fuzzy fallback:** company (normalized) + title (normalized) + location + a description similarity threshold.
3. **Sightings table:** every (job, source, first_seen, last_seen, source_url) row is kept. The UI shows **one icon per source** (A1) and links each one.
4. **Liveness (F25):** if the ATS feed stops returning a job, or its URL returns 404 or a "no longer accepting" page, the listing is flagged *no longer live* and kept in the pipeline history.

## 4. Open items to verify (Eng Design phase)

- ToS and robots.txt for each Ingest source, especially Workday tenants, Eluta and Google Careers
- Whether Workable's widget endpoint needs auth
- Which Canadian VC boards exist and which platform each uses (Georgian, OMERS, Radical, Portage, Golden…)
- How many watchlist companies use each ATS (to size coverage)
- The latest quarter of the ESDC LMIA list, and how to match employer names to companies

## Sources

- [a16z Portfolio Jobs](https://portfoliojobs.a16z.com/companies)
- [Greenhouse public jobs API (developer write-up)](https://dev.to/zsevic/integration-with-greenhouse-public-jobs-api-1lj3) · [JobsPipe: Greenhouse](https://jobspipe.dev/sources/greenhouse.md)
- [Lever API guide](https://100hires.com/lever-api.html) · [JobsPipe: Lever](https://jobspipe.dev/sources/lever.md)
- [Ashby Job Postings API (official)](https://developers.ashbyhq.com/docs/public-job-posting-api)
- [SmartRecruiters list postings (official)](https://developers.smartrecruiters.com/reference/v1listpostings.md)
- [Workable public jobs API (write-up)](https://dev.to/zsevic/integration-with-workable-public-jobs-api-3nk4)
- [Workday JSON API (write-up)](https://dev.to/udaninn/workday-job-boards-have-a-json-api-too-its-just-better-hidden-23fl)
- [Getro on apis.io](https://apis.io/providers/getro/) · [Communitech Getro board](https://communitech.getro.com/companies/bdc-2/jobs/60677301-associate-seed-venture-fund) · [Diagram jobs](https://careers.diagram.ca/jobs)
- [Inovia careers board](https://careers.inovia.vc/companies/inovia-capital-2) · [Consider: Inovia job board](https://blog.consider.com/posts/introducing-the-inovia-capital-job-board)
- [Communitech takes over Prospect (BetaKit)](https://betakit.com/communitech-takes-over-canadian-tech-startup-job-board-prospect/)
- [Wellfound PM jobs Canada](https://wellfound.com/role/l/product-manager/canada-startups) · [Built In Toronto](https://builtintoronto.com/jobs/product/search/product-manager) · [startup.jobs Toronto](https://startup.jobs/locations/toronto/product-manager)
- [Top PM job boards 2026 (uxcel)](https://uxcel.com/blog/top-product-management-job-boards)
- [Eluta (Job Junction overview)](https://www.jobjunction.ca/job-search-engines-1)
- [Job Bank open data](https://open.canada.ca/data/en/dataset/ea639e28-c0fc-48bf-b5dd-b8899bd43072) · [Job Bank network](https://www.jobbank.gc.ca/network)
- [ESDC Positive LMIA Employers List](https://open.canada.ca/data/en/dataset/90fed587-1364-4f33-a9ee-208181dc0b97)
- [GTS program requirements (ESDC)](https://www.canada.ca/en/employment-social-development/services/foreign-workers/global-talent/requirements) · [CIC News: GTS partner list trimmed (Sep 2026)](https://www.cicnews.com/2026/09/canada-trims-list-of-partners-providing-access-to-fast-track-hiring-under-global-talent-stream-of-tfwp-0980494.html/amp)
- [LinkedIn on the hiQ ruling](https://blog.linkedin.com/2022/november/4/update-hi-q-legal-proceeding) · [Metaverse Law analysis](https://www.metaverselaw.com/hiq-v-linkedin-user-agreements-in-the-age-of-data-scraping/)
- [Indeed Publisher API status (JobsPipe)](https://jobspipe.dev/blog/indeed-publisher-api)
- [Scrapfly on Wellfound](https://scrapfly.io/blog/how-to-scrape-wellfound-aka-angellist/)
- [HN Who's Hiring parsing (Apify)](https://apify.com/getascraper/hn-hiring-scraper)
- Ontario pay transparency: [CP24 (Jan 2026)](https://www.cp24.com/local/toronto/2026/01/05/new-pay-transparency-laws-are-now-in-effect-in-ontario-heres-how-it-could-change-the-hiring-process/) · [Fogler Rubinoff](https://www.foglers.com/insights/new-year-new-rules-changes-to-job-posting-requirements-in-2026/) · [WTW](https://edge.sitecorecloud.io/willistower8735-wtw7458-prode832-66e2/media/project/wtw-sites/wtwco/insights/2025/01/ontario-pay-transparency.pdf) · [Law Times](https://lawtimesnews.com/practice-areas/labour-and-employment/ontario-job-posting-laws-tackle-vast-pay-ranges-spurred-by-rules-in-other-jurisdictions/390519)
