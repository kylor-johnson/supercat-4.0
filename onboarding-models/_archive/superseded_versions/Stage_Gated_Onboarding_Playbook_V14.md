# Stage-Gated Onboarding Playbook V14

**Author:** Kylor Johnson  
**Date:** January 21, 2026  
**Version:** 14.0 (100% Queryable Stages)  
**Status:** Production Ready

---

## Document Purpose

This is a **single unified document** for executing Stage-Gated Onboarding Readiness Assessments. It combines:
- **Execution Protocol** (anti-hallucination, tool verification)
- **MANDATORY Recent Activity First Protocol** (V13 FIX: Check TODAY first)
- **Stage-by-Stage Checklist** (what to validate)
- **Output Templates** (exact format for Notion)

**Load this one file. Execute exactly as written. Copy output to Notion.**

---

# 🚨 V13 CRITICAL FIX: RECENT ACTIVITY FIRST PROTOCOL

## The Problem V12 Failed to Solve

Every week, recent meetings and tickets were missed because:
1. Fathom queries were filtered too early (missing relevant meetings)
2. Help Scout queries didn't search thread_body (missing non-English subjects)
3. No mandatory "TODAY FIRST" check existed
4. No client alias registry for fuzzy matching

**V13 Solution:** BEFORE any client assessment, run the Recent Activity First protocol. This catches TODAY's activity before it gets buried.

---

## STEP -1: RECENT ACTIVITY SCAN (MANDATORY FIRST STEP)

### ⛔ THIS STEP CANNOT BE SKIPPED

Before running ANY client assessment, you MUST execute STEP -1. This is the FIRST thing that runs, every time.

### Why This Step Exists

- Magic Lite meeting TODAY? Fathom query catches it.
- Coaster standup TODAY? Fathom query catches it.
- PEBL ticket with Chinese subject? Help Scout thread_body search catches it.

**If you skip this step, you WILL miss recent activity.**

---

### 1A: Get ALL Fathom Meetings (Last 14 Days, UNFILTERED)

```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
python3 -c "
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.getcwd(), 'integrations/fathom'))
from fathom_api import get_meetings

meetings = get_meetings()
cutoff = (datetime.now() - timedelta(days=14)).isoformat()

print('='*80)
print('FATHOM MEETINGS - LAST 14 DAYS (UNFILTERED)')
print('='*80)
print(f'Total meetings in API: {len(meetings)}')
print()

for m in sorted(meetings, key=lambda x: x.get('recording_start_time', ''), reverse=True):
    start = m.get('recording_start_time', '')
    if start >= cutoff:
        date = start[:10] if start else 'N/A'
        time = start[11:16] if len(start) > 11 else ''
        rid = m.get('recording_id', 'N/A')
        title = m.get('meeting_title', 'No Title')
        duration = m.get('duration_seconds', 0) // 60
        print(f'{date} {time} | ID:{rid} | {duration}min | {title}')
"
```

**⚠️ CRITICAL:** Review EVERY meeting title. Match against the Client Alias Registry (Section 1D).

**⛔ DO NOT SKIP "[Hold]" MEETINGS:** Meetings with "[Hold]" in the title are CALENDAR PLACEHOLDERS for recurring meetings. These meetings STILL TAKE PLACE. You MUST get the summary for these meetings - they often contain the most valuable client progress information.

---

### 1B: Get ALL Help Scout Tickets (Last 14 Days, UNFILTERED)

```sql
-- Query 1: Get ALL recent tickets (unfiltered by client)
SELECT DISTINCT
  ticket_number,
  ticket_subject,
  ticket_status,
  ticket_created_at,
  conv_customer_organization,
  conv_customer_email,
  conv_creator_name,
  mailbox_name,
  LEFT(ticket_preview, 400) as preview,
  LEFT(thread_body, 500) as thread_preview
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 14 DAY)
ORDER BY ticket_created_at DESC
LIMIT 200
```

