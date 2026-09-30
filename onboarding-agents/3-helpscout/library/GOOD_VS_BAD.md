# Good versus bad: paired examples per ticket type

De-identified. Each example is a **shape**: no client, contact or ticket names, and no verbatim client text.
IDs (`G-good-1`, `K-bad-2`, ...) trace to raw rows in the gitignored `runs/library_sources.md`.
Type numbers are from `TICKET_TYPES.md`; response types (R1 to R9) from `RESPONSE_TYPES.md`; rule
references (§) are to `ecat-client-email/CLAIMS_STANDARD.md` unless stated.

**Good** = the diagnosis and fix that actually resolved the ticket, confirmed by an outcome in later threads or
data (the outcome cards in the batch 7 and 8 grades). These entries record what worked, taken from the outcome
cards; they are not quotations of the sent replies, whose wording is only in the gitignored record. Where no
confirmed resolution exists for a type, this file says so; do not invent one.
**Bad** = a draft error found by an independent grader in batches 5 to 8 or the re-draft check, with the rule it broke.

Measured background: about 45% of held-out drafts carried a false or unsupported sentence in the client text
after verification, and in 18 of 21 such errors the finding underneath was roughly right; the sentence claimed
more than the evidence reached.

---

## Type 7. Login, access or account change

**Good (G-good-1).** A person needed access to a second org. What worked: adding the person's existing global login to
that org, with no invite. Outcome: done within a couple of hours the same day, confirmed. The shape to copy: look the
person up in `users` across all orgs first and use the existing login (pre-send checklist).

**Good (G-good-2).** A person signed in with an address that lacked the brand. What worked: adding the brand to that
address, then signing out and back in. Outcome: worked.

**Good (G-good-3).** Reps could not order; the cause was an empty Customer Number on the login. What worked: a test
login, or linking the person's own login to a customer account (the second puts orders on that account). Outcome: fixed
in 25 minutes in one case, and the client confirmed it works.

**Bad (G-bad-1).** The draft treated our earlier claim ("there are two logins for this person") as still standing.
The users row for the second login was created years before our claim, so the claim was provably wrong at that
time. Rule: § 1.3 (concessions and our statements need the record) and correspondence § 5 (a wrong claim in our
earlier reply forces ESCALATE and a correction by name). Should have been R6, ESCALATE.

**Bad (G-bad-2).** "The customer-service group lets them start practicing." Each login also needs a matching
Customer Number, so the sentence implied more than the group grants. Rule: § 2 row "so they can start practicing
when a precondition is missing" (state the precondition in the same sentence).

**Bad (G-bad-3).** "We need the order fields the help article lists." The importer requires none of them; a blank
status imports clean. Rule: § 2 row "we need [KB-listed fields]" -> "the importer requires [code-enforced fields];
the KB also lists [others]".

## Type 8. User groups, territories, rep visibility

**Good.** *No confirmed-resolution example is recorded for a plain territory-filtering ticket.* The nearest confirmed
outcome is the customer-number fix under type 7.

**Bad (H-bad-1).** Reps were told their sales history would be in the Sales Portal. The group the reps belonged to
had the Portal switched off at that time (audit row). True for the main group, false for the addressees' group.
Rule: § 5 checklist ("read the capability for every group the addressees are in") and § 1.1 (a claim covers what
the query covered).

**Bad (H-bad-2).** "Each rep sets their own password." That is the new-user path; existing users skip the step,
and about 50 of about 58 reps already had accounts. Rule: § 2 row "each rep / every user / all your accounts will ..."
-> the counted group ("the 8 reps without an existing login will ...").

## Type 9. Prices, promos, discounts, freight

**Good (I-good-1).** "Prices don't show on eOL for one login." What worked: setting the Admin group's default price
level (it was null). The shape to copy: name the level that login renders and whether the product has a price at it,
then the Admin field to set. Outcome: the fix was that setting (dated 09-18) and the swivel option plan also worked.

**Good (I-good-2).** eOL shows one price per login: the group default, else the first authorised level. What worked was
explaining that rule for the complaining login. Outcome: no further pushback; a walkthrough video was still owed.

