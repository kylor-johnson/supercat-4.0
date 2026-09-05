# V8

# Multi-Product Stage-Gated Onboarding Readiness Framework

## Overview

This framework tracks client progression through **up to 9 sequential stages**, from initial account setup through full product suite deployment. Each stage has specific validation checkpoints that determine readiness (🟢 GREEN), warnings (🟡 YELLOW), blockers (🔴 RED), or not applicable (⚪ N/A).

### What's New in V8

V8 extends the original 7-stage iPad-focused model to support the full SuperCat product suite:
- **Stages 1-6:** Shared platform foundation (applies to ALL products)
- **Stage 7:** eCat iPad Order-Ready
- **Stage 8:** eCat Online (B2B Web Catalog)
- **Stage 9:** Sales Portal (Sales Analytics Dashboard)

---

## Product-Specific Stage Requirements

### Which Stages Apply to Which Products?

| Product | Associated Stages | Prerequisites |
|---------|------------------|---------------|
| **eCat iPad** | Stages 1-7 | None |
| **eCat Online** | Stages 1-6, **Stage 8** | Core platform (Stages 1-6) |
| **Sales Portal** | Stages 1-6, **Stage 9** | Core platform (Stages 1-6) + eCat Online recommended |

### Stage Execution Logic

Before running this assessment, check the client's **HubSpot "Associated Product(s)"** field:

```
IF "eCat iPad" AND "eCat Online" AND "eCat Sales Portal" are checked:
    → Run Stages 1-9 (Full Assessment)
    
IF "eCat iPad" AND "eCat Online" are checked (no Sales Portal):
    → Run Stages 1-8 (Skip Stage 9)
    
IF only "eCat iPad" is checked:
    → Run Stages 1-7 (Original V6 Model)
    
IF only "eCat Online" is checked (no iPad):
    → Run Stages 1-6 + Stage 8 (Skip Stage 7)
    
IF only "eCat Sales Portal" is checked:
    → Run Stages 1-6 + Stage 9 (Skip Stages 7-8)
```

### How to Validate HubSpot Product Association

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

#### Product Association Values Reference

| Product | Value in `associated_product_s` field | Stages to Run |
|---------|---------------------------------------|---------------|
| **eCat iPad** | `eCat (iPad) Service` OR `eCat (iPad) - Add'l Seats` | Stages 1-7 |
| **eCat Online** | `eCat Online - Catalog` OR `eCat Online - B2B Cart` OR `eCat Online - Closed Site` | Stages 1-6 + Stage 8 |
| **Sales Portal** | `eCat Online - Portal` | Stages 1-6 + Stage 9 |

**Note:** The `associated_product_s` field contains semicolon-separated values. Use SQL `LIKE` to check for presence:
```sql
-- Check if client has eCat Online
WHERE associated_product_s LIKE '%eCat Online%'

-- Check if client has Sales Portal
WHERE associated_product_s LIKE '%eCat Online - Portal%'

-- Check if client has eCat iPad
WHERE associated_product_s LIKE '%eCat (iPad)%'
```

---

## Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

### Checklist

- [ ] Company name filled in
- [ ] At least 1 admin user exists (excluding internal test users: Kylor_Johnson, brentsanders, cwiebe)
- [ ] Settings initialized with defaults

### Pass Criteria

- **🔴 RED (BLOCKER):** Any item above unchecked
- **🟢 GREEN (READY):** All items checked

### How to Validate

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 1.1 | Company name filled in | `get_organization_info` | `company_information.name` not null |
| 1.2 | Admin user exists | `get_org_users` | At least 1 user with `is_admin: true` (excluding Kylor_Johnson, brentsanders, cwiebe) |
| 1.3 | Settings initialized | `get_organization_info` | `preferences` object exists with defaults |

---

## Stage 2: Catalog Setup

**Goal:** Products imported and browsable by users

### Checklist

- [ ] At least 10 products imported
- [ ] At least 10 products have images
- [ ] At least 1 category configured
- [ ] At least 1 collection exists
- [ ] Products updated within last 30 days

### Pass Criteria

- **🔴 RED (BLOCKER):** Less than 10 products imported
- **🟡 YELLOW (WARNING):** 10-100 products OR no updates in 60+ days OR less than 10 products with images
- **🟢 GREEN (READY):** 100+ products AND updated within last 30 days

### How to Validate

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 2.1 | Products imported | `get_data_summary` | `products.count` >= 10 |
| 2.2 | Products have images | `get_products` | Sample check: images array not empty |
| 2.3 | Category configured | `get_categories` | `count` >= 1 |
| 2.4 | Collection exists | `get_collections` | `count` >= 1 |
| 2.5 | Recent update | `get_data_summary` | `last_product_update` within 30 days |

---

## Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

### Checklist

- [ ] Price levels configured
- [ ] At least 2 price levels configured (recommended)
- [ ] Price levels have descriptive names, not generic defaults like "Price Level 1" (recommended)
- [ ] Price level codes assigned (recommended)

### Pass Criteria

- **🔴 RED (BLOCKER):** No price levels configured
- **🟡 YELLOW (WARNING):** Only 1 price level configured OR generic names like "Price Level 1" OR missing/duplicate codes
- **🟢 GREEN (READY):** 2+ price levels with descriptive names (e.g., "Dealer Net", "Wholesale", "Retail") AND unique codes assigned

### How to Validate

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 3.1 | Price levels exist | `get_price_levels` | `count` >= 1 |
| 3.2 | Multiple levels | `get_price_levels` | `count` >= 2 |
| 3.3 | Descriptive names | `get_price_levels` | No names matching "Price Level [0-9]" pattern |
| 3.4 | Codes assigned | `get_price_levels` | All levels have non-empty `code` field |

---

