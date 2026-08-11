# Insightful Product — Overview

**What this is**: A fully scoped recommendations and insights strategy for SuperCat — 40 value moments across 8 domains, grounded in live customer data, with a validated query library, audience-specialized report templates, and a phased delivery plan. The work positions an "Insights Layer" as a net-new, sellable product capability that drives MRR and ACV.

**Where we are**: Strategy, data validation, template design, and cross-instance infrastructure are complete. We've validated every insight against real customer data (Braxton Culler as primary, Gabriella White and Gabby as secondary, cross-instance views for all orgs). **All 40 value moments are queryable today** — including cross-instance benchmarking, automated health scoring, at-risk detection, and expansion targeting. No structural blockers remain.

---

## Quick Numbers

| | |
|---|---|
| Value moments defined | **42** across 8 domains |
| Queryable today | **42 (100%)** |
| SQL queries validated | **45+** (MCP + Mixpanel + HelpScout + Clicky + Product/Inventory + Cross-Instance) |
| Customer orgs portability-tested | **13** |
| Portability: fully portable | **39 of 42** |
| Data sources integrated | MCP (production DB), Mixpanel, HelpScout, Clicky Analytics, **BigQuery cross-instance (`insightful_product`)** |
| BigQuery cross-instance views | **12 live views**, 3 tables, 2 scheduled monthly queries |
| Report templates | 2 (customer-facing + internal CS brief), both populated with live data |

---

## What's in This Folder

| File | What it is | Who should read it |
|------|-----------|-------------------|
| `SKILL.md` | Technical context — data sources, schemas, pipeline status, gaps | Engineering, data |
| `01_bcf_instance_profile.md` | Complete profile of Braxton Culler — the "what it looks like when it's real" reference | Everyone — start here for the visceral version |
| `02_strategy_and_game_plan.md` | Full strategy, phasing, commercial model thinking, current status, next steps | Leadership, product, CS leads |
| `03_rep_performance_intelligence.md` | Deep dive on the anchor capability — rep behavioral scorecards, archetypes, coaching opportunities | CS, product |
| `04_value_moment_catalog.md` | The full menu — all 40 VMs with examples, prioritization, portability analysis, enhancement backlog | Product, CS, engineering |
| `05_query_library.md` | Parameterized SQL — copy, replace org ID, run | CS (for report generation), engineering (for productization) |
| `06a_external_report_template.md` | Customer-facing QBR / monthly digest — the sellable artifact | CS, sales, leadership |
| `06b_internal_report_template.md` | Internal account intelligence brief — health scores, churn risk, expansion readiness, QBR prep | CS, sales |
| `07_cross_instance_infrastructure.md` | Cross-instance infrastructure plan (design document) | Engineering, data |
| `08_bigquery_cross_instance_infrastructure.md` | **LIVE implementation** — 12 views, 3 tables, 2 scheduled queries in BigQuery | Engineering, data, CS |
| `09_operator_prompts.md` | Operator index — explains the system and links to the 5 operator files | **Everyone** — start here if you want to use the system |
| `operators/` | **5 standalone operator files** — `@` reference any one in a Cursor chat to run it | **Everyone** — this is how you use the system |

**Suggested reading path**: `09` (understand the operators) → `01` (see it real) → `06a` (see the customer deliverable) → `04` (see the full menu) → `02` (understand the strategy). Everything else is reference material.

**If you just want to use the system**: Open a Cursor chat, type `@skills/insightful_product/operators/01_generate_customer_reports.md`, then type the customer name. Done. No copy-pasting, no SQL.

---

## The 8 Domains

1. **Rep Performance Intelligence** — behavioral scorecards, archetypes, coaching opportunities (the anchor)
2. **Instance Health & Configuration** — catalog completeness, data freshness, import health
3. **Customer & Buyer Intelligence** — activation rates, dormancy, concentration risk, enrollment, at-risk high-value customers, **new customer acquisition by channel & rep** *(new — Founder feedback)*
4. **Ordering & Commerce Analytics** — order velocity, channel mix, AOV, order types
5. **Product & Inventory Intelligence** — stockout detection, category analysis, regional sales, product velocity, **new item performance by collection** *(new — Founder feedback)*
6. **Cross-Instance Benchmarking** — peer comparison, feature adoption benchmarks, best practice identification *(NOW LIVE in BigQuery — 12 views, always current)*
7. **SuperCat-Internal Intelligence** — health scores, churn risk, expansion readiness, support burden *(health scores and at-risk detection now automated via BigQuery views)*
8. **Portal & Demand-Side Intelligence** — portal traffic, geographic demand, traffic sources, visitor identification *(powered by Clicky Analytics)*

