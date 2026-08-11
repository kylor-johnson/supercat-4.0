# Monetization Reference (baseline + enriched inputs)

Baseline source: `Roundup of Ad-hoc Pricing Exploration` (RTF). Treat as true unless contradicted by fresher customer data.

---

## 0) Enriched inputs (pending incorporation)

- **Current product suite + pricing detail**: received 2026-01-28 (stored verbatim in `00_intake/2026-01-28__current_product_suite_and_pricing__INPUT.md`) and incorporated below.
- **Feature menu + usage proxies by product**: received 2026-01-28 (canonical source: `reports/feature_menu/supercat_feature_menu_2026-01-27.md`; pointer stored in `00_intake/2026-01-28__feature_menu_with_usage_proxies__INPUT.md`) and incorporated below.
- **Enriched TAM / prospect universe**: received 2026-01-28 (canonical CSV: `TAM Universe Segmentation & Fit Scoring - Prospect Summary.xlsx - [NEW] Full TAM - Segments & Fit Scoring v2 (4.6k).csv`). **Important**: user notes many fields are Supercat-enriched and subjective; treat scores/segments as hypotheses.
- **Pricing & Monetization Manifesto (internal POV)**: received 2026-01-29 (canonical file: `SuperCat Pricing & Monetization Manifesto.md`; pointer in `00_intake/source_docs/2026-01-29__pricing_monetization_manifesto__SOURCE_POINTER.md`; digest in `01_reference/2026-01-29__manifesto_digest.md`). Treat as internal operating doctrine; validate any “facts” against customer/billing data.
- **Enriched customer dataset (Master Customer Data — Q425)**: received 2026-01-29 (canonical CSV: `Pricing Refresh Master Data - Master Customer Data - Q425.csv`; pointer in `03_data/extracts/2026-01-29__enriched_customers__SOURCE_POINTER.md`). **Interpretation**: columns C–X = Q425 transactional/admin-panel metrics; Y–BA = high-level feature access; BB–CN = enrichment; **some enrichment fields (BG–BN) are subjective SuperCat POV**.
  - **Q425 window (confirmed)**: 2025-10-01 to 2025-12-31
  - **ARR definition (confirmed)**: `ARR` is **implied ARR = MRR * 12** in most cases (monthly-heavy base; seasonality present)

## 1) Current-state pricing architecture (facts from Roundup)

### Pricing & packaging today

- **Structure**: 5 separate priced products (fragmented), plus a foundational `eCat Admin Console` (backend command center).
- **Price band (monthly)**: **$395–$920/month** across the current priced products.
- **Seat model (only on iPad products)**: **25 active users included**, **$25/month** per additional active user over 25.
- **Implementation fees**: separate upfront fees by product, **$1,250–$6,500** (friction point).

### Current rate card (as provided)

| Product | Description | Base (monthly) | Additional charges | Implementation cost |
|---|---|---:|---|---:|
| eCat iPad **Non-Configurable** | B2B sales rep app (non-configurable products) | $725 | $25/mo per additional active user over 25 | $4,500 |
| eCat iPad **Configurable** | B2B sales rep app (configurable products) | $920 | $25/mo per additional active user over 25 | $6,500 |
| eCat Online **Product Catalog** | Online product catalog + user registration | $395 | None listed | $2,500 |
| eCat Online **B2B Cart Service** | Online secure B2B cart | $395 | None listed | $1,250 |
| **Sales Portal (BI)** | Order status, tracking, analytics | $395 | None listed | $2,250 |

### Implied bundle economics (derived; validate against actual sold bundles)

- **“Full online suite” (Catalog + B2B Cart + Sales Portal)**: **$1,185/mo** base; **$6,000** implementation total.
- **Online suite + iPad Non-Config**: **$1,910/mo** base; **$10,500** implementation total (plus seat overages on iPad if >25 active users).
- **Online suite + iPad Config**: **$2,105/mo** base; **$12,500** implementation total (plus seat overages on iPad if >25 active users).

### What’s being monetized today (observed)

- **Primary monetization**: product/module selection (which of 5 products).
- **Secondary monetization**: “active users” (iPad products only), which creates the same failure modes the Roundup flagged (seasonality + sharing pressure).
- **Services monetization**: upfront implementation fee by module (high-friction gate).

### Contract / billing rails (overarching SaaS agreement)

Canonical terms: `https://supercatsolutions.com/licensingagreement` (pointer stored in `00_intake/source_docs/2026-01-29__saas_licensing_agreement__SOURCE_POINTER.md`).

