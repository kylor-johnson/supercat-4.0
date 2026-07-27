# Stage-Gated Onboarding Playbook V12

**Author:** Kylor Johnson  
**Date:** January 14, 2026  
**Version:** 12.0 (Unified Operational Playbook)  
**Status:** Production Ready

---

## Document Purpose

This is a **single unified document** for executing Stage-Gated Onboarding Readiness Assessments. It combines:
- **Execution Protocol** (anti-hallucination, tool verification)
- **Stage-by-Stage Checklist** (what to validate)
- **Output Templates** (exact format for Notion)

**Load this one file. Execute exactly as written. Copy output to Notion.**

---

# PART 1: EXECUTION PROTOCOL

## ⛔ CRITICAL: ANTI-HALLUCINATION RULES

### The Problem This Solves

In V11 testing, the LLM hallucinated metrics that looked plausible but were completely fabricated:
- CST inventory reported as 79,665 when actual was 4,821 (16.5x error)
- DCCL options reported as 15 when actual was 2 (7.5x error)
- Orders, customers, and users routinely fabricated

**Root Cause:** V11 allowed the model to skip tool calls and didn't require proof of query execution.

### Mandatory Rules

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
Every metric in output MUST be retrievable from a specific tool call.

#### Rule 4: No Skip Conditions
ALL validation phases are mandatory. No exceptions for "obvious" status.

---

## STEP 0: CLIENT DISCOVERY (HubSpot Source of Truth)

**⚠️ CRITICAL:** Do NOT use MCP `status` field to find onboarding clients. It is unreliable.

**HubSpot is the authoritative source** for identifying which clients are in active onboarding.

### Why HubSpot, Not MCP?

| Source | Field | Reliability | Issue |
|--------|-------|-------------|-------|
| MCP | `org.status` | ❌ Unreliable | Shows "inactive" for actively implementing clients (e.g., Coaster) |
| HubSpot | `lifecyclestage = 'evangelist'` | ✅ Accurate | Actively managed, reflects real engagement status |

### Query: Get All Onboarding Clients

```python
import json
import urllib.request
import ssl

ACCESS_TOKEN = 'REDACTED'  # HubSpot PAT removed before public commit
BASE_URL = "https://api.hubapi.com"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def hubspot_post(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    req_data = json.dumps(data).encode('utf-8')
    request = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    with urllib.request.urlopen(request, context=ssl_context, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))

# Get all companies in "Onboarding" lifecycle stage
# Internal HubSpot value: "evangelist" = "Onboarding" in UI
search_data = {
    'filterGroups': [{
        'filters': [{
            'propertyName': 'lifecyclestage',
            'operator': 'EQ',
            'value': 'evangelist'
        }]
    }],
    'properties': ['name', 'domain', 'hs_date_entered_evangelist'],
    'limit': 100
}

result = hubspot_post('/crm/v3/objects/companies/search', search_data)
companies = result.get('results', [])

print(f"Found {len(companies)} companies in Onboarding:")
for c in companies:
    props = c.get('properties', {})
    print(f"  - {props.get('name')} | {props.get('domain')} | Entered: {props.get('hs_date_entered_evangelist', 'N/A')[:10] if props.get('hs_date_entered_evangelist') else 'N/A'}")
```

### Mapping HubSpot Company to MCP Org Shortname

| HubSpot Name | Domain | MCP Shortname |
|--------------|--------|---------------|
| Magic Lite | magiclite.com | mali |
| Donald Choi Canada | donaldchoi.com | dccl |
| Coaster Fine Furniture | coasterfurniture.com | cst |
| Terracotta Designs | terracottalighting.com | tcd |
| Kaleen Rugs, Inc. | kaleen.com | krb |
| Jonathan Charles | jonathancharlesus.com | jc |
| Pebl Furniture | peblfurniture.com | pebl |

### Batch Assessment Flow

1. **Query HubSpot** → Get companies where `lifecyclestage = 'evangelist'`
2. **Map to MCP shortnames** → Use domain/name mapping
3. **Run MCP/BigQuery/Fathom** → For each mapped shortname
4. **Compile Output** → Pipeline overview sorted by readiness

---

