# Postmortem: pay ranges in posting text shown as "No pay posted"

| | |
|---|---|
| **Date** | 2026-10-15 |
| **Found by** | Ayush, on a Thomson Reuters Product Manager role in the app (P1-S2 review) |
| **Severity** | High for the product: pay is a core triage signal (R5, B8) |
| **Status** | Fixed (D-045) |

## What happened
The app showed "No pay posted" for roles whose postings state a pay range. Example: Thomson Reuters lists ranges for named US cities, for other US locations, and "For Ontario, Canada ... $126,000 CAD - $176,000 CAD".

## Impact
Of 546 candidates, pay was captured for 26 (5%). A further 247 (45%) stated a range in the description text that Lodestone ignored, mostly Workday (125 of 146) and Greenhouse (74 of 92). 79 roles had no description fetched at all, and 41 RBC/Bell/Air Canada roles had only a 2-line teaser, so their pay was never checked.

## Root cause
Pay was read only from structured salary fields, which only a few job systems have (Ashby, Lever, HiBob, ADP). Most employers write the range into the description text instead. No step read pay from text.

## Contributing causes
1. The UI asserted a fact it hadn't checked: "No pay posted" instead of "not detected".
2. Quality checks looked at titles and locations only; there was no test or coverage metric for pay.
3. A known signal was missed: DR-4 records Ontario's pay-transparency rules (Jan 2026), so most Ontario postings should carry a range. 5% coverage should have been a red flag.
4. Found during the fix: list views with no description (Avature, Coveo, Rippling, iCIMS, SmartRecruiters, Njoyn) and Phenom teasers were never expanded; a bot-check page from CGI was stored as a description; jobs from sources that errored on a run kept stale pay.

## Fix (D-045)
- `lodestone/pay.py` reads every range in the posting text (formats like `$126,000 CAD - $176,000 CAD`, `$140K–$175K`, `CA$…`, hourly), with the region each sentence names (carrying context such as "in any of those locations" from the previous sentence), and picks the Canadian range to feature: the job's own city or province first, then any Canadian range. Ashby's per-country salary tiers are used instead of its single summary.
- All ranges are kept. The app features the Canadian one on the card ("CA$126K–176K Ontario  +2 US") and lists every range, with the sentence it came from, in the role's detail view. US-only postings say "US range only".
- Full postings are now fetched for every role match whose list view has no description (or only a teaser), with bot-check pages discarded.
- Wording: "No pay in posting" only when the full posting was read; otherwise "Pay not checked yet".
- Tests for real phrasings (multi-region Thomson Reuters, K-notation, hourly, US-only, non-pay numbers, Ashby tiers). Every refresh now reports pay coverage (`pay_found`, `pay_canada`).

## Lessons / action items
- [x] Report coverage for every field the UI shows (pay now; extend to work mode and level in S3).
- [x] Never label missing data as a fact about the employer; distinguish "not stated" from "not checked".
- [x] Runbook rule: when a field is unexpectedly empty for most roles, investigate before reporting.
