# Lodestone test personas and journeys (D-072)

> Owner: Product (UX) · Started 2026-10-16 · A living document: **every new feature adds a task to at least one persona,
> and new kinds of user add a persona.** The journeys run automatically (`node scripts/persona_test.cjs`) against the real
> app with an in-memory copy of its database; each run saves screenshots and a results file that Claude reviews by eye.
> All five people are fictional composites. None is a real user, and none carries real personal data.

## Why these five
Each persona stresses a different part of the product promise ("the jobs that fit you, in the country you want, that
will actually hire you", D-066), and a different way of using the app:

| | Persona | Situation | Work permit | Resume | How they use it | Stresses |
|---|---|---|---|---|---|---|
| 1 | **Priya**, Staff PM, Seattle → Toronto | Urgent, methodical | Needs sponsorship | Ready | Desktop + iPad, daily, 10 minutes | Today list, triage speed, pipeline, pay, "why ranked" |
| 2 | **Daniel**, product marketer, arriving in Calgary | New, anxious, unsure what fits | Open work permit (spouse) | None yet | Laptop, first visit | First-time experience, empty profile, PM-adjacent roles, paste a job |
| 3 | **Mei**, AI PM, permanent resident in Montreal | Not urgent, exploring the market | Doesn't need one | Ready | Desktop, weekly, browses | Companies, pay comparison, search, the work-permit layer for someone who doesn't need it |
| 4 | **Tomás**, TPM, Mexico City | Busy, sporadic | Needs sponsorship | Half-done | Phone only, a few minutes on the bus | Mobile layout, Later, "Not for me" reasons, one-tap suggestions, catching up after days away |
| 5 | **Aisha**, Principal PM, London → Toronto | Careful, privacy-minded | Needs sponsorship | Ready | Keyboard only, screen reader | Keyboard flow, focus, labels, learning controls, deleting her data |
| 7 | **Lena**, Group PM with a design background, Berlin → Vancouver | Discerning, judges a product by its polish | Needs sponsorship | Ready | Large desktop monitor, laptop, phone; light and dark mode | Visual consistency: type, spacing, colour, alignment, wording, every screen size and state |

---

## 1. Priya Raman: "I have a plan and ten minutes"
**Who.** 34, Staff PM (L6) on a payments platform at a large US tech company, on an H-1B that runs out in 18 months.
Wants Toronto or Waterloo, staff level, CA$200k+ base, platform or fintech or AI. Has a strong resume.

**Mindset.** Efficient, sceptical of job boards, hates scrolling past junk. She'll open Lodestone every morning with
coffee and wants to be done in ten minutes. Trusts a number only if she can see why.

**Goals.** Spend her time only on roles that can actually hire her; never miss a great new one; keep her pipeline tidy.

**Tasks (journey)**
1. Morning triage: open the app, see today's list, triage the clear ones fast, skip the maybes.
2. **"I've seen enough of these, show me more"** before finishing all 10 (the question Ayush raised).
3. Open a strong role: read why it's ranked where it is, read the job description, check pay against the market.
4. Mark it Interested, follow the next step (request a market check, add a note), move it to Applied in the pipeline.
5. Tell Lodestone "more like this" on a role she loves, and see the effect.
6. Come back after finishing: what does "All caught up" offer?

**Delight looks like.** Ten minutes, every decision taken with the facts on one screen, nothing she's already seen.
**Frustration looks like.** Being forced through roles she doesn't care about; numbers without reasons; lost place.

## 2. Daniel Okafor: "Where do I even start?"
**Who.** 29, product marketing manager at a Lagos fintech, moving to Calgary in 6 weeks on an open work permit through
his wife's study permit. Wants to move into product management or stay in product marketing. No Canadian-format resume yet.

**Mindset.** Hopeful and anxious. Doesn't know the Canadian market, the levels, or the pay. Afraid of being judged
by a half-finished resume. Will leave if the first screen asks for too much.

**Goals.** Understand what roles fit him and who will hire someone new to Canada; get started without a resume.

**Tasks**
1. First visit with an empty profile: does the app explain itself, and does it show useful roles straight away?
2. Tell it he has an open work permit and wants Calgary; does the list react?
3. Find PM-adjacent roles (product marketing, program) and understand the role-type labels.
4. Paste a job link he found on LinkedIn.
5. Find out how to add his background without a finished resume.

**Delight.** Useful roles in under a minute, plain explanations, no jargon, "a rough draft is fine".
**Frustration.** Empty screens, Toronto-only defaults, Canadian jargon (LMIA, L5) with no explanation, being told to upload first.

## 3. Mei Chen: "Just show me the market"
**Who.** 38, AI product lead at a Montreal startup, Canadian permanent resident. Not job hunting yet; wants to know
who's hiring for AI PMs, at what pay, and which companies are worth watching.

**Mindset.** Curious, data-minded, no urgency. Mildly irritated by anything about visas, which don't apply to her.

**Goals.** Compare pay; follow a few companies; see the market across Canada, not just one city.

**Tasks**
1. Browse all roles across Canada sorted by pay; compare base vs total pay labels.
2. Search for "AI" and open a company's other roles.
3. Explore the Companies page and the daily report.
4. Tell the app she doesn't need a work permit, and see the permit layer step aside.

**Delight.** Clear, comparable pay; the company view; no immigration noise.
**Frustration.** Every card shouting about sponsorship; no way to say "I'm a PR"; a Today list built for urgent triage.

## 4. Tomás Herrera: "Five minutes on the bus"
**Who.** 31, Technical Program Manager at a Mexico City e-commerce company. Wants Toronto, Vancouver or remote in Canada.
Half-finished resume. Uses only his phone, a few times a week.

**Mindset.** Busy, decisive, impatient with small buttons. Says no a lot and wants the app to learn from it.

**Goals.** Clear a short list quickly on his phone; stop seeing roles that pay too little or at companies he dislikes.

**Tasks**
1. Open on the phone after four days away: what's waiting, and what came back from Later?
2. Triage with thumbs; say why not ("Pay too low", "Company").
3. Accept a suggestion the app makes from his reasons; then undo it.
4. Run out of today's list; get more without hunting for it.

**Delight.** Big targets, one-hand use, the app visibly learning from his "no"s.
**Frustration.** Tiny chips, long scrolls, reasons hidden after the card disappears, losing his place.

## 5. Aisha Rahman: "Let me do this my way, and keep my data mine"
**Who.** 41, Principal PM in London moving to Toronto with her family. Low vision; uses the keyboard and a screen reader.
Privacy-minded after a data breach at a previous employer.

**Mindset.** Methodical. Expects standard keyboard behaviour and clear labels. Reads privacy text.

**Goals.** Triage entirely by keyboard; understand and control what the app learns; delete her reading history.

**Tasks**
1. Triage with J/K and I/L/N; open a role with Enter; move between tabs with the arrow keys; close with Escape.
2. Check that buttons and tabs have names a screen reader can say, and that focus is visible and returns sensibly.
3. Turn off "learn from what I read", then delete her reading data.
4. See what the app has learned about her and undo something.

**Delight.** Everything reachable by keyboard; honest, plain privacy controls.
**Frustration.** Focus lost after an action, unlabelled icons, controls that only work with a mouse.

---

## 7. Lena Vogel: "If the details are sloppy, why trust the data?"
**Who.** 36, Group PM at a Berlin design-tools company; spent five years as a product designer before moving into
product. Moving to Vancouver with her partner; needs sponsorship. Uses a 27-inch monitor at work, a laptop at home and
her phone in between, and switches between light and dark mode with the time of day.

**Mindset.** Notices everything: a button 2px off, two greys that almost match, "CA$200k" next to "CA$148K", a heading
in Title Case beside one in sentence case. To her, polish is a proxy for care: if the interface is sloppy, she assumes the
scores are too. She likes calm, minimal, professional screens with few colours, one type scale and generous space.
Decoration that carries no meaning (extra borders, badges, emoji, three kinds of tag on one card) annoys her.

**Goals.** A tool she'd be proud to show a design-minded hiring manager; screens she can scan in seconds.

**Tasks (journey)**
1. **Card audit.** Look at ten cards on Today: is there one clear hierarchy (title, company, then everything else)? How
   many tag styles, colours and font sizes does one card use? Does anything wrap awkwardly, truncate mid-word, or
   misalign between cards?
2. **Every screen, every size.** Visit Today, All to triage, the role view (all three tabs), Pipeline, Add job, Reports,
   Companies and Profile at 1440, 1024, 768, 390 and 320px wide, in light and dark mode. Look for horizontal scroll,
   cramped or uneven spacing, text running into edges, and colours that lose contrast in dark mode.
3. **States.** Loading, empty (no jobs, nothing matches, all caught up, empty pipeline, no reports), error and
   offline states: are they designed, or just leftover text?
4. **Wording and numbers.** One way to write money (CA$148K, not also CA$200k or $148,000), dates ("7d ago" vs "7 days
   ago"), sentence case for every heading and button, consistent punctuation (one separator, no doubled spaces), no
   jargon or internal names on screen.
5. **Interaction polish.** Hover, pressed and focus states on every button; no layout jump when a toast, banner or
   reason row appears; smooth (or no) motion; nothing that looks clickable but isn't, and the reverse.

**Delight.** Calm, consistent screens where the eye goes straight to what matters; dark mode as good as light.
**Frustration.** Visual noise, mixed styles, inconsistent numbers and capitals, anything that looks unfinished.

**Planned automated checks** (to build in `tests/personas/7_lena.cjs`; screenshots reviewed by eye as well):
- Distinct font sizes on screen ≤ 6, font weights ≤ 3, font families ≤ 3 (body, display, mono).
- Distinct text and background colours per screen within the design tokens (no stray hard-coded colours).
- Spacing values (margins, padding, gaps) come from one scale (4/6/8/10/12/14/16/20/24…); flag outliers.
- No horizontal scroll and no element wider than the viewport at 320, 390, 768, 1024 and 1440px, in both themes.
- Text contrast ≥ 4.5:1 (3:1 for large text) in light and dark mode.
- Tags per card ≤ 8, tag styles per card ≤ 4; card heights within a sane range; titles not truncated mid-word.
- Money, dates and counts match one format each (regex audit of all visible text); headings and buttons in sentence case;
  no doubled spaces, stray separators, or text like "undefined", "null", "NaN".
- No layout shift (cumulative movement of the list) when a toast, banner, reason row or "done" state appears.
- Every interactive element has visible hover and focus styles; nothing with a pointer cursor lacks an action.

## Running the journeys
`node scripts/persona_test.cjs [persona …]` (needs `data/state/app_export/`, made by `python3 -m lodestone export`).
Screenshots and `results.json` go to `data/state/persona_runs/` (not committed). Each journey is a file in
`tests/personas/` with the persona's starting data (`seed`) and tasks (`run`). Checks are things that must be true;
notes are what Claude saw while playing the persona: *works*, *annoyance*, *bug* or *idea*.

## Findings log
Newest first. Each finding names the persona, what happened, and what changed.

### Round 1 (2026-10-16): 5 personas, 57 checks; 19 failed at first, all 57 pass after fixes (app v25)
| # | Persona | What happened | Fix |
|---|---|---|---|
| 1 | Priya, Tomás | **Today made you finish all 10 before you could see more.** "Show 10 more" only appeared once the list was empty | "Show 10 more" and "See all N roles to triage" sit under the list at all times |
| 2 | Priya, Tomás | **A role vanished the moment you answered it**, taking the "Why not?" reasons with it, and a misclick couldn't be undone | Answered roles stay in place (dimmed, with what you chose and "tap again to undo") until you leave the tab; reasons stay open |
| 3 | Priya | When the last role was answered, the dimmed cards hid "All caught up" | "All caught up" shows as soon as nothing is left to answer |
| 4 | Daniel | **No welcome.** A first-timer landed on a ranked list built from someone else's defaults | A welcome card says what Lodestone is, the three steps, and offers "Set up my profile" or "Just browse"; it goes away once the profile is saved or dismissed |
| 5 | Daniel | **Changing the Profile didn't change today's list** (Calgary set, Toronto roles still shown) | Saving the Profile, or accepting a suggestion that changes cities, role types or hidden companies, re-picks the unanswered part of today's list; answered roles stay |
| 6 | Daniel | "My regions" mixed in the rest of Canada at the same rank as his own city | Today picks from your own cities first, then the rest of Canada if you allow it |
| 7 | Daniel | "L5", "L6" on cards weren't explained | The colour legend explains levels |
| 8 | Daniel | Profile said only "No resume uploaded yet" | It says a rough draft, a few lines, or nothing at all is fine to start |
| 9 | Mei | **No way to say "I'm a citizen or permanent resident"** | New work-permit choice; the permit check, the permit table and the company "Work permit" line step aside. Open-permit holders also lose the redundant permit tag (a posting limited to citizens still shows red) |
| 10 | Mei | Cohere's "About" ran on into the job posting ("ROLE OVERVIEW We are seeking…") | Headings written in capitals are recognised (not pay ranges or tags); reading check still 100% |
| 11 | Tomás | **On a phone, no role was visible on opening**: report, suggestion, counts, two rows of tabs and the legend filled the screen | Report banner is one line on phones; the counts moved onto the tabs; tabs are one swipeable row |
| 12 | Tomás | Triage buttons 36px and reason chips 30px tall: hard to hit with a thumb | 44px and 40px on touch screens |
| 13 | All | The header said "545 to triage", the Digest badge 502 | Both count roles that fit your Profile |
| 14 | Aisha | **Focus was lost after every live update**, so keyboard users fell back to the top of the page | Focus is put back after the whole page, including the role panel, redraws |
| 15 | Aisha | Cards couldn't be reached with Tab; Enter didn't move focus into the role; Escape didn't return to the card | Cards are focusable with a name ("title at company, marked …"); opening focuses the role title; closing returns to the card; I/L/N moves to the next role |

**What already worked well.** The why-ranked line, next steps after Interested, the market-check request, the pipeline,
"More like this", the inbox, the learning controls and deleting reading data all did what each persona expected.

**Left for later (not yet fixed).**
- Fit scores in a new person's copy are blank until the first scoring run. A new user sees a list ranked by role type and
  region only for their first few hours. P1-S7 onboarding should say so.
- The daily report banner speaks to the owner's runs. A brand-new user doesn't need it on day one.
- Mei would like a market view (pay by level and company) rather than a triage list. That's a V1 idea; logged.
