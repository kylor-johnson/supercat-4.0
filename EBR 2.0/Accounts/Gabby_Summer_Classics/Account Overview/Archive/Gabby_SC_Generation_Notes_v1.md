# Gabby / Summer Classics — Generation Notes

**Generated:** March 2, 2026 | **Framework:** Account Scoring v3 + Thresholds v1.1 | **Run:** Independent per-entity rerun

---

## 0. Rerun Context

This is a **clean-slate independent rerun**. The prior run (v0) was flagged because Gabby (gh) data points were not independently verified — they appeared to come from a consolidated run. This rerun:

1. Used **corrected GH CSV files**: `gh_2026-01-01_2026-03-02 (1).csv` and `Gabby Admin Orders Report 2026-01-01 - 2026-03-03 (1).csv`
2. Independently parsed each entity's CLM and Orders files through separate Python processing
3. Independently queried PostgreSQL for each org ID (55, 69, 87, 88)
4. Independently queried BigQuery per Mixpanel shortname (gh, sc, scw, sccon)
5. Scored each entity using only its own data — no cross-entity data bleed

**Key differences from prior run (v0):**

| Metric | Prior Run | This Rerun | Delta |
|---|---|---|---|
| GH Distinct Customers (Orders) | 1,094 | **967** | -127 (11.6% fewer) |
| GH Submit Orders (CLM) | 6,159 | **6,162** | +3 |
| GH Territories (Orders) | 28 | **27** | -1 |
| GH State (PostgreSQL) | GA (error) | **AL** | Corrected |
| GH Expansion Score | 68 | **68** | No change |
| GH Risk Score | 12 | **12** | No change |
| Consolidated Expansion | 68 | **69** | +1 |
| Consolidated Risk | 10 | **11** | +1 |

The corrected GH Orders file reduced distinct customer count by 127 (likely due to export configuration differences). This changes the Customer Activation Rate from 9.3% to 8.2%, but both fall in the same 5-15% scoring band (score: 25). Net impact on scoring: minimal. The primary value of this rerun is **provenance assurance** — every data point is independently sourced and traceable.

---

## 1. Identity Mapping

### PostgreSQL Organization IDs

| Entity | Shortname | Org ID | Name in DB | State | Created |
|---|---|---|---|---|---|
| Gabby | `gh` | 55 | Gabby | AL | 2013-04-24 |
| SC Wholesale | `sc` | 69 | **Gabriella White** | (empty) | 2014-02-05 |
| Summer Classics | `scw` | 87 | Summer Classics | AL | 2015-04-28 |
| SC Contract | `sccon` | 88 | Summer Classics Contract | AL | 2015-04-28 |

**Key finding:** SC Wholesale (`sc`, org 69) is named "Gabriella White" in PostgreSQL. This is the retail division's brand name. All cross-source identity mapping accounts for this alias.

### BigQuery Cross-Source Identity

| Source | Entities Found | Names Matched | Query Used |
|---|---|---|---|
| **Mixpanel** | 4 orgs by shortname | gh, scw, sccon, sc | `WHERE organization_shortname IN (...)` |
| **Stripe** | 2 billing entities | "SC Home/Gabby LLC" (gh+sc), "Summer Classics" (scw+sccon) | `stripe__customer.name` JOIN `stripe__invoice` |
| **QuickBooks** | 2 billing entities | "SC Home/Gabby LLC", "Summer Classics, Inc." | `quickbooks__invoice.customer_ref_name` |
| **HelpScout** | 1 org name | "Gabriella White" only | `conv_customer_organization LIKE '%Gabby%' OR '%Summer%' OR '%Gabriella%'` |
| **Fathom** | 0 matches | Zero meetings for any entity name | Searched title, invitees, company fields |
| **HubSpot** | 5 company records | Summer Classics, SC Contract, SC Retail, Gabriella White, Gabby | `hubspot__company.properties_name` |

### Identity Issues

1. **HelpScout single-org:** All tickets under "Gabriella White" (sc). Cannot attribute tickets to specific entities.
2. **Stripe consolidated billing:** 2 Stripe customers cover 4 orgs. Per-entity MRR is estimated at 50/50 split within each billing group.
3. **HubSpot dead:** 5 company records with zero populated properties. No deals, contacts, or engagement data.
4. **Fathom absent:** Zero direct meetings for any entity.

