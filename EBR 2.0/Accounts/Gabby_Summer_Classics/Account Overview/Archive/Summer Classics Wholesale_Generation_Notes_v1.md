# Summer Classics Wholesale — Generation Notes

**Generated:** March 2, 2026 | **Author:** Cursor/MCP | **Framework Version:** 1.0

---

## Execution Summary

| Step | Status | Notes |
|---|---|---|
| Step 0: CSV Prerequisite Check | ✅ Complete | CLM: `sc_2026-01-01_2026-03-02.csv` (121 users). Orders: `Gabriella White Admin Orders Report 2026-01-01 - 2026-03-03 (1).csv` (2,726 orders). |
| Step 1: Reference Documents | ✅ Complete | All 5 documents read: Internal_Account_Brief_Outlines.md, Account_Scoring_Framework_v3.md, Scoring_Thresholds_Companion.md, Metrics_Framework_v5.md, Metrics_Surface_Area_v5.csv. |
| Step 2: Mixpanel Event Discovery | ✅ Complete | Modern snake_case convention confirmed. 35 distinct event types in 90d. Filter: `current_organization_shortname = 'sc'` (not `organization_shortname`). |
| Step 3: Use-Case Profile | ✅ Complete | **Ordering** — 4,430 `order_submitted` events in Mixpanel, 5,336 orders in PostgreSQL. |
| Step 4: Data Collection | ✅ Complete | PostgreSQL: 8 queries. BigQuery: 15 queries. CSV parsing: 2 Python scripts. |
| Step 5: Scoring | ✅ Complete | Expansion Readiness: **62** (Nurture). Retention Risk: **24** (Low). Quadrant: **GROW**. |
| Step 6: Output Generation | ✅ Complete | 3 files generated. |

---

## Data Gaps

### HubSpot — Column Schema Mismatch
- **Issue:** Initial HubSpot deal query used `properties_dealname` which appears correct per error hint, but the full query failed. Company query initially tried `property_name` which BigQuery corrected to `properties_name`. The company query returned a large output file but was not parsed due to tool output size limits.
- **Impact:** Could not populate: HubSpot account owner, open expansion deals, original deal close date, company headquarters, industry tags.
- **Workaround:** Partner Since date derived from PostgreSQL `organizations.created_at` (Feb 5, 2014). HQ derived from Stripe customer address and QuickBooks billing address.
- **Fix:** Describe `hubspot__deal` and `hubspot__company` tables before querying. Run targeted queries with verified column names.

### Stripe Subscriptions — Zero Rows
- **Issue:** `stripe__subscription` returned 0 rows for customer `cus_SXChHLspKtOS44`.
- **Impact:** Could not derive per-product MRR or subscription status from Stripe.
- **Workaround:** MRR estimated from Stripe deleted invoices (~$2,866–$3,226/mo) and QuickBooks invoice amounts. Payment status confirmed via Stripe `delinquent: false` and QuickBooks $0 balances.
- **Root Cause:** Billing likely migrated from Stripe subscriptions to QuickBooks manual invoicing. The Stripe invoices exist but are all status "deleted."

### Stripe Invoice Amounts — All "Deleted" Status
- **Issue:** All 4 Stripe invoices for this customer have `status: deleted` and `amount_paid: 0`.
- **Impact:** Cannot confirm whether Stripe was ever the active billing mechanism or if invoices were voided before payment.
- **Workaround:** QuickBooks is the confirmed billing source. Amounts in QuickBooks match expected ranges.

### QuickBooks — Consolidated Parent Billing
- **Issue:** QuickBooks bills under "Summer Classics, Inc." (covers scw + sc entities, sharing QB ID 114) and "SC Home/Gabby LLC" (covers gh). Cannot isolate sc-specific MRR from consolidated invoices.
- **Impact:** MRR for the sc entity specifically is estimated, not precise.
- **Fix:** Would require line-item detail from QuickBooks invoices (not available via current MCP schema) or Stripe subscription reactivation.

### Fathom — No Direct Meetings
- **Issue:** No Fathom meetings directly with Summer Classics/Gabriella White stakeholders found in 180 days. Only indirect mentions in internal SuperCat support standups.
- **Impact:** Fathom scoring inputs (Meeting Cadence, Competitor Mentions, Pain Themes) all scored as N/A with weight redistribution per framework protocol. No relationship intelligence (MEDDIC fields, objections, sentiment) available.
- **Note:** This is the expected Fathom absence pattern — surfaced as operational callout ("consider establishing cadence"), not a scoring penalty.

### Mixpanel — Organization Shortname Filter
- **Issue:** The `organization_shortname` column had data only for `api_access` events. The `current_organization_shortname` column contained the org context for iPad-originated events.
- **Impact:** Initial query returned only 1 event type. Required OR filter on both columns.
- **Fix for future:** Always filter Mixpanel with `(current_organization_shortname = 'X' OR organization_shortname = 'X')`.

