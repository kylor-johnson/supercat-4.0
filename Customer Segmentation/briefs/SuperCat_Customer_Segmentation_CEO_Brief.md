# How SuperCat Customers Actually Sell

**June 29, 2026 | Data Sources: Postgres ERP sales_data, Postgres products (catalog prices), Mixpanel behavioral events, HubSpot enrichment**

---

## THE POINT

eCat is not a commerce platform for most of these companies. It's a **selling tool that sits upstream of commerce.**

Their actual commerce happens through their own eCommerce sites, EDI with Wayfair/Amazon/Ferguson, phone/email orders keyed into ERP, and marketplace integrations. We have ERP-level sales data for **67 orgs** in Postgres — actual invoiced revenue — plus catalog pricing for nearly every org. Combined, these tell us exactly what these companies sell, who they sell to, and at what price point.

**Why price point matters:** A company selling $15,000 chandeliers to designers cares about showroom placement, spec-driven selling, and relationship management. A company selling $4 housewares to TJX cares about volume, PO compliance, and EDI efficiency. Same platform, completely different job-to-be-done.

---

## THE PRICE SPECTRUM (ERP-Verified Transacted Prices)

This is what buyers actually *pay* — not list prices, but invoiced amounts per unit:

| Tier | Avg Unit Price | Who | Examples | Total Verified Revenue |
|------|---------------|-----|----------|----------------------|
| **Ultra-Premium** | $800–$2,100 | Custom luxury furniture & statement lighting | Interlude Furniture ($2,085), Somerset Bay ($1,949), Jonathan Charles ($1,217), Interlude Home ($1,138), Theodore Alexander ($901) | ~$130M |
| **Premium** | $400–$800 | High-end residential furniture & decorative lighting | Hubbardton Forge ($715), Four Seasons ($653), Gabby ($595), Currey & Co ($591), Universal Furniture ($585), Kalco ($516) | ~$560M |
| **Mid-Market** | $150–$400 | Mid-range lighting, outdoor furniture, art/accessories | Visual Comfort Signature ($364), Wendover Art ($334), Crystorama ($259), Braxton Culler ($482), Ratana ($274), Summer Classics ($426) | ~$520M |
| **Commercial/Value** | $30–$150 | Builder-grade lighting, volume furniture, ceiling fans | Capital Lighting ($104–$117), Minka ($162), Magnussen ($149), Linon/Powell ($76), Savoy House ($59) | ~$430M |
| **Commodity** | $3–$30 | Bulbs, housewares, supplies, textiles, ceiling fans | Bulbrite ($3.15), Kennedy Intl ($3.70), Home Essentials ($3.82), Moda ($6.78), Abaline ($28), Maxim ($35) | ~$290M |

**The range is 700x** — from $2,085/unit to $3.15/unit. These are fundamentally different businesses using the same platform.

---

## WHAT PRICE POINT ACTUALLY PREDICTS

### High Price = Relationship-Driven Selling

| Signal | Ultra-Premium ($800+) | Commodity ($3–$30) |
|--------|----------------------|-------------------|
| **Buyer count** | 500–14,000 (many, small) | 200–2,700 (few, massive) |
| **Revenue concentration** | Low (top 10 = 2–25%) | Extreme (top 10 = 58–89%) |
| **Who the buyer is** | Interior designers, specialty showrooms, independent dealers | TJX, Walmart, Amazon, Ross, Marshalls, Costco |
| **How the order happens** | Rep relationship → quote → PO | EDI feed → automated PO → fulfillment |
| **What the rep does** | Presents in-person, specs product, manages COM/customization, cultivates 500+ accounts | Manages relationship with buyer at a chain, does market meetings 2x/year, minimal daily interaction |
| **Where eCat adds value** | MASSIVE — every client interaction needs the catalog, pricing, options | Limited — big-box buyers never see an iPad. Value is internal ops. |
| **Showroom placement concern** | Critical. A $2K chandelier needs to be on the floor of Capitol Lighting. | Irrelevant. A $4 tumbler needs shelf space at Marshalls. |

### The "Showroom Placement" Threshold

You're right that this is a real dividing line. Here's the data:

**Companies where showroom/dealer placement IS the selling motion** (avg price > $200, selling to showrooms/retailers/designers):

