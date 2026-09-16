# External VM Index

> **Status**: Frozen — all 51 VMs classified.
> **Derived from**: `reference/value_moment_catalog.md` (semantic authority)
> **Purpose**: Compact, machine-usable runtime lookup table for the external report operator.
> **This file is a derivative.** It does not override the catalog. If any row conflicts with the catalog, the catalog wins.

---

## Runtime Status Definitions

| Status | Meaning |
|--------|---------|
| `active` | External-safe, live queries exist, no engineering dependency, not internal-only. Operator should run. |
| `conditional` | External-safe but gated by data flag or feature availability. Run only when gate condition is met. |
| `pending_query` | External-safe and data schema confirmed, but query not yet written or validated in audited library. |
| `pending_engineering` | Requires engineering work not yet done. Do not attempt to run. |
| `internal_only` | Must never appear in the Phase 1 external report. Not in operator read path. |
| `non_runtime` | Exists in catalog as strategy/reference. Operator does not call this VM. |

---

## Hard Rules (Non-Negotiable)

- **VM-27** (Account Health Score) = `internal_only` — never in Phase 1 external report
- **VM-29** (Churn Risk) = `internal_only` — never in Phase 1 external report
- **VM-28** (Expansion Readiness) = `internal_only`
- **VM-36** (Portal Traffic Decline Signal) = `internal_only` — churn input, not a client-facing output
- **VM-48** (HubSpot Expansion Signals) = `internal_only`
- **VM-38b** = `pending_engineering` — do not run until `invoice_date` added to `sales_data`
- **VM-45** = gated to `portal_orders` presence AND strict denominator validity check — do not degrade to denominator-less half-VM. Formal gate (validated across 3 live runs): **skip if `ecat_gmv >= portal_orders_gmv`** (partial ERP sync — eCat is larger than the denominator) OR **skip if `ecat_gmv < 0.05 × portal_orders_gmv`** (eCat too small to interpret as capture rate vs. noise). Only render when `portal_orders_gmv > ecat_gmv` AND `ecat_gmv >= 0.05 × portal_orders_gmv`.
- **All Domain 8 VMs (VM-31 through VM-36)** = gated to `has_clicky = true` — binary gate
- **Segment labels** = **never allowed externally, including the Peer Benchmarking section**. Internal segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) must not appear in any section of the delivered report. In §7 Peer Benchmarking, `peer_group_id_effective` is the internal source value used to build plain-language cohort framing (e.g., "Lighting manufacturers on the same platform bundle" — derived from "Lighting / iPad+Catalog+Portal") — the raw label string must not appear literally in client-facing prose.
- **Health score** = never surfaces in external report in any form

---

## VM Table

### Domain 1 — Rep Performance Intelligence

| Field | VM-01 | VM-02 | VM-03 | VM-04 | VM-05 | VM-06 | VM-43 | VM-46 |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **name** | Rep Behavioral Scorecard | Selling Archetype Classification | Behavioral Funnel Gap Analysis | Non-Selling User Role Classification | Seat Utilization Analysis | Rep Engagement Trajectory | Territory Coverage & Dormancy | eCat Selling Workflow Maturity |
| **section** | Sales Team Performance | Sales Team Performance | Sales Team Performance | Sales Team Performance | Sales Team Performance | Sales Team Performance | Sales Team Performance | Sales Team Performance |
| **data_required** | Mixpanel `user_feature_usage_report` + MCP `orders` | Derived from VM-01 (Mixpanel + `orders`) | Derived from VM-01 + VM-03 | Mixpanel + MCP `org_users` | MCP `org_users`, `login_events`, `orders` | MCP `login_events`, `orders` | MCP `customers`, `orders`, `org_users` | Mixpanel + MCP `orders` |
| **gate** | Active iPad app users; Mixpanel data present | VM-01 required; 3+ active selling reps | VM-01 required | 10+ active users; Mixpanel data present | None | Active ordering reps (180d) | 3+ territories; rep assignments in `org_users` or `orders` | Active Mixpanel behavioral data |
| **priority** | P1 | P1 | P1 | P2 | P2 | P2 | P2 | P2 |
| **allowed_claims** | Per-rep eCat GMV, order count, AOV, customer count. Behavioral dimension scores. Coaching opportunities. | Archetype descriptions and behavioral profiles. Archetype-specific coaching. | Per-rep funnel gap with behavioral data. Quantified upside estimate using peer AOV. [HYPOTHETICAL] tag required. | Non-selling role identification with behavioral evidence. Seat value assessment. | Active vs. inactive user breakdown. Security hygiene recommendation. | Rolling login and eCat order trend per rep. Decline percentage over 90-day windows. | Accounts assigned but never ordered via eCat. Territory activation rate. Dormant accounts by rep assignment. | Submit-through rate with four-band classification. Presentation-depth as primary value metric for non-submit-through accounts. |
| **forbidden_claims** | "Net-new customers." Total-business GMV attributed to rep behavior. Claims about non-eCat order outcomes. | "Net-new customers." Implied archetype superiority without data support. | Guaranteed revenue improvement claims. | "X% of your licenses are wasted." | "X% of your licenses are wasted." | "Rep is about to leave." Total-business order decline attributed to rep. | "These accounts don't buy from you" (they may order via non-eCat channels). "Net-new customers." | "Low eCat submit volume = low platform value." "Your team isn't using eCat" when behavioral signals are high. |
| **query_ids** | Q-01, Q-18 Part A | Derived from Q-01 | Derived from Q-01, Q-18 Part A | Q-04 | Q-05 | Q-06 | Q-43 | Q-46 (pending_query — to be added) |
| **runtime_status** | `active` | `active` | `active` | `active` | `active` | `active` | `conditional` | `pending_query` |

