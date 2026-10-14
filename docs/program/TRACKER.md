# Lodestone — Program Tracker

> The live status of the work in [`PROGRAM_PLAN.md`](./PROGRAM_PLAN.md). Claude updates it at the end of every working session.
> Legend: `⬜ Not started` · `🟦 In progress` · `🟨 In review` · `✅ Done` · `⛔ Blocked` · `➖ Dropped` | RAG: `🟢` `🟡` `🔴`

**Last updated:** 2026-10-14 · **Current milestone:** M0 → M1 · **Overall RAG:** 🟢

**Status summary (2026-10-14, end of day).** All PgM questions are closed. CR-3 is confirmed and extended: listings with no pathway info are kept, and missing signals get filled from employer-level research (CR-3a). No offer-by date (D-019). Milestones are gate-sequenced with rolling dates because the sponsor's time is unpredictable (D-020). M1 to M3 dates are now rolling. **Next:** PRD v0, drafted async by Claude for Ayush to review when he has a slot.

---

## 1. Milestone dashboard

| # | Milestone | RAG | Status | Target | Gate approved | Notes |
|---|---|---|---|---|---|---|
| M0 | Program kickoff | 🟢 | ✅ Done | 10-13 | ✅ 10-14 (D-013) | |
| M1 | PRD approved | 🟢 | 🟦 In progress | Rolling (D-020) | — | Claude drafts PRD v0 async. Depends on DR-1 to DR-4 |
| M2 | UX review passed | 🟢 | ⬜ | Rolling | — | |
| M3 | Eng Design Doc approved | 🟢 | ⬜ | Rolling | — | M4 and M5 estimates get committed here |
| M4 | MVP dogfood | 🟢 | ⬜ | TBD at M3 | — | Placeholder: about 2 weeks after M3 |
| M5 | Launch (v1) | 🟢 | ⬜ | TBD at M3 | — | |
| M6 | Post-launch review | 🟢 | ⬜ | Launch + 2 weeks | — | |

## 2. Deliverables

| ID | Deliverable | Workstream | Milestone | Status | Owner | Link / notes |
|---|---|---|---|---|---|---|
| D0.1 | Program Plan | PgM | M0 | ✅ | Claude → Ayush | [PROGRAM_PLAN.md](./PROGRAM_PLAN.md) |
| D0.2 | Tracker | PgM | M0 | ✅ | Claude → Ayush | this file |
| D0.3 | Repo skeleton, README, CLAUDE.md | PgM | M0 | ✅ | Claude | |
| D1.1 | DR-1 Leveling equivalency | Domain research | M1 | ⬜ | Claude | PRD §4 |
| D1.2 | DR-2 Comp normalization | Domain research | M1 | ⬜ | Claude | Needs Q-02 |
| D1.3 | DR-3 Immigration pathways | Domain research | M1 | ⬜ | Claude | Signals only, not advice. Priority raised (R-09). Should cover CEC after a work permit, PNP, category-based draws, and comparing either spouse as principal applicant |
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
| D-011 | 10-14 | Role scope widens from PM roles to PM and PM-adjacent roles, inside or outside Google. The exact adjacent families get defined in the PRD (Q-18) | Google Canada has few PM roles that fit, and Ayush is open to adjacent work | Ayush |
| D-012 | 10-14 | A Google-internal transfer (Google Canada) is tracked as its own channel next to external roles | Intra-company transfers are LMIA-exempt, so this is likely the fastest route to a work permit | Ayush |
| D-013 | 10-14 | **M0 approved:** Program Plan v2 and the tracker | Gate review | Ayush |
| D-014 | 10-14 | Comp target is a user setting in the app, not a program input: an adjustable range filter, plus a toggle that includes postings without a pay range | Keeps the program unblocked, and it's better product (D-005) | Ayush |
| D-015 | 10-14 | The MVP runs locally. Hosting budget isn't needed. LLM/API spend still gets decided at M3 | Ayush's direction | Ayush |
| D-016 | 10-14 | Program deadline: the H-1B expires in Sep 2027, so the search aims to land an offer and work permit comfortably before then. The exact offer-by date is still open (Q-19) | Ayush's direction | Ayush |
| D-017 | 10-14 | Claude defines the default PM-adjacent role families (PRD §2b). They are user-editable config, not hard-coded | Ayush delegated Q-18 | Ayush (delegated) |
| D-018 | 10-14 | Batch syncing: the repo tracker updates every session, and the Drive Sheet and Docs refresh only at gates (or on request) | Less link churn and noise | Ayush |
| D-019 | 10-14 | No offer-by date or deadline. The goal is to see what's available and apply to relevant postings. The Sep 2027 H-1B expiry stays as context only | Ayush's direction (Q-19) | Ayush |
| D-020 | 10-14 | Milestones follow gate sequence, not the calendar. Dates are rolling and re-baselined as needed, and a slip from sponsor availability doesn't count against RAG | The sponsor's capacity is unpredictable (Q-13) | Ayush |
| D-021 | 10-14 | Listings with no immigration-pathway info are never excluded. Missing signals get filled from employer-level research and shown with a source and a confidence level, or as "unknown" | Relevant roles often don't mention sponsorship (CR-3a) | Ayush |