## Tool Call Verification Requirements

Before presenting output, you MUST have executed:

### HubSpot Query (FOR BATCH ASSESSMENTS)
- [ ] Query `lifecyclestage = 'evangelist'` to get active onboarding clients

### MCP Queries (ALL REQUIRED per client)
- [ ] `get_organization_info(org_shortname)` 
- [ ] `get_data_summary(org_shortname)`
- [ ] `get_org_users(org_shortname)`
- [ ] `get_price_levels(org_shortname)`
- [ ] `get_categories(org_shortname)`
- [ ] `get_collections(org_shortname)`
- [ ] `get_options(org_shortname)`
- [ ] `get_user_territories(org_shortname)`
- [ ] `get_import_events(org_shortname)`
- [ ] `get_inventories(org_shortname)`
- [ ] `get_mobile_sites(org_shortname)`
- [ ] `get_reports_config(org_shortname)`
- [ ] `get_orders(org_shortname)`
- [ ] `get_permissions_summary(org_shortname)`

### BigQuery Queries (ALL REQUIRED)
- [ ] iPad Activity Query (MixPanel)
- [ ] Help Scout Support Tickets Query
- [ ] Help Scout Onboarding Tickets Query

### Fathom API (ALL REQUIRED)
- [ ] `get_meetings()` filtered by client
- [ ] `get_summary()` for EACH relevant call
- [ ] Transcript check if summary insufficient

---

## Pre-Output Validation Checklist

Before presenting ANY output, verify:

### Data Integrity Checks
- [ ] Every numeric value came from a tool call (not estimated)
- [ ] No two different fields have identical values (red flag for copy error)
- [ ] Days Active calculated from actual `created_at` date
- [ ] Stage assessments match tool call evidence

### Anti-Hallucination Checks
- [ ] No metrics marked as "~" or "approximately"
- [ ] No metrics copied from user-provided documents
- [ ] No metrics inferred from context
- [ ] Failed queries marked as ❓ QUERY FAILED (not substituted)

---

# PART 2: FATHOM & HELP SCOUT VALIDATION (ENHANCED)

## ⚠️ CRITICAL: 100% Certainty Required

Before stating "no recent calls" or "no tickets found", you MUST be 100% certain.

---

## Fathom API Validation Protocol

### Step 1: Get ALL Meetings (MANDATORY)

```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'fathom'))
from fathom_api import get_meetings

meetings = get_meetings()
for m in sorted(meetings, key=lambda x: x.get('recording_start_time', ''), reverse=True)[:50]:
    print(f\"{m.get('recording_id')} | {m.get('recording_start_time', '')[:10]} | {m.get('meeting_title')}\")
"
```

### Step 2: Filter for Client (MULTI-CRITERIA)

Search meeting titles for ANY of these patterns:
1. **Client name** (full or abbreviated)
2. **Client shortname** (org shortname)
3. **Keywords:** "implementation", "onboarding", "support", "training", "kickoff", "standup"
4. **DO NOT SKIP:** "[Hold]" titles - this is a calendar placeholder for recurring meetings, NOT a status

```python
# Example filtering logic
clients = ['client_name', 'shortname', 'alternate_names', 'common_abbreviations']
keywords = ['implementation', 'onboarding', 'support', 'training', 'kickoff', 'standup', 'demo']

relevant = [m for m in meetings 
            if any(c.lower() in m.get('meeting_title', '').lower() for c in clients)
            or any(k.lower() in m.get('meeting_title', '').lower() for k in keywords)]
```

### Step 3: Check Invite Lists (MANDATORY FOR UNCERTAIN MATCHES)

For meetings where title doesn't clearly indicate client:
```bash
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'fathom'))
from fathom_api import get_summary

summary = get_summary([RECORDING_ID])
# Check attendees for client email domains
attendees = summary.get('attendees', [])
for a in attendees:
    print(f\"Attendee: {a.get('email', 'N/A')}\")
"
```

**Match email domains to client.** Example: `@coaster.com` for Coaster, `@donaldchoi.com` for DCCL

### Step 4: Get Summary AND Transcript (MANDATORY)

For EACH relevant call in the last 90 days:

```bash
# Get Summary
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'fathom'))
from fathom_api import get_summary

summary = get_summary([RECORDING_ID])
print('=== SUMMARY ===')
print(summary.get('summary', {}).get('markdown_formatted', '')[:3000])
print('=== ACTION ITEMS ===')
for item in summary.get('action_items', []):
    print(f\"- {item.get('content', '')}\")
"

# Get Transcript (if summary insufficient)
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'fathom'))
from fathom_api import get_transcript

transcript = get_transcript([RECORDING_ID])
print(transcript[:5000])
"
```

### Step 5: Document ALL Relevant Calls

**Index toward including more calls, not fewer.** If a call MIGHT be relevant, include it.

| Call ID | Date | Title | Relevance Reason |
|---------|------|-------|------------------|
| [ID] | [Date] | [Title] | Client name in title / Keyword match / Email domain match |

### Fathom "No Calls" Certification

Before stating "No Fathom calls found", you MUST certify:
- [ ] Searched last 90 days of ALL meetings
- [ ] Checked for client name, shortname, and abbreviations in titles
- [ ] Checked for implementation/onboarding/support keywords
- [ ] Checked invite lists for matching email domains on ambiguous titles
- [ ] Verified "[Hold]" meetings are NOT skipped (they're recurring placeholders)

---

## Help Scout Validation Protocol

### ⚠️ CRITICAL: Search BOTH Inboxes, BOTH Statuses

Help Scout has TWO mailboxes:
1. **Support** (support@supercatsolutions.com)
2. **Onboarding** (onboarding@supercatsolutions.com)

Help Scout has TWO status types:
1. **Open/Active** tickets
2. **Closed** tickets

**YOU MUST QUERY ALL FOUR COMBINATIONS.**

### Query 1: Support Inbox - All Statuses

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
       OR LOWER(ticket_subject) LIKE '%[CLIENT_PATTERN]%'
       OR LOWER(ticket_preview) LIKE '%[CLIENT_PATTERN]%')
  AND LOWER(ticket_mailbox_name) LIKE '%support%'
  AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY ticket_created_at DESC
LIMIT 25
```

### Query 2: Onboarding Inbox - All Statuses

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
       OR LOWER(ticket_subject) LIKE '%[CLIENT_PATTERN]%'
       OR LOWER(ticket_preview) LIKE '%[CLIENT_PATTERN]%')
  AND LOWER(ticket_mailbox_name) LIKE '%onboarding%'
  AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY ticket_created_at DESC
LIMIT 25
```

### Query 3: Combined Query (Alternative)

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
       OR LOWER(ticket_subject) LIKE '%[CLIENT_PATTERN]%'
       OR LOWER(ticket_preview) LIKE '%[CLIENT_PATTERN]%')
  AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY)
ORDER BY ticket_created_at DESC
LIMIT 50
```

### Search Patterns to Use

For each client, search using MULTIPLE patterns:
- Full company name: `%coaster furniture%`
- Short name: `%coaster%`
- Org shortname: `%cst%`
- Contact names if known
- Product names if unique

### Document ALL Relevant Tickets

**Index toward including more tickets, not fewer.** If a ticket MIGHT be relevant, include it.

| # | Date | Subject | Mailbox | Status | Relevance |
|---|------|---------|---------|--------|-----------|
| [#] | [Date] | [Subject] | Support/Onboarding | Open/Closed | [Why relevant] |

### Help Scout "No Tickets" Certification

Before stating "No Help Scout tickets found", you MUST certify:
- [ ] Queried BOTH Support AND Onboarding mailboxes
- [ ] Queried BOTH Open AND Closed tickets
- [ ] Searched by company name, shortname, AND org shortname
- [ ] Searched ticket subject AND preview text
- [ ] Extended search to 180 days if 90 days returns nothing

---

# PART 3: STAGE-BY-STAGE CHECKLIST

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

## FOUNDATION STAGES (1-6) - Required for ALL Products

---

### Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

#### Checklist
- [ ] Company name filled in
- [ ] At least 1 admin user exists (excluding: Kylor_Johnson, brentsanders, cwiebe)
- [ ] Settings initialized with defaults

#### Pass Criteria
- 🔴 **RED (BLOCKER):** Any item above unchecked
- 🟢 **GREEN (READY):** All items checked

#### How to Validate
```
REQUIRED TOOL CALLS:
1. get_organization_info(org_shortname) 
   → Check: basic_info.name is not empty
   → Check: basic_info.status = "active"
   