## Stage 4: Option Configuration

**Goal:** If options enabled, CPQ/configurators are functional

### Check if Stage Applies

- [ ] Run `get_options` - does it return any options?
    - **YES** → Continue with checklist below
    - **NO** → Mark stage as **⚪ N/A** and skip to Stage 5

### Checklist (If Options Enabled)

- [ ] At least 1 option configured

### Pass Criteria

- **⚪ N/A:** Options disabled - skip this stage
- **🔴 RED (BLOCKER):** Options enabled but none configured
- **🟡 YELLOW (WARNING):** Less than 5 options configured
- **🟢 GREEN (READY):** 5+ options configured

### How to Validate

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 4.1 | Options enabled | `get_options` | Returns data (not empty) |
| 4.2 | Options configured | `get_options` | `count` >= 1 |
| 4.3 | Sufficient options | `get_options` | `count` >= 5 |
| 4.4 | Valid options required | `get_organization_settings` | Check `require_valid_options_to_submit_orders` |

---

## Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

### Check Assignment Model

- [ ] Run `get_user_territories` - are territories configured?
    - **YES** → Use Territory Model checklist
    - **NO** → Use Direct Assignment checklist

### Checklist (Both Models)

- [ ] At least 10 customers imported
- [ ] At least 2 users configured
- [ ] Multiple user types exist
- [ ] Customers updated within last 30 days

### Additional Checklist: Territory Model

- [ ] At least 1 territory exists
- [ ] Users assigned to territories (via `territory_codes`)
- [ ] Customers assigned to territories or users within territories

### Additional Checklist: Direct Assignment Model

- [ ] Customers directly assigned to users
- [ ] No territory structure required

### Pass Criteria

- **🔴 RED (BLOCKER):** Less than 10 customers OR no users configured
- **🟡 YELLOW (WARNING):** 10-100 customers OR no updates in 30+ days
- **🟢 GREEN (READY):** 100+ customers AND updated within last 30 days AND proper assignments configured

### How to Validate

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 5.1 | Customers imported | `get_data_summary` | `customers.count` >= 10 |
| 5.2 | Users configured | `get_org_users` | `count` >= 2 |
| 5.3 | Multiple user types | `get_org_users` | More than 1 unique `user_type` value |
| 5.4 | Recent update | `get_data_summary` | `last_customer_update` within 30 days |
| 5.5 | Territories (if used) | `get_user_territories` | At least 1 territory with user assignments |

---

## Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

### Check if Inventory Tracking Applies

- [ ] Is inventory tracking enabled?
    - **YES** → Include inventory validation checks
    - **NO** → Skip inventory checks (mark **⚪ N/A**)

### Checklist (Always Required)

- [ ] No critical import errors in last 30 days
- [ ] Smart stacks configured OR feature disabled

### Additional Checklist: If Inventory Enabled

- [ ] Inventory data exists (`inventories.count > 0`)
- [ ] Inventory updated within last 7 days

### Pass Criteria

- **🔴 RED (BLOCKER):** Inventory enabled but no data OR critical import errors present
- **🟡 YELLOW (WARNING):** Stale inventory (7+ days old) OR minor import warnings
- **🟢 GREEN (READY):** Fresh data (updated within 7 days) AND no import errors

### How to Validate

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 6.1 | Inventory exists | `get_data_summary` | `inventories.count` > 0 |
| 6.2 | Inventory fresh | `get_data_summary` | `last_inventory_update` within 7 days |
| 6.3 | No import errors | `get_import_events` | No `error` status in last 30 days |
| 6.4 | Smart stacks | `get_smart_stacks` | Configured OR explicitly disabled |

---

## Stage 7: eCat iPad Order-Ready

**Goal:** iPad app can receive, process, and fulfill orders end-to-end

### ⚠️ Stage Applicability

**Only run this stage if:** HubSpot "Associated Product(s)" includes **"eCat iPad"**

### Critical Blockers (Must Pass)

- [ ] 1+ user types exist (more than just Default User Group - e.g., Sales Rep or Customer)
- [ ] At least 1 user has logged into eCat iPad app (via iPad device)
- [ ] Report formats configured (minimum 3 required)
- [ ] Test order processed (at least 1 order exists)

### Recommended (Should Pass)

- [ ] Order notification email configured
- [ ] Export type configured (if ERP integration needed)
- [ ] Multiple users actively using iPad app

### Post-Launch Health Check

- [ ] iPad app logins within last 30 days (after launch)
- [ ] Orders placed within last 30 days (after launch)

### Pass Criteria

- **🔴 RED (BLOCKER):** Any critical blocker unchecked
- **🟡 YELLOW (WARNING):** All critical blockers pass but recommended items missing OR no recent iPad activity
- **🟢 GREEN (READY):** All criteria pass AND recent iPad activity + orders

### How to Validate

| # | Criterion | Data Source | Query/Check | Pass Condition |
|---|-----------|-------------|-------------|----------------|
| 7.1 | User types exist | MCP | `get_org_users` | More than 1 unique `user_type` value |
| 7.2 | iPad users logged in | BigQuery (Mixpanel) | See SQL below | `unique_ipad_users` >= 1 |
| 7.3 | Report formats | MCP | `get_reports_config` | `count` >= 3 |
| 7.4 | Test order exists | MCP | `get_orders` | `count` >= 1 |
| 7.5 | Order email configured | MCP | `get_organization_info` | `order_email_recipient` not empty |
| 7.6 | Export type (if needed) | MCP | `get_organization_info` | `export_type` not empty |
| 7.7 | Recent iPad activity | BigQuery (Mixpanel) | See SQL below | `days_since_last_login` <= 30 |
| 7.8 | Recent orders | MCP | `get_data_summary` | `orders_last_30_days` > 0 |