**⚠️ CRITICAL:** Review EVERY ticket. Match against the Client Alias Registry (Section 1D).

---

### 1C: Match Activity to Clients

After running 1A and 1B, you MUST output a **Recent Activity Report**:

```markdown
## 📋 RECENT ACTIVITY REPORT (Last 14 Days)

**Generated:** [TODAY'S DATE]
**Assessment Date:** [TODAY'S DATE]

### Fathom Meetings Found

| Date | Time | ID | Title | Matched Client |
|------|------|-----|-------|----------------|
| 2026-01-20 | 15:31 | 115590046 | MagicLite + Supercat Onboarding | MALI |
| 2026-01-20 | 18:31 | 115696872 | eCat x Coaster Standup | CST |
| ... | ... | ... | ... | ... |

**TODAY'S Meetings:** [X] found
**This Week's Meetings:** [X] found

### Help Scout Tickets Found

| # | Date | Subject | Email Domain | Matched Client |
|---|------|---------|--------------|----------------|
| 13859 | 2026-01-17 | [Chinese text] | @skyard.com | PEBL |
| ... | ... | ... | ... | ... |

**TODAY'S Tickets:** [X] found
**This Week's Tickets:** [X] found

### Unmatched Activity (REVIEW MANUALLY)

| Source | Date | Title/Subject | Notes |
|--------|------|---------------|-------|
| Fathom | 2026-01-18 | Internal Team Meeting | Not client-related |
| ... | ... | ... | ... |
```

**⛔ FORBIDDEN:** Proceeding to client assessments without completing this report.

---

### 1D: Client Alias Registry (MANDATORY REFERENCE)

Use this registry to match Fathom meetings and Help Scout tickets to clients:

| MCP Shortname | Full Name | Aliases | Email Domains | Key Contacts |
|---------------|-----------|---------|---------------|--------------|
| **mali** | Magic Lite | MagicLite, Magic-Lite, MALI | @magiclite.com | |
| **cst** | Coaster Furniture | Coaster, CST, Coaster Fine Furniture | @coasterfurniture.com, @coaster.com | |
| **tcd** | Terracotta Designs | Terracotta, TCD | @terracottalighting.com | |
| **pebl** | Pebl | PEBL, Pebl Furniture, SKYARD | @peblfurniture.com, @skyard.com | Jon |
| **krb** | Kaleen Rugs & Broadloom | Kaleen, KRB, Kaleen Rugs | @kaleen.com | |
| **dccl** | Donald Choi Canada | Donald Choi, DCCL | @donaldchoi.com | |
| **jc** | Jonathan Charles Fine Furniture | Jonathan Charles, JC, JCUSA | @jonathancharlesus.com, @jonathancharles.com | |

**Matching Logic:**
1. Check meeting title for ANY alias (case-insensitive)
2. Check ticket subject for ANY alias (case-insensitive)
3. Check `conv_customer_email` domain against Email Domains
4. Check `conv_customer_organization` for ANY alias
5. Check `thread_body` for ANY alias (catches non-English subjects)

**⚠️ If unsure, GET THE FATHOM SUMMARY. The attendee list will have email domains.**

---

### 1E: Get Summaries for ALL Matched Meetings

For EVERY meeting matched to a client in 1C, get the full summary:

```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
python3 -c "
import sys
import os
import json

sys.path.insert(0, os.path.join(os.getcwd(), 'integrations/fathom'))
from fathom_api import get_summary

# Replace with ACTUAL recording ID from 1A
summary = get_summary('[RECORDING_ID]')

if summary:
    print('='*80)
    print('MEETING SUMMARY')
    print('='*80)
    
    # Summary content
    if summary.get('summary'):
        s = summary.get('summary')
        if isinstance(s, dict):
            print('SUMMARY:', s.get('markdown_formatted', s.get('text', str(s)))[:3000])
        else:
            print('SUMMARY:', str(s)[:3000])
    
    # Action items
    print()
    print('ACTION ITEMS:')
    for item in summary.get('action_items', []):
        if isinstance(item, dict):
            print(f'  - {item.get(\"content\", item.get(\"text\", str(item)))}')
        else:
            print(f'  - {item}')
    
    # Attendees (for client matching)
    print()
    print('ATTENDEES:')
    for a in summary.get('attendees', []):
        if isinstance(a, dict):
            print(f'  - {a.get(\"name\", \"Unknown\")} ({a.get(\"email\", \"no email\")})')
        else:
            print(f'  - {a}')
    
    # Full JSON for debugging
    print()
    print('FULL RESPONSE KEYS:', list(summary.keys()))
"
```

**⛔ FORBIDDEN:** Stating "no recent calls" without running get_summary() on ambiguous meetings.

---

## STEP -1 COMPLETION GATE

Before proceeding to STEP 0 (Client Discovery), you MUST confirm:

```markdown
## ✅ STEP -1 COMPLETION CHECKLIST

- [ ] Ran Fathom query for ALL meetings (last 14 days, unfiltered)
- [ ] Ran Help Scout query for ALL tickets (last 14 days, unfiltered)
- [ ] Created Recent Activity Report with matched clients
- [ ] Got Fathom summaries for ALL meetings matched to target clients
- [ ] Identified TODAY's activity specifically: [X] meetings, [Y] tickets
- [ ] Listed any unmatched activity for manual review

**If ANY checkbox is unchecked, DO NOT proceed.**
```

---

# PART 1: EXECUTION PROTOCOL

## ⛔ CRITICAL: ANTI-HALLUCINATION RULES

### The Problem This Solves

In V11/V12 testing, the LLM:
- Hallucinated metrics that looked plausible but were fabricated
- Missed TODAY's meetings because queries were filtered too early
- Missed tickets with non-English subjects

**Root Cause:** V12 didn't require checking TODAY's activity FIRST.

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

#### Rule 5: STEP -1 IS MANDATORY (V13 NEW)
The Recent Activity First protocol (STEP -1) MUST run before ANY client assessment.

#### Rule 6: DO NOT USE HEALTH SCORING TOOLS (V13 NEW)
```
⛔ FORBIDDEN: Calling get_organization_health() 
⛔ FORBIDDEN: Calling get_organization_health_csv()
⛔ FORBIDDEN: Substituting health scores for stage-gated readiness

These tools are for a SEPARATE workflow (ongoing account health monitoring).
Stage-Gated Onboarding Assessment uses ONLY the endpoints in the MCP Reference.
```

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

1. **Run STEP -1** → Recent Activity First (MANDATORY)
2. **Query HubSpot** → Get companies where `lifecyclestage = 'evangelist'`
3. **Map to MCP shortnames** → Use domain/name mapping
4. **Run MCP/BigQuery** → For each mapped shortname
5. **Cross-reference STEP -1 data** → Include today's activity in assessment
6. **Compile Output** → Pipeline overview sorted by readiness

---

## Tool Call Verification Requirements

Before presenting output, you MUST have executed:

### STEP -1: Recent Activity (MANDATORY FIRST)
- [ ] Fathom: Get ALL meetings (last 14 days, unfiltered)
- [ ] Help Scout: Get ALL tickets (last 14 days, unfiltered)
- [ ] Created Recent Activity Report
- [ ] Got summaries for ALL matched meetings

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
- [ ] Help Scout Support Tickets Query (client-specific)
- [ ] Help Scout Onboarding Tickets Query (client-specific)

### Fathom API (ALL REQUIRED)
- [ ] `get_summary()` for EACH matched call from STEP -1
- [ ] Transcript check if summary insufficient

---

## Pre-Output Validation Checklist

Before presenting ANY output, verify:

### STEP -1 Validation (V13 NEW)
- [ ] Recent Activity Report was generated
- [ ] TODAY's activity count: [X] meetings, [Y] tickets
- [ ] ALL matched meetings have summaries retrieved

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

