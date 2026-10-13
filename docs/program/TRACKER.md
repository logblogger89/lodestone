# Lodestone — Program Tracker

> The live status of the work in [`PROGRAM_PLAN.md`](./PROGRAM_PLAN.md). Claude updates it at the end of every working session.
> Legend: `⬜ Not started` · `🟦 In progress` · `🟨 In review` · `✅ Done` · `⛔ Blocked` · `➖ Dropped` | RAG: `🟢` `🟡` `🔴`

**Last updated:** 2026-10-13 · **Current milestone:** M0 → M1 · **Overall RAG:** 🟢

**Status summary (2026-10-13).** Program Plan v2 is in review. The artifacts now follow Google's split: PgM docs here, product content in the PRD stub. Ayush answered the scope questions on audience, level, geography and motivation. **Next:** approve M0, then answer the M1 blockers (Q-02 comp floor, Q-13 capacity, Q-14 immigration profile), then start the PRD session.

---

## 1. Milestone dashboard

| # | Milestone | RAG | Status | Target | Gate approved | Notes |
|---|---|---|---|---|---|---|
| M0 | Program kickoff | 🟢 | 🟨 In review | 10-13 | — | Plan v2 and tracker restructured |
| M1 | PRD approved | 🟢 | ⬜ | 10-14 | — | Depends on Q-02, Q-14 and DR-1 to DR-4 |
| M2 | UX review passed | 🟢 | ⬜ | 10-15 | — | |
| M3 | Eng Design Doc approved | 🟢 | ⬜ | 10-16 | — | M4 and M5 dates get committed here |
| M4 | MVP dogfood | 🟢 | ⬜ | TBD at M3 | — | Placeholder: about 2 weeks after M3 |
| M5 | Launch (v1) | 🟢 | ⬜ | TBD at M3 | — | |
| M6 | Post-launch review | 🟢 | ⬜ | Launch + 2 weeks | — | |

## 2. Deliverables

| ID | Deliverable | Workstream | Milestone | Status | Owner | Link / notes |
|---|---|---|---|---|---|---|
| D0.1 | Program Plan | PgM | M0 | 🟨 | Claude → Ayush | [PROGRAM_PLAN.md](./PROGRAM_PLAN.md) |
| D0.2 | Tracker | PgM | M0 | 🟨 | Claude → Ayush | this file |
| D0.3 | Repo skeleton, README, CLAUDE.md | PgM | M0 | ✅ | Claude | |
| D1.1 | DR-1 Leveling equivalency | Domain research | M1 | ⬜ | Claude | PRD §4 |
| D1.2 | DR-2 Comp normalization | Domain research | M1 | ⬜ | Claude | Needs Q-02 |
| D1.3 | DR-3 Immigration pathways | Domain research | M1 | ⬜ | Claude | Signals only, not advice. Needs Q-14 |
| D1.4 | DR-4 Job-source inventory and ToS | Data and sourcing | M1 | ⬜ | Claude | |
| D1.5 | PRD v1 | Product | M1 | ⬜ | Ayush + Claude | [PRD.md](../product/PRD.md) (stub) |
| D2.1 | CUJ flows and IA | Product (UX) | M2 | ⬜ | Claude | |
| D2.2 | Mocks and visual direction | Product (UX) | M2 | ⬜ | Claude → Ayush | |
| D2.3 | Clickable prototype | Product (UX) | M2 | ⬜ | Claude | |
| D2.4 | UX spec and review | Product (UX) | M2 | ⬜ | Ayush | |
| D3.1 | Eng Design Doc | Engineering | M3 | ⬜ | Claude → Ayush | Includes the extensibility design (D-005) |
| D3.2 | ADRs (stack, hosting, sourcing, scoring) | Engineering | M3 | ⬜ | Claude → Ayush | |
| D3.3 | Build plan and estimate (commits M4 and M5) | PgM / Eng | M3 | ⬜ | Claude → Ayush | |
| D4.1 | MVP build | Engineering | M4 | ⬜ | Claude | |
| D4.2 | Dogfood and bug bash | Launch | M4 | ⬜ | Ayush | |
| D5.1 | Launch checklist (privacy, security, ToS, quality) | Launch | M5 | ⬜ | Claude | |
| D6.1 | Post-launch review and V1.x roadmap | PgM / Product | M6 | ⬜ | Ayush + Claude | |

