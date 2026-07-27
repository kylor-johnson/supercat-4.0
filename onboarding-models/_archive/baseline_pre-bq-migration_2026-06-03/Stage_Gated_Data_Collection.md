# Stage-Gated Data Collection Playbook

**Purpose:** Collect all quantitative TRUE/FALSE metrics from PostgreSQL (eCat production) and BigQuery (HubSpot, MixPanel, Fathom, HelpScout)  
**Output:** Structured data per client (no prose, just metrics)  
**Next Step:** Run `Validation_Layer_Fathom_HelpScout.md`

**Reference:** See `BIGQUERY_WINDMILL_MCP_REFERENCE.md` for complete BigQuery setup and table documentation

---

## ⛔ ANTI-HALLUCINATION RULES

These rules are NON-NEGOTIABLE:

```
⛔ FORBIDDEN: Generating ANY numeric value without a tool call
⛔ FORBIDDEN: Using "approximately", "estimated", or "~" for metrics
⛔ FORBIDDEN: Inferring values from context or prior knowledge
⛔ FORBIDDEN: Copying values from user-provided documents
⛔ FORBIDDEN: Using cached data from earlier in conversation
⛔ FORBIDDEN: Calling any user-supercat-cs-tools MCP endpoints (they return 404 - API not built)
```

**If a tool call fails:**
1. Mark the metric as `❓ QUERY FAILED: [error message]`
2. DO NOT substitute a plausible value
3. Document which tool failed and why

---

## STEP 1: CLIENT DISCOVERY (HubSpot via BigQuery)

**⚠️ CRITICAL:** Do NOT use MCP `status` field. HubSpot is the authoritative source.

### Query: Get All Onboarding Clients

**Use MCP BigQuery Tool:**

```
Tool: user-bigquery-vpn > query
Parameters:
  query: |
    SELECT 
      company_id,
      properties_name,
      properties_domain,
      properties_lifecyclestage,
      properties_hs_date_entered_evangelist,
      properties_createdate
    FROM hubspot__company
    WHERE properties_lifecyclestage = 'evangelist'
    ORDER BY properties_hs_date_entered_evangelist DESC
  max_results: 50
```

**Notes:**
- HubSpot data is in BigQuery via Weld (syncs daily)
- Internal HubSpot value: `evangelist` = "Onboarding" in the UI
- No API tokens needed - query directly via MCP

### Output: Client List for Assessment

After running the HubSpot query, document:

```markdown
## CLIENTS TO ASSESS

| HubSpot Name | Domain | MCP Shortname | Date Entered Onboarding |
|--------------|--------|---------------|-------------------------|
| [Company 1] | [domain.com] | [shortname] | [YYYY-MM-DD] |
| [Company 2] | [domain.com] | [shortname] | [YYYY-MM-DD] |
```

---

## STEP 2: POSTGRESQL DATA COLLECTION

All eCat configuration data is queried via the PostgreSQL MCP connection (`user-supercat-postgres-vpn`).

### ⚡ BATCH QUERY PATTERN (Recommended for Multiple Clients)

When assessing multiple clients, **batch queries** to avoid excessive individual tool calls. Replace single-client `WHERE o.shortname = '[ORG_SHORTNAME]'` with:

```sql
WHERE o.shortname IN ('pebl', 'tcd', 'mali', 'hvusa', 'krb', 'cst', 'dccl')
```

Add `o.shortname` or `o.name` to the SELECT clause and `GROUP BY o.shortname` where needed. This reduces ~15 queries per client down to ~15 total queries for all clients.

**Example (batched product metrics):**
```sql
SELECT o.shortname,
  COUNT(*) as total_products,
  COUNT(CASE WHEN image_exists = true THEN 1 END) as products_with_images,
  COUNT(DISTINCT category_code) as unique_categories,
  COUNT(DISTINCT collection_code) as unique_collections,
  MAX(p.last_modified_at) as last_product_update
FROM products p
JOIN organizations o ON p.organization_id = o.id
WHERE o.shortname IN ('pebl', 'tcd', 'mali', 'hvusa', 'krb', 'cst', 'dccl')
  AND p.deleted = false
GROUP BY o.shortname
ORDER BY o.shortname
```

The individual queries below are still valid for single-client runs.

