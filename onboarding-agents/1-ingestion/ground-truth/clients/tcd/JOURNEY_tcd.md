# JOURNEY — Terracotta Designs (`tcd`), org 282

> Independent reconstruction from `CORPUS_tcd.md` (read start to finish, all 5,517
> lines, nothing skimmed) and `RAWSTATE_tcd.json`, plus read-only queries against
> `supercat-postgres-vpn`. Written before reading any client profile, handoff,
> registry, or framework document.

**Contamination disclosure.** I opened none of the forbidden files and invoked no
`ecat-*` skill. Two things were nonetheless in my context without my choosing, and
you should know about them: (1) the workspace `CLAUDE.md` is auto-injected by the
harness and contains eCat import ground truth — including the meanings of
fatal/error/warning tiers and the `/data` vs `/images` FTP split. That is
mechanics, not phase doctrine, but it did inform how I read the import history.
(2) The one-line *descriptions* of the `ecat-*` skills appear in my tool listing
(e.g. "take an org from data-loaded to rep-ready"). I loaded none of their content.
Neither source told me what a phase is or when one ends.

---

## Narrative

Terracotta Designs is a two-brand residential lighting importer in Liberty Hill,
Texas — Terracotta Designs and Kanova & Co — run day-to-day for this project by one
person, Scott Tang, a former software engineer who also maintains the company's
in-house ERP and CRM. The org was created 2025-10-16; Scott filled in the
onboarding questionnaire on 2025-10-31 and met Brent Sanders, SuperCat's CTO, for a
60-minute kickoff on 2025-11-11. That call went unusually well: Scott's spreadsheets
were already close to eCat's product format, and Brent had products imported the
same day.

Then it stopped being about data. Within six weeks Scott had decided the iPad app
itself was the problem. He wanted the product detail page laid out his way, the
left-hand nav to say "Brands" and not "Collections", the SKU and dimensions promoted
to the top, the co-branded logo rendered correctly. On 2025-12-21 he wrote that the
tool "feels less like a mature commercial product and more like an early-stage
amateur implementation" and that, had he known, he "likely would not have signed up."
Brent's private reaction leaked into the ticket thread. The project came close to
ending there.

What followed was a four-month stall. Dallas Market prep, the market itself (where
Kylor Johnson — who had taken over the account on 2025-12-08 — met Scott in person),
then two weeks in China, then a backlog. Between 2025-12-27 and 2026-04-19 the only
things that moved were a handful of product re-imports and Scott's repeated request
for the same UI controls. SuperCat's position hardened: on 2026-02-24 Brent wrote
that "the catalog looks empty and the product feels broken due to the lack of data"
and asked whether eCat was still a fit. Scott replied the same morning that "the
user interface is the only showstopper for us." They met anyway that afternoon.

That 45-minute screen-share is the hinge of the whole engagement. Brent walked Scott
through custom fields, company settings, field ordering, related items and the
stories file, and Scott's posture flipped inside the call — "I know where to start.
Otherwise, I don't know where to start." Everything that had been stuck for four
months got unstuck over the next eight weeks: new 2026 price sheets and products
(March), a fatal products import debugged by Brent (2026-03-13), the first stories
file (2026-03-28), and finally the customer file, which took four attempts across
2026-04-05 to 2026-04-20 before importing clean.

The customer file was the real gate. On 2026-04-20 Kylor found that Scott's own admin
user had no territory codes, pasted all 40 in, and the iPad populated. Scott replied
on 2026-04-23: "now I can see the customers on my iPAD... overall, it is in good
shape now. What is the next step. Should I invite users ( our sales reps) now?" He
sent the first eight invitations that same evening. Reps started signing in on
2026-04-25.

From there onboarding effectively ended and support began. Kylor handed the account
to Kyla Bosch on 2026-04-27, cc'ing the Chief of Staff for invoicing; Kyla declared
onboarding complete on 2026-04-28. The admin training that was supposed to close the
loop never happened — Scott missed it on 2026-05-05, missed it again around
2026-05-13, and on 2026-05-14 said he would work from the documentation instead.
Kyla substituted a written audit of the org, which is the only "training" artifact
that exists.

Today the org is live and maintained. Products imported clean on 2026-08-15,
inventory this morning, 397 products, 346 customers, 24 reps — seven of whom logged
into the iPad today. But adoption is thin in one specific way: of those 24 reps,
exactly one, JC Gonzalez in South Florida, has ever created an order. All seven
submitted orders are his, between 2026-06-24 and 2026-07-18. No SmartLists were ever
built, no rep training was ever scheduled, and nothing at all appears in the record
between 2026-05-15 and 2026-07-16 — the exact window in which those orders were
written.

