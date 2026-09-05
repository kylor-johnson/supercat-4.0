# Jira edits — Bet A, batched for one pass

**Date:** 2026-07-29 · **Owner:** Kylor · **Tickets:** EBR-40, EBR-212, EBR-91, SERV-2447, SERV-2448, SERV-2449

Jira is read-only via MCP, so nothing below has been applied. This is one batch —
apply it in a single sitting rather than in rounds. Six tickets, and only two of them
need more than a pointer change.

**Why these edits:** the AC has been rewritten into executable form, the 2026-07-28
"leak" is retracted, baselines were re-derived on 2026-07-29, and two of the fixtures
named on these tickets do not work. Confluence is now the source of truth; every
ticket currently cites a local `.md` path that engineering cannot open.

**Do not change any status.** SERV-2447/2448/2449 stay To Do, EBR-40/EBR-91 stay
Approved, EBR-212 stays In Progress. Nothing here is a transition.

---

## 1. Global pointer change — all six tickets

Every ticket cites local PM file paths as the AC or eng source of truth. Replace
those lines wherever they appear.

**Find (varies slightly per ticket):**

```
**AC:** FILTER-TRUTH-AC AC-A1.1 / A1.3 / A1.4
**Eng SoT:** `PM/sales-portal-agent-starters/cycle-03-outputs/ENG-HANDOFF-bet-a-b-c-e.md` §C.1
```

**Replace with:**

```
**AC (source of truth):** Bet A — Filter Truth AC (EBR-40 / EBR-212 / EBR-91)
  https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1819836417
**Code map:** Bet A — Eng Handoff (filter truth: AC to code map)
  https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1819869185
**Eng plan:** Bet A — Eng Implementation Plan (SERV-2447 / 2448 / 2449)
  https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1820262402
**Verification record:** Bet A — Verification & Evidence (wwjc)
  https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1819901953

The local PM `.md` files are the PM working copy and are no longer citable.
```

---

## 2. SERV-2447 — invoice list

### 2a. Replace the `**Verify:**` line

**Find:** `**Verify:** wwjc · `cmallon` · Current YTD · territory `105:1 Gigi Lane``

**Replace with:**

```
**Verify:** wwjc · cmallon (non-admin, WW only Reps, six territories, all-customer
sales totals false) · Current YTD · territory `105:1 Gigi Lane`.
BLOCKED: product has no non-admin login. See AC page §1.1 — nothing on this ticket
can be verified until impersonation, a password reset, or a non-admin test user exists.
```

### 2b. Replace the whole `### Acceptance` block

The shorthand is not testable. Point at the executable clauses instead of restating them.

**Replace with:**

```
### Acceptance

Executable steps, named accounts and derived figures are on the AC page — clauses
A1.1, A1.3, A1.4, A1.5, A1.6, A1.8. Do not re-state them here; the page is the
source of truth and the figures move.

Summary of what must hold:

* A1.1 — cmallon on Invoices, Current YTD, `105:1 Gigi Lane` selected: every row
  belongs to a customer in that territory, and the header total equals the sum of
  exactly those invoices. Pass within 0.05% of a same-day baseline.
* A1.3 — cmallon with nothing selected: the total is the union of her six assigned
  territories, never the company book, and the filter offers only those six.
* A1.4 — a rep whose `territory_codes` is NULL: empty list, $0.00, and the message
  "No territories are assigned to your account — contact your administrator."
  Never the company book.
* A1.5 — same test where `territory_codes` is `[]` rather than NULL. Separate
  criterion: nine wwjc accounts carry `[]`, four carry NULL, and they reach the
  same guard as different values.
* A1.6 — a territory with a genuinely empty book returns $0.00 and does not fall
  back to a wider book. This is the criterion that catches "empty result treated
  as no restriction."
* A1.8 — the territory selection survives a drill-through.
```

### 2c. Replace the `### Evidence (2026-07-21)` block

The figures are stale and drift about +0.8% per week.

**Replace with:**

