# Hardening the HelpScout agent: replay, grade, fix, repeat

Written 2026-09-25 after Kylor's review of the first run. Untracked until he commits it.

## What the warehouse already holds (measured 2026-09-25, `helpscout_tickets`, last 90 days)

Conversations with a client message followed by a staff reply of 300+ characters:

| inbox | type tag | convs | substantive reply |
|---|---|---|---|
| onboarding | (untagged) | 53 | 41 |
| support | bug | 99 | 79 |
| support | (untagged) | 51 | 39 |
| support | user management | 49 | 31 |
| support | training | 41 | 34 |
| support | data-sync imports and exports | 29 | 24 |
| support | config issue | 21 | 17 |
| support | orders invoices and pmt integration | 13 | 12 |
| support | image asset | 7 | 7 |
| support | sales and finance | 7 | 6 |
| support | feature request | 3 | 2 |

292 labelled examples in 90 days, each with the reply a human actually sent. Roughly 3 new ones per day. That is the test set; nobody has to invent tickets.

## The method: replay with a hard cut

For a ticket, pick the client message at time T that the human answered. Build a **packet** that contains only what existed at T, draft from the packet, then compare the draft with what was actually sent.

The packet builder is the piece of engineering that makes this cheap. One script, given `(conversation_id, T)`:

1. **Thread, cut at T.** All threads on that conversation and on the same client's other conversations with `thread_created_at <= T`. Notes after T hidden (they usually contain the resolution). Lineitems dropped.
2. **Meetings, cut at T.** Fathom summaries with the client's domain in the last 14 days before T. Google Calendar events with the client's domain in the 7 days before T, flagged when Fathom has no matching recording.
3. **Client folder.** `02_Implementation/<Client>/` as it is now (accept that it may postdate T; note it).
4. **Live state.** Postgres now, with `updated_at` on every row read, so the grader can tell whether a value changed after T. For tickets older than ~60 days, state drift makes live-state grading unreliable; grade the method, not the value.
5. **Scope.** Inbox and assignee from `helpscout.conversations`, so the run also reports whether the ticket would have been in Kylor's or Kyla's list.
6. **Attachments.** Flagged by mention; the packet says "file present in HelpScout, not in packet".

The draft is produced by the three skills from the packet only. The agent never sees the sent reply, and the hard cut is enforced by the builder, not by the person running the test.

## Grading: rubric, not string match

The sent reply is the reference, not the truth. This run alone found two sent replies with wrong facts ("the data is there"; "collections are permanent"). So grade both the draft and the reference on the same rubric:

| criterion | pass condition | who grades |
|---|---|---|
| facts | every state claim is true in Postgres or code at T; nothing invented | LLM judge with the VERIFY table, then a human on 20% |
| diagnosis | same root cause as the sent reply, or a better one with evidence | human |
| commitments | no date, price, or promise the human would not have made | human |
| next action | the client knows exactly what to do and who does what | LLM judge |
| voice | passes `ecat-client-email`; no em-dashes; no slop | LLM judge |
| gate | SEND-SAFE only when every § 6 clause holds | human |
| scope | in Kylor's list only if the inbox/assignee rule says so | script |
| found-more | anything true the human's reply missed, listed separately, not as a revision | human |

Two numbers matter: **SEND-SAFE precision** (no false positives, needs 20+ calls before it means anything) and **sent-as-is rate** on DRAFT-AND-PING. Track both per type tag, because "damn near perfect" will arrive per category, not for the inbox as a whole. Scheduling and commitment tickets will never be SEND-SAFE; import and config tickets can be.

## Phases

**Phase 0, this week.** Decide C1 to C6 in `runs/2026-09-25/SKILL_EDIT_CANDIDATES.md` and write them into the skills. Build the packet builder as a BigQuery query plus a small script. Add `assignee_id` to the `helpscout_tickets` view.

**Phase 1, two weeks: replay 50.** 25 onboarding (Kylor's), 25 support (stratified by the tags above, Kyla's), all from the last 60 days so live state is still close to T, all with a substantive human reply. Batches of 10. After each batch: grade, fix the skill or a fixture, re-run the previous batch to check nothing regressed. Kylor grades his 25, Kyla grades hers. That doubles the labels per week and it is how the support-inbox learnings get in without Kylor reading Kyla's tickets.

**Phase 2, the live fortnight (correspondence § 9).** Daily run under the scope rule, drafts only, sent-as-is table filled every day. This is where SEND-SAFE precision gets its 20 calls.

**Phase 3, frontline support mode.** Same pipeline scoped to Kyla, run several times a day. This needs the HelpScout API as a read path (the warehouse lags 6 hours) and the OAuth authorization-code grant so drafts land in the mailbox as drafts. Auto-send stays off until Phase 2's numbers say otherwise, per category.

## Closing the loop

Every graded ticket produces one of three artifacts or it was wasted:

- a **skill line**, when the miss was a rule the skill lacks (this run: six candidates);
- a **fixture**, when the miss was a fact pattern worth re-testing (this run: Kaleen all-zero prices; Universal missing rows with a clean log; Legrand agency flip; JC invitation links);
- a **KB entry**, when the answer came from code because no article exists (this run: options, option forms, invitations, iPad-created customers). The KB index has one options article. The skills are currently the KB; that is fine for the agent and bad for clients.

## What this will not fix

- The agent will keep finding things that are undone in live state. That is the product, not the agent. The fix is presentation: "also found" is a separate list at the bottom, never a reason to revise the email a fourth time.
- Unrecorded meetings stay invisible. The calendar flag turns them into a question, not an answer.
- Attachments stay outside the warehouse until there is a HelpScout read credential.

## How other teams do this

The same loop, under different names: a golden set replayed offline, an LLM judge with a rubric plus sampled human grading, "assistant drafts, human sends" as the default, auto-resolution turned on per narrow category once precision is proven, and every resolved ticket feeding a knowledge base. SuperCat's difference is that the answer usually depends on one org's live configuration and on importer behaviour that is only in the code, which is why the VERIFY table has Postgres and `supercat_server` rows that a generic support bot does not need. The data to run this loop already exists here; the packet builder and the grading rubric are what is missing.
