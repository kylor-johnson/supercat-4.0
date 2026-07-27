# FRD: Accuracy Mode Stage-Gated Onboarding Readiness Scoring

**Author:** Kylor Johnson  
**Date:** January 14, 2026  
**Version:** 12.0 (Accuracy Mode + Anti-Hallucination + Mandatory Tool Verification)  
**Status:** Production Ready  
**Related JIRA:** [Link to your JIRA ticket]

---

## Document Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 10.0 | Jan 14, 2026 | Production baseline (12-stage multi-product framework) | Kylor Johnson |
| 11.0 | Jan 14, 2026 | Fast Mode Protocol: Parallel MCP batching, conditional validation, 85% accuracy target | Kylor Johnson |
| 11.3 | Jan 14, 2026 | Fathom API + Help Scout mandatory fixes | Kylor Johnson |
| **12.0** | Jan 14, 2026 | **ACCURACY MODE:** Complete rewrite prioritizing 100% data accuracy. Added mandatory tool call verification, anti-hallucination rules, source attribution requirements. Removed all skip conditions. Every metric must be retrieved from actual tool calls - NO data estimation or generation permitted. | Kylor Johnson |

---

## Executive Summary

V12 Accuracy Mode is a **complete rewrite** of the Stage-Gated framework, prioritizing **100% data accuracy** over execution speed. This version was created after discovering that prior versions allowed LLM hallucination of metrics due to insufficient verification requirements.

**Core Principle:** Every single metric in the output MUST come from a verifiable tool call. No estimation, no approximation, no generation.

**Key Requirements:**
1. **Mandatory Tool Call Verification:** Every metric must show its source tool call
2. **Anti-Hallucination Rules:** Explicit prohibition on generating plausible-looking data
3. **Source Attribution:** Every value in output must include `[Source: endpoint.field]`
4. **No Skip Conditions:** ALL validation phases are mandatory, regardless of apparent status
5. **Pre-Output Validation:** Checklist to verify data came from actual queries

**Performance Expectations:**
- Execution time: 15-25 min/client (accuracy over speed)
- Accuracy target: **100%** (no tolerance for hallucination)
- Every metric traceable to source tool call

---

## ⛔ CRITICAL: ANTI-HALLUCINATION RULES

### The Problem V12 Solves

In V11 testing, the LLM hallucinated metrics that looked plausible but were completely fabricated:
- CST inventory reported as 79,665 when actual was 4,821 (16.5x error)
- DCCL options reported as 15 when actual was 2 (7.5x error)
- Orders, customers, and users routinely fabricated

**Root Cause:** V11 allowed the model to skip tool calls for "obvious" cases and didn't require proof of query execution.

### V12 Mandatory Rules

#### Rule 1: No Data Without Tool Calls
```
⛔ FORBIDDEN: Generating ANY numeric value without a tool call
⛔ FORBIDDEN: Using "approximately", "estimated", or "~" for metrics
⛔ FORBIDDEN: Inferring values from context or prior knowledge
⛔ FORBIDDEN: Copying values from user-provided documents
⛔ FORBIDDEN: Using cached data from earlier in conversation
```

#### Rule 2: Failed Queries Must Be Marked
```
If a tool call fails or returns an error:
1. Mark the metric as "❓ QUERY FAILED: [error message]"
2. DO NOT substitute a plausible value
3. Flag the client for manual verification
4. Document which tool failed and why
```

#### Rule 3: Source Attribution Required
Every metric in output MUST include its source:
```markdown
| Metric | Value | Source |
|--------|-------|--------|
| Products | 2,657 | `get_data_summary.counts.products` |
| Price Levels | 3 | `get_price_levels.length` |
| iPad Orders | 149 | `BigQuery: mixpanel_order_submitted WHERE mp_lib='iphone'` |
```

#### Rule 4: Tool Call Proof Required
Before presenting output, you MUST have executed and shown results from:
- [ ] `get_organization_info(org_shortname)` 
- [ ] `get_data_summary(org_shortname)`
- [ ] `get_price_levels(org_shortname)`
- [ ] BigQuery iPad activity query
- [ ] BigQuery Help Scout query
- [ ] Fathom API `get_meetings()` filtered by client
- [ ] Fathom API `get_summary()` for recent calls

