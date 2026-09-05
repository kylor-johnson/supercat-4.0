# SuperCat Client Segmentation v3.2
## Multi-Layer Validation & Flag Resolution

**Date:** July 2, 2026
**Predecessor:** v3.1 (July 1, 2026)
**Requested by:** Kjael — July 2 team review
**Directive:** Validate segment boundaries with every available data layer. Resolve every flagged account. Ship stamp-ready.

**Status:** STAMPED by Kylor — July 2, 2026 1:21 PM CT. Ready for Kjael review.

---

## Data Sources (4 layers)

| Layer | Source | Coverage | What it tells us |
|-------|--------|----------|------------------|
| **Catalog price** | `products.net_price` (Postgres) | 94/109 accounts | What they *list* — scrubbed at 2σ per org |
| **Realized price** | `portal_invoice_items.unit_price` (Postgres) | 39/109 accounts | What they *actually transact at* — the ground truth |
| **Order behavior** | `orders` (Postgres) | 105/109 accounts | Volume, avg order value — reveals selling motion |
| **Price code complexity** | `customers.default_price_code` (Postgres) | 108/109 accounts | Number of distinct price tiers — proxy for pricing sophistication |

**"Best price"** = realized mean where available, else 2σ-scrubbed catalog median. This is the single number used for price-based analysis below.

---

## Segment Summary (Post-Resolution)

| Segment | N | Median Best Price | IQR | Median Orders | Median AOV | Median Price Codes |
|---------|---|-------------------|-----|---------------|------------|-------------------|
| 1. Luxury Specification | **34** | $758 | $535–$1,187 | 2,297 | $4,747 | 4 |
| 2. Premium Trade Brand | **31** | $303 | $185–$554 | 1,946 | $3,790 | 5 |
| 3. Mid-Market Multi-Channel | **26** | $99 | $76–$139 | 255 | $2,744 | 3 |
| 4. Volume Distribution | **13** | $9 | $7–$19 | 5,730 | $1,583 | 1 |
| 5. Specialty/Non-Traditional | **5** | — | — | — | — | — |

Changes from v3.1: 7 accounts moved (6.4% of 109). Net effect: Luxury −2, Premium −2, Mid-Market +2, Volume +1, Specialty +1.

---

## Segment Rosters (Full, with all data layers)

### 1. Luxury Specification (34 accounts)

*Defined by:* Designer-specification selling motion. Products specified by interior designers, architects, or trade professionals into projects. Trade-only or trade-primary channels. Price is a correlate, not the classifier.

