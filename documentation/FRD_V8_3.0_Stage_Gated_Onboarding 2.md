# FRD: Multi-Product Stage-Gated Onboarding Readiness Scoring

**Author:** Kylor Johnson  
**Date:** January 13, 2026  
**Version:** 3.0  
**Status:** Production Ready  
**Related Documents:** V8_Checklist_Version.md

---

## Document Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 2.0 | Jan 5, 2026 | Initial production version (eCat iPad only) | Kylor Johnson |
| 2.1 | Jan 6, 2026 | Revised Stage 7.1: iPad app vs web mobile sites | Kylor Johnson |
| 3.0 | Jan 13, 2026 | **Multi-Product Support:** Added Stage 8 (eCat Online), Stage 9 (Sales Portal), HubSpot product association, Fathom/Help Scout validation overlay, BigQuery Mixpanel iPad tracking | Kylor Johnson |

---

## Executive Summary

Replace SuperCat's existing 100-point onboarding scoring system with a **9-stage progressive framework** that supports the full SuperCat product suite:

- **eCat iPad** (Stages 1-7) - Field sales ordering app
- **eCat Online** (Stages 1-6 + 8) - B2B web catalog/ordering
- **Sales Portal** (Stages 1-6 + 9) - Sales analytics dashboard

**Key Innovations in V8 3.0:**
1. **Multi-product support** - Single framework covers all products with conditional logic
2. **HubSpot integration** - Product association drives which stages to run
3. **Two-layer validation** - MCP data + Fathom/Help Scout qualitative validation
4. **iPad activity tracking** - BigQuery Mixpanel queries for real device usage
5. **Comprehensive search requirements** - Detailed protocols for thorough validation

---

## Problem Statement

### Current Issues
- 100-point scoring system doesn't map to actual implementation workflow  
- No visibility into what's blocking a launch vs. "nice to have"  
- CS team lacks structured framework to guide multi-product clients  
- eCat Online and Sales Portal have no standardized onboarding criteria
- System data can pass validation while implementation is incomplete

### Business Impact
- Extended time-to-value for new clients  
- Higher support burden during onboarding  
- Risk of client churn when launches miss deadlines  
- False positives from data-only assessment (test data vs production)

---

## Proposed Solution

A **9-stage progressive framework** supporting all SuperCat products.

| Stage | Name | Core Focus | Applies To |
|-------|------|------------|------------|
| 1 | Account Foundation | Basic org setup | All |
| 2 | Catalog Setup | Products imported | All |
| 3 | Pricing Configuration | Products can be priced | All |
| 4 | Option Configuration | CPQ/options configured | All (conditional) |
| 5 | Customer & User Setup | Buyer/seller relationships | All |
| 6 | Operational Data | Real-time data flowing | All |
| 7 | eCat iPad Order-Ready | iPad app functional | eCat iPad |
| 8 | eCat Online Ready | B2B web portal functional | eCat Online |
| 9 | Sales Portal Ready | Analytics dashboard functional | Sales Portal |

### Two-Layer Validation Approach

| Layer | Source | Purpose |
|-------|--------|---------|
| **Layer 1** | MCP Endpoints (Stages 1-9) | Data-driven assessment - "What does the system say?" |
| **Layer 2** | Fathom + Help Scout | Contradiction detection - "What do conversations say?" |

---

## Product-Specific Stage Requirements

### Which Stages Apply to Which Products?

| Product | Associated Stages | Prerequisites |
|---------|------------------|---------------|
| **eCat iPad** | Stages 1-7 | None |
| **eCat Online** | Stages 1-6, **Stage 8** | Core platform (Stages 1-6) |
| **Sales Portal** | Stages 1-6, **Stage 9** | Core platform (Stages 1-6) |

### Stage Execution by Product Configuration

| HubSpot Products Selected | Stages to Run | Skip |
|---------------------------|---------------|------|
| eCat iPad only | 1-7 | 8, 9 |
| eCat iPad + eCat Online | 1-8 | 9 |
| eCat iPad + Sales Portal | 1-7, 9 | 8 |
| eCat iPad + eCat Online + Sales Portal | 1-9 | None |
| eCat Online only (no iPad) | 1-6, 8 | 7, 9 |
| Sales Portal only | 1-6, 9 | 7, 8 |
| eCat Online + Sales Portal (no iPad) | 1-6, 8, 9 | 7 |

