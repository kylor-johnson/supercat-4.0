# Audit: SuperCat Client Segmentation v3

**Auditor:** Automated (Claude, via Postgres ERP/catalog data, BigQuery behavioral data, enrichment CSV, master account data, Insightful Product provenance foundation)  
**Date:** July 1, 2026  
**Scope:** Accuracy, completeness, logical consistency, actionability  
**Correction note:** Initial audit contained a biased finding (treating eCat iPad submissions as consummated orders). That finding is retracted. This version is grounded in the Provenance Spine's axioms: ERP = commercial truth; eCat orders = intent (pre-re-key); SuperCat's commerce visibility is structurally partial.

---

## VERDICT

**Yes, with caveats — presentable after 3 targeted fixes (~45 minutes).**

The model's architecture is sound. Segmenting by external business model (how they sell, who they sell to, what they sell) rather than eCat usage is the correct pivot from v1/v2. The four segments are conceptually clean, mostly well-defined, and the price data that DOES exist confirms the placements.

**What must be fixed:**
1. One account misclassified due to wrong-company enrichment data (Bliss Studio) — 5 min
2. GTM classification has systematic false positives for luxury brands — 30 min
3. Remove staging org + add ARR deduplication note — 10 min

**What leadership should know but the report doesn't say:**
- The model is built on EXTERNAL enrichment (scraped websites) validated where possible by INTERNAL first-party data (catalog prices, ERP sales_data). This is the best available approach given that most clients don't give SuperCat their ERP data back — but it means the model's "how they sell" classifications are marketing-copy-derived, not transaction-verified.
- Only ~20 of 110 clients have meaningful ERP data in SuperCat. For the other ~90, the ONLY ground truth is catalog data (product types, price points) and the customer file (who buys from them). The segmentation report correctly identifies external selling motion as the dimension, but the EVIDENCE base for most placements is thin.

---

## WHAT SUPERCAT CAN ACTUALLY SEE (epistemological frame)

This section doesn't exist in the report but is critical context for leadership.

**Per the Provenance Spine (validated against 21 live orgs):** SuperCat's commerce visibility is structurally partial. What we see through our rails (iPad orders + B2B commerce) is only part of any client's revenue. The rest — other online channels, EDI, manual keyed orders — reaches their ERP without touching us.

| What SuperCat has | What it tells us | Coverage |
|---|---|---|
| Product catalog (`products`) | What they SELL (types, price points) | ~100% of clients |
| Customer file (`customers`) | Who BUYS from them (billing entities, territories) | ~100% of clients |
| eCat orders (`orders`) | What reps SUBMIT through us (intent, not revenue) | ~100% of clients |
| ERP sales_data (coarse) | Total invoiced amount + qty per SKU (no dates) | ~62 of 110 |
| ERP invoices (`portal_invoices`) | True invoiced revenue with dates, line detail | ~20 of 110 |
| ERP booked orders (`portal_orders`) | Consummated/keyed orders (fallback) | ~20 of 110 |
| External enrichment (HubSpot/TAM CSV) | Scraped website descriptions of selling motion | 110 of 110 |

**The segmentation relies primarily on the bottom row** (external enrichment) to classify "how they sell" and "who they sell to." It uses ERP `sales_data` and catalog `net_price` for price-point placement. This is the best you can do today — but it means the model is built on marketing copy, not commercial transaction patterns.

**What WOULD ground-truth this model (future agent opportunity):**
- Analyze each client's `customers` table: what kinds of businesses are buying from them? (showrooms, designers, chains, distributors)
- Look at those customers' actual websites to classify them (interior design firm? big-box buyer? independent showroom?)
- Use `default_price_code` distribution as a tier signal (single code = single channel; 15+ codes = multi-tier trade program)
- Use catalog `category_code`/`collection_code` structure to type the product (decorative vs. architectural vs. consumer)
- Where ERP data exists, use invoice patterns (order size, frequency, customer concentration) to verify the selling motion

This would replace scraped enrichment with first-party transaction truth — but only where data exists, and with the explicit understanding that for most Tier 1 clients, we CANNOT close the loop to commercial outcome.