---

### Domain 2 — Instance Health & Data Quality

| Field | VM-07 | VM-08 | VM-09 | VM-10 | VM-11 | VM-47 | VM-50 |
|-------|-------|-------|-------|-------|-------|-------|-------|
| **name** | Catalog Completeness Score | Data Freshness Monitor | Import Health & Sync Reliability | Feature Enablement Gap Analysis | Configuration Completeness | Smart Stack Effectiveness | Library / Document Engagement Effectiveness |
| **section** | Platform & Feature Utilization | Platform & Feature Utilization | Platform & Feature Utilization | Platform & Feature Utilization | Platform & Feature Utilization | Platform & Feature Utilization | Platform & Feature Utilization |
| **data_required** | MCP `products` | MCP `data_versions` | MCP `import_events` | MCP `mobile_sites`, `organizations`, `kit_items`, `contract_prices`, `enrollment_applicants`, `smart_stacks`, `shared_resources` + BigQuery `segment_benchmarks_monthly` | MCP `data_versions`, `sales_data`, `kit_items`, `contract_prices` | MCP `smart_stacks`, `orders` + BigQuery Mixpanel | MCP `shared_resources` + BigQuery Mixpanel `view_document`, `email_document` |
| **gate** | None — all accounts with a product catalog | None | Automated imports must exist; N/A for Admin Console-only accounts | None | None | `smart_stacks` count > 0 AND Mixpanel stack events available | Mixpanel `view_document` / `email_document` events confirmed for org |
| **priority** | P1 | P1 | P2 | P2 | P2 | P2 | P2 |
| **allowed_claims** | Visible product completeness %. Missing image/price counts for visible products only. Platform median comparison. | Entity-level freshness with age and 3-label status (Fresh / Monitor / Stale). Kit items × options gap alert. | Monthly import count trend. Presence/absence of error arrays. | "This feature is available in your plan but not yet active." Per-feature adoption rates across same-bundle accounts. | Feature is enabled but data is stale or unpopulated. Specific recommendation to re-import or disable. | Stack view counts. Post-view eCat order rate. Stale stack identification. | Document view and email share counts where Mixpanel coverage confirmed. Stale document identification. Top-performing content by engagement. |
| **forbidden_claims** | Flag missing images on hidden products as actionable. Include hidden products in completeness % without disclosure. | Attribute business impact to freshness without supporting evidence. Use labels other than Fresh/Monitor/Stale. | Specific error root causes without parsing the `data` YAML field. | List eCat Online features as "gaps" for iPad-only clients. List CPQ as adoption gap for non-CPQ clients. "Platform-Embedded." "Commerce-Active." | Assert client has abandoned a feature without confirming. | Attribute revenue exclusively to a stack view. Stack performance for stacks with fewer than 5 views. | Attribute sales outcomes to document views. Claims about document performance for orgs with incomplete Mixpanel coverage. |
| **query_ids** | Q-07 | Q-08 | Q-09 | Q-10 | Q-11 | Q-47 (pending_query — to be added) | Q-50 (pending_query — to be added) |
| **runtime_status** | `active` | `active` | `active` | `active` | `active` | `pending_query` | `conditional` |