**Bad (I-bad-1).** The drafts listed surface switches (eOL My Account choice, Show Prices) and never read the
account-level default price level, so the offered actions would not have produced a price. Rule: triage
"find the level that renders first" (`ecat-support-triage`); not a claims-standard rule, an omission.

## Type 10. Items, inventory, options or search not as expected

**Good (J-good-1).** Stock was blank on the iPad. The feed carried only a quantity-on-hand column, and the same-day fix
was an Admin view-field change. Shape to copy: lead with that no-code route and put the file change second. Outcome: fixed
the same day.

**Good (J-good-2).** Both stock and price complaints on one login: the feed lacked the two quantity columns and the
Admin group had no default price level. What worked: two plain columns and one Admin setting. Outcome: the sent reply
shipped the fixes in about three hours.

**Bad (J-bad-1).** The draft led with a parser change that needed engineering and days while an Admin view-field change
fixed it the same day; it also wrote "started coming in by email in early August" from the date of the first import
event. Rules: correspondence § 6 "Lead with the no-code route"; § 2 row "yesterday / Thursday" (dates must match what
was seen); § 1.1.

**Bad (J-bad-2).** A product missing on the iPad: the copy said to refresh data, but the server filters that product
out (the org requires a photo for sync and the product had none). Rule: triage "Fewer items than expected" (count
every gate, including the image gate); a "try this" step must be checked to change the result server-side.

**Bad (J-bad-3).** "The collections are there," true, but about 27 collection codes on the client's earlier product rows
were missing from the taxonomy, so the new items still rejected. The sent reply named the missing codes. Rule: § 3
(the answer stays: an omission that leaves the ticket unresolved is worse than a shorter true reply that names the gap).

## Type 3. Import or file error, or a file question

**Good.** *No confirmed-resolution example is recorded for a plain import error in the graded sets.* (The nearest is the
sent reply in J-bad-3, which named the exact codes.)

**Bad (C-bad-1).** "The file failed because the column names were shortened." The import log showed non-matching
headers only. Rule: § 2 row "the file failed because the column names were shortened" -> "the file's headers didn't
match: it had BASEITEM where the importer expects BaseItemCode".

**Bad (C-bad-2).** The run proved the importer reads `data/inventory.csv` and that the client's script wrote a bare
filename; the copy said "leave it as is". The verified fix stayed in the owner notes. Rule: the answer stays
(§ 3) and `RESPONSE_TYPES.md` rule 1; a verified cause that answers the question goes in the first line.

## Type 4. Order or quote will not submit, export or reach the ERP

**Good.** *No confirmed-resolution example is recorded for this type in the graded sets. This is the largest gap in
the library by volume (11.6% of tickets).*

**Bad (D-bad-1).** An order email existed with no server row, which means the order was queued on the iPad; the copy
asked for the order number and the rep, both of which the client's attachment already held, and said "I can't open the
attachment". Rules: `RESPONSE_TYPES.md` rule 2 (don't ask for what you can read), § 2 row "I can't open the
attachment" (never client text; it becomes an owner action).

## Type 2. Reply to our app-update or duplicate-order notice

**Good.** *No confirmed-resolution example is recorded; most replies to these notices are acknowledgments.*

**Bad (B-bad-1).** "I can see your sign-in at about 5:07 PM." The 5:07 row was the app's sync check; the sign-in was at
5:02 and was stored with a NULL organisation. Rule: § 2 row "I can see your sign-in at 5:07 from one row" -> name the event
you saw ("the app checked in with our server at 5:07") or query the event you mean.

## Type 11. Sales Portal or reporting numbers

**Good (K-good-1).** The Portal held open orders only; the fix was setting all five dashboard widgets to "invoices"
(changed 2026-09-21).

**Good (K-good-2).** The order download and the Portal upload are different records; the missing orders were the ones
marked Complete. What worked: naming that column and which file it comes from.

**Bad (K-bad-1).** "Four bill-tos are left out of every territory." The source said four *invoices*, and the bridge also
takes territory from eCat orders (a unit changed across a hop, and a scope wider than the search). The re-draft wrote
"every order, open and complete", which the two-verifier loop passed as clean and a grader found false. Rules: § 1.1
(scope), § 2 row "each rep / every user / all ..." -> counted group; and the owed-timeline chase should have been
R7, ESCALATE.