### Query 1: Organization Info

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT id, name, shortname, created_at, order_email_recipient,
      send_order_email_on_submit
    FROM organizations
    WHERE shortname = '[ORG_SHORTNAME]'
```

### Query 2: Product Metrics

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT 
      COUNT(*) as total_products,
      COUNT(CASE WHEN image_exists = true THEN 1 END) as products_with_images,
      COUNT(DISTINCT category_code) as unique_categories,
      COUNT(DISTINCT collection_code) as unique_collections,
      MAX(last_modified_at) as last_product_update
    FROM products p
    JOIN organizations o ON p.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]' AND p.deleted = false
```

### Query 3: Customer Metrics

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT 
      COUNT(*) as total_customers,
      MAX(updated_at) as last_customer_update
    FROM customers c
    JOIN organizations o ON c.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
```

### Query 4: User Metrics (Excluding SuperCat Staff)

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT 
      COUNT(*) as total_users,
      COUNT(CASE WHEN ou.is_admin = true THEN 1 END) as admin_users,
      COUNT(CASE WHEN ou.is_admin = false THEN 1 END) as non_admin_users
    FROM org_users ou
    JOIN organizations o ON ou.organization_id = o.id
    JOIN users u ON ou.user_id = u.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
      AND u.email NOT LIKE '%@supercatsolutions.com'
```

### Query 5: Price Levels

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT code, name
    FROM price_levels pl
    JOIN organizations o ON pl.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
    ORDER BY code
```

### ~~Query 6: Categories~~ (REMOVED — no `categories` table exists)

**⚠️ NOTE:** There is no separate `categories` table in production. Category counts are already captured by Query 2 via `COUNT(DISTINCT category_code) as unique_categories` from the `products` table. Use `unique_categories` from Query 2 instead.

### ~~Query 7: Collections~~ (REMOVED — no `collections` table exists)

**⚠️ NOTE:** There is no separate `collections` table in production. Collection counts are already captured by Query 2 via `COUNT(DISTINCT collection_code) as unique_collections` from the `products` table. Use `unique_collections` from Query 2 instead.

### Query 8: Options

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT COUNT(*) as options_count
    FROM options opt
    JOIN organizations o ON opt.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
```

### ⚠️ CRITICAL: Options Count

When counting options:
- Count the NUMBER OF RECORDS returned from the `options` table
- NOT the number of option columns in the schema
- This is a common error source

### Query 9: Territories

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT COUNT(*) as territory_count
    FROM territories t
    JOIN organizations o ON t.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
```

### Query 10: Import Events (Last 30 Days)

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT id, created_at, LEFT(data::text, 500) as data_preview
    FROM import_events ie
    JOIN organizations o ON ie.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
    ORDER BY ie.created_at DESC
    LIMIT 30
```

**Note:** `import_events.data` is YAML text. Look for `:error` entries in the data to identify import failures.

### Query 11: Inventories

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT 
      COUNT(*) as inventory_count,
      MAX(updated_at) as last_inventory_update
    FROM inventories inv
    JOIN organizations o ON inv.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
```

### Query 12: Mobile Sites (eCat Online / Sales Portal)

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT 
      ms.url_key,
      ms.custom_cname,
      ms.title,
      ms.enable_online_catalog,
      ms.enable_sales_portal,
      ms.document_logo_file_name
    FROM mobile_sites ms
    JOIN organizations o ON o.id = ms.organization_id
    WHERE o.shortname = '[ORG_SHORTNAME]'
```

### Query 13: Report Formats (iPad Reports)

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT COUNT(*) as report_format_count
    FROM ipad_reports ir
    JOIN organizations o ON ir.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
```

### Query 14: Orders

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT COUNT(*) as order_count
    FROM orders ord
    JOIN organizations o ON ord.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
```

### Query 15: User Types & Permissions

```
Tool: user-supercat-postgres-vpn > execute_sql
Parameters:
  sql: |
    SELECT ut.id, ut.name, ut.allow_ipad_logins,
      ut.enable_online_ordering, ut.allow_user_enrollment
    FROM user_types ut
    JOIN organizations o ON ut.organization_id = o.id
    WHERE o.shortname = '[ORG_SHORTNAME]'
    ORDER BY ut.name
```

---

## STEP 3: BIGQUERY DATA COLLECTION

