# Validation Layer: Fathom & Help Scout

**Purpose:** Add qualitative validation to quantitative data from Stage_Gated_Data_Collection.md  
**Input:** Client list and metrics from Data Collection  
**Output:** Validation flags, recent activity, sentiment analysis  
**Next Step:** Run `Notion_Output_Format.md`

**Reference:** See `BIGQUERY_WINDMILL_MCP_REFERENCE.md` for complete BigQuery setup and table documentation

---

## ⛔ THIS DOCUMENT RUNS SECOND

**Prerequisites:**
1. ✅ `Stage_Gated_Data_Collection.md` has been completed
2. ✅ You have the client list with MCP shortnames and domains

**If prerequisites not met:** STOP. Run Data Collection first.

---

## 🔄 DATA FRESHNESS CHECK

**Before starting validation, check BigQuery data freshness:**

```
Tool: user-bigquery-vpn > query
Parameters:
  query: |
    SELECT 'fathom (parsed - PRIMARY)' as source, MAX(`Meeting Start Time`) as latest_record
    FROM fathom__ai_summaries_parsed
    UNION ALL
    SELECT 'fathom (ai_summaries - STALE)' as source, MAX(`Meeting Start Time`) as latest_record
    FROM fathom__ai_summaries
    UNION ALL
    SELECT 'fathom (call_transcripts - STALE)' as source, MAX(`Meeting Scheduled Start Time`) as latest_record
    FROM fathom__call_transcripts
    UNION ALL
    SELECT 'helpscout (latest thread reply)' as source, MAX(thread_created_at) as latest_record
    FROM helpscout__help_scout_tickets
  max_results: 10
```

**⚠️ CRITICAL (as of March 2026):** The `fathom__ai_summaries` Weld sync is broken and stuck at ~Feb 4, 2026. **Always use `fathom__ai_summaries_parsed`** as the primary Fathom table — it has fresh data synced daily.

**⚠️ NOTE:** `fathom__call_transcripts` is also stale (stuck at ~Feb 4, 2026). It contains full `Transcript Plaintext` for deeper keyword searches but only covers meetings up to that date. Check freshness before relying on it.

**If data is >2 days old:**
- ⚠️ Check for manual validation data files in `onboarding-models/MANUAL_VALIDATION_DATA_[DATE].md`
- Use manual data for clients covered in those files
- Note in your output: "Data source: Manual entry (BigQuery stale as of [date])"

---

## EXECUTION RULES

### Rule 1: 100% Certainty Required

Before stating "no recent calls" or "no tickets found", you MUST be 100% certain. Follow EVERY validation step in this document.

### Rule 2: Get ALL Activity First, Then Filter

```
⛔ FORBIDDEN: Filtering by client name in initial queries
⛔ FORBIDDEN: Assuming a call isn't relevant based on title alone
⛔ FORBIDDEN: Skipping meetings with "[Hold]" in the title
```

**Correct approach:** Get ALL activity, THEN match to clients using multiple signals.

### Rule 3: Multiple Matching Signals Required

Even if a meeting title contains a client name, you MUST STILL:
1. Get the full meeting data from BigQuery (summary + all invitee/domain columns)
2. Check attendee email domains across ALL 10 invitee_email columns and ALL 5 external_domain columns
3. Verify the meeting content is actually about that client

Even if NO meeting title matches a client, you MUST STILL:
1. Review ALL meeting summaries for client email domains in attendee lists
2. Check for implementation/onboarding keywords

---

## STEP 1: GET ALL FATHOM MEETINGS (UNFILTERED)

### Execute This Query First

**Use MCP BigQuery Tool — use `fathom__ai_summaries_parsed` (the fresh, actively-synced table):**