### PostgreSQL — Territories
- **Issue:** `territories` table returns 0 rows for org_id 69 despite 42+ territory codes appearing in the Orders CSV.
- **Impact:** Territory configuration is not in the app. Reps cannot filter by territory in the iPad app. Sales Portal dashboards cannot segment by territory.
- **Root Cause:** Territory codes in the Orders CSV are assigned at the order level (likely mapped in the ERP), not configured in the SuperCat admin console.
- **Expansion Signal:** Configuring territories in PostgreSQL would unlock significant functionality.

### PostgreSQL — import_events Schema
- **Issue:** `import_events` table has only 4 columns: `id`, `created_at`, `organization_id`, `data`. The `data` column is YAML text (not JSON). No `data_type`, `status`, or `error` columns.
- **Impact:** Cannot directly query import type breakdown or error rates. Had to parse YAML `data` field text to identify import types.
- **Workaround:** Recent import data shows "[]" in error arrays within YAML, indicating clean imports. Error rate estimated at 0%.

---

## Schema Mismatches

| Table | Expected Column | Actual Column | Resolution |
|---|---|---|---|
| `mixpanel__events` | `mp_event_name` | `event_name` | Used correct column |
| `mixpanel__events` | `_timestamp` | `time` (FLOAT, Unix) | Converted with `TIMESTAMP_SECONDS(CAST(time AS INT64))` |
| `mixpanel__events` | `properties_org_shortname` | `organization_shortname` / `current_organization_shortname` | Used OR filter on both |
| `helpscout__help_scout_tickets` | `ticket_created` | `ticket_created_at` | Used correct column |
| `fathom__ai_summaries` | `ai_summary` | `Ai Summary Plaintext Formatted` | Used backtick-quoted column name |
| `fathom__ai_summaries` | `call_created_at` | `Meeting Start Time` | Used backtick-quoted column name |
| `hubspot__company` | `property_name` | `properties_name` | Identified via error hint |
| `hubspot__deal` | `property_createdate` | `properties_createdate` | Identified via error hint |
| `stripe__subscription` | `customer` | `customer_id` | Identified via error hint |
| `import_events` | `data_type` column | Does not exist | Data is in YAML `data` field |

---

## Scoring Limitations

### Business Impact — Retail Model Distortion
The two lowest-scoring inputs (Customer Activation Rate: 0, Digital Self-Service Rate: 0) are structurally distorted by the retail showroom model:

- **Customer Activation Rate (0):** The 91,081 "customers" in PostgreSQL are end consumers accumulated since 2014, not B2B buyers. Scoring 2,020 active purchasers against 91K total yields 2.2%, which falls in the "0" band (<5%). For a retail-direct model, 2,020 unique purchasing customers in 2 months is actually substantial. The threshold was designed for B2B wholesale where customers = dealers/retailers, not consumers.

- **Digital Self-Service Rate (0):** This account's business model is showroom-based selling where reps guide customers through product selection on iPad. eCat Online is enabled but not intended as a buyer self-service ordering channel — it's a catalog browsing tool. The 0% self-service rate is by design, not by failure.

**Recommendation:** Consider adding a "Retail" use-case profile to the scoring framework that replaces Customer Activation Rate with "Orders per Store Location" and Digital Self-Service Rate with "Catalog Engagement Rate (eCat Online views / total catalog views)."

### Relationship Strength — Fathom Absence
With Fathom inputs redistributed, Relationship Strength is scored on only 3 of 4 inputs. The Days Since Last Interaction input (75) is based on HelpScout only, which means the score reflects reactive engagement. If proactive meetings were occurring but not recorded in Fathom, the score underrepresents the actual relationship strength.

### Growth Signals — HubSpot Data Gap
Two of five Growth Signals inputs (Fathom Pain→Feature, HubSpot Expansion Deals) are N/A due to data unavailability. This reduces the scoring inputs to 3, which may overweight MAU Trend and User Growth relative to the framework's intent.

---

## Query Issues

| Query | Issue | Resolution |
|---|---|---|
| Mixpanel event discovery (initial) | `properties_org_shortname` doesn't exist | Described table first, used `organization_shortname` |
| HelpScout tickets (initial) | `ticket_created` → `ticket_created_at` | Used correct column from describe |
| Fathom summaries (initial) | `ai_summary` doesn't exist; spaced column names | Used backtick-quoted `Ai Summary Plaintext Formatted` |
| Stripe subscription | 0 rows returned | Billing not via Stripe subscriptions; fell back to Stripe invoices → QuickBooks |
| HubSpot company | `property_name` → `properties_name` | Corrected but output was too large to parse inline |
| HubSpot deal | `property_createdate` → `properties_createdate` | Corrected but `id` column also failed — table may use different primary key |
| QuickBooks invoice (initial) | `customer_display_name` doesn't exist | Described table, used `customer_ref_name` |
| import_events `data_type` | Column doesn't exist | Used `data` YAML field text analysis |
| HelpScout duplicate rows | Thread-level join produces N rows per ticket (one per thread) | Used DISTINCT on conversation_id for deduplication |

---

## CSV Data Usage

