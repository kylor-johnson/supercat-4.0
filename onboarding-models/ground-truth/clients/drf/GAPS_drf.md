# GAPS — Dorell Fabrics (`drf`, org 290)

Companion to `JOURNEY_drf.md`. What I could not determine, what conflicts, and what the
corpus is missing.

---

## 1. Evidence-quality problem that affects every quote in this run

**Fathom speaker attribution in this corpus is unreliable, and in several transcripts it is
demonstrably wrong.** This is the single biggest threat to the accuracy of anything quoted
from a call, so it is stated first.

Demonstrated instances:

| Call | Line | Problem |
|---|---|---|
| 2026-02-03 | ~L180 | "Hi, I'm Suzanne." is attributed to **Jon Vanderberg**; the surrounding block also has Jon speaking Christine's lines |
| 2026-02-10 | throughout | Jon's and Suzanne's blocks are transposed for long stretches — the SuperCat product walkthrough appears under `SuzanneFukunaga (2)` and client questions under Jon |
| 2026-05-05 | throughout | A speaker labelled `kylor (Unverified)` carries Brian Frankel's lines and vice versa; `Brian Frankel (loomcraft.com)` speaks Kylor's demo narration |
| 2026-05-18 | throughout | The entire client side is labelled `Christine Soh`, but the content is plainly Suzanne's (dog, construction, "Christina and I") and Christine's (firewall, WinSCP) interleaved |
| 2026-04-29 | ~L1312 | Kylor's apology is attributed to Kylor but the preceding line is under `Suzanne fukuanga`; boundaries are off by one turn |

**How I handled it.** Where attribution was uncertain I preferred (a) HelpScout email, which
carries a real `From:` header, over transcript; and (b) transcript lines whose content is
self-identifying (a speaker naming their own company, referring to "my boss Brian", or
describing something only that person could describe). Where I quoted a call line whose
speaker label I could not independently corroborate, I attributed it to the call rather than
the person, or noted the label. Two quotes in `JOURNEY_drf.md` are affected and marked:
the 2026-05-18 "we kind of missed it" line and the 2026-05-18 "it's to go to our customer
service" line are both labelled `Christine` in the transcript but read as Suzanne. I cited
them by call, not by person.

**What would settle it:** the Fathom recordings themselves (share links are in the corpus
headers), or Fathom's per-speaker diarisation confidence.

---

## 2. Could not determine

### 2.1 Who performed the 2026-07-06 and 2026-07-08 imports
`import_events` records the event and payload but has no actor column (`id`, `created_at`,
`organization_id`, `data` only). The 2026-07-08 Product Stories imports are almost certainly
Kylor's — [HS #14707, 2026-07-08T16:57:07Z] "I'm doing the initial import now to be sure I
have it correct" — but the 2026-07-06 Products import and the 2026-07-06 image batches could
be either Christine or Kylor. This matters because it determines whether the client's *own*
last import was 2026-07-06 or 2026-07-02.
**Would settle it:** an application-level audit trail (`audit_log_entries` exists in the
schema; I did not find org-290 rows joining to imports), or the Admin Console File Import
Status page which displays the uploading user.

