# SuperCat Customer Segmentation — Executive Report

**Date:** June 29, 2026  
**Analyst:** Customer Intelligence / Strategy  
**Dataset:** 110 active accounts, usage + enrichment data  
**Total Book:** $1.95M ARR across 110 accounts

---

## CRITICAL FRAME: What This Data Can and Cannot Tell Us

### The Commerce Distortion

SuperCat's order data captures a **narrow slice** of how customers actually transact. The typical flow:

```
Rep uses iPad → shows catalog / builds quote → sends order to HQ →
HQ audits → keys into ERP → order is consummated
```

eCat is the **selling tool**, not the **order-of-record system**. Nearly zero customers route 100% of their orders straight from iPad to ERP. What flows through eCat's transaction layer is some combination of:
- Orders submitted by reps via iPad (which still get audited at HQ before fulfillment)
- Buyer self-service orders via eOL portal (a minority channel for most)
- A large unknown volume that never touches eCat's order system at all (phone, email, EDI, manual entry)

**Implication:** eCat order volume is NOT a proxy for "how much this customer sells" or even "how important SuperCat is to their business." It's a proxy for "how much of their order flow they've chosen to formalize through SuperCat's submission layer." A company with 0 eCat orders but 80 reps logging in daily at 100 logins/user is getting massive value from the platform — they just consummate orders elsewhere.

### What We CAN Measure (Reliable Signals)

| Signal | What it actually tells us |
|--------|--------------------------|
| **Logins/Active user** | How deeply reps live in the app day-to-day — the best available proxy for platform value without ERP data |
| **Active users / Billable users** | Team penetration — what % of their sales org is on the platform |
| **Total products / Total customers loaded** | How much of their business data lives in SuperCat (switching cost proxy) |
| **Feature: eOL Cart/Portal** | Whether they've extended beyond rep-tool to buyer self-service |
| **eOL orders (when > 0)** | Confirmed buyer self-service adoption — a distinct commercial motion, not just a volume indicator |

### What We CANNOT Measure (The Blind Spot)

| Blind spot | Why it matters |
|-----------|----------------|
| Total order volume (all channels) | Can't calculate wallet share or platform ROI |
| Rep activity → consummated revenue link | Can't prove SuperCat drives revenue without ERP closed-loop |
| Whether "zero orders" = catalog-only use vs. dormant | Can't distinguish valid use case from churn risk |
| Order velocity trend | Lifetime totals without timestamps give no trajectory |

**The single biggest analytical unlock: ERP integration data.** Until SuperCat can see consummated orders (even at aggregate level per account), all commercial analysis is working from a distorted partial view.

---

## THE REVISED SEGMENTATION

Given the commerce distortion, the primary axis shifts from **order volume** to **platform engagement pattern** — specifically, *how* the customer uses SuperCat in their selling workflow, measured by the signals we can actually trust.

---

### Segment 1: "Revenue Engines" — Deep Transactional Dependency
**~18 accounts | Median ARR: $26K | ~24% of total book ARR**

**Definition:** Order count > 500 AND Customers ordering > 100 AND Logins/Active user > 30

**Who they are:** The rare accounts that have actually routed significant order volume through SuperCat's transaction layer. Their buyers place hundreds to thousands of orders through the platform annually. Whether or not this represents their *full* order volume, they've built real workflow dependency on eCat as an order submission system — not just a catalog.

**Examples:** Gabriella White, Gabby, RENWIL, Jamie Young, Summer Classics, Abaline Supply, Pioneer Morton, Wildwood/Chelsea House

**What's actually happening:** These companies have either (a) integrated eCat deeply enough into their order workflow that reps submit through the app as standard practice, or (b) activated buyer self-service via eOL at scale, or (c) both. They represent the full realized potential of the platform.

