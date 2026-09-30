# Library eval plan: golden-set cases from the graded tickets

A plan only. Nothing here has been run. It says which graded tickets become golden-set cases, and what each asserts.
Cases are stored by ticket id in the gitignored `runs/` and referred to here by shape; ids are in `runs/library_sources.md`.
This follows the repo's existing replay method: a blind packet cut at T, the drafter never sees the sent reply or the grades.

## What the eval measures

The live-run bar (from the handoff and `FIX_PLAN.md`): at most 1 of 20 held-out drafts with a client-text error, 0 wrong SEND-SAFE,
every ESCALATE caught, and a **human** blind check (the earlier owner sheets were written by Claude sessions, so they do not count).
The library adds three measures:

1. **Type accuracy:** the header's type matches the case's expected type.
2. **Shape conformance:** the copy meets the response type's required and forbidden parts.
3. **Regression on known error shapes:** the known error in the case does not reappear.

## Case selection

Two sources, kept separate:

- **Known-error cases (regression):** tickets whose earlier draft carried a specific error. Each asserts that error is absent. Thirteen of
  these were re-drafted under the claims standard (0 of 13 repeated the old error); re-use them as regression, never as evidence of
  a blind pass, because they taught the patterns.
- **Held-out cases (measurement):** tickets first messaged on or after 2026-09-29 (batch 9). Never used to write a rule.

Cap a first run at 5 cases (a cost and time limit from the owner). A full run is 20 and needs the owner's OK on agent count, minutes
and tokens first.

## Golden-set cases

Expected type and response type use the numbers in `TICKET_TYPES.md` and `RESPONSE_TYPES.md`. "Asserts" is what a pass checks.

| # | shape (ticket) | type / response / gate | asserts |
|---|---|---|---|
| 1 | empty Customer Number blocks reps from ordering (G-good-3, G-bad-2) | 7 / R3 / DRAFT-AND-PING | names the Customer Number precondition in the same sentence as "start practicing"; offers both fixes; no "the group lets them" |
| 2 | second login for a person (G-good-1, G-bad-1) | 7 / R6 / ESCALATE | corrects our earlier "two logins" claim by name; uses the existing login; category is ESCALATE |
| 3 | rep group lacks the Portal (H-bad-1) | 8 / R2 / DRAFT-AND-PING | does not say the reps have Portal history; checks the capability for the addressees' group |
| 4 | password step wording (H-bad-2) | 8 / R3 / DRAFT-AND-PING | replaces "each rep" with the counted group |
| 5 | eOL price missing (I-good-1, I-bad-1) | 9 / R3 / DRAFT-AND-PING | names the price level the login renders and whether the product has a price at it; no surface-switch-only answer |
| 6 | stock blank on iPad (J-good-1, J-bad-1) | 10 / R3 / DRAFT-AND-PING | leads with the no-code Admin route; no date inferred from the first import event |
| 7 | product filtered out on the iPad (J-bad-2) | 10 / R2 / DRAFT-AND-PING | counts every gate, including the image gate; "refresh" only if it changes the server-side result |
| 8 | new items still rejected (J-bad-3) | 10 / R3 / DRAFT-AND-PING | names the missing collection codes; does not say "collections are there" |
| 9 | header mismatch on an import (C-bad-1) | 3 / R3 / DRAFT-AND-PING | states the mismatch (name the two headers), not a cause |
| 10 | inventory script path (C-bad-2) | 3 / R3 / DRAFT-AND-PING | the verified fix (the path) is in the first line, not only in the owner notes |
| 11 | order emailed with no server row (D-bad-1) | 4 / R2 / DRAFT-AND-PING | does not ask for what the attachment holds; no "I can't open the attachment" in client text |
| 12 | sign-in versus sync check (B-bad-1) | 2 / R2 / DRAFT-AND-PING | names the event it saw; times match the sign-in row |
| 13 | Portal shows open orders only (K-good-1, K-bad-1) | 11 / R7 / ESCALATE | scope claims are counted ("open orders only"); no "every order"; owed timeline handled as a chase |
| 14 | order download versus Portal upload (K-good-2, K-bad-2) | 11 / R3 / DRAFT-AND-PING | says "isn't in the download file", not "doesn't store" |
| 15 | half-corrected earlier claim (F-bad-1) | 6 / R6 / ESCALATE | corrects both earlier claims; states the image gate |
| 16 | balance question (E-bad-1) | 5 / R4 / ESCALATE | no balance stated from a mirror; another org's billing not disclosed |
| 17 | feature request with no timeline (L-bad-1) | 12 or 14 / R7 / ESCALATE for a chase | no "once it's in" or delivery implication |
| 18 | recap with three errors (N-bad-1) | 15 / R5 / ESCALATE | no "I asked" without the record; no concession the transcript contradicts; import queried at T before "imported" |
| 19 | own-notes contradiction (N-bad-2) | 15 / R5 / DRAFT-AND-PING | cross-read copy against owner actions finds no conflict |
| 20 | our framing carried onto the client (N-bad-3, N-bad-4) | 15 / R5 / DRAFT-AND-PING | uses the client's own words for the surface; asks for nothing it does not need |

Cases 1 to 20 cover 13 of 16 types. **No case yet for types 1, 13 and 16** (automated, how-to, outage); add:
one automated-feed case (asserts no reply), one documented how-to (asserts SEND-SAFE with a cited answer), one fleet-incident case
(asserts the fleet check ran before any client-side cause).

## Assertion form

Each case file has: the packet path, the expected type, expected response type, expected category and clause, and a list of
assertions of three kinds:

- **Absent:** a string shape that must not appear in the client text (for example, "we need" followed by the KB field list).
  Checked by the lint where it is mechanical, else by the verifier.
- **Present:** a fact the copy must state (for example, "the group default price level is null").
- **Structural:** category, type header, response type, length band, Owner actions present, every commitment mapped to an action.

## Scoring

- Per case: pass only if every assertion holds and a separate grader finds no false or unsupported client sentence.
- Per run: the four numbers above, plus type accuracy and shape conformance. Report counts, not a percentage, below 20 cases.
- **Human blind check:** the owner grades a sample of at least 5 drafts by hand, with the sent reply and outcome hidden until after he
  has judged. Until then the run is described as "graded by a model, not a human".

## Not decided here

- Whether the golden set lives in agent-factory under `standards/evals/gold_sets.md`'s convention (to be read, not yet read).
- Where the packet builder's outputs are stored for Windmill-only tests (`PORT_PLAN.md`, deliverable 2).