---

## Products Supported

| Product | Required Stages |
|---------|-----------------|
| **eCat iPad** | 1, 2, 3, 4*, 5, 6, 7 |
| **eCat Online** | 1, 2, 3, 4*, 5, 6, 8, 9, 10* |
| **Sales Portal** | 1, 2, 3, 4*, 5, 6, 8, 9, 11, 12 |

*Conditional stages based on feature enablement

---

## Quick Reference: Status Colors

| Status | Meaning | Action |
|--------|---------|--------|
| 🔴 RED | Launch Blocker | Must resolve before proceeding |
| 🟡 YELLOW | Warning | Can launch but needs follow-up |
| 🟢 GREEN | Ready | Proceed to next stage |
| ⚪ N/A | Not Applicable | Skip - feature not enabled |
| ❓ UNKNOWN | Query Failed | Flag for manual verification |

---

# PHASE 1: MANDATORY MCP VALIDATION

## ⚠️ CRITICAL: All Tool Calls Are Mandatory

**V12 removes ALL skip conditions.** Every endpoint must be called for every client.

### Pre-Execution Validation

Before running any assessment:
1. **Verify org shortname exists** - Run `get_organization_info` first
2. **Confirm MCP connection** - Verify tool calls return data, not errors
3. **Document the shortname used** - Include in output header

### Batch 1: Foundation Data (MANDATORY)

**Endpoints - ALL REQUIRED:**
- `get_organization_info(org_shortname)` → Stage 1
- `get_org_users(org_shortname)` → Stage 1, 5
- `get_data_summary(org_shortname)` → Stages 2, 5, 6

**Execution:**
```
Call: mcp_supercat-cs-tools_get_organization_info
Parameter: org_shortname = "[CLIENT_SHORTNAME]"
Required Fields to Extract:
- basic_info.shortname (verify matches expected)
- basic_info.name (verify correct client)
- basic_info.status (active/inactive)
- basic_info.created_at (for Days Active calculation)

Call: mcp_supercat-cs-tools_get_data_summary
Parameter: org_shortname = "[CLIENT_SHORTNAME]"  
Required Fields to Extract:
- counts.products
- counts.options
- counts.customers
- counts.org_users
- counts.price_levels
- counts.inventories
- counts.orders
- counts.orders_last_30_days
- recent_activity.last_product_update
- recent_activity.last_customer_update
- recent_activity.last_order_created
- recent_activity.last_inventory_update
```

**Output Format (Required):**
```markdown
### Batch 1 Results: [CLIENT_NAME] ([SHORTNAME])

**Tool Call:** `get_organization_info(org_shortname="[X]")`
**Response:** 
- Name: [value from basic_info.name]
- Status: [value from basic_info.status]
- Created: [value from basic_info.created_at]

**Tool Call:** `get_data_summary(org_shortname="[X]")`
**Response:**
- Products: [value from counts.products]
- Options: [value from counts.options]
- Customers: [value from counts.customers]
- Users: [value from counts.org_users]
- Price Levels: [value from counts.price_levels]
- Inventories: [value from counts.inventories]
- Orders Total: [value from counts.orders]
- Orders (30 days): [value from counts.orders_last_30_days]
```

---

### Batch 2: Configuration Data (MANDATORY)

**Endpoints - ALL REQUIRED:**
- `get_price_levels(org_shortname)` → Stage 3
- `get_categories(org_shortname)` → Stage 2
- `get_collections(org_shortname)` → Stage 2
- `get_options(org_shortname)` → Stage 4

**Output Format (Required):**
```markdown
### Batch 2 Results: [CLIENT_NAME]

**Tool Call:** `get_price_levels(org_shortname="[X]")`
**Response:** [X] price levels found
- Level 1: [name] (code: [code])
- Level 2: [name] (code: [code])
- ...

**Tool Call:** `get_categories(org_shortname="[X]")`
**Response:** [X] categories found

**Tool Call:** `get_collections(org_shortname="[X]")`
**Response:** [X] collections found

**Tool Call:** `get_options(org_shortname="[X]")`
**Response:** [X] options found (or "0 options - Stage 4 N/A")
```

---

### Batch 3: Operations Data (MANDATORY)