## 3. Decision log

| ID | Date | Decision | Rationale | Decided by |
|---|---|---|---|---|
| D-001 | 10-13 | The program runs as gated stages: PgM, then Product (requirements, UX), then Engineering design, then Build | Ayush's direction | Ayush |
| D-002 | 10-13 | All program docs live in the repo under `docs/`. Status lives only in `TRACKER.md` | One source of truth, versioned | Ayush |
| D-003 | 10-13 | No resume or personal contact details are committed to the repo | Privacy | Ayush |
| D-004 | 10-13 | Readable copies are published to the Lodestone Google Drive folder. The repo stays canonical | Easy to read and share | Ayush |
| D-005 | 10-13 | Built for one, ready for many: user-specific dimensions are config or plugins | Extensible after the MVP | Ayush |
| D-006 | 10-13 | Single-user and private for now. Revisit going public at M6 | Ayush's direction | Ayush |
| D-007 | 10-13 | Geography: GTA plus Waterloo first, then the rest of Canada if results are thin. Any work mode | Ayush's direction | Ayush |
| D-008 | 10-13 | Level: any level, as long as it is competitive and comparable to current scope | Widens a market that may be thin (R-07) | Ayush |
| D-009 | 10-13 | Artifacts follow Google practice: the Program Plan is PgM only, the PRD holds all product work (including UXR, UX and mocks), and the Eng Design Doc covers engineering | Ayush's direction | Ayush |
| D-010 | 10-13 | Milestones M0–M6 replace the earlier phases. Build dates (M4, M5) get committed at M3 | An honest schedule only exists after scope and design are set | Proposed (Claude) |

## 4. Open questions

| ID | Question | Blocks | Status | Answer |
|---|---|---|---|---|
| Q-01 | Single-user or multi-user? | — | ✅ Answered | Just Ayush for now, could go public later (D-006) |
| Q-02 | Comp: the walk-away floor and the "would move for" number, in CAD. How should private equity be valued? | M1 (DR-2) | Open | |
| Q-03 | Target level? | — | ✅ Answered | Any level that is competitive and comparable to current scope (D-008) |
| Q-04 | Geography and work mode? | — | ✅ Answered | GTA plus Waterloo, then the rest of Canada. Any work mode (D-007) |
| Q-05 | Why Canada? What does the immigration goal look like? | — | ✅ Answered | PR, then citizenship. Stability with a newborn, no employer-tied status, travel freedom (PRD §2) |
| Q-06 | Domain preferences | — | ➡️ Deferred to PRD session | |
| Q-07 | Company-type preferences | — | ➡️ Deferred to PRD session | |
| Q-08 | Scope beyond "find" (resume tailoring, referrals, interview prep) | — | ➡️ Deferred to PRD session | |
| Q-09 | Delivery surface (web, email digest) | — | ➡️ Deferred to PRD session | |
| Q-10 | Monthly budget for hosting and LLM/API costs | M3 | Open | |
| Q-11 | Should the repo be public or private? | — | ✅ Answered | Private for now (D-006). Scrub personal details before any public release (A-03) |
| Q-12 | Is there a target date to start applying, have an offer, or move? | M3 (build priority) | Open | |
| Q-13 | **Capacity.** How many hours a week can Ayush spend on reviews and gates? | Schedule for M1–M5 | Open | |
| Q-14 | **Immigration profile.** Do you or your spouse have an Express Entry profile, a CRS estimate, language test results or an ECA? This decides whether a PR route without a job offer can run in parallel | M1 (DR-3) | Open | |
| Q-15 | **Hard dates.** H-1B extension or expiry, vesting or refresh cliffs, parental leave: anything that constrains timing | M3 | Open | |
| Q-16 | Is a Google-internal transfer to Google Toronto or Waterloo on the table? If so, it's an LMIA-exempt channel to track | M1 (DR-3) | Open | |

