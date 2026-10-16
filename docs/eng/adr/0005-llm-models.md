# ADR-0005: LLM: Claude via structured outputs, model tier chosen by Ayush
- **Status:** Proposed. Model option pending Ayush (E-2, Q-10)
- **Phase 1:** scoring runs in-session on the most capable model (D-070); the options here apply to Phase 2.
- **Decision:** Use the Anthropic Python SDK with structured outputs (strict JSON schemas) for JD parsing and fit scoring. The profile and instructions go in a cached prefix. The daily run uses the Batch API. Weights are applied outside the LLM.
- **Options:** A: Claude Opus 5.5 everywhere (about $105–270/month). B: Claude Haiku 5.5 for parse and pre-score plus Claude Opus 5.5 for the top ~20 a day (about $25–45/month). C: Claude Haiku 5.5 only (about $5–10/month). The choice is confirmed against the eval set (50 labelled JDs plus triage labels) before it's locked.
- **Provider:** Anthropic API (recommended) or Google Vertex AI (E-3).