### BigQuery: Check iPad App Logins

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

**Pass Criteria for iPad Logins:**
- **🔴 RED (BLOCKER):** `unique_ipad_users` = 0 (no one has logged into iPad app)
- **🟡 YELLOW (WARNING):** `unique_ipad_users` >= 1 BUT `days_since_last_login` > 30
- **🟢 GREEN (READY):** `unique_ipad_users` >= 1 AND `days_since_last_login` <= 30

---

# Extended Product Stages

## Crossover: Shared Platform Foundation

Before proceeding to Stages 8 and 9, understand how the core platform (Stages 1-6) supports eCat Online and Sales Portal:

### What eCat Online Inherits from Stages 1-6

| Stage | What Carries Over to eCat Online | Why It Matters |
|-------|----------------------------------|----------------|
| **Stage 1** | Organization identity, admin users | Same org, same admins manage eOL |
| **Stage 2** | Product catalog, images, categories | eOL displays the same products |
| **Stage 3** | Price levels, pricing structure | Prices shown to online buyers |
| **Stage 4** | Product options/configurators | CPQ works in web interface |
| **Stage 5** | Customer accounts, user types | Online users link to customer records |
| **Stage 6** | Inventory data, real-time feeds | Stock availability shown online |

### What Sales Portal Inherits from Stages 1-6

| Stage | What Carries Over to Sales Portal | Why It Matters |
|-------|-----------------------------------|----------------|
| **Stage 1** | Organization identity | Portal branded to company |
| **Stage 5** | User permissions, territories | Controls who sees what data |
| **Stage 6** | Data import infrastructure | Same import process handles portal data |

### Key Insight

**If Stages 1-6 pass for eCat iPad, most of the work for eCat Online is already done.** Stage 8 focuses only on the web-specific configuration required to make the online portal functional.

---

## Stage 8: eCat Online (B2B Web Portal)

**Goal:** Web-based B2B catalog is accessible and customers can browse/order online

### ⚠️ Stage Applicability

**Only run this stage if:** HubSpot "Associated Product(s)" includes **"eCat Online"**

### Prerequisites

- [ ] Stages 1-6 must be GREEN (shared platform foundation complete)

### Critical Blockers (Must Pass)

- [ ] Mobile site enabled (at least 1 with `enabled: true`)
- [ ] More than 1 user group exists (indicates customer/buyer user types configured)
- [ ] At least 1 customer/online user created (can log in and access site)

### Recommended (Should Pass)

- [ ] Enrollment email recipients configured (to receive new user requests)

### Optional (Nice-to-Have)

- [ ] Custom CNAME configured (branded URL like catalog.company.com)
- [ ] Custom theming applied (colors, logo, branding)
- [ ] Enrollment workflow enabled (self-service registration)

### Pass Criteria

- **🔴 RED (BLOCKER):** Mobile site disabled OR only 1 user group exists OR no online users created
- **🟡 YELLOW (WARNING):** All blockers pass but enrollment recipients not configured
- **🟢 GREEN (READY):** All critical + recommended criteria pass

### How to Validate

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 8.1 | Mobile site enabled | `get_mobile_sites` | At least 1 site with `enabled: true` |
| 8.2 | Multiple user groups | `get_org_users` | More than 1 distinct `user_type` exists (e.g., "Sales Rep" + "Customers" OR "Trade Gold" + "Trade Silver") |
| 8.3 | Online user created | `get_org_users` | At least 1 non-admin, non-rep user exists |
| 8.4 | Enrollment recipients | `get_organization_settings` | `enrollment_email_recipients` array not empty |
| 8.5 | Custom CNAME | `get_mobile_sites` | `sites_with_custom_domains` > 0 |
| 8.6 | Custom theming | `get_mobile_sites` | `sites_with_theming` > 0 |
| 8.7 | Enrollment enabled | `get_organization_settings` | `enrollment_enabled` = `true` |

**Note:** Web order validation removed - order source (iPad vs web) cannot be reliably distinguished in the current data model. The presence of any test order in Stage 7 validates the ordering workflow functions, which applies to both iPad and web.

---

## Stage 9: Sales Portal (Analytics Dashboard)

**Goal:** Sales analytics portal is configured with data and accessible to authorized users

### ⚠️ Stage Applicability

**Only run this stage if:** HubSpot "Associated Product(s)" includes **"eCat Sales Portal"**

### Prerequisites

- [ ] Stages 1-6 must be GREEN (shared platform foundation complete)
- [ ] eCat Online (Stage 8) recommended but not required

### Critical Blockers (Must Pass)

- [ ] Portal dashboard feature enabled (`enable_portal_dashboard: true`)
- [ ] Order data file uploaded (CSV with order history)
- [ ] Invoice data file uploaded (CSV with invoice history)

### Recommended (Should Pass)

- [ ] Data verified against ERP source (numbers match)
- [ ] Territory/user permissions configured (controls data visibility)

### Optional (Nice-to-Have)

- [ ] Limited user group rollout first (test before full launch)
- [ ] Admin user designated for portal management

### Pass Criteria

- **🔴 RED (BLOCKER):** Portal dashboard disabled OR no order data uploaded OR no invoice data uploaded
- **🟡 YELLOW (WARNING):** All blockers pass but ERP verification incomplete OR no permission structure
- **🟢 GREEN (READY):** All critical + recommended criteria pass AND data verified accurate

### How to Validate

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 9.1 | Portal enabled | `get_organization_settings` | `flags.enable_portal_dashboard` = `true` |
| 9.2 | Order data uploaded | Manual check | Order data visible in portal admin |
| 9.3 | Invoice data uploaded | Manual check | Invoice data visible in portal admin |
| 9.4 | ERP verification | Manual check | Client confirms data accuracy |
| 9.5 | Permissions configured | `get_user_territories` OR `get_org_users` | Territory codes assigned OR user groups with portal access |
| 9.6 | Currency configured | `get_organization_settings` | `sales_portal_currency_code` set appropriately |