### 2.2 Whether Kylor is still with SuperCat
[HS #15031, 2026-08-11T22:40:28Z, Suzanne@dorellfabrics.com]: "Congrats again on your new
chapter!" — "again" points back to the 2026-06-30 congratulations on his marriage, so this is
most likely still the wedding. But "new chapter" is an odd second reference to a marriage six
weeks later, and it sits alongside a support handoff to Kyla that then failed to hold. He is
still sending from `kylor@supercatsolutions.com` on 2026-08-12. **Undetermined.** I did not
assume a departure, and no conclusion in `JOURNEY_drf.md` depends on it.
**Would settle it:** SuperCat HR/directory, or any thread after 2026-08-12.

### 2.3 Why Kate Gothreau's account was removed
`kate@dorellfabrics.com` (user_id 80151, "KateG", iPad6,3, DefaultUserGroup) has two
`login_events` on 2026-07-01 against organization_id 290 — but **no `org_users` row exists**
for her in org 290 today, and no invitation record. She was referenced on the 2026-05-18
call ("Kate's going to send me the product stories for the new one"). So she was provisioned
some way that left no invitation trace, used the iPad once, and was removed. Deliberate
cleanup or accident is undetermined.
**Would settle it:** soft-delete/audit history on `org_users`, or asking Christine.

### 2.4 Whether the 2026-08-18 activity is a live show or a rehearsal
Four users on device, a new user provisioned, an invitation sent by the client, and three
orders with real ship dates and negotiated prices — but nothing in the corpus names an event
on that date. Dorell attends "market and Showtime twice a year" (2026-07-21). Showtime was
May 19–21; a second-half show would plausibly fall in this window, but I have no source for
it. I described the pattern and stopped short of naming the occasion.
**Would settle it:** the Showtime/High Point 2026 fall calendar, or Suzanne's reply to any
post-08-18 message.

### 2.5 Whether the 209 uncosted SKUs have since been costed
[HS #14707, 2026-07-07T22:42:04Z] Christine: "The ones that are still at zero has not been
costed yet." No product import has run since 2026-07-08, so **in eCat they are still $0** —
that much is certain. Whether Dorell has costed them internally and simply not re-uploaded
is unknown, and it is the difference between "client is blocked" and "client hasn't gotten
to it."

### 2.6 Whether Kyla's four 2026-07-29 action items were ever answered off-corpus
All four carried ETA "This week". None has a reply in any captured thread, and Kyla does not
appear after 2026-07-29. Whether these were answered by phone, dropped, or are still open is
undetermined — but no *artefact* of any of them exists: pricing is still in the stories file
(1,418 products), no product custom fields carry price values, the catalog layout is
unchanged, and no barcode field is populated. The absence of artefacts is weak evidence they
were not delivered.

### 2.7 The derivation of the $8.00 order total
`155309-071426-5` totals $8.00 from a single line, `BAYLIN-C0-GRAPHITE`, with
`calculated_price` 8.0 and `extended_price` 8.0, while its three siblings are 0.0. Given
`net_price` is $1.00 org-wide and quantity is 1, $8.00 is not derivable from the price
system — it looks hand-keyed on the order pad. Consistent with Dorell's documented "write
the price in" workflow, but I could not confirm the mechanism.

---

## 3. Contradictions between sources

### 3.1 "We missed the show" vs. the login table — the most important one
[CALL, 2026-05-18T21:00Z]: "Yeah, we kind of missed it, so, but don't worry because we can
use it right after." But `login_events` records **25 sign-ins on 2026-05-19 and 10 on
2026-05-20** (Showtime was May 19–21), and order `155309-051826-1` — billed to AMALFI, the
only real customer account in the org's order history — was submitted 2026-05-18T21:27:38,
during that very call.

**Resolution:** both are true about different things. They missed *catalog completeness*, not
*use*. The deadline narrative in the correspondence understates what actually happened at the
show. A framework scoring this client from tickets alone would record a missed go-live; the
database records a partial one. I went with the database and said so.

### 3.2 "Sorry for the silence" vs. continuous usage
Christine's 2026-06-30 apology implies a dormant client. `login_events` shows Dorell users in
the product on 13 separate days between 2026-05-22 and 2026-06-30. The silence was
correspondence-only. Same failure mode as 3.1: ticket volume is a poor proxy for engagement
on this account, in both directions.

### 3.3 Kylor's "created user groups" vs. `user_types.created_at`
[HS #14798, 2026-07-17T16:27:36Z]: "Created user groups (Dorell Internal for your team,
SuperCat Team for us) so everyone isn't stuck in DefaultUserGroup." But `Dorell Internal` has
`created_at` = 2026-04-15T13:51:34.595917 — the same second the org was created. It is the
renamed DefaultUserGroup, not a new group. Only `SuperCat Team` (2026-07-17T16:06:05) was
new. The substance of the claim (users moved out of an undifferentiated default) holds; the
mechanism described does not.

### 3.4 Kyla's "default order origin remains like a quote or a sample" vs. order records
[CALL, 2026-07-21]. But `organizations.order_origins` = `[]` and **all 10 orders carry
`order_type = 'Confirmed'`**, including all three placed on 2026-08-18, four weeks after the
training. Never configured. Consequence: Dorell's sample requests are recorded in eCat as
confirmed orders, which will misstate any order export they later feed to their ERP — a
stated future goal ([CALL, 2026-07-21] Suzanne: "We would love to have the orders interface
with our ERP").

### 3.5 Product count drift across sources
Kylor reports 1,676 active products (2026-06-17), then 1,630 (2026-07-02), then "~1,630"
(Kyla, 2026-07-20). Today: **1,627**. The decline is consistent with the 2026-07-02/07-06
cleanup rather than an error, but no single message announces the deletions. Image coverage
moved the other way and much further than reported: 84% at 2026-06-17, **96% (1,564/1,627)**
today, with no corpus message claiming the improvement.

### 3.6 RAWSTATE vs. live DB
Six items, itemised in `JOURNEY_drf.md` § "Contradictions with RAWSTATE_drf.json". The two
that change the reading: the 10th order submitted 5½ minutes after capture, and the fact that
RAWSTATE's `reps: 3` are PD staff rather than the sales reps the phase model means.

---

## 4. Tier B tickets — relevance judgement

**All 9 tier B tickets were judged relevant. None were discarded.** This is unusual and worth
recording explicitly, because tier B is described as unfiltered and normally contains noise.

Here it does not: every tier B thread is the *same* Dorell conversation captured a second time
through the SuperCat onboarding/support inbox, or a genuine Dorell working thread that
happened to be filed with a `supercatsolutions.com` customer-of-record.

| Ticket | What it is | Kept because |
|---|---|---|
| #14433 | "Re: Next meeting" | Contains Suzanne's 2026-04-30 spec for Color Family, half-yard and waterfall SKU naming, and Christine's 2026-05-01 admin-login failure — primary source, not a copy |
| #14461 | "Samples 18x54 and waterfall.csv" | Kylor's 2026-05-05 import summary and Suzanne's "I sent this to you on Friday" — primary |
| #14463 | "SuperCat Onboarding Open Items" | Brian Frankel's only email in the corpus; establishes his CEO title and second address |
| #14469 | "Re: updates" | The 2026-05-06 Google Drive / SharePoint permissions failure chain — primary, and the cause of a real delay |
| #14486 | "Re: updates" | Contains David Lok's only appearance and the 2026-05-11 "list has changed dramatically" turn — primary |
| #14613 | "FW: Thank you for your order" | The Foxtrot-Carbon wrong-image incident, 2026-06-10/11 — primary, and the reason order #2 exists |
| #14655 | Kylor's wedding OOO | Duplicate of #14638 2026-06-18, but confirms the onboarding-inbox routing and names Brent and Kyla |
| #14811 | Kyla intro thread | Support-inbox capture of #14799; supplies Kyla's full title and signature block |
| #14858 | Kyla's post-training recap | Support-inbox capture of #14799 2026-07-29; identical body |

**Nothing in tier B was third-party or off-topic.** Tier C is empty, as the manifest states.

---

## 5. Duplicate-capture accounting

The brief warned that ticket count overstates activity ~2×. Confirmed, at almost exactly that
ratio.

**16 unique ticket numbers across 62 threads collapse to approximately 8 real conversations:**

| Real conversation | Ticket numbers | Note |
|---|---|---|
| Initial imports + next steps | #14401 | 3 threads, single conversation |
| Next meeting / scheduling + Color Family spec | #14433 | |
| Product file progress | #14438 | |
| Samples 18x54 & waterfall | #14461, #14463 | |
| Updates / permissions / rebuild | #14469, #14486 | |
| Foxtrot image mismatch | #14613 | |
| **Check-In & Next Steps (pricing → stories)** | **#14638 + #14707 + #14655** | **#14638 and #14707 are the same conversation double-captured — bodies identical, timestamps differ by seconds (e.g. 2026-07-01T19:31:05 vs 19:31:27). 26 threads for one conversation.** |
| **Support intro + admin training** | **#14798 + #14799 + #14811 + #14858** | Kylor's handoff note, Kyla's client thread, and two internal captures — one conversation, 4 ticket numbers |
| "pack" — email template question | #15031 | Post-handoff, answered by Kylor |

So: **16 tickets → 8 conversations, a 2.0× overstatement.** Volume-based activity scoring on
this account would roughly double real engagement. Conversely, and more dangerously, it would
*halve* the June stall if you assumed each ticket were distinct — the #14638/#14707 pair alone
accounts for 26 of the 62 threads and all of them fall in a nine-day window (06-30 → 07-09).

---

## 6. Corpus holes

### 6.1 Contract, order form, and commercial close are absent
Pricing is discussed on 2026-02-03 ($4,500 + $8,700/yr, 25 licences) and re-presented as
tiers on 2026-03-19 (Tier 1, 10 users, flat monthly). **No signed agreement, no order form,
no close date, no invoice appears anywhere.** The corpus jumps from "It's me convincing my
boss" (2026-02-10) to a provisioned org (2026-04-15) with nothing in between. Which tier and
what price Dorell actually bought is unrecoverable from this evidence, as is who signed.

### 6.2 Replies with no question, and questions with no reply
- **Kylor's 2026-06-17 check-in got no answer for 13 days.** It closes with a direct question — "what's your target timeline for getting reps on the iPad?" — that is never answered anywhere in the corpus, then or since.
- **Kyla's 2026-07-29 recap is the last message she sends.** It contains 4 SuperCat commitments and 5 Dorell action items. There is no reply, no follow-up, and no closure — the corpus simply moves to 2026-08-11 with a different SuperCat person answering a different question.
- **Suzanne's 2026-07-07 "Let's try this and see how it looks!"** — no one ever reports back on how it looked.
- **[CALL, 2026-07-21] Kyla:** "Remind me a little bit later to come back to that point" (color thumbnails) and "let me put a pin in that" (per-item custom-field pricing). Neither pin is ever pulled in writing.

### 6.3 Referenced artefacts never seen
- The **initial collection list Suzanne shared with Jon** (referenced 2026-05-06) — the file that decided which collections shipped. Never in the corpus.
- The **30,000-SKU characteristics file** and the several revisions of it.
- **`build_stories_with_pricing.py`**, the script Kylor sent Christine on 2026-07-09 for her to run herself. Whether she ever ran it is unknown and matters — it is the maintenance path for the pricing workaround.
- The **screenshot Christine sent on 2026-07-03** showing the desired multi-price layout. Attachments are stripped throughout.
- The **Loom videos** Kylor offered repeatedly.

### 6.4 Calls referenced but not captured
The 2026-04-13 call refers to a meeting "the 25th at 2.30 p.m." scheduled on 2026-03-19; a
2026-03-25 call is not in the corpus (11 calls captured, 0 without transcript per the
manifest). Either it did not happen or it was not recorded. Similarly, the 2026-05-05 call
ends with "we can find 30 minutes to review it live at the end of the week" — the 2026-05-06
call exists, but a promised Friday 2026-05-08 session does not.

### 6.5 The Sales Portal / eCat Online question is never closed
Jon sells eCat Online repeatedly in February. Suzanne says on 2026-07-21 "we're not granting
access to the customers, for our customers to access any of our eCat database for the time
being" and that it needs a CEO decision. Whether Dorell bought Tier 1 (which per the
2026-03-19 pitch *includes* a gated buyer view) or whether eOL is simply unconfigured is
undetermined; `mobile_sites` was not examined.

### 6.6 No rep-training thread exists
Kyla states twice (2026-07-20, 2026-07-29) that "Jon will schedule" iPad training for field
reps. Jon does not appear in any thread after 2026-05-18. There is no rep-training
correspondence, no scheduled call, and no rep account. This is the clearest single unfinished
thread in the account.

---

## 7. Things I deliberately did not conclude

- **That the missing options / inventory / eCat Online are gaps.** They are documented client
  decisions, stated on the record more than once. Scoring them as incomplete would repeat
  exactly the failure the brief warned about.
- **That $0.00 order totals mean the client has not transacted.** For a free-sample workflow,
  $0.00 is the correct value. The right question is whether *sample requests* are flowing,
  and they are.
- **That "no import since 2026-07-08" is a decay signal.** For a seasonal rotation catalog
  with no inventory feed, it is the resting state. See `JOURNEY_drf.md` § E.C.
- **That the client is at risk.** Nothing in 153k tokens of evidence supports it. The risk in
  this account is on SuperCat's side of the relationship, not Dorell's.