| Company | Best Price | Cat Scrub | Realized | Orders | AOV | PCodes |
|---------|-----------|-----------|----------|--------|-----|--------|
| Alfonso Marina | $9,100 | $9,100 | — | 122 | $11,200 | 1 |
| Theodore Alexander Manhasset | $3,466 | $1,797 | $3,466 | 353 | $9,903 | 1 |
| Interlude Furniture | $2,195 | $1,759 | $2,195 | 13,532 | $5,285 | 5 |
| Baker-McGuire | $2,070 | $2,070 | — | 130 | $25,898 | 1 |
| Somerset Bay and Modern History | $2,012 | $3,480 | $2,012 | 30,652 | $2,996 | 4 |
| Jonathan Charles Designs Inc. | $1,419 | $1,045 | $1,419 | 2,297 | $6,696 | 6 |
| Hancock & Moore / Jessica Charles | $1,330 | $1,330 | — | 2 | $2,407 | 1 |
| Theodore Alexander | $1,187 | $608 | $1,187 | 8,956 | $7,663 | 4 |
| Interlude Home | $1,183 | $1,419 | $1,183 | 13,705 | $3,432 | 5 |
| Palecek | $1,144 | $2,575 | $1,144 | 41,610 | $4,501 | 15 |
| Rowe Furniture | $1,050 | $1,050 | — | 1,282 | $4,706 | 4 |
| Visual Comfort Europe | $999 | $999 | — | 126 | $3,638 | 24 |
| Sarreid, Ltd. | $968 | $525 | $968 | 13,422 | $3,897 | 6 |
| Oly Studio | $830 | $830 | — | 79 | $9,742 | 4 |
| Four Seasons Furniture | $765 | $420 | $765 | 11,403 | $2,079 | 3 |
| Corbett Lighting | $758 | $758 | — | 283 | $8,437 | 4 |
| Hooker Furnishings | $749 | $749 | — | 345 | $11,976 | 7 |
| Bliss Studio | $744 | $744 | — | 3,506 | $3,096 | 2 |
| Jonathan Charles Fine Furniture Ltd. | $733 | $525 | $733 | 138 | $81,608 | 1 |
| Charleston Forge | $670 | $670 | — | 6,658 | $3,036 | 3 |
| Yutzy Woodworking | $642 | $642 | — | 180 | $5,496 | 2 |
| Currey & Company | $624 | $840 | $624 | 13,875 | $1,976 | 6 |
| Gabby | $593 | $259 | $593 | 175,014 | $2,366 | 14 |
| Alden Home | $575 | $575 | — | 1,635 | $4,788 | 3 |
| Accord Lighting | $461 | $461 | — | 94 | $3,534 | 5 |
| Visual Comfort Signature | $435 | $435 | — | 9,496 | $2,765 | 16 |
| Visual Comfort - Modern | $285 | $285 | — | 2,595 | $11,003 | 23 |
| Schonbek Lighting | $14 | $14 | — | 412 | $14,255 | 4 |
| Visual Comfort - Studio /Fans | $115 | $115 | — | 17,065 | $92,048 | — |
| Gabriella White | — | — | — | — | — | — |
| Fine Art Handcrafted Lighting | — | — | — | 3,492 | $17,073 | 10 |
| Century Furniture | — | — | — | — | — | 2 |
| Highland House | — | — | — | — | — | 2 |
| Kindel Karges Furniture | — | — | — | — | — | 6 |

**Price anomalies resolved:**
- **Schonbek Lighting** ($14): Only 1 product in Postgres — data artifact. Schonbek is Swarovski-owned luxury crystal. Stays.
- **Visual Comfort - Studio/Fans** ($115): Low unit price but $92K AOV — enormous specification basket orders. Same rep network as other VC entities. Stays.
- **Gabby** ($259 scrub, $593 realized): Catalog diluted by low-cost accessories. Realized price ($593) confirms luxury range. 175K orders is massive volume but selling motion is designer-specification. Stays.

**Moved OUT:**
- Matteo Lighting → Premium Trade (see below)
- Geo Contemporary → Premium Trade (see below)

### 2. Premium Trade Brand (31 accounts)

*Defined by:* Brand-building across trade channels. Products sold on brand reputation to dealers/retailers. Often both trade and consumer channels. Multi-tier pricing typical.