---

## HubSpot Product Association

### How to Validate Products Purchased

Query BigQuery CRM Companies table:

```sql
SELECT 
  name,
  org_id,
  associated_product_s,
  lifecyclestage,
  status
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.crm_companies`
WHERE LOWER(name) LIKE LOWER('%{client_name}%')
   OR LOWER(org_id) = LOWER('{org_shortname}')
```

### Product Association Values Reference

| Product | Value in `associated_product_s` field | Stages to Run |
|---------|---------------------------------------|---------------|
| **eCat iPad** | `eCat (iPad) Service` OR `eCat (iPad) - Add'l Seats` | Stages 1-7 |
| **eCat Online** | `eCat Online - Catalog` OR `eCat Online - B2B Cart` OR `eCat Online - Closed Site` | Stages 1-6 + Stage 8 |
| **Sales Portal** | `eCat Online - Portal` | Stages 1-6 + Stage 9 |

### SQL Pattern Matching

```sql
-- Check if client has eCat iPad
WHERE associated_product_s LIKE '%eCat (iPad)%'

-- Check if client has eCat Online
WHERE associated_product_s LIKE '%eCat Online%'

-- Check if client has Sales Portal (specific)
WHERE associated_product_s LIKE '%eCat Online - Portal%'
```

---

## Critical Launch Blockers

### eCat iPad 🔴

| # | Blocker | Stage |
|---|---------|-------|
| 1 | No price levels configured | 3 |
| 2 | No customers imported | 5 |
| 3 | No iPad app logins | 7 |
| 4 | No report formats configured | 7 |
| 5 | No test order processed | 7 |

### eCat Online 🔴

| # | Blocker | Stage |
|---|---------|-------|
| 1 | No price levels configured | 3 |
| 2 | No customers imported | 5 |
| 3 | Mobile site disabled | 8 |
| 4 | Only 1 user group exists | 8 |
| 5 | No online users created | 8 |

### Sales Portal 🔴

| # | Blocker | Stage |
|---|---------|-------|
| 1 | Portal dashboard disabled | 9 |
| 2 | No order data uploaded | 9 |
| 3 | No invoice data uploaded | 9 |

---

## Color Threshold System

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| 🟢 Green | Production-ready | None - proceed to next stage |
| 🟡 Yellow | Launchable with minor issues | CS follow-up recommended |
| 🔴 Red | Blocker | Halt launch until resolved |
| ⚪ N/A | Not applicable | Feature disabled or product not purchased |
| ❓ Unknown | Investigate | Data source unavailable |

---

## Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 1.1 | Organization exists | `get_organization_info` | `status: "active"` |
| 1.2 | Company information complete | `company_information` | Name not null |
| 1.3 | Admin user exists | `get_org_users` | At least 1 user with `is_admin: true` (excluding Kylor_Johnson, brentsanders, cwiebe) |
| 1.4 | Settings initialized | `preferences` | Object exists with defaults |

### Thresholds

- 🔴 **Red:** Any required criterion fails
- 🟢 **Green:** All criteria pass

---

## Stage 2: Catalog Setup

**Goal:** Products imported and browsable by users

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 2.1 | Products imported | `get_data_summary` | `products.count >= 10` |
| 2.2 | Product images uploaded | `get_products` (sample) | At least 50% have images |
| 2.3 | Categories configured | `get_categories` | `count >= 1` |
| 2.4 | Collections exist | `get_collections` | `count >= 1` |
| 2.5 | Recent product update | `last_product_update` | Within 30 days |

### Thresholds

- 🔴 **Red:** Products < 10
- 🟡 **Yellow:** Products 10-100 OR no update in 60+ days OR < 50% have images
- 🟢 **Green:** Products > 100 AND recent update AND images present

---

## Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 3.1 | Price levels configured | `get_price_levels` | `count >= 1` |
| 3.2 | Multiple price levels | `get_price_levels` | `count >= 2` (recommended) |
| 3.3 | Descriptive names | `get_price_levels` | No "Price Level [0-9]" patterns |
| 3.4 | Codes assigned | `get_price_levels` | All levels have non-empty `code` |

### Thresholds