---

## A. Cast

### SuperCat

| Person | Email(s) | Role | First seen | Last seen |
|---|---|---|---|---|
| **Brent Sanders** | brent@supercatsolutions.com (`brentsanders`) | CTO; ran kickoff and all early data work | 2025-10-16 (org_user created 13:24:02, [DB]); first in corpus 2025-11-11 kickoff call | 2026-03-13 (#14152, import-error diagnosis). Last iPad login 2026-02-24 [DB] |
| **Kylor Johnson** | kylor@supercatsolutions.com, onboarding@supercatsolutions.com (`Kylor_Johnson`, kylor22johnson@gmail.com) | Onboarding owner from Dec 2025 | 2025-12-08 (#13448); org_user created 2025-11-21 18:32 [DB] | 2026-05-05 (call with Kyla). Last written contact 2026-04-29 (#14411) |
| **Kyla Bosch** | kyla@supercatsolutions.com, support@supercatsolutions.com | Introduced by Kylor as "our Head of Support"; signs as "Onboarding & Implementation Manager" | 2026-04-24 21:08 (#14375); org_user created 2026-04-26 [DB] | 2026-08-03 (#14874) — current owner |
| **Angie** | — | "our Chief of Staff", cc'd 2026-04-27 to send invoice details | 2026-04-27 (#14402, mentioned) | never appears directly |
| **Emery** | — | Named by Brent on the kickoff call as SuperCat's California person; reappears as a stray token in Kyla's 2026-04-28 template ("Separately, Emery, we'll schedule a session with your sales team") | 2025-11-11 | 2026-04-28 |
| **bruce** | — | @-mentioned internally by Kyla 2026-04-24 re: invite-flow UX | 2026-04-24 | 2026-04-24 |

**Authorship handoffs — three, all datable:**

1. **Brent → Kylor, 2025-12-08.** Kylor introduces himself in-thread: *"I wanted to
   quickly introduce myself, as I recently joined the team at SuperCat and have been
   working with Brent to get up to speed on your project."* Brent does not leave —
   he stays on as the technical escalation through 2026-03-13 — but from this date
   Kylor writes the cadence emails. (One artifact of the transition: Kylor's
   2025-12-12 21:35 reply is signed **"Brent"**.)
2. **Kylor → Kyla, 2026-04-27.** *"I've looped in Kyla (cc'd), our Head of Support,
   who will be your primary point of contact from here on out."* (#14402)
3. **Kyla assumes ownership, 2026-04-28.** *"My name is Kyla, and I'll be your
   primary point of contact at SuperCat going forward. Kylor has done a great job
   getting Terracotta Designs through onboarding."* (#14411)

### Terracotta Designs

| Person | Email(s) | Role | First seen | Last seen |
|---|---|---|---|---|
| **Scott Tang** | scott.tang@terracottalighting.com · sales@terracottalighting.com · terracottalighting@gmail.com (`TerraCat`, admin) | Sole client-side admin and project owner. Ex-software engineer; also runs their in-house ERP/CRM | org_user created 2025-10-31 23:03:14 [DB]; questionnaire 2025-10-31 23:11 (#13379) | 2026-08-03 (#14874). Last iPad login 2026-08-18 14:36 [DB] |

Scott operates from **three** addresses and signs some of them "Sales Operations" —
the same phone/fax block and the same voice throughout. `terracottalighting@gmail.com`
is where SuperCat's automated import-error notifications land, which is why two
import escalations (#14471, #14476) surface under a gmail.com customer domain.

### Reps who appear by name in the corpus

| Person | Email | Agency / territory | In DB as | First seen | Last seen |
|---|---|---|---|---|---|
| **Cindy Vackar** | cindyvackar@vackaragency.com | Vackar Agency, TX | `cindyvackar`, TX | 2026-04-23 (fwd inside #14371) | 2026-04-30 (#14420) |
| **Clyde Cutrer, III** | cmcutrer@gmail.com / clydecutrer@markneallighting.com | MNL Sales Agency, LA/MS | `ccutrer`, LA,MS | 2026-04-24 (#14380) | 2026-04-27 (#14380) |
| **Todd Neal** | toddneal@markneallighting.com | President, Mark Neal Lighting | `toddneal`, AR,MS,TN-W,LA | 2026-04-24 (cc on #14379) | 2026-07-16 (#14790) |
| **Angie Schaefer-Kist** | alice74x@gmail.com · orderstjs7143@gmail.com · Alice74@fuse.net | T.J. Schaefer Associates, Cincinnati | `schaefer`, KY,OH,PA-W | 2026-04-30 (#14421) | 2026-05-01 (#14421) |
| **JC Gonzalez** | jc@finelightsales.com | Fine Light Sales, FL-S | `JCGonzalez`, FL-S | 2026-04-25 (#14375, named as "FL rep... username is JCGonzalez") | 2026-08-03 (#14874) |
| **Keith Eichenblatt** | keith.lighting@yahoo.com | Greenway Resource, FL | `keith`, FL-S | 2026-08-03 (#14874) | 2026-08-03 |
| **Forrest Denbow** | forrestdenbow@vackaragency.com | Vackar Agency | *not a user* | 2026-04-23 | 2026-04-24 |

The other 18 active reps never appear in the corpus at all. All 24 are on personal or
rep-agency domains; **only Scott sits on `terracottalighting.com`**.

### Not part of this account

| Person | Email | Why they appear |
|---|---|---|
| **David Solis** | davids@maximlighting.com | Ticket #11412, 2024-09-19 — a Maxim Lighting support question, 13 months before the org existed |
| **Christina Sabo** | cs.ecls@outlook.com | Emerald Coast Lighting Sales. "Terracotta Designs" appears **only in her email signature**, in a list of ten lines her agency carries. This is the mention-token false positive that pulled #11412 into the corpus |

---

## B. Phase transitions

### Phase 0 → 1 · Discovery / Kickoff · 2025-11-11 · confidence: high

**What changed:** SuperCat and Scott held a scheduled 60-minute kickoff in which
price levels were created live, the data model was walked through, and concrete
follow-ups were assigned to both sides.

**Evidence:**
- [DB] `organizations.created_at` = 2025-10-16T13:23:33; `org_users` for
  brent@supercatsolutions.com created 2025-10-16T13:24:02 (one minute later).
- [DB] `org_users` for scott.tang@terracottalighting.com (`TerraCat`, is_admin=true)
  created 2025-10-31T23:03:14 — eight minutes before the questionnaire notification.
- [HS #13379, 2025-10-31T23:11:09, noreply@supercatsolutions.com (system)]
  > "Onboarding Questionnaire Completed
  > Organization: Terracotta Designs (tcd)
  > Completed: October 31, 2025 at 11:11 PM UTC"
- [HS #13380, 2025-10-31T23:40:48, noreply@supercatsolutions.com (system)] first
  onboarding file upload: `Screenshot 2025-10-31 at 10.17.02 AM.png`, 71.9 KB.
- [CALL, 2025-11-11T14:00, Brent Sanders (SuperCat)]
  > "So, on this call...    Well, wanted to just provide, you know, a little bit of introduction to the system that you'll be working with to get the data into the sales experience."
- [CALL, 2025-11-11T14:00, Scott Tang (Terracotta Designs)]
  > "Okay.    Good.    Good.    Yeah.    I think that finally we started.    And thank you very much to the, you know, the initiatives of the meeting.    And, yeah, we kind of move forward, you know.    Great.    Yeah."
- [DB] `price_levels` created on this call and still present today: `dn` Dealer Net
  ×1.0, `ns` Designer Price ×1.25, `imap` IMAP ×2.0, `show50` Showroom 50% ×0.5.

**Against:** The org record and Brent's account predate the kickoff by 26 days, so a
framework anchored on org creation would date this 2025-10-16. Nothing happened in
that window — the first client artifact is 2025-10-31.

---

### Phase 1 → 2 · Initial Import · 2025-11-11 · confidence: high

**What changed:** The products file was imported. Same calendar day as kickoff.

**Evidence:**
- [DB] `import_history` first row of the entire timeline:
  `{"d": "2025-11-11", "type": "Products", "clean": 2, "warning": 2, "error": 1, "fatal": 2}`
- [HS #13421, 2025-11-11T19:23:53, brent@supercatsolutions.com (SuperCat)]
  > "As of now, you should be able to use your same credentials you've setup online to access your catalog directly on the eCat iPad app. Feel free to download the app and login to start viewing your catalog in its current state. I've also attached the products file to this thread."

**Against:** Two caveats that matter for how this phase should be read.
1. **SuperCat performed this import, not the client.** Brent built the file from
   Scott's two spreadsheets and uploaded it himself: *"I'm going to take the data
   based on our kind of discussion... I'll be uploading the initial product file"*
   (kickoff call, 00:16:01 / 00:27:46). If "has the products file been imported" is
   meant as a signal of client capability, it is over-read here by about six weeks.
2. The 2025-11-11 block set contains 2 fatals. The first genuinely clean products
   day is **2025-11-25** (clean 5, warning 4). The client's own first successful
   upload is 2025-11-22→24, after a false start on 2025-11-17 caused by using the
   filename `products-251117-Scott.csv` instead of `products.csv`.

---

### Phase 2 → 3 · Progress · 2025-12-09 · confidence: medium

**What changed:** A second core file type landed with no fatal on the most recent
block — inventory, from files Scott supplied on 2025-12-08.

**Evidence:**
- [HS #13448, 2025-12-08T22:38:47, scott.tang@terracottalighting.com (customer)]
  > "We do have Inventory files - Terracotta and Kanova has separate inventory files, See attached. This is the format we sent it to our partners. Hope the format works with SuperCAT as well."
- [DB] `import_history`: `{"d": "2025-12-09", "type": "Inventory", "warning": 1}` —
  warning tier, not fatal. Next inventory 2025-12-19, also warning.
- [CALL, 2026-02-24T19:30, Brent Sanders (SuperCat), 00:23:40]
  > "Cool.    Yeah.    It's a really simple file and it looks like, yes, we have inventory from mid-December and I'll just show you."

**Against:** An earlier reading is defensible. Options, option groups and matrix
options all imported on **2025-11-25** with clean latest blocks
(`{"Options": clean 5, error 3}`, `{"Option Groups": clean 4, error 4}`,
`{"Matrix Options": clean 2, warning 4}`), and `latest_per_type` still shows all
three as 2025-11-25/clean today. If options count as a core file, this transition is
2025-11-25. I chose inventory because options were an experiment Brent built and then
reversed — see Turning Point 1 — whereas inventory was client-supplied production
data. Confidence is medium precisely because of this ambiguity, not because the
dates are uncertain.

---

### Phase 3 → 4 · Catalog Completeness · 2026-04-23 · confidence: high

**What changed:** The customer file finally imported clean, Scott's admin user got
territory codes so the iPad would actually render customers, and Scott declared the
catalog usable. Until this date no order could be written at all, because in eCat an
order starts from a customer.

**Evidence:**
- [HS #13448, 2025-12-21T14:37:35, brent@supercatsolutions.com (SuperCat)] — why
  this was the gate, stated four months early:
  > "We see that 100% of successful orders start with the customer selected first. Having this missing data impacts the sales experience you are seeing."
- [DB] `import_history`, the four-attempt customer arc:
  `2026-04-05 error 2 fatal 1` → `2026-04-18 error 1 fatal 1` →
  `2026-04-19 clean 1 error 7` → `2026-04-20 clean 1` → `2026-04-23 clean 1`.
- [HS #14280, 2026-04-20T00:12:51, scott.tang@terracottalighting.com (customer)]
  > "I finally successfully uploaded the customer file. However, when I open my iPA, somehow I can't see any customers"
- [HS #14280, 2026-04-20T17:23:05, kylor@supercatsolutions.com (SuperCat)]
  > "The reason you weren't seeing customers on the iPad was that your user account in the Admin Console didn't have any Territory Codes assigned, so the sync had nothing to match against."
- [DB] Scott's `org_users.territory_codes` today still holds exactly the 40-code
  string Kylor pasted, lowercase typo `FL-s` included:
  `["AL","AR","AZ","CA","CA-N","CA-S","CO","FL","FL-P","FL-S","FL-s","GA","IA","ID","IL","IN","KS","KY","LA","MD","MN","MO","MS","MT","NC","NJ","NY","OH","PA","PA-E","PA-P","SC","SD","TN","TN-E","TN-W","TX","UT","VA","WI"]`
- [HS #14280, 2026-04-23T15:19:19, scott.tang@terracottalighting.com (customer)]
  > "I fixed some issues you mentioned in customer files, and now I can see the customers on my iPAD. I also updated inventory as well.
  > While I may continue to improve data going forward, but overall, it is in good shape now.
  > What is the next step. Should I invite users ( our sales reps) now?"
- [DB] 346 customers today, 0 with unresolved DefaultPriceCode, 0 without territory.

**Against:** Product Stories — the file Brent named on 2025-12-21 as the specific
thing making the product page "look broken" — was **not** clean on this date. First
stories import 2026-03-28 (clean 2, warning 2, **fatal 2**); a further 4 fatals on
2026-05-07; not clean until **2026-07-05**. On a strict "buildable as a live iPad"
reading, stories were still broken for another ten weeks. I still date the transition
2026-04-23 because customers, not stories, were the blocking dependency for the
selling motion, and because Scott himself declares the catalog good here.

---

### Phase 4 → 5 · Reps Signed In · 2026-04-25 · confidence: high

**What changed:** Reps stopped being a plan and became users on iPads. Note this
begins **the same evening** Scott asked whether he should invite them — phases 4 and
5 are not separated in time for this client.

**Evidence:**
- [DB] `organization_invitations` by day: 2026-04-23 → 8 sent / 6 redeemed;
  04-24 → 5/4; 04-27 → 4/4; 04-28 → 6/2; 04-29 → 2/0. First rep `org_user` row
  created **2026-04-23T23:35:06** (jimhcfs@gmail.com, `jimhickey`).
- [HS #14371, forwarded, 2026-04-23T18:26:32 CT, Sales@terracottalighting.com (Scott)]
  > "I just sent you an eCAT trial invitation.  It is not officially launched.
  > I am still working on it now.  Your Feedback will be apprecaicte."
- First hard evidence of an actual iPad **sign-in** —
  [HS #14375, 2026-04-25T17:43:59, sales@terracottalighting.com (customer)]
  > "One of our rep - FL rep reported that our brand are blacked out when he sign in his ecAT account - see attached
  > His username is JCGonzalez"
- [HS #14420, 2026-04-30T04:31:44, cindyvackar@vackaragency.com (rep)]
  > "So I signed on Monday and Terracotta/Kanova loaded on my eCat. I went through both brands and pulled up items and looked at the images."
- [HS #14380, 2026-04-27T16:34:26, cmcutrer@gmail.com (rep)]
  > "I used ccutrer and I was able to get setup. Thank you so much."
- [DB] All 24 active reps have a non-null `last_ipad_login_at`; the most recent seven
  are all 2026-08-18.

**Against:** `org_users.created_at` proves invitation redemption, not a device login;
the DB stores only *last* login, so first-login dates cannot be reconstructed. I
therefore date the transition from the first quoted sign-in report (2026-04-25)
rather than the first account creation (2026-04-23). Also worth recording: rep
onboarding did not stop at the wave — five more reps joined between 2026-06-19 and
2026-07-07 and one on 2026-08-03, with no corpus coverage of any of them.

---

### Phase 5 → 6 · Admin Training · 2026-05-13 · confidence: medium

**What changed:** Admin training was *delivered*, but not as trained — Scott missed
every live session and SuperCat substituted a written org audit, which Scott
accepted in lieu.

**Evidence:**
- [HS #14411, 2026-04-28T21:53:18, kyla@supercatsolutions.com (SuperCat)] — offered
  three dates, plus a rep-training track that never materialised:
  > "1. Admin Training (with me): I'd like to schedule a session to walk you and your team through the essentials of managing your SuperCat environment."
- [HS #14411, 2026-04-29T22:06:02, scott.tang@terracottalighting.com (customer)]
  > "PLease schedule my session : Tuesday, May 5: 12:00 PM - 1:00 PM"
- [CALL, 2026-05-05T16:00, "SuperCat x TDL Admin Training", 60 min] — Scott never
  joins. The full 13-minute transcript is Kyla and Kylor talking about other
  accounts, ending:
  > Kylor Johnson (SuperCat Solutions), 00:12:39: "right, Scotty Tang, let me know if he hits you up, but I guess we can just reschedule with him."
- [HS #14411, 2026-05-05T16:35:26, scott.tang@terracottalighting.com (customer)]
  > "Sorry, I forgot it
  > is it too late now?"
- Rescheduled to 2026-05-08 (Kyla 2026-05-05T21:06; Scott accepts 21:45; Kyla
  confirms 2026-05-06T13:02). **No record of that session exists.**
- [CALL, 2026-05-13T16:00, "Admin Training Handoff", 45 min] — again entirely Kyla
  and Kylor on other topics; Scott absent.
- [HS #14496, 2026-05-13T16:32:52, kyla@supercatsolutions.com (SuperCat)] — the
  substitute artifact:
  > "Sorry, we missed each other on today's training call. I went ahead and did an audit of your Terracotta Designs setup so I could focus on areas that would be most useful for you."
- [HS #14496, 2026-05-14T16:09:52, scott.tang@terracottalighting.com (customer)] —
  the client closes the phase himself:
  > "My apologies for missing our meeting. I mistakenly thought it was scheduled for today.
  > I am becoming much more comfortable with eCat and appreciate the audit review. The areas for improvement you identified are very helpful as I look to enhance our setup.
  > Regarding admin training, I will review the documentation and links you provided first. I believe I can figure out the next steps on my own, but I will reach out if I have any questions."

**Against:** This is the weakest transition in the timeline and the confidence rating
reflects a real disagreement about what "done" means, not date uncertainty. A strict
reading — a live session covering platform orientation, admin console and imports,
with the admin present — gives **`undetermined`, never completed**. I date it
2026-05-13 because the *content* was delivered in writing, the client read it and
said it was sufficient, and the ongoing-operations evidence that follows is strong:
Scott has since run 20+ product/inventory imports unaided. Two of the audit's own
recommendations were never acted on — see Current Phase.

---

### Phase 6 → 7 · Go-Live · 2026-04-28 · confidence: high

**What changed:** SuperCat formally ended onboarding, transferred the account to
support, and triggered invoicing. Note this is **fifteen days before** the admin
training transition above.

**Evidence:**
- [HS #14402, 2026-04-27T19:30:03, kylor@supercatsolutions.com (SuperCat)]
  > "Great progress — your reps are logging in and outside of a few troubleshooting issues, it seems like you're in a spot to be "live."
  > The natural next step is to get your admin training scheduled. This is where we shift from onboarding into ongoing support... I've looped in Kyla (cc'd), our Head of Support, who will be your primary point of contact from here on out."
  and, in the same message, the commercial trigger:
  > "I've also cc'd Angie, our Chief of Staff — now that your reps are active, she'll be reaching out with invoice details."
- [HS #14411, 2026-04-28T21:53:18, kyla@supercatsolutions.com (SuperCat)] — the
  explicit declaration:
  > "Your onboarding is now complete. Your product catalog (with images), pricing, options, customers, and inventory have all been imported and are live. Reps have been invited, and your user groups and territory codes are configured. That's a great milestone, so congratulations on getting here!"
- [DB] `org_users` for support@supercatsolutions.com created 2026-04-29T15:30 —
  the support account is provisioned into the org the next day.
- Ongoing client activity since: [DB] products imported clean 2026-08-15, inventory
  2026-08-18 (warning), 7 orders submitted 2026-06-24 → 2026-07-18, and two
  post-handoff support tickets resolved by Kyla (#14790 on 2026-07-16, #14874 on
  2026-08-03).

**Against:** "Live" was declared on rep logins, not on selling. The first order was
written **2026-06-24 — 57 days after the handoff** — and by then Kylor, who made the
call, was gone from the account. If go-live requires demonstrated commercial use, the
date is 2026-06-24, confidence high; the DB supports either reading.

---

## C. Current phase, as of 2026-08-18

**Phase 7 — Go-Live, sustained.** The org is live, actively maintained by the client,
and in steady-state support with Kyla. It is not, however, adopted.

**Evidence for "live and maintained":**
- [DB] `import_history.latest_per_type`: Products 2026-08-15 clean; Inventory
  2026-08-18 warning; Images 2026-08-15 clean; Product Stories 2026-07-05 clean;
  Customers 2026-04-23 clean. `inventory_last_updated` 2026-08-18T15:02:13.
- [DB] 397 active products, 396 with images, 346 customers, 222 options across 98
  option groups, 173 collections, 2 trade names (`TN1` = Terracotta Designs,
  `TN2` = Kanova & Co), 4 price levels.
- [DB] 24 active reps, all in the `Sales Reps` user group; seven logged into the iPad
  today (2026-08-18), the oldest last-login is 2026-06-30. Scott's own last iPad
  login is 2026-08-18T14:36.
- [HS #14874, 2026-08-03T14:13:47, scott.tang@terracottalighting.com (customer)] —
  the relationship is healthy:
  > "Thank you so much for the impressively quick response,
  > Appreciated!"

**Evidence for "not adopted":**
- [DB] `orders` joined to `org_users`: all 7 submitted orders — and all 7 orders of
  any status ever created in this org — belong to a single rep, `JCGonzalez`
  (jc@finelightsales.com, FL-S), between 2026-06-24 and 2026-07-18. **23 of 24 reps
  have never opened an order.** Nothing has been written in the 31 days since.
- [DB] `smart_stacks` for org 282 = **0**. Kyla's audit flagged this on 2026-05-13 as
  "one of the most useful features for your reps"; it was never acted on.
- [DB] `ipad_reports` = 1 — still the default tearsheet, the second unactioned
  recommendation from the same audit.
- Rep training, offered by Kyla on 2026-04-28 (*"Separately... we'll schedule a
  session with your sales team to cover the eCat iPad app"*), was never scheduled and
  is never mentioned again.
- [DB] 5 of 24 reps have `territory_codes = null` — `lytestyles@charter.net`,
  `kaceywilliamswls@gmail.com`, `Williamsoffice4@gmail.com`, `cwlikes@sbcglobal.net`,
  `dennis@lmlightinggroup.com` — all onboarded after 2026-06-19, i.e. after the
  account left onboarding. Kyla's 2026-05-13 audit could correctly say "territories
  assigned to all 20 reps"; that has since regressed.

---

## D. Turning points

### 1. 2025-12-18 → 2025-12-21 — the options reversal and the "amateur implementation" email

Brent had consolidated size variants into eCat options. On the 2025-12-18 call Scott
rejected the entire approach because the detail page no longer showed a full SKU:

> [CALL, 2025-12-18T14:30, Scott Tang, 00:02:27] "I think the people, before people order, people go through detail, every information before they order.    If you don't have the complete information, how can they make an order, right?"

Brent reversed it inside the call (*"So I will go back and remove the options and
re-update the product file"*), but three days later Scott escalated past the feature
to the product itself:

> [HS #13448, 2025-12-21T00:27:32, scott.tang@terracottalighting.com (customer)] "At the current stage of this account, there are quite a few issues that need to be cleaned up before we can officially launch. I'm not yet certain whether these issues come from data mapping or from the underlying software architecture. If it turns out to be the latter, I would be genuinely surprised - speaking as someone with over 10 years of experience in software engineering, the tool feels less like a mature commercial product and more like an early-stage amateur implementation.
> To be honest, had I known this earlier, I likely would not have signed up."

Brent's internal reaction was pasted into the customer-facing ticket by mistake and
is preserved verbatim:

> [HS #13448, 2025-12-21T14:37:35, brent@supercatsolutions.com (SuperCat)] "@kylor I was going to write something like this. Two points I wish I could articulate better or more clearly 1) why did you buy this software in the first place? and 2) I will meet with you but only if it is productive."

This is the closest the engagement came to ending. It maps to no phase boundary —
the org sat at Phase 3 before and after.

### 2. 2025-12-27 → 2026-04-19 — the four-month client-side stall

Dallas Market prep, the market itself, two weeks in China, then backlog. Scott's own
framing, in sequence:

> [2025-12-27T14:18:47] "My original plan was to have everything ready before the January 10 Dallas Market. However, due to the heavy preparation required leading up to the market, we may need to push this to later next month."
> [2026-01-07T15:45:53] "At the moment, I'm fully immersed in preparing the showroom, so I've had to temporarily pause work on this."
> [2026-01-22T22:45:46] "I am still in China now. will back home after tomorrow, unfortunately I didn't have the time to work on this when I am in China"
> [2026-02-13T00:14:00] "Unfortunately, it has been nearly two months, and I have forgotten where to start. Could you please resend the documentation or links regarding these configuration options?"

[DB] corroborates: between 2025-12-22 and 2026-03-12 there are exactly **two** import
days in the entire history (2026-02-24 Products clean 2). Kylor sent six check-in
emails across this window. One thing did go right in it: Kylor met Scott in person at
Dallas Market on 2026-01-13, which is plausibly what kept the account alive.

### 3. 2026-02-24 — the standoff, and the screen-share that broke it

The morning exchange is the sharpest in the corpus. Brent, three hours before the
scheduled call:

> [HS #13448, 2026-02-24T17:14:48, brent@supercatsolutions.com (SuperCat)] "I dug back into your CSV files and there hasn't been any changes from our last call in December. I don't want to waste your time but the catalog looks empty and the product feels broken due to the lack of data. I don't know if it makes sense to meet today until a baseline of data is populated."
> "...If you don't have the capacity to work on this project and/or you require us to rework the eCat iPad app. Specifically with how Tradenames are enabled or toggled then we should probably go in a different direction."

Scott, 34 minutes later:

> [HS #13448, 2026-02-24T17:48:51, scott.tang@terracottalighting.com (customer)] "I have new data sheets ready this week with updated pricing and 2026 products. However, the primary concern remains the user interface rather than the data.
> ...Regarding the data, I will have everything-including the new data sheets, products, customer data, and stories-available by this weekend. At this stage, the user interface is the only showstopper for us."

They met anyway. Brent screen-shared the Admin Console, had Scott drive, and showed
him custom fields, field ordering, company settings and related items. Scott's
posture flips inside the call:

> [CALL, 2026-02-24T19:30, Scott Tang, 00:37:45] "Yeah, yeah, yeah.    I really like that.    You know, I just didn't realize, you know, I mean, you can have this powerful future.    You I really like that, you know, so I can't wait to try"
> [same call, 00:39:36] "I see a nice, I see.    I know where to start.    Otherwise, I don't know where to start."

Every subsequent phase transition happens within nine weeks of this call. Four months
of email had produced nothing; 45 minutes of shared screen produced everything.

### 4. 2026-04-20 — the missing territory codes on the admin's own user

The customer file had imported, and the iPad still showed nothing — a failure mode
that looks identical to a failed import from the client's side, and which Scott could
not have diagnosed:

> [HS #14280, 2026-04-20T00:12:51, scott.tang@terracottalighting.com (customer)] "I finally successfully uploaded the customer file. However, when I open my iPA, somehow I can't see any customers
> Should I create a user for myself and assign territory codes? how to do?"

Kylor pasted all 40 codes onto Scott's user the next morning. Within 72 hours the
first eight rep invitations went out. This single 30-second admin action is the
highest-leverage moment in the whole timeline.

### 5. 2026-05-11 → 2026-05-12 — images in `/data`, and a wrong first answer

New products were importing clean but not appearing on iPads. Kyla's first diagnosis
blamed filename/SKU mismatches. Scott pushed back, correctly:

> [HS #14483, 2026-05-11T17:51:55, scott.tang@terracottalighting.com (customer)] "Yes, some image names do not match the item SKU. But as long as the listed image names in the products file matches the uploaded image names, I assume it should be ok"

Kyla re-investigated and found the real cause:

> [HS #14483, 2026-05-11T20:40:26, kyla@supercatsolutions.com (SuperCat)] "You're absolutely right that the image filenames don't need to match the SKU; what matters is that the filename listed in the products.csv matches the actual filename of the uploaded image file. I apologize for the confusion in my earlier message.
> I dug deeper and found the issue. I checked your FTP directory and your image files for KCH5180-20, KCH5180-33, KWS5180-18, etc. are in the /data folder. They need to be in the /images folder for the image import to pick them up."

Compounding it, [DB] `organizations.product_synch_requires_photo` = **true** (still
true today), so any product whose image the server could not confirm was silently
withheld from the iPad — 8 of 392 products at the time. Resolved next day:

> [HS #14483, 2026-05-12T17:41:42, scott.tang@terracottalighting.com (customer)] "Thanks for the help., I fixed the issue, all is good now"

### Honourable mention · 2026-04-24 — the user-group regression

Mid-invitation-wave, every rep silently moved out of `Sales Reps` into
`DefaultUserGroup`:

> [HS #14379, 2026-04-24T22:25:30, scott.tang@terracottalighting.com (customer)] "Also,  something wrong at your end.   Now all Reps moved to DefaultUserGroup from Sales Rep Group  - see attached screenshot"

Scott fixed it himself before SuperCat had finished investigating (*"I have manually
changed their usergroup back to Sales Rep now"*, 22:50:52). Root cause was never
established in the corpus. [DB] all 24 reps are in `Sales Reps` today.

---

## E. Does the seven-phase model fit this client?

Partly. Four specific mismatches, each load-bearing:

**1. Phases 4 and 5 are the same event.** Catalog completeness (2026-04-23) and rep
invitations (2026-04-23, 18:26 CT) are separated by hours, not by a stage. Scott's
own sentence does both at once: *"overall, it is in good shape now. What is the next
step. Should I invite users ( our sales reps) now?"* A model that scores them as
distinct phases will report two transitions where one decision occurred.

**2. Phase 7 preceded Phase 6 by fifteen days.** Go-live handoff and invoicing fired
2026-04-27/28; admin training resolved 2026-05-13. The ordering is not a data
artifact — it is how SuperCat actually ran the account, and the same inversion is
visible in the emails themselves (Kylor calls it "live" *and then* proposes training).

**3. Phase 6 did not happen in the form the model assumes.** Three scheduled
sessions, three no-shows, and a written audit accepted in lieu. Any framework that
requires a training *event* will score this `undetermined` forever, while the client
is demonstrably self-sufficient. The honest state is "trained asynchronously, by
client preference."

**4. The model has no state for *live but not selling*.** This is the most important
finding. Every Phase 7 condition is satisfied — handoff done, imports current, reps
logging in daily, tickets flowing — and yet 23 of 24 reps have never opened an order,
no SmartLists exist, and rep training was never delivered. Admin data maintenance and
sales adoption are two different things, and on this account they diverge sharply.
A phase number alone would read `tcd` as a clean success.

There is also a structural blind spot the seven questions cannot see: **the four-month
stall between 2025-12-27 and 2026-04-19, during which the phase state was constant
and the account nearly churned.** The single most decision-relevant fact about this
onboarding — that it was saved by an in-person meeting at Dallas Market and a
45-minute screen-share, after four months of email had failed — is invisible to a
model that only asks whether files are in.
