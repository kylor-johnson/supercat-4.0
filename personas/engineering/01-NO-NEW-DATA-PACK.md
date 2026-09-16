---
id: ENG-01
title: Engineering handoff — the four no-new-data items
version: 1.1
status: ready for engineering
date: 2026-09-15
owner: Kylor Johnson
engineering_reader: Brent Sanders
depends_on: [PROD-GAPS §D, PROD-MAP, JTBD-REG, SALES-PORTAL-SPEC]
supersedes: v1.0 (2026-08-27) seat-register IDs (JTBD-0xx / PER-0x)
---

# Four items, no new data required

**Read this whole file before starting. It is one conversation's worth of work, ordered.**

Job IDs are `JOB-*` from [`../analytics/jtbd-register.md`](../analytics/jtbd-register.md). Seats
(PER-01…08) are headcount, not the persona set — see
[`../00-PERSONA-GROUPS.md`](../00-PERSONA-GROUPS.md).

Every claim below is either cited to a checked-in file or labelled `[SQL 2026-08-27]` for a
read-only query run against production while writing this. Where something could not be verified it
says **UNKNOWN** rather than guessing.

**Order is deliberate:** A6 first. HQ jobs land on the Sales Portal
(`product/surface-mapping.md` §2) and A6 is the defect that undermines trust in every number
on it. Nothing downstream is worth building on an untrusted surface.

| # | Item | Size | Ticket | Status entering this pack |
|---|---|---|---|---|
| **A6** | Export/UI reconciliation | S | **EBR-91 / SERV-2449** | Body already written and approved — ship it |
| **A4** | Rep adoption view | S | none — needs one | **Re-scoped. Read §A4 before touching `enable_rep_activity`** |
| **A3** | Catalog completeness | S | none — needs one | Rule now defined; was undefined |
| **A2** | Inventory snapshot age | S | none — needs one | Mechanism confirmed |

These four are **shared HQ / buyer-honesty work.** They are not a universal field-rep analytics
surface. Field analytics is iPad-EC, job pack by persona group — `02-IPAD-ACCOUNT-BRIEF-SPEC.md`
is the **PG-01** pack, not the home screen for PG-05/PG-07.

---

## A6 — Export/UI reconciliation (EBR-91 / SERV-2449)

**Ship this first. The ticket body already exists and is approved.**

### Jobs and personas served

| Job | Group | Relationship |
|---|---|---|
| **JOB-HQ-5** Make the export match the screen | **PG-HQ** (VP / ops) | Direct — this *is* the job |
| JOB-HQ-1 Get one topline I can defend | PG-HQ (owner / VP) | Gated — a topline whose export disagrees is not defensible |
| JOB-01-3 / JOB-03-3 See only my territory, and trust it | PG-01 / PG-03 | Secondary metric is export-to-UI reconciliation rate |

`../PER-06-owner-exec.md` (seat evidence) states the dependency: *"three things must be true
before Intelligence is trustworthy: territory scopes the book; export reconciles to UI; quotes never
counted as sales."* A6 is the second of those three.

The documented trust failure: *"export ≠ displayed total [EBR-91], which makes this persona the one
who fields 'the CSV doesn't match' and rebuilds it by hand."* When the rebuild happens, Excel
becomes the real system of record and every downstream analytics job is dead on arrival.

### The specific defect

Three separate defects under one ticket. All three are `PROD-REPRO` as of 2026-08-04, recorded in
`PM/Sales Portal Docs/BRENT-ENGINEERING-QUEUE-2026-08-04.md` §4:

1. **Selected-period values calculated but hidden.** Previous Month is correctly calculated *and
   correctly exported*, but its total card and per-customer column are suppressed on the page.
   Previous YTD renders correctly (`PROD-PASS`). Root cause is an accidental Ruby substring test
   that admits only `previous_ytd` and `custom` — `00-SALES-PORTAL-SYSTEM-SPEC.md` §9.2.
