# GAPS — Terracotta Designs (`tcd`), org 282

Companion to `JOURNEY_tcd.md`. What I could not determine, what I discarded, and
where the sources disagree.

---

## 1. Could not determine

### 1.1 Whether the "Collections → Brands" relabel was ever delivered
Scott's single most repeated request across five months. Brent committed to it on
2026-02-24 and Kylor restated it in the recap:

> [HS #14038, 2026-02-24T22:34:21, kylor@supercatsolutions.com] "Collections → Brands - Brent will change the "Collections" label to "Brands" once the company settings save error is resolved"

The save error was live during the call (*"Now, again, I'm going to save this, and
it's going to throw an error. So I need to fix this"* — Brent, 00:21:44). Nothing in
the corpus ever confirms the fix shipped or the label changed. [DB] shows
`organizations.legacy_custom_labels IS NULL` and I found no column that stores a
nav-label override, so I cannot settle it from the database either.
**Would settle it:** the `company_settings` / app-behaviour serialisation for org 282,
or a Jira/commit reference for the settings save bug.

### 1.2 What happened at the rescheduled 2026-05-08 training
Kyla proposed Friday 2026-05-08 12:00 EST (2026-05-05T21:06:26), Scott accepted
(21:45:59), Kyla confirmed the invite was accepted (2026-05-06T13:02:24). Then
nothing. The next call in the corpus is 2026-05-13, and Scott's apology
(2026-05-14) says *"I mistakenly thought it was scheduled for today"* — singular,
so it is not clear whether he missed one session or two.
**Would settle it:** the calendar record, or a Fathom recording for 2026-05-08.

### 1.3 Whether order `155226-062426-19` is a real order or a test
The first order ever written in this org, by JC Gonzalez, 2026-06-24, $6,681.00 to
"Adino Decoracion" — the only one of the seven with
`matches_real_customer: false` [RAWSTATE]. It could be a first-run test against a
free-text bill-to, or a genuine order for an account absent from the customer file.
The next order follows 19 hours later against a matched customer.
**Would settle it:** the order's line items and whether an order email was sent, or
asking Scott.

### 1.4 How the 2026-05-07 Product Stories fatal was resolved
Raised twice, on two different tickets, and **never answered anywhere in the corpus**:

> [HS #14471, 2026-05-07T14:28:23, terracottalighting@gmail.com] "Fatal: Column baseitemcode is missing and is required. Line number(s): 1
> But  the BaseItemCode Column is indeed in the stories.csv file - see attached
> It is very confusing what is wrong."

[DB] confirms the damage — Product Stories 2026-05-07: clean 1, **fatal 4**; then
2026-05-12 error 1; 2026-05-24 clean 2 / error 2; not clean until 2026-07-05, two
months later. The resolution path is entirely invisible.
**Would settle it:** the HelpScout thread continuation, or the import log for the
2026-05-07 stories blocks (probably a BOM or an encoding issue on the header row,
given the error is on line 1 and the column is visibly present).

### 1.5 Whether invoicing ever happened
Angie, "our Chief of Staff", was cc'd on 2026-04-27 specifically to send invoice
details. She never appears in the corpus, and nothing about billing, contract, or
payment appears anywhere in 174 threads.
**Would settle it:** the billing system; out of scope for this reconstruction.

### 1.6 First-login dates for reps
`org_users` stores only `last_ipad_login_at`, so I can prove *that* all 24 reps have
signed in but not *when* each first did. I used `org_users.created_at` (invitation
redemption) as the proxy and dated Phase 4→5 from the first quoted sign-in report
instead. If a login-event or sync-event table exists, the transition could be dated
to the hour rather than argued.

---

## 2. Tier B and C tickets: what I judged, and why

### Discarded as irrelevant

| Ticket | Tier | Date | Why discarded |
|---|---|---|---|
| **#11412** | C | 2024-09-19 | The only genuine false positive in the corpus. A Maxim Lighting support question forwarded by David Solis. "Terracotta Designs" appears **once**, inside Christina Sabo's email signature, in a list of ten lines her agency (Emerald Coast Lighting Sales) carries. It predates the org by 13 months and has no bearing on this relationship. It is a good illustration of why the mention-token sweep needs a human — a name in a signature block is not a mention of the account. |

The handoff warned that the corpus opens more than a year before the org was created
and that early material might be pre-sales or a different relationship. It is neither:
it is a third party's ticket that merely names the brand.

### Kept, but low value (thread duplication)

Roughly **half of the 31 tickets are the same conversation captured twice** — once on
the client-domain mailbox and once on `supercatsolutions.com` / `onboarding@` /
`support@`. Confirmed duplicate pairs:

| Pair | Content |
|---|---|
| #14402 / #14403 | "Next Steps -- Admin Training and Go-Live" |
| #14411 / #14412 | "Welcome to SuperCat Support, Next Steps: Admin Training" |
| #14496 / #14497 | "SuperCat Admin Training Handoff" |
| #14371 / #14377 | "Fwd: eCAT trial invitation" |
| #14421 / #14424 | "TJS You're invited to join Terracotta Designs" |
| #14471 / #14476 | "Fwd: Import error (TCD)" |
| #14379 / #14381 | "Fwd: You're invited to join Terracotta Designs" |

The `supercatsolutions.com` copy usually carries the HelpScout satisfaction footer
and a plain-text re-render. **A naive thread count roughly doubles the apparent
volume of this account.** Any framework scoring "support burden" or "touch count"
from ticket totals will overstate `tcd` by ~2×.

### Kept and load-bearing

| Ticket | Tier | Why it matters |
|---|---|---|
| **#14280** | B | **Misfiled.** This is the entire customer-file arc — the single most consequential thread in the onboarding — sitting in tier B only because the mailbox is `supercatsolutions.com`. Everything in it is direct Scott↔Kylor correspondence. Any tier-A-only analysis loses Phase 3→4 completely. |
| **#13379 / #13380** | B | System notifications that date Phase 1 precisely (questionnaire 2025-10-31T23:11; first file upload 23:40). |
| **#14038** | B | Kylor's 2026-02-24 recap — the only written record of what the pivotal call decided. |
| **#14152** | B | Brent's diagnosis of the 2026-03-12 fatal (`undefined method 'downcase' for nil:NilClass`): blank columns, blank rows, `$` currency symbols. |
| **#14420** | C | Cindy Vackar's own account of signing in and browsing both brands — independent, rep-side proof of Phase 5. |
| **#14421** | C | Angie Schaefer-Kist's three-address identity tangle; needed to reconcile `alice74@fuse.net` in the DB. |
| **#14471 / #14476** | C | Scott's own gmail. Tier C only because of the sending domain. |
| **#14790** | C | Todd Neal's July login issue — evidence of live-phase support. |
| **#14378** | C | Invitation body only; thin but confirms the 2026-04-24 invite to Clyde. |

### The four gmail.com tickets — who those people are

The handoff flagged these as invisible to a domain-based search. Resolved:

1. **#14378** — Clyde Cutrer, III (`cmcutrer@gmail.com`), MNL Sales Agency, LA/MS.
   A **rep**. In DB as `ccutrer`, territories LA, MS.
2. **#14421** — Angie Schaefer-Kist (`alice74x@gmail.com`, invited at
   `orderstjs7143@gmail.com`, real account `Alice74@fuse.net`), T.J. Schaefer
   Associates, Cincinnati. A **rep agency principal**. In DB as `schaefer`,
   territories KY, OH, PA-W.
3. **#14471** and **#14476** — `terracottalighting@gmail.com` is **Scott Tang
   himself**. Same signature block, same phone/fax. This is the address SuperCat's
   automated import-error notifications are sent to, which is why import escalations
   arrive from a gmail domain. He also uses `sales@terracottalighting.com`, signing
   as "Sales Operations". **Three addresses, one person.**

The handoff's warning about off-domain addresses is correct and then some: not only
are the reps off-domain, the *admin* corresponds from a personal gmail for anything
triggered by a system notification.

---

## 3. Contradictions between sources

### 3.1 `import_active: false` is not a signal
[RAWSTATE] reports `"import_active": false` for an org that imported inventory on the
capture date itself. I checked: **no organization in the database has
`import_active = true`** (125 false, 132 null). It is a dormant or legacy column.
Anyone reading it as "imports are switched off" — or as evidence of a stalled
account — will be wrong. Recommend dropping it from the raw-state capture or
annotating it.

### 3.2 `visible_products` (397) vs `products_with_images` (396) with require-photo on
[DB] `organizations.product_synch_requires_photo = true`. One product currently has
no image and therefore should not be reaching any iPad, yet `visible_products` reports
397. The two fields are measuring different things — `visible` is almost certainly a
product-level flag, not sync eligibility. **The raw state does not tell you how many
products a rep can actually see.** For this org those numbers have diverged before,
and materially: 8 of 392 products were silently withheld throughout early May 2026.

### 3.3 Kyla's 2026-05-13 audit vs today
Not contradictions — the audit was accurate when written — but three of its
statements no longer hold, and one has regressed:

| Audit claim (2026-05-13) | Today [DB] |
|---|---|
| "392 active products across 153 collections" | 397 products, 173 collections |
| "Inventory data is flowing (382 records)" | 425 inventory rows |
| "all 392 products now have images" | 396 of 397 |
| **"territories assigned to all 20 reps"** | **24 reps, 5 with `territory_codes = null`** — all onboarded after 2026-06-19 |

The last one is a real regression: reps added *after* the account left onboarding did
not get the territory-code treatment that reps added during it did.

### 3.4 Price-level advice that the data contradicts
> [HS #14280, 2026-04-07T20:34:25, kylor@supercatsolutions.com] "Most of your customers appear to be showroom accounts, so show50 is likely the right default for most - but confirm with your team."

[DB] `customers.default_price_code`: **339 `dn`, 7 `ns`, 0 `show50`, 0 `imap`.**
The `show50` level Scott specifically designed on the kickoff call — his 50%
primary-showroom display program — is configured and **used by zero customers**.
Either the program is handled outside eCat or it was never operationalised. Worth
raising with the client; it is a live gap in the pricing setup, not a data error.

### 3.5 Conflicting image-format guidance, three times in eight days
- 2026-04-27T20:40 (Kyla): *"Formats accepted: JPG, PNG"*
- 2026-04-27T21:24 (Kyla, 44 min later): *"I apologize for the confusion in my previous email. The system accepts JPG/JPEG files only"*
- 2026-04-29T15:53 (Kyla): *"it only recognizes .jpg , not .jpeg . Even though they're the same image format, the system treats them differently"* — contradicting her own correction two days earlier
- 2026-05-13 (Kyla's audit): *"/images = product image files (.jpg, .png)"* — back to allowing PNG

Meanwhile Brent, 2025-11-17: *"This should ideally only include JPG files."* The
record contains four different answers to one question. The `.jpeg` quirk is
acknowledged as a bug (*"This is a quirk in our system that we're looking into
fixing"*) and cost Scott a full re-upload cycle.

### 3.6 Kyla's first diagnosis on 2026-05-11 was wrong, and the client caught it
Documented in Turning Point 5 of the journey. Recording it here because it is a
pattern worth measuring: the correct answer (`/data` vs `/images`) came only after
the client pushed back on a plausible-sounding but incorrect first response. Three
hours were lost.

### 3.7 A plaintext password was emailed to a rep
> [HS #14790, 2026-07-16T15:41:30, kyla@supercatsolutions.com] "You should be able to sign in now using the credentials below. Please remember to reset your password.
> Username: toddneal
> Password: password2026!"

Not a contradiction; flagging it because it is in the permanent record.

### 3.8 Brand name spelled four ways
"Canova" (Brent's kickoff transcript — likely ASR), "Kanova" (Scott, consistently),
"Konova" (Kylor's 2026-02-24 recap), "Kanoa" (2025-12-18 transcript). [DB]
`taxonomies` settles it: `TN1` = **Terracotta Designs**, `TN2` = **Kanova & Co**.
Also note [DB] the trade-name *codes* are `TN1`/`TN2` while the display names are
correct — the cryptic codes are not reaching the iPad, but they are what appears in
`products.trade_name_code`.

---

## 4. Things that look missing from the corpus

### 4.1 A reply with no question — the 2026-04-07 customer-file answer
[HS #14280, 2026-04-07T20:34:25] opens *"Thanks for your patience --"* and then
answers, point by point, five specific questions Scott must have asked:
`BuyerEmail`/`BuyerPhone` vs `BillToEmail`/`BillToPhone`, the `DefaultPriceCode` "0"
error, where `TerritoryCodes` are defined, the `ShipToFax` warning, and required
fields. **Scott's question email is not in the corpus.** [DB] confirms the customers
import failed on 2026-04-05 (error 2, fatal 1), so the question was almost certainly
sent 2026-04-05 or 2026-04-06.

### 4.2 Two long silences that contain most of the actual activity

**2026-03-20 → 2026-04-07 (18 days, zero threads).** [DB] shows in that window:
Products fatal ×2 on 2026-03-12, error ×8 + fatal ×2 on 2026-03-13, clean on
2026-03-28, **the first-ever Product Stories import** on 2026-03-28 (clean 2,
warning 2, fatal 2), and the first Customers attempt on 2026-04-05. The stories
file — the thing Brent had been asking for since December — arrives with no
correspondence at all.

**2026-05-15 → 2026-07-16 (62 days, zero threads).** [DB] shows in that window:
five new reps onboarded (2026-06-19, 06-30, 07-02, 07-06 ×2), **the first five
orders ever submitted** (2026-06-24 → 06-26, $27,277 total), and seven
product/inventory import days. The single most important business event in the
account's history — first revenue through the platform — generated no support
traffic, no check-in, and no acknowledgement. Nobody at SuperCat appears to have
noticed.

This is the clearest structural finding about the evidence itself: **support
correspondence and actual client activity are anti-correlated for this account.**
The busiest email months (December, February, April) are the least productive; the
quietest (June, July) are when the platform was actually used. A model that infers
health or progress from ticket volume will read this account exactly backwards.

### 4.3 Attachments and screenshots
Referenced constantly, present nowhere: Scott's annotated UI images (2025-12-21),
the login error screenshot (2025-12-25), the user-group screenshots (2026-04-24),
the import-status screenshots (2026-04-17), the black-logo screenshots (2026-04-25),
the Loom videos (three, 2025-11-11 / 2025-11-25 / 2025-12-22), and every CSV
exchanged. Several disputes in the record — particularly the UI arguments — turn on
images I cannot see.

### 4.4 A rep-training track that was announced and then vanished
> [HS #14411, 2026-04-28T21:53:18, kyla@supercatsolutions.com] "2. Rep Training (eCat iPad App) Separately, Emery, we'll schedule a session with your sales team to cover the eCat iPad app: syncing, browsing products, creating presentations, and placing orders. This is hands-on training tailored to your reps."

Never scheduled, never mentioned again by either side. Given that 23 of 24 reps have
never written an order, this is the most consequential thing that did not happen.
(Note also the stray "Emery" — a SuperCat name from the 2025-11-11 kickoff call
surfacing inside a 2026-04-28 template sent to the client.)

### 4.5 The 2026-05-05 and 2026-05-13 "training" recordings
Both are captured as calls with Scott listed as an attendee, and in both he is
absent for the entire duration. The transcripts are Kyla and Kylor discussing
unrelated accounts (Magic Light, NSL, Braxton Color, Al Fresco Home) and internal
tooling. **They are labelled as this client's training sessions and contain no
training and no client.** Any automated pass that counts calls, or that summarises
call content, will badly misread these two.

---

## 5. Self-check

1. **Every transition has a date and evidence?** Yes — six transitions plus current
   phase, each with at least one timestamped verbatim quote or a specific
   `RAWSTATE`/DB fact. No transition is `undetermined`, though Phase 5→6 (admin
   training) is marked `medium` and I state explicitly that a stricter definition
   yields `undetermined, never completed`.
2. **Every quote verbatim, with author and timestamp?** Yes. Call quotes preserve the
   transcript's internal spacing. Nothing is paraphrased inside quote marks.
3. **Whole corpus, or skimmed?** Read start to finish, all 5,517 lines, in ten
   contiguous passes with no gaps. Three stretches are pure whitespace padding inside
   forwarded email bodies (≈ lines 2190–2440, 3190–3560, 4640–4930); those contain no
   content. Everything else was read.
4. **Forbidden files avoided?** Yes — none of `CLIENT_PROFILE.md`, `HANDOFF.md`,
   `REGISTRY.yaml`, `Phase_Anchors.md`, `Phase_Progression_Framework.md`,
   `Flags_and_Signals.md`, `Output_Contract.md`, `RUN_PROMPT.md`, or any `ecat-*`
   skill was opened. Two partial-exposure caveats are disclosed at the top of
   `JOURNEY_tcd.md`: the harness auto-injects the workspace `CLAUDE.md` (which
   contains eCat import mechanics, including import-tier semantics), and the one-line
   descriptions of the `ecat-*` skills are visible in my tool listing. No skill
   content was loaded, and neither source defines phases.
5. **Does the narrative contradict `RAWSTATE_tcd.json`?** In one place, deliberately:
   `import_active: false` (§3.1) and the `visible_products`/`products_with_images`
   pair (§3.2). Both are flagged as raw-state artifacts rather than findings about
   the client. Everything else in the journey is consistent with the capture; where
   the DB is richer than the capture — order attribution to a single rep,
   `smart_stacks = 0`, `product_synch_requires_photo = true`, invitation timeline,
   trade-name display values — I queried it live and said so.