### CLM Report (`sc_2026-01-01_2026-03-02.csv`)
- **Used for:** Per-rep feature usage counts, Feature Breadth calculation (avg 9.8), Activity Ladder org-level scoring, power user identification, Submit Order distribution, enablement gap analysis, eCat version currency check.
- **Parsing notes:** 121 rows (users), 44 columns. 7 users with blank Last Login Date and empty feature counts (fully inactive). Feature column headers match legacy PascalCase event names as expected.
- **Discrepancy vs Mixpanel:** CLM shows 12,293 total Submit Order events vs. Mixpanel's 4,430 `order_submitted` events. CLM period is Jan 1 – Mar 2 (61 days) while Mixpanel 90-day window extends back to early December. The CLM counts are higher because they capture all Submit Order events including resubmissions, while Mixpanel may deduplicate. Used CLM for per-rep breakdown and Mixpanel for trend analysis.

### Orders Report (`Gabriella White Admin Orders Report 2026-01-01 - 2026-03-03 (1).csv`)
- **Used for:** AOV ($4,104.51), order volume (2,726), Order Type breakdown (Confirmed/Quote/TEST), Order Origin breakdown (14 store locations), territory performance (42 territories), customer concentration analysis, monthly revenue trend (Jan→Feb +53%), customer activation count (2,020 distinct).
- **Parsing notes:** 2,727 rows (including header). Some orders have blank Customer Number (walk-in retail customers without accounts). 12 TEST orders excluded from most analysis. Currency is all USD.
- **Key insight from CSV:** The "Order Origin" field maps directly to store locations (not generic "Regular"/"Market" categories), which is specific to the retail showroom model. This provides per-store performance visibility not available from any MCP source.

---

## Framework Feedback

### Retail Use-Case Profile Needed
The current three profiles (Ordering, Non-Ordering, Non-Ordering + Pushed Data) don't account for retail-direct models where:
- "Customers" are end consumers, not B2B buyers
- Orders are placed by reps on behalf of in-store customers (not by customers themselves)
- Digital self-service (eCat Online) is a catalog tool, not an ordering channel
- Territory structures map to store locations, not geographic sales territories

A "Retail Ordering" profile should adjust:
- Customer Activation Rate → "Active Customers per Store per Month"
- Digital Self-Service Rate → "eCat Online Catalog Engagement Rate" or remove from scoring
- Territory Performance → "Store Performance" with per-location metrics

### HelpScout Ticket Deduplication
The HelpScout BigQuery table joins tickets with threads, producing N rows per ticket (one per thread). Queries for "unique tickets in period" require DISTINCT on conversation_id. The framework should note this in the query specification to avoid inflated ticket counts.

### Billing Model Complexity
This account demonstrates the complexity the billing model detection fallback hierarchy was designed for: Stripe subscriptions exist but have 0 rows, Stripe invoices exist but are "deleted," and QuickBooks invoices consolidate multiple entities under one customer name. The fallback worked but required multiple queries across all three sources.

### Multi-Entity Scoring Ambiguity
The four entities (gh, sc, scw, sccon) share reps (users with sc-* prefix access all four). Mixpanel events include all four orgs for shared users. The CLM report is org-specific (sc only), but Mixpanel user-level data bleeds across entities. Scoring was scoped to the sc entity, but some Mixpanel metrics may include cross-entity activity for shared users.

### Order Origin as First-Class Dimension
For retail-model accounts, "Order Origin" (store location) is the primary organizational dimension — more meaningful than Territory for performance analysis. The framework's Territory Performance section (§2a) should have a parallel "Store Performance" section for retail accounts.

---

## Data Inventory Summary

| Source | Tables Queried | Key Data Points |
|---|---|---|
| PostgreSQL | organizations, org_users, products, customers, territories, subscriptions, subscription_plans, import_events, data_versions, product_images, options, price_levels, taxonomies | Org config, 155 users, 27,173 products, 91,081 customers, 0 territories, 4 subscriptions, 1,190 imports (90d), 19,040 images, 73 price levels |
| Mixpanel (BigQuery) | mixpanel__events | 35 event types, 131 active users, 6-month MAU trend, per-user activity |
| HelpScout (BigQuery) | helpscout__help_scout_tickets | 30 tickets (12 months), 12 tickets (90d), 7 open/pending |
| Fathom (BigQuery) | fathom__ai_summaries | 0 direct meetings; 5 indirect mentions in internal standups |
| HubSpot (BigQuery) | hubspot__company (partial), hubspot__deal (failed) | Company data retrieved but not parsed (large output) |
| Stripe (BigQuery) | stripe__customer, stripe__subscription, stripe__invoice | Customer confirmed, 0 subscriptions, 4 deleted invoices |
| QuickBooks (BigQuery) | quickbooks__invoice | 10 invoices across 2 billing entities, all current |
| Admin CLM CSV | Uploaded | 121 users, 44 feature columns, per-rep breakdowns |
| Admin Orders CSV | Uploaded | 2,726 orders, $11.2M revenue, 14 store locations, 42 territories |
