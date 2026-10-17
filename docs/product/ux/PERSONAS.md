# Lodestone test personas and journeys (D-072)

> Owner: Product (UX) · Started 2026-10-16 · A living document: **every new feature adds a task to at least one persona,
> and new kinds of user add a persona.** The journeys run automatically (`node scripts/persona_test.cjs`) against the real
> app with an in-memory copy of its database; each run saves screenshots and a results file that Claude reviews by eye.
> All five people are fictional composites. None is a real user, and none carries real personal data.

## Why these five (now ten)
Each persona stresses a different part of the product promise ("the jobs that fit you, in the country you want, that
will actually hire you", D-066), and a different way of using the app:

| | Persona | Situation | Work permit | Resume | How they use it | Stresses |
|---|---|---|---|---|---|---|
| 1 | **Priya**, Staff PM, Seattle → Toronto | Urgent, methodical | Needs sponsorship | Ready | Desktop + iPad, daily, 10 minutes | Today list, triage speed, pipeline, pay, "why ranked" |
| 2 | **Daniel**, product marketer, arriving in Calgary | New, anxious, unsure what fits | Open work permit (spouse) | None yet | Laptop, first visit | First-time experience, empty profile, a non-PM field (product marketing), paste a job |
| 3 | **Mei**, AI PM, permanent resident in Montreal | Not urgent, exploring the market | Doesn't need one | Ready | Desktop, weekly, browses | Companies, pay comparison, search, the work-permit layer for someone who doesn't need it |
| 4 | **Tomás**, TPM, Mexico City | Busy, sporadic | Needs sponsorship | Half-done | Phone only, a few minutes on the bus | Mobile layout, Later, "Not for me" reasons, one-tap suggestions, catching up after days away, a program manager's own field |
| 5 | **Aisha**, Principal PM, London → Toronto | Careful, privacy-minded | Needs sponsorship | Ready | Keyboard only, screen reader | Keyboard flow, focus, labels, learning controls, deleting her data |
| 6 | **Sam**, product manager, curious but wary | Not ready to commit; skips every question | Unknown | None | Phone, a few minutes | Skipping: does everything still work with no answers, and can setup be done later? |
| 7 | **Lena**, Group PM with a design background, Berlin → Vancouver | Discerning, judges a product by its polish | Needs sponsorship | Ready | Large desktop monitor, laptop, phone; light and dark mode | Visual consistency: type, spacing, colour, alignment, wording, every screen size and state |
| 10 | **Ravi**, senior PM, long-time user | Settled, uses it daily | Needs sponsorship | Read from resume | Laptop | Older settings carried forward: re-running setup, taste test, roles on the Profile, a broken Today list |
| 9 | **Kai**, IT project manager, Halifax | Curious, shares little at first | Not said | None | Laptop, a few minutes | Role-first setup, ranking on role type only, gentle nudges, the meter |
| 8 | **Omar**, senior business analyst, Toronto | Moving from banking to tech; wary of "PM tools" | Permanent resident | None in the app | Laptop, evenings, first visit | A field other than product management: setup in his words, role tags, pay targets, choosing related fields |

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
5. (D-075) Jump to a Profile section with the chips at the top, change one setting, save from the bar that stays in view.
6. (D-076) See his own roles as "Program", his field, not "PM-adjacent"; filter the full list to program roles.

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

## 6. Sam Park: "Let me look around first"
**Who.** 27, product manager at a Seoul gaming studio, idly curious about Canada. Hasn't decided to move, doesn't
want to explain himself to an app, and taps "Skip" on anything that looks like a form.

**Mindset.** Wary of questions and sign-up walls. Will give the app about a minute; if it shows him real jobs, he'll come
back and maybe tell it more later.

**Goals.** See what's out there with zero effort; set things up later only if it seems worth it.

**Tasks (journey)**
1. Skip setup on the first screen; does he still get a real list straight away, and does it say what it's based on?
2. Come back later (reload): setup must not ask again.
3. Find where to do setup later, run it, and skip every question including the taste test.
4. Everything works on a phone, with no sideways scrolling.

**Delight.** Real roles in seconds with no questions; the option to say more, later, without pressure.
**Frustration.** Being forced through questions; nagging; an empty or broken list when he hasn't said anything.

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

## 8. Omar Haddad: "I'm not a product manager. Is this for me?"
**Who.** 38, Senior Business Analyst at a Toronto bank for nine years (requirements, process redesign, payments
projects). Permanent resident. Wants to move into a tech company or fintech as a senior BA, or a business systems or
data-leaning analyst role. Laptop, evenings. Added 10-16 for D-076, when Ayush asked how a non-PM sees Lodestone.

**Mindset.** Wary of tools "for product people". If the first screen talks PM, he leaves. Precise; reads labels.

**Goals.** A list of BA roles in Toronto, at pay a BA actually earns; nearby roles (analytics, project) only if he asks.

**Tasks**
1. Set up in his own words ("senior business analyst, banking and payments") without hunting for the right card.
2. Taste test: BA and nearby roles, not product managers.
3. First list: his field first, tagged in his words, never "PM"; normal BA pay not marked red.
4. Read the legend: what the tags mean, for him.
5. In the Profile, stop seeing analytics roles; the full list and its role-type filter follow.

**Delight.** "Got it: Business analysis" as he types; every tag in his language; pay that looks right.
**Frustration.** "PM-adjacent", "Core PM", a list of product manager jobs, red pay on every ordinary BA role.

## 9. Kai Tremblay: "Just show me something"
**Who.** 34, IT project manager in Halifax at a regional insurer, curious about tech roles anywhere in Canada. Not ready
to share much. Laptop, a few minutes at lunch. Added 10-17 for D-077 (role-first setup).

**Mindset.** Will answer one question, not five. Will share more if the app proves useful first.

**Tasks**
1. Pick a role type and see jobs immediately, with nothing else asked.
2. Understand what the list is based on.
3. Get at most one gentle nudge a day; say "Not now" and not see it again today.
4. Next day, answer where and work status from the nudge; see the meter move.

**Delight.** A real list after one tap; nudges that ask for one thing at a time.
**Frustration.** Forms before value; red warnings about things never asked; nagging.

## 10. Ravi Menon: "I've been using this for weeks"
**Who.** 37, senior PM, a long-time user set up before role types existed (no field saved, older settings, roles
read from his resume, his own pay targets, "rest of Canada" off). Laptop. Added 10-17 after Ayush hit three bugs in
exactly this state. Fictional; mirrors the owner's real state without his data.

**Tasks**
1. Open the app on a day whose saved Today list came out empty: it should repair itself.
2. See and edit his past roles, education and years on the Profile.
3. Run setup again: his field, cities and work status are pre-selected; nothing he set is reset.
4. Take the taste test: mostly his field, nothing he already answered; his list is full afterwards and after a reload.

## Monkey and resilience tests
`tests/personas/11_monkey.cjs`: 300 seeded random taps on every safe button, from three starting points (long-time
user, brand-new user, phone), checking after every tap that there is no script error, the page isn't blank and Today
isn't empty while roles match. After every persona's journey, the runner also checks invariants: no script errors,
Today never empty while matching roles exist, every role in Today exists, saved role types are known, every visible
role has a relevance score.

## Running the journeys
`node scripts/persona_test.cjs [persona …]` (needs `data/state/app_export/`, made by `python3 -m lodestone export`).
Screenshots and `results.json` go to `data/state/persona_runs/` (not committed). Each journey is a file in
`tests/personas/` with the persona's starting data (`seed`) and tasks (`run`). Checks are things that must be true;
notes are what Claude saw while playing the persona: *works*, *annoyance*, *bug* or *idea*.

## Findings log
Newest first. Each finding names the persona, what happened, and what changed.

### Round 7 (2026-10-17): the "no jobs" outage; 12 journeys, 336 checks, all pass (app v34)
Postmortem: `docs/eng/postmortems/2026-10-17-no-jobs-displayed.md`. The harness now freezes everything the imitation
database delivers, like the real one, and reproduced the outage before the fix.
- **Everyone: no roles at all** (the app wrote onto frozen database objects). Fixed: the app works on its own copies;
  roles without a relevance score are shown, not hidden; a screen that fails shows "Something went wrong" with a way out.
- **New persona "resilience"** breaks things on purpose (relevance failing for every role, a crashing screen) and checks
  the safety nets and the health note.
- **Monkey test speed check found:** "Skip and browse" took 4.7 s (a company lookup scanned the whole list per role;
  now 1.5 s including the test's own wait), and a tap on a covered button counted as slow (test fixed).
- **Aisha: the page jumped back up whenever it redrew** (restoring focus scrolled to the focused heading). Fixed.
- **Every journey now ends with invariant checks:** no script errors, roles visible, Today not empty while roles match,
  every Today role exists, a health note saved.

### Round 6 (2026-10-17): Ayush's three bugs; 10 personas + monkey test, 274 checks, all pass (app v33)
Ayush ran setup again from his Profile and took the taste test. Replayed with a local copy of his real settings (never
committed), then built persona Ravi from the same state.
- **Taste test showed mostly non-PM roles.** His Profile never stored a field (PM was assumed), so setup and the taste
  test saw "no field" and showed the newest roles of every kind. Fixed: existing users' field is pre-selected and saved
  explicitly; the taste test shows 6 roles from your field and 2 related ones, nothing you already answered, nearby
  first, not company types you avoid, best fit first.
- **Digest empty after the taste test.** Today was saved with no roles, so the app said "You've reviewed your top
  matches" when he hadn't. Fixed: an empty or stale Today rebuilds itself; never written empty while roles match.
  The exact moment it was saved empty couldn't be reproduced; the repair and the new invariant checks cover it.
- **"Why don't I see any roles on my profile?"** His 7 past roles (and education, years) were stored but never shown.
  Fixed: "Your roles" on the Profile, editable (add, remove, edit; the rest of each role kept).
- **Found while fixing:** running setup again reset custom pay targets to the field's defaults and turned on "rest of
  Canada". Fixed: same field keeps your pay targets and the other types you see; cities chosen keep your setting.
- **Proof the tests would have caught it:** Ravi's journey against the previous version fails 4 of its first 5 checks.

### Round 5 (2026-10-17): type scores and role-first setup; 9 personas, 201 checks, all pass (app v32)
New: persona Kai (one answer, then nudges). Daniel and Omar now answer the role first and take the taste test from the
first-list banner; Sam skips each question of the new 3-step setup; Tomás sees hybrid jobs ("Program · also Product")
and jobs titled otherwise but with real program work; Priya (whose Profile says she'd avoid traditional banks) accepts
the one-tap suggestion and bank roles move down. Lena audits the new role step.
- **Kai: a red "No sponsorship" tag before being asked about work status.** Fixed: status "not set" keeps work-permit
  tags as information only.
- **Kai (phone): "Show my jobs" sat below ten role cards.** Fixed: setup buttons stay pinned above the tab bar.
- **Kai: ordinary project-manager pay showed red.** Lowered the project family's default pay targets (CA$115K/90K).
- **Tomás: filtering to Program showed a card tagged only "Strategy & ops".** Fixed: a second type is shown from 50,
  the same threshold the filter uses.
- **Priya: accepting the bank suggestion rebuilt Today mid-session.** Fixed: re-ranking preferences don't reshuffle
  today's list; only ones that hide roles do.
- **Readers' notes on type scores (400 roles):** 10 postings had no usable description (EvenUp, Kinaxis, Shopify,
  Certn, Lululemon) and were scored from the title, marked so; several "Product Manager" titles were really threat
  research, pricing analysis, service operations or customer solution design, and now rank by that work.

### Round 4 (2026-10-16): Profile navigation, role types for any field; 8 personas, 169 checks, all pass (app v30)
New tasks: Aisha uses the Profile side menu by keyboard; Tomás jumps with the phone chips and saves from the sticky bar,
and now sees Lodestone as a program manager; Priya checks her old settings carry over; Daniel's field is product
marketing; new persona Omar (business analyst) sets up in his own words. Lena audits the new Profile screens.
- **Tomás, Daniel, Omar: "PM-adjacent" on their own field (the reason for D-076).** Fixed: tags name the job's family,
  highlighted when it's yours; nothing says "PM" to someone who isn't one (checked on Omar's whole list).
- **Omar: his roles weren't collected, and typing "business analyst" said it wasn't covered.** Fixed: three new families
  collected; typed words light up the matching card ("Got it: Business analysis").
- **Omar: every ordinary BA salary was red** (a senior PM's pay targets). Fixed: setup sets pay targets for the field.
- **Tomás: his list led with product roles** because existing scores were made for a product manager. Fixed: when the
  scored field differs, the role factor comes from closeness to his field and his field ranks first until re-scored.
- **Omar: the daily report banner talked about a Staff PM role.** Fixed: reports written for another field don't show
  as a banner; the Reports page says who they were written for.
- **Daniel: tapping cards after typing toggled them off.** Fixed in the flow: typed words pre-select cards; tapping adds
  or removes from that set.
- **Sam (found by timing): a 3-second freeze after "Skip and browse"** from re-checking families on every role. Fixed
  with a cheap cache; back to 1.4 s in the test harness.
- **Lena: role chips with notes ran off a 320px screen.** Fixed: family chips wrap.
- **Aisha: a section id clashed with a form field id** ("pf-work"), breaking the work-permit select. Fixed (sections are
  `ps-*`).
- **Omar: "e.g. L5, Senior PM" placeholder.** Now "e.g. Senior, or L5". "What you do" moved above "Where".
- **Idea (not built):** reports per person once there is more than one user; level wording beyond Google's L-scale for
  non-tech ladders.

### Round 3 (2026-10-16): Lena's design pass; 7 personas, 112 checks, all pass (app v27)
Lena's journey audits 13 screens (Today, All to triage, the role view's three tabs, Pipeline, Add job, Reports,
Companies, Profile, setup, the "not sure" step, an empty search) at 1440, 1024, 768, 390 and 320px, in light and dark
mode: 130 screen states, 52 screenshots reviewed by eye. 7 of 17 checks failed at first.
| # | What Lena saw | Fix |
|---|---|---|
| 1 | **13 font sizes** (9 to 28px, including a stray 12.5px) and 5 weights | One scale: 11, 12, 13, 15, 16, 18, 22, 26px; weights 400, 600, 700 |
| 2 | **Noisy cards**: six tag styles over up to three rows (role, checks, years, a bold monospace source chip, outlined "+ equity" pills, orange flags) | One row of tags; the source is a quiet link in the company line; pay notes are plain grey text; at most one flag; "New" is a quiet accent tag |
| 3 | Green and yellow tag text slightly under readable contrast (4.4 and 4.2 to 1); the grey "Unknown" tag 4.1 | Darker text colours; all text now passes in light and dark |
| 4 | "$181K" with no currency | Unknown currency says so: "181K–241K (currency not stated)"; never a bare $ |
| 5 | The next card jumped down when you answered one | The "Later: back in 7 days" note replaces the one-line summary instead of adding a line |
| 6 | Panel headings in small capitals, some of them full sentences ("MATCH QUALITY: LEVEL 2 OF 4") | Sentence case, one heading style |
| 7 | "Open posting" button underlined, unlike every other button | Buttons are never underlined |
| 8 | Selected filters were a glaring white pill in dark mode | Selected filters use the accent colour in both themes |
| 9 | The Pipeline cut its last column ("Closed") off the screen | All six stages fit on a laptop screen; phones scroll sideways |
| 10 | "Careers ↗" broke over two lines in the Companies table | Kept on one line |
| 11 | Spacing values off the scale (7, 9, 15, 22px) | On the scale |
| 12 | The "FIT" caption touched the score; "Upload" bold beside regular buttons; two reassurance lines far apart | Aligned, matched, merged |

**Left for later.** Role-type filters read heavy when all three are on (three solid pills); consider showing them only
when one is off. Long titles wrap to three lines on phones; fine, but worth a look with real users.

### Round 2 (2026-10-16): P1-S7 onboarding; 6 personas, 95 checks, all pass (app v26)
| # | Persona | What happened | Fix |
|---|---|---|---|
| 1 | Daniel | The taste test showed only 3 roles: few roles of his types in Calgary | Taste test tops up from remote-in-Canada roles, then the rest of Canada, one role per company, mixed role types |
| 2 | Daniel | His Today list had only 4 roles: picking Calgary left out remote-in-Canada roles he could take | Setup always includes "Remote in Canada" with any city, and says so |
| 3 | Daniel | "LODESTONE" above the promise repeated the logo beside it | It says "Welcome" |
| 4 | Daniel | "Delete my experience" was a bold accent link right under the three options | A quiet grey link |
| 5 | Daniel | The Upload button was smaller than Paste text and Start | Same size |
| 6 | Sam | (checks) Skip on the first screen, reload, skip every question, phone layout | All worked first time |
| 7 | Priya, Aisha | (checks) Existing users never see setup | Worked: setup only shows with no profile and no history |

**Left for later.** The city question (shortlisting a role outside your cities) wasn't exercised by Daniel, because all
his roles were in Calgary or remote; give a persona a mixed list next round. One-tap "count internal transfers?" isn't
needed: transfers count automatically once the current employer is in the Profile.

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
