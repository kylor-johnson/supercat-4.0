---
id: ENG-02
title: Account Brief — the first rep-facing iPad component (JTBD-011)
version: 1.0
status: ready for engineering
date: 2026-08-27
owner: Kylor Johnson
engineering_reader: Brent Sanders
jtbd: JTBD-011
persona: PER-01 independent sales rep
surface: iPad-EC (web component embedded in the offline eCat iPad app)
depends_on: [PROD-MAP §5, PER-01, PROD-GAPS §B1 §B2]
---

# Account Brief

**The job.** JTBD-011, rank 1 of PER-01's five, and the highest-ranked of the five iPad-embedded jobs
(011, 012, 014, 015 rep-side; 085 buyer-side — `product/surface-mapping.md` §5):

> *When I'm about to walk into an account, I want to know what they've bought, what's open, and what
> they've stopped buying, so I can lead with the right conversation instead of asking them.*

**The decision it changes.** What the rep opens the meeting with, and which three products they show
first.

**Primary metric.** Invoiced net for this account, trailing 12 months, versus the prior 12.

**Today this is done from memory or a spreadsheet the rep maintains themselves** — `PER-01`.

---

## 1. What this is, and the one thing not to re-derive

A **read-only web component embedded in the existing offline iPad app**, opened from the customer
record. It reads only from a locally cached extract.

**The embedding pattern already exists — do not re-derive it.** `PM/ecat-web-rewrite-estimate/01_CODE_CENSUS.md`
line 476: **WebView bridge — 36 call sites, classed `NATIVE_EQUIVALENT`.** Embedding a web component
in this app is an established pattern, not a new architecture.

**Read-only is a deliberate scope boundary** (`surface-mapping.md` §5.5). The rep cannot edit an
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

That is not an argument against building it. It is greenfield (`surface-mapping.md` §3: Territory
Dashboard is enabled for zero orgs, so nothing is displaced), the extract and aggregation logic are
reusable if the surface choice turns out wrong, and §6 establishes the iPad path is the smaller loss.
But **a build assumed to reach 4,058 reps that reaches 667 is the kind of surprise that kills a
roadmap**, so it is stated here first.

