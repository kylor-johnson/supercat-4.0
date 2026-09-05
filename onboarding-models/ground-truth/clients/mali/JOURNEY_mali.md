# JOURNEY — Magic Lite | NSL (`mali`, org 285)

*Independent ground truth, reconstructed blind from `CORPUS_mali_part1.md`,
`CORPUS_mali_part2.md`, `RAWSTATE_mali.json` and direct read-only SQL against
`supercat-postgres-vpn`. Written 2026-08-25.*

**Contamination statement:** No forbidden file was opened. I did not read
`CLIENT_PROFILE.md`, any `HANDOFF*.md` / `READINESS_CHECKLIST*.md` /
`LIBRARY-BUILD-CHECKLIST.md` in `eCat_Onboarding/mali/`, `REGISTRY.yaml`, any
`onboarding-models/` framework doc, `SCORECARD.md`, any other client's
`JOURNEY_*.md`, or any `ecat-*` skill. The only files read under
`eCat_Onboarding/mali/` are the three inputs inside `_ground_truth/`. I did
read `HANDOFF_mali.md` — that is the instruction sheet I was given.

---

## Narrative

Magic Lite came to SuperCat in September 2025 as an unusually well-qualified
buyer: a 40-year-old Canadian lighting manufacturer with a US sister company
(NSL), Dynamics GP as a system of record, a 400-page catalogue, and a COO who
had written her own RFP. They signed in November. What they did not have —
and what nobody established before the contract — was a structured product
data file. SuperCat's answer was to build one by scraping the PDF catalogue.
That decision set the shape of the next eight months.

The scrape produced 948 SKUs by 22 December 2025 and a catalogue that, in
Brent Sanders' own words on 20 January, "doesn't look very good because
there's no pictures in it." What followed was a five-month grind in which
SuperCat repeatedly declared data complete and the client repeatedly found it
wasn't: wrong images, missing pricing, absent cut sheets, NSL content branded
Magic Lite. Twice the relationship nearly broke — on 10 March, when Jen Penton
wrote that she was "admittedly a bit disappointed with the website
scraping/info upload results of supercat," and far more seriously on 10 July,
when she asked to "meet asap to discuss if and how we are going to conclude
this project."

The 10 July escalation reached SuperCat's CEO and worked. A CEO-chaired call
on 15 July, an intensive fortnight of image and pricing repair, and a genuinely
good feedback loop with a newly-added Magic Lite product specialist (Craig
Shinde) turned the project around. Five beta rep invitations went out on
10 August. Three were redeemed. The first automated inventory file from the
ERP integrator landed on 12 August, and the recurring 6am/noon schedule was
confirmed on 25 August — the day this was written.

The org has never submitted an order, and that is not a failure signal. It was
never configured to take one: ship-to addresses were deliberately excluded from
the customer file because, as the CFO put it in March, "we are not entering
orders through SuperCat at this time"; the default order type was set to
*Quote*; and no outside rep has ever opened the iPad app. The single row in
`orders` is an empty server-side cart created by SuperCat's own support account
during a screen-share on 15 July.

Two things in the brief need correcting before anything else is read. First,
"the entire Magic Lite rep team has never signed in" is true only of the iPad.
Four of the five ML Reps accounts have eCat Online logins, and the *only*
outside rep-agency person who has ever used this system at all is Dan French of
GS Lighting Group — a **Magic Lite** rep, on 10 August. Second, the three "NSL
Reps" who have signed into the iPad are two SuperCat employees and one NSL
head-office employee. Outside-rep iPad adoption in this org is zero, for both
brands.

---

## A. Cast

### Magic Lite / NSL (client)

| Person | Email | Side | First seen | Last seen | Role & changes |
|---|---|---|---|---|---|
| Jennifer "Jen P" Penton | jen.penton@magiclite.com | ML (both brands) | 2025-09-12 (intro call) | 2026-08-24 (email) | Introduces herself as "business development for MagicLight and NSL" on 2025-11-20; signs every email from 2025-12-05 onward as **Chief Operating Officer**. Project owner and primary escalation voice. |
| Jen "Jen Z" Zorony | jen@magiclite.com | ML (both brands) | 2025-10-02 (demo); her 2025-10-10 email to Endeavour is quoted inside ticket #13970 | 2026-08-17 (email) | **Chief Financial Officer.** Owns customer/inventory data and the Endeavour relationship. Becomes the day-to-day driver from June onward while Jen P travels. |
| Tom Penton | penton@magiclite.com | ML | 2026-04-30 | 2026-04-30 | Owner / "upper boss." Named on 2025-10-10 ("That's my dad."). Invited 2026-04-30; hit the period-in-username defect; **invitation never redeemed** [DB]. |
| Marquel Cardenas | marquel@magiclite.com | ML | 2026-02-11 (added by Jen P) | 2026-04-30 (eOL login) | "Bookkeeper/Customer Service." Assigned the product-hierarchy data entry; completed ProductFamily and ProductType only. |
| Craig Shinde | craig@magiclite.com | ML | 2026-04-28 (listed as internal staff) | 2026-07-29 | "Product Data and Quotations Specialist." Effectively inactive until 2026-07-21, when his catalogue punch list becomes the single most useful client artefact in the project. |
| Priya Singh | priya@magiclite.com | ML | 2025-11-27 (invited, redeemed) | 2026-07-22 (mentioned) | Internal ML. Flagged on 2026-04-15 as mis-filed among the rep list. |
| Pansy Ali | pansy@magiclite.com | ML | 2026-04-29 (invite, expired) | 2026-05-13 (re-invited live on call, redeemed) | Internal ML. |
| Jason Fisher | jason@nslusa.com | NSL | 2026-04-28 | 2026-08-19 (iPad login) | **National Sales Manager, NSL.** Hit the `jfisher` username collision. The only client-side person other than Jen P ever to open the mali iPad app. |
| Michelle Coleman | michelle@nslusa.com | NSL | 2026-04-28 | 2026-07-20 (login) | "Assistant Executive Administrator." Hit the `michelle` username collision. |
| Patricia Krpic | patricia@nslusa.com | NSL | 2026-04-28 | 2026-07-21 (login) | NSL internal. Never appears in a thread in her own voice. |
| Mike Krause | mike@nslusa.com | NSL | 2026-08-10 [DB only] | 2026-08-10 | Username `Rockymountain`. Beta invite, redeemed same day. **Never appears in the corpus.** |
| Dan French | daniel@gslightinggroup.ca | ML rep agency (GS Lighting Group) | 2026-08-10 [DB only] | 2026-08-11 | Beta invite redeemed 2 min after issue; eCat Online login 2026-08-10. **Never appears in the corpus.** The only outside rep to use the system. |
| Josh Nelson | josh.jsna@gmail.com | NSL rep agency (James S. Nelson) | 2026-05-13 (named as beta rep) | 2026-08-17 (invite redeemed) | Redeemed with ~2h before expiry. No mali iPad or eOL login. |
| Ryan / Jason, Electra Sales | ryan@ / jason@electrasalesltd.ca | ML rep agency | 2026-08-10 [DB only] | expired 2026-08-17 | Beta invites, **never redeemed.** |