**Endpoints - ALL REQUIRED:**
- `get_user_territories(org_shortname)` → Stage 5
- `get_import_events(org_shortname)` → Stage 6
- `get_smart_stacks(org_shortname)` → Stage 6
- `get_inventories(org_shortname)` → Stage 6

---

### Batch 4: Product-Specific Data (MANDATORY)

**Endpoints - ALL REQUIRED:**
- `get_mobile_sites(org_shortname)` → Stages 7, 8
- `get_reports_config(org_shortname)` → Stage 7
- `get_orders(org_shortname)` → Stage 7, 10
- `get_permissions_summary(org_shortname)` → Stages 5, 9, 12

---

# PHASE 2: MANDATORY BIGQUERY VALIDATION

## ⚠️ CRITICAL: BigQuery Queries Are Mandatory

Both queries MUST be executed. No exceptions.

### Query 1: iPad Activity (Stage 7)

**Execute via `mcp_bigquery_query`:**
```sql
SELECT 
  currentorganizationshortname as org,
  COUNT(*) as ipad_orders,
  COUNT(DISTINCT distinct_id) as unique_ipad_users,
  MAX(TIMESTAMP_SECONDS(CAST(time AS INT64))) as last_ipad_order,
  MIN(TIMESTAMP_SECONDS(CAST(time AS INT64))) as first_ipad_order
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.mixpanel_order_submitted`
WHERE currentorganizationshortname = '[ORG_SHORTNAME]'
  AND mp_lib = 'iphone'
GROUP BY currentorganizationshortname
```

**Output Format (Required):**
```markdown
### BigQuery iPad Activity: [CLIENT_NAME]

**Query Executed:** iPad orders from MixPanel
**Org Filter:** currentorganizationshortname = '[X]'
**Results:**
- iPad Orders: [value]
- Unique iPad Users: [value]
- First iPad Order: [date]
- Last iPad Order: [date]
- Days Active: [calculated from first to last]
```

### Query 2: Help Scout Activity (All Stages)

**Execute via `mcp_bigquery_query`:**
```sql
SELECT 
  ticket_number,
  ticket_subject,
  ticket_status,
  DATE(ticket_created_at) as created_date,
  conv_customer_organization as client,
  ticket_mailbox_name as mailbox,
  LEFT(ticket_preview, 300) as preview
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE (LOWER(conv_customer_organization) LIKE '%[CLIENT_PATTERN]%'
       OR LOWER(ticket_subject) LIKE '%[CLIENT_PATTERN]%')
  AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY ticket_created_at DESC
LIMIT 25
```

**Output Format (Required):**
```markdown
### BigQuery Help Scout: [CLIENT_NAME]

**Query Executed:** Help Scout tickets (90 days)
**Client Filter:** '[X]'
**Results:** [X] tickets found

**Recent Tickets:**
| # | Date | Subject | Mailbox | Status |
|---|------|---------|---------|--------|
| 12345 | 2026-01-10 | [subject] | Support | active |
| ... | ... | ... | ... | ... |

**Key Findings:**
- [Quote from ticket if relevant]
- [Activity indicators]
```

---

# PHASE 3: MANDATORY FATHOM VALIDATION

## ⚠️ CRITICAL: Fathom API Is Mandatory

You MUST execute the Fathom API calls. Notion search is NOT a substitute.

### Step 1: Get All Meetings (MANDATORY)

**Execute via terminal:**
```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'fathom'))
from fathom_api import get_meetings

meetings = get_meetings()
clients = ['[client_name]', '[shortname]', '[alternate_names]']
relevant = [m for m in meetings 
            if any(c.lower() in m.get('meeting_title', '').lower() for c in clients)]

print(f'Found {len(relevant)} calls for {clients}')
for m in sorted(relevant, key=lambda x: x.get('recording_start_time', ''), reverse=True)[:10]:
    print(f\"{m.get('recording_id')} | {m.get('recording_start_time', '')[:10]} | {m.get('meeting_title')}\")
"
```

### Step 2: Get Summaries for Recent Calls (MANDATORY)

**For EACH call found in the last 90 days, execute:**
```bash
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'fathom'))
from fathom_api import get_summary

