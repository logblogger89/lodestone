# Lodestone — Program Tracker

> The live status of the work in [`PROGRAM_PLAN.md`](./PROGRAM_PLAN.md). Update it at the end of every working session.
> Legend: `⬜ Not started` · `🟦 In progress` · `🟨 In review` · `✅ Done` · `⛔ Blocked` · `➖ Dropped` | Health: `🟢` `🟡` `🔴`

**Last updated:** 2026-10-13 · **Current phase:** 0 → 1 · **Overall health:** 🟢

---

## 1. Phase dashboard

| Phase | Health | Status | Target end | Gate approved | Notes |
|---|---|---|---|---|---|
| 0: Setup | 🟢 | 🟨 In review | 2026-10-13 | — | Plan and tracker drafted, waiting on sign-off |
| 1: Requirements | 🟢 | ⬜ | 2026-10-14 | — | Brainstorm agenda ready (§4) |
| 2: Design / prototype | 🟢 | ⬜ | 2026-10-15 | — | |
| 3: Technical design | 🟢 | ⬜ | 2026-10-16 | — | |
| 4: Build | 🟢 | ⬜ | per P3.9 | — | |

## 2. Deliverables

| ID | Deliverable | Phase | Status | Owner | Target | Link / notes |
|---|---|---|---|---|---|---|
| P0.1 | Program plan | 0 | 🟨 | Claude → Ayush | 10-13 | [PROGRAM_PLAN.md](./PROGRAM_PLAN.md) |
| P0.2 | Tracker | 0 | 🟨 | Claude → Ayush | 10-13 | this file |
| P0.3 | Repo skeleton and README | 0 | ✅ | Claude | 10-13 | [README](../../README.md) |
| P1.1 | Problem statement, goals, non-goals | 1 | ⬜ | Ayush + Claude | 10-14 | |
| P1.2 | User profile and persona | 1 | ⬜ | Ayush + Claude | 10-14 | |
| P1.3 | Critical user journeys | 1 | ⬜ | Ayush + Claude | 10-14 | |
| P1.4 | Feature brainstorm and prioritized backlog | 1 | ⬜ | Ayush + Claude | 10-14 | |
| P1.5 | Leveling equivalency framework | 1 | ⬜ | Claude (research) | 10-14 | |
| P1.6 | Comp normalization framework | 1 | ⬜ | Claude (research) | 10-14 | |
| P1.7 | Eligibility and immigration model | 1 | ⬜ | Claude (research) | 10-14 | Not legal advice. Confirm with an immigration lawyer |
| P1.8 | Job-source inventory and feasibility | 1 | ⬜ | Claude (research) | 10-14 | |
| P1.9 | Success metrics | 1 | ⬜ | Ayush + Claude | 10-14 | |
| P1.10 | PRD v1 | 1 | ⬜ | Claude → Ayush | 10-14 | `docs/requirements/PRD.md` |
| P2.1 | Information architecture | 2 | ⬜ | Claude | 10-15 | |
| P2.2 | User flows | 2 | ⬜ | Claude | 10-15 | |
| P2.3 | Wireframes | 2 | ⬜ | Claude | 10-15 | |
| P2.4 | Visual direction | 2 | ⬜ | Ayush + Claude | 10-15 | |
| P2.5 | Clickable prototype | 2 | ⬜ | Claude | 10-15 | |
| P2.6 | Design review and self-test | 2 | ⬜ | Ayush | 10-15 | |
| P2.7 | Design doc v1 | 2 | ⬜ | Claude → Ayush | 10-15 | `docs/design/DESIGN.md` |
| P3.1 | System architecture | 3 | ⬜ | Claude | 10-16 | |
| P3.2 | Data model | 3 | ⬜ | Claude | 10-16 | |
| P3.3 | Ingestion design | 3 | ⬜ | Claude | 10-16 | |
| P3.4 | Matching and scoring design and eval set | 3 | ⬜ | Claude + Ayush (labels) | 10-16 | |
| P3.5 | Hosting, cost and ops | 3 | ⬜ | Claude | 10-16 | |
| P3.6 | Security and privacy | 3 | ⬜ | Claude | 10-16 | |
| P3.7 | Test and eval strategy | 3 | ⬜ | Claude | 10-16 | |
| P3.8 | ADRs | 3 | ⬜ | Claude → Ayush | 10-16 | `docs/tech/adr/` |
| P3.9 | Build plan and milestones | 3 | ⬜ | Claude → Ayush | 10-16 | |
| P3.10 | Tech design doc v1 | 3 | ⬜ | Claude → Ayush | 10-16 | `docs/tech/TECH_DESIGN.md` |

