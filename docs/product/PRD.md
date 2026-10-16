# Lodestone — Product Requirements Document (PRD)

| | |
|---|---|
| **PM** | Ayush Gupta (lead), Claude (PM partner) |
| **Status** | **v0, approved 2026-10-14** (D-029, gate M1) |
| **Last updated** | 2026-10-14 |
| **Program** | [Program Plan](../program/PROGRAM_PLAN.md) · [Tracker](../program/TRACKER.md) |
| **Research** | [DR-1 Leveling](research/DR-1_LEVELING.md) · [DR-2 Pay](research/DR-2_PAY.md) · [DR-3 Immigration](research/DR-3_IMMIGRATION_PATHWAYS.md) · [DR-4 Job sources](research/DR-4_JOB_SOURCES.md) |

---

## 1. Overview

**Vision (D-066, 10-16):** Lodestone is the job platform for people moving countries for work: *the jobs that fit you, in the country you want to move to, and the ones that will actually hire you.* Its core advantage is helping country-switchers and immigrants (who sponsors, internal-transfer routes, pay in local terms, level translation, the route to permanent status). Citizens and permanent residents are welcome too; for them the work-permit layer simply disappears.

**MVP scope:** destination Canada; tech product and adjacent roles; users from any starting point and any status. Expansion to other destinations, job types and functions comes through packages (destination country: sources, government data, permit routes, pay norms, cities; role type: families and scoring rules; status rules per country), not rebuilds (D-005, D-060, D-061). The first live user is Ayush (P1).

*Original framing (M1, 10-14):* a personal job-search portal that finds roles in Canada that fit a senior PM on a path to Canadian PR, explains *why* each one fits, and tracks the pipeline from discovery to offer.

What makes it different from a generic job board:
- **It understands both sides.** It reads the job description *and* the user's CV, then ranks by real fit (role, level, domain, pay, immigration pathway) with explainable sub-scores.
- **It handles the cross-border details:** levels across companies, pay disclosure (and its gaps), and immigration-pathway signals. A listing is never hidden just because information is missing.
- **It goes to the source.** Jobs come from public ATS feeds, discovery boards help find companies, and LinkedIn and similar sites work through low-friction paste-a-link capture.
- **It's built for one user and ready for many.** Everything user-specific is config (D-005).

## 2. Problem statement

Ayush is a Google L5 PM (operating near L6) on an H-1B in the NYC area. He wants a role in Canada that starts a PR path: a work permit, then 12 months of Canadian work experience, then CEC (DR-3 §2a). Today the search is:
- **Fragmented.** Roles are spread across company ATSs, VC portfolio boards, Canadian aggregators and LinkedIn, with lots of duplicates.
- **Hard to evaluate.** Titles don't map cleanly to levels, senior roles often have no posted pay (Ontario exempts roles above $200K), and immigration feasibility is rarely stated.
- **Time-starved.** Ayush is a new parent with unpredictable free time, so every minute spent searching needs to land on a relevant role.

## 3. Goals and non-goals

**Goals (MVP)**
1. Surface the relevant Canadian PM and PM-adjacent roles from a broad set of sources, deduplicated, with each source visible.
2. Rank roles by explainable fit to Ayush's profile, so the top of the digest is worth his time.
3. Show pay (posted or estimated) and immigration-pathway signals (stated or inferred), clearly labelled.
4. Make triage and pipeline tracking fast enough to do in a few spare minutes.
5. Run locally, keep personal data on the user's machine, and use only sources whose ToS allow it.

**Non-goals (MVP)**
- Multi-user accounts or public hosting (D-006)
- Applying on the user's behalf, or automating any application
- Immigration or legal advice. Lodestone shows signals only (R-03)
- Scraping LinkedIn, Indeed, Glassdoor or Wellfound (DR-4)
- Roles outside Canada (a later geography pack)

## 4. Users and personas

| Persona | Description | MVP? |
|---|---|---|
| **P1: Ayush, cross-border senior PM** | Google L5 PM, enterprise AI, data governance, trust and safety, FS policy, commerce. H-1B holder targeting Canada, open to PM-adjacent IC roles, no people management. Has 5–30 minute windows, often on an iPad | **Primary** |
| **P1b: Any non-citizen, non-PR professional seeking work in Canada, in tech product and adjacent roles** | Same industry as P1 for now. Brings their own resume, current employer, work-permit status (needs a permit, or has an open permit), target regions, level, pay and domains, all set in the app's Profile page (D-060). Gets their own private copy of Lodestone (Q-24 option A, `docs/ops/NEW_USER.md`) | **Designed for in the MVP**; P1 is still the only live user |
| P2: Future cross-border job seeker | Any industry, any origin and destination country. Served through role, geo and eligibility packs, and a shared sign-in | Post-MVP (D-005) |