```
Tool: user-bigquery-vpn > query
Parameters:
  query: |
    SELECT 
      ID as recording_id,
      `Meeting Title` as meeting_title,
      `Meeting Start Time` as meeting_start,
      `Meeting Duration in Minutes` as duration_minutes,
      `Fathom User Name` as fathom_user,
      `Meeting Has External Invitees` as has_external,
      external_domain_1,
      external_domain_2,
      external_domain_3,
      external_domain_4,
      external_domain_5,
      invitee_email_1,
      invitee_email_2,
      invitee_email_3,
      invitee_email_4,
      invitee_email_5,
      invitee_email_6,
      invitee_email_7,
      invitee_email_8,
      invitee_email_9,
      invitee_email_10,
      `Meeting Invitees Name` as invitee_names,
      `Recording Share URL` as recording_url
    FROM fathom__ai_summaries_parsed
    WHERE `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 14 DAY)
    ORDER BY `Meeting Start Time` DESC
  max_results: 200
```

**Important Notes:**
- **PRIMARY TABLE: `fathom__ai_summaries_parsed`** — this is the actively-synced table with fresh data
- ⚠️ DO NOT use `fathom__ai_summaries` — its Weld sync is broken (stuck at ~Feb 4, 2026)
- Column names have spaces and require backticks: `` `Meeting Title` ``
- **External domains are PRE-PARSED** into individual columns: `external_domain_1` through `external_domain_5`
- **Invitee emails are PRE-PARSED** into individual columns: `invitee_email_1` through `invitee_email_10`
- ⚠️ **YOU MUST CHECK ALL 10 invitee email columns** — live data shows ~37% of meetings have attendees in slots 6-10. Queries that only check slots 1-5 will miss client matches.
- To match a domain, check across ALL domain columns (1-5): `external_domain_1 LIKE '%domain%' OR external_domain_2 LIKE '%domain%' OR ...`
- **MEDDIC fields are INCLUDED** on this table (Situation, Pain, Impact, etc.) — no need for a separate table
- `Meeting Invitees Name` contains comma-separated attendee names
- Summary column is `` `Ai Summary Plaintext Formatted` `` (note: lowercase 'i' in 'Ai')
- `Recording Share URL` provides a direct link to the Fathom recording for human review
- No need for local Python scripts - query directly via MCP

### Output: Complete Meeting List

Document ALL meetings returned:

```markdown
## FATHOM MEETINGS (Last 14 Days)

| Date | Time | Recording ID | Duration | Title | External Domains |
|------|------|--------------|----------|-------|------------------|
| 2026-02-04 | 21:00 | 123456789 | 60min | SuperCat / Venue - Intro | venueindustries.com |
| ... | ... | ... | ... | ... | ... |

**Total Meetings:** [X]
**Today's Meetings:** [X]
```

---

## STEP 2: MATCH MEETINGS TO CLIENTS

### ⚠️ CRITICAL: "[Hold]" Is NOT a Status Indicator

**"[Hold]" in meeting titles is a CALENDAR PLACEHOLDER for recurring meetings.**

| Title Pattern | What It Means | What To Do |
|---------------|---------------|------------|
| "[Hold] Client Standup" | Recurring meeting placeholder | **GET SUMMARY** - contains active progress |
| Any title with "[Hold]" | Calendar hold, NOT implementation hold | **NEVER assume paused** |

**ALWAYS retrieve `get_summary()` for every call. NEVER assume status from title.**

### Client Matching Logic

For EACH meeting from Step 1, attempt to match using these signals (in order):

1. **Title Match:** Does the title contain the client's company name or MCP shortname?
2. **Domain Match:** Do the attendee emails match the client's domain (from HubSpot)?
3. **Keyword Match:** Does the title contain implementation/onboarding keywords?

### Get Summary for EVERY Potentially Relevant Meeting

**Use MCP BigQuery Tool to get full meeting summary + MEDDIC fields (all on one table now):**

```
Tool: user-bigquery-vpn > query
Parameters:
  query: |
    SELECT 
      ID,
      `Meeting Title`,
      `Meeting Start Time`,
      `Fathom User Name`,
      `Meeting Invitees Name`,
      `Ai Summary Plaintext Formatted` as summary,
      `AI Summary Sections Title` as section_titles,
      `Recording Share URL`,
      invitee_email_1, invitee_email_2, invitee_email_3,
      invitee_email_4, invitee_email_5, invitee_email_6,
      invitee_email_7, invitee_email_8, invitee_email_9,
      invitee_email_10,
      external_domain_1, external_domain_2, external_domain_3,
      external_domain_4, external_domain_5,
      Situation, Pain, Impact, `Critical Event`, `Decision Process`,
      `Economic Buyer`, `Solution Fit`, `Tech Stack`, Objections, Competitors,
      Timeline, `Next Steps`
    FROM fathom__ai_summaries_parsed
    WHERE ID = [RECORDING_ID]
  max_results: 1
