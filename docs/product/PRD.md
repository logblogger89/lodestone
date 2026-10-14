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
| CR-1 | **Adjustable comp range.** The user sets a target comp range (normalized to CAD) in the app, and listings are filtered or scored against it | D-014 | DR-2 supplies the normalization and defaults. Uses the anchor from A-02 |
| CR-2 | **Toggle: include postings without a pay range.** On or off. When on, the listing shows "pay not disclosed", or an estimate with a confidence level if DR-2 supports one | D-014 | Ontario pay-transparency rules may make posted ranges more common. Check in DR-2 |
| CR-3 | **Immigration-pathway signal per Canadian listing.** For example: LMIA-exempt (ICT), likely Global Talent Stream, sponsorship mentioned, and how it would build toward CEC or PNP. Usable as a filter or sort | Ayush (answer to Q-14) | Signals only, not advice (R-03). *Interpretation to confirm with Ayush* |
| CR-4 | **Current-employer awareness and an "internal transfer" badge.** Know the user's current employer (via LinkedIn connect, import or manual entry). When a listing's employer matches it, label the listing "internal transfer" and show the ICT route | Ayush (answer to Q-16), D-012 | Feasibility risk R-10: LinkedIn API limits |
| CR-5 | **Optional in-app Express Entry profile and CRS calculator.** The user enters their own and their spouse's details (age, education, language, work experience, ECA). Lodestone computes the CRS, shows which levers move it and by how much (a year of Canadian work experience, French, a provincial nomination, swapping the principal applicant), and weights or labels listings by how much they advance PR | Ayush (answer to Q-17) | Every field optional. CRS rules live in versioned config (R-12). Not advice (R-03) |
| CR-6 | **People-management toggle.** Include or exclude roles that have direct reports. Defaults to exclude | Ayush (answer to Q-18) | Needs a "manages people" classifier on each listing |
| NFR-1 | **Runs locally.** The MVP runs on the user's own machine | D-015 | Input to the Eng Design Doc |

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
| DR-1 | **Leveling equivalency.** Google L5/L6 compared with Amazon, Meta, Microsoft, Shopify, Canadian banks and scale-ups, plus heuristics for startups | Level fit scoring |
| DR-2 | **Comp normalization.** USD→CAD, cost of living, base/bonus/equity weighting, a liquidity discount for private equity, and the target and floor (Q-02) | Comp fit scoring |
| DR-3 | **Immigration pathways.** Employer work permit with LMIA, Global Talent Stream, intra-company transfer (for example, Google US → Google Canada), Express Entry PR without a job offer, provincial programs (OINP), CEC after Canadian work experience, category-based draws, and comparing either spouse as principal applicant. What signals can be read from job listings | Eligibility scoring and a parallel PR track |
| DR-4 | **Job-source inventory.** Public ATS feeds (Greenhouse, Lever, Ashby, Workday), career pages, aggregators. ToS and legal feasibility | Sourcing (also an input to the Eng Design Doc) |

## 5. Deferred to the PRD session (Ayush: "let's chat MVP and post-MVP in detail")

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
