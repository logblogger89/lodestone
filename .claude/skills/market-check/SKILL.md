---
name: market-check
description: Lodestone on-request market pay check. When Ayush asks to check levels.fyi (or "market pay") for a specific role, read that company's levels.fyi page for the role's family and location, pick the matching level, and attach it to the role in the app. Never run as part of a refresh.
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

Always credit "Data source: Levels.fyi" with the link (their attribution rule); the app does this automatically.
