---
id: MEAS-03
title: Line B — measured problem size per job
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
---

# Line B — how big is the problem each job claims to solve?

One row per job. Where the problem cannot be measured, that is stated rather than skipped.
Tags: `MEASURED` (a query) · `CODE-AUDIT` · `JUDGMENT` · `UNVERIFIABLE-FROM-DB`.

---

## Summary table

| JTBD | Problem measured | Size | Unit | Orgs | Query | Tag |
|---|---|---:|---|---:|---|---|
| 011 | Reps who would open an account brief (band C) | 353 | rep records | — | Q010 | MEASURED |
| 012 | Active reps who cannot be territory-scoped | **3,371** | rep records (1,808 people) | 143 | Q004, Q038, Q052 | MEASURED |
| 013 | — protect; no problem to size | — | — | — | — | — |
| 014 | Accounts down >30% vs own prior 90d | **23,243** | accounts ($112.9M) | 40 | Q037 | MEASURED |
| 015 | ERP orders whose status is unusable free text | **1,280,046** | order rows / 125 status values | 43 | Q031, Q032 | MEASURED |
| 021–023 | Agency reps with no `company_name` recorded | 465 of 590 | rep records | 42 | Q071 | MEASURED |
| 024 | — needs A9 view-as; nothing to size in DB | — | — | — | — | UNVERIFIABLE |
| 031 | Order value distorted by outliers | **$496.1M in 15 orders** (24.2% of 24m value) | dollars | 3 | Q055, Q056 | MEASURED |
| 032 / 063 | Reps "active" who wrote nothing in 90d | **2,806** | rep records (69.7%) | — | Q010 | MEASURED |
| 033 | Access-rule surface count [F10] | not reproducible | — | — | Q070 | CODE-AUDIT |
| 034 | Import events carrying error text, 30d | **6,092** | events | **71** | Q043 | MEASURED |
| 035 | Export/UI reconciliation defect | not observable in DB | — | — | — | UNVERIFIABLE |
| 041 / 082 | ERP orders with no matching invoice, 12m | **167,884** (13.1%) | orders | **43** | Q030 | MEASURED |
| 042 | — served; price-code complexity sized in 06 | — | — | — | Q040 | MEASURED |
| 043 | same as 015 | — | — | 43 | Q031 | MEASURED |
| 044 | Orders carrying a real export error, 12m | **1,862** (1.0%) | orders | 16 | Q041, Q042 | MEASURED |
| 051 | — needs inventory history (A14); not in DB | — | — | — | — | UNVERIFIABLE |
| 052 | Orgs holding option data / configurator cascade | **92** / **7** | orgs | — | Q039 | MEASURED |
| 053 | Active items genuinely failing a check | **153,084** image, **98,441** price | items | 241 | Q005, Q045, Q046 | MEASURED |
| 054 | Collections created in 12m (unusable as launch date) | 19,197 | collections | 119 | Q035, Q036 | MEASURED |
| 061 | same as 031 | — | — | — | Q055 | MEASURED |
| 062 | same as 014 | 23,243 | accounts | 40 | Q037 | MEASURED |
| 081 | Active buyers who ordered at all in 12m | 6,896 of 18,764 (**36.8%**) | buyers | 31 | Q016, Q017 | MEASURED |
| 083 | Price-code spread across orgs | median 8, tail to **192** | price codes | 109 | Q040 | MEASURED |
| 084 | Inventory rows >30 days stale | **335,571** (48.8%) — but only **205 buyers** see it | rows / buyers | 187 / 20 | Q033, Q034 | MEASURED |
| 085 | — buyer-side offline; not observable in DB | — | — | — | — | UNVERIFIABLE |
| 086 | Active buyers reachable (ceiling) | **17,522** | buyer records | 24 | Q062 | MEASURED |

---

## The ones worth reading in full

### JTBD-041 / 082 — reconstruct an account's history · orders with no invoice
`MEASURED` · Q030, Q031

**167,884 of 1,279,729 ERP orders in the trailing 12 months (13.1%) have no matching invoice row**,
and **all 43** orgs with both feeds are affected. Restricting to orders older than 90 days (so
genuinely open orders are excluded), the orphan rate on nominally-closed statuses is 19.6% for
status `C` (49,337 orders) and 9.7% for `Closed`.

A CS agent reconstructing an account, or a buyer checking what they were billed, will hit a hole in
roughly one order in eight. **This is the Portal's strongest existing fit, quantified — and the gap
inside it is not coverage across orgs, it is completeness within them.**

