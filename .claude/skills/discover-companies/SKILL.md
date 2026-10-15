---
name: discover-companies
description: Lodestone company discovery. Find employers not on the watchlist (government hiring lists, job-board web search, VC portfolio boards, pasted links), prove each with evidence, review them, and suggest them in the app for Ayush to approve. Use daily (part of the daily run), when Ayush says /discover-companies, or when he asks to find new companies.
---

# /discover-companies (P1-S5, D-058)

Nothing joins the watchlist without Ayush's approval in the app (Companies > Suggested companies).

1. **Network check.** `python3 scripts/check_network.py` (D-038).
2. **Government hiring lists + pasted links.** `python3 -m lodestone discover harvest`
   (uses the ESDC files in `data/external/esdc/`; run `/refresh-signals` first if a new quarter is out).
3. **VC portfolio boards.** `python3 -m lodestone discover vc` (boards listed in `config/discovery.json`).
4. **Job-board web search.** Run ~6 web searches such as `site:jobs.lever.co "product manager" Toronto`,
   `site:jobs.ashbyhq.com "product manager" Canada`, `site:job-boards.greenhouse.io "senior product manager" Toronto`,
   plus Waterloo/Vancouver/Montreal and "AI" variants. Write each employer you find (skip aggregators like Jobgether,
   Toptal, PitchMeAI) as `{"name", "route": "search", "evidence": "<role, city (board)>", "url"}` and run
   `python3 -m lodestone discover add <file>`. Never search LinkedIn, Indeed, Glassdoor or Wellfound.
5. **Probe.** `python3 -m lodestone discover probe` finds each new candidate's job board and counts its open
   Canadian roles in Ayush's families.
6. **Review.** For each new candidate worth a look (open Canadian roles, or ≥8 government-approved tech hires, or any
   VC/search candidate), decide: `suggest` product employers in or near his domains; `skip` IT consultancies and
   staffing firms, government, universities, law/accounting, pure hardware/biotech, and companies already on the
   watchlist under another name (then add that legal name to `config/employer_aliases.json`). Write
   `[{key, verdict, brand, segment, why}]` (why = one plain sentence a PM would care about) and run
   `python3 -m lodestone discover review <file>`. Then re-probe suggested ones by brand name if their board wasn't
   found (see `discover.py`).
7. **Publish.** `python3 -m lodestone discover export`, then `ArtifactData set meta/suggestions` (with if_version).
8. **Apply decisions** (also done in every daily run): `ArtifactData list company_decisions` with `out_dir`, then
   `python3 -m lodestone discover apply <folder>`. Approved companies join `data/seed/watchlist_seed.csv` and, when
   their board is confirmed, the source index; for `needs_source_research` companies, find their careers site and add
   a source row (refresh-jobs step 2). Re-export suggestions so decided ones drop off.
9. Commit `data/state/discovery.json`, the seed, the source index and config; push; tracker change-log line.