---

## What's Delegatable Now

### CS can start immediately — use the operators
- **Generate reports for any customer** — open a Cursor chat, type `@skills/insightful_product/operators/01_generate_customer_reports.md`, then type the customer name. Produces both the customer-facing report and internal CS brief automatically. No SQL knowledge needed.
- **Prep for any meeting in 2 minutes** — `@skills/insightful_product/operators/02_account_quick_look.md` + customer name. Returns health score, peer standing, risk signals, expansion flags, and top talking points.
- **Weekly portfolio review** — `@skills/insightful_product/operators/03_portfolio_risk_and_expansion.md`. Surfaces at-risk paying accounts and expansion candidates across the full portfolio. Run every Monday.
- **Pilot the external report** with 2-3 accounts for QBR delivery. BCF is the obvious first. Recommend selecting one account with Clicky Analytics (e.g., Gabby, Jamie Young, Charleston Forge) to showcase the portal intelligence section with real data.

### Engineering — three remaining requests
1. **Establish Clicky Analytics for Braxton Culler** — BCF's health score is 0.75; the 25-point gap is entirely the missing Clicky portal. Establishing it raises the score to 0.95+ and makes BCF the complete reference account.
2. **Add `invoice_date` column to `sales_data` table** — a one-column schema change. Unlocks time-series product trending (VM-38) for 81 orgs.
3. **Add `introduced_date` column to `products` table** — a one-column schema change. Unlocks time-cohorted intro performance (VM-42 full version — "how are our January 2026 intros doing?") for 164 orgs.

### Engineering — completed (2026-03-24)
- Cross-instance infrastructure built and LIVE in BigQuery. 12 views, 3 tables, 2 scheduled queries. See `08_bigquery_cross_instance_infrastructure.md`.

### Product — decisions needed
- **Commercial model**: Add-on module? Tier differentiator? The external report template defines the customer-facing content boundary; the internal template defines the operational boundary. The gap between them is the pricing boundary.
- **Delivery surface**: Where do insights live in the product? Sales Portal extension, Admin Console alerts, standalone module, or all three?

---

## Key Findings Worth Knowing

- **"Best sellers out of stock"** is the strongest single customer-facing insight. For BCF: 9 of the top 10 revenue products have zero inventory, representing $500K+ in unfulfillable demand.
- **New customer acquisition tracking** reveals channel dynamics invisible otherwise. BCF adds ~11 new ordering customers/month — 68% rep-acquired, 32% eOL self-serve. Sharyn Moss is the top acquirer (20 new accounts) despite not being the top GMV producer.
- **New intro performance varies 107x** between BCF's best and worst collections. COL11 generates $1,398/item; COL61 generates $13/item from 55 items. This is the kind of product development feedback loop manufacturers lack.
- **Rep behavioral intelligence** is the anchor capability and the strongest differentiator. No competitor has per-rep behavioral scorecards cross-referenced with a validated selling correlation model.
- **Portability is strong**: 37 of 40 VMs run identically across customers. The one exception (category analysis) is a display-name issue, not a data issue — manageable with a lightweight per-customer mapping.
- **Portal + rep data = unique story**: The supply → demand → outcome chain (rep activity [Mixpanel] → portal engagement [Clicky] → orders [MCP]) is data-complete for 48 accounts. Only SuperCat can tell this story.
- **Cross-instance benchmarking is live and automated**: 12 BigQuery views provide always-current peer comparison, health scores, at-risk detection, and expansion targeting. Segment distribution: 86 Catalog-Focused, 15 Commerce-Active, 31 Platform-Embedded. Monthly snapshots enable trending starting May 2026.
- **Immediate operational value already surfaced**: Jonathan Charles and Bliss Studio are highest-risk paying accounts (risk score 125). Craftmade is a clear expansion candidate. BCF is "Below Average" on orders vs. peers — a surprising and actionable QBR finding.
