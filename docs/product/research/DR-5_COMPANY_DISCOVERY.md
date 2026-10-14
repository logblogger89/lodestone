# DR-5 — Company Discovery: Seed Watchlist and Discovery Pathways

| | |
|---|---|
| **Feeds** | PRD R1 (ingestion), R1a (company discovery engine), A2 (watchlist) |
| **Status** | v1, 2026-10-14. Seed list: **[data/seed/watchlist_seed.csv](../../../data/seed/watchlist_seed.csv)** (210 companies + 17 discovery sources) |

---

## 1. Principle

A fixed list goes stale. **The watchlist is the output of a discovery engine, not a hand-curated list.** The seed only starts it. Every pathway below drops *candidate companies* into a queue. Lodestone then **auto-detects the company's ATS** (by probing Greenhouse, Lever, Ashby and SmartRecruiters slugs, and following career-page links to Workday or Workable) and **checks for Canadian presence** (any posting located in Canada, or remote-Canada). Candidates that pass go on the watchlist automatically. The rest wait in "needs review."

## 2. Seed watchlist v1 (in the CSV)

| Segment | Count | Examples |
|---|---|---|
| Big tech / US tech with Canadian offices | 56 | Google (ICT), Microsoft, Amazon, Meta, Nvidia, Uber, Stripe, Snowflake, Salesforce, Reddit, Cloudflare, Zip, Legora |
| Canadian AI and deep tech | 30 | Cohere, Ada, Waabi, Tenstorrent, BenchSci, **Armilla AI and Private AI (AI-governance fit)**, Borealis AI, Layer 6 |
| Canadian fintech and payments | 30 | Wealthsimple, KOHO, Neo, Float, Nesto, Interac, **Trulioo (identity verification), Verafin (fraud/AML)** |
| Canadian SaaS and scale-ups | 66 | Shopify, Clio, Faire, 1Password, Arctic Wolf, Kinaxis, **Assent and Resolver (compliance fit)**, Magnet Forensics |
| Banks, insurers, telcos, large enterprises | 28 | RBC, TD, BMO, Scotiabank, CIBC, Manulife, Sun Life, Intact, TELUS, Rogers |
| Ecosystem orgs and VCs (discovery seeds) | 17 | Communitech, MaRS, DMZ, CDL, Inovia, Radical, Golden, Portage, a16z, YC |

**Caveats.** The list combines web research (2026-10-14) with Claude's knowledge. Search snippets were the only research channel available (page fetching was blocked in this environment). Every row is **unverified** until the app's ATS-detection and Canada-presence checks run. Rows marked *verify* are less certain (offices, HQ, current status).

## 3. Discovery pathways (beyond the seed)

| # | Pathway | How it works | Tier |
|---|---|---|---|
| P1 | **ATS reverse search** | Search-engine queries for ATS hosts plus Canadian locations, e.g. `site:boards.greenhouse.io "Toronto" product`, `site:jobs.lever.co Canada`, `site:jobs.ashbyhq.com "Remote - Canada"`. Every new slug becomes a company with its ATS already known. **Likely the highest-yield pathway** | MVP (needs a search API key) |
| P2 | **VC and ecosystem portfolio boards** | Pull company lists from Getro or Consider boards (Inovia, Communitech, BDC, Diagram, a16z…), MaRS, CDL, DMZ and Vector Institute partner pages | MVP |
| P3 | **ESDC positive-LMIA employer list** | The quarterly government list of employers that sponsored foreign workers. Filter to tech and management occupations. It's a discovery source *and* a sponsorship signal (CR-3a) | MVP |
| P4 | **Capture spill-over** | Any company first seen via a pasted link (A3) or a job-alert email (A3e, V1) becomes a candidate automatically | MVP |
| P5 | **Funding news** | Watch BetaKit, The Logic and press-wire funding announcements. Newly funded Canadian companies are about to hire | V1 |
| P6 | **Community threads** | Reddit (r/cscareerquestionsCAD, r/askTO, r/waterloo), Blind Toronto threads, and HN "Who is hiring" (official API). Pull company names out of posts mentioning Canadian roles or offices | V1 |
| P7 | **Rankings and awards** | Deloitte Technology Fast 50, Globe and Mail Top Growing Companies, Canada's Top 100 Employers, Seedtable and Tracxn lists, Built In "Best Places to Work" | V1 (yearly) |
| P8 | **"More like this"** | From companies Ayush marks Interested, suggest look-alikes: same investors, sector, size and stage | V1 |
| P9 | **Conference sponsors and exhibitors** | Web Summit Vancouver, Elevate (Toronto), SaaS North (Ottawa), ALL IN (Montreal AI), TechTO | Later |
| P10 | **Remote-first employers hiring in Canada** | Remote boards (Himalayas, etc.) filtered to "Canada eligible" | V1 |