---

## Quick Reference: Status Colors

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| 🔴 RED | Launch Blocker | Stop - must resolve before proceeding |
| 🟡 YELLOW | Warning | Can launch but requires CS follow-up |
| 🟢 GREEN | Ready | Proceed to next stage |
| ⚪ N/A | Not Applicable | Feature disabled or product not purchased - skip validation |

---

## Quick Reference: Critical Launch Blockers by Product

### eCat iPad (Stages 1-7)

| # | Blocker | Stage |
|---|---------|-------|
| 1 | Price levels configured | Stage 3 |
| 2 | Customers imported | Stage 5 |
| 3 | Mobile site enabled | Stage 7 |
| 4 | Report formats configured | Stage 7 |
| 5 | Test order processed | Stage 7 |

### eCat Online (Stages 1-6 + 8)

| # | Blocker | Stage |
|---|---------|-------|
| 1 | Price levels configured | Stage 3 |
| 2 | Customers imported | Stage 5 |
| 3 | Mobile site enabled | Stage 8 |
| 4 | Multiple user groups configured | Stage 8 |
| 5 | At least 1 online user created | Stage 8 |

### Sales Portal (Stages 1-6 + 9)

| # | Blocker | Stage |
|---|---------|-------|
| 1 | Portal dashboard enabled | Stage 9 |
| 2 | Order data uploaded | Stage 9 |
| 3 | Invoice data uploaded | Stage 9 |

---

## Quick Reference: Stage Execution by Product Configuration

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

## Assessment Execution Checklist

Before running assessment:

1. **Check HubSpot** for client's "Associated Product(s)" field
2. **Determine applicable stages** using the table above
3. **Run Stages 1-6** for all clients (shared foundation)
4. **Run product-specific stages** based on purchased products:
   - Stage 7 for eCat iPad
   - Stage 8 for eCat Online
   - Stage 9 for Sales Portal

---

---

# Validation Overlay: Fathom + Help Scout

## Overview

The stage-gated assessment above provides **quantitative data** from system endpoints. However, **system state ≠ implementation reality**. Data may exist because:
- Someone tested a feature but hasn't loaded production data
- Test configurations were never cleaned up
- Imports ran but the client hasn't verified accuracy

The Validation Overlay cross-references qualitative sources (Fathom calls, Help Scout tickets) to flag contradictions.

### Two-Layer Validation Approach

| Layer | Source | Purpose |
|-------|--------|---------|
| **Layer 1** | MCP Endpoints (Stages 1-9) | Data-driven assessment - "What does the system say?" |
| **Layer 2** | Fathom + Help Scout | Contradiction detection - "What do conversations say?" |

### Flag Types

| Flag | Icon | Meaning | Action |
|------|------|---------|--------|
| **CONTRADICT** | 🔴 | Evidence directly contradicts system data | Block until resolved |
| **REVIEW** | ⚠️ | Needs clarification from CSM/client | Add to standup agenda |
| **TIMELINE** | ⏰ | Date/target has changed from expected | Update project timeline |
| **ACTIVITY** | 📭 | Zero engagement signals | Outreach to confirm status |
| **CONFIRMED** | ✅ | Qualitative sources validate system data | No action needed |

---

# ⚠️ CRITICAL: Comprehensive Search Requirements

## Fathom API Search Protocol

**DO NOT BE LAZY.** Every Fathom search MUST be exhaustive. Missing relevant calls can lead to false assessments.

### Required Search Passes (Run ALL of these)

| Pass # | Search Location | What to Search For |
|--------|-----------------|-------------------|
| **1** | Call Titles | Full client name (e.g., "Kuzco Lighting") |
| **2** | Call Titles | Client shortname (e.g., "kll", "KLL") |
| **3** | Call Titles | Partial name matches (e.g., "Kuzco") |
| **4** | Call Summaries | Full client name |
| **5** | Call Summaries | Client shortname |
| **6** | Call Summaries | Product keywords (eCat Online, Sales Portal) |
| **7** | Call Transcripts | Full client name |
| **8** | Call Transcripts | Client shortname |
| **9** | Call Transcripts | Product keywords |
| **10** | Call Titles/Summaries/Transcripts | Client email domain (e.g., "@kuzcolighting.com") |

### Fathom Search Implementation