2. **Malformed CSV — field/heading count mismatch.** Three independent 2026-08-04 exports each
   produced **1,965 rows, nine headings, and ten fields on every row.** The unlabelled tenth value is
   `DN`, `EP`, or `WS` — `CODE-IMPLICATION`: it is `PriceLevel.cue_character`.
3. **Top total scope.** The total must cover the complete matching customer set after search and
   territory filters, not only the visible page — spec §4.1 and §9.1.

Corroborating detail from the same exports: the two Current Month exports are byte-identical;
Previous YTD changes the heading to `Previous YTD Sales` and changes 408 selected-period values.

### Where it lives

Named in `00-SALES-PORTAL-SYSTEM-SPEC.md` §15 (code map) and §12 (export contract):

- `app/controllers/ecat_customers_controller.rb`
- `app/services/controllers/ecat_customer.rb`
- `app/views/ecat_customers/index.html.erb`
- `test/services/controllers/ecat_customer_test.rb`

The display-rule bug is the period-name test in the customers controller/service path; the CSV bug is
the header array in the export path failing to include the price-level cue column that the row
builder emits.

### Acceptance criteria

Taken verbatim from the approved SERV-2449 body (`BRENT-ENGINEERING-QUEUE-2026-08-04.md` §4) — do
not re-derive these:

1. Non-standing selected periods display their total and per-customer values.
2. Current YTD and Previous Year are not duplicated.
3. The top total covers the complete matching customer set after current search and territory
   filters, not only the page.
4. Page and CSV customer sets and selected-period values agree.
5. Preserve human-readable headings such as `Previous Month Sales`.
6. CSV header and every row have equal field counts.
7. Label the existing cue field `Price Level Cue`.
8. Preserve calculation sources and bill-to/ship-to behaviour.

**Tests required:** Previous Month fail-to-pass; Previous YTD remains passing; no standing-column
duplicates; complete filtered-set total; UI/CSV set and value parity; CSV field parity and label.

**Acceptance fixture — use a closed period, never Current YTD.** `00-SALES-PORTAL-SYSTEM-SPEC.md`
§13.2: `wwjc`, territory `105:1 Gigi Lane`, 2026-06-01 → 2026-06-30 = **110 invoices, 75 accounts,
`$123,585.35`.** Run as the restricted non-admin fixture `wwjc/betaverify` (§13.1), not as an admin —
spec §7.1: *"Admin sessions are invalid evidence for restricted-rep acceptance."*

### Explicitly out of scope

Inherited from the ticket body, and each of these has been argued once already: scope/preamble block
before the CSV header (it breaks normal CSV consumers — spec §12), totals row, generic
`Selected Range Sales` header, new date ranges, broad CY/LY relabeling, revenue definition changes,
shared territory-resolver work, and SERV-2196 bill-to/ship-to semantics.

### One correction to carry into this ticket

JOB-01-3 / JOB-03-3 (territory trust) were documented against EBR-40/212/91. **EBR-40 and EBR-212
are closed, not open.** `BRENT-ENGINEERING-QUEUE-2026-08-04.md` §6 records `PROD-PASS` on both —
restricted `betaverify`, Gigi Lane June 2026 displayed `$123,585` against `$123,585.35` in SQL;
Dashboard Current-YTD showed `$836,263` matching Invoices. Under spec §2.1 production behaviour
outranks documentation, so treat EBR-40/212 as closed. The live reproduced authorization defect is a
*different* one — direct-record out-of-book access (`INV65157`, email-invoice id `4667912895`,
customer `14378`), covered by the net-new authorization package in §3 of that queue, which is
sequenced **before** SERV-2449.

---

## A4 — Rep adoption view

> **Stop. `data-gaps.md` A4 describes this item incorrectly, and the correction changes the work.**

### What the docs assume, and what is actually true

`product/data-gaps.md` A4 reads: *"`enable_rep_activity` is on for 7 of 257 orgs `[MEASURED]`. Data
exists; the switch is off"* — implying JOB-HQ-3 is a config flip.