summary = get_summary([RECORDING_ID])
print(summary.get('summary', {}).get('markdown_formatted', '')[:3000])
"
```

**Output Format (Required):**
```markdown
### Fathom Validation: [CLIENT_NAME]

**Tool Call:** `get_meetings()` filtered by '[client_terms]'
**Results:** [X] calls found in last 90 days

**Call Log:**
| ID | Date | Title |
|----|------|-------|
| 113941321 | 2026-01-13 | [Hold] eCat x Client Standup |
| ... | ... | ... |

**Summary Retrieved for Call [ID] ([Date]):**
> "[Exact quote from summary relevant to implementation status]"

**Validation Findings:**
- Timeline: [any deadlines mentioned]
- Blockers: [any blockers mentioned]
- Sentiment: [positive/neutral/negative with evidence]
```

---

# STAGE DEFINITIONS (Aligned with V8 Checklist)

## FOUNDATION STAGES (1-6) - Required for ALL Products

---

## Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

### Checklist
- [ ] Company name filled in
- [ ] At least 1 admin user exists (excluding: Kylor_Johnson, brentsanders, cwiebe)
- [ ] Settings initialized with defaults

### Pass Criteria
- 🔴 **RED (BLOCKER):** Any item above unchecked
- 🟢 **GREEN (READY):** All items checked

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_organization_info(org_shortname) 
   → Check: basic_info.name is not empty
   → Check: basic_info.status = "active"
   
2. get_org_users(org_shortname)
   → Check: At least 1 user with is_admin: true
   → Check: Admin is not internal test user
```

### Evidence Required in Output
```markdown
| Criterion | Status | Source | Evidence |
|-----------|--------|--------|----------|
| Company name | 🟢 | `get_organization_info.basic_info.name` | "Jonathan Charles Fine Furniture Ltd." |
| Admin exists | 🟢 | `get_org_users` | 3 admins found (excluding internal) |
| Settings init | 🟢 | `get_organization_info.settings` | Currency: USD, defaults configured |
```

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
- 🔴 **RED (BLOCKER):** Less than 10 products imported
- 🟡 **YELLOW (WARNING):** 10-100 products OR no updates in 60+ days
- 🟢 **GREEN (READY):** 100+ products AND updated within last 30 days

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_data_summary(org_shortname)
   → Extract: counts.products
   → Extract: recent_activity.last_product_update
   
2. get_categories(org_shortname)
   → Count: number of categories returned
   
3. get_collections(org_shortname)
   → Count: number of collections returned
```

### Evidence Required in Output
```markdown
| Criterion | Status | Source | Evidence |
|-----------|--------|--------|----------|
| Products ≥10 | 🟢 | `get_data_summary.counts.products` | 2,657 products |
| Categories ≥1 | 🟢 | `get_categories.length` | 76 categories |
| Collections ≥1 | 🟢 | `get_collections.length` | 194 collections |
| Updated <30d | 🟢 | `get_data_summary.recent_activity.last_product_update` | 2026-01-14 |
```

---

## Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

### Checklist
- [ ] Price levels configured
- [ ] At least 2 price levels configured (recommended)
- [ ] Price levels have descriptive names, not "Price Level 1"
- [ ] Price level codes assigned (recommended)

### Pass Criteria
- 🔴 **RED (BLOCKER):** No price levels configured
- 🟡 **YELLOW (WARNING):** Only 1 price level OR generic names
- 🟢 **GREEN (READY):** 2+ price levels with descriptive names

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_price_levels(org_shortname)
   → Count: number of price levels
   → Extract: names and codes for each level
   → Check: names are not generic defaults
```

### Evidence Required in Output
```markdown
| Criterion | Status | Source | Evidence |
|-----------|--------|--------|----------|
| Price levels ≥1 | 🟢 | `get_price_levels.length` | 3 price levels |
| Descriptive names | 🟢 | `get_price_levels[*].name` | "Dealer Net", "Designer", "IMAP" |
| Codes assigned | 🟢 | `get_price_levels[*].code` | All have unique codes |
```

---

## Stage 4: Option Configuration (CONDITIONAL)

**Goal:** If options enabled, CPQ/configurators are functional