```python
from fathom_api import get_meetings, get_summary, get_transcript

def comprehensive_fathom_search(client_info):
    """
    COMPREHENSIVE Fathom search - DO NOT SKIP ANY STEP
    
    Args:
        client_info: dict with keys:
            - full_name: "Kuzco Lighting Inc."
            - shortname: "kll"
            - email_domain: "@kuzcolighting.com"
            - product_keywords: ["eCat Online", "Sales Portal", "eOL", "portal"]
    """
    
    all_relevant_meetings = set()
    
    # Step 1: Get ALL meetings (paginate through all pages)
    all_meetings = []
    for page in range(1, 20):  # Search up to 20 pages
        meetings = get_meetings(page=page)
        if not meetings:
            break
        all_meetings.extend(meetings)
    
    # Step 2: Search call TITLES for client identifiers
    search_terms_titles = [
        client_info['full_name'],           # "Kuzco Lighting Inc."
        client_info['shortname'],            # "kll"
        client_info['shortname'].upper(),    # "KLL"
        client_info['full_name'].split()[0], # "Kuzco" (first word)
    ]
    
    for meeting in all_meetings:
        title = meeting.get('title', '').lower()
        for term in search_terms_titles:
            if term.lower() in title:
                all_relevant_meetings.add(meeting['call_id'])
                break
    
    # Step 3: Search SUMMARIES for client + product keywords
    for meeting in all_meetings:
        if meeting['call_id'] in all_relevant_meetings:
            continue  # Already captured
        
        try:
            summary = get_summary(meeting['call_id'])
            summary_text = summary.lower() if summary else ""
            
            # Check for client identifiers
            for term in search_terms_titles:
                if term.lower() in summary_text:
                    all_relevant_meetings.add(meeting['call_id'])
                    break
            
            # Check for product keywords
            for keyword in client_info['product_keywords']:
                if keyword.lower() in summary_text:
                    all_relevant_meetings.add(meeting['call_id'])
                    break
                    
        except Exception:
            continue
    
    # Step 4: Search TRANSCRIPTS for deeper matches (including email domain)
    for meeting in all_meetings:
        if meeting['call_id'] in all_relevant_meetings:
            continue  # Already captured
        
        try:
            transcript = get_transcript(meeting['call_id'])
            transcript_text = transcript.lower() if transcript else ""
            
            # Check for email domain (last resort identifier)
            if client_info['email_domain'].lower() in transcript_text:
                all_relevant_meetings.add(meeting['call_id'])
                continue
            
            # Check for client name in transcript
            for term in search_terms_titles:
                if term.lower() in transcript_text:
                    all_relevant_meetings.add(meeting['call_id'])
                    break
                    
        except Exception:
            continue
    
    return list(all_relevant_meetings)

# Example usage:
client = {
    'full_name': 'Kuzco Lighting Inc.',
    'shortname': 'kll',
    'email_domain': '@kuzcolighting.com',
    'product_keywords': ['eCat Online', 'Sales Portal', 'eOL', 'portal', 'B2B', 'enrollment']
}
relevant_calls = comprehensive_fathom_search(client)
```

### Fathom Search Checklist (MUST Complete All)

Before marking Fathom validation complete, confirm:

- [ ] Searched call titles for **full client name**
- [ ] Searched call titles for **client shortname** (both cases)
- [ ] Searched call titles for **partial name** (first word)
- [ ] Searched call summaries for **full client name**
- [ ] Searched call summaries for **shortname**
- [ ] Searched call summaries for **product keywords** (eCat Online, Sales Portal, eOL, portal, B2B)
- [ ] Searched call transcripts for **full client name**
- [ ] Searched call transcripts for **shortname**
- [ ] Searched call transcripts for **email domain** (e.g., @kuzcolighting.com)
- [ ] Paginated through **ALL available meeting pages** (not just first page)
- [ ] Excluded **internal training meetings** (unless client-specific)

---

## Help Scout Search Protocol

**CRITICAL:** Query BOTH inboxes and ALL ticket statuses. Missing tickets = missing context.

### Required Query Parameters

| Parameter | Requirement | Why |
|-----------|-------------|-----|
| **Mailboxes** | BOTH "Support" AND "Implementation/Onboarding" | Tickets may be in either inbox |
| **Ticket Status** | ALL (open, pending, closed, spam) | Closed tickets contain historical context |
| **Date Range** | Last 180 days minimum (or all time for new clients) | Implementation context may be older |
| **Search Fields** | ticket_subject, thread_body, conv_customer_organization | Tickets may not have org filled in |

### Help Scout Master Query Template

```sql
-- ⚠️ COMPREHENSIVE Help Scout Query - DO NOT MODIFY FILTERS
-- This query searches BOTH mailboxes and ALL ticket statuses

SELECT DISTINCT
  ticket_number,
  ticket_subject,
  ticket_status,
  mailbox_name,  -- Shows which inbox (Support vs Implementation)
  conv_customer_organization as org_name,
  DATE(ticket_created_at) as created_date,
  DATE(ticket_updated_at) as updated_date,
  LEFT(thread_body, 1000) as thread_excerpt
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  -- ⚠️ CRITICAL: Search by MULTIPLE client identifiers
  (
    -- Option 1: Organization name match
    LOWER(conv_customer_organization) LIKE LOWER('%{client_full_name}%')
    OR LOWER(conv_customer_organization) LIKE LOWER('%{client_shortname}%')
    -- Option 2: Subject line mentions client
    OR LOWER(ticket_subject) LIKE LOWER('%{client_full_name}%')
    OR LOWER(ticket_subject) LIKE LOWER('%{client_shortname}%')
    -- Option 3: Email domain in thread body
    OR LOWER(thread_body) LIKE LOWER('%{client_email_domain}%')
  )
  -- ⚠️ CRITICAL: Include ALL statuses (DO NOT add status filter)
  -- ticket_status can be: 'active', 'pending', 'closed', 'spam'
  
  -- ⚠️ CRITICAL: Search BOTH mailboxes (DO NOT filter by mailbox_name)
  -- mailbox_name can be: 'Support', 'Implementation', etc.

ORDER BY ticket_created_at DESC
LIMIT 200
```

### Help Scout Search Checklist (MUST Complete All)

Before marking Help Scout validation complete, confirm:

- [ ] Queried **BOTH** mailboxes (Support AND Implementation/Onboarding)
- [ ] Included **ALL** ticket statuses (open, pending, closed)
- [ ] Searched by **organization name** (full name and shortname)
- [ ] Searched by **ticket subject** containing client name
- [ ] Searched by **email domain** in thread body
- [ ] Retrieved at least **200 results** (or all if fewer exist)
- [ ] Checked tickets from **last 180 days** minimum
- [ ] Noted **mailbox_name** for each ticket to identify source

### Help Scout Validation Queries by Stage

#### Stage 8: eCat Online Tickets