2. get_org_users(org_shortname)
   → Check: At least 1 user with is_admin: true
   → Check: Admin is not internal test user
```

---

### Stage 2: Catalog Setup

**Goal:** Products imported and browsable by users

#### Checklist
- [ ] At least 10 products imported
- [ ] At least 10 products have images
- [ ] At least 1 category configured
- [ ] At least 1 collection exists
- [ ] Products updated within last 30 days

#### Pass Criteria
- 🔴 **RED (BLOCKER):** Less than 10 products imported
- 🟡 **YELLOW (WARNING):** 10-100 products OR no updates in 60+ days
- 🟢 **GREEN (READY):** 100+ products AND updated within last 30 days

#### How to Validate
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

---

### Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

#### Checklist
- [ ] Price levels configured
- [ ] At least 2 price levels configured (recommended)
- [ ] Price levels have descriptive names, not "Price Level 1"
- [ ] Price level codes assigned (recommended)

#### Pass Criteria
- 🔴 **RED (BLOCKER):** No price levels configured
- 🟡 **YELLOW (WARNING):** Only 1 price level OR generic names
- 🟢 **GREEN (READY):** 2+ price levels with descriptive names

#### How to Validate
```
REQUIRED TOOL CALLS:
1. get_price_levels(org_shortname)
   → Count: number of price levels
   → Extract: names and codes for each level
   → Check: names are not generic defaults
```

---

### Stage 4: Option Configuration (CONDITIONAL)

**Goal:** If options enabled, CPQ/configurators are functional

#### Check if Stage Applies
- Run `get_options(org_shortname)`
- If returns 0 options → Mark ⚪ **N/A**, skip to Stage 5
- If returns 1+ options → Continue with checklist

#### Pass Criteria
- ⚪ **N/A:** Options disabled (0 options returned)
- 🔴 **RED (BLOCKER):** Options enabled but broken
- 🟡 **YELLOW (WARNING):** Less than 5 options configured
- 🟢 **GREEN (READY):** 5+ options configured

#### How to Validate
```
REQUIRED TOOL CALLS:
1. get_options(org_shortname)
   → Count: ACTUAL number of option RECORDS returned
   → NOT the number of option_group columns in schema
   
⚠️ CRITICAL: Count the OPTIONS returned, not schema columns
```

---

### Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

#### Checklist
- [ ] At least 10 customers imported
- [ ] At least 2 users configured
- [ ] Multiple user types exist
- [ ] Customers updated within last 30 days

#### Pass Criteria
- 🔴 **RED (BLOCKER):** Less than 10 customers OR no users configured
- 🟡 **YELLOW (WARNING):** 10-100 customers OR no updates in 30+ days
- 🟢 **GREEN (READY):** 100+ customers AND updated within last 30 days

#### How to Validate
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

### Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

#### Checklist
- [ ] No critical import errors in last 30 days
- [ ] Smart stacks configured OR feature disabled
- [ ] Inventory data exists (if tracking enabled)
- [ ] Inventory updated within last 7 days (if tracking enabled)

#### Pass Criteria
- 🔴 **RED (BLOCKER):** Inventory enabled but no data OR critical import errors
- 🟡 **YELLOW (WARNING):** Stale inventory (7+ days) OR minor warnings
- 🟢 **GREEN (READY):** Fresh data AND no import errors

#### How to Validate
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

## eCAT iPAD STAGE (7)

### Stage 7: iPad Order-Ready

**Goal:** iPad app can receive, process, and fulfill orders end-to-end

**Applies to:** eCat iPad ✅ | eCat Online ⚪ | Sales Portal ⚪

#### Critical Blockers (Must Pass)
- [ ] 1+ user types exist (more than Default User Group)
- [ ] iPad app activity exists (at least 1 order from iPad)
- [ ] Report formats configured (minimum 3)
- [ ] Test order processed (at least 1 order exists)

#### Recommended (Should Pass)
- [ ] Order notification email configured
- [ ] Export type configured (if ERP integration needed)

#### Pass Criteria
- ⚪ **N/A:** eCat iPad not being implemented
- 🔴 **RED (BLOCKER):** Any critical blocker unchecked
- 🟡 **YELLOW (WARNING):** Critical blockers pass but recommended missing
- 🟢 **GREEN (READY):** All criteria pass

#### How to Validate
```
REQUIRED TOOL CALLS:
1. get_reports_config(org_shortname)
   → Count: report formats (must be ≥3)
   
