# ADR-0001: Host on Google Cloud Run
- **Status:** Accepted (D-034, 2026-10-14)
- **Context:** Ayush switches between his iPad and laptop and wants no friction. Local hosting (D-015) needs the laptop to be on and manual updates.
- **Decision:** Run Lodestone as a Cloud Run service (web UI and API) plus Cloud Run Jobs (batch), scheduled by Cloud Scheduler, in Ayush's own GCP project in the Toronto region, behind Google sign-in (IAP).
- **Consequences:** Works on any device with the laptop off, and every push deploys automatically. Personal data lives in a cloud account Ayush controls. Small monthly cost (see ENG_DESIGN §12). Supersedes D-015.
