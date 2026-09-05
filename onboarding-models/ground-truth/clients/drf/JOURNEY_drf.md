# JOURNEY — Dorell Fabrics (`drf`, org 290)

**Built blind** from `CORPUS_drf.md` (read start to finish, all 5,660 lines, no skimming),
`RAWSTATE_drf.json`, and direct read-only queries against `supercat-postgres-vpn`.

**Forbidden-file confirmation:** I did not open `CLIENT_PROFILE.md`, `HANDOFF.md`,
`REGISTRY.yaml`, `Phase_Anchors.md`, `Phase_Progression_Framework.md`,
`Flags_and_Signals.md`, `Output_Contract.md`, `RUN_PROMPT.md`, `SCORECARD.md`, or any
`ecat-*` skill. The workspace `CLAUDE.md` was auto-injected into context by the harness
(not opened by me); it contains eCat file-format reference, not phase definitions or any
Dorell-specific interpretation.

---

## What actually happened

Loomcraft Textiles, doing business as Dorell Fabrics, is a mature fabric wholesaler on an
AS/400 ERP (Vantage Point) selling to furniture manufacturers — Lazy Boy, Crate & Barrel —
where 95% of revenue arrives as POs and EDI, 70% of it FOB China. They did not buy a sales
system. They bought a replacement for one piece of paper: the three-part NCR checkoff sheet
a buyer marks up at Showtime to request fabric samples. Suzanne Fukunaga named the scope
herself on the kickoff call — "I'm going to call it Phase 1" — and never let it drift.

Jon Vanderberg ran a four-month sales cycle from February. Kylor Johnson joined on
2026-04-13, the org was provisioned on 2026-04-15, and the first products and customers
landed on 2026-04-27, five weeks after Suzanne had named a hard deadline: Showtime,
May 19–21.

They missed it. Not because anyone stalled, but because the data question was never
actually settled before the build started. Dorell's catalog is a pattern × colorway ×
sample-type cube, and three different files described three different slices of it. By
2026-05-06 Kylor was merging five source files including a 30,000-SKU characteristics dump
against roughly 130 images, and colorways were disappearing from the iPad. Suzanne's fix
was to throw it all out — "can you just delete everything and just bring a new thing?" —
and the rebuild ran through late May and June.

Then the record diverges from the database, and the database is right. On the 2026-05-18
call Dorell said they had missed the show. The login table says otherwise: 25 sign-ins on
May 19 and 10 on May 20, and the first order in the system — the only one ever billed to a
real customer account, AMALFI — was submitted the evening of May 18. They used it at
Showtime anyway, partially, off a catalog nobody had signed off on.

After the show the forcing function was gone and correspondence went quiet for six weeks.
Christine Soh reopened it on 2026-06-30 with "Sorry for the silence" and a request that
changed the project's character: ten price levels. She created all ten in the Admin Console
herself on July 2 and uploaded the columns without help. Because the iPad shows one price
level at a time and Dorell's reps negotiate across FOB and warehouse simultaneously, Kylor
solved it by rendering all ten prices as static text inside the product story — a
workaround, and the one Dorell is running on today. Onboarding was declared complete on
2026-07-20 and handed to Kyla Bosch, who trained Christine and Suzanne on July 21.

Today the client is more active than at any point since Showtime. On 2026-08-18 four Dorell
people signed in, Christine invited a fifth person and a sixth was provisioned, and three
sample orders went through carrying hand-typed negotiated prices — "FOB Price 4.75",
"Send half yard cut price $2.20" — which is precisely the paper workflow they set out to
replace. The catalog has not been re-imported since July 8, and for this client that is
seasonal, not decay. What is genuinely unfinished is smaller and quieter: submitted orders
still route to Suzanne's personal inbox rather than customer service, every customer still
resolves to a $1.00 placeholder price level, and no field sales rep has ever been given an
account.

---

## A. Cast

### SuperCat Solutions

