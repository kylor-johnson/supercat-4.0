# HANDOFF — Bet A: rewrite the three SERV tickets in Brent's voice

**Date:** 2026-08-03  
**Owner:** Kylor Johnson (PO)  
**Prior session:** [Bet A ticket evidence + capture work](c8df62f7-3c49-4e14-8b2e-31b16c77c4b7)

---

## What happened and why this handoff exists

Brent (engineering lead) asked for the Bet A ticket descriptions to be rewritten
in plain language with reproduction links. Multiple agent sessions rewrote
Confluence pages, posted comments as Kylor, and produced overlapping draft files.
It's gotten tangled. This session has one job: **produce final paste-ready text
for SERV-2447, SERV-2448, and SERV-2449** that gives Brent a link he can click,
a plain-language description of the bug, and a clear definition of done.

Brent's exact ask (Slack, 2026-07-30):  
> "we just want to see a more human explanation like 'when I change the filter it
> doesn't update' with a link to a page that I can reproduce. Then, when I change
> the code, I can test that and see it working."

---

## Hard rules — read before touching anything

- **Jira is READ-ONLY.** Never call any write tool. Every edit below is drafted in
  chat and Kylor pastes it himself. Do not call `editJiraIssue`, `addCommentToJiraIssue`,
  or any Jira write.
- **Confluence writes are gated.** Ask explicitly before touching any page. Prefer
  amendments that leave existing content visible. Do not invent acceptance criteria.
- **Verify before restating.** Prior agents circulated fixture lists that turned out
  to be wrong. If you cannot verify a claim, mark it as unverified rather than
  repeating it as fact.
- **Postgres MCP is read-only and available.** Use it to re-derive any number you
  need. Do not use stale figures.
- Source code is at `~/supercat-code/supercat_server` (Rails). Read it if needed.

---

## Primary objective

Produce three paste blocks — one per SERV ticket — that replace the current
ticket description bodies. Each block must:

1. Open with a one-sentence plain-language statement of what's broken
2. Include at least one URL Brent can paste into his browser right now to see the bug
3. State what he should see after the fix
4. Keep any existing diagnosis code pointers (they are correct)
5. Not exceed one screen of scrolling on the ticket

Kylor will paste each block himself. You draft, he applies.

---

## Current state of the three SERV tickets (as of 2026-07-30, verify by re-reading)

All three are **To Do**. None of the prior drafted paste blocks have been applied.

### SERV-2449 — Customers period column and malformed export (EBR-91)

Current description still says:
- "CY/LY blocks ignore the date dropdown; selected-range export column only appears
  for `previous_ytd` / `custom`" — correct diagnosis but not human-readable
- Acceptance is A2.1–A2.4 shorthand — not executable
- Diagnosis pointer `ecat_customers_controller.rb ~294` is correct, keep it
- Does NOT mention the malformed CSV (A2.5)
- Frames it as a math bug — it is a **display-gating defect**, not a math defect

**This is the only ticket Brent can start coding today.** No non-admin login or
warehouse build required.

### SERV-2447 — Invoices territory filter (EBR-40)

Current description still has:
- Stale evidence figures (~1,404 / $1.46M — from 2026-07-21, now wrong)
- Stale code pointer `warehouse_access.rb ~424–434` (cite the method name:
  `territory_code_limit_common_table_expression`, lines 999–1059)
- Verify line does not mention the admin short-circuit blocker
- No mention that the 2026-07-28 captures were void

**Verification blocked** until: (a) non-admin test user exists on wwjc and
(b) portal warehouse build runs. Status of the test user is unknown — ask Kylor
or check Postgres for a recently-created `WW only Reps` account on wwjc.

### SERV-2448 — Dashboard territory scope (EBR-212)

Current description still says:
- `**Verify:** wwjc — Office/SuperCat or dash-enabled multi-terr rep`
- This fixture **does not exist**. All 22 wwjc user types have `view_dashboard: false`,
  including the one named "Office - All - Dashboard". The Dashboard was only reachable
  in prior captures via the admin short-circuit.

**Verification blocked** until A1.2 fixture is decided (new wwjc user type, or `bri`/`alugo`).
Brent can code this without it; the blocker is only on verification.

---