- 🔴 **Red:** No price levels configured
- 🟡 **Yellow:** Only 1 price level OR generic names
- 🟢 **Green:** 2+ price levels with descriptive names

---

## Stage 4: Option Configuration

**Goal:** If options enabled, CPQ/configurators are functional

### Conditional Logic

```python
options = get_options(org_shortname)
if options["total_count"] == 0:
    stage_4_status = "N/A"  # Skip - not applicable
else:
    validate_stage_4_criteria()
```

### Required Criteria (If Options Enabled)

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 4.1 | Options configured | `get_options` | `count >= 1` |
| 4.2 | Options have values | Sample validation | At least 80% have choice values |
| 4.3 | Option validation | Settings check | `require_valid_options_to_submit_orders` |

### Thresholds

- ⚪ **N/A:** Options disabled (skip stage)
- 🔴 **Red:** Options enabled but count = 0
- 🟡 **Yellow:** Options < 5 or incomplete data
- 🟢 **Green:** Options >= 5 with complete configuration

---

## Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 5.1 | Customers imported | `get_data_summary` | `customers.count >= 10` |
| 5.2 | Users configured | `get_org_users` | `count >= 2` |
| 5.3 | User types configured | `get_org_users` | Multiple distinct `user_type` values |
| 5.4 | Recent customer update | `last_customer_update` | Within 30 days |
| 5.5 | Assignment logic | `get_user_territories` | Validated based on model |

### Conditional Logic: Territory vs Direct Assignment

```python
territories = get_user_territories(org_shortname)
if territories["total_count"] > 0:
    # Territory-based model
    validate_territory_assignments()
else:
    # Direct assignment model
    validate_direct_customer_user_relationships()
```

### Thresholds

- 🔴 **Red:** Customers < 10 OR no users configured
- 🟡 **Yellow:** Customers 10-100 OR no recent update
- 🟢 **Green:** Customers > 100 AND recent update AND proper assignment

---

## Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 6.1 | Inventory tracking | `get_data_summary` | `inventories.count > 0` OR tracking disabled |
| 6.2 | Recent inventory update | `last_inventory_update` | Within 7 days (if enabled) |
| 6.3 | Smart stacks configured | `get_smart_stacks` | At least 1 OR feature disabled |
| 6.4 | Data import health | `get_import_events` | No critical errors in last 30 days |

### Conditional: Inventory Tracking

```python
if inventory_tracking_enabled:
    validate_inventory_data_exists()
    validate_recent_inventory_update()
else:
    stage_6_inventory_status = "N/A"
```

### Thresholds

- 🔴 **Red:** Inventory enabled but no data OR critical import errors
- 🟡 **Yellow:** Stale inventory (7+ days) OR minor import warnings
- 🟢 **Green:** Fresh data AND no import errors

---

## Stage 7: eCat iPad Order-Ready

**Goal:** iPad app can receive, process, and fulfill orders end-to-end

### ⚠️ Stage Applicability

**Only run if:** HubSpot `associated_product_s` contains `eCat (iPad)`

### Required Criteria

| # | Criterion | Data Source | Query | Pass Condition | Status |
|---|-----------|-------------|-------|----------------|--------|
| 7.1 | User types exist | MCP | `get_org_users` | > 1 unique `user_type` | 🔴 Blocker |
| 7.2 | iPad users logged in | BigQuery | Mixpanel query | `unique_ipad_users >= 1` | 🔴 Blocker |
| 7.3 | Report formats | MCP | `get_reports_config` | `count >= 3` | 🔴 Blocker |
| 7.4 | Test order exists | MCP | `get_orders` | `count >= 1` | 🔴 Blocker |
| 7.5 | Order email configured | MCP | `get_organization_info` | `order_email_recipient` not empty | 🟡 Recommended |
| 7.6 | Export type (if ERP) | MCP | `get_organization_info` | `export_type` not empty | 🟡 Conditional |
| 7.7 | Recent iPad activity | BigQuery | Mixpanel query | `days_since_last_login <= 30` | 🟡 Health |
| 7.8 | Recent orders | MCP | `get_data_summary` | `orders_last_30_days > 0` | 🟡 Health |

### BigQuery: iPad App Login Validation