### Check if Stage Applies
- Run `get_options(org_shortname)`
- If returns 0 options → Mark ⚪ **N/A**, skip to Stage 5
- If returns 1+ options → Continue with checklist

### Pass Criteria
- ⚪ **N/A:** Options disabled (0 options returned)
- 🔴 **RED (BLOCKER):** Options enabled but `require_valid_options_to_submit_orders` = true with broken options
- 🟡 **YELLOW (WARNING):** Less than 5 options configured
- 🟢 **GREEN (READY):** 5+ options configured

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_options(org_shortname)
   → Count: ACTUAL number of option records returned
   → NOT the number of option_group columns in schema
   
⚠️ CRITICAL: Count the OPTIONS returned, not schema columns
```

---

## Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

### Checklist (Both Models)
- [ ] At least 10 customers imported
- [ ] At least 2 users configured
- [ ] Multiple user types exist
- [ ] Customers updated within last 30 days

### Pass Criteria
- 🔴 **RED (BLOCKER):** Less than 10 customers OR no users configured
- 🟡 **YELLOW (WARNING):** 10-100 customers OR no updates in 30+ days
- 🟢 **GREEN (READY):** 100+ customers AND updated within last 30 days

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_data_summary(org_shortname)
   → Extract: counts.customers
   → Extract: counts.org_users
   → Extract: recent_activity.last_customer_update
   
2. get_org_users(org_shortname)
   → Count: unique user types
   → Verify: multiple user types exist
   
3. get_user_territories(org_shortname)
   → Determine: Territory vs Direct Assignment model
```

---

## Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

### Checklist
- [ ] No critical import errors in last 30 days
- [ ] Smart stacks configured OR feature disabled
- [ ] Inventory data exists (if tracking enabled)
- [ ] Inventory updated within last 7 days (if tracking enabled)

### Pass Criteria
- 🔴 **RED (BLOCKER):** Inventory enabled but no data OR critical import errors
- 🟡 **YELLOW (WARNING):** Stale inventory (7+ days) OR minor warnings
- 🟢 **GREEN (READY):** Fresh data AND no import errors

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_data_summary(org_shortname)
   → Extract: counts.inventories
   → Extract: recent_activity.last_inventory_update
   
2. get_import_events(org_shortname, limit=30)
   → Check: No critical errors in last 30 days
   
3. get_inventories(org_shortname, limit=10)
   → Verify: Data exists and has values
```

---

## Stage 7: iPad Order-Ready (eCat iPad ONLY)

**Goal:** iPad app can receive, process, and fulfill orders end-to-end

**Applies to:** eCat iPad ✅ | eCat Online ⚪ | Sales Portal ⚪

### Critical Blockers (Must Pass)
- [ ] 1+ user types exist (more than Default User Group)
- [ ] iPad app activity exists (at least 1 order from iPad)
- [ ] Report formats configured (minimum 3)
- [ ] Test order processed (at least 1 order exists)

### Pass Criteria
- ⚪ **N/A:** eCat iPad not being implemented
- 🔴 **RED (BLOCKER):** Any critical blocker unchecked
- 🟡 **YELLOW (WARNING):** Critical blockers pass but recommended missing
- 🟢 **GREEN (READY):** All criteria pass

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_reports_config(org_shortname)
   → Count: report formats (must be ≥3)
   
2. get_orders(org_shortname)
   → Count: total orders
   
3. get_organization_info(org_shortname)
   → Check: order_email_recipient is configured

REQUIRED BIGQUERY:
4. iPad Activity Query (see Phase 2)
   → Extract: ipad_orders count
   → Extract: unique_ipad_users count
```

---

## Stage 8: eCat Online Site Configuration

**Goal:** Web catalog is accessible and properly branded

**Applies to:** eCat iPad ⚪ | eCat Online ✅ | Sales Portal ✅

### Critical Blockers (Must Pass)
- [ ] eCat Online site created and enabled
- [ ] Site name configured (not default)
- [ ] Public user group exists with permissions

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_mobile_sites(org_shortname)
   → Check: enabled = true
   → Check: site_name is configured
   
2. get_permissions_summary(org_shortname)
   → Check: public user group exists
