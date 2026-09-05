# HANDOFF — Bet A: work out what Kylor still has to capture, test and decide

## Your job

Kylor is the PO on Bet A (Sales Portal filter truth). The acceptance criteria have been
rewritten twice, engineering has asked for plain-language reproducible bugs, and the
verification record has been reset after a batch of void captures. **Your job is not to
write more AC.** It is to read the current state and hand Kylor a single ordered list of
what *he personally* still has to do: which screenshots/captures to take, which are
possible today versus blocked, which acceptance criteria are still unproven, and which
decisions are outstanding.

Separate ruthlessly into two buckets:

1. **Doable today on Kylor's existing admin login** — permission-independent defects.
2. **Blocked on a non-admin rep login** — everything that depends on territory scoping.

That split is the whole value of this pass. Getting it wrong wastes his week.

## Hard rules — read before doing anything

- **Jira is READ-ONLY.** No comments, transitions, field edits, links. Ever. Draft text and
  hand it over. Brent has agreed the tickets should be edited, but **Kylor pastes**, not you.
- **Confluence writes are gated.** Ask before every single page or comment write. Prefer
  amendments and strike-through over replacing a body. Never invent acceptance criteria.
- **Anything you post publishes as Kylor.** Do not answer engineering's questions in his
  voice. Draft, hand over, stop.
- Postgres MCP is read-only and working — use it freely.
- Source code is at `~/supercat-code/supercat_server` (Rails). Read it; don't guess.
- **Verify before you restate.** Two prior agents got in trouble here: one exceeded its
  mandate on writes, and both circulated fixture lists that turned out to be wrong. Kylor is
  under CTO criticism specifically for unverified acceptance criteria. A claim you can't
  reproduce is worse than no claim.

## Read these first

In `SuperCat 4.0/PM/sales-portal-agent-starters/cycle-04-outputs/`:

| File | What it is |
|---|---|
| `BET-A-AC-HUMAN-REPRO-draft.md` | The AC rewritten as reproducible defects with real URLs. Current as of 2026-07-30. |
| `TICKET-EDITS-bet-a-2026-07-30.md` | Paste-ready description blocks for SERV-2447/2448/2449 plus a light-touch option for EBR-40/212/91. Nothing pasted yet. |
| `JIRA-EDITS-bet-a-2026-07-29.md` | Older draft from a prior session. Nothing was ever applied from it. Disposition undecided — treat as untrusted. |

Confluence, space `EOL`:

