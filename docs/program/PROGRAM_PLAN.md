# Lodestone — Program Plan

> A personal job portal that finds, ranks and tracks senior product roles in the Greater Toronto Area (GTA) for one user: an L5 Google PM (operating at L6 scope) on an H-1B in the NYC area, with a ~US$450K total-comp anchor.

| | |
|---|---|
| **Owner / PM** | Ayush Gupta |
| **Partner** | Claude: research, docs, prototyping, engineering |
| **Status** | Phase 0 (program setup) |
| **Last updated** | 2026-10-13 |
| **Live status** | [`TRACKER.md`](./TRACKER.md) |

---

## 1. Why this program exists

Searching for jobs across borders comes down to three translation problems that generic job boards don't solve:

1. **Title and level translation.** "Product Manager", "Product Lead", "Group PM", "Product Owner" and "Technical PM" mean different things at different companies. A Google L5 maps to roughly L6/L7 at Amazon and to "Senior" or "Principal" elsewhere. At a startup the title tells you very little about the level.
2. **Comp translation.** US$450K at Google (US$229K base, a 15% bonus target and about US$187K in equity) has to be converted into CAD. It also has to be adjusted for the cost of living in Toronto and for comp bands that are structurally lower in Canada, and liquid public RSUs have to be compared fairly with private-company equity.
3. **Eligibility translation.** The roles have to be workable for someone moving from the US to Canada. That includes employer-supported work permits, the Global Talent Stream, intra-company transfers, and a possible Express Entry path.

Lodestone's job is to handle all three on every listing, so the user only spends time on roles that pass.

## 2. Program goals (draft, to be confirmed in Phase 1)

| # | Goal | Draft success signal |
|---|---|---|
| G1 | Find the relevant GTA PM roles without manual searching | ≥ 90% of roles the user would have found manually also show up in Lodestone |
| G2 | Rank by real fit (level, comp, domain, visa) | Most of the top 10 in each digest are worth applying to |
| G3 | Track the pipeline from discovery to offer | One place for the status of every application |
| G4 | Be fun and a showcase | A portfolio-quality product with PM artifacts behind it |
| G5 | Be extensible after the MVP to other users, roles, geographies and criteria | Adding a new role family or geography takes configuration, not a rewrite |

### 2.1 Design principle: built for one, ready for many

The MVP serves one user: Ayush, a senior PM looking in the GTA. Everything specific to that user is modeled as **data or configuration, never hard-coded logic**, so the product can later serve other people with other roles, in other places, with other criteria:

| Dimension | MVP value | Extension point |
|---|---|---|
| User | Ayush | User profile and preferences per user. The data model is ready for multiple tenants |
| Role family | Product management (PM, GPM, TPM, Product Lead…) | A pluggable role taxonomy and title-synonym packs |
| Geography | GTA (± Waterloo) | Geo packs: locations, currency, cost-of-living index, pay-transparency rules |
| Leveling | Google ladder ↔ other companies | Leveling maps per role family, as versioned data |
| Comp | USD→CAD with a cost-of-living adjustment and an equity liquidity discount | A comp model driven by per-user anchor and weights |
| Eligibility | US H-1B → Canada work authorization | Eligibility rule packs per (origin status, destination country) |
| Sources | Public ATS feeds and career pages | Source adapters behind a common interface |
| Scoring | Fit criteria for Ayush | User-weighted criteria with explainable sub-scores |

Rule of thumb for every requirement and design decision: *"Would this still work for a nurse in Berlin?"* If the answer is no, the specific part belongs in a profile or pack, not in the core.

## 3. Phases, deliverables and exit gates

The work runs as four gated phases. A phase closes only when its exit criteria are met and the user signs off. Each sign-off is logged in the tracker's Decision Log.

```
Phase 0      Phase 1              Phase 2               Phase 3              Phase 4
Setup   -->  Requirements    -->  Design / Prototype -> Technical Design --> Build (coding)
(today)      brainstorm + PRD     flows, wireframes,    architecture,        milestone-based
             leveling & comp      clickable prototype   data sourcing,       sprints
             frameworks                                 ADRs
```

### Phase 0: Program setup
| ID | Deliverable | Location |
|---|---|---|
| P0.1 | Program plan (this doc) | `docs/program/PROGRAM_PLAN.md` |
| P0.2 | Tracker: status, decisions, open questions, RAID | `docs/program/TRACKER.md` |
| P0.3 | Repo skeleton and README | `/README.md`, `docs/` |

**Exit gate:** the user approves the plan, the phase dates and how the tracker works.

### Phase 1: Requirements brainstorm and PRD
| ID | Deliverable | Notes |
|---|---|---|
| P1.1 | Problem statement, goals and non-goals | The MVP is single-user, but the extensibility constraints in §2.1 are in scope as requirements |
| P1.2 | User profile and job-search persona | Experience, domains (Enterprise AI, Trust & Safety, Data platforms, Commerce), must-haves and deal-breakers |
| P1.3 | Critical user journeys (CUJs) | e.g. "Morning digest", "Evaluate a role", "Tailor and apply", "Track pipeline", "Prep for interview" |
| P1.4 | Feature brainstorm, then a prioritized backlog | Diverge first, then converge with MoSCoW and RICE. MVP / V1 / Later cut lines |
| P1.5 | **Leveling equivalency framework** (spec) | Google L5/L6 mapped to Amazon, Meta, Microsoft, Shopify and Canadian banks, plus heuristics for startups (stage, headcount, scope, reports) |
| P1.6 | **Comp normalization framework** (spec) | USD→CAD, cost-of-living adjustment, base/bonus/equity weighting, liquidity discount for private equity, target band and walk-away floor |
| P1.7 | **Eligibility and immigration model** (spec) | Which listing signals matter (sponsorship, GTS, remote-in-Canada, relocation). Also note the Google-internal transfer path (Google Toronto/Waterloo) as its own channel |
| P1.8 | **Job-source inventory and feasibility** | ATS public feeds (Greenhouse, Lever, Ashby, Workday), company career pages, aggregators. ToS and legal checks (e.g. no LinkedIn scraping) |
| P1.9 | Success metrics | North-star and guardrail metrics for a single-user tool |
| P1.10 | **PRD v1** that brings P1.1–P1.9 together | `docs/requirements/PRD.md` |