**Bad (K-bad-2).** "An eCat order doesn't store Shipment Preference." It is stored in `additional_fields` and
captured at eOL checkout; the check had read the `orders` columns only. Rule: § 2 row "X doesn't store / doesn't
exist / isn't there" -> "X isn't in the [download file / Admin list / table you searched]", naming the place.

## Type 6. Images and assets

**Good.** *No confirmed-resolution example is recorded for a plain image ticket in the graded sets.*

**Bad (F-bad-1).** A draft conceded one placeholder claim but left "none were deleted or removed" standing; 35 products had
been removed on a known date, and the image gate (a photo is required for sync when the org flag is on) was the
real answer. Rules: `ecat-correspondence` § 6 step 0 (every claim in our earlier replies is checked, a half-correction is
a failure) and the triage image-gate note.

## Type 5. Billing, contract, cancellation, seats

**Good (E-good-1).** A seat-count question: the draft's diagnosis was graded correct and safe (it deferred three of four
asks to the owner). Category: ESCALATE. Confirmed by the grade, not by a later client message.

**Bad (E-bad-1).** A draft told a client "one open invoice, due Aug 15" from the Stripe mirror; minutes later the billing
owner had already answered "nil balance, nothing owed", and the client accepted that. It also disclosed another org's
billing state. Rule: `truth-discipline` (billed is not collected; the mirror is not the ledger), R4 (billing goes to the
owner, never a balance in a draft), correspondence § 5 (ESCALATE).

## Type 12. Scheduling, check-in or chase

**Good.** *No confirmed-resolution example is recorded for a plain scheduling ticket.*

**Bad (L-bad-1).** For a feature request with "no timeline" already sent, the draft said "I'll let you know once it's in".
Rule: R7/R8 and § 2 row "the fix ships in the next update"; a feature-request reply says "logged", never a delivery
implication.

**Bad (L-bad-2).** "[the support lead] will confirm" and "we'll send it before the call", with no owner action behind either. Rule:
every commitment maps to a named owner action (`ecat-client-email` Owner actions).

## Type 15. Onboarding build thread

**Good.** *No confirmed-resolution example is recorded.*

**Bad (N-bad-1).** Three errors in one draft: "I asked [a colleague] to confirm" (only an internal note existed),
"fair point on the app registration" (the meeting transcript shows it was covered), and "customer data from the files
we've imported" (the import at that time had rejected rows). Category should have been ESCALATE. Rules: § 1.3 (past tense
and concessions need a record), § 2 rows "I asked engineering to confirm ..." and "the customer data from the files we've
imported".

**Bad (N-bad-2).** "Keep the onboarding@ address so nothing is missed" against the draft's own owner action (mail to that
address is not imported). Rule: `VERIFY_PASS_BRIEF.md` cross-read of copy against Owner actions.

**Bad (N-bad-3).** "Once the Sales Portal correction is finished": our own earlier framing carried onto a client who wrote
"eCat portal" and later confirmed they meant the Admin Console. Rule: § 2 row "once the [X] correction is finished".

**Bad (N-bad-4).** "I need two answers from you", when neither was needed to proceed. Rule: `RESPONSE_TYPES.md` rule 2.

## Cross-type: verify-loop side effects

**Bad (hollow reply).** In batch 8, 10 of 18 drafts ended as holding replies after the revise loop: true, but the
verified answer sat only in the owner notes. Rule: `RESPONSE_TYPES.md` rule 1; the verifier and drafter both check that the
last revision still answers the question.

**Bad (premise repeat).** Two drafts passed a CLEAN verify verdict while repeating a premise from an earlier message as fact
("the customer data from the files we've imported"; "every order, open and complete"). Rule: `CLAIMS_STANDARD.md` § 5
(map every factual sentence to a VERIFY row) and a separate verifier with no shared context.

## Gaps to fill before this library is a full inventory

Types with no confirmed-resolution example: 2, 3, 4, 6, 8, 12, 13, 14, 15, 16. Type 4 (order and ERP) is the most
important gap because of its volume. Fill them from tickets that resolved in later threads, using the same outcome-card
method (`runs/replay/_grader/GRADES_B7.md` appendix).