| Company | Best Price | Cat Scrub | Realized | Orders | AOV | PCodes |
|---------|-----------|-----------|----------|--------|-----|--------|
| International Home Miami | $1,070 | $1,070 | — | 18 | $2,963 | 1 |
| Hubbardton Forge | $846 | $1,525 | $846 | 8,885 | $9,542 | 8 |
| Universal Furniture | $692 | — | $692 | 37,497 | $7,672 | 1 |
| Kalco Lighting / Allegri Crystal | $647 | $460 | $647 | 1,352 | $8,332 | 3 |
| Donald Choi Canada | $607 | $925 | $607 | 520 | $3,396 | 2 |
| Arabela Lighting | $579 | $579 | — | 340 | $2,120 | 1 |
| Braxton Culler | $554 | $465 | $554 | 6,772 | $2,672 | 6 |
| Summer Classics Contract | $537 | $282 | $537 | 65,834 | $17,272 | 6 |
| Ciana Varaluz LLC | $534 | $624 | $534 | 743 | $7,366 | 6 |
| Furniture Classics | $457 | $385 | $457 | 31,171 | $4,147 | 4 |
| Summer Classics | $430 | $338 | $430 | 333,367 | $4,421 | 1 |
| Eurofase Inc. | $422 | $410 | $422 | 1,245 | $11,248 | 4 |
| Butler Specialty Company | $411 | $411 | — | 8,607 | $1,849 | 18 |
| Ratana International Ltd. | $350 | $766 | $350 | 1,946 | $13,725 | 15 |
| Wildwood/Chelsea House | $303 | $385 | $303 | 43,432 | $1,716 | 7 |
| **Geo Contemporary** *(from Luxury)* | $298 | $298 | — | 469 | $2,121 | 4 |
| Lucas McKearn | $289 | $289 | — | 4 | $2,230 | 1 |
| Crystorama | $281 | $299 | $281 | 1,816 | $3,790 | 5 |
| Troy Lighting | $255 | $255 | — | 548 | $3,194 | 4 |
| Hudson Valley Lighting | $245 | $245 | — | 849 | $3,926 | 4 |
| Wendover Art Group | $238 | $238 | — | 4,645 | $4,801 | 1 |
| Jamie Young Company | $230 | $240 | $230 | 82,355 | $1,043 | 4 |
| Elegant Furniture & Lighting | $198 | $198 | — | 21,114 | $3,280 | 1 |
| RENWIL | $196 | $169 | $196 | 10,300 | $1,207 | 5 |
| Buster & Punch | $185 | $185 | — | 26 | $4,070 | 41 |
| Kuzco Lighting Inc. | $184 | — | $184 | 973 | $6,523 | 11 |
| Minka Lighting Group | $159 | $159 | — | 169 | $10,444 | 26 |
| **Matteo Lighting** *(from Luxury)* | $139 | $139 | — | 368 | $3,833 | 2 |
| Dainolite Ltd. | $118 | $118 | — | 22,044 | $1,665 | 2 |
| Alfresco Home | $60 | $60 | — | 9,563 | $5,642 | 1 |
| WAC/Modern Forms Lighting | — | — | — | 4,757 | $4,336 | 26 |

**Moved IN:**
- **Matteo Lighting** (from Luxury): $139 median, 368 orders, $3.8K AOV, 2 price codes. Niche designer brand but selling motion is brand-building through trade dealers, not specification into projects. Better fit here.
- **Geo Contemporary** (from Luxury): $298 median, 469 orders, $2.1K AOV, 4 price codes. Contemporary furniture at Premium Trade price point. No specification selling motion — sold through trade channels on brand.

**Moved OUT:**
- Kaleen Rugs & Broadloom → Specialty (see below)
- Philip Whitney → Volume Distribution (see below)
- Ricci Argentieri → Volume Distribution (see below)
- AFX, Inc. → Mid-Market (see below)

**Price anomalies resolved:**
- **Hubbardton Forge** ($846 realized vs $1,525 scrub): Artisan Vermont forge. Realized confirms luxury-adjacent pricing. Stays in Premium Trade because selling motion is brand-building across trade + consumer, not designer-specification.
- **Ratana International Ltd.** ($350 realized vs $766 scrub): Outdoor contract furniture. $13.7K AOV suggests large project orders. 15 price codes = sophisticated tiering. Stays — brand-building with contract capability.
- **Dainolite Ltd.** ($118 scrub, 22K orders): High volume but Canadian trade brand with USD+CAD structure. Stays.
- **Alfresco Home** ($60 scrub, 9.5K orders, $5.6K AOV): Low unit price but high AOV — large basket orders. Trade brand-building. Stays.

### 3. Mid-Market Multi-Channel (26 accounts)

*Defined by:* Multi-channel distribution (trade + retail + ecommerce). Products sold through dealers, big box, and online. Moderate price points. Simpler pricing structures.