**Note a discrepancy, resolved in favour of the query.** `data-gaps.md` B2 [F11] records the territory
master as *"empty in 32 of 55 orgs."* Measured against orgs with active iPad reps it is **122 of 145
empty**. The denominators differ (F11's 55 is a narrower roster); the figure above is the one that
governs this build, because it is measured against exactly the population this component serves.

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
│   INVOICED NET          T12M          PRIOR T12M             │
│   ▏                  $148,220          $171,455              │
│   ▏                                      ▼ 13.5%             │
│                                                              │
│   Open orders          $22,410   (7 orders)          →       │
│   Last order           14 Jun 2026  — 74 days ago            │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  STOPPED BUYING            bought last year, not this        │
│                                                              │
│   Upholstery              $31,200 last year          →       │
│   Occasional tables       $12,880 last year          →       │
│   Lighting                 $4,150 last year          →       │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  STILL BUYING                                                │
│                                                              │
│   Case goods       $71,400   ▲ 8%                    →       │
│   Bedroom          $52,600   ▼ 22%                   →       │
│   Accents          $24,220   ▲ 3%                    →       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### What the rep can tap

Four things, and nothing else. Every one stays inside the local extract — no tap may trigger a
network call.

| Tap target | Result |
|---|---|
| **Open orders** row | Expands in place to a list of open orders: order number, PO, order date, value, status, ship date where present. Read-only. |
| **A category row** (either section) | Expands in place to that category's items for this account: item number, description, T12M units and value, prior T12M. |
| **An item inside an expanded category** | Hands off to the **existing native catalog screen** for that item via the WebView bridge. This is the one exit from the component, and it is the point of the whole thing — "which three products do I show first." |
| **Collapse** chevron | Collapses the panel back to the header line, so the rep can get to the order pad fast. |

### What it deliberately does not have

- **No search, no filters, no date picker.** The periods are fixed at T12M and prior T12M. A rep
  walking into an appointment is not running a report. `00-SALES-PORTAL-SYSTEM-SPEC.md` §3 —
  *"not a generic BI builder"* — applies with more force on a 10-inch screen.
- **No charts.** §5.4 bars lazy-loaded remote assets, and a sparkline over two periods carries no
  information a delta percentage doesn't.
- **No rep-vs-rep anything.** `PER-01` cut the leaderboard: `RS-01` bars named rep→revenue below
  `REP_IDENTITY_TIER` 2.
- **No margin, no commission.** Schema-absent, both barred outright — `data-gaps.md` §C.
- **No decline flag yet.** "Stopped buying" here is a factual category-level statement over two
  windows, not a computed decline verdict. The scored version is **JTBD-014** and it needs the
  per-account baseline store (A8, M-sized). Do not smuggle it in — `PER-06` JTBD-062 records that a
  naive decline rule fires constantly on lumpy project buying.

---

## 4. The cached extract

**Never ship raw tables to the device.** `surface-mapping.md` §5.1 — SEG-04 orgs run a median 5,759
orders, SEG-01 orgs a median 4,418 customers. This is a **pre-aggregated per-rep extract**, computed
server-side, replaced wholesale on sync.

### Schema

One file per rep per sync. Four objects.

```
extract_meta
  rep_user_id            int      org_users.id
  organization_id        int
  generated_at           timestamp   server time the extract was built
  invoice_feed_present   bool        drives the ECAT_ONLY label — see §6
  channel_posture        string      ALL_CHANNEL | ECAT_ONLY
  inventory_snapshot_at  timestamp   max(inventories.updated_at) for the org — see pack item A2
  territory_codes        string[]    the codes baked in at sync — see §7
  account_count          int

account_summary                          one row per customer in the rep's territory
  customer_bill_to_number  string        portal_invoices.customer_bill_to_number / customers.code
  customer_name            string
  invoiced_net_t12m        numeric       sum portal_invoices.net_amount, invoice_date in T12M
  invoiced_net_prior_t12m  numeric       same, prior 12 months
  ordered_value_t12m       numeric       sum portal_orders.total_amount — the ECAT_ONLY fallback
  ordered_value_prior_t12m numeric
  open_order_value         numeric       portal_orders where NOT complete, excluded statuses removed
  open_order_count         int
  last_order_date          date          max portal_orders.order_date
  last_invoice_date        date          max portal_invoices.invoice_date

category_mix                             customer × category, two periods
  customer_bill_to_number  string
  category_code            string        products.category_code / category_codes
  category_name            string
  value_t12m               numeric
  value_prior_t12m         numeric
  units_t12m               int

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
column anywhere.** The T12M aggregation is server-side; the device stores only the result.

### Size

Extending `surface-mapping.md` §5.1's budget with measured account counts. `[SQL 2026-08-27]`, the 20
scopable orgs hold **141,521 customers** between them; the largest single org holds **20,307**.

| Object | Grain | Per-row | Typical rep | Tail rep |
|---|---|---|---|---|
| `extract_meta` | one row | — | negligible | negligible |
| `account_summary` | per account | ~200 B | 300 accts ≈ **0.06 MB** | 5,000 accts ≈ **1 MB** |
| `category_mix` | account × category | ~50 B | 300 × 20 ≈ **0.3 MB** | 5,000 × 20 ≈ **5 MB** |
| `open_orders` | per open order | ~150 B | ≈ **0.02 MB** | 1,000 ≈ **0.15 MB** |
| **Total** | | | **< 1 MB** | **≈ 6 MB** |

**Budget 15 MB** for the SEG-04 / SEG-01 tail, per §5.1. Small against the existing catalog cache.

**`category_mix` is the dominant term — cap it.** Emit at most the top 20 categories per account by
combined T12M + prior T12M value, plus an "all other" rollup row. An account buying across 200
categories is not a screen a rep reads.

**Parameterise on the org's own structure — territory size and account count — not on segment.**
`surface-mapping.md` §5.1 and the standing build-once rule.

---

## 5. Staleness

`surface-mapping.md` §5.2 sets the windows; §5.3 sets the display rule. Both are inherited verbatim.

| Data | Acceptable age | Why |
|---|---|---|
| Account summary / invoiced totals | **24 hours** | Warehouse ETL already runs on a delay (spec §5.3). Intra-day precision is not a decision input for a pre-appointment brief |
| Open order status | **4 hours** | Changes during a business day, and is quoted to a customer |
| Category mix | **7 days** | A trend signal; daily recomputation is false precision |
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

`data-gaps.md` §B1 puts JTBD-011 in **Group 1: degrades to a usable order-based view, shippable with
a label.** Both paths ship; the label is what makes the fallback honest.

- **`invoice_feed_present = true` → `ALL_CHANNEL`.** Lead with invoiced net. This is 618 of the 667
  launch reps.
- **`invoice_feed_present = false` → `ECAT_ONLY`.** Show `ordered_value_*` instead, label the panel
  explicitly, and present the figure as **absolute eCat dollars only — never as the account's
  business.**

The label text is inherited verbatim and must not be softened: eCat is *"directionally unreliable as
a size proxy — it ran **0.22–3.10×** the invoiced truth across the brand_to_customer cohort (usually
understating 2–4.5×)."*

**Acceptance:** an `ECAT_ONLY` org must never render the string "invoiced" anywhere in the component,
and must never render a figure positioned as the account's total business.

---

## 7. Permission scope, and the limitation baked in at sync

This is the section to get right. It is the documented root trust failure — EBR-40 — and
`surface-mapping.md` §5.6 calls the rule non-negotiable.

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
   whole-org.** Same rule as JTBD-012. `data-gaps.md` B2: *"the fastest way to lose a rep
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

**This is the normal case, not the exception** — `surface-mapping.md` §5.4.

- The component reads **only** from the local extract. **No component may block on a network call.**
- **No lazy-loaded remote assets.** Charts, fonts and icons ship with the component. (There are no
  charts — see §3 — which makes this easy to honour.)
- **Market week is the worst connectivity and the highest usage simultaneously. Treat it as the
  design case.**
- **Degradation order when the extract is missing entirely:** show the customer record and catalog —
  existing behaviour, untouched — and state that the analytics extract has not synced. **Never a
  blank screen.**

**The overriding constraint:** JTBD-013 — *work the whole appointment with no connectivity* — is
currently **Served, and is SuperCat's strongest asset** (`PER-01`; `PLATFORM_ANATOMY §1.3`: *"fully
offline-capable"*). An analytics panel that spins on a market floor breaks the one thing that already
works. **If this component can degrade JTBD-013, it is wrong.** That is the acceptance bar.

**Test:** device in airplane mode, cold app start, open a customer, open the panel, expand a category,
tap through to an item — all of it working, with no network, and no measurable delay added to the
existing customer screen's time-to-usable.

---

## 9. Sync

`surface-mapping.md` §5.5, inherited:

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
   is the reusable half — if the surface decision is ever revisited, this survives.
2. **Sync piggyback + local storage + full-replace semantics** (§9).
3. **Inventory snapshot timestamp into `extract_meta`** — shared with pack item A2.
4. **The panel itself** (§3), read-only, offline-only, with the §5 staleness rules and the §6 label.
5. **WebView bridge hand-off to the native catalog screen** for the item tap — the one exit, using
   the existing 36-call-site pattern.

**Blocked on / sequenced after:** SERV-2196 (§7). **Not blocked on:** the invoice feed — the
`ECAT_ONLY` path ships to non-feed orgs by design (§6).

## Open, and recorded rather than guessed

- **No usage evidence exists for any of this.** `surface-mapping.md` §3: there is no incumbent rep
  analytics surface, therefore no telemetry, no complaints, and no "reps do X today" baseline. **Every
  design assumption in §3 is untested.** The cheapest correction is showing this screen to reps at
  market and watching which rows they tap.
- **Time-to-first-usable-screen budget: UNKNOWN.** JTBD-013's secondary metric is *"time from sync to
  first usable screen"*, and no current baseline was found in the checked-in files. Measure it before
  the component ships so a regression is detectable.