**VM-50 note**: `conditional` because Mixpanel document event coverage varies by org. Validate coverage before running.
**VM-08 note**: Use exactly three freshness labels — Fresh (≤30 days), Monitor (31–180 days), Stale (>180 days). Never use "Acceptable," "Warning," or "Critical" as labels.

---

### Domain 3 — Customer & Buyer Intelligence

| Field | VM-12 | VM-13 | VM-14 | VM-15 | VM-16 | VM-17 | VM-41 | VM-44 | VM-49 |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **name** | eCat Customer Activation & ERP Penetration | Customer Concentration Risk (eCat) | Customer Reorder Frequency & Velocity (eCat) | Enrollment Funnel Analysis | ERP Total Business Visibility | Dormant eCat Customer Identification | First-Time eCat Orderers by Channel & Rep | Onboarding Velocity / Time-to-First-eCat-Order | Buyer-Level Repeat Purchase |
| **section** | Customer & Buyer Intelligence | Customer & Buyer Intelligence | Customer & Buyer Intelligence | Customer & Buyer Intelligence | Commerce Analytics | Customer & Buyer Intelligence | Customer & Buyer Intelligence | Customer & Buyer Intelligence | Customer & Buyer Intelligence |
| **data_required** | MCP `orders`, `customers` | MCP `orders` | MCP `orders` | MCP `enrollment_applicants`, `orders` *(non_runtime)* | MCP `portal_orders` | MCP `orders`, `customers` | MCP `orders` | MCP `enrollment_applicants`, `orders`, `customers` *(non_runtime)* | MCP `portal_orders` (buyer attribution required) |
| **gate** | Active eCat orders | Active eCat orders (12 months) | Active eCat buyers with 3+ orders (12 months) | `enrollment_applicants` count > 0 | `portal_orders` present | Active eCat order history | Active eCat order history (12+ months) | Enrollment enabled + `enrollment_applicants` accepted records | `portal_orders` with buyer attribution confirmed |
| **priority** | P1 | P2 | P2 | P2 | P1 | P2 | P1 | P2 | P2 |
| **allowed_claims** | eCat retention rate (active_12mo / total_ever_ordered_via_ecat). Lapsed eCat buyer count. ERP penetration as secondary context. | eCat GMV concentration percentages. Top buyer and top-5 buyer share of eCat GMV. | eCat reorder frequency and trend per buyer. Lapsing risk flag based on frequency decline. | Acceptance rate and funnel stage breakdown. First-eCat-order conversion rate when joined to `orders`. | Total ERP order volume across all channels. Order-origin breakdown (where `order_origin` field populated). Seasonality patterns from full business data. | Lapsed eCat buyer count by dormancy window. At-risk high-value eCat buyer list with last order date. | First-time eCat orderer count by channel (iPad vs. eCat Online) and rep. | Acceptance-to-first-eCat-order conversion rates at 30/60/90-day windows. Median time-to-first-order. % of accepted applicants with no eCat order. | Buyer repeat purchase rate where buyer attribution confirmed in `portal_orders`. Cohort return rates at 90/180-day windows. |
| **forbidden_claims** | "81% of your dealers are dormant" using ERP total as denominator. "Net-new customers." Treating all ERP accounts as intended eCat users. | Total-business concentration (eCat-only). Implied conclusions about business risk without broader ERP context. | Total-business reorder frequency (eCat-only). Conclusions about overall buyer health without ERP context. | "Accepted applicants = new customers." "Net-new customers." | "`portal_orders` = buyer self-service orders." "Portal ordering adoption." "Buyer self-service" when referring to `portal_orders`. "Buyers are ordering on the portal." | "Dormant" applied to buyers who have never ordered via eCat. "Net-new customers." | "Net-new customers." "eCat Online-acquired buyers are net-new accounts." | Acceptance = eCat buyer. "Net-new customers." | Apply this VM to orgs without confirmed buyer attribution. Claim buyer-level data when only aggregate `portal_orders` available. |
| **query_ids** | Q-12 | Q-13 | Q-14 | Q-15 | Q-16 | Q-17 | Q-41 | Q-44 (pending_query — to be added) | Q-49 (pending_query — to be added) |
| **runtime_status** | `active` | `active` | `active` | `non_runtime` | `conditional` | `active` | `active` | `non_runtime` | `conditional` |