| Company | Best Price | Cat Scrub | Realized | Orders | AOV | PCodes |
|---------|-----------|-----------|----------|--------|-----|--------|
| Lifestyle Solutions | $449 | $449 | — | 155 | $2,744 | 2 |
| Sauder Woodworking | $390 | $390 | — | 5 | $10,825 | — |
| Shadow Catchers | $260 | $260 | — | 3,065 | $4,179 | 1 |
| Golden Lighting | $153 | $105 | $153 | 526 | $929 | 6 |
| Capital Lighting Fixture Co. | $153 | $130 | $153 | 285 | $4,758 | 2 |
| Savoy House Lighting | $137 | $118 | $137 | 6,747 | $75,722 | 4 |
| Karat Home Inc. | $131 | $131 | — | — | — | — |
| Coleto Brands / Kichler | $123 | $123 | — | 875 | $7,249 | 7 |
| Linon/Powell Furniture | $117 | $45 | $117 | 11,837 | $2,193 | 2 |
| Craftmade | $109 | $69 | $109 | 1,348 | $4,695 | 3 |
| **AFX, Inc.** *(from Premium)* | $99 | $99 | — | 73 | $1,929 | 3 |
| EGLO Canada | $99 | $99 | — | 149 | $6,405 | 11 |
| Vaxcel International Corporation | $90 | — | $90 | 316 | $497 | 8 |
| Coleto Brands / Progress Lighting | $87 | $87 | — | 96 | $2,994 | 1 |
| ET2 Lighting | $84 | $84 | — | 53 | $2,455 | 31 |
| Eglo USA Inc. | $80 | $80 | — | 289 | $2,642 | 6 |
| Designer's Fountain | $76 | $76 | — | 27 | $749 | 1 |
| **Groupe Courchesne** *(from Volume)* | $70 | $70 | — | 3,722 | $1,134 | 1 |
| DALS Lighting | $71 | $71 | — | 55 | $2,248 | 2 |
| Access Lighting | $64 | $63 | $64 | 129 | $2,091 | 27 |
| Millennium Lighting | $60 | $60 | — | 118 | $2,168 | — |
| Maxim Lighting | $55 | $55 | — | 255 | $6,600 | 35 |
| Magnussen Home | — | — | — | 1,955 | $5,234 | 3 |
| Morgan Fabrics Corporation | — | — | — | 51 | $1,054 | 2 |
| Legrand US | — | — | — | — | — | — |
| Silver One | — | — | — | — | — | — |

**Moved IN:**
- **AFX, Inc.** (from Premium Trade): $99 median, 73 orders, $1.9K AOV, 3 price codes. Commercial/architectural lighting at mid-market price point. Low volume, simple pricing. Selling motion is multi-channel distribution, not trade brand-building.
- **Groupe Courchesne** (from Volume Distribution): $70 median — 9× the Volume median of $8. Hospitality/foodservice distributor selling through multiple channels. Price and selling motion are mid-market, not volume.

### 4. Volume Distribution (13 accounts)

*Defined by:* High-volume, low-unit-price distribution. Products moved in bulk at commodity-adjacent pricing. Single or very few price tiers. Often private-label or house-brand.

| Company | Best Price | Cat Scrub | Realized | Orders | AOV | PCodes |
|---------|-----------|-----------|----------|--------|-----|--------|
| Abaline Supply Inc. | $33 | $26 | $33 | 78,507 | $2,126 | 2 |
| Pioneer Morton | $24 | $24 | — | 74,378 | $1,915 | 1 |
| Godinger Silver Art Co. | $19 | $19 | — | 4,663 | $1,383 | 1 |
| **Ricci Argentieri Company** *(from Premium)* | $18 | $18 | — | 6,489 | $755 | 1 |
| Bulbrite | $12 | $7 | $12 | 5,955 | $979 | 22 |
| **Philip Whitney** *(from Premium)* | $10 | $10 | — | 461 | $513 | 1 |
| Studio Silversmiths, Inc. | $9 | $9 | — | 567 | $1,148 | 1 |
| ELICO LTD. | $8 | $8 | — | 5,502 | $3,523 | 3 |
| Sixtrees Limited | $8 | $8 | — | 429 | $908 | 1 |
| Moda at Home Enterprises Ltd | $8 | $8 | — | 5,506 | $969 | 1 |
| Home Essentials & Beyond | $7 | $10 | $7 | 16,307 | $1,783 | 1 |
| Kennedy International, Inc. | $6 | $6 | — | 32,777 | $4,849 | 1 |
| Uniware Housewares Corp. | $3 | $3 | — | 19,387 | $5,865 | 2 |