## 5. RAID log (risks, assumptions, issues, dependencies)

| ID | Type | Description | Impact | Mitigation / next step | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | Risk | Job sources may restrict automated access (e.g. LinkedIn ToS) | High | Prefer public ATS feeds and official APIs (DR-4) | Claude | Open |
| R-02 | Risk | Comp data for Canadian roles is sparse | Med | Use pay-transparency postings where they exist, plus benchmarks. Show confidence levels | Claude | Open |
| R-03 | Risk | Immigration rules are complex and change over time | High | Show signals, never advice. Validate with a licensed consultant or lawyer | Ayush | Open |
| R-04 | Risk | The compressed schedule to M3 may lower quality | Med | Time-boxed gates, MVP cut line | Ayush + Claude | Open |
| R-05 | Risk | LLM fit scores may be noisy | Med | Labeled eval set, explainable sub-scores | Claude | Open |
| R-06 | Risk | Over-engineering for extensibility slows the MVP | Med | Build the seams now, but only one implementation of each | Claude | Open |
| R-07 | Risk | Few roles fit, because Canadian employers are reluctant to sponsor (LMIA) | High | Widen geography and level (D-007, D-008). Weight LMIA-exempt routes. Consider a parallel PR track (Q-14, Q-16) | Ayush + Claude | Open |
| R-08 | Risk | Ayush's limited time slows the gates | Med | Claude pre-drafts, reviews stay short and async | Claude | Open |
| A-01 | Assumption | Google L5 maps roughly to Amazon L6/L7 and to "Senior/Principal PM" elsewhere | — | Validate in DR-1 | Claude | Open |
| A-02 | Assumption | Comp anchor of about US$450K TC (US$229K base, 15% bonus, about US$187K equity per year) | — | Confirm in DR-2 | Ayush | Open |
| A-03 | Assumption | The repo stays private. The PRD holds personal immigration and family context | — | Scrub it before any public release (M6) | Claude | Open |
| DEP-1 | Dependency | Ayush's review time at each gate | — | See Q-13 | Ayush | Open |
| DEP-2 | Dependency | Job sources that are legal to use | — | DR-4 | Claude | Open |
| DEP-3 | Dependency | Budget decision | — | See Q-10 | Ayush | Open |
| DEP-4 | Dependency | Comp target and immigration profile | — | See Q-02 and Q-14 | Ayush | Open |

## 6. Change log

| Date | Change | By |
|---|---|---|
| 2026-10-13 | Created the program plan, tracker and README | Claude |
| 2026-10-13 | Added the extensibility principle, the Drive companion folder and CLAUDE.md | Claude |
| 2026-10-13 | Restructured to Google-style artifacts: the Program Plan is PgM only (OKRs, milestones M0–M6, staffing, governance), and product content moved to a PRD stub. Recorded Ayush's answers (D-006 to D-008). Added Q-13 to Q-16 and R-07, R-08 | Claude |

## 7. Published artifacts (Google Drive)

Folder: [Lodestone](https://drive.google.com/drive/folders/1Lg2FCikLlqf2YzYX--DrWZ4w2fUCQ4GV)

| Artifact | Type | Source in repo | Drive link | Last synced |
|---|---|---|---|---|
| Program Plan v2 | Google Doc | docs/program/PROGRAM_PLAN.md | [Open](https://docs.google.com/document/d/1uN4yjH74UHUzIk1aHfKpV8YDsLtMhYH6hfHaOsS5aq8/edit) | 2026-10-13 |
| Program Tracker | Google Sheet (one tab per section) | docs/program/TRACKER.md | [Open](https://docs.google.com/spreadsheets/d/1gnJmUCWiPqOAelZ44zO_wDcLAYOKlTFBCzn2hJwEJwU/edit) | 2026-10-13 |
| PRD (stub) | Google Doc | docs/product/PRD.md | [Open](https://docs.google.com/document/d/1DAm9z6qX6K8gUXFmxLJ-EeHHLu0B_UII5FT4_1iDvgk/edit) | 2026-10-13 |