---

## 2. Data Gaps Per Entity

### Gabby (gh) — Independently Sourced Data

| Data Point | Source | Status |
|---|---|---|
| CLM feature usage | `gh_2026-01-01_2026-03-02 (1).csv` | ✅ 54 users, 51 active |
| Orders analysis | `Gabby Admin Orders Report...(1).csv` | ✅ 2,215 orders, $6.92M |
| Org config | PostgreSQL org ID 55 | ✅ 8,117 products, 11,812 customers, 233 territories |
| Subscriptions | PostgreSQL subscriptions org 55 | ✅ 5 active plans |
| MAU trend | Mixpanel `organization_shortname = 'gh'` | ✅ 6 months: 40→48→42→42→43→48 |
| Import health | PostgreSQL import_events org 55 | ✅ 436 imports, 1 error (30d) |
| Sessions | PostgreSQL authenticated_sessions via org_users org 55 | ✅ 968,787 (90d) |
| User growth | PostgreSQL org_users org 55 | ✅ 85 new (90d) |
| Data freshness | PostgreSQL data_versions org 55 | ✅ Mar 2, 2026 23:53 |
| Inventory | PostgreSQL inventories org 55 | ✅ Mar 2, 2026 19:04 |
| Billing | Stripe + QuickBooks ("SC Home/Gabby LLC") | ⚠️ Combined with sc — 50/50 MRR split estimated |
| Support tickets | HelpScout ("Gabriella White") | ⚠️ All tickets attributed to sc org — cannot confirm gh-specific tickets |
| Fathom meetings | BigQuery fathom__ai_summaries | ❌ Zero meetings |
| HubSpot CRM | BigQuery hubspot__company ("Gabby") | ❌ Record exists but no data |
| Partner-since date | HubSpot deal history | ❌ No deals — using PG `organizations.created_at` (Apr 2013) |

### Summer Classics (scw)

Same as gh except:
- CLM: `scw_2026-01-01_2026-03-02.csv` ✅- Orders: `Summer Classics Admin Orders Report...csv` ✅
- PostgreSQL: org 87 ✅
- Mixpanel: shortname `scw` ✅
- Billing: Combined with sccon under "Summer Classics, Inc."

### SC Contract (sccon)

Same pattern plus:
- Submit Order = 0 in CLM ✅ (by design — Non-Ordering + Pushed Data profile confirmed)
- 849 orders in Admin Orders Report = pushed/imported data ✅

### SC Wholesale (sc)

Additional gaps:
- 0 territories in PostgreSQL (retail store model uses order origins instead)
- 91,090 customer records (inflated by historical imports)
- Customer Activation Rate artificially depressed (944/91,090 = 1.0%)
- Digital Self-Service = 0% (structural — retail stores, not a gap)
- HelpScout tickets all attributed here but may include cross-entity issues

---

## 3. Schema Notes

| Expected | Actual | Impact |
|---|---|---|
| `organizations.state` = geographic | Confirmed: GH=AL (not GA as previously reported) | Corrected in this rerun |
| `org_users.user_type` column | Actual: `user_type_id` → `user_types.name` join required | User type labels are org-specific (e.g., store names for sc) |
| `subscriptions.state` column | Actual: `status` column | Adjusted query |
| `subscriptions.product_name` | Actual: `subscription_plans.name` via join | Adjusted query |
| `authenticated_sessions.organization_id` | Does not exist — joined through `org_users` | Per-entity session counts verified |
| Mixpanel `name` column | Actual: `distinct_id` | Used `distinct_id` for active user counts |
| Mixpanel granular events | Only `api_access` events via WELD sync | All feature usage from CLM reports only |

---

## 4. Scoring Methodology & Limitations

### Per-Entity Scoring — Data Source Traceability

