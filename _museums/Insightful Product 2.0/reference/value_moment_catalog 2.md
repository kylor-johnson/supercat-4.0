# Value Moment Catalog v2 — Insightful Product 2.0

> **Version**: 2.0
> **Status**: Active — Phase 2 complete
> **Scope**: 51 active value moments across 8 domains
> **Data readiness**: All VMs queryable; conditional and pending engineering variants noted per VM

---

## How to Read This Catalog

Each **value moment** (VM) is a discrete recommendation or insight the Insights Layer can deliver. The schema for each VM is:

| Field | Meaning |
|-------|---------|
| **Audience** | External-safe [E], Internal only [I], Dual [D], or Conditional [C] |
| **Commerce Lens** | eCat transaction / ERP total-business / Comparative capture / Non-commerce |
| **Internal Name** | System/engineering name used in gating and query references |
| **Customer-Facing Name** | Name used in report prose and external claims |
| **Gating** | Feature flags, bundle types, or data conditions required |
| **Signal** | Data sources and query logic |
| **Example** | Real grounding from a validated client account |
| **Action** | What CS or the customer does with this insight |
| **Customer Value** | Why the customer cares |
| **SuperCat Value** | Why SuperCat cares (retention, expansion, differentiation) |
| **Segments** | Which bundle types or account profiles benefit |
| **Complexity** | Simple / Moderate / Complex |
| **Data Dependency** | Explicit table names, source system, data readiness |
| **Data Readiness** | Live / Conditional Live / Pending Engineering / Deferred |
| **Bundle Required** | Specific bundle(s) or "All" |
| **Query IDs** | References to query library |
| **Allowed Claims** | What this VM can say — safe for external use if [E] or [D] |
| **Forbidden Claims** | Claims this VM must never make |
| **Portability** | Fully portable / Query portable–interpretation varies / Data-gated |
| **Enhancement Path** | What would expand this VM's capability (where relevant) |

**Delivery surface**: Where each VM lives in the product (Admin Console, Sales Portal, Insights Layer, internal CS tooling) is a commercial decision resolved separately from this catalog.

---

## Global Query Guardrail

All queries touching the `orders` table must use the nullable delete guard:

```sql
AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
```

This is not repeated per VM. The `is_marked_deleted` column is nullable — some orgs store `NULL` (meaning "not deleted") rather than `false`. Using `= false` alone silently drops valid orders and understates all eCat metrics.

---

## Commerce Ontology

Every commerce-related VM belongs to one of three lenses:

| Lens | Source Table | What It Covers |
|------|-------------|----------------|
| **eCat transaction** | `orders` | iPad + eCat Online orders only. Rep-submitted and buyer self-service eCat orders. |
| **ERP total-business** | `portal_orders` | All orders synced from the client's ERP — eCat, phone, EDI, trade shows, showroom. Feeds the internal Sales Portal. Not buyer activity. |
| **Comparative capture** | `orders` vs. `portal_orders` | eCat share of total business. What % of the client's real order volume flows through eCat. |

`portal_orders` is never framed as buyer self-service activity. "Self-service" in this catalog means `orders.order_source = 'server'` (B2B Cart / eCat Online ordering) only.

---

## Domain 1 — Rep Performance Intelligence

*The anchor capability of the Insights Layer. Validated by the SuperCat behavioral correlation model (r > 0.96 for customer targeting). Full analysis in `03_rep_performance_intelligence.md`.*

---

### VM-01: Rep Behavioral Scorecard

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: rep_behavioral_scorecard
**Customer-Facing Name**: Sales Team Performance Report

**Gating**: Mixpanel behavioral data available for org (active iPad app users). For catalog-only accounts, substitute engagement proxies (library views, PDF generation, product discovery depth) for order outcomes.

**Signal**: Per-rep Mixpanel event counts (38 behavioral counters) mapped to the six-dimension correlation model — Customer Targeting, Product Discovery, Configuration & Bundling, Presentation & Communication, Information & Planning, Engagement Depth — cross-referenced with MCP `orders` outcomes (order count, GMV, unique customers, AOV).

**Example** *(BCF — validated)*:
> **Todd Teague — Q4 2025**
> | Dimension | Score | Peer Avg | Rating |
> |-----------|------:|:--------:|--------|
> | Customer Targeting | 10.5/order | 14.2 | Efficient |
> | Product Discovery | 98.9/order | 85.3 | Thorough |
> | Configuration & Bundling | 28.2/order | 19.4 | Above average |
> | Presentation & Communication | 32.0/order | 8.1 | Standout |
> | Information & Planning | 599 library views | 645 avg | On par |
> | Engagement Depth | 1.7 logins/day | 2.0 avg | Consistent |
>
> Outcome: 26 eCat orders, $148K eCat GMV, 10 customers served, $5,683 AOV

**Action**: Sales managers use the scorecard to identify per-rep coaching priorities. CS uses it during QBR to show the customer their team's behavioral profile.

**Customer Value**: Targeted coaching based on behavioral evidence, not intuition. A manager can see exactly where each rep is strong and where a training investment has the highest ROI.

**SuperCat Value**: Highest action-proximity insight in the catalog. Creates expansion conversations. Strongest competitive differentiator — no competitor provides per-rep behavioral data tied to order outcomes.

**Segments**: All bundles with active iPad app users. iPad-only, iPad+Catalog, iPad+Catalog+Cart, Full.

**Complexity**: Complex (multi-source: Mixpanel behavioral data + MCP `orders` + peer aggregation)

**Data Dependency**: BigQuery `user_feature_usage_report` (behavioral counters) + MCP `orders`

**Data Readiness**: Live

**Bundle Required**: Any bundle with `eCat iPad`

**Query IDs**: Q-01 (Mixpanel behavioral scorecard), Q-18 Part A (eCat order outcomes)

**Allowed Claims**: "Here is how your sales team uses the platform behaviorally." | "These reps show strong product discovery but low configured ordering — here's the coaching opportunity." | Per-rep eCat GMV, order count, AOV, customer count.

**Forbidden Claims**: "Net-new customers" | Total-business GMV attributed to rep behavior | Claims about non-eCat order outcomes

**Portability**: Fully portable — Mixpanel org shortname + `orders` org_id are standardized.

---

### VM-02: Selling Archetype Classification

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: selling_archetype_classification
**Customer-Facing Name**: Sales Team Archetype Report

**Gating**: VM-01 must be run first. Requires 3+ active selling reps for meaningful clustering.

**Signal**: Cluster analysis on VM-01 behavioral scorecard dimensions. Identifies distinct selling styles based on the ratio of behaviors to eCat order outcomes.

**Example** *(BCF — validated)*:
> | Archetype | Reps | Signature | Implication |
> |-----------|------|-----------|-------------|
> | Deep-Account Specialist | Barbara Harper | Extreme targeting at 1 account. 58 Q4 eCat orders, $192K. Zero presentation. | High output, concentration risk. |
> | Curated Discovery Seller | Todd Teague | Highest presentation and curation. 10 customers, $5,683 AOV. | Most scalable style — model for team. |
> | Volume Relationship Seller | Sharyn Moss | Most logins (624), broadest reach (22 customers). Lower AOV, compensates with volume. | Could improve AOV with configuration coaching. |
> | Precision Closer | Steve Billingsley | Low browsing, very high AOV ($8,881). 49 configured items per order. | If frequency increased, significant upside. |

**Action**: Managers adapt coaching strategy to archetype rather than applying one-size-fits-all training.

**Customer Value**: Replaces one-size-fits-all sales coaching with archetype-specific development.

**SuperCat Value**: Creates "aha moments" during QBR that justify Insights Layer investment.

**Segments**: Commerce-active bundles with 5+ active selling reps. iPad+Catalog+Cart, Full.

**Complexity**: Complex (behavioral scoring + clustering logic derived from VM-01)

**Data Dependency**: Mixpanel + MCP `orders`

**Data Readiness**: Live

**Bundle Required**: Any bundle with `eCat iPad` and active ordering

**Query IDs**: Derived from Q-01

**Allowed Claims**: "Your team uses distinct selling styles." | Archetype descriptions and behavioral profiles. | Per-archetype coaching recommendations.

**Forbidden Claims**: "Net-new customers" | Implied archetype superiority without data support

**Portability**: Fully portable.

---

### VM-03: Behavioral Funnel Gap Analysis

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: behavioral_funnel_gap
**Customer-Facing Name**: Sales Funnel Coaching Report

**Gating**: VM-01 required. Sufficient rep-level behavioral data for funnel mapping.

**Signal**: Map each rep's activity to the validated funnel (Customer Targeting → Product Discovery → Configuration → Presentation → eCat Orders). Identify where a rep has strong upstream activity but disproportionately weak downstream conversion.

**Example** *(BCF — validated)*:
> **Coaching Priority: Katrinka Barnhart**
> - Customer Targeting: Very Strong (1,745 events — highest of any rep)
> - Product Discovery: Very Strong (2,537 searches)
> - Configuration & Bundling: Moderate (213 — disproportionately low)
> - Presentation: Weak (25)
> - eCat Orders: Low (6 orders, $21K, $3,488 AOV)
>
> Gap: Configuration. She does the hard work of finding customers and products but doesn't convert to complex configured orders.
> Recommended action: Train Katrinka on bundling and CPQ tools. If her AOV increases from $3,488 to Jerry Montini's $4,846 (+39%), that's ~$8K/quarter in incremental eCat GMV.

**Action**: Specific, per-rep coaching recommendation with quantified upside estimate.

**Customer Value**: Directly translates behavioral data into a dollar-value coaching opportunity.

**SuperCat Value**: Strongest ROI story for the Insights Layer. "The add-on pays for itself if it improves one rep's performance by a measurable amount."

**Segments**: All commerce-active bundles.

**Complexity**: Moderate (funnel ratio calculation per rep, derived from VM-01)

**Data Dependency**: Mixpanel + MCP `orders`

**Data Readiness**: Live

**Bundle Required**: Any bundle with `eCat iPad` and ordering data

**Query IDs**: Derived from Q-01, Q-18 Part A

**Allowed Claims**: Per-rep funnel gap with specific behavioral data. | Quantified upside estimate based on peer AOV benchmarks.

**Forbidden Claims**: Guaranteed revenue improvement claims

**Portability**: Fully portable.

---

### VM-04: Non-Selling User Role Classification

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: non_selling_user_classification
**Customer-Facing Name**: Platform User Role Report

**Gating**: Org with 10+ active users and Mixpanel behavioral data.

**Signal**: Identify users with significant platform activity but zero or near-zero eCat orders. Classify by behavioral fingerprint (high library + PDF + zero orders = Content Manager; high portal + zero orders = Analytics User; etc.).

**Example** *(BCF — validated)*:
> 7 of 49 active Q4 users are non-selling roles:
> - Morgan Horwitz: Catalog/Data Manager (83 PDFs, 120 kit views, 15 CSV exports)
> - Paul Camillo: Content/Library Manager (940 library views, 123 library emails)
> - Kirsten Seidl: Customer Insights/Analytics (1,084 library views, 320 portal views)

**Action**: Exclude non-sellers from rep performance benchmarks. Validate that non-selling seats are generating value (content creation, catalog maintenance, analytics) commensurate with seat cost.

**Customer Value**: Cleaner performance data. Avoids unfairly comparing sales reps to catalog managers.

**SuperCat Value**: Seat utilization conversation. Transparent discussion about value-per-seat.

**Segments**: All bundles with 10+ users.

**Complexity**: Moderate (behavioral fingerprint classification)

**Data Dependency**: Mixpanel + MCP `org_users`

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-04 (user classification)

**Allowed Claims**: Non-selling role identification with behavioral evidence. | Seat value assessment.

**Forbidden Claims**: Seat count = wasted spend (framing must be value-neutral)

**Portability**: Fully portable.

---

### VM-05: Seat Utilization Analysis

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: seat_utilization
**Customer-Facing Name**: Platform Adoption Summary

**Gating**: None.

**Signal**: Compare total `org_users` against active users (logged in within 90 days), ordering users, and role-classified users.

**Example** *(BCF — validated)*:
> BCF has 1,370 org users:
> | Category | Count | % of Total |
> |----------|------:|----------:|
> | Active sellers (>5 Q4 eCat orders) | 10 | 0.7% |
> | Light sellers (1–5 Q4 eCat orders) | 14 | 1.0% |
> | Non-selling active roles | 7 | 0.5% |
> | Logged in, minimal activity | 18 | 1.3% |
> | Never logged in / inactive | 1,321 | 96.4% |

**Action**: Review user roster. Deactivate unused accounts (security hygiene). Identify whether inactive users represent untapped adoption opportunity or stale records from ERP import.

**Customer Value**: Security hygiene and adoption gap visibility.

**SuperCat Value**: Seat utilization conversation frames both cleanup (lower overhead) and activation (more value from the platform).

**Segments**: All bundles. Most impactful for accounts with large ERP-imported user bases.

**Complexity**: Simple (org_users count + login_events + orders aggregation)

**Data Dependency**: MCP `org_users`, `login_events`, `orders`

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-05

**Allowed Claims**: Active vs. inactive user breakdown. | Security hygiene recommendation.

**Forbidden Claims**: "X% of your licenses are wasted" (framing must be value-neutral, not accusatory)

**Portability**: Fully portable. Note: large ERP-imported user bases (BCF: 1,370 users) are common — inactive users are not inherently a problem.

---

### VM-06: Rep Engagement Trajectory

**Audience**: Dual [D] — Input signal to VM-29
**Commerce Lens**: eCat transaction
**Internal Name**: rep_engagement_trajectory
**Customer-Facing Name**: Sales Team Engagement Trend

**Gating**: Active ordering reps in the last 180 days.

**Signal**: Track per-rep login frequency and eCat ordering velocity over rolling 90-day windows. Surface reps whose engagement is declining.

**Example** *(BCF — validated)*:
> | Rep | Logins (prev 90d) | Logins (curr 90d) | Δ | eCat Orders (prev 90d) | eCat Orders (curr 90d) | Δ |
> |-----|------------------:|------------------:|---:|:---:|:---:|:---:|
> | Sharyn Moss | 312 | 312 | 0% | 24 | 25 | +4% |
> | Todd Teague | 82 | 72 | −12% | 15 | 11 | −27% |

**Action**: CS or sales manager follows up with declining reps before the trend becomes a problem.

**Customer Value**: Early warning on rep disengagement.

**SuperCat Value**: Rep disengagement often precedes account-level churn by 60–90 days. This signal feeds VM-29 (Churn Risk).

**Segments**: All bundles with active ordering reps.

**Complexity**: Moderate (rolling window aggregation on `login_events` + `orders`)

**Data Dependency**: MCP `login_events`, `orders`

**Data Readiness**: Live

**Bundle Required**: Any bundle with `eCat iPad`

**Query IDs**: Q-06

**Allowed Claims**: Rolling login and eCat order trend per rep. | Decline percentage over 90-day windows.

**Forbidden Claims**: "Rep is about to leave" (leading indicator, not confirmation) | Total-business order decline attributed to rep

**Portability**: Fully portable.

---

### VM-43: Territory Coverage & Dormancy

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: territory_coverage_dormancy
**Customer-Facing Name**: Territory Coverage Report

**Gating**: Rep territory assignments populated in `org_users` or orders. Meaningful for accounts with 3+ active territories.

**Signal**: Cross-reference rep territory assignments with `customers` (all assigned accounts) and `orders` (eCat ordering history per customer). Surface: accounts assigned to a rep but never ordered via eCat, accounts assigned but dormant (ordered before, not in trailing 90 days), and territories with no rep coverage at all.