```

---

## Stage 9: eCat Online User Access & Enrollment

**Goal:** Users can access the catalog via enrollment or invitation

**Applies to:** eCat iPad ⚪ | eCat Online ✅ | Sales Portal ✅

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_org_users(org_shortname)
   → Filter: eCat Online user types
   
2. get_organization_info(org_shortname)
   → Check: enrollment templates configured
   
3. get_permissions_summary(org_shortname)
   → Check: user_type_permissions configured
```

---

## Stage 10: eCat Online Ordering (B2B Cart) - CONDITIONAL

**Goal:** If B2B ordering enabled, customers can place orders through web

**Applies to:** eCat iPad ⚪ | eCat Online ✅ (conditional) | Sales Portal ⚪

### Check if Stage Applies
- Is B2B ordering enabled?
- **YES** → Continue with checklist
- **NO** → Mark ⚪ **N/A** (catalog-only)

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_organization_info(org_shortname)
   → Check: ordering preferences configured
   
2. get_orders(org_shortname)
   → Check: web orders exist (filter by order_source if available)
```

---

## Stage 11: Sales Portal Data Configuration

**Goal:** Sales data imported and displaying accurately

**Applies to:** eCat iPad ⚪ | eCat Online ⚪ | Sales Portal ✅

### Critical Blockers (Must Pass)
- [ ] Sales Portal functionality enabled
- [ ] Invoice data imported
- [ ] Order data imported
- [ ] Import completed without critical errors

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_organization_info(org_shortname)
   → Check: enable_portal_dashboard = true
   
2. get_import_events(org_shortname)
   → Filter: Portal imports
   → Check: No critical errors
```

---

## Stage 12: Sales Portal User Access

**Goal:** Reps and customers can access sales data appropriate to role

**Applies to:** eCat iPad ⚪ | eCat Online ⚪ | Sales Portal ✅

### Critical Blockers (Must Pass)
- [ ] User groups with portal access permissions
- [ ] Territory assignments correct
- [ ] At least 1 rep user verified

### How to Validate (V12 MANDATORY)
```
REQUIRED TOOL CALLS:
1. get_permissions_summary(org_shortname)
   → Check: portal access configured
   
2. get_user_territories(org_shortname)
   → Check: territory structure exists
   
3. analyze_user_permissions(org_shortname, user_id)
   → Verify: sample rep sees correct data
```

---

# VALIDATION LAYER (MANDATORY)

## Layer 2: Fathom + Help Scout Cross-Check

**V12 REQUIREMENT:** This layer is MANDATORY for ALL clients. No skip conditions.

### Flag Types

| Flag | Meaning | Action |
|------|---------|--------|
| 🔴 CONTRADICT | Evidence contradicts system data | Investigate immediately |
| 🔴 BLOCKER | System data shows critical gap | Cannot proceed |
| 🔴 STALLED | Implementation on hold (verified by call summary, NOT title) | Reactivate before proceeding |
| 🔴 SENTIMENT | Negative client sentiment detected | Executive escalation |
| ⚠️ REVIEW | Potential issue needs clarification | CSM follow-up |
| ⚠️ TIMELINE | Missed or at-risk deadline | Update target |
| ⚠️ ACTIVITY | Low/no engagement | Confirm client status |
| ⚠️ UNFULFILLED | Commitment not delivered | CSM verify |
| ✅ CONFIRMED | Layer 2 validates Layer 1 | Proceed confidently |

### Confidence Scoring

| Layer 1 | Layer 2 | Confidence |
|---------|---------|------------|
| 🟢 GREEN | ✅ CONFIRMED | **95%+** |
| 🟢 GREEN | No flags | **80%** |
| 🟢 GREEN | ⚠️ REVIEW | **60%** |
| 🟢 GREEN | 🔴 CONTRADICT | **30%** |
| Any | ❓ UNKNOWN | **0%** - Manual verification required |

### ⚠️ CRITICAL: "[Hold]" Is NOT a Status Indicator

**"[Hold]" in meeting titles is a CALENDAR PLACEHOLDER** for recurring meetings.

| Title Pattern | What It Means | What To Do |
|---------------|---------------|------------|
| "[Hold] Client Standup" | Recurring meeting placeholder | **GET SUMMARY** - may show active progress |
| Any title with "[Hold]" | Calendar hold, NOT implementation hold | **NEVER assume paused** |