`[SQL 2026-08-27]` confirms the count exactly: **7 of 257 organizations** have
`organizations.enable_rep_activity = true`. But the flag does not gate what the register thinks it
gates.

Per `docs/REP_ACTIVITY_TRACKING.md` (2026-04-28) in `supercat_server`, `enable_rep_activity` gates a
**CRM-style rep activity logging pilot**: reps tap Call / Visit / Email buttons on the iPad against
the currently selected customer, records sync via `PUT /api/v1/:org/rep_activities/:uuid`, and admins
get a drafts index, an activities index, a customer timeline, and a Rep Activity dashboard. That
document's own §3 non-goals list includes, verbatim: *"Sales-portal / web view for reps."*

Two consequences:

- **It is a pilot, not a suppressed feature.** The 7 orgs are `demo`, `wwjc`, `kl`, `demo2`, `pebl`,
  `cst`, `bgu` `[SQL 2026-08-27]` — **two of the seven are demo orgs.** That is five real orgs in a
  deliberate phased rollout, which is what the plan document describes.
- **Ungating it would not serve JOB-HQ-3.** That job measures logins against seats.
  The pilot measures rep-logged activities, depends on the iPad client shipping the buttons, and
  would render empty tables in any org where reps have never tapped them.

`rep_activities` row counts are **UNKNOWN** — the read-only role returns `permission denied for
table rep_activities`, so actual pilot volume could not be verified.

**Decision taken 2026-08-27: build the login-based adoption view. Leave `enable_rep_activity` alone.**

### Jobs and personas served

| Job | Group | Metric |
|---|---|---|
| **JOB-HQ-3** Know the team is actually using it | **PG-HQ** (VP / ops / owner) | Reps active in 30d ÷ seats licensed |

Same underlying data at two altitudes (ops vs owner). The owner-facing view must never imply that
low SuperCat-submitted order volume is failed adoption — selling instrument ≠ order consummation.

This job **does not differ by selling motion.** Volume orgs and spec orgs both need the count. Do
not skip it for volume.

### The gap, and the fields it lives in

There is no view anywhere that renders active reps against seats. Both inputs exist:

| Input | Table.field | Verified |
|---|---|---|
| iPad last login | `org_users.last_ipad_login_at` | `[SQL 2026-08-27]` present |
| eOL last login | `org_users.last_ecat_online_login_at` | `[SQL 2026-08-27]` present |
| Rep vs buyer discriminator | `org_users.customer_number` blank ⇒ internal/rep | `../PER-00-persona-set.md` §1 |
| Orders per user | `orders` | `product/surface-mapping.md` |
| Seats licensed | `subscription_plans.user_limit` via `subscriptions.subscription_plan_id` | `[SQL 2026-08-27]` present |

**Reproduced numerator** `[SQL 2026-08-27]`, filtering `customer_number IS NULL OR = ''`:
**3,185 reps active in 30 days; 4,058 active in 90 days across 145 organizations.** The 90-day figure
reproduces `PER-00`'s 4,058 exactly, which is a good sign the definition matches.

**Denominator coverage is the real constraint.** Only **115 of 257 organizations** have an active
subscription carrying a `user_limit` `[SQL 2026-08-27]` (118 have any subscription row; 115 are
`status = 'active'` and have a non-null `user_limit`). So the ratio is computable for 115 orgs and the
count alone for the rest.

### Acceptance criteria

1. For an org with an active subscription and a `user_limit`, the view shows: reps active in the last
   30 days, seats licensed, and the ratio. Denominator is `subscription_plans.user_limit` for the
   org's `status = 'active'` subscription.
2. "Rep" means an `org_users` row for the organization with `customer_number` null or blank. A user
   with a `customer_number` is a buyer and must never appear in this count —
   `PER-00` §1(a): `should_show_customers_tab` requires `customer_number.blank?`.
3. "Active" means `greatest(last_ipad_login_at, last_ecat_online_login_at)` within the window, with
   nulls treated as never-logged-in, not as zero-age.
