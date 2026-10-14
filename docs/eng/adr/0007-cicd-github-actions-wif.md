# ADR-0007: CI/CD: GitHub Actions to Cloud Run via Workload Identity Federation
- **Status:** Proposed (M3)
- **Decision:** On every push to `main`: run tests and evals, build the image, push it to Artifact Registry, and deploy to Cloud Run. Authentication uses Workload Identity Federation, so there are no stored keys. Pull requests run tests only.
- **Why:** Deploys with no manual step. Combined with Claude Code on the web, Ayush needs nothing installed locally.
