# Lodestone — Program Tracker

> The live status of the work in [`PROGRAM_PLAN.md`](./PROGRAM_PLAN.md). Claude updates it at the end of every working session.
> Legend: `⬜ Not started` · `🟦 In progress` · `🟨 In review` · `✅ Done` · `⛔ Blocked` · `➖ Dropped` | RAG: `🟢` `🟡` `🔴`

**Last updated:** 2026-10-15 · **Current milestone:** M4 (build) · **Overall RAG:** 🟢

**Status summary (2026-10-15).** **P1-S3 done (D-049):** 543 roles scored with explanations, freshness factor added; Ayush's Interested picks rank at the top (5 of 9 in the top 7). **P1-S4 built:** pathway signals (D-050), paste inbox (D-052), pay estimates (D-053), Later/closed checks passed. Market pay checks from levels.fyi on request (D-054). **P1-S5 built:** discovery (D-058), profile for anyone (D-061), score quality check (D-062). **Next: M4 gate review with Ayush** (daily use, P0 journeys end to end).

---

## 1. Milestone dashboard

| # | Milestone | RAG | Status | Target | Gate approved | Notes |
|---|---|---|---|---|---|---|
| M0 | Program kickoff | 🟢 | ✅ Done | 10-13 | ✅ 10-14 (D-013) | |
| M1 | PRD approved | 🟢 | ✅ Done | Rolling | ✅ 10-14 (D-029) | PRD v0 approved |
| M2 | UX review passed | 🟢 | ✅ Done | Rolling | ✅ 10-14 (D-033) | UX spec v0 + prototype v3 |
| M3 | Eng Design Doc approved | 🟢 | ✅ Done | Rolling | ✅ 10-14 (D-040) | Phase 1 design (Claude Code engine + Artifact app) |
| M4 | MVP dogfood | 🟢 | 🟦 In progress | After P1-S1 to P1-S5 | — | Sprint P1-S1 started 10-14 |
| M5 | Launch (v1) | 🟢 | ⬜ | TBD at M3 | — | |
| M6 | Post-launch review | 🟢 | ⬜ | Launch + 2 weeks | — | |

## 2. Deliverables

