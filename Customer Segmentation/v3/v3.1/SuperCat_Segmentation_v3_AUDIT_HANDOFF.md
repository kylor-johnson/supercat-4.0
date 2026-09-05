# Audit Handoff: SuperCat Client Segmentation v3

## Your task

You are auditing a customer segmentation model before it goes to SuperCat's leadership team. Your job is to stress-test it for accuracy, completeness, logical consistency, and actionability. You have no stake in the outcome — flag everything that doesn't hold up.

---

## Context you need

**SuperCat Solutions** is a B2B SaaS company serving ~110 furniture, lighting, and home goods manufacturers. Products: eCat iPad (offline rep app for field selling), eCat Online (buyer-facing B2B portal), Sales Portal, Admin Console. Three pricing tiers: T1 $749/mo, T2 $1,295/mo, T3 $2,295/mo, plus per-user overages.

**The segmentation being audited** is v3. It segments SuperCat's clients by their external business model (how they sell, who they sell to, what they sell) rather than by how they use eCat. This was a deliberate pivot after v1 (price-point-based) and v2 (eCat behavioral engagement) were both rejected by the author as too eCat-centric.

**The report to audit:** `/Users/kylorjohnson/Downloads/SuperCat_Client_Segmentation_v3.md`

**The underlying data (CSV with all 110 accounts and their assignments):** `/Users/kylorjohnson/Downloads/SuperCat_Customer_Segmentation_v3_Business_Model.csv`

**The original enrichment source (CSV with "How They Sell", "Who They Sell To", channel flags, Product Type):** `/Users/kylorjohnson/Downloads/Copy of Customer & Prospect TAM enriched - Customers.csv` (header row is row 2)

**Master account data (ARR, health scores, tiers, parent entities):** `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_master-account-data-v6.2.csv` (header row is row 2)

**Entity roll-up data (parent/child brand relationships):** `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_master-entity-data-v6.2.csv` (header row is row 2)

---

## Live data access

You have access to two MCP integrations for ground-truth verification:

- **`user-supercat-postgres-vpn`** — Production Postgres database. Tables include: `organizations`, `products`, `customers`, `sales_data`, `login_events`, `orders`. Use for verifying price points, buyer counts, order patterns, catalog size.

- **`user-bigquery-admin`** — BigQuery data warehouse. Dataset `insightful_product.org_master_with_segments` contains Mixpanel behavioral data (logins, order submissions, feature usage, pre-computed segments). Use to cross-reference eCat engagement against segment placement.

---

## What to audit

### 1. Segment boundaries and placements
- Are the 4 segment definitions mutually exclusive and collectively exhaustive?
- Spot-check 10–15 specific account placements against the enrichment CSV data. Does the "How They Sell" and "Who They Sell To" description match the segment they landed in?
- Are there accounts that obviously belong in a different segment? (e.g., a company described as "trade-only, showroom-only, no public checkout" placed in "Mid-Market Multi-Channel")
- The model was built with manual overrides for all 110 accounts. Are those overrides defensible?

### 2. Price data accuracy
- Price points come from ERP `sales_data` (avg unit price = total amount_invoiced / total qty) with a catalog `products.net_price` fallback. Only ~62 of 110 accounts have ERP price data; others have catalog data or nothing.
- Spot-check 5–8 prices against Postgres `sales_data` and/or `products` tables. Are they correct?
- Are there accounts placed in "Luxury Specification" that actually sell cheap products, or "Volume Distribution" accounts that actually sell expensive products?

### 3. Go-to-market classification accuracy
- The "go_to_market" field was derived by parsing the "How They Sell" text for keywords: "shopify/checkout/add to cart" → DTC; "amazon/wayfair/home depot/marketplace" → Marketplace. Everything else → Trade Only.
- Is this keyword logic too aggressive or too lenient? Are there clear false positives/negatives?
- Cross-check 5–10 accounts: does their actual website and business match the GTM classification?

### 4. Data gaps and their impact
- 48 of 110 accounts have no ERP price data. How does this affect segment placement reliability?
- Channel flags in the CSV are 1/0 (not Y/N). The "Has eCommerce" flag is only 1 for 14 accounts — does this match reality for companies that obviously sell online?
- Are there key fields in the source CSVs that were ignored but would sharpen the model?

### 5. Portfolio/entity consolidation
- Visual Comfort has 4 orgs (VC Modern, VC Signature, VC Studio/Fans, VC Europe). Theodore Alexander has 3. Jonathan Charles has 2. Gabriella White has 2+ (Gabby, Gabriella White, Summer Classics, Summer Classics Contract share an entity).
- Are portfolio members always in the same segment? If not, is that a problem or actually correct?
- Does treating them individually inflate segment counts artificially?

### 6. Actionability for leadership
- Can a CEO read this and know what to do differently tomorrow?
- Are the "What This Means for SuperCat" implications actually supported by the segment definitions, or are they aspirational?
- Is there anything in this report that leadership could act on that would be WRONG based on the data?

### 7. What's missing
- What questions would a CEO or Head of CS immediately ask that this report can't answer?
- Does the model say anything about retention risk, expansion likelihood, or lifetime value?
- Is there a dimension of "how they sell" that the model ignores?

---

## How to conduct the audit

1. Read the report in full first.
2. Load the segmentation CSV and cross-reference specific accounts.
3. Use Postgres/BigQuery to spot-check 10–15 data points (prices, buyer counts, login activity).
4. Look for internal contradictions (e.g., a claim in the report contradicted by the underlying data).
5. Identify the 3–5 most consequential potential errors — things that, if wrong, would lead leadership to make bad decisions.

---

## What to produce

Write a structured audit with:
- **VERDICT**: Is this model ready to present to leadership? (Yes with caveats / No, fix X first)
- **CONFIRMED**: Claims in the report that check out against data
- **CONTRADICTED**: Claims that the data actively disproves
- **MISCLASSIFIED**: Specific accounts that belong in a different segment (with evidence)
- **MISSING**: Important context or caveats not in the report that leadership needs
- **RECOMMENDATIONS**: Specific fixes before presenting (ranked by impact)

Save your audit to: `/Users/kylorjohnson/Downloads/SuperCat_Segmentation_v3_AUDIT.md`

---

## Important constraints

- You are NOT the author of this model. You have no reason to defend or validate it.
- If the model is fundamentally wrong, say so directly.
- If it's mostly right with edge-case issues, say that too.
- Do not suggest alternative models. Your job is to audit THIS one.
- Use actual data to support every claim. No hand-waving.
- Do not use eCat behavioral data (logins, order submissions) as evidence that a segment placement is wrong — that's the exact bias this model was built to avoid. However, you CAN note where eCat behavior is wildly inconsistent with a segment's described selling motion, as that may indicate a misclassification.
