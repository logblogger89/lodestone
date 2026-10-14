# Lodestone — Engineering Design Doc

| | |
|---|---|
| **Author** | Claude (SWE/TL), for Ayush's review |
| **Status** | **v1, in review** (gate M3). Phase 1 = Claude Code engine + Artifact app (D-036). Cloud Run is Phase 2 |
| **Implements** | [PRD v0](../product/PRD.md) P0 R1–R15 (+ R1a), [UX spec](../product/ux/UX_SPEC.md) |
| **Decisions** | [ADRs](adr/) · [Tracker](../program/TRACKER.md) |
| **Last updated** | 2026-10-14 |

---

## Phase 1 (current): Claude Code as the engine, an Artifact as the app (D-036)

No cloud servers and no paid API yet. **Phase 2** (Cloud Run + the Claude API, §1–§14 below) starts when there are more users or the data needs a fixed schedule.

**How it works**
1. **The app** is a private claude.ai Artifact (the prototype, made real). Ayush opens it on any device.
2. **Its data** lives in the Artifact's built-in database (the `db` capability): jobs, scores, signals, and Ayush's triage, pipeline and preferences. The page reads it live. Claude reads and writes it from any Claude Code session.
3. **A refresh** happens when Ayush asks for one in a Claude Code session (`/refresh-jobs`, from the iPad or the laptop browser):
   - a repo script (`lodestone refresh`) pulls public job-system feeds for the watchlist, normalizes them, removes duplicates, applies the rules filter, and checks whether postings are still live
   - **Claude, in the session, reads and scores the new candidates.** This is covered by Ayush's Claude subscription, so there's no API bill
   - the results are written to the Artifact's database, and the code changes are pushed to GitHub
4. **Capture:** Ayush pastes a link or job description in the app. It lands in an "inbox" in the database and is processed at the next refresh. Pasted text can also be parsed right away inside the app via the `sample` capability (to verify during the build).
5. **Learning:** Claude reads Ayush's triage from the database at each refresh, adjusts the rankings, and grows the eval set.

**What stays the same for Phase 2:** the job-system adapters, dedup, rules, prompts, scoring schema and data model are shared code. Phase 2 only changes *who calls the model* (the API instead of the session) and *where data lives* (Postgres instead of the Artifact database).

**Trade-offs:** data is only as fresh as the last refresh (fine for a personal search; a scheduled Claude Code routine can automate it later without the API). A large refresh uses a meaningful share of a Pro plan's usage, so score only what passes the rules filter, and upgrade to Max only if limits bite.

**Prerequisite (one-time, Ayush):** let this Claude Code environment reach the public job feeds. Add these allowed domains in the environment's network settings: `boards-api.greenhouse.io`, `api.lever.co`, `api.eu.lever.co`, `api.ashbyhq.com`, `api.smartrecruiters.com`, `apply.workable.com`, `myworkdayjobs.com`, `open.canada.ca`, `www.canada.ca`, `hacker-news.firebaseio.com`, `hn.algolia.com`.