```

**Note:** MEDDIC fields (Situation, Pain, Impact, Critical Event, etc.) are now included directly on `fathom__ai_summaries_parsed`. The old `fathom__sales_meetings_from_fathom_hubspot` table still exists if you need HubSpot CRM context (company_name, deal_name, deal_stage), but its sync is also stale (~Feb 5, 2026).

**Alternative: Get summaries for multiple meetings matched to a client:**

```
Tool: user-bigquery-vpn > query
Parameters:
  query: |
    SELECT 
      ID,
      `Meeting Title`,
      `Meeting Start Time`,
      LEFT(`Ai Summary Plaintext Formatted`, 1000) as summary_preview,
      `Recording Share URL`,
      invitee_email_1, invitee_email_2, invitee_email_3,
      invitee_email_4, invitee_email_5, invitee_email_6,
      invitee_email_7, invitee_email_8, invitee_email_9,
      invitee_email_10,
      external_domain_1, external_domain_2, external_domain_3,
      external_domain_4, external_domain_5
    FROM fathom__ai_summaries_parsed
    WHERE `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 14 DAY)
      AND (
        LOWER(`Meeting Title`) LIKE '%[CLIENT_NAME]%'
        OR LOWER(invitee_email_1) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_2) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_3) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_4) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_5) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_6) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_7) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_8) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_9) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(invitee_email_10) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(external_domain_1) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(external_domain_2) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(external_domain_3) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(external_domain_4) LIKE '%[CLIENT_DOMAIN]%'
        OR LOWER(external_domain_5) LIKE '%[CLIENT_DOMAIN]%'
      )
    ORDER BY `Meeting Start Time` DESC
  max_results: 50
```

### Why Attendee Email Domains Matter

- A meeting titled "Weekly Implementation Standup" may not mention the client name
- BUT `external_domain_1..5` and `invitee_email_1..10` contain client domains (pre-parsed into individual columns)
- ⚠️ **YOU MUST CHECK ALL 10 invitee email columns AND ALL 5 domain columns** — ~37% of meetings have attendees in slots 6-10
- Match these fields against HubSpot company domains
- Use `LOWER()` and `LIKE '%domain%'` across ALL invitee/domain columns

### Output: Meeting-to-Client Mapping

```markdown
## MEETING-CLIENT MAPPING

| Recording ID | Date | Title | Matched Client | Match Method |
|--------------|------|-------|----------------|--------------|
| 123456789 | 2026-01-21 | MagicLite Onboarding | mali | Title match |
| 123456790 | 2026-01-20 | [Hold] Weekly Standup | cst | Attendee email domain |
| 123456791 | 2026-01-19 | Internal Team Sync | NONE | Not client-related |

**Clients with meetings this week:** [list]
**Clients with NO meetings this week:** [list]
```

---

## STEP 3: GET ALL HELP SCOUT TICKETS (UNFILTERED)

### Execute This Query First

**Use MCP BigQuery Tool — use the `helpscout__help_scout_tickets` denormalized view (pre-joined, includes all fields):**