**VM-16 note**: `portal_orders` = ERP-synced all-channel business. This is internal BI data in the client's Sales Portal. This VM surfaces total business visibility — it is never framed as buyer activity or self-service adoption. Q-16 interpretation from the old query library was wrong and must not be carried forward.

**VM-15, VM-44 note**: Both are `non_runtime` for the external report system. Enrollment data is intentionally out of scope for external reporting — the enrolled population is too often a weakly governed top-of-funnel list with structural inconsistencies (open-registration vs. dealer-controlled models, variable ERP match rates) that make client-facing claims unreliable. These VMs remain in the catalog for future internal or specialized use but do not appear in any external runtime path.

---

### Domain 4 — eCat Commerce Analytics

| Field | VM-18 | VM-19 | VM-20 | VM-21 | VM-22 | VM-45 |
|-------|-------|-------|-------|-------|-------|-------|
| **name** | eCat Order Velocity & Trend (with ERP Context) | eCat Channel Mix Evolution | eCat AOV Analysis | eCat Order Type & Workflow Analysis | Feature Usage Depth (Behavioral) | eCat Capture Rate vs. Total Business |
| **section** | Commerce Analytics | Commerce Analytics | Commerce Analytics | Commerce Analytics | Platform & Feature Utilization | Commerce Analytics |
| **data_required** | MCP `orders` (Part A) + MCP `portal_orders` (Part B, conditional) | MCP `orders` | MCP `orders` | MCP `orders` | BigQuery Mixpanel `org_feature_usage_report` | MCP `orders` + MCP `portal_orders` |
| **gate** | Active eCat orders (Part A always; Part B gated to `portal_orders` presence) | `has_cart = true` AND `order_source = 'server'` orders confirmed in data | 10+ orders per dimension | Active eCat orders | Mixpanel behavioral data available | `portal_orders` present AND `orders` present — if absent, VM is N/A |
| **priority** | P1 | P2 | P2 | P2 | P2 | P1 |
| **allowed_claims** | eCat order volume and GMV trend. eCat share of total ERP business (Part B, when available). Seasonal pattern from eCat data and full business data. | iPad vs. eCat Online order split and trend within `orders`. "Your buyers are increasingly placing orders directly." | eCat AOV by rep, buyer, channel, order type. Quote vs. non-Quote AOV comparison within eCat. | eCat order type distribution. Quote vs. Confirmed AOV comparison within eCat. | Feature event counts and intensity levels. Comparison to same-bundle peer accounts. | eCat order count and GMV share of total ERP business. eCat capture posture classification. "eCat processes X% of your total order volume." |
| **forbidden_claims** | ERP total volume = eCat volume. Attribute non-eCat channels to eCat performance. | Show eCat Online as a channel for iPad-only clients. "100% iPad / 0% eOL" as channel mix when only one channel. Reference `portal_orders` as a channel. | Total-business AOV (eCat-only data). "Your average deal size is $X" without clarifying eCat-only. | Total-business workflow analysis (eCat-only). | "Platform-Embedded." "Commerce-Active." "Catalog-Focused." Claims about eCat Online adoption strength when Health V2 OD-5 is unresolved. | Run VM-45 without a `portal_orders` denominator. Attribute non-eCat orders to eCat. Frame low capture rate as failure. |
| **query_ids** | Q-18 | Q-19 | Q-20 | Q-21 | Q-22 | Q-45 (pending_query — to be added) |
| **runtime_status** | `active` | `conditional` | `active` | `active` | `active` | `conditional` |

**VM-19 note**: Only include for accounts where `has_cart = true` AND server-source orders are confirmed to exist. For iPad-only clients, state "All orders were placed through the eCat iPad App" — no channel mix section.

