---
id: TAX-A
title: Layer A — Account Segments
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
layer: A
availability: post-sale-only
source_lineage:
  - Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv  # ROSTER_ANSWER_KEY, 109 rows, stamped Kjael 2026-07-09
  - Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.md            # stamped narrative, §4 signatures
  - Postgres (read-only): organizations, products, customers, orders, portal_invoices, org_users
  - foundation/07_how_we_establish_truth.md                                        # principle 7 (first-party over imposed labels)
depends_on: []
consumed_by: [TAX-MAP]
---

# Layer A — Account Segments

**What this layer is.** The v4.0 selling-motion classification of SuperCat's own client
organizations, computed from first-party commercial data in Postgres.

**Availability: POST-SALE ONLY.** Every field below requires a live SuperCat instance with
loaded catalog, customer file, and order history. **No Account Segment can be assigned to a
company that is not already a customer.** This is a schema-level constraint, not a caveat —
see `availability: post-sale-only` in the frontmatter. Anything needed before a company is a
customer belongs in [Layer B](prospect-archetypes.md).

---

## 1. The segments

| ID | Name | Slug | n | Selling motion (quoted from the stamped v4.0 doc §4) |
|---|---|---|---:|---|
| SEG-01 | Luxury Specification | `luxury_specification` | 33 | *"Designers and architects specify these products into projects."* |
| SEG-02 | Premium Trade Brand | `premium_trade_brand` | 38 | *"Dealers carry the line based on brand reputation."* |
| SEG-03 | Mid-Market Multi-Channel | `mid_market_multi_channel` | 24 | *"Products reach the market through multiple channels — trade, retail, online, contract."* |
| SEG-04 | Volume Distribution | `volume_distribution` | 14 | *"Commodity distribution — high volume, low unit price, low touch."* |
| SEG-00 | Unclassified — insufficient data | `unclassified` | 9 | Not a segment. Abstention state; see §5. |

Populations are `[MEASURED]` from ROSTER_ANSWER_KEY (109 rows; 33/38/24/14 verified by row count
2026-08-25). SEG-00 is a state of the *rule*, not a partition of the roster — the 9 orgs it covers
carry stamped labels assigned by human judgment.

**Alias.** SEG-02 is written as **"Brand-Building"** throughout §2, §3 and §6 of the stamped v4.0
document, in `build_v4.py`, in the MASTER CSV, and in four Insightful Product 4.0 profiles
`[MEASURED: grep]`. **"Premium Trade Brand" is canonical; "Brand-Building" is a deprecated alias.**
Existing files are not swept — new writes bind to the canonical name.

---

## 2. Field-level data lineage

The four defining fields, as established:

| Field | MASTER CSV column | Postgres origin | Coverage on roster |
|---|---|---|---|
| Average order value | `avg_order_value` | `orders` — total value ÷ order count | 100/109 non-zero |
| Price code count | `price_code_count` | `customers` — distinct price codes | 99/109 non-zero |
| Customer count | `customer_count` | `customers` — rows per org | 99/109 non-zero |
| Order volume | `order_count` | `orders` — submitted orders | 100/109 non-zero |

All `[MEASURED]` 2026-08-25 against the stamped CSV. Supporting (non-defining) columns in the same
roster: `product_count`, `territory_count`, `distinct_categories`, `distinct_collections`,
`total_invoiced_net`, `ipad_active_users`, `most_recent_order`, `best_price`, `catalog_avg_price`.

**Invoiced revenue is not a defining field** and must not become one: only 38 of 109 orgs have an
invoice feed `[OBSERVED: stamped v4.0 §1.1]`, and per `07_how_we_establish_truth.md` principle 4 a
composite inherits the lowest confidence of its inputs.

---

## 3. Measured distributions — read this before trusting any threshold

Per-segment quartiles of the four defining fields, computed directly from ROSTER_ANSWER_KEY
`[MEASURED]`:

