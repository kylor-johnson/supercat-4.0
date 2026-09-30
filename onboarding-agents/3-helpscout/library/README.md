# HelpScout agent context library

De-identified reference for the HelpScout drafting agent ("agent 3"). It never sends; it drafts. The library says
what kinds of requests arrive, what kind of reply each calls for, and what a good and a bad reply look like.

| file | what it holds |
|---|---|
| `TICKET_TYPES.md` | the request types, derived from 150 days of real tickets: signals, facts to check first, routing, usual gate |
| `RESPONSE_TYPES.md` | nine reply shapes (direct answer through acknowledgment): when, required, forbidden, length |
| `GOOD_VS_BAD.md` | paired examples per type: the reply that resolved it, and the graded draft errors with the violated rule |
| `LIBRARY_EVAL.md` | which graded tickets become golden-set cases and what each asserts |

Raw ticket rows, quotes and ids live only in the gitignored `onboarding-agents/3-helpscout/runs/library_sources.md`.
Nothing client-identifying is committed here.

## How the drafter uses it

1. After scope and openness (`ecat-correspondence` § 3), **classify the ticket type** from `TICKET_TYPES.md` (the signals
   column). If two types fit, take the one whose "facts to check first" the ticket actually depends on. If none fits,
   mark `type: unclassified` and continue with plain triage.
2. Load that type's **facts to check first** and run them before any diagnosis prose. They are the checks that were
   missed in graded drafts, not a generic checklist.
3. Pick the **response type** (`RESPONSE_TYPES.md`) from the type and the gate. Draft to its required and forbidden parts
   and length.
4. Read that type's entries in `GOOD_VS_BAD.md` before writing the client text: the "bad" entries name the sentence shapes
   to avoid and the `CLAIMS_STANDARD.md` rule behind each.
5. Write the header line `Type: <n> <name> · Response: R<n> · Gate: <category, clause>`.

## How the verifier uses it

The verifier (`tools/VERIFY_PASS_BRIEF.md`, one separate sonnet call with no shared context) gets the draft, the lint output and
**two library extracts only**: the ticket type's section and the response type's section. It adds three checks to its rows:

- **Type check:** does the header's type match the ticket, given the signals?
- **Shape check:** does the copy match the response type's required and forbidden parts and length? (For example, an R4
  holding line that promises a follow-up with no owner action, or an R2 that asks the client for something the packet holds.)
- **Facts-first check:** were the type's "facts to check first" actually read, per the VERIFY table?

A shape mismatch is a flagged row, not an automatic failure. The verifier never sees `GOOD_VS_BAD.md` bad examples as
text to pattern-match on; they are for the drafter and the eval.

## What this library is not

- Not a replacement for the domain skills. It routes to them.
- Not a source of facts about a client. Every state claim is still read live and cited in VERIFY.
- Not complete: the count method is approximate (see `TICKET_TYPES.md`), and ten of sixteen types have no confirmed-resolution
  example yet (`GOOD_VS_BAD.md`, last section).

## Maintenance

- A type earns a place when three or more graded or live tickets share a need and a fact-to-check. A ticket that does not fit
  goes to `unclassified`; three of the same shape mean a new type.
- Every "good" example needs an outcome (a later thread or data that shows the reply worked). Every "bad" example needs the
  violated rule and a source row.
- Refresh counts from `helpscout_tickets` after a hand-labelled sample of 100. Do not re-run the keyword rule and quote it.
