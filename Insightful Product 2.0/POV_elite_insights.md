# POV: What Makes This Report Worth Paying For

## The Core Problem with the Current Report

The current report answers: **"How is our platform doing?"** — useful at QBR time, impressive as a vendor deliverable, but not something a VP Sales opens on Monday morning to decide what to do this week.

The reports that command premium pricing answer a different question: **"What should we do differently tomorrow to make more money?"**

The gap is between *descriptive intelligence* (here's what happened) and *prescriptive intelligence* (here's what to do about it, quantified in dollars).

---

## The "Holy Shit" Hierarchy

What makes a VP of Sales at a $20M–$200M furniture/lighting manufacturer stop scrolling and forward the report to their entire leadership team:

### Tier 1: "I didn't know I was losing this" (Competitive Loss Signals)

The single most powerful insight in B2B wholesale: **detecting when a customer is spending MORE overall but LESS with you** — meaning dollars are going to a competitor. Nobody in this industry surfaces this.

**What we can build today (data ready):**
- Category-level competitive displacement: "Bedroom dropped $21.8K at this account while their total business grew 17.7%. Those dollars went somewhere else."
- Per-rep capture rate decay: "Rep X's accounts are spending 13% of total business through eCat, down from 18% last quarter."
- Geographic displacement: States where eCat share is declining while total business grows.

**Data sources:** `portal_orders` (total business) vs. `orders` (eCat) trended over time. Already available for any org with `HAS_PORTAL_ORDERS`.

---

### Tier 2: "Show me the money on the table" (Quantified Whitespace)

Not "here are some opportunities" but **exact dollar amounts sitting uncaptured with specific account names and a clear next action.**

**What we can build today:**
- **Wallet share estimation**: "Magnolia spends $284K with you. Similar retailers in the Southeast average $412K. Estimated wallet share: 69%. Addressable gap: $128K."
- **Cross-sell whitespace by category**: "This customer buys Upholstery and Lighting but zero Outdoor. 23 similar accounts average $31K in Outdoor. That's your opening."
- **Uncommitted market items**: "They committed to $52K at High Point. They've ordered $31K. These 3 items ($21K) are in stock RIGHT NOW and haven't been ordered."
- **New intro adoption gap**: "You launched 50 SKUs. This customer bought 6. Similar customers average 22. Here are the top 8 they haven't tried."

**Data sources:** `portal_orders` cohort analysis, `portal_invoice_items` + `products` category/collection mix, `commitment_reports` vs. `portal_order_items`, `products.new_item` cross-ref.

---

### Tier 3: "Tell me before it's too late" (Predictive Early Warning)

The difference between $X analytics and $10X analytics is **catching problems 60-90 days before revenue drops.**

**What we can build today:**
- **Per-SKU reorder decay detection**: "Monroe Chair historical interval: 28 days. Last 3 intervals: 32, 41, 58 days. This product is dying at this account."
- **Account velocity deceleration**: "12 accounts have order intervals stretching beyond 1.5x their historical average. Combined annual value: $840K."
- **Backorder-to-revenue-loss correlation**: "When this customer experiences a backorder, reorder interval increases 2.3x. Currently 3 top items backordered. Projected annual impact: -$14K."
- **Lifecycle stage forecasting**: "Based on cohort behavior, this account should peak at $400K in Year 3. They're tracking 18% above the curve. Or: this account is 6 months behind where similar accounts were at this tenure — intervention window closing."

**Data sources:** `portal_order_items` + `portal_orders.order_date` per customer x item, `portal_order_items.quantity_backordered`, cohort grouping.

---

### Tier 4: "I can see what my reps are actually doing" (Behavioral Intelligence)

The #1 VP Sales complaint: "I don't know what my reps are doing." eCat is the ONLY platform that can answer this with real behavioral data (not self-reported CRM entries).

**What we can build today:**
- **Product presentation intelligence**: "Rep showed 142 products to this account but only 21 converted to orders. Presented-but-not-purchased gap = your training opportunity."
- **New product launch velocity by rep**: "You launched the Riviera collection 45 days ago. 3 of 17 reps have shown it. Only 1 has sold it. The other 14 reps haven't even searched for it."
- **Rep engagement vs. account revenue correlation**: "Reps who engage accounts 8+ times/month produce 3.2x the revenue of reps at 2x/month. These 6 accounts get <2 touches/month and have $180K combined spend."
- **Selling time vs. admin time by rep** (from session patterns, search density, order rate per session)

**Data sources:** `mixpanel.events` with `selected_bill_to_code` + `username`, product_search, add_configured_item, order_submitted, pdf_catalog_generated events.

---

### Tier 5: "This is operationally addictive" (The Per-Customer Brief)

This is the product that creates lock-in. The org report is impressive 4x/year. **A per-customer brief before every sales call is daily dependency.**