Named but never present: Jim Bechkos and Tim Veal (GSL), Alton McKey, Shelley
Aldridge, Josh Skula, Anna Tardif — the beta list Jen P supplied on 2026-05-13.
Only Josh Nelson survived to the invitations actually sent on 2026-08-10.

### SuperCat

| Person | Email | First | Last | Role |
|---|---|---|---|---|
| Emery Rust | emery@supercatsolutions.com | 2025-09-12 | 2025-11-20 | AE. Ran the entire sales cycle. Disappears at kickoff. |
| Jon Vanderberg | — | 2025-10-02 | 2025-10-02 | Solutions/demo. One appearance. |
| Kjael Skaalerud | kjael@supercatsolutions.com | 2025-10-02 | 2026-07-28 | **CEO.** Present at demo and kickoff, then absent for eight months, then re-enters on 2026-07-10 and personally chairs the recovery. |
| Chuck Wiebe | chuck@supercatsolutions.com | 2025-11-20 | 2026-01-13 | Head of implementation at kickoff. Total contribution after kickoff: one HelpScout note, "@brentS Magiclite for you." |
| Brent Sanders | brent@supercatsolutions.com | 2025-11-20 | 2026-03-19 (last call); invited 2026-07-15 | **CTO.** Owns the scrape strategy and the catalogue-display decisions. Hands off to Kylor after March. |
| Kylor Johnson | kylor@supercatsolutions.com | 2025-12-08 ("I recently joined the team at SuperCat") | 2026-08-25 | Onboarding lead → signs as **Head of Customer Success** by 2026-08-10. The continuous thread through the whole project. |
| Kyla Bosch | kyla@ / support@supercatsolutions.com | 2026-03-11 (internal note) / 2026-04-09 (introduced to client) | 2026-08-25 | "Onboarding & Implementation Manager"; introduced on 2026-04-09 as "our head of support." Based in South Africa. Owns the account from April. |

### Endeavour Solutions (ERP integrator, tier C)