```sql
-- Stage 8: eCat Online - COMPREHENSIVE ticket search
-- Searches BOTH mailboxes, ALL statuses
SELECT DISTINCT
  ticket_number,
  ticket_subject,
  ticket_status,
  mailbox_name,
  conv_customer_organization as org,
  DATE(ticket_created_at) as created_date,
  LEFT(thread_body, 500) as excerpt
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  -- Client identification (use ALL three methods)
  (
    LOWER(conv_customer_organization) LIKE LOWER('%{client_name}%')
    OR LOWER(ticket_subject) LIKE LOWER('%{client_name}%')
    OR LOWER(thread_body) LIKE LOWER('%{email_domain}%')
  )
  AND (
    -- eCat Online keywords in subject OR body
    LOWER(ticket_subject) LIKE '%ecat online%'
    OR LOWER(ticket_subject) LIKE '%eol%'
    OR LOWER(ticket_subject) LIKE '%b2b%'
    OR LOWER(ticket_subject) LIKE '%enrollment%'
    OR LOWER(ticket_subject) LIKE '%online catalog%'
    OR LOWER(ticket_subject) LIKE '%web portal%'
    OR LOWER(ticket_subject) LIKE '%cname%'
    OR LOWER(ticket_subject) LIKE '%public site%'
    OR LOWER(ticket_subject) LIKE '%can''t log in%'
    OR LOWER(ticket_subject) LIKE '%login%'
    OR LOWER(thread_body) LIKE '%ecat online%'
    OR LOWER(thread_body) LIKE '%enrollment%'
    OR LOWER(thread_body) LIKE '%public site%'
    OR LOWER(thread_body) LIKE '%web catalog%'
    OR LOWER(thread_body) LIKE '%online ordering%'
  )
  -- NO status filter - get ALL statuses
  -- NO mailbox filter - get BOTH inboxes
ORDER BY ticket_created_at DESC
LIMIT 100
```

#### Stage 9: Sales Portal Tickets

```sql
-- Stage 9: Sales Portal - COMPREHENSIVE ticket search
-- Searches BOTH mailboxes, ALL statuses
SELECT DISTINCT
  ticket_number,
  ticket_subject,
  ticket_status,
  mailbox_name,
  conv_customer_organization as org,
  DATE(ticket_created_at) as created_date,
  LEFT(thread_body, 500) as excerpt
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  -- Client identification (use ALL three methods)
  (
    LOWER(conv_customer_organization) LIKE LOWER('%{client_name}%')
    OR LOWER(ticket_subject) LIKE LOWER('%{client_name}%')
    OR LOWER(thread_body) LIKE LOWER('%{email_domain}%')
  )
  AND (
    -- Sales Portal keywords in subject OR body
    LOWER(ticket_subject) LIKE '%sales portal%'
    OR LOWER(ticket_subject) LIKE '%portal dashboard%'
    OR LOWER(ticket_subject) LIKE '%analytics%'
    OR LOWER(ticket_subject) LIKE '%order data%'
    OR LOWER(ticket_subject) LIKE '%invoice data%'
    OR LOWER(ticket_subject) LIKE '%csv%'
    OR LOWER(ticket_subject) LIKE '%reporting%'
    OR LOWER(thread_body) LIKE '%sales portal%'
    OR LOWER(thread_body) LIKE '%portal dashboard%'
    OR LOWER(thread_body) LIKE '%order file%'
    OR LOWER(thread_body) LIKE '%invoice file%'
    OR LOWER(thread_body) LIKE '%doesn''t match%'
    OR LOWER(thread_body) LIKE '%erp%'
    OR LOWER(thread_body) LIKE '%territory%'
  )
  -- NO status filter - get ALL statuses
  -- NO mailbox filter - get BOTH inboxes
ORDER BY ticket_created_at DESC
LIMIT 100
```

---

## Stage 8 Validation: eCat Online

### Fathom API Search Keywords

Search call **titles**, **summaries**, AND **transcripts** for these terms:

| Category | Search Terms |
|----------|--------------|
| **Product mentions** | `"eCat Online"`, `"eOL"`, `"B2B"`, `"web portal"`, `"online catalog"`, `"public site"` |
| **Feature discussions** | `"enrollment"`, `"CNAME"`, `"custom domain"`, `"user group"`, `"site settings"` |
| **Status indicators** | `"go-live"`, `"launch"`, `"live"`, `"ready"`, `"testing"`, `"not ready"` |
| **Issue indicators** | `"broken"`, `"not working"`, `"issue"`, `"problem"`, `"error"`, `"can't"` |

### Stage 8 Contradiction Patterns

| System Says | But Fathom/Help Scout Says | Flag |
|-------------|---------------------------|------|
| Mobile site enabled ✅ | "We haven't set up the online site yet" | 🔴 CONTRADICT |
| eOL user group exists ✅ | "Still deciding on user group permissions" | ⚠️ REVIEW |
| Enrollment configured ✅ | "Enrollment not needed - direct customer creation only" | ⚠️ REVIEW |
| CNAME configured ✅ | "DNS hasn't been updated by IT" | ⏰ TIMELINE |
| Web orders exist ✅ | "Those are test orders - need to delete before go-live" | 🔴 CONTRADICT |
| No recent tickets | 0 tickets in 90+ days for active eOL client | 📭 ACTIVITY |

### Stage 8 Validation Checklist

After running MCP assessment, check:

- [ ] **Fathom (last 90 days):** Any calls mentioning eOL status?
- [ ] **Fathom transcript search:** Does recent call mention "not ready" or "testing"?
- [ ] **Help Scout (BOTH inboxes):** Any open tickets about enrollment or site access issues?
- [ ] **Help Scout (BOTH inboxes):** Any tickets about "can't log in" or "can't see products"?
- [ ] **Help Scout (ALL statuses):** Recent tickets about pricing not showing correctly?

