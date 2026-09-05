# SuperCat Client Segmentation v4.0

> **Date:** 2026-07-09 · **Status:** STAMPED by Kjael, corrected post-stamp (three rounds).
> **This is the live/current copy.** Corrections after the stamp are traced through
> [`../v4/v4.0_archive/unmatched_accounts_validation_2026-07-09.md`](../v4/v4.0_archive/unmatched_accounts_validation_2026-07-09.md):
>
> 1. **Round 1:** Validated the 5 unmatched (`??`) accounts against live Postgres. Legrand US,
>    Silver One, Tomlinson Companies, and Ideal Living resolved cleanly to real, active orgs.
>    Gabriella White was (incorrectly) treated as a duplicate of "Summer Classics" and dropped,
>    taking the roster to 108.
> 2. **Round 2:** That was wrong. `organizations.company_website` proves org `sc`
>    (mapped to "Summer Classics" since v3.2) is actually **Gabriella White**
>    (www.GabriellaWhite.com) — the parent LLC that owns the Summer Classics / Summer Classics
>    Contract brands. The real Summer Classics org, `scw` (www.summerclassics.com), had full
>    Postgres data already pulled but was never attached to any roster row. `sc`, `scw`, and
>    `sccon` (Summer Classics Contract) are three separately-billed, simultaneously-active
>    entities — a parent/sibling-brand family, not a duplicate (per `VM-K6`: no native parent
>    key in Postgres, family relationships must never be silently merged). Fixed at the root in
>    `build_v4.py` (see `SHORTNAME_CORRECTIONS`) and the whole pipeline re-run — not hand-patched.
> 3. **Round 3 (independent audit):** Re-derived the Round 2 identity claim from live Postgres
>    and public sources — **confirmed**. Also found that Round 1/2 matched shortnames for
>    `leg`/`soi`/`tel`/`ilc`/`abol` but never backfilled their enrichment dicts, so those five
>    rows had blank product/customer/order/iPad/category fields. Backfilled from live Postgres
>    and regenerated; headline counts unchanged (109 / 33 / 38 / 24 / 14). Brand-Building §3
>    medians shifted slightly (AOV / product count / categories) because those rows now
>    contribute real values instead of empties.
>
> **Net effect: the roster is 109, and the segment counts (33 / 38 / 24 / 14) match what Kjael
> originally stamped** — the as-stamped totals were right all along; what was wrong was which
> *org* two of those 109 rows pointed at, plus incomplete enrichment on five Round-1 matches.
> `sc`'s data (17,510 products, 92,470 customers, $122.7M invoiced) now correctly represents
> Gabriella White, and a new row for the real Summer Classics (6,941 products, 8,463 customers,
> $166.1M invoiced) now exists. This also caught and fixed a latent bug in the original analysis:
> several "median" figures in §3 were actually single raw org values mislabeled as medians
> (e.g. "median AOV $5,295" was literally org `ihw`'s AOV). `build_v4.py` now computes every
> figure in §3/§6 programmatically via `statistics.median()` — see `compute_enrichment_medians()`.
>
> The exact document Kjael reviewed and stamped is preserved unchanged at
> [`../v4/v4.0_archive/SuperCat_Client_Segmentation_v4.0.md`](../v4/v4.0_archive/SuperCat_Client_Segmentation_v4.0.md)
> — go there for the as-stamped historical record (its headline counts, 109/33/38/24/14, turn out
> to match this corrected copy; only the underlying per-org data for a few rows and the §3
> medians differ).  
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
| `products` (Postgres) | Catalog size, avg/min/max price, category/collection/tradename diversity | 95 orgs with active products |
| `customers` (Postgres) | Customer count, territory diversity, price-code complexity | 96 orgs |
| `orders` (Postgres) | Order count, AOV, recency, total GMV | 99 orgs with submitted orders |
| `portal_invoices` (Postgres) | Invoiced revenue (commercial truth per provenance_spine) | 38 orgs with invoice feeds |
| `org_users` (Postgres) | iPad-active rep count | 99 orgs |
| `distribution_centers` (Postgres) | Fulfillment footprint | 17 orgs (sparse) |
| v3.2 Comprehensive CSV | Prior segment assignment, catalog scrub median, realized mean, best price | All 109 |

### 1.2 The Three Classification Axes (from Kjael)

1. **How they sell** — the primary segmenting axis (selling motion)
2. **What they sell** — product vertical (furniture, lighting, outdoor, accessories, decor, rugs, textiles)
3. **Who they sell to** — buyer type (trade/designers, wholesale/dealers, mixed, retail, contract)

### 1.3 Approach

- Used v3.2 validated segments as the **null hypothesis** (Kylor-stamped)
- Pulled every available dimension from Postgres for all 109 orgs on the v3.2 seed list (5 initially unmatched on shortname, all 5 resolved to real orgs — see the header note and §9)
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
- Sabine Pools → Brand-Building (outdoor/pool retailer, dealer model)
- Kaleen Rugs → Volume Distribution (commodity rug distribution)
- Tomlinson Companies → Brand-Building (furniture)
- America's Backyards → Brand-Building (outdoor)
- Ideal Living → Brand-Building (furniture)

The other 3 of the 8 moves were all v3.2 "unknown"/`??` accounts resolved to real, active orgs by
direct Postgres lookup: Legrand US and Silver One → Brand-Building, and **Gabriella White →
Brand-Building** (org `sc`; the parent LLC that owns the Summer Classics brands — see the header
note). Gabriella White is not a duplicate; it's a distinct, separately-billed entity from Summer
Classics (`scw`) and Summer Classics Contract (`sccon`), both also present on the roster in
Brand-Building. See [`../v4/v4.0_archive/unmatched_accounts_validation_2026-07-09.md`](../v4/v4.0_archive/unmatched_accounts_validation_2026-07-09.md).

### 2.2 Price as a Continuous Dimension (not a boundary)

v3.2 found that price doesn't create clean segment boundaries. v4.0 **confirms this** with the full enrichment:

| Segment | Price Range (best available) | Mean | Observation |
|---------|------------------------------|------|-------------|
| Specification | $14 – $14,600 | $1,724 | Enormous range; includes parts-only orgs (Schonbek $14) and ultra-luxury |
| Brand-Building | $60 – $1,070 | $413 | Overlaps heavily with Specification at the low end |
| Multi-Channel | $55 – $449 | $134 | Tight band; most homogeneous on price |
| Volume | $3 – $33 | $12 | Only boundary that is cleanly numeric |

**The Luxury/Premium boundary is selling motion (specification vs. brand-building), NOT price.** Multiple Specification orgs have lower average prices than several Brand-Building companies (e.g. Summer Classics Contract at $537) — designer-specification motion, not price point, is what separates the two segments.

**The only clean numeric boundary is Mid-Market/Volume** — below ~$50 avg price, everything is volume distribution.

### 2.3 Product Vertical (What They Sell) — a Dimension, Not a Segment

| Vertical | Count | Segments Represented |
|----------|-------|---------------------|
| Lighting | 44 | All 4 segments |
| Furniture | 33 | Specification, Brand-Building, Multi-Channel |
| Accessories/Giftware | 14 | Brand-Building, Multi-Channel, Volume |
| Decor/Art | 9 | Specification, Brand-Building, Multi-Channel |
| Outdoor | 7 | Brand-Building only (Gabriella White, Summer Classics, Summer Classics Contract, Sabine Pools, America's Backyards, + 2 more) |
| Rugs | 1 | Volume |
| Textiles | 1 | Multi-Channel |

**Key finding:** Product type does NOT segment cleanly. Lighting companies span all four segments (from Visual Comfort at Specification to Bulbrite at Volume). Furniture similarly spans the full range.

### 2.4 Buyer Type (Who They Sell To) — Aligns with Selling Motion

| Buyer Type | Count | Primary Segment |
|-----------|-------|-----------------|
| Trade (Designers/Architects) | 33 | Specification (100% alignment) |
| Wholesale (Dealers) | 27 | Brand-Building |
| Wholesale (Dealers/Retailers) | 20 | Multi-Channel |
| Wholesale (Retailers) | 14 | Volume |
| Mixed (Trade + Retail) | 8 | Brand-Building (incl. Summer Classics) + Multi-Channel |
| Wholesale (Broad Dealer Network) | 7 | Brand-Building (large-scale) |

**Buyer type is almost perfectly predicted by selling motion.** This confirms that the selling-motion axis (how they sell) is the fundamental classifier — who they sell to follows naturally.

---

## 3. Enrichment Dimensions (new data from Postgres)

*(All figures below are computed by `build_v4.py`'s `compute_enrichment_medians()` via
`statistics.median()` directly on the CSV — not hand-picked. This fixes a bug in the original
pass, where several "median" figures were actually single raw org values.)*

### 3.1 Platform Activity & Scale

| Metric | Specification (33) | Brand-Building (38) | Multi-Channel (24) | Volume (14) |
|--------|-------------------|--------------------|--------------------|-------------|
| Median iPad-active reps | 46 | 79 | 56 | 42 |
| Median order count | 1,283 | 1,584 | 210 | 5,759 |
| Median AOV | $4,501 | $3,864 | $2,549 | $1,266 |
| Orgs with invoice feed | 12 (36%) | 16 (42%) | 7 (29%) | 3 (21%) |
| Median invoiced revenue (where present) | $39.6M | $63.9M | $87.5M | $61.2M |

### 3.2 Catalog Complexity

| Metric | Specification | Brand-Building | Multi-Channel | Volume |
|--------|--------------|----------------|---------------|--------|
| Median product count | 2,344 | 1,962 | 2,425 | 4,498 |
| Median distinct categories | 35 | 36 | 28 | 44 |
| Median distinct collections | 46 | 152 | 381 | 30 |

Multi-Channel orgs run the most collection-heavy catalogs (median 381 collections) — consistent with broad, aesthetic-driven multi-line assortments. Volume has the fewest collections relative to its category count — it organizes by functional type, not aesthetic/design collections.

### 3.3 Customer Structure

| Metric | Specification | Brand-Building | Multi-Channel | Volume |
|--------|--------------|----------------|---------------|--------|
| Median customer count | 4,418 | 2,567 | 1,544 | 1,695 |
| Median territory count | 26 | 41 | 29 | 39 |
| Median price codes | 4 | 4 | 3 | 1 |

**Interesting:** Brand-Building has the most territory coverage (median 41) despite fewer customers than Specification — broad dealer networks spread thin geographically. Volume has the simplest pricing (median 1 code = flat pricing) despite the highest order volume of any segment.

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

**Price range:** $60–$1,070

**Exemplars:** Braxton Culler, Summer Classics, Summer Classics Contract, Gabriella White, Wildwood/Chelsea House, Furniture Classics, Jamie Young Company, Hubbardton Forge

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

### Specification (30 orgs with catalog price data) — price distribution
```
$14 ─── $624 ─── $798 ─── $1,330 ─── $14,600
         Q1       Median     Q3
```

### Brand-Building (32 orgs with catalog price data) — price distribution
```
$60 ─── $216 ─── $300 ─── $579 ─── $1,070
         Q1       Median    Q3
```

### Multi-Channel (22 orgs with catalog price data) — price distribution
```
$55 ─── $76 ─── $99 ─── $137 ─── $449
        Q1      Median    Q3
```

### Volume (14 orgs with catalog price data) — price distribution
```
$3 ─── $7 ─── $8 ─── $18 ─── $33
       Q1     Median   Q3
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
- **109 accounts is the universe.**
- **5 accounts originally had `??` shortnames** and no Postgres match in the build script's join. Direct name-based lookup against `organizations.company_website`/`company_email` resolved all 5 to real, active orgs: Legrand US → `leg`, Silver One → `soi`, Tomlinson Companies → `tel`, Ideal Living → `ilc`, and Gabriella White → `sc`. The `sc`↔`scw` mapping had a deeper root-cause bug: `sc` had been mapped to "Summer Classics" since v3.2, but it's actually Gabriella White (the parent LLC); the real Summer Classics org (`scw`) was previously missing from the roster entirely. Both are now correctly represented as separate rows, alongside the already-present Summer Classics Contract (`sccon`) — three distinct, simultaneously-active billing entities in one corporate family. See [`../v4/v4.0_archive/unmatched_accounts_validation_2026-07-09.md`](../v4/v4.0_archive/unmatched_accounts_validation_2026-07-09.md).
- **14 orgs have no products in Postgres** (portal-only orgs with invoice/order data but no catalog). Classified by order behavior and company identity.
- **MCP SQL limitations:** `PERCENTILE_CONT`, `STDDEV`, `ROUND`, `::numeric` casts were blocked. All statistical analysis done in Python post-retrieval, using `statistics.median()` for every median in §3/§6 (not hand-picked values).
- **The kll (Kuzco) invoice figure ($437B) is a data anomaly** — excluded from revenue analysis.

---

## 10. Output Files

| File | Location |
|------|----------|
| This document (current, corrected — 3 rounds) | `Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.md` |
| Master CSV (109 rows, corrected, all dimensions) | `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` |
| Stamp-ready HTML (regenerated from CSV + this MD) | `Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.html` |
| HTML builder | `Customer Segmentation/current/build_segmentation_html.py` |
| As-stamped historical record (109 rows, 2 rows' underlying data later corrected) | `Customer Segmentation/v4/v4.0_archive/` |
| Unmatched-account validation (all correction rounds) | `Customer Segmentation/v4/v4.0_archive/unmatched_accounts_validation_2026-07-09.md` |
| Build script (reproducible — identity fixes + median calc fixed at the root) | `Customer Segmentation/v4/v4.0_archive/build_v4.py` |

---

## 11. Next Steps

1. ~~Dissolve the Specialty segment in all downstream references~~ — done, no downstream references found.
2. ~~Propagate the three-axis classification to the Insightful Product customer intelligence layer~~ — done (2026-07-09); see the scope note in `Insightful Product 4.0/foundation/segmentation_derivation.md` (that pipeline governs a different, frozen mechanism — per-client customer segmentation — so propagation there is a cross-reference, not a rewire).
3. **Use product vertical and median price as continuous dimensions** in ICP/product-market-fit work — done (2026-07-09); see the new section in `SuperCat 4.0/foundation/02_who_we_serve.md`.
4. ~~Validate the 5 unmatched (??) accounts with Kjael~~ — done (2026-07-09) by direct Postgres lookup; see `unmatched_accounts_validation_2026-07-09.md`. Two residual flags left for human confirmation: (a) a second, dormant `legrand` org (`lna`, last order 2015) that should not be conflated with the active `leg` account; (b) the Gabriella White / Summer Classics / Summer Classics Contract family is now correctly split into 3 rows, but no one has re-examined whether each sibling's *individual* qualitative profile still supports Brand-Building, vs. treating one or more as Multi-Channel given the DTC + trade-portal + retail-showroom model described for the parent brand.
5. **Consider adding a "platform maturity" dimension** (not a segment) based on iPad activity, invoice feed presence, and catalog completeness — not yet done.