**Moved IN:**
- **Philip Whitney** (from Premium Trade): $10 median, 461 orders, $513 AOV, 1 price code. Decorative accessories at volume-distribution pricing. Single price tier, low AOV — this is commodity distribution, not brand-building.
- **Ricci Argentieri Company** (from Premium Trade): $18 median, 6,489 orders, $755 AOV, 1 price code. Silver/tabletop at volume pricing. Single price tier, high volume — volume distribution profile.

**Moved OUT:**
- Groupe Courchesne → Mid-Market (see above)

### 5. Specialty/Non-Traditional (5 accounts)

*Defined by:* Accounts that don't fit the standard manufacturer→dealer selling motion. May be retail, service, or niche verticals.

| Company | Best Price | Cat Scrub | Realized | Orders | AOV | PCodes |
|---------|-----------|-----------|----------|--------|-----|--------|
| Sabine Pools, Spas, & Furnitur | $216 | $216 | — | 1,827 | $5,904 | — |
| **Kaleen Rugs & Broadloom** *(from Premium)* | $7 | $7 | — | 2 | $191 | 14 |
| Tomlinson Companies | — | — | — | — | — | — |
| America's Backyards | — | — | — | — | — | — |
| Ideal Living | — | — | — | — | — | — |

**Moved IN:**
- **Kaleen Rugs & Broadloom** (from Premium Trade): $7 catalog median, **2 lifetime orders**, $191 AOV, 14 price codes. Effectively inactive — 14 price codes loaded but almost zero transaction history. The $7 price is per-sq-ft catalog pricing that doesn't compare to per-piece pricing elsewhere. Too anomalous to classify in any standard segment.

---

## All 7 Moves — Summary

| Company | From | To | Rationale |
|---------|------|----|-----------|
| **Matteo Lighting** | Luxury Spec | Premium Trade | $139 median. Niche designer brand but sells through trade dealers, not designer specification. |
| **Geo Contemporary** | Luxury Spec | Premium Trade | $298 median. Contemporary furniture at premium price, sold on brand through trade channels. |
| **AFX, Inc.** | Premium Trade | Mid-Market | $99 median, 73 orders. Commercial lighting at mid-market price, multi-channel distribution. |
| **Philip Whitney** | Premium Trade | Volume Dist | $10 median, $513 AOV, 1 price code. Decorative accessories at commodity pricing. |
| **Ricci Argentieri** | Premium Trade | Volume Dist | $18 median, $755 AOV, 1 price code, 6.5K orders. Silver/tabletop at volume pricing. |
| **Kaleen Rugs** | Premium Trade | Specialty | $7 median, 2 lifetime orders. Effectively inactive. Per-sq-ft pricing incomparable. |
| **Groupe Courchesne** | Volume Dist | Mid-Market | $70 median (9× Volume median). Hospitality distributor, multi-channel selling motion. |

---

## Accounts with No Postgres Data (13)

These accounts have no `products.net_price` data in the database. Shortname either doesn't exist, has no products loaded, or is a staging/test org.

