# SuperCat Client Segmentation v4.0

> **Date:** 2026-07-09  
> **Status:** STAMPED by Kjael. **This file is preserved exactly as stamped — do not edit its
> body.** Two rounds of post-stamp correction happened; both are documented in
> [`unmatched_accounts_validation_2026-07-09.md`](unmatched_accounts_validation_2026-07-09.md):
>
> 1. The 5 unmatched (`??`) accounts were validated against live Postgres. Legrand US, Silver
>    One, Tomlinson Companies, and Ideal Living resolved cleanly to real orgs. Gabriella White
>    was (incorrectly, see round 2) treated as a duplicate of "Summer Classics" and dropped,
>    producing a since-superseded "108 account" interim figure.
> 2. That was wrong: `sc` (mapped to "Summer Classics" since v3.2) is actually **Gabriella
>    White** — the parent LLC of the Summer Classics family. The real Summer Classics org
>    (`scw`) was missing from the roster entirely. Fixed at the root in `build_v4.py`; both are
>    now separate rows, alongside Summer Classics Contract (`sccon`).
>
> **Net result: the corrected universe is 109 accounts — the same headline counts Kjael
> originally stamped below (33 / 38 / 24 / 14).** What changed on correction was which org 2 of
> those 109 rows point at (and, separately, a median-calculation bug in §3 — see
> `../../current/SuperCat_Client_Segmentation_v4.0.md`, which carries every corrected number).
> The counts below are the as-stamped figures and happen to already be correct at the headline
> level; treat `current/SuperCat_Client_Segmentation_v4.0.md` as canonical for per-org data and §3 medians.  
> **Null hypothesis:** The v3.2 4-segment model (Kylor-stamped)  
> **Verdict:** **The 4-segment model holds.** Dissolve the 5th segment (Specialty). All enrichment axes confirm the existing boundaries.

---

## Executive Summary

v4.0 tested the v3.2 4-segment model against **every available first-party data dimension** from SuperCat's Postgres database — product catalogs, customer structures, order behavior, invoice revenue, rep activity, and taxonomy diversity — combined with the v3.2 comprehensive analysis (109 orgs, all data layers).

**Result:** The four selling-motion segments are empirically sound. The enrichment adds three classification axes (how they sell, what they sell, who they sell to) as dimensions *within* segments, validating v3.2's finding that "price is a correlate, not a classifier." No natural new cut emerged from the richer data.

### Recommendation for Kjael

**Stamp the 4-segment model as definitive.** Dissolve the 5th segment (Specialty/Non-Traditional) — those 5 accounts all fit cleanly in existing segments. The final structure is:

| # | Segment | Count | Selling Motion |
|---|---------|-------|----------------|
| 1 | Luxury Specification | 33 | Designers put it in a project |
| 2 | Premium Trade Brand | 38 | Dealers carry the line on brand reputation |
| 3 | Mid-Market Multi-Channel | 24 | Trade + retail + online distribution |
| 4 | Volume Distribution | 14 | Commodity distribution, high volume |

---

## 1. Methodology

### 1.1 Data Sources

| Source | What it provides | Coverage |
|--------|-----------------|----------|
| `organizations` (Postgres) | Identity, join key | All 109 |
| `products` (Postgres) | Catalog size, avg/min/max price, category/collection/tradename diversity | 98 orgs with active products |
| `customers` (Postgres) | Customer count, territory diversity, price-code complexity | 97 orgs |
| `orders` (Postgres) | Order count, AOV, recency, total GMV | 103 orgs with submitted orders |
| `portal_invoices` (Postgres) | Invoiced revenue (commercial truth per provenance_spine) | 55 orgs with invoice feeds |
| `org_users` (Postgres) | iPad-active rep count | All matched orgs |
| `distribution_centers` (Postgres) | Fulfillment footprint | 17 orgs (sparse) |
| v3.2 Comprehensive CSV | Prior segment assignment, catalog scrub median, realized mean, best price | All 109 |

### 1.2 The Three Classification Axes (from Kjael)

1. **How they sell** — the primary segmenting axis (selling motion)
2. **What they sell** — product vertical (furniture, lighting, outdoor, accessories, decor, rugs, textiles)
3. **Who they sell to** — buyer type (trade/designers, wholesale/dealers, mixed, retail, contract)

### 1.3 Approach