| Person | Role | First appearance | Last appearance | Notes |
|---|---|---|---|---|
| Jon Vanderberg (`jon@supercatsolutions.com`) | AE / sales | 2026-02-03 Discovery Call | 2026-05-18 call (attendee); still referenced 2026-07-20 | Owned Feb–Apr. Last iPad login 2026-06-10. Named as future rep-training owner but never appears again in writing. |
| **Kylor Johnson** (`kylor@supercatsolutions.com`) | Onboarding / data readiness | 2026-04-13 call | 2026-08-12 (ticket #15031) | **Authorship shifts to Kylor 2026-04-27** (ticket #14401: "Moving this thread to our onboarding inbox"). Sole SuperCat voice 04-27 → 07-17. Out of office 06-18 → ~06-23 (wedding). |
| **Kyla Bosch** (`kyla@supercatsolutions.com`) | Onboarding & Implementation Manager / Head of Support | named 2026-06-18; active 2026-07-20 | 2026-07-29 | **Authorship shifts to Kyla 2026-07-20.** Ran admin training 07-21. Silent after 07-29. |
| Brent | CTO | 2026-06-18 (named only) | — | Never appears in any thread or call. |

**Authorship changes:** Jon → Kylor on **2026-04-27**; Kylor → Kyla on **2026-07-20**. The
second handoff did not hold — the 2026-08-11 support ticket was answered by Kylor, not Kyla.

### Dorell Fabrics / Loomcraft

| Person | Role | First | Last | System state |
|---|---|---|---|---|
| **Suzanne Theodore Fukunaga** (`Suzanne@dorellfabrics.com`) | Project Manager — the driver | 2026-02-03 (joined mid-call) | 2026-08-18 | org_user 04-27; admin; **last iPad login 2026-08-18 18:24**; submitted **all 10** orders |
| **Christine Soh** (`Christine.Soh@dorellfabrics.com`) | Director of Operations & I.T. — the operator | 2026-02-03 | 2026-08-18 | org_user 05-01; admin; last iPad login 2026-08-18 16:38; created all 10 price levels herself |
| **Brian Frankel** (`brian@loomcraft.com`, also `brian@dorellfabrics.com`) | CEO | 2026-02-03 | 2026-05-18 call | org_user 05-03; **never logged into the iPad** |
| David Lok (`DavidL@dorellfabrics.com`) | IT | 2026-05-11 | 2026-05-11 | SharePoint permissions only; no account |
| Gina Garza | Product Development | 2026-05-05 (named) | 2026-08-18 | org_user 06-30; logged in 06-30 and 08-18 |
| Heather Steczko | Product Development | 2026-07-02 | 2026-08-18 | org_user 07-02; logged in 07-06 and 08-18 |
| Kate Gothreau (`kate@dorellfabrics.com`) | Product Development | 2026-05-06 (named as "Kate") | 2026-07-01 | **Logged in twice on 2026-07-01 (iPad6,3, DefaultUserGroup) — org_user no longer exists** |
| Claudia Frankel | PD / showroom lead | 2026-05-05 (named) | 2026-08-18 | Invite 05-19 expired unredeemed; **org_user created 2026-08-18 16:50**; never logged in |
| Rachel Jenkins | — | 2026-06-30 | 2026-07-07 | Invited 06-30, expired 07-07, never redeemed, no account |
| Dana Gomez | — | 2026-08-18 | 2026-08-18 | **Invited 2026-08-18 17:00 by Christine Soh**; pending, expires 08-25 |
| Chip (Stroup), Andy, Danny | Field sales reps | 2026-04-27 (territory codes) | 2026-07-29 (named in Kyla's action list) | **Never provisioned. No account, no invite, no login.** |

---

## B. Phase transitions

### Pre-phase · 2026-02-03 → 2026-04-13 · confidence: high

**What changed:** Nothing in the product. This is a 10-week sales cycle that precedes
onboarding entirely, and it explains the corpus/provisioning gap the brief flagged.

**Evidence:**
- [CALL, 2026-02-03T17:30Z, Discovery Call] Jon Vanderberg presents; Brian Frankel attends from `loomcraft.com`. Brian on the relationship between the two companies:
  > "Loomcraft's just a parent company."
- [CALL, 2026-02-03] Initial commercial terms quoted:
  > "there's a one-time setup fee.    It's $4,500.    That is for us to onboard you and basically hold your hand from start of the implementation to going live.    And then from there, it is $8,700 annually for the application, which includes 25 licenses."
- [CALL, 2026-03-19T18:00Z] Pricing is re-presented as a tier model; Dorell is placed in Tier 1.
- [DB] `organizations.created_at` = 2026-04-15T13:51:34 — the org does not exist during any of this.

**Against:** None. No import, no org, no user, no data file exists before 2026-04-15.

---

### → Phase 1 (Discovery / Kickoff) · **2026-04-13** · confidence: high

**What changed:** Kylor Johnson joins, scope is fixed to sample capture at Showtime, the
deadline is stated, and both sides name the call a kickoff.

**Evidence:**
- [CALL, 2026-04-13T20:00Z, "Dorell path forward alignment", attendees Suzanne, Christine, Kylor] Kylor:
  > "So, yeah, so to Jon's point, I guess we can kind of call this like the, you know, kickoff call of, you know, really starting to implement your data."
- [CALL, 2026-04-13T20:00Z] Suzanne fixes scope:
  > "And I'm going to call it Phase 1 because we are just going to look at it as a tool when we go to showtime.    So there'll be limited information that we're going to first share with you because we only want to show our new products.    And it's not, it's not anything where our customers will be able to purchase as much as sampling."
- [CALL, 2026-04-13T20:00Z] Suzanne on the deadline: "It's on the end of May."
- [CALL, 2026-04-13T20:00Z] Suzanne on scale: "The thing about our company, we only have really three reps."
- [DB] Org `drf` (id 290) created 2026-04-15T13:51:34; user group `Dorell Internal` created the same second (2026-04-15T13:51:34.595917).

**Against:** The org is provisioned two days *after* the kickoff, not before it, so if
provisioning is the anchor the date is 2026-04-15. The 2026-04-15 "Data Files" call is
better read as a file-handover working session — Jon on that call still describes kickoff
as ahead: "And then we can start looking at having a kickoff meeting."

---

### Phase 1 → 2 (Initial Import) · **2026-04-27** · confidence: high

**What changed:** First products and first customers imported. The catalog exists.

**Evidence:**
- [HS #14401, 2026-04-27T20:29:08Z, kylor@supercatsolutions.com (SuperCat)]
  > "Quick recap: we've completed the initial product file (80 SKUs across 8 Collections) and customer file (389 records) imports for your eCat platform. The product upload is intentionally a subset — I only imported the patterns we had photos for."
- [DB] `import_history`: 2026-04-27 Products (warning ×3); 2026-04-27 Customers (error ×1, warning ×1).
- [DB] `customers`: 389 rows, all `created_at` 2026-04-27T18:59:11–18:59:15.
- [DB] `price_levels`: `net` created 2026-04-27T18:49:36 — the only level for the next 66 days.
- [DB] Suzanne's org_user created 2026-04-27T19:19:52; invitation redeemed the same day.

**Against:** The Customers import carried an `error` tier, which means row-level rejects
and suppressed deletes. It is still the only customer import this org has ever had —
`customers.updated_at` has a max of 2026-04-27T18:59:15, 113 days ago.

---

### Phase 2 → 3 (Progress) · **2026-04-27**, regressed 2026-05-05, firm **2026-06-09** · confidence: medium

**What changed:** Two core files were in from day one, so the bar is met immediately on
2026-04-27. But the *most recent* Products import took a fatal on 2026-05-05, which is a
genuine regression, and the phase is only durably held from 2026-06-09.

**Evidence:**
- [DB] `import_history` 2026-04-27: both `Products` and `Customers` present — two core files, worst tier `error`, no fatal.
- [DB] `import_history` 2026-05-05: `Products` — **clean ×5, fatal ×1**.
- [CALL, 2026-05-05T18:00Z, attendees Brian, Suzanne, Christine, Kylor] Suzanne, looking at the iPad:
  > "Well, it would be nice if we had, look at dancing.    I don't understand why all the colors are missing."
- [CALL, 2026-05-05T18:00Z] Suzanne again: "Adelina, go up to Adelina, UB, okay.    So what I was hoping is, now see, the Adelina, the colors are missing."
- [DB] `import_history` 2026-06-09 onward: Products `clean` with no fatal on 06-09, 06-11, 06-12; `Product Stories` added 2026-06-30 (clean ×2) — a third core file.

**Against:** If "progress" is read strictly as *no fatal on the most recent of each type*,
the phase is not held between 2026-05-05 and 2026-06-09 — the intervening Products imports
(05-06, 05-12, 05-13, 05-19, 05-20, 06-02) are warning-only, which technically clears the
fatal but on a file everyone on the call agreed was wrong.

---

### Phase 3 → 4 (Catalog Completeness) · **2026-06-17**, completed **2026-07-08** · confidence: high

**What changed:** The catalog became buildable as a live iPad — full colorway coverage,
images, SmartList, PDF formats. Pricing completed it three weeks later.

**Evidence:**
- [HS #14638, 2026-06-17T00:44:03Z, kylor@supercatsolutions.com (SuperCat)]
  > "Catalog is in solid shape — 1,676 active products, all importing clean with no errors on the last several uploads."
  > "Images — about 84% coverage right now (1,404 of 1,676 products have images)."
  > "SmartList — 'Spring 2026 Rotation' is live and getting use."
  > "PDF reports — three formats configured and ready (Org Tearsheet, 3x3, One Per Page)."
- [DB] `ipad_reports`: 3 rows — Organization Tearsheet, 3 x 3, One Per Page (all created 2026-04-27).
- [DB] `smart_stacks`: `Spring 2026 Rotation` (created 2026-05-20, 98 items, published) and `Dorell Studio` (created 2026-07-02, 113 items, published). Neither is dormant.
- [HS #14707, 2026-07-08T18:47:32Z, kylor@supercatsolutions.com] on the stories-with-pricing load: "1,340 products: description + pricing / 78 products: pricing only".
- [DB] Today: 1,627 active products, 1,564 with images (96%), 1,512 with a story, **1,418 with pricing embedded in the story** — matching Kylor's 1,340 + 78 exactly.

**Against:** "Complete" is scope-relative and the scope is unusual. There are **0 options,
0 option_groups, 0 inventory rows** — and that is by design, stated twice by the client, not
unfinished work:
- [CALL, 2026-04-29T21:00Z] Kylor: "then any, Suzanne, any inventory that you guys would want to capture?" — Suzanne: **"Nope."**
- [CALL, 2026-04-29T21:00Z] Suzanne: "We just this is purely to show customer samples and to show them it shows a new product to order waterfalls and samples."
- [CALL, 2026-04-13T20:00Z, reading the data-readiness questionnaire] "And then, so no options.    It's straightforward."
- 209 SKUs remain uncosted. [HS #14707, 2026-07-07T22:42:04Z, christine.soh@dorellfabrics.com]: "All the pricing are in. The ones that are still at zero has not been costed yet."

---

### Phase 4 → 5 (Reps Signed In) · **not reached** on the strict reading; **2026-06-30** on the practical one · confidence: high

**What changed:** Non-admin Dorell staff began using the iPad. No field sales rep ever did.

**Evidence (strict reading — not reached):**
- [DB] Every `org_user` in org 290 that is not SuperCat staff is Suzanne, Christine, Brian, Gina, Heather, or Claudia. **Chip Stroup, Andy, and Danny — the three field reps whose territory codes (53, 62, 7) have been in the customer file since 2026-04-27 — have never been provisioned, invited, or logged in.**
- [HS #14799, 2026-07-29T15:44:15Z, kyla@supercatsolutions.com] still lists this as a future action item: "Send field rep list for iPad onboarding … When you're ready to bring Chip, Andy, Claudia, Danny, and the rest onto the iPad".
- [DB] Brian Frankel (CEO), provisioned 2026-05-03, `last_ipad_login_at` = **NULL**.

**Evidence (practical reading — 2026-06-30):**
- [DB] `login_events`: Gina Garza first signs in 2026-06-30 (3 events); Kate Gothreau 2026-07-01 (2 events); Heather Steczko 2026-07-06.
- [DB] `org_users`: Gina created 2026-06-30T17:34, Heather 2026-07-02T17:07 — both `is_admin=false`, both in `Dorell Internal`.

**Against:** Dorell told SuperCat at kickoff that "reps" would never be the user base:
- [CALL, 2026-04-13T20:00Z] Suzanne: "We have a, you know, sell very large, large customers, large volume.    So we don't have a lot of reps.    So, but it will be utilized by the product development team.    So they're going to be our reps in that sense".
On that definition — the PD team is the rep base — the phase was reached on 2026-06-30 and
is currently satisfied by Gina, Heather and (as of today) Claudia.

---

### Phase 5 → 6 (Admin Training) · **2026-07-21** · confidence: high

**What changed:** Kyla Bosch delivered a live 80-minute Admin Console training to Christine
and Suzanne.

**Evidence:**
- [CALL, 2026-07-21T18:30:00Z, "Dorell x SCS Admin Training", 60 min scheduled, transcript runs to 01:20:20; attendees Suzanne Fukunaga, Christine Soh, Kyla Bosch]
- [HS #14799, 2026-07-20T18:18:30Z, kyla@supercatsolutions.com] "I have sent a meeting invite in the meantime for 11:30 -12:30 PST."
- [HS #14799, 2026-07-20T16:55:10Z, Suzanne@dorellfabrics.com (customer)]
  > "Admin Training: Christine will lead on this, and I would be her backup."
- Content covered per [HS #14799, 2026-07-29T15:44:15Z]: data flow, users and user groups, territory codes, customer accounts and local customers, order origin, Quick View fields, email templates, user-group permissions.
- [DB] Kyla's org_user created 2026-07-17T16:07; `login_events` shows 3 sign-ins on 2026-07-21 — the training session itself.

**Against:** "with ongoing operations covered" is only partly true. The training closed with
four unresolved items and a promise:
- [HS #14799, 2026-07-29T15:44:15Z, kyla@supercatsolutions.com] lists four SuperCat action items with ETA "This week": pricing display options, color-thumbnail/fabric-family view, single-item editing, SKU-builder/barcode clarification.
**None of the four has any answer anywhere in the corpus.** Kyla's 2026-07-29 message is her
last appearance.

---

### Phase 6 → 7 (Go-Live / handoff to support) · **2026-07-20** · confidence: high

**What changed:** Formal handoff from onboarding to support, declared in writing.

**Evidence:**
- [HS #14799, 2026-07-20T14:28:22Z, kyla@supercatsolutions.com (SuperCat)]
  > "My name is Kyla, and I'll be your primary point of contact at SuperCat going forward. Kylor has done a great job getting Dorell Fabrics through onboarding, and I'm excited to take it from here as we move into the next phase."
  > "**Your onboarding is now complete.**"
- [HS #14811, 2026-07-20T14:29:02Z] The same message captured under `support@supercatsolutions.com`, signed "Kyla Bosch / Onboarding & Implementation Manager".
- [HS #14799] Ticket tags change to `l1 - handled by frontline support`, `product - admin console`, `type: training` — support-queue routing, not onboarding.
- Ongoing client activity after handoff is real: [DB] 4 orders submitted post-handoff (07-14 ×2 pre-handoff; 08-18 ×3), 20 client login events across 08-10 → 08-18.

**Against:** The handoff did not hold operationally. [HS #15031, 2026-08-11T04:09:03Z]
Suzanne addresses "Hi Kyla or support person," and the answer on 2026-08-11T18:42:53Z and
2026-08-12T18:31:54Z comes from `kylor@supercatsolutions.com`, not Kyla. Kyla has not
appeared since 2026-07-29.

---

## C. Current phase as of 2026-08-18

**Phase 7 — post-go-live, in active use, with three specific operational settings still
unfinished.** Confidence: high.

**Evidence for Phase 7 held:**
- [DB] On 2026-08-18 alone: Heather Steczko signs in 16:19:46, Gina Garza 16:38:25, Christine Soh 16:38:44, Suzanne Fukunaga 18:24:04. **Four distinct Dorell users on device in one day** — the most since Showtime.
- [DB] `org_users`: Claudia Frankel provisioned 2026-08-18T16:50:14.
- [DB] `organization_invitations`: Dana Gomez invited 2026-08-18T17:00:00, `created_by_id` = 155510 = **Christine Soh**. The client is adding users without SuperCat.
- [DB] Three orders submitted 2026-08-18: 16:48:45, 17:12:42, and **18:30:25**.

**Evidence for "not finished":**
- [DB] `organizations.order_email_recipient` = `Suzanne@dorellfabrics.com` — still the placeholder Kylor flagged 32 days ago. [HS #14798, 2026-07-17T16:27:36Z]: "I staged these using our standard demo subject-line patterns and Suzanne's email as a temporary placeholder". This contradicts the stated business purpose — [CALL, 2026-05-18T21:00Z]: "it's to go to our customer service, not to the customer."
- [DB] `products.net_price` = **1.00 on all 1,627 rows**; all 389 customers still have `DefaultPriceCode = net`. Kylor advised the fix on [HS #14707, 2026-07-08T18:47:32Z]: "use list as the DefaultPriceCode instead of net. Net is still a $1.00 placeholder". The customer file has not been touched since 2026-04-27.
- [DB] `organizations.order_origins` = `[]`, and **all 10 orders have `order_type = 'Confirmed'`** — Kyla's stated intent was not configured. [CALL, 2026-07-21] Kyla: "I think what we can maybe do is just make sure that the default order origin remains like a quote or a sample."

---

## D. Turning points

**1. 2026-04-13 — Kylor joins and Suzanne fences the scope.**
Suzanne's "I'm going to call it Phase 1" and "Nope" to inventory are the two decisions that
made this project deliverable at all. Everything absent from the org today — 0 options,
0 inventory, 0 eCat Online — traces to this call, and none of it is a gap.

**2. 2026-04-27 → 2026-04-29 — the twelve-day silence, and how it was handled.**
Data was handed over 2026-04-15; nothing happened until 2026-04-27. Jon was at High Point
with no out-of-office. [CALL, 2026-04-29T21:00Z] Kylor opened by owning it:
> "I just want to start this off with apologies.    Okay.    Totally our bad.    This was a crazy week last week.    This kind of got honestly buried in my inbox, and there was a lot of craziness going on.    But that's absolutely not the precedent that we want to start with."
Twelve days out of a five-week runway, at the front. It never became a trust problem —
Suzanne's response was "Yeah, it really is" about the state of the build — but the deadline
never recovered the time.

**3. 2026-05-05 → 2026-05-06 — the data collapse and the scrap-and-restart.**
The single most damaging stretch. Kylor was reconciling five incompatible sources:
> "So basically where I've been running into a bit of a roadblock is like you sent that source file last night and there's 30,000 SKUs in there.    Correct.    And I have like 130 pictures."
Suzanne diagnosed her own side of it — "I'm going to give you a new file that's going to
have all this.    The only SKUs we need" — and then made the call that saved the project:
> "And you can just, if you can, can you just delete everything and just bring a new thing?"
This is what a healthy client looks like under pressure. It also cost two weeks, and it is
why the show was missed.

**4. 2026-05-18 → 2026-05-20 — the deadline is conceded, and then partly met anyway.**
On the 2026-05-18 call, one day before Showtime:
> "Yeah, we kind of missed it, so, but don't worry because we can use it right after.    So, we see, we see X amount of customers this week, but we see customers for the next four weeks, you know, individually.    So we missed a couple of days, but we're okay."
The database disagrees. Order `155309-051826-1` was submitted 2026-05-18T21:27:38, billed
to **AMALFI** (customer_num 15124) — the only order in the org's history tied to a real
customer account — containing `ARCADIA-C0-BIRCH` plus `ARCADIA-WF-ASSORTED`: a colorway and
its waterfall, exactly the intended motion. `login_events` then records 25 sign-ins on
2026-05-19 (Suzanne 14, Christine 11) and 10 on 2026-05-20. They took it to the show.
The concession was about completeness, not about use.

**5. 2026-06-30 → 2026-07-08 — Christine takes the system over, and the project changes shape.**
[HS #14638, 2026-06-30T20:39:16Z, christine.soh@dorellfabrics.com]:
> "Sorry for the silence. I think we have all the products corrected and aligned now."
> "We would like to add pricing to the products. We have 10 prices that we need to upload per item."
Two days later she had created all ten price levels in Admin herself — [DB]
`price_levels.created_at` runs 2026-07-02T00:48:56 through 00:54:24, ten levels in six
minutes — and uploaded the columns. The requirement that followed (see all ten prices at
once, because reps negotiate FOB and warehouse together) hit a hard product limit, and
Suzanne escalated it commercially: [HS #14707, 2026-07-06T19:39:25Z] "We are willing to pay
programming charges to accomplish this." Kylor answered with the stories workaround rather
than a dev ticket, Suzanne accepted — "Let's try this and see how it looks!" — and it
shipped 2026-07-08. That workaround is what 1,418 products display today, and it is also
the thing Kyla flagged on 2026-07-29 as needing revisiting, because embedded story pricing
leaks into emailed presentations.

---

## E. The three questions the phase model does not ask

### A. Did this client ever go backwards?

**Yes — once badly, once quietly. Never close to churn.**

**The hard regression: 2026-05-05 → 2026-05-20.** Colorways vanished from the iPad, a
Products import took a fatal (`import_history` 2026-05-05: clean ×5, fatal ×1), the whole
product file was scrapped and rebuilt from scratch, and the only hard deadline in the
project — Showtime, May 19–21 — was missed. Trigger: no single source of truth for a
pattern × colorway × sample-type catalog. Ended by Suzanne's decision to restart clean.

**The quiet one: 2026-05-20 → 2026-06-30, six weeks.** Between the 2026-05-20 SmartList
creation and Christine's 2026-06-30 email there are exactly two substantive corpus items
(the 2026-06-10/11 Foxtrot image mismatch, and Kylor's unanswered 2026-06-17 check-in).
Christine named it herself: "Sorry for the silence."

**But the silence was correspondence, not usage — and this distinction matters.** `login_events`
for that same window shows Dorell users signing in on 05-22, 05-27, 06-02 (11 events),
06-08, 06-09, 06-10, 06-11, 06-12, 06-15, 06-17, 06-18, 06-22, 06-24 (8 events) and 06-30.
They were in the product almost every week while nobody was answering email. Anyone reading
only the ticket stream would score this stretch as a stall; anyone reading only the login
table would not see a stall at all. Trigger for the email silence: the forcing function had
passed. Ended by Christine's own initiative, unprompted by SuperCat.

**No churn signal at any point.** No pricing complaint post-signature, no competitive
mention, no escalation, no threat. The one commercial friction — the multi-price display —
Dorell offered to *pay more* to solve. The nearest thing to a negative is Brian's pre-sale
2026-02-25 remark, "it might be a little robust for what we're looking for," which is a
scoping observation, not a churn risk, and it was answered by scoping down to Tier 1.

### B. Adoption — separate from go-live

**Five Dorell people have ever signed into eCat. Two were provisioned and never did. Zero
field sales reps have ever been given an account.**

| Person | Ever logged in | Login days | Last login |
|---|---|---|---|
| Suzanne Fukunaga | yes | ~30 distinct days | 2026-08-18 18:24 |
| Christine Soh | yes | ~22 distinct days | 2026-08-18 16:38 |
| Gina Garza | yes | 2 (06-30, 08-18) | 2026-08-18 16:38 |
| Heather Steczko | yes | 2 (07-06, 08-18) | 2026-08-18 16:19 |
| Kate Gothreau | yes | 1 (07-01) | 2026-07-01 — **account since removed** |
| Brian Frankel (CEO) | **no** | 0 | provisioned 2026-05-03 |
| Claudia Frankel | **no** | 0 | provisioned 2026-08-18 16:50 |

Pipeline: Rachel Jenkins invited 2026-06-30, expired unredeemed 2026-07-07. Dana Gomez
invited 2026-08-18 by Christine, pending. Chip Stroup, Andy, Danny — the actual field
reps — have never been invited.

**Volume and shape.** Roughly 190 login events across 77 user-days, 2026-04-27 → 2026-08-18.
The distribution is bimodal: a Showtime spike (2026-05-19: 25 events; 2026-05-20: 10) and a
long administrative tail dominated by Suzanne and Christine doing catalog work. Peak
client-side day since the show is **2026-08-18** — 7 events across 4 users.

**What they actually do with it.** Ten orders, all submitted by Suzanne, all `order_source =
'ipad'`, all `price_level = 'net'`. The line contents are the real proof that the product is
being used as designed rather than merely opened:

| Order | Date | Lines | Content |
|---|---|---|---|
| 155309-051826-1 | 05-18 | 2 | ARCADIA-C0-BIRCH, ARCADIA-WF-ASSORTED — **billed to AMALFI, a real customer** |
| 155309-061026-2 | 06-10 | 1 | FOXTROT-CARBON — the image-mismatch reproduction |
| 155309-063026-3 / -3-1 | 06-30 | 4 | BEC-WF, AMES-WF, CHROMA-WF + BEC-C0-CAMEL *"Half yard cut"* |
| 155309-063026-4 | 06-30 | 3 | AMES-WF, BENSON-UV-WF + BEC-C0-FRENCH-BLUE *"Please send 1\2 cut"*; order note *"Fedex ground"* |
| 155309-071426-5 / -5-1 | 07-14 | 4 | ADELINA-UV-GRAPHITE, ADELINA-UV-WF + BAYLIN-C0-DOVE/GRAPHITE *"1/2 yd"* |
| 155309-081826-6 | 08-18 | 4 | ADELINA-UV-LAGOON ×3 *"3.20"*, *"Price4.00"* + AMES-WF; note *"Ship by August 25, 2026"* |
| 155309-081826-7 | 08-18 | 4 | ADELINA-UV-WF, AMES-WF, WINSLET-WF ×2 + AMES-C0-CASHMERE *"Send half yard cut price $2.20"* |
| 155309-081826-8 | 08-18 | 1 | BAYLIN-C0-PEARL *"FOB Price 4.75"* |

Every order is waterfall SKUs plus colorway SKUs carrying a hand-typed half-yard instruction
and, increasingly, a negotiated price in the line note. That is the NCR checkoff sheet,
digitised — including Suzanne's own 2026-02-10 requirement that reps "write it in":
> "Can you write stuff?    Because we actually when they're looking at samples, they ask us how much is and we say 550 and that we put it on the order so that they know."

**So: has this client transacted?** No, and it never intended to. Every total is $0.00
except one $8.00, and that $8.00 is a single hand-keyed `calculated_price` on line 4 of
order -5, not a sale. Suzanne stated the model twice — "We don't charge for our half-yard
cuts, and we don't charge for our waterfalls" (2026-04-29) and "But they're not ordering the
product itself.    They're in samples" (2026-07-21). **$0.00 is the correct value.** Nine of
the ten are billed to Suzanne or a misspelt "Christine Son" because they are rehearsals of a
customer-facing motion performed by the people who own it, and the tenth — AMALFI, at
Showtime — is the real thing.

**Self-sufficiency is the strongest adoption signal here, and it is not visible in login
counts.** Christine created all 10 price levels in Admin (2026-07-02), uploaded the price
columns unaided, built the `Dorell Studio` SmartList (2026-07-02, 113 items), edited the
`One Per Page` PDF format (2026-07-28), and invited Dana Gomez (2026-08-18). Suzanne created
the Gina, Claudia, Rachel and Heather invitations herself (`created_by_id` 155309). This
client administers its own org.

### C. Current trajectory

**Improving.** Not steady, not decaying.

**On the "no import since 2026-07-08" signal — it is normal for this client, and I would not
flag it.** Three independent reasons:
1. There is nothing left to import. The catalog hit completeness on 2026-07-08 with the
   stories-plus-pricing load; 1,627 products, 96% images, 1,418 priced. The 209 uncosted
   SKUs are blocked on Dorell's costing, not on an import.
2. Dorell's data changes seasonally, by design. [CALL, 2026-05-06T22:00Z] Kylor: "usually
   people are like, hey, you know, once or twice a year, we update our products, we update
   our customer file." Dorell explicitly bought a per-show rotation tool, not a live feed —
   no inventory, no sales data, no ERP loop.
3. The import cadence has always tracked show prep, not weeks. It ran hot April–July because
   there was a build; it went quiet because the build finished.

Six weeks of import silence would be alarming for an inventory-driven furniture client. For
a fabric wholesaler running a seasonal rotation between Showtimes, it is the expected
resting state.

**What actually indicates direction is the 2026-08-18 activity, and it is unambiguous.** In
one day: four distinct users on device (three of them non-admin PD staff, the population
that was supposed to adopt this), a fifth user provisioned, a sixth invited *by the client*,
and three sample orders carrying real negotiated prices and a real ship-by date. That is a
show day or a dress rehearsal for one, and it is the busiest client-side day since Showtime
in May. Usage is broadening from two administrators to the PD team — the exact trajectory
Suzanne described at kickoff.

**Three things are drifting, and none of them are catalog problems:**
1. **Order routing is still wrong.** `order_email_recipient` = `Suzanne@dorellfabrics.com`,
   `backup_order_email_recipient` = blank. The whole point is that sample requests reach
   customer service. Today three orders' worth of buyer requests landed in one person's
   personal inbox, 32 days after Kylor asked for the correct address and got no answer.
2. **Pricing resolves to a placeholder at the moment of use.** `net_price` = $1.00 across all
   1,627 products and all 389 customers default to `net`. The instant a rep selects a
   customer — the recommended first step — every price becomes $1. The ten real levels only
   show with no customer selected, or via the story text. Fixing it needs one customer-file
   re-import, which has not happened since 2026-04-27.
3. **SuperCat's side of the last conversation was never answered.** Kyla's four action items
   of 2026-07-29 all carried ETA "This week"; none has any reply in the corpus, and she has
   not appeared since. The 2026-08-11 ticket went to Kylor instead. The support handoff is
   nominal, not real.

**Net:** the client is healthier than the import table suggests and the account is being
supported more thinly than the go-live declaration suggests. If the trajectory turns, it
will turn on item 3, not on data.

---

## Contradictions with `RAWSTATE_drf.json`

Flagged as required. None of these are errors in the capture; two change the reading.

1. **Order count is 9 in RAWSTATE, 10 in the database.** `155309-081826-8` was submitted
   2026-08-18T18:30:25 — five and a half minutes after RAWSTATE's `captured_at` of
   2026-08-18T18:25:00Z. A capture-boundary artifact, but it means the client transacted
   again *while the snapshot was being taken*, which strengthens the trajectory finding.
2. **`distinct_ordering_reps: 1` is true but misleading.** Suzanne is `is_admin=true` and is
   therefore excluded from RAWSTATE's own `reps` definition. Read together, the two fields
   say the org has 3 reps and 0 of them have ever ordered — which is correct and is the more
   useful statement.
3. **`reps: 3` are not sales reps.** They are Gina Garza, Heather Steczko and Claudia Frankel —
   product-development staff. Dorell's three actual field reps (Chip, Andy, Danny) have no
   accounts. The label is right by the query and wrong by the business.
4. **`user_types: 2` is correct, but Kylor's 2026-07-17 claim to have "created user groups
   (Dorell Internal for your team...)" is not.** `Dorell Internal` was created
   2026-04-15T13:51:34.595917 — the same second as the org — i.e. it is the renamed
   DefaultUserGroup. Only `SuperCat Team` (2026-07-17T16:06:05) was genuinely new.
5. **`customers_unresolved_dpc: 0` is true and reassuring in the wrong direction.** All 389
   resolve because all 389 point at `net`, a $1.00 placeholder. Resolved ≠ correct.
6. **`price_levels: 11`, all `ad-hoc`, is not remarkable — it is the client's answer.**
   Christine specified exactly ten in [HS #14638, 2026-07-01T19:31:05Z] with three currencies
   (USD, RMB, CAD), because Dorell quotes domestic, FOB-China and Canadian on the same SKU
   and holds a "lowest sell" floor per channel: "that is the lowest that we are allowed to.
   Quote for, before we need to get the CEO's approval." `net` is the eleventh, created
   2026-04-27, and is the placeholder. Ad-hoc is correct: none of them are calculated.