**Exit gate:** the PRD is signed off, the MVP scope is frozen, and the three frameworks (P1.5–P1.7) are approved with test cases.

### Phase 2: UX design and prototype
| ID | Deliverable | Notes |
|---|---|---|
| P2.1 | Information architecture and sitemap | |
| P2.2 | User flows for each MVP CUJ | |
| P2.3 | Low-fi wireframes | Key screens: Digest, Job detail (with fit breakdown), Pipeline board, Profile and preferences |
| P2.4 | Visual direction | Name, tone, palette, type. The "lodestone/compass" motif |
| P2.5 | Clickable hi-fi prototype | HTML prototype filled with realistic sample jobs |
| P2.6 | Design review and usability self-test | Walk each CUJ and log the issues |
| P2.7 | **Design doc v1** | `docs/design/DESIGN.md` |

**Exit gate:** the prototype covers every MVP CUJ and the design doc is signed off.

### Phase 3: Technical design
| ID | Deliverable | Notes |
|---|---|---|
| P3.1 | System architecture | Frontend, backend, scheduler, storage |
| P3.2 | Data model | Job, Company, Source, FitScore, Application, Preference |
| P3.3 | Ingestion design | Source adapters, deduplication, freshness, rate limits, ToS compliance |
| P3.4 | Matching and scoring design | Rules plus LLM scoring that uses the P1.5–P1.7 frameworks. Explainable scores, eval set |
| P3.5 | Hosting, cost and ops | Budget ceiling, deploy pipeline, monitoring |
| P3.5a | Extensibility design | Plugin and config boundaries for sources, role taxonomies, geo, comp and eligibility packs. Multi-tenant-ready data model (see §2.1) |
| P3.6 | Security and privacy | The resume and comp data are PII: auth, secrets, data retention |
| P3.7 | Test strategy and eval plan | Unit, integration and scoring evals against a labeled set of jobs |
| P3.8 | ADRs (Architecture Decision Records) | `docs/tech/adr/NNNN-*.md` |
| P3.9 | Build plan: milestones and sprint breakdown | Feeds Phase 4 |
| P3.10 | **Tech design doc v1** | `docs/tech/TECH_DESIGN.md` |

**Exit gate:** the tech design is signed off, the stack is chosen through ADRs, and the build milestones are estimated.

### Phase 4: Build (outline only, detailed in P3.9)
Milestones are illustrative until Phase 3 sets them: **M1** skeleton and deploy → **M2** ingestion from the first sources → **M3** fit scoring → **M4** digest UI and job detail → **M5** pipeline tracker → **M6** polish and launch.

## 4. Timeline (targets, not commitments)

The user wants to start coding in about two days, so the design phases are compressed. Each phase is time-boxed. If one overruns, the tracker records a dated replan instead of letting the dates drift silently.

| Phase | Target start | Target end | Time-box |
|---|---|---|---|
| 0: Setup | Tue 2026-10-13 | Tue 2026-10-13 | 0.5 day |
| 1: Requirements | Tue 2026-10-13 | Wed 2026-10-14 | 1 day |
| 2: Design / prototype | Wed 2026-10-14 | Thu 2026-10-15 | 1 day |
| 3: Technical design | Thu 2026-10-15 | Fri 2026-10-16 | 0.5–1 day |
| 4: Build | Fri 2026-10-16 → | per P3.9 | sprints |

## 5. Ways of working

- **Single source of truth.** All docs live in this repo under `docs/`. Status lives only in `TRACKER.md`.
- **Readable companion copies (Google Drive).** Shareable versions of key artifacts (docs, sheets, slides) are published to the [Lodestone Drive folder](https://drive.google.com/drive/folders/1Lg2FCikLlqf2YzYX--DrWZ4w2fUCQ4GV). The repo stays canonical. Drive copies are refreshed at milestones and gates, and links are listed in the tracker's §7.
- **Session ritual.** Each working session starts with a tracker review (2 minutes) and ends with a tracker update: status, decisions, new questions and risks. Claude commits the updates.
- **Decisions.** Every material choice gets a Decision Log entry (`D-###`) with its rationale. Major technical choices also get an ADR.
- **Gates.** A phase moves to ✅ only with an explicit "approved" from the user, logged as a decision.
- **Change control.** Scope added after a gate goes to the backlog as "Later" unless the user explicitly re-opens the gate.
- **Roles (RACI-lite).** The user is accountable for scope, priorities and sign-off. Claude is responsible for drafting, research, prototypes and code, and is consulted on trade-offs.
- **Privacy.** Resume files and personal contact details stay out of the repo. A sanitized `profile` (skills, domains, preferences) is enough for the product.

## 6. Status legend (used in the tracker)

`⬜ Not started` · `🟦 In progress` · `🟨 In review` (waiting on the user) · `✅ Done` · `⛔ Blocked` · `➖ Dropped`

Phase health: `🟢 On track` · `🟡 At risk` · `🔴 Off track`