4. Where the org has no active subscription or a null `user_limit`, render the active-rep **count**
   and suppress the ratio. **Never substitute total user records for licensed seats** — that produces
   a ratio that looks authoritative and is wrong.
5. Window is configurable to 30 / 60 / 90 days; 30 is the default. A 90-day run against the whole
   estate must return 4,058 to match the baseline above.
6. **Mandatory honesty label on the surface:** low SuperCat-submitted order volume is **not**
   evidence of failed adoption — *"selling instrument ≠ order consummation."* Narrate activity;
   never imply failure. An owner-facing activity view implying otherwise would cause real, wrong
   personnel decisions.
7. Reps with no territory assignment still appear in the activity count. Fail-closed applies to
   *sales data*, not to *login counts* — an unterritoried rep is exactly who a VP needs to see.

**Tests:** an org with active subscription and user_limit (ratio renders); an org with no
subscription (count renders, ratio suppressed); a buyer record present in the org (excluded); a user
with both login fields null (excluded from active, included in seats); 30/60/90 window parity.

### Ticket

**None exists. Needs one.** Do not reuse or extend the `enable_rep_activity` pilot ticket — it is a
different feature with a different data path. Suggested title: *Sales Portal: rep adoption view —
active reps against licensed seats.*

### Also worth doing, separately

The rep-activity pilot is a real feature with a written, approved plan. Whether it graduates from 5
orgs is a product call about that feature, on its own evidence, and it is **not** in this pack.

---

## A3 — Catalog completeness aggregation

### Jobs and personas served

| Job | Group | Metric |
|---|---|---|
| **JOB-HQ-9** Find where the catalog is broken before a rep does | **PG-HQ** (merch) | Count of active items failing a completeness check |

Second-order beneficiary is the field: the decision this changes is *"whether a rep is embarrassed
in front of a customer."* That is why PG-07 still has a reason to open the iPad even if we skip an
L analytics panel.

**Motion note.** Completeness itself is **shared HQ work** — do not skip it for volume. Volume
catalogs are the largest (SEG-04 median ~4,498 products against median 30 collections), so paginate
and rank by fail count; eyeballing is tractable at 600 items and impossible at 30,000. What *does*
differ by motion is merch **grain for "what sold"** (JOB-HQ-8: collection vs velocity). This view is
the broken-catalog list, not sell-through. Do not condition completeness on segment.

### The gap

`data-gaps.md` A3: *"No new fields — images, prices and taxonomy all exist. Pure aggregation."*
Confirmed `[SQL 2026-08-27]` — every field needed is present on `products`. What was missing was not
data but a **definition**: the merch seat says *"no image, no price, no category"*, which is a
phrase, not a testable rule.

**Rule fixed 2026-08-27.** Three independent checks over active items.

### Fields and the rule

| Check | Condition | Field |
|---|---|---|
| Active item | `NOT deleted AND NOT hideable` | `products.deleted`, `products.hideable` |
| **No image** | `image_exists` is false or null | `products.image_exists` (boolean, maintained by image import matching) |
| **No price** | `net_price` is null or 0 **AND** `prices_json` is empty (`{}`, `[]`, `null`, or blank) | `products.net_price`, `products.prices_json` |
| **No category** | `category_codes` is empty **AND** `category_code` is blank | `products.category_codes`, `products.category_code` |

`collection_codes` / `collection_code` are **not** part of the rule — collection is a merchandising
grouping, not a completeness requirement, and treating a missing collection as a defect would swamp
flat volume catalogs.

### Baseline — run this and expect these numbers

`[SQL 2026-08-27]`, all orgs, active items only:

| Measure | Value |
|---|---|
| Orgs with active products | **240** |
| Active products | **938,394** |
| Failing **no image** | **179,577** (**19.14%**) |
| Failing **no price** | **48,061** |
| Failing **no category** | **1,158** |
| Orgs with at least one failing item | **210 of 240** |

