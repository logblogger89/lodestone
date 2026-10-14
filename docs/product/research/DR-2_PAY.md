# DR-2 — Pay Display and Estimation

| | |
|---|---|
| **Feeds** | PRD B8 (pay as posted, estimate with an "est." icon), CR-1 (range filter), CR-2 (no-range toggle) |
| **Status** | v1, 2026-10-14 |

---

## 1. Decisions already made

- **Display pay as posted**, with no normalization (B8). The currency is shown as posted.
- The filter (CR-1) compares in **CAD** internally, using a daily FX rate for USD postings (e.g. remote US roles).
- When no pay is posted, show an **estimate** with an "est." icon and a confidence level (CR-2).

## 2. Why estimates matter more than expected

Ontario's pay-transparency rules (from 2026-01-01) require ranges for employers with 25+ employees, capped at $50K wide, **but exempt roles above $200K** (DR-4). Many roles at Ayush's level will have no posted range. Postings below $200K, though, will reliably carry ranges, which **gives Lodestone its own calibration data**.

## 3. Estimation method (proposal; details in the Eng Design Doc)

In order of preference, with confidence falling down the list:
1. **Same company, same level, posted range.** Use another of the company's postings at a similar level (from Lodestone's own corpus). *High*
2. **Same company, adjacent level.** Extrapolate from that company's posted ladder. *Medium*
3. **Market benchmark** by city, role family and level (from public aggregates). *Low–Medium*
4. **LLM estimate** from JD signals, as a last resort. *Low*, always labelled

The estimate covers **base salary** (what postings disclose). Equity and bonus are shown separately as "not disclosed" unless stated.

## 4. Benchmarks seen (for orientation only)

- An aggregator citing levels.fyi puts **Toronto Staff PM median total comp at ~$227K** (P25–P75 about $184K–$292K) and **Toronto PM median at ~$133K**. **The currency isn't stated**, so verify before using it.

## 5. Sources

- [IdeaPlan: Staff PM pay, Toronto](https://www.ideaplan.io/product-manager-salary/staff-product-manager/toronto) · [IdeaPlan: PM pay, Toronto](https://www.ideaplan.io/product-manager-salary/product-manager/toronto)
- Ontario pay transparency: see DR-4 sources