### iPad Activity Query (MixPanel)

**Use MCP BigQuery Tool:**

**⚠️ FIRST: Verify event names if this is your first run. Event names may vary:**

```
Tool: user-bigquery-vpn > get_unique_event_names
Parameters:
  table_name: "mixpanel__events"
  event_column: "event_name"
  limit: 50
```

**Then run the actual query. IMPORTANT: iPad events do NOT have `organization_shortname` populated — only `api_access` events do. Use the subquery join pattern below to map users to orgs:**

```
Tool: user-bigquery-vpn > query
Parameters:
  query: |
    SELECT 
      COUNT(*) as ipad_order_count,
      COUNT(DISTINCT e.distinct_id) as unique_ipad_users,
      TIMESTAMP_SECONDS(CAST(MAX(e.time) AS INT64)) as last_ipad_order
    FROM mixpanel__events e
    JOIN (
      SELECT username, organization_shortname,
        ROW_NUMBER() OVER (PARTITION BY username ORDER BY time DESC) as rn
      FROM mixpanel__events
      WHERE event_name = 'api_access'
        AND organization_shortname IS NOT NULL
        AND username IS NOT NULL
    ) org_map ON e.username = org_map.username AND org_map.rn = 1
    WHERE e.event_name = 'order_submitted'
      AND org_map.organization_shortname = '[ORG_SHORTNAME]'
  max_results: 10
```

**Key Notes (Windmill/Weld Pipeline):**
- Table: `mixpanel__events` (no dataset prefix needed - MCP scopes to `WELD_RAW`)
- **⚠️ `organization_shortname` is NULL for ALL iPad/mobile events** (order_submitted, product_search, etc.). ONLY `api_access` events have it populated.
- **Must use subquery join:** Map users to orgs via `api_access` events (the `username` field links them), then join to the target event type.
- The `time` column is a FLOAT (Unix timestamp) — always wrap with `TIMESTAMP_SECONDS(CAST(time AS INT64))` to get a readable date.
- Event names are snake_case: `order_submitted`, `product_search`, `customer_search`, etc.
- Device detection columns (`os`, `model`) exist but are not needed for the org-level query above — all `order_submitted` events are from iPads.
- `os` values include `iPadOS`, `iOS`, `iPhone OS`; `model` values are like `iPad14,6`, `iPad15,8`

---

## STAGE VALIDATION CRITERIA

### Products Supported

| Product | Required Stages |
|---------|-----------------|
| **eCat iPad** | 1, 2, 3, 4*, 5, 6, 7 |
| **eCat Online** | 1, 2, 3, 4*, 5, 6, 8, 9, 10* |
| **Sales Portal** | 1, 2, 3, 4*, 5, 6, 8, 9, 11 |

*Conditional stages based on feature enablement

---

### Stage 1: Account Foundation

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Company name exists | Query 1 (organizations) | `name` is not empty |
| Account active | Query 1 (organizations) | Organization record exists (no `status` column - existence = active) |
| Admin user exists | Query 4 (org_users) | At least 1 user with `is_admin = true` (excluding SuperCat staff emails) |

**Pass Criteria:**
- 🔴 **RED:** Any check FALSE
- 🟢 **GREEN:** All checks TRUE

---

### Stage 2: Catalog Setup

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Products imported | Query 2 (products) | `total_products >= 10` |
| Products have images | Query 2 (products) | `products_with_images >= 10` |
| Categories exist | Query 2 (products) | `unique_categories >= 1` |
| Collections exist | Query 2 (products) | `unique_collections >= 1` |

**Pass Criteria:**
- 🔴 **RED:** Products < 10
- 🟡 **YELLOW:** Products 10-100
- 🟢 **GREEN:** Products >= 100
  - ✅ **Bonus:** `last_product_update` within 30 days (shows active catalog maintenance)

---

### Stage 3: Pricing Configuration

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Price levels exist | Query 5 (price_levels) | Row count >= 1 |
| Multiple price levels | Query 5 (price_levels) | Row count >= 2 |
| Descriptive names | Query 5 (price_levels) | `name` values are NOT "Price Level 1", "Price Level 2" |