| ID | Deliverable | Workstream | Milestone | Status | Owner | Link / notes |
|---|---|---|---|---|---|---|
| D0.1 | Program Plan | PgM | M0 | ✅ | Claude → Ayush | [PROGRAM_PLAN.md](./PROGRAM_PLAN.md) |
| D0.2 | Tracker | PgM | M0 | ✅ | Claude → Ayush | this file |
| D0.3 | Repo skeleton, README, CLAUDE.md | PgM | M0 | ✅ | Claude | |
| D1.1 | DR-1 Leveling equivalency | Domain research | M1 | ✅ | Claude → Ayush | [DR-1_LEVELING.md](../product/research/DR-1_LEVELING.md). v1 hypotheses, low-confidence rows flagged |
| D1.2 | DR-2 Pay display and estimation | Domain research | M1 | ✅ | Claude → Ayush | [DR-2_PAY.md](../product/research/DR-2_PAY.md) |
| D1.3 | DR-3 Immigration pathways | Domain research | M1 | ✅ | Claude → Ayush | [DR-3_IMMIGRATION_PATHWAYS.md](../product/research/DR-3_IMMIGRATION_PATHWAYS.md). Signals only, not advice |
| D1.4 | DR-4 Job-source inventory and ToS | Data and sourcing | M1 | ✅ | Claude → Ayush | [DR-4_JOB_SOURCES.md](../product/research/DR-4_JOB_SOURCES.md). v1 done. ToS checks deferred to Eng Design |
| D1.4a | DR-5 Company discovery and seed watchlist | Data and sourcing | M1 | ✅ | Claude → Ayush | [DR-5_COMPANY_DISCOVERY.md](../product/research/DR-5_COMPANY_DISCOVERY.md) · [watchlist_seed.csv](../../data/seed/watchlist_seed.csv) |
| D1.5 | PRD v0 | Product | M1 | ✅ | Ayush + Claude | [PRD.md](../product/PRD.md). v0 in review: P0 R1–R15 with acceptance criteria, metrics, 4 open questions |
| D2.1 | CUJ flows and IA | Product (UX) | M2 | ✅ | Claude → Ayush | [UX_SPEC.md](../product/ux/UX_SPEC.md) §2–3 |
| D2.2 | Screen specs and visual direction | Product (UX) | M2 | ✅ | Claude → Ayush | [UX_SPEC.md](../product/ux/UX_SPEC.md) §4–6 |
| D2.3 | Clickable prototype | Product (UX) | M2 | ✅ | Claude → Ayush | [prototype.html](../product/ux/prototype.html) · [live link](https://claude.ai/artifact/C9f5CPbspLeydxtwVVBUKG) (private) |
| D2.4 | UX review | Product (UX) | M2 | ✅ | Ayush | All 3 questions resolved (D-030 to D-032) |
| D3.1 | Eng Design Doc | Engineering | M3 | ✅ | Claude → Ayush | [ENG_DESIGN.md](../eng/ENG_DESIGN.md) v1: Phase 1 = Claude Code engine + Artifact app |
| D3.2 | ADRs (stack, hosting, sourcing, scoring) | Engineering | M3 | ✅ | Claude → Ayush | [adr/](../eng/adr/) 0001 (accepted) to 0007 |
| D3.3 | Build plan and estimate (commits M4 and M5) | PgM / Eng | M3 | ✅ | Claude → Ayush | ENG_DESIGN §14: S1–S5 ≈ 10–15 sessions, then hardening |
| D4.1 | MVP build | Engineering | M4 | 🟦 | Claude | P1-S1 ✅, P1-S1b ✅, P1-S2 🟨 (awaiting Ayush's triage on iPad), P1-S3 ✅ (calibrated on 11 triaged roles, D-049), P1-S4 ✅ (pathway signals, paste inbox, pay estimates, Later/closed checks; market checks) |
| D4.2 | Dogfood and bug bash | Launch | M4 | ⬜ | Ayush | |
| D5.1 | Launch checklist (privacy, security, ToS, quality) | Launch | M5 | ⬜ | Claude | |
| D6.1 | Post-launch review and V1.x roadmap | PgM / Product | M6 | ⬜ | Ayush + Claude | |

## 3. Decision log

| ID | Date | Decision | Rationale | Decided by |
|---|---|---|---|---|
| D-001 | 10-13 | The program runs as gated stages: PgM, then Product (requirements, UX), then Engineering design, then Build | Ayush's direction | Ayush |
| D-002 | 10-13 | All program docs live in the repo under `docs/`. Status lives only in `TRACKER.md` | One source of truth, versioned | Ayush |
| D-003 | 10-13 | No resume or personal contact details are committed to the repo | Privacy | Ayush |
| D-004 | 10-13 | Readable copies are published to the Lodestone Google Drive folder. The repo stays canonical | Easy to read and share | Ayush. **Superseded by D-024** |
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
| D-015 | 10-14 | The MVP runs locally. Hosting budget isn't needed. LLM/API spend still gets decided at M3 | Ayush's direction | Ayush. **Superseded by D-034** |
| D-016 | 10-14 | Program deadline: the H-1B expires in Sep 2027, so the search aims to land an offer and work permit comfortably before then. The exact offer-by date is still open (Q-19) | Ayush's direction | Ayush |
| D-017 | 10-14 | Claude defines the default PM-adjacent role families (PRD §2b). They are user-editable config, not hard-coded | Ayush delegated Q-18 | Ayush (delegated) |
| D-018 | 10-14 | Batch syncing: the repo tracker updates every session, and the Drive Sheet and Docs refresh only at gates (or on request) | Less link churn and noise | Ayush |
| D-019 | 10-14 | No offer-by date or deadline. The goal is to see what's available and apply to relevant postings. The Sep 2027 H-1B expiry stays as context only | Ayush's direction (Q-19) | Ayush |
| D-020 | 10-14 | Milestones follow gate sequence, not the calendar. Dates are rolling and re-baselined as needed, and a slip from sponsor availability doesn't count against RAG | The sponsor's capacity is unpredictable (Q-13) | Ayush |
| D-021 | 10-14 | Listings with no immigration-pathway info are never excluded. Missing signals get filled from employer-level research and shown with a source and a confidence level, or as "unknown" | Relevant roles often don't mention sponsorship (CR-3a) | Ayush |
| D-022 | 10-14 | Feature backlog and MVP cut line approved after the brainstorm (PRD §2c). E23 dropped. The match engine (JD parsing plus profile understanding, then ranking) is the core of the MVP (PRD §2d) | Brainstorm with Ayush | Ayush |
| D-023 | 10-14 | Capture-feature tiers approved: A3a, A3b, A3c and A3h in the MVP; A3d, A3e and A3f in V1; A3g later. A3e stays in V1 | Ayush's review | Ayush |
| D-024 | 10-14 | Stop syncing to Google Drive. GitHub is the only home for artifacts. The existing Drive files stay as frozen snapshots | Ayush's direction | Ayush |
| D-025 | 10-14 | Digest shows the top 20 by default, adjustable from 1 to 100 | PRD v0 review | Ayush |
| D-026 | 10-14 | Default score weights accepted, and editable in Advanced settings | PRD v0 review | Ayush |
| D-027 | 10-14 | Watchlist = a continuous discovery engine (R1a) plus a 210-company seed, not a fixed list of 75 | PRD v0 review: "as many as possible" | Ayush |
| D-028 | 10-14 | Pipeline stages confirmed: Discovered → Shortlisted → Applied → Screen → Interviewing → Offer → Closed | PRD v0 review | Ayush |
| D-029 | 10-14 | **M1 approved:** PRD v0, with research DR-1 to DR-5 accepted as v1 inputs | Gate review | Ayush |
| D-030 | 10-14 | Job card content and density approved for iPad | UX review | Ayush |
| D-031 | 10-14 | "Later" roles come back in the digest after 7 days (configurable) | UX review | Ayush |
| D-032 | 10-14 | Interested automatically adds the role to Shortlisted in the pipeline | UX review | Ayush |
| D-033 | 10-14 | **M2 approved:** UX spec v0 and prototype v3 | Gate review | Ayush |
| D-034 | 10-14 | **Hosting: Google Cloud Run** (option B). The app runs in the cloud, so it's usable from any device with the laptop off and deploys on every push. **Supersedes D-015** (local-only). Personal data lives in Ayush's own GCP project | Least friction moving between iPad and laptop | Ayush |
| D-035 | 10-14 | GCP region: **us-central1 (Iowa)**, the cheapest tier, instead of Toronto. Canadian data residency isn't required for a personal tool. Prices get confirmed during setup | Ayush wants the cheapest region | Ayush |
| D-036 | 10-14 | **Phase 1 has no Cloud Run and no paid API.** Claude Code is the engine (refresh on request, with scoring covered by the Claude subscription), and a private Artifact with its built-in database is the app. Cloud Run + the Claude API (D-034, D-035) move to Phase 2, for when there are more users or a fixed schedule is needed | Ayush: avoid API costs until there's a need | Ayush |
| D-037 | 10-14 | Infrequent refreshes are fine. Add a freshness indicator with the last-refresh time per component (job pulls, scoring and model version, signals, discovery, profile) (R11a) | Ayush | Ayush |
| D-038 | 10-14 | Required domains live in `config/network_allowlist.txt`. `scripts/check_network.py` runs at every refresh and lists any that are blocked. Network settings can only be changed by Ayush (an environment setting) | Future sources need new domains | Claude |
| D-039 | 10-14 | Command names: `/refresh-jobs` (main), `/discover-companies`, `/refresh-signals`, `/rescore`. Each updates its freshness timestamp | Specific names, room for more refresh types | Ayush |
| D-040 | 10-14 | **M3 approved:** Phase 1 design. Build starts with P1-S1 | Gate review | Ayush |
| D-041 | 10-14 | Engine code uses only Python's standard library (no installs in fresh cloud sessions). Refresh state (`data/state/`) is committed so each new session knows what was seen before (needed for "no longer live"). Job-board auto-matches on a shortened name are flagged and fixed in `config/ats_overrides.csv` | Fresh containers, liveness history, avoid wrong-company matches | Claude |
| D-042 | 10-15 | **Every watchlist company gets a source.** Where no hosted board exists, Claude researches the careers site and the job system behind it, and records it in the source index (`data/sources/source_index.csv`, readable copy `data/sources/README.md`). One adapter per job system, reused across companies. Sites that block automated reading are paste-only. Sub-brands that hire through a parent (Tangerine, Simplii, Layer 6, Borealis, Ownr) are picked up via the parent | Q-21 | Ayush |
| D-043 | 10-15 | **Careers-page reader** is the fallback for companies with no feed: Lodestone saves the page as text and Claude reads the jobs from it during `/refresh-jobs` (covered by the subscription). Applies to Vidyard, Autoverify, Digitail, Taalas. Sites that block automated visitors (Indeed, WestJet, Definity, Resolver, Ross Video, Dayforce) stay paste-only; bot checks are never bypassed | Ayush asked whether careers pages can be read directly | Ayush |
| D-044 | 10-15 | App data layout: refresh writes jobs as 8 bucket documents plus company and freshness documents in one database write; the app owns triage, settings and the paste inbox. Only the owner can write. Until scoring (S3), "Best match" = role tier, then preferred regions, then newest | One write per refresh; Claude reads triage to learn | Claude |
| D-045 | 10-15 | **Pay:** read every pay range from the posting (salary field or description text), keep all regions, feature the Canadian one (job's city/province first). Card shows the Canadian range plus "+N US"; detail lists all ranges with the source sentence. "No pay in posting" only when the full posting was read | Ayush's RCA request (postmortem 2026-10-15) | Ayush |
| D-046 | 10-15 | Each pay range carries its **type** from the posting's wording (base, base + bonus, OTE, total compensation, not stated) and whether the employer calls it an estimate. Non-base ranges get a small card tag ("incl. bonus") and rank after base ranges in the pay sort. **Equity** is shown when mentioned: the amount if given, else "Offered" or "May be offered (amount not stated)"; diversity-statement and finance uses of "equity" are ignored. Every pay section names its source (company, job system, date read, link) and shows the exact wording with numbers highlighted | Ayush review of the Ratehub role | Ayush |
| D-047 | 10-15 | Fit scoring runs in-session with Claude (Sonnet sub-agents, 2 batches at a time, results saved per batch) against rubric v1.0; only new or changed roles are re-scored on later refreshes. Inferred pathway scores are normalized per company | Usage-limit interruption (R-16) and cross-batch consistency | Claude |
| D-048 | 10-15 | **Freshness** joins the fit score as a 7th factor (default 10%), computed by the app daily from the posting date (≤14 days 100 … >90 days 5; undated roles use first-seen, capped at 70). Optional Settings cut-off hides roles older than N days (off by default). Postings over 45 days show their age in amber | Ayush: a 50-day-old posting is likely filled | Ayush |
| D-049 | 10-15 | Freshness stays as designed (no exception for evergreen postings that are still live). **P1-S3 closed:** of Ayush's 9 Interested picks, 5 rank in the top 7 and all in the top 20%; the one "Not for me" (50-day-old posting) dropped from #8 to #29 with freshness | Calibration on 11 triaged roles | Ayush |
| D-050 | 10-15 | **Pathway signals from ESDC:** the last 9 quarters of positive-LMIA employer lists (2024Q1–2026Q1) are matched to the watchlist (58 companies, 54 with tech roles). Each role's pathway score now comes from evidence: Google ICT 95; posting offers sponsorship 85; frequent LMIA employer (≥10 tech positions or ≥5 Global Talent Stream) 80; any tech LMIA 70; non-tech only 55; no evidence 45; posting says must already be eligible 15. Shown as chips with status (Stated / Inferred / Unknown) and a source link; `/refresh-signals` reloads quarterly | R10, DR-3, CR-3 | Claude |
| D-051 | 10-15 | Large multinationals absent from the LMIA lists (e.g. Microsoft, Workday) get no special treatment: neutral pathway score (45, "No public signal"). Revisit only if triage shows Ayush consistently wants them | Ayush's question on missing big-tech employers | Ayush |
| D-052 | 10-15 | **Paste inbox:** at each refresh, pasted items are processed: known links are matched to existing roles; readable pages are fetched and read by Claude; LinkedIn/Indeed/Glassdoor/Wellfound are never fetched, so the pasted description is used or the app asks for it; non-Canadian roles are declined with a note. Added roles dedup against everything known, get pay read from the text, are scored like any other, and are never marked closed by a refresh. Status and a one-line result show in the app's Add job page | R3, A3a–c | Claude |
| D-053 | 10-15 | **Pay estimates:** roles with no posted Canadian range get an "est." base range from Lodestone's own posted Canadian ranges, in order: same company and level (high confidence), same company one level away ±15% per level (medium), 3+ similar-segment companies at the level (medium-low), 5+ watched companies at the level (low). Median of comparables, rounded to $5K. Shown muted with basis, confidence and example postings; the pay sub-score from an estimate is capped at 75 so a guess never outranks a posted range. Caveat shown: Ontario doesn't require ranges above $200K, so senior estimates may run low | R5, B8 | Claude |
| D-054 | 10-15 | **Market pay checks on request (Q-22):** levels.fyi is read only when Ayush asks about a named role (its terms forbid automated reading and compiled datasets; robots.txt allows user-requested fetches). One page per role, Canadian figures only (Toronto, Waterloo, else Canada; US fallbacks rejected); Claude picks the matching company level and the app shows that level's median total pay with its neighbours, date and a "Data source: Levels.fyi" link. Never used in a refresh, and display-only (not in the fit score) because it is total pay, not base. Runbook: `/market-check` | R5 | Ayush |
| D-055 | 10-15 | **Request market check from the app:** a button in each role's Pay panel saves a request (`market_req/<role>`); Claude answers requests at the start of its next session or refresh, one levels.fyi read per requested role. Cap: 20 requests a day (Ayush), enforced in the app and in processing (`config/market.json` daily_cap); extras wait a day. Statuses: Requested, done (figure shows), no Canadian data, failed (retry) | R5 | Ayush |
| D-056 | 10-15 | **Daily run and report:** a scheduled task runs every day at 6:53am New York time in a fresh cloud session: market-check requests, full `/refresh-jobs` (refresh, paste inbox, scoring, push to the app), tracker entry, then a plain-language report (new roles and top 3 matches, closures, inbox and market-check results, problems and what Ayush must do) sent by email and phone notification. Uses the Claude plan's usage; if a limit hits mid-scoring, the rest is scored next day | Ops | Ayush |
| D-057 | 10-15 | **Daily report in the app:** each run saves its report as `reports/<date>` (and in `data/state/reports/` for history). The Digest shows a banner with the latest report for 2 days; a new Reports page shows the latest in full plus an Archive of the last N days (Settings, default 14, max 90). Top matches open the role. The db keeps 90 days | R11 | Ayush |
| D-058 | 10-15 | **Company discovery (P1-S5):** four routes find employers not on the watchlist: government hiring lists (≥5 tech/product hires or ≥2 Global Talent Stream), job-board web search, VC portfolio boards (Inovia, Communitech, Diagram, Real Ventures via Getro's public company list), pasted links. Each candidate is probed for a job board and open Canadian roles, then reviewed by Claude (IT consultancies, staffing, government, universities and hardware/biotech skipped). Suggestions show in Companies with evidence; nothing joins the watchlist without Ayush's approval. Approvals apply at the next daily run; discovery runs daily as part of the morning run (changed from weekly, then twice weekly, at Ayush's request, 10-15). First pass: 54 suggestions from ~540 candidates. Side fix: 8 watchlist companies now matched under their legal names (pathway signals 79 → 86 companies) | R1a, DR-5 | Claude |
| D-059 | 10-15 | **Green / yellow / red preference checks:** every role shows a strip of checks (Location, Work permit, Pay, Level, Posted, and Team when it manages people), each green, yellow or red against Ayush's preferences, with an icon as well as colour and a plain-language reason on hover; the detail view lists them as "Against your preferences". Defaults: green = his ticked regions (Toronto area, Waterloo, remote in Canada), strong evidence of hiring from abroad or an internal transfer, posted pay up to ≥CA$190K (yellow ≥160K), ≈Google L6+ (yellow L5), posted ≤14 days (yellow ≤30; changed from 21/45 at Ayush's request). Estimates turn green only at high confidence. All thresholds editable in Settings → Colour rules (D-005). Also fixed: "Posted N days ago" dates now count from when Lodestone read them, not from today | Ayush ask | Ayush |
| D-060 | 10-15 | **MVP audience widened (Ayush):** design the MVP for anyone who is not a Canadian citizen or permanent resident and wants work in Canada, in Ayush's industry (tech product and adjacent roles) for now; other industries later. Every personal input (resume, current employer, work-authorization status, locations, level, pay, domains, role families, people management, colour rules, weights) must live in the user's own profile and be editable there, and a user must be able to upload their own resume. Ayush stays the first and only user until the multi-user approach (Q-24) is chosen. Domain preference recorded: everything tied to his CV is equally welcome (AI/agents/platform, risk and compliance, data governance, trust and safety, fintech, ads, commerce, analytics) | Scope (D-005) | Ayush |
| D-061 | 10-15 | **Profile for anyone (Q-24 → A):** one private copy of Lodestone per person; shared sign-in later. Built: the Settings page became **Profile** (resume upload as PDF or pasted text; current employer, title, level, location; work-permit status; regions, role types, domains, target level and pay; ranking weights; app settings). Nothing personal in code: the Google transfer rule now comes from the user's current employer, an open work permit makes sponsorship irrelevant, pay scores use the user's own pay targets, and the scoring rubric reads everything from the profile. Profile edits trigger re-scoring, capped at 150 roles a day. The daily run reads a newly uploaded resume and fills in the profile (resume never leaves the app). New-user steps: `docs/ops/NEW_USER.md` | D-005, D-060 | Ayush |
| D-062 | 10-15 | **Score quality check (P1-S5 eval set):** (1) ranking vs the user's own triage, computed with exactly the app's formula: how many Interested roles are in the top 25, and how often Interested roles score above Later / Not for me (pairwise); shown live on the Profile page and recorded each run; (2) reading accuracy on a hand-checked set (`data/eval/reading_gold.json`, 22 postings to start, target 50): pay amounts and currency, pay type, location, people management, level, and filtering out non-roles. Gate: no rubric, scoring or reader change ships if either check drops. Baseline 10-15: 9/9 Interested in the top 25 (of 536); pairwise 59% on 9 Interested vs 7 Later (early read: needs 10+ of each); reading 88% pay, 60% pay type before fixes → 100% after. Fixes: hourly cents ($24.25), currency named earlier in the sentence ("in CAD"), "plus commissions" / "+ X% bonus" read as base, and hourly roles under CA$45/h (Lululemon store jobs) filtered out (config) | R7, ENG §9 | Claude |

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
| Q-10 | Monthly budget for hosting and LLM/API costs | — | ✅ Deferred | Phase 1 costs $0 beyond the Claude subscription (D-036). Revisit in Phase 2 |
| Q-11 | Should the repo be public or private? | — | ✅ Answered | Private for now (D-006). Scrub personal details before any public release (A-03) |
| Q-12 | Is there a target date to start applying, have an offer, or move? | — | ✅ Answered | As soon as possible, and comfortably before the H-1B expires in Sep 2027 (D-016) |
| Q-13 | Capacity: how much review time per week? | — | ✅ Answered | Unpredictable (newborn). Dates will move as needed (D-020) |
| Q-14 | **Immigration profile.** Do you or your spouse have an Express Entry profile, a CRS estimate, language test results or an ECA? | — | ✅ Answered | There is an Express Entry profile with strong IELTS scores, but the CRS is low because of age (Ayush turns 37 on 11-15, his spouse turns 33 on 01-03). A PR route without a job offer isn't realistic on its own right now, so a job is the main path |
| Q-15 | **Hard dates.** H-1B extension or expiry, vesting or refresh cliffs, parental leave: anything that constrains timing | — | ✅ Answered | The H-1B expires in Sep 2027 (D-016) |
| Q-19 | Offer-by date? | — | ✅ Answered | None. Explore and apply to relevant roles (D-019) |
| Q-20 | Where does the app run? | — | ✅ Answered | Google Cloud Run (D-034) |
| Q-16 | Is a Google-internal transfer to Google Toronto or Waterloo on the table? If so, it's an LMIA-exempt channel to track | — | ✅ Answered | Yes. PM roles that fit at Google Canada are scarce, so Ayush is open to PM-adjacent roles inside or outside Google (D-011, D-012) |
| Q-17 | Express Entry details for DR-3 | — | ✅ Resolved | They become optional in-app inputs: an Express Entry profile and CRS calculator that adjust listings (CR-5). Ayush has the details and will enter them in the app |
| Q-18 | Which PM-adjacent families count? | — | ✅ Resolved | Delegated to Claude (D-017), with defaults in PRD §2b. No people-management roles by default, via a toggle (CR-6) |
| Q-21 | Coverage gap (R-15): build careers-site connections for companies without a hosted board, including Google? | Ayush | ✅ Answered | Yes, for every company, with an index of all sources (D-042) |
| Q-22 | Triangulate pay estimates with outside data (levels.fyi etc.)? | Ayush | ✅ Answered | levels.fyi's terms rule out scheduled reads; Ayush chose on-request checks per role (D-054) |
| Q-23 | Adaptive, Spotify-style recommendations that learn from viewing, shortlisting and other behaviour (PRD backlog D19a): what's the scope, which signals and when on the roadmap? | Ayush + Claude | 🟨 Parked | Seed idea logged 10-15. Flesh out together after M4 dogfood, when there is enough triage and viewing history to learn from |
| Q-24 | How should the MVP serve other people (D-060)? | Ayush | ✅ Answered | Option A: profile-first, one private copy per person; shared sign-in later (D-061) |

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
| R-09 | Risk | The CRS score drops at each birthday after 35 (Ayush on 11-15, spouse on 01-03), so a PR route without a job offer gets harder over time | High | Treat getting a work permit sooner as the priority (ICT and LMIA-exempt routes). DR-3 to check levers: Since DR-3: job-offer CRS points were removed (2025-03-25) and Ontario's HCP stream is closed, so CEC through Canadian work experience is the main lever. Validate with a licensed consultant (RCIC) | Ayush + Claude | Open |
| R-10 | Risk | LinkedIn's API probably won't expose the user's current employer to a personal app (OAuth sign-in returns only basic identity) | Med | DR-4 checks this. Fallbacks: import the LinkedIn data export or profile PDF, parse the resume, or enter it manually | Claude | Open |
| R-11 | Risk | Starting the search late leaves less buffer before the H-1B expires (Sep 2027) | Med | Ship the MVP fast. Run the Google transfer channel in parallel. No fixed offer-by date (D-019) | Ayush + Claude | Open |
| R-12 | Risk | The CRS rules (points grid, how job offers count, category draws) change over time, so a hard-coded calculator would go stale | Med | Put CRS rules in versioned config (D-005), show the rules version and date, and link to the official IRCC calculator for verification | Claude | Open |
| R-13 | Risk | Employer-level sponsorship signals from web research may be stale, wrong or unverifiable | Med | Prefer official data, e.g. ESDC's published positive-LMIA employer lists (to verify in DR-3/DR-4). Show the source, date and a confidence level, and never hide a listing because of it (D-021) | Claude | Open |
| R-14 | Risk | A browser extension that reads LinkedIn or Wellfound pages could breach their terms, even when the user is looking at the page themselves | Med | Review ToS before building A3d. Fall back to paste URL or paste text (A3a, A3b), which are always available | Claude | Open |
| I-02 | Issue | Pay ranges written in posting text were not captured (26 of 546 roles had pay) | — | **Fixed 10-15 (D-045):** text parsing, full-posting fetch, honest wording, tests, coverage metric. See [postmortem](../eng/postmortems/2026-10-15-pay-not-captured.md) | Claude | Closed |
| I-01 | Issue | The environment's network blocked the required domains | — | **Resolved 10-14:** Ayush set Network access to Full. All 10 refresh sources are reachable. www.canada.ca doesn't respond to cloud servers, but it isn't needed by refresh (only browser links) | Ayush | Closed |
| I-03 | Issue | Daily scheduled run (D-056) could not save to GitHub. Run 1 (6:53am): its fresh session had no copy of the code and no way to attach it. Run 2 (catch-up, dedicated runner session): refresh, scoring, report and app update all worked, but GitHub refused its push (no write access), and it sent Ayush four alerts. It also found a Python 3.11 incompatibility in signals.py (fixed). Today's results were rebuilt and saved to GitHub from the build session; fixed 10-15: the daily task now runs inside the build session, which already has the code and GitHub access; the separate runner session was archived. Trade-offs: no email or phone alert (the report is in the app and posted in this conversation), and runs appear in this conversation | High | Claude | ✅ Fixed |
| R-16 | Risk | Claude plan usage limits interrupt large scoring runs (first full run of 543 roles hit the limit) | Med | Score with a lighter model in small, resumable batches; afterwards only new/changed roles are scored each refresh. Upgrade the plan only if limits keep biting | Claude | Open |
| R-15 | Risk | Coverage: careers sites change layouts or block automated reading | Med | **Mitigated 10-15:** 183 of 210 companies pulled (was 71). Each refresh reports failing sources; a parse that finds nothing is an error, not silence. Workable is rate-limiting this environment (Borrowell, Mila, Nuvei); retry next refresh, else paste. Paste capture (A3) covers the rest | Claude | Open |
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
| 2026-10-14 | Brainstorm results recorded in PRD §2c and §2d (D-022). DR-4 started | Claude |
| 2026-10-14 | DR-4 v1 done: source inventory, ingest strategy, dedup design, and pay-transparency and LMIA findings | Claude |
| 2026-10-14 | Added the paste-link capture features A3a to A3h (tiers proposed) and R-14 | Claude |
| 2026-10-14 | DR-1, DR-2 and DR-3 v1 done. Key findings: job-offer CRS points removed (Mar 2025), Ontario HCP and Employer Job Offer streams closed in 2026, ICT is the strongest route, and CEC is the main PR lever | Claude |
| 2026-10-14 | PRD v0 written (Google-style, P0/P1/P2, acceptance criteria, metrics). Drive sync discontinued (D-024) | Claude |
| 2026-10-14 | PRD v0 questions resolved (D-025 to D-028). DR-5 and the 210-company seed watchlist done. R1a discovery engine added | Claude |
| 2026-10-14 | M1 approved (D-029). M2 (UX) started | Claude |
| 2026-10-14 | UX spec v0 and clickable prototype v1 published for the M2 review | Claude |
| 2026-10-14 | Prototype v2 and v3 (deep links, label explainer, exact-URL previews). UX review questions resolved (D-030 to D-032) | Claude |
| 2026-10-14 | M2 approved (D-033). M3 started, beginning with the runtime decision (Q-20) | Claude |
| 2026-10-14 | Hosting decided: Cloud Run (D-034). Eng Design Doc v0 and ADR-0001 to ADR-0007 written | Claude |
| 2026-10-14 | Region changed to us-central1 (D-035). Plain-English summary added to the Eng Design Doc. Working agreement: explain in plain language for a PM audience | Claude |
| 2026-10-14 | Architecture pivot: Phase 1 runs on a Claude Code engine with an Artifact app (D-036). Cloud Run moved to Phase 2. I-01 is now high priority | Claude |
| 2026-10-14 | Freshness indicator added (R11a, D-037). Domain allowlist file and checker added (D-038) | Claude |
| 2026-10-14 | Network access set to Full. All refresh sources verified reachable (I-01 closed) | Claude |
| 2026-10-14 | Command names set (D-039) | Claude |
| 2026-10-14 | M3 approved (D-040). P1-S1 built and run live: 146 candidates from 71 feeds. Added D-041, R-15, Q-21 | Claude |
| 2026-10-15 | D-062 built: score quality check (ranking vs triage, reading vs 22 hand-checked postings), Profile panel, 4 pay-reader fixes, hourly store roles filtered; refresh rerun; tests | Claude |
| 2026-10-15 | D-061 built: Profile page (resume upload, work-permit status, all preferences), Google-specific rules removed, pay scored against the user's targets, profile-change re-scoring (150/day), rubric made generic, new-user guide, PRD personas updated; tests | Claude |
| 2026-10-15 | D-060: MVP designed for any non-citizen/non-PR job seeker in Ayush's industry; freshness colours 14/30 days; domain preferences saved to profile; Q-24 raised | Claude |
| 2026-10-15 | Preference colour checks on every role (D-059); relative posting dates fixed; triage pattern reviewed with Ayush | Claude |
| 2026-10-15 | Discovery now daily, per Ayush (was twice a week) | Claude |
| 2026-10-15 | Discovery now twice a week (Mon and Thu), per Ayush | Claude |
| 2026-10-15 | I-03 fixed: daily 6:53am task re-created to run in the build session (has GitHub access); paused task deleted, runner session archived | Claude |
| 2026-10-15 | I-03: daily run setup and GitHub-access failures; today's run rebuilt and saved here; Python 3.11 fix in signals.py; scheduled task paused pending re-creation from claude.ai | Claude |
| 2026-10-15 | P1-S5 started: discovery engine built and run (D-058): 54 suggested companies in the app (Companies tab) with evidence; `/discover-companies` runbook; daily run applies approvals and discovers on Mondays; tests | Claude |
| 2026-10-15 | Ayush's idea logged: adaptive Spotify-style recommendations (PRD D19a, Q-23), parked until after M4 dogfood | Claude |
| 2026-10-15 | Reports page, Digest banner and Archive added (D-057); daily run now posts its report to the app | Claude |
| 2026-10-15 | Daily 6:53am ET run with emailed report scheduled (D-056); first run today | Claude |
| 2026-10-15 | "Request market check" button in the app (D-055), 20 a day; `market pending`; runbooks updated; tests | Claude |
| 2026-10-15 | On-request levels.fyi market checks built (D-054): `market fetch/add`, app Pay panel row, `/market-check` runbook, tests | Claude |
| 2026-10-15 | Q-22: levels.fyi terms checked; automated/scheduled reading not allowed; build paused pending Ayush | Claude |
| 2026-10-15 | Q-22: Ayush chose levels.fyi direct reads (option B); www.levels.fyi added to the network allowlist; waiting on the environment setting | Claude |
| 2026-10-15 | Sprint 4 checks: Later roles return after 7 days (verified); closed postings show "Posting closed <date>" in the pipeline. Fixed: moving a role from Interested to Later or Not now takes it off the auto-Shortlist. Q-22 raised (outside pay data) | Claude |
| 2026-10-15 | Pay estimates live (D-053): 181 of 214 roles without a Canadian range now show an estimate (28 high, 9 medium, 117 medium-low, 27 low confidence); tests added | Claude |
| 2026-10-15 | Paste inbox processing (D-052): prepare/add commands, app statuses, tests | Claude |
| 2026-10-15 | LMIA name-matching fix after Ayush's question: legal-name variants ("Salesforce.com Canada Corp.", "Okta", "Snowflake Computing") now match; 79 companies (was 58). Microsoft, Workday, Nvidia, Adobe, Meta, Google, Lyft, Databricks confirmed absent from the 2024Q1–2026Q1 lists | Claude |
| 2026-10-15 | ESDC LMIA pathway signals live (D-050); `/refresh-signals` skill added | Claude |
| 2026-10-15 | P1-S3 closed after calibration (D-049); P1-S4 started | Claude |
| 2026-10-15 | Freshness factor and old-posting cut-off added (D-048); iCIMS posting dates captured | Claude |
| 2026-10-15 | All 543 roles scored (D-047); top matches include Workday, Microsoft, Amazon, StackAdapt, Zip, Okta Principal/Staff PM roles. Scores live in the app | Claude |
| 2026-10-15 | P1-S3 started: profile from CV (app db only), rubric v1.0, scoring pipeline, app score ring and breakdown; scoring run deferred to 7am ET by usage limit (R-16). App pinned to sidebar | Claude |
| 2026-10-15 | Pay type, equity and source attribution added (D-046) | Claude |
| 2026-10-15 | Pay capture fixed after RCA (I-02, D-045, postmortem); app shows all ranges with the Canadian one featured | Claude |
| 2026-10-15 | P1-S2 started: app built on real data and published privately; refresh now exports to it (D-044) | Claude |
| 2026-10-15 | Careers-page reader added (D-043): 4 more companies pulled; 6 bot-protected sites confirmed paste-only | Claude |
| 2026-10-15 | Q-21 answered (D-042). Source index built for all 210 companies (research by 4 parallel agents); 26 new adapters; 546 candidates from 183 companies. R-15 mitigated. Eng Design updated | Claude |

## 7. Published artifacts (Google Drive)

> **Discontinued 2026-10-14 (D-024).** The links below are frozen snapshots, no longer updated.

Folder: [Lodestone](https://drive.google.com/drive/folders/1Lg2FCikLlqf2YzYX--DrWZ4w2fUCQ4GV)

| Artifact | Type | Source in repo | Drive link | Last synced |
|---|---|---|---|---|
| Program Plan v2 | Google Doc | docs/program/PROGRAM_PLAN.md | [Open](https://docs.google.com/document/d/1uN4yjH74UHUzIk1aHfKpV8YDsLtMhYH6hfHaOsS5aq8/edit) | 2026-10-14 (edited in place, so the link is stable) |
| Program Tracker | Google Sheet (one tab per section) | docs/program/TRACKER.md | [Open](https://docs.google.com/spreadsheets/d/1YjGxImyoUVQimHPlJV_Ch9J8bkolRsDu-KaWdqM7KmI/edit) | 2026-10-14 (M0 gate) |
| PRD (stub) | Google Doc | docs/product/PRD.md | [Open](https://docs.google.com/document/d/1DAm9z6qX6K8gUXFmxLJ-EeHHLu0B_UII5FT4_1iDvgk/edit) | 2026-10-13 |