High-signal clauses that constrain pricing + migration mechanics:

- **Activation Date billing**: billing commences on “Activation Date” (service made available for configuration), regardless of production use; **implementation fee due** upon Activation Date; **platform fees commence** on Activation Date.
- **Term structure**: monthly is month-to-month following any initial commitment period (if any); annual renews per pricing schedule; **no mid-term cancellations/refunds**.
- **Price changes**: after the initial term, fees may be modified with **60 days written notice**, effective at the next renewal term; increases not more than **once per 12 months**.
- **Renewal/non-renewal notices**: annual non-renewal notice at least **30 days** before term end; renewal notice (incl. fee changes) at least **90 days** before term end; monthly termination notice at least **30 days**.

Execution note: majority of customers are on **monthly terms**, but there is a **locked pricing / in-implementation cohort (5 accounts)** with contracted “true ARR” that is not reflected in the Q425 baseline dataset — treat as **exceptions** in the migration plan (see `07_migration/2026-01-29__locked_pricing_cohort__v0.md`).

---

## 1.1) Current product surface area + measured usage proxies (from feature menu)

This section translates the feature menu into **monetization-relevant usage signals** and **packaging fence levers** (what can actually be measured/enforced).

### Tenant / gating architecture (important for packaging)

- **Tenant identifier**: `organizations.id` + `organizations.shortname` (routes use `:org_shortname`).
- **Primary product gating** is implemented via:
  - **Mobile Site flags** (e.g., `enable_online_ordering`, `enable_sales_portal`)
  - **UserType permissions** (role-based access control)
  - **Org/MobileSite properties & flags** (JSON `properties` / `flags`)
  - Some code-level **Feature flags** (allowlists)

Implication: you already have strong, enforceable “fences” for packaging (especially around **online ordering**, **sales portal**, **library**, **RMA**, and advanced permissions).

### Installed base & enablement (feature menu; tenant universe = 244 orgs)

- **Mobile Sites present**: **96/244 (39.3%)**
- **eCat Online catalog enabled**: **91/244 (37.3%)**
- **eCat Online ordering enabled**: **53/244 (21.7%)**
- **Sales Portal enabled**: **47/244 (19.3%)**

Interpretation: today, “online ordering” and “sales portal” are **premium capabilities** in the installed base (low enablement), while catalog access is broader but still not universal.

### Adoption/usage signals (last 90 days, where available)

- **Authentication usage**: **136/244 orgs (55.7%)** had ≥1 non-admin login event in last 90d.
- **Orders submitted (total)**: **39,174** submitted orders across **96** orgs.
  - **iPad orders** (`order_source='ipad'`): **31,065** submitted orders across **95** orgs.
  - **eCat Online orders** (`order_source='server'`): **8,108** submitted orders across **29** orgs.
- **eCat Online ordering (among ordering-enabled orgs)**:
  - **28/53 (52.8%)** had ≥1 `cart_items` row
  - **29/53 (54.7%)** had ≥1 submitted eOL order
- **Sales Portal operational data presence (among portal-enabled orgs)**:
  - portal orders present for **37/47 (78.7%)**
  - portal invoices present for **38/47 (80.9%)**
- **Catalog complexity signals**:
  - Product images present for **225/244 (92.2%)** orgs (rows: 2,535,796)
  - Option images present for **99/244 (40.6%)** orgs
  - Price levels present for **223/244 (91.4%)** orgs; **207/244 (84.8%)** have ≥2 price levels
  - Inventory rows present for **181/244 (74.2%)** orgs
  - Smart stacks present for **179/244 (73.4%)** orgs; **102/244 (41.8%)** updated a smart stack in last 90d
- **Operational “stickiness” signals**:
  - Import events: **52,118** import events across **123/244 (50.4%)** orgs in last 90d
  - Enrollment applicants: **1,916** applicants across **39/244 (16.0%)** orgs in last 90d
  - Projects: **57,624** projects exist across **77** orgs; **48/244 (19.7%)** had project updates in last 90d

### Where the feature menu changes our monetization design immediately

- **Orders are already measurable and attributable** (iPad vs eOL), which strengthens the case for **order pools / credits** as a scalable component.
- **Mobile Site enablement flags** provide clean packaging gates for:
  - online ordering
  - sales portal
  - library (enablement exists)
  - RMA (rare enablement today)