The Customer Intelligence brief design (already fully specified in your files) delivers:
- Account at a Glance (5-second scan)
- Purchase DNA (what they buy, top SKUs, category mix)
- Buying Rhythm (when they buy, predicted next order window)
- Money Profile (spend trajectory, price behavior)
- Channel Mix (phone/fax volume = eCat conversion opportunity)
- Rep Engagement Profile (how much attention this account gets)
- Inventory Alert (are their favorites in stock?)
- Cross-Sell Opportunity (what similar customers buy that they don't)
- Fulfillment and Returns
- Market Commitments vs. Actuals
- Showroom Placements (stale placements, discontinued items on floor)
- Account Health Signal (composite score + pre-meeting priorities)

**The killer: "Pre-Meeting Priorities for Sarah"** — 5 numbered actions, each grounded in data, each with a dollar figure. The rep walks in knowing exactly what to talk about.

---

## What the Org-Level Report is Missing (Specific Additions)

Beyond the per-customer brief (which is a separate product), the org-level report itself can be elevated:

### A. Post-Market Attribution (the industry's white whale)

High Point costs $30K–$100K+ per show. Nobody can prove ROI.

**We can build:** "High Point April 2026 generated $412K in closed orders within 90 days of market (tagged via `portal_orders.order_origin` market codes + `commitment_reports.market_code`). That's 4.8x your market investment. Here are the breakdown by rep, by product category, by customer. Here are the 14 commitment items ($48K) that were NEVER ordered — all currently in stock."

### B. Fill Rate Revenue Impact (turns Operations into a Sales problem)

**We can build:** "Your fill rate is 88.1%. When customers experience backorders, their subsequent reorder interval extends 2.3x. Across all accounts, current backorder exposure impacts $340K in annualized reorder revenue. Top 5 impacted SKUs: [list with projected revenue impact]."

The VP Sales takes this to Operations: "Fix these 5 SKUs, it's costing us $340K."

### C. Buyer-Within-Account Intelligence

**We can build:** "Across your top 50 accounts, 23 have a new buyer name appearing in the last 90 days. New buyers who start in one category expand to 2.3 categories within 6 months on average. Here are the new names your reps should be building relationships with."

This is invisible without `portal_orders.buyer_name` segmentation.

### D. Same-Store Comps (Multi-Location Dealers)

**We can build:** "Your top 20 multi-location accounts: Charlotte +24%, Asheville +11%, Greenville -18%. The Greenville decline correlates with 4 stockouts in Q1 — may be supply-driven, not demand-driven."

Retail chains do this internally. No manufacturer does this across their dealer network.

### E. Price Erosion / Trade-Down Detection

**We can build:** "These 15 accounts are trading down — average unit price declining 4%+ per quarter. Combined, they represent $2.1M in annual business. If the trend continues, projected revenue impact: -$89K annualized at same volume."

---

## Why Clients Would Pay

| Value Driver | Current Report | Enhanced Report | Per-Customer Brief |
|---|---|---|---|
| **Frequency** | Quarterly | Quarterly | Every sales call |
| **Action proximity** | Strategic (informs decisions) | Strategic + tactical (quantified actions) | Tactical (informs the next conversation) |
| **Revenue attribution** | "Platform is doing well" | "Here's $840K at risk and $2.1M in whitespace" | "I closed a $12K order because the brief told me their top item was backordered" |
| **Who cares** | VP Sales at QBR | VP Sales + every rep manager | Every single rep |
| **Lock-in mechanism** | Impressive at renewal | Indispensable for planning | Operational dependency |
| **Volume** | 1/org/quarter | 1/org/quarter | 1/customer/visit (hundreds/quarter) |

---

## The Competitive Moat

From the industry research: **no tool exists** purpose-built for furniture/lighting that combines ERP transactional data + rep engagement behavioral data + trade show intelligence into dealer-level analytics. The landscape:

- STORIS, CFI Suite, Ward AI = retailer-focused (wrong side)
- Salesforce Manufacturing Cloud = enterprise $$$, no furniture specialization
- Hylos = sell-through only (dealer to consumer), not sell-in
- Sparrowhawk = CPQ + territory (no behavioral data layer)
- Power BI / Domo = generic BI (not industry-specific, requires heavy setup)

eCat is the ONLY platform sitting at the intersection of what the manufacturer ships, what the rep shows, and what the dealer orders. That's the moat.

---

## Recommended Implementation Sequence

**Phase 1 — Org report enhancements (immediate, no new infra):**
1. Competitive displacement detection (category drift + capture rate decay)
2. Quantified whitespace summary (wallet share + cross-sell by category)
3. Post-market attribution (commitment conversion + order origin attribution)
4. Reorder velocity early warning (account-level acceleration/deceleration)
5. Fill rate revenue impact quantification

**Phase 2 — Per-customer brief MVP (next):**
- Build from existing Customer Intelligence designs
- Start with top-10 accounts per org as proof of concept
- Sections 1-4, 7-8, 12 (most valuable, least complex)

**Phase 3 — Full prescriptive layer:**
- Next Best Product (purchase sequence prediction)
- Buyer-within-account intelligence
- Same-store comps
- Account lifecycle stage forecasting
- Product launch velocity by rep

All of this is buildable TODAY from existing data. Zero engineering. Zero new tables. Zero schema changes.
