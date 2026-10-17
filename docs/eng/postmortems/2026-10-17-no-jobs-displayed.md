# Postmortem: the app showed no jobs (10-17)

| | |
|---|---|
| **Date** | 2026-10-17 (app v32 and v33, roughly 03:00 to 07:40 UTC) |
| **Found by** | Ayush: "after the taste test my digest was empty", then "no jobs get displayed still" |
| **Severity** | Critical: the app's main screen was empty for its only user |
| **Status** | Fixed in v34 (D-079) |

## What happened
After type scores shipped (D-077, v32) the Digest showed no roles. The Today list was saved empty, so the app said
"You've reviewed your top matches" although nothing had been reviewed. A v33 fix for the empty list did not help,
because it treated a symptom.

## Root cause
The claude.ai database delivers frozen objects (runtime contract 0.2.80, `db.d.ts`: "Delivered snapshots and their
data() are frozen"). The app wrote its own fields (relevance, type, closeness) onto each job object it received. The
app runs in strict mode, so each write threw; no job got a relevance score, and the rule "show a job from relevance 50"
hid all 946 roles. Before v32 the same writes failed too, but the values they wrote were already in the data, so
nothing visible broke.

## Why testing missed it
The test harness imitated the database with ordinary, writable copies. 274 checks passed, and a "replay with Ayush's
real data" passed too, because it used the same imitation. The tests covered the app's logic but never checked that
the imitation behaves like production. Claude reported the work as rigorously tested; it was not tested against the
one property that broke it.

## Contributing causes
1. A filter that hides by default when a computed value is missing (it should fail open: D-021, missing data never hides a job).
2. No signal from the real app: nothing told the scheduled runs, or Claude, that the live app showed zero roles.
3. No error boundary: a failure left a blank or misleading screen instead of saying something went wrong.

## Fix (D-079, v34)
- The app works on its own copies of delivered jobs.
- The test imitation now freezes everything it delivers, deeply, like the real database; it reproduced the outage
  exactly ("Cannot add property rel, object is not extensible") before the fix. A code search found no other writes to
  delivered data.
- Fail-safe: a role whose relevance can't be worked out is shown (and the failure recorded).
- Safety net: if a screen fails to draw, the user sees "Something went wrong showing this page", with Reload and a way
  to another page, never a blank page.
- Health note: the app saves `health/app` (version, roles visible, Today count, errors) when it opens; every scheduled
  run reads it and flags zero visible roles, errors or an old version (refresh step 0).
- Invariant checks after every persona journey, a resilience persona that breaks things on purpose, a 300-tap monkey
  test with a speed check (it found two slow paths, fixed: 4.7 s → 1.5 s for "Skip and browse"), and a scroll jump on
  every redraw (fixed).

## Lessons
- Test against the platform's contract, not our assumptions: read the runtime's type definitions when the contract
  version changes and keep the imitation faithful.
- "Done" means verified in the real app: after a release, read the health note from Ayush's next open before calling
  it done.
- Fail open, and fail visibly.
