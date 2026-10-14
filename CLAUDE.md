# Lodestone: working agreements for Claude

- **Google-style artifacts and roles (D-009).** Keep the program and product work separate:
  - **PgM** (`docs/program/`): Program Plan (mission, OKRs, scope, workstreams, milestones, staffing/RASCI, governance, dependencies, risks) and Tracker. No product requirements here.
  - **Product** (`docs/product/`): PRD, CUJs, requirements, metrics, and all UX work (UXR, UX and interaction design, mocks, prototypes). Following Google practice, UX sits under the PM.
  - **Engineering** (`docs/eng/`): Eng Design Doc and ADRs.
  - Ayush is the sponsor, PM lead and only approver. Claude plays TPgM, PM partner, UX, SWE/TL and researcher.
- **Process.** Work moves through gated milestones M0–M6 (see the Program Plan). At the end of every working session, update `docs/program/TRACKER.md` (status summary, deliverables, decisions, questions, RAID, change log) and commit it.
- **No Google Drive syncing (D-024).** GitHub is the only home for artifacts. Don't create or update Google Drive copies unless Ayush explicitly asks again. The existing Drive files are frozen snapshots as of 2026-10-14.
- **Built for one, ready for many (D-005).** User profile, role family, geography, leveling, comp, eligibility, sources and scoring weights are data, config or plugins, never hard-coded. Build the seams, but only one implementation of each.
- **Privacy.** Never commit resumes or contact details. The repo is private (D-006). Personal immigration and family context must be scrubbed before any public release.