## 5. Critical user journeys (CUJs)

| # | CUJ | Tier |
|---|---|---|
| **CUJ-1** | **Set up my profile.** Upload my CV, review the extracted profile (roles, scope, domains, current employer), and set preferences (locations, work mode, role families, pay, toggles) | MVP |
| **CUJ-2** | **Morning check.** Open Lodestone, see "N new since yesterday," scan the ranked digest with fit scores, source icons and badges | MVP |
| **CUJ-3** | **Evaluate a role.** Open a listing: parsed summary, fit breakdown with reasons, pay (posted or est.), pathway badges (stated, inferred or unknown), internal-transfer badge, all sources, link to apply. **Plus (10-16, D-065):** the full job description in its own tab with the key sentences highlighted, and a Company & team tab (what the company does, in its own words where possible; the team's description when the posting has one) | MVP |
| **CUJ-4** | **Triage fast.** Mark Interested / Not / Later with a quick reason. The ranking learns from it | MVP |
| **CUJ-5** | **Capture a role I found elsewhere.** Paste a LinkedIn (or any) link, or the JD text. Lodestone parses it, dedups it, scores it and adds the source icon | MVP |
| **CUJ-6** | **Track my pipeline.** Move roles through stages. Lodestone flags postings that have closed | MVP |
| **CUJ-0** | **Get started (D-067).** From first visit to a useful list in about a minute, with or without a resume; add experience later as an upgrade | MVP |
| **CUJ-7** | **Manage my watchlist and sources.** Add or remove companies and see source health | MVP |
| CUJ-8 | Tailor and apply: get a resume version tailored to the role, find referrals, follow an apply checklist | V1 |
| CUJ-9 | Plan my PR path: optional Express Entry profile, CRS what-ifs, PR impact per job | V1 |
| CUJ-10 | Compare roles and offers side by side | V1 / Later |

## 6. Requirements

**Priority:** **P0** = MVP launch blocker · **P1** = V1 fast follow · **P2** = later. IDs refer to the backlog in Appendix D.

### 6.1 P0: MVP

| ID | Requirement | Acceptance criteria |
|---|---|---|
| **R1. Ingestion** (A1, A2) | Pull jobs from public ATS feeds (Greenhouse, Lever, Ashby, SmartRecruiters, plus Workday and Workable once verified) for every company on the watchlist. Use discovery boards (VC portfolio boards, Communitech, YC, Built In Toronto, etc.) to add companies and their ATS slugs. The watchlist is managed in the UI and pre-seeded | Daily refresh. New postings show up within 24h of appearing in an ATS feed. Seed watchlist of 210 companies (data/seed/watchlist_seed.csv). Per-source health shown (last success, item count, errors) |
| **R1a. Company discovery engine** (A2, DR-5) | The watchlist grows automatically. Discovery pathways (ATS reverse search, VC and ecosystem boards, ESDC LMIA list, capture spill-over) feed a candidate queue. Each candidate gets **auto ATS detection** and a **Canada-presence check**, then is auto-accepted or held for review. Pathways are pluggable config | ≥500 watchlist companies within 2 weeks of dogfood. Each company shows its discovery pathway(s), ATS, and open Canadian roles. Mute and block available |
| **R2. Dedup and source attribution** (A1, A4) | Merge the same job across sources, using the canonical ATS ID or URL first and a fuzzy match second. Keep every sighting | One listing per job. **One icon per source**, each one a deep link to the exact posting on that source. **Click-through test: every icon lands on the posting page itself, never a company home page or a search results page.** Posting age, "new since last visit" and a repost flag are visible. Dedup precision ≥95% on a 100-pair spot check |
| **R3. Capture** (A3, A3a, A3b, A3c, A3h) | Paste one or more URLs anywhere (Cmd/Ctrl+V or "+ Add job"). Fall back to pasted JD text. Resolve to the ATS source and dedup. Show coaching tips | A pasted LinkedIn URL produces a scored listing within 30s, or prompts for the JD text if the page can't be fetched. A known job reports "already in Lodestone via X" and adds the icon. A confirmation card lets the user fix the parsed fields |
| **R4. Profile** (H31, CR-4) | Import the CV (PDF or DOCX) into a structured profile: roles, scope signals, domains, skills, seniority, current employer. LinkedIn data export is optional. Every field can be edited | Ayush reviews his profile in ≤10 minutes. Current employer is set (from the CV or manually). No CV is stored in the repo (D-003) |
| **R5. Preferences** (H32, CR-1, CR-2, CR-6, B11) | Locations (GTA + Waterloo by default, expandable), work mode, role families and tiers (Appendix B), a **pay range filter** (CAD), a **"include roles without posted pay"** toggle, a **people-management** toggle (exclude by default) | Every preference is config, not code (D-005). Changes re-rank the digest immediately |
| **R6. JD understanding** (B6) | Parse each posting into a structured record: role family and tier, level signals, domain, must-haves and nice-to-haves, people management, location and work mode, pay, immigration signals | ≥90% field accuracy on a 50-JD labelled sample. People-management classification ≥90% |
| **R7. Match engine** (B6) | Hard filters first (location, work mode, families, people management, pay when on), and missing data **never** excludes a job. Then LLM sub-scores (role, level, domain, skills, pay, pathway), each with a one-line reason. A user-weighted overall score. Default weights: role 25%, level 20%, domain 20%, pathway 15%, pay 10%, skills 10%, **editable in Advanced settings** (D-026) | Every listing shows its score breakdown and reasons. **Quality bar:** ≥50% of the digest top 10 marked Interested or Later during dogfood. Ranking changes are checked against the triage-labelled eval set before they ship (R-05) |
| **R8. Pay display** (B8, DR-2) | Show pay as posted (currency as posted). When it's missing, show an estimate with an **"est." icon** and a confidence level | No estimate ever appears without the est. icon. The estimate's source tier is visible on hover or tap |
| **R9. Pathway signals** (B9, CR-3, CR-3a, DR-3) | Per listing: ICT-eligible, sponsorship mentioned, sponsored before (ESDC positive-LMIA list), GTS-likely, and whether the work location is in Canada (CEC credit). Each one is labelled **Stated / Inferred / Unknown** with its source and date | No listing is hidden for missing signals (D-021). Inferred signals always show their source **as a deep link** (e.g. the ESDC dataset, official IRCC pages). Plain-language explanations of LMIA, CEC, tiers and statuses are available in place. The ESDC list is loaded and matched to companies |
| **R10. Internal-transfer badge** (B10, CR-4) | When the listing's employer equals the user's current employer, show an "Internal transfer" badge and the ICT route | All Google Canada roles carry the badge when the current employer is Google |
| **R11. Daily digest** (D18) | An in-app home view: top N new matches since the last visit (**N=20 by default, configurable from 1 to 100**, D-025), then the full ranked list | Loads in <2s locally. Readable and usable on an iPad browser (responsive) |
| **R11a. Freshness indicator** (D-037) | The app always shows when each part of the data was last refreshed: **job pulls** (overall and per source), **scoring** (last run, plus the prompt and model version that scored the jobs), **pathway signals** (ESDC list quarter and load date), **company discovery**, and **profile** (last update). Refreshes are on request in Phase 1 (D-036) | A header chip shows "Updated <time ago>". Tapping it opens a panel with every component's timestamp and version. Anything older than 7 days is flagged |
| **R12. Triage and learning** (D19) | Interested / Not / Later, with optional quick reasons (e.g. "wrong level," "people management," "domain," "location"). It feeds the weights and the eval set. **Later** roles come back in the digest after 7 days (configurable). **Interested** adds the role to Shortlisted | Triage takes ≤2 taps or keys. Keyboard shortcuts on desktop. Reasons are stored and visible in the eval set |
| **R13. Pipeline** (F25) | Stages: Discovered → Shortlisted → Applied → Screen → Interviewing → Offer → Closed. Liveness check on each refresh | A closed or removed posting is flagged "no longer live" within 24h and kept in the history |
| **R14. Local and private** (NFR-1) | Runs on the user's Windows laptop, and the iPad can reach it on the LAN (or via Tailscale). All personal data stays local. API keys live in local config | No personal data leaves the machine except LLM API calls, which carry only the JD and profile text needed for scoring. Works offline for browsing already-fetched data |
| **R15. Compliant sourcing** (DR-4) | Automated pulls only from sources whose access is permitted. LinkedIn, Indeed, Glassdoor and Wellfound are capture-only (R3) | A source registry records the access method and ToS status for every source |
| **R26. Onboarding without a resume** (D-067, UX §8.3) | First visit: welcome with the promise and privacy line; destination (country, cities); status (citizen/PR, open permit, needs sponsorship, not sure); role in the user's own words, a pasted job they'd love, or example cards; an 8-role taste test (skippable); then their list | A new user sees real, filtered roles within about a minute, with no resume. Each screen asks one question and says why. Citizens and PRs see no work-permit layer |
| **R27. Profile, three ways** (D-067, UX §8.4) | Offered after first value, never as a gate: upload, paste text, or "Build it with me" (about five questions). Read at the next daily run; "Here's what we understood" with every line editable | A user without a resume reaches a complete profile in under 5 minutes. Copy promises privacy, "a rough draft is fine", and delete any time |
| **R28. Today stack** (D-067, UX §8.8) | The home view shows "N new for you" (default up to 10) that can be finished; the full ranked list is one tap away | An "All caught up" state exists. The backlog never appears as the default view. **Built P1-S6 (D-068)** |
| **R29. Learning from signals** (D-067, UX §8.6) | Explicit actions plus reading time on the Job description tab (capped, with an off switch) feed ranking. Preference changes are suggested with one tap to accept, shown with their reason, and undoable. "More / less like this". About 1 in 10 cards is exploration, labelled | No preference changes silently. The off switch stops reading-time collection. The score quality check (D-062) gates any learning change. **Built P1-S6 (D-068)**: ordering with learning 70% vs 60% without, on the owner's triage |
| **R30. Match-quality levels** (D-067, UX §8.5) | Levels 0–4 by what the system knows; a Profile meter shows the level and the next step | The meter is visible from the first visit and moves as the user acts |
| **R31. One-tap questions in context** (D-067, UX §8.7) | Ask a preference question only when an action makes it relevant, once, dismissible | No question repeats after dismissal. Answers update the Profile |

### 6.2 P1: V1 (fast follow)

| ID | Requirement |
|---|---|
| R16 | Level translator, e.g. "Staff PM at X ≈ Google L6" (B7, DR-1), with confidence |
| R17 | "Why this fits you," plus gaps and how to frame them (B12) |
| R18 | Red flags: vague role, layoff or reorg news, chronic reposts (B13). Company hiring signals (A5) |
| R19 | Compare 2–3 roles side by side (B14) |
| R20 | Optional Express Entry profile and CRS calculator with what-ifs, and PR impact per job (C15, C16, CR-5). Rules in versioned config (R-12) |
| R21 | A version of the resume tailored to each posting, plus bullets and a cover letter draft (E21) |
| R22 | Referral finder from the LinkedIn connections export (E22). Apply checklist and one-click open (E24) |
| R23 | Saved searches and alerts (D20). Email digest |
| R24 | Browser "Send to Lodestone" (A3d, after the ToS check, R-14). Job-alert email ingestion (A3e). Search launcher (A3f) |
| R25 | Notes, contacts and reminders per application (F26) |

### 6.3 P2: Later

PR timeline view (C17) · interview prep pack for roles marked Interested (F27) · offer comparator (F28) · market view and what-ifs (G29) · funnel stats (G30) · mobile share target (A3g) · multi-user and admin console.

## 7. UX principles and key screens (mocks at M2)

- **Glanceable in 5 minutes on an iPad.** Digest first, big tap targets, keyboard-first on desktop.
- **Never hide, always label.** Estimates, inferences and unknowns are visible and marked, not silently filtered out.
- **Explain every score.** Every number has a "why."
- **Key screens:** Digest (home) · Listing detail · Pipeline board · Add job (paste) · Profile review · Preferences · Watchlist and Sources.

## 8. Success metrics

| Type | Metric | Target (MVP dogfood) |
|---|---|---|
| **North star** | Relevant roles surfaced per week (marked Interested) | Baseline in week 1, then trending up or holding |
| Quality | Precision@10 of the digest (Interested + Later out of the top 10) | ≥50% |
| Coverage | **Already-known rate:** of the roles Ayush pastes from elsewhere, the share Lodestone had already found | ≥70% by week 2 |
| Freshness | Time from a posting appearing in an ATS to appearing in Lodestone | ≤24h |
| Efficiency | Median time to triage a listing | ≤20s |
| Accuracy | JD parsing field accuracy · people-management classification | ≥90% · ≥90% |
| Guardrails | Jobs hidden for missing data · non-permitted automated access · estimates shown without a label | 0 · 0 · 0 |
| Program link | Applications made from Lodestone-sourced roles (O2) | Tracked, no target |

## 9. Privacy, security and legal

- Personal data (CV, profile, immigration details) is stored only locally, is never committed to the repo (D-003), and gets scrubbed before any public release (A-03).
- LLM calls send only the minimum text needed. The provider and key are set in local config. The spend budget gets decided at M3 (Q-10).
- Source ToS are tracked in the source registry (R15). Polite crawling: rate limits, caching, a clear user agent.
- Immigration content is always labelled "signals, not advice," with links to official IRCC tools.

## 10. Launch plan

| Phase | Scope | Exit |
|---|---|---|
| **MVP dogfood (M4)** | P0 (R1–R15) | Ayush uses it daily for a week, and the metrics are measurable |
| **Launch v1 (M5)** | P0 hardened, bug bash done | Launch checklist (privacy, ToS, quality bar) passed |
| **V1.x** | P1 (R16–R25), prioritized at M6 | Post-launch review |

## 11. Open questions (resolved 2026-10-14)

1. Digest size: **20 by default, user-adjustable up to 100** (D-025).
2. Score weights: the defaults are accepted, and **editable in Advanced settings** (D-026).
3. Seed watchlist: **as many companies as possible, discovered continuously**. The seed has 210 companies plus the discovery engine R1a (DR-5, D-027).
4. Pipeline stages: confirmed.

## 12. Alternatives considered

- **Scraping LinkedIn or Indeed directly.** Rejected: ToS (DR-4). Replaced by capture (R3) and, in V1, email-alert ingestion.
- **Pure keyword matching.** Rejected: it can't handle title and level ambiguity. The LLM scoring with explainable sub-scores and an eval set is kept.
- **Normalizing pay.** Rejected by Ayush (B8). Pay shows as posted, and the filter compares in CAD internally.
- **Hosted web app.** Deferred: local-first for privacy and cost (D-015). LAN or Tailscale gives iPad access.

---

# Appendices

## Appendix A. User inputs captured

| Topic | Input from Ayush |
|---|---|
| **Motivation** | A path to Canadian PR and then citizenship. Today: H-1B, approved I-140, stuck in the EB-2 India queue. Values geographic stability (newborn) and freedom from employer-tied status. Wants to stay in the developed world. Travel freedom from a Canadian passport |
| **Level** | Open to any level, as long as the role is competitive and comparable to his current scope (Google L5, operating near L6) |
| **Role family** | PM roles plus PM-adjacent roles, inside or outside Google. PM roles that fit at Google Canada are scarce (D-011). Which adjacent families count is open (Q-18) |
| **Channels** | External roles plus a Google-internal transfer to Google Canada, which is LMIA-exempt (D-012) |
| **Timeline** | As soon as possible, and comfortably before the H-1B expires in Sep 2027 (D-016) |
| **Express Entry** | There is a profile with strong IELTS scores, but the CRS is low because of age, and it drops at each birthday (R-09). For now a job or work permit is the main path to PR |
| **Work mode** | In-office, hybrid or remote are all fine |
| **Geography** | GTA plus Waterloo first. Expand to the rest of Canada if results are thin |
| **Audience** | Just for Ayush for now. It might go public later. **Updated 10-15 (D-060):** the MVP is designed for any non-citizen, non-PR professional seeking work in Canada in Ayush's industry; every personal input lives in the user's Profile |
| **Market hypothesis** | Canadian employers may be reluctant to hire people outside Canada or without Canadian work experience (because of LMIA), which could limit options. *To be validated in domain research* |

## Appendix B. Default role families (D-017, user-editable)

Proposed by Claude. The defaults are based on Ayush's background: enterprise AI and data platforms, trust and safety, risk and compliance, commerce, and analytics.

| Tier | Role families | Rationale |
|---|---|---|
| **Core** | Product Manager / Senior PM / Group PM (IC), Product Lead, Product Owner (at senior scope) | Direct match |
| **Adjacent: strong** | Technical Program Manager, Product-facing Program Manager, Product Operations, Product Strategy / Strategy & Operations / BizOps, Chief of Staff (IC) | Same skills (roadmaps, cross-functional leadership, strategy). Common in Canadian tech, banks and scale-ups |
| **Adjacent: domain** | Trust & Safety / Risk / Fraud / Compliance product or program roles, AI governance and responsible-AI roles, data platform or analytics product roles | Uses Ayush's domain depth. Banks and fintechs in Toronto hire these |
| **Adjacent: stretch (off by default)** | Product Marketing Manager, Solutions or Customer Engineer, Product Analytics Lead | Partial overlap. Can be turned on if results are thin |
| **Excluded by default** | Any role with direct reports (CR-6), project coordinator or junior PM titles | Ayush's preference and level fit |

## Appendix C. Sponsor requirements (CR) and NFRs

| ID | Candidate requirement | Source | Notes |
|---|---|---|---|
| CR-1 | **Adjustable comp range.** The user sets a target comp range in the app, and listings are filtered or scored against it. **Pay is shown as posted, not normalized** (brainstorm B8). The filter compares in CAD internally | D-014, B8 | DR-2 supplies the conversion and estimation method |
| CR-2 | **Toggle: include postings without a pay range.** On or off. When on, the listing shows an **estimated** range, marked with an "est." icon (B8) | D-014 | Ontario pay-transparency rules may make posted ranges more common. Check in DR-2 |
| CR-3 | **Immigration-pathway signal per Canadian listing.** For example: LMIA-exempt (ICT), likely Global Talent Stream, sponsorship mentioned, and how it would build toward CEC or PNP. Usable as a filter or sort | Ayush (answer to Q-14) | Signals only, not advice (R-03). *Interpretation to confirm with Ayush* |
| CR-3a | **Fill in missing pathway signals with research.** If a posting doesn't say, look up employer-level evidence: whether they have sponsored before, for example ESDC's published lists of employers with positive LMIAs (to verify), Global Talent Stream use, intra-company transfer patterns, and whether the role builds Canadian work experience toward CEC or a provincial nomination. Show each signal as Yes / Likely / Unknown, with its source and date. **Never exclude a listing because signals are missing** (D-021) | Ayush (CR-3 confirmation) | Possible data sources go in DR-3 and DR-4. R-13 |
| CR-4 | **Current-employer awareness and an "internal transfer" badge.** Know the user's current employer (via LinkedIn connect, import or manual entry). When a listing's employer matches it, label the listing "internal transfer" and show the ICT route | Ayush (answer to Q-16), D-012 | Feasibility risk R-10: LinkedIn API limits |
| CR-5 | **Optional in-app Express Entry profile and CRS calculator.** The user enters their own and their spouse's details (age, education, language, work experience, ECA). Lodestone computes the CRS, shows which levers move it and by how much (a year of Canadian work experience, French, a provincial nomination, swapping the principal applicant), and weights or labels listings by how much they advance PR | Ayush (answer to Q-17) | Every field optional. CRS rules live in versioned config (R-12). Not advice (R-03) |
| CR-6 | **People-management toggle.** Include or exclude roles that have direct reports. Defaults to exclude | Ayush (answer to Q-18) | Needs a "manages people" classifier on each listing |
| NFR-1 | **Runs locally.** The MVP runs on the user's own machine | D-015 | Input to the Eng Design Doc |

## Appendix D. Feature backlog (brainstorm 2026-10-14)

Tiers: **MVP** (v1 launch) · **V1** (fast follow) · **Later** · **Dropped**. Priorities (P0/P1/P2) get assigned in PRD v0.

| ID | Feature | Tier | Notes from Ayush |
|---|---|---|---|
| A1 | Multi-source ingestion: ATS feeds, career pages, **niche boards** (e.g. a16z and other VC portfolio boards). **Dedup across boards.** Each listing shows **an icon for every source** it was found on | MVP | Full source inventory in DR-4 |
| A2 | Company watchlist, managed in the UI and pre-seeded | MVP | |
| A3 | Paste any job URL (including LinkedIn) to parse and score it | MVP | The legal way to use LinkedIn (R-01) |
| A3a | **Quick add anywhere.** Paste a URL anywhere in the app (Cmd/Ctrl+V), or use a global "+ Add job" button. Accepts **several URLs at once**. Shows a confirmation card with the parsed fields so the user can correct them | MVP | |
| A3b | **Fallback: paste the JD text.** When a page can't be fetched (e.g. LinkedIn's login wall), the user pastes the job description text, which gets parsed the same way | MVP | |
| A3c | **Resolve to the source.** If a pasted posting links to the company's ATS, follow the link and attach the listing to the canonical ATS record. If the job is already known, say so ("already in Lodestone via Greenhouse") and just add the source icon | MVP | Dedup (DR-4 §3) |
| A3d | **One-click capture from the browser.** A bookmarklet or extension, "Send to Lodestone," that captures the job page the user is viewing | V1 | ToS check before building (R-14) |
| A3e | **Job-alert email ingestion.** Parse LinkedIn, Indeed and Glassdoor job-alert emails that the user already gets, from a Gmail label or by forwarding | V1 | The user's own email, so no scraping |
| A3f | **Search launcher.** Generate ready-made searches on LinkedIn, Indeed and Wellfound from the user's preferences (titles, locations, families), opening in the browser for fast manual browsing | V1 | |
| A3g | **Mobile share target.** Share a job from the phone (e.g. the LinkedIn app) straight into Lodestone | Later | Needs the app reachable from the phone, which conflicts with local-only hosting (D-015) |
| A3h | **In-app coaching.** Empty states and tips: "Found a role on LinkedIn? Paste the link or press Cmd+V," a first-run tour, and shortcut hints | MVP | |
| A4 | Dedup, repost flag, posting age, "new since last visit" | MVP | |
| A5 | Company hiring signals (funding, headcount, layoffs) | V1 | |
| B6 | **Match engine:** fit score with explainable sub-scores. See §2d | MVP | **The core of the product** |
| B7 | Level translator (e.g. "Staff PM at X ≈ Google L6") | V1 | |
| B8 | Pay shown **as posted**. An estimate when none is posted, with an "est." icon | MVP | Ties to CR-1 and CR-2. **More important than first thought:** Ontario exempts roles above $200K from pay disclosure (DR-4 §1) |
| B9 | Immigration-pathway signals, **marked as inferred** when they come from research | MVP | Ties to CR-3 and CR-3a |
| B10 | Internal-transfer badge, using the current employer from LinkedIn or the profile | MVP | Ties to CR-4. R-10 |
| B11 | People-management toggle and role-family tiers | MVP | Ties to CR-6 and §2b |
| B12 | "Why this fits you," plus gaps and how to frame them | V1 | |
| B13 | Red flags (vague role, reorg or layoff news, chronic reposts) | V1 | |
| B14 | Compare 2–3 roles side by side | V1 | |
| C15 | Express Entry profile and CRS calculator with what-if levers | V1 | Ties to CR-5 |
| C16 | PR impact for each job. **CEC credit only when the work is done in Canada** (remote-from-US roles get none) | V1 | DR-3 §2a |
| C17 | PR pathway timeline view: offer → permit → move → 12 months → CEC → PR | Later | DR-3 §2a |
| D18 | Daily digest (in-app; email in V1) | MVP | |
| D19 | Triage (interested / not / later, with reasons) that learns preferences | MVP | Feeds the match engine (§2d) |
| D19a | **Adaptive recommendations ("like Spotify").** Learn from behaviour as well as explicit triage: which postings Ayush opens and how long he spends on them, what he shortlists, moves through the pipeline, marks Later or rejects (and the reasons), market checks he requests. Use these signals to refine ranking over time. Open points to explore together: which signals to trust (implicit vs explicit), how fast it adapts and how to keep it explainable ("ranked higher because you shortlisted 3 similar AI-governance roles"), avoiding a filter bubble (keep some exploration), cold start, and privacy when there are many users (D-005) | Idea (to scope with Ayush, then roadmap) | Seed idea from Ayush, 2026-10-15. Builds on D19, the fit score (B6) and the calibration in D-049 |
| D20 | Saved searches and alerts | V1 | |
| E21 | **A version of the resume tailored to each posting** (plus tailored bullets and a cover letter draft) | V1 | |
| E22 | Referral finder (LinkedIn connections export, alumni) | V1 | |
| E23 | Internal-transfer helper | **Dropped** | Ayush doesn't need it |
| E24 | Apply checklist and one-click open of the application page | V1 | |
| F25 | Pipeline board. **Auto-flag postings that are no longer live** | MVP (basic) | Liveness check on each refresh |
| F26 | Notes, contacts and reminders per application | V1 | |
| F27 | Interview prep pack **for each role marked "interested"** | Later | |
| F28 | Offer comparator (pay and PR impact) | Later | |
| G29 | Market view and what-ifs (e.g. "expanding geography adds X roles") | Later | |
| G30 | Funnel stats | Later | |
| H31 | Profile import from **CV** (primary), LinkedIn export, or manual entry | MVP | The CV feeds the match engine |
| H32 | Preferences: locations, work mode, families, pay, toggles (all config) | MVP | D-005 |

