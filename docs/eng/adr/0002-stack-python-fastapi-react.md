# ADR-0002: Stack: Python/FastAPI backend, React/TypeScript frontend, one container
- **Status:** Proposed (M3)
- **Decision:** Python 3.12, FastAPI, Pydantic, SQLAlchemy and Alembic, httpx, and the Anthropic SDK on the backend. React with TypeScript and Vite on the frontend, built to static files and served by FastAPI. One image, with entry points for the web service and for batch jobs.
- **Why:** Python has the best tooling for ingestion and parsing and for the Anthropic SDK. React carries the prototype forward. A single image keeps CI/CD and versioning simple.
- **Alternatives:** Next.js full-stack (TypeScript everywhere, but weaker for data work). Server-rendered HTMX (simpler, but the triage, slider and keyboard interactions get clunkier).