- Used v3.2 validated segments as the **null hypothesis** (Kylor-stamped)
- Pulled every available dimension from Postgres for all 109 orgs
- Classified each org on all three axes using quantitative signals
- Tested whether the data supports, contradicts, or refines the 4-segment model
- Used median price as a **continuous dimension** (per Kjael's direction), not a boundary

---

## 2. Findings: The Model Holds

### 2.1 Segment Stability

Of the 109 accounts:
- **101 accounts** (93%) remain in their v3.2 segment when enrichment data is applied
- **8 accounts** moved — all from the "unknown" (no DB match) or "Specialty" catch-all categories
- **0 accounts** from the core 4 segments were reclassified by quantitative evidence

The Specialty segment (5 accounts in v3.2) dissolves cleanly:
- Sabine Pools → Brand-Building (outdoor/pool retailer, $614 avg, dealer model)
- Kaleen Rugs → Volume Distribution ($7 avg price, commodity rug distribution)
- Tomlinson Companies → Brand-Building (furniture)
- America's Backyards → Brand-Building (outdoor)
- Ideal Living → Brand-Building (furniture)

### 2.2 Price as a Continuous Dimension (not a boundary)

v3.2 found that price doesn't create clean segment boundaries. v4.0 **confirms this** with the full enrichment:

| Segment | Price Range (best available) | Mean | Observation |
|---------|------------------------------|------|-------------|
| Specification | $14 – $13,000 | $1,582 | Enormous range; includes parts-only orgs (Schonbek $14) and ultra-luxury (Alfonso Marina $9,100) |
| Brand-Building | $60 – $2,500 | $427 | Overlaps heavily with Specification at the low end |
| Multi-Channel | $55 – $450 | $139 | Tight band; most homogeneous on price |
| Volume | $3 – $33 | $13 | Only boundary that is cleanly numeric |

**The Luxury/Premium boundary is selling motion (specification vs. brand-building), NOT price.** This is confirmed: Gabby ($593), Currey & Company ($624), and Sarreid ($968) all sell through designer specification despite having lower average prices than some Brand-Building companies like Hubbardton Forge ($846) or Summer Classics Contract ($537).

**The only clean numeric boundary is Mid-Market/Volume** — below ~$50 avg price, everything is volume distribution.

### 2.3 Product Vertical (What They Sell) — a Dimension, Not a Segment

| Vertical | Count | Segments Represented |
|----------|-------|---------------------|
| Lighting | 44 | All 4 segments |
| Furniture | 33 | All 4 segments (Volume = housewares/parts) |
| Accessories/Giftware | 14 | Primarily Volume + Brand-Building |
| Decor/Art | 9 | Primarily Specification + Brand-Building |
| Outdoor | 7 | Specification + Brand-Building |
| Rugs | 1 | Volume |
| Textiles | 1 | Multi-Channel |

**Key finding:** Product type does NOT segment cleanly. Lighting companies span all four segments (from Visual Comfort at Specification to Bulbrite at Volume). Furniture similarly spans the full range.

### 2.4 Buyer Type (Who They Sell To) — Aligns with Selling Motion

| Buyer Type | Count | Primary Segment |
|-----------|-------|-----------------|
| Trade (Designers/Architects) | 33 | Specification (100% alignment) |
| Wholesale (Dealers) | 28 | Brand-Building |
| Wholesale (Dealers/Retailers) | 20 | Multi-Channel |
| Wholesale (Retailers) | 14 | Volume |
| Wholesale (Broad Dealer Network) | 7 | Brand-Building (large-scale) |
| Mixed (Trade + Retail) | 7 | Brand-Building + Multi-Channel |

**Buyer type is almost perfectly predicted by selling motion.** This confirms that the selling-motion axis (how they sell) is the fundamental classifier — who they sell to follows naturally.

---

## 3. Enrichment Dimensions (new data from Postgres)

### 3.1 Platform Activity & Scale

| Metric | Specification (33) | Brand-Building (38) | Multi-Channel (24) | Volume (14) |
|--------|-------------------|--------------------|--------------------|-------------|
| Median iPad-active reps | 56 | 68 | 55 | 42 |
| Median order count | 2,595 | 6,817 | 289 | 5,955 |
| Median AOV | $5,295 | $3,391 | $2,248 | $1,783 |
| Orgs with invoice feed | 16 (48%) | 19 (50%) | 10 (42%) | 10 (71%) |
| Median invoiced revenue (where present) | $67M | $50M | $18M | $61M |

### 3.2 Catalog Complexity

| Metric | Specification | Brand-Building | Multi-Channel | Volume |
|--------|--------------|----------------|---------------|--------|
| Median product count | 3,340 | 2,480 | 2,651 | 4,916 |
| Median distinct categories | 32 | 33 | 24 | 53 |
| Median distinct collections | 113 | 195 | 270 | 22 |

Volume orgs have FEWER collections but MORE categories — they organize by functional type, not aesthetic/design collections.

### 3.3 Customer Structure

| Metric | Specification | Brand-Building | Multi-Channel | Volume |
|--------|--------------|----------------|---------------|--------|
| Median customer count | 4,803 | 3,746 | 1,978 | 1,764 |
| Median territory count | 32 | 34 | 43 | 48 |
| Median price codes | 5 | 6 | 3 | 1 |

**Interesting:** Multi-Channel has MORE territories but FEWER customers — broader geographic reach with thinner coverage per territory (consistent with multi-channel distribution strategy). Volume has the simplest pricing (1 code = flat pricing).

---

## 4. Segment Definitions (v4.0 — data-grounded)

### Segment 1: Luxury Specification (33 orgs)

**Selling motion:** Designers and architects specify these products into projects. The sale is project-driven, relationship-driven, and taste-driven. Orders are large, complex, and often bespoke.

**Quantitative signature:**
- High AOV ($5,000+, often $10,000+)
- Moderate order volume (large value, fewer transactions)
- 3–15 price codes (trade/designer/contract tiers)
- Products organized by aesthetic collections
- Customer base is designers, showrooms, A&D firms

**Price range:** $14–$13,000 (price does NOT define this segment — selling motion does)

**Exemplars:** Palecek, Theodore Alexander, Interlude, Visual Comfort Signature, Currey & Company, Gabby, Charleston Forge

### Segment 2: Premium Trade Brand (38 orgs)

**Selling motion:** Dealers carry the line based on brand reputation. The manufacturer builds brand awareness; dealers stock and sell. The relationship is brand→dealer→end consumer.

**Quantitative signature:**
- Moderate-high AOV ($2,000–$8,000)
- Moderate-high order volume
- 4–8 price codes (wholesale tiers)
- Broad dealer network (2,000–9,000 customers)
- Territory-based rep coverage

**Price range:** $60–$2,500

**Exemplars:** Braxton Culler, Summer Classics, Wildwood/Chelsea House, Furniture Classics, Jamie Young Company, Hubbardton Forge

### Segment 3: Mid-Market Multi-Channel (24 orgs)

**Selling motion:** Products reach the market through multiple channels — trade, retail, online, contract. Distribution is broad and not exclusive. Often the manufacturer sells through a mix of showrooms, big-box adjacent, online marketplace, and direct.

**Quantitative signature:**
- Moderate AOV ($1,000–$4,000)
- Highly variable order volume
- Many price codes (7–35; complex multi-channel pricing)
- Broad territory coverage with thinner per-territory penetration
- Often lighting companies with residential + commercial channels

**Price range:** $55–$450

**Exemplars:** Savoy House, Craftmade, Maxim Lighting, Kichler, Linon/Powell, Golden Lighting

### Segment 4: Volume Distribution (14 orgs)

**Selling motion:** Commodity distribution — high volume, low unit price, low touch. The competitive advantage is logistics, breadth of assortment, and price. Often importers or distributors rather than manufacturers.

**Quantitative signature:**
- Low AOV ($500–$2,000 despite volume)
- Very high order count (5,000–80,000+)
- 1–2 price codes (flat pricing)
- Large product catalogs (5,000–35,000 SKUs)
- Categories organized functionally, not aesthetically

**Price range:** $3–$33

**Exemplars:** Abaline Supply, Home Essentials & Beyond, Kennedy International, Pioneer Morton, Uniware

---

## 5. Accounts That Remain Ambiguous

| Account | Issue | Current Placement | Data Says |
|---------|-------|-------------------|-----------|
| Schonbek Lighting (sbl) | Only 1 product in DB ($14), but v3 placed at Specification with $14,255 AOV | Specification | Likely a data artifact (old/demo org). Keep at Specification based on AOV + brand position |
| Visual Comfort - Studio/Fans (fms) | $115 median, $92K AOV — the AOV is from the VC consolidated ordering system, not per-item | Specification | AOV inflated by consolidated orders. Products are mid-range fans/studio lighting. Could be Multi-Channel, but keeps Specification due to VC family selling motion |
| WAC/Modern Forms (wac) | No products in DB, $4,338 AOV, 139 iPad users — significant platform activity | Brand-Building | Commercial lighting / architectural spec. Could be Specification. Stay at Brand-Building per v3.2 |
| Universal Furniture (ufi) | No products in DB (portal-only ERP org), $7,671 AOV | Brand-Building | Massive furniture company. $252M invoiced. Clearly a premium brand. Placement correct |
| Fine Art Handcrafted Lighting (fal) | No products in DB, $17,073 AOV | Specification | Ultra-luxury decorative lighting. Placement correct |

---

## 6. Median Price as a Continuous Variable

Per the handoff directive, median price is tracked as a **continuous data point within each segment**, not a boundary:

### Specification (33 orgs) — price distribution
```
$14 ─── $461 ─── $749 ─── $1,183 ─── $9,100 ─── $13,000
         Q1       Median     Q3
```

### Brand-Building (38 orgs) — price distribution
```
$60 ─── $196 ─── $350 ─── $607 ─── $2,500
         Q1       Median    Q3
```

### Multi-Channel (24 orgs) — price distribution
```
$55 ─── $80 ─── $109 ─── $153 ─── $450
         Q1      Median     Q3
```

### Volume (14 orgs) — price distribution
```
$3 ─── $7 ─── $10 ─── $19 ─── $33
        Q1     Median    Q3
```

**The Spec/Brand-Building overlap zone ($300–$700) is the widest.** This is exactly where selling motion — not price — determines segment membership.

---

## 7. Does a Different Cut Emerge?

The handoff asked: "Test whether a different cut emerges naturally."

**Answer: No.** The three-axis enrichment (how/what/who) confirms the 4-segment model rather than suggesting a new structure. Specifically:

1. **Product type (what they sell) does NOT segment.** Lighting companies are in all 4 segments. Furniture companies span 3 segments. Product vertical is a tag, not a classifier.

2. **Buyer type (who they sell to) is redundant with selling motion.** It's almost perfectly predicted by the segment — adding it as a separate axis provides no new discrimination.

3. **The only axis that segments is selling motion (how they sell).** And it produces exactly the 4 groups v3.2 identified.

4. **Price is the strongest continuous correlate** but still cannot cleanly separate segments 1 and 2.

The data-driven conclusion: **Keep the 4-segment model. Enrich each segment with product vertical and price as continuous dimensions for downstream use (ICP work, product-market fit, pricing strategy).**

---

## 8. Full Roster

See companion file: `SuperCat_Customer_Segmentation_v4.0_MASTER.csv`

Columns:
- `Company`, `org`, `org_id` — identity
- `v3_segment`, `v4_segment`, `segment_changed` — movement tracking
- `how_they_sell`, `what_they_sell`, `who_they_sell_to` — the three axes
- `best_price`, `catalog_avg_price`, `catalog_scrub_median`, `realized_mean` — price dimensions
- `product_count`, `customer_count`, `territory_count`, `price_code_count` — structure
- `order_count`, `avg_order_value`, `most_recent_order` — activity
- `total_invoiced_net` — commercial truth (where available)
- `ipad_active_users` — platform engagement
- `distinct_categories`, `distinct_collections` — catalog complexity

---

## 9. Constraints & Caveats

- **Postgres is read-only.** All queries were SELECT-only against `user-supercat-postgres-vpn`.
- **No imposed labels.** Per the provenance spine, segments emerged from first-party data (selling motion, not fit scores).
- **109 accounts is the universe.** The v3.2 comprehensive CSV is the canonical list.
- **5 accounts have `??` shortnames** and no Postgres match. Classified by company name and qualitative knowledge only.
- **11 orgs have no products in Postgres** (portal-only orgs with invoice/order data but no catalog). Classified by order behavior and company identity.
- **MCP SQL limitations:** `PERCENTILE_CONT`, `STDDEV`, `ROUND`, `::numeric` casts were blocked. All statistical analysis done in Python post-retrieval.
- **The kll (Kuzco) invoice figure ($437B) is a data anomaly** — excluded from revenue analysis.

---

## 10. Output Files

| File | Location |
|------|----------|
| This document | `Customer Segmentation/v4/v4.0_archive/SuperCat_Client_Segmentation_v4.0.md` |
| Master CSV (109 rows, all dimensions) | `Customer Segmentation/v4/v4.0_archive/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` |
| Build script (reproducible) | `Customer Segmentation/v4/v4.0_archive/build_v4.py` |

---

## 11. Next Steps (if stamped)

1. **Dissolve the Specialty segment** in all downstream references
2. **Propagate the three-axis classification** to the Insightful Product customer intelligence layer
3. **Use product vertical and median price as continuous dimensions** in ICP/product-market-fit work
4. **Validate the 5 unmatched (??) accounts** with Kjael — confirm company→org mapping
5. **Consider adding a "platform maturity" dimension** (not a segment) based on iPad activity, invoice feed presence, and catalog completeness
