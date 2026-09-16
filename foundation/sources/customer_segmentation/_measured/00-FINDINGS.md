---
id: MEAS-00
title: Findings, ranked by what they change
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
---

# Findings

> **2026-09-15 — this pack measured the Aug 25 *seat* register (PER-01…08, JTBD-0xx), now demoted.**
> Headcounts, invoice-feed shape, disjoint rep/buyer populations still stand. **Do not treat
> “only 4 of 31 jobs vary / build once not on segment” as current doctrine.** Canonical set:
> [`../personas/00-PERSONA-GROUPS.md`](../personas/00-PERSONA-GROUPS.md).

Ranked by what each would change about what we build, not by how interesting it is.
Every figure carries a query id. Every claim carries a tag.

---

## The five that most change what we build

### 1. The invoice-feed gap is rep-shaped, not universal — and it is 10 conversations, not 64

`MEASURED` · **Q020, Q022** · *high confidence*

The register calls the invoice feed "the single largest constraint," degrading 13 of 31 jobs. That
is true by **org count** and misleading by **user reach**.

| Behind the 64 active orgs with **no feed** | Behind the 48 **with** a feed |
|---|---|
| **1,893 active reps — 49.3% of the rep base** | 1,947 active reps |
| **1,164 active buyers — 6.2%** | 17,599 active buyers — 93.8% |
| $126.9M order value — 15.9% | $672.5M — 84.1% |
| 33,578 orders — 18.8% | 145,358 orders |
| 211,841 customer records | 456,237 customer records |

**The feed gap costs us half the rep base and almost none of the buyer base.** Buyer-heavy orgs are
already fed. So the feed push is a *rep-value* motion, and it is the smaller half of the business by
dollars — not the universal constraint the register describes.

And it is far more tractable than "71 accounts": **the top 6 no-feed orgs hold 64.1% of the missing
order value and the top 10 hold 74.6%** (Q022). Ten conversations recover three-quarters of the gap.
Target list in `05-GAPS-SIZED.md` and `data/Q021.csv`.

**What it changes:** re-frames Decision 05 from a 71-account campaign to a named 10-account push,
and re-scopes its benefit as rep enablement rather than buyer value.

---

### 2. "Independent sales rep" is not one persona. It is three, and 70% of the active base writes nothing

`MEASURED` · **Q010, Q012** · *high confidence — confirmed on two independent axes*

Of 4,026 reps counted "active" (logged in within 90 days):

| Band | Reps | Share | Orders in 90d | Value | Avg days active /90 |
|---|---:|---:|---:|---:|---:|
| **A — wrote nothing** | 2,806 | 69.7% | 0 | $0 | 12.4 |
| **B — 1–19 orders** | 867 | 21.5% | 4,447 | $23.5M | 26.5 |
| **C — 20+ orders** | **353** | **8.8%** | **28,087 (86.3%)** | **$143.4M (85.9%)** | **54.2** |

This is not an artefact of order attribution. The same three bands separate cleanly on an
independent measure — days with a login event (Q012). Producers are on the device 54 of 90 days and
**not one of them** is below 6 days. Meanwhile 1,324 zero-order reps are on 1–5 days.

But band A is not dormant either: **368 zero-order reps used the iPad on 30+ separate days.** They
are heavy users of a catalog and price-lookup tool who never submit an order through it. That is a
real, sizeable persona the register does not have: a **reference/presentation user**, not an
order-writer.

**What it changes:** the rep component (JTBD-011/014) is currently specified for "the rep." Band C
is 353 people and would use an account brief daily. Band A is 2,806 people for whom an
invoiced-dollars panel answers a question they are not asking. These need different designs, and
`02-PERSONA-EVIDENCE.md` sets out which jobs land on which band.

---

### 3. Every rep number in the register is inflated ~1.9× — 4,026 records are 2,141 people

`MEASURED` · **Q051, Q052** · *high confidence*

`org_users` rows are per-org memberships, not people. Counting people via `org_users.user_id`:

- **4,026 active rep records = 2,141 distinct people** (1.88 memberships each)
- **18,764 active buyer records = 12,972 people** (1.45 each) — Q053
- The buyer:internal ratio is **6.1:1 in people**, not the 7.5:1 the readout reports on records
- The rep-component launch population is **559 people**, not 664 or 655 records

