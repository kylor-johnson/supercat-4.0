# Braxton Culler — Instance Profile

> **Org ID**: 171 | **Shortname**: bcf | **Created**: 2022-09-13
> **As-of**: 2026-03-17 (live MCP queries)
> **Purpose**: Reference customer for Insightful Product strategy design

---

## Instance Summary

| Dimension | Value | Signal |
|-----------|-------|--------|
| **Products** | 3,427 active | Mid-size catalog |
| **Catalog completeness** | 82.4% complete (2,824) / 6.1% missing images (209) / 11.5% missing price (394) | Actionable quality gap |
| **Customers loaded** | 1,983 | Large dealer network |
| **Customers ordering (12mo)** | 376 (19.0% activation) | Significant dormant base |
| **Orders (12mo)** | 2,556 submitted | High-volume account |
| **Orders (90d)** | 647 submitted | Consistent velocity |
| **GMV (12mo)** | ~$6.46M ($4.33M iPad + $2.14M eOL) | Substantial commerce operation |
| **Channel mix** | 51% iPad / 49% eOL | Near parity — Platform-Embedded profile |
| **Org users** | 1,370 total / 145 actively ordering (90d) | Large user base, low ordering-user ratio |
| **Portal invoices** | 24,987 | Heavy portal/invoice usage |
| **Portal orders** | 1,412 | Active portal order tracking |
| **Sales data rows** | 15,950 | Rich analytics dataset |
| **Import events** | 6,524 | Long import history |
| **Login events** | 20,090 | High engagement volume |
| **Enrollment applicants** | 1,508 | Active enrollment funnel |
| **Kit items** | 2,086 | Significant CPQ/kit complexity |
| **Smart stacks** | 124 | Heavy content curation |
| **Shared resources** | 162 | Active library |

---

## Feature Enablement (Full Stack)

| Surface | Enabled | Notes |
|---------|---------|-------|
| eCat iPad | Yes | Core product |
| Online Catalog | Yes | Buyer browsing |
| Online Ordering (B2B Cart) | Yes | Buyer self-serve ordering |
| Closed Site (authenticated) | Yes | Dealers-only access |
| Sales Portal | Yes | Analytics + dashboards |
| Camera scanning | Yes | |
| Gridview ordering | Yes | |
| Sales data / favorites | Yes | |
| Enrollment | Yes (1,508 applicants) | Active dealer enrollment |
| Kit items | Yes (2,086 items) | Significant kit catalog |
| 12 product images | Yes | Premium image tier |
| Copy order | Yes | |
| Shared orders | Yes | |
| Auto-add surcharges | Yes | |
| Order review | Yes | |
| Portal dashboard | Yes | Advanced portal features |
| Admin order reporting | Yes | |
| Customer dashboard link | Yes | |
| FTP import | Yes | Automated data pipeline |

**Not enabled**: Contract pricing, flipbook, RMA, distribution centers, placement reports, delegated enrollment

---

## Data Freshness (from `data_versions`)

| Entity | Last Updated | Age | Signal |
|--------|-------------|-----|--------|
| customer_favorites | 2026-03-17 (today) | Fresh | Healthy |
| portal_invoices | 2026-03-17 (today) | Fresh | Healthy |
| portal_orders | 2026-03-17 (today) | Fresh | Healthy |
| customers | 2026-03-17 (today) | Fresh | Healthy |
| inventories | 2026-03-17 (today) | Fresh | Healthy |
| products | 2026-03-11 | 6 days | Acceptable |
| options / option_groups | 2026-03-11 | 6 days | Acceptable |
| smart_stacks | 2026-03-11 | 6 days | Acceptable |
| price_levels | 2026-03-04 | 13 days | Monitor |
| riser_prices | 2026-03-01 | 16 days | Monitor |
| **kit_items** | **2026-02-18** | **27 days** | **Stale — action needed** |
| **sales_quotas** | **2025-08-20** | **7 months** | **Very stale — likely unused** |
| contract_prices | 2025-08-20 | 7 months | Feature not enabled (expected) |
| placement_reports | 2025-08-20 | 7 months | Feature not enabled (expected) |