### JTBD-015 / 043 — "where is my order" · the status field is not missing, it is unusable
`MEASURED` · Q031, Q032 · **This reframes two blocked jobs.**

Both jobs sit in bucket C, blocked, because open-order status "lives in the client's ERP." It does
not: it is in `portal_orders.status` for 43 orgs across 1,280,046 rows.

The problem is that it carries **125 distinct values**:

- *closed* → `C` (251,691) · `Closed` (154,750) · `CLOSED` (43,603)
- *cancelled* → `Cancelled` · `Canceled` · `CANCELLED` · `Cancelled Order` · `X` · `X-Canceled`
- *open* → `Open` · `OPEN` · `Open Order` · `Open order` · `O` · `OPEN ORDER - OD` · `OPEN ORDER - 99`
- 12 single/double-character codes cover **574,621 rows (44.9%)**
- **18 values are literal dates** (`09/01/2026`, `08/31/2026`) — a field-mapping defect, 94 rows

`JUDGMENT`: this does not make 015/043 shippable. It changes the blocker from *"we do not hold the
data"* to *"we hold it in 125 spellings and have not written the map."* Those have very different
costs, and the second is per-org configuration work of the kind onboarding already does. **Both jobs
deserve re-testing before they stay in the blocked bucket.**

`UNVERIFIABLE-FROM-DB`: whether those statuses are *refreshed* on a useful cadence per org. A
normalised status is worthless if the feed updates weekly. See `08-UNVERIFIABLE.md`.

### JTBD-053 — find where the catalog is broken · the spec needs changing
`MEASURED` · Q005, Q045, Q046 · **This is the cheapest build on the roadmap and its spec is wrong.**

Gross figures reproduce the roadmap exactly: 938,893 active items, 179,623 with no image. Broken
apart by check and by org:

| Check | Gross | Genuine | Why the difference |
|---|---:|---:|---|
| No image | 179,623 | **153,084** | 26,539 sit in orgs where *no* item has an image — catalogs that do not use images |
| No `net_price` | 189,471 | **98,441** | **25 orgs never populate the field at all** (91,030 items) — they price through price levels. Configuration, not defect |
| No `prices_json` | 210,652 | — | 54 orgs never use it. Same problem |
| No category | **8** | 8 | Essentially complete |
| No collection | **196** | 196 | Essentially complete |

Two further contaminants: **test and staging orgs** are in the headline (`ctest` 9,267,
`tam-staging` 7,870, `ahtest` 5,630 — ~24,700 items).

**Three consequences for the spec:**
1. **Drop the category and collection checks.** 8 and 196 items system-wide is not a job.
2. **Make the price check org-relative** — "does this item have a price by the mechanism this org
   uses" — or the view reports ~91,000 false positives and tells five clients their entire catalog
   is broken.
3. **Exclude non-production orgs.**

Corrected problem size: **153,084 image gaps and 98,441 price gaps**, ~118,000 items smaller than
the naive figure.

### JTBD-014 / 062 — the account gone quiet · a naive rule is unusable, demonstrated
`MEASURED` · Q037

Across the 40 orgs with usable invoice coverage, trailing 90 days vs the prior 90:

| | Accounts | Share |
|---|---:|---:|
| Active in either period | 52,818 | 100% |
| **Went silent entirely** | 15,156 | 28.7% |
| **Down >30%, still buying** | 7,862 | 14.9% |
| **Total firing a naive rule** | **23,243** | **44.0%** |
| Newly buying this period | 14,133 | 26.8% |

Dollars of decline: **$112.9M** against a $302.7M prior-period base.

A fixed 30% threshold flags **nearly half the customer base**. That is not a call list. The register
*asserts* that A8 (a per-account baseline store) is needed because SEG-01 project buyers order
lumpily; this **demonstrates** it across all segments and gives the tuning target.

`JUDGMENT`: the comparison (Jun–Aug vs Mar–May) crosses a market cycle, so seasonality inflates the
count. That confound argues the same way — the window must be account-aware, not calendar-fixed.

### JTBD-084 — stock with its age · severe by org, negligible by buyer
`MEASURED` · Q033, Q034

| | Orgs | Buyers behind them |
|---|---:|---:|
| Inventory refreshed ≤2 days | 68 (of 187) | **15,837 of 17,550 — 90.2%** |
| Stale >30 days | 20 (of 48 Cart orgs) | **205** |
| Stale >1 year | **83** (of 187) | **84** |

Mean snapshot age across all 187 orgs is **1,071 days**; the worst is 5,530 days. 335,571 of 687,455
inventory rows (48.8%) are more than 30 days old.