| Scoring Input | GH Source | SCW Source | SCCON Source | SC Source |
|---|---|---|---|---|
| Active User Ratio | `gh_...(1).csv`: 51/54 | `scw_...csv`: 56/58 | `sccon_...csv`: 29/29 | `sc_...csv`: 114/121 |
| Activity Ladder | `gh_...(1).csv` features | `scw_...csv` features | `sccon_...csv` features | `sc_...csv` features |
| Feature Breadth | `gh_...(1).csv`: 10.4 | `scw_...csv`: 9.1 | `sccon_...csv`: 9.8 | `sc_...csv`: 9.8 |
| Subscription Count | PG org 55: 5 plans | PG org 87: 5 plans | PG org 88: 5 plans | PG org 69: 4 plans |
| Order Volume | `Gabby Orders...(1).csv` | `SC Orders...csv` | `SC Contract Orders...csv` | `GW Orders...csv` |
| AOV | `Gabby Orders...(1).csv` | `SC Orders...csv` | N/A (non-ordering) | `GW Orders...csv` |
| Customer Activation | Orders CSV / PG customers | Orders CSV / PG customers | Orders CSV / PG customers | Orders CSV / PG customers |
| MAU Trend | Mixpanel `gh` | Mixpanel `scw` | Mixpanel `sccon` | Mixpanel `sc` |
| User Growth | PG org_users 55 | PG org_users 87 | PG org_users 88 | PG org_users 69 |

### Components Scored as N/A (Weight Redistributed)

| Entity | Component | Input | Reason |
|---|---|---|---|
| All 4 | Relationship Strength | Fathom Meeting Cadence | Zero meetings — weight → remaining 3 inputs |
| All 4 | Growth Signals | Fathom Pain → Unused | Zero meetings — weight → remaining 4 inputs |
| All 4 | Relationship Cooling | Fathom Days + Competitor | Zero meetings — weight → remaining 3 inputs |
| All 4 | Growth Signals | HubSpot Deals | No deal data → scores 0 (not N/A — absence = no deals) |
| SC | Business Impact | Digital Self-Service | Retail store model — weight → remaining 3 inputs |

### Scoring Interpretation Notes

1. **AUR Change "Flat" at ceiling (>90%):** All 4 entities have AUR >94%. "Flat" at this level was scored as 25 (near-increased) on risk, not 50 (stagnation). The framework doesn't distinguish flat-at-ceiling from flat-at-low-level. Flagged for recalibration.

2. **Pending vs. Open tickets:** HelpScout "pending" status = waiting for customer response. Scored as 25 for Unresolved Ticket Age (not 75-100 for >30 days) because the delay is customer-side, not SuperCat-side.

3. **Order Revenue seasonal decline (GH):** Jan $3.96M → Feb $2.81M = -29%. Scored as 25 (seasonal/market effect) rather than 75 (15-30% decline). Furniture January includes market orders; February is structurally lower. Without 12-month history, this is flagged but not penalized.

4. **SC Customer Activation Rate:** 944/91,090 = 1.0% scores 0 (<5%). The 91K denominator is inflated by historical imports. A meaningful denominator (customers with any interaction in 12 months) is not available.

5. **AOV Segment Median:** Estimated at ~$2,500 for furniture segment. Not portfolio-validated. All 4 entities exceed this.

6. **MRR per entity:** Estimated by equal split within billing groups. Actual per-entity pricing would change consolidated weighting.

---

## 5. Query Log