```
Tool: user-bigquery-vpn > query
Parameters:
  query: |
    SELECT DISTINCT
      ticket_number,
      ticket_subject,
      ticket_status,
      ticket_created_at,
      thread_created_at,
      thread_type,
      thread_created_by_type,
      conv_customer_organization,
      conv_creator_email,
      conv_customer_email,
      thread_customer_email_value,
      thread_user_name,
      thread_user_email,
      agent_name,
      mailbox_name,
      LEFT(thread_body, 400) as thread_content
    FROM helpscout__help_scout_tickets
    WHERE thread_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 14 DAY)
    ORDER BY thread_created_at DESC
    LIMIT 200
  max_results: 200
```

**⚠️ CRITICAL: `ticket_created_at` vs `thread_created_at`**

| Column | What It Means | When to Use |
|--------|--------------|-------------|
| `ticket_created_at` | When the conversation was FIRST OPENED | Finding when onboarding started |
| `thread_created_at` | When each individual REPLY was sent | **ALWAYS use this for "last activity"** |

This table is **denormalized** — each row is a ticket+thread combination. A ticket created Feb 5 may have replies through Mar 10. If you filter by `ticket_created_at`, you'll miss all recent replies on older tickets. **Always filter and sort by `thread_created_at` to find recent activity.**

**⚠️ CRITICAL: Three separate email columns exist — you MUST check ALL THREE for client matching:**

| Column | What It Contains | When It Differs |
|--------|-----------------|-----------------|
| `conv_creator_email` | Email of whoever created the conversation | **Often a SuperCat agent email** when agent creates ticket on behalf of customer |
| `conv_customer_email` | The customer's email on the conversation | **Most reliable for client domain matching** |
| `thread_customer_email_value` | Customer email at the thread level | May be NULL on some threads (populated on ~77% of recent rows) |

Live data shows **~10% of recent tickets have `conv_creator_email` != `conv_customer_email`** — typically when a SuperCat agent (e.g., `jimmy@supercatsolutions.com`) created the conversation. If you only match on `conv_creator_email`, you will match the agent's domain instead of the client's.

**Key Table: `helpscout__help_scout_tickets` (Denormalized View)**

This is the **recommended table** — it pre-joins conversation + threads + customer + mailbox + agent data:
- `ticket_number`, `ticket_subject`, `ticket_status`, `ticket_created_at`, `ticket_closed_at`
- `ticket_user_updated_at` — when the ticket was last updated by any user
- `conv_customer_organization` — customer's company name
- `conv_customer_email` — **customer's email address (PRIMARY for domain matching)**
- `conv_creator_email` — email of whoever created the conversation (may be agent OR customer)
- `thread_customer_email_value` — customer email at thread level (SECONDARY for domain matching)
- `thread_created_at` — **when this specific reply/thread was created (USE THIS for "last activity")**
- `thread_type` — type of thread entry (e.g., `customer`, `message`, `note`, `lineitem`)
- `thread_created_by_type` — who created this thread (`customer` or `user`/agent)
- `thread_user_name` — name of the person who posted this thread
- `thread_user_email` — email of the person who posted this thread
- `agent_name`, `agent_email` — assigned agent info
- `mailbox_name` — mailbox (Support, Onboarding)
- `thread_body` — full thread content (for body searches)
- `ticket_tags` — RECORD REPEATED (nested struct, not a simple array — use UNNEST() to query)

**Raw tables still available if needed:**
- `helpscout__conversation` — base ticket data
- `helpscout__conversation_threads` — threads (join: `CAST(c.id AS STRING) = t.conversation_id`)
- `helpscout__customer` — customer info
- `helpscout__customer_email` — customer emails

### Output: Complete Ticket List

```markdown
## HELP SCOUT TICKETS (Last 14 Days by Thread Activity)

| # | Thread Date | Ticket Created | Subject | Status | Customer Email | Thread By | Mailbox |
|---|-------------|----------------|---------|--------|----------------|-----------|---------|
| 13859 | 2026-01-21 | 2026-01-15 | [Subject] | open | cust@client.com | [thread_user_name] | Support |
| 13860 | 2026-01-21 | 2026-01-10 | [Subject] | open | cust@client.com | [thread_user_name] | Onboarding |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Total Thread Entries (14d):** [X]
**Today's Thread Activity:** [X]
**Note:** "Thread Date" = `thread_created_at` (latest reply), "Ticket Created" = `ticket_created_at` (conversation start)
```

