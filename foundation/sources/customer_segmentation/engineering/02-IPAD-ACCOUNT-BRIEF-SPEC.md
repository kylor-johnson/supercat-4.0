---
id: ENG-02
title: Account Brief — PG-01 (Luxury Spec) iPad-EC job pack
version: 1.1
status: ready for engineering
date: 2026-09-15
owner: Kylor Johnson
engineering_reader: Brent Sanders
jtbd: JOB-01-1
persona_group: PG-01 Project specifier
surface: iPad-EC (web component embedded in the offline eCat iPad app)
depends_on: [PROD-MAP §3, PERSONA-GROUPS, PROD-GAPS §B1 §B2]
supersedes: v1.0 (2026-08-27) which specified this as a universal PER-01 / JTBD-011 component
---

# Account Brief — PG-01 only

**This is the Luxury Spec field pack.** Do not ship it as the home screen for PG-03 (dealer line),
PG-05 (channel-mix, marketplace excluded), or PG-07 (skip an L panel). Same iPad-EC **shell**
(WebView, extract pipeline, staleness UI, fail-closed sync). Different grain.

Canonical groups: [`../personas/00-PERSONA-GROUPS.md`](../personas/00-PERSONA-GROUPS.md).
Offline rules: [`../product/surface-mapping.md`](../product/surface-mapping.md) §3.

**The job.** JOB-01-1:

> When I'm about to walk into an account, I want to know what they have **specified**, by collection,
> over **24 months**, so I can lead with the right conversation instead of asking them.

**The decision it changes.** What the rep opens the meeting with, and which collection / finish they
show first.

**Primary metric.** Specified / invoiced net for this account, last 24 months, **by collection** —
not a 90-day retail decline flag, not T12M vs prior T12M "stopped buying."

**Today this is done from memory or a spreadsheet the rep maintains themselves.**

Also on this panel, not as the hero: JOB-01-2 (open items + next receipt for SKUs on the table).
JOB-01-3 (territory trust) is extract-level, not a widget.

---

## 1. What this is, and the one thing not to re-derive

A **read-only web component embedded in the existing offline iPad app**, opened from the customer
record. It reads only from a locally cached extract.

**The embedding pattern already exists — do not re-derive it.** `PM/ecat-web-rewrite-estimate/01_CODE_CENSUS.md`
line 476: **WebView bridge — 36 call sites, classed `NATIVE_EQUIVALENT`.** Embedding a web component
in this app is an established pattern, not a new architecture.

**Read-only is a deliberate scope boundary** (`surface-mapping.md` §3). The rep cannot edit an
account summary, so there are no write conflicts by design. If a later job needs the rep to write
through this component — dismissing a decline flag, say — conflict handling stops being trivial and
must be re-specified. Keep it read-only.

---

## 2. Read this before estimating: who this actually reaches

The fail-closed territory rule (§7 below) is non-negotiable, and it caps the launch population hard.

`[SQL 2026-08-27]`, active iPad reps = `org_users` with blank `customer_number` and
`last_ipad_login_at` within 90 days:

| Population | Count |
|---|---:|
| Active iPad reps, all orgs | **4,058** across 145 orgs |
| …of which have **no** territory codes at all | **935** |
| Orgs with active iPad reps **and** a populated `territories` master | **23 of 145** |
| **Reps who can be territory-scoped today** (org has a territory master **and** rep has codes) | **667**, in **20 orgs** |
| …of those, also in an org with an invoice feed | **618**, in **19 orgs** |

**So this component launches to roughly 667 reps — 16% of the active rep base — and 618 of them get
invoiced net rather than the labelled order-based fallback.**

That is the *scopable* ceiling across motions. PG-01 is the subset of those 667 whose org is stamped
**Luxury Spec** on the v4.0 roster. Look the org up; do not infer segment from AOV.

This is greenfield (`surface-mapping.md`: Territory Dashboard enabled for zero orgs). A build
assumed to reach 4,058 reps that reaches 667 is the kind of surprise that kills a roadmap, so it is
stated here first.

