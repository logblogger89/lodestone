# ADR-0006: Ingestion: ATS public feeds behind a pluggable adapter registry
- **Status:** Proposed (M3)
- **Decision:** Pull jobs from public ATS feeds (Greenhouse, Lever, Ashby, SmartRecruiters in the MVP; Workday and Workable after a ToS check) through a `SourceAdapter` interface. Discovery pathways are plugins too. LinkedIn, Indeed, Glassdoor and Wellfound are capture-only.
- **Why:** Structured data, an exact posting URL for every deep link, ToS-compliant access (DR-4), and extensible by design (D-005).