---

## STEP 4: MATCH TICKETS TO CLIENTS

### Matching Logic

For EACH ticket from Step 3, attempt to match using these signals:

1. **Organization Match:** Does `conv_customer_organization` match the client name?
2. **Customer Email Domain Match:** Does `conv_customer_email` domain match the client's domain? (PRIMARY — most reliable)
3. **Creator Email Domain Match:** Does `conv_creator_email` domain match the client's domain? (SECONDARY — may be agent email)
4. **Thread Customer Email Match:** Does `thread_customer_email_value` domain match? (TERTIARY — not always populated)
5. **Subject Match:** Does `ticket_subject` contain the client name?
6. **Thread Body Match:** Does `thread_body` contain the client name?

**⚠️ CRITICAL:** Always check `conv_customer_email` FIRST — it is the most reliable for client domain matching. `conv_creator_email` is often a SuperCat agent's email when the agent created the ticket on behalf of a customer.

### ⚠️ CRITICAL: Non-English Subjects

Tickets may have non-English subjects (Chinese, Spanish, etc.) that won't match by subject alone.

**Solution:** ALWAYS search `thread_body` field (on `helpscout__help_scout_tickets`) AND match by ALL email domain columns (`conv_customer_email`, `conv_creator_email`, `thread_customer_email_value`).

### Extended Search Query (If Needed)

For deeper client-specific searches using the denormalized view:

```
Tool: user-bigquery-vpn > query
Parameters:
  query: |
    SELECT DISTINCT
      ticket_number,
      ticket_subject,
      ticket_status,
      ticket_created_at,
      conv_customer_organization,
      conv_customer_email,
      conv_creator_email,
      thread_customer_email_value,
      mailbox_name,
      LEFT(thread_body, 1000) as thread_content
    FROM helpscout__help_scout_tickets
    WHERE (
      LOWER(conv_customer_organization) LIKE '%[CLIENT_NAME]%'
      OR LOWER(conv_customer_email) LIKE '%@[CLIENT_DOMAIN]%'
      OR LOWER(conv_creator_email) LIKE '%@[CLIENT_DOMAIN]%'
      OR LOWER(thread_customer_email_value) LIKE '%@[CLIENT_DOMAIN]%'
      OR LOWER(ticket_subject) LIKE '%[CLIENT_NAME]%'
      OR LOWER(ticket_preview) LIKE '%[CLIENT_NAME]%'
      OR LOWER(thread_body) LIKE '%[CLIENT_NAME]%'
    )
    AND thread_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY)
    ORDER BY thread_created_at DESC
    LIMIT 100
  max_results: 100
```

### Output: Ticket-to-Client Mapping

```markdown
## TICKET-CLIENT MAPPING

| Ticket # | Last Reply | Ticket Created | Subject | Matched Client | Match Method | Status |
|----------|------------|----------------|---------|----------------|--------------|--------|
| 13859 | 2026-01-21 | 2026-01-15 | [Subject] | mali | conv_customer_email domain | open |
| 13860 | 2026-01-20 | 2025-12-10 | 产品问题 | pebl | Thread body + conv_customer_email | closed |
| 13861 | 2026-01-20 | 2026-01-18 | [Subject] | krb | conv_customer_email (creator was agent) | open |
| 13862 | 2026-01-19 | 2026-01-19 | [Subject] | NONE | Not client-related | - |

**Clients with recent thread activity (30d):** [list — based on `thread_created_at`]
**Clients with NO thread activity (180d):** [list — based on `thread_created_at`]
```

---

## STEP 5: EXTRACT VALIDATION FLAGS

### Flag Types