```sql
-- Stage 7: iPad App Activity Validation
SELECT 
  currentorganizationshortname as org,
  COUNT(DISTINCT username) as unique_ipad_users,
  COUNT(*) as total_login_events,
  MAX(TIMESTAMP_SECONDS(CAST(time AS INT64))) as most_recent_login,
  DATE_DIFF(CURRENT_DATE(), DATE(MAX(TIMESTAMP_SECONDS(CAST(time AS INT64)))), DAY) as days_since_last_login
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.mixpanel_selected_org`
WHERE currentorganizationshortname = '{org_shortname}'
  AND _model LIKE 'iPad%'  -- Only iPad devices
  AND username IS NOT NULL
GROUP BY currentorganizationshortname
```

### iPad Login Thresholds

- 🔴 **Red:** `unique_ipad_users = 0` (no iPad logins)
- 🟡 **Yellow:** `unique_ipad_users >= 1` BUT `days_since_last_login > 30`
- 🟢 **Green:** `unique_ipad_users >= 1` AND `days_since_last_login <= 30`

---

## Stage 8: eCat Online (B2B Web Portal)

**Goal:** Web-based B2B catalog is accessible and customers can browse/order online

### ⚠️ Stage Applicability

**Only run if:** HubSpot `associated_product_s` contains `eCat Online`

### Prerequisites

- Stages 1-6 must be GREEN (shared platform foundation complete)

### Shared Foundation from Stages 1-6

| Stage | What Carries Over | Why It Matters |
|-------|-------------------|----------------|
| 1 | Organization identity, admin users | Same org, same admins manage eOL |
| 2 | Product catalog, images, categories | eOL displays the same products |
| 3 | Price levels, pricing structure | Prices shown to online buyers |
| 4 | Product options/configurators | CPQ works in web interface |
| 5 | Customer accounts, user types | Online users link to customer records |
| 6 | Inventory data, real-time feeds | Stock availability shown online |

### Required Criteria

| # | Criterion | MCP Query | Pass Condition | Status |
|---|-----------|-----------|----------------|--------|
| 8.1 | Mobile site enabled | `get_mobile_sites` | At least 1 with `enabled: true` | 🔴 Blocker |
| 8.2 | Multiple user groups | `get_org_users` | > 1 distinct `user_type` values | 🔴 Blocker |
| 8.3 | Online user created | `get_org_users` | At least 1 non-admin, non-rep user | 🔴 Blocker |
| 8.4 | Enrollment recipients | `get_organization_settings` | `enrollment_email_recipients` not empty | 🟡 Recommended |
| 8.5 | Custom CNAME | `get_mobile_sites` | `sites_with_custom_domains > 0` | ⚪ Optional |
| 8.6 | Custom theming | `get_mobile_sites` | `sites_with_theming > 0` | ⚪ Optional |
| 8.7 | Enrollment enabled | `get_organization_settings` | `enrollment_enabled = true` | ⚪ Optional |

### Thresholds

- 🔴 **Red:** Mobile site disabled OR only 1 user group OR no online users
- 🟡 **Yellow:** All blockers pass but enrollment recipients not configured
- 🟢 **Green:** All critical + recommended criteria pass

**Note:** Web order validation removed - order source (iPad vs web) cannot be reliably distinguished. Stage 7 test order validates shared ordering workflow.

---

## Stage 9: Sales Portal (Analytics Dashboard)

**Goal:** Sales analytics portal is configured with data and accessible to authorized users

### ⚠️ Stage Applicability

**Only run if:** HubSpot `associated_product_s` contains `eCat Online - Portal`

### Prerequisites

- Stages 1-6 must be GREEN
- eCat Online (Stage 8) recommended but not required

### Shared Foundation from Stages 1-6

| Stage | What Carries Over | Why It Matters |
|-------|-------------------|----------------|
| 1 | Organization identity | Portal branded to company |
| 5 | User permissions, territories | Controls who sees what data |
| 6 | Data import infrastructure | Same process handles portal data |

### Required Criteria

| # | Criterion | Data Source | Pass Condition | Status |
|---|-----------|-------------|----------------|--------|
| 9.1 | Portal enabled | `get_organization_settings` | `flags.enable_portal_dashboard = true` | 🔴 Blocker |
| 9.2 | Order data uploaded | Manual check | Order data visible in portal admin | 🔴 Blocker |
| 9.3 | Invoice data uploaded | Manual check | Invoice data visible in portal admin | 🔴 Blocker |
| 9.4 | ERP verification | Manual check | Client confirms data accuracy | 🟡 Recommended |
| 9.5 | Permissions configured | `get_user_territories` / `get_org_users` | Territory codes or user groups set | 🟡 Recommended |
| 9.6 | Currency configured | `get_organization_settings` | `sales_portal_currency_code` set | 🟡 Recommended |

### Thresholds

- 🔴 **Red:** Portal disabled OR no order data OR no invoice data
- 🟡 **Yellow:** All blockers pass but ERP verification incomplete OR no permissions
- 🟢 **Green:** All criteria pass AND data verified accurate

---

# Validation Overlay: Fathom + Help Scout

## Overview

The stage-gated assessment provides **quantitative data** from system endpoints. However, **system state ≠ implementation reality**. Data may exist because:

- Someone tested a feature but hasn't loaded production data
- Test configurations were never cleaned up
- Imports ran but the client hasn't verified accuracy

The Validation Overlay cross-references qualitative sources to flag contradictions.

## ⚠️ CRITICAL: Evidence-Based Validation

**Every validation flag MUST include the actual quote/sentiment from the source.**

DO NOT simply say "flagged" or "issue detected." ALWAYS include:
- The **exact quote** from Fathom transcript/summary
- The **ticket excerpt** from Help Scout
- The **date** the evidence was captured
- The **source** (which call or ticket number)

### ❌ BAD Example (Do Not Do This)
```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | 🔴 CONTRADICT | Help Scout | Customer data issue flagged |
```

### ✅ GOOD Example (Required Format)
```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | 🔴 CONTRADICT | Help Scout #12345 (Jan 10) | *"Customer data requires re-import. A script clobbered customer-specific price levels (e.g., DSFOB C6) with default (Z3T1)."* |
```

---

## Flag Types

| Flag | Icon | Meaning | Action |
|------|------|---------|--------|
| **CONTRADICT** | 🔴 | Evidence directly contradicts system data | Block until resolved |
| **REVIEW** | ⚠️ | Needs clarification from CSM/client | Add to standup agenda |
| **TIMELINE** | ⏰ | Date/target has changed | Update project timeline |
| **ACTIVITY** | 📭 | Zero engagement signals | Outreach to confirm status |
| **PENDING** | ⏳ | Fathom call found but transcript unavailable | Retry in 24 hours |
| **CONFIRMED** | ✅ | Qualitative sources validate system data | No action needed |

---

## Fathom API Search Protocol

### ⚠️ CRITICAL: DO NOT BE LAZY

Every Fathom search MUST be exhaustive. Missing relevant calls leads to false assessments.

### Required Search Passes (Run ALL)

| Pass # | Search Location | What to Search For |
|--------|-----------------|-------------------|
| 1 | Call Titles | Full client name (e.g., "Kuzco Lighting") |
| 2 | Call Titles | Client shortname (e.g., "kll", "KLL") |
| 3 | Call Titles | Partial name matches (e.g., "Kuzco") |
| 4 | Call Summaries | Full client name |
| 5 | Call Summaries | Client shortname |
| 6 | Call Summaries | Product keywords ("eCat Online", "Sales Portal") |
| 7 | Call Transcripts | Full client name |
| 8 | Call Transcripts | Client shortname |
| 9 | Call Transcripts | Product keywords |
| 10 | All locations | **Email domain** (e.g., "@kuzcolighting.com") |

### Fathom Search Implementation

```python
import requests
import time