## Appendix E. Match engine approach (B6)

The match engine is the core of the product. Its shape is below; the details belong in the Eng Design Doc.

1. **Understand the user (profile model).** Parse the CV, plus the LinkedIn export if available, into a structured profile: role history, scope signals (team size led, cross-functional breadth, exec exposure, metrics moved), domains (enterprise AI and agents, data governance, trust and safety, fintech and financial-services policy, commerce, analytics), skills, seniority, and current employer. Ayush can review and edit it, and his preferences (H32) sit on top.
2. **Understand each job (JD parsing).** Turn every posting into a structured record: role family and tier, level signals (title, years, scope language, "lead/own/define"), domain, must-haves vs nice-to-haves, people management (yes/no), location and work mode, pay (as posted or estimated), and immigration signals (stated or inferred).
3. **Hard filters first, cheap and transparent.** Location, work mode, people management, role families, and the pay filter when it's on. Missing data never hides a job (D-021).
4. **Then score fit.** An LLM compares the profile to the parsed JD and returns sub-scores (role, level, domain, skills, pay, pathway), each with a one-line reason. The overall score is a **user-weighted** blend, and the weights are config (D-005).
5. **Learn from triage (D19).** Interested / not / later, plus reasons, become labeled data. They tune the weights, and they become the **eval set** that checks ranking quality before any change to the engine ships (R-05).
6. **Show the top hits.** The daily digest (D18) shows the top N new roles, each with its score breakdown, its source icons (A1) and its badges (est. pay, inferred pathway, internal transfer).