- **Catalog complexity is measurable** (price levels, option images, inventories, product images) but “active SKU” must be defined carefully (and may require new instrumentation if `products` table alone is insufficient).

### Customer base quantitative readout (Master Customer Data — Q425)

Source: `Pricing Refresh Master Data - Master Customer Data - Q425.csv`  
Window (confirmed): **2025-10-01 → 2025-12-31**  
ARR definition (confirmed): **ARR is implied ARR = MRR * 12** (monthly-heavy base; seasonality present).

**Book shape (n=110 accounts)**

- **Status**: 109 active, 1 inactive
- **MRR distribution** (USD):
  - p25 **$725**, median **$1,192.50**, p75 **$1,899**, mean **$1,408.69**
- **Implied ARR distribution** (USD):
  - p25 **$9,425**, median **$16,122.75**, p75 **$25,084.50**, mean **$17,726.71**
- **Order volume distribution (Q425)**:
  - p25 **1**, median **29**, p75 **330**, p90 **~923**, mean **~330**
- **Channel mix (Q425)**:
  - total orders **36,249**
  - iPad orders **27,371** (**~75.5%**)
  - eCat Online (eOL) orders **8,878** (**~24.5%**)
  - reconciliation check: total orders = iPad orders + eOL orders (**0 mismatches**)
- **Catalog proxy (“Total products”)**:
  - p25 **~1,108**, median **~2,747**, p75 **~5,538**, p90 **~10,197**, max observed **48,727**

**High-level feature enablement rates (within these 110 accounts)**

- `Feature: eOL Catalog`: **53/110 (48.2%)**
- `Feature: eOL Cart`: **32/110 (29.1%)**
- `Feature: eOL Portal`: **35/110 (31.8%)**
- `Feature: Credit Card`: **10/110 (9.1%)**
- `Feature: Address Validation`: **4/110 (3.6%)**
- `Feature: Enrollment`: **55/110 (50.0%)**
- `Mobile Site: Enable Online Library`: **45/110 (40.9%)**
- `Mobile Site: Enable RMA Processing`: **4/110 (3.6%)**

**Observed adoption cohorts (based on Cart/Portal enablement; counts + economics)**

- **Rep-led only (no cart/portal)**: **64 accounts**
  - median MRR **$725**
  - median orders (Q425) **3** (p75 **49.5**)
- **Digital + visibility (cart+portal)**: **21 accounts**
  - median MRR **$2,095**
  - median orders (Q425) **574** (p75 **1,584**)
- **Portal only**: **14 accounts**
  - median MRR **$1,937**
  - median orders (Q425) **262.5** (p75 **754.25**)
- **Cart only**: **11 accounts**
  - median MRR **$1,415**
  - median orders (Q425) **118** (p75 **310.5**)

Immediate implication: the installed base already behaves like **Tier 1 (rep-led)** vs **Tier 2 (commerce/visibility)** cohorts, with clear ARPA and usage separation.

### Commercial motion (mix + clustering)

- **Contract split**: **89% monthly**, **11% annual**.
- **Median ARR**: **~$16,643** (≈ **$1,387/month**).
- **Price clustering**: “no-man’s land” around **~$15k/year** (too small for enterprise motion, too large for SMB).

### Operational symptoms tied to pricing

- **Seasonality**: **16.8% user variance** + account sharing → “users” behaving like a proxy for seasonality/role-sharing, not value.
- **Billing complexity**: called out as a pain point; recommendation theme is “predictable, visible, finance-friendly.”

---

## 1.2) Insights Layer — Tier 3 differentiator (new; 2026-01-30)

**Source**: `01_reference/2026-01-30__insights_layer_definition__v1.md`

### The headline

> With MCP/agentic access into each customer's instance, SuperCat can now surface insights customers cannot easily generate themselves—turning raw operational data into interpretation, benchmarks, and recommendations.

### What "Insights" means (vs Analytics)

| Dimension | Analytics (existing) | Insights Layer (new) |
|-----------|---------------------|----------------------|
| **Who generates** | Customer self-service | SuperCat (proactive) |
| **What it shows** | Raw metrics, dashboards | Interpretation + recommendations |
| **Context** | Single-customer view | Cross-customer benchmarks, peer comparison |
| **Actionability** | "Here's your data" | "Here's what to do and why" |
| **Cadence** | On-demand, self-pull | Delivered (monthly/quarterly QBR) |

### Three pillars

