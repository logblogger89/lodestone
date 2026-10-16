# Lodestone

The job platform for people moving countries for work: the jobs that fit you, in the country you want to move to, and the ones that will actually hire you (D-066). Citizens and permanent residents are welcome too. The MVP covers tech product and adjacent roles in Canada, built for Ayush first and ready for others.

## Status

M4 build: P1-S1 to P1-S6 built; see the [Tracker](docs/program/TRACKER.md) and the [Program Plan](docs/program/PROGRAM_PLAN.md).

## Repo layout

```
app/         The app: one HTML page, published as a private claude.ai Artifact
lodestone/   The engine: Python code for refresh, scoring, signals, discovery and reports
config/      Settings as data: role types, scoring, discovery, network allowlist
data/        Watchlist seed, job sources, eval sets and refresh state (no personal data)
scripts/     Checks: network access and the automated app check
docs/
  program/   PgM: Program Plan, Tracker
  product/   Product: PRD, CUJs, UX spec, mocks, prototype
  eng/       Engineering: Eng Design Doc, ADRs
  ops/       Run prompts for the scheduled runs, new-user guide
```