| Field | | SEG-01 | SEG-02 | SEG-03 | SEG-04 |
|---|---|---:|---:|---:|---:|
| avg_order_value | p25 / **med** / p75 | 2,765 / **4,501** / 9,742 | 2,100 / **3,864** / 6,349 | 1,782 / **2,548** / 4,851 | 923 / **1,266** / 2,076 |
| price_code_count | p25 / **med** / p75 | 1 / **4** / 6 | 1 / **4** / 6 | 1 / **2** / 6 | 1 / **1** / 2 |
| customer_count | p25 / **med** / p75 | 301 / **4,418** / 6,548 | 673 / **2,567** / 7,975 | 741 / **1,544** / 3,206 | 643 / **1,695** / 2,160 |
| order_count | p25 / **med** / p75 | 126 / **1,283** / 11,531 | 354 / **1,584** / 10,231 | 68 / **210** / 994 | 1,591 / **5,759** / 18,662 |

Only AOV is monotonic across segments, and its interquartile ranges overlap on every adjacent pair.
`price_code_count` does not separate SEG-01 from SEG-02 at all (identical p25/median/p75).

### 3.1 The stamped §4 signatures do not reproduce

The "quantitative signature" bullets in the stamped v4.0 §4 are **descriptive prose written
alongside the classification, not rules that generate it.** Tested against the roster they
describe `[MEASURED]`:

| Stamped claim (§4, quoted) | Measured on its own segment | Holds? |
|---|---|---|
| SEG-01 *"High AOV ($5,000+, often $10,000+)"* | 14 of 33 are ≥ $5,000 | **No — 58% of the segment fails it** |
| SEG-03 *"Many price codes (7–35; complex multi-channel pricing)"* | 6 of 24 in range; median is **2** | **No — 75% of the segment fails it** |
| SEG-03 *"Highly variable order volume"* | Lowest median order count of any segment (210) | Misleading |
| SEG-04 *"1–2 price codes (flat pricing)"* | 11 of 14 (`bri`=22, `krb`=14, `etl`=3 fail) | Mostly |
| SEG-04 *"Very high order count (5,000–80,000+)"* | 9 of 14 in range | Mostly |

This is a finding, not a defect I introduced. It means **Layer A thresholds had to be authored,
not transcribed** — and it caps how well any rule can do.

---

## 4. The authored classification rule

Thresholds below are chosen as round, defensible values informed by the measured medians in §3.
They are **not** fitted to maximise agreement with the answer key.

### 4.1 Precedence rule (first match wins — order is load-bearing)

```
0. if avg_order_value = 0 AND order_count = 0        -> SEG-00  (abstain, insufficient data)
1. if order_count >= 4,000 AND avg_order_value < 2,500 -> SEG-04  (volume distribution)
2. if order_count <  1,000 AND avg_order_value < 5,000 -> SEG-03  (mid-market multi-channel)
3. if avg_order_value >= 5,000                        -> SEG-01  (luxury specification)
4. otherwise                                          -> SEG-02  (premium trade brand)
```

**Why this order.** SEG-04 is the only segment with a clean numeric boundary — the stamped doc says
so itself (*"The only clean numeric boundary is Mid-Market/Volume"*, §2.2) and the data agrees, so
it is tested first. SEG-03 is the low-order-count segment and must be tested before the AOV cut,
or its members fall through into SEG-01/SEG-02 on price alone. SEG-02 is the residual because it
is the largest segment and the least numerically distinctive. SEG-01 is a positive AOV test rather
than a residual so that misclassification lands in SEG-02 rather than in the premium segment.

### 4.2 How well it works — the real number

| Measure | Result |
|---|---|
| Reproduces stamped label | **42 / 109 = 38.5%** |
| On scored subset (excluding the 9 abstentions) | 42 / 100 = 42.0% |
| Majority-class baseline (call everything SEG-02) | 38 / 109 = **34.9%** |
| Best-fit ceiling — 1,800 threshold combinations optimised **on the answer key itself** | **50.0%** |

All `[MEASURED]` 2026-08-25.

Per-segment recall of the authored rule:

| Stamped | → SEG-00 | → SEG-01 | → SEG-02 | → SEG-03 | → SEG-04 | Recall |
|---|---:|---:|---:|---:|---:|---:|
| SEG-01 | 4 | **14** | 9 | 3 | 3 | 42.4% |
| SEG-02 | 4 | 12 | **8** | 9 | 5 | 21.1% |
| SEG-03 | 1 | 6 | 3 | **13** | 1 | 54.2% |
| SEG-04 | 0 | 1 | 2 | 4 | **7** | 50.0% |

### 4.3 What this means — the governing conclusion of Layer A

**The v4.0 segment assignment is not a computable function of the four defining fields.** An
authored rule reaches 38.5% against a 34.9% majority baseline, and even thresholds fitted directly
to the answer key cap at 50%. SEG-02 — the largest segment — has 21% recall.

The v4.0 labels were assigned from **selling-motion judgment inherited from v3.2**, with the
quantitative fields used as corroboration. The stamped doc is explicit that this was the method
(*"Used v3.2 validated segments as the null hypothesis"*, §1.3) and that price *"does NOT define
this segment"* (§4). The four fields are **correlates of a human classification, not its
definition.**

Therefore:

- **The authority for an Account Segment is the stamped roster — a lookup, not a computation.**
  `SuperCat_Customer_Segmentation_v4.0_MASTER.csv` keyed on org shortname is the answer.
- **The rule in §4.1 is a provisional classifier for orgs not on the roster** (new customers since
  2026-07-09). It is marked **FLAGGED** and must not be used to re-derive, audit, or overwrite a
  stamped label. Its output carries confidence tier PARTIAL at best per
  `07_how_we_establish_truth.md` §3.
- Assigning a segment to a **new** customer should be a human read corroborated by §4.1, not §4.1
  alone.

---

## 5. SEG-00 — the abstention set

Nine orgs have zero in both `avg_order_value` and `order_count`, so no rule can classify them
`[MEASURED]`: `fal`, `cf`, `hh`, `kkc`, `leg`, `mfc`, `soi`, `abol`, `ilc`.

A further overlapping set has zero `price_code_count` and `customer_count`: adds `swc`, `ml`, `sp`.

Five of these are already named in the stamped doc §5 as *"Accounts That Remain Ambiguous"* —
`sbl`, `fms`, `wac`, `ufi`, `fal` — four of which have no products in Postgres. Overlap between the
two lists is `fal` only, so **the union of orgs that Layer A cannot stand behind is 13**, not 5.

These orgs keep their stamped labels. They must be excluded from any distribution, median, or
threshold computed off Layer A, and never silently dropped (principle 6).

---

## 6. What each segment is valid for deciding

| Decision | Valid? | Why |
|---|---|---|
| Messaging vocabulary, buyer-mix expectations, product-identity language | **Yes** | The purpose the lens was built and stamped for `[OBSERVED: sources/customer_segmentation/README.md]` |
| Which analytics surface / JTBD variant an existing customer needs | **Yes, with care** | To be tested per-JTBD in Phase 2; a "does not differ by segment" result is a valid finding |
| Pricing, tier, WTP, expansion path | **No** | That is Lens 1 (Digital Selling Maturity, T1/T2/T3). *"Segment is not tier"* `[OBSERVED: CEO_SYSTEM_CONTEXT.md lens router]` |
| Qualifying or scoring a **prospect** | **No** | Post-sale-only. Established input: 53% vs 30% baseline on public data. Use Layer B |
| Account-level buyer type | **No** | Predicted by motion at brand level, but *"must be resolved from account evidence, not inherited"* `[OBSERVED: sources README §3]` |
| Re-deriving or auditing a stamped label | **No** | See §4.3 |

---

## 7. Open items

- The §4 signature prose in the stamped document is inaccurate for SEG-01 and SEG-03 (§3.1). It is
  stamped and is **not** edited here. Proposed correction is held in `../FOUNDATION-CORRECTIONS.md`.
- No segment has been re-derived. This layer restates and constrains v4.0; it does not re-litigate it.