| Person | Email | First | Last | Role |
|---|---|---|---|---|
| Brittni Pryputniski | bpryputniski@endeavoursolutions.com *and* @endeavor4solutions.com | 2025-10-15 (email quoted inside #13970) | 2026-08-25 | "Solution Analyst/Senior Consultant." Owns the GP → SFTP inventory pipeline. |
| Robert Volpato | rvolpato@endeavoursolutions.com | 2025-10-15 (cc) | 2025-10-15 | Never active. |

> **Correction to the brief:** the handoff calls Endeavour "the Business Central
> integrator." Every reference in the corpus is to **Microsoft Dynamics GP**,
> on-premises, with a SQL Server back end — Brittni on 2026-04-09: "GP is housed
> in a SQL Server on-prem". No Business Central anywhere.

---

## B. Phase transitions

Where the two brands diverge I give both. Where they don't, they don't — through
Phase 4 there is one product file, one import pipeline and one catalogue.

### Phase 0 → 1 (Discovery / Kickoff) · both brands 2025-11-20 · confidence: high

**What changed:** The implementation kickoff call was held and the org was
created the next morning.

**Evidence:**
- [CALL, 2025-11-20T20:00Z, "SuperCat / MagicLite - Implementation Intro"] attendees Chuck Wiebe, Brent Sanders, Kjael Skaalerud, Emery Rust, Jen Penton, Jen Zorony. Chuck Wiebe (SuperCat): "I'm Chuck Wiebe. I work on a lot of implementations and I'll be helping you get this going"
- [Kjael Skaalerud (SuperCat), same call] > "So generally we pace against six weeks for like, let her rip, in-market, writing orders, doing the thing."
- [DB] `organizations.created_at` = 2025-11-21 17:37:37; the first two admin invitations (jen.penton@, jen@magiclite.com) were created 2025-11-21 17:41:57 — four minutes later.

**Against:** The kickoff call is also the call at which the project was
*deferred*. Jen P: "in my mind, if it was back into kind of our court to push it
out to our reps and do that training around January, that would be great." A
phase model that marks 2025-11-20 as "started" will over-count roughly two
months of deliberate inactivity.

### Phase 1 → 2 (Initial Import) · both brands 2025-12-22 · confidence: high

**What changed:** The first products.csv was imported — twelve attempts over two
hours, ending error-free.

**Evidence:**
- [DB `import_events`] 2025-12-22 21:54:17 Products — 1 fatal, 1,003 errors. Twelve product imports that evening; 2025-12-22 22:45:35 and 23:54:31 are the first with zero errors. `Taxonomies` clean at 22:27:20.
- [DB `import_events`] 2025-12-23 05:05:18 first Images import, clean.

**Against:** **Nothing in the corpus records this.** No email, no ticket, no call
mentions a product import in December. The client's next contact was Brent on
2026-01-07 asking for "some time slots open this week or next to do a
preliminary review of your catalog." A framework driven by correspondence would
date Phase 2 to 2026-01-20 — a month late.

### Phase 2 → 3 (Progress) · both brands 2025-12-23 mechanically / 2026-03-26 substantively · confidence: medium

**What changed:** Depends entirely on how the question is read.

**Evidence:**
- Mechanically — "more than one core file in, without fatal errors on the most recent of each" — is satisfied on **2025-12-23**: the most recent Products (22:45 / 23:54, error-free), Taxonomies (clean) and Images (clean) imports all carry no fatal. Three files in, none fatal.
- Substantively, the last core file lands on **2026-03-26**: [DB] Customers first clean import 2026-03-18 03:32:42; Inventory first clean 2026-03-26 20:15; Product Stories first clean 2026-03-16.
- [HS #14005, 2026-03-11, kylor@supercatsolutions.com] > "The cleaned file (906 products) is imported and live." and > "We combined the ML (421 customers) and NSL (3,096 customers) lists into one file — 3,517 rows total, no overlapping account numbers."

**Against:** The 2025-12-23 reading is the reason I flag this phase as the
weakest in the model. On 2025-12-23 the catalogue had no correct images, no
pricing, no customers, no inventory and no stories. Three months later the
client was still calling it unusable. "No fatal errors on the most recent
import" measures whether a CSV parsed, not whether a project progressed.

### Phase 3 → 4 (Catalog Completeness) · ML 2026-07-24 / NSL 2026-08-03 · confidence: medium

**What changed:** The catalogue became buildable as a live iPad — brand-separated
pricing, brand-correct cut sheets, and an image set the client's own product
specialist had signed off.

**Evidence:**
- [HS #14727, 2026-07-24, kyla@supercatsolutions.com] > "Imported the final product file Applied 130 image fixes, added UPC codes, and updated pricing." and > "ML and NSL each have their own pricing, cut sheets, instructions, Library documents, and UPC codes, all correctly assigned to their respective user groups."
- [HS #14851, 2026-08-03, kylor@supercatsolutions.com] > "We have added the new NSL Code field and populated it for the 55 confirmed products where Magic Lite and NSL use different item numbers." — the last structural gap specific to NSL.
- [DB] `price_levels_user_types`: ML Reps → ML DN + ML List; NSL Reps → NSL DN + NSL List; eOL ML Public Site → ML pair; eOL NSL Public Site → NSL pair. Brand separation is correct today.
- [DB] `customers`: 3,418 rows, 415 `mldn` / 3,003 `nsldn`; zero rows missing a territory code, a default price code, a billing address, a city, a post code or a country. Zero `TBD` placeholders remain.

**Against, and it is substantial:** the catalogue is not complete today. [DB]
16 of the 117 visible hero products have `nsldn`/`nsllist` = null, and 3 have no
ML price. An NSL rep opening the app right now sees no price on 14% of the
visible catalogue. 73 of 725 active products have no image and 65 have no story
— against Kylor's 2026-07-08 claim that "all 695 products now have a product
story populated." Confidence is *medium* precisely because the client's own
verification of Phase 4 is still open: [HS #14891, 2026-08-24, jen.penton@magiclite.com]
> "Following up on this - where are we at? Any other updates or are you waiting
on anything from our end?"

### Phase 4 → 5 (Reps Signed In) · ML 2026-08-10 (eCat Online only) / NSL not reached · confidence: high

**What changed:** Beta invitations went out and were redeemed — for the first
time by people outside Magic Lite's head office.

**Evidence:**
- [DB `organization_invitations`] Five invitations created 2026-08-10 19:54:22 by SuperCat: `ryan@electrasalesltd.ca` (ML Reps, **not redeemed**, expired 2026-08-17), `jason@electrasalesltd.ca` (ML Reps, **not redeemed**, expired), `daniel@gslightinggroup.ca` (ML Reps, redeemed 2026-08-10 19:56:14), `mike@nslusa.com` (NSL Reps, redeemed 2026-08-10 22:32:42), `josh.jsna@gmail.com` (NSL Reps, redeemed 2026-08-17 17:57:56).
- [DB `org_users`] `dfrench1994` / daniel@gslightinggroup.ca, ML Reps: `last_ecat_online_login_at` = 2026-08-10 20:13:31. This is the **only** outside-rep session in the org's history.
- [DB] `last_ipad_login_at` is non-null for exactly five org_users, ever: Kylor Johnson (2026-08-25), Kyla Bosch (2026-08-10), Brent Sanders (2026-03-24) — all SuperCat — plus Jen Penton (2026-07-10) and Jason Fisher (2026-08-19). **Zero outside reps have opened the iPad, for either brand.**
- [HS #15008, 2026-08-10, kylor@supercatsolutions.com] > "Please let me know if you would like me to send out the tester invites while we work with Brittini to finalize the formatting."

**Against:** if "signed in" means the iPad app, this phase is **not reached for
either brand**, and the honest answer for NSL is that two people redeemed an
invitation and then did nothing with it. If it means "signed in at all," ML
reached it on 2026-08-10 and NSL has not (neither Krause nor Nelson has a mali
iPad or eCat Online login). **The brief's framing has this exactly backwards:
NSL looks alive because SuperCat's own staff sit in the NSL Reps group.**

### Phase 5 → 6 (Admin Training) · both brands 2026-04-29 (formal) · ongoing operations: not reached · confidence: high

**What changed:** A 68-minute admin training was delivered by Kyla Bosch and
Kylor Johnson to Jen Penton and Jen Zorony.

**Evidence:**
- [CALL, 2026-04-29T17:00Z, "SuperCat / Magic Lite: Admin Training"] Kyla Bosch: > "welcome to officially the support handover."
- [HS #14418, 2026-04-29, kylor@supercatsolutions.com, tags: `type: training`] > "We covered a lot of ground: the Admin Console overview, user management and territory codes, pricing and user group settings, order configuration, and eCat Online."

**Against:** the ongoing-operations half never landed. The training call ended
with Jen Penton unable to reach the Admin Console at all ("I'm still getting a
non-permitted, and I just did all the cash clearing") — resolved live when Kylor
found her admin flag unchecked. Product-file management training was still an
open action item three months later: [HS #14727, 2026-07-15] "SuperCat | Schedule
admin training on product file management (how to update products, pricing,
add/remove items) | Next meeting". And [CALL, 2026-08-04] Jen Penton: > "I have
not played enough around enough. Openly admit it."

### Phase 6 → 7 (Go-Live) · **declared 2026-04-29, retracted 2026-07-10, not reached today** · confidence: high

**What changed:** Nothing durable. This is the transition that the seven-phase
model cannot represent.

**Evidence for the declaration:**
- [CALL, 2026-04-29] Kylor Johnson: > "really we're at a point where this meeting is being recorded and I go live stage of the the implementation process."
- [HS #14728, 2026-07-02, kylor@supercatsolutions.com, internal] > "@kylaB going to let you handle this go-forward as we're billing them and they are \"live\" but classic reply of them coming back up for air."

**Evidence for the retraction:**
- [HS #14728, 2026-07-10, kylor@supercatsolutions.com] > "I wanted to follow up on the \"go-live\" confusion. The data scrape from the website and PDFs were in good shape, and my intent was to get you acclimated with the admin side early so you could see how everything works. In hindsight, that was premature, and it surfaced some key gaps that you both flagged during our initial handoff and again with Kyla this week. That's on me, and I apologize for the added confusion."
- [DB] Zero submitted orders. `order_email_recipient` = ''. Zero smart lists. Zero distribution centers. Zero sales-data imports ever.

**Against:** none. Both parties agree in writing that go-live has not happened.
The current plan, as of 2026-08-04, is beta feedback → fresh inventory → full
rep launch → eCat Online public launch.

---

## C. Current phase as of 2026-08-25

| | Magic Lite | NSL |
|---|---|---|
| **Phase** | **5 (Reps Signed In), partial — eCat Online only** | **4 (Catalog Completeness), with residual gaps** |
| Reps invited outside head office | 3 (Electra ×2, GS Lighting ×1) | 2 (Krause, Nelson) |
| Redeemed | 1 of 3 | 2 of 2 |
| Ever opened eCat Online | 1 (Dan French, 2026-08-10) | 0 |
| Ever opened the iPad | 0 | 0 |
| Catalogue price coverage (visible products) | 114 / 117 priced | 101 / 117 priced |
| Blocking item | fresh inventory feed; 2 unredeemed invites | 16 unpriced visible SKUs; no rep has opened anything |

Org-wide: not go-live, not transacting, formally still in an onboarding →
support transition that was declared once and taken back.

---

## D. Turning points

**1. 2025-11-20 — the decision to scrape the PDF.** [CALL] Brent Sanders:
> "Emory, Emory, Emory, Shared a really comprehensive 2025 catalog. Is that
indicative of your products? ... our thought was like, hey, we could take this
catalog and run with it". The client had no product CSV and SuperCat chose to
manufacture one from a 400-page PDF rather than gate the project on getting
structured data out of GP. Every image, pricing, related-item and cut-sheet
defect for the next eight months descends from this. Kylor named it himself on
2026-03-26: > "It's amazing what AI can do when you – it was so – we were like,
oh, my God, we totally forgot about the website. Like, that's the easiest thing
to scrape than a PDF of 400 pages."

**2. 2026-03-10 — the first near-churn.** [HS #14005, jen.penton@magiclite.com]
> "We are struggling with the demands and admittedly a bit disappointed with the
website scraping/info upload results of supercat." and > "It was part of the
interview that we would not have to do this - literally something that was a
huge deciding factor in going with supercat instead of someone like fathom."
SuperCat's response was correct and immediate — Kylor took the related-items
work back in-house the same day — and the project accelerated sharply through
late March.

**3. 2026-04-29 — the premature handoff.** Support handover was declared, the
onboarding inbox was closed ("moving from like the onboarding inbox"), and the
account moved to Kyla with the catalogue still missing pricing on ~87% of SKUs,
no cut sheets, and wrong images throughout. This is the direct cause of the
July crisis. Kylor's own diagnosis on 2026-07-10 is the best statement of it.

**4. 2026-05-19 → 2026-07-07 — the Distribution Center detour.** [HS #14418,
2026-05-19, kyla@supercatsolutions.com] > "We have set up two Distribution
Centers in SuperCat: one for Magic Lite (ml ) and one for NSL (nsl )... We have
already converted your current inventory data to this format and imported it
successfully." Brittni rebuilt the GP export to that two-rows-per-SKU spec. By
2026-07-22 Kyla had reverted to brand-prefixed columns ("what I've done is I've
created a column specifically for magic-like quantity available"). [DB]
`distribution_centers` for org 285 = **0 rows**; `inventories` = 703 rows, one
per SKU. Seven weeks of integrator work against a spec that was withdrawn — and
this sat on top of an SFTP permission error that took from 2026-06-18 to
2026-08-06 to resolve.

**5. 2026-07-10 — the escalation that saved it.** [HS #14727,
jen.penton@magiclite.com] > "Meeting: Let's meet asap to discuss if and how we
are going to conclude this project." and > "March was the original launch date.
We haven't even begun to pass to the beta to our rep trial group, which was
promised over 2 months ago." Kylor tagged the CEO within two hours
(> "@kjael"); Kjael replied > "@brentS @kylor @kylaB let's have an internal
huddle on this prior to meeting with them so we have dialed plan to
completion." From that point the project runs properly: 15 July CEO-chaired
call, 21 July Craig Shinde's 30-item punch list, 24 July a genuinely detailed
status with owners and ETAs, 28 July a working session, 10 August beta invites.

---

## E. The seven questions the phase model does not ask

### A. Did this client ever go backwards?

Yes, four times, two of them serious.

- **Deliberate stall, 2025-11-20 → 2026-01-20 (61 days).** Agreed at kickoff: year-end plus two new sales managers. Jen P: "the next two or three weeks for me is going to be very busy and no time to crunch data." Not a failure, but the six-week plan was dead before it started.
- **Data regression, 2026-02-27.** The client's own upload dropped SuperCat's added columns. [HS #13861, kylor@] > "the most recent product file upload dropped the 5 custom columns I added previously to support the hierarchy we discussed". Repeated on 2026-03-11: > "some columns were in the wrong order, a chunk of products were missing, and the price level columns got dropped."
- **Near-churn #1, 2026-03-10.** Above. Trigger: two months of the client doing data-entry work they believed they had bought their way out of. Ended by Kylor taking the related-items and hierarchy work back the same day.
- **Silence, 2026-05-19 → 2026-06-18 (30 days) and 2026-06-18 → 2026-07-02.** Zero contact in the corpus for a month after the Distribution Center email, then a single Endeavour update, then another two weeks. Nothing in the DB either: no import of any kind between 2026-05-19 and 2026-07-07 — a 49-day gap in a project that had been importing several times a week.
- **Near-churn #2, 2026-07-10.** The most serious. Trigger: the premature handoff colliding with the discovery that pricing, cut sheets and images were all still broken. Ended by CEO escalation.

### B. Adoption — separate from go-live

Measured from `org_users`, which distinguishes iPad from eCat Online per org.

**iPad, ever, in this org — five people total:**

| Person | Side | Last iPad login |
|---|---|---|
| Kylor Johnson | SuperCat | 2026-08-25 |
| Jason Fisher | NSL (National Sales Manager) | 2026-08-19 |
| Kyla Bosch | SuperCat | 2026-08-10 |
| Jen Penton | ML (COO) | 2026-07-10 |
| Brent Sanders | SuperCat | 2026-03-24 |

**eCat Online, ever, in this org — seven people total:**

| Person | Side | Last eOL login |
|---|---|---|
| Dan French | GS Lighting Group (ML rep agency) | 2026-08-10 |
| Craig Shinde | ML | 2026-08-04 |
| Kyla Bosch | SuperCat | 2026-07-23 |
| Pansy Ali | ML | 2026-05-13 |
| Marquel Cardenas | ML | 2026-04-30 |
| Jen Penton | ML | 2026-04-29 |
| Jen Zorony | ML | 2026-02-03 |

**What they did:** browsed. Zero orders, zero quotes, zero presentations, zero
smart lists, zero sales-data records. The only artefact any session produced is
one empty cart (see F).

**Invitations:** 16 issued over the org's life; 12 redeemed, 4 never (Pansy's
first, Tom Penton, and both Electra Sales reps). Redemption rate on the
2026-08-10 beta batch: 3 of 5.

**The brand asymmetry is the opposite of what it looks like.** All eight
client-side eOL/iPad users except Jason Fisher, Patricia Krpic and Michelle
Coleman are Magic Lite. The one outside rep is Magic Lite. NSL's apparent
activity is SuperCat's own three accounts sitting in the NSL Reps group.

### C. Current trajectory

**Improving, from a low base, and fragile.**

For:
- Beta invites issued and 3 of 5 redeemed (2026-08-10 / 08-17) — the first real forward motion on adoption in the project's life.
- First successful automated inventory import 2026-08-12 15:38, after two failures (2026-08-06 fatal, 2026-08-10 error).
- Recurring schedule confirmed [HS #14891, 2026-08-25, bpryputniski@]: > "This powershell script has been scheduled to run Monday to Friday at 6AM EST and 11:59AM EST."
- Client sentiment recovered: [CALL, 2026-07-28] Jen Penton: > "a lot of progress, a lot of work. I'm relieved. We're getting there."
- Client is chasing SuperCat, not the reverse [HS #14891, 2026-08-24].

Against:
- **No inventory import between 2026-08-12 and 2026-08-25** despite the schedule being announced — the automated feed has run successfully exactly once.
- [DB `import_events`] 2026-08-25 19:41 Products import: **102 errors**, `Invalid CategoryCodes code: '["LIGHT"]'` — JSON array syntax leaked into the CSV. Re-run clean 13 minutes later, but this is SuperCat's own file, on the snapshot date.
- Both 2026-08-25 product imports warn that seven custom fields are *missing from the file* — including `MountingType`, `Wattage`, `Applications`, `ProductFamily`, the exact fields Kyla enabled as iPad filters on 2026-05-19. The same column-dropping regression SuperCat warned the client about in February is now in SuperCat's own export.
- The three reps who redeemed have not opened the iPad.
- Zero smart lists. Kjael on 2026-07-28: > "smart list, just as a concept for both of you all, is the biggest point of leverage to put the sales execution on rails." Nobody built one.

### D. Was the catalog ever *wrong* while the imports looked *clean*?

**Continuously, for five months, and the import log could never have told anyone.**

[DB] There have been **86 `Images` imports** in this org's history and **not one
of them has ever recorded a single error or fatal.** Every one is clean or
warning tier. The importer verifies that a JPEG exists and that its filename
matches `ImageFileName`. It has no way to know the JPEG is a picture of
something else. (For contrast: 12 of 14 `Customers` imports and 37 of 109
`Products` imports carry errors or fatals. Images is the one file type whose
correctness the log cannot speak to at all.)

The dated collisions:

| Import log | Client, at the same time |
|---|---|
| 2026-03-19 / 03-20 / 03-23 / 03-24 — **36 Images imports, every one clean** | [CALL, 2026-03-26] Jen Penton: > "I think those J's are actually jumper cables, not. So just use the second image instead of the first one." and > "Like that's a jumper, that's a jumper cable. That's the product. That's The 12-inch product is not 560." |
| 2026-04-28 — 4 Images imports, clean; 2026-07-23 / 07-24 / 07-27 / 07-28 — 30 more, all clean | [HS #14727, 2026-07-21, jen@magiclite.com] a 30-line punch list: > "The pictures of the eStrip connectors are just pictures of the eStrip itself." > "All the outdoor sconce pictures (including the application photos) are pictures of the SL-CC (wrong)" > "The non-dimmable driver pictures are dimmable drivers." > "All construction plates in the downlight section-pictures wrong" |
| 2026-08-03 — 1 Images import, clean | [CALL, 2026-07-28] Jen Penton, five days earlier, still finding them live: > "When you go into related items of that 120-volt strip that you were just in, it's showing the wrong extrusion" |

The scale: [CALL, 2026-07-22] Kyla Bosch: > "We were able to update 104 images
from the old file and correct them. However, it seems like we still have
mismatched images"; > "It's only 68 compared to where we were." A further 130
fixes were applied on 2026-07-24. So on the order of **200 of ~725 products
carried a wrong image** while every image import in the log read clean.

Two more of the same species:
- **Product stories.** [HS #14727, 2026-07-08, kylor@] > "We've re-imported the stories file and all 695 products now have a product story populated." [DB] 660 of 725 active products have a story today; 65 do not. The stories import on 2026-07-08 was error-tier.
- **Inventory, 2026-08-12.** Kylor to Brittni [HS #14891, 2026-08-12] > "The file imported cleanly and ML warehouse quantities are showing on the active catalog items." The import log for that file is warning-tier with rows silently discarded: `'Line 3: Product not found, record ignored., BaseItemCode=ES-120V-27K-XX'`, `YH-HRF50CA120S-505060RGB`, `YH-RGB-PC-10` and others. "Imported cleanly" is the reading of a status word, not of the file.

### E. Placeholders, and pointers to things that no longer exist

**Placeholder pricing: no.** Only four active products sit at `net_price = 1.00`
(`LV-RD54/55-EC-WF`, `LV-RD54/55-EC`, `LES-STCN`, `NFLX-PINS`) and each carries
differentiated brand prices — e.g. `{"mllist":1.0,"mldn":0.5,"nsllist":1.4,"nsldn":0.7}`.
These are real prices for cheap parts, not a `$1.00` placeholder pattern.

**Placeholder *data*: yes, deliberately, and now cleaned.** To force the customer
import through, SuperCat wrote junk into required fields. [CALL, 2026-03-19]
Kylor Johnson: > "there was a lot of, like, initial errors just of, like,
missing email addresses, some states and zip codes not filled out. And so what I
went ahead and did just to bypass that was, like, through zeros or dashes in
there so that the import would work." Quantified a week later [HS #14217,
2026-03-26]: > "2,735 customer records with \"TBD\" placeholder values that need
real billing addresses before import." [DB] Today: **zero** rows contain `TBD`,
`-`, `0` or blank in address1 / city / state / post code / country. The client
did clean it — ML on 2026-04-07, NSL on 2026-04-27.

**Pointers to things that don't exist: four.**

1. **A price level that never existed.** [DB `audit_log_entries`] 2026-07-15 20:24:32 — `MobileSite updated {"id":151,"price_level_id":5722}`. There is **no `price_levels` row with id 5722 in any organization.** The Magic Lite eCat Online site pointed at a nonexistent price level for eight days, until it was set to 5665 (ML DN) on 2026-07-23 16:39. This window contains Jen Zorony's 2026-07-20 report: > "NSL -pricing is wrong (looks like ML pricing) and it still has CAD."
2. **A deleted eCat Online site.** `MobileSite id=150, url_key="1"` was created by Brent on 2026-01-20 and no longer exists in the table. The "quick reference links" block in the 2026-04-29 admin-training follow-up — the document the client was told to keep — lists `eCat Online [eOL]: https://supercat.supercatsolutions.com/mali/e/1/login`. That link points at a deleted site. The live sites are `/mali/e/12` (ML) and `/mali/e/13` (NSL).
3. **A link into a different customer's org.** [HS #14217, 2026-03-31, kylor@] the bulk-invite instructions read > "Go to Admin Console → Users → Invitations → Invite Users:https://supercat.supercatsolutions.com/supercat/**tcd**/admin/invitations/new". `tcd` is a different SuperCat client's shortname.
4. **Inventory rows for products that aren't in the catalogue** — the 2026-08-12 `Product not found, record ignored` warnings above.

**And one live credential in plaintext:** the mali SFTP password appears
unredacted in [HS #14329, 2026-04-15] and again inside Brittni's pasted
PowerShell in [HS #14743, 2026-07-07]. Not a data-quality issue, but it is in
the record.

### F. What `audit_log_entries` actually shows

I confirmed `RAWSTATE`'s counts and then went past them. Matching on
`data::text ILIKE '%"organization":"mali"%'` returns **80 rows**, not the nine
that `RAWSTATE`'s `OrgUser created` / `OrgUser destroyd` summary implies. Those
nine are right (6 created, 4 destroyed, correct by month) — but they are 11% of
the table's content for this org. The rest is `OrgUser updated` (49) and
`MobileSite created`/`updated` (17), and the MobileSite trail is the only
first-hand record of how eCat Online was actually built.

**No customer account was ever destroyed.** All four `OrgUser destroyd` events
target SuperCat's own accounts:
- 2026-04-09 17:18:01 and 17:18:06 — two deletions on `User 72428` = `support@supercatsolutions.com`, fired *during* the 17:00 Integration Discussion call with Brittni and both Jens. Unmentioned on the call.
- 2026-05-13 17:28:42 and 2026-07-09 20:19:40 — the same shared support account again.

This is the direct opposite of the pebl finding the brief warns about. Here the
audit log's value is elsewhere:

- **2026-01-20 15:54:09** `MobileSite created {"url_key":"1"}` by Brent, 24 minutes into the onboarding call — the moment eCat Online was switched on, matching Brent's "I'm going to turn on what's called a mobile site" verbatim. 35 minutes later it was set to `allows_unauthenticated_users: true`.
- **2026-04-29 00:00:23** `MobileSite created {"url_key":"12"}` — six minutes before Kylor's 00:06:52 email announcing "eCat Online is live."
- **2026-07-09 21:55:54** `hide_products_marked_hideable: true`, then **22:28:13** back to `false`. A 32-minute experiment with hiding the hero-variant products on eCat Online, reverted, recorded nowhere else.
- **2026-07-15 20:24:35** `MobileSite created {"url_key":"13","title":"National Specialty Lighting"}` — the brand split made real.
- **2026-07-22 17:44:44** `support` account `customer_number` set to `"913"` — Jen Zorony on that call: "Okay, can you put in, just put in customer 913?" The audit log timestamps a live debugging step.

**The blind spot inside the blind spot:** the three org_users created in August
— `dfrench1994` (2026-08-10), `Rockymountain` (2026-08-10), `josh_jsna`
(2026-08-17) — have **no audit entries at all**. The last audit row for this org
is 2026-08-03 20:56:09. Self-enrolment through an invitation link does not write
to `audit_log_entries`. So the single most important adoption event in this
project's history is invisible in the table that is supposed to catch what
HelpScout and Fathom miss. It is visible only in `organization_invitations`.

### G. What "using the system" means here, and has anything completed?

For this client, "using the system" was never going to mean writing orders. It
means three separable things, and only one of them is happening:

1. **Answering "what's the price / what's in stock?" without calling head office.** This is the actual purchase justification, stated at the intro call and again at the end: [CALL, 2026-07-28] Jen Penton: > "a lot of the questions are just, oh, price and availabilities. If we have this, it'll save us a lot of time internally." Status: possible for ML, partly broken for NSL (16 unpriced visible SKUs), and untested because inventory has been refreshed once.
2. **Sending a quote or a presentation to a distributor.** Zero have been sent. Order type is configured as *Quote*; no rep has produced one.
3. **Taking a cart from a distributor via eCat Online.** Both storefronts have `enable_online_ordering = true` and `allows_authenticated_users = true` / `allows_unauthenticated_users = false`. No customer has ever been enrolled: `enrollment_applicants` = 0.

**Has anything completed?** One thing, and only in the last fifteen days: the
ERP inventory pipeline. GP → PowerShell → SFTP `/data/inventory.csv` ran end to
end successfully on 2026-08-12 and is scheduled twice daily from 2026-08-25.
Nothing else in the project has reached a state where it runs without someone
at SuperCat driving it.

---

## F. The zero-order question, answered

**Why has this client never submitted an order?**

Because it was never asked to, by design, and then nobody who could was given
the app.

1. **Ordering was scoped out of this phase by the client, in writing, in March.** [HS #14005, 2026-03-10, jen@magiclite.com] > "Ship to addresses- I understand we are not entering orders through SuperCat at this time so we do not need to include the ship to's. Some customers have quite a few and some change every time the have an order." Ship-to data — required to complete an order — was deliberately excluded from the 3,418-row customer file. That single decision makes zero orders the expected state, not an anomaly.
2. **What eCat produces here is a quote, not a booking.** [HS #14418, 2026-04-29] action item 9: "Configure PO number and ship-to as required fields; set default order type to Quote." Jen Zorony on that call: > "Yeah, I think if we have it as quote and a purchase order is still required to be sent in." and > "we would enter the order in our NGP and our CSR would email that customer directly with their confirmation." SuperCat was never going to be the system of record for an order at Magic Lite; GP is.
3. **No rep who could write one has ever opened the app.** [DB] Outside-rep iPad logins: zero, for both brands, over the org's entire history. The only client-side iPad users are the COO and NSL's National Sales Manager.
4. **Go-live never happened.** Beta invites went out 2026-08-10 — fifteen days ago — explicitly caveated as look-and-feel only. [CALL, 2026-08-04] Kylor Johnson: > "the caveat with this initial beta testers are, you know, it's more of like a UI, UX look and feel... but hey, you know, inventory hasn't been refreshed in like six months." Kjael, same call: > "if we launch without that data, you're setting yourself up for a shmillion. Calls from your sales reps about what's in stock, what's not. So it's like, we do not want, it's worth waiting."
5. **The empty `order_email_recipient` is a symptom, not the cause.** It is one field under Tools → Company Settings → Order Preferences, handed to the client on 2026-04-29 and never filled. But user-group templates supersede org settings, and Kyla did populate the per-group Order Email Recipient on 2026-07-24 ("Email templates: Understood. We have completed the remaining template sections using your contact details"). A submitted order would have routed. The blank field is evidence that the org-level order configuration was never finished — which is consistent with everything else — not evidence that an order was written and lost.

**The one row in `orders`.** [DB] There is exactly one: id 1700808, created
2026-07-15 17:25:07, `order_state = 'cart'`, `order_source = 'server'`,
`is_submitted = NULL`, no items, no total, no customer, order number
`155369-07152026-1-S`. `org_user_id 155369` is SuperCat's shared `support`
account. The 2026-07-15 call ran 17:00–17:45; at ~24 minutes in, Kyla Bosch was
demonstrating the eCat Online cart to Jen Zorony. The only object ever created
in this org's order table is SuperCat's own demo cart, abandoned mid-screen-share.

> Note on the brief's phrasing: `orders WHERE is_submitted = 0` returns **zero
> rows**, because `is_submitted` on that row is `NULL`, not `0`. `count(*)` on
> the table returns 1. The conclusion is unchanged; the query is not.

**Does anyone appear to have noticed?** No — and correctly so. In 266 threads
and 18 calls, nobody asks why there are no orders, because with no reps live
there is nothing to explain. The closest anyone comes is Kyla, using it as a
convenience: [CALL, 2026-05-19] > "I think because we don't have any reps logged
in at the moment, is that correct, Jen? So they're not actively using eCat yet.
We can do that and then see how the data pulls through." Zero orders was
understood by both sides as the state of a project that had not launched.
Whether anyone will notice if it *stays* zero after the rep launch is the open
question.

---

## Contradictions with `RAWSTATE_mali.json`

Flagged as instructed. The snapshot is not wrong so much as compressed in ways
that invert the conclusion.

1. **`"status": "active"`.** `organizations` has no `status` column. It has
   `state`, which is a geographic field (81 orgs have `''`, 31 have `'NC'`).
   Org 285's `state` is `''`. `import_active` is `NULL`. There is no column in
   `organizations` that says this org is active. Whatever "active" came from,
   it is not this table.
2. **`user_types[].ever_logged_in` counts iPad logins only.** Verified: filtering
   `org_users` on `last_ipad_login_at IS NOT NULL` reproduces the snapshot's
   numbers exactly for all seven groups. Counting `last_ecat_online_login_at`
   instead gives ML Reps **4 of 5**, most recent 2026-08-10 — not 0. The
   snapshot's `most_recent_login: null` for ML Reps, and the handoff's headline
   "The entire Magic Lite rep team has never signed in," are both artefacts of
   an iPad-only definition.
3. **`"NSL Reps": ever_logged_in 3, active_30d 3, most_recent_login 2026-08-25`.**
   All three are `Kylor_Johnson`, `kyla` and `jasonf`. Two are SuperCat
   employees. `most_recent_login: 2026-08-25` is SuperCat's own Head of Customer
   Success logging in on the day of capture. Read as rep adoption, this row is
   the reverse of the truth.
4. **`orders_summary.submitted: 0` is right; "Zero submitted orders" understates.**
   There is one order row — an empty SuperCat demo cart (above).
5. **`audit_log.note: "Modest activity here"`.** 80 rows, not 9. The counts
   quoted are correct for the two event types chosen; `MobileSite` and
   `OrgUser updated` events — which contain the only record of how eCat Online
   was built and of the 2026-07-09 hideable-products experiment — are excluded.
   And the three August rep enrolments appear in *neither* the audit log nor the
   corpus.
6. **`inventory_rows: 703` is correct but should not be read as brand-split.**
   All 703 rows are ML-warehouse rows from Brittni's GP export; NSL quantities
   are carried in `NSL_*` columns on the same row. `distribution_centers` = 0,
   despite the 2026-05-19 email stating two were created.

---

## Before-finishing checklist

1. **Does every transition have a date and evidence, or an explicit
   `undetermined`?** Yes. Seven transitions, each with a date (or a per-brand
   pair), a verbatim quote or a specific DB fact, and an "Against" section.
   Phase 6→7 is dated as *declared and retracted* rather than reached, which is
   the accurate answer; Phase 2→3 carries two dates because the question admits
   two readings, and I have given both rather than picking one silently.
2. **Is every quote verbatim, with author and timestamp?** Yes. Every quoted
   string was copied from the corpus and spot-checked with `grep` against the
   source files. No paraphrase appears inside quotation marks. DB facts are
   marked `[DB]` and were obtained by direct SQL, not from `RAWSTATE`.
3. **Did I read both corpus parts in full?** Yes, both, in order.
   **What I skimmed:** tickets #13582–#13631 — 50 automated "New Onboarding File
   Upload" notifications from 2025-12-23, spanning corpus lines 1150–3199. I read
   five in full, confirmed they are byte-identical boilerplate apart from
   filename and size, and extracted the filename and timestamp from all 50
   programmatically rather than reading the remaining 45 line by line. Nothing
   else was skimmed.
4. **Forbidden files avoided?** Confirmed — see the contamination statement at
   the top.
5. **Are ML and NSL treated separately wherever the evidence differs?** Yes:
   Phases 4, 5 and the Current Phase table are split by brand; adoption, pricing
   coverage, invitation redemption and catalogue defects are reported per brand.
   Phases 1–3 are not split, because through March there was one product file,
   one import pipeline and one catalogue — splitting them would invent a
   distinction the evidence does not support.
6. **Contradictions with `RAWSTATE` flagged?** Yes — six, in the section above.
