# Lodestone: working agreements for Claude

- **Google-style artifacts and roles (D-009).** Keep the program and product work separate:
  - **PgM** (`docs/program/`): Program Plan (mission, OKRs, scope, workstreams, milestones, staffing/RASCI, governance, dependencies, risks) and Tracker. No product requirements here.
  - **Product** (`docs/product/`): PRD, CUJs, requirements, metrics, and all UX work (UXR, UX and interaction design, mocks, prototypes). Following Google practice, UX sits under the PM.
  - **Engineering** (`docs/eng/`): Eng Design Doc and ADRs.
  - Ayush is the sponsor, PM lead and only approver. Claude plays TPgM, PM partner, UX, SWE/TL and researcher.
- **Process.** Work moves through gated milestones M0–M6 (see the Program Plan). At the end of every working session, update `docs/program/TRACKER.md` (status summary, deliverables, decisions, questions, RAID, change log) and commit it.
- **Readable copies on Google Drive.** Publish readable copies to the Lodestone Drive folder (id `1Lg2FCikLlqf2YzYX--DrWZ4w2fUCQ4GV`): Docs for documents, Sheets for the tracker and other tables, Slides for decks. The repo stays canonical. Refresh the copies at gates and record each link in the tracker's §7. When importing markdown, keep `**` out of table cells and avoid 4-byte emoji, because both render badly in Docs. Update an existing Google Doc in place with the Docs `update_doc` tool (replaceAllText, updateTextStyle) so its link stays stable. Sheets can't be edited in place, so re-upload them, move the old copy to trash, and fix any links that point to it.
- **Built for one, ready for many (D-005).** User profile, role family, geography, leveling, comp, eligibility, sources and scoring weights are data, config or plugins, never hard-coded. Build the seams, but only one implementation of each.
- **Privacy.** Never commit resumes or contact details. The repo is private (D-006). Personal immigration and family context must be scrubbed before any public release.
