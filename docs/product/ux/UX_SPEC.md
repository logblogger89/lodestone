# Lodestone — UX Spec (M2)

| | |
|---|---|
| **Owner** | Claude (UX, under PM), for Ayush's review |
| **Status** | v0, in review (gate M2) |
| **Implements** | [PRD v0](../PRD.md) P0 requirements R1–R15, CUJ-1 to CUJ-7 |
| **Prototype** | [prototype.html](prototype.html) (open locally, or via the published link in the tracker) |

---

## 1. Design principles

1. **Glanceable in 5 minutes on an iPad.** The digest comes first. Tap targets are at least 44px, and nothing needs hover.
2. **Never hide, always label.** Estimates ("est."), inferred signals and unknowns are visible and marked. Filters never drop a job just because data is missing (D-021).
3. **Explain every number.** The fit score expands into sub-scores, each with a one-line reason.
4. **Two taps to triage.** Interested, Later and Not are always visible. Reasons are optional chips.
5. **Every claim links to its source.** Source icons, "found on" entries and pathway-signal sources are deep links (the exact posting, dataset or official page). Jargon (role tier, LMIA, CEC, Stated/Inferred/Unknown) is explained in place via a "What do these labels mean?" panel. (Ayush's review, 2026-10-14)
6. **Built for one, ready for many.** Every preference lives in Settings as data, not code (D-005).

## 2. Information architecture

```
Lodestone
├── Digest (home)            CUJ-2, CUJ-4: top N new matches (default 20, 1–100), then all ranked
│   └── Listing detail       CUJ-3: fit breakdown, pay, pathway signals, sources, actions
├── Pipeline                 CUJ-6: Discovered → Shortlisted → Applied → Screen → Interviewing → Offer → Closed
├── Add job (global)         CUJ-5: paste URL(s) or JD text from anywhere (Cmd/Ctrl+V or the + button)
├── Companies                CUJ-7: watchlist, discovery candidates, source health
└── Settings                 CUJ-1
    ├── Profile              CV-derived profile, editable
    ├── Preferences          locations, work mode, role families, pay filter, toggles, digest size
    └── Advanced             score weights (sum to 100%)
```

**Navigation:** a bottom tab bar on iPad and phone, a left rail on desktop. "+ Add job" is always reachable from the top bar.

## 3. Key flows

```mermaid
flowchart LR
  A[Open app] --> B[Digest: N new since last visit]
  B --> C{Scan card}
  C -->|Tap card| D[Listing detail]
  C -->|Interested / Later / Not| E[Triage + optional reason]
  D --> E
  E --> F[Interested → Pipeline: Shortlisted]
  E --> G[Reasons feed weights + eval set]
```

```mermaid
flowchart LR
  P[Cmd+V or + Add job] --> Q{URL fetchable?}
  Q -->|Yes| R[Parse → resolve to ATS → dedup]
  Q -->|No, e.g. LinkedIn login wall| S[Ask for JD text]
  S --> R
  R --> T{Already known?}
  T -->|Yes| U[Add source icon · 'Already in Lodestone via Greenhouse']
  T -->|No| V[Confirmation card: fix parsed fields → Save]
```

## 4. Screen specs

### 4.1 Digest (home)
- **Header:** "N new since your last visit", digest size, and active filter chips (tap to edit)
- **Job card:** title · company · location and work mode · posting age · **fit score** (0–100, with a ring) · **source icons** (one per source, A1) · **pay** (as posted, or an estimate with an "est." icon, B8) · **pathway chips** (ICT, Sponsorship, Sponsored before, GTS, CEC credit), each marked Stated / Inferred / Unknown · **Internal transfer** badge (B10) · repost or "no longer live" flags · triage buttons
- **Sort:** fit (default), newest, pay. **Group:** "New" (the top N), then "Earlier"

### 4.1a Freshness panel (R11a)
- A header chip on every screen: "Updated 2h ago". Tap it to open a panel listing job pulls (overall and per source), scoring (time, prompt and model version), pathway signals (ESDC quarter), discovery and profile, each with a timestamp. Items older than 7 days are flagged.

### 4.2 Listing detail (updated 10-16, D-065)
A side drawer (full screen on phones). **Header, always visible:** role type (Core PM / PM-adjacent / Stretch with what it means), title, company and location, then the actions: Interested · Later · Not for me · **Open posting ↗** (full width on phones).

Below the header, three **tabs** (ARIA tabs; arrow keys move between them; the bar sticks to the top while you scroll). The tab you pick stays selected as you move between roles with J/K, so you can read descriptions one after another.
1. **Summary** (default, for deciding): against-your-preferences checks with reasons; fit breakdown (sub-scores, weights, reasons); posting facts (location, work mode, team, posted, experience asked, people management); pay (posted ranges, estimate, equity, market check); work-permit signals table with status and linked source ("Signals, not immigration advice"); every source with live/gone; pipeline stage and notes.
2. **Job description** (for reading): the posting as written, formatted (headings, bullet lists, paragraphs), with the sentences Lodestone used for **years of experience and pay highlighted** so you can check them in context. Header line: which site it's from, when it was read, and a link to the original. Legal notices (equal opportunity, accommodation, privacy) are left out with a one-line note; very long postings are cut at about 12,000 characters with a link to the rest. Loaded only when the tab opens (the digest stays fast). States: loading · couldn't load (link to original) · not read (link to original).
3. **Company & team** (for context): **About the company**: its own "About us" text from its postings ("In its own words"), or a short **Summary by Claude** labelled as possibly dated when its postings don't describe it; facts: open roles in Lodestone (with "See all", which filters the digest to that company), where in Canada, work-permit evidence, careers site. **The team**: the posting's team name and its "About the team" section when there is one; otherwise says plainly that the posting doesn't describe the team.

Why tabs: the Summary is what you decide on and was already long; descriptions run 7,000–11,000 characters. Putting them in their own tab keeps the decision view short and the reading view uninterrupted, on the iPad as well as the laptop.

### 4.3 Add job
- One input that takes **one or more URLs, or pasted JD text**. Cmd/Ctrl+V anywhere opens it pre-filled
- States: parsing → **confirmation card** (editable fields) → saved; **already known** (adds the source icon); **can't fetch** (asks for JD text)
- Coaching tips (A3h): "Found a role on LinkedIn? Copy the link and press Cmd+V here."

### 4.4 Pipeline
- Kanban with seven stages. Cards show fit, pay and a **no longer live** flag
- Drag (desktop) or a stage menu (touch) to move. Closed postings keep their history

### 4.5 Companies
- **Watchlist:** company, segment, discovery pathway(s), ATS, open Canadian roles, last refresh, mute/block
- **Candidates:** discovered companies waiting for review (ATS not found, or Canada presence unclear)
- **Source health:** each source with last success, item count and errors

### 4.6 Settings
- **Profile:** fields extracted from the CV (current employer, roles, scope signals, domains, skills). All editable
- **Preferences:** locations (GTA + Waterloo, expand to Canada) · work mode · role families by tier · pay range (CAD) · **include roles without posted pay** · **exclude people-management roles** · digest size (1–100, default 20)
- **Advanced:** six weight sliders that always sum to 100%, plus "Reset to defaults"

## 5. Visual direction

- **Theme:** "magnetite and survey map." Cool mineral neutrals with a slight blue-grey bias, and one deep ore-blue accent for primary actions and scores. Semantic colors (good, caution, unknown) are separate from the accent. Light and dark themes are both designed.
- **Type:** a characterful grotesque for headings and the wordmark, a highly legible sans for body text, and a mono face for numbers (scores, pay, dates) with tabular figures.
- **Signature detail:** the fit score is drawn as a **compass ring**. Fill shows the score, and the needle points "true north" at 100. It's used sparingly: on cards and in the detail header.

## 6. Accessibility

- WCAG AA contrast in both themes. Status is never shown by color alone (chips always carry text)
- Visible focus states. Full keyboard support on desktop: **J/K** to move, **I/L/N** to triage, **Enter** to open, **Cmd/Ctrl+V** to add a job
- Respects `prefers-reduced-motion`

## 7. UX review questions (resolved 2026-10-14)

1. Card density on iPad: **fine as is.** The card shows the right things at a glance (D-030).
2. "Later" roles **come back in the digest after 7 days** (adjustable in Settings) (D-031).
3. Marking a role **Interested adds it to Shortlisted** in the pipeline automatically (D-032).

## 8. UX v2: end-to-end flow and onboarding (10-16, D-066, D-067)

Lodestone is for **people moving countries for work** (D-066). Many arrive without a ready resume, or with one they'd rather not share yet. v2 is designed from their point of view: show value before asking for effort, ask one thing at a time, and let every action quietly sharpen the matches.

### 8.1 Who arrives, and what they're thinking
| Person | In their head | What the design does |
|---|---|---|
| No resume ready | "Let me see what's out there first" | Three ways to say what they want, none needs a resume |
| Half-baked resume | "It undersells me; matches will be wrong" | Resume comes later, as an upgrade, with "a rough draft is fine" and an editable "what we understood" |
| Privacy-wary | "Where does this go? Why ask my status?" | Privacy promise on the first screen; every question says why it's asked |
| Busy, on a phone | "5 minutes, show me something" | Real roles in about a minute; one question per screen |
| Unsure of status | "I don't know what permit I'd need" | "Not sure" is a first-class answer with a short explainer |
| Citizen or PR | "Is this for me?" | Yes: the work-permit layer hides; nothing feels "not for them" |

### 8.2 Principles (extends §1)
1. **Value before effort.** Real roles on screen within a minute; ask for more only after showing why.
2. **One clear next action per screen.**
3. **Every signal is a free answer.** Taps, reasons, reading and pipeline moves teach the ranking; no tuning forms.
4. **Show the learning** in plain words ("Ranked higher: like 3 AI-platform roles you shortlisted").
5. **Explain on screen, never on hover.**
6. **The user is in control.** Everything inferred is visible, editable and can be switched off.

### 8.3 Onboarding (first visit)
1. **Welcome.** Promise: *"Find the jobs that fit you, in the country you want to move to, and the ones that will actually hire you."* Privacy line: "Everything you tell us stays private to you. Nothing is shared with employers." Button: **Get started**.
2. **Where do you want to work?** Country (Canada live; others "coming soon: tell us where", recorded as demand), then cities or "anywhere in the country / remote".
3. **Can you already work there?** "Yes, I'm a citizen or permanent resident" · "I have an open work permit" · "I'll need sponsorship" · "Not sure" (treated as needing sponsorship, with a two-line explainer). "We use this only to show which employers hire people from abroad."
4. **What kind of role?** Three ways, none needs a resume: type it in your own words ("senior PM, fintech, ~8 years"); paste a job you'd love; or "Not sure, show me examples" (tap role-family cards). Fields not covered yet get an honest "We don't cover this yet; want us to tell you when we do?"
5. **Quick taste test (8 real roles, skippable).** Interested / not for each. Feels like browsing, and every tap trains the ranking.
6. **Your list.** Banner: "Based on 3 answers and 8 taps. Your personalised ranking arrives tomorrow morning and gets sharper as you use Lodestone." (Scoring runs in the daily run, not on the viewer's Claude usage: Ayush, 10-16.) Until then the list is filtered by destination, status and role and sorted by the taste test and recency.

### 8.4 The profile, later, as an upgrade
Offered after the first session, or when a user opens a role's fit details ("Fit: not personal yet"). "Want sharper matches? Add your experience to see how it fits each role." Reassurance in plain words: a rough draft is fine; only you can see it; never sent to employers; delete it any time. Three ways:
- **Upload** a resume (PDF or text).
- **Paste** any text (even a LinkedIn "About" section and job titles).
- **Build it with me** (MVP): about five short questions (current role and level, years, biggest win, domains, tools). Answers are saved instantly; the profile is built at the next daily run. The resulting summary can also be copied as a starting point for a resume.
After it's read: **"Here's what we understood"**, every line editable, so a weak resume never has the last word.

### 8.5 Match quality grows with signals
| Level | What we know | What the user gets |
|---|---|---|
| 0 Answers | Destination, status, role in their words | Filtered list with work-permit signals, newest first |
| 1 Taste test | ~8 likes and dislikes | Ranking by similarity to what they liked |
| 2 Profile | Experience, level, domains (resume, text or build-with-me) | Fit scores with plain reasons |
| 3 Daily use | Triage, "Not for me" reasons, what they open and read | Rankings that learn; one-tap suggestions |
| 4 Applying | Pipeline moves | Nudges, follow-ups, pay checks |
Shown on the Profile page as a meter: "Match quality: level 2 of 4 · Triage 10 more roles to reach level 3."

### 8.6 Learning from signals (Q-23)
- **Explicit:** Interested, Later, Not for me + reason, pipeline moves, market-check requests.
- **Reading time** on the Job description tab (and opening the original posting), capped per role, **with an off switch** in the Profile ("Learn from what I read").
- **Preference suggestions, one tap to accept** (never applied silently): after three "Pay too low", "Raise your pay target to CA$190K? · Accept · Not now". Accepted changes show in the Profile with their reason and can be undone.
- **More / less like this** acts on the pattern (domain, company type, level), not only the one role.
- **Exploration:** about 1 card in 10 is outside the user's pattern, labelled "Something different".
- **Explain:** each card can say why it's ranked where it is, in a sentence.

### 8.7 Ask only when it matters (one-tap questions)
Asked once, at the moment they're relevant, each dismissible: first "Pay too low" → minimum base pay; three people-manager dismissals → hide manager roles?; shortlisting a role outside the user's regions → add that city?; a role at the user's current employer → count transfers as a strong route?

### 8.8 The daily loop
- **Today:** "N new for you" (default up to 10), a short stack you can finish ("All caught up" when done). The full ranked backlog is one tap away under "All roles".
- **Evaluate:** the role view (§4.2) plus "why it's ranked here" and more / less like this.
- **Act:** Interested opens a gentle next step: Open posting · Request market check · Add a note.
- **Track:** pipeline with nudges ("Applied 10 days ago: follow up?") and closed-posting alerts.
- **Weekly:** a Monday "Your week": market changes, what Lodestone learned about you, companies to consider.