```
### Baselines — derived 2026-07-29, re-derive on the capture day

Bill-to book, `SUM(portal_invoices.net_amount)`, Current YTD = 2026-01-01 through
the derivation date.

| Scope | Invoices | Accounts | Invoiced net |
|---|---|---|---|
| `105:1 Gigi Lane` | 747 | 246 | $812,857.19 |
| `105:2 Katherine McMullan` | 579 | 135 | $531,730.44 |
| `105:3 Weezie Ward` | 104 | 30 | $127,853.05 |
| `105:4 Susan Rutherford` | 49 | 21 | $57,034.28 |
| `105:5 Grace Ingram` | 0 | 0 | $0.00 |
| `105:6 Krissa DeGennaro Newell` | 0 | 0 | $0.00 |
| Union of the six — cmallon's correct default book | 1,479 | 432 | $1,529,474.96 |
| Org-wide — contrast only, never a rep's book | 10,535 | 2,643 | $10,917,581.97 |

Two things a tester will otherwise mis-call:

1. **Two of the six territories are legitimately empty.** Selecting `105:5` or
   `105:6` and seeing nothing is the correct answer, not a bug.
2. **cmallon's book is exactly additive** — the four non-empty territories sum to
   $1,529,474.96, matching the union to the penny, because none of her customers
   is shared between two of her six. Earlier text on this ticket implied the parts
   would exceed the whole. They do not. Non-additivity is real on the org (1,153
   customers sit in both `105:1 Gigi Lane` and `40 Daniel Ratchford`, the two-brand
   structure) but it cannot be demonstrated on this account.

Baselines drift as invoices land inside closed windows — the same query for the same
window returned $10,478,474.02 org-wide on 07-21, $10,871,602.36 on 07-28 and
$10,917,581.97 on 07-29. **Any capture against a baseline from an earlier day is
invalid.** The derivation query is on the AC page §3.2. Closed periods are stable:
June 2026 has been $123,585.35 across three derivation dates.

Tolerance: the screen sums `sales_fact.amount_invoiced` while these sum
`portal_invoices.net_amount` (Q1 keeps that split deliberate), so pass within 0.05%.
```

### 2d. Correct the diagnosis pointer

**Find:** `* `warehouse_access.rb` ~424–434 — empty keys + all-totals leak`

**Replace with:**

```
* `warehouse_access.rb` ~424–434 — empty territory keys may be treated as "no
  restriction" rather than "no access". **Unverified inference, not evidence.** It
  was inferred from UI behavior on an admin account, which proves nothing, and the
  warehouse is not readable from the application database. A1.6 is the criterion
  that would actually demonstrate it. One eng query settles whether
  `rep_to_territory_bridge` has any rows for cmallon.
```

### 2e. Add a note block

```
### Note — the 2026-07-28 "exposure" finding is retracted

A capture that appeared to show a rep-shaped account the entire company book was
taken on a SuperCat staff login that is admin on both `org_users.is_admin` and
`users.is_admin`. `UserTypePermissions.may?` short-circuits to true for admins
without reading the user type, so `access_all_customer_sales_totals = false` was
never consulted. **Severity is not escalated. This remains a filter-correctness
bug, not a demonstrated data-exposure defect.**

Changing the admin short-circuit is explicitly out of this bet and needs its own
ticket.
```

---

## 3. SERV-2448 — dashboard

The fixture on this ticket does not exist. This is the most important edit in the batch.

### 3a. Replace the `**Verify:**` line

**Find:** `**Verify:** wwjc — Office/SuperCat or dash-enabled multi-terr rep`

**Replace with:**

```
**Verify:** NOT on wwjc. All 22 wwjc user types have `view_dashboard: false` —
including `Office - All - Dashboard` despite its name. There is no rep-shaped
account on this org that can open the Dashboard, so A1.2 has no fixture here and
the earlier plan of "cmallon with the dashboard temporarily enabled" means editing
a user type carrying 19 live production users.

Verify on `bri` as `alugo` (Primary_External_Sales_Reps, non-admin on both columns,
`view_dashboard` true, all-customer totals false, three territories) — standard
resolution path, same as wwjc. Second capture on `shl` as `rjazimi`, labeled
match-mode, since `territory_access_via_rep_number` is enabled for that org.
Derive that org's baselines separately with the query on the AC page §3.2.
```

### 3b. Replace the `### Acceptance` block

```
### Acceptance

A1.2 on the AC page. Log in as a non-admin rep with dashboard permission and
multiple territories. On Invoices, set Current YTD, select one territory, record the
header total. Without changing the range or the selection, open the Dashboard.

Pass: the invoiced KPI equals the Invoices header total from the same session within
0.05%, allowing ±$1 for the Dashboard's whole-dollar rounding, and no Top-N entry
belongs to an unselected territory.

Fail: the KPI shows the rep's full book while one territory is selected, or shows the
company book, or Top-N includes customers outside the selection.

Also in scope per Q16 and Q17: the drill-through carries the territory parameter, and
the Top Territories panel gets a non-additivity footnote (behavior unchanged).
```

---

## 4. SERV-2449 — Customers period and export

The framing is wrong on this ticket in a way that will cost engineering time: it reads
as a math bug and it is a display bug.

### 4a. Replace the `### Problem (current)` block

```
### Problem (current)

**This is a display-gating defect, not a math defect.** Every figure the Customers
page computes reconciles to SQL exactly; six of the eight date ranges refuse to
render the period figure, and the export already contains it.

Proven on the 2026-06-01..2026-06-30 export for `105:1 Gigi Lane`: the CSV carries a
Previous Month Sales column summing to **$123,585.35 across 75 accounts**, matching
`SUM(portal_invoices.net_amount)` for June 2026 to the penny — while the screen
showed no June figure anywhere. That is the cleanest single statement of EBR-91.

Only `previous_ytd` and `custom` render the selected-range block, because of an
accidental `String#[]` substring gate. **The default range is one of the six that
renders nothing**, so a rep who never touches the picker never sees a period figure.
The one block that does render prints without cents while every neighbour prints cents.