**Note a discrepancy, resolved in favour of the query.** `data-gaps.md` B2 [F11] records the territory
master as *"empty in 32 of 55 orgs."* Measured against orgs with active iPad reps it is **122 of 145
empty**. The denominators differ (F11's 55 is a narrower roster); the figure above is the one that
governs this build.

**The implication for the roadmap is larger than this component.** Fixing territory-master coverage
unblocks more rep value than the component itself does — see `03-ROADMAP.md`.

---

## 3. The screen

One scrollable panel, opened from the customer record the rep already has selected. No navigation
chrome of its own — the rep is already inside a customer context.

```
┌──────────────────────────────────────────────────────────────┐
│  BRIGHTWATER HOME                             ⌄ collapse     │
│  As of Tue 9:14am — 2 days old                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   SPECIFIED / INVOICED          LAST 24 MONTHS               │
│                              $319,675                        │
│                                                              │
│   Open items           $22,410   (7 orders)          →       │
│   Next receipt         14 Jun 2026  — COM pending            │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  BY COLLECTION           24 months                           │
│                                                              │
│   Case goods           $142,800                      →       │
│   Upholstery            $89,400                      →       │
│   Lighting              $41,150                      →       │
│   All other             $46,325                      →       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### What the rep can tap

Four things, and nothing else. Every one stays inside the local extract — no tap may trigger a
network call.

| Tap target | Result |
|---|---|
| **Open items** row | Expands in place: order number, PO, order date, value, status, ship date where present, next receipt. Read-only. |
| **A collection row** | Expands in place to that collection's items for this account: item number, description, 24-month units and value. |
| **An item inside an expanded collection** | Hands off to the **existing native catalog screen** for that item via the WebView bridge. This is the one exit — "which collection / finish do I show first." |
| **Collapse** chevron | Collapses the panel back to the header line, so the rep can get to the order pad fast. |

### What it deliberately does not have

- **No search, no filters, no date picker.** The period is fixed at 24 months. A rep walking into an
  appointment is not running a report. `00-SALES-PORTAL-SYSTEM-SPEC.md` §3 — *"not a generic BI
  builder"* — applies with more force on a 10-inch screen.
- **No charts.** Lazy-loaded remote assets are barred, and a sparkline over two periods is not this
  job.
- **No rep-vs-rep anything.** Named rep→revenue is barred below `REP_IDENTITY_TIER` 2.
- **No margin, no commission.** Schema-absent, both barred outright — `data-gaps.md` §C.
- **No "stopped buying" / T90D / T12M-vs-prior decline hero.** Project buying is lumpy — a quiet
  quarter is often the cycle, not churn. That pattern belongs to JOB-HQ-2 with a **motion-aware
  window**, not on this panel. Do not smuggle it in.

### What the other packs are (not this file)

| Group | Home screen | This spec? |
|---|---|---|
| **PG-01** | 24-month specified / invoiced **by collection** | **Yes** |
| **PG-03** | Dealer line vs holes (T12M by collection + SKUs peers carry that they don't) | No — follow-on pack, same shell |
| **PG-05** | Dealer slice only; exclude marketplace/EDI from "my book" | No |
| **PG-07** | Catalog as reference; skip an L panel by default | No |

---

## 4. The cached extract

**Never ship raw tables to the device.** `surface-mapping.md` §3 — SEG-04 orgs run a median 5,759
orders, SEG-01 orgs a median 4,418 customers. This is a **pre-aggregated per-rep extract**, computed
server-side, replaced wholesale on sync.

**PG-01 extract ≠ PG-03 extract.** Same pipeline, different grain. Segment comes from the stamped
roster, not from a threshold on AOV.

### Schema (PG-01)

One file per rep per sync. Four objects.

```
extract_meta
  rep_user_id            int      org_users.id
  organization_id        int
  generated_at           timestamp   server time the extract was built
  persona_group          string      PG-01 for this pack
  invoice_feed_present   bool        drives the ECAT_ONLY label — see §6
  channel_posture        string      ALL_CHANNEL | ECAT_ONLY
  inventory_snapshot_at  timestamp   max(inventories.updated_at) for the org — see pack item A2
  territory_codes        string[]    the codes baked in at sync — see §7
  account_count          int

account_summary                          one row per customer in the rep's territory
  customer_bill_to_number  string        portal_invoices.customer_bill_to_number / customers.code
  customer_name            string
  invoiced_net_24m         numeric       sum portal_invoices.net_amount, invoice_date in last 24 months
  ordered_value_24m        numeric       sum portal_orders.total_amount — the ECAT_ONLY fallback
  open_order_value         numeric       portal_orders where NOT complete, excluded statuses removed
  open_order_count         int
  last_order_date          date          max portal_orders.order_date
  last_invoice_date        date          max portal_invoices.invoice_date
  next_receipt_date        date          may be null — never infer one

collection_mix                           customer × collection, 24 months
  customer_bill_to_number  string
  collection_code          string
  collection_name          string
  value_24m                numeric
  units_24m                int

open_orders                              one row per open order
  customer_bill_to_number  string
  order_number             string        portal_orders.order_number
  customer_po_number       string
  order_date               date
  ship_date                date          may be null — never infer one
  status                   string        portal_orders.status
  total_amount             numeric
```

Sources are all existing tables — `portal_invoices`, `portal_orders`, `portal_order_items`,
`portal_invoice_items`, `products`, `customers`, `inventories`, `org_users`, `territories`. **No new
column anywhere.** The 24-month aggregation is server-side; the device stores only the result.

### Size

Extending `surface-mapping.md` §3's budget with measured account counts. `[SQL 2026-08-27]`, the 20
scopable orgs hold **141,521 customers** between them; the largest single org holds **20,307**.

| Object | Grain | Per-row | Typical rep | Tail rep |
|---|---|---|---|---|
| `extract_meta` | one row | — | negligible | negligible |
| `account_summary` | per account | ~200 B | 300 accts ≈ **0.06 MB** | 5,000 accts ≈ **1 MB** |
| `collection_mix` | account × collection | ~50 B | 300 × 20 ≈ **0.3 MB** | 5,000 × 20 ≈ **5 MB** |
| `open_orders` | per open order | ~150 B | ≈ **0.02 MB** | 1,000 ≈ **0.15 MB** |
| **Total** | | | **< 1 MB** | **≈ 6 MB** |

**Budget 15 MB** for the fat tail, per §3. Small against the existing catalog cache.

**`collection_mix` is the dominant term — cap it.** Emit at most the top 20 collections per account
by 24-month value, plus an "all other" rollup row. An account specified across 200 collections is
not a screen a rep reads.

**Parameterise extract *size* on the org's own account count / territory size. Parameterise extract
*grain* on the stamped segment.** Those are different knobs. Size is not "build once not on
segment."

---

## 5. Staleness

Inherited from `surface-mapping.md` §3.

| Data | Acceptable age | Why |
|---|---|---|
| Account summary / invoiced totals | **24 hours** | Warehouse ETL already runs on a delay. Intra-day precision is not a decision input for a pre-appointment brief |
| Open order status | **4 hours** | Changes during a business day, and is quoted to a customer |
| Collection mix | **7 days** | A trend signal; daily recomputation is false precision |
| Territory / permission scope | **must match server at last sync** | Never stale-serve an access decision — see §7 |

**Display rule: always show the data with its age. Never hide it, never silently serve it as
current.**

- A persistent, non-modal age line in the panel header: *"As of Tue 9:14am — 2 days old."* Absolute
  time **and** relative age, never relative alone.
- **Past the window:** the same numbers, plus a visible warning state, still fully usable. A rep in a
  dealer's office with 6-day-old numbers is far better off than a rep with a spinner.
- **Never an empty state where cached data exists.**
- **Open orders past 4 hours** are labelled as needing confirmation rather than presented as fact —
  this is the one number on the screen a rep will read aloud to a customer.

---

## 6. The invoice-feed label — mandatory, not cosmetic

`data-gaps.md` §B1 puts invoiced-net jobs in **Group 1: degrades to a usable order-based view,
shippable with a label.** Both paths ship; the label is what makes the fallback honest.

- **`invoice_feed_present = true` → `ALL_CHANNEL`.** Lead with invoiced / specified net. This is 618
  of the 667 scopable reps (across motions).
- **`invoice_feed_present = false` → `ECAT_ONLY`.** Show `ordered_value_24m` instead, label the panel
  explicitly, and present the figure as **absolute eCat dollars only — never as the account's
  business.**

The label text is inherited verbatim and must not be softened: eCat is *"directionally unreliable as
a size proxy — it ran **0.22–3.10×** the invoiced truth across the brand_to_customer cohort (usually
understating 2–4.5×)."*

**Acceptance:** an `ECAT_ONLY` org must never render the string "invoiced" anywhere in the component,
and must never render a figure positioned as the account's total business.

Invoice feed exists for **38 of 109** roster orgs. That is a commercial motion, not a sprint.

---

## 7. Permission scope, and the limitation baked in at sync

This is the section to get right. It is the documented root trust failure — EBR-40 — and
`surface-mapping.md` §3 calls the rule non-negotiable.

1. **The component inherits the authenticated iPad session and must not present its own login.**
2. **Permission scope is baked into the extract at sync time.** The extract contains **only** the
   accounts the rep is entitled to see. There is **no client-side filtering of a wider dataset**, so a
   compromised device cannot reveal a wider book.
3. **The consequence, stated plainly because the product must not claim otherwise:** *a permission
   change does not take effect until the next sync.* That is acceptable for **widening** and **not
   acceptable for revocation.**
   - Revocation must be enforced **server-side at next sync**.
   - **The product must not claim real-time revocation it cannot deliver.** No UI copy, no sales
     material, and no support answer may say scope changes take effect immediately.
   - Where an org needs faster revocation than its sync cadence, the answer is disabling the rep's
     account server-side — which blocks sync — not a claim the component cannot honour.
4. **Fail closed, always.** No valid extract, or an empty territory set → **show nothing. Never
   whole-org.** Same rule as JOB-01-3. `data-gaps.md` B2: *"the fastest way to lose a rep
   permanently."*
5. `access_all_customer_sales_totals` users get a whole-org extract legitimately — but **size it
   before enabling**: at the 20,307-customer org that is well past the 15 MB budget. Gate
   company-wide extracts behind an explicit account-count ceiling and fall back to server-side
   viewing rather than shipping an oversized extract.

**Acceptance for §7** — mirror the spec's own verification matrix (§14):

| Case | Required result |
|---|---|
| Rep with one assigned territory | Extract contains exactly that territory's accounts |
| Rep with several territories, none selected | Union of permitted territories |
| Rep with NULL territory assignment | **Empty extract, component shows nothing** |
| Rep with empty territory array | **Empty extract, component shows nothing** |
| Org with empty `territories` master | **Empty extract** — never whole-org |
| Territory revoked server-side, before next sync | Old scope still visible; **this is the documented limitation** — test that it is not claimed otherwise |
| Territory revoked server-side, after next sync | Revoked accounts absent from the extract |
| Territory widened, after next sync | New accounts present |
| Mixed-case territory code | Case-insensitive match (spec §8 records downcasing/raw-casing divergence as a known risk) |
| Blank / collapsed ship-to key | **No accidental bridge match** — spec §8 and SERV-2196 |

**Dependency worth flagging:** the blank-ship-to-key collapse repaired by **SERV-2196** affects which
accounts land in the extract. Building the extract before SERV-2196 ships means building it against
a book that is knowingly over-granted in at least one org (`shl` actively over-grants 24 customers —
`BRENT-ENGINEERING-QUEUE-2026-08-04.md` §5). **Sequence this component after SERV-2196**, or accept
that the extract inherits that over-grant.

---

## 8. Zero connectivity

**This is the normal case, not the exception** — `surface-mapping.md` §3.

- The component reads **only** from the local extract. **No component may block on a network call.**
- **No lazy-loaded remote assets.** Charts, fonts and icons ship with the component. (There are no
  charts — see §3 — which makes this easy to honour.)
- **Market week is the worst connectivity and the highest usage simultaneously. Treat it as the
  design case.**
- **Degradation order when the extract is missing entirely:** show the customer record and catalog —
  existing behaviour, untouched — and state that the analytics extract has not synced. **Never a
  blank screen.**

**The overriding constraint:** the existing iPad — catalog, customer, price, stock, write the order,
offline — is SuperCat's strongest asset (`PLATFORM_ANATOMY §1.3`: *"fully offline-capable"*). An
analytics panel that spins on a market floor breaks the one thing that already works. **If this
component can degrade existing iPad selling, it is wrong.** That is the acceptance bar.

**Test:** device in airplane mode, cold app start, open a customer, open the panel, expand a
collection, tap through to an item — all of it working, with no network, and no measurable delay
added to the existing customer screen's time-to-usable.

---

## 9. Sync

`surface-mapping.md` §3, inherited:

- **Full replace of the extract, not a merge.** Simpler and idempotent.
- **Piggyback the existing catalog/customer sync.** Do not add a second sync channel.
- **Partial failure leaves the previous complete extract in place** — never a half-updated one. A
  stale-but-consistent view beats a fresh-but-partial one.
- **No write conflicts by design** — the component is read-only (§1).
- The extract is generated server-side per rep. Generation cost scales with the rep's account count,
  not the org's; cache and reuse across reps sharing a territory where practical.

**Acceptance:** interrupt a sync mid-transfer → previous extract intact and rendering, with its
original `generated_at`. Complete a sync → `generated_at` advances and the age line updates. Sync with
a revoked territory → §7 revocation case passes.

---

## 10. Build order

1. **Extract generator, server-side**, with the §7 scoping rules and the §7 acceptance matrix. This
   is the reusable half — if the surface decision is ever revisited, this survives. PG-03 will reuse
   it with a different grain.
2. **Sync piggyback + local storage + full-replace semantics** (§9).
3. **Inventory snapshot timestamp into `extract_meta`** — shared with pack item A2.
4. **The panel itself** (§3), read-only, offline-only, with the §5 staleness rules and the §6 label.
5. **WebView bridge hand-off to the native catalog screen** for the item tap — the one exit, using
   the existing 36-call-site pattern.

**Blocked on / sequenced after:** SERV-2196 (§7). **Not blocked on:** the invoice feed — the
`ECAT_ONLY` path ships to non-feed orgs by design (§6).

## Open, and recorded rather than guessed

- **No usage evidence exists for any of this.** There is no incumbent rep analytics surface,
  therefore no telemetry, no complaints, and no "reps do X today" baseline. **Every design
  assumption in §3 is untested.** The cheapest correction is showing this screen to spec-motion reps
  and watching which rows they tap.
- **Time-to-first-usable-screen budget: UNKNOWN.** No current baseline was found in the checked-in
  files. Measure it before the component ships so a regression is detectable.
- **JOB-01-2's ERP ship-status half stays blocked.** Next receipt on inventory is ours; "where is
  the truck" is not. Do not promise a ship date we do not hold.