**Commands (project skills, D-039).** Each command updates its own timestamp in the freshness panel (R11a):
| Command | Does | Typical cadence |
|---|---|---|
| `/refresh-jobs` | Pull new postings, dedup, filter, score new jobs, flag closed postings, process the paste inbox | Whenever you like (e.g. a few times a week) |
| `/discover-companies` | Run the discovery pathways and add new companies to the watchlist | Weekly |
| `/refresh-signals` | Load the newest ESDC LMIA employer list and recompute pathway signals | Quarterly (`/refresh-jobs` warns when it's due) |
| `/rescore` | Re-score every open job after a change to the scoring logic or your profile | After changes |

**Phase 1 build plan**
| Sprint | Scope | Exit |
|---|---|---|
| P1-S1 | Core library: Greenhouse, Lever, Ashby and SmartRecruiters adapters, normalization, Canada filter, dedup, rules, plus the `/refresh-jobs` command (D-039) | A refresh produces deduplicated Canadian candidates from the seed list |
| P1-S2 | The Artifact app wired to the `db` capability: digest, detail, triage, pipeline, settings, companies | Ayush triages real jobs on the iPad |
| P1-S3 | Profile (from the CV, stored in the Artifact's database, never in the repo), Claude scoring with explanations, weights | Ranked, explained digest |
| P1-S4 | Capture inbox, pay estimates, pathway signals (ESDC list), liveness | All P0 journeys work |
| P1-S5 | Discovery (ATS reverse search through the session's web search, VC boards, ESDC, capture spill-over), eval set | M4 dogfood |

## 0. Plain-English summary

- **What runs where:** The app lives on Google Cloud, in your own account. You open it in any browser (iPad or laptop) and sign in with your Google account. Nobody else can get in.
- **How it updates:** When I change the code and push it to GitHub, it tests itself and goes live automatically. You don't install or run anything.
- **What it does every morning:** It checks hundreds of companies' job boards for new Canadian roles, removes duplicates, has Claude read and score each one against your profile, and fills your digest.
- **What you decide:** a few product and cost choices (§13). I handle the engineering.
- **Cost:** roughly $10–20/month for Google Cloud, plus the Claude cost of the option you pick ($5–270/month, §12).

---

# Phase 2 design (Cloud Run + Claude API). Deferred, kept for later

## 1. Context and goals

Lodestone is a single-user job-search portal (built so more users can be added later) hosted on **Google Cloud Run** (D-034). The design must:

1. Work from any device (iPad, laptop browser) with no local install, and deploy automatically on every push.
2. Pull jobs only through access paths that each source permits (DR-4), deduplicate them, and keep them fresh (no more than 24h old).
3. Parse and score jobs with Claude, explain each score, and let the user's weights re-rank results instantly.
4. Keep personal data (CV, immigration details) private: in Ayush's own GCP project, behind Google sign-in.
5. Model every user-specific dimension as data or config so it can be extended later (D-005).
6. Keep running costs low and visible (§12).

**Non-goals (MVP):** multi-user signup, native mobile apps, applying on the user's behalf, and scraping LinkedIn or Indeed.

## 2. Architecture

```mermaid
flowchart LR
  subgraph GitHub
    R[Repo: logblogger89/lodestone] --> CI[GitHub Actions: test, build, deploy]
  end
  CI -->|Workload Identity Federation| AR[Artifact Registry]
  AR --> WEB
  subgraph GCP project · us-central1 Iowa (cheapest tier)
    IAP[Google sign-in gate: IAP, allow-list = Ayush] --> WEB[Cloud Run service: web UI + API]
    SCH[Cloud Scheduler] --> JOBS[Cloud Run Jobs: ingest · discover · score · signals]
    WEB --> DB[(Postgres)]
    JOBS --> DB
    WEB --> GCS[(Cloud Storage: CV, private)]
    WEB & JOBS --> SM[Secret Manager]
  end
  JOBS -->|public ATS feeds, boards, ESDC data| NET[(Internet sources)]
  WEB & JOBS -->|parse + score| CLAUDE[Claude API]
  U[iPad / laptop browser] --> IAP
```

- **One container image, two entry points.** The Cloud Run *service* serves the React UI and the JSON API. Cloud Run *Jobs* run batch work (ingestion, discovery, scoring, signal refresh) on a schedule from Cloud Scheduler. Jobs have no request timeout, so long pulls are safe.
- **Region: `us-central1` (Iowa)** (D-035). It's one of Google's lowest-price regions, has every service we need, and the latency difference from NYC or Toronto is unnoticeable. Data lives in the US instead of Canada, which is fine for a personal tool. *Prices are confirmed in the GCP pricing calculator during setup (Sprint 1).*

## 3. Tech stack (ADR-0002)

| Layer | Choice | Why |
|---|---|---|
| Backend | **Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 + Alembic** | Best ecosystem for HTTP ingestion, parsing and the Anthropic SDK. Typed models end to end |
| HTTP | `httpx` (async) with per-host rate limits and retries | Polite, concurrent feed pulls |
| LLM | **Anthropic Python SDK**, structured outputs (`output_config.format`) | Schema-valid JSON from Claude for parsing and scores |
| Frontend | **React + TypeScript + Vite**, built to static files and served by FastAPI | Evolves directly from the prototype. Responsive for iPad |
| DB | **Postgres** (ADR-0003; hosting option is a decision for Ayush, §13) | Relational dedup, `pg_trgm` fuzzy matching, transactions |
| Tests | pytest, recorded HTTP fixtures, Playwright smoke test | §11 |

## 4. Data model (multi-user ready)

Every user-owned table carries `user_id` (D-005). Shared reference data (companies, jobs, ESDC list) has no `user_id`.

| Table | Key fields | Notes |
|---|---|---|
| `users` | id, email | One row in MVP |
| `profiles` | user_id, current_employer, level, domains[], scope_signals[], skills[], raw_cv_ref | From CV parse. Editable |
| `preferences` | user_id, locations[], work_modes[], families/tiers, pay_min_cad, include_no_pay, exclude_people_mgmt, digest_size (1–100, default 20), later_resurface_days (7), weights{} | All config (R5, D-025, D-026, D-031) |
| `companies` | id, name, segment, canada_presence, ats_type, ats_slug, careers_url, status (active/muted/blocked) | The watchlist |
| `company_candidates` | id, name, pathway, evidence_url, ats_detected, canada_check, decision | R1a queue |
| `sources` | id, type (greenhouse/lever/…/capture), access_method, tos_status, health | R15 registry |
| `jobs` | id, canonical_key, company_id, title, location, work_mode, posted_at, live, last_seen | One row per real job |
| `job_sightings` | job_id, source_id, source_url (**exact posting URL**), first_seen, last_seen | Source icons and deep links (R2) |
| `job_parses` | job_id, model, schema_version, family, tier, level_signals, domain, must_haves, people_mgmt, pay{min,max,cur,posted}, immigration_mentions | Structured JD (R6) |
| `job_scores` | job_id, user_id, model, prompt_version, subscores{role,level,domain,pathway,pay,skills}, reasons{} | Weights are applied at read time, so re-ranking is instant |
| `pay_estimates` | job_id, min, max, confidence, tier, method | DR-2 |
| `pathway_signals` | job_id, user_id, signal, status (stated/inferred/unknown), source_label, **source_url**, as_of | R9, with deep links |
| `lmia_employers` | quarter, employer_name, normalized_name, company_id?, positions | ESDC open data (DR-3) |
| `triage_events` | user_id, job_id, action (i/l/n), reasons[], at | Also the eval labels (R12) |
| `pipeline_items` | user_id, job_id, stage, history[] | R13. Interested → Shortlisted (D-032) |
| `config_packs` | kind (role_taxonomy / leveling / geo / eligibility_rules / crs_rules), version, as_of, data(jsonb) | Extensibility seams, versioned |

## 5. Ingestion (R1, R2, R13)

**Adapter interface** (one per source type, registered in the source registry):

```python
class SourceAdapter(Protocol):
    type: str                                  # "greenhouse", "lever", "ashby", ...
    async def list_jobs(self, company: Company) -> list[RawPosting]: ...
    async def detect(self, name: str, hints: Hints) -> AtsMatch | None: ...   # for discovery
```

- **MVP adapters:** Greenhouse, Lever, Ashby (pulls pay when the employer publishes it), SmartRecruiters. **Workday** and **Workable** are added behind a feature flag once their ToS and behaviour are verified (DR-4 §4).
- **Canada filter:** keep postings whose location is in Canada or "Remote – Canada". Remote postings tied to another country are kept but labelled "no CEC credit" (DR-3 §2a).
- **Normalization:** title, location (geocoded to a city and province), work mode, posted date, and the **exact posting URL** (Greenhouse `absolute_url`, Lever `hostedUrl`, Ashby `jobUrl`).
- **Dedup:** match on the canonical key `ats_host + ats_job_id` first, falling back to the normalized apply URL. Then a fuzzy match on (company, normalized title, city) with `pg_trgm` similarity ≥ 0.85 plus a description shingle check. Every match adds a `job_sightings` row.
- **Liveness:** when a job is missing from its feed for 2 consecutive runs (or its URL returns 404 or "no longer accepting"), set `live=false` and keep the history.
- **Schedule:** daily at 05:00 ET (Cloud Scheduler → `ingest` job), plus on-demand runs per company. Concurrency is capped per host. Requests send an honest user agent and use cached ETags where available.

## 6. Company discovery engine (R1a, DR-5)

- **Pathway plugins** (each emits candidates with evidence): `ats_reverse_search`, `vc_boards` (Getro/Consider company lists), `esdc_lmia`, `capture_spillover` (MVP). Funding news, community threads, rankings and "more like this" come in V1.
- **ATS reverse search** runs search-engine queries like `site:jobs.ashbyhq.com "Toronto"`. *Implementation choice (§13):* the Claude API `web_search` server tool (no separate search vendor), or a dedicated search API. Either way, results are only used to learn ATS slugs, and the job data itself comes from the ATS feed.
- **Detection:** probe `{greenhouse,lever,ashby,smartrecruiters}` slugs built from the company name and domain, and follow careers-page links to Workday or Workable. **Canada check:** the company has at least one live posting in Canada. **Auto-accept** when an ATS is found and the Canada check passes. Otherwise the candidate goes to "needs review."
- **Seed:** `data/seed/watchlist_seed.csv` (210 companies) is loaded on first deploy.

## 7. Capture (R3, A3a/b/c)

`POST /api/capture` accepts URLs or text. For each URL: (1) if it's a known ATS host, call that adapter's single-job endpoint; (2) otherwise fetch the page server-side. If the response shows a login wall (e.g. LinkedIn), return `needs_text`. Parse with Claude, follow any ATS apply link to resolve to the canonical job, dedup, and add the sighting with the pasted URL (source = `capture`, icon by host). New companies feed the discovery engine (P4).

## 8. Match engine (R6, R7, R8, R9)

| Stage | What | Where |
|---|---|---|
| 0. Rules | Location, work mode and role family (title taxonomy from `config_packs`). Cheap, transparent. **Missing data never excludes a job** (D-021) | Python |
| 1. Parse | JD → `job_parses` via structured outputs (strict JSON schema): family, tier, level signals, domain, must-haves, people management, pay, immigration mentions | Claude (model per §12 decision) |
| 2. Score | Profile + parsed JD → six sub-scores (0–100) plus one-line reasons, also via structured outputs. The profile and instructions sit in a **cached prompt prefix**, so per-job input stays small | Claude |
| 3. Rank | Overall score = user-weighted blend, computed at read time from `preferences.weights` (instant re-rank, D-026) | Postgres/API |
| 4. Learn | Triage events become labelled examples. The **eval harness** reports precision@10 and parse accuracy and gates any prompt or model change (R-05) | CI job |

- **Prompts and schemas are versioned** (`prompt_version`). A version change re-scores in the background.
- **Pay (R8, DR-2):** posted pay is stored as posted. Estimates follow the tier ladder: same company and level → adjacent level → market benchmark → LLM, with the confidence stored. The UI always shows "est." for estimates.
- **Pathway signals (R9, DR-3):** ICT (employer equals the profile's current employer), sponsorship stated (from the parse), sponsored before (`lmia_employers` match, linked to the ESDC dataset), GTS-likely (occupation list in `config_packs`), and CEC credit (work location). Every signal stores a `source_url` and an `as_of` date.
- **ESDC refresh:** a weekly job checks for a new quarterly XLSX and loads it, with fuzzy employer→company matching plus manual overrides.

## 9. API surface (MVP)

`GET /api/digest?limit=` · `GET /api/jobs/{id}` · `POST /api/triage` · `GET/PATCH /api/pipeline` · `POST /api/capture` · `GET/PATCH /api/preferences` · `GET/PATCH /api/profile` · `POST /api/profile/cv` · `GET/POST /api/companies` · `GET /api/candidates` · `GET /api/sources/health`

## 10. Security and privacy (R14)

- **Access:** the Google sign-in gate (**IAP**) lets in only Ayush's Google account. *Verify direct IAP-on-Cloud-Run support; the fallback is an HTTPS load balancer with IAP (adds cost) or in-app Google Sign-In with an allow-list.* No public endpoints except the health check.
- **Data:** stored in `us-central1`. The CV is in a private GCS bucket, with uniform access and no public ACLs. Automated DB backups. Personal data is never logged.
- **Secrets:** the Claude API key and any search key live in Secret Manager. Each component gets a least-privilege service account (web, jobs, CI deployer).
- **CI/CD:** GitHub → GCP through Workload Identity Federation, so no long-lived keys.
- **LLM:** only the JD text and the profile fields needed for scoring are sent. The Anthropic API data-retention terms apply.
- **Repo:** private. No personal data in the repo (D-003); the seed list holds public company data only.

## 11. Testing and quality

| Layer | Tests |
|---|---|
| Unit | Normalizers, dedup keys, rules filter, weight blending, pay ladder, CRS config parsing |
| Adapter contracts | Recorded JSON fixtures for each ATS. A nightly live canary pulls one known company per adapter and alerts on schema drift |
| Dedup | A labelled 100-pair set; precision ≥95% (R2) |
| Parse eval | A 50-JD labelled set; field accuracy ≥90% and people-management classification ≥90% (R6) |
| Ranking eval | Precision@10 on triage labels (R7). Runs in CI on any prompt or model change |
| E2E | A Playwright smoke test against the deployed revision: digest loads in under 2s, triage works, capture works, **every source icon resolves to a posting URL rather than a homepage or search page** (R2 click-through test) |

## 12. Cost estimate (monthly, for Ayush's decision)

**Infrastructure (approximate list prices; verify in the GCP pricing calculator):**
- Cloud Run service and jobs: low traffic, likely **within the free tier** to a few dollars
- Cloud Scheduler: ≤3 jobs free
- Postgres: **Cloud SQL smallest instance ≈ $10–15**, *or* a free external Postgres (e.g. a Neon free tier), *or* Firestore's free tier (no Postgres; rework needed)
- Artifact Registry, Secret Manager, Storage, Logging: well under $2

**Note:** a Claude.ai subscription (Pro, Max) covers Ayush's own use of Claude and Claude Code (i.e. building Lodestone). It does **not** cover the app's Claude API calls, which are billed separately, pay-as-you-go, through an Anthropic Console account (or Vertex AI).

**Claude usage.** Assumptions: about 150 new relevant jobs a day after the rules stage (≈4,500 a month), about 5K input and 2K output tokens per job for parse plus score. Prompt caching cuts the repeated profile and instructions. The Batch API (50% off) suits the daily run. Prices are Anthropic's first-party list (as of 2026-10-06).

| Option | Models | Est. / month (cached + batch → uncached) |
|---|---|---|
| **A. Best quality** (the skill's default model) | Claude Opus 5.5 for parse and score on every job | **≈ $105 → $270** |
| **B. Tiered** | Claude Haiku 5.5 parses and pre-scores every job; Claude Opus 5.5 re-scores the top ~20 a day with full reasons | **≈ $25 → $45** |
| **C. Lowest cost** | Claude Haiku 5.5 for everything | **≈ $5 → $10** |

Option C is roughly 40× cheaper per token than Option A. The quality difference for *this* task is unknown until measured. **Plan:** build the eval set first (50 labelled JDs + early triage), run A and C on it, then lock the choice with real numbers. Until then the app runs whichever option Ayush chooses.

## 13. Decisions needed from Ayush

| # | Decision | Recommendation |
|---|---|---|
| E-1 | **Database:** Cloud SQL Postgres (~$10–15/mo, all in GCP) vs. free external Postgres vs. Firestore | Cloud SQL Postgres: simplest to run, and it stays in your own GCP project |
| E-2 | **Claude models and budget** (Q-10): Option A, B or C in §12 | Your call. My suggestion is to start on B and confirm with the eval |
| E-3 | **Claude via the Anthropic API or Google Vertex AI** | Anthropic API (newest features, server-side fallback). Vertex keeps billing in GCP if you prefer |
| E-4 | **ATS reverse search:** Claude `web_search` tool vs. a separate search API | Claude `web_search`: one vendor, no extra key |
| E-5 | **GCP setup:** you create the project and billing account, then add me through CI (WIF). A one-time step-by-step guide is in M4 Sprint 1 | Personal GCP project `lodestone-prod` |

## 14. Build plan (commits M4 and M5)

Sprints are measured in working sessions, not calendar days (D-020). Each sprint ends deployed to Cloud Run.

| Sprint | Scope | Exit |
|---|---|---|
| **S1. Skeleton** | Repo scaffold, FastAPI and React app, Postgres plus migrations, CI/CD to Cloud Run with WIF, IAP sign-in, seed load | A sign-in-protected empty app is live; pushes auto-deploy |
| **S2. Ingestion** | Greenhouse, Lever, Ashby and SmartRecruiters adapters, Canada filter, dedup, sightings with exact URLs, liveness, scheduler | Real jobs from the seed companies in the DB daily |
| **S3. Match** | CV upload and profile parse, JD parse, scoring, weights, digest UI and listing detail | The digest ranks real jobs with explanations |
| **S4. Workflow** | Triage (with Later resurfacing), pipeline, capture (paste URL or text), settings, companies screens, pay estimates, pathway signals plus ESDC load | All P0 CUJs work end to end |
| **S5. Discovery + quality** | Discovery engine (P1–P4), eval harness and CI gates, Playwright smoke test, source health, Workday and Workable once verified | **M4 dogfood** |
| Hardening | Bug bash, launch checklist (privacy, ToS, quality bar) | **M5 launch** |

**Estimate:** S1–S5 ≈ 10–15 working sessions; hardening ≈ 2–3. Calendar dates stay rolling (D-020).

## 15. Risks

| Risk | Mitigation |
|---|---|
| An ATS endpoint changes or blocks access | Adapter contract tests plus a nightly canary. Source health in the UI |
| LLM cost overrun | Batch API plus caching. A monthly spend cap enforced in the app, with an alert at 80% |
| IAP-on-Cloud-Run limits | A documented fallback (§10) |
| This dev environment can't reach ATS APIs (I-01) | Run adapter tests against recorded fixtures, with live checks in Cloud Run. Or allow the hosts in the environment's network settings |
