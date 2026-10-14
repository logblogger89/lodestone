# DR-3 — Immigration Pathways (signals for Lodestone)

| | |
|---|---|
| **Feeds** | PRD CR-3, CR-3a, B9 (pathway signals), C15 and C16 (CRS calculator and PR impact) |
| **Status** | v1, desk research 2026-10-14. **Signals, not advice** (R-03). Confirm every decision with a licensed consultant (RCIC) or lawyer |

---

## 1. What changed vs. our earlier assumptions

| Earlier assumption | What the research says | Impact on Lodestone |
|---|---|---|
| A job offer adds CRS points | **Arranged-employment CRS points were removed on 2025-03-25.** IRCC called it temporary but gave no end date. A job offer still counts for *eligibility* in some programs and some PNP streams | A job's value for PR comes from **Canadian work experience** and **PNP or category eligibility**, not from offer points. Keep this as a config flag, since it may come back (R-12) |
| The Ontario PNP (Human Capital Priorities tech draws) is a lever | **Ontario closed HCP and the Employer Job Offer streams in 2026.** Sources give different dates (May 30 or June 25). They were replaced by a single **Ontario Workforce Priority** stream, whose EOI reopened 2026-08-04. No draws or minimum score have been published yet | Treat Ontario PNP as **"unknown, watch."** Other provinces' tech streams (e.g. BC) only matter if geography expands (D-007) |
| STEM category draws | The 2026 categories still include STEM, but with a **narrower occupation list**. New for 2026: **Senior managers (needs Canadian work experience)**, physicians, researchers and others. One Senior-managers draw (2026-09-16) had a CRS cutoff of **389** | Once Ayush has Canadian experience, check whether his NOC could qualify for a category. That's a lever for C15 |

## 2. Pathways and the signals Lodestone should detect

| Pathway | What it means for Ayush | Signals in a listing or employer | Confidence source |
|---|---|---|---|
| **Intra-company transfer (ICT)** | LMIA-exempt work permit. Needs about 1 year of full-time work in the past 3 years with the related company, in an executive, managerial or specialized-knowledge role. **Ayush qualifies at Google** (since 2020). Processing is roughly 2–16 weeks (sources vary). Exemption code to verify (commonly cited as C12) | Listing employer = current employer (B10, CR-4). Also any multinational where Ayush could first join the US entity, then transfer | Stated (employer match) |
| **Employer work permit with an LMIA** | The employer must get an LMIA, which is slow and costly. Many employers avoid it (R-07) | "Sponsorship available," "visa support," "relocation." The employer is on the **ESDC positive-LMIA list** | Stated in posting, or **Inferred** from the ESDC list (by quarter) |
| **Global Talent Stream (GTS)** | A fast LMIA (about 2-week target) for listed tech occupations, or via referral from a designated partner (Category A; the list was cut to 41 in Sep 2026) | Tech employer. Occupation on the GTS list. Employer history on the LMIA list | Inferred |
| **Canadian Experience Class (CEC)** | After **1 year of skilled Canadian work in the last 3 years**, Ayush is CEC-eligible and earns CRS points for Canadian experience. This is the realistic PR path | Any skilled role in Canada with a valid work permit counts. So PR impact (C16) ≈ "time to 12 months of Canadian experience" | Derived |
| **Provincial nomination (PNP)** | +600 CRS when nominated. Ontario's streams are in transition (see §1) | Province of the role. The PNP stream status comes from config | Config, refreshed |
| **Category-based draws** | Draws can have lower cutoffs (e.g. Senior managers at 389, but it needs Canadian experience) | The role's NOC and its mapping to a category | Derived (NOC classifier) |
| **Express Entry with no job offer** | Ayush's CRS is limited by age, and it drops at each birthday (R-09) | Not listing-specific. Comes from C15 | Calculator |

## 3. Requirements this implies

1. **Pathway badges per listing** (B9): *ICT-eligible*, *Sponsorship mentioned*, *Sponsored before (ESDC list, quarter)*, *GTS-likely*. Each one is labelled **Stated** or **Inferred** with its source and date. Missing signals show as **Unknown**, and a listing is never hidden for that (D-021).
2. **PR impact** (C16): for a role in Canada with a valid permit, estimate "CEC-eligible after 12 months." Show what changes in the CRS what-if (Canadian experience points, possible category eligibility).
3. **Rules as config** (R-12): CRS grid, arranged-employment flag, category list and cutoffs, PNP stream status. Each carries a version and an "as of" date, plus a link to the official IRCC tools.
4. **ESDC LMIA list ingestion:** quarterly XLSX. Match employer names to companies with fuzzy matching and manual overrides.

## 4. Open items to verify

- The current ICT exemption code and IRCC's guidance on specialized knowledge for PM roles
- The Ontario Workforce Priority stream's design and its first draws
- Which NOC fits Ayush's roles (e.g. 20012 computer and information systems managers vs. a PM-specific code) and which category it maps to
- Whether IRCC has restored arranged-employment points (check the official CRS page)

## Sources

- [CIC News: CRS points for arranged employment removed (Mar 2025)](https://www.cicnews.com/2025/03/breaking-canada-removes-bonus-crs-points-for-arranged-employment-from-express-entry-0353251.html) · [EIG Law](https://eiglaw.com/ircc-enacts-changes-to-the-express-entry-scoring-system/)
- [Fragomen: Express Entry category-based selection for 2026](https://www.fragomen.com/insights/canada-updates-to-express-entry-category-based-selection-for-2026.html) · [Avalvisa draw tracker](https://avalvisa.com/en/express-entry-draws/)
- [Bridgepoint Law: ICT work permit guide 2026](https://bridgepointlaw.ca/?p=37835) · [Welcomeaide: ICT 2026](https://welcomeaide.com/fr/blog/intra-company-transfer-work-permit-canada-2026) · [VisaPlace: ICT](https://www.visaplace.com/?p=41948)
- [Immigration 2 Canada: 2026 OINP updates](https://www.immigration2canada.com/2026-ontario-immigrant-nominee-program-oinp-updates/) · [ircc.com: OINP 2026](https://ircc.com/pnp/ontario-oinp-requirements) · [Treadstone Law: OINP tech draws](https://treadstonelaw.ca/articles/oinp-tech-draws-in-demand-occupations-ontario)
- [ESDC Positive LMIA Employers List](https://open.canada.ca/data/en/dataset/90fed587-1364-4f33-a9ee-208181dc0b97) · [GTS requirements (ESDC)](https://www.canada.ca/en/employment-social-development/services/foreign-workers/global-talent/requirements) · [CIC News: GTS partner list trimmed](https://www.cicnews.com/2026/09/canada-trims-list-of-partners-providing-access-to-fast-track-hiring-under-global-talent-stream-of-tfwp-0980494.html/amp)