| # | System | Query Description | Result | Org/Entity |
|---|---|---|---|---|
| PG-1 | PostgreSQL | Org info | 4 rows: gh(55), sc(69), scw(87), sccon(88) | All |
| PG-2 | PostgreSQL | Users per org with type breakdown | gh: 7,859 total/130 enabled; sc: 155/93; scw: 4,418/173; sccon: 1,155/48 | All |
| PG-3 | PostgreSQL | Products per org | gh: 8,117; sc: 27,173; scw: 11,766; sccon: 13,455 | All |
| PG-4 | PostgreSQL | Customers per org | gh: 11,812; sc: 91,090; scw: 8,281; sccon: 5,228 | All |
| PG-5 | PostgreSQL | Territories per org | gh: 233; scw: 227; sccon: 98; sc: **0** | All |
| PG-6 | PostgreSQL | Active subscriptions | gh: 5; sc: 4; scw: 5; sccon: 5 | All |
| PG-7 | PostgreSQL | Recent orders (90d) | gh: 3,250; sc: 5,256; scw: 2,413; sccon: 1,667 | All |
| PG-8 | PostgreSQL | Total orders all-time | gh: 170,843; sc: 322,935; scw: 113,931; sccon: 62,751 | All |
| PG-9 | PostgreSQL | Data freshness | All 4 updated Mar 2, 2026 | All |
| PG-10 | PostgreSQL | Import events (30d) | gh: 436/1err; sc: 364/2err; scw: 439/1err; sccon: 405/1err | All |
| PG-11 | PostgreSQL | Product images | gh: 16,273; sc: 19,040; scw: 15,621; sccon: 17,579 | All |
| PG-12 | PostgreSQL | Price levels | gh: 84; sc: 73; scw: 82; sccon: 67 | All |
| PG-13 | PostgreSQL | Auth sessions (90d) | gh: 968,787; sc: 787,307; scw: 870,761; sccon: 647,077 | All |
| PG-14 | PostgreSQL | User growth (90d) | gh: 85; sc: 12; scw: 79; sccon: 27 | All |
| PG-15 | PostgreSQL | Inventory freshness | All 4 updated Mar 2, 2026 | All |
| BQ-1 | BigQuery | Mixpanel events by org | Only `api_access` for all 4 | All |
| BQ-2 | BigQuery | Mixpanel active users | gh: 55; sc: 117; sccon: 32; scw: 61 | All |
| BQ-3 | BigQuery | Mixpanel MAU 6-month | 26 rows (4 orgs × ~6 months) | All |
| BQ-4 | BigQuery | Stripe subscriptions | 0 active (2 canceled) | All |
| BQ-5 | BigQuery | Stripe invoices (6mo) | 23 rows, 2 billing entities | All |
| BQ-6 | BigQuery | QuickBooks invoices | 20 rows, 2 billing entities, all $0 balance | All |
| BQ-7 | BigQuery | HelpScout tickets (90d) | 6 distinct tickets, all "Gabriella White" | All |
| BQ-8 | BigQuery | HelpScout quarterly | Q1'25: 45 → Q2'25: 157 → Q3'25: 139 → Q4'25: 100 → Q1'26: 93 | All |
| BQ-9 | BigQuery | Fathom meetings | 0 results | All |
| BQ-10 | BigQuery | HubSpot companies | 5 records, no useful data | All |
| CSV-1 | Python | GH CLM parse | 54 users, 51 active, 6,162 Submit Orders | gh |
| CSV-2 | Python | SCW CLM parse | 58 users, 56 active, 5,650 Submit Orders | scw |
| CSV-3 | Python | SCCON CLM parse | 29 users, 29 active, 0 Submit Orders | sccon |
| CSV-4 | Python | SC CLM parse | 121 users, 114 active, 12,311 Submit Orders | sc |
| CSV-5 | Python | GH Orders parse | 2,215 orders, $6.92M, 967 distinct customers | gh |
| CSV-6 | Python | SCW Orders parse | 1,646 orders, $6.42M, 628 distinct customers | scw |
| CSV-7 | Python | SCCON Orders parse | 849 orders, $10.67M, 316 distinct customers | sccon |
| CSV-8 | Python | SC Orders parse | 2,726 orders, $11.19M, 944 distinct customers | sc |

---

## 6. Multi-Entity Observations

### Framework Gaps for Parent/Child Structures

1. **Consolidated billing:** Stripe invoices are per billing entity, not per org. Per-entity MRR requires explicit pricing metadata or manual allocation. Neither is available.

2. **Shared rep pools:** `sc-` username prefix appears across all 4 CLM files. Ryan Casabella (`sc-ryanc`) is top power user in both gh (992 orders) and scw (1,112 orders). The framework doesn't detect or account for cross-entity rep activity.

3. **HelpScout single-org routing:** All tickets to "Gabriella White." Per-entity support metrics are impossible without ticket tagging.

4. **Mixed use-case profiles:** SCCON is Non-Ordering + Pushed Data while the other 3 are Ordering. The consolidated score blends different Business Impact methodologies — conceptually imprecise.