The interesting part is not the deflation. It is what causes it: **the typical SuperCat rep carries
about two manufacturers on the same iPad.** And 226 people are territory-scopeable at one
manufacturer and not at another — the same human sees their book at org A and, under the mandatory
fail-closed rule, a blank screen at org B.

**What it changes:** Decision 01 ("build at 664 reps, or sequence behind the territory push?") is
really "build for 559 people." More importantly the multi-line rep — which the register only meets
as PER-02, the agency principal it declines — is the *modal* rep, measured.

---

### 4. Plan-level entitlement IS in Postgres. 37 orgs pay for the Sales Portal; 25 orgs run Cart without paying

`MEASURED` · **Q060, Q061** · *high confidence*

The register and readout both state that feature gates live in application YAML and cannot be read
from the database. That is true of **fine-grained** gates. It is **false of commercial entitlement**,
which is fully queryable in `subscription_plans` + `subscriptions` — a table pair the register never
consults.

- **`eCat Online - Portal`** — *"Sales Portal service with enhanced sales reporting"*, $395/mo —
  **37 orgs** (35 status `active`). 36 of the 37 also have an invoice feed.
- **`eCat Online - B2B Cart`** — $295/mo — **32 orgs**. But `mobile_sites.enable_online_ordering`
  is on for **55 orgs**. → **25 orgs run Cart with no Cart subscription**, roughly **$88,500/yr** of
  un-billed entitlement.
- CPQ entitlement (plans 3 + 9 + 12) = **21 orgs**, against the register's "16 CPQ orgs."
- T1/T2/T3 tier plans exist but carry only **5 orgs** between them — the new pricing has barely landed.

This also gives JTBD-086 a real denominator for the first time (Q062): the ceiling is **17,522
active buyer records** at orgs that are both on the Portal plan and have an invoice feed — not the
whole 18,764.

**What it changes:** `08-UNVERIFIABLE.md` shrinks. Decision 03's reach question gets a measured
ceiling and a defensible range. And there is a revenue item on the table that no one was looking for.

---

### 5. Segment explains ≤10.9% of the variance in every structural driver — the architecture call is *more* right than the register claims, and two of its four supporting attributions are wrong

`MEASURED` · **Q040** · *high confidence* · **This was the load-bearing claim. It holds.**

Recomputing the structural distributions live for all 109 roster orgs and asking how much variance
the stamped v4 segment explains (η², log scale):

| Structural driver | Variance explained by segment | Between-segment median spread | Within-population IQR |
|---|---:|---:|---:|
| Price codes | **1.7%** | 2 | 10 |
| Active products | **1.9%** | 2,489 | 4,317 |
| Orders (12m) | **2.8%** | 460 | 1,671 |
| Territories | **3.4%** | 0 | 0 |
| Customers | **4.9%** | 3,212 | 4,629 |
| Customer price codes | **5.2%** | 3 | 5 |
| Collections | **10.9%** | 372 | 434 |

On every metric, the spread *within* segments exceeds the spread *between* them. **Structure is
essentially independent of selling motion.** "Build the surface once, parameterise on the org's own
structure, do not condition on segment" is not merely supported — it is better supported than the
register claims.

**But two of the four named job-level attributions do not reproduce** (detail in
`06-SEGMENT-VARIATION.md`):

| Job | Register's claim | Measured | Verdict |
|---|---|---|---|
| JTBD-013 | SEG-04, median 4,498 products | SEG-04 median **4,505** | **Reproduces** |
| JTBD-053 | SEG-04, largest catalogs / least structure, median 30 collections | SEG-04 largest catalogs ✓, fewest collections ✓ (median **58**, not 30) | **Reproduces directionally** |
| JTBD-012 | SEG-02, median **41 territories** | Median is **0 in every segment**; 90 of 109 orgs have none. Among the 19 that do, SEG-02's median is 102 | **Does not reproduce** |
| JTBD-083 | SEG-03, widest price-code spread | SEG-03 has the **second-narrowest** customer price-code median (2). The widest spread is SEG-02 (max 192, p90 69) | **Misattributed** |

