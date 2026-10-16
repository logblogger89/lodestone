# Setting Lodestone up for another person (D-060, Q-24 option A)

Lodestone is for people moving countries for work (D-066). It starts with tech product and adjacent roles in Canada,
built first for people who need a work permit; citizens and permanent residents are welcome too. Other roles and
countries come later. Today each person gets **their own private copy**: their
own app, their own data and their own daily run. A shared sign-in comes later (Phase 2).

Nothing about a user is in the code. Everything personal lives in the app's Profile page:
resume, current employer (for internal transfers), current level, where they live, work-permit status, the regions,
role types, domains, level and pay they want, colour rules, ranking weights and app settings.

## Steps (Claude does these in a Claude Code session; the new user only uploads a resume and fills in the Profile)
1. **Repository.** The new user's own copy of the Lodestone repo (a private fork or a new branch they own). Their job
   data, scores and reports live there, never mixed with anyone else's.
2. **App.** Publish `app/lodestone.html` as a new private Artifact owned by the new user, with the same capabilities
   (`db` with the profile rule, `user`, `assets`). Put its link wherever the current one appears: `.claude/skills/*`,
   `docs/ops/daily-run-prompt.md`, `docs/ops/update-run-prompt.md` and `docs/eng/ENG_DESIGN.md` (`grep -r` for the
   old link).
3. **Empty data.** Start with the shared watchlist and source index; clear `data/state/` (jobs, scores, reports,
   discovery, market checks) so nothing of the previous user's carries over.
4. **Profile.** The new user opens the app → Profile, uploads their resume (PDF or pasted text), picks their work-permit
   status, regions, target level and pay, and saves. The next run reads the resume and fills in the rest.
5. **Scheduled runs.** In their own session, create their two scheduled tasks: the full morning run
   (`daily-run-prompt.md`) and the midday and evening updates (`update-run-prompt.md`).
6. **First run.** Refresh, then scoring of every role against the new profile (a few hundred roles, a large share of a
   day's Claude usage). After that only new or changed roles are scored, plus up to 150 re-scores a day when the
   profile changes.

## Privacy
Each user's resume and profile stay in their own app's private database and asset store. Never commit them, never put
them in reports, and never share one user's app or data with another.