---

## CONFIRMED

Claims that check out against first-party data (Postgres `sales_data` + `products.net_price`):

| Claim | Source | Verified Value |
|-------|--------|---------------|
| Theodore Alexander avg $907/unit | ERP `sales_data` | $906.75 ✓ |
| Interlude Furniture avg $2,085/unit | ERP `sales_data` | $2,085.50 ✓ |
| Kindel Karges avg $6,828/unit | ERP `sales_data` | $6,827.83 ✓ |
| Bulbrite avg $3/unit | ERP `sales_data` | $3.08 ✓ |
| Kennedy International avg $4/unit | ERP `sales_data` | $3.68 ✓ |
| Abaline Supply avg $28/unit | ERP `sales_data` | $27.96 ✓ |
| Savoy House avg $59/unit | ERP `sales_data` | $53.87 (directionally correct) |
| VC Signature avg $364/unit | ERP `sales_data` | $363.88 ✓ |
| Palecek avg $3,626/unit | Catalog `net_price` (no ERP amount) | $3,625.53 ✓ |
| Alfonso Marina avg $12,916/unit | Catalog `net_price` | $12,916.18 ✓ |
| Charleston Forge avg $841/unit | Catalog `net_price` | $840.51 ✓ |
| Luxury Spec median $/unit = $892 | Calculated (24 priced accounts) | $892 ✓ |
| Premium Trade median = $354 | Calculated (23 priced accounts) | $354 ✓ |
| Mid-Market median = $60 | Calculated (11 priced accounts) | $60 ✓ |
| Volume Distribution median = $4 | Calculated (5 priced accounts) | $4 ✓ |
| Segment counts 36/33/24/13/4 = 110 | CSV row count | ✓ |
| 67% Premium Trade Brand do contract (most) | Channel flags | 67% vs. Lux 44%, Mid 54%, Vol 62% ✓ |
| "Orders don't consummate in eCat" (Luxury Spec) | Provenance Spine §2 | **Correct.** Almost no order flows straight from iPad to ERP. Rep submits → HQ audits → human re-keys → invoices. eCat is intent, not transaction. |

**Price methodology is sound.** Every spot-checked price matched ERP or catalog data within $6. The dual-source approach (ERP `sales_data` avg unit price as primary, catalog `products.net_price` as fallback) is legitimate and produces reliable numbers where data exists.

---

## CONTRADICTED

### ~~1. "Orders don't consummate in eCat"~~ — RETRACTED

Initial audit incorrectly treated eCat iPad submission counts as consummated orders. This violated the Provenance Spine's core axiom (§2: "An eCat order is intent, not a transaction. It may be edited, split, partially shipped, cancelled, or never keyed.") and violated the audit handoff's own constraint ("Do not use eCat behavioral data as evidence that a segment placement is wrong").

**The report's characterization is correct.** eCat is the presentation, quoting, and project-capture tool. Whether a rep submits 5,000 quotes or 0 through eCat says nothing about whether the business model is luxury specification vs. volume distribution. It only tells us how the rep uses our tool.

### 1. Interlude Home price: $1,142 (CSV) vs. $661 (ERP) vs. $878 (catalog)

The segmentation CSV reports Interlude Home at $1,142/unit. Postgres ERP `sales_data` shows $661.07 (total invoiced $13.4M / 20,217 qty). Catalog avg `net_price` is $877.86.

$1,142 matches neither first-party source. It doesn't change the segment placement (Luxury Specification is correct at any of these figures), but it's a data integrity issue — the methodology should produce numbers traceable to a source.

**Impact:** Low. Placement is correct regardless. But leadership may ask "where did $1,142 come from?" and there's no clean answer.

### 2. "Marketplace + Trade" GTM classification for luxury brands

Six Luxury Specification accounts carry "Marketplace + Trade":
- Theodore Alexander, Currey & Company, Accord Lighting, Corbett Lighting, TA Manhasset, TA Manhasset (Staging)