**Quality bar (draft, for the metrics section):** most of the top 10 in each digest are worth Ayush's time, and nothing he would have applied to is buried below the fold.

## Appendix F. Product principle: built for one, ready for many (D-005)

The MVP serves one user. Everything specific to that user is modeled as **data or configuration, never hard-coded logic**:

| Dimension | MVP value | Extension point |
|---|---|---|
| User | Ayush | User profile and preferences per user. The data model is ready for multiple tenants |
| Role family | PM plus PM-adjacent families (defined via Q-18) | A pluggable role taxonomy and title-synonym packs |
| Geography | GTA plus Waterloo, then the rest of Canada | Geo packs: locations, currency, cost-of-living index, pay-transparency rules |
| Leveling | Google ladder ↔ other companies | Leveling maps per role family, as versioned data |
| Comp | USD→CAD with a cost-of-living adjustment and an equity liquidity discount | A comp model driven by a per-user anchor and weights |
| Eligibility | US H-1B (Indian citizen) → Canadian work permit → PR | Eligibility rule packs per (origin status, destination country) |
| Sources | Public ATS feeds and career pages | Source adapters behind a common interface |
| Scoring | Fit criteria for Ayush | User-weighted criteria with explainable sub-scores |

Test for every requirement: *"Would this still work for a nurse in Berlin?"*

## Appendix G. Original problem framing

Searching for jobs across borders comes down to three translation problems that generic job boards don't solve:

1. **Title and level.** "Product Manager", "Product Lead", "Group PM", "Product Owner" and "Technical PM" mean different things at different companies. A Google L5 maps to roughly L6/L7 at Amazon and to "Senior" or "Principal" elsewhere. At a startup the title tells you very little about the level.
2. **Comp.** Google total comp of about US$450K (US$229K base, 15% bonus target, about US$187K a year in equity) has to be converted into CAD. It also has to be adjusted for the cost of living and for Canadian comp bands, which are structurally lower, and public RSUs have to be compared fairly with private-company equity.
3. **Eligibility.** A role only counts if it can lead to a valid work authorization and, from there, to PR. Many Canadian employers avoid hiring from abroad because of the LMIA process. LMIA-exempt routes, such as intra-company transfers, matter a lot.