**CS motion:**
- Protect at all costs — these accounts have genuine switching cost
- Expansion: CPQ, credit card processing, additional eOL features
- Use as reference accounts and case studies for other segments
- Monitor login decline as early warning (orders alone won't alert you to disengagement)

---

### Segment 2: "The Daily Drivers" — High Rep Engagement, Low/No Transaction Flow
**~21 accounts | Median ARR: $22K**

**Definition:** Logins/Active user > 40 AND Active users > 20 AND (Order count < 100 OR orders are predominantly iPad-submitted without eOL)

**Who they are:** Manufacturers whose reps live in eCat daily — logging in 40–130+ times each — but consummate most orders outside the platform. The app is their primary selling tool (presentations, catalog, pricing lookup, quote generation) even though the order-of-record lives in their ERP. This is a **valid, high-value use case**, not a failure to activate.

**Examples:** Palecek (143 billable users, 110 active), Hubbardton Forge (112 users), Crystorama (88 users), Eurofase (98 users), Capital Lighting (88 users), Universal Furniture (95 users)

**What's actually happening:** These are often larger lighting and furniture companies with established ERP-based order processing. Their reps use eCat as the field selling interface — browse products, show customers, check inventory, look up pricing — then submit orders through their existing channels. eCat is the *front-end* to their selling process, not the *transaction system*.

**CS motion:**
- Do NOT treat low eCat order count as disengagement — login intensity confirms high value
- Expansion: eOL buyer portal (let their dealers do what reps do — browse/search/self-serve)
- Expansion: Deeper ERP integration that closes the loop (if SuperCat develops this)
- Protect by ensuring the catalog/presentation experience stays best-in-class
- These accounts are the strongest candidates for an "order capture" motion — can we make it easier for the rep to submit through eCat vs. email/phone? What's blocking them?

---

### Segment 3: "The Digital Storefronts" — Buyer Self-Service Activated
**~18 accounts | Median ARR: $24K**

**Definition:** Number of eOL orders > 50 AND Feature: eOL Cart = Y

**Who they are:** The subset that has successfully shifted ordering from rep-pushed to buyer-pulled via the eOL portal. Their *buyers* log in, browse, and transact — meaning SuperCat is not just a rep tool but a buyer-facing commerce channel.

**Examples:** Wildwood/Chelsea House (1,290 eOL orders), Jamie Young (965), Bulbrite (746), Four Seasons (604), Linon/Powell (353), Charleston Forge (327), Summer Classics (284)

**What's actually happening:** This is the most commercially evolved segment. They've built a distinct commerce channel through SuperCat that generates orders *without rep intervention*. In the context of the commerce distortion, these are the accounts where SuperCat genuinely IS the order system for a meaningful chunk of volume — specifically the buyer-initiated chunk.

**CS motion:**
- Highest expansion potential: CPQ, credit card, more eOL features
- Monitor buyer adoption metrics (unique buyers ordering, buyer activation rate)
- These accounts prove the eOL value prop — use their metrics in expansion pitches to Field Warriors
- 10 accounts in this segment have eOL orders exceeding their iPad orders — they've flipped the primary ordering surface

**Key insight:** Only 28 of 110 accounts (25%) have any eOL orders at all. Of those, 18 have meaningful volume. eOL remains the single biggest expansion whitespace in the book.

---

### Segment 4: "The Ramp" — Early Lifecycle or Light Engagement
**~25 accounts | Median ARR: $11K | Median Active Users: 24**

**Definition:** Order count 1–100 AND Logins/Active user 5–30 AND Billable users < 40

**Who they are:** Smaller or newer deployments where the platform is live but hasn't become central to the selling motion. Reps log in periodically, place some orders, but eCat isn't yet the daily tool. Could be early in their adoption curve or at their natural ceiling.

**What's actually happening (the commerce context reframe):** Some of these are genuinely early. Others are small companies where 5 reps and 30 orders *is* full adoption — they just don't have 80-person sales teams. The critical question is: **is their current usage proportional to their selling operation, or is there untapped headroom?**

This is where commercial profile (Approach B) becomes the essential overlay:
- A "Ramp" account with $50M revenue and 200 employees → massive headroom, invest in activation
- A "Ramp" account with $3M revenue and 8 employees → may already be at ceiling, maintain but don't over-invest

**CS motion:**
- Triage using company revenue/employee count to separate "early" from "ceiling"
- For high-headroom accounts: dedicated activation push (training, data optimization, success metrics)
- For ceiling accounts: lightweight touch, ensure renewals, don't over-invest

---

### Segment 5: "The Question Marks" — Zero Transactional Signal
**~26 accounts | Median ARR: $9K | Median Cohort Year: 2018**

**Definition:** Order count = 0 (both iPad and eOL)

**Who they are:** Accounts with zero orders through the platform. Under the old lens, these looked like failures. Under the commerce context reframe, they split into at least three sub-populations:

1. **Catalog-only deployments (valid):** Paying for eCat as a digital catalog and rep presentation tool. Orders consummate elsewhere by design. Value is real — just not transactional.
2. **Pre-launch / stalled implementations:** Signed up, loaded data, never fully rolled out to the sales team. The 2024–2025 cohort accounts likely fall here.
3. **Truly dormant:** Signed years ago, reps stopped using it, no one's paying attention. The 2011–2016 cohort accounts with low login counts fall here.

**The critical diagnostic:** Logins/Active user separates these sub-populations.
- Zero orders BUT Logins/Active user > 20 → Catalog-only use (valid)
- Zero orders AND Logins/Active user < 5 → Likely dormant (churn risk)

**Looking at the data:**
- 25 zero-order accounts
- Of these: ~8 have Logins/Active user > 15 (likely catalog-only — legitimate use)
- Of these: ~12 have Logins/Active user < 5 (likely dormant — high churn risk)
- Of these: ~5 are ambiguous (moderate logins, unclear intent)

**CS motion:**
- Immediately separate catalog-only (no action needed beyond renewal) from dormant (intervention required)
- For catalog-only: validate with the client that this is intentional; document in CRM so they don't get misclassified in future reviews
- For dormant: save-or-sunset conversation. What happened? Is there a new champion? Or is this a clean churn candidate?
- For stalled implementations: reactivation campaign with fresh onboarding resources
- **$233K in ARR sits in this segment** — the save/activate decision matters financially

---

## THE COMMERCIAL PROFILE OVERLAY

The usage segments above drive weekly CS operations. The commercial profile overlay drives *strategic targeting* — who to pitch what, who has headroom, and what their natural tier ceiling is.

### Overlay Dimension 1: Selling Motion (How They Go to Market)

| Profile | Count | Defining Traits | SuperCat Fit | Natural Tier Ceiling |
|---------|-------|-----------------|--------------|---------------------|
| **Pure Dealer/Trade** | ~16 | Sells exclusively through dealer networks and trade programs. No DTC. | Perfect core ICP. iPad for reps visiting dealers, eOL for dealer self-service ordering. | T2–T3 depending on dealer count |
| **Multi-Channel Operator** | ~29 | 6+ channels: dealer + direct + trade + contract/hospitality. Complex GTM. | High fit but complex needs. Multiple pricing tiers, multiple buyer types, more configuration. | T3+ (highest ceiling) |
| **Lighting Specialist** | ~35 | Decorative/commercial lighting. High SKU counts (fixtures × finishes × sizes). Dealer-driven. | Strong fit. Matrix options, large catalogs, showroom-centric selling. | T2–T3 |
| **Emerging Brand** | ~15 | <$10M revenue, <50 employees, ≤5 channels. Building their GTM. | Good entry point. Will grow into other profiles if successful. | T1–T2 today, rising |
| **Enterprise Holdout** | ~9 | >$50M revenue or 200+ employees — but ARR < $20K. Under-deployed. | Massive headroom if champion exists. Organizational inertia is the blocker. | T3+ (if you can get penetration) |

### Overlay Dimension 2: The Selling Context

This is the dimension that matters most for **product positioning and feature development** — and where Postgres-level data (product types, price points, customer records) would be transformative:

| Selling Context | What They're Doing | What They Need From SuperCat |
|----------------|-------------------|-------------------------------|
| **Lighting → Showrooms & Builders** | High-SKU catalog (1,000–10,000+ items), specification selling, AOR (agent of record) relationships, spec-driven projects with long cycles | Fast product search/filter by spec, finish matrix options, project/quote tracking, showroom inventory visibility |
| **Furniture → Trade & Retailers** | Curated collections, seasonal launches, showroom appointments (HPMKT etc.), dealer stock orders + custom/COM orders | Collection-based presentation, COM/customization support, order templates for reorders, buyer portal for dealer stock replenishment |
| **Accessories/Décor → Volume Wholesale** | High-volume, lower-AOV, many SKUs turning fast, price-sensitive buyers | Quick order entry, inventory-forward views, promotional pricing, buyer self-service for reorders |
| **Outdoor/Specialty → Seasonal + Project** | Seasonal buying cycles, project-based (hospitality, pools, commercial), longer lead times | Lead time/availability visibility, project quoting, seasonal catalog management |

**This is where Postgres data would be a massive unlock.** If we could pull — per org — actual product type distribution, average price points, customer record structure (dealer vs. direct vs. contract), and option/configuration complexity, we could assign each account to a selling context bucket with data, not inference. The enrichment fields give us a directional view, but org-level Postgres queries would provide ground truth.

---

## RECOMMENDED OPERATING MODEL

### Primary: Usage-Based Segmentation (5 segments above)
- Drives daily/weekly CS operations
- Auto-classifying from existing data
- Translates directly into differentiated playbooks
- Scales without additional data collection

### Overlay: Commercial Profile (applied within segments for prioritization)
- Determines which "Ramp" accounts deserve investment vs. maintenance
- Identifies natural tier ceiling for expansion conversations
- Informs feature-specific upsell messaging (eOL pitch differs by selling context)
- Refreshed quarterly, not daily

### Modifiers (sort criteria within segments, not standalone axes):
- **Tenure (Cohort Year):** Veteran Ghost Accounts are more urgent than new ones. New Revenue Engines need less attention than established ones.
- **ARR:** Higher ARR = higher stakes for any intervention. But ARR alone doesn't determine segment or playbook.

---

## DATA HARDENING PRIORITIES (Revised)

Ranked by impact given the commerce distortion:

### Tier 1: Closes the Loop (Transformative)

| Data Point | What It Reveals | Source |
|-----------|----------------|--------|
| **ERP order/invoice data (even aggregate)** | Actual consummated revenue per account. Wallet share. Whether eCat activity correlates with sales outcomes. | Client ERP exports, EDI feeds, or even self-reported annual revenue through the platform. Start with top 20 accounts. |
| **Login recency + 90-day trend** | Whether engagement is current, growing, or declining. Immediately separates active catalog users from dormant accounts in the "Question Marks" segment. | Product telemetry — SuperCat already tracks this. Add `last_login_date` and `logins_last_90d` to reporting. |
| **Postgres org-level profile data** | Product type distribution, price point ranges, customer record structure, option complexity per org. Assigns selling context with data instead of inference. | `supercat-postgres-vpn` MCP — queryable today. Would be the first time segmentation has been informed by actual platform data at depth. |

### Tier 2: Sharpens Prioritization (High Value)

| Data Point | What It Reveals | Source |
|-----------|----------------|--------|
| **NPS/CSAT per account** | Satisfaction independent of usage. Separates "happy catalog user" from "trapped and frustrated." Identifies at-risk Revenue Engines. | Quarterly email survey (Delighted/Wootric). 110 accounts = achievable response rates. |
| **Contract renewal date** | When the save-or-expand conversation must happen. Time-bounds all interventions. | Billing system / HubSpot. Almost certainly exists somewhere — needs to be surfaced. |
| **Support ticket volume + category** | Which accounts consume disproportionate support. Segments product friction patterns. | HelpScout or equivalent. Tag by account, categorize, export quarterly. |

### Tier 3: Completes the Picture (Strategic)

| Data Point | What It Reveals | Source |
|-----------|----------------|--------|
| **Champion/decision-maker contact health** | Whether there's a path to expand vs. just maintaining. Enterprise Holdouts without exec contact are dead ends. | HubSpot contact records. Track last meeting with economic buyer. |
| **Self-reported platform purpose** | Whether zero-order accounts are catalog-only by design or accidentally dormant. Eliminates guesswork in the Question Marks segment. | Single-question survey or onboarding tag: "What's your primary use case for eCat?" |
| **Rep activity patterns (non-order)** | What reps actually DO in the app: browse products, check inventory, generate quotes, download tearsheets. This is the Tier 1 insight path when you can't close the loop to ERP. | Product telemetry. Event-level data on feature usage per session. |

---

## STRATEGIC IMPLICATIONS

### For the Insightful Product / Intelligence Report

The commerce distortion means the Insightful report **must lead with what we CAN say** (rep behavior, platform engagement, catalog utilization) and be transparent about what we **cannot say** (revenue attribution, order closure rates). For Tier 1 clients without ERP integration:

- Lead with rep engagement metrics (login frequency, feature usage, catalog breadth explored)
- Show customer activation rates (% of loaded customers who interact via eOL)
- Flag opportunity gaps (large customer lists with low buyer activation = untapped potential)
- Explicitly disclaim: "eCat order data represents submitted orders through the platform; total commercial activity includes orders consummated via other channels"

For Tier 2/3 clients with ERP data: close the loop, show actual revenue attribution.

### For Rep Copilot / Brent Sanders Context

The selling context dimension is directly relevant to how a rep copilot should behave:
- A lighting rep selling to a showroom buyer needs spec sheets, finish options, lead times, and project context
- A furniture rep selling to a retailer needs collection decks, promotional pricing, and reorder history
- The copilot's conversational mode should adapt to the selling context of the org it's deployed in

### For Pricing Migration

The segmentation reveals that ~26 "Question Mark" accounts ($233K ARR) need resolution before any pricing migration. Are they catalog-only (reprice accordingly, possibly into a lighter tier) or dormant (at risk of churning during a price increase)? Migrating pricing without first clarifying intent in this segment invites unnecessary churn.

---

## APPENDIX: SEGMENT ASSIGNMENT COUNTS

| Segment | Accounts | ARR | % of Book |
|---------|----------|-----|-----------|
| Revenue Engines | 18 | ~$471K | 24% |
| Daily Drivers | 21 | ~$462K | 24% |
| Digital Storefronts | 18 | ~$439K | 23% |
| The Ramp | 25 | ~$279K | 14% |
| Question Marks | 26 | ~$233K | 12% |
| **Total** | **110** | **$1.95M** | **100%** |

*Note: Some accounts could qualify for multiple segments (e.g., a Revenue Engine that is also a Digital Storefront). In those cases, assign to the segment that drives the primary CS playbook — typically the one representing their dominant usage pattern.*

---

## NEXT STEPS

1. **Immediate (this week):** Pull login recency data from product telemetry. Separate Question Marks into "catalog-only active" vs. "truly dormant." Size the actual churn-risk pool.

2. **Near-term (30 days):** Run Postgres org-level queries across the top 30 accounts to validate selling context assignment. Test whether product type + price point + customer structure data matches the enrichment-derived profiles.

3. **Medium-term (60 days):** Pilot ERP data collection with 5 willing Revenue Engine accounts. Even self-reported "total annual order volume" would allow wallet share calculation.

4. **Quarterly:** Refresh segmentation with updated login/order data. Move accounts between segments as behavior changes. Report on segment-level retention and expansion rates.

---

*This analysis acknowledges a fundamental constraint: without ERP closed-loop data, SuperCat's view of commercial reality is partial. The segmentation is built on what we can reliably observe (engagement, feature adoption, platform configuration) rather than what we wish we could measure (total revenue influence). The data hardening roadmap is designed to progressively close this gap.*