1. **Sales Effectiveness Insights** (CXO/Sales Leaders)
   - Revenue vs. peer benchmarks (114+ organizations)
   - Channel mix diagnosis (iPad vs. eCat Online)
   - Customer activation rate vs. benchmark (e.g., 19.6% vs. 9.2% = 2x)
   - Revenue leakage analysis (inactive customers × AOV = quantified opportunity)
   - Seasonal pattern analysis (market peaks, summer slowdowns)

2. **Instance Health Insights** (IT/Ops/Admin)
   - Data sync status and freshness (products, customers, inventory)
   - Import error rate and trend (zero errors = "exceptional performance")
   - Data completeness audit (e.g., "29% of products missing images")
   - Integration health by data type

3. **Feature Adoption & ROI Insights** (Reps/Leaders/CS)
   - Feature usage vs. benchmarks (SmartPicks, PDF Catalogs, Scan to Search)
   - Underutilization identification with impact quantification (e.g., "SmartPicks → +23% AOV")
   - Training opportunity signals

### Composite: Account Health Score

A single 0-100 score synthesizing all pillars:
- Engagement (20%), Sales Performance (25%), Data Health (20%), Support Health (15%), Feature Utilization (20%)
- Example: **92/100 — EXCELLENT**

### Why customers can't do this themselves

1. **Cross-customer benchmarking**: requires access to anonymized peer data
2. **Pattern recognition at scale**: seasonal trends, feature ROI—aggregate intelligence
3. **Proactive interpretation**: translates metrics into "so what" and "now what"
4. **Time-to-insight**: delivered pre-packaged; no analyst effort required

### Packaging implication

- **Tier 3 (Commerce Enterprise)**: Insights Layer included (QBRs, monthly reports, Account Health Scoring)
- **Tier 1/2**: raw analytics only (Sales Portal, Admin Console dashboards); Insights Layer is an upgrade path

---

## 2) Customer value drivers & why the current metric is misaligned

### Why “users” is misaligned (Roundup claims)

- **Value is not created per seat**; value is created via:
  - catalog complexity handled (SKUs/variants)
  - orders/transactions processed (especially in seasonal spikes)
  - adoption across buyer accounts (platform “spread”)
- **Per-seat pricing failure modes** (explicitly mentioned or implied):
  - incentivizes account sharing
  - creates artificial adoption barriers
  - fails under seasonality (seat spikes ≠ durable value)
  - pushes customers to “optimize spend” by limiting usage (bad for outcomes and NRR)

### Vertical-specific value moments (furniture/lighting)

- Trade-show workflows + offline/mobile expectations
- Complex SKU hierarchies (fabric/finish combinations, variants)
- Seasonal buying cycles and demand swings (Roundup cites 30–45% seasonality at industry level)
- Workflow automation that reduces manual order-processing cost (Roundup cites **$35–$50 per manual order** fully-loaded)

---

## 3) Competitive landscape (price bands, packaging patterns, differentiators)

### Market pattern: legacy opacity vs modern transparency

- **Legacy incumbents**: quote-only/high-touch pricing (e.g., MarketTime, AmpTab), heavy setup fees, longer implementations.
- **Modern alternatives**: transparent published pricing, faster implementation, mobile-first.
- **Buyer preference**: Roundup cites **78% of B2B buyers demand upfront pricing**.
- **Implementation speed**: legacy **3–6 months** vs target **30–60 days** (Roundup recommendation); WizCommerce cited as “sub-30-day implementation.”

### Direct competitor snapshots (as reported)

- **AmpTab**:
  - Pricing: **$500/mo Starter**, **$1,000/mo Advanced**, **$3,000/mo Pro**
  - Setup fees: **$5k / $10k / $30k**
  - Positioning: industry-specific, but “outdated software / unintuitive website”
- **Pepperi**:
  - Pricing: **$500/mo Basic**, **$1,500/mo Pro**, Enterprise custom
  - Theme: eliminates transaction fees; uses “generous pools of annual transactions”
- **MarketTime**:
  - Quote-only; network effects cited (300k retailers / 6,500 brands / $5B+ annual orders)
  - Criticism: “lack of transparency / pricing opacity”
- **WizCommerce**:
  - Pricing: **$500–$1,000/mo**
  - “Sub-30-day implementation,” “AI-first” positioning; “500+ customers,” “$8M Series A”

### Competitive packaging patterns (Roundup)