## 3. Decision log

| ID | Date | Decision | Rationale | Decided by |
|---|---|---|---|---|
| D-001 | 2026-10-13 | The program runs as gated phases: Requirements → Design / Prototype → Tech Design → Build | Ayush's direction | Ayush |
| D-002 | 2026-10-13 | All program docs live in the repo under `docs/`. Status lives only in `TRACKER.md` | One source of truth, versioned | Proposed (Claude) |
| D-003 | 2026-10-13 | No resume or personal contact details are committed to the repo | Privacy, since the repo may become public | Proposed (Claude) |

## 4. Open questions (agenda for the Phase 1 brainstorm)

| ID | Question | Feeds | Status | Answer |
|---|---|---|---|---|
| Q-01 | Who is Lodestone for: just you, or could it become multi-user later? This drives auth, data model and scope | P1.1 | Open | |
| Q-02 | Comp target: what's the walk-away floor vs. the "would move for" number, in CAD? How should private-startup equity be valued against Google RSUs? | P1.6 | Open | |
| Q-03 | Level target: L6-equivalent only, or also strong L5-equivalent roles with a clear promo path? Open to Group PM / Head of Product at startups? | P1.5 | Open | |
| Q-04 | Geography: GTA in person, hybrid, or remote-in-Canada? Is Waterloo/Kitchener inside the radius? | P1.1, P1.8 | Open | |
| Q-05 | Immigration: which routes are in play (employer work permit, Global Talent Stream, Google intra-company transfer, Express Entry PR)? Should a Google-internal transfer be tracked as a channel? | P1.7 | Open | |
| Q-06 | Domain preferences: Enterprise AI / agents, Trust & Safety, Data / Governance, Fintech, Commerce? Any industries that are excluded? | P1.2 | Open | |
| Q-07 | Company-type preferences: Big Tech Canada offices, Canadian scale-ups (Shopify, Wealthsimple, Cohere…), banks, startups by stage? | P1.2, P1.8 | Open | |
| Q-08 | How much of the scope is "find" and how much is "act" (tailored resume or cover letter, referral finder, interview prep)? Where does the MVP stop? | P1.4 | Open | |
| Q-09 | Delivery surface: web app only, or also an email/Slack daily digest? | P1.3, P1.4 | Open | |
| Q-10 | Budget limits for hosting and LLM/API spend per month? | P3.5 | Open | |
| Q-11 | Should the repo be public (portfolio piece) or private? | P0, P3.6 | Open | |
| Q-12 | Is there a timeline for the move or the search (e.g. start applying by a certain date)? It sets the build priority | P1.1 | Open | |

## 5. RAID log (risks, assumptions, issues, dependencies)

| ID | Type | Description | Impact | Mitigation / next step | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | Risk | Job sources may restrict automated access (e.g. LinkedIn ToS) | High | Prefer public ATS feeds (Greenhouse, Lever, Ashby) and official APIs. Feasibility check in P1.8 | Claude | Open |
| R-02 | Risk | Comp data for Canadian roles is sparse (many postings omit or show wide bands) | Med | Use the Ontario pay-transparency postings where they exist, plus benchmarks. Show confidence levels | Claude | Open |
| R-03 | Risk | Immigration rules are complex and change over time | High | Treat the eligibility model as signals only, not advice. Validate with an immigration lawyer | Ayush | Open |
| R-04 | Risk | The compressed timeline (about 2 days of design) may cut design quality | Med | Strict time-boxes, MVP cut lines, defer non-MVP to "Later" | Ayush + Claude | Open |
| R-05 | Risk | LLM fit scores may be noisy or uncalibrated | Med | A labeled eval set (P3.4) and explainable sub-scores | Claude | Open |
| A-01 | Assumption | A Google L5 maps roughly to Amazon L6/L7 and to "Senior/Principal PM" at most others, and the target is L6-equivalent scope | — | Validate in P1.5 | Claude | Open |
| A-02 | Assumption | The comp anchor is about US$450K TC (US$229K base, 15% bonus target, about US$187K equity per year) | — | Confirm the equity figure and vesting in P1.6 | Ayush | Open |
| D-01 | Dependency | Toolchain and hosting choice | — | ADRs in Phase 3 | Claude | Open |

## 6. Change log

| Date | Change | By |
|---|---|---|
| 2026-10-13 | Created the program plan, tracker and README. Phase 0 ready for review | Claude |