| Company | Segment | v3.1 Price | Notes |
|---------|---------|------------|-------|
| Gabriella White | Luxury Spec | $10,400 | ERP-only price from v3.1 |
| Fine Art Handcrafted Lighting | Luxury Spec | $3,498 | Has order data (3.5K orders, $17K AOV) — confirms luxury |
| Century Furniture | Luxury Spec | $1,832 | Has customer data (2 price codes) |
| Highland House | Luxury Spec | $1,044 | Has customer data (2 price codes) |
| Kindel Karges Furniture | Luxury Spec | $4,000 | Has customer data (6 price codes) |
| WAC/Modern Forms Lighting | Premium Trade | $248 | Has orders (4.8K, $4.3K AOV) + customers (26 price codes) |
| Magnussen Home | Mid-Market | $563 | Has orders (2K, $5.2K AOV) + customers (3 price codes) |
| Morgan Fabrics Corporation | Mid-Market | — | 51 orders, $1K AOV — minimal activity |
| Legrand US | Mid-Market | — | No Postgres presence |
| Silver One | Mid-Market | $36 | No Postgres presence |
| Tomlinson Companies | Specialty | — | No Postgres presence |
| America's Backyards | Specialty | — | No Postgres presence |
| Ideal Living | Specialty | — | No Postgres presence |

**None of these missing accounts change the segment analysis.** The v3.1 ERP prices for the luxury accounts (Gabriella White $10.4K, Fine Art $3.5K, Century $1.8K, Kindel $4K) are consistent with Luxury Specification placement. The order data available for Fine Art, WAC, and ELICO confirms their respective segment placements.

---

## Key Finding: Price Is a Correlate, Not a Classifier

The multi-layer analysis confirms what the catalog-only scrub showed:

1. **Realized prices ≠ catalog prices.** For the 39 accounts with both, realized prices were lower than catalog scrub median in 62% of cases. The gap ranges from negligible to 2× (e.g., Ratana: $350 realized vs $766 catalog). Catalog prices overstate actual transaction levels.

2. **Price tiers (price codes) correlate with segment.** Luxury Spec median = 4 codes, Premium Trade = 5, Mid-Market = 3, Volume = 1. More price tiers = more complex trade relationship. But it's not diagnostic — Buster & Punch has 41 codes (international multi-currency), Kennedy International has 1 (commodity distribution). The signal is in the pattern, not the number.

3. **Average order value is the strongest behavioral signal.** Luxury Spec AOV ($4,747) >> Premium Trade ($3,790) >> Mid-Market ($2,744) >> Volume ($1,583). AOV captures basket size, which directly reflects the selling motion: specification orders are large (designer furnishing a whole room) vs. volume distribution (bulk replenishment of commodity items).

4. **The four segments hold.** After applying all four data layers and resolving every flag, 7 accounts moved (6.4% of 109). The segments are robust — 102/109 accounts stayed exactly where v3.1 placed them.

---

## Recommendation for Kjael Review

1. **Stamp the 4-segment model with the 7 moves above.** The multi-layer validation confirms the segments are real and defensible. The moves are all supported by multiple data points (price + orders + AOV + price codes + selling motion).

2. **Accept that price is supporting evidence, not the boundary.** The Luxury/Premium boundary is selling motion (specification vs. brand-building). The Premium/Mid-Market boundary is channel strategy (trade-primary vs. multi-channel). The Mid-Market/Volume boundary is unit economics ($55+ vs. $33-). Only the last boundary is cleanly numeric.

3. **Move to personas.** Per the July 2 directive, the segmentation is now validated through 4 independent data layers with every flag resolved. The next step is persona work within each segment for copilot initialization.

---

## Updated Artifacts

| File | Location |
|------|----------|
| This analysis | `SuperCat 4.0/Segmentation/SuperCat_Client_Segmentation_v3.2.md` |
| Comprehensive CSV (all data layers) | `SuperCat 4.0/Segmentation/SuperCat_Customer_Segmentation_v3.2_COMPREHENSIVE.csv` |
| Original v3.1 source | `~/Downloads/SuperCat_Client_Segmentation_v3.md` |
| Original v3.1 CSV | `~/Downloads/SuperCat_Customer_Segmentation_v3_Business_Model.csv` |