**Example** *(illustrative)*:
> Territory: Southeast
> - Rep: Jerry Montini
> - Assigned accounts: 247
> - Accounts with any eCat order history: 89 (36%)
> - Accounts dormant in last 90 days: 34 (38% of ever-ordered)
> - Accounts never activated via eCat: 158 (64%)
>
> Coaching priority: Of Jerry's 247 assigned accounts, 158 have never placed an eCat order. The top 10 by historical `sales_data` volume are the highest-ROI activation targets.

**Action**: Generate a territory-attributed dormant account list. Pair with VM-17 for aggregate view and VM-37 for top-account revenue context.

**Customer Value**: Structured view of rep coverage gaps by territory — "which accounts does your Southeast rep own but not actively work via eCat?"

**SuperCat Value**: Territory coverage is a core eCat selling use case. Activating dormant assigned accounts = more eCat orders = stronger platform ROI story.

**Segments**: All bundles with active rep model and territory structure.

**Complexity**: Moderate (customers + orders + org_users territory join)

**Data Dependency**: MCP `customers`, `orders`, `org_users`

**Data Readiness**: Live

**Bundle Required**: Any bundle with `eCat iPad` and territory assignments

**Query IDs**: Q-43 (territory coverage — to be added to query library)

**Allowed Claims**: "These accounts are assigned to your reps but have no eCat order history." | Territory-level activation rate. | Dormant accounts by rep assignment.

**Forbidden Claims**: "These accounts don't buy from you" (they may order through non-eCat channels) | "Net-new customers"

**Portability**: Fully portable. Territory assignment structure varies by org but `customers.billing_state` and rep attribution in `orders` fields are standardized.

---

### VM-46: eCat Selling Workflow Maturity

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: ecat_workflow_maturity
**Customer-Facing Name**: eCat Workflow Assessment

**Gating**: Active Mixpanel behavioral data. Most useful for accounts where the eCat submit-through rate is below 25%.

**Signal**: Calculate the eCat order submission rate as a fraction of behavioral selling signals. Map to a four-band heuristic:

| Submit Rate | Band | Platform Role |
|-------------|------|---------------|
| 0% | Non-submit-through | Pure selling/presentation layer |
| < 10% | Minimal submit-through | Enablement-heavy; occasional eCat orders |
| 10%–25% | Partial capture | Meaningful eCat order volume; majority close outside eCat |
| > 25% | Transactional | eCat is a primary order capture channel |

High behavioral signals (product search, customer selection, presentation events, PDF catalogs, library sharing) with low or zero submit-through indicates a client using eCat as a selling enablement layer, not just a lazy adopter. This is a legitimate and recognized use pattern.

**Example** *(illustrative — iPad+Catalog+Portal account)*:
> Platform role: Enablement-heavy (submit rate: 3%)
> Behavioral signals:
> - Product searches: 12,400 (90d)
> - Customer selection events: 8,200 (90d)
> - Presentation events (Magic Button): 3,100 (90d)
> - PDF catalogs sent: 420 (90d)
> - eCat submitted orders: 47 (90d)
>
> Assessment: This team uses eCat heavily for selling — browsing, presenting, and sharing catalogs with buyers. Final orders enter through phone or EDI. eCat is driving the selling process even though it isn't capturing the transaction. To measure true selling value: presentation-to-close rate, not eCat order count.

**Action**: For non-submit-through accounts, reframe value metrics to presentation depth and engagement intensity. For partial-capture accounts, identify whether increasing eCat submit-through is a workflow optimization opportunity. For the client: "here's what your team uses eCat for, regardless of whether they submit orders through it."

**Customer Value**: Accurate characterization of how the team uses the platform. Avoids penalizing reps for using eCat as designed (catalog + selling) even when final orders close elsewhere.

**SuperCat Value**: Prevents Health V2 and the scorecard from systematically undervaluing enablement-heavy accounts. Creates a natural conversion narrative: "you're closing with eCat-presented products — routing orders through eCat would give you full-cycle visibility."

**Segments**: Most relevant for iPad-only, iPad+Catalog, and iPad+Catalog+Portal bundles. Less relevant for accounts already transactional (>25% submit-through).

**Complexity**: Moderate (Mixpanel behavioral events + eCat order count ratio)

**Data Dependency**: Mixpanel `user_feature_usage_report` + MCP `orders`

**Data Readiness**: Live

**Bundle Required**: Any bundle with `eCat iPad`

**Query IDs**: Q-46 (workflow maturity heuristic — to be added to query library)

**Allowed Claims**: Submit-through rate with band classification. | "Your team uses eCat as a selling layer even without full order submission." | Presentation-depth as primary value metric for non-submit-through accounts.

**Forbidden Claims**: "Low eCat submit volume = low platform value" | "Your team isn't using eCat" when behavioral signals are high

**Portability**: Fully portable. The four-band heuristic is a calibration guide — absolute thresholds should be adjusted based on portfolio distribution.

---

## Domain 2 — Instance Health & Data Quality

*Universally applicable. These are "check engine lights" — they flag problems the customer should fix. All MCP-only except VM-10.*

---

### VM-07: Catalog Completeness Score

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: catalog_completeness
**Customer-Facing Name**: Catalog Health Report

**Gating**: None. Applies to all accounts with a product catalog.

**Signal**: Count visible products (`hideable = false`) with missing images (`image_exists = false`) and missing prices (`net_price IS NULL`). Express as a completeness percentage for visible products. Report hidden products separately as context only. Compare against platform median.

**Example** *(BCF — validated)*:
> Visible products: 2,980 total
> - Complete (image + price): 2,453 (82.3%)
> - Missing images: 209 (7.0%)
> - Missing prices: 318 (10.7%)
>
> Hidden/inactive products: 447 — missing images here are expected and not flagged.
>
> Platform benchmark: Median catalog completeness for active accounts is 74%. BCF is above average — but closing the image gap on visible products would improve rep productivity and buyer conversion.

**Action**: Admin uploads missing images and sets missing prices for visible products. Prioritize products that appear in recent eCat orders or Smart Stacks.

**Customer Value**: Direct impact on rep and buyer experience. Incomplete visible products slow down the selling workflow.

**SuperCat Value**: Data quality drives platform engagement. Customers with >90% complete visible catalogs have higher eCat order velocity (testable hypothesis via cross-instance analysis).

**Segments**: All bundles.

**Complexity**: Simple (single query on `products` with `hideable` split)

**Data Dependency**: MCP `products`

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-07

**Allowed Claims**: Visible product completeness percentage. | Missing image and price counts for visible products. | Comparison to platform median.

**Forbidden Claims**: Flag missing images on hidden products as actionable | Completeness score that includes hidden products in numerator or denominator without disclosure

**Portability**: Fully portable.

**Note**: Health V2 §4.4 `catalog_completeness` uses the same underlying calculation. VM-07 provides the detailed per-product breakdown; Health V2 uses the aggregate percentage as an input to Operational Health scoring.

---

### VM-08: Data Freshness Monitor

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: data_freshness
**Customer-Facing Name**: Data Health Report

**Gating**: None.

**Signal**: Query `data_versions` for each entity type per org. Classify by days since last update: Fresh (≤30 days), Monitor (31–180 days), Stale (>180 days). Severity-ranked alerts.

**Example** *(BCF — validated)*:
> | Entity | Last Updated | Age | Status |
> |--------|-------------|-----|--------|
> | kit_items | 2026-02-18 | 27 days | Monitor |
> | sales_quotas | 2025-08-20 | 7 months | **Stale** |
> | price_levels | 2026-03-04 | 13 days | Fresh |
> | customers | Today | 0 days | Fresh |
> | inventories | Today | 0 days | Fresh |

**Action**: Admin triggers re-import of stale entities or disables unused features (sales_quotas if budget tracking is abandoned).

**Customer Value**: Prevents data quality issues before they impact reps or buyers.

**SuperCat Value**: Data freshness is a proxy for account health. Proactive alerting builds trust and prevents support escalation.

**Segments**: All bundles. Particularly critical for accounts with automated FTP imports.

**Complexity**: Simple (single query on `data_versions`)

**Data Dependency**: MCP `data_versions`

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-08

**Allowed Claims**: Entity-level freshness with age and status classification.

**Forbidden Claims**: Attribute business impact to freshness without supporting evidence

**Portability**: Fully portable.

**Note**: Health V2 §4.4 uses `days_since_critical_update` (max days since most recent update to products, customers, or inventory). VM-08 provides full entity-level detail; Health V2 uses the summary signal.

---

### VM-09: Import Health & Sync Reliability

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: import_health
**Customer-Facing Name**: Data Pipeline Health

**Gating**: Accounts with automated imports (FTP/API integration). For accounts managing data entirely through Admin Console (no import history), this VM is N/A — note in output.

**Signal**: Analyze `import_events` frequency and error patterns over time. Flag declining import frequency, import gaps, and error spikes.

**Example** *(BCF — validated)*:
> | Month | Imports | Assessment |
> |-------|--------:|-----------|
> | Mar 2026 | 74 (partial) | On track |
> | Feb 2026 | 98 | Stable |
> | Jan 2026 | 119 | Stable |
> | Oct 2025 | 225 | High (seasonal?) |
>
> Assessment: BCF maintains consistent daily imports. No errors in recent event data arrays. Healthy pipeline.

**Action**: For accounts with declining or erratic imports, alert CS and customer admin before stale data cascades.

**Customer Value**: Early warning on broken data pipelines.

**SuperCat Value**: Import failures are a top-3 support ticket driver. Proactive detection reduces support burden.

**Segments**: All bundles with automated imports.

**Complexity**: Simple (time-series aggregation on `import_events`)

**Data Dependency**: MCP `import_events`

**Data Readiness**: Live

**Bundle Required**: All (N/A for Admin Console-only data management)

**Query IDs**: Q-09

**Allowed Claims**: Monthly import count trend. | Presence or absence of error arrays in recent imports.

**Forbidden Claims**: Specific error root causes without parsing the `data` YAML field

**Portability**: Fully portable.

**Note**: Health V2 §4.4 `import_success_rate` is the scored version of this signal. VM-09 provides the detailed per-month trend; Health V2 uses the aggregate success rate.

---

### VM-10: Feature Enablement Gap Analysis

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: feature_enablement_gap
**Customer-Facing Name**: Feature Utilization Review

**Gating**: None.

**Signal**: Compare the client's enabled features (from `mobile_sites` flags + `organizations` properties) against features used by accounts on the same bundle type. Surface "available but not used" gaps and platform-wide adoption rates for context.

**Example** *(BCF — validated)*:
> Features enabled and well-used: Kit Builder (1,110 views, 188 orders), Product Configurator (CPQ) (7,306 configured items), Library (17,287 views), Enrollment (1,508 applicants).
>
> Features available in BCF's bundle but showing minimal usage:
> - Contract Pricing: Enabled. 0 contract prices loaded. 18 other accounts at BCF's bundle level use it.
> - Quick-Order Grid: Not enabled. High-volume buyers like BCF's top customers might benefit.

**Action**: Evaluate underutilized features. Connect CS conversation to bundle-peer adoption rates for context.

**Customer Value**: Surfaces features available in their bundle that they aren't using.

**SuperCat Value**: Feature activation = higher stickiness = lower churn.

**Segments**: All bundles. Gap analysis is bundle-aware — eCat Online features should not be listed as gaps for iPad-only clients.

**Complexity**: Moderate (cross-reference `mobile_sites` + `organizations` + cross-instance feature adoption rates)

**Data Dependency**: MCP `mobile_sites`, `organizations`, `kit_items`, `contract_prices`, `enrollment_applicants`, `smart_stacks`, `shared_resources`. BigQuery `insightful_product.segment_benchmarks_monthly` for adoption rates.

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-10

**Allowed Claims**: "This feature is available in your plan but not yet active." | Per-feature adoption rates across same-bundle accounts.

**Forbidden Claims**: List eCat Online features (Online Ordering, Private Storefront) as "gaps" for iPad-only clients — those are not gaps, they are expansion opportunities | "CPQ is an adoption gap" for accounts without CPQ subscription | "Full-stack deployment" | "Platform-Embedded deployment"

**Portability**: Fully portable. Bundle classification from Health V2 determines which features are in-scope.

**Note**: eCat Online engagement measurement adequacy is an open question in Health V2 (OD-5). Do not make stronger claims about eCat Online adoption scoring than current measurement supports.

---

### VM-11: Configuration Completeness

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: configuration_completeness
**Customer-Facing Name**: Platform Configuration Health

**Gating**: None.

**Signal**: Identify features that are enabled but incompletely configured — enabled but stale data (>30 days), or enabled but zero records loaded. Examples: sales quotas enabled but data 7 months stale; enrollment enabled but no processed applicants recently; contract pricing enabled but zero contracts loaded.

**Example** *(BCF — validated)*:
> Configuration Alert: Sales Quotas
> Data: enabled, 15,950 rows loaded. Last import: 2025-08-20 (7 months ago).
> Your Sales Intelligence Dashboard budget tracking may be showing outdated targets. Recommendation: Re-import current quota data or disable budget tracking to avoid misleading reps.

**Action**: Admin re-imports abandoned data or disables the feature to avoid platform noise.

**Customer Value**: Prevents "enabled but abandoned" features from creating confusion.

**SuperCat Value**: Clean configuration = fewer support tickets from stale data.

**Segments**: All bundles.

**Complexity**: Moderate (requires logic to detect "enabled but stale or empty" patterns)

**Data Dependency**: MCP `data_versions`, `sales_data`, `kit_items`, `contract_prices`

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-11

**Allowed Claims**: Feature is enabled but data is stale or unpopulated. | Specific recommendation to re-import or disable.

**Forbidden Claims**: Assert the client has abandoned a feature without confirming (ask first)

**Portability**: Fully portable.

---

### VM-47: Smart Stack Effectiveness

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: smart_stack_effectiveness
**Customer-Facing Name**: Curated List Performance

**Gating**: `smart_stacks` count > 0 AND Mixpanel stack interaction events available.

**Signal**: For each Smart Stack, calculate: view count (Mixpanel `view_smart_stack` events), the customers who viewed the stack, and whether those customers subsequently placed eCat orders containing stack items. Identify high-engagement stacks (high views, downstream orders) and stale stacks (created but never viewed or not updated in 90+ days).

**Example** *(illustrative)*:
> BCF has 124 Smart Stacks. Top performers:
> | Stack | Views (90d) | Customers Who Viewed | Post-View eCat Orders | Conversion |
> |-------|:---:|:---:|:---:|:---:|
> | Spring 2026 Intros | 87 | 23 | 14 | 61% |
> | Coastal Collection | 64 | 18 | 9 | 50% |
> | High-Velocity Reorders | 45 | 12 | 8 | 67% |
>
> Stale stacks (not viewed in 90 days): 38 of 124 (31%)
> Recommendation: Archive the 38 stale stacks to reduce clutter. Replicate the High-Velocity Reorders stack model — it shows the highest conversion rate.

**Action**: Archive stale stacks. Use high-converting stack structures as templates for new curation. Surface conversion data to reps who build stacks.

**Customer Value**: Quantifies whether the curation investment (building stacks) is paying off in eCat orders.

**SuperCat Value**: Smart Stack adoption is a stickiness signal. Showing stack ROI encourages more curation, which deepens platform engagement.