**VM-45 note**: Formal denominator validity gate (required, validated across 3 live runs — sccon, ali, fc):
1. Skip if `portal_orders` is absent.
2. Skip if `ecat_gmv >= portal_orders_gmv` — eCat exceeds the ERP sync; denominator is a partial subset, not total business.
3. Skip if `ecat_gmv < 0.05 × portal_orders_gmv` — eCat too small relative to ERP; rate is not interpretable as activation progress.
4. Render only when: `portal_orders_gmv > ecat_gmv` AND `ecat_gmv >= 0.05 × portal_orders_gmv`.

---

### Domain 5 — Product & Inventory Intelligence

| Field | VM-37 | VM-38a | VM-38b | VM-39 | VM-40 | VM-42 |
|-------|-------|--------|--------|-------|-------|-------|
| **name** | Inventory × Sales Intelligence | Product Velocity Trend (eCat Orders) | Product Velocity Trend (Full — Pending Engineering) | Line Analysis by Category & Collection | Regional Product Intelligence | New Item Performance |
| **section** | Product & Inventory Intelligence | Product & Inventory Intelligence | — (deferred) | Product & Inventory Intelligence | Customer & Buyer Intelligence | Product & Inventory Intelligence |
| **data_required** | MCP `sales_data` + `inventories` + `products` | MCP `portal_order_items` + `portal_orders` | Requires `invoice_date` on `sales_data` (not yet available) | MCP `sales_data` + `products` | MCP `orders` + `customers` + optionally `sales_data`, `products`, BigQuery Clicky | MCP `products` (`new_item = true`) + `sales_data` |
| **gate** | Both `sales_data` and `inventories` present | `portal_order_items` present (~52 orgs) | `invoice_date` column on `sales_data` — pending engineering | `sales_data` + `products` with `category_code` populated | `customers.billing_state` populated | `products.new_item = true` AND `sales_data` present |
| **priority** | P1 | P2 | — | P2 | P2 | P2 |
| **allowed_claims** | "These historically high-volume items currently show zero available inventory." Top-sellers by historical ERP invoiced sales cross-referenced with current stock level. | eCat product order velocity trend over time. Accelerating vs. declining items by order count. | — | Sales by category with per-item productivity metrics. Collection-level revenue comparison. | Geographic distribution of eCat orders and buyers. Category × state sales patterns. Portal traffic vs. eCat order geography gap (when Clicky data available). | New item sell-through by collection. Per-item productivity for new introductions. Collections with near-zero sell-through. |
| **forbidden_claims** | "Revenue at risk" as precise figure without caveating inventory is point-in-time snapshot. Claims about how long items have been out of stock. | Full-channel product velocity (eCat-only data). Claims about total inventory demand. | Do not attempt to run. | Category-level conclusions for opaque category codes without acknowledging client must interpret. | Definitive attribution of regional patterns to a single cause. International geography claims based only on `billing_state`. | Attribute poor sell-through to product quality alone. "These products are failing" without noting alternatives. |
| **query_ids** | Q-37 | Q-38a | — | Q-39 | Q-40 | Q-42 |
| **runtime_status** | `conditional` | `conditional` | `pending_engineering` | `conditional` | `active` | `conditional` |

**VM-38a note**: This VM is live for ~52 orgs with `portal_order_items`. It is NOT fully gated pending engineering — only VM-38b is pending engineering. VM-38a should run when `portal_order_items` is confirmed present.

**VM-37 note**: Always include the inventory snapshot caveat: "Based on today's inventory import. Inventory data reflects current state only — we cannot determine how long items have been out of stock."

---

### Domain 6 — Cross-Instance Benchmarking