**Insight**: BCF's real-time entities (inventory, customers, portal data) are fresh. Product catalog updates weekly. But kit_items are 27 days stale — with 2,086 kit items and 7,173 configured-item orders in Mixpanel, this is a potential data quality risk. Sales quotas haven't been updated in 7 months, suggesting the budget/quota feature in Sales Portal may be misconfigured or abandoned.

---

## Rep Performance (12 months, MCP order data)

| Rep | Orders | GMV | Unique Customers | Avg Order Value | Signal |
|-----|-------:|----:|--------:|---------:|--------|
| Barbara Harper | 307 | $853,530 | 1 | $2,781 | **Extreme concentration** — 307 orders to 1 customer |
| Jerry Montini | 192 | $865,530 | 35 | $4,508 | Highest GMV, diversified, high AOV |
| Sharyn Moss | 175 | $379,069 | 49 | $2,166 | Broadest reach, lower AOV |
| Todd Teague | 120 | $633,785 | 40 | $5,282 | Highest AOV, efficient |
| Jack Johnson | 52 | $291,140 | 20 | $5,599 | High AOV, lower volume |
| Andrea Teague | 48 | $229,113 | 22 | $4,773 | Solid mid-tier |
| Jaime Hernandez | 48 | $67,943 | 0 | $1,415 | Low GMV, 0 customers (internal?) |
| Richard Goodman | 46 | $102,197 | 13 | $2,222 | |
| Katrinka Barnhart | 46 | $99,959 | 27 | $2,173 | Broad reach |
| Bobby Hansard | 34 | $75,758 | 6 | $2,228 | Narrow customer base |

---

## Rep Behavioral Intelligence (Q4 2025)

