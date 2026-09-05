# SuperCat Client Segmentation v3
## By How They Sell and To Whom — Not By How They Use eCat

**Date:** July 1, 2026  
**Sources:** HubSpot enrichment CSV (channel flags, "How They Sell", "Who They Sell To", company revenue), ERP sales_data (avg unit price per org), master account data (ARR, health)  
**Post-audit corrections (v3.1):** Bliss Studio reclassified to Luxury Specification (enrichment had scraped wrong company — Bliss Hammocks, not Bliss Studio; first-party catalog avg = $1,900); staging org removed (109 accounts); GTM label "Marketplace + Trade" corrected to "Trade + Select Retailers" for luxury accounts where the keyword referred to curated retail sites (Lumens, Lightology), not mass marketplaces.

---

## The Shift

Previous versions segmented by eCat behavior — logins, order submissions, feature usage. That tells us about our product-market fit. It says nothing about **how these companies actually run their businesses.**

This version segments by three questions:
1. **What do they sell?** (product type and price point)
2. **How do they sell it?** (trade-only, DTC + trade, marketplace, omnichannel)
3. **Who buys from them?** (designers, retail chains, consumers, hospitality)

eCat usage is irrelevant to these answers. A company that submits 8,000 orders through eCat and a company that submits zero may both sell luxury furniture to interior designers through showrooms — they just use our tool differently.

---

## The Four Segments

| # | Segment | Accounts | ARR | Median $/Unit | Defining Trait |
|---|---------|----------|-----|---------------|----------------|
| 1 | Luxury Specification | 36 | $630K | $892 | Their customer is the designer, not the consumer |
| 2 | Premium Trade Brand | 33 | $677K | $354 | Building a brand name across trade + consumer |
| 3 | Mid-Market Multi-Channel | 24 | $392K | $60 | Compete on availability, not specification |
| 4 | Volume Distribution | 12 | $179K | $4 | Sell to category managers at chains |