**Read by org count this is a crisis; read by buyer reach it is a rounding error.** The staleness
label remains correct and cheap — it just will not surface much, because the orgs with buyers are
the orgs that refresh. This is the clearest instance of a pattern that runs through the whole
register: **org-count framing systematically overstates user impact, because the large orgs are the
well-configured ones.**

### JTBD-054 — did the introduction land · the obvious shortcut fails
`MEASURED` · Q035, Q036

`products` has **no `created_at` and no `updated_at` — only `id`.** The register's A1 (one nullable
launch date) is genuinely necessary; this confirms it.

`taxonomies` (Collection) *does* carry `created_at`, and 19,197 collections were created in 12
months across 119 orgs — which looks like a free collection-level launch date. It is not:
**149 of 239 orgs (62%) created half or more of their collections on a single day**, and 64 orgs
created 90%+ on one day. That is bulk import, not launch. Only **56 orgs** spread creation across 20+
distinct days, and only for those is the field plausibly meaningful.

**A1 stands. The shortcut is now tested and rejected rather than untried.**

### JTBD-052 — which options get chosen · wider than assumed, and still blocked
`MEASURED` · Q039

| | Orgs |
|---|---:|
| `option_groups` present | **93** (12,541 groups) |
| `options` present | **92** (46,432 values) |
| `matrix_options` present | 53 (4,865,103 rows) |
| **`option_mappings`** (the configurator cascade) | **7** |
| `option_forms` | 10 |
| CPQ subscription entitlement | **21** (Q060) |

The register's "16 CPQ orgs" matches none of these cleanly. Reporting reach is ~4× wider than
assumed (92 orgs hold option data); configurator reach is far narrower (7).

The blocker is confirmed by measurement: sampling 30,000 populated `custom_data` blobs on
`portal_order_items` returns **only the key `item`**. Chosen option values are not captured per
order line anywhere queryable. **A13 is genuinely required.**

### JTBD-044 — catch the order that will fail · the register is wrong, and it does not matter much
`MEASURED` · Q041, Q042

Failure reason data **does** exist: `orders.num_failures` and `orders.export_errors`.

*A trap for anyone re-running this:* a naive count of non-blank `export_errors` returns 19,003 —
but **17,141 of those are the literal string `[]`**, an empty JSON array meaning *no error*. The
real count is **1,862 orders across 16 orgs**, which matches `num_failures > 0` exactly.

Classes: mostly integration transport — `401 Unauthorized` ×1,003, gateway/timeout errors ~150.
Preventable-at-entry content errors ("Customer number is blank" 523, `customer_num is required` 18,
`invalid order_type` 32) total roughly **580 orders**. Separately, **5,007 orders are stuck**
(`to_export` true, `is_exported` not true).

**Correct the register's "does not exist." Do not promote the job on it** — 1.0% of orders, and most
failures are transport rather than order content, which is a different fix from the one 044
describes.

### JTBD-034 — nightly import failures
`MEASURED` · Q043 · 42,575 import events in 30 days across 107 orgs. **6,092 carry error text across
71 orgs** — two-thirds of importing orgs hit an error in a month — plus 10,157 carrying warnings.
Nothing pushes. The register's framing is right and the size is larger than "Size S" implies as a
*problem*, even if the build stays small.

### JTBD-081 — reorder from history
`MEASURED` · Q016, Q017 · Cart is enabled for 55 orgs holding **18,057 of 18,764 active buyers
(96.2%)**. But only **6,896 buyers (36.8%) placed any order in 12 months**, and 241 buyers drove
39.4% of the value. The config-vs-build framing is right; the reach framing in the roadmap
("55 of 258 orgs") badly understates it — by buyers it is already at 96%.

---

## Jobs whose problem cannot be measured here

| JTBD | Why | What would settle it |
|---|---|---|
| **035** export/UI reconciliation | A UI defect. No DB artefact | The EBR-91 / SERV-2449 ticket and a reproduction |
| **051** true sell-through | Needs inventory *history*; `inventories` is overwritten on every import (no history table exists) | A14 — an inventory snapshot table |
| **085** buyer offline ordering | A client-side capability question | Browser/service-worker audit of the eOL app |
| **024** view-as preview | A mechanism that does not exist yet | A9 spec |
| **033** access-rule sprawl | The "134 toggles / 39 flags / 6 layers" count is a code audit. `user_types` has 12 boolean columns and `organizations` 35 — not reconcilable to 134 | Re-run the original F10 audit and record its method |
| **011** the brief's *value* | Reach is measurable (Q010); whether a rep acts on it is not | Field test at market |