---

## Stage 9 Validation: Sales Portal

### Fathom API Search Keywords

Search call **titles**, **summaries**, AND **transcripts** for these terms:

| Category | Search Terms |
|----------|--------------|
| **Product mentions** | `"Sales Portal"`, `"portal"`, `"dashboard"`, `"analytics"`, `"reporting"` |
| **Data discussions** | `"order data"`, `"invoice data"`, `"CSV"`, `"upload"`, `"import"`, `"ERP"` |
| **Verification** | `"verify"`, `"numbers match"`, `"discrepancy"`, `"doesn't match"`, `"wrong data"` |
| **Permission discussions** | `"territory"`, `"visibility"`, `"who can see"`, `"permissions"` |
| **Status indicators** | `"go-live"`, `"billing"`, `"launch date"`, `"implemented"`, `"live"` |

### Stage 9 Contradiction Patterns

| System Says | But Fathom/Help Scout Says | Flag |
|-------------|---------------------------|------|
| Portal enabled ✅ | "We haven't started Sales Portal yet" | 🔴 CONTRADICT |
| Order data exists ✅ | "Data is test data - not production" | 🔴 CONTRADICT |
| Invoice data exists ✅ | "Still waiting on IT for invoice extract" | ⏰ TIMELINE |
| Permissions configured ✅ | "Numbers don't match ERP report" | ⚠️ REVIEW |
| Portal ready ✅ | "Rolling out to limited users first" | ⚠️ REVIEW |
| All green ✅ | "Haven't billed for portal yet - not live" | 🔴 CONTRADICT |

### Stage 9 Validation Checklist

After running MCP assessment, check:

- [ ] **Fathom (last 90 days):** Any calls mentioning Sales Portal implementation?
- [ ] **Fathom transcript search:** Does client mention "data doesn't match"?
- [ ] **Fathom transcript search:** Has billing/go-live date been discussed?
- [ ] **Help Scout (BOTH inboxes):** Any open tickets about wrong data in portal?
- [ ] **Help Scout (BOTH inboxes):** Any tickets about missing orders or invoices?
- [ ] **Help Scout (ALL statuses):** Tickets mentioning ERP discrepancies?

---

## ⚠️ Validation Completion Checklist

**Before finalizing ANY client assessment, confirm ALL of these:**

### Fathom Completion Checklist

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Searched call titles for **full client name** | ☐ |
| 2 | Searched call titles for **shortname** (both cases) | ☐ |
| 3 | Searched call summaries for **full client name** | ☐ |
| 4 | Searched call summaries for **product keywords** | ☐ |
| 5 | Searched call transcripts for **client identifiers** | ☐ |
| 6 | Searched call transcripts for **email domain** | ☐ |
| 7 | Paginated through **ALL meeting pages** | ☐ |
| 8 | Reviewed **last 90 days minimum** | ☐ |

### Help Scout Completion Checklist

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Queried **Support** mailbox | ☐ |
| 2 | Queried **Implementation/Onboarding** mailbox | ☐ |
| 3 | Included **open** tickets | ☐ |
| 4 | Included **closed** tickets | ☐ |
| 5 | Included **pending** tickets | ☐ |
| 6 | Searched by **organization name** | ☐ |
| 7 | Searched by **ticket subject** containing client name | ☐ |
| 8 | Searched by **email domain** in thread body | ☐ |
| 9 | Retrieved **last 180 days minimum** | ☐ |

### If Checklist Not Complete

**DO NOT mark validation as complete.** Go back and run the missing searches.

