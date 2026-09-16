# Validation: §4 Product & Inventory Intelligence

| Check | Status | Evidence |
|-------|--------|----------|
| **A. Subsection Completeness** | | |
| Subsection 1: Top Sellers Out of Stock | PASS | `<div class="subsection-title">Top Sellers Out of Stock</div>` found (line 13); gate met (HAS_SALES_DATA=true AND HAS_INVENTORY=true) |
| Subsection 2: New Introduction Performance | PASS | `<div class="subsection-title">New Introduction Performance</div>` found (line 215); gate met (HAS_SALES_DATA=true) |
| Subsection 3: Product Velocity Trend | PASS | `<div class="subsection-title">Product Velocity Trend</div>` found (line 238); gate met (HAS_PORTAL_ORDERS=true) |
| Subsection 4: Catalog Completeness | PASS | `<div class="subsection-title">Catalog Completeness</div>` found (line 369); gate always-on |
| Subsection 5: What's Selling | PASS | `<div class="subsection-title">What&rsquo;s Selling</div>` found (line 397); gate met (HAS_SALES_DATA=true) |
| section-contents middot list | PASS | Lists all 5 rendered subsections separated by ` · `: "Top Sellers Out of Stock · New Introduction Performance · Product Velocity Trend · Catalog Completeness · What's Selling" |
| **B. Fragment Contract** | | |
| Opens with correct `<details>` | PASS | `<details class="section-collapse" id="product">` — id matches §4=product lock |
| Closes with `</details>`, nothing after | PASS | Line 897 is `</details>`, final line of file |
| No `<html>/<head>/<body>/<style>` | PASS | grep returns zero matches |
| No HTML comments | PASS | grep for `<!--` returns zero matches |
| `section-sub` data-dense | PASS | "3,622 visible products at 99.9% completeness · 20 top sellers out of stock ($1.0M all-time all-channel sales) · Table Lamps leads at $6.8M" — specific stats, not generic |
| `expand-hint` span | PASS | `<span class="expand-hint">&#9662; Click to expand</span>` found (line 8) |
| Inner `<section class="section">` | PASS | `<section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">` found (line 10) |
| **C. Subsection Structure** | | |
| subsection-title as first child (all 5) | PASS | Each `<div class="subsection">` immediately contains `<div class="subsection-title">` — verified for all 5 subsections |
| what-this-means closes each (all 5) | PASS | `<div class="what-this-means">` found at lines 209, 232, 363, 391, 891 — one per subsection |
| **D. Forbidden Phrases** | | |
| "health score" / "health scores" | PASS | zero matches (case-insensitive) |
| "portal orders" / "portal ordering" as buyer activity | PASS | zero matches |
| "net-new customers" | PASS | zero matches |
| "ERP" | PASS | zero matches — fragment uses "all-channel" framing throughout |
| "Mixpanel" | PASS | zero matches |
| "Clicky" | PASS | zero matches |
| "Platform-Embedded" / "Commerce-Active" / "Catalog-Focused" | PASS | zero matches |
| Internal identifiers (VM codes, query IDs, table/column names, org IDs) | PASS | zero matches |
| "bounce_rate" | PASS | zero matches |
| `order_source = 'ipad'` or similar code literals | PASS | zero matches |
| "benchmark_confidence" / "peer_group_level" / "peer_group_n" | PASS | zero matches |
| **D. Hard Rules** | | |
| HR7: time qualifiers on metrics | PASS | "Current inventory snapshot", "All-time all-channel", "trailing 6 months", "recent 90-day window (February–April 2026)", "prior 90-day window (November 2025–January 2026)", "Current snapshot", "all-time all-channel sales" — all metrics qualified |
| HR8: projections tagged [HYPOTHETICAL] | PASS | No projections present in fragment — N/A |
| HR9: extrapolations tagged [ESTIMATED] | PASS | No extrapolations present in fragment — N/A |
| HR2: VM-27/28/29/36/48 not surfaced | PASS | zero matches for any VM codes |
| VM-38b not surfaced | PASS | Fragment uses Q-38a velocity data only; no fabricated invoice_date-based velocity |
| HR4: portal_orders not framed as buyer self-service | PASS | "portal_orders" / "portal ordering" not referenced |
| **E. Section-Specific Rendering** | | |
| Top Sellers OOS: table with product detail | PASS | Table with Item Code, Description, Category, All-Time Sales, Backordered, Next Receipt — meaningful detail for OOS items |
| New Intro Performance: sparse data handled | PASS | Callout explains only 1 new introduction found; metric cards show 1 item / $95; matches Q-42 gate_flags note |
| Velocity Trend: exact 6-column table | **FAIL** | Guide specifies exactly 6 columns: Direction, Item Code, Category, Recent 90d, Prior 90d, Velocity Change. Fragment renders 7 columns: Direction, Item Code, **Description** (extra), **Collection** (should be Category), Recent 90d, Prior 90d, Velocity Change. Two deviations: (1) extra "Description" column not in spec, (2) "Collection" instead of "Category" |
| Velocity Trend: top 3–5 accelerating + declining | PASS | 5 accelerating and 5 declining items shown — within spec |
| Velocity Trend: prose note on replenishment/clearance | PASS | Closing prose paragraph covers replenishment for accelerating items and clearance/repositioning for declining items |
| Velocity Trend: fee items excluded note | PASS | "Fee items, freight charges, and non-product line items are excluded" stated in opening prose |
| Catalog Completeness: exact 5-column table | PASS | Visibility, Products, Missing Images, Missing Price, Complete % — matches spec exactly |
| Catalog Completeness: callout below 90% or 50+ assets | PASS | 99.9% completeness and only 4 missing images — no callout required, none rendered |
| What's Selling: single subsection (not split) | PASS | One `<div class="subsection">` with title "What's Selling" — not split into category/collection subsections |
| What's Selling: two progressive-disclosure tables | PASS | Two `<details>` blocks: "Category Breakdown" and "Collection Breakdown" |
| What's Selling: Category table columns | **FAIL** | Guide specifies: Category, Orders, GMV, Customers, Value/Order. Fragment has: Category, **Catalog Items** (not in spec), **Units Sold** (instead of Orders), **All-Time Sales** (instead of GMV), **Sales/Item** (instead of Value/Order). Missing "Customers" column entirely. 4 of 5 column names deviate. |
| What's Selling: Collection table columns | **FAIL** | Guide specifies: Collection, Items, Orders, GMV. Fragment has: Collection, **Catalog Items** (instead of Items), **Units Sold** (instead of Orders), **All-Time Sales** (instead of GMV). 3 of 4 column names deviate. |
| What's Selling: callout on dominant collection + low-activity categories | PASS | Callout identifies Chelsea House Misc at $9.1M / 36% share and lists Sofas & Settees, Floor Mirrors, Screens, Lighting as low-activity categories |
| **F. Highlight File** | | |
| File exists | PASS | `cache/section_04_highlights.md` present |
| 2–4 highlight candidates | PASS | 4 candidates — within range |
| Each: bold headline + context + section link | PASS | All 4 have `**bold headline**`, data-backed context sentence, and `[→ §product]` link |
| Priority action candidate format | PASS | 1 candidate with HIGH urgency, quantified impact, [HYPOTHETICAL] tag, section link |