**What it changes:** nothing about the build-once decision — keep it, and state it more confidently.
Everything about the evidence cited for it. Do not repeat "SEG-02 median 41 territories" or
"SEG-03 has the widest price-code spread" in the readout; both are wrong.

---

## The rest, still consequential

### 6. Buyer-initiated web ordering is the fastest-growing channel in the system — and the register ranks it last
`MEASURED` · **Q054** · Over eight quarters: buyer web orders **+29.2%** (8,441 → 10,907) against
iPad **+10.2%** (34,013 → 37,480). Web share of orders 19.9% → 22.5%. Total orders +14.0%.
Meanwhile the internal/rep population is **flat to declining** since 2025Q2 (Q050: 2,530 → 2,301
distinct people per quarter). The roadmap puts the two buyer configuration items at ranks 15 and 16
of bucket A — last. **Growth is in the population we deprioritised.**

### 7. JTBD-053's problem is ~118,000 items smaller than stated, and two of its four checks should be deleted
`MEASURED` · **Q005, Q045, Q046** · The 179,623 "no image" figure reproduces exactly. But:
`no_net_price` is **all-or-nothing per org** — 25 orgs never populate the field at all (91,030
items) because they price through price levels. Counting them as incomplete flags entire correct
catalogs. Genuine missing prices: **98,441**, not 189,471. Genuine missing images (excluding orgs
that use no images at all): **153,084**, not 179,623. Category and collection are essentially
complete — **8** and **196** items respectively; drop both checks. Test/staging orgs (`ctest`,
`tam-staging`, `ahtest`) contribute ~24,700 of the headline. **The completeness rule must be
org-relative or the cheapest build on the roadmap ships ~118,000 false positives.**

### 8. ERP order status exists for 43 orgs — in 125 unnormalised spellings
`MEASURED` · **Q031, Q032** · JTBD-015 and JTBD-043 are filed as blocked because open-order status
"lives in the client's ERP." It is in Postgres, on `portal_orders.status`, for **43 orgs across
1,280,046 rows in 12 months** — but as **125 distinct values**. "Closed" appears as `C` (251,691),
`Closed` (154,750) and `CLOSED` (43,603); "cancelled" in six spellings; "open" in seven. Twelve
single-character codes cover 574,621 rows. **Eighteen values are literal dates** (`09/01/2026`) — a
field-mapping defect. This reframes 015/043 from "data we do not have" to "a status-normalisation
map we have not written." That is a materially cheaper conclusion and it deserves re-testing before
those jobs stay in the blocked bucket.

### 9. A naive decline rule fires on 44% of the customer base
`MEASURED` · **Q037** · Across 40 feed orgs, comparing trailing 90 days to the prior 90:
52,818 accounts active in either period; **15,156 went silent entirely**, 7,862 more are down >30%
while still buying — **23,243 accounts, 44.0%**, carrying $112.9M of decline against a $302.7M base.
That is not a work list, it is noise. The register *asserts* JTBD-062 needs an account-aware window
(A8); this **demonstrates** it and gives the tuning target. `JUDGMENT`: the Jun–Aug vs Mar–May
comparison crosses a market cycle, which inflates the count — a confound that argues the same way.

### 10. Fifteen orders are 24.2% of all recorded order value. One of them is $464M
`MEASURED` · **Q055, Q056** · Over 24 months, 357,317 orders total $2.048B. **Fifteen orders above
$1M account for $496.1M** — and a single order at org `shl` is **$464,039,002**, which alone creates
the entire 2025Q2 spike in `data/Q054.csv`. Excluding it, 24-month value is ~$1.584B. 11,925 orders
(3.3%) have a zero total. Any topline built on `orders.total` without outlier handling is wrong by a
quarter. This is a concrete mechanism behind the register's "eCat runs 0.22–3.10× invoiced truth,"
and it bears directly on the JTBD-031/061 honesty ceiling.

### 11. PER-02: right decision, wrong reason
`MEASURED` · **Q070, Q071** · The register declines the rep agency principal because normalising
"11,880 free-text company names" is a migration. The 11,880 reproduces (**11,799** internal distinct
names; case-insensitive dedup only reaches 11,612, so casing is not the problem). But the real
blocker is different and stronger: **only 868 of 4,026 active reps (21.6%) have `company_name`
populated at all**, and among `primary_rep_group` reps only 125 of 590 (21.2%). **Normalisation
cannot fix absence.** Keep the decline; change the reason on file.

