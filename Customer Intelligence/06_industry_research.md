# Customer Intelligence — Industry Research

> **Status**: Research findings from furniture/lighting wholesale vertical analysis
> **Date**: 2026-06-15
> **Purpose**: Identify industry-specific intelligence needs that eCat's data can uniquely serve

---

## The Core Problem

Furniture and lighting manufacturers sell *through* independent reps and dealers but have almost no visibility into what happens after shipment. They know what they shipped. They don't know what sold through, what reps are actually presenting, or which dealers are quietly switching to a competitor.

Over 55% of furniture manufacturers lack real-time visibility into distributor demand and stock levels. Production plans ignore real sell-through data. The intelligence gap is structural, not a technology maturity issue — there simply hasn't been a platform sitting in the right position to see both sides.

eCat IS that platform.

---

## Competitive Landscape

**No tool exists** purpose-built for furniture/lighting manufacturers that combines:
1. Transactional order data (from ERP)
2. Rep/dealer engagement data (from sales enablement)
3. Trade show interaction data
4. Inventory/fulfillment patterns

into dealer intelligence. The competitive landscape:

| Tool | What It Does | What It Doesn't Do |
|---|---|---|
| STORIS | Full ERP for furniture *retailers* | Manufacturer-facing; no dealer network analytics |
| CFI Suite (NetSuite) | Contract furniture dealer ERP | Dealer-side; manufacturer sees nothing |
| Ward AI | AI analytics on Epicor/SAP/NetSuite for retailers | Retail-focused; no manufacturer-to-dealer intelligence |
| Salesforce Manufacturing Cloud | Dealer forecasting, AI scoring | Enterprise $$$; requires full SF ecosystem; doesn't understand furniture |
| Epicor / SAP Business One | Manufacturing operations ERP | Back-office; no rep enablement or dealer intelligence |
| eventkrowd | Badge scanning at High Point Market | Lead capture only; no connection to order data |
| Domo / Power BI | General BI dashboards | Requires heavy setup; not industry-specific |

**The gap is exactly where eCat sits.** The ERP knows what shipped. eCat knows what the rep showed, what the dealer browsed, what was quoted. The combination is unique.

---

## VP of Sales Pain Points (What They Actually Complain About)

1. **"I don't know what my reps are doing."** Reps spend 28% of time selling, 72% on admin. No visibility unless the rep self-reports.

2. **"We lose 4 out of 5 deals to competitors with faster quoting."** Speed-to-quote is the #1 competitive differentiator.

3. **"15-20% of orders have errors."** Configuration complexity (120K+ configs at some brands) means manual order entry is error-prone.

4. **"I can't tell which dealers are growing and which are dying."** No automated health scoring. A dealer can quietly stop ordering for a quarter before anyone notices.

5. **"Market costs us six figures and I can't prove the ROI."** No closed-loop attribution from showroom visit to order.

6. **"My best reps know everything; my average reps know nothing."** Top reps log in 10-12x/day, underperformers <2x.

7. **"We don't know what products dealers are actually showing."** 50 new SKUs launched, no idea which ones reps present or dealers browse.

8. **"Our ERP and our sales tools don't talk to each other."** Ranked #1 pain point across all company sizes.

---

## Industry-Specific Metrics That Are Hard to Track