**Segments**: All bundles with `eCat iPad`. Most impactful for accounts with 10+ stacks.

**Complexity**: Moderate (Mixpanel stack interaction events + `orders` item join)

**Data Dependency**: MCP `smart_stacks`, `orders`. BigQuery Mixpanel `user_feature_usage_report` for stack view events.

**Data Readiness**: Live

**Bundle Required**: Any bundle with `eCat iPad`

**Query IDs**: Q-47 (to be added to query library)

**Allowed Claims**: Stack view counts. | Post-view eCat order rate for customers who viewed each stack. | Stale stack identification.

**Forbidden Claims**: Attribute revenue exclusively to a stack view (correlation, not causation) | Stack performance for stacks with fewer than 5 views

**Portability**: Fully portable. Stack names are client-defined but stack IDs and Mixpanel events are standardized.

---

### VM-50: Library / Document Engagement Effectiveness

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: Non-commerce
**Internal Name**: library_document_engagement
**Customer-Facing Name**: Digital Library Performance

**Gating**: Mixpanel `view_document` and `email_document` events must be present for the org. Some orgs have sparse document-level event coverage — validate before running.

**Signal**: For each `shared_resources` document, calculate: view count (Mixpanel `view_document`), email share count (Mixpanel `email_document`), and days since last activity. Identify high-engagement documents, under-used documents, and stale resources not accessed in 90+ days.

**Example** *(BCF — validated)*:
> BCF has 162 library resources. Total views: 17,287. Total email shares: 444.
>
> Top-performing documents (views + shares):
> | Document | Views (90d) | Emails Sent | Last Accessed |
> |----------|:---:|:---:|:---:|
> | 2026 Spring Catalog | 1,840 | 94 | Today |
> | Trade Program Overview | 1,120 | 67 | 3 days ago |
> | Installation Guide Series | 876 | 12 | 8 days ago |
>
> Stale documents (no activity >90 days): 34 of 162 (21%)
> Recommendation: Archive stale resources or update them for the current season.

**Action**: Archive stale documents. Identify what content reps rely on most and ensure it's current. Use email-share data to understand what reps send to customers.

**Customer Value**: The library is a core selling tool for content-heavy accounts. Engagement data shows what's working.

**SuperCat Value**: Library engagement is one of the strongest per-account stickiness signals. Accounts with high library usage churn at lower rates.

**Segments**: All bundles with `eCat iPad` and active `shared_resources`. Most impactful for content-heavy accounts (BCF: 17,287 views, 162 resources).

**Complexity**: Moderate (Mixpanel document events + `shared_resources` join)

**Data Dependency**: MCP `shared_resources`. BigQuery Mixpanel `user_feature_usage_report` for `view_document`, `email_document` events.

**Data Readiness**: Conditional Live — dependent on Mixpanel document event coverage per org. Validate coverage before running.

**Bundle Required**: Any bundle with `eCat iPad`

**Query IDs**: Q-50 (to be added to query library)

**Allowed Claims**: Document view and email share counts where Mixpanel coverage is confirmed. | Stale document identification. | Top-performing content by engagement.

**Forbidden Claims**: Attribute sales outcomes to document views | Claims about document performance for orgs with incomplete Mixpanel coverage

**Portability**: Query portable — interpretation varies by content strategy. Document names are client-defined.

---

## Domain 3 — Customer & Buyer Intelligence

*High customer value, strong retention signal. Surfaces patterns in the customer's dealer/buyer network that they often can't see themselves.*

---

### VM-12: eCat Customer Activation & ERP Penetration

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction (primary) + ERP total-business (secondary context)
**Internal Name**: ecat_customer_activation
**Customer-Facing Name**: Buyer Network Activation Report

**Gating**: Active eCat orders (`orders` table with submitted orders).

**Signal**: 
- **Primary metric** (eCat retention rate): `active_12mo` / `total_ever_ordered_via_ecat` — of all buyers who have ever placed an eCat order, what share is still active?
- **Secondary context** (ERP penetration): `total_ever_ordered_via_ecat` / `total_erp_customers` — what fraction of all ERP-loaded customer records have ever used eCat?

The ERP customer count is context, not the activation denominator. Most ERP-loaded accounts represent years of accumulated trade relationships — many of which were never intended for eCat ordering.

**Example** *(BCF — based on v2 query Q-12)*:
> **Primary: eCat Retention**
> | Window | eCat Active Buyers | of Total Ever Ordered | Retention |
> |--------|-------------------:|:---:|:---:|
> | 12 months | 373 | 486 | **76.7%** |
> | 6 months | 263 | 486 | 54.1% |
> | 3 months | 187 | 486 | 38.5% |
>
> 113 buyers (23.3%) placed eCat orders in prior years but not in the trailing 12 months — recently lapsed eCat users, highest reactivation potential.
>
> **Secondary: ERP Penetration**
> 486 buyers have ever ordered via eCat out of 1,983 ERP-loaded accounts (24.5%). The remaining 1,497 ERP accounts have no eCat order history — some may be candidates for activation, others may be historical records not intended for eCat.

**Action**: Segment the 113 recently lapsed eCat buyers for targeted reactivation outreach. Separately, evaluate whether any of the 1,497 never-activated ERP accounts are realistic eCat adoption candidates.

**Customer Value**: Accurate picture of eCat buyer network health. Separates "buyers who've lapsed from eCat" (reactivatable) from "accounts that have never used eCat" (different conversation).

**SuperCat Value**: eCat dormancy reactivation = more orders = stronger platform ROI. ERP penetration context creates the expansion conversation.

**Segments**: Commerce-active bundles (iPad+Catalog+Cart, Full). For iPad-only: substitute "customers who have logged in" for ordering activity.

**Complexity**: Moderate (Q-12 with corrected denominator logic)

**Data Dependency**: MCP `orders`, `customers`

**Data Readiness**: Live

**Bundle Required**: iPad+Catalog+Cart, Full (ordering bundles)

**Query IDs**: Q-12

**Allowed Claims**: eCat retention rate using `total_ever_ordered_via_ecat` as denominator. | Lapsed eCat buyer count and segmentation. | ERP penetration rate as secondary context.

**Forbidden Claims**: "81% of your dealers are dormant" using ERP customer total as denominator | "Net-new customers" | Treating all ERP accounts as intended eCat users

**Portability**: Fully portable. The corrected denominator (`total_ever_ordered`) is standardized. ERP penetration rate interpretation varies by how the client manages their customer master.

---

### VM-13: Customer Concentration Risk (eCat)

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: customer_concentration_ecat
**Customer-Facing Name**: Customer Concentration Analysis

**Gating**: Active eCat orders (12 months).

**Signal**: Calculate eCat GMV concentration across the buyer base. Flag accounts where a small number of buyers represent a disproportionate share of eCat revenue. Also surface rep-level concentration risk.

**Example** *(BCF — validated)*:
> eCat GMV concentration (trailing 12 months):
> - Top buyer (Trident Furnishings): 4.7% of eCat GMV
> - Top 5 buyers: 13.0%
> - Top 10 buyers: 20.8%
>
> Assessment: Well-distributed eCat revenue. No single-buyer dependency.
>
> Rep-level: Barbara Harper generates 28% of eCat GMV from a single buyer. Even with healthy account-level distribution, rep-level concentration is a risk.

**Action**: Monitor rep-level concentration alongside account-level. A healthy customer mix can mask dangerous rep dependency.

**Customer Value**: Risk awareness at both the account and rep level.

**SuperCat Value**: Retention signal. High concentration accounts are at higher churn risk if a key buyer relationship breaks.

**Segments**: Commerce-active bundles.

**Complexity**: Simple (eCat `orders` aggregation by `customer_num`)

**Data Dependency**: MCP `orders`

**Data Readiness**: Live

**Bundle Required**: iPad+Catalog+Cart, Full

**Query IDs**: Q-13

**Allowed Claims**: eCat GMV concentration percentages. | Top buyer and top-5 buyer share of eCat GMV.

**Forbidden Claims**: Total-business concentration (this is eCat-channel only) | Implied conclusions about business risk without broader ERP context

**Portability**: Fully portable.

---

### VM-14: Customer Reorder Frequency & Velocity (eCat)

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: customer_reorder_velocity
**Customer-Facing Name**: Buyer Activity Report

**Gating**: Active eCat buyers with 3+ orders in trailing 12 months.

**Signal**: For active eCat buyers, calculate average days between eCat orders, order frequency trend, and identify buyers whose eCat reorder velocity is declining.

**Example** *(BCF — validated)*:
> Top buyers by eCat reorder frequency:
> | Buyer | eCat Orders (12mo) | Avg Days Between | eCat GMV |
> |-------|:---:|:---:|---:|
> | Outer Banks Furniture | 89 | 4.0 days | $170K |
> | W.F. Booth & Son | 74 | 4.9 days | $116K |
> | Trident Furnishings | 61 | 6.0 days | $303K |
>
> Buyers ordering less frequently than every 14 days show 3x higher lapsing risk.

**Action**: Flag buyers whose eCat order frequency drops below their historical baseline. Reach out proactively.

**Customer Value**: Early warning on lapsing eCat buyers.

**SuperCat Value**: eCat order velocity is the primary platform health signal. Declining velocity is an early churn predictor.

**Segments**: Commerce-active bundles.

**Complexity**: Moderate (time-series calculation per buyer in eCat `orders`)

**Data Dependency**: MCP `orders`

**Data Readiness**: Live

**Bundle Required**: iPad+Catalog+Cart, Full

**Query IDs**: Q-14

**Allowed Claims**: eCat reorder frequency and trend per buyer. | Lapsing risk flag based on frequency decline.

**Forbidden Claims**: Total-business reorder frequency (eCat-only data) | Conclusions about overall buyer health without ERP context

**Portability**: Fully portable.

---

### VM-15: Enrollment Funnel Analysis

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: Non-commerce
**Internal Name**: enrollment_funnel
**Customer-Facing Name**: Buyer Registration Funnel

**Gating**: `enrollment_applicants` count > 0 (Buyer Registration feature enabled and in use).

**Signal**: Track enrollment applicants through the funnel: applied → accepted/rejected → first eCat login → first eCat order. Identify conversion bottlenecks.

**Example** *(BCF — validated)*:
> | Stage | Count | Conversion |
> |-------|------:|:----------:|
> | Total applicants | 1,508 | — |
> | Accepted | 1,218 | 80.8% |
> | Rejected | 288 | 19.1% |
> | Pending | 2 | 0.1% |
>
> Open question: Of the 1,218 accepted applicants, how many have placed their first eCat order? Join `enrollment_applicants` (accepted) against `orders` on customer matching. See VM-44 for time-to-first-order analysis.

**Action**: Track time-to-first-eCat-order for accepted applicants. If >30 days, investigate onboarding friction. Feeds VM-44.

**Customer Value**: Buyer Registration is a growth channel. If accepted dealers aren't converting to eCat buyers, the registration process is generating leads but not revenue.

**SuperCat Value**: Enrollment-to-first-order conversion is a platform health metric.

**Segments**: Accounts with Buyer Registration enabled (~68 orgs, ~28% of platform).

**Complexity**: Moderate (`enrollment_applicants` + `orders` join on customer matching)

**Data Dependency**: MCP `enrollment_applicants`, `orders`

**Data Readiness**: Live — gated by enrollment enablement

**Bundle Required**: Any bundle with `eCat Online - Closed Site` or `eCat Online - Catalog` (Buyer Registration feature)

**Query IDs**: Q-15

**Allowed Claims**: Acceptance rate and funnel stage breakdown. | First-eCat-order conversion rate (when joined to `orders`).

**Forbidden Claims**: "Accepted applicants = new customers" (not confirmed eCat buyers until they order) | "Net-new customers"

**Portability**: Fully portable — gated by enrollment flag.

---

### VM-16: ERP Total Business Visibility

**Audience**: Dual [D]
**Commerce Lens**: ERP total-business
**Internal Name**: erp_total_business
**Customer-Facing Name**: Total Business Overview (via Sales Intelligence Dashboard)

**Gating**: `portal_orders` data present (Sales Portal / Sales Intelligence Dashboard enabled and ERP sync active).

**Signal**: Use `portal_orders` to show total business volume across all channels: eCat, direct, EDI, trade shows, showroom. Surface order-origin mix (where available via `order_origin` field), total GMV, and seasonality patterns that are only visible in ERP-synced data.

**Example** *(BCF — based on v2 query Q-16)*:
> Total ERP orders (trailing 12 months): 4,891
> eCat-originated orders in ERP: 1,773 (36.2%)
> Trade show / market orders: 847 (17.3%)
> Direct / phone / EDI: 2,271 (46.5%)
>
> Your Sales Intelligence Dashboard shows the full picture of your business — eCat, trade shows, and direct channels combined. eCat represents 36% of total order volume.

**Action**: Use ERP totals for seasonality planning and capacity planning. Use eCat share figure to frame platform ROI conversation (VM-45 provides the dedicated capture rate analysis).

**Customer Value**: Visibility into total business context that complements eCat-specific data. Trade show seasonality and direct channel contribution visible here.

**SuperCat Value**: Frames eCat's contribution within the client's real business — makes the platform ROI story honest and credible.

**Segments**: Accounts with Sales Portal / Sales Intelligence Dashboard and active ERP sync.

**Complexity**: Simple (aggregation on `portal_orders` by `order_origin`)

**Data Dependency**: MCP `portal_orders`

**Data Readiness**: Live — gated by `portal_orders` presence

**Bundle Required**: iPad+Catalog+Portal, Full

**Query IDs**: Q-16 *(Note: Q-16 interpretation block updated — this query shows ERP-synced total business, NOT buyer self-service activity on a portal)*

**Allowed Claims**: Total ERP order volume across all channels. | Order-origin breakdown (eCat vs. trade show vs. direct) where `order_origin` field is populated. | Seasonality patterns from full business data.

**Forbidden Claims**: "`portal_orders` = buyer self-service orders" | "Portal ordering adoption" using `portal_orders` | "Buyer self-service" when referring to `portal_orders` data | "Buyers are ordering on the portal" based on `portal_orders` counts

**Portability**: Data-gated. Only available for Sales Portal clients with active ERP sync. `order_origin` field population varies by client.

---

### VM-17: Dormant eCat Customer Identification

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: dormant_ecat_customers
**Customer-Facing Name**: Lapsed Buyer Report

**Gating**: Active eCat order history.

**Signal**: Identify buyers who placed eCat orders in a prior period but not in the current period. Segment by their historical eCat value (high-value lapsed vs. low-value). Distinguish: "dormant eCat buyers" (ordered before, not recently) from "never activated via eCat" (distinct segment, see VM-12).

**Sub-view: At-Risk High-Value eCat Buyers**:
Rank buyers by trailing-12-month eCat GMV, then flag those with no eCat order in the last 90 days.

**Example** *(BCF — validated)*:
> Of 486 all-time eCat buyers:
> - 373 active in last 12 months
> - 113 placed eCat orders 7–24 months ago but NOT in the last 12 months — **recently lapsed eCat buyers, highest reactivation potential**
> - 76 placed eCat orders 4–12 months ago but NOT in last 3 months — **lapsing, urgent outreach window**
>
> At-Risk High-Value Sub-view: 4 buyers with >$10K trailing-12mo eCat GMV have not placed an eCat order in 90+ days.

**Action**: Generate a lapsed eCat buyer list with territory assignment. Assign to reps for targeted outreach.

**Customer Value**: Turns aggregate dormancy data into a prioritized outreach list.