## Verified facts — confirmed against production, reuse freely

**Code:**
- `OrgUser#is_admin?` is true if EITHER `org_users.is_admin` OR `users.is_admin` is set.
  `UserTypePermissions.may?` returns true for every permission on an admin without reading
  the user type. So any admin login bypasses all territory permission logic entirely.
- `Kylor_Johnson` on wwjc is admin on both columns. Every capture taken on that account
  is void for territory criteria.
- Portal reads territories from `rep_to_territory_bridge` joined to `rep_dimension.username`
  (`warehouse_access.rb:1040–1047`). Does NOT read `org_users.territory_codes` directly.
- `territory_code_limit_common_table_expression` has three branches (lines 999–1059):
  all-totals/admin (1002), associated-customer (1012), normal rep (1040). Only the third
  makes empty territory columns decisive.
- EBR-91 root cause: `ecat_customers_controller.rb:293–295` uses `String#[]`, a substring
  match, so only ranges whose name contains "previous_ytd" or "custom" render the period
  block. The value is discarded at lines 25 and 59. Display-gating only; math is correct.
- The CSV export has 9 header fields and 10 data fields on every row. The unlabeled 10th
  column carries a customer class (DN / WS).

**Data (verified against Postgres):**
- All 22 wwjc user types have `view_dashboard: false`. No rep-shaped account on wwjc
  can open the Dashboard.
- 0 of 14,030 wwjc shipping locations carry a territory code. The ship-to bridge fix
  will not move wwjc baselines.
- Every non-admin multi-territory rep on wwjc has an exactly additive book (no overlap).
- `rfreeman` (customer_number 10168) and `bulluckfurn` (customer_number 2155) are INVALID
  fail-closed fixtures — they take the associated-customer branch, not the normal rep branch.
  Do not cite them.

**Baselines — `SUM(portal_invoices.net_amount)`, re-derived 2026-07-30:**
- `105:1 Gigi Lane`, current YTD: 754 invoices / 250 accounts / **$823,224.99**
- `105:1 Gigi Lane`, June 2026: 110 invoices / 75 accounts / **$123,585.35** (closed, stable)
- `104 Madeline Cole`, current YTD: 764 / 228 / $1,113,363.57
- `104:1 Bella Scarpa`, current YTD: 0 / 0 / $0.00
- `95 BILL MINCHEW`, current YTD: 1,069 / 350 / $1,324,694.54
- `cmallon` union of six, current YTD: 1,479 / 432 / $1,529,474.96 (re-derive on capture day)
- Org-wide: 10,535+ / $10,917,581+ (re-derive on capture day)
- Drift is ~+0.8%/week. Re-derive on capture day. Closed periods are stable.

**Fail-closed fixtures (non-admin on both columns, no customer_number, rep user type):**
- `territory_codes` is NULL: `tomo`, `jkinch`, `highpoint` (all `WW & CH Reps`)
- `territory_codes` is `[]`: `jamiegatto`, `fperez`, `moxielighting` (`WW only Reps`) ·
  `ehysler`, `gclark1`, `jrawlins`, `scooth3` (`WW & CH Reps`) ·
  `atlantashowroom` (`ATL Sales Reps`) · `mark` (`CH only Reps`)

**Portal link bases (wwjc):**
- Wildwood: `https://supercat.supercatsolutions.com/wwjc/e/wwfc-2`
- Chelsea House: `https://supercat.supercatsolutions.com/wwjc/e/ch-2`
- Pages: `/invoices`, `/customers`, `/portal` (Dashboard)

**Territory casing:** comes from the warehouse, downcased — use `105:1 gigi lane` in URLs.
If a link returns nothing, tick the box in the UI once and copy the resulting URL.

---

## Evidence captured 2026-07-30 (use this to write the ticket descriptions)

### Customers screenshots (admin account — valid for A2.x, which is permission-independent)

Seven screenshots taken by Kylor showing the period column absent/present:

| Date range | Territory filter | Period block shown? |
|---|---|---|
| Current YTD | none | No |
| Previous YTD | none | Yes ($8,687,297) |
| Custom 2026-06-01–06-30 | 105:1 gigi lane | Yes ($123,585) |
| Previous Month | 105:1 gigi lane | No |
| Current YTD | 105:1 gigi lane | No |
| Previous Year | 105:1 gigi lane | No |
| Previous YTD | 105:1 gigi lane | Yes ($708,089) |