| Field | VM-23 | VM-24 | VM-25 | VM-26 |
|-------|-------|-------|-------|-------|
| **name** | Peer Comparison Dashboard | Feature Adoption Benchmarking | Growth Trajectory Comparison | Best Practice Identification |
| **section** | Peer Benchmarking | Peer Benchmarking | Peer Benchmarking | Peer Benchmarking |
| **data_required** | BigQuery `insightful_product.segment_peer_comparison` + `segment_benchmarks_monthly` | BigQuery `insightful_product.org_summary` + `segment_benchmarks_monthly` | BigQuery `insightful_product.segment_peer_comparison` + `segment_benchmarks_monthly` | BigQuery `insightful_product.org_master_with_segments` + `top_performers_by_segment` + `segment_benchmarks_monthly` |
| **gate** | Peer benchmark data available | `segment_benchmarks_monthly` available | Minimum 2 monthly benchmark snapshots (started March 2026; time-series available May 2026+) | `insightful_product.top_performers_by_segment` available |
| **priority** | P1 | P2 | P2 | P2 |
| **allowed_claims** | Client metrics vs. anonymized peer segment medians and percentiles. "You're above/below median for your plan type." | Feature adoption % vs. same-bundle peers. "X% of accounts on your plan actively use [feature]." | Current-period percentile position vs. peers. Trajectory direction once 2+ snapshots available. | "Top performers on your plan type share these behavioral patterns." Anonymized benchmarks only. |
| **forbidden_claims** | Internal segment labels ("Platform-Embedded," "Commerce-Active," "Catalog-Focused") in client-facing text. Name specific peer clients. Compare across different bundle types. | Internal segment labels in client-facing text. Strong eCat Online adoption claims when Health V2 OD-5 is unresolved. | Definitive trend claims before 2+ monthly snapshots available. | Name specific top-performing clients. Internal segment labels in client-facing text. |
| **query_ids** | Q-CI-02 | Q-CI-03 | Q-CI-02, Q-CI-04 | Q-CI-05, Q-CI-06 |
| **runtime_status** | `active` | `active` | `conditional` | `active` |

**Segment label rule for all Domain 6 VMs**: The cohort label used in the Peer Benchmarking section is derived from `peer_group_id_effective` in the Peer Benchmark output (e.g., "Furniture / Full"). Internal segment labels like "Platform-Embedded" must never appear in external report prose. The Peer Benchmarking section is the only place where any cohort context label appears externally.

**VM-24 placement note**: VM-24 (Feature Adoption Benchmarking) surfaces in the **Peer Benchmarking section**, not Platform & Feature Utilization. It answers "how does your feature adoption compare to peers?" — a benchmark question. VM-22 (Feature Usage Depth) in Domain 4 answers "how intensively does this account use features?" — an absolute usage question. Both may appear in an external report but are distinct subsections in distinct sections.

**VM-25 note**: Current-period snapshot is live. Time-series trending requires 2+ monthly snapshots — first meaningful time-series comparison available May 2026.

---

### Domain 7 — SuperCat Internal Intelligence (all internal_only)

| Field | VM-27 | VM-28 | VM-29 | VM-30 | VM-48 |
|-------|-------|-------|-------|-------|-------|
| **name** | Account Health Score (Health V2) | Expansion Readiness Signals | Churn Risk (Composite Output) | Support Burden Analysis | HubSpot Expansion Signals |
| **section** | — (internal only) | — (internal only) | — (internal only) | — (internal only, optional external-safe framing deferred) | — (internal only) |
| **runtime_status** | `internal_only` | `internal_only` | `internal_only` | `internal_only` | `internal_only` |
| **note** | Health V2 is the authoritative scoring system. Health score never surfaces in Phase 1 external report in any form. | Feeds CS/Sales upsell targeting. Not for client delivery. | Composite churn risk output. VM-06 and VM-36 are inputs. | Optional external-safe framing deferred to Phase 2. | HubSpot CRM context for VM-28. Internal only. |

---

### Domain 8 — Portal & Demand-Side Intelligence

**All Domain 8 VMs are gated to `has_clicky = true`. If `has_clicky = false`, these VMs do not exist in the report — no placeholder, no mention.**