Single-org control for a unit test — org id 26: **32,728 active products, 32 no-image, 0 no-price,
0 no-category.** A well-maintained large catalog yields a short, actionable list, which is the
behaviour the job wants.

Note that `no_category` is small (1,158 across the estate). That is the argument for keeping it in
the rule: it is signal, not noise.

### Acceptance criteria

1. The view reports, per organization: active item count, and a count for each of the three checks.
2. Each failing item is reachable as a list, filterable by check, exportable.
3. Only active items are counted — `deleted` or `hideable` items never appear.
4. The three checks are counted independently; an item failing two checks appears in both counts and
   is counted **once** in any "items failing at least one check" total. State which of the two a
   given number is.
5. Running the aggregation across all orgs reproduces the baseline table above within the drift
   expected from imports since 2026-08-27.
6. Org id 26 returns 32 no-image, 0 no-price, 0 no-category against 32,728 active products.
7. The view carries no new column on `products` and no schema change. If one appears necessary, stop
   and re-scope — that would move this item out of the no-new-data set.
8. Image check reads `image_exists` only. Do **not** re-derive image presence by parsing
   `images_json` or hitting the filesystem/FTP in the request path.

### Ticket

**None exists. Needs one.** Suggested title: *Admin Console: catalog completeness view.*
Surface is **Admin** per `product/surface-mapping.md` — this is where merch acts, and the fix
happens in the same place as the finding.

---

## A2 — Inventory snapshot age exposed to the UI

### Jobs and personas served

| Job | Group | Relationship |
|---|---|---|
| JOB-02-2 / 04-2 / 08-2 Know what's in stock before I promise it | PG-02 / 04 / 08 (buyers on eOL) | Direct — staleness disclosure is the gap, not the data |
| Every offline staleness rule | PG-01 / 03 / 05 field extracts | `product/surface-mapping.md` §3 requires an age line on the iPad extract |

**Scope decided 2026-08-27: both surfaces — the eOL buyer view and the iPad extract.** One timestamp,
two renderings. iPad-EC staleness rules cannot be implemented without it, and the iPad side is the
larger population (4,058 active reps). Buyer-side fit still follows motion: spec/trade high,
volume fringe.

### The gap, and the mechanism — confirmed

`data-gaps.md` A2: *"The import timestamp exists; it is simply never surfaced."* True, and the
mechanism is now pinned down.

`[SQL 2026-08-27]`: **inventory import is a full delete-and-recreate per organization.** On every org
sampled, `created_at = updated_at` on every row, and all rows in an org fall inside a single import
window of roughly one to six minutes. Example — org 277: 41,388 rows, all written between
`2026-08-26 13:11:09` and `13:13:29`.

**Therefore `max(inventories.updated_at)` grouped by `organization_id` is an exact snapshot
timestamp.** No new column, no new table, no parse.

**Do not use `import_events` for this.** `[SQL 2026-08-27]` its columns are only
`id, created_at, organization_id, data`, where `data` is a YAML blob keyed by import type
(`"Images"`, `"Option Images"`, …). Deriving inventory freshness from it means parsing YAML text —
fragile, and unnecessary given the above.

Where distribution centres are in play, group by `distribution_center_id` as well — it exists on
`inventories` and one org in the estate carries up to 5 `[SQL 2026-08-27]`.

### Why it matters, sized honestly

`[SQL 2026-08-27]`, joining snapshot age to buyers active in 90 days:

| Snapshot age | Orgs | Orgs with an active buyer | Active buyers exposed |
|---|---:|---:|---:|
| Fresh (< 7 days) | 73 | 28 | 17,692 |
| Stale 7–180 days | 15 | 4 | 490 |
| Stale > 180 days | 99 | 2 | 87 |

**The headline is not "99 stale orgs."** Most stale-inventory orgs are dormant. The acute buyer-facing
exposure is **6 orgs and roughly 577 active buyers** being shown availability with no age indicator.
The worst single case found is an org whose inventory last imported **2021-01-04** — five and a half
years old, still rendering as current.

