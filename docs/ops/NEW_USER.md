# Setting Lodestone up for another person (D-060, Q-24 option A)

Lodestone is designed for anyone who isn't yet a Canadian citizen or permanent resident and wants work in Canada,
in tech product and adjacent roles (other industries later). Today each person gets **their own private copy**: their
own app, their own data and their own daily run. A shared sign-in comes later (Phase 2).

Nothing about a user is in the code. Everything personal lives in the app's Profile page:
resume, current employer (for internal transfers), current level, where they live, work-permit status, the regions,
role types, domains, level and pay they want, colour rules, ranking weights and app settings.

## Steps (Claude does these in a Claude Code session; the new user only uploads a resume and fills in the Profile)
1. **Repository.** The new user's own copy of the Lodestone repo (a private fork or a new branch they own). Their job
   data, scores and reports live there, never mixed with anyone else's.
2. **App.** Publish `app/lodestone.html` as a new private Artifact owned by the new user, with the same capabilities
   (`db` with the profile rule, `user`, `assets`). Put its link in the runbooks (`.claude/skills/*`, `docs/ops/daily-run-prompt.md`).
3. **Empty data.** Start with the shared watchlist and source index; clear `data/state/` (jobs, scores, reports,
   discovery, market checks) so nothing of the previous user's carries over.
4. **Profile.** The new user opens the app → Profile, uploads their resume (PDF or pasted text), picks their work-permit
   status, regions, target level and pay, and saves. The next run reads the resume and fills in the rest.
5. **Daily run.** Create their own daily scheduled task (see `daily-run-prompt.md`) in their own session.
6. **First run.** Refresh, then scoring of every role against the new profile. Scoring is capped per day, so a full
   first pass takes a few days on a standard plan.

## Privacy
Each user's resume and profile stay in their own app's private database and asset store. Never commit them, never put
them in reports, and never share one user's app or data with another.