FATHOM_API_KEY = "your_api_key"
BASE_URL = "https://fathom.video/api"

def comprehensive_fathom_search(client_name, shortname, email_domain):
    """
    Perform exhaustive Fathom search for a client.
    DO NOT skip any search passes.
    """
    all_meetings = []
    
    # Define all search terms
    search_terms = [
        client_name,           # Full name
        shortname,             # Shortname (lowercase)
        shortname.upper(),     # Shortname (uppercase)
        client_name.split()[0] if ' ' in client_name else client_name,  # First word
        email_domain,          # Email domain
    ]
    
    # Product keywords for eCat Online / Sales Portal
    product_keywords = [
        "eCat Online", "eOL", "B2B", "online catalog",
        "Sales Portal", "portal", "dashboard", "analytics"
    ]
    
    # Search all pages of meetings
    for term in search_terms + product_keywords:
        page = 1
        while True:
            response = search_meetings(term, page)
            if not response.get('meetings'):
                break
            all_meetings.extend(response['meetings'])
            page += 1
            time.sleep(0.5)  # Rate limiting
    
    # Deduplicate by meeting ID
    unique_meetings = {m['id']: m for m in all_meetings}
    return list(unique_meetings.values())

def search_meetings(query, page=1):
    """Search Fathom API for meetings matching query."""
    headers = {"Authorization": f"Bearer {FATHOM_API_KEY}"}
    params = {"query": query, "page": page}
    response = requests.get(f"{BASE_URL}/meetings", headers=headers, params=params)
    return response.json()