- **Good/Better/Best** with real feature gaps and 2–3x price steps.
- **Modular add-ons** for expansion (trade show tools, visual commerce, advanced integrations).
- **Vertical premium**: **25–30%** pricing premium for industry specialization vs horizontal solutions.

---

## 4) Candidate value metrics ranked (primary + secondary)

Ranked against: alignment, scalability, predictability, controllability, measurability, customer-perceived fairness, seasonality resilience, anti-gaming.

### 1) Hybrid “Catalog + Transactions + Seasonal Credits” (recommended in Roundup)

- **Primary**: active catalog size (active SKUs)
- **Secondary**: transaction volume (count or GMV; “customer choice” is suggested)
- **Guardrail/flex**: seasonal credit system (pre-purchased credits, rollover, avoids surprise overages)
- **Pros**
  - captures two real value drivers (catalog complexity + commerce throughput)
  - smooths seasonality without seat-gaming
  - predictable base + expansion path
- **Cons / failure modes**
  - SKU definition disputes (“active SKU” must be precisely defined)
  - transaction counting disputes (“what counts as an order?”)
  - risk of discouraging adoption if overages feel punitive (needs generous included + clear top-ups)

**New (from feature menu): measurability notes**

- **Transactions/orders**: strong measurability today via `orders` (incl. `order_source` attribution). This is a “ready now” metric.
- **Catalog complexity**: multiple measurable proxies exist (images, option images, inventories, price levels). However, “active SKUs” requires an explicit product/SKU definition and likely a curated “active” lens.

### 2) Transaction pools (orders processed) as the primary metric (Roundup primary recommendation theme)

- **Primary**: annual or monthly order/transaction pool included by tier; overage/top-ups for growth
- **Pros**
  - strongest alignment to business growth; intuitive fairness for buyers
  - eliminates seat sharing friction
- **Cons / failure modes**
  - seasonal invoice shock if pools are too tight or overage math is confusing
  - can penalize adoption if modeled like a “tax” (must avoid per-order nickel-and-diming)

**New (from feature menu): measurability notes**

- You can count **submitted orders** today and attribute by channel (iPad vs eOL). This supports:
  - annual pools (preferred for seasonality)
  - channel-specific allowances (optional) if you want to encourage eOL adoption without penalizing iPad-heavy orgs
  - “usage transparency” in admin reports (the feature menu references an existing usage statistics report service)

### 3) Active buyer accounts (secondary expansion metric)

- **Pros**: encourages platform spread; aligns with network effects.
- **Cons / failure modes**: definitional ambiguity (active buyer), potential gaming (automation / duplicates).

**New (from feature menu): measurability notes**

- Likely measurable via `customers` and/or ordering customer associations (not fully enumerated in the excerpt), but we need to confirm:
  - how “buyer” is represented (customers vs org_users associated to customers)
  - whether “active buyer” can be derived from orders in a clean way

### 4) Revenue processed / GMV (enterprise option)

- **Pros**: aligns with value for large accounts; supports enterprise custom deals.
- **Cons / failure modes**: “success tax” perception; requires robust data accuracy + auditability.

### 5) Seats/users (deprioritized; correlation-only)

- **Pros**: easy to measure.
- **Cons**: explicitly misaligned here; high gaming risk; discourages adoption; collapses under seasonality.

---

## 5) “Must-keep” insights vs weak/uncertain claims (Roundup quality assessment)

### Must-keep (high confidence / directly actionable)

- **Users are a weak primary metric** given **16.8% seasonal variance** + account sharing behavior.
- **5-product fragmentation** at **$395–$1,020/mo** creates confusion and weak upgrade triggers.
- **Monthly-heavy book (89% monthly)** is an under-monetized lever; annual adoption is a priority.
- **Implementation fees ($1,250–$6,500) add friction**; embed/bundle or reframe as packaged onboarding.
- **Transparency is a competitive advantage** (78% want upfront pricing; legacy is quote-only).
- **Hybrid subscription + usage pools** is the market direction (avoid punitive per-transaction fees).

### Weaker / requires validation with SuperCat-specific data

- Any **industry-wide benchmarks** (e.g., “38% faster revenue growth,” “50% higher multiples,” market sizing stats) are directionally useful but should not drive internal targets without validation.
- Competitor metrics (customer counts, ROI claims) are helpful as narrative anchors but should be verified via win/loss + buyer interviews.
- The existence of multiple “strawmen” in the Roundup (different tier ladders and metrics) implies **we must choose one** based on SuperCat’s actual distribution of customer size/usage and cost-to-serve.