Screenshots are at:
`~/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-com-apple-CloudDocs-SuperCat-4-0/assets/Screenshot_2026-07-30_at_12.3*.png` and `12.4*.png`

### CSV export (2026-07-30)

File: `~/Downloads/WildwoodChelsea House Eol Customers Report 2026-01-01 - 2026-07-30.csv`

- Header: 9 fields (Bill to Code, Customer, City, State, Last Year Sales, Current Year
  Sales, Current YTD Sales, Backlog, Last Order)
- All 1,156 data rows: 10 fields
- Unlabeled 10th column: DN (998 rows), WS (158 rows)
- Column sums: LY $1,300,171.90 / CY $823,224.99 / Current YTD Sales $823,224.99 /
  Backlog $239,293.95
- The "Current YTD Sales" column IS populated in the export ($823,224.99) but absent from
  the screen — that's the defect.

---

## Local files — read these, do not treat as authoritative for Jira paste

In `SuperCat 4.0/PM/sales-portal-agent-starters/cycle-04-outputs/`:

| File | What it is |
|---|---|
| `BET-A-AC-HUMAN-REPRO-draft.md` | Plain-language repro doc written in response to Brent's ask. Good source material for ticket descriptions. |
| `TICKET-EDITS-bet-a-2026-07-30.md` | Earlier paste-ready blocks. Baselines now stale ($812,857.19 → use $823,224.99 for 105:1). Use as structural template only. |
| `JIRA-EDITS-bet-a-2026-07-29.md` | Earlier draft. Superseded for SERV tickets by the 07-30 file. Treat as untrusted. |

---

## Confluence pages — read-only unless Kylor approves a specific edit

| Page | State | What still needs doing |
|---|---|---|
| [1819836417 — Bet A AC](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1819836417) | v3, agent-rewritten without Kylor's approval. Contains two invalid fixtures (rfreeman under A1.4, bulluckfurn under A1.5) and is missing `mark` from the A1.5 list. | Fix fixture errors only — do not rewrite the page. Ask Kylor before making any edit. |
| [1819901953 — Verification & Evidence](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1819901953) | v7. Same fixture errors (rfreeman, bulluckfurn, missing mark). Kylor's own comments 1820229633 and 1820786689 are intact — do not touch. | Fix fixture errors. Kylor also owes an endorsement comment — ask if he wants to add it. |
| [1820262402 — Eng Implementation Plan](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1820262402) | v1, Brent's. | Comment 1821179905 (agent-posted as Kylor, no replies) should be deleted by Kylor. Confirm whether he's done this yet. |

---

## What to do, in order

### Step 1: Re-read the three SERV tickets live

The tickets may have changed since 2026-07-30. Read them fresh before drafting anything.
`getJiraIssue` for SERV-2447, SERV-2448, SERV-2449.

### Step 2: Ask Kylor two quick questions before drafting

1. Did you create the test user on wwjc? If yes, what username?
2. Has the warehouse build run since then?

These affect what SERV-2447 says about the Verify line.

### Step 3: Produce three paste blocks, one per ticket

**Each block must meet Brent's ask:**
- Plain-English sentence: what's broken
- At least one clickable URL that shows the bug right now
- What the correct behavior looks like after the fix
- Keep the existing `### Diagnosis pointers` and `### Out of scope` sections exactly as they are

**Keep each block SHORT.** Brent is not reading a design doc. He needs a link and an outcome.

Present each block separately in chat. Do NOT write to Jira.

### Step 4: Note what Confluence still needs (don't write it yet)

After the tickets are drafted, flag the fixture errors on the AC and Evidence pages
to Kylor and ask if he wants you to produce the specific amendment text.

---

## What good looks like

Three paste blocks Kylor can apply in a single Jira sitting. No new Confluence pages,
no comments, no status transitions. After he pastes them, Brent can click a link on
each ticket, see the bug, and know exactly what "fixed" means.

---

_Generated 2026-08-03. Prior session context: [Bet A ticket evidence + capture work](c8df62f7-3c49-4e14-8b2e-31b16c77c4b7)._