**SuperCat Value**: eCat reactivation = more orders = platform GMV growth.

**Segments**: Commerce-active bundles.

**Complexity**: Moderate (eCat `orders` time-window analysis per buyer)

**Data Dependency**: MCP `orders`, `customers`

**Data Readiness**: Live

**Bundle Required**: iPad+Catalog+Cart, Full

**Query IDs**: Q-17

**Allowed Claims**: Lapsed eCat buyer count by dormancy window. | At-risk high-value eCat buyer list with last order date.

**Forbidden Claims**: "Dormant" applied to buyers who have never ordered via eCat (that's "not yet activated") | "Net-new customers"

**Portability**: Fully portable.

---

### VM-41: First-Time eCat Orderers by Channel & Rep

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: first_time_ecat_orderers
**Customer-Facing Name**: New eCat Buyer Acquisition Report

**Gating**: Active eCat order history (12+ months of data for meaningful trend).

**Signal**: Track buyers whose first-ever eCat order falls within the reporting period. Attribute by channel (`order_source = 'ipad'` = rep-acquired, `order_source = 'server'` = eCat Online self-acquired) and by rep for iPad-acquired buyers. Keep enrollment pipeline data separate — enrollment acceptance ≠ proven eCat ordering.

**Example** *(BCF — validated, 15 months Jan 2025–Mar 2026)*:
> | Month | Rep-Acquired (iPad) | eCat Online-Acquired (server) | Total |
> |-------|:---:|:---:|:---:|
> | Jan 2025 | 7 | 4 | 11 |
> | Jun 2025 | 13 | 3 | 16 |
> | Jan 2026 | 8 | 5 | 13 |
> | **15-month total** | **113 (68%)** | **54 (32%)** | **167** |
>
> Top reps by first-time eCat buyer acquisition: Sharyn Moss (20), Katrinka Barnhart (15), Jerry Montini (12).
>
> Enrollment pipeline (separate): ~30 applications/month, 80.6% acceptance rate — these are accepted registrations, not confirmed eCat orderers.

**Action**: Surface during QBR as "here is how your eCat buyer base is growing." Pair with VM-17 (lapsed eCat buyers) for full lifecycle view: "you added 167 first-time eCat buyers this period while 113 lapsed — net eCat buyer base change."

**Customer Value**: Growth visibility by channel and rep. Quantifies eCat Online's contribution to buyer acquisition independently from rep activity.

**SuperCat Value**: eCat Online-acquired buyers (54, 32% of total) demonstrate direct platform ROI independent of the rep team.

**Segments**: Commerce-active bundles. Enrollment pipeline data available for enrollment-enabled accounts.

**Complexity**: Simple (CTE + aggregation on eCat `orders` for first-time buyers; separate aggregation on `enrollment_applicants`)

**Data Dependency**: MCP `orders` (first-time eCat buyers), `enrollment_applicants` (pipeline context only)

**Data Readiness**: Live

**Bundle Required**: iPad+Catalog+Cart, Full

**Query IDs**: Q-41

**Allowed Claims**: First-time eCat orderer count by channel (iPad vs. eCat Online) and rep. | Enrollment pipeline as a leading indicator (applications, acceptance rate).

**Forbidden Claims**: "Net-new customers" | "eCat Online-acquired buyers are net-new accounts" (they may have pre-existing ERP relationships) | Enrollment acceptances = proven eCat buyers

**Portability**: Fully portable. `order_source` values are standardized.

---

### VM-44: Onboarding Velocity / Time-to-First-eCat-Order

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: eCat transaction
**Internal Name**: onboarding_velocity
**Customer-Facing Name**: Buyer Onboarding Report

**Gating**: `enrollment_applicants` with accepted status AND joining `orders` to find first eCat order. Gate: enrollment enabled.

**Signal**: For accepted enrollment applicants, calculate the cohort distribution of time from acceptance to first eCat order. Identify the median days-to-first-order, the % who have converted at 30/60/90-day marks, and the % who have never converted.

**Example** *(illustrative)*:
> Accepted applicants in trailing 12 months: 412
> | Time Window | Converted to First eCat Order | Conversion Rate |
> |-------------|:---:|:---:|
> | Within 30 days | 89 | 21.6% |
> | 31–60 days | 52 | 12.6% |
> | 61–90 days | 31 | 7.5% |
> | 90+ days (still waiting) | 48 | 11.7% |
> | Never converted (>90 days, no order) | 192 | 46.6% |
>
> Median time to first eCat order (for those who converted): 19 days.
> 46.6% of accepted applicants have not placed any eCat order — this is the onboarding conversion gap.

**Action**: Implement an onboarding sequence for accepted applicants who haven't placed their first eCat order within 30 days (welcome email, rep assignment, first-order prompt). Track whether the sequence improves 30-day conversion.

**Customer Value**: Enrollment is a growth channel — accepted buyers who don't convert represent a wasted opportunity. The time-to-first-order metric makes the onboarding gap concrete and actionable.

**SuperCat Value**: Enrollment-to-first-order conversion is a platform health metric. Low conversion = enrollment investment generating leads but not eCat volume.

**Segments**: Enrollment-enabled accounts (~68 orgs).

**Complexity**: Moderate (`enrollment_applicants` accepted + `orders` first-order join)

**Data Dependency**: MCP `enrollment_applicants`, `orders`, `customers`

**Data Readiness**: Live — gated by enrollment data

**Bundle Required**: Any bundle with Buyer Registration enabled

**Query IDs**: Q-44 (to be added to query library)

**Allowed Claims**: Acceptance-to-first-eCat-order conversion rates at 30/60/90-day windows. | Median time-to-first-order for converted buyers. | Percentage of accepted applicants with no eCat order.

**Forbidden Claims**: Acceptance = eCat buyer | "Net-new customers"

**Portability**: Fully portable for enrollment-enabled accounts.

---

### VM-49: Buyer-Level Repeat Purchase

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: ERP total-business
**Internal Name**: buyer_repeat_purchase
**Customer-Facing Name**: Buyer Loyalty Report

**Gating**: `portal_orders` buyer attribution present (buyer-level attribution in `portal_orders` — coverage varies by org and ERP sync configuration). Validate buyer attribution before running.

**Signal**: For accounts with buyer-attributed `portal_orders`, calculate repeat purchase rates at the buyer level: buyers who placed their first order in a given period and returned within 90/180 days. Identifies buyer loyalty patterns across all channels (not just eCat).

**Example** *(illustrative)*:
> Buyers with first `portal_orders` order in Q4 2025: 84
> | Window | Returned with 2nd Order | Repeat Rate |
> |--------|:---:|:---:|
> | Within 90 days | 54 | 64.3% |
> | Within 180 days | 67 | 79.8% |
> | No repeat order (>180 days) | 17 | 20.2% |

**Action**: Identify first-time buyers who haven't returned. Targeted outreach by assigned rep.

**Customer Value**: Buyer loyalty visibility across all channels — not just eCat.

**SuperCat Value**: Buyer repeat purchase rate is a proxy for the health of the client's dealer relationships. Declining rates are a business signal.

**Segments**: Accounts with Sales Portal and buyer-attributed `portal_orders`. Most relevant for Full bundle accounts.

**Complexity**: Moderate (`portal_orders` buyer cohort analysis)

**Data Dependency**: MCP `portal_orders` (buyer attribution required)

**Data Readiness**: Conditional Live — primary dependency is `portal_orders` buyer attribution field. Not universally populated.

**Bundle Required**: iPad+Catalog+Portal, Full

**Query IDs**: Q-49 (to be added to query library)

**Allowed Claims**: Buyer repeat purchase rate where buyer attribution is confirmed in `portal_orders`. | Cohort return rates at 90/180-day windows.

**Forbidden Claims**: Apply this VM to orgs without confirmed buyer attribution in `portal_orders` | Claim buyer-level data when only aggregate `portal_orders` are available

**Portability**: Data-gated. Conditional on buyer attribution field population.

---

## Domain 4 — eCat Commerce Analytics

*Deepens eCat platform value. Surfaces trends and patterns in eCat-channel behavior that inform strategy and operations.*

---

### VM-18: eCat Order Velocity & Trend (with ERP Context)

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction (primary) + ERP total-business (context layer)
**Internal Name**: ecat_order_velocity
**Customer-Facing Name**: eCat Order Performance Report

**Gating**: Active eCat orders.

**Signal**: 
- **Part A (eCat transaction lens)**: Monthly eCat order count, GMV, and trend from `orders`. Surface iPad vs. eCat Online split where applicable.
- **Part B (ERP context layer)**: Monthly total order count and GMV from `portal_orders`. Calculate eCat share of total business. Show seasonality patterns visible only from full ERP data.

**Example** *(BCF — validated using Q-18 Part A + Part B)*:
> eCat orders: ~200–250/month, stable trend. Seasonal December dip ~30%.
> ERP total orders: ~400/month. eCat share: ~52% of total ERP order volume.
> Trade show / market orders visible in `portal_orders` — seasonal spike in Oct–Nov explains Nov eCat share decline.

**Action**: Use seasonal patterns for capacity planning, promotional timing, and rep goal-setting. Use eCat share % to frame platform ROI.

**Customer Value**: Both the eCat-specific view (what the platform does) and the total business context (what eCat's contribution is).

**SuperCat Value**: eCat velocity is the primary platform health signal. ERP context makes the ROI story credible.

**Segments**: Commerce-active bundles for Part A. Part B additionally requires `portal_orders`.

**Complexity**: Simple (monthly aggregation from two sources)

**Data Dependency**: MCP `orders` (Part A), MCP `portal_orders` (Part B — present only with Sales Portal)

**Data Readiness**: Live (Part A for all commerce accounts; Part B gated to `portal_orders` presence)

**Bundle Required**: Part A: iPad+Catalog+Cart, Full. Part B: additionally requires iPad+Catalog+Portal or Full.

**Query IDs**: Q-18

**Allowed Claims**: eCat order volume and GMV trend. | eCat share of total ERP business (when Part B data present). | Seasonal pattern from eCat data (Part A) and full business data (Part B).

**Forbidden Claims**: ERP total volume = eCat volume | Attribute non-eCat channels to eCat performance

**Portability**: Part A fully portable. Part B data-gated to `portal_orders` clients.

---

### VM-19: eCat Channel Mix Evolution

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: eCat transaction
**Internal Name**: ecat_channel_mix
**Customer-Facing Name**: eCat Ordering Channel Report

**Gating**: `has_cart = true` AND confirmed `order_source = 'server'` orders in the data. Do not show channel mix for iPad-only clients — there is no mix when only one channel exists.

**Signal**: Track the ratio of iPad-originated eCat orders (`order_source = 'ipad'`) vs. eCat Online orders (`order_source = 'server'`) over time within the `orders` table. Surface the trajectory and what it means for the client's digital selling strategy.

**Example** *(BCF — validated)*:
> | Month | iPad Orders | eCat Online Orders | Online Share |
> |-------|:---:|:---:|:---:|
> | Mar 2026 | 81 | 67 | 45% |
> | Feb 2026 | 121 | 126 | 51% |
> | Jan 2026 | 91 | 113 | 55% |
>
> eCat Online ordering has reached near-parity with iPad ordering (Jan 2026: 55%). The overall trend shows buyer self-service growing as a share of total eCat volume — complementary to rep selling, not a replacement.

**Action**: Ensure the Online Ordering experience is optimized (inventory freshness, product completeness) as buyer self-service grows. Frame as: "your buyers are increasingly ordering directly — investing in the online catalog experience compounds over time."

**Customer Value**: Understanding the iPad vs. Online Ordering shift informs investment decisions (rep training vs. online catalog improvement).

**SuperCat Value**: Channel mix evolution is a key segmentation signal. Tracking the shift to Online Ordering predicts bundle upgrade readiness.

**Segments**: Accounts with Online Ordering (B2B Cart) confirmed active. Not applicable to iPad-only accounts.

**Complexity**: Simple (`order_source` aggregation from `orders`)

**Data Dependency**: MCP `orders`

**Data Readiness**: Live — gated to `has_cart = true` with server orders confirmed

**Bundle Required**: iPad+Catalog+Cart, Full

**Query IDs**: Q-19 (derived from Q-18 Part A `ipad_orders` / `eol_orders` columns)

**Allowed Claims**: iPad vs. eCat Online order split and trend within `orders`. | "Your buyers are increasingly placing orders directly through your Online Ordering channel."

**Forbidden Claims**: Show eCat Online as a channel for iPad-only clients | "100% iPad / 0% eOL" as a "channel mix" when only one channel exists | Reference `portal_orders` as a channel in this VM

**Portability**: Data-gated — only applicable when B2B Cart is confirmed active and server orders exist.

---

### VM-20: eCat AOV Analysis

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: ecat_aov
**Customer-Facing Name**: eCat Order Value Analysis

**Gating**: Active eCat orders (10+ orders per dimension for meaningful averages).

**Signal**: eCat Average Order Value by rep, by buyer, by channel, over time. Surface outliers and trends — reps with unusually high or low AOV, buyers with declining AOV, channel-specific AOV differences.

**Example** *(BCF — validated)*:
> | Dimension | eCat AOV | Context |
> |-----------|:---:|---------|
> | All eCat orders | $2,525 | — |
> | iPad orders | $2,783 | 10% higher than eCat Online |
> | eCat Online orders | $2,254 | Self-service orders tend to be smaller |
> | Top rep (Jack Johnson) | $5,599 | 2.2x eCat average |
> | Quotes (22 orders) | $2,994 | Higher AOV — quotes used for larger deals |
>
> Opportunity: Only 22 of 2,557 eCat orders (0.9%) used the Quote workflow. Given that quotes show 19% higher AOV, expanding Quote usage for larger deals could improve eCat GMV capture.

**Action**: Review Quote workflow adoption. Train reps on using Quotes for orders above a threshold (e.g., $5,000).

**Customer Value**: Granular eCat AOV visibility by dimension. Identifies workflow optimization opportunities.

**SuperCat Value**: Quote feature adoption = deeper platform integration.

**Segments**: Commerce-active bundles.

**Complexity**: Simple (eCat `orders` aggregation with segmentation)

**Data Dependency**: MCP `orders`

**Data Readiness**: Live

**Bundle Required**: iPad+Catalog+Cart, Full

**Query IDs**: Q-20

**Allowed Claims**: eCat AOV by rep, buyer, channel, order type. | Quote vs. non-Quote AOV comparison within eCat orders.

**Forbidden Claims**: Total-business AOV (eCat-only data) | "Your average deal size is $X" without clarifying this is eCat-only

**Portability**: Fully portable.

---

### VM-21: eCat Order Type & Workflow Analysis

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction
**Internal Name**: ecat_order_type
**Customer-Facing Name**: eCat Workflow Analysis

**Gating**: Active eCat orders.

**Signal**: Break down eCat orders by `order_type` (Confirmed, Quote, HFC) and `order_source` to surface workflow patterns. Identify underutilized workflows.

**Example** *(BCF — validated)*:
> | Type | eCat Orders | % | eCat GMV | Avg Value |
> |------|:---:|:---:|---:|---:|
> | Confirmed | 2,535 | 99.1% | $6.40M | $2,524 |
> | Quote | 22 | 0.9% | $66K | $2,994 |
>
> BCF uses almost exclusively Confirmed orders. If their sales process involves negotiations or approvals, routing through the Quote workflow would provide better audit trails and visibility.

**Action**: Evaluate whether the Confirmed-only pattern is intentional or a training gap.

**Customer Value**: Workflow optimization — ensures the platform matches the actual selling process.

**SuperCat Value**: Quote workflow adoption increases platform involvement in the sales process.

**Segments**: Commerce-active bundles.

**Complexity**: Simple (eCat `orders` aggregation by `order_type`)

**Data Dependency**: MCP `orders`

**Data Readiness**: Live

**Bundle Required**: iPad+Catalog+Cart, Full

**Query IDs**: Q-21

**Allowed Claims**: eCat order type distribution. | Quote vs. Confirmed AOV comparison within eCat.

**Forbidden Claims**: Total-business workflow analysis (eCat-only)

**Portability**: Fully portable.

---

### VM-22: Feature Usage Depth (Behavioral)

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: feature_usage_depth
**Customer-Facing Name**: Platform Feature Usage Report

**Gating**: Mixpanel behavioral data available.

**Signal**: Aggregate Mixpanel iPad events per org to surface feature usage intensity. Compare against platform averages for accounts on the same bundle. Identify heavily used features (validates investment) and underused features (adoption opportunity).

**Example** *(BCF — validated)*:
> | Feature | BCF Activity | Signal |
> |---------|:---:|---|
> | Product Configurator (CPQ) (7,173 items configured) | Very High | Core workflow — power CPQ user |
> | Digital Library (17,287 views, 444 emails) | Very High | Content-heavy operation |
> | Curated Lists / Smart Stacks (2,147 views) | High | Active curation |
> | PDF Catalogs (1,183 started, 867 generated, 73% completion) | High | 27% abandonment may indicate UX friction |
> | Customer Favorites (227 views) | Low | Underutilized for 486-buyer active base |

**Action**: Investigate PDF catalog abandonment (27% drop-off). Promote Customer Favorites to reps.

**Customer Value**: Quantifies how the sales team actually uses the platform. Identifies features that could drive more value if better adopted.

**SuperCat Value**: Feature depth = stickiness. Accounts using 5+ features churn at far lower rates.

**Segments**: All bundles with active iPad users. Note: eCat Online engagement measurement adequacy is an open decision in Health V2 (OD-5) — do not make stronger claims about eCat Online adoption scoring than current measurement supports.

**Complexity**: Moderate (Mixpanel event aggregation per org + optional Clicky join for portal accounts)

**Data Dependency**: BigQuery `org_feature_usage_report`. Enrichment: BigQuery `clicky_analytics` for `has_clicky = true` accounts.

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-22

**Allowed Claims**: Feature event counts and intensity levels. | Comparison to same-bundle peer accounts.

**Forbidden Claims**: Use "Platform-Embedded" / "Commerce-Active" / "Catalog-Focused" labels in client-facing text | "You're using eCat Online heavily" when eCat Online engagement measurement is not well-validated for this org's bundle (Health V2 OD-5)

**Portability**: Fully portable.

---

### VM-45: eCat Capture Rate vs. Total Business

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: Comparative capture
**Internal Name**: ecat_capture_rate
**Customer-Facing Name**: eCat Platform Penetration Report

**Gating**: `portal_orders` data present AND `orders` data present. If `portal_orders` is absent, this VM is N/A — do not approximate without a denominator.

**Signal**: Calculate eCat's share of total business across three dimensions:
1. **eCat order count share**: eCat `orders` (submitted) / `portal_orders` total order count
2. **eCat GMV share**: eCat `orders.total` sum / `portal_orders.total_amount` sum
3. **Platform capture model**: categorize the client's eCat posture based on capture rate

| eCat GMV Share | Posture |
|----------------|---------|
| > 50% | Primary transaction system |
| 25–50% | Meaningful eCat channel; dual-system |
| 10–25% | Partial capture; eCat is growing |
| < 10% | Enablement-heavy; eCat captures little of total volume |

**Example** *(BCF — based on Q-18 Part A + Part B data)*:
> eCat orders (trailing 12 months): 1,773
> ERP total orders (`portal_orders`): ~4,891
> eCat capture rate by order count: 36.2%
> eCat capture rate by GMV: ~38% (estimated from Q-18 Part B structure)
>
> Posture: Meaningful eCat channel — dual-system. eCat processes more than a third of total order volume.
> Opportunity: The 64% of orders placed outside eCat represent the platform's expansion headroom within this account.

**Action**: Use capture rate to frame platform ROI: "eCat already handles X% of your total business volume." For partial-capture accounts (<25%), identify whether increasing eCat submit-through is an achievable workflow goal.

**Customer Value**: Answers the strategic question: "how much of our real business actually runs through eCat?" — a question most clients have intuitions about but not data.

**SuperCat Value**: eCat capture rate is the most honest platform ROI metric. It makes the expansion headroom concrete: "you have Y% of your business still flowing outside eCat."

**Segments**: Accounts with both `orders` and `portal_orders` data (Sales Portal clients with active ERP sync). Full bundle primarily; iPad+Catalog+Portal where ERP sync is active.

**Complexity**: Moderate (join of `orders` GMV + `portal_orders` GMV by month)

**Data Dependency**: MCP `orders` + MCP `portal_orders`

**Data Readiness**: Live — gated to clients with `portal_orders`

**Bundle Required**: iPad+Catalog+Portal, Full

**Query IDs**: Q-45 (to be added; builds on Q-18 Part A + Part B structure)

**Allowed Claims**: eCat order count and GMV share of total ERP business. | eCat capture posture classification. | "eCat processes X% of your total order volume."

**Forbidden Claims**: Run this VM without a `portal_orders` denominator | Attribute non-eCat orders to eCat channel performance | Frame low capture rate as failure (it may reflect legitimate multi-channel business structure)

**Portability**: Data-gated. Only available for Sales Portal clients with ERP sync. `order_origin` field in `portal_orders` varies by ERP integration.

---

## Domain 5 — Product & Inventory Intelligence

*Manufacturer business intelligence. These are "how is your business performing" insights — not platform analytics.*

---

### VM-37: Inventory × Sales Intelligence

**Audience**: Dual [D]
**Commerce Lens**: ERP total-business
**Internal Name**: inventory_sales_crossref
**Customer-Facing Name**: Inventory & Sales Opportunity Report

**Gating**: Both `sales_data` (ERP-invoiced sales history) and `inventories` (current stock levels) present for the org.

**Signal**: Cross-reference historical sales volume per product (`sales_data.amount_invoiced`, `quantity_invoiced`) with current inventory levels (`inventories.qty_available`, `qty_on_hand`, `qty_on_backorder`). Surface top sellers with zero or critically low current inventory.

**Important limitation**: `inventories` is a point-in-time snapshot from the last import. There is no historical inventory data — cannot determine how long an item has been out of stock. Always note this.

**Example** *(BCF — validated)*:
> Top-selling products with zero current availability:
> | Item | Category | Historical ERP Sales | Qty Sold | Qty Available |
> |------|----------|:---:|:---:|:---:|
> | 0510-005 | CAT1 | $400,303 | 675 | **0** |
> | 0728-011 | SOFAS | $381,107 | 401 | **0** |
> | 0635-002 | CAT1 | $339,478 | 472 | **0** |
>
> 8 of BCF's top 10 revenue-generating products show zero current availability. These items represent $2.55M in historical demand that cannot currently be fulfilled.

**Action**: Restock or reorder top-selling items with zero availability. Prioritize by historical sales velocity.

**Customer Value**: "Here are your best sellers you can't currently sell" — a headline-level QBR insight.

**SuperCat Value**: Demonstrates business intelligence, not just platform analytics. "The add-on pays for itself if restocking one product category captures incremental revenue."

**Segments**: Accounts with `sales_data` + `inventories` (81 orgs with ERP sales data, 182 orgs with inventory data — intersection ~81 orgs).

**Complexity**: Simple (cross-table join: `sales_data` × `inventories` on `base_item_code`)

**Data Dependency**: MCP `sales_data` + `inventories` + `products` (for category context)

**Data Readiness**: Live

**Bundle Required**: All (data-dependent)

**Query IDs**: Q-37

**Allowed Claims**: "These historically high-volume items currently show zero available inventory." | Top-sellers by historical ERP invoiced sales cross-referenced with current stock level.

**Forbidden Claims**: "Revenue at risk" as a precise figure without caveating that inventory is a point-in-time snapshot and historical sales may not reflect future demand | Claims about how long items have been out of stock (no historical inventory data)

**Portability**: Fully portable — `base_item_code` is standardized within each org.

---

### VM-38a: Product Velocity Trend (eCat Orders — Current Capability)

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: eCat transaction
**Internal Name**: product_velocity_ecat
**Customer-Facing Name**: Product Sales Velocity Report (eCat Orders)

**Gating**: `portal_order_items` + `portal_orders` present (52 orgs with portal order items).

**Signal**: Track product-level eCat order velocity over time using `portal_order_items` (line items) joined to `portal_orders` (with order dates). Identify items with rising or falling eCat demand.

**Example** *(illustrative)*:
> Item 0848-026 (BEDS collection): 588 units ordered via eCat historically. Month-over-month trend: +12% in last 3 months. Velocity accelerating — monitor inventory levels.

**Action**: Surface items with accelerating eCat velocity to flag for inventory replenishment before stockout. Surface items with declining eCat velocity to inform clearance or repositioning.

**Customer Value**: Product-level demand direction that complements ERP inventory reports.

**SuperCat Value**: When paired with VM-37 (stockout detection), creates a comprehensive product health view.

**Segments**: Accounts with `portal_order_items` (~52 orgs).

**Complexity**: Moderate (time-series aggregation per product from `portal_order_items` + `portal_orders`)

**Data Dependency**: MCP `portal_order_items` + `portal_orders`

**Data Readiness**: Live — Conditional on `portal_order_items` availability

**Bundle Required**: iPad+Catalog+Cart, Full (portal order tracking)

**Query IDs**: Q-38a

**Allowed Claims**: eCat product order velocity trend over time. | Accelerating vs. declining items by order count.

**Forbidden Claims**: Full-channel product velocity (eCat-only data via `portal_order_items`) | Claims about total inventory demand

**Portability**: Data-gated to orgs with `portal_order_items`.

---

### VM-38b: Product Velocity Trend (Full — Pending Engineering)

**Audience**: Dual [D] — Pending Engineering
**Commerce Lens**: ERP total-business
**Internal Name**: product_velocity_full
**Customer-Facing Name**: Product Sales Velocity Report (All Channels)

**Gating**: Requires `invoice_date` or `period` column on `sales_data` — not yet available. This is a one-column schema change to the ERP import pipeline.

**Signal**: Once `invoice_date` is added to `sales_data`, track product-level sales velocity across all ERP channels by month. Covers 81 orgs with `sales_data` vs. the 52 covered by VM-38a.

**Action**: When available, this VM provides full-channel product trending rather than eCat-only. Creates a complete demand signal.

**Customer Value**: Product demand direction across all channels — a genuinely new capability that most ERPs don't surface in this form.

**SuperCat Value**: Positions the Insights Layer as a business intelligence tool. Deepens Domain 5 from eCat-centric to full-business.

**Data Readiness**: Pending Engineering — requires `invoice_date` column addition to ERP import pipeline. High-priority engineering request.

**Enhancement Path**: Engineering adds `invoice_date` or `period` column to `sales_data`. One-column schema change to the ERP import pipeline. When available, VM-38b unlocks for all 81 orgs with `sales_data`.

---

### VM-39: Line Analysis by Category & Collection

**Audience**: Dual [D]
**Commerce Lens**: ERP total-business
**Internal Name**: line_analysis_category
**Customer-Facing Name**: Product Line Performance Report

**Gating**: `sales_data` + `products` with `category_code` populated.

**Signal**: Aggregate ERP sales by `products.category_code` and `products.collection_code` to show which product lines drive revenue, which are underperforming, and where catalog investment is concentrated vs. where revenue comes from.

**Example** *(BCF — validated)*:
> | Category | ERP Sales | Items | Sales/Item |
> |----------|:---:|:---:|:---:|
> | CAT1 | $5.79M | 150 | $38,600 |
> | SOFAS | $3.46M | 102 | $33,882 |
> | BEDS | $1.73M | 21 | **$82,534** (highest per-item) |
> | CAT23 | $264K | 806 | **$328** (lowest per-item) |
>
> BEDS: 21 items, $1.73M — highest per-item productivity. CAT23: 806 items, $264K — largest catalog investment with lowest per-item return.

**Action**: Review high-item / low-revenue categories for potential SKU rationalization. Invest in categories with high per-item productivity.

**Customer Value**: "Analyze the line by category" — a core product management need.

**SuperCat Value**: Positions the Insights Layer as a product strategy tool, not just a sales tool.

**Segments**: All accounts with `sales_data` + `products` with `category_code` populated (~81 orgs).

**Complexity**: Simple (aggregation join: `sales_data` × `products` on `base_item_code` grouped by `category_code` or `collection_code`)

**Data Dependency**: MCP `sales_data` + `products`

**Data Readiness**: Live

**Bundle Required**: All (data-dependent on `sales_data`)

**Query IDs**: Q-39

**Allowed Claims**: Sales by category with per-item productivity metrics. | Collection-level revenue comparison.

**Forbidden Claims**: Category-level conclusions for customers with opaque category codes (e.g., "CAT1") without acknowledging that the client must interpret their own codes

**Portability**: Query is fully portable. Interpretation varies by customer — category codes are client-configured. Descriptive names (e.g., "SOFAS", "BEDS") are self-explanatory; opaque codes (e.g., "CAT1") require client interpretation. A per-customer category name mapping (~10–30 rows) resolves this for self-serve delivery.

**Enhancement Path**: Attribute-level analysis (style, color, size) requires structured product metadata from `products.custom_fields` (JSONB, client-specific schemas) — Phase 4+ capability.

---

### VM-40: Regional Product Intelligence

**Audience**: Dual [D]
**Commerce Lens**: eCat transaction + ERP total-business (combined)
**Internal Name**: regional_product_intelligence
**Customer-Facing Name**: Geographic Sales Intelligence Report

**Gating**: `customers.billing_state` populated. Category × geography analysis additionally requires `sales_data`.

**Signal**: Cross-reference eCat orders or ERP sales data with buyer geographic location (`customers.billing_state`) to surface regional patterns. Optional: combine with Clicky Analytics geographic demand data (VM-33) to compare sales geography with portal traffic geography.

**Example** *(BCF — validated)*:
> Top states by eCat order GMV (trailing 12 months):
> | State | Buyers | eCat Orders | eCat GMV |
> |-------|:---:|:---:|---:|
> | NC | 37 | 382 | $874K |
> | NJ | 35 | 320 | $746K |
> | FL | 52 | 290 | $658K |
>
> Category × geography insight: BEDS sell disproportionately in Massachusetts ($703K) vs. NC ($213K). Is this a rep effect, a market effect, or a distribution effect? Each explanation implies a different action.
>
> Supply × demand gap (with Clicky): "Your portal attracts visitors from 20 states, but eCat orders come from 8 primary states — there's portal traffic from regions you're not actively converting."

**Action**: Overlay geographic data with rep territory assignments. Identify regions with high portal traffic (VM-33) but low eCat order volume.

**Customer Value**: Geographic demand intelligence that informs territory strategy and dealer expansion.

**SuperCat Value**: "There's demand in regions you don't actively serve" is a powerful expansion conversation.

**Segments**: All accounts with `customers.billing_state` populated (197 orgs, 81% of platform). Category × geography additionally requires `sales_data`.

**Complexity**: Moderate (orders × customers join grouped by `billing_state`; optional Clicky enrichment)

**Data Dependency**: MCP `orders` + `customers` (eCat lens). MCP `sales_data` + `customers` + `products` (ERP lens). BigQuery `clicky_analytics` (for `has_clicky = true` accounts as enrichment).

**Data Readiness**: Live

**Bundle Required**: All (data-dependent)

**Query IDs**: Q-40

**Allowed Claims**: Geographic distribution of eCat orders and buyers. | Category × state sales patterns. | Portal traffic vs. eCat order geography gap (when Clicky data available).

**Forbidden Claims**: Definitive attribution of regional patterns to a single cause without analysis | International geography claims based only on `billing_state`

**Portability**: Fully portable — `billing_state` is standardized. Map-based visualization is a Phase 3/4 product decision; current delivery is table-based.

---

### VM-42: New Item Performance

**Audience**: Dual [D]
**Commerce Lens**: ERP total-business
**Internal Name**: new_item_performance
**Customer-Facing Name**: New Introduction Performance Report

**Gating**: `products.new_item = true` (164 orgs, 67%) AND `sales_data` (81 orgs, 33%) — intersection.

**Signal**: Cross-reference the `new_item` flag on `products` with `sales_data` to show how newly introduced products are performing. Group by `collection_code` to surface collection-level performance.

**Example** *(BCF — validated 2026-03-24)*:
> BCF has 230 new introduction items.
> | Collection | New Items | ERP Sales | Qty Sold | Sales/Item | Assessment |
> |------------|:---:|:---:|:---:|:---:|---|
> | COL119 | 14 | $17,890 | 19 | $1,278 | Strong |
> | COL11 | 8 | $11,185 | 27 | **$1,398** | Strongest per-item |
> | CORA | 21 | $510 | 1 | $24 | Needs attention |
> | COL61 | 55 | $733 | 12 | $13 | 55 items, near-zero sell-through |
>
> Spread between best and worst collection: 107x ($1,398/item vs. $13/item). This variance is invisible without the cross-reference.

**Action**: Surface during QBR as "here is how your new introductions are performing." Lead with winners, then flag underperformers for merchandising review.

**Customer Value**: Product development feedback loop. Near-real-time sell-through visibility for new introductions.

**SuperCat Value**: Positions Insights Layer as a business intelligence tool for CEO/VP Sales persona, not just IT admin.

**Segments**: Accounts with both `new_item` flag and `sales_data` (~81 orgs intersection).

**Complexity**: Simple (JOIN `products` where `new_item = true` with `sales_data`, grouped by `collection_code`)

**Data Dependency**: MCP `products` (new_item flag) + `sales_data`

**Data Readiness**: Live

**Bundle Required**: All (data-dependent)

**Query IDs**: Q-42

**Allowed Claims**: New item sell-through by collection. | Per-item productivity for new introductions. | Collections with near-zero sell-through.

**Forbidden Claims**: Attribute poor sell-through to product quality alone (could be rep awareness, timing, or pricing) | "These products are failing" without noting alternative explanations

**Portability**: Fully portable — `new_item` flag and `collection_code` are standardized. Collection codes tend to be more readable than category codes (named collections like CORA, FLORA vs. opaque codes).

**Enhancement Path**: Full time-cohorted intro performance ("how are our January 2026 intros doing?") requires `introduced_date` field on `products` — a one-column ERP import pipeline addition. Companion enhancement to `invoice_date` on `sales_data` (VM-38b).

---

## Domain 6 — Cross-Instance Benchmarking

*The long-term moat. Only SuperCat can provide cross-customer comparison because only SuperCat sees data across all instances. Requires anonymization — no product-level best-seller data exposed.*

---

### VM-23: Peer Comparison Dashboard

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce (platform metrics)
**Internal Name**: peer_comparison
**Customer-Facing Name**: Industry Benchmark Report

**Gating**: BigQuery `insightful_product.segment_peer_comparison` view (live).

**Signal**: Rank the client on key platform metrics against peers in the same bundle segment. Anonymized — no client names exposed. Live via `insightful_product.segment_peer_comparison` + `segment_benchmarks_monthly`.

**Example** *(BCF — validated 2026-03-24)*:
> BCF vs. Full-bundle peers (33 orgs):
> | Metric | BCF | Segment Median | vs. Peer |
> |--------|----:|:---:|:---:|
> | eCat Orders | 1,773 | 2,986 | −40.6% |
> | Logins | 7,863 | 6,368 | +23.5% |
> | MRR | $2,280 | $1,685 | +35.3% |
>
> BCF is above median on logins and MRR but below median on orders — more engaged than peers but converting less of that engagement into eCat orders. The dormant eCat buyer base (23% lapsed) is the most likely constraint.

**Action**: Surface during QBR. Lead with strengths, then frame the order gap as opportunity: "your engagement is above median — the eCat buyer reactivation effort (VM-17) is the most direct path to closing the order gap."

**Customer Value**: Context. Raw numbers are meaningless without comparison.

**SuperCat Value**: Benchmarking is the single strongest Insights Layer differentiator. No competitor can provide segment-aware peer comparison.

**Segments**: All bundles — benchmark is bundle-specific.

**Complexity**: Simple — single query on `insightful_product.segment_peer_comparison`

**Data Dependency**: BigQuery `insightful_product.segment_peer_comparison` + `segment_benchmarks_monthly`

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-CI-02

**Allowed Claims**: Client metrics vs. anonymized peer segment medians and percentiles. | "You're above / below median for your plan type."

**Forbidden Claims**: Use internal segment labels ("Platform-Embedded," "Commerce-Active," "Catalog-Focused") in client-facing text | Name specific peer clients | Compare clients across different bundle types

**Portability**: Fully portable.

---

### VM-24: Feature Adoption Benchmarking

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: feature_adoption_benchmarking
**Customer-Facing Name**: Feature Utilization Benchmark

**Gating**: BigQuery `insightful_product.org_summary` + `segment_benchmarks_monthly`.

**Signal**: For each major feature, calculate adoption rate across same-bundle accounts. Show the client where they stand — are they using features that most peers on their plan use? Are they missing features that top-performing accounts adopt?

**Example** *(BCF — validated 2026-03-24)*:
> | Feature | BCF | Same-Bundle Adoption Rate | Status |
> |---------|:---:|:-:|---|
> | Digital Library | Active (17,418 views) | 100% | At norm |
> | PDF Catalogs | Active (870 created) | 100% | At norm |
> | Product Configurator (CPQ) | Active (7,306 items) | 36.4% | Above most peers |
> | Online Ordering | Active | 66.7% | Active |
> | Clicky Analytics | Not established | — | Opportunity |

**Action**: For BCF, expansion conversation is about depth (Clicky Analytics, Insights Layer) rather than breadth.

**Customer Value**: "You're in the top tier of feature adoption for your plan type" is a validation that strengthens the relationship. Surfaces the one or two gaps in context.

**SuperCat Value**: Feature benchmarking is a natural upsell vehicle. Segment-specific adoption rates make the pitch concrete.

**Segments**: All bundles — adoption rates are bundle-specific.

**Complexity**: Simple — `insightful_product.org_summary` + `segment_benchmarks_monthly`

**Data Dependency**: BigQuery `insightful_product.org_summary` + `segment_benchmarks_monthly`

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-CI-03

**Allowed Claims**: Feature adoption percentage vs. same-bundle peers. | "X% of accounts on your plan actively use [feature]."

**Forbidden Claims**: Internal segment labels in client-facing text | Compare eCat Online adoption with high certainty when Health V2 OD-5 is unresolved

**Portability**: Fully portable.

---

### VM-25: Growth Trajectory Comparison

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: growth_trajectory_comparison
**Customer-Facing Name**: Growth Trajectory Report

**Gating**: Minimum 2 monthly benchmark snapshots for trending (started March 2026).

**Signal**: Compare the client's eCat order velocity against their segment cohort's trajectory over time. Monthly benchmark snapshots (scheduled queries running 1st of each month) enable MoM and YoY trending.

**Example** *(BCF — live, March 2026 snapshot)*:
> BCF vs. Full-bundle peers:
> | Metric | BCF | p25 | Median | p75 | BCF Position |
> |--------|:---:|:---:|:------:|:---:|---|
> | eCat Orders | 1,773 | 1,205 | 2,986 | 6,109 | Between p25 and median |
> | Logins | 7,863 | 4,640 | 6,368 | 8,568 | Between median and p75 |
>
> Growth trajectory: Is BCF closing the gap to median or falling further behind? First meaningful time-series comparison available May 2026.

**Action**: Frame order gap as opportunity and track trajectory monthly. "Here's what would move you from p25–median to p50–p75."

**Customer Value**: Growth benchmarking answers "are we keeping up?" with real percentile context.

**SuperCat Value**: Growth trajectory creates urgency and anchors the value of continuous monitoring.

**Segments**: Commerce-active bundles.

**Complexity**: Simple for current snapshot. Time-series trending requires 2–3 months of `segment_benchmarks_monthly`.

**Data Dependency**: BigQuery `insightful_product.segment_peer_comparison` (live now) + `segment_benchmarks_monthly` (accumulating monthly from March 2026).

**Data Readiness**: Live (current snapshot); Time-series trending from May 2026.

**Bundle Required**: iPad+Catalog+Cart, Full

**Query IDs**: Q-CI-02, Q-CI-04

**Allowed Claims**: Current-period percentile position vs. peers. | Trajectory direction once 2+ snapshots available.

**Forbidden Claims**: Definitive trend claims before 2+ monthly snapshots are available

**Portability**: Fully portable.

---

### VM-26: Best Practice Identification

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: best_practices
**Customer-Facing Name**: What Top-Performing Accounts Do

**Gating**: BigQuery `insightful_product.top_performers_by_segment` and `org_master_with_segments`.

**Signal**: Identify behavioral patterns correlated with high performance across the platform. Surface as actionable best practices tailored to the client's bundle segment. Cross-instance data enables correlation analysis between feature adoption, engagement patterns, and outcomes.

**Example** *(BCF — validated 2026-03-24)*:
> Top Full-bundle performers by eCat orders: Gabriella White (38,049), Summer Classics (13,424), Gabby (13,049).
> Common patterns:
> 1. Feature depth 8/8: Top 3 performers all at maximum feature depth. BCF at 7/8 — gap is Clicky Analytics.
> 2. Portal analytics established: Top performers have Clicky Analytics. BCF does not.
> 3. eCat order volume > 5,000: All top performers exceed this. BCF at 1,773 has significant headroom.

**Action**: Focus on closing the specific feature depth gaps that top performers share, then work on eCat buyer reactivation.

**Customer Value**: Evidence-based recommendations anchored in what top performers actually do — "the top 3 accounts on your plan all do X."

**SuperCat Value**: Best practices position SuperCat as a strategic partner.

**Segments**: All bundles — best practices are bundle-specific.

**Complexity**: Moderate — requires analytical queries across `org_master_with_segments` and `top_performers_by_segment`.

**Data Dependency**: BigQuery `insightful_product.org_master_with_segments` + `top_performers_by_segment` + `segment_benchmarks_monthly`

**Data Readiness**: Live — data available. Correlation build ongoing.

**Bundle Required**: All

**Query IDs**: Q-CI-05, Q-CI-06

**Allowed Claims**: "Top performers on your plan type share these behavioral patterns." | Anonymized benchmarks only.

**Forbidden Claims**: Name specific top-performing clients | Use internal segment labels in client-facing text

**Portability**: Fully portable.

---

## Domain 7 — SuperCat Internal Intelligence

*Not customer-facing (except VM-30 which has an external-safe variant). Powers CS playbooks, expansion targeting, and churn prevention.*

---

### VM-27: Account Health Score (Health V2)

**Audience**: Internal [I]
**Commerce Lens**: Non-commerce
**Internal Name**: account_health_score
**Customer-Facing Name**: N/A — internal only

**Gating**: Health V2 scoring system. Entity must meet Health V2 inclusion criteria (§1 of Health V2 README).

**Signal**: Surfaces Health V2 outputs for the account. Health V2 is the only authoritative scoring methodology — do not maintain a parallel formula.

Health V2 output fields used:
- `health_score` (0–100, after risk modifier caps)
- `health_band` (Thriving / Healthy / Watch / At Risk / Critical)
- `classification` (Expand / Stabilize First / Maintain / Intervene)
- `churn_risk` (boolean), `churn_risk_severity` (immediate / near-term / monitored)
- `expansion_ready` (boolean), `expansion_type`
- `engagement_score`, `adoption_score`, `value_delivery_score`, `operational_health_score`, `trajectory_score` (component scores)
- `risk_modifier_applied` (modifier ID if fired — RM-1 through RM-4)
- `score_explanation` (1–2 sentence plain-English summary)

The `org_summary.health_score` (0–1.0 scale) from the BigQuery `insightful_product` cross-instance views is a legacy precursor. It may be referenced for historical continuity in trend views but is not a co-equal formula. Health V2 is authoritative for current scoring.

**Example** *(BCF — Health V2 output)*:
> BCF (Full bundle) — Health V2:
> - Health Score: [run Health V2 operator for current score]
> - Health Band: [derived from score]
> - Classification: [Expand / Stabilize First / Maintain / Intervene]
> - Component drivers: engagement and adoption scores above median; value delivery constrained by order gap vs. peers
> - Risk modifiers: none fired
> - Score explanation: "[from operator output]"

**Action**: CS prioritizes outreach based on health band and classification. "Intervene" accounts require immediate action plan. "Expand" accounts are ready for upsell conversation. "Stabilize First" accounts need health remediation before any commercial motion.

**SuperCat Value**: Replaces intuition-driven CS prioritization with data-driven account management. CS team knows which accounts need attention and why.

**Segments**: All accounts meeting Health V2 inclusion criteria.

**Complexity**: Simple — run Health V2 operator to get scores. No manual calculation.

**Data Dependency**: Health V2 operator output CSV (`client_health_scores_YYYY-MM-DD.csv`). Source data: Mixpanel, MCP `orders`/`login_events`/`org_users`/`import_events`/`products`, BigQuery `clicky_analytics`, HelpScout.

**Data Readiness**: Live — Health V2 operator is runnable now.

**Bundle Required**: All (Health V2 is bundle-aware — weights and inputs adjust per bundle)

**Query IDs**: Health V2 operator (`operator.py`), `QUERIES.md`. BigQuery `insightful_product.org_summary` for historical context.

**Allowed Claims**: Health V2 scores and bands as produced by the Health V2 operator. | Classification and CS action recommendation.

**Forbidden Claims**: Present the legacy `org_summary.health_score` (0–1.0) as the current authoritative health score | Recompute health outside Health V2 | Use Health V2 score language with clients (internal only)

**Portability**: Fully portable — Health V2 is bundle-aware and handles bundle-specific weight redistribution.

---

### VM-28: Expansion Readiness Signals

**Audience**: Internal [I]
**Commerce Lens**: Non-commerce
**Internal Name**: expansion_readiness
**Customer-Facing Name**: N/A — internal only

**Gating**: Health V2 Growth Score output + BigQuery `insightful_product.expansion_candidates`.

**Signal**: Identify accounts whose behavior indicates readiness for bundle upgrade or add-on purchase. Sources:
- Health V2 `growth_score`, `growth_band`, `expansion_ready`, `expansion_type`, `bundle_upgrade_signal`, `feature_gap_score`, `customer_headroom_score`
- BigQuery `insightful_product.expansion_candidates` view — segment upgrade opportunities and feature upsell flags
- VM-48 (HubSpot Expansion Signals) — open deals, lifecycle stage, CRM context

**Example** *(live 2026-03-24)*:
> Platform-wide expansion candidates (from `expansion_candidates` view):
> - Craftmade — current bundle: iPad+Catalog+Cart. Flagged for Full bundle upgrade. Missing Kit Builder and CPQ.
> - Geo Contemporary — iPad+Catalog. Flagged for adding Online Ordering. Has eCat Online traffic but no B2B Cart.
> - Designers Fountain, Godinger, Butler Specialty — iPad-only. All flagged for iPad+Catalog upgrade with Kit Builder + CPQ opportunities.

**Action**: CS/Sales uses this as a prioritized upsell hit list — sorted by ARR to focus on highest-value accounts first.

**SuperCat Value**: Data-driven upsell targeting replaces intuition. The `expansion_candidates` view is a live sales pipeline for platform expansion.

**Segments**: All accounts.

**Complexity**: Simple — single query on `insightful_product.expansion_candidates`. Health V2 `growth_score` provides the scored version.

**Data Dependency**: BigQuery `insightful_product.expansion_candidates` + Health V2 output CSV + VM-48 (HubSpot)

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-CI-07, Health V2 operator (Growth Score)

**Allowed Claims**: Bundle upgrade signals, feature gap signals, customer headroom signals from Health V2 Growth Score. | Named expansion candidates from `expansion_candidates` view.

**Forbidden Claims**: Share expansion signals directly with the client | Use "Platform-Embedded" / "Commerce-Active" labels in client-facing text

**Portability**: Fully portable.

---

### VM-29: Churn Risk (Composite Output)

**Audience**: Internal [I]
**Commerce Lens**: Non-commerce
**Internal Name**: churn_risk_composite
**Customer-Facing Name**: N/A — internal only

**Gating**: Health V2 risk modifiers + BigQuery `insightful_product.at_risk_accounts`.

**Signal**: Composite churn risk output synthesizing all input signal families:
- **Input: VM-06** — rep engagement trajectory (declining logins, declining eCat orders)
- **Input: VM-36** — portal traffic decline signal (demand-side disengagement via Clicky)
- **Input: Health V2 Risk Modifiers** (RM-1 through RM-4) — authoritative churn triggers
  - RM-1: ARR > $5K AND zero logins in 90 days → cap at 20
  - RM-2: Primary value metric down > 60% AND value delivery score < 20 → cap at 20
  - RM-3: 5+ L3+ support escalations in current period → cap at 30
  - RM-4: `days_since_critical_update` > 180 for 2+ entity types → cap at 30
- **BigQuery `at_risk_accounts` view** — multi-factor risk scoring across all orgs

**Example** *(live 2026-03-24)*:
> Highest-risk accounts (from `at_risk_accounts`):
> - Jonathan Charles: risk score 125, ARR $27.8K — zero logins, zero eCat orders, declining portal traffic. Paying but fully disengaged. RM-1 fires (ARR > $5K + zero logins).
> - Bliss Studio: risk score 125, ARR $6.8K — similar profile.
> - Tomlinson & Interlude Furniture: paying but disengaged. Warrant immediate CS outreach.

**Action**: CS proactively reaches out to at-risk accounts with a diagnostic conversation. "We noticed your data imports stopped — is there a technical issue we can help resolve?" — not a sales pitch.

**SuperCat Value**: Churn prevention is the highest-ROI internal use of the Insights Layer. Saving one $2K/month account that would otherwise churn is worth more than many new sales.

**Segments**: All accounts.

**Complexity**: Simple — single query on `insightful_product.at_risk_accounts`. Health V2 Risk Modifiers surface in operator output.

**Data Dependency**: BigQuery `insightful_product.at_risk_accounts` + `portal_health_alerts` + Health V2 operator output (risk modifier fields)

**Data Readiness**: Live — automated. `at_risk_accounts` view is always current.

**Bundle Required**: All

**Query IDs**: Q-CI-01 (at_risk_accounts), Q-CI-08 (portal_health_alerts), Health V2 operator

**Allowed Claims**: At-risk account identification with risk factors. | Health V2 risk modifier status.

**Forbidden Claims**: Share churn risk scores directly with clients | Treat a single signal (login decline alone) as definitive churn evidence without composite view

**Portability**: Fully portable.

---

### VM-30: Support Burden Analysis

**Audience**: Internal [I] — Optional external-safe framing noted
**Commerce Lens**: Non-commerce
**Internal Name**: support_burden
**Customer-Facing Name**: (Optional) Support Partnership Summary

**Gating**: HelpScout account matching for the org. ~80% exact match on org name; ~95% fuzzy match. HelpScout account matching is email-domain-based and inherently approximate (Health V2 OD-6).

**Signal**: Aggregate HelpScout conversation volume, response time, and topic distribution per account. Identify accounts generating disproportionate support load. Tag distribution: product area (eCat, Admin Console, eOL, Sales Portal), severity (S1–S4), type (bug, feature request, training), level (L1–L3).

**Example** *(BCF — validated)*:
> BCF Support Profile: 162 tickets (2nd highest on platform after internal "SuperCat Solutions")
> | Metric | BCF | Platform Avg |
> |--------|-----|-------------|
> | Total tickets | 162 | ~40 (est. median) |
> | Current quarter trend | 11 (declining) | — |
> | eOL product area | 18% | ~7% |
> | Bug type | 39% | ~28% |
> | S1/S2 severity | 48% | ~39% |
>
> Primary contact: mhorwitz@braxtonculler.com — also BCF's Catalog/Data Manager (VM-04). Single point of contact for both data management and support communication.

**Action**: CS uses support profile for account health context (feeds VM-29). Reduce support burden by deploying proactive monitoring for top ticket drivers.

**Optional external-safe framing**: A sanitized QBR version — "here's what your team contacts us about most, how we categorize and resolve it, and how this quarter compares to prior quarters" — is valid and builds trust. This does not expose internal severity classifications or support comparisons across clients.

**SuperCat Value**: Reduces support cost per account. Identifies where product investment would have the highest support burden reduction.

**Segments**: All accounts with HelpScout history.

**Complexity**: Moderate (HelpScout account matching + tag parsing via JSON_QUERY_ARRAY)

**Data Dependency**: HelpScout BigQuery (`helpscout.conversations`, `helpscout.conversation_threads`, `helpscout.customers`). Account matching via org name or email domain.

**Data Readiness**: Live — Q-HS-01 through Q-HS-06 in query library.

**Bundle Required**: All

**Query IDs**: Q-HS-01 through Q-HS-06

**Allowed Claims**: Internal: per-account ticket volume, tag distribution, trend. External-safe: "here's how your support interactions break down by category" (omit internal severity classifications and cross-account comparisons).

**Forbidden Claims**: Share cross-account support comparisons with clients | Share internal S1/S2 severity classifications externally without reframing | Claim exact account matching when fuzzy matching may have introduced errors

**Portability**: Moderate — HelpScout account matching is ~80% exact. Known discrepancies documented in `07_cross_instance_infrastructure.md`.

---

### VM-48: HubSpot Expansion Signals

**Audience**: Internal [I]
**Commerce Lens**: Non-commerce
**Internal Name**: hubspot_expansion_signals
**Customer-Facing Name**: N/A — internal only

**Gating**: HubSpot BigQuery sync active. `hubspot_company_id` mapping present in `org_feature_usage_report`.

**Signal**: Pull HubSpot deal stage, lifecycle stage, open opportunity count, and last sales activity per account. Combine with platform expansion signals from VM-28 to create a complete expansion readiness picture: platform says "ready to expand" + CRM has an active deal in stage 3 = high-priority CS/Sales action.

**Example** *(illustrative)*:
> Account: Craftmade
> - Health V2 classification: Expand
> - Platform expansion signal: Bundle upgrade from iPad+Catalog+Cart to Full
> - HubSpot status: Active deal, Stage 3 ("Contract Sent"), open since 45 days
> - Last CRM activity: CS call 12 days ago
>
> CS action: Follow up on contract — platform signals and CRM activity both point to conversion readiness.

**Action**: CS/Sales prioritizes accounts where both platform signals (VM-28) and CRM signals (VM-48) align. This is the highest-confidence expansion target list.

**SuperCat Value**: Combines platform behavioral intelligence with CRM context for the most efficient expansion targeting.

**Segments**: All accounts with HubSpot records.

**Complexity**: Simple — BigQuery query on HubSpot tables + join to `org_master_with_segments`

**Data Dependency**: BigQuery HubSpot tables. Mapping via `hubspot_company_id` in `org_feature_usage_report`.

**Data Readiness**: Live

**Bundle Required**: All

**Query IDs**: Q-48 (to be added to query library)

**Allowed Claims**: HubSpot deal stage and lifecycle as internal CS context. | Combined platform + CRM expansion signal priority list.

**Forbidden Claims**: Share HubSpot deal data with clients | Use CRM data in client-facing reports

**Portability**: Fully portable for accounts with HubSpot records and `hubspot_company_id` mapping.

---

## Domain 8 — Portal & Demand-Side Intelligence

*Powered by Clicky Analytics data in BigQuery — 48 client portals, 22 table types per client. This is the demand-side complement to Mixpanel's supply-side rep behavior. All VMs in this domain are gated to `has_clicky = true`.*

*Do not mention Clicky Analytics in client-facing reports when `has_clicky = false`. For clients without Clicky, Clicky setup is a SuperCat-side action item (noted in internal brief, not surfaced to client).*

*VM-36 appears in this domain because it reads Clicky data, but it feeds Domain 7 (VM-29 Churn Risk). It is an input signal family, not a standalone output.*

---

### VM-31: Portal Traffic Health

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: portal_traffic_health
**Customer-Facing Name**: Online Catalog Traffic Report

**Gating**: `has_clicky = true`

**Signal**: Daily portal metrics — unique visitors, pageviews, bounce rate, average session duration — aggregated monthly. Surface trend direction and benchmark against cross-portal median.

**Example** *(Gabby — validated)*:
> | Month | Avg Daily Visitors | Avg Daily Pageviews | Bounce Rate | Avg Session |
> |-------|:---:|:---:|:---:|:---:|
> | Mar 2026 | 366 | 2,486 | 14.5% | 7.8 min |
> | Feb 2026 | 395 | 2,682 | 13.7% | 8.4 min |
> | Dec 2025 | 275 | 1,795 | 17.0% | 8.0 min |
>
> 374 avg daily visitors — above cross-portal median of ~170. 14% bounce rate, 8-minute sessions = engaged, active users. December seasonal dip mirrors eCat order seasonality.

**Action**: CS surfaces traffic health during QBR. For accounts with declining traffic, flag as a leading demand-side warning signal.

**Customer Value**: Visibility into how many buyers are browsing the online catalog — a question manufacturers always ask but rarely have data for.

**SuperCat Value**: Portal traffic is a retention signal. High traffic = buyers depend on the platform. Declining traffic = leading churn indicator (see VM-36).

**Segments**: Accounts with Clicky Analytics enabled (48 portals).

**Complexity**: Simple (single query on `daily_metrics` table)

**Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_daily_metrics`

**Data Readiness**: Live — gate: `has_clicky = true`

**Bundle Required**: Any bundle with `eCat Online` + Clicky Analytics

**Query IDs**: Q-CL-01

**Allowed Claims**: Daily visitor count, pageviews, bounce rate, session duration trend. | Cross-portal benchmark comparison.

**Forbidden Claims**: Traffic figures for clients without `has_clicky = true` | Attribute traffic to specific dealers without visitor identity confirmation

**Portability**: Data-gated — 48 portals covered. BCF not among the 48 — BCF Clicky setup is a pending action.

---

### VM-32: Portal Content Performance

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: Non-commerce
**Internal Name**: portal_content_performance
**Customer-Facing Name**: Online Catalog Content Report

**Gating**: `has_clicky = true` AND page-level data available for the portal. Data availability varies — validate date range and coverage before running.

**Signal**: Page-level view data from the portal — which product pages, categories, or content sections get the most views. Entrance and exit page patterns reveal the visitor journey. Cross-reference top-viewed pages with eCat order data to identify high-view / low-order conversion gaps.

**Example** *(illustrative)*:
> Top-viewed category: SOFAS (45% of pageviews). Orders in that category: 22% of eCat GMV. The category attracts disproportionate browsing traffic — potential conversion opportunity (pricing issue? availability issue? product detail quality?).

**Action**: Cross-reference top-viewed pages with eCat orders. High-view / low-order products represent conversion opportunities.

**Customer Value**: Content performance data that can only be obtained by combining portal browsing patterns with eCat ordering data — a capability unique to SuperCat.

**Segments**: Clicky-enabled accounts with commerce activity.

**Complexity**: Moderate (Clicky `pages` data + MCP eCat orders join on product/category matching)

**Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_pages` + MCP `orders`

**Data Readiness**: Conditional Live — data availability varies by portal. Validate before running.

**Bundle Required**: Any bundle with eCat Online + Clicky Analytics

**Query IDs**: Q-CL-02

**Allowed Claims**: Top-viewed pages and categories. | Browse-to-eCat-order conversion comparison where data permits.

**Forbidden Claims**: Conclusions about conversion without sufficient page + order data for the specific portal

**Portability**: Data-gated. Page data availability varies by portal and date range.

---

### VM-33: Geographic Demand Map

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: geographic_demand_map
**Customer-Facing Name**: Online Catalog Geographic Demand Report

**Gating**: `has_clicky = true`

**Signal**: Geographic distribution of portal visitors by state/region, with visit volume. Cross-reference with rep territory coverage to identify demand-supply gaps.

**Example** *(Gabby — validated)*:
> Top visitor states (6 months): Georgia (8,568), Texas (8,448), Alabama (7,655), Florida (5,316).
>
> Geographic demand gap: "Your portal attracts visitors from 20 states. If your rep team covers 12 states, there are 8+ states with active portal interest but no direct coverage — organic demand not yet converted."

**Action**: Overlay portal geographic data with rep territory assignments. Identify regions with high portal traffic but low eCat order coverage.

**Customer Value**: Geographic demand intelligence — "where are buyers engaging with your catalog, and where are you not yet selling?"

**SuperCat Value**: "There's demand in regions you don't actively serve" is a powerful expansion conversation justifying territory expansion and rep additions.

**Segments**: Clicky-enabled accounts with national distribution.

**Complexity**: Simple (single query on Clicky `regions` table)

**Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_regions` + optionally MCP (rep territory mapping)

**Data Readiness**: Live — gate: `has_clicky = true`

**Bundle Required**: Any bundle with eCat Online + Clicky Analytics

**Query IDs**: Q-CL-03

**Allowed Claims**: State-level portal visitor volume. | Regions with traffic but no known rep coverage.

**Forbidden Claims**: Geographic visitor data for clients without `has_clicky = true`

**Portability**: Data-gated. International clients may use `billing_country` rather than `billing_state`.

---

### VM-34: Visitor Organization Identification

**Audience**: Dual [D] — Conditional [C]
**Commerce Lens**: Non-commerce
**Internal Name**: visitor_org_identification
**Customer-Facing Name**: Portal Visitor Companies Report

**Gating**: `has_clicky = true`. Value depends heavily on visitor network characteristics — B2B environments with corporate networks yield better organization identification than residential ISPs.

**Signal**: Reverse DNS identification of organizations visiting the portal from Clicky `organizations` table. Most visitors resolve to ISPs (Comcast, Spectrum, AT&T) rather than named businesses. "Business" ISP variants and named corporate networks are the actionable subset.

**Example** *(Gabby — validated)*:
> Top visitor organizations (6 months): iCloud Private Relay (15,221), Comcast Cable (11,996), Spectrum (7,761), Spectrum Business (2,804), Cox Business (2,431).
>
> Reality check: Most visitors resolve to residential ISPs. The "Business" variants suggest commercial visitors. True company-level identification is limited to visitors on corporate networks with identifiable DNS.
>
> Where this shines: Accounts whose dealers use corporate networks will see named companies — furniture retail chains, design firms, contract furnishers — which is immediately actionable for sales teams.

**Action**: Filter for "Business" ISP variants and named organizations. Flag organizations appearing that aren't in the client's current dealer list as potential leads.

**Customer Value**: Lead generation signal — limited by ISP obfuscation but valuable when corporate networks are identifiable.

**SuperCat Value**: Unique capability — no competitor provides visitor identification on the manufacturer's catalog portal.

**Segments**: Clicky-enabled accounts. Value is context-dependent — B2B portal environments with dealer networks on corporate networks yield the best results.

**Complexity**: Simple (single query on Clicky `organizations` table)

**Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_organizations`

**Data Readiness**: Conditional Live — gate: `has_clicky = true`. Accuracy varies by portal.

**Bundle Required**: Any bundle with eCat Online + Clicky Analytics

**Query IDs**: Q-CL-04

**Allowed Claims**: Named organization visits where corporate network identification is confirmed. | "Business" ISP visitor counts as a proxy for commercial visitor volume.

**Forbidden Claims**: Claim specific company visitor identity based on ISP alone | Present ISP counts as company counts

**Portability**: Data-gated. Accuracy depends on visitor network type — not uniformly reliable across all portals.

---

### VM-35: Traffic Source Intelligence

**Audience**: Dual [D]
**Commerce Lens**: Non-commerce
**Internal Name**: traffic_source_intelligence
**Customer-Facing Name**: Online Catalog Traffic Source Report

**Gating**: `has_clicky = true`

**Signal**: Portal traffic source distribution — Direct, Links/Referrals, Search, Social, Email, Advertising. Distribution reveals dealer awareness, SEO effectiveness, and marketing channel performance.

**Example** *(Gabby — validated)*:
> | Source | Visits | Share |
> |--------|-------:|:----:|
> | Direct | 44,996 | 59.7% |
> | Links (Referrals) | 28,112 | 37.3% |
> | Search (Organic) | 1,779 | 2.4% |
>
> 60% direct = strong brand recall — dealers know the portal URL. 37% referral = active linking from brand website. 2.4% organic search = limited SEO visibility. Cross-portal benchmarking: accounts with <30% direct traffic may have weak dealer awareness of the portal's existence.

**Action**: For accounts with low direct traffic, improve portal awareness via dealer communications. For accounts with high search traffic, ensure content is optimized.

**Customer Value**: Marketing channel intelligence for their digital catalog presence.

**SuperCat Value**: Portal awareness conversations. Low direct traffic triggers a dealer communication campaign recommendation.

**Segments**: Clicky-enabled accounts.

**Complexity**: Simple (single query on Clicky `traffic_sources` table)

**Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_traffic_sources`

**Data Readiness**: Live — gate: `has_clicky = true`

**Bundle Required**: Any bundle with eCat Online + Clicky Analytics

**Query IDs**: Q-CL-05

**Allowed Claims**: Traffic source distribution and trend. | Direct traffic percentage as dealer awareness proxy.

**Forbidden Claims**: Traffic source data for clients without `has_clicky = true`

**Portability**: Data-gated.

---

### VM-36: Portal Traffic Decline Signal *(Churn Input → VM-29)*

**Audience**: Internal [I] — input signal family feeding VM-29
**Commerce Lens**: Non-commerce
**Internal Name**: portal_traffic_decline_signal
**Customer-Facing Name**: N/A — internal churn signal

**Gating**: `has_clicky = true`

**Signal**: Month-over-month trend in portal daily visitor count. Two or more consecutive months of >15% traffic decline is a leading demand-side churn indicator. This signal fires into `at_risk_accounts` and VM-29.

Demand-side disengagement (dealer/buyer interest fading) typically precedes supply-side disengagement (reps stop logging in, orders decline) by 30–60 days. This makes VM-36 one of the earliest available churn signals.

**Example** *(Clicky data — validated 2026-03-24)*:
> Alert: Sixtrees & Renwil — portal health CRITICAL. Traffic crashed >30%. Under 5 visitors/day.
>
> This signal fires RM-level urgency in VM-29 for these accounts.
>
> Counter-example (Gabby): Dec 2025 dip (−19%) followed by Jan 2026 recovery (+31%) = seasonal, not a churn signal.

**Relationship to VM-29**: VM-36 fires signals. VM-29 synthesizes all signals (VM-06 + VM-36 + Health V2 risk modifiers) into the composite output.

**SuperCat Value**: The earliest churn indicator in the stack. Combined with VM-06 (rep engagement trajectory) and Health V2 risk modifiers, creates a three-tier early warning system.

**Complexity**: Simple (monthly aggregation + MoM calculation from `daily_metrics`)

**Data Dependency**: BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_daily_metrics`. Signal output feeds `at_risk_accounts` + VM-29.

**Data Readiness**: Live — gate: `has_clicky = true`. Portals without Clicky do not contribute to this signal.

**Bundle Required**: Any bundle with eCat Online + Clicky Analytics

**Query IDs**: Q-CL-01 (source data), Q-CI-08 (portal_health_alerts)

**Allowed Claims**: MoM portal traffic trend as an input signal to churn risk scoring. | CRITICAL/WARNING portal health flags.

**Forbidden Claims**: Present as a standalone churn prediction without VM-29 composite context | Share portal traffic decline signals directly with clients

**Portability**: Data-gated to Clicky-enabled portals.

---

## Prioritization Matrix

### Tier 1 — Implement Now

All data available. No infrastructure blockers.

| VM | Name | Primary Data Source | Why Now |
|----|------|---------------------|---------|
| VM-01 | Rep Behavioral Scorecard | BigQuery Mixpanel + MCP orders | Anchor capability. Strongest differentiator. |
| VM-03 | Behavioral Funnel Gap Analysis | Derived from VM-01 | Per-rep coaching with quantified upside. |
| VM-07 | Catalog Completeness Score | MCP products | Single query, universally applicable, aligned with Health V2. |
| VM-08 | Data Freshness Monitor | MCP data_versions | Single query, universally applicable. |
| VM-12 | eCat Customer Activation & ERP Penetration | MCP orders + customers | Corrected denominator, high-impact insight. |
| VM-16 | ERP Total Business Visibility | MCP portal_orders | Foundational ERP context — corrects the v1 framing error. |
| VM-18 | eCat Order Velocity & Trend | MCP orders + portal_orders | Part A + Part B dual-lens structure. |
| VM-19 | eCat Channel Mix Evolution | MCP orders | Gated to Cart accounts. Clear channel attribution. |
| VM-22 | Feature Usage Depth | BigQuery Mixpanel | Org-level feature adoption. |
| VM-23 | Peer Comparison Dashboard | BigQuery insightful_product | Single query. BCF: below median on orders, above on logins/MRR. |
| VM-27 | Account Health Score (Health V2) | Health V2 operator | Now authoritative — replace legacy formula. |
| VM-29 | Churn Risk (Composite) | BigQuery insightful_product + Health V2 | `at_risk_accounts` live. Jonathan Charles, Bliss Studio surfaced. |
| VM-37 | Inventory × Sales Intelligence | MCP sales_data + inventories | Headline QBR insight for clients with ERP sales data. |
| VM-40 | Regional Product Intelligence | MCP orders + customers | Geographic demand, fully portable via `billing_state`. |
| VM-41 | First-Time eCat Orderers | MCP orders | Corrected terminology. eOL channel attribution via `order_source`. |
| VM-43 | Territory Coverage & Dormancy | MCP customers + orders + org_users | Live now. Fills rep-coverage gap. |
| VM-45 | eCat Capture Rate vs. Total Business | MCP orders + portal_orders | Most important new commerce VM. Gated to portal_orders clients. |
| VM-46 | eCat Selling Workflow Maturity | BigQuery Mixpanel + MCP orders | Live now. Critical for enablement-heavy accounts. |
| VM-47 | Smart Stack Effectiveness | MCP smart_stacks + Mixpanel + orders | Live now. Quantifies curation ROI. |

### Tier 2 — Implement Next

Moderate complexity or data dependency, high value.

| VM | Name | Data Source | Why Next |
|----|------|-------------|----------|
| VM-02 | Selling Archetype Classification | Derived from VM-01 | Requires VM-01 first. |
| VM-04 | Non-Selling User Role Classification | BigQuery Mixpanel + MCP | Behavioral fingerprint classification. |
| VM-05 | Seat Utilization | MCP org_users + login_events + orders | Simple, universal. |
| VM-06 | Rep Engagement Trajectory | MCP login_events + orders | Leading churn input to VM-29. |
| VM-09 | Import Health | MCP import_events | Top support ticket driver reduction. |
| VM-10 | Feature Enablement Gap | MCP mobile_sites + cross-instance | Bundle-aware gap analysis. |
| VM-11 | Configuration Completeness | MCP data_versions | "Enabled but abandoned" detection. |
| VM-13 | Customer Concentration Risk (eCat) | MCP orders | Simple aggregation, risk awareness. |
| VM-14 | Customer Reorder Frequency (eCat) | MCP orders | Per-customer time-series. |
| VM-15 | Enrollment Funnel | MCP enrollment_applicants + orders | Gate: enrollment enabled. Feeds VM-44. |
| VM-17 | Dormant eCat Customer Identification | MCP orders + customers | Prioritized reactivation list. |
| VM-20 | eCat AOV Analysis | MCP orders | Multi-dimension AOV. |
| VM-21 | eCat Order Type & Workflow | MCP orders | Quote workflow adoption signal. |
| VM-24 | Feature Adoption Benchmarking | BigQuery insightful_product | Detailed peer adoption comparison. |
| VM-25 | Growth Trajectory Comparison | BigQuery insightful_product | Time-series accumulating. |
| VM-26 | Best Practice Identification | BigQuery insightful_product | Cross-instance correlation. |
| VM-28 | Expansion Readiness | BigQuery insightful_product + Health V2 + VM-48 | `expansion_candidates` live. |
| VM-30 | Support Burden Analysis | HelpScout BigQuery | Q-HS-01 through Q-HS-06 live. |
| VM-31 | Portal Traffic Health (Clicky) | BigQuery clicky_analytics | Single query, cross-portal benchmark live. |
| VM-33 | Geographic Demand Map (Clicky) | BigQuery clicky_analytics | "Demand where you don't have reps." |
| VM-35 | Traffic Source Intelligence (Clicky) | BigQuery clicky_analytics | Dealer awareness signal. |
| VM-38a | Product Velocity Trend (eCat Orders) | MCP portal_order_items + portal_orders | Live for 52 orgs. |
| VM-39 | Line Analysis by Category | MCP sales_data + products | Category naming caveat noted. |
| VM-42 | New Item Performance | MCP products + sales_data | New intro sell-through. BCF: 107x spread. |
| VM-44 | Onboarding Velocity | MCP enrollment_applicants + orders | Live now. Acceptance-to-order conversion. |
| VM-48 | HubSpot Expansion Signals | BigQuery HubSpot | CRM context for VM-28. |
| VM-50 | Library Document Engagement | BigQuery Mixpanel + MCP shared_resources | Conditional: Mixpanel coverage required. |

### Tier 2.5 — Pending Engineering Enhancement

| VM | Name | What's Needed |
|----|------|--------------|
| VM-38b | Product Velocity Trend (Full) | `invoice_date` column on `sales_data` — one-column ERP import pipeline change |

### Conditional — Run When Data Confirmed

| VM | Name | Condition |
|----|------|-----------|
| VM-32 | Portal Content Performance | Clicky page data availability varies by portal |
| VM-34 | Visitor Organization Identification | Corporate network DNS resolution varies |
| VM-36 | Portal Traffic Decline Signal | `has_clicky = true` |
| VM-49 | Buyer-Level Repeat Purchase | `portal_orders` buyer attribution confirmed |

### Deferred

| Item | Reason |
|------|--------|
| Standalone Stripe Billing Health VM | Stripe in BigQuery but data not mature for standalone promotion |
| Cross-Customer Product Trend Intelligence | Category code normalization unsolved platform-wide. Phase 4+. |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total active VMs | **51** |
| Customer-facing (External-safe or Dual) | 43 |
| SuperCat-internal only | 5 (VM-27, VM-28, VM-29, VM-36, VM-48) |
| Conditional (gated by data or feature flag) | 11 |
| Pending Engineering (VM-38b) | 1 |
| Deferred | 2 |
| Domains | 8 |
| Tier 1 (implement now) | 19 |
| Tier 2 (implement next) | 26 |
| Tier 2.5 (pending engineering) | 1 |
| Data sources: MCP only | 18 |
| Data sources: BigQuery Mixpanel | 7 |
| Data sources: BigQuery HelpScout | 1 |
| Data sources: BigQuery Clicky Analytics | 6 (VM-31 through VM-36) |
| Data sources: BigQuery insightful_product | 5 (VM-23, VM-24, VM-25, VM-26, VM-28) |
| Data sources: Health V2 operator | 2 (VM-27, VM-29) |
| Data sources: Composite / multi-source | 7 |
| **Fully portable** | 35 |
| **Query portable / interpretation varies** | 3 (VM-39, VM-34, VM-30) |
| **Data-gated (conditional coverage)** | 13 |

---

## Appendix: Forbidden Claims Register

| Forbidden Claim | Why | Allowed Alternative |
|-----------------|-----|---------------------|
| "net-new customers" | Cannot confirm ERP lifecycle | "first-time eCat orderers" |
| "`portal_orders`" as buyer self-service | `portal_orders` = ERP-synced data, not buyer activity | "orders synced from your ERP" / "total business" |
| "buyer self-service" for anything other than B2B Cart | Sales Portal is internal BI | Only for `order_source = 'server'` with `has_cart = true` confirmed |
| "self-service portal" for Sales Portal | Sales Portal = internal BI | "Sales Intelligence Dashboard" / "Sales Portal" |
| "revenue at risk" for OOS items without caveating | Inventory is point-in-time | "historically high-volume items currently showing zero availability" |
| "Platform-Embedded" / "Commerce-Active" / "Catalog-Focused" in client-facing text | Internal segment labels | Use bundle names or describe what the client has |
| "full-stack deployment" | Invented label | Describe actual products ("eCat iPad, Online Ordering, and Sales Intelligence Dashboard") |
| eOL orders / channel mix for iPad-only clients | No eCat Online ordering channel exists | No eOL column; no channel mix section |
| CPQ/Kit Builder as "adoption gap" when client doesn't have the product | That's an "expansion opportunity" | "Enabling [Product Name] would allow..." |
| Health score from any formula other than Health V2 in VM-27 | Legacy formula conflicts with Health V2 | Health V2 outputs only |
| "Low eCat submit volume = low platform value" | Ignores enablement-without-submit-through pattern | Frame via VM-46 workflow maturity lens |
| Clicky Analytics mention when `has_clicky = false` | Clicky setup is a SuperCat-side action for these clients | Omit from client-facing report entirely |