CY/LY/Backlog held identical values across every range tested, confirming they ignore
the picker entirely — intended per Q4, needing an honest relabel rather than a
behavior change.
```

### 4b. Replace the `### Acceptance` block

```
### Acceptance

Executable steps on the AC page — A2.1 through A2.5.

* A2.1 — the selected-range block renders on the default range (Current YTD), with
  cents, derived through `Eol::DateRanges`.
* A2.2 — it renders on all eight dropdown options. On Previous Month with June 2026
  selected it reads $123,585.35 across 75 accounts. An unrecognized `date_range`
  falls back to the default rather than resolving to `[nil, nil]`.
* A2.3 — every export column sum equals its on-screen block. **This already holds on
  all four columns, so treat it as a regression guard rather than a fix target.** The
  header total must be the column summed across all filtered accounts, not just the
  visible page, both respecting search text and territory.
* A2.4 — the export is structurally well formed. See below.
* A2.5 — CY/LY are labeled as fixed calendar anchors ("Calendar year 2026 · Jan 1 –
  Dec 31") with the selected-range column shown beside them. Label only; the ranges
  do not move.
```

### 4c. Add the malformed-CSV block — this is new scope, confirmed in scope by the PO

```
### The export is structurally malformed — in scope

Confirmed by field count on the 2026-07-28 artifact:

* Header row has **9** fields: Bill to Code, Customer, City, State, Last Year Sales,
  Current Year Sales, Previous Month Sales, Backlog, Last Order.
* All **1,154** data rows have **10** fields.
* The unlabeled tenth column carries a customer class: `DN` on 996 rows, `WS` on 158.

Any consumer parsing by header position mis-maps or silently drops a field. This is
the concrete form of the `sarreid` automation risk behind Q12 and is arguably a
larger export defect than the missing column.

Note also that the current header is range-specific ("Previous Month Sales"). Per Q12
it becomes the stable header `Selected Range Sales`, with the actual range printed in
a scope header block, plus a totals row per Q11.
```

### 4d. Correct one stated cause

**Find** the cause describing the per-row column as unfiltered and page-scoped.

**Replace with:**

```
* The per-row column being unfiltered and page-scoped **does not reproduce on the
  export path** — 1,154 rows is the whole territory-filtered set, not one page. The
  header-versus-row split may still be two queries in code; it is not producing a
  reconciliation error in the export today.
```

### 4e. Add a scope note

```
### Not observable on wwjc

Q13 — "CY Sales includes future-dated invoices" — is real in code but cannot be
demonstrated here. wwjc has zero invoices dated later than today, so calendar-year
and through-today cover the same invoices. Needs a different org to observe.
```

---

## 5. EBR-40 — program ticket

### 5a. Same `**Verify org:**` change as SERV-2447 §2a, and the same baseline block replacing `### Evidence (validation 2026-07-21)`

### 5b. Mark the preserved original request as stale

The `### Original request (pre-shaping — preserve)` block with the two Kalco URLs
stays — it is the ticket's history. Add immediately beneath it:

```
**This repro is stale — verified 2026-07-21. Do not cite it as evidence.** Ferguson
bill-to `0010023` is assigned to territory `0999`, no 2021-02-17 Ferguson invoice
remains, and that account's ship-tos are not `0016`. It also describes invoice-level
territory matching, which Q2 rules out of scope: territory is a property of the
customer and location master, and the filter selects which accounts appear rather
than slicing an individual invoice. Invoice-level rep matching is EBR-180 / SERV-2178.
Use the wwjc baselines above as the modern proof.
```

---

## 6. EBR-212 — program ticket

Same fixture correction as SERV-2448 §3a. Replace:

**Find:** `**Verify org:** wwjc — Office/SuperCat or dash-enabled multi-terr rep`

**Replace with:**

```
**Verify org:** `bri` as `alugo` — NOT wwjc. No wwjc user type grants
`view_dashboard`, so A1.2 has no fixture on that org. Second capture on `shl` as
`rjazimi`, labeled match-mode.
```

---

## 7. EBR-91 — program ticket

Pointer change only (§1), plus the display-gating reframe from SERV-2449 §4a and the
malformed-CSV block from §4c. No other change.

---

## 8. What is deliberately NOT in this batch

| Item | Why |
|---|---|
| Any status transition | Nothing has been verified, so nothing has moved. |
| Severity escalation on SERV-2447 | The exposure finding is retracted. |
| A new ticket for the `may?` admin short-circuit | Brent is drafting it; it is out of Bet A and needs its own prioritization. Do not create it as part of this batch. |
| A new ticket for the ship-to bridge casing fix | It is Phase 1 of SERV-2447's foundation PR per the eng plan. It needs its own verification org (`cci`, `ta`, `ih`, `bmc2` or `gb`) but not its own ticket unless Brent wants one. |
| Anything about EBR-87 | Parked with evidence; unchanged. |
| EBR-7 | Closeable on the existing evidence; separate conversation, not this batch. |