*(Plus 4 Specialty accounts — $63K ARR — that don't fit the model. 109 total accounts.)*

> **Note on ARR:** Multi-org entities (e.g., Theodore Alexander × 3 orgs, Gabriella White / Gabby × 2) share billing and therefore the same ARR value. Segment ARR totals are not additive across portfolio members — Luxury Spec ARR is inflated ~14% from duplicate counting. Medians are based on priced accounts only: 24/36 (Luxury), 23/33 (Premium), 11/24 (Mid-Market), 5/12 (Volume).

---

## Segment 1: Luxury Specification

**36 accounts | $630,454 ARR | Median unit price: $892**

### What they are
High-end furniture and lighting companies selling products above $500/unit through controlled trade channels. Their end customer is an interior designer, architect, or hospitality procurement team — not a retail consumer.

### How they sell
- Relationship-driven field sales through rep networks
- Showroom presentations (High Point, Dallas Market, private showrooms)
- Custom/configured orders (COM fabrics, custom finishes, bespoke sizing)
- Orders originate as specifications on design projects, not impulse purchases
- Most do NOT sell direct-to-consumer online (no public checkout on their site)

### Who buys
- Interior designers specifying for residential projects
- Architects specifying for commercial/hospitality builds
- Showroom dealers (independently owned lighting/furniture showrooms)
- Hospitality procurement (hotels, restaurants, luxury residential developers)

### Representative accounts
| Company | $/Unit | Company Revenue | Contract? |
|---------|--------|-----------------|-----------|
| Palecek | $3,626 | $27M | Yes |
| Interlude Furniture | $2,085 | $10M | — |
| Theodore Alexander | $907 | $21M | Yes |
| Charleston Forge | $841 | $35M | Yes |
| Currey & Company | $592 | $486M | — |
| Hooker Furnishings | $940 | $500M | — |
| Visual Comfort (3 orgs) | $30–$632 | $10M each | — |
| Jonathan Charles (2 orgs) | $619–$1,217 | $59M | — |

> *Visual Comfort - Studio/Fans ($30 avg ERP unit price) handles Visual Comfort's builder-grade studio line; it shares the same rep network and showroom channel as the other VC orgs and is grouped by selling motion, not price point.*

### Key commercial truth
These companies' orders don't consummate in eCat. A designer specs a $6,000 chandelier → rep enters the project in eCat → order goes to HQ → HQ audits, configures, enters into ERP → ships weeks later. eCat is the **presentation and project-capture tool**, never the transaction system.

The selling motion is: *build relationships with designers → get specified on projects → fulfill custom orders*. Whether they log into eCat 3,000 times or 300 times doesn't change what their business IS.

### Note on segment boundary (Luxury Specification vs. Premium Trade Brand)

These segments overlap in the $350–$715 price range. Some Luxury Spec accounts price below $500 (VC Signature at $364, Gabriella White at $482) while some Premium Trade accounts price above $500 (Hubbardton Forge at $715, Universal Furniture at $585). The distinguishing criterion is the **primary selling motion**: Luxury Specification accounts sell primarily to designers who *specify* products for projects (the designer selects the product *for* their client); Premium Trade Brand accounts sell primarily to consumers or dealers who *choose* a brand (the buyer picks the product for themselves). Price point is a strong correlate but not the boundary line — selling motion is.

---

## Segment 2: Premium Trade Brand

**33 accounts | $676,527 ARR | Median unit price: $354**

### What they are
Mid-to-upper-market brands ($150–$715/unit) actively building brand recognition with consumers while maintaining their trade/dealer channel as the primary revenue driver. They want the end consumer to know their name AND want the designer/dealer to carry them.

### How they sell
- Multi-channel: own DTC website AND trade accounts AND select retail/marketplace partnerships
- 67% do contract/hospitality work (more than any other segment)
- Brand marketing to consumers (social media, own site with lifestyle imagery)
- Trade programs with tiered pricing and designer discounts
- Some presence on Wayfair, Lumens, or other curated marketplaces

### Who buys
- Interior designers (still a primary channel)
- Retail showroom partners (curated, not mass)
- Direct consumers via their website (growing but secondary)
- Hospitality/contract specifiers (hotels, restaurants)

### Representative accounts
| Company | $/Unit | Company Revenue | Channels |
|---------|--------|-----------------|----------|
| Summer Classics | $426–$438 | $100M | DTC + Trade |
| Hubbardton Forge | $715 | $10M | Omnichannel |
| Crystorama | $259 | $6M | Omnichannel |
| Jamie Young Company | $214 | $4M | DTC + Trade |
| WAC/Modern Forms | — | $56M | DTC + Trade |
| Kuzco Lighting | — | $5M | Omnichannel |
| Arabela Lighting | — | $450M | Omnichannel |
| Hudson Valley Lighting | — | $10M | Trade Only |

### Key commercial truth
These brands are in transition. They grew on trade relationships but are investing in DTC — their own Shopify stores, brand marketing, consumer awareness campaigns. Many are on select marketplaces (Lumens, Perigold) but NOT on Amazon or Wayfair broadly.

Their challenge is: *maintain trade-partner loyalty while building direct consumer demand*. The dealer must not feel disintermediated. This tension defines their business, not how many eCat logins they have.

---

## Segment 3: Mid-Market Multi-Channel

**24 accounts | $391,742 ARR | Median unit price: $60**

### What they are
Lighting, furniture, and home goods companies selling $30–$150 products through as many channels as possible. They compete on availability, breadth of distribution, and price competitiveness — not on specification or brand prestige.

### How they sell
- Everywhere: own site, Amazon, Wayfair, Home Depot, Lowe's, lighting showrooms, electrical distributors
- High SKU counts (thousands of products)
- Dealer portals and catalogs for wholesale partners
- Online retailers get product feeds; showrooms get catalogs
- Mix of decorative/residential and builder/commercial products

### Who buys
- Lighting showrooms and electrical distributors (traditional channel)
- Online marketplace shoppers (growing fast)
- Builders, contractors, and electricians
- Home Depot / Lowe's as retail partners
- Some trade designers (but not the primary buyer)

### Representative accounts
| Company | $/Unit | Company Revenue | Channels |
|---------|--------|-----------------|----------|
| Savoy House | $59 | $50M | Omnichannel |
| Capital Lighting | $104 | $6M | DTC + Trade |
| Golden Lighting | $95 | $10M | Omnichannel |
| Craftmade | $41 | $9M | DTC + Trade |
| Magnussen Home | $149 | $10M | Omnichannel |
| Sauder Woodworking | — | $59M | DTC + Trade |
| Designer's Fountain | — | $39M | Trade Only |
| Legrand US | — | $5M | Trade Only |

### Key commercial truth
These companies are in a distribution arms race. They need to be wherever a buyer might look — Amazon, Wayfair, Lowe's, independent showrooms, AND their own site. Their competitive advantage is **availability and catalog breadth**, not exclusivity or specification prestige.

Their eCat is a **wholesale ordering tool for their dealer channel**, which is ONE of their many channels. Most of their volume probably comes from big-box POs and marketplace orders that never touch eCat.

---

## Segment 4: Volume Distribution

**12 accounts | $179,276 ARR | Median unit price: $4**

### What they are
Companies selling high volumes of low-priced products (<$30/unit) through wholesale, mass retail, and marketplace channels. Their buyer is a category manager at a chain or a purchasing agent at a distribution company — not a designer or consumer.

### How they sell
- Purchase orders from major retail chains (Walmart, Target, Costco, Home Depot)
- Marketplace presence (Amazon, often seller-fulfilled or wholesale to marketplace)
- Trade shows (AmericasMart, housewares/gift shows)
- Category management: planogram placement, shelf space negotiation
- High MOQs, container-direct from overseas manufacturing

### Who buys
- Category managers at big-box retailers
- Regional distributors and wholesalers
- Convenience/drug/grocery chain buyers
- Mass marketplace shoppers (high volume, low price)

### Representative accounts
| Company | $/Unit | Company Revenue | Core Channel |
|---------|--------|-----------------|--------------|
| Bulbrite | $3 | $9M | Omnichannel |
| Kennedy International | $4 | $1M | Omnichannel |
| Home Essentials & Beyond | $4 | $50M | Omnichannel |
| Moda at Home | $7 | $31M | Marketplace + Trade |
| Abaline Supply | $28 | $2M | DTC + Trade |
| ELICO LTD | — | $105M | Omnichannel |
| Godinger Silver Art | — | $26M | Omnichannel |
| Groupe Courchesne | — | $18M | DTC + Trade |

### Key commercial truth
These companies move tens of thousands of units. Their rep's iPad is a **territory management and order-capture tool** — the rep visits retail stores, checks planograms, writes reorders. The order value per line is low but the velocity is high.

Their selling conversation is about margins, minimums, freight, and fill rates — not about design, finish, or specification. They may submit MORE orders through eCat than a luxury company because their reps are writing orders in the field every day.

---

## Segment 5: Specialty/Non-Traditional

**4 accounts | $63,425 ARR**

Companies that don't fit the furniture/lighting trade model:
- **Ideal Living** — DTC wellness tech (AirDoctor, AquaTru)
- **America's Backyards** — Custom pool/spa builder + patio furniture retail
- **Sabine Pools, Spas, & Furniture** — Local retail + service business
- **Tomlinson Companies** — Local furniture retail/showroom

These are unique businesses using eCat in non-standard ways.

---

## What This Means for SuperCat

> **Note:** The following are strategic hypotheses informed by the segment definitions above. They are not yet validated against commercial outcome data (retention, expansion, churn by segment). They represent logical implications to test, not confirmed findings.

### Pricing and packaging implications
| Segment | What they need from eCat | Price sensitivity |
|---------|--------------------------|-------------------|
| Luxury Spec | Digital briefcase for showroom selling + project management | Low — they pay for a tool that makes reps look good |
| Premium Brand | Trade portal + DTC catalog + maybe B2B commerce | Medium — comparing against building their own |
| Mid-Market | One of many ordering channels, dealer portal, product feeds | Higher — comparing against alternatives |
| Volume Dist | Territory management, high-volume order capture, quick reorder | Higher — pure ROI calculation |

### CS resource allocation
| Segment | Right CS motion |
|---------|-----------------|
| Luxury Spec | White-glove onboarding, catalog presentation quality, showroom mode |
| Premium Brand | Commerce enablement, DTC integration, multi-channel strategy |
| Mid-Market | Efficiency, self-serve, fast import/export, integrations |
| Volume Dist | Account health monitoring, renewal focus, usage-based value proof |

### Expansion plays
| Segment | Natural expansion |
|---------|-------------------|
| Luxury Spec | eCat Online (buyer portal for their designers), more users/reps |
| Premium Brand | Sales Portal (intelligence), eCat Online (B2B commerce) |
| Mid-Market | Additional product modules, integration marketplace |
| Volume Dist | More users (scale-based), territory/analytics features |

---

## Summary

This segmentation answers: **"What is this company's actual business?"** — not "How much do they use our product?"

**109 accounts.** Classifications are derived primarily from external enrichment (scraped website descriptions) validated where possible against first-party data (ERP sales_data for unit price, catalog products.net_price as fallback). Price data exists for 63 of 109 accounts; for the remaining ~46, classification rests on enrichment alone. This is the best classification achievable from available data — not ground-truth-verified commercial reality for most accounts.

A company like Abaline Supply ($28/unit, 8,381 eCat order submissions) and a company like Theodore Alexander ($907/unit, 0 eCat order submissions) are in *fundamentally different businesses* — but both may be equally valuable SuperCat clients. One uses eCat as a field ordering tool because their reps write hundreds of small orders daily. The other uses eCat as a digital showroom because their designers browse and specify but orders consummate elsewhere.

Neither usage pattern is "better" or "worse." They're just different businesses selling different products to different buyers through different channels.