## 4. Open questions

| ID | Question | Blocks | Status | Answer |
|---|---|---|---|---|
| Q-01 | Single-user or multi-user? | — | ✅ Answered | Just Ayush for now, could go public later (D-006) |
| Q-02 | Comp: the walk-away floor and the "would move for" number, in CAD. How should private equity be valued? | — | ✅ Resolved | It becomes an in-app setting (D-014). DR-2 still defines the normalization method and sensible defaults |
| Q-03 | Target level? | — | ✅ Answered | Any level that is competitive and comparable to current scope (D-008) |
| Q-04 | Geography and work mode? | — | ✅ Answered | GTA plus Waterloo, then the rest of Canada. Any work mode (D-007) |
| Q-05 | Why Canada? What does the immigration goal look like? | — | ✅ Answered | PR, then citizenship. Stability with a newborn, no employer-tied status, travel freedom (PRD §2) |
| Q-06 | Domain preferences | — | ➡️ Deferred to PRD session | |
| Q-07 | Company-type preferences | — | ➡️ Deferred to PRD session | |
| Q-08 | Scope beyond "find" (resume tailoring, referrals, interview prep) | — | ➡️ Deferred to PRD session | |
| Q-09 | Delivery surface (web, email digest) | — | ➡️ Deferred to PRD session | |
| Q-10 | Monthly budget for hosting and LLM/API costs | M3 | Partly answered | Hosting is local (D-015). LLM/API spend is deferred to M3 |
| Q-11 | Should the repo be public or private? | — | ✅ Answered | Private for now (D-006). Scrub personal details before any public release (A-03) |
| Q-12 | Is there a target date to start applying, have an offer, or move? | — | ✅ Answered | As soon as possible, and comfortably before the H-1B expires in Sep 2027 (D-016) |
| Q-13 | Capacity: how much review time per week? | — | ✅ Answered | Unpredictable (newborn). Dates will move as needed (D-020) |
| Q-14 | **Immigration profile.** Do you or your spouse have an Express Entry profile, a CRS estimate, language test results or an ECA? | — | ✅ Answered | There is an Express Entry profile with strong IELTS scores, but the CRS is low because of age (Ayush turns 37 on 11-15, his spouse turns 33 on 01-03). A PR route without a job offer isn't realistic on its own right now, so a job is the main path |
| Q-15 | **Hard dates.** H-1B extension or expiry, vesting or refresh cliffs, parental leave: anything that constrains timing | — | ✅ Answered | The H-1B expires in Sep 2027 (D-016) |
| Q-19 | Offer-by date? | — | ✅ Answered | None. Explore and apply to relevant roles (D-019) |
| Q-16 | Is a Google-internal transfer to Google Toronto or Waterloo on the table? If so, it's an LMIA-exempt channel to track | — | ✅ Answered | Yes. PM roles that fit at Google Canada are scarce, so Ayush is open to PM-adjacent roles inside or outside Google (D-011, D-012) |
| Q-17 | Express Entry details for DR-3 | — | ✅ Resolved | They become optional in-app inputs: an Express Entry profile and CRS calculator that adjust listings (CR-5). Ayush has the details and will enter them in the app |
| Q-18 | Which PM-adjacent families count? | — | ✅ Resolved | Delegated to Claude (D-017), with defaults in PRD §2b. No people-management roles by default, via a toggle (CR-6) |

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
| R-08 | Risk | Ayush's review time is unpredictable (newborn), which slows the gates | Med | Claude pre-drafts, reviews stay short and async. Rolling, gate-sequenced dates (D-020) | Claude | Open |
| A-01 | Assumption | Google L5 maps roughly to Amazon L6/L7 and to "Senior/Principal PM" elsewhere | — | Validate in DR-1 | Claude | Open |
| A-02 | Assumption | Comp anchor of about US$450K TC (US$229K base, 15% bonus, about US$187K equity per year) | — | Confirm in DR-2 | Ayush | Open |
| R-09 | Risk | The CRS score drops at each birthday after 35 (Ayush on 11-15, spouse on 01-03), so a PR route without a job offer gets harder over time | High | Treat getting a work permit sooner as the priority (ICT and LMIA-exempt routes). DR-3 to check levers: CEC after Canadian work experience, PNP, category-based draws, spouse as principal applicant. Validate with a licensed consultant (RCIC) | Ayush + Claude | Open |
| R-10 | Risk | LinkedIn's API probably won't expose the user's current employer to a personal app (OAuth sign-in returns only basic identity) | Med | DR-4 checks this. Fallbacks: import the LinkedIn data export or profile PDF, parse the resume, or enter it manually | Claude | Open |
| R-11 | Risk | Starting the search late leaves less buffer before the H-1B expires (Sep 2027) | Med | Ship the MVP fast. Run the Google transfer channel in parallel. No fixed offer-by date (D-019) | Ayush + Claude | Open |
| R-12 | Risk | The CRS rules (points grid, how job offers count, category draws) change over time, so a hard-coded calculator would go stale | Med | Put CRS rules in versioned config (D-005), show the rules version and date, and link to the official IRCC calculator for verification | Claude | Open |
| R-13 | Risk | Employer-level sponsorship signals from web research may be stale, wrong or unverifiable | Med | Prefer official data, e.g. ESDC's published positive-LMIA employer lists (to verify in DR-3/DR-4). Show the source, date and a confidence level, and never hide a listing because of it (D-021) | Claude | Open |
| A-03 | Assumption | The repo stays private. The PRD holds personal immigration and family context | — | Scrub it before any public release (M6) | Claude | Open |
| DEP-1 | Dependency | Ayush's review time at each gate | — | See Q-13 | Ayush | Open |
| DEP-2 | Dependency | Job sources that are legal to use | — | DR-4 | Claude | Open |
| DEP-3 | Dependency | Budget decision | — | See Q-10 | Ayush | Open |
| DEP-4 | Dependency | Comp target and immigration details | — | See Q-02 and Q-17 | Ayush | Open |

