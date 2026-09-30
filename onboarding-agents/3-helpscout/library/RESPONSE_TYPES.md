# Response types: what kind of reply a situation calls for

Pick the response type after the ticket type (`TICKET_TYPES.md`) and the gate category
(`ecat-correspondence` § 5). Voice and sentence rules live elsewhere and bind on every type:
`ecat-client-email/SKILL.md` (voice, no em-dashes, plain text, the owner sign-off, Owner actions) and
`ecat-client-email/CLAIMS_STANDARD.md` (what a sentence may claim). This file says **which shape**, and what is
required and forbidden in it.

Two rules from the graded batches apply to every type:

1. **The answer stays.** A verified cause or fix that answers the question goes in the copy, first, at the
   confidence the evidence gives it. Trimming a reply to a holding note is a failure, not a safe choice. In batch 8,
   10 of 18 drafts ended as hollow holding replies after the revise loop.
2. **Don't ask for what you can read.** Any question to the client whose answer is in the packet, the attachment
   they sent, an earlier thread or a query is removed.

Length: under about 200 words unless the client asked several numbered questions (claims budget, § 3).
Every added sentence is a chance to be wrong.

| # | response type | use when | usual gate |
|---|---|---|---|
| R1 | Direct answer | the answer is documented and needs no client-specific state | SEND-SAFE |
| R2 | Answer with a check first | the answer depends on state the run read, or a cheap client action comes before evidence | DRAFT-AND-PING |
| R3 | Diagnosis plus the client's next action | the cause is found and the client (or we) must act | DRAFT-AND-PING |
| R4 | Owner action plus a holding line | the reply needs something only the owner can do first | ESCALATE or DRAFT-AND-PING |
| R5 | Recap note | onboarding client mid-build with several open threads | DRAFT-AND-PING |
| R6 | Correction of our own earlier reply | an earlier reply of ours is wrong | ESCALATE |
| R7 | Chase on something we owe | client is asking for an item we already owe | ESCALATE |
| R8 | Scheduling | the ask is a time to meet | DRAFT-AND-PING |
| R9 | Acknowledgment (no reply) | the last client message asks for nothing | none |

---

## R1. Direct answer

- **When:** how-to and documented-limit questions (an FTP path, a field length, the import order, a URL shape, a stated UI limit).
- **Required:** the answer first; the KB article or "none exists" recorded in VERIFY (not in the copy unless the client can open it); one concrete next step if any.
- **Forbidden:** any state claim about the client's org that was not read; a commitment, date, price or apology (those make it R2/R3); jargon for a non-technical reader.
- **Length:** 2 to 6 lines.

## R2. Answer with a check first

- **When:** the answer turns on live state (a flag, a count, a price level, a group), or the cheapest fix is a client action.
- **Required:** the one fact checked, named with its surface ("in the Admin Console user group", "on eOL"); then the answer; then the cheap action before any request for evidence (full sync, update the app, hard refresh, then a private window, then clearing site cookies for eOL) **only if** that action can change the server-side result; then what to send back if it persists.
- **Forbidden:** "most likely" causes when the error text has not been seen (say what the log shows and ask for the exact text); "each / all / every" over a group that was not counted; "shows"/"displays" without naming the surface; a test the client ran treated as evidence before saying what it tested (a private window on eOL is logged out and may browse as a different group).
- **Length:** 4 to 10 lines.

## R3. Diagnosis plus the client's next action

- **When:** the cause is established and someone must act.
- **Required:** the observation in plain words, with its scope ("the file's headers didn't match: it had BASEITEM where the importer expects BaseItemCode"); who does what next, in order; for any "try this" step, confirmation that it changes the result server-side; the label quoted from the screen that person uses (Admin modern versus classic); lead with the no-code Admin route when it meets what they asked.
- **Forbidden:** a cause you did not observe joined by "because", "so", "which is why"; a promise to edit a value the client's own import file controls (it comes back on their next upload: name the file and column they change); a claim wider than the search (say "isn't in the download file", not "doesn't store it").
- **Length:** 5 to 12 lines; more only for several numbered questions.

## R4. Owner action plus a holding line

- **When:** billing, contract or cancellation; or the reply needs an owner-only step (a config change, a decision, a number) before it can be true.
- **Required:** the Owner actions list, complete (path, file and column or script with dry-run first, the check that proves it landed, who owns it); a one- or two-line holding reply that says only what is true now.
- **Forbidden:** a balance or state from a mirror without its owner's confirmation; another org's billing details; a date or price; a holding line that promises a follow-up with no owner action behind it ("I'll let you know when it's ready").
- **Length:** holding line 1 to 3 lines; Owner actions as long as needed.
- **Note:** use this only when the owner really must act. If a verified answer exists, use R2 or R3 instead (rule 1 above).

## R5. Recap note for onboarding clients mid-build

- **When:** an onboarding client has several open threads (correspondence § 6 step 0 decides reply versus recap; mid-build defaults to recap).
- **Required:** one note in a new thread listing done, in progress, what the client owes and what we owe; the threads to close named; every commitment lifted from a meeting checked against live state before it is written as done ("four of nine commitments from one call were not in the database"); files versus what we still need, as two short lists plus the one ask that unblocks.
- **Forbidden:** "we've imported the customer data" or any completion claim before the import was queried at T; an internal-only fact (health score, China CDN, internal ticket text); re-narrating the whole diagnosis.
- **Length:** a short list per section; not a narrative.

## R6. Correction of our own earlier reply (ESCALATE)

- **When:** an earlier reply of ours is contradicted by data or code at T, or a concession or "I asked X" cannot be shown in the thread.
- **Required:** name the earlier claim by what it said and its date; state what is true, with the evidence that shows it; the next step. The header names the ESCALATE clause.
- **Forbidden:** repeating the earlier claim as background; half-correcting ("concede A but leave B standing"); a concession ("you're right", "fair point", "that's on me") the record does not support; an apology for the product.
- **Length:** 3 to 8 lines.

## R7. Chase on something we owe (ESCALATE)

- **When:** the client is asking again for an item, date or answer we already owe.
- **Required:** what is owed and since when, from the threads; the current status read from live state or the calendar (not from memory); a named owner action with the check that proves it landed.
- **Forbidden:** a new delivery date the owner did not decide; "I'll get back to you" with no owner action; any delivery implication for something unscheduled.
- **Length:** 2 to 5 lines.

## R8. Scheduling

- **When:** the ask is a meeting time.
- **Required:** the date written out with weekday (verify the weekday) and time zone; check the client's calendar visibility and any unrecorded meeting flag; one proposed slot, or two; a next step.
- **Forbidden:** "tomorrow", "Thursday" or "yesterday" unless certain from the send date; "you met us on <date>" without a recording or event; a promise to attend that the owner has not confirmed.
- **Length:** 2 to 4 lines.

## R9. Acknowledgment (no reply)

- **When:** the last client message asks for nothing: "Done, thanks", "Thank you [support lead]", a reacted-to message, an automated feed, an out-of-office.
- **Required:** counted in the run header and listed one line each so the judgement is auditable.
- **Forbidden:** a courtesy reply; treating "Thanks, will that work for the October file?" as an acknowledgment (it asks for something).