**ALWAYS retrieve `get_summary()` for every call. NEVER assume status from title.**

---

# OUTPUT FORMAT (V12 Required)

## Per-Client Assessment Template

```markdown
# [CLIENT_NAME] ([SHORTNAME]) - V12 Assessment

**Assessment Date:** [DATE]
**Assessed By:** Cursor AI (V12 Accuracy Mode)
**Products:** [eCat iPad / eCat Online / Sales Portal]

---

## Tool Call Verification ✅

| Phase | Tool Call | Status | Response |
|-------|-----------|--------|----------|
| MCP | `get_organization_info(org="[X]")` | ✅ | Name: [X], Status: [X] |
| MCP | `get_data_summary(org="[X]")` | ✅ | Products: [X], Customers: [X] |
| MCP | `get_price_levels(org="[X]")` | ✅ | [X] levels found |
| BigQuery | iPad Activity | ✅ | [X] orders, [X] users |
| BigQuery | Help Scout | ✅ | [X] tickets found |
| Fathom | `get_meetings()` | ✅ | [X] calls found |
| Fathom | `get_summary([ID])` | ✅ | Summary retrieved |

---

## Stage Assessment

| Stage | Status | Evidence | Source |
|-------|--------|----------|--------|
| 1 - Account Foundation | 🟢 | Active org, 3 admins | `get_organization_info`, `get_org_users` |
| 2 - Catalog Setup | 🟢 | 2,657 products, 76 categories | `get_data_summary.counts.products` |
| 3 - Pricing | 🟢 | 3 price levels configured | `get_price_levels.length` |
| 4 - Options | ⚪ N/A | 0 options (feature disabled) | `get_options.length = 0` |
| 5 - Customers/Users | 🟢 | 351 customers, 23 users | `get_data_summary.counts` |
| 6 - Operational Data | 🟢 | 329 inventory records | `get_data_summary.counts.inventories` |
| 7 - iPad Ready | 🟢 | 149 iPad orders | `BigQuery: ipad_orders` |

**Overall Readiness:** [X]% | Stage [X] of [Y]

---

## Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 8 | ⚠️ REVIEW | Help Scout #13785 (Jan 8) | *"eCat Online catalogue not showing the latest trade names"* |

---

## Key Metrics Summary

| Metric | Value | Source |
|--------|-------|--------|
| Products | 2,657 | `get_data_summary.counts.products` |
| Customers | 351 | `get_data_summary.counts.customers` |
| Users | 23 | `get_data_summary.counts.org_users` |
| Price Levels | 3 | `get_price_levels.length` |
| Options | 0 | `get_options.length` |
| Inventories | 329 | `get_data_summary.counts.inventories` |
| Total Orders | 397 | `get_data_summary.counts.orders` |
| iPad Orders | 149 | `BigQuery: mixpanel_order_submitted` |
| Days Active | 204 | Calculated from `basic_info.created_at` |

---

## Next Action

🎯 **[Single, specific action item]**
```

---

# PRE-OUTPUT VALIDATION CHECKLIST

Before presenting ANY output, verify:

## Data Integrity Checks
- [ ] Every numeric value came from a tool call (not estimated)
- [ ] Source attribution exists for every metric
- [ ] No two different fields have identical values (red flag for copy error)
- [ ] Days Active calculated from actual date (not estimated)

## Tool Call Verification
- [ ] `get_organization_info` returned success
- [ ] `get_data_summary` returned success
- [ ] `get_price_levels` returned success
- [ ] BigQuery iPad query executed (not skipped)
- [ ] BigQuery Help Scout query executed (not skipped)
- [ ] Fathom `get_meetings()` executed (not skipped)
- [ ] Fathom `get_summary()` called for recent calls

## Anti-Hallucination Checks
- [ ] No metrics marked as "~" or "approximately"
- [ ] No metrics copied from user-provided documents
- [ ] No metrics inferred from context
- [ ] Failed queries marked as ❓ QUERY FAILED (not substituted)

---

# COMMON MISTAKES TO AVOID

### Mistake 1: Generating Data Without Tool Calls
**Problem:** Producing plausible-looking numbers without actually calling MCP/BigQuery
**Why it fails:** Numbers will be fabricated and incorrect
**Solution:** EVERY metric requires a tool call. Show the call in output.