That is a modest buyer population. The larger case is the rep side: the same snapshot feeds 4,058
active iPad reps, and iPad-EC's entire staleness contract depends on this timestamp existing in the UI.

### Acceptance criteria

1. `max(inventories.updated_at)` per organization (and per `distribution_center_id` where the org uses
   them) is exposed as a snapshot timestamp on the read path that serves availability.
2. **eOL buyer view:** anywhere `qty_available` or `next_scheduled_receipt_date` is rendered, the
   snapshot age is rendered with it, non-modally, in the same visual unit as the quantity. Never show
   a quantity without its age.
3. Age renders as an absolute local time plus a relative age — *"As of Tue 9:14am — 2 days old."*
   Not a bare relative age; a rep or buyer quoting a number needs the timestamp.
4. **iPad extract:** the snapshot timestamp is carried into the extract at sync and rendered by the
   same rule. See `02-IPAD-ACCOUNT-BRIEF-SPEC.md` §4.
5. Past the acceptable window the numbers still render, with a visible warning state — **never an
   empty state where cached data exists**. A stale number with its age beats a spinner.
6. Where an org has never imported inventory (no rows), render "inventory not provided" — not a zero,
   not a blank. Prior work bars rendering absent data as `$0`/`0`.
7. Anything a buyer or rep would quote to a customer, past its window, is labelled as needing
   confirmation rather than presented as fact.
8. No new column on `inventories`. No write path. Read-only derivation.

**Tests:** fresh org renders age; the 2021-snapshot org renders age plus warning state; an org with
zero inventory rows renders "not provided"; a multi-distribution-centre org renders per-DC ages; the
iPad extract carries the timestamp through a full sync cycle.

### Ticket

**None exists. Needs one** — and it should be **two**, because the surfaces ship independently:
*eOL: disclose inventory snapshot age to buyers* and *iPad extract: carry inventory snapshot age*.
The second is a dependency of the PG-01 component and can ship with it.

---

## Sequencing, and what blocks what

1. **Direct-record authorization package** (`BRENT-ENGINEERING-QUEUE-2026-08-04.md` §3) — already
   ahead of A6 in the existing queue and reproduced in production. Not part of this pack; noted so
   A6 is not started out of order.
2. **A6 / SERV-2449** — ship after package 1, per the existing exit gate.
3. **A4, A3, A2** — mutually independent. Any order, or in parallel. None touches the Portal
   territory or amount contracts, so none collides with A6 or with SERV-2196.

**A2's iPad half is the one cross-dependency:** it is also step one of the PG-01 component in
`02-IPAD-ACCOUNT-BRIEF-SPEC.md`.

Canonical field-analytics order after this pack: territory fail-closed → iPad-EC shell → PG-01 and
PG-03 job packs (`product/surface-mapping.md` §2). Do not implement a single seat-based analytics
surface for all motions.

## Open items a developer will hit, recorded rather than guessed

- **`rep_activities` volume: UNKNOWN.** Read-only role lacks the grant. If A4's scope is ever
  revisited, someone with access needs to answer whether the pilot orgs are actually logging.
- **`data-gaps.md` B3 is overstated.** It says ERP ship status / carrier / tracking is *"not in
  SuperCat at all."* `[SQL 2026-08-27]`: `portal_invoices` carries `tracking_number` on **1,121,123
  of 4,940,477** invoices across **26 organizations**, plus `tracking_carrier` (744,046) and
  `ship_via` (2,712,248), and a dedicated `portal_invoice_tracking_records` table exists. This does
  **not** unblock JOB-01-2's ERP ship-status half — tracking is post-invoice, and that job asks
  about open items / next receipt — but the flat claim is wrong and is corrected in `03-ROADMAP.md`.
  B3's *conclusion* stands: do not build a ship-date promise on data we do not hold.
- **Territory master coverage is worse than F11 records**, and it caps the iPad work rather than this
  pack. See `02-IPAD-ACCOUNT-BRIEF-SPEC.md` §2.