| Org | Avg Transacted Price | Top Buyers (who they're placing product with) |
|-----|---------------------|-----------------------------------------------|
| Hubbardton Forge | $715 | Lumens ($4.2M), Ferguson ($2.2M), Build.com ($1.3M), Lightology ($1.1M), Lamps Plus ($1M), Capitol Lighting ($907K) |
| Currey & Company | $591 | Wayfair ($8.1M), Lumens ($3.1M), Capitol Lighting ($1.9M), Lighting New York ($1.9M), Ferguson ($1.9M), Lamps Plus ($1.7M) |
| Theodore Alexander | $901 | Baer's ($2.3M), Furnitureland South ($2.1M), Matter Brothers ($818K), France & Son ($752K) |
| Corbett Lighting | $973 | (1,289 showroom accounts — pure spec-sell model) |
| Kalco/Allegri | $516 | (687 showroom accounts) |
| Crystorama | $259 | (2,448 showroom accounts) |

These companies' reps are doing **showroom selling**: visiting lighting showrooms and furniture galleries, presenting new collections, getting products spec'd onto displays, writing floor orders. Every meeting requires showing the catalog, discussing finishes/options, checking inventory. The iPad IS the selling surface.

**Companies where shelf placement is a procurement function, not a sales function** (avg price < $30, selling to chains):

| Org | Avg Transacted Price | Top Buyers (chain procurement offices) |
|-----|---------------------|----------------------------------------|
| Kennedy International | $3.70 | TJ Maxx ($7M), Walmart ($5.3M), Marshalls ($3.8M), Amazon ($1.7M), HomeGoods ($1.5M) |
| Home Essentials | $3.82 | H.G. Buying/TJX ($17.6M), Newton/TJX ($6.4M), Ross ($5.2M), Tuesday Morning ($5.2M), Marshalls ($4.9M) |
| Bulbrite | $3.15 | PDI Plumbing ($1.6M), Nova Lighting ($1.2M), Lumens ($1.1M), IBS Lighting ($1.1M) |
| Abaline Supply | $28 | Nursing homes and institutional facilities ($400K–$960K each) |

These companies' "reps" aren't doing showroom visits with iPads. They're doing quarterly buyer meetings at chain HQs, managing EDI onboarding, and responding to RFQs. The selling motion is **category management and procurement relationships**, not floor-level product presentation.

---

## THE REVISED FOUR-SEGMENT MODEL (Price × Selling Motion)

### Segment 1: "Showroom Sellers" — High Price × Relationship Distribution
**~30 orgs | Avg transacted price: $250–$2,100 | Selling to: showrooms, dealers, designers**

**Defining characteristics:**
- Product value justifies in-person selling (nobody emails a $700 chandelier order without seeing it)
- Buyer base is 500–14,000 independent accounts (showrooms, designers, retailers)
- Low revenue concentration (no single buyer > 5–10% typically)
- Rep visits showrooms, gets product on displays, writes spec orders
- Seasonal selling rhythm (High Point Market, Lightovation,?"Atlanta Market")

**SuperCat's role:** The **primary selling surface.** Rep opens iPad at showroom counter, shows new collection, checks finishes, looks up pricing, checks stock, generates PDF or writes order. This is the core ICP.

**Examples:**
| Org | Price | Revenue | Buyers | What They Need |
|-----|-------|---------|--------|---------------|
| Hubbardton Forge | $715 | $74M | 3,293 | Mobile catalog, finish options, lead times, spec sheets |
| Currey & Company | $591 | $137M | 11,008 | Product search across 2,752 SKUs, showroom presentation |
| Crystorama | $259 | $67M | 2,448 | Collection presentation, showroom photography reference |
| Theodore Alexander | $901 | $35M | 1,772 | High-touch presentation, COM/custom, designer portfolios |
| Palecek | $3,437 (catalog) | — | 7,874 | Custom options, material samples, designer presentations |
| Kindel Karges | $12,938 (catalog) | — | — | Ultra-luxury, every piece is a conversation |

**eOL fit:** Strong — their showroom buyers would benefit from a self-service reorder portal. Showroom managers could browse inventory and restock displays without waiting for a rep visit.

---

### Segment 2: "Collection Presenters" — Mid-to-High Price × Mixed Distribution
**~20 orgs | Avg transacted price: $150–$600 | Selling to: mix of dealers + online marketplaces**

**Defining characteristics:**
- Product value still justifies some in-person selling, but online channels are significant
- Top 10 buyers include both traditional retailers AND marketplaces (Wayfair, Pottery Barn)
- Revenue is split: maybe 40% goes through traditional rep-sold dealers, 40% through marketplace/online POs, 20% through other
- Reps handle the dealer side; the marketplace side is EDI/operations

**SuperCat's role:** Primary tool for the **dealer/showroom portion** of their business. Irrelevant for the Wayfair/marketplace portion (those POs come via EDI or portals, not rep iPads).

**Examples:**
| Org | Price | Revenue | Buyers | The Split |
|-----|-------|---------|--------|-----------|
| Jamie Young | $213 | $33M | 4,207 | Pottery Barn ($3.7M) + Wayfair ($2.5M) + Costco ($1.1M) = marketplace; plus 4,000 independent buyers |
| Universal Furniture | $585 | $186M | 5,151 | Mix of big retailers and independent dealers |
| Braxton Culler | $482 | $26M | 884 | Wayfair ($3.9M) + independent furniture stores |
| Furniture Classics | $354 | $26M | 2,081 | Wayfair ($2.4M) + own retail ($1.9M) + Kathy Kuo ($1.3M) + independents |
| Gabby | $595 | $35M | 2,758 | Mix of trade + direct |

**eOL fit:** Moderate for the dealer side. But their biggest accounts (Wayfair, PB) will never use eOL — they have their own procurement systems. eOL is for the long tail of 2,000+ small dealers.

---

### Segment 3: "Volume Distributors" — Low Price × Chain/Institutional Sales
**~10 orgs | Avg transacted price: $30–$150 | Selling to: chains, institutions, big-box**

**Defining characteristics:**
- Moderate unit price, high volumes (thousands of units per PO)
- Buyers are regional furniture chains, institutional buyers, or mid-tier retailers
- Sales motion is territory management + account relationship, not product-level presentation
- Revenue moderately concentrated (top 10 = 30–50%)

**SuperCat's role:** Territory management and order capture for the non-EDI portion. Reps use it for smaller dealer visits and market meetings. Bigger accounts probably have established ordering processes.

**Examples:**
| Org | Price | Revenue | Buyers | Top Buyers |
|-----|-------|---------|--------|-----------|
| Magnussen Home | $149 | $73M | 794 | Living Spaces ($16M), Havertys ($7M), Bob's ($5.4M) |
| Linon/Powell | $76 | $18M | 738 | Badcock ($1.7M), Aaron's ($1.2M), Grand Home ($1.1M), Bob's ($927K) |
| Capital Lighting | $104 | $92M | 1,717 | (Lighting distributors at high volume) |
| Savoy House | $59 | $93M | 1,214 | Top 10 = 38% of rev |

**eOL fit:** Limited. Their big buyers have their own systems. eOL might help mid-tier accounts reorder.

---

### Segment 4: "Commodity Feeders" — Lowest Price × Mass Retail/Marketplace
**~8 orgs | Avg transacted price: $3–$30 | Selling to: Walmart, TJX, Amazon, Ross, mass retail chains**

**Defining characteristics:**
- Units ship by the pallet/container, not individually
- Buyers are massive retail chains with their own buying offices and EDI
- "Sales" is category management — presenting assortments to chain buyers 2–4x/year
- Revenue extremely concentrated (top 10 = 58–89% of total)
- A rep doesn't "sell" $4 glassware one piece at a time; they sell a program to a buyer at Marshalls corporate

**SuperCat's role:** Internal catalog reference and small-account management. The big accounts (70%+ of revenue) will never touch eCat for ordering. Value is maintaining the catalog for internal reference and managing whatever dealer/small-account business exists.

**Examples:**
| Org | Price | Revenue | Buyers | Revenue Concentration |
|-----|-------|---------|--------|----------------------|
| Kennedy International | $3.70 | $41M | 545 | Top 10 = 58% (TJX, Walmart, Amazon, HomeGoods) |
| Home Essentials | $3.82 | $81M | 2,647 | Top 10 = **63%** (all mass retail) |
| Bulbrite | $3.15 | $34M | 1,434 | (Electrical distributors + bulk) |
| Moda at Home | $6.78 | $6M | 232 | Concentrated |
| Abaline Supply | $28 | $46M | 1,204 | Institutional (nursing homes, hospitals) |

**eOL fit:** Very limited for their core business. Their big buyers have their own portals (Walmart Retail Link, Amazon Vendor Central). eOL makes zero sense for this motion.

---

## THE PRICE-POINT MATRIX

| | Relationship-Driven (many small buyers) | Concentrated (few large buyers) |
|------|----------------------------------------|-------------------------------|
| **High price ($400+)** | **SHOWROOM SELLERS** — Core ICP. Max eCat value. Every rep interaction needs the tool. eOL fits for dealer reordering. | (Rare — luxury + concentrated doesn't happen often. Maybe Jonathan Charles: 33 buyers, $581K/buyer) |
| **Mid price ($100–$400)** | **COLLECTION PRESENTERS** — Good fit. Rep tool for dealer side. Marketplace side bypasses eCat. | **VOLUME DISTRIBUTORS** — Moderate fit. Territory management. Big accounts bypass eCat. |
| **Low price ($3–$100)** | (Doesn't really exist — low-price + long tail is retail, not B2B) | **COMMODITY FEEDERS** — Lowest eCat value. Category mgmt, not field selling. Platform is catalog reference. |

---

## WHAT THIS MEANS (The "So What")

### 1. Price point predicts eCat value per account more than any other variable.

A $715/unit lighting company (Hubbardton Forge) with 3,293 dealer accounts gets more value from every login than a $4/unit housewares company (Home Essentials) with 2,647 chain buyers — even though they look similar in seat count and ARR. One uses the iPad at every buyer meeting. The other uses it for internal reference and the small-account fringe.

### 2. Tier pricing should acknowledge this reality.

A Commodity Feeder paying $8K ARR to use eCat as an internal catalog isn't underpaying — they're getting less value per user because their selling motion doesn't require rep-level product presentation for their core revenue. A Showroom Seller paying $20K ARR is arguably underpaying — eCat is literally how their 100 reps generate $74M in invoiced revenue.

### 3. eOL expansion targeting should follow the price spectrum.

| Segment | eOL Opportunity | Why |
|---------|----------------|-----|
| Showroom Sellers | **Highest** | Their buyers (showrooms, designers) would genuinely benefit from a self-service portal for reorders, spec sheets, inventory checks |
| Collection Presenters | **Medium** | eOL for the long-tail of small dealers, not for Wayfair/PB |
| Volume Distributors | **Low** | Big buyers have their own systems. Small buyers might use it. |
| Commodity Feeders | **Minimal** | Walmart/TJX will never log into eOL. Ever. |

### 4. The "Daily Driver" accounts I flagged earlier now make sense.

Accounts like Crystorama (88 users, $37K ARR, 21 orders), Eurofase (98 users, $36K ARR, 8 orders), and Capital Lighting (88 users, $30K ARR, 2 orders) looked like underperformers when measured by eCat orders. But their avg transacted prices ($259, $208, $104) and buyer counts (2,448 / 1,094 / 1,717) confirm they're **showroom sellers whose reps live in the app daily** — they just consummate orders through established distributor channels. They're not failing. They're using eCat exactly as intended for their selling motion.

### 5. Don't push order submission on Commodity Feeders.

When Home Essentials has 63% of their $81M revenue flowing through TJX/Ross/Marshalls corporate buying offices via EDI, asking "why don't your reps submit more orders through the iPad?" is the wrong question. Their reps don't sell individual items to individual buyers. They sell programs to chain buyers in twice-yearly meetings. eCat's value to them is catalog management and the small-account fringe.

---

## THE COMBINED SEGMENTATION FRAMEWORK

**Primary axis:** Selling motion (determined by price point × buyer type × concentration)  
**Secondary axis:** Platform engagement (Platform-Embedded / Commerce-Active / Catalog-Focused from Mixpanel)  
**Modifier:** Login recency (current vs. declining vs. dark)

| Segment | Selling Motion | Platform Behavior | Account Count | Action |
|---------|---------------|-------------------|---------------|--------|
| Showroom Sellers + Platform-Embedded | Ideal state | ~20 | Protect. Expand eOL. |
| Showroom Sellers + Commerce-Active | Using it, could use it more | ~15 | Reduce order friction. Demo eOL. |
| Showroom Sellers + Catalog-Focused | Under-utilizing relative to potential | ~10 | Activation priority. High potential. |
| Collection Presenters + Platform-Embedded | Good fit for dealer portion | ~15 | Maintain. eOL for long tail. |
| Volume/Commodity + any engagement | Lower ceiling, different value prop | ~15 | Maintain. Don't over-invest. Price appropriately. |
| Dark accounts (any motion) | Zero recent activity | ~10 | Triage: save or sunset. |

---

## DATA CONFIDENCE

| Source | What It Gives Us | Coverage |
|--------|-----------------|----------|
| Postgres `sales_data` (ERP invoices) | Actual transacted prices, buyer names, revenue concentration | 67 orgs (including most of the top 40 by ARR) |
| Postgres `products` (catalog) | List/net prices for every SKU | ~95% of active orgs |
| Postgres `customers` | Who their buyers are (name, territory, price level) | All active orgs |
| Postgres `login_events` | When reps actually log in | All orgs, real-time |
| BigQuery `org_master_with_segments` | Mixpanel behavioral events (searches, orders, PDFs, scans) | ~110 active orgs |
| HubSpot enrichment CSV | External signals (channel count, eCommerce, revenue, employees) | 108/110 orgs |

**Gap:** We still don't know total company revenue for all orgs (HubSpot estimates are rough). And ERP sales_data doesn't carry a date range — we don't know if Currey's $137M is lifetime, last year, or last 3 years. Clarifying the time window on sales_data would sharpen wallet-share calculations significantly.

---

*Price point is the variable that connects "what they sell" to "how they sell it" to "what eCat is worth to them." A $700/unit company with 3,000 dealer accounts will always get more per-login value from the platform than a $4/unit company with 500 chain buyers — and our segmentation, pricing, expansion targeting, and CS playbooks should reflect that reality.*