## 4. Requirements this implies (R1a, see PRD)

- A **candidate company queue** that records each candidate's discovery pathway, auto ATS detection, a Canada-presence check, and auto-accept vs. needs-review
- A **pathway registry** as config (D-005), so a new pathway is a plugin
- **Watchlist UI:** for each company, its source pathway(s), ATS, count of open Canadian roles, last refresh, and an option to mute or block
- Target: **≥500 watchlist companies within 2 weeks of MVP dogfood**, growing automatically from there

## Sources

- [Blind: best Toronto tech companies 2025](https://www.teamblind.com/post/2025-best-toronto-tech-companies-to-work-8tszbwz4) · [Glassdoor: top Toronto PM employers](https://www.glassdoor.com/Explore/top-product-manager-companies-toronto_IO.4,19_IL.30,37_IC2281069.htm)
- [BetaKit: Waabi Series C](https://betakit.com/waabi-lands-750-million-usd-series-c-partners-with-uber-on-robotaxis/) · [BetaKit: Beacon Series C](https://betakit.com/ai-rollup-company-beacon-closes-225-million-series-c-round/) · [BetaKit: Digitail Series B](https://betakit.com/digitail-grows-toronto-hub-as-it-fetches-23-million-usd-series-b-round/)
- [Deloitte Technology Fast 50 2025](https://www.deloitte.com/ca/en/about/press-room/deloitte-canada-unveils-2025-technology-fast-50-program-winners-as-tech-resilience-powers-cross-country-innovation.html)
- [Seedtable: AI startups in Toronto](https://seedtable.com/best-ai-startups-in-toronto) · [Tracxn: AI in Canada](https://tracxn.com/d/artificial-intelligence/ai-startups-in-canada/__--w76hANh0pcvjf4mrYKzjkUhRzpAVLHxfhJAAT4fGU/companies) · [Cohere (Wikipedia)](https://en.wikipedia.org/wiki/Cohere)
- [Karat: Toronto engineering talent](https://karat.com/toronto-software-engineering-talent/) · [Legora Toronto office](https://legora.com/newsroom/legora-expands-north-american-footprint-with-san-francisco-and-toronto-offices-new-york-engineering-hub) · [Zip Toronto office](https://www.businesswire.com/news/home/20251125219369/en/Zip-Accelerates-Canadian-Expansion-with-New-Toronto-Office-Plans-to-Nearly-Triple-Local-Workforce)
- [The Logic: YC and Canada](https://thelogic.co/news/exclusive/y-combinator-canada-startups/) · [vcbacked: YC companies in Toronto](https://www.vcbacked.co/yc/location/toronto)
- [fintech.ca: startups to watch 2026](https://www.fintech.ca/2026/01/07/canadian-fintech-startups-to-watch-in-2026/) · [Tracxn: Toronto fintech](https://tracxn.com/d/explore/fintech-startups-in-toronto-canada/__rSBKKPBKITCuka7_I0J9gyO27QdHypkvqSNcT7joSNs)
- [HostPapa, Globe Top Growing 2025](https://www.hostpapa.ca/about-hostpapa/pressroom/2025-09-26-hostpapa-ranks-no-115-on-the-globe-and-mail-s-canada-s-top-growing-companies-2025/) · [Tech Alliance London honourees](https://www.techalliance.ca/?p=49205)