| Field | VM-31 | VM-32 | VM-33 | VM-34 | VM-35 | VM-36 |
|-------|-------|-------|-------|-------|-------|-------|
| **name** | Portal Traffic Health | Portal Content Performance | Geographic Demand Map | Visitor Organization Identification | Traffic Source Intelligence | Portal Traffic Decline Signal |
| **section** | Portal Engagement | Portal Engagement | Portal Engagement | Portal Engagement | Portal Engagement | — (internal churn input) |
| **data_required** | BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_daily_metrics` | BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_pages` + MCP `orders` | BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_regions` | BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_organizations` | BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_traffic_sources` | BigQuery `clicky_analytics.{{CLICKY_PREFIX}}_daily_metrics` |
| **gate** | `has_clicky = true` | `has_clicky = true` AND page-level Clicky data available | `has_clicky = true` | `has_clicky = true` | `has_clicky = true` | `has_clicky = true` (internal signal only) |
| **priority** | P2 | P2 | P2 | P2 | P2 | — |
| **allowed_claims** | Daily visitor count, pageviews, session duration trend. Cross-portal benchmark. Note: bounce rate data is excluded — scale calibration is unresolved and this metric must not appear in external output. | Top-viewed pages and categories. Browse-to-eCat-order conversion comparison where data permits. | State-level portal visitor volume. Regions with traffic but no known rep coverage. | Named organization visits where corporate network identification confirmed. "Business" ISP visitor counts as commercial visitor proxy. | Traffic source distribution and trend. Direct traffic % as dealer awareness proxy. | (Internal) MoM portal traffic trend as churn risk input. CRITICAL/WARNING portal health flags. |
| **forbidden_claims** | Traffic figures for clients without `has_clicky = true`. Attribute traffic to specific dealers without confirmation. | Conclusions about conversion without sufficient page + order data. | Geographic visitor data for clients without `has_clicky = true`. | Claim specific company visitor identity based on ISP alone. Present ISP counts as company counts. | Traffic source data for clients without `has_clicky = true`. | Present as standalone churn prediction. Share portal traffic decline directly with clients. |
| **query_ids** | Q-CL-01 | Q-CL-02 | Q-CL-03 | Q-CL-04 | Q-CL-05 | Q-CL-01 (internal) |
| **runtime_status** | `conditional` | `conditional` | `conditional` | `conditional` | `conditional` | `internal_only` |

**VM-31 note**: `bounce_rate` is excluded from VM-31 external output. The Clicky bounce_rate metric's scale calibration is unresolved — it is not comparable across accounts and must not appear in client-facing reports. Do not surface bounce_rate in the Portal Engagement section or Appendix.

**VM-36 note**: VM-36 is an input signal family feeding VM-29 (Churn Risk). It is not a standalone client-facing output. It appears in Domain 8 because it reads Clicky data. It is internal-only.

---

## VM Count by Runtime Status

> **Version note**: Counts updated after Run 2B query audit. VMs that were `pending_query` in Run 1 are now reclassified as `conditional` (gate-dependent but query exists) or remain `pending_query` where query coverage is still partial.

| Status | Count | VMs |
|--------|-------|-----|
| `active` | 21 | VM-01, VM-02, VM-03, VM-04, VM-05, VM-06, VM-07, VM-08, VM-09, VM-10, VM-11, VM-12, VM-13, VM-17, VM-18, VM-20, VM-21, VM-22, VM-23, VM-26, VM-40, VM-41 |
| `conditional` | 14 | VM-16, VM-19, VM-24, VM-25, VM-31, VM-32, VM-33, VM-34, VM-35, VM-37, VM-38a, VM-39, VM-42, VM-43, VM-45, VM-49, VM-50 |
| `pending_query` | 3 | VM-46 (workflow maturity — Mixpanel denominator), VM-47 (smart stack per-stack Mixpanel), VM-49 (buyer attribution confirmation) |
| `pending_engineering` | 1 | VM-38b (requires `invoice_date` on `sales_data`) |
| `internal_only` | 6 | VM-27, VM-28, VM-29, VM-30, VM-36, VM-48 |
| `non_runtime` | 2 | VM-15, VM-44 — enrollment/onboarding intentionally excluded from external reporting (see note above) |

**Status notes**:
- `VM-43` (Territory Coverage): query written in Run 2B; status is `conditional` (gated to territory data present)
- `VM-44` (Onboarding Velocity): `non_runtime` — enrollment excluded from external report system; queries remain in library for internal/future use
- `VM-45` (eCat Capture Rate): query written; status is `conditional` (requires `portal_orders` AND denominator validity gate — see VM-45 note above; validated across 3 live runs)
- `VM-46` (Workflow Maturity): Postgres side written; Mixpanel denominator still `pending_query`
- `VM-47` (Smart Stack): aggregate Postgres metadata live; per-stack Mixpanel interaction still `pending_query`
- `VM-50` (Library Engagement): Postgres metadata live; Mixpanel per-doc attribution conditional — `conditional`