**What actually triggers it:** The keyword parser flags "marketplace" anywhere in the enrichment text. For these luxury brands:
- **Currey & Company:** "retail/dealer partner marketplace" in context — refers to their dealer network platform, NOT Amazon/Wayfair. Primary description: "Trade-first B2B wholesale via an online catalog gated by trade registration"
- **Accord Lighting:** Triggered by "Lumens" and "Lightology" — curated lighting showroom websites that carry trade brands. These are authorized dealers, not mass marketplaces.
- **Corbett Lighting:** The word "marketplace" appears in a distribution-partner sentence. Primary description: "B2B project sales to hospitality/commercial clients"

**Impact:** A CEO reading "Marketplace + Trade" next to Theodore Alexander would conclude they sell on Amazon. They don't. Being carried by Lumens or Lightology is the equivalent of being in an authorized showroom — it's the trade channel, not marketplace distribution. This GTM label actively misinforms.

---

## MISCLASSIFIED

### 1. Bliss Studio — Wrong Company in Enrichment Data (CRITICAL)

| Field | Enrichment Data Says | Postgres First-Party Reality |
|-------|---------------------|------------------------------|
| Product Type | "Outdoor leisure consumer goods: hammocks, hanging chairs, gravity-free chairs..." | Luxury furniture/accessories |
| How They Sell | "blisshammocks.com (Shopify), Amazon, Walmart, Target, Costco" | Trade showroom channel |
| Avg Catalog Price | (not used — no price in CSV) | **$1,900.68** across 486 active products |

**What happened:** The enrichment AI scraped **Bliss Hammocks** (blisshammocks.com — a mass-market outdoor leisure company selling $20-50 hammocks to big-box chains) instead of **Bliss Studio** (the actual SuperCat client — a luxury accessories/decor brand selling $1,900+ items through trade channels).

**Evidence:** Postgres `products` table for org `blh` (Bliss Studio) shows 486 active products with avg net_price = $1,900.68. BigQuery shows the org as "Catalog-Focused" with 49 total logins and 0 order submissions — a tiny, low-activity luxury account using eCat purely as a digital catalog.

**Correct placement:** Luxury Specification. At $1,900 avg catalog price, Bliss Studio's products are priced ABOVE the segment median ($892).

**Consequence if uncorrected:** Leadership would see this as a "Volume Distribution" company and apply a volume/efficiency CS motion. In reality it's a luxury catalog account.

### 2. Theodore Alexander Manhasset (Staging) — Not a Real Account

A staging/test environment counted as a real account, sharing the same $32,340 ARR as the production orgs. Inflates Luxury Spec by 1 and inflates its ARR.

**Fix:** Remove. Count drops to 109 real accounts.

### 3. Visual Comfort - Studio/Fans — Borderline (Flag, Don't Move)

- **ERP avg unit price: $29.52** | **Catalog avg: $182.08**
- **Placed in:** Luxury Specification (segment median: $892)

At $30 ERP avg, this org's transacted price is Mid-Market level. However:
- Same parent entity (Visual Comfort & Co.)
- Same rep network and trade-showroom selling motion
- The $30 ERP price likely reflects builder-grade fan/studio products sold through the SAME designer/showroom channel as the $632 Visual Comfort Modern line

**Recommendation:** Keep in Luxury Specification (the selling motion IS luxury trade). But the report already lists it at "$30" in the representative accounts table — leadership will ask about it. Add one sentence: "This org handles Visual Comfort's builder-grade studio line; it shares the same rep network and showroom channel as the other VC orgs and is grouped by selling motion, not price point."

---

## MISSING

### 1. The epistemological limits of the model

The report presents confident segment definitions without disclosing HOW those definitions were derived or how reliable the evidence is. Specifically:

- **"How They Sell" and "Who They Sell To"** come from website scraping (the enrichment CSV) — marketing copy, not commercial transaction data. For the ~90 accounts without ERP data, there is no way to verify these descriptions against actual buying patterns.
- **Price data coverage is partial:**

  | Segment | With Price Data | Total | Coverage |
  |---------|----------------|-------|----------|
  | Luxury Specification | 24 | 36 | 67% |
  | Premium Trade Brand | 23 | 33 | 70% |
  | Mid-Market Multi-Channel | 11 | 24 | **46%** |
  | Volume Distribution | 5 | 13 | **38%** |

  Mid-Market and Volume medians are based on fewer than half their accounts. A median from 5 data points is an anecdote.