**V13 CHANGE:** The unfiltered scans in STEP -1 should catch everything. Client-specific queries here are for ADDITIONAL context only.

---

## Fathom API Validation Protocol

### Already Completed in STEP -1:
- ✅ Got ALL meetings (unfiltered)
- ✅ Matched to clients using Alias Registry
- ✅ Got summaries for matched meetings

### Additional Context (If Needed)

For meetings where client attribution is unclear:

```bash
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'integrations/fathom'))
from fathom_api import get_summary

summary = get_summary('[RECORDING_ID]')
# Check attendees for client email domains
attendees = summary.get('attendees', [])
for a in attendees:
    print(f\"Attendee: {a.get('name', 'N/A')} - {a.get('email', 'N/A')}\")
"
```

**Match email domains to client using Alias Registry (Section 1D).**

### Fathom "No Calls" Certification

Before stating "No Fathom calls found", you MUST certify:
- [ ] STEP -1 was completed (unfiltered scan)
- [ ] Checked for client name, shortname, and ALL aliases in titles
- [ ] Checked for implementation/onboarding/support keywords
- [ ] Got summaries and checked attendee email domains on ambiguous titles
- [ ] Verified "[Hold]" meetings are NOT skipped (they're recurring placeholders)

---

## Help Scout Validation Protocol

### Already Completed in STEP -1:
- ✅ Got ALL tickets (unfiltered)
- ✅ Matched to clients using Alias Registry
- ✅ Searched thread_body (catches non-English subjects)

### Additional Context (If Needed)

For deeper client-specific searches:

```sql
-- Search ALL text fields for client
SELECT DISTINCT
  ticket_number,
  ticket_subject,
  ticket_status,
  ticket_created_at,
  conv_customer_organization,
  conv_customer_email,
  mailbox_name,
  LEFT(thread_body, 1000) as thread_content
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE (
  -- Search by organization
  LOWER(conv_customer_organization) LIKE '%[CLIENT_PATTERN]%'
  -- Search by email domain
  OR LOWER(conv_customer_email) LIKE '%@[DOMAIN]%'
  -- Search in subject
  OR LOWER(ticket_subject) LIKE '%[CLIENT_PATTERN]%'
  -- Search in preview
  OR LOWER(ticket_preview) LIKE '%[CLIENT_PATTERN]%'
  -- Search in FULL thread body (catches non-English subjects)
  OR LOWER(thread_body) LIKE '%[CLIENT_PATTERN]%'
)
AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY)
ORDER BY ticket_created_at DESC
LIMIT 50
```

### Search Patterns to Use (from Alias Registry)

For each client, search using ALL patterns from Section 1D:
- Full company name: `%magic lite%`
- Short name: `%magiclite%`
- Org shortname: `%mali%`
- ALL email domains: `%@magiclite.com%`
- Key contacts if known

### Help Scout "No Tickets" Certification

Before stating "No Help Scout tickets found", you MUST certify:
- [ ] STEP -1 was completed (unfiltered scan)
- [ ] Searched ALL aliases from Client Alias Registry
- [ ] Searched thread_body field (catches non-English subjects)
- [ ] Searched by email domain
- [ ] Extended search to 180 days

---

# PART 3: STAGE-BY-STAGE CHECKLIST

## Products Supported

| Product | Required Stages |
|---------|-----------------|
| **eCat iPad** | 1, 2, 3, 4*, 5, 6, 7 |
| **eCat Online** | 1, 2, 3, 4*, 5, 6, 8, 9, 10* |
| **Sales Portal** | 1, 2, 3, 4*, 5, 6, 8, 9, 11 |

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

### Stage 8: eCat Online Site Setup

**Goal:** Web catalog is accessible

**Applies to:** eCat iPad ⚪ | eCat Online ✅ | Sales Portal ✅

#### Check if Stage Applies
- Is eCat Online OR Sales Portal being implemented?
  - **YES** → Continue with checklist below
  - **NO** → Mark stage as ⚪ **N/A**

#### Critical Blockers (Must Pass)
- [ ] eCat Online site exists and enabled
- [ ] Public user group exists

#### Recommended (Flag if False)
- [ ] Logo uploaded

#### Pass Criteria
- ⚪ **N/A:** Neither eCat Online nor Sales Portal being implemented - skip this stage
- 🔴 **RED (BLOCKER):** No site exists OR site disabled OR no public user group
- 🟡 **YELLOW (WARNING):** Site exists but no logo uploaded
- 🟢 **GREEN (READY):** Site enabled AND logo uploaded

#### How to Validate

| Check | Tool Call | True Condition |
|-------|-----------|----------------|
| Site enabled | `get_mobile_sites` | `enabled = true` |
| Public user group exists | `get_permissions_summary` | User type containing "eOL" or "Public" exists |
| Logo uploaded | `get_organization_info` | `preferences.display.logo_url != null` |

---

### Stage 9: eCat Online User Access

**Goal:** Users can access the catalog

**Applies to:** eCat iPad ⚪ | eCat Online ✅ | Sales Portal ✅

#### Check if Stage Applies
- Is eCat Online OR Sales Portal being implemented?
  - **YES** → Continue with checklist below
  - **NO** → Mark stage as ⚪ **N/A**

#### Check Access Model
- Is this a **Closed Site** (login required)?
  - **YES** → Continue with Critical Blockers
  - **NO** → Stage 8 validation sufficient for public sites

#### Critical Blockers (Must Pass) - Closed Sites Only
- [ ] At least 1 non-public user type exists
- [ ] At least 1 non-admin user exists

#### Recommended (Flag if False)
- [ ] More than 1 user type configured

#### Pass Criteria
- ⚪ **N/A:** Neither eCat Online nor Sales Portal being implemented - skip this stage
- ⚪ **N/A:** Public site - Stage 8 sufficient
- 🔴 **RED (BLOCKER):** Closed site with no user types OR no non-admin users
- 🟡 **YELLOW (WARNING):** Only 1 user type configured
- 🟢 **GREEN (READY):** Multiple user types AND non-admin users exist

#### How to Validate

| Check | Tool Call | True Condition |
|-------|-----------|----------------|
| User types exist | `get_permissions_summary` | `user_types` count ≥ 1 (excluding public) |
| Non-admin users exist | `get_org_users` | Users where `is_admin = false` count ≥ 1 |
| Multiple user types | `get_permissions_summary` | `user_types` count ≥ 2 |

---

### Stage 10: eCat Online Ordering (B2B Cart)

**Goal:** Customers can place orders through web

**Applies to:** eCat iPad ⚪ | eCat Online ✅ (conditional) | Sales Portal ⚪

#### Check if Stage Applies
- Is B2B ordering enabled for this eCat Online implementation?
  - **YES** → Continue with checklist below
  - **NO** → Mark stage as ⚪ **N/A** (catalog-only)

#### Critical Blockers (Must Pass)
- [ ] Order recipient email address configured

#### Recommended (Flag if False)
- [ ] Order PDF attachment enabled

#### Pass Criteria
- ⚪ **N/A:** B2B ordering not enabled - catalog-only implementation
- 🔴 **RED (BLOCKER):** No order email recipient configured
- 🟡 **YELLOW (WARNING):** Order email configured but PDF attachment disabled
- 🟢 **GREEN (READY):** Order email configured AND PDF enabled

#### How to Validate

| Check | Tool Call | True Condition |
|-------|-----------|----------------|
| Order email configured | `get_organization_info` | `preferences.administrative.order_email_recipient != null` |
| PDF attachment enabled | `get_organization_info` | `preferences.flags.attach_pdf_to_order_email = true` |

---

## SALES PORTAL STAGE (11)

### Stage 11: Sales Portal Configuration

**Goal:** Sales Portal enabled and users can access sales data

**Applies to:** eCat iPad ⚪ | eCat Online ⚪ | Sales Portal ✅

#### Check if Stage Applies
- Is Sales Portal being implemented?
  - **YES** → Continue with checklist below
  - **NO** → Mark stage as ⚪ **N/A**

#### Critical Blockers (Must Pass)
- [ ] Sales Portal functionality enabled
- [ ] At least 1 territory configured
- [ ] At least 1 non-admin user exists

#### Recommended (Flag if False)
- [ ] Multiple user types configured

#### Pass Criteria
- ⚪ **N/A:** Sales Portal not being implemented - skip this stage
- 🔴 **RED (BLOCKER):** Portal not enabled OR no territories OR no non-admin users
- 🟡 **YELLOW (WARNING):** Only 1 user type configured
- 🟢 **GREEN (READY):** Portal enabled AND territories exist AND multiple user types

#### How to Validate

| Check | Tool Call | True Condition |
|-------|-----------|----------------|
| Portal enabled | `get_organization_info` | `preferences.flags.enable_portal_dashboard = true` |
| Territories configured | `get_user_territories` | Territory count ≥ 1 |
| Non-admin users exist | `get_org_users` | Users where `is_admin = false` count ≥ 1 |
| Multiple user types | `get_permissions_summary` | `user_types` count ≥ 2 |

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

## Recent Activity Header (V13 NEW - MANDATORY)

**EVERY assessment must start with this header:**

```markdown
## 📋 Assessment Context

**Assessment Date:** [TODAY'S DATE]
**STEP -1 Completed:** ✅ Yes

### Today's Activity Summary
- **Fathom Meetings Today:** [X] ([list client shortnames])
- **Help Scout Tickets Today:** [X] ([list client shortnames])

### This Week's Activity Summary
- **Fathom Meetings (7 days):** [X]
- **Help Scout Tickets (7 days):** [X]

---
```

---

## Pipeline Overview Table

```markdown
## **Pipeline Overview**

| Client | Product | Owner | V13 Stage | V13 Readiness | Key Flag | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **[SHORTNAME]** | [Product] | [Owner] | [X] / [Y] | [X]% | [Key issue] | [Specific blocker] | [🔴/⚠️/✅] [X] flags | [X] |
```

**Column Definitions:**
- **Client:** Org shortname in bold
- **Product:** eCat / eOL / Sales Portal
- **Owner:** CSM name (Brent/Chuck)
- **V13 Stage:** Current stage / Total stages for product
- **V13 Readiness:** Percentage (calculate from stages passed)
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

**V13 Assessment:** Stage [X] | [X]% Ready | Products: [Product list]

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟢 | [X] products |
| 3 | 🔴 | **[X] price levels** (Stage 3 criteria: [explanation]) |
| 4 | ⚪ N/A | Options not configured |
| 5 | 🔴 | **[X] customers** (Stage 5 criteria: [explanation]) |
| 6 | 🔴 | **[X] inventory** |
| 7 | 🔴 | No orders |

**🎯 V13 Next Action:** [Specific action item]

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

| Client | V13 Stage | V13 Readiness | Status |
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
| 8 - eCat Online Site Setup | ⚪ N/A | ✅ | ✅ |
| 9 - eCat Online User Access | ⚪ N/A | ✅ | ✅ |
| 10 - eCat Online Ordering | ⚪ N/A | ⚪ Conditional | ⚪ N/A |
| 11 - Sales Portal Configuration | ⚪ N/A | ⚪ N/A | ✅ |

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
5. Non-admin users exist (Stage 9, if closed site)
6. Order email configured (Stage 10, if B2B enabled)

### Sales Portal (Stages 1-6, 8-9, 11)
1. Price levels configured (Stage 3)
2. Customers imported (Stage 5)
3. Site created and enabled (Stage 8)
4. Portal functionality enabled (Stage 11)
5. Territories configured (Stage 11)
6. Non-admin users exist (Stage 11)

---

## MCP Endpoints Reference

### ⛔ EXCLUDED TOOLS (Do NOT Use)

| Tool | Reason |
|------|--------|
| `get_organization_health` | Separate tool for account health scoring - NOT part of Stage-Gated Onboarding Assessment |
| `get_organization_health_csv` | CSV export of health scoring - NOT part of this workflow |

**These tools serve a different purpose** (ongoing account health monitoring) and should NOT be used during onboarding readiness assessments. Using them will produce metrics that don't align with the stage-gated model.

### ✅ REQUIRED TOOLS (Use These)

| Endpoint | Purpose | Stages |
|----------|---------|--------|
| `get_organization_info` | Org status, settings, templates, logo | 1, 7, 8, 10, 11 |
| `get_org_users` | User configuration | 1, 5, 9, 11 |
| `get_data_summary` | All counts in one call | 2, 5, 6 |
| `get_price_levels` | Pricing setup | 3 |
| `get_categories` | Taxonomy | 2 |
| `get_collections` | Product organization | 2 |
| `get_options` | Options (count records, not columns) | 4 |
| `get_user_territories` | Territory validation | 5, 11 |
| `get_import_events` | Data health | 6 |
| `get_smart_stacks` | Smart list config | 6 |
| `get_inventories` | Inventory data | 6 |
| `get_mobile_sites` | eCat Online site config | 7, 8 |
| `get_reports_config` | Report formats | 7 |
| `get_orders` | Order validation | 7 |
| `get_permissions_summary` | User permissions, public user group | 5, 8, 9, 11 |

---

## BigQuery Tables Reference

| Table | Purpose | Stage |
|-------|---------|-------|
| `mixpanel_order_submitted` | iPad activity (filter: `mp_lib='iphone'`) | 7 |
| `help_scout_tickets` | Support/Onboarding activity | All |

---

## Common Mistakes to Avoid

### Mistake 1: Skipping STEP -1 (V13 CRITICAL)
**Problem:** Jumping straight to client assessments without checking TODAY's activity
**Solution:** STEP -1 is MANDATORY. Run it FIRST, every time.

### Mistake 2: Generating Data Without Tool Calls
**Problem:** Producing plausible-looking numbers without actually calling MCP/BigQuery
**Solution:** EVERY metric requires a tool call.

### Mistake 3: Using Wrong Org Shortname
**Problem:** Querying "jcusa" when client refers to "jc" (different entities)
**Solution:** Verify org shortname in first tool call, confirm name matches expected client

### Mistake 4: Counting Schema Columns Instead of Data
**Problem:** Reporting "15 options" because schema has 15 option_group columns
**Solution:** Count the RECORDS returned by `get_options`, not schema fields

### Mistake 5: Skipping Validation Because Status Looks Obvious
**Problem:** Not running Fathom/Help Scout because MCP data looks good
**Solution:** V13 has NO skip conditions. All validation is mandatory.

### Mistake 6: Assuming Status From Meeting Titles
**Problem:** Seeing "[Hold]" and assuming implementation is paused
**Solution:** ALWAYS get call summary. NEVER assume from title.

### Mistake 7: Only Checking One Help Scout Inbox
**Problem:** Only querying Support, missing Onboarding tickets
**Solution:** Query BOTH Support AND Onboarding, BOTH Open AND Closed

### Mistake 8: Saying "No Calls" Without Checking Invite Lists
**Problem:** Missing relevant calls because client name wasn't in title
**Solution:** Check attendee email domains for ambiguous meeting titles

### Mistake 9: Missing Non-English Help Scout Tickets (V13 NEW)
**Problem:** Ticket with Chinese subject line missed because subject didn't match
**Solution:** Search thread_body field AND email domains, not just subject

### Mistake 10: Filtering Fathom/Help Scout Before Scanning All (V13 NEW)
**Problem:** Applying client filters too early, missing relevant activity
**Solution:** STEP -1 gets ALL activity first, THEN matches to clients

### Mistake 11: Using `get_organization_health` Tool (V13 CRITICAL)
**Problem:** Calling `get_organization_health` or `get_organization_health_csv` during onboarding assessment
**Solution:** These are SEPARATE tools for account health scoring. Stage-Gated Onboarding uses the specific endpoints listed in the MCP Endpoints Reference. Do NOT substitute health scoring for stage-gated assessment.

---

## Execution Checklist (V13 UPDATED)

**STEP -1: Recent Activity First (MANDATORY):**
1. [ ] Get ALL Fathom meetings (last 14 days, unfiltered)
2. [ ] Get ALL Help Scout tickets (last 14 days, unfiltered)
3. [ ] Match activity to clients using Alias Registry
4. [ ] Get summaries for ALL matched Fathom meetings
5. [ ] Create Recent Activity Report
6. [ ] Confirm TODAY's activity: [X] meetings, [Y] tickets

**STEP 0: Client Discovery (if batch assessment):**
7. [ ] Query HubSpot for onboarding clients
8. [ ] Map HubSpot companies to MCP shortnames

**Run MCP queries (ALL REQUIRED per client):**
9. [ ] Foundation data batch
10. [ ] Configuration data batch
11. [ ] Operations data batch
12. [ ] Product-specific data batch

**Run BigQuery queries (ALL REQUIRED):**
13. [ ] iPad Activity (MixPanel)
14. [ ] Help Scout client-specific queries (for deep dive)

**Compile output:**
15. [ ] Start with Recent Activity Header (V13 NEW)
16. [ ] Use exact templates from Part 5
17. [ ] Verify all metrics have sources
18. [ ] Run pre-output validation checklist

---

**Document Status:** Production Ready  
**Version:** 14.0 (100% Queryable Stages)  
**Last Updated:** January 21, 2026  
**Contact:** Kylor Johnson

---

## V14 Changelog (from V13)

| Change | Reason |
|--------|--------|
| **Stage 8: Removed "Site name configured"** | Field not reliably queryable |
| **Stage 8: Updated logo check** | `logo_url` is in `get_organization_info`, not `get_mobile_sites` |
| **Stage 10: Removed "Web orders exist"** | Cannot distinguish web vs iPad orders via MCP |
| **Stage 11-12: Combined into Stage 11** | Simplified Sales Portal to single stage |
| **Stage 11: Removed import type checks** | Import types not reliably filterable for portal data |
| **Stage 11: Removed portal permissions check** | Field not exposed in `get_permissions_summary` |
| **All stages: Added validation tables** | Explicit True Condition for each check |
| **All stages: 100% queryable** | Every item returns True/False from MCP |
| Updated MCP Endpoints Reference | Reflect new stage assignments |
| Updated Critical Launch Blockers | Aligned with simplified stages |

---

## V13 Changelog (from V12)

| Change | Reason |
|--------|--------|
| Added STEP -1: Recent Activity First | Missed TODAY's meetings every week |
| Added Client Alias Registry | Fuzzy matching for company names, email domains |
| Added thread_body search for Help Scout | Missed tickets with non-English subjects (PEBL) |
| Added Recent Activity Header to output | Forces visibility of TODAY's activity |
| Added unfiltered scan requirement | Filtering too early missed relevant activity |
| Added Mistake 9-10 to common mistakes | Document specific V12 failures |
| Updated execution checklist order | STEP -1 is now first |
| **Added Rule 6: No Health Scoring Tools** | `get_organization_health` is a separate workflow - must not be used here |
| **Added Excluded Tools section to MCP Reference** | Explicitly list tools NOT to use |
| **Added Mistake 11** | Document health scoring tool exclusion |