# How We Got Here: Client Segmentation v3

**Internal context document — July 2026**

---

## The short version

We stopped segmenting clients by how they use eCat and started segmenting them by how they run their businesses. The result is four segments across 109 accounts that describe *what these companies actually are* — not how much they log in.

---

## Why we needed a new approach

### What v1 and v2 did

Previous segmentation attempts grouped clients by **eCat behavior** — logins, order submissions, feature adoption, support tickets. That told us about product engagement. It was useful for identifying at-risk accounts and planning CS touches.

But it couldn't answer the questions that matter for pricing, packaging, positioning, and product roadmap:

- Why does one client submit 8,000 orders and another submits zero — and both renew happily?
- Why does white-glove onboarding delight some clients and feel like overhead to others?
- Why do some clients compare us to Shopify B2B and others compare us to nothing?

### The core problem

Usage-based segmentation treats all clients as if they're playing the same game at different skill levels. They're not. They're playing different games entirely.

A luxury furniture company selling $900 chandeliers to interior designers through showrooms is a fundamentally different business than a housewares company selling $4 items to category managers at Walmart. Both use eCat. Both pay us money. But their needs, their price sensitivity, their expansion potential, and the right way to serve them have almost nothing in common.

We were one-size-fitting a portfolio that contains at least four very different business models.

---

## What changed in v3

### The new segmentation axis

Instead of "How do they use eCat?", v3 asks three questions:

1. **What do they sell?** — product type and price point
2. **How do they sell it?** — trade-only, DTC + trade, marketplace, omnichannel
3. **Who buys from them?** — designers, retail chains, consumers, hospitality

eCat usage is deliberately excluded from the classification. A company's segment is determined by its business model, not by its engagement with our product.

### Data sources

| Source | What it gave us | Coverage |
|--------|-----------------|----------|
| HubSpot enrichment CSV | Channel flags, "How They Sell", "Who They Sell To", company revenue (scraped from websites) | All 109 accounts |
| ERP `sales_data` | Average unit price per org (transaction-level) | 63 of 109 accounts |
| Master account data | ARR, health score, contract status | All accounts |
| Product catalog (`products.net_price`) | Fallback unit price from catalog when ERP data unavailable | Supplemental |

Price data exists for 63 of 109 accounts. For the remaining ~46, classification relies on enrichment data (website descriptions, channel flags) alone.

### The resulting segments

| # | Segment | Accounts | ARR | Med $/Unit | One-liner |
|---|---------|----------|-----|------------|-----------|
| 1 | Luxury Specification | 36 | $630K | $892 | Sells to designers who *specify* products for projects |
| 2 | Premium Trade Brand | 33 | $677K | $354 | Building a brand across trade + consumer channels |
| 3 | Mid-Market Multi-Channel | 24 | $392K | $60 | Competes on availability and distribution breadth |
| 4 | Volume Distribution | 12 | $179K | $4 | Sells to category managers at chains |

Plus 4 Specialty accounts ($63K ARR) that don't fit the model. **109 total.**

---

## The journey: v1 → v2 → v3

### v1 — Usage tiers

Grouped clients into high/medium/low engagement buckets based on logins and order volume. Useful for CS prioritization. Not useful for anything strategic — it just told us who was active.

### v2 — Behavioral clusters

Added feature adoption and support patterns. Better for predicting churn risk. Still couldn't explain *why* clients used eCat differently or what they actually needed from us.

### v3 — Business model segmentation

Flipped the lens entirely. Instead of starting with our product and measuring how clients interact with it, we started with the client's business and asked what role eCat plays in it.

**Key insight that triggered the shift:** Theodore Alexander ($907/unit, 0 eCat order submissions) and Abaline Supply ($28/unit, 8,381 eCat order submissions) are both healthy accounts — but previous segmentation models would put Theodore Alexander in the "disengaged/at-risk" bucket and Abaline in the "power user" bucket. That's backwards. Theodore Alexander's orders consummate in their ERP after a custom configuration process; eCat is their digital showroom. Abaline's reps write field orders on iPads every day; eCat is their order-capture system. Both are using the product exactly as their business requires.

### v3.1 — Post-audit corrections

Three corrections after manual review:

- **Bliss Studio** reclassified from Mid-Market to Luxury Specification — the enrichment scraper had pulled data from Bliss Hammocks (a different company). First-party catalog data showed avg unit price of $1,900.
- **Staging org removed** — brought the count from 110 to 109 real accounts.
- **GTM label fix** — "Marketplace + Trade" was misleading for luxury accounts whose "marketplace" presence was curated sites like Lumens and Lightology, not mass marketplaces. Corrected to "Trade + Select Retailers."

---

## What we know vs. what we're hypothesizing

### Confirmed (data-backed)

- The four segments exist and are distinguishable by price point, channel mix, and buyer type
- Price data validates the segmentation for 63 of 109 accounts
- The segments produce meaningfully different ARR distributions and unit economics
- Multi-org entities (Theodore Alexander × 3, Visual Comfort × 3, etc.) cluster correctly by selling motion even when individual orgs vary in price point

### Hypothesized (logical but unvalidated)

- That these segments predict different **price sensitivity** to SuperCat
- That they require different **CS motions** (white-glove vs. self-serve vs. commerce enablement)
- That they have different **expansion paths** (eCat Online vs. Sales Portal vs. integrations)
- That retention and churn patterns differ by segment

We have not yet run retention/expansion/churn analysis against these segments. The strategic implications in the segmentation doc are hypotheses to test, not findings.

---

## Known limitations

1. **Enrichment quality varies.** ~46 accounts are classified on scraped website descriptions alone, with no first-party price data to validate. Some scrapes were wrong (Bliss Studio / Bliss Hammocks). Others may be too.

2. **ARR double-counting.** Multi-org entities share billing. Segment ARR totals overcount by ~14% in Luxury Spec due to Theodore Alexander (3 orgs), Visual Comfort (3 orgs), Gabriella White (2 orgs), and Jonathan Charles (2 orgs).

3. **Segment boundaries are fuzzy.** Luxury Spec and Premium Trade Brand overlap in the $350–$715 price range. The distinguishing factor is selling motion (specify-for-client vs. choose-a-brand), which is a judgment call, not a numeric threshold.

4. **Specialty is a catch-all.** Four accounts (Ideal Living, America's Backyards, Sabine Pools, Tomlinson Companies) don't fit the model. They're real clients with real revenue, but the segmentation framework doesn't describe their businesses well.

---

## What this unlocks next

With a business-model segmentation in place, we can now:

- **Test pricing and packaging** against actual client economics instead of usage tiers
- **Differentiate CS playbooks** by segment instead of running one onboarding motion for everyone
- **Prioritize product roadmap** by understanding which features serve which business models
- **Score expansion opportunities** by matching our product capabilities to each segment's natural next need
- **Run churn analysis** against segments to see if business model predicts retention better than engagement metrics

None of that was possible when we only knew how much clients clicked around in eCat.

---

## How to use this document

This is the backstory. The [segmentation itself](https://supercat-segmentation.pages.dev) is the reference — it has the full segment definitions, representative accounts, and strategic hypotheses.

Share this doc when someone asks "why did we redo segmentation?" or "how confident are we in these segments?" It's meant to be honest about both what we know and what we're still guessing at.