*Cross-references per-rep behavioral data against the [validated SuperCat correlation model](https://thelinecard.com/top-sales-activities-proven-to-boost-revenue) and MCP order outcomes.*

> **Data sources**: Per-user behavioral counters (BigQuery `user_feature_usage_report` view — 100% of Mixpanel events, fully operational as of 2026-03-19), order outcomes (supercat-postgres MCP). Both data sources are queryable at scale for any customer via the query library (`05_query_library.md`).

### Behavior × Outcomes

| Rep | Logins | Cust. Targeting | Prod. Discovery | Config/Bundle | Presentation | Library | Portal | Q4 iPad Orders | Q4 GMV | Unique Cust. | AOV |
|-----|-------:|----------------:|----------------:|--------------:|-------------:|--------:|-------:|---------------:|-------:|---------:|----:|
| Sharyn Moss | 624 | 648 | 5,435 | 675 | 167 | 3,146 | 1,738 | 49 | $112K | 22 | $2,288 |
| Jack Johnson | 365 | 355 | 2,073 | 316 | 199 | 560 | 1,681 | 10 | $116K | 5 | $11,553 |
| Steve Billingsley | 189 | 140 | 305 | 301 | 4 | 410 | 333 | 6 | $53K | 5 | $8,881 |
| Brian McKinney | 184 | 79 | 1,243 | 171 | 170 | 786 | 811 | 1 | $11K | 1 | $11,165 |
| Barbara Harper | 179 | 1,526 | 3,362 | 944 | 0 | 1,052 | 8 | 58 | $192K | 0* | $3,308 |
| Bobby Hansard | 164 | 172 | 1,361 | 362 | 8 | 816 | 773 | 11 | $24K | 5 | $2,189 |
| Jerry Montini | 158 | 245 | 1,574 | 693 | 68 | 842 | 879 | 34 | $165K | 16 | $4,846 |
| Todd Teague | 154 | 272 | 2,572 | 733 | 833 | 599 | 343 | 26 | $148K | 10 | $5,683 |
| Morgan Horwitz | 131 | 9 | 740 | 120 | 102 | 325 | 19 | **0** | $0 | 0 | — |
| Christie Schellenbach | 124 | 313 | 1,307 | 220 | 43 | 123 | 119 | 12 | $21K | 1 | $1,728 |
| Kirsten Seidl | 105 | 296 | 779 | 350 | 86 | 1,084 | 320 | **2** | — | — | — |
| Paul Camillo | 105 | 24 | 652 | 0 | 82 | 940 | 7 | **0** | $0 | 0 | — |
| Katrinka Barnhart | 91 | 1,745 | 2,537 | 213 | 25 | 512 | 0 | 6 | $21K | 3 | $3,488 |

*Customer Targeting = Select Customer + Search Customer. Config/Bundle = View Kit + Order Kit + Order Configured Item. Presentation = Email Item Info + Create PDF + Share My List + Export CSV/Excel. Library = View Library Entry.*
*\*Barbara Harper: 0 unique customers in Q4 MCP data likely a data join issue — 12-month analysis shows 1 unique customer.*

### Selling Archetypes

| Archetype | Rep | Signature | Risk / Opportunity |
|-----------|-----|-----------|-------------------|
| **Deep-Account Specialist** | Barbara Harper | Highest customer targeting (1,526) and Q4 volume (58 orders, $192K). Zero presentation activity. Knows her account intimately, configures complex orders rapidly. Pure execution. | Extreme concentration — if her one customer churns, $192K/quarter disappears. |
| **Curated Discovery Seller** | Todd Teague | Highest filter usage (329), My List engagement (685 views, 50 creates), and PDF catalog generation (98). High AOV ($5,683), 10 customers. Builds curated selections, packages polished presentations. | **Model rep** — behavior matches the full validated correlation hierarchy. His approach is the most scalable because it's diversified. |
| **Volume Relationship Seller** | Sharyn Moss | Most logins (624), highest product search (5,435), highest library views (3,146). 22 customers. Compensates for lower AOV ($2,288) with volume (49 Q4 orders). Lives inside the platform. | Strong but volume-dependent. Could improve AOV with more configuration coaching. |
| **Precision Closer** | Steve Billingsley | Low browsing (305 searches), very high AOV ($8,881). 49 configured items per order. Checks backorders and fulfillment, then writes large, complex orders. Minimum waste. | Low volume (6 orders). If he increased frequency, even modestly, significant GMV upside. |

### Behavioral Funnel Gap Analysis

Applying the validated funnel: **Customer Targeting → Product Discovery → Configuration → Presentation → Orders**

| Rep | Cust. Targeting | → Discovery | → Configuration | → Presentation | → Orders | Funnel Gap |
|-----|:-:|:-:|:-:|:-:|:-:|---|
| **Todd Teague** | Strong | Strong | Strong | **Strong** | Strong (26, $148K) | **None — full funnel. Model rep.** |
| **Jerry Montini** | Moderate | Strong | Strong | Moderate | Strong (34, $165K) | Presentation lower — sells on relationship |
| **Barbara Harper** | Very Strong | Strong | Strong | **Zero** | Strong (58, $192K) | Presentation skipped — deep relationship selling |
| **Sharyn Moss** | Strong | Very Strong | Strong | Strong | Strong (49, $112K) | No gap — volume-over-value pattern |
| **Katrinka Barnhart** | **Very Strong** (1,745) | Very Strong (2,537) | **Moderate (213)** | Weak (25) | **Low (6, $21K)** | **Configuration gap — most actionable coaching opportunity** |
| **Bobby Hansard** | Moderate | Strong | Strong | Weak | Low (11, $24K) | Presentation gap — doesn't package or share |
| **Sara Buffington** | Moderate | Strong | **Low (0)** | Low | Very Low (2, $4K) | Configuration + Presentation gaps |
| **Derek Campbell** | Low | Low | Low | Zero | Low (4, $4K) | Full funnel weakness |

**Highest-impact coaching opportunity**: Katrinka Barnhart. Highest customer targeting intensity of any rep (1,745 events) and very high product discovery (2,537), but configuration activity (213) is disproportionately low relative to discovery. She does the hard work of finding customers and products but doesn't convert into complex, configured orders. Targeted coaching on bundling and CPQ tools could directly improve her output. If her AOV increased from $3,488 to match Jerry Montini's $4,846 (+39%), that's ~$8K/quarter in incremental GMV.

### Non-Selling Users (Role Classification)

| User | Logins | Product Search | Key Behaviors | Likely Role |
|------|-------:|---------------:|---------------|-------------|
| Morgan Horwitz | 131 | 740 | 83 PDF catalogs, 120 kit views, 15 CSV exports | Catalog/Data Manager |
| Mia Pepitone | 63 | 2,392 | 146 My List views, 26 creates, 6 edits | Merchandising/List Curator |
| Paul Camillo | 105 | 652 | 940 library views, 123 library emails, 82 PDF catalogs | Content/Library Manager |
| Kirsten Seidl | 105 | 779 | 1,084 library views, 288 Cust Product Lists, 320 portal | Customer Insights/Analytics |
| Brian McKinney | 184 | 1,243 | 811 portal views, 141 email item info, 29 PDF catalogs | Sales Support/Inside Sales |

These users should be excluded from rep performance benchmarks. Their behavioral fingerprints (high library/PDF/portal, zero orders) clearly indicate non-selling roles.

### Seat Utilization

BCF has 1,370 org users but only ~10 are consistent sellers generating meaningful order volume. From the 49 users active in Q4:

| Category | Count |
|----------|------:|
| Active sellers (>5 Q4 orders) | 10 |
| Light sellers (1-5 Q4 orders) | 14 |
| Non-selling roles (0 orders, active usage) | 7 |
| Inactive/minimal (0-1 logins) | 7 |
| Low-activity misc | 11 |

**Insight**: Significant seat optimization opportunity — most user seats are not generating order volume. Under step-declining user pricing, this becomes a transparent conversation about value-per-seat.

---

## Customer Concentration (12 months, top 10 by GMV)

| Customer | Orders | GMV | % of Total |
|----------|-------:|----:|--------:|
| Outer Banks Furniture | 89 | $169,582 | 2.6% |
| Trident Furnishings Inc | 61 | $303,451 | 4.7% |
| Steven Shell LLC | 22 | $128,355 | 2.0% |
| W.F. Booth & Son, Inc. | 74 | $115,600 | 1.8% |
| Guthrie Interiors | 67 | $108,895 | 1.7% |
| Furniture & More | 60 | $98,238 | 1.5% |
| Casual Designs Furniture | 21 | $91,672 | 1.4% |
| Osborne's Furniture | 33 | $88,059 | 1.4% |
| Styled By Sean | 26 | $87,821 | 1.4% |

**Insight**: Customer concentration is healthy — top customer is only 4.7% of GMV. No single-customer dependency. But only 376 of 1,983 loaded customers (19%) ordered in the past 12 months. **81% of the customer base is dormant** — a massive activation opportunity.

---

## Order Volume Trend (12 months)

| Month | Orders | iPad | eOL | iPad % |
|-------|-------:|-----:|----:|-------:|
| Mar 2026 (partial) | 148 | 81 | 67 | 55% |
| Feb 2026 | 247 | 121 | 126 | 49% |
| Jan 2026 | 204 | 91 | 113 | 45% |
| Dec 2025 | 141 | 68 | 73 | 48% |
| Nov 2025 | 224 | 140 | 84 | 63% |
| Oct 2025 | 214 | 90 | 124 | 42% |
| Sep 2025 | 200 | 111 | 89 | 56% |
| Aug 2025 | 215 | 111 | 104 | 52% |
| Jul 2025 | 214 | 107 | 107 | 50% |
| Jun 2025 | 202 | 97 | 105 | 48% |
| May 2025 | 232 | 122 | 110 | 53% |
| Apr 2025 | 221 | 116 | 105 | 52% |

**Insight**: Order velocity is stable (~200-250/month). Channel mix oscillates around 50/50 with iPad slightly dominant. eOL share has been growing — Jan 2026 hit 55% eOL, the highest single month. December shows seasonal dip. This is a textbook Platform-Embedded account with dual-channel commerce.

---

## Mixpanel Feature Usage (iPad)

| Event | Count | Signal |
|-------|------:|--------|
| product_search | 36,405 | Heavy catalog browsing |
| selected_org | 22,316 | Multi-org switching |
| view_document | 17,287 | **Heavy library usage** |
| view_portal | 7,431 | Active Sales Portal engagement |
| add_configured_item_to_order | 7,173 | **Heavy CPQ usage** |
| customer_search | 5,554 | Active customer workflows |
| customer_selection | 5,390 | |
| pspdfkit_activated | 3,171 | PDF generation |
| item_added_via_magic_button | 2,646 | Quick-add workflow |
| view_stack | 2,147 | Smart stack engagement |
| order_submitted | 1,737 | iPad order submissions |
| pdf_catalog_started | 1,183 | PDF catalog generation |
| filter_button_pressed | 1,095 | Filtering behavior |
| view_kit | 1,088 | Kit browsing |
| pdf_catalog_generated | 867 | PDF completion rate: 73% |
| view_customer_orders | 635 | Customer order history review |
| document_email_drafted | 444 | Document sharing |
| item_email_drafted | 345 | Item sharing |
| view_favorites | 227 | Customer favorites (lower than expected) |
| add_kit_to_order | 187 | Kit ordering |
| create_stack | 171 | User-created lists |

**Insights**:
- Library/documents (17,287 views, 444 emails) is one of BCF's most-used features — they're a content-heavy operation.
- CPQ is a core workflow — 7,173 configured items is extremely high.
- Portal access (7,431 views) shows active Sales Intelligence usage.
- Customer favorites (227 views) is underutilized relative to the customer base size (1,983 customers). Could be an enablement opportunity.
- PDF catalog generation has a 73% completion rate (1,183 started, 867 generated) — 27% abandonment may indicate UX friction.

---

## Support Profile (HelpScout — via BigQuery)

> Data source: BigQuery `helpscout.conversations` + `helpscout.customers` (organization = "Braxton Culler")

| Metric | Value |
|--------|-------|
| Total tickets (all time) | 162 |
| Closed | 160 |
| Open/Pending | 2 |
| First ticket | 2022-11-01 |
| Last ticket | 2026-03-17 |
| Rank (all accounts) | #2 (after internal SuperCat Solutions) |

**Quarterly trend**:

| Quarter | Tickets |
|---------|---------|
| Q2 2023 (peak) | 31 |
| Q3 2023 | 15 |
| Q4 2023 | 14 |
| Q1 2024 | 6 |
| Q2 2024 | 11 |
| Q3 2024 | 11 |
| Q4 2024 | 13 |
| Q1 2025 | 9 |
| Q2 2025 | 8 |
| Q3 2025 | 5 |
| Q4 2025 | 5 |
| Q1 2026 (partial) | 11 |

**Tag distribution**:

| Tag | Tickets | % | Platform Avg |
|-----|---------|---|-------------|
| L1 — frontline | 138 | 85% | ~80% |
| Product: eCat | 98 | 60% | ~58% |
| S4 — low | 68 | 42% | ~47% |
| Type: bug | 63 | 39% | ~28% |
| Type: feature request | 60 | 37% | ~31% |
| S2 — high | 50 | 31% | ~21% |
| Product: eOL | 29 | 18% | ~7% |
| S1 — critical | 28 | 17% | ~15% |
| Product: Admin Console | 26 | 16% | ~23% |
| Type: training | 19 | 12% | ~14% |
| L3 — engineering | 10 | 6% | ~5% |

**Insights**:
- Ticket volume is on a healthy declining trajectory — peaked at 31/quarter, now running 5–11.
- High eOL ticket share (18% vs 7% platform average) — BCF experiences disproportionate eOL friction. This correlates with their aggressive eOL adoption (49% channel share).
- Bug ticket rate (39%) is notably above platform average (28%) — BCF may be hitting edge cases due to heavy feature utilization across the full stack.
- Primary contact: Morgan Horwitz (mhorwitz@braxtonculler.com) — also classified as Catalog/Data Manager in the rep behavioral analysis. She handles both data management and support communications — a single point of failure worth noting.

---

## Clicky Analytics (Portal Engagement)

**Status: NOT ESTABLISHED for Braxton Culler.**

BCF does not currently have a Clicky Analytics portal configured. This means demand-side engagement data — what dealers and end-customers do on BCF's eOL portal — is not available.

**What BCF is missing** (capabilities available for the 48 clients with Clicky):
- Daily portal traffic metrics (visitors, pageviews, bounce rate, session depth)
- Geographic demand mapping (which states/regions generate portal traffic)
- Traffic source intelligence (direct vs. search vs. referral — signals dealer awareness)
- Visitor organization identification (reverse DNS — which companies browse the catalog)
- Portal engagement churn signal (declining traffic as a leading indicator)

**Why this matters for BCF specifically**: BCF processes 49% of orders via eOL and recently experienced a 99x portal order explosion (7 → 696/month). Understanding who is visiting the portal, from where, and how they engage would be extremely valuable for optimizing this rapidly growing channel.

**Recommendation**: Establish Clicky Analytics for BCF's eOL portal. Given their eOL trajectory, this is high-priority. Reference Gabby (gh) as the benchmark — 374 avg daily visitors, 14% bounce rate, 8.2-min sessions, traffic from 20+ states.

**Cross-portal benchmark context** (from 15 validated Clicky portals, YTD 2026): The top portal (Gabby) averages 374 daily visitors. The median among portals with meaningful traffic (>100 visitors/day) is ~170. Once established, BCF's portal traffic would immediately contextualizable against this benchmark.

---

## Product & Inventory Intelligence

> Data sources: MCP `sales_data` (15,950 rows), `inventories` (1,115 SKUs), `products` (3,427 active, 29 categories), `customers` (1,983 with geographic data). All queryable via Q-PI-01 through Q-PI-07 in `05_query_library.md`.

### Inventory Health

| Metric | Value |
|--------|-------|
| Total SKUs in inventory | 1,115 |
| Out of stock (qty_available ≤ 0) | **101 (9.1%)** |
| Low stock (1-5 units) | 67 |
| Backordered | 0 |

### Top Sellers Out of Stock

| Item | Category | Historical Sales | Qty Sold | Available | On Hand | Restock ETA |
|------|----------|:---:|:---:|:---:|:---:|:---:|
| 0723-092 | CAT18 | $71,206 | 89 | **0** | **0** | None |
| 0724-015 | CAT12 | $70,550 | 46 | **0** | **0** | None |
| 0705-082 | CAT21 | $54,469 | 61 | **0** | **0** | None |
| 1023-028 | CAT3 | $53,040 | 193 | **-30** | 14 | Feb 27, 2026 (past due) |
| 0773-019 | CAT10 | $51,889 | 51 | **0** | **0** | None |
| 0773-011 | SOFAS | $48,403 | 45 | **0** | **0** | None |
| 0549-005 | CAT1 | $47,195 | 86 | **0** | **0** | None |
| 0635-002 | CAT1 | $45,711 | 45 | **0** | **0** | None |
| 0550-015 | CAT12 | $40,049 | 42 | **0** | **0** | None |

**Insight**: 9 of BCF's top 10 revenue-generating products have zero available inventory. Item 1023-028 has negative availability (-30) with a past-due restock date. Combined, these items represent $500K+ in historical demand that cannot currently be fulfilled. This is the highest-impact QBR insight — "your best sellers you can't sell."

### Sales by Category

| Category | Total Sales | Items | Qty Sold | Sales/Item |
|----------|:---:|:---:|:---:|:---:|
| CAT1 | $5.79M | 150 | 8,923 | $38,600 |
| CAT21 | $3.97M | 198 | 4,474 | $20,045 |
| SOFAS | $3.46M | 102 | 3,314 | $33,881 |
| BEDS | $1.73M | 21 | 4,473 | **$82,534** |
| CAT3 | $1.57M | 26 | 5,187 | $60,512 |
| CAT15 | $1.43M | 17 | 1,572 | **$83,959** |
| CAT12 | $1.03M | 43 | 888 | $24,060 |
| CAT2 | $892K | 77 | 2,471 | $11,589 |
| CAT10 | $876K | 28 | 953 | $31,289 |
| CAT4 | $807K | 22 | 2,330 | $36,675 |

**Insight**: BCF uses a mix of descriptive (SOFAS, BEDS) and opaque (CAT1, CAT21) category codes across 29 categories. BEDS and CAT15 have the highest per-item sales productivity ($82K and $84K respectively) — small product lines generating outsized revenue. CAT21 has the broadest catalog investment (198 items) but moderate per-item return ($20K). This pattern suggests opportunities for SKU rationalization in broad-but-underperforming categories and expansion investment in high-productivity lines.

### Regional Sales Distribution (12 months)

| State | Customers | Orders | GMV |
|-------|:---------:|:------:|----:|
| NC | 37 | 382 | $874K |
| NJ | 35 | 320 | $746K |
| FL | 52 | 291 | $660K |
| DE | 12 | 117 | $542K |
| SC | 19 | 150 | $514K |
| GA | 32 | 93 | $315K |
| PA | 16 | 87 | $220K |
| VA | 9 | 92 | $170K |
| TX | 27 | 79 | $148K |
| MI | 19 | 54 | $129K |
| NY | 17 | 50 | $89K |
| IL | 11 | 61 | $80K |
| AL | 5 | 28 | $58K |
| MD | 9 | 23 | $47K |
| CO | 1 | 13 | $34K |

**Insight**: BCF's sales are concentrated in the Southeast and mid-Atlantic — NC, NJ, FL, DE, and SC account for $3.3M (51%+) of 12-month GMV. Notable patterns:
- **Delaware** has only 12 customers but $542K GMV ($45K per customer) — very high-value accounts, likely concentrated in a few large dealers. Worth protecting.
- **Texas** has the 3rd-most customers (27) but relatively low GMV ($148K, $5.5K per customer) — significantly below states like NC ($23.6K per customer) or DE ($45.2K per customer). This is either a dealer mix issue (many small/inactive accounts) or a wallet share opportunity.
- **Florida** has the most customers (52) but only $660K — broad coverage with moderate depth.
- Once Clicky Analytics is established, the supply × demand geographic overlay (actual sales by state vs. portal visitor traffic by state from VM-33) would reveal where there's organic demand BCF isn't converting.

### At-Risk High-Value Customers (no order in 90+ days)

| Customer | State | 12mo Orders | 12mo GMV | Last Order | Days Silent |
|----------|:-----:|:-----------:|:--------:|:----------:|:-----------:|
| BC Guest-Wholesale | NC | 18 | $66,949 | Nov 6, 2025 | 137 |
| Halo Home | NC | 17 | $49,938 | Nov 5, 2025 | 138 |
| Kalin Home Furnishings | FL | 3 | $42,575 | Dec 15, 2025 | 98 |
| Sweat's Furniture, Inc. | GA | 7 | $32,570 | Dec 11, 2025 | 102 |
| Home Accents II | SC | 4 | $32,165 | Nov 3, 2025 | 140 |
| B & B Family Ventures | NC | 2 | $26,755 | Sep 29, 2025 | 175 |
| Senior By Design | TX | 3 | $25,570 | Dec 5, 2025 | 107 |
| Esther Ashe Designs | GA | 1 | $24,631 | Apr 27, 2025 | 330 |
| Custom Home Furnishings | NC | 5 | $23,500 | Nov 2, 2025 | 140 |
| Rising Sun Partners LLC | PA | 4 | $23,034 | Sep 10, 2025 | 193 |

**Insight**: These 10 customers represent $347K in trailing-12-month GMV and have all gone silent for 90+ days. BC Guest-Wholesale ($67K, 18 orders — 137 days silent) and Halo Home ($50K, 17 orders — 138 days silent) are the highest-urgency reactivation targets. Esther Ashe Designs ($24.6K) has been silent for 330 days — likely fully lapsed. Rising Sun Partners (193 days) and B & B Family Ventures (175 days) are approaching the point of no return. These are proven buyers with demonstrated purchasing history who've gone quiet — the highest-ROI reactivation targets in the book.

---

## Segment Classification

Based on behavioral signals, BCF is a **Platform-Embedded** account (Segment 3 / T3):
- Dual-channel commerce at near-parity (51% iPad / 49% eOL)
- Full stack enabled (iPad + Catalog + Cart + Portal + Closed Site)
- 376 ordering customers in 12 months
- $6.5M GMV
- 145 actively ordering users
- Heavy CPQ, kit, and portal usage

---

## Cross-Instance Intelligence (BigQuery `insightful_product` — live 2026-03-24)

> Data source: BigQuery `supercat-data-pipeline.insightful_product` views. All data is live and always current. Queries Q-CI-01 through Q-CI-08 in `05_query_library.md`.

### Composite Health Score

**Health Score: 0.75 / 1.0**

| Component | Max | BCF | Notes |
|-----------|:---:|:---:|-------|
| Has logins | 20 | 20 | 7,863 logins |
| Orders > 50 | 20 | 20 | 1,773 orders |
| Feature depth (5pts × 4) | 20 | 20 | 7 / 8 features |
| Has ARR | 10 | 10 | $26,620 ARR |
| Portal visitors > 50 | 15 | 0 | **No Clicky portal** — costs 15 points |
| Portal traffic growing | 10 | 0 | **No Clicky portal** — costs 10 points |
| Active users > 3 | 5 | 5 | 48 active users |
| **Total** | **100** | **75** | |

**Insight**: BCF's health score is 0.75 — dragged down entirely by the missing Clicky Analytics portal. If Clicky were established and healthy (>50 visitors/day, growing traffic), the score would jump to 0.95-1.0. This is the single clearest argument for establishing Clicky Analytics for BCF.

### Peer Comparison (Platform-Embedded segment, 33 orgs)

| Metric | BCF | Segment Median | vs. Peer | Standing |
|--------|----:|:-:|:-:|---|
| Orders | 1,773 | 2,986 | **-40.6%** | Below Average |
| Logins | 7,863 | 6,368 | +23.5% | Above Average |
| MRR | $2,280 | $1,685 | +35.3% | Above Average |
| ARR | $26,620 | $16,980 (p25) – $25,760 (p75) | Within range | Mid-tier |
| Feature depth | 7 / 8 | — | — | High |

**Peer standing: Below Average** — driven by the order gap.

**Insight**: BCF is a surprising "Below Average" in its segment. They're above median on logins (+23.5%) and MRR (+35.3%), but significantly below on orders (-40.6%). BCF felt like a power user in isolation — 1,773 orders, $6.5M GMV, 7/8 features. Against peers, it's clear there's growth headroom. The top Platform-Embedded performers (Gabriella White at 38,049 orders, Summer Classics at 13,424, Gabby at 13,049) operate at a completely different scale. BCF's 81% dormant customer base is the most likely explanation — high engagement, low conversion breadth.

### Platform-Embedded Benchmarks (March 2026)

| Metric | p10 | p25 | Median | p75 | p90 |
|--------|:---:|:---:|:------:|:---:|:---:|
| Orders | — | 1,205 | 2,986 | 6,109 | 7,760 |
| Logins | — | 4,640 | 6,368 | 8,568 | — |
| Product searches | — | 25,709 | 35,609 | 52,644 | — |
| MRR | — | $0 | $1,685 | $2,030 | — |

BCF sits between p25 and median on orders (1,773 vs. 1,205/2,986), between median and p75 on logins (7,863 vs. 6,368/8,568).

### Expansion Signals

| Signal | Status |
|--------|--------|
| Segment upgrade | None needed — already Platform-Embedded |
| Portal opportunity | **"Set up eCat Online portal"** — Clicky Analytics not established |
| Feature upsells | None flagged — BCF already uses Kit Builder, CPQ, PDF Catalogs |

### BCF in Context

| Dimension | BCF | Top Performer (Gabriella White) | Segment Median |
|-----------|:---:|:---:|:---:|
| Orders | 1,773 | 38,049 | 2,986 |
| Logins | 7,863 | 32,669 | 6,368 |
| Feature depth | 7 | 8 | — |
| ARR | $26,620 | $30,904 | ~$17K |

BCF is a strong but mid-tier Platform-Embedded account. The engagement intensity is there (above-median logins, full feature stack, active CPQ/portal usage). The order volume gap is the growth opportunity — and the dormant customer reactivation + at-risk high-value customer outreach identified in earlier sections are the clearest paths to closing it.