| Page | State |
|---|---|
| 1819836417 — Bet A — Filter Truth AC | **v3, agent-rewritten without approval.** Decision made but NOT yet executed: restore to v1 via page history, then add a dated header note saying the fixtures below are superseded. |
| 1819901953 — Bet A — Verification & Evidence (wwjc) | **v7, agent-rewritten.** Recommendation: leave v7 (v6 re-publishes a leak claim Kylor already retracted) and add his own endorsement comment. Not executed. Kylor's own comments 1820229633 and 1820786689 are intact — do not touch them. §5 has a capture-plan table worth reconciling against what's actually possible. |
| 1820262402 — Bet A — Eng Implementation Plan (Brent's) | Footer comment **1821179905** was posted by an agent as Kylor, has no replies, and should be deleted by him. Comment **1820655618** is Kylor's own — keep it. |

Jira (read only): SERV-2447 (invoices), SERV-2448 (dashboard), SERV-2449 (Customers),
EBR-40, EBR-212, EBR-91.

## Verified facts — confirmed against production 2026-07-30, reuse freely

- **All 22 wwjc user types have `view_dashboard: false`**, including `Office - All -
  Dashboard` and `z'-Bet A Verify`. No rep-shaped account on wwjc can open the Dashboard.
- **0 of 14,030 wwjc shipping locations carry a territory code**, in either
  `territory_codes` or `territory_codes_json`. The ship-to bridge casing fix cannot move
  wwjc baselines. Orgs that do have ship-to territory data: `cci` (75,088), `ta` (39,573),
  `ih` (33,294), `bmc2` (31,937), `gb` (30,960).
- **Baselines**, `SUM(portal_invoices.net_amount)` on the bill-to book, YTD through
  2026-07-30 — identical to the 07-29 derivation, nothing moved overnight:
  `105:1 Gigi Lane` 747/$812,857.19 · `105:2` 579/$531,730.44 · `105:3` 104/$127,853.05 ·
  `105:4` 49/$57,034.28 · `105:5` and `105:6` both zero · `cmallon` union of six
  1,479/$1,529,474.96 · `95 BILL MINCHEW` 1,069/$1,324,694.54 · `104 Madeline Cole`
  764/$1,113,363.57 · `104:1 Bella Scarpa` zero · `40 Daniel Ratchford`
  2,302/$2,503,022.96 · org-wide 10,535/$10,917,581.97 · `105:1` June 2026 110/$123,585.35.
- **Drift is real but not continuous.** Org-wide read $10,478,474.02 on 07-21,
  $10,871,602.36 on 07-28, $10,917,581.97 on both 07-29 and 07-30 (~+0.8%/week). Closed
  periods don't move: June 2026 has read $123,585.35 on four derivation dates. Re-derive on
  capture day and compare — don't assume movement.
- **Every non-admin multi-territory rep on wwjc has an exactly additive book.** Customer
  counts, sum of parts vs union: `cmallon` 1,971/1,971 · `dself2` 1,971/1,971 · `bminchew`
  1,782/1,782 · `bscarpa` 1,075/1,075. Zero overlap anywhere.
- **`105:1 Gigi Lane` is a complete subset of `40 Daniel Ratchford`** — 1,153 of 1,156
  customers in both, all 246 invoiced ones. Selecting both should return $2,503,022.96, not
  the arithmetic sum $3,315,880.15. Only `dratchford` holds `40 Daniel Ratchford` and it's
  his only territory, so demonstrating non-additivity needs a constructed account.
- **Fail-closed fixtures** — non-admin on both columns, no `customer_number`, on a rep user
  type. NULL (3): `tomo`, `jkinch`, `highpoint`. Empty array (9): `jamiegatto`, `fperez`,
  `moxielighting`, `ehysler`, `gclark1`, `jrawlins`, `scooth3`, `atlantashowroom`, `mark`.
  **`rfreeman` and `bulluckfurn` appear in older drafts and are invalid** — they carry
  customer_numbers 10168 and 2155, so they take a different code branch entirely.
- **`territory_code_limit_common_table_expression` has three branches**, at
  `warehouse_access.rb:999-1059`: all-totals/admin (1002) returns every territory in the
  org, associated-customer (1012) derives from the linked customer, normal rep (1040) reads
  `rep_to_territory_bridge` by username. Only the third makes empty territories decisive.
  The ticket's old pointer `~424-434` has drifted — cite the method name.
- **The portal never reads `org_users.territory_codes`.** It reads the warehouse bridge.
  So the wwjc warehouse build must have run or a correct implementation still shows nothing.
- **Admin short-circuit:** `OrgUser#is_admin?` is true if either `org_users.is_admin` or
  `users.is_admin` is set, and `UserTypePermissions.may?` returns true for everything on an
  admin without reading the user type. `Kylor_Johnson` on wwjc is admin on both. This is why
  the 2026-07-28 captures are void, and it's already publicly retracted.
- **EBR-91 mechanism:** `ecat_customers_controller.rb:293-295` uses `String#[]`, a substring
  match, so the per-row period column only survives when the range name contains
  "previous_ytd" or "custom" — 2 of 8 ranges. The value is computed correctly at line 23 and
  discarded at lines 25 and 59. That's why June's $123,585.35 is in the export but not on
  screen. Display gating, not a math defect.
- **Malformed export:** header has 9 fields, all 1,154 data rows have 10; the unlabeled
  tenth carries a customer class, `DN` on 996 rows and `WS` on 158.
- **URL format** (confirmed from EBR-40's preserved original request):
  `…/invoices?utf8=%E2%9C%93&date_range=current_ytd&multi-select-filters%5B%5D=%5B%22territory%22%2C%22105%3A1%20gigi%20lane%22%5D`
  Link bases: `https://supercat.supercatsolutions.com/wwjc/e/wwfc-2` (Wildwood, the `105:x`
  territories) and `/wwjc/e/ch-2` (Chelsea House). Date values: `all_available`,
  `current_ytd`, `previous_ytd`, `previous_year`, `current_mtd`, `previous_month`,
  `yesterday`, `custom` + `from_date`/`to_date`. Territory casing comes from the warehouse
  and is downcased — if a link returns nothing, tick the box in the UI and copy the URL.
- **The Kalco repro in EBR-40 is stale:** bill-to `0010023` is `FEI FERGUSON MAIN ACCOUNT`,
  assigned to territory `0999`, with 0 invoices on 2021-02-17. Keep as provenance, don't test.

## NOT verified — do not restate these as fact without checking

- The cross-org dashboard candidates `bri`/Primary_External_Sales_Reps (`alugo`,
  `jonmcmahan`, `dpatruno`), `jcusa`/Sales Reps, `shl`/Sales Reps SH/Mer/L1. `shl` is a
  match-mode org (`territory_access_via_rep_number` on). **Verify these if A1.2 is going to
  name them.**
- The CSV column sums other than June: Last Year $1,300,171.90/315 rows, Current Year
  $808,094.79/245, Backlog $245,657.50/510. Artifact is at
  `~/Downloads/WildwoodChelsea House Eol Customers Report 2026-06-01 - 2026-06-30.csv`.
  Only the June figure has been tied to SQL independently.
- Whether `/customers` with no `date_range` param at all raises — line 294 would evaluate
  `nil['previous_ytd']`. Nothing in that controller defaults the param.
- Whether the fail-closed path actually fails closed **downstream** of the empty
  customer-key set. The code suggests yes; nobody has proven it, and the void captures can't
  because they were on an admin.

## Do this, in order

1. **Read the three local files and the three Confluence pages.** Don't write anything yet.
2. **Build the two-bucket list.** For every acceptance criterion currently in play, say
   whether Kylor can capture it today on his admin login or whether it's blocked, and why.
   Be specific about which ones are permission-independent — that's the set he can clear
   this week.
3. **For each capturable item, tell him exactly what to screenshot.** URL, what has to be
   visible in frame, what number to compare against, and what makes the capture void. The
   existing rule is that a capture with no same-day derivation beside it isn't evidence, and
   any capture on an account that is admin on either column is void.
4. **Reconcile the §5 capture-plan table on page 1819901953 against reality.** It lists rows
   that cannot be run at all right now. Say which, and propose (don't apply) a corrected
   table.
5. **List the acceptance criteria that have no fixture anywhere**, with what would need to
   exist to make them testable.
6. **Surface the outstanding decisions** without deciding them: how non-additivity gets
   handled given no current rep can demonstrate it; which org or user type for the Dashboard
   criterion; what to do with the stale `JIRA-EDITS-bet-a-2026-07-29.md`; and whether the
   Confluence cleanup (delete comment 1821179905, restore AC page to v1, evidence page
   endorsement) has been executed yet — check, don't assume.
7. **Report in chat.** No page edits, no Jira writes, no new Confluence pages unless Kylor
   explicitly approves after reading your report.

## What good looks like

A single ordered checklist Kylor can work through, where every line is either "do this now,
here's the link and the expected number" or "blocked, and here's who unblocks it." Anything
you can't verify, mark as unverified in the line itself rather than in a footnote.

The one thing genuinely on the critical path is a **non-admin rep login for product** —
cheapest version is a new non-admin test user on wwjc, on the existing `WW only Reps` user
type, given `cmallon`'s six territories, so no live user and no shared user type is touched.
Zero territory criteria can be verified without it. If your report buries that, it's wrong.
