# Lodestone — Program Plan

| | |
|---|---|
| **Program** | Lodestone: a personal job-search portal for roles in Canada |
| **Sponsor and decision-maker** | Ayush Gupta |
| **Program manager (TPgM)** | Claude |
| **Doc status** | Draft v2, in review |
| **Last updated** | 2026-10-13 |
| **Live status** | [`TRACKER.md`](./TRACKER.md) |

> **Scope of this doc.** This is the *program* plan: why the program exists, what it commits to, milestones, timeline, staffing, governance and risks. *Product* content (users, CUJs, requirements, features, UX) lives in the PRD ([`docs/product/PRD.md`](../product/PRD.md)) and is worked in the Product phase.

---

## 1. Background and mission

Ayush is a Google PM in NYC on an H-1B. He has an approved I-140, but in the EB-2 India queue a US green card is years away. The H-1B ties his family's status to a single employer, and with a newborn the family puts a high value on geographic stability. **Canada offers a path to permanent residency and then citizenship.** Canadian citizenship would also give the family the travel freedom they want.

The biggest lever on that path is a qualifying Canadian job offer, or a parallel PR route that doesn't need one. Lodestone is the tool that makes that search systematic.

**Mission:** Build and run a personal job-search portal that consistently finds the Canadian roles worth Ayush's time and helps him land one that starts his PR path.

## 2. Objectives and key results

| Objective | Key results | Target |
|---|---|---|
| **O1. Ship the Lodestone MVP on schedule** | KR1.1 PRD, UX and Eng Design Doc approved at their gates | By M3 |
| | KR1.2 MVP in daily dogfood use | By M4 |
| **O2. Lodestone powers the actual job search** | KR2.1 Lodestone is the main source of new leads (vs. manual browsing) | Within 2 weeks after launch |
| | KR2.2 Targets for qualified roles surfaced and applications made per week | Set in the PRD (Phase 1) |
| **O3. Build in a way that is portfolio-quality and extensible** | KR3.1 A complete set of Google-style artifacts (Program Plan, PRD, UX spec, Eng Design Doc, launch checklist) | By M5 |
| | KR3.2 An architecture that allows other users, roles and geographies after the MVP, with no rewrite | Verified at the M3 design review |

The program's real outcome, Ayush landing a role, depends on the job market as well as the product, so it is tracked as the North Star but isn't a KR the program controls.

## 3. Program scope

| In scope | Out of scope (for now) |
|---|---|
| A single-user product for Ayush, kept private | Multi-user accounts, a public launch. Revisit after launch (D-006) |
| Roles in Canada: GTA and Waterloo first, then the rest of Canada if results are thin | Roles outside Canada |
| Discovery, fit evaluation and tracking of roles (details in the PRD) | Running the applications themselves or giving immigration legal advice |
| An architecture that can extend to other users, roles and geographies later (D-005) | Building those extensions before the MVP launches |

## 4. Workstreams

| Workstream | What it covers | Lead |
|---|---|---|
| **PgM** | Plan, tracker, milestones, risks, status, launch coordination | Claude (TPgM) |
| **Product** | PRD, CUJs, requirements and prioritization, UX research, UX design, mocks, prototype, metrics. Following Google practice, UX, UXR and interaction design sit under the PM | Ayush (PM lead) with Claude (PM partner) |
| **Engineering** | Eng Design Doc, ADRs, build, test, deploy, ops | Claude (SWE / TL) |
| **Data and sourcing** | Job sources and feeds, ToS and legal checks, data quality | Claude (SWE), reviewed by Ayush |
| **Domain research** | Leveling equivalency, comp benchmarks, Canadian immigration pathways. These feed the PRD | Claude (research), validated by Ayush |
| **Launch** | Privacy and security review, launch checklist, dogfood, launch | Claude (TPgM) |

## 5. Milestones and timeline

All dates are **targets, not commitments**. Each milestone has a gate that Ayush approves, and every approval is logged in the Decision Log. If a milestone slips, it gets a dated re-baseline in the tracker. Dates never drift silently.