Separately, PER-02 is **behaviourally real**: agency reps are measurably more productive than other
reps — 60.3% zero-order vs 71.3%, 11.67 vs 7.46 average orders (Q011).

### 12. Inventory staleness is severe by org and negligible by buyer
`MEASURED` · **Q033, Q034** · 187 orgs hold inventory; only 68 refreshed within 2 days and **83 have
not been updated in over a year** (max age 5,530 days). 48.8% of all inventory rows are >30 days
stale. But weighted by the buyers who actually see it: **15,837 of 17,550 (90.2%) are at orgs
refreshed within 2 days**, and only **84 buyers** sit behind year-stale inventory. JTBD-084's
staleness label is cheap and correct — it just will not surface much.

### 13. `taxonomies.created_at` is not a usable launch date
`MEASURED` · **Q035, Q036** · `products` has **no timestamp columns whatsoever** — confirming the
register's A1 is genuinely needed. `taxonomies` (Collection) does have `created_at`, and 19,197
collections were created in 12 months across 119 orgs, which looks like a free launch date. It is
not: **149 of 239 orgs (62%) created half or more of their collections on a single day**, and 64
orgs created 90%+ on one day. That is bulk import, not launch. Only 56 orgs spread creation across
20+ days. The shortcut fails; A1 stands, now with evidence.

### 14. Two-thirds of importing orgs hit an import error last month
`MEASURED` · **Q043** · 42,575 import events in 30 days across 107 orgs; **6,092 carry error text
across 71 orgs**, plus 10,157 carrying warnings. Nothing pushes a notification. JTBD-034 is sized.

### 15. Order-failure reasons do exist — but the job is smaller than it looks
`MEASURED` · **Q041, Q042** · The register says order-failure reason codes "do not exist as a
queryable field." `orders.export_errors` and `orders.num_failures` exist and are populated on
**1,862 orders across 16 orgs** (1.0% of 12-month volume). *Caution:* a naive count of non-blank
`export_errors` returns 19,003, but 17,141 of those are the literal string `[]` — an empty array,
meaning no error. The real classes are mostly integration transport (`401 Unauthorized` ×1,003,
gateway errors, timeouts); the preventable-at-entry class is roughly **580 orders**. So: correct the
register's "does not exist," but do **not** move JTBD-044 up the roadmap on the strength of it.

### 16. The option/CPQ footprint is ~4× wider than assumed for reporting, and narrower for configuration
`MEASURED` · **Q039** · Option groups exist in **93 orgs**, options in **92** (46,432 values), matrix
options in **53**. But the configurator cascade — `option_mappings` — exists in only **7 orgs**, and
`option_forms` in 10. "16 CPQ orgs" sits between two different definitions. Confirmed separately:
chosen option values are **not** captured per order line (sampling 30,000 populated `custom_data`
blobs on `portal_order_items` returns only the key `item`). A13 is genuinely required.

### 17. Only 44 of 56 feed orgs have a *live* feed
`MEASURED` · **Q003** · 56 orgs have rows in `portal_invoices`, but only **44** have any row dated in
the last 12 months. Twelve orgs have a feed that has stopped. The register's coverage figures count
historical presence, not current delivery. For any job that asks "what happened this year," the real
denominator is 44 of 112, not 48 of 112.

---

## Confidence notes

- All population and coverage counts are **high confidence**: single-table counts over well-defined
  predicates, reproduced against the register's own stamped figures in `01-CALIBRATION.md`.
- The rep-band split (finding 2) is **high confidence** because it reproduces on an independent
  variable (login-days) that was not used to construct it.
- Finding 9's magnitude is **medium confidence** on the exact percentage — the seasonality confound
  is real. Its *direction* (a naive rule is unusable) is high confidence.
- Finding 8's implication is **medium confidence**: the status values are present and unnormalised,
  which is measured, but whether a normalisation map would satisfy JTBD-015/043 depends on whether
  those statuses are refreshed on a useful cadence per org. That is not tested here and is named in
  `08-UNVERIFIABLE.md`.
