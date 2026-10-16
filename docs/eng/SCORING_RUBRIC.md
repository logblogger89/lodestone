# Fit-scoring rubric (v1.0, generic wording 10-15, D-060)

Used by Claude to score each role against the candidate profile (PRD Appendix E, R6–R9). Every sub-score is 0–100 with a one-line reason a person can check against the posting. **Missing information scores 50 (neutral) and says so; it never hides a job (D-021).** Weights live in `config/scoring.json` and each user's Profile; the overall score is computed in the app at read time.

## Inputs
- The candidate profile (stored in the app's private database; a working copy is passed to the scorer, never committed). Read its `current` (employer, title, level), `domains`, `preferences` (target level, domains wanted, people management), `skills` and `scope_signals`. Nothing about any one person is written in this rubric: everything comes from the profile.
- One posting: title, company, location, pay as posted (with type), the full description.

## Sub-scores

| Sub-score | What it measures | Anchors |
|---|---|---|
| **role** | Is this the kind of job the candidate does? | 95 core IC product management of a product/platform; 75 product-heavy adjacent (TPM on a product, product ops, strategy roles that own a roadmap); 50 adjacent with little product ownership (program management of operations, chief of staff); 25 stretch (product marketing, solutions/sales engineering, analytics); 5 not a product job |
| **level** | Does the scope match the candidate's target level (profile `preferences.target_level`, on Google's scale as the common reference: L5 Senior, L6 Staff, L7 Principal; DR-1 maps other ladders)? | 95 at the target level with the right scope; 75 one level off, or a lead role with light management when the candidate wants IC; 50 unclear; 30 two levels off; 10 far off (junior, or an executive role). Use years asked, scope language (own strategy, multi-team, exec stakeholders), title, and the company's ladder |
| **domain** | Overlap with the candidate's `domains` and `preferences.domains_wanted` (all listed domains count equally unless the profile ranks them) | 90+ direct overlap with a listed domain; 70 adjacent to one; 50 general consumer/B2B product; 25 unrelated specialist domain (hardware, clinical, gaming design) |
| **pathway** | What the posting says about hiring people who need a Canadian work permit (DR-3) | 85 posting states visa sponsorship or relocation support; 45 says nothing; 15 posting says no sponsorship / must already be authorized to work in Canada / citizenship or clearance required. Say whether it is stated. Employer evidence (ESDC lists), intra-company transfers from the candidate's own employer and open work permits are added by Lodestone, not scored here |
| **pay** | Featured Canadian range vs. target (`config/scoring.json`). The app replaces this with the user's own pay targets whenever a Canadian range or estimate exists | ≥ excellent 95; ≥ good 80; ≥ ok 60; ≥ low 40; below 20; no Canadian range 50 (say "not posted"). US-only ranges: 50 and say so. Bonus-inclusive or OTE ranges: compare at 90% |
| **skills** | Must-haves the candidate has | 90 has nearly all must-haves; 70 most; 50 unclear; 30 missing key ones (e.g. deep domain credential, specific language, hands-on engineering) |

## Computed by the app (not scored by Claude)

| Factor | What it measures | Anchors |
|---|---|---|
| **freshness** | How recently the role was posted; older postings are more often filled (10-15) | ≤14 days 100; ≤30 85; ≤45 60; ≤60 30; ≤90 15; older 5. No posting date: uses the day Lodestone first saw the role, capped at 70. Recomputed daily, so no re-scoring is needed. Optional Profile cut-off hides roles older than N days |

## Also extract
- `summary`: one plain sentence on what the job is ("Own the roadmap for X used by Y").
- `level_guess`: e.g. "Senior PM (≈ L5)", "Principal PM (≈ L6)".
- `people_mgmt`: true only if the posting says the role manages people.
- `work_mode`: onsite / hybrid / remote / unclear.
- `must_haves`: up to 4 short items.
- `flags`: short warnings (e.g. "French required", "Security clearance", "Contract role", "Retail store role").

## Rules
- Judge the posting, not the company's reputation.
- Reasons are specific and short (≤ 120 characters), written to the candidate ("Matches your ads-safety work"), using only what their profile says.
- Never mention personal immigration or family details in reasons; say "work permit" generically.