| # | Milestone | Exit criteria (gate) | Target |
|---|---|---|---|
| **M0** | Program kickoff | Program Plan and tracker approved | Tue 10-13 |
| **M1** | PRD approved | Problem, users, CUJs, P0/P1/P2 requirements, MVP cut line, metrics. Domain research (leveling, comp, immigration) folded in | Wed 10-14 |
| **M2** | UX review passed | Flows, mocks and a clickable prototype that cover every P0 CUJ | Thu 10-15 |
| **M3** | Eng Design Doc approved | Architecture, data model, sourcing, scoring, extensibility seams, privacy and security, test plan, build estimate | Fri 10-16 |
| **M4** | MVP dogfood | P0 CUJs work end to end on real job data, and Ayush uses it daily | **Re-baselined at M3** (placeholder: ~2 weeks after M3) |
| **M5** | Launch (v1) | Launch checklist complete (privacy, security, ToS, quality bar), launch approved | **Re-baselined at M3** |
| **M6** | Post-launch review | Review against O2, then a V1.x roadmap and a decision on going public | Launch + 2 weeks |

The build schedule (M4 and M5) can't be committed honestly until the scope is frozen at M1 and the design is set at M3. It is committed at M3.

## 6. Staffing and roles (RASCI)

The program is a two-person team. Claude takes on each functional hat. Ayush is the sponsor, the PM lead and the only approver.

| Activity | Ayush | Claude |
|---|---|---|
| Program goals, scope, gate approvals | **A/R** | C |
| Plan, tracker, status, risks | A | **R** |
| PRD and requirements | **A**/R | R (drafts) |
| UXR, UX design, mocks, prototype | A | **R** |
| Domain research (leveling, comp, immigration) | A / validates | **R** |
| Eng Design Doc, ADRs, build, test | A | **R** |
| Launch checklist and launch | A | **R** |

*R = Responsible, A = Accountable, S = Supporting, C = Consulted, I = Informed*

**Capacity constraint.** Ayush works a full-time PM job and has a newborn. His available hours (Q-13) set how fast reviews and gates can move. Claude will always pre-read and pre-draft so his review time stays short.

## 7. Governance and cadence

- **Working sessions.** Each session opens with a 2-minute tracker review and closes with a tracker update, which Claude commits.
- **Gates.** M1–M5 each need Ayush's explicit "approved", logged as a `D-###` decision.
- **Status.** At the end of each session the tracker header carries a one-line RAG status (Green, Yellow or Red), plus a short summary of what happened and what's next.
- **Decisions.** Every material decision is recorded in the Decision Log with its rationale. Engineering decisions also get ADRs.
- **Change control.** Once M1 is approved, new scope goes to the backlog as V1.x unless Ayush reopens the gate.
- **Artifacts.** The repo is the source of truth. Readable copies (Docs, Sheets, Slides) are published to the [Lodestone Drive folder](https://drive.google.com/drive/folders/1Lg2FCikLlqf2YzYX--DrWZ4w2fUCQ4GV) at each gate (D-004).

## 8. Dependencies

| ID | Dependency | Needed by | Owner |
|---|---|---|---|
| DEP-1 | Ayush's review time at each gate | M1–M5 | Ayush |
| DEP-2 | Access to job sources that are legal to use (public ATS feeds, career pages) | M3 design, M4 build | Claude |
| DEP-3 | Hosting and LLM/API budget decision (Q-10) | M3 | Ayush |
| DEP-4 | Ayush's comp floor and target (Q-02) and his immigration profile (Q-14) | M1 | Ayush |

## 9. Top risks

The full RAID log is in the tracker. These are the risks that matter at program level:

| ID | Risk | Mitigation |
|---|---|---|
| R-04 | The compressed planning schedule (about 3 days to M3) could lower quality | Time-boxed gates, MVP cut line, and anything that isn't MVP goes to V1.x |
| R-07 | The Canadian market may not have enough roles that fit: employers often avoid sponsoring foreign hires because of the work-permit (LMIA) process | Widen geography if needed (D-007). Weight LMIA-exempt routes in the PRD. Treat a PR route that doesn't need a job offer as a parallel track (Q-14) |
| R-08 | Ayush's limited time slows the gates | Claude pre-drafts everything, and reviews are kept short and async-friendly |
| R-03 | Immigration rules are complex and change over time | Lodestone only shows signals, never advice. Any decision gets validated with a licensed immigration consultant or lawyer |

## 10. Document index

| Artifact | Type | Owner | Status |
|---|---|---|---|
| Program Plan (this doc) | PgM | Claude → Ayush | In review |
| [Tracker](./TRACKER.md) (status, deliverables, decisions, questions, RAID) | PgM | Claude | Live |
| [PRD](../product/PRD.md) | Product | Ayush + Claude | Stub, inputs captured |
| UX spec, mocks and prototype | Product | Claude → Ayush | Not started (M2) |
| Eng Design Doc and ADRs | Engineering | Claude → Ayush | Not started (M3) |
| Launch checklist | PgM / Launch | Claude | Not started (M5) |