Incomplete validation can result in:
- ❌ False positives (marking a stage as ready when it's not)
- ❌ Missing critical context from support tickets
- ❌ Overlooking implementation blockers discussed in calls
- ❌ Incorrect CSM recommendations
- [ ] **Help Scout:** Tickets mentioning ERP discrepancies?

---

## Validation Workflow

### Step 1: Run Data Assessment (Stages 1-9)

```
1. Query MCP endpoints for each applicable stage
2. Record GREEN/YELLOW/RED status
3. Calculate overall readiness percentage
```

### Step 2: Run Fathom Validation

```python
# Fathom API validation flow
from fathom_api import get_meetings, get_summary, get_transcript

# 1. Get all meetings for client (last 90 days)
meetings = get_meetings(page_limit=5)

# 2. Filter by client name and product keywords
client_meetings = [m for m in meetings 
                   if client_name.lower() in m['title'].lower()
                   or any(kw in m['title'].lower() for kw in product_keywords)]

# 3. For each meeting, check summary + transcript for contradictions
for meeting in client_meetings:
    summary = get_summary(meeting['call_id'])
    transcript = get_transcript(meeting['call_id'])
    
    # Check for contradiction keywords
    check_for_flags(summary, transcript, stage_criteria)
```

### Step 3: Run Help Scout Validation

```sql
-- Combined validation query for all stages
SELECT 
  ticket_number,
  ticket_subject,
  ticket_status,
  conv_customer_organization as client,
  mailbox_name,
  DATE(ticket_created_at) as created_date,
  CASE 
    WHEN LOWER(ticket_subject) LIKE '%portal%' 
      OR LOWER(thread_body) LIKE '%sales portal%' THEN 'Stage 9: Sales Portal'
    WHEN LOWER(ticket_subject) LIKE '%eol%' 
      OR LOWER(ticket_subject) LIKE '%ecat online%' 
      OR LOWER(thread_body) LIKE '%enrollment%' THEN 'Stage 8: eCat Online'
    ELSE 'Stages 1-7: Core Platform'
  END as related_stage
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  conv_customer_organization LIKE '%{client_name}%'
  AND ticket_created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
ORDER BY ticket_created_at DESC
```

### Step 4: Compile Flags

For each stage, record:

| Stage | Data Status | Fathom Flag | Help Scout Flag | Final Status |
|-------|-------------|-------------|-----------------|--------------|
| 8 | 🟢 GREEN | None | None | ✅ CONFIRMED |
| 8 | 🟢 GREEN | 🔴 CONTRADICT | None | 🔴 BLOCKED |
| 9 | 🟡 YELLOW | ⚠️ REVIEW | None | ⚠️ REVIEW |

---

## Example Validation Output

### Client: Example Corp (exc)

**HubSpot Products:** eCat iPad ✅, eCat Online ✅, Sales Portal ✅  
**Assessment Date:** January 13, 2026

#### Stage 8: eCat Online

| # | Criterion | MCP Result | Fathom/HS Flag | Final |
|---|-----------|------------|----------------|-------|
| 8.1 | Mobile site enabled | ✅ `enabled: true` | None | 🟢 |
| 8.2 | eOL user group | ✅ "eCat Online" group | ⚠️ "Still finalizing permissions" | ⚠️ REVIEW |
| 8.3 | Online user created | ✅ 12 users | None | 🟢 |
| 8.4 | Enrollment recipients | ❌ Empty | None | 🟡 |
| 8.5 | Web order exists | ✅ 3 orders | 🔴 "Test orders, not real" | 🔴 CONTRADICT |

**Stage 8 Status:** 🔴 BLOCKED - Test order contradiction, needs cleanup

#### Stage 9: Sales Portal

| # | Criterion | MCP Result | Fathom/HS Flag | Final |
|---|-----------|------------|----------------|-------|
| 9.1 | Portal enabled | ✅ `true` | None | 🟢 |
| 9.2 | Order data | ✅ Present | None | 🟢 |
| 9.3 | Invoice data | ✅ Present | ⏰ "Invoice data refresh needed" | ⏰ TIMELINE |
| 9.4 | ERP verification | ❓ Manual | ⚠️ "Numbers slightly off" | ⚠️ REVIEW |
| 9.5 | Permissions | ✅ Territories set | None | 🟢 |

**Stage 9 Status:** ⚠️ REVIEW - Data accuracy needs confirmation

---

## Validation Flag Summary Template

Use this format for standup reporting:

```
## {Client Name} ({shortname})
### V8 Assessment: Stage X | Y% Ready

| Stage | Data Status | Validation Status | Flag Count |
|-------|-------------|-------------------|------------|
| 8 | 🟢 | ⚠️ REVIEW | 2 flags |
| 9 | 🟡 | ✅ Confirmed | 0 flags |

### 🔴 Critical Flags (Require Action)
| Stage | Issue | Source | Evidence |
|-------|-------|--------|----------|
| 8 | Test orders | Fathom Dec 15 | "Those are test orders - delete before go-live" |

### ⚠️ Review Flags (Need Clarification)
| Stage | Issue | Source | Evidence |
|-------|-------|--------|----------|
| 8 | Permissions | Fathom Dec 20 | "Still finalizing user group permissions" |
| 9 | Data accuracy | Help Scout #45678 | "Portal numbers don't match our ERP exactly" |

### ✅ Confirmed (Validated)
- Stage 8.1: Mobile site enabled - confirmed in Dec 15 call
- Stage 9.1: Portal enabled - Help Scout ticket #12345 confirms live
```

---

## Appendix: Data Sources Reference

### MCP Endpoints

| Endpoint | Used In Stages | Primary Purpose |
|----------|----------------|-----------------|
| `get_organization_info` | 1, 7, 8 | Basic org data, settings |
| `get_organization_settings` | 8, 9 | Flags, enrollment, portal settings |
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
| `get_smart_stacks` | 6 | Smart stack configuration |
| `get_mobile_sites` | 8 | Web portal configuration (eCat Online) |
| `get_reports_config` | 7 | Report templates |
| `get_orders` | 7, 8 | Order history |

### BigQuery Tables

| Table | Used In Stages | Primary Purpose |
|-------|----------------|-----------------|
| `mixpanel_selected_org` | 7 | iPad app login activity tracking |
| `mixpanel_order_submitted` | 7, 8 | Order source validation (iPad vs Web) |
| `help_scout_tickets` | Validation | Support ticket review for contradictions |
| `crm_companies` | Pre-assessment | HubSpot product association check |

### Fathom API

| Function | Used For | Primary Purpose |
|----------|----------|-----------------|
| `get_meetings()` | Validation | Retrieve implementation calls |
| `get_summary()` | Validation | Call summaries for keyword search |
| `get_transcript()` | Validation | Full transcripts for contradiction detection |

---

## Appendix: Key Distinction - Stage 7 vs Stage 8

| Check | Stage 7 (iPad) | Stage 8 (eCat Online) |
|-------|----------------|----------------------|
| **What it validates** | Native iOS app usage | Web portal accessibility |
| **Data source** | BigQuery Mixpanel (`mixpanel_selected_org`) | MCP (`get_mobile_sites`) |
| **Filter criteria** | `_model LIKE 'iPad%'` | `enabled: true` |
| **User type** | Sales reps with iPads | Online customers (B2B) |
| **Metric** | Unique iPad users logged in | Mobile site enabled |

This distinction is critical because:
- **Stage 7** checks if **reps** are using the **iPad app** (offline-capable, full-featured)
- **Stage 8** checks if the **web portal** is configured for **customers** (browser-based, B2B shopping)

A client could have Stage 7 complete (reps using iPads) but Stage 8 incomplete (web portal not configured for customer self-service), or vice versa.

---

*V8 Stage-Gated Model - Updated January 2026*
*Extends V6 (iPad) + V7 (Validation Layer) to support full product suite*