```

### ⚠️ Troubleshooting: Meetings Without IDs

**Known Issue:** The Fathom API may return meetings with `id: None`. This happens when:
- The meeting was recently recorded and hasn't fully processed
- The meeting is a calendar hold without a recording
- API sync delays (especially for same-day calls)

**When this happens:**

1. **Document the gap** - Note that Fathom calls exist but transcripts unavailable
2. **Flag for manual review** - Add `⏳ PENDING` flag indicating validation incomplete
3. **Retry later** - Same-day calls may take 1-24 hours to process with IDs
4. **Use title/date as context** - Even without transcript, note the meeting occurred

```markdown
### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 7 | ⏳ PENDING | Fathom | Meeting found: "eCat x Coaster Standup" (Jan 14) - transcript unavailable, retry in 24 hours |
```

### Required: Include Actual Quotes

**When Fathom data IS available, you MUST quote directly:**

```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 3 | ⚠️ REVIEW | Fathom (Dec 3 call) | *"Use eCat's Contract Pricing feature for all pricing."* - May not align with 19 standard price levels in system |
| 7 | 🔴 CONTRADICT | Fathom (Jan 6 call) | *"Customer data requires re-import. A script clobbered customer-specific price levels."* |
```

### Stage 8 Fathom Keywords

Search for these terms in call titles/summaries/transcripts:

- `eCat Online`, `eOL`, `online catalog`, `B2B`
- `mobile site`, `web portal`, `enrollment`
- `user group`, `customer login`, `trade tier`
- `CNAME`, `custom domain`, `branding`

### Stage 9 Fathom Keywords

Search for these terms in call titles/summaries/transcripts:

- `Sales Portal`, `portal`, `dashboard`, `analytics`
- `order data`, `invoice data`, `CSV upload`
- `ERP`, `data match`, `verification`
- `territory permissions`, `user access`

---

## Help Scout Search Protocol (BigQuery)

### ⚠️ CRITICAL: Search BOTH Inboxes

Always query both Support AND Onboarding/Implementation inboxes.

### Required Query Structure

```sql
-- Help Scout: Comprehensive ticket search for eCat Online & Sales Portal
SELECT DISTINCT
  ticket_number,
  ticket_subject,
  ticket_status,
  mailbox_name,  -- Check BOTH inboxes
  conv_customer_organization as client,
  DATE(ticket_created_at) as created_date,
  ticket_preview,  -- Include preview for quick context
  LEFT(thread_body, 500) as thread_excerpt  -- MUST include excerpt for quotes
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  -- Client identification (use multiple methods)
  (
    LOWER(conv_customer_organization) LIKE LOWER('%{client_name}%')
    OR LOWER(ticket_subject) LIKE LOWER('%{client_name}%')
    OR LOWER(ticket_subject) LIKE LOWER('%{shortname}%')
    OR LOWER(thread_body) LIKE LOWER('%{client_name}%')
    OR LOWER(thread_body) LIKE LOWER('%{shortname}%')
  )
  -- Include ALL ticket statuses
  AND ticket_status IN ('active', 'pending', 'closed', 'spam')
  -- Product-specific keywords (REMOVE this filter for general client search)
  AND (
    LOWER(ticket_subject) LIKE '%online%'
    OR LOWER(ticket_subject) LIKE '%portal%'
    OR LOWER(ticket_subject) LIKE '%enrollment%'
    OR LOWER(ticket_subject) LIKE '%b2b%'
    OR LOWER(thread_body) LIKE '%ecat online%'
    OR LOWER(thread_body) LIKE '%sales portal%'
    OR LOWER(thread_body) LIKE '%enrollment%'
    OR LOWER(thread_body) LIKE '%mobile site%'
  )