### Mistake 2: Using Wrong Org Shortname
**Problem:** Querying "jcusa" when client refers to "jc" (different entities)
**Why it fails:** Returns data for wrong organization entirely
**Solution:** Verify org shortname in first tool call, confirm name matches expected client

### Mistake 3: Counting Schema Columns Instead of Data
**Problem:** Reporting "15 options" because schema has 15 option_group columns
**Why it fails:** Schema columns ≠ actual option records
**Solution:** Count the RECORDS returned by `get_options`, not schema fields

### Mistake 4: Skipping Validation Because Status Looks Obvious
**Problem:** Not running Fathom/Help Scout because MCP data looks good
**Why it fails:** Qualitative issues (blockers, timeline, sentiment) won't be detected
**Solution:** V12 has NO skip conditions. All validation is mandatory.

### Mistake 5: Assuming Status From Meeting Titles
**Problem:** Seeing "[Hold]" and assuming implementation is paused
**Why it fails:** "[Hold]" is a calendar placeholder, not a status indicator
**Solution:** ALWAYS get call summary. NEVER assume from title.

### Mistake 6: Not Attributing Data Sources
**Problem:** Presenting metrics without showing where they came from
**Why it fails:** Cannot verify accuracy or debug errors
**Solution:** Every metric must include `[Source: endpoint.field]`

---

## MCP Endpoints Reference

| Endpoint | Purpose | Stages |
|----------|---------|--------|
| `get_organization_info` | Org status, settings, templates | 1, 7, 8, 9, 10, 11, 12 |
| `get_org_users` | User configuration | 1, 5, 9 |
| `get_data_summary` | All counts in one call | 2, 5, 6 |
| `get_price_levels` | Pricing setup | 3 |
| `get_categories` | Taxonomy | 2 |
| `get_collections` | Product organization | 2 |
| `get_options` | Options (count records, not columns) | 4 |
| `get_user_territories` | Territory validation | 5, 12 |
| `get_import_events` | Data health | 6, 11 |
| `get_smart_stacks` | Smart list config | 6 |
| `get_inventories` | Inventory data | 6 |
| `get_mobile_sites` | eCat Online site config | 7, 8 |
| `get_reports_config` | Report formats | 7 |
| `get_orders` | Order validation | 7, 10 |
| `get_permissions_summary` | User permissions | 5, 9, 12 |

---

## BigQuery Tables Reference

| Table | Purpose | Stage |
|-------|---------|-------|
| `mixpanel_order_submitted` | iPad activity (filter: `mp_lib='iphone'`) | 7 |
| `help_scout_tickets` | Support/Onboarding activity | All |

---

## Approvals

| Role | Name | Date | Status |
|------|------|------|--------|
| **Author** | Kylor Johnson | Jan 14, 2026 | ✅ Complete (V12) |
| **CS Lead** | [Name] | [Date] | ⏳ Pending |
| **Engineering Lead** | [Name] | [Date] | ⏳ Pending |
| **Product Manager** | [Name] | [Date] | ⏳ Pending |

---

**Document Status:** Production Ready  
**Version:** 12.0 (Accuracy Mode + Anti-Hallucination + Mandatory Tool Verification)  
**Last Updated:** January 14, 2026  
**Contact:** Kylor Johnson

---

## Version Comparison: V11 vs V12

| Aspect | V11 (Fast Mode) | V12 (Accuracy Mode) |
|--------|-----------------|---------------------|
| **Priority** | Speed (4-5 min/client) | Accuracy (15-25 min/client) |
| **Accuracy Target** | 85% | **100%** |
| **Skip Conditions** | Yes (obvious status) | **None** |
| **Tool Call Verification** | Not required | **Mandatory** |
| **Source Attribution** | Optional | **Required** |
| **Anti-Hallucination Rules** | None | **Explicit** |
| **Fathom Validation** | Tiered/Conditional | **All Tiers Mandatory** |
| **Help Scout** | Mandatory | **Mandatory** |
| **Pre-Output Checklist** | None | **Required** |
| **Failed Query Handling** | Substitute estimate | **Mark as ❓ QUERY FAILED** |
