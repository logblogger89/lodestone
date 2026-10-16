---
name: market-check
description: Lodestone on-request market pay check. When Ayush asks to check levels.fyi (or "market pay") for a specific role, read that company's levels.fyi page for the role's family and location, pick the matching level, and attach it to the role in the app. Only for roles Ayush asked about: his own request in chat, or his Request market check taps in the app (answered in refresh step 3c). Never bulk or unrequested.
---

# Market check (levels.fyi, D-054)

levels.fyi's terms forbid automated reading and compiling datasets. Its robots.txt allows a fetch a person asks for
at that moment (`Claude-User`). So this runs **only when Ayush asks about named roles**, one page per role, and
never inside `/refresh-jobs`, a scheduled task, or "all roles" sweeps. If he asks for many roles at once, suggest
the paste inbox instead (he pastes the pages himself).

1. `python3 -m lodestone market fetch "<job id, or words from company + title>"`
   - `pick_one`: show him the matches and ask which. `not_found`: the role isn't in the current results.
   - `no_data`: levels.fyi has no Canadian figures for that company and role family (it falls back to US
     numbers, which we never use). Tell him so; `config/market.json` maps regions, role families and company slugs
     if the URL guess was wrong.
2. Pick the company level that matches the role: use the posting title, the role's `level_guess` (Google-equivalent)
   and the page's years-of-experience notes. If unsure between two, choose the lower and say so in the note.
3. `python3 -m lodestone market add <job id> <level> "<one line on why this level>"`
4. `python3 -m lodestone export` and push the changed `jobs/b*` documents (refresh-jobs step 6), commit
   `data/state/market_checks.json`, and tell Ayush the figure in plain words: it is median **total** pay
   (base + stock + bonus), so it runs higher than posted base ranges.

## Requests from the app (D-055)

Ayush can tap **Request market check** on a role in the app. Each scheduled run answers them once, in `/refresh-jobs`
step 3c (and a hand-run session can too):

1. `ArtifactData list market_req` with `out_dir` set to a scratchpad folder, then
   `python3 -m lodestone market pending <that folder>`. It returns up to `daily_cap` (20, `config/market.json`)
   requests, oldest first, minus the levels.fyi reads already made today (New York time) in any run; the rest wait
   for the next day.
2. Run steps 1–3 above for each. Each request is Ayush asking about that one role, which is why this is allowed;
   never add roles he didn't request.
3. Write each back with `ArtifactData update market_req/<id>` (if_version from the list): `status` `done`, `no_data`
   or `failed`, and a one-line `result` (fields `status` and `result` only). Then export and push as in step 4.

Always credit "Data source: Levels.fyi" with the link (their attribution rule); the app does this automatically.