2. get_orders(org_shortname)
   → Count: total orders
   
3. get_organization_info(org_shortname)
   → Check: order_email_recipient is configured

REQUIRED BIGQUERY:
4. iPad Activity Query
   SELECT COUNT(*) as ipad_order_count,
          COUNT(DISTINCT distinct_id) as unique_ipad_users
   FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.mixpanel_order_submitted`
   WHERE currentorganizationshortname = '[ORG_SHORTNAME]'
     AND mp_lib = 'iphone'
```

---

## eCAT ONLINE STAGES (8-10)

### Stage 8: eCat Online Site Configuration

**Goal:** Web catalog is accessible and properly branded

**Applies to:** eCat iPad ⚪ | eCat Online ✅ | Sales Portal ✅

#### Critical Blockers (Must Pass)
- [ ] eCat Online site created and enabled
- [ ] Site name configured (not default)
- [ ] Public user group exists with permissions

#### Recommended (Should Pass)
- [ ] Home page logo uploaded
- [ ] Custom domain configured (CNAME)

#### Pass Criteria
- ⚪ **N/A:** eCat Online not being implemented
- 🔴 **RED (BLOCKER):** No site exists OR site disabled
- 🟡 **YELLOW (WARNING):** Site exists but missing branding
- 🟢 **GREEN (READY):** Site enabled with custom branding

#### How to Validate
```
REQUIRED TOOL CALLS:
1. get_mobile_sites(org_shortname)
   → Check: enabled = true
   → Check: site_name is configured
   
2. get_permissions_summary(org_shortname)
   → Check: public user group exists
```

---

### Stage 9: eCat Online User Access & Enrollment

**Goal:** Users can access the catalog via enrollment or invitation

**Applies to:** eCat iPad ⚪ | eCat Online ✅ | Sales Portal ✅

#### Pass Criteria
- ⚪ **N/A:** eCat Online not being implemented
- 🔴 **RED (BLOCKER):** Closed site with no enrollment workflow
- 🟡 **YELLOW (WARNING):** Default templates not customized
- 🟢 **GREEN (READY):** Enrollment workflow functional

#### How to Validate
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

### Stage 10: eCat Online Ordering (B2B Cart) - CONDITIONAL

**Goal:** If B2B ordering enabled, customers can place orders through web

**Applies to:** eCat iPad ⚪ | eCat Online ✅ (conditional) | Sales Portal ⚪

#### Pass Criteria
- ⚪ **N/A:** B2B ordering not enabled (catalog-only)
- 🔴 **RED (BLOCKER):** Ordering enabled but no test order
- 🟢 **GREEN (READY):** Test orders submitted via web

---

## SALES PORTAL STAGES (11-12)

### Stage 11: Sales Portal Data Configuration

**Goal:** Sales data imported and displaying accurately

**Applies to:** eCat iPad ⚪ | eCat Online ⚪ | Sales Portal ✅

#### Critical Blockers (Must Pass)
- [ ] Sales Portal functionality enabled
- [ ] Invoice data imported
- [ ] Order data imported
- [ ] Import completed without critical errors

#### Pass Criteria
- ⚪ **N/A:** Sales Portal not being implemented
- 🔴 **RED (BLOCKER):** Portal enabled but no data
- 🟡 **YELLOW (WARNING):** Less than 12 months history
- 🟢 **GREEN (READY):** Clean import with 12+ months

#### How to Validate
```
REQUIRED TOOL CALLS:
1. get_organization_info(org_shortname)
   → Check: enable_portal_dashboard = true
   
2. get_import_events(org_shortname)
   → Filter: Portal imports
   → Check: No critical errors
```