| Metric | Why It's Hard | What They Want |
|---|---|---|
| **Showroom/floor model performance** | Floor models exist in a liminal state — not sellable, not pure assets. No standard tracking. | Revenue attributed per floor placement; time-on-floor before first reorder; floor model ROI by dealer |
| **Market/trade show ROI** | High Point costs $30K-$100K+ per show. Order surge appears 1-14 days after, but attribution is broken. | Closed revenue attributed to market contacts at 30/90/365 days |
| **Dealer tier management** | Manual today — spreadsheets, gut feel, annual reviews | Automated scoring; tier migration alerts; "at risk" flags |
| **Territory optimization** | Boundaries are legacy, not data-driven. No whitespace visibility. | Heatmaps of order density vs. dealer coverage; whitespace identification |
| **Designer vs. retailer vs. contract segments** | Different buying patterns, margins, service needs. ERPs treat them as flat list. | Revenue, margin, growth rate by segment; segment-specific reorder frequency |
| **Lead time / MTO vs. stocked** | 65% of manufacturers experience margin erosion from inaccurate costing on custom orders. Same product can be stocked or MTO. | MTO vs. stock mix by dealer; lead time accuracy; COM completion rates |
| **COM (Customer's Own Material)** | Specialized workflow. Most systems don't track yardage utilization or waste. | COM volume by dealer; utilization rates; COM vs. standard margin comparison |
| **Drop-ship vs. warehouse** | Hybrid fulfillment is standard. LTL damage rates 8-12%. | Fulfillment method mix by dealer; damage rates by carrier/route |

---

## Trade Show Calendar (Drives Everything)

| Quarter | Key Events | Ordering Dynamic |
|---|---|---|
| Q1 (Jan-Mar) | Atlanta Market, Las Vegas Market, Spring Market | Spring buying; early-buy programs |
| Q2 (Apr-Jun) | **High Point Market (Apr)**, Atlanta Market (Jun) | The Big One. New intros. Order surge 1-14 days post-market. |
| Q3 (Jul-Sep) | Casual Market Atlanta, Las Vegas Market, Fall Market | Outdoor/casual focus; fall assortment planning |
| Q4 (Oct-Dec) | **High Point Market (Oct)**, Holiday | Fall intros; holiday promo; early-buy programs launch |

Post-market attribution is the most wanted and least available metric in the industry. The order surge happens 1-14 days after market but nobody can connect showroom visits to orders.

---

## Lighting Industry Specifics

- **Configuration complexity**: Single fixture can have 10+ variants (finish, shade, size, chain length, voltage). Visual Comfort describes "fragmented product and customer data" from M&A acquisitions.

- **Specification-driven sales**: Lighting is spec'd by designers/architects into projects months before orders. The spec-to-order pipeline is invisible — manufacturers don't know how many specs are out, conversion rate, or which dealers convert best.

- **eMRP enforcement**: Manufacturers enforce electronic Minimum Retail Price but have no automated compliance monitoring for dealer online pricing.

- **Lightovation / Dallas Market**: Additional market cycle beyond High Point/Las Vegas. Another attribution gap.

- **Stock vs. custom split**: Some brands stock 1,000+ items for 72-hour ship, but much of the line is MTO from overseas. "Sales staff had no visibility into product availability or projected delivery times."

- **Hubbardton Forge example**: 160+ independent reps all using SuperCat. The data exhaust from rep activity is a goldmine for product development intelligence.

---

## eCat-Unique Analytics Opportunities

### Tier 1 — eCat data is the ONLY source

1. **Product Presentation Intelligence** — Which products are reps actually showing (filter/search/browse from eCat iPad)? Correlate with orders to find "presented but not purchased" gaps. Source: Mixpanel events with `selected_bill_to_code`.

2. **Rep Engagement Scoring** — Login frequency, session duration, products browsed, quotes generated, orders placed. Automated ranking that predicts revenue performance. Source: Mixpanel + orders.

3. **Dealer Browse-to-Buy Funnel** — For eCat Online: what dealers browse, add to cart, actually order. Source: orders.order_source = 'server' + Mixpanel/Clicky.

4. **New Product Launch Velocity** — After a new intro: how fast does it appear in rep presentations? Which dealers are early adopters? Source: Mixpanel product_search events + orders by time since product creation.

5. **Post-Market Order Attribution** — Tag orders placed within 1-14 days of High Point/Las Vegas/Lightovation. Measure the "market bump" by dealer, rep, and product. Source: orders.created_at + commitment_reports.market_code.

### Tier 2 — eCat + ERP data combined

6. **Dealer Health Score** — Combine order frequency, AOV trends, breadth of line purchased, and eCat engagement into a composite score. Source: portal_orders + orders + Mixpanel.

7. **Territory Whitespace Analysis** — Map order density by zip code against dealer locations. Source: customers.billing_* + orders + shipping_locations.

8. **MTO vs. Stock Intelligence by Dealer** — Which dealers order mostly quick-ship vs. custom/MTO? Source: portal_order_items + product attributes.

9. **Collection/Category Penetration by Dealer** — What % of your line does each dealer carry? Source: portal_invoice_items + products.

10. **Seasonal Pattern Recognition** — Dealer-level seasonality curves. Predict next order based on historical cadence. Alert reps to "overdue" reorders. Source: portal_orders.order_date.

### Tier 3 — Differentiating, deeper integration

11. **Floor Model ROI** — If inventory data includes showroom/display flags: which floor models drive reorders? Source: placement_reports + portal_order_items.

12. **COM Program Analytics** — Volume and margin of COM orders by dealer. Source: orders with options metadata + portal_order_items.

13. **Price Level Effectiveness** — Which price levels drive most volume? Promo cannibalization? Source: orders.price_level + portal_invoice_items.unit_price.

14. **Competitive Displacement Signals** — Sudden drops in order frequency or category ordering. Source: portal_orders + portal_order_items trend analysis.

---

## Cross-Reference: What Can We Actually Build Today?

| Industry Insight | Data Available? | Notes |
|---|---|---|
| Product presentation intelligence | **YES** | Mixpanel `product_search`, `filter_products` with `selected_bill_to_code` |
| Post-market order attribution | **YES** | `commitment_reports.market_code` + `orders.created_at` window |
| Dealer health scoring | **YES** | All components available across Postgres + Mixpanel |
| New product launch velocity | **YES** | `products.new_item` + `portal_order_items` time-series |
| Territory whitespace | **YES** | `customers.billing_*` + `orders` geographic aggregation |
| Collection penetration by dealer | **YES** | `portal_invoice_items` + `products.collection_code` |
| Seasonal pattern recognition | **YES** | `portal_orders.order_date` per customer |
| Floor model ROI | **PARTIAL** | `placement_reports` exist but item parsing needed from text blob |
| MTO vs. stock by dealer | **PARTIAL** | Would need product-level MTO flag (not confirmed in products schema) |
| COM analytics | **PARTIAL** | COM orders may be identifiable via `orders.order_items` options metadata |
| Spec-to-order pipeline | **NO** | Specification tracking not in eCat data model |
| eMRP compliance monitoring | **NO** | Would need dealer website price scraping |
| Sell-through data | **NO** | eCat has sell-in (manufacturer to dealer), not sell-through (dealer to consumer) |
