# Lodestone — Product Requirements Document (PRD)

| | |
|---|---|
| **PM** | Ayush Gupta (lead), Claude (PM partner) |
| **Status** | **Stub.** Inputs captured. Active work starts in the Product phase (gate M1) |
| **Last updated** | 2026-10-14 |
| **Program** | [Program Plan](../program/PROGRAM_PLAN.md) · [Tracker](../program/TRACKER.md) |

> This stub collects product inputs that came up during program setup so nothing is lost. The PRD will be written in full during the Product phase. Its planned outline is in §6.

---

## 1. Problem framing (draft)

Searching for jobs across borders comes down to three translation problems that generic job boards don't solve:

1. **Title and level.** "Product Manager", "Product Lead", "Group PM", "Product Owner" and "Technical PM" mean different things at different companies. A Google L5 maps to roughly L6/L7 at Amazon and to "Senior" or "Principal" elsewhere. At a startup the title tells you very little about the level.
2. **Comp.** Google total comp of about US$450K (US$229K base, 15% bonus target, about US$187K a year in equity) has to be converted into CAD. It also has to be adjusted for the cost of living and for Canadian comp bands, which are structurally lower, and public RSUs have to be compared fairly with private-company equity.
3. **Eligibility.** A role only counts if it can lead to a valid work authorization and, from there, to PR. Many Canadian employers avoid hiring from abroad because of the LMIA process. LMIA-exempt routes, such as intra-company transfers, matter a lot.

## 2. User inputs captured (2026-10-13)

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
| **Audience** | Just for Ayush for now. It might go public later |
| **Market hypothesis** | Canadian employers may be reluctant to hire people outside Canada or without Canadian work experience (because of LMIA), which could limit options. *To be validated in domain research* |

## 2a. Candidate requirements from the sponsor (2026-10-14, not yet prioritized)

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

## 2c. Feature backlog (brainstorm 2026-10-14, cut line approved by Ayush)

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
| C16 | PR impact for each job | V1 | |
| C17 | PR pathway timeline view | Later | |
| D18 | Daily digest (in-app; email in V1) | MVP | |
| D19 | Triage (interested / not / later, with reasons) that learns preferences | MVP | Feeds the match engine (§2d) |
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

## 2d. Core matching approach (B6): understand the JD, understand the user, rank

The match engine is the core of the product. Its shape is below; the details belong in the Eng Design Doc.

1. **Understand the user (profile model).** Parse the CV, plus the LinkedIn export if available, into a structured profile: role history, scope signals (team size led, cross-functional breadth, exec exposure, metrics moved), domains (enterprise AI and agents, data governance, trust and safety, fintech and financial-services policy, commerce, analytics), skills, seniority, and current employer. Ayush can review and edit it, and his preferences (H32) sit on top.
2. **Understand each job (JD parsing).** Turn every posting into a structured record: role family and tier, level signals (title, years, scope language, "lead/own/define"), domain, must-haves vs nice-to-haves, people management (yes/no), location and work mode, pay (as posted or estimated), and immigration signals (stated or inferred).
3. **Hard filters first, cheap and transparent.** Location, work mode, people management, role families, and the pay filter when it's on. Missing data never hides a job (D-021).
4. **Then score fit.** An LLM compares the profile to the parsed JD and returns sub-scores (role, level, domain, skills, pay, pathway), each with a one-line reason. The overall score is a **user-weighted** blend, and the weights are config (D-005).
5. **Learn from triage (D19).** Interested / not / later, plus reasons, become labeled data. They tune the weights, and they become the **eval set** that checks ranking quality before any change to the engine ships (R-05).
6. **Show the top hits.** The daily digest (D18) shows the top N new roles, each with its score breakdown, its source icons (A1) and its badges (est. pay, inferred pathway, internal transfer).

**Quality bar (draft, for the metrics section):** most of the top 10 in each digest are worth Ayush's time, and nothing he would have applied to is buried below the fold.