---

### Stage 12: Sales Portal User Access

**Goal:** Reps and customers can access sales data appropriate to role

**Applies to:** eCat iPad ⚪ | eCat Online ⚪ | Sales Portal ✅

#### Critical Blockers (Must Pass)
- [ ] User groups with portal access permissions
- [ ] Territory assignments correct
- [ ] At least 1 rep user verified

#### Pass Criteria
- ⚪ **N/A:** Sales Portal not being implemented
- 🔴 **RED (BLOCKER):** No users can access portal
- 🟡 **YELLOW (WARNING):** Only admin users can see data
- 🟢 **GREEN (READY):** Reps see their territory data correctly

#### How to Validate
```
REQUIRED TOOL CALLS:
1. get_permissions_summary(org_shortname)
   → Check: portal access configured
   
2. get_user_territories(org_shortname)
   → Check: territory structure exists
```

---

# PART 4: VALIDATION LAYER

## Flag Types

| Flag | Meaning | Action |
|------|---------|--------|
| 🔴 CONTRADICT | Evidence contradicts system data | Investigate immediately |
| 🔴 BLOCKER | System data shows critical gap | Cannot proceed |
| 🔴 STALLED | Implementation on hold (verify in call summary) | Reactivate before proceeding |
| 🔴 SENTIMENT | Negative client sentiment detected | Executive escalation |
| ⚠️ REVIEW | Potential issue needs clarification | CSM follow-up |
| ⚠️ TIMELINE | Missed or at-risk deadline | Update target |
| ⚠️ ACTIVITY | Low/no engagement | Confirm client status |
| ⚠️ UNFULFILLED | Commitment not delivered | CSM verify |
| ⚠️ MEETING | Meeting scheduled/pending | Track follow-up |
| ✅ ACTIVE | Active engagement confirmed | Continue progress |
| ✅ CONFIRMED | Layer 2 validates Layer 1 | Proceed confidently |

---

## Confidence Scoring

| Layer 1 (MCP) | Layer 2 (Fathom/HS) | Confidence |
|---------------|---------------------|------------|
| 🟢 GREEN | ✅ CONFIRMED | **95%+** |
| 🟢 GREEN | No flags | **80%** |
| 🟢 GREEN | ⚠️ REVIEW | **60%** |
| 🟢 GREEN | 🔴 CONTRADICT | **30%** |
| Any | ❓ UNKNOWN | **0%** - Manual verification required |

---

## ⚠️ CRITICAL: "[Hold]" Is NOT a Status Indicator

**"[Hold]" in meeting titles is a CALENDAR PLACEHOLDER** for recurring meetings.

| Title Pattern | What It Means | What To Do |
|---------------|---------------|------------|
| "[Hold] Client Standup" | Recurring meeting placeholder | **GET SUMMARY** - may show active progress |
| Any title with "[Hold]" | Calendar hold, NOT implementation hold | **NEVER assume paused** |

**ALWAYS retrieve `get_summary()` for every call. NEVER assume status from title.**

---

## Key Contradiction Keywords to Search

In Fathom summaries and Help Scout tickets, search for:
- "test data", "sample products", "placeholder"
- "re-import", "clobbered", "wrong data"
- "not ready", "haven't tested", "not set up yet"
- "disappointed", "frustrated", "cancel"
- Timeline indicators: specific dates, "by end of week", "next month"

---

# PART 5: OUTPUT TEMPLATES

## ⚠️ CRITICAL: Use These Exact Formats

The output must be copy-paste ready for Notion. Follow these templates exactly.

---

## Pipeline Overview Table

```markdown
## **Pipeline Overview**

| Client | Product | Owner | V12 Stage | V12 Readiness | Key Flag | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **[SHORTNAME]** | [Product] | [Owner] | [X] / [Y] | [X]% | [Key issue] | [Specific blocker] | [🔴/⚠️/✅] [X] flags | [X] |
```