**VERDICT: FAIL**

## Failed Checks (3)

### FAIL 1 — Velocity Trend table columns (§E)
- **Guide requirement**: "Render as a table with these exact columns: Direction | Item Code | Category | Recent 90d | Prior 90d | Velocity Change" (6 columns)
- **Fragment renders**: Direction | Item Code | Description | Collection | Recent 90d | Prior 90d | Velocity Change (7 columns)
- **Issues**: (a) Extra "Description" column not in the specification; (b) "Collection" used instead of "Category"

### FAIL 2 — What's Selling Category table columns (§E)
- **Guide requirement**: Category | Orders | GMV | Customers | Value/Order
- **Fragment renders**: Category | Catalog Items | Units Sold | All-Time Sales | Sales/Item
- **Issues**: (a) "Catalog Items" is not a specified column; (b) "Units Sold" ≠ "Orders" (units vs transactions); (c) "All-Time Sales" used instead of "GMV"; (d) "Sales/Item" ≠ "Value/Order" (revenue-per-catalog-item vs revenue-per-order); (e) "Customers" column missing entirely

### FAIL 3 — What's Selling Collection table columns (§E)
- **Guide requirement**: Collection | Items | Orders | GMV
- **Fragment renders**: Collection | Catalog Items | Units Sold | All-Time Sales
- **Issues**: (a) "Catalog Items" instead of "Items"; (b) "Units Sold" instead of "Orders"; (c) "All-Time Sales" instead of "GMV"
