---
name: refresh-jobs
description: Lodestone job refresh. Pull every watched company's job feed or careers site (listed in data/sources/source_index.csv), keep Canadian roles in Ayush's role families, dedup, update liveness, then (from Sprint 2/3) score and push to the Lodestone app. Use when Ayush says /refresh-jobs or asks to refresh or update jobs.
---

# /refresh-jobs

Runbook for one refresh (ENG_DESIGN "Phase 1"). Everything runs from the repo root with the
standard library only, so no installs are needed.

## Steps

1. **Network check (D-038).** `python3 scripts/check_network.py`
   If any domain is blocked, stop and tell Ayush which ones, with the click-by-click fix
   (Claude Code environment settings → Network access → Full, or add the domain to the allowlist).
2. **Source index.** `python3 -m lodestone detect`
   Every company's job source lives in `data/sources/source_index.csv` (one row per source: job system,
   feed parameters, status). `detect` only probes companies that have no row yet, for the hosted boards
   (Greenhouse, Ashby, Lever, SmartRecruiters). A company not found there needs research: find its careers
   site, identify the job system, verify the feed, and add a row (an existing adapter in
   `lodestone/adapters/` covers most systems; a new system means a new adapter file).
   Shortened-name matches are added as `paused` until confirmed.
3. **Refresh.** `python3 -m lodestone refresh` (or `--only <company or platform>` to test one source)
   Writes `data/state/jobs.json`, `data/state/candidates_to_score.json` and `data/state/runs.json`
   (freshness, R11a), and updates each source's Canada count in the index. One broken source never
   stops the run; failures are listed under `errors`. Fix or pause failing sources.
   Then `python3 -m lodestone index` to refresh the readable index (`data/sources/README.md`).
4. **Score (from Sprint 3).** Score each new or changed candidate against the profile in the
   Lodestone Artifact db. Not available yet.
5. **Push to the app (from Sprint 2).** Write jobs and freshness to the Lodestone Artifact db with
   ArtifactData `batch`. Not available yet.
6. **Save and report.** Run the tests (`python3 -m unittest discover -s tests -t .`), commit
   `data/state/` and `data/sources/` and push to the working branch. Then give Ayush a plain-language summary: feeds
   pulled, Canadian roles found, candidates by tier and region, new ones, ones that closed, and any errors.

## Rules

- Never scrape LinkedIn, Indeed, Glassdoor or Wellfound. Those are paste-only (A3).
- Missing data never excludes a job (D-021). Only the title rules and the Canada check filter at this stage.
- Never commit resumes or contact details.