ORDER BY ticket_created_at DESC
LIMIT 100
```

### ⚠️ CRITICAL: Active Tickets Require Special Attention

**If ANY active or pending tickets exist for a client, they MUST be:**

1. **Included in the assessment** - Never skip active tickets
2. **Quoted with context** - Include the relevant excerpt from `ticket_preview` or `thread_body`
3. **Flagged appropriately** - Active tickets often indicate ongoing blockers or coordination

### General Client Search (No Product Filter)

**For comprehensive validation, ALSO run a search without product keywords:**

```sql
-- Help Scout: ALL tickets for a client (regardless of topic)
SELECT DISTINCT
  ticket_number,
  ticket_subject,
  ticket_status,
  mailbox_name,
  DATE(ticket_created_at) as created_date,
  ticket_preview
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  LOWER(conv_customer_organization) LIKE LOWER('%{client_name}%')
  OR LOWER(ticket_subject) LIKE LOWER('%{client_name}%')
  OR LOWER(conv_creator_email) LIKE LOWER('%{email_domain}%')
ORDER BY ticket_created_at DESC
LIMIT 50
```

### Required: Include Ticket Excerpts in Flags

**Every Help Scout validation flag MUST include actual ticket content:**

```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | 🔴 ACTIVE | Help Scout (Nov 17) | Subject: "Re: Terracotta Onboarding Kickoff Follow Ups" - *"I'd love the opportunity to meet and speak with you in person at Dallas Market, showroom #3751..."* - Indicates ongoing coordination needed |
```

**DO NOT do this:**
```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | ⚠️ REVIEW | Help Scout | Active ticket exists |
```

### Stage 8 Help Scout Keywords

```sql
-- eCat Online specific tickets
WHERE 
  LOWER(ticket_subject) LIKE '%online%'
  OR LOWER(ticket_subject) LIKE '%b2b%'
  OR LOWER(ticket_subject) LIKE '%enrollment%'
  OR LOWER(ticket_subject) LIKE '%mobile site%'
  OR LOWER(thread_body) LIKE '%ecat online%'
  OR LOWER(thread_body) LIKE '%user group%'
  OR LOWER(thread_body) LIKE '%customer login%'
```

### Stage 9 Help Scout Keywords

```sql
-- Sales Portal specific tickets
WHERE 
  LOWER(ticket_subject) LIKE '%portal%'
  OR LOWER(ticket_subject) LIKE '%dashboard%'
  OR LOWER(ticket_subject) LIKE '%analytics%'
  OR LOWER(thread_body) LIKE '%sales portal%'
  OR LOWER(thread_body) LIKE '%order data%'
  OR LOWER(thread_body) LIKE '%invoice%'
  OR LOWER(thread_body) LIKE '%csv%'
```

---

## Validation Workflow

### Step 1: Run Data-Driven Assessment (MCP)

```python
def run_stage_assessment(org_shortname):
    """Layer 1: MCP data-driven assessment"""
    results = {}
    
    # Determine products from HubSpot
    products = get_hubspot_products(org_shortname)
    
    # Always run Stages 1-6
    for stage in range(1, 7):
        results[stage] = validate_stage(org_shortname, stage)
    
    # Conditional stages based on products
    if 'eCat iPad' in products:
        results[7] = validate_stage_7(org_shortname)
    
    if 'eCat Online' in products:
        results[8] = validate_stage_8(org_shortname)
    
    if 'Sales Portal' in products:
        results[9] = validate_stage_9(org_shortname)
    
    return results
```

### Step 2: Query Fathom for Qualitative Data

```python
def get_fathom_context(client_name, shortname, email_domain):
    """Layer 2a: Fathom qualitative validation"""
    meetings = comprehensive_fathom_search(client_name, shortname, email_domain)
    
    flags = []
    for meeting in meetings:
        summary = get_meeting_summary(meeting['id'])
        transcript = get_meeting_transcript(meeting['id'])
        
        # Check for contradiction patterns
        flags.extend(analyze_for_contradictions(summary, transcript))
    
    return flags