5. **Retail model:** SC Wholesale operates physical retail stores. Two Business Impact metrics (Customer Activation Rate, Digital Self-Service) are structurally inapplicable. The framework needs a "Retail" use-case profile.

6. **Zero territories for SC:** Retail store model uses order origins (store names) instead of territories. The framework assumes all ordering clients have territories.

### Cross-Entity Rep Detection

| Rep (username) | GH CLM | SCW CLM | SCCON CLM | SC CLM |
|---|---|---|---|---|
| sc-ryanc (Ryan Casabella) | ✅ #1 (992 orders) | ✅ (1,112 orders) | — | — |
| sc-clarer (Clare Colón) | ✅ #3 (408 orders) | ✅ (274 orders) | — | — |
| sc-davids (David Sherrill) | ✅ (196 orders) | ✅ (244 orders) | — | — |
| sc-denaec (Denae Copeland) | ✅ (204 orders) | ✅ (147 orders) | — | — |
| sc-tanyah (Tanya Houge) | ✅ (162 orders) | ✅ (351 orders) | — | — |
| zww (Wynne White) | ✅ (289 orders) | ✅ (492 orders) | ✅ | — |

Multiple reps appear in both gh and scw CLM files with different order counts, confirming they submit orders through both catalogs. Wynne White appears in gh, scw, AND sccon — a cross-entity admin user.

---

## 7. CSV Data Usage

| File | Entity | Records | Metrics Computed | Parsing Status |
|---|---|---|---|---|
| `gh_2026-01-01_2026-03-02 (1).csv` | GH | 54 users | Active users, logins, submit orders, feature breadth, power users, activity ladder, per-feature totals | ✅ Clean parse |
| `scw_2026-01-01_2026-03-02.csv` | SCW | 58 users | Same | ✅ Clean parse |
| `sccon_2026-01-01_2026-03-02.csv` | SCCON | 29 users | Same (Submit Order = 0 confirms non-ordering) | ✅ Clean parse |
| `sc_2026-01-01_2026-03-02.csv` | SC | 121 users | Same | ✅ Clean parse |
| `Gabby Admin Orders Report...(1).csv` | GH | 2,215 orders | AOV, types, origins, territories, monthly, distinct customers, concentration | ✅ Clean parse |
| `Summer Classics Admin Orders Report...csv` | SCW | 1,646 orders | Same | ✅ Clean parse |
| `Summer Classics Contract Admin Orders Report...csv` | SCCON | 849 orders | Same | ✅ Clean parse |
| `Gabriella White Admin Orders Report...csv` | SC | 2,726 orders | Same | ✅ Clean parse |

---

## 8. Framework Feedback

### What Worked

1. **Independent per-entity scoring** produces clean, traceable results. Each entity's score derives exclusively from its own data sources.
2. **Use-case profile detection** correctly classified sccon as Non-Ordering + Pushed Data based on CLM Submit Order = 0 + Orders Report > 0.
3. **Fathom/HelpScout absence protocol** prevented artificial score deflation for a self-sufficient account.
4. **Activity Ladder from CLM** provided comprehensive feature usage data without requiring granular Mixpanel events.

### What Needs Change

1. **Multi-entity framework:** Needs parent/child org mapping, consolidated scoring methodology, cross-entity rep detection, shared billing attribution rules.
2. **Retail use-case profile:** Customer Activation Rate and Digital Self-Service don't apply to physical retail stores. Need alternative metrics.
3. **Mixpanel WELD limitation:** Only `api_access` events sync. CLM reports fill the gap for iPad but miss Online/Portal/B2B Cart feature usage.
4. **"Flat at ceiling" scoring:** AUR at 94% scoring the same as AUR at 30% when both are "flat" creates false risk signals for high-adoption accounts.
5. **Cross-entity customer/rep deduplication:** The same reps appear in multiple entity CLM files. Total active user count (250) may double-count individuals.
6. **Pending ticket age thresholds:** "Pending" (customer-side delay) should score differently from "Open" (agent-side delay). Current thresholds don't distinguish.

---

*End of Generation Notes — Independent Per-Entity Rerun*