**Pass Criteria:**
- 🔴 **RED:** No price levels (count = 0)
- 🟡 **YELLOW:** Only 1 price level OR generic names
- 🟢 **GREEN:** 2+ price levels with descriptive names

---

### Stage 4: Option Configuration (CONDITIONAL)

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Options enabled | Query 8 (options) | `options_count > 0` |
| Options configured | Query 8 (options) | `options_count >= 5` |

**Pass Criteria:**
- ⚪ **N/A:** Options disabled (0 records returned) - SKIP TO STAGE 5
- 🔴 **RED:** Options enabled but broken
- 🟡 **YELLOW:** 1-4 options configured
- 🟢 **GREEN:** 5+ options configured

---

### Stage 5: Customer & User Setup

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Customers imported | Query 3 (customers) | `total_customers >= 10` |
| Users configured | Query 4 (org_users) | `total_users >= 2` |
| Multiple user types | Query 15 (user_types) | Row count >= 2 |

**Pass Criteria:**
- 🔴 **RED:** Customers < 10 OR users < 2
- 🟡 **YELLOW:** Customers 10-100
- 🟢 **GREEN:** Customers >= 100
  - ✅ **Bonus:** `last_customer_update` within 30 days (shows active customer data maintenance)

---

### Stage 6: Operational Data

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| No critical import errors | Query 10 (import_events) | No `:error` entries in last 30 events |
| Inventory data exists | Query 11 (inventories) | `inventory_count > 0` |
| Inventory fresh | Query 11 (inventories) | `last_inventory_update` within 7 days |

**Pass Criteria:**
- 🔴 **RED:** Critical import errors OR inventory enabled but no data
- 🟡 **YELLOW:** Stale inventory (7+ days)
- 🟢 **GREEN:** Fresh data AND no import errors

---

### Stage 7: iPad Order-Ready (eCat iPad Only)

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| User types exist | Query 15 (user_types) | More than 1 user type (not just default) |
| iPad activity exists | BigQuery MixPanel query | `ipad_order_count >= 1` |
| Report formats configured | Query 13 (ipad_reports) | `report_format_count >= 3` |
| Orders exist | Query 14 (orders) | `order_count >= 1` |
| Order email configured | Query 1 (organizations) | `order_email_recipient` is not null |

**Pass Criteria:**
- ⚪ **N/A:** eCat iPad not being implemented
- 🔴 **RED:** Any critical check FALSE
- 🟡 **YELLOW:** Critical checks pass but order email missing
- 🟢 **GREEN:** All checks TRUE

---

### Stage 8: eCat Online Site Setup (eCat Online / Sales Portal)

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Site enabled | Query 12 (mobile_sites) | `enable_online_catalog = true` OR `enable_sales_portal = true` |
| Web portal configured | Query 12 (mobile_sites) | `custom_cname` is not null/empty OR `title` is not null/empty |
| Logo uploaded | Query 12 (mobile_sites) | `document_logo_file_name` is not null |

**Pass Criteria:**
- ⚪ **N/A:** Neither eCat Online nor Sales Portal being implemented
- 🔴 **RED:** No site OR site disabled OR no web portal branding configured
- 🟡 **YELLOW:** Site exists but no logo (`document_logo_file_name` is null)
- 🟢 **GREEN:** Site enabled AND web portal branding configured AND logo uploaded

**Web Portal Branding Check (from Query 12):**
- `custom_cname` - Custom domain (e.g., "catalog.alfrescohome.com", "portal.accesslighting.com")
- `title` - Portal title/name (e.g., "Alfresco Home Catalog", "Access Lighting")
- `document_logo_file_name` - Logo file (if uploaded)
- At least ONE of `custom_cname` or `title` should be populated for proper branding

---

### Stage 9: eCat Online User Access (eCat Online / Sales Portal)

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Non-public user types exist | Query 15 (user_types) | User types (excluding public-access) count >= 1 |
| Non-admin users exist | Query 4 (org_users) | `non_admin_users >= 1` |
| Multiple user types | Query 15 (user_types) | Row count >= 2 |

**Pass Criteria:**
- ⚪ **N/A:** Neither eCat Online nor Sales Portal OR public site (Stage 8 sufficient)
- 🔴 **RED:** Closed site with no user types OR no non-admin users
- 🟡 **YELLOW:** Only 1 user type
- 🟢 **GREEN:** Multiple user types AND non-admin users exist