```

### Step 3: Query Help Scout for Support Context

```python
def get_helpscout_context(client_name, shortname):
    """Layer 2b: Help Scout qualitative validation"""
    query = build_helpscout_query(client_name, shortname)
    tickets = execute_bigquery(query)
    
    flags = []
    for ticket in tickets:
        flags.extend(analyze_ticket_for_issues(ticket))
    
    return flags
```

### Step 4: Compile Final Assessment

```python
def compile_assessment(org_shortname, client_name, shortname, email_domain):
    """Combine Layer 1 and Layer 2 into final assessment"""
    
    # Layer 1: Data
    data_results = run_stage_assessment(org_shortname)
    
    # Layer 2: Qualitative
    fathom_flags = get_fathom_context(client_name, shortname, email_domain)
    helpscout_flags = get_helpscout_context(client_name, shortname)
    
    # Combine and flag contradictions
    final_results = {
        'stages': data_results,
        'validation_flags': fathom_flags + helpscout_flags,
        'overall_status': calculate_overall_status(data_results, fathom_flags, helpscout_flags)
    }
    
    return final_results
```

---

## Example Validation Output

```markdown
# Client Assessment: Kuzco Lighting (kll)

## V8 Stage Assessment: January 13, 2026

### Products Purchased
- ✅ eCat iPad
- ✅ eCat Online
- ✅ Sales Portal
→ Running Stages 1-9 (Full Assessment)

### Stage Summary

| Stage | Status | Key Finding |
|-------|--------|-------------|
| 1 | 🟢 | Account foundation complete |
| 2 | 🟢 | 6,271 products, 28 collections |
| 3 | 🟢 | 8 price levels configured |
| 4 | ⚪ N/A | Options not enabled |
| 5 | 🟢 | 2,673 customers, 782 users |
| 6 | 🟢 | Inventory fresh, no import errors |
| 7 | 🟢 | 15 iPad users, 66 orders (30d) |
| 8 | 🟢 | Mobile site enabled, 10 user groups |
| 9 | 🟡 | Portal enabled, ERP verification pending |

### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 9 | ⚠️ REVIEW | Fathom Jan 10 | "Need to verify invoice numbers match ERP" |

### Overall Status: 🟡 YELLOW (Launchable with CS follow-up)

**Next Action:** Confirm ERP data verification with client before Sales Portal launch.
```

---

## MCP Endpoints Reference

| Endpoint | Used In Stages | Primary Purpose |
|----------|----------------|-----------------|
| `get_organization_info` | 1, 7, 8, 9 | Org settings, flags, emails |
| `get_organization_settings` | 8, 9 | Enrollment, portal flags |
| `get_org_users` | 1, 5, 7, 8, 9 | User counts, types, permissions |
| `get_data_summary` | 2, 5, 6, 7 | Counts, last update dates |
| `get_products` | 2 | Product details, images |
| `get_categories` | 2 | Category structure |
| `get_collections` | 2 | Collection structure |
| `get_price_levels` | 3 | Pricing configuration |
| `get_options` | 4 | CPQ/configurator options |
| `get_customers` | 5 | Customer data |
| `get_user_territories` | 5, 9 | Territory assignments |
| `get_inventories` | 6 | Stock levels |
| `get_import_events` | 6 | Import history/errors |
| `get_smart_stacks` | 6 | Smart stack config |
| `get_mobile_sites` | 8 | Web portal configuration |
| `get_reports_config` | 7 | Report formats |
| `get_orders` | 7 | Order history |

## BigQuery Tables Reference

| Table | Used In Stages | Primary Purpose |
|-------|----------------|-----------------|
| `crm_companies` | Pre-assessment | HubSpot product association |
| `mixpanel_selected_org` | 7 | iPad app login tracking |
| `help_scout_tickets` | Validation | Support ticket history |

---

## Approvals

| Role | Name | Date | Status |
|------|------|------|--------|
| **Author** | Kylor Johnson | Jan 13, 2026 | ✅ Complete |
| **CS Lead** | [Name] | [Date] | ⏳ Pending |
| **Engineering Lead** | [Name] | [Date] | ⏳ Pending |
| **Product Manager** | [Name] | [Date] | ⏳ Pending |

---

**Document Status:** Ready for Review  
**Version:** 3.0  
**Last Updated:** January 13, 2026  
**Contact:** Kylor Johnson