| Flag | Meaning | When to Apply |
|------|---------|---------------|
| 🔴 CONTRADICT | Evidence contradicts MCP data | Fathom summary shows status different from MCP |
| 🔴 BLOCKER | Critical gap identified in call | Client mentioned blocker in recent call |
| 🔴 STALLED | Implementation on hold | Call summary indicates pause/delay |
| 🔴 SENTIMENT | Negative client sentiment | Frustrated, disappointed, cancel mentioned |
| ⚠️ REVIEW | Potential issue needs clarification | Unclear status, conflicting signals |
| ⚠️ TIMELINE | Missed or at-risk deadline | Specific dates mentioned, deadlines discussed |
| ⚠️ ACTIVITY | Low/no engagement | No calls in 30+ days, no Help Scout thread activity (`thread_created_at`) in 30+ days |
| ⚠️ UNFULFILLED | Commitment not delivered | Action items from previous calls not done |
| ⚠️ MEETING | Meeting scheduled/pending | Future meeting mentioned |
| ✅ ACTIVE | Active engagement confirmed | Recent call with progress |
| ✅ CONFIRMED | Qualitative validates quantitative | Fathom confirms MCP data |

### Keywords to Search For

In Fathom summaries and Help Scout tickets, search for these patterns:

**🔴 Red Flag Keywords:**
- "test data", "sample products", "placeholder"
- "re-import", "clobbered", "wrong data"
- "not ready", "haven't tested", "not set up yet"
- "disappointed", "frustrated", "cancel", "concerned"
- "paused", "on hold", "delayed", "pushed back"

**⚠️ Yellow Flag Keywords:**
- "by end of week", "next month", "target date"
- "need to follow up", "waiting on", "pending"
- "questions about", "confused", "unclear"

**✅ Green Flag Keywords:**
- "making progress", "looks good", "ready to test"
- "launched", "live", "successful"
- "happy with", "impressed", "excited"

### Output: Validation Flags Per Client

```markdown
## VALIDATION FLAGS: [CLIENT SHORTNAME]

### Recent Activity Summary
- **Last Fathom Call:** [Date] - [Title]
- **Call Summary:** [2-3 key points]
- **Open Tickets:** [X]
- **Last Ticket Activity:** [thread_created_at Date] - [Subject] (by [thread_user_name])

### Flags Identified

| Flag | Source | Date/ID | Evidence |
|------|--------|---------|----------|
| ✅ ACTIVE | Fathom | 2026-01-20 / 123456789 | "Making good progress on catalog setup" |
| ⚠️ TIMELINE | Fathom | 2026-01-20 / 123456789 | "Hoping to launch by end of January" |
| ⚠️ REVIEW | Help Scout | 13859 | Question about price level configuration |

### Sentiment Analysis
- **Overall Sentiment:** [Positive / Neutral / Negative / Concerned]
- **Key Quotes:** "[exact quote from call or ticket]"

### Action Items from Recent Calls
1. [Action item and owner]
2. [Action item and owner]
```

---

## STEP 6: CERTIFICATIONS

### "No Fathom Calls" Certification

Before stating "No Fathom calls found" for a client, you MUST certify:

- [ ] Got ALL meetings (unfiltered) in Step 1 from `fathom__ai_summaries_parsed`
- [ ] Checked for client company name in ALL titles
- [ ] Checked for MCP shortname in ALL titles
- [ ] Checked for implementation/onboarding keywords in titles
- [ ] Got summaries for ambiguous meetings and checked ALL `invitee_email_1..10` (all 10 columns) and ALL `external_domain_1..5` (all 5 columns) — pre-parsed, use LIKE on each
- [ ] Verified "[Hold]" meetings were NOT skipped
- [ ] Extended search to 30 days if nothing found in 14 days

**If ALL checked:** You may state "No Fathom calls found in last [X] days"

### "No Help Scout Tickets" Certification

Before stating "No Help Scout tickets found" for a client, you MUST certify:

- [ ] Got ALL tickets (unfiltered) in Step 3 from `helpscout__help_scout_tickets` **using `thread_created_at`** (NOT `ticket_created_at`)
- [ ] Searched by company name in `conv_customer_organization` field
- [ ] Searched by company name in `ticket_subject` field
- [ ] Searched by email domain in `conv_customer_email` field (PRIMARY — most reliable)
- [ ] Searched by email domain in `conv_creator_email` field (SECONDARY — may be agent email)
- [ ] Searched by email domain in `thread_customer_email_value` field (TERTIARY)
- [ ] Searched `thread_body` field (catches non-English subjects)
- [ ] Extended search to 180 days **using `thread_created_at`** as the time filter
- [ ] Verified "Last Activity" dates reflect `thread_created_at` (latest reply), NOT `ticket_created_at` (conversation start)

**If ALL checked:** You may state "No Help Scout tickets found in last [X] days"

---

## CONFIDENCE SCORING

### Combine MCP Data + Validation

| MCP Stage Status | Validation Result | Confidence | Meaning |
|------------------|-------------------|------------|---------|
| 🟢 GREEN | ✅ CONFIRMED | **95%+** | High confidence, proceed |
| 🟢 GREEN | No flags | **80%** | Good confidence, minor uncertainty |
| 🟢 GREEN | ⚠️ REVIEW | **60%** | Medium confidence, follow up needed |
| 🟢 GREEN | 🔴 CONTRADICT | **30%** | Low confidence, investigate immediately |
| Any | ❓ UNKNOWN | **0%** | Cannot assess, manual verification required |

---

## OUTPUT FORMAT

### Recent Activity Report (Start of Output)

```markdown
## 📋 RECENT ACTIVITY REPORT

**Generated:** [TODAY'S DATE]
**Assessment Scope:** [X] clients from HubSpot onboarding list

### Today's Activity
- **Fathom Meetings Today:** [X] - [list client shortnames]
- **Help Scout Tickets Today:** [X] - [list client shortnames]

### This Week's Activity (7 days)
- **Fathom Meetings:** [X]
- **Help Scout Tickets:** [X]

### Unmatched Activity (Review Manually)

| Source | Date | Title/Subject | Notes |
|--------|------|---------------|-------|
| Fathom | 2026-01-20 | Internal Team Meeting | Not client-related |
| Help Scout | 2026-01-19 | General inquiry | No client match |
```

### Per-Client Validation Summary

```markdown
---

## VALIDATION: [CLIENT SHORTNAME]

**Last Fathom Call:** [Date] - [Title]
**Open Tickets:** [X] | **Last Ticket Activity:** [thread_created_at Date] (by [thread_user_name])

### Flags

| Flag | Source | Evidence |
|------|--------|----------|
| [🔴/⚠️/✅] [TYPE] | [Fathom/HS] [Date/ID] | "[quote or description]" |

### Confidence Score
- **MCP Status:** [Stage X - 🟢/🟡/🔴]
- **Validation Result:** [✅ CONFIRMED / ⚠️ REVIEW / 🔴 CONTRADICT]
- **Combined Confidence:** [X]%

### Key Takeaway
[1-2 sentence summary of client status and any required follow-up]

---
```

---

## NEXT STEP

After completing validation for ALL clients:

**Run:** `Notion_Output_Format.md`

This will format all data (quantitative from Data Collection + qualitative from this Validation Layer) into the exact Notion output format.

---

## COMMON MISTAKES TO AVOID

### Mistake 1: Skipping "[Hold]" Meetings
**Wrong:** "Meeting titled '[Hold] Weekly Standup' - skipping as it's on hold"
**Right:** Get the full meeting data. "[Hold]" is a calendar placeholder, the meeting still happened.

### Mistake 2: Only Checking Meeting Titles
**Wrong:** "No meetings found with 'ClientName' in title"
**Right:** Check ALL `external_domain_1..5` AND ALL `invitee_email_1..10` columns using `LIKE '%domain%'` (pre-parsed into individual columns on `fathom__ai_summaries_parsed`). ~37% of meetings have attendees in slots 6-10. Generic titles like "Implementation Call" may be client meetings.