## 6. Change log

| Date | Change | By |
|---|---|---|
| 2026-10-13 | Created the program plan, tracker and README | Claude |
| 2026-10-13 | Added the extensibility principle, the Drive companion folder and CLAUDE.md | Claude |
| 2026-10-13 | Restructured to Google-style artifacts: the Program Plan is PgM only (OKRs, milestones M0–M6, staffing, governance), and product content moved to a PRD stub. Recorded Ayush's answers (D-006 to D-008). Added Q-13 to Q-16 and R-07, R-08 | Claude |
| 2026-10-14 | Recorded the Q-14 and Q-16 answers. Added D-011, D-012, Q-17, Q-18 and R-09. Raised DR-3 priority | Claude |
| 2026-10-14 | M0 approved. Recorded the answers to Q-02, Q-10, Q-12, Q-15 and Q-16 as D-013 to D-016, and moved the feature asks to the PRD. Added Q-19, R-10 and R-11. Clarified Q-13 | Claude |
| 2026-10-14 | Resolved Q-17 and Q-18 as product features (CR-5, CR-6) and role-family defaults (D-017). Batch Drive sync (D-018). Added R-12 | Claude |
| 2026-10-14 | CR-3 confirmed and extended (CR-3a, D-021). Q-19: no deadline (D-019). Q-13: rolling, gate-sequenced dates (D-020). Added R-13 and revised R-08 and R-11. All PgM questions closed | Claude |

## 7. Published artifacts (Google Drive)

Folder: [Lodestone](https://drive.google.com/drive/folders/1Lg2FCikLlqf2YzYX--DrWZ4w2fUCQ4GV)

| Artifact | Type | Source in repo | Drive link | Last synced |
|---|---|---|---|---|
| Program Plan v2 | Google Doc | docs/program/PROGRAM_PLAN.md | [Open](https://docs.google.com/document/d/1uN4yjH74UHUzIk1aHfKpV8YDsLtMhYH6hfHaOsS5aq8/edit) | 2026-10-14 (edited in place, so the link is stable) |
| Program Tracker | Google Sheet (one tab per section) | docs/program/TRACKER.md | [Open](https://docs.google.com/spreadsheets/d/1YjGxImyoUVQimHPlJV_Ch9J8bkolRsDu-KaWdqM7KmI/edit) | 2026-10-14 (M0 gate) |
| PRD (stub) | Google Doc | docs/product/PRD.md | [Open](https://docs.google.com/document/d/1DAm9z6qX6K8gUXFmxLJ-EeHHLu0B_UII5FT4_1iDvgk/edit) | 2026-10-13 |