**Column Definitions:**
- **Client:** Org shortname in bold
- **Product:** eCat / eOL / Sales Portal
- **Owner:** CSM name (Brent/Chuck)
- **V12 Stage:** Current stage / Total stages for product
- **V12 Readiness:** Percentage (calculate from stages passed)
- **Key Flag:** Primary risk or status indicator
- **Biggest Blocker:** Specific issue preventing advancement
- **Validation Status:** 🔴/⚠️/✅ + flag count
- **Days Active:** From created_at to today

---

## Pipeline Visualization

```markdown
## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

[SHORT] ██░░░░░░░░░░░░░░░░░░ 10%  Stage X - [Name]    🔴 STALLED

[SHORT] █████░░░░░░░░░░░░░░░ 25%  Stage X - [Name]    🔴 FLAGGED

[SHORT] ████████░░░░░░░░░░░░ 40%  Stage X - [Name]    ⚠️ ACTIVE ENGAGEMENT

[SHORT] ████████████░░░░░░░░ 60%  Stage X - [Name]    ⚠️ FLAGGED

[SHORT] ██████████████░░░░░░ 70%  Stage X - [Name]    ⚠️ SUPPORT ACTIVE

[SHORT] █████████████████░░░ 85%  Stage X - [Name]    ⚠️ MARKET PREP

[SHORT] ███████████████████░ 95%  Stage X - [Name]    ✅ CONFIRMED

═══════════════════════════════════════════════════════════════════
```

**Progress Bar Calculation:**
- Each █ = 5%
- 20 characters total
- Round to nearest 5%

---

## Per-Client Assessment Template

```markdown
---

## **[SHORTNAME] ([Full Company Name])**

**V12 Assessment:** Stage [X] | [X]% Ready | Products: [Product list]

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟢 | [X] products |
| 3 | 🔴 | **[X] price levels** (Stage 3 criteria: [explanation]) |
| 4 | ⚪ N/A | Options not configured |
| 5 | 🔴 | **[X] customers** (Stage 5 criteria: [explanation]) |
| 6 | 🔴 | **[X] inventory** |
| 7 | 🔴 | No orders |

**🎯 V12 Next Action:** [Specific action item]

**[🔴/⚠️/✅] Validation Flags ([X])**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| [X] | [🔴/⚠️/✅] [TYPE] | [Fathom/Help Scout] [Date/ID] | "[Exact quote or description]" |

**Validation Summary:** [2-3 sentence summary of client status, key risks, and recommended action]

---
```

---

## Validation Flags Summary Template

```markdown
---

## **Validation Flags Summary**

**🔴 Critical Flags (Require Immediate Action)**

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| [SHORT] | [X] | [Issue description] | "[Quote]" | [Required action] |

**⚠️ Review Flags (Need Clarification)**

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| [SHORT] | [X] | [Issue description] | "[Quote]" | [Required action] |

**✅ Confirmed (No Flags)**

| Client | V12 Stage | V12 Readiness | Status |
| --- | --- | --- | --- |
| [SHORT] | Stage [X] | [X]% | [Brief status] |

---
```

---

## Key Takeaways Template

```markdown
---

## **Key Takeaways**

**🔴 Immediate Action Required ([X] clients):**

1. **[SHORT] ([X]%)** - [Specific action needed]
2. **[SHORT] ([X]%)** - [Specific action needed]

**⚠️ Active Monitoring ([X] clients):**

1. **[SHORT] ([X]%)** - [What to monitor]
2. **[SHORT] ([X]%)** - [What to monitor]

**✅ Stable ([X] clients):**

1. **[SHORT] ([X]%)** - [Current status]
```

---

# PART 6: QUICK REFERENCE

## Stage Summary by Product

| Stage | eCat iPad | eCat Online | Sales Portal |
| --- | --- | --- | --- |
| 1 - Account Foundation | ✅ | ✅ | ✅ |
| 2 - Catalog Setup | ✅ | ✅ | ✅ |
| 3 - Pricing Configuration | ✅ | ✅ | ✅ |
| 4 - Option Configuration | ⚪ Conditional | ⚪ Conditional | ⚪ Conditional |
| 5 - Customer & User Setup | ✅ | ✅ | ✅ |
| 6 - Operational Data | ✅ | ✅ | ✅ |
| 7 - iPad Order-Ready | ✅ | ⚪ N/A | ⚪ N/A |
| 8 - eCat Online Site | ⚪ N/A | ✅ | ✅ |
| 9 - eCat Online User Access | ⚪ N/A | ✅ | ✅ |
| 10 - eCat Online Ordering | ⚪ N/A | ⚪ Conditional | ⚪ N/A |
| 11 - Sales Portal Data | ⚪ N/A | ⚪ N/A | ✅ |
| 12 - Sales Portal User Access | ⚪ N/A | ⚪ N/A | ✅ |

