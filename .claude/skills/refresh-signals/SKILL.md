---
name: refresh-signals
description: Lodestone pathway-signal refresh. Download the newest ESDC positive-LMIA employer lists and recompute each role's work-permit pathway signals. Use when Ayush says /refresh-signals, or quarterly when ESDC publishes a new list.
---

# /refresh-signals (D-039, R10)

1. Find the newest quarters at https://open.canada.ca/data/api/3/action/package_show?id=90fed587-1364-4f33-a9ee-208181dc0b97
   (English `tfwp_YYYYqN_pos_en.xlsx` files). Keep the latest 9 quarters in `data/external/esdc/` (not committed;
   public data, re-downloadable). Remove older files so the window stays about two years.
2. `python3 -m lodestone signals load` parses them and matches employers to the watchlist using
   `config/employer_aliases.json` (add an alias when a company's legal name differs from its brand; short brand
   names only match through an alias). Review new matches for false positives before trusting them.
3. `python3 -m lodestone export`, then push to the app as in /refresh-jobs step 6. Commit and report which
   companies gained or lost LMIA evidence.

Signals, not advice: the app always says so and links each signal to its source.