---

### Stage 10: eCat Online Ordering (eCat Online with B2B)

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Order email configured | Query 1 (organizations) | `order_email_recipient` is not null/empty |
| Order email on submit | Query 1 (organizations) | `send_order_email_on_submit = true` |

**Pass Criteria:**
- ⚪ **N/A:** B2B ordering not enabled (catalog-only)
- 🔴 **RED:** No order email recipient
- 🟡 **YELLOW:** Order email configured but `send_order_email_on_submit = false`
- 🟢 **GREEN:** Order email configured AND `send_order_email_on_submit = true`

---

### Stage 11: Sales Portal Configuration (Sales Portal Only)

| Check | Source | TRUE Condition |
|-------|--------|----------------|
| Portal enabled | Query 12 (mobile_sites) | `enable_sales_portal = true` |
| Territories configured | Query 9 (territories) | `territory_count >= 1` |
| Non-admin users exist | Query 4 (org_users) | `non_admin_users >= 1` |
| Multiple user types | Query 15 (user_types) | Row count >= 2 |

**Pass Criteria:**
- ⚪ **N/A:** Sales Portal not being implemented
- 🔴 **RED:** `enable_sales_portal = false` OR no territories OR no non-admin users
- 🟡 **YELLOW:** Only 1 user type
- 🟢 **GREEN:** `enable_sales_portal = true` AND territories exist AND multiple user types

---

## OUTPUT FORMAT

After collecting all data, output in this EXACT format for each client:

```markdown
---

## CLIENT: [SHORTNAME] ([Full Company Name])

**Data Collection Date:** [TODAY'S DATE]
**Days Active:** [calculated from created_at]
**Product(s):** [eCat iPad / eCat Online / Sales Portal]

### Stage Results

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 - Account Foundation | [🔴/🟡/🟢] | [specific metrics] |
| 2 - Catalog Setup | [🔴/🟡/🟢] | [X] products, [X] categories |
| 3 - Pricing Configuration | [🔴/🟡/🟢] | [X] price levels: [names] |
| 4 - Option Configuration | [🔴/🟡/🟢/⚪] | [X] options OR N/A |
| 5 - Customer & User Setup | [🔴/🟡/🟢] | [X] customers, [X] users |
| 6 - Operational Data | [🔴/🟡/🟢] | [import status, inventory status] |
| 7 - iPad Order-Ready | [🔴/🟡/🟢/⚪] | [orders, reports, iPad activity] |
| 8 - eCat Online Site | [🔴/🟡/🟢/⚪] | [site status] |
| 9 - eCat Online Access | [🔴/🟡/🟢/⚪] | [user types] |
| 10 - eCat Online Ordering | [🔴/🟡/🟢/⚪] | [order config] |
| 11 - Sales Portal | [🔴/🟡/🟢/⚪] | [portal status] |

### Raw Metrics

- **Products:** [X]
- **Products with Images:** [X]
- **Categories:** [X]
- **Collections:** [X]
- **Price Levels:** [X] ([names])
- **Options:** [X] records
- **Customers:** [X]
- **Users:** [X]
- **User Types:** [X] ([types])
- **Web Portal Configured:** [Yes/No] ([portal name if configured])
- **Territories:** [X]
- **Orders:** [X]
- **iPad Orders (MixPanel):** [X]
- **Report Formats:** [X]
- **Last Product Update:** [date] *(bonus indicator)*
- **Last Customer Update:** [date] *(bonus indicator)*
- **Last Inventory Update:** [date]
- **Import Errors (30 days):** [X]

### Current Stage & Readiness

- **Current Stage:** [X] - [Stage Name]
- **Stages Passed:** [X] / [Y]
- **Readiness:** [X]%

### Blockers Identified

1. [Specific blocker from stage checks]
2. [Specific blocker from stage checks]

---
```

---

## NEXT STEP

After completing data collection for ALL clients:

**Run:** `Validation_Layer_Fathom_HelpScout.md`

This will add qualitative validation (recent calls, support tickets, sentiment analysis) to the quantitative data collected here.

---

**Document Purpose:** Quantitative data collection only  
**No validation flags assigned here** - that happens in the Validation Layer  
**No Notion formatting here** - that happens in the Output Format document
