# ADR-0003: Database: Postgres
- **Status:** Proposed. Hosting choice pending Ayush (E-1)
- **Decision:** Postgres with `pg_trgm` for fuzzy dedup and JSONB for config packs and parses. Recommended host: the smallest Cloud SQL instance in Toronto (about $10–15/month, automated backups).
- **Alternatives:** A free external Postgres such as the Neon free tier ($0, but a third party and data outside GCP). Firestore (free tier, but no relational dedup or fuzzy matching, so more application code).