## 2b. Default role families (D-017, user-editable)

Proposed by Claude. The defaults are based on Ayush's background: enterprise AI and data platforms, trust and safety, risk and compliance, commerce, and analytics.

| Tier | Role families | Rationale |
|---|---|---|
| **Core** | Product Manager / Senior PM / Group PM (IC), Product Lead, Product Owner (at senior scope) | Direct match |
| **Adjacent: strong** | Technical Program Manager, Product-facing Program Manager, Product Operations, Product Strategy / Strategy & Operations / BizOps, Chief of Staff (IC) | Same skills (roadmaps, cross-functional leadership, strategy). Common in Canadian tech, banks and scale-ups |
| **Adjacent: domain** | Trust & Safety / Risk / Fraud / Compliance product or program roles, AI governance and responsible-AI roles, data platform or analytics product roles | Uses Ayush's domain depth. Banks and fintechs in Toronto hire these |
| **Adjacent: stretch (off by default)** | Product Marketing Manager, Solutions or Customer Engineer, Product Analytics Lead | Partial overlap. Can be turned on if results are thin |
| **Excluded by default** | Any role with direct reports (CR-6), project coordinator or junior PM titles | Ayush's preference and level fit |

## 3. Product principle: built for one, ready for many (D-005)

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

## 4. Domain research needed (inputs to the PRD)

| ID | Research spec | Feeds |
|---|---|---|
| DR-1 | **Leveling equivalency.** Google L5/L6 compared with Amazon, Meta, Microsoft, Shopify, Canadian banks and scale-ups, plus heuristics for startups **v1 done: [research/DR-1_LEVELING.md](research/DR-1_LEVELING.md).** | Level fit scoring |
| DR-2 | **Comp normalization.** USD→CAD, cost of living, base/bonus/equity weighting, a liquidity discount for private equity, and the target and floor (Q-02) **v1 done: [research/DR-2_PAY.md](research/DR-2_PAY.md).** | Comp fit scoring |
| DR-3 | **Immigration pathways.** Employer work permit with LMIA, Global Talent Stream, intra-company transfer (for example, Google US → Google Canada), Express Entry PR without a job offer, provincial programs (OINP), CEC after Canadian work experience, category-based draws, and comparing either spouse as principal applicant. What signals can be read from job listings **v1 done: [research/DR-3_IMMIGRATION_PATHWAYS.md](research/DR-3_IMMIGRATION_PATHWAYS.md).** | Eligibility scoring and a parallel PR track |
| DR-4 | **Job-source inventory.** **v1 done: [research/DR-4_JOB_SOURCES.md](research/DR-4_JOB_SOURCES.md).** Summary: discover companies broadly, ingest from public ATS feeds, and use A3 (paste URL) for LinkedIn, Indeed and Wellfound | Sourcing (also an input to the Eng Design Doc) |

## 5. PRD session status

The brainstorm is done (§2c). The MVP cut line was approved 2026-10-14 (D-022). Still to come in PRD v0: personas and CUJs, P0/P1/P2 requirements with acceptance criteria, and success metrics. The items below are kept for reference:

- CUJs and personas
- How far beyond "find" the product goes: tailored resume, referrals, interview prep
- Delivery surface: web only, or also an email digest
- Domain and company-type preferences (Q-06, Q-07)
- MVP vs V1.x vs Later cut lines, P0/P1/P2 requirements
- Product success metrics (feeds KR2.2)

## 6. Planned PRD outline (Google style)

1. Overview and background
2. Problem statement and opportunity
3. Goals and non-goals
4. Users, personas and CUJs
5. Requirements (P0 / P1 / P2) with acceptance criteria
6. UX: flows, mocks, prototype (links to the UX spec)
7. Success metrics and instrumentation
8. Privacy, security and legal considerations
9. Launch plan (phasing and the MVP cut line)
10. Open questions, alternatives considered, appendix (domain research)
