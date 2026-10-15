# Fit-scoring rubric (v1.0)

Used by Claude to score each role against the candidate profile (PRD Appendix E, R6–R9). Every sub-score is 0–100 with a one-line reason a person can check against the posting. **Missing information scores 50 (neutral) and says so; it never hides a job (D-021).** Weights live in `config/scoring.json` and the app's Settings; the overall score is computed in the app at read time.

## Inputs
- The candidate profile (stored in the app's private database; a working copy is passed to the scorer, never committed).
- One posting: title, company, location, pay as posted (with type), the full description.

## Sub-scores

| Sub-score | What it measures | Anchors |
|---|---|---|
| **role** | Is this the kind of job the candidate does? | 95 core IC product management of a product/platform; 75 product-heavy adjacent (TPM on a product, product ops, strategy roles that own a roadmap); 50 adjacent with little product ownership (program management of operations, chief of staff); 25 stretch (product marketing, solutions/sales engineering, analytics); 5 not a product job |
| **level** | Does the scope match an L5 operating near L6 (≈ Amazon L6/L7, Microsoft Senior/Principal, Meta IC5–IC6, scale-up Senior/Staff/Principal PM; see DR-1)? | 95 Senior/Staff/Principal IC with multi-team scope; 75 Senior with narrower scope, or Group PM/Lead with light management; 50 unclear; 30 mid-level (PM II, 3–5 yrs) or Director/VP with large org; 10 junior (APM, PM I, <3 yrs). Use years asked, scope language (own strategy, multi-team, exec stakeholders), title, and the company's ladder |
| **domain** | Overlap with the candidate's domains | 90+ direct overlap (trust & safety, integrity, fraud/scams, risk & compliance, governance, enterprise AI/agents, data platforms, financial-services/fintech, ads, commerce); 70 adjacent (security, identity, payments, developer/cloud platforms, B2B SaaS data/analytics); 50 general consumer/B2B product; 25 unrelated specialist domain (hardware, clinical, gaming design) |
| **pathway** | How realistic a Canadian work permit is for someone hired from the US (DR-3), from the posting and the company | 95 Google (intra-company transfer); 85 posting states visa sponsorship or relocation support; 65 large multinational or known Global Talent Stream user (inferred); 45 no information; 15 posting says no sponsorship / must already be authorized to work in Canada. Say whether it is stated or inferred |
| **pay** | Featured Canadian range vs. target (`config/scoring.json`) | ≥ excellent 95; ≥ good 80; ≥ ok 60; ≥ low 40; below 20; no Canadian range 50 (say "not posted"). US-only ranges: 50 and say so. Bonus-inclusive or OTE ranges: compare at 90% |
| **skills** | Must-haves the candidate has | 90 has nearly all must-haves; 70 most; 50 unclear; 30 missing key ones (e.g. deep domain credential, specific language, hands-on engineering) |

## Also extract
- `summary`: one plain sentence on what the job is ("Own the roadmap for X used by Y").
- `level_guess`: e.g. "Senior PM (≈ L5)", "Principal PM (≈ L6)".
- `people_mgmt`: true only if the posting says the role manages people.
- `work_mode`: onsite / hybrid / remote / unclear.
- `must_haves`: up to 4 short items.
- `flags`: short warnings (e.g. "French required", "Security clearance", "Contract role", "Retail store role").

## Rules
- Judge the posting, not the company's reputation.
- Reasons are specific and short (≤ 120 characters), written to the candidate ("Matches your ads-safety work").
- Never mention personal immigration or family details in reasons; say "work permit" generically.