- **The Bliss Studio error demonstrates the fragility of enrichment-based classification.** If the scraper hits the wrong website, the classification is completely wrong — and without first-party price data, there's nothing to catch it.

### 2. ARR double-counting from shared billing entities

Multiple orgs share the same billing entity and therefore the same ARR value:

| Shared Entity | Accounts | Segment |
|---|---|---|
| Theodore Alexander (3 orgs) | $32,340 × 3 | Luxury Spec |
| Gabriella White / Gabby | $26,307 × 2 | Luxury Spec |
| Kennedy / Moda at Home | $16,642 × 2 | Volume Dist |
| Arabela / Kaleen / DALS / Silver One / Sauder | $8,700 × 5 | Multiple |

**Luxury Spec ARR is inflated 14.4%** ($90,987) from duplicate counting. If leadership uses these for resource allocation, they're over-weighting Luxury Spec.

### 3. Segment boundary overlap undiscussed

Luxury Spec ($892 median) and Premium Trade ($354 median) overlap in the $350–$715 range:
- **Luxury Spec below $500:** VC Signature ($364), Gabriella White ($482)
- **Premium Trade above $500:** Hubbardton Forge ($715), Universal Furniture ($585), Kalco ($516)

The distinguishing factor is selling MOTION — whether the primary buyer is a designer specifying for a project (Luxury) vs. a consumer/dealer choosing a brand (Premium). This is defensible and arguably the point of v3. But leadership will ask "why is Hubbardton ($715) in Premium and not Luxury?" and the report doesn't explain the overlap zone.

### 4. No retention risk, expansion likelihood, or LTV

The report says nothing about which segments churn, expand, or concentrate revenue risk. A CEO's first question after "what are they?" is "which ones are at risk?"

### 5. "What This Means for SuperCat" implications are hypotheses, not conclusions

The CS resource allocation and expansion play tables are logical hypotheses — they COULD be correct — but they're presented with the same confidence as the data-backed segment definitions. They should be labeled as strategic hypotheses to test, not as findings.

---

## WHAT A FUTURE AGENT SHOULD DO DIFFERENTLY

The segmentation is built on externally-scraped enrichment data. The next version should be grounded in **first-party Postgres data** — what SuperCat actually KNOWS about each client from their own data living in our system.

**Available first-party signals (no enrichment needed):**

| Signal | Table | What it reveals about "how they sell" |
|---|---|---|
| **Product price distribution** | `products.net_price` | Luxury vs. volume vs. mid-market — not just the average, but the SHAPE of the distribution (tight cluster = focused; wide spread = multi-tier) |
| **Product category structure** | `products.category_code`, `collection_code` | Decorative lighting vs. architectural vs. furniture vs. accessories — type of product without relying on a scraper |
| **Customer count + type signals** | `customers.default_price_code` distribution | 1 price code = single-channel; 15+ = sophisticated multi-tier trade program with different pricing for designers vs. dealers vs. retail |
| **Customer concentration** | `portal_invoices` or `sales_data` | Top-10 customer share — indicates whether they sell to many small accounts (distribution) or few large ones (specification/project) |
| **Geographic spread** | `customers.billing_state` + territory structure | National rep coverage vs. regional vs. single-market |
| **Order pattern** (behavioral, not commerce) | `orders` — avg order value, SKU breadth per order, configured items | High-config orders = specification selling; low-config, high-frequency = reorder/distribution |
| **Customer NAMES and websites** | `customers.name`, `customers.code` patterns | A client whose customers are named "Smith Interiors," "ABC Design Group," "Kravet" is selling to designers. A client whose customers are "Home Depot Store #4521," "Amazon Vendor Central" is selling to chains. |

**The deep unlock:** For each of the 110 clients, an agent could:
1. Pull the `customers` table (who buys from them)
2. Classify those customers by TYPE (designer, showroom, chain, distributor) — potentially by looking at their websites
3. Pull the `products` price distribution (what price tier are they)
4. Pull the category/collection structure (what kind of products)
5. Where ERP data exists, pull invoice patterns (order size, frequency, concentration, seasonality)