---

## Critical Launch Blockers by Product

### eCat iPad (Stages 1-7)
1. Price levels configured (Stage 3)
2. Customers imported (Stage 5)
3. iPad app activity exists (Stage 7)
4. Report formats configured (Stage 7)
5. Test order processed (Stage 7)

### eCat Online (Stages 1-6, 8-10)
1. Price levels configured (Stage 3)
2. Customers imported (Stage 5)
3. Site created and enabled (Stage 8)
4. Public user group exists (Stage 8)
5. Enrollment workflow configured (Stage 9, if closed site)
6. Test web order submitted (Stage 10, if B2B enabled)

### Sales Portal (Stages 1-6, 8-9, 11-12)
1. Price levels configured (Stage 3)
2. Customers imported (Stage 5)
3. Site created and enabled (Stage 8)
4. Portal functionality enabled (Stage 11)
5. Invoice data imported (Stage 11)
6. Order data imported (Stage 11)
7. Territory assignments correct (Stage 12)

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

## Common Mistakes to Avoid

### Mistake 1: Generating Data Without Tool Calls
**Problem:** Producing plausible-looking numbers without actually calling MCP/BigQuery
**Solution:** EVERY metric requires a tool call.

### Mistake 2: Using Wrong Org Shortname
**Problem:** Querying "jcusa" when client refers to "jc" (different entities)
**Solution:** Verify org shortname in first tool call, confirm name matches expected client

### Mistake 3: Counting Schema Columns Instead of Data
**Problem:** Reporting "15 options" because schema has 15 option_group columns
**Solution:** Count the RECORDS returned by `get_options`, not schema fields

### Mistake 4: Skipping Validation Because Status Looks Obvious
**Problem:** Not running Fathom/Help Scout because MCP data looks good
**Solution:** V12 has NO skip conditions. All validation is mandatory.

### Mistake 5: Assuming Status From Meeting Titles
**Problem:** Seeing "[Hold]" and assuming implementation is paused
**Solution:** ALWAYS get call summary. NEVER assume from title.

### Mistake 6: Only Checking One Help Scout Inbox
**Problem:** Only querying Support, missing Onboarding tickets
**Solution:** Query BOTH Support AND Onboarding, BOTH Open AND Closed

### Mistake 7: Saying "No Calls" Without Checking Invite Lists
**Problem:** Missing relevant calls because client name wasn't in title
**Solution:** Check attendee email domains for ambiguous meeting titles

---

## Execution Checklist

**Before running assessment:**
1. [ ] Verify org shortname with `get_organization_info`
2. [ ] Confirm MCP connection working
3. [ ] Determine product(s) being implemented

**Run MCP queries (ALL REQUIRED):**
4. [ ] Foundation data batch
5. [ ] Configuration data batch
6. [ ] Operations data batch
7. [ ] Product-specific data batch

**Run BigQuery queries (ALL REQUIRED):**
8. [ ] iPad Activity (MixPanel)
9. [ ] Help Scout - Support inbox
10. [ ] Help Scout - Onboarding inbox

**Run Fathom validation (ALL REQUIRED):**
11. [ ] Get all meetings
12. [ ] Filter by client (name + keywords + domains)
13. [ ] Get summaries for each relevant call
14. [ ] Check transcripts if needed

**Compile output:**
15. [ ] Use exact templates from Part 5
16. [ ] Verify all metrics have sources
17. [ ] Run pre-output validation checklist

---

**Document Status:** Production Ready  
**Version:** 12.0 (Unified Operational Playbook)  
**Last Updated:** January 14, 2026  
**Contact:** Kylor Johnson
