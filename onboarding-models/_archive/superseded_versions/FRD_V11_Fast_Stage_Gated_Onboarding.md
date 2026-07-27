# FRD: Fast Mode Stage-Gated Onboarding Readiness Scoring

**Author:** Kylor Johnson  
**Date:** January 14, 2026  
**Version:** 11.3 (Fast Mode + Fathom API Fix + Help Scout Mandatory)  
**Status:** Production Ready  
**Related JIRA:** [Link to your JIRA ticket]

---

## Document Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 10.0 | Jan 14, 2026 | Production baseline (12-stage multi-product framework) | Kylor Johnson |
| 11.0 | Jan 14, 2026 | **Fast Mode Protocol:** Parallel MCP batching, consolidated BigQuery, tiered Fathom validation. Reduces execution from 10+ min to ~5 min with 85% accuracy vs 95% full mode. | Kylor Johnson |
| 11.1 | Jan 14, 2026 | **CRITICAL FIX:** Added explicit Fathom API integration instructions. Phase 3 now documents the Python script method (`fathom_api.py`) for `get_meetings()`, `get_summary()`, `get_transcript()`. Clarified that Notion search alone is INSUFFICIENT for qualitative validation. | Kylor Johnson |
| 11.2 | Jan 14, 2026 | **CRITICAL FIX:** Clarified that "[Hold]" in meeting titles is a CALENDAR PLACEHOLDER for recurring meetings, NOT an indication that implementation is paused. ALWAYS retrieve call summaries to understand actual status - never assume from title alone. | Kylor Johnson |
| 11.3 | Jan 14, 2026 | **CRITICAL FIX:** Help Scout validation is now EQUALLY MANDATORY as Fathom. Must query ALL mailboxes (Support + Onboarding) for recent activity. File uploads, meeting scheduling, and support exchanges are critical engagement indicators. Never conclude "no activity" without checking both sources. | Kylor Johnson |

---

## Executive Summary

V11 Fast Mode optimizes the V10 Stage-Gated framework for **speed and context efficiency** while maintaining accuracy. This protocol extends the 12-stage multi-product framework with execution optimizations designed for high-volume assessments.

**Key Innovations:**
1. **Parallel MCP Batching:** 4 parallel groups instead of 15+ sequential calls (60% faster)
2. **Consolidated BigQuery:** Single query for iPad + Help Scout + HubSpot (70% reduction)
3. **Tiered Fathom Validation:** Title search always, deeper tiers conditional
4. **Context-Efficient Output:** Extract only assessment-relevant fields (75% token reduction)
5. **Conditional Validation:** Skip Layer 2 for obvious GREEN/RED status

**Performance Metrics:**
- Execution time reduced from 10-15 min/client to 4-5 min/client
- Context tokens reduced from ~15K/client to ~5K/client
- Accuracy maintained at 85% vs 95% full mode (acceptable for screening)

---

## Problem Statement

### Current Issues (V10)
- Full Mode assessments take 10-15 minutes per client
- Sequential MCP calls waste time on independent data
- Multiple BigQuery queries duplicate connection overhead
- Deep Fathom validation unnecessary for obvious status
- Context token limits restrict batch assessment capacity

### Business Impact
- CS standup preparation takes too long for pipeline reviews
- Batch assessments (5+ clients) exceed practical time budgets
- Weekly pipeline reviews consume excessive agent context
- Time-sensitive status checks delayed by full validation

---

## Proposed Solution

### A. Mode Selection Framework

A **two-mode system** providing appropriate depth for different use cases:

| Use Case | Mode | Time | Accuracy |
|----------|------|------|----------|
| Weekly CS standup pipeline reviews | Fast (V11) | 4-5 min | 85% |
| Batch assessments (5+ clients) | Fast (V11) | 4-5 min | 85% |
| Initial triage / screening | Fast (V11) | 4-5 min | 85% |
| Status checks on known-good implementations | Fast (V11) | 4-5 min | 85% |
| Pre-launch validation (final check) | Full (V10) | 10-15 min | 95% |
| Investigating flagged clients | Full (V10) | 10-15 min | 95% |
| Churn risk deep dives | Full (V10) | 10-15 min | 95% |
| Executive escalation documentation | Full (V10) | 10-15 min | 95% |
| New client initial assessment | Full (V10) | 10-15 min | 95% |

### B. Parallel MCP Batching Architecture

Execute 4 batches simultaneously instead of 15+ sequential calls:

| Batch | Endpoints | Stages Covered |
|-------|-----------|----------------|
| **Batch 1: Foundation** | `get_organization_info`, `get_org_users`, `get_data_summary` | 1, 2, 5, 6 |
| **Batch 2: Configuration** | `get_price_levels`, `get_categories`, `get_collections`, `get_options` | 2, 3, 4 |
| **Batch 3: Operations** | `get_user_territories`, `get_import_events`, `get_smart_stacks`, `get_inventories` | 5, 6, 7 |
| **Batch 4: Product-Specific** | `get_mobile_sites`, `get_reports_config`, `get_orders`, `get_permissions_summary` | 7, 8, 9, 10, 12 |

**Time Savings:** ~60% reduction (4 round-trips vs 15+)

### C. Tiered Validation Architecture

| Tier | When to Run | What to Search | Time Cost |
|------|-------------|----------------|-----------|
| **Tier 1** | ✅ Always | Notion title/page search for client name | ~1 min |
| **Tier 2** | 🔶 If Tier 1 finds calls | Fathom call summaries | ~2 min |
| **Tier 3** | 🔶 If flags detected | Full transcript search | ~3 min |

**Key Principle:** Tier 1 catches most issues. Deeper tiers only when warranted.

---

## Success Criteria

### CS / Implementation Team
- Pipeline assessments completed in under 35 minutes for 7 clients
- Clear visibility into which clients need full-mode deep dives
- Actionable escalation triggers for automatic mode switching
- Reduced context token consumption for batch processing

### Leadership
- Faster pipeline visibility during standup preparation
- Efficient resource allocation between screening and deep dives
- Maintained accuracy for critical decisions

### Operations
- Standardized execution checklist for consistent assessments
- Clear escalation criteria for mode switching
- Performance metrics tracking (time, accuracy, flags)

---

## Critical Launch Blockers

### Fast Mode Escalation Triggers 🔴
**Auto-escalate to Full Mode (V10) if:**

| Trigger | Condition | Action |
|---------|-----------|--------|
| Sentiment Flag | Client has 🔴 SENTIMENT flag from call summary | Full Mode + Executive escalation |
| Stalled + Payment | STALLED status + recent payment received | Full Mode + Finance review |
| No Engagement | 0 Fathom calls in 90+ days | Full Mode + Outreach plan |
| Contradiction | Layer 1 GREEN but Layer 2 🔴 CONTRADICT | Full Mode + Investigation |
| Executive Request | Leadership requests detailed assessment | Full Mode required |
| Pre-Launch | Final validation before go-live | Full Mode required |

**⚠️ NOTE:** "[Hold]" in meeting titles is NOT an escalation trigger. It's a calendar placeholder for recurring meetings.

### Fast Mode Skip Conditions 🟢
**Skip Layer 2 validation when:**

| Condition | Evidence | Action |
|-----------|----------|--------|
| High Activity | orders_last_30_days > 50 AND ipad_users > 5 | Mark ✅ CONFIRMED by activity metrics |
| Known Blocker | RED status with data-based blocker (0 customers, 0 price levels) | Mark 🔴 BLOCKER confirmed by system data |
| Obvious Stall | org_status == "inactive" AND orders == 0 | Run Tier 1 only for context |

---

## Conditional Logic Framework

| Feature | Detection Method | Fast Mode Handling |
|---------|------------------|-------------------|
| **High Activity** | orders > 50 in 30 days | Skip Layer 2, confirm by metrics |
| **Known Blockers** | 0 customers OR 0 price levels | Skip Layer 2, confirm by data |
| **Stalled Status** | org_status = inactive + 0 orders | Tier 1 Fathom only |
| **Ambiguous Status** | All other cases | Full tiered validation |
| **Escalation Triggers** | Sentiment/Contradiction detected | Auto-escalate to Full Mode |

---

## Color Threshold System

| Status | Meaning | Fast Mode Action |
|--------|---------|------------------|
| 🟢 Green | Production-ready | Proceed, skip Layer 2 if high activity |
| 🟡 Yellow | Launchable with minor issues | Run Tier 1 validation |
| 🔴 Red | Blocker | Confirm by data, note for follow-up |
| ⚪ N/A | Not applicable | Skip in assessment |
| ❓ Unknown | Cannot validate | Flag for Full Mode review |

---

## Confidence Scoring System

Fast Mode uses simplified confidence calculation:

| Layer 1 Status | Tier 1 Result | Confidence Score | Interpretation |
|----------------|---------------|------------------|----------------|
| 🟢 GREEN | High activity metrics | **90%+** | Auto-confirmed, proceed |
| 🟢 GREEN | No issues found | **80%** | Good confidence, proceed |
| 🟢 GREEN | "[Hold]" detected | **30%** | Escalate to Full Mode |
| 🟡 YELLOW | No issues found | **60%** | Acceptable with monitoring |
| 🟡 YELLOW | Flags detected | **40%** | Run Tier 2, consider Full Mode |
| 🔴 RED | Data-confirmed blocker | **10%** | Blocker confirmed, must resolve |
| 🔴 RED | Ambiguous | **0%** | Full Mode investigation required |

---

## Validation Flag Types

### Standard Flags (Same as V10)

| Flag | Meaning | Action |
|------|---------|--------|
| 🔴 CONTRADICT | Layer 2 contradicts Layer 1 | Investigate immediately |
| 🔴 BLOCKER | System data shows critical gap | Cannot proceed |
| ⚠️ REVIEW | Potential issue needs clarification | CSM follow-up |
| ⚠️ TIMELINE | Missed or at-risk deadline | Update target |
| ⚠️ ACTIVITY | Low/no engagement | Confirm client status |
| 🔴 SENTIMENT | Negative client sentiment detected | Executive escalation |
| ✅ CONFIRMED | Layer 2 validates Layer 1 | Proceed confidently |

### Fast Mode-Specific Flags

| Flag | Meaning | Action |
|------|---------|--------|
| 🔴 STALLED | Org inactive + 0 orders + **NO Fathom calls in 90+ days** | Reactivate before proceeding |
| ⚠️ UNFULFILLED | Commitment detected in call summary but not met | CSM verify status |
| ⚠️ TIMELINE | Target date mentioned in call summary, approaching/passed | Update project plan |
| ⚪ SKIP_L2 | Layer 2 skipped (obvious status) | Full mode if uncertain |

**⚠️ NOTE:** "[Hold]" in meeting titles is a calendar placeholder, NOT an indicator of stalled status.

---

# PHASE 1: PARALLEL MCP BATCHING

## Batch 1: Foundation Data

**Goal:** Retrieve core organizational and data counts in single batch

**Endpoints:**
- `get_organization_info` → Stage 1
- `get_org_users` → Stage 1, 5
- `get_data_summary` → Stages 2, 5, 6

### Required Criteria

| # | Criterion | Endpoint | Pass Condition |
|---|-----------|----------|----------------|
| 1.1 | Organization active | `get_organization_info` | `status: "active"` |
| 1.2 | Admin user exists | `get_org_users` | At least 1 admin (excluding SuperCat staff) |
| 1.3 | Products imported | `get_data_summary` | `products.count >= 10` |
| 1.4 | Customers imported | `get_data_summary` | `customers.count >= 10` |

### Thresholds
- 🔴 **Red:** Organization inactive OR 0 products OR 0 customers
- 🟡 **Yellow:** Products/customers < 100
- 🟢 **Green:** Active org with 100+ products and customers

---

## Batch 2: Configuration Data

**Goal:** Retrieve pricing and catalog structure in single batch

**Endpoints:**
- `get_price_levels` → Stage 3
- `get_categories` → Stage 2
- `get_collections` → Stage 2
- `get_options` → Stage 4

### Required Criteria

| # | Criterion | Endpoint | Pass Condition |
|---|-----------|----------|----------------|
| 2.1 | Price levels configured | `get_price_levels` | `count >= 1` |
| 2.2 | Categories exist | `get_categories` | `count >= 1` |
| 2.3 | Collections exist | `get_collections` | `count >= 1` |
| 2.4 | Options configured (if used) | `get_options` | `count >= 1` OR N/A |

### Thresholds
- 🔴 **Red:** 0 price levels (absolute blocker)
- 🟡 **Yellow:** Only 1 price level OR no categories
- 🟢 **Green:** 2+ price levels with catalog structure

---

## Batch 3: Operations Data

**Goal:** Retrieve operational health data in single batch

**Endpoints:**
- `get_user_territories` → Stage 5
- `get_import_events` → Stage 6
- `get_smart_stacks` → Stage 7
- `get_inventories` → Stage 6

### Required Criteria

| # | Criterion | Endpoint | Pass Condition |
|---|-----------|----------|----------------|
| 3.1 | Import health | `get_import_events` | No critical errors in 30 days |
| 3.2 | Territory assignments (if used) | `get_user_territories` | Configured OR direct assignment |
| 3.3 | Inventory exists (if enabled) | `get_inventories` | `count > 0` OR N/A |
| 3.4 | Smart stacks (if enabled) | `get_smart_stacks` | `count >= 1` OR N/A |

### Thresholds
- 🔴 **Red:** Critical import errors
- 🟡 **Yellow:** Stale inventory (7+ days) OR minor warnings
- 🟢 **Green:** Fresh data AND no import errors

---

## Batch 4: Product-Specific Data

**Goal:** Retrieve product-specific configuration in single batch

**Endpoints:**
- `get_mobile_sites` → Stages 7, 8
- `get_reports_config` → Stage 7
- `get_orders` → Stage 7, 10
- `get_permissions_summary` → Stages 5, 9, 12

### Required Criteria

| # | Criterion | Endpoint | Pass Condition |
|---|-----------|----------|----------------|
| 4.1 | Presentation formats (iPad) | `get_reports_config` | `count >= 3` |
| 4.2 | Test orders exist | `get_orders` | `count >= 1` |
| 4.3 | Site enabled (eCat Online) | `get_mobile_sites` | `enabled: true` OR N/A |
| 4.4 | Permissions configured | `get_permissions_summary` | User types with access |

### Thresholds
- 🔴 **Red:** 0 orders AND iPad product scope
- 🟡 **Yellow:** Missing presentation formats OR permissions gaps
- 🟢 **Green:** Orders exist AND proper configuration

---

# PHASE 2: CONSOLIDATED BIGQUERY + HELP SCOUT VALIDATION

## ⚠️ CRITICAL: Help Scout is EQUALLY MANDATORY as Fathom

**Help Scout validation is NOT optional. It is a REQUIRED data source for every client.**

### What Help Scout Catches That Fathom Misses

| Signal Type | Example | Why It Matters |
|-------------|---------|----------------|
| **File Uploads** | "New Onboarding File Upload - Magic Lite" (30+ uploads Jan 6) | Shows active engagement even without Fathom calls |
| **Support Activity** | "eCat Online not updating trade names" | Reveals production issues and client involvement |
| **Meeting Scheduling** | "Re: Scheduling review meeting" | Shows upcoming engagement, timeline context |
| **Technical Issues** | "Server cache happening now!" | Indicates active usage and potential blockers |
| **Client Sentiment** | Direct client communication | May reveal frustration not captured in Fathom |

### Mailboxes to Query (BOTH REQUIRED)

| Mailbox | What It Contains | Why Required |
|---------|------------------|--------------|
| **SuperCat Support** | Production issues, technical questions | Active usage indicators |
| **SuperCat Onboarding** | File uploads, onboarding progress, scheduling | Implementation progress indicators |

### ❌ COMMON MISTAKE: Only Checking Fathom

**If Fathom shows no recent calls, DO NOT conclude "no activity."**
A client may be:
- Uploading files to onboarding portal (Help Scout Onboarding mailbox)
- Emailing about scheduling (Help Scout Support/Onboarding)
- Reporting issues while actively testing (Help Scout Support)

**ALWAYS check Help Scout before concluding engagement status.**

---

## Single Query for Multi-Source Validation

**Goal:** Replace 3+ separate queries with single consolidated query

### Query Template

```sql
WITH ipad_activity AS (
  SELECT 
    currentorganizationshortname as org,
    COUNT(*) as ipad_orders,
    COUNT(DISTINCT distinct_id) as unique_ipad_users,
    MAX(TIMESTAMP_SECONDS(CAST(time AS INT64))) as last_ipad_order
  FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.mixpanel_order_submitted`
  WHERE currentorganizationshortname IN ([ORG_LIST])
    AND mp_lib = 'iphone'
  GROUP BY currentorganizationshortname
),
helpscout AS (
  SELECT 
    ticket_number,
    ticket_subject,
    ticket_status,
    DATE(ticket_created_at) as created_date,
    conv_customer_organization as client,
    LEFT(ticket_preview, 200) as preview
  FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
  WHERE (LOWER(conv_customer_organization) LIKE '%[CLIENT_PATTERNS]%'
         OR LOWER(ticket_subject) LIKE '%[CLIENT_PATTERNS]%')
    AND ticket_status IN ('active', 'pending', 'closed')
    AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  ORDER BY created_date DESC
  LIMIT 20
)
SELECT * FROM ipad_activity
UNION ALL
SELECT * FROM helpscout
```

### Required Criteria

| # | Criterion | Query Section | Pass Condition |
|---|-----------|---------------|----------------|
| 2.1 | iPad activity (Stage 7) | `ipad_activity` | `ipad_orders >= 1` |
| 2.2 | Unique iPad users | `ipad_activity` | `unique_ipad_users >= 1` |
| 2.3 | Recent Help Scout activity | `helpscout` | Tickets exist (context only) |
| 2.4 | Active issues | `helpscout` | `status = 'active'` flagged |

### Thresholds
- 🔴 **Red:** 0 iPad orders AND iPad in product scope
- 🟡 **Yellow:** Active Help Scout tickets exist
- 🟢 **Green:** iPad activity confirmed AND no active tickets

**Time Savings:** ~70% reduction (1 query vs 3+)

---

# PHASE 3: TIERED FATHOM VALIDATION

## ⚠️ CRITICAL: Fathom API Integration (MANDATORY)

**The Fathom API is the PRIMARY source for qualitative validation. DO NOT skip this step.**

### Fathom API Access Method

The Fathom API is accessed via a Python script located at:
```
/fathom/fathom_api.py
```

**Available Functions:**
| Function | Purpose | Returns |
|----------|---------|---------|
| `get_meetings()` | Retrieve all recorded meetings | List of meeting objects with `recording_id`, `meeting_title`, `recording_start_time` |
| `get_summary(recording_id)` | Get AI-generated summary for a specific call | Summary object with key points, action items |
| `get_transcript(recording_id)` | Get full transcript (Tier 3 only) | Full text transcript |

### Execution Method

```bash
cd "/path/to/SuperCat 4.0"
python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'fathom'))
from fathom_api import get_meetings, get_summary

# Step 1: Get all meetings
meetings = get_meetings()

# Step 2: Filter by client name/shortname
clients = ['client_name', 'shortname']
relevant = [m for m in meetings 
            if any(c in m.get('meeting_title', '').lower() for c in clients)]

# Step 3: For each match, print ID, date, title
for m in relevant:
    print(f\"{m.get('recording_id')} | {m.get('recording_start_time')[:10]} | {m.get('meeting_title')}\")

# Step 4: Get summaries for critical calls
summary = get_summary(recording_id)
print(summary.get('summary', ''))
"
```

### ❌ COMMON MISTAKE: Using Only Notion Search

**DO NOT** rely solely on Notion search for Fathom data. Notion search finds:
- ✅ Fathom call titles synced to Notion
- ✅ References in CS meeting notes
- ❌ Does NOT provide call summaries
- ❌ Does NOT detect "[Hold]" patterns reliably
- ❌ Does NOT capture full context

**ALWAYS** use the Fathom API directly for:
- "[Hold]" pattern detection in call titles
- Call summary extraction for validation quotes
- Sentiment/blocker keyword detection

---

## Tier 1: Fathom Title Search (ALWAYS RUN)

**Goal:** Scan all Fathom calls for client meetings and critical patterns

**Method:** Use `get_meetings()` function, filter by client name/shortname

### Search Patterns

```python
# Client search terms (lowercase)
clients = ['client_name', 'full_name', 'shortname']

# Filter by client name - get ALL calls, don't filter by title patterns
```

### ⚠️ CRITICAL: Title Patterns DO NOT Indicate Status

**"[Hold]" in meeting titles is a CALENDAR PLACEHOLDER** for recurring meetings, NOT an indication that implementation is paused.

| Title Pattern | What It Means | What To Do |
|---------------|---------------|------------|
| "[Hold] Client Standup" | Recurring meeting placeholder | **ALWAYS get summary** - call may show active progress |
| "Client Check-In" | Regular touchpoint | Get summary for status |
| "Client Training" | Active implementation | Get summary for details |

**NEVER assume implementation status from title alone. ALWAYS retrieve `get_summary()` for any call found.**

### Required Criteria

| # | Criterion | Search Pattern | Pass Condition |
|---|-----------|----------------|----------------|
| 1.1 | Client meetings exist | Client name in title | Found in last 90 days |
| 1.2 | Recent engagement | Meeting dates | Activity in last 60 days |
| 1.3 | Call frequency | Number of calls | Multiple calls = active engagement |
| 1.4 | Summary retrieved | `get_summary()` called | **MANDATORY for every call found** |

### Thresholds
- 🔴 **Red:** No meetings in 90+ days (potential disengagement)
- 🟡 **Yellow:** No meetings in 60+ days OR only 1 call found
- 🟢 **Green:** Recent meetings with summaries retrieved

### What Tier 1 Catches (via Fathom API)
- ✅ Recent call existence (engagement level)
- ✅ Call frequency and recency
- ✅ Meeting type patterns (standup, training, kickoff)
- ✅ **Requires Tier 2 summary retrieval for actual status**

### Example Tier 1 Output

```
Found 8 calls for CST (Coaster):
113941321 | 2026-01-13 | [Hold] eCat x Coaster Standup  → GET SUMMARY
113295642 | 2026-01-06 | [Hold] eCat x Coaster Standup  → GET SUMMARY
112428519 | 2025-12-30 | [Hold] eCat x Coaster Standup  → GET SUMMARY
111768293 | 2025-12-23 | [Hold] eCat x Coaster Standup  → GET SUMMARY

⚠️ "[Hold]" is calendar placeholder - MUST get summary to determine actual status
```

---

## Tier 2: Summary Search (Conditional)

**Goal:** Extract validation quotes from call summaries

**Trigger:** Tier 1 finds 1+ calls in last 90 days

**Method:** Use `get_summary(recording_id)` for most recent calls

### Execution

```python
from fathom_api import get_summary

# Get summary for most recent call
summary = get_summary(113941321)
print(summary.get('summary', '')[:2000])
```

### Search Patterns

| Category | Keywords to Extract |
|----------|---------------------|
| Blockers | "blocker", "blocked", "waiting", "re-import" |
| Rework | "restructure", "rework", "rebuild" |
| Timeline | "deadline", "target date", "go-live", "launch" |
| Data Issues | "clobbered", "wrong", "missing", "error" |
| Urgency | "urgent", "critical", "escalate", "ASAP" |

### Required Criteria

| # | Criterion | Pattern | Pass Condition |
|---|-----------|---------|----------------|
| 2.1 | No blockers mentioned | Blocker keywords | Not found = pass |
| 2.2 | No rework required | Rework keywords | Not found = pass |
| 2.3 | Timeline captured | Timeline keywords | Extract and note |
| 2.4 | No escalation needed | Urgency keywords | Not found = pass |

### Thresholds
- 🔴 **Red:** "blocker" OR "escalate" found → consider Full Mode
- 🟡 **Yellow:** "rework" OR "re-import" found
- 🟢 **Green:** No concerning patterns

### Example Tier 2 Output

```
Summary from Fathom call 113941321 (Jan 13):
*"Customer data requires re-import. A script clobbered customer-specific 
price levels (e.g., DSFOB C6) with default (Z3T1)."*

*"Rep training urgent - invites Jan 13, market training Jan 23. 
All data issues must be resolved this week."*
```

---

## Tier 3: Transcript Search (Conditional)

**Goal:** Full validation when issues detected

**Trigger:** Tier 2 detects potential issue OR client has 🔴 flag

**Method:** Use `get_transcript(recording_id)` - use sparingly (high token cost)

### Search Patterns

| Category | Keywords |
|----------|----------|
| Sentiment | "frustrated", "disappointed", "concerned" |
| Quality | "amateur", "immature", "not ready" |
| Churn | "cancel", "churn", "reconsider" |
| Escalation | "escalate", "executive", "leadership" |

### Required Criteria

| # | Criterion | Pattern | Pass Condition |
|---|-----------|---------|----------------|
| 3.1 | Sentiment check | Sentiment keywords | Not found = pass |
| 3.2 | Quality concerns | Quality keywords | Not found = pass |
| 3.3 | Churn risk | Churn keywords | Not found = pass |
| 3.4 | Escalation history | Escalation keywords | Noted if found |

### Thresholds
- 🔴 **Red:** Any sentiment/churn keyword → Full Mode + Executive escalation
- 🟡 **Yellow:** Quality concerns mentioned
- 🟢 **Green:** No concerning patterns

---

# PHASE 4: CONDITIONAL VALIDATION LOGIC

## Skip Conditions

**Goal:** Avoid unnecessary validation when status is obvious

### Conditional Logic

```python
# Pseudocode for Fast Mode validation decisions

if layer1_status == "RED" and blocker_is_data_based:
    # Known blocker (0 customers, 0 price levels)
    skip_fathom_search()
    validation = "🔴 BLOCKER confirmed by system data"
    
elif orders_last_30_days > 50 and ipad_users > 5:
    # High activity = obviously production live
    skip_fathom_search()
    validation = "✅ CONFIRMED by activity metrics"
    
elif org_status == "inactive" and orders == 0:
    # Obvious stall, but still search Fathom for context
    run_tier1_fathom()
    validation = "⚠️ STALLED - check Fathom for reason"
    
else:
    # Ambiguous - run full Tier 1 + conditional Tier 2
    run_tiered_fathom()
```

### Required Criteria

| # | Condition | Action | Validation Result |
|---|-----------|--------|-------------------|
| 4.1 | RED + data blocker | Skip Fathom | 🔴 BLOCKER confirmed |
| 4.2 | High activity metrics | Skip Fathom | ✅ CONFIRMED |
| 4.3 | Inactive + 0 orders | Tier 1 only | ⚠️ STALLED |
| 4.4 | Ambiguous status | Tier 1 + 2 | Full validation |

### Thresholds
- 🔴 **Red:** Confirmed blockers by data
- 🟡 **Yellow:** Stalled requiring context
- 🟢 **Green:** Confirmed by activity OR clean validation

---

# PHASE 5: CONTEXT-EFFICIENT OUTPUT

## Output Format

**Goal:** Replace verbose MCP responses with structured summary

### Per-Client Quick Summary Template

```markdown
## [CLIENT_NAME] ([SHORTNAME])

**V11 Fast Assessment:** Stage [X] | [XX]% Ready | Products: [LIST]

| Stage | Status | Quick Evidence |
|-------|--------|----------------|
| 1 | 🟢/🟡/🔴 | [one-liner] |
| 2 | 🟢/🟡/🔴 | [one-liner] |
| ... | ... | ... |

**🎯 Next Action:** [single action item]

**Validation:** [✅ CONFIRMED / ⚠️ X flags / 🔴 BLOCKED]
- [Flag 1 if any]
- [Flag 2 if any]
```

### Pipeline Overview Template

```markdown
## Pipeline Overview (V11 Fast Mode)

| Client | Stage | Products | Readiness | Flags | Key Issue |
|--------|-------|----------|-----------|-------|-----------|
| AAA | 7 | iPad | 90% | ✅ | Production live |
| BBB | 5 | iPad+Online | 60% | ⚠️ 2 | Customer data |
| CCC | 3 | iPad | 25% | 🔴 | 0 price levels |
```

### Visual Pipeline View

```
PIPELINE VIEW
═══════════════════════════════════════════════════════════
AAA ██████████████████░░ 90%  Stage 7 - iPad Ready     ✅
BBB ████████████░░░░░░░░ 60%  Stage 5 - Customer Setup ⚠️
CCC █████░░░░░░░░░░░░░░░ 25%  Stage 3 - Pricing        🔴
═══════════════════════════════════════════════════════════
```

**Token Savings:** ~75% reduction per client

---

# VALIDATION LAYER IMPLEMENTATION

## ⚠️ CRITICAL: Evidence-Based Validation

**Every validation flag MUST include the actual quote/sentiment from the source.**

DO NOT simply say "flagged" or "issue detected." ALWAYS include:
- The **exact quote** from Fathom transcript/summary
- The **ticket excerpt** from Help Scout
- The **date** the evidence was captured
- The **source** (which call or ticket)

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
| 5 | 🔴 CONTRADICT | Help Scout #12345 (Jan 10) | *"Customer data requires re-import. A script clobbered customer-specific price levels."* |
```

---

## Fast Mode Execution Checklist

### Pre-Execution
- [ ] Identify client shortnames for batch processing
- [ ] Confirm product scope per client (HubSpot)
- [ ] Check for known issues from prior assessments

### Execution
- [ ] Run Phase 1: Parallel MCP batches (4 simultaneous)
- [ ] **Run Phase 2: Help Scout BigQuery (MANDATORY)**
  - [ ] Query BOTH mailboxes: Support + Onboarding
  - [ ] Check for file uploads, meeting scheduling, support exchanges
  - [ ] Note any tickets from last 30 days
  - [ ] Extract quotes with ticket numbers and dates
- [ ] **Run Phase 3: Fathom API Validation (MANDATORY)**
  - [ ] Execute `get_meetings()` via Python script
  - [ ] Filter results by client name/shortname
  - [ ] Get summaries for ALL recent calls with `get_summary()`
  - [ ] Extract validation quotes with dates
- [ ] Apply Phase 4: Conditional logic
- [ ] Format Phase 5: Context-efficient output (V7 Notion format)

**⚠️ NEVER conclude "no activity" without checking BOTH Fathom AND Help Scout**

### Post-Execution
- [ ] Flag any clients needing Full Mode deep dive
- [ ] Update pipeline dashboard
- [ ] Document any new flags for tracking

---

## ⛔ COMMON MISTAKES TO AVOID

### Mistake 1: Skipping Fathom API
**Problem:** Using only Notion search for qualitative validation
**Why it fails:** Notion search doesn't provide call summaries or detailed context
**Solution:** ALWAYS run `get_meetings()` via the Python script in `/fathom/fathom_api.py`

### Mistake 2: Not Extracting Actual Quotes
**Problem:** Flagging issues without supporting evidence
**Why it fails:** Validation flags without quotes are not actionable
**Solution:** Use `get_summary()` to extract exact quotes with dates

### Mistake 3: Assuming Status From Meeting Titles
**Problem:** Seeing "[Hold]" in a meeting title and assuming implementation is paused
**Why it fails:** "[Hold]" is a **calendar placeholder** for recurring meetings, NOT an indication of implementation status. A "[Hold] Client Standup" may contain evidence of very active, on-track progress.
**Solution:** ALWAYS retrieve `get_summary()` for every call found. NEVER make status assumptions based on meeting titles alone.

### Mistake 4: Skipping Tier 2 for "Obvious" Cases
**Problem:** Assuming high order counts mean everything is fine
**Why it fails:** System data can show activity while qualitative data reveals blockers, timeline risks, or sentiment issues
**Solution:** Run Tier 2 summary retrieval for ALL clients with recent Fathom calls, regardless of system data status

### Mistake 5: Treating Help Scout as Optional
**Problem:** Checking Fathom but skipping Help Scout, or only checking Support mailbox
**Why it fails:** Critical engagement signals often appear ONLY in Help Scout:
- File uploads (30+ images uploaded = very active, even with no Fathom calls)
- Meeting scheduling (shows upcoming engagement)
- Technical support (shows active usage)
**Solution:** Query BOTH Help Scout mailboxes (Support + Onboarding) for EVERY client. Help Scout is EQUALLY MANDATORY as Fathom.

### Mistake 6: Concluding "No Activity" Without Checking All Sources
**Problem:** Seeing no Fathom calls and concluding client is disengaged
**Why it fails:** Client may be actively uploading files, emailing about meetings, or working through support tickets
**Solution:** NEVER conclude "no activity" until you have checked:
1. Fathom calls (get_meetings)
2. Help Scout Support tickets
3. Help Scout Onboarding tickets
4. MCP system data (orders, imports, logins)

---

## MCP Endpoints Required

| Endpoint | Purpose | Batch | Stages |
|----------|---------|-------|--------|
| `get_organization_info` | Org status and settings | 1 | 1, 7, 8, 9, 10, 11, 12 |
| `get_org_users` | User configuration | 1 | 1, 5, 9 |
| `get_data_summary` | Counts (replaces individual calls) | 1 | 2, 5, 6 |
| `get_price_levels` | Pricing setup | 2 | 3 |
| `get_categories` | Taxonomy | 2 | 2 |
| `get_collections` | Product organization | 2 | 2 |
| `get_options` | Options validation (conditional) | 2 | 4 |
| `get_user_territories` | Territory validation (conditional) | 3 | 5, 12 |
| `get_import_events` | Data health | 3 | 6, 11 |
| `get_smart_stacks` | Smart list config (conditional) | 3 | 6 |
| `get_inventories` | Inventory data | 3 | 6 |
| `get_mobile_sites` | eCat Online site config | 4 | 7, 8 |
| `get_reports_config` | Report formats | 4 | 7 |
| `get_orders` | Order validation | 4 | 7, 10 |
| `get_permissions_summary` | User permissions | 4 | 5, 9, 12 |

---

## BigQuery Endpoints Required

| Query | Purpose | Stage |
|-------|---------|-------|
| Consolidated query (iPad + Help Scout) | Multi-source validation | 7, All |

---

## Accuracy Validation

**Tested January 14, 2026 against 7 clients:**

| Client | Fast Mode Result | Full Mode Comparison | Accuracy |
|--------|------------------|----------------------|----------|
| JCUSA | Stage 7, 90%, ✅ | Same | ✅ Match |
| DCCL | Stage 8, 75%, ⚠️ | Same | ✅ Match |
| KRB | Stage 7, 60%, ⚠️ | Same | ✅ Match |
| CST | Stage 7, 50%, 🔴 | Same | ✅ Match |
| TCD | Stage 5, 25%, 🔴 | Same | ✅ Match |
| MALI | Stage 3, 25%, ✅ | Same | ✅ Match |
| PEBL | Stage 3, 10%, 🔴 | Same | ✅ Match |

**Result:** 100% agreement on stage + status between Fast and Full modes in test run.

---

## Performance Metrics

| Metric | Target | Jan 14 Test |
|--------|--------|-------------|
| Execution time (7 clients) | < 35 min | 32 min |
| Per-client average | < 5 min | 4.5 min |
| Flags detected vs Full Mode | > 80% | 100% |
| Stage agreement | 100% | 100% |
| Context tokens per client | < 6K | ~5K |

---

## Approvals

| Role | Name | Date | Status |
|------|------|------|--------|
| **Author** | Kylor Johnson | Jan 14, 2026 | ✅ Complete (V11) |
| **CS Lead** | [Name] | [Date] | ⏳ Pending |
| **Engineering Lead** | [Name] | [Date] | ⏳ Pending |
| **Product Manager** | [Name] | [Date] | ⏳ Pending |

---

**Document Status:** Production Ready  
**Version:** 11.3 (Fast Mode + Fathom API Fix + Help Scout Mandatory)  
**Last Updated:** January 14, 2026  
**Contact:** Kylor Johnson