This replaces "we scraped their website and it said they're trade-only" with "60% of their customer file is interior designers ordering $3K+ configured orders through showroom reps, which makes them luxury specification BY TRANSACTION PATTERN, not by marketing claim."

**Critical caveat:** This only works where data exists. For Tier 1 accounts (iPad + catalog only), the agent can analyze product price/type and customer name patterns — but cannot close the loop to revenue. For accounts WITH ERP data (~20), the loop closes fully. For the ~62 with `sales_data` (coarse), you get price point and volume but not patterns. **Know what you don't know.**

---

## RECOMMENDATIONS (Ranked by Impact)

### 1. Fix Bliss Studio classification (5 min)
Move to Luxury Specification. Note that enrichment scraped wrong company. First-party catalog data confirms $1,900 avg.

### 2. Fix or caveat GTM labels for luxury accounts (30 min)
Options:
- (a) Rename "Marketplace + Trade" → "Trade + Select Retailers" for luxury brands where the "marketplace" keyword was a curated retailer (Lumens, Lightology)
- (b) Add a caveat: "'Marketplace' here means listed on curated retail sites like Lumens/Lightology — not Amazon/Wayfair mass marketplace"
- (c) Drop the GTM field for luxury accounts entirely (the segment itself conveys the selling motion)

### 3. Remove staging org + add ARR deduplication note (10 min)
- Remove "Theodore Alexander Manhasset (Staging)" (count → 109)
- Footnote: "Multi-org entities share billing; segment ARR totals are not additive across portfolio members"

### 4. Add price data coverage disclosure (5 min)
Footnote to the median-price column: medians are based on 24/36, 23/33, 11/24, and 5/13 accounts respectively.

### 5. Add "boundary zone" explanation (10 min)
Between Segment 1 and 2: 2-3 sentences on why Hubbardton ($715) is Premium and VC Signature ($364) is Luxury. The criterion: primary buyer is a designer SPECIFYING (Luxury) vs. consumer/dealer CHOOSING a brand (Premium).

### 6. Label implications as hypotheses (5 min)
The "What This Means for SuperCat" section should open with: "The following are strategic hypotheses informed by segment definitions. They are not yet validated against commercial data."

---

## Summary Table

| Issue | Severity | Fix Time | Risk if Unfixed |
|---|---|---|---|
| Bliss Studio misclassified | HIGH | 5 min | Wrong strategy applied to luxury account |
| GTM false positives for luxury | MEDIUM | 30 min | Leadership thinks luxury brands sell on Amazon |
| Staging org in model | LOW | 5 min | Inflates count by 1 |
| ARR double-counting | MEDIUM | 10 min | Over-allocates resources to Luxury Spec |
| Price coverage undisclosed | MEDIUM | 5 min | False precision for Mid-Market/Volume |
| No boundary explanation | MEDIUM | 10 min | First question from CEO goes unanswered |
| Implications unlabeled | LOW | 5 min | Acceptable risk if audience understands context |

**Total fix time: ~45 minutes.** After these fixes, the model is presentable — with the understanding that it's the best classification achievable from available data, not ground-truth-verified commercial reality for most accounts.

---

## AUDITOR NOTE ON INITIAL BIAS (transparency)

The first version of this audit treated eCat iPad "order submissions" (5,112 for Gabriella White, 7,006 Mixpanel events for Interlude Home) as evidence that orders DO consummate in eCat. This was wrong:

- Per the Provenance Spine §2: "Almost no order flows straight from the iPad app into the ERP. The dominant real-world path is: rep writes an order/quote on iPad → HQ audits → human re-keys into ERP → invoices."
- An eCat "order submission" is a QUOTE or intent capture — not a consummated transaction. It may be edited, split, partially shipped, cancelled, or never keyed.
- The initial audit violated its own constraint: "Do not use eCat behavioral data as evidence that a segment placement is wrong."

The retraction is documented here so that the record is clean and the reasoning is traceable.