### Mistake 3: Missing Non-English Tickets
**Wrong:** "No tickets found matching 'ClientName' in subject"
**Right:** Search `thread_body` on `helpscout__help_scout_tickets` AND match by `conv_customer_email` domain (PRIMARY), `conv_creator_email` domain (SECONDARY), and `thread_customer_email_value` domain (TERTIARY). Subjects may be in Chinese, Spanish, etc.

### Mistake 4: Filtering Too Early
**Wrong:** Only querying for meetings with specific client name in WHERE clause
**Right:** Get ALL meetings first, THEN match to clients using multiple signals in post-processing.

### Mistake 5: Not Checking Multiple Match Signals
**Wrong:** "Meeting titled 'Weekly Standup' - probably internal, skipping"
**Right:** Check ALL `external_domain_1..5`, ALL `invitee_email_1..10` columns (pre-parsed on `fathom__ai_summaries_parsed`), and summary content. Could be a client meeting.

### Mistake 9: Only Using `conv_creator_email` for Help Scout Domain Matching
**Wrong:** Matching tickets to clients using only `conv_creator_email` domain
**Right:** `conv_creator_email` is often a SuperCat agent's email (e.g., `jimmy@supercatsolutions.com`) when the agent created the ticket. **Always use `conv_customer_email` as the PRIMARY email for domain matching.** Also check `thread_customer_email_value` as a secondary signal. Live data shows ~10% of tickets have different creator vs customer emails.

### Mistake 6: Stating "No Activity" Without Certification
**Wrong:** "No recent calls found for this client"
**Right:** Complete the certification checklist FIRST, then state finding with proof.

### Mistake 7: Using the Wrong (Stale) Fathom Table
**Wrong:** Using `fathom__ai_summaries` (Weld sync broken since ~Feb 4, 2026 — data is over a month stale)
**Right:** Use `fathom__ai_summaries_parsed` for ALL Fathom queries — it has fresh data synced daily, includes MEDDIC fields, and has pre-parsed invitee/domain columns. Column name for summary: `` `Ai Summary Plaintext Formatted` `` (note: lowercase 'i' in 'Ai')

**Also stale:** `fathom__call_transcripts` (stuck at ~Feb 4, 2026). Contains full `Transcript Plaintext` for deep keyword searches but is not current.

### Mistake 8: Looking for MEDDIC Fields on a Separate Table
**Wrong:** Querying `Situation`, `Pain`, `Impact` from a separate `fathom__sales_meetings_from_fathom_hubspot` table
**Right:** MEDDIC/SPICED fields (Situation, Pain, Impact, Critical Event, etc.) are now included directly on `fathom__ai_summaries_parsed`. The `fathom__sales_meetings_from_fathom_hubspot` table still exists for HubSpot CRM context (company_name, deal_name, deal_stage) but is also stale.

### Mistake 10: Using `ticket_created_at` Instead of `thread_created_at` for Activity
**Wrong:** Filtering/ordering by `ticket_created_at` to find "recent Help Scout activity" — this only shows when the conversation was first opened
**Right:** **Always use `thread_created_at`** for assessing recent activity. The `helpscout__help_scout_tickets` table is denormalized (one row per ticket+thread). A ticket created Feb 5 can have replies through Mar 10. If you filter by `ticket_created_at >= 14 days ago`, you'll miss ALL recent replies on older tickets. This is the #1 cause of incorrectly marking clients as "stalled" when they're actively engaged.

### Mistake 11: Only Reading `ticket_preview` for Sentiment
**Wrong:** Using `ticket_preview` (first ~200 chars of the conversation) to assess client sentiment
**Right:** Read `thread_body` of recent threads (filtered by `thread_created_at`). Critical sentiment like UI frustration, data issues, or escalations is often expressed in replies deep in the conversation thread, not in the initial ticket opening message.

---

**Document Purpose:** Qualitative validation only  
**Requires:** Completed Data Collection output  
**Produces:** Validation flags, confidence scores, activity summary
