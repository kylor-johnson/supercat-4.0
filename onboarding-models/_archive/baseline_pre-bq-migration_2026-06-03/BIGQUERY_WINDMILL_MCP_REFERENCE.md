# BigQuery Windmill MCP Reference Guide

> **Purpose**: This document is the definitive reference for querying SuperCat's data warehouse via the BigQuery Windmill MCP connection. Read this entirely before executing any queries.

## Connection Details

- **MCP Server URL**: `http://bigquery-cli-staging.k8s.supercatsolutions.com:3003/mcp`
- **Project**: `supercat-data-pipeline`
- **Connection Name**: May vary by user (e.g., `bigquery-windmill`, `bigquery-mcp`, etc.) but URL is always the same

## Critical Rules & Guardrails

### Query Syntax Rules

1. **DO NOT use fully qualified table names with dots** - The MCP connection is scoped to WELD_RAW dataset
   ```sql
   -- WRONG: Will fail with syntax error
   SELECT * FROM WELD_RAW.helpscout__conversation
   
   -- CORRECT: Use table name directly
   SELECT * FROM helpscout__conversation
   ```

2. **INFORMATION_SCHEMA queries are not supported** - Use the `describe_table` and `list_tables` MCP tools instead

3. **Always use LIMIT** - Never run unbounded queries
   ```sql
   -- ALWAYS include LIMIT
   SELECT * FROM helpscout__conversation LIMIT 100
   ```

4. **Column names with spaces require backticks** - Fathom tables have spaces in column names
   ```sql
   -- Fathom tables need backticks for column names
   SELECT `Meeting Title`, `Fathom User Email` FROM fathom__ai_summaries LIMIT 10
   ```

### Performance Guidelines

1. **Filter on indexed/timestamp columns first** - Most tables have `created_at`, `_weld_synced`, or similar
2. **Avoid SELECT *** - Specify only needed columns, especially for wide tables like HubSpot
3. **Use date range filters** for time-series queries
4. **Max results default is 1000** - Use the `max_results` parameter if you need more

---

## Available Data Sources

### Fresh Data (Updated Daily)

| Source | Tables | Description |
|--------|--------|-------------|
| HelpScout | 13 tables | Support tickets, conversations, customers |
| Fathom | 4 tables | Sales call recordings, AI summaries, transcripts |
| HubSpot | ~25 views | CRM data - companies, contacts, deals, owners |
| Mixpanel | 1 view | Product analytics events |
| Stripe | ~10 views | Billing, invoices, subscriptions, payments |
| QuickBooks | ~15 views | Accounting, invoices, payments |

---

## HelpScout Tables

### Primary Use Cases
- Support ticket analysis and metrics
- Customer satisfaction tracking
- Response time analysis
- Agent performance metrics
- Ticket volume trends

### helpscout__conversation
**Rows**: ~2,600 | **Primary key**: `id`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Unique conversation ID |
| number | INTEGER | Human-readable ticket number |
| type | STRING | Conversation type (email, chat, phone) |
| status | STRING | Status: active, pending, closed, spam |
| state | STRING | State: published, draft, deleted |
| subject | STRING | Conversation subject line |
| preview | STRING | First ~200 chars of content |
| mailbox_id | INTEGER | FK to helpscout__mailbox |
| assignee_id | INTEGER | FK to helpscout__user (agent) |
| created_by_id | INTEGER | FK to customer or user who created |
| created_by_type | STRING | "customer" or "user" |
| created_at | TIMESTAMP | When conversation was created |
| closed_at | TIMESTAMP | When conversation was closed |
| closed_by_user_id | INTEGER | Agent who closed it |
| user_updated_at | TIMESTAMP | Last update timestamp |
| customer_waiting_since_time | INTEGER | Unix timestamp (milliseconds) |
| source_type | STRING | Source: email, api, web |
| source_via | STRING | How it arrived: customer, user |
| tag_ids | ARRAY<INTEGER> | Array of tag IDs |
| cc | ARRAY<STRING> | CC email addresses |
| bcc | ARRAY<STRING> | BCC email addresses |

**Common Queries**:
```sql
-- Recent open tickets
SELECT id, number, subject, status, created_at
FROM helpscout__conversation
WHERE status = 'active'
ORDER BY created_at DESC
LIMIT 50

-- Tickets by status (last 30 days)
SELECT status, COUNT(*) as count
FROM helpscout__conversation
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY status
ORDER BY count DESC

-- Average time to close (last 30 days)
SELECT 
  AVG(TIMESTAMP_DIFF(closed_at, created_at, HOUR)) as avg_hours_to_close
FROM helpscout__conversation
WHERE closed_at IS NOT NULL
  AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
```

### helpscout__conversation_threads
**Rows**: ~19,000 | **Primary key**: `id`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Thread ID |
| conversation_id | STRING | FK to conversation (note: STRING type) |
| type | STRING | Thread type: customer, message, note, lineitem |
| body | STRING | Full HTML/text content of the thread |
| action_type | STRING | Action performed |
| customer_id | INTEGER | Customer who sent (if customer thread) |
| created_by_id | INTEGER | Who created the thread |
| created_by_type | STRING | "customer" or "user" |
| assigned_to_id | INTEGER | Agent assigned |
| status | STRING | Thread status |
| state | STRING | published, draft |
| created_at | TIMESTAMP | When thread was created |
| cc | ARRAY<STRING> | CC recipients |
| to | ARRAY<STRING> | To recipients |

**Common Queries**:
```sql
-- Get full conversation history
SELECT t.type, t.body, t.created_at, t.created_by_type
FROM helpscout__conversation_threads t
WHERE t.conversation_id = '1234567890'
ORDER BY t.created_at ASC

-- Thread counts by conversation
SELECT conversation_id, COUNT(*) as thread_count
FROM helpscout__conversation_threads
GROUP BY conversation_id
ORDER BY thread_count DESC
LIMIT 20
```

### helpscout__help_scout_tickets
**Rows**: ~19,000 | **Denormalized view combining conversation + thread + mailbox + agent data**

This is the **recommended table for most ticket queries** - it's pre-joined and includes all relevant fields.

| Column | Type | Description |
|--------|------|-------------|
| conversation_id | INTEGER | Ticket ID |
| ticket_number | INTEGER | Human-readable number |
| ticket_status | STRING | active, pending, closed |
| ticket_subject | STRING | Subject line |
| ticket_preview | STRING | Content preview |
| ticket_created_at | TIMESTAMP | When created |
| ticket_closed_at | TIMESTAMP | When closed |
| ticket_user_updated_at | TIMESTAMP | Last update |
| mailbox_id | INTEGER | Mailbox ID |
| mailbox_name | STRING | Mailbox name |
| mailbox_email | STRING | Mailbox email address |
| agent_id | INTEGER | Assigned agent ID |
| agent_name | STRING | Agent full name |
| agent_email | STRING | Agent email |
| conv_creator_email | STRING | Customer email who created |
| conv_customer_organization | STRING | Customer's organization |
| thread_id | INTEGER | Individual thread ID |
| thread_body | STRING | Thread content |
| thread_type | STRING | customer, message, note |
| thread_created_at | TIMESTAMP | Thread timestamp |
| ticket_tags | ARRAY<RECORD> | Tags with id, name, color |

**Common Queries**:
```sql
-- Recent tickets with agent info
SELECT 
  ticket_number,
  ticket_subject,
  ticket_status,
  agent_name,
  mailbox_name,
  ticket_created_at
FROM helpscout__help_scout_tickets
WHERE thread_type = 'customer'  -- First message only
ORDER BY ticket_created_at DESC
LIMIT 50

-- Tickets by agent (last 30 days)
SELECT 
  agent_name,
  COUNT(DISTINCT conversation_id) as ticket_count
FROM helpscout__help_scout_tickets
WHERE ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND agent_name IS NOT NULL
GROUP BY agent_name
ORDER BY ticket_count DESC

-- Search ticket content
SELECT 
  ticket_number,
  ticket_subject,
  conv_customer_organization,
  ticket_created_at
FROM helpscout__help_scout_tickets
WHERE LOWER(thread_body) LIKE '%error%'
  OR LOWER(ticket_subject) LIKE '%error%'
ORDER BY ticket_created_at DESC
LIMIT 20
```

### helpscout__customer
**Rows**: ~750 | **Primary key**: `id`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Customer ID |
| first_name | STRING | First name |
| last_name | STRING | Last name |
| organization | STRING | Company/org name |
| job_title | STRING | Job title |
| location | STRING | Location |
| created_at | TIMESTAMP | When created |
| updated_at | TIMESTAMP | Last updated |

### helpscout__mailbox
**Rows**: 2 | **Primary key**: `id`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Mailbox ID |
| name | STRING | Mailbox name (e.g., "SuperCat Support") |
| slug | STRING | URL slug |
| email | STRING | Mailbox email address |

### helpscout__tag
**Rows**: ~43 | **Primary key**: `id`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Tag ID |
| name | STRING | Tag name |
| slug | STRING | URL-friendly name |
| color | STRING | Hex color code |
| ticket_count | INTEGER | Number of tickets with this tag |

### helpscout__user
Agent/team member data with id, email, first_name, last_name, role, created_at

---

## Fathom Tables (Sales Call Intelligence)

### Primary Use Cases
- Sales call analysis and coaching
- Meeting summaries and action items
- Deal intelligence from conversations
- Sales methodology tracking (MEDDIC/SPICED)

### fathom__ai_summaries
**Rows**: ~450 | **Primary key**: `ID`

> **Note**: Column names have spaces - use backticks!

| Column | Type | Description |
|--------|------|-------------|
| ID | INTEGER | Unique meeting ID |
| `Meeting Title` | STRING | Calendar event title |
| `Meeting Start Time` | TIMESTAMP | When meeting started |
| `Meeting End Time` | TIMESTAMP | When meeting ended |
| `Meeting Duration in Minutes` | INTEGER | Total meeting length |
| `Recording Duration in Minutes` | INTEGER | Recorded portion length |
| `Recording URL` | STRING | Link to full recording |
| `Recording Share URL` | STRING | Shareable link |
| `Fathom User Name` | STRING | SuperCat employee on call |
| `Fathom User Email` | STRING | Employee email |
| `Fathom User Team` | STRING | Team name |
| `Meeting Invitees Name` | STRING | Attendee names (comma-separated) |
| `Meeting Invitees Email` | STRING | Attendee emails (comma-separated) |
| `Meeting Invitees Is External` | STRING | External/internal flags |
| `Meeting Has External Invitees` | BOOLEAN | True if external attendees |
| `External Domain Names` | STRING | External company domains |
| `AI Summary Plaintext Formatted` | STRING | Plain text summary |
| `AI Summary Markdown` | STRING | Markdown formatted summary |
| `AI Summary HTML Format` | STRING | HTML formatted summary |
| `AI Summary Template Name` | STRING | Template used for summary |
| `AI Summary Sections Title` | STRING | Section headings |
| `AI Summary Sections Plaintext Format` | STRING | Section content |

**Common Queries**:
```sql
-- Recent sales calls with summaries
SELECT 
  `Meeting Title`,
  `Fathom User Name`,
  `Meeting Start Time`,
  `Meeting Duration in Minutes`,
  `External Domain Names`,
  `AI Summary Plaintext Formatted`
FROM fathom__ai_summaries
WHERE `Meeting Has External Invitees` = TRUE
ORDER BY `Meeting Start Time` DESC
LIMIT 20

-- Calls by team member
SELECT 
  `Fathom User Name`,
  COUNT(*) as call_count,
  AVG(`Meeting Duration in Minutes`) as avg_duration
FROM fathom__ai_summaries
WHERE `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY `Fathom User Name`
ORDER BY call_count DESC
```

### fathom__call_transcripts
**Rows**: ~314 | **Primary key**: `ID`

| Column | Type | Description |
|--------|------|-------------|
| ID | INTEGER | Meeting ID |
| `Meeting Title` | STRING | Calendar title |
| `Transcript Plaintext` | STRING | Full call transcript |
| `Meeting Scheduled Start Time` | TIMESTAMP | Scheduled start |
| `Recording Duration in Minutes` | FLOAT | Recording length |
| `Fathom User Name` | STRING | SuperCat employee |
| `Fathom User Email` | STRING | Employee email |
| `Meeting External Domain Names` | STRING | External domains |

**Common Queries**:
```sql
-- Search transcripts for keywords
SELECT 
  `Meeting Title`,
  `Fathom User Name`,
  `Meeting Scheduled Start Time`,
  SUBSTR(`Transcript Plaintext`, 1, 500) as transcript_preview
FROM fathom__call_transcripts
WHERE LOWER(`Transcript Plaintext`) LIKE '%competitor%'
ORDER BY `Meeting Scheduled Start Time` DESC
LIMIT 10
```

### fathom__sales_meetings_from_fathom_hubspot
**Rows**: ~136 | **The most valuable sales intelligence table - enriched with HubSpot CRM data and AI-extracted deal insights**

| Column | Type | Description |
|--------|------|-------------|
| fathom_meeting_id | INTEGER | Meeting ID |
| `Meeting Title` | STRING | Calendar title |
| `Meeting Start Time` | TIMESTAMP | Start time |
| `Meeting End Time` | TIMESTAMP | End time |
| `Meeting Duration in Minutes` | INTEGER | Duration |
| `Fathom User Name` | STRING | Sales rep name |
| `Fathom User Email` | STRING | Sales rep email |
| `Recording URL` | STRING | Full recording |
| `Recording Share URL` | STRING | Shareable link |
| **AI-Extracted MEDDIC Fields** | | |
| Situation | STRING | Current state/context |
| Pain | STRING | Customer pain points |
| Impact | STRING | Business impact of pain |
| `Critical Event` | STRING | Compelling event/deadline |
| `Decision Process` | STRING | How they make decisions |
| `Economic Buyer` | STRING | Who signs the check |
| `Solution Fit` | STRING | How we solve their problem |
| `Tech Stack` | STRING | Their technology |
| Objections | STRING | Concerns raised |
| Competitors | STRING | Who we're competing against |
| Timeline | STRING | Expected timeline |
| `Next Steps` | STRING | Agreed next actions |
| **HubSpot CRM Data** | | |
| contact_id | INTEGER | HubSpot contact ID |
| contact_email | STRING | Contact email |
| contact_first_name | STRING | Contact first name |
| contact_last_name | STRING | Contact last name |
| contact_owner_name | STRING | Contact owner |
| company_id | INTEGER | HubSpot company ID |
| company_name | STRING | Company name |
| company_owner_name | STRING | Company owner |
| company_engagement_status | STRING | Engagement status |
| company_type | STRING | Company type |
| deal_id | INTEGER | Associated deal ID |
| deal_name | STRING | Deal name |
| deal_stage | STRING | Current deal stage |
| deal_amount | FLOAT | Deal value |
| deal_close_date | TIMESTAMP | Expected close date |
| deal_created_date | TIMESTAMP | When deal was created |

**Common Queries**:
```sql
-- Active deals with recent calls
SELECT 
  company_name,
  deal_name,
  deal_stage,
  deal_amount,
  `Fathom User Name`,
  `Meeting Start Time`,
  Pain,
  `Next Steps`
FROM fathom__sales_meetings_from_fathom_hubspot
WHERE deal_id IS NOT NULL
  AND `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
ORDER BY `Meeting Start Time` DESC

-- Calls mentioning competitors
SELECT 
  company_name,
  deal_name,
  Competitors,
  Objections,
  `Meeting Start Time`
FROM fathom__sales_meetings_from_fathom_hubspot
WHERE Competitors IS NOT NULL AND Competitors != ''
ORDER BY `Meeting Start Time` DESC
LIMIT 20

-- Pipeline with call intelligence
SELECT 
  deal_stage,
  COUNT(DISTINCT deal_id) as deals,
  SUM(deal_amount) as pipeline_value,
  COUNT(*) as total_calls
FROM fathom__sales_meetings_from_fathom_hubspot
WHERE deal_id IS NOT NULL
GROUP BY deal_stage
ORDER BY pipeline_value DESC
```

---

## HubSpot Tables

### Primary Use Cases
- CRM data analysis (companies, contacts, deals)
- Sales pipeline reporting
- Contact and company lookups
- Owner/team assignments

> **Note**: HubSpot tables are VIEWs with hundreds of columns. Always SELECT specific columns, never SELECT *.

### hubspot__company
**Primary key**: `company_id`

**Key Columns** (subset - table has 400+ columns):
| Column | Type | Description |
|--------|------|-------------|
| company_id | INTEGER | Unique company ID |
| properties_name | STRING | Company name |
| properties_domain | STRING | Website domain |
| properties_industry | STRING | Industry |
| properties_city | STRING | City |
| properties_state | STRING | State/province |
| properties_country | STRING | Country |
| properties_numberofemployees | FLOAT | Employee count |
| properties_annualrevenue | FLOAT | Annual revenue |
| properties_hubspot_owner_id | STRING | Owner ID |
| properties_lifecyclestage | STRING | Lifecycle stage |
| properties_createdate | TIMESTAMP | Created date |
| properties_hs_lastmodifieddate | TIMESTAMP | Last modified |

**Common Queries**:
```sql
-- Search companies by name
SELECT 
  company_id,
  properties_name,
  properties_domain,
  properties_industry,
  properties_lifecyclestage
FROM hubspot__company
WHERE LOWER(properties_name) LIKE '%lighting%'
LIMIT 20

-- Companies by lifecycle stage
SELECT 
  properties_lifecyclestage,
  COUNT(*) as count
FROM hubspot__company
WHERE properties_lifecyclestage IS NOT NULL
GROUP BY properties_lifecyclestage
ORDER BY count DESC
```

### hubspot__contact
**Primary key**: `contact_id`

**Key Columns**:
| Column | Type | Description |
|--------|------|-------------|
| contact_id | INTEGER | Unique contact ID |
| properties_email | STRING | Email address |
| properties_firstname | STRING | First name |
| properties_lastname | STRING | Last name |
| properties_phone | STRING | Phone number |
| properties_company | STRING | Company name |
| properties_jobtitle | STRING | Job title |
| properties_hubspot_owner_id | STRING | Owner ID |
| properties_lifecyclestage | STRING | Lifecycle stage |
| properties_createdate | TIMESTAMP | Created date |

**Common Queries**:
```sql
-- Search contacts by email domain
SELECT 
  contact_id,
  properties_email,
  properties_firstname,
  properties_lastname,
  properties_company,
  properties_jobtitle
FROM hubspot__contact
WHERE properties_email LIKE '%@millenniumlighting.com'
LIMIT 50

-- Contacts by owner
SELECT 
  properties_hubspot_owner_id,
  COUNT(*) as contact_count
FROM hubspot__contact
WHERE properties_hubspot_owner_id IS NOT NULL
GROUP BY properties_hubspot_owner_id
ORDER BY contact_count DESC
```

### hubspot__deal
**Primary key**: `deal_id`

**Key Columns**:
| Column | Type | Description |
|--------|------|-------------|
| deal_id | INTEGER | Unique deal ID |
| properties_dealname | STRING | Deal name |
| properties_amount | FLOAT | Deal amount |
| properties_dealstage | STRING | Current stage |
| properties_pipeline | STRING | Pipeline ID |
| properties_closedate | TIMESTAMP | Expected close date |
| properties_createdate | TIMESTAMP | Created date |
| properties_hubspot_owner_id | STRING | Owner ID |
| properties_dealtype | STRING | Deal type |
| properties_closed_lost_reason | STRING | If lost, why |
| properties_closed_won_reason | STRING | If won, why |

**Common Queries**:
```sql
-- Active pipeline
SELECT 
  deal_id,
  properties_dealname,
  properties_dealstage,
  properties_amount,
  properties_closedate
FROM hubspot__deal
WHERE properties_dealstage NOT IN ('closedwon', 'closedlost')
ORDER BY properties_amount DESC
LIMIT 50

-- Won deals last 90 days
SELECT 
  deal_id,
  properties_dealname,
  properties_amount,
  properties_closedate
FROM hubspot__deal
WHERE properties_dealstage = 'closedwon'
  AND properties_closedate >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY properties_closedate DESC
```

### hubspot__owner
**Primary key**: `owner_id`

| Column | Type | Description |
|--------|------|-------------|
| owner_id | STRING | Owner ID (matches hubspot_owner_id) |
| email | STRING | Email address |
| first_name | STRING | First name |
| last_name | STRING | Last name |
| user_id | INTEGER | User ID |
| archived | BOOLEAN | Is archived |

**Joining with owners**:
```sql
-- Deals with owner names
SELECT 
  d.properties_dealname,
  d.properties_amount,
  o.first_name || ' ' || o.last_name as owner_name
FROM hubspot__deal d
LEFT JOIN hubspot__owner o ON d.properties_hubspot_owner_id = o.owner_id
WHERE d.properties_amount > 0
ORDER BY d.properties_amount DESC
LIMIT 20
```

---

## Mixpanel Tables

### mixpanel__events
Product analytics events from the eCat application.

**Key Columns**:
| Column | Type | Description |
|--------|------|-------------|
| event_name | STRING | Event name in snake_case (e.g., "order_submitted", "product_search") |
| time | FLOAT | Unix timestamp |
| distinct_id | STRING | User identifier |
| organization_id | STRING | Org ID |
| organization_shortname | STRING | Org shortname |
| username | STRING | Username |
| uri | STRING | Page/screen URI |
| full_url | STRING | Full URL |
| device_id | STRING | Device identifier |
| os | STRING | Operating system |
| model | STRING | Device model |
| app_version | STRING | App version |
| city | STRING | User city |
| region | STRING | User region |
| mp_country_code | STRING | Country code |
| search_text | STRING | Search query (if search event) |
| item_count | FLOAT | Items in cart/order |
| order_total | FLOAT | Order total |
| _weld_synced | TIMESTAMP | Sync timestamp |

**Common Queries**:
```sql
-- Event counts by type (last 7 days)
SELECT 
  event_name,
  COUNT(*) as count
FROM mixpanel__events
WHERE _weld_synced >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY event_name
ORDER BY count DESC
LIMIT 30

-- Active organizations
SELECT 
  organization_shortname,
  COUNT(*) as event_count,
  COUNT(DISTINCT username) as unique_users
FROM mixpanel__events
WHERE _weld_synced >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND organization_shortname IS NOT NULL
GROUP BY organization_shortname
ORDER BY event_count DESC
LIMIT 50
```

---

## Stripe Tables

### stripe__invoice
Billing invoices.

**Key Columns**:
| Column | Type | Description |
|--------|------|-------------|
| id | STRING | Invoice ID |
| customer_id | STRING | Customer ID |
| subscription_id | STRING | Subscription ID |
| number | STRING | Invoice number |
| status | STRING | draft, open, paid, void, uncollectible |
| amount_due | INTEGER | Amount due (cents) |
| amount_paid | INTEGER | Amount paid (cents) |
| amount_remaining | INTEGER | Remaining (cents) |
| total | INTEGER | Total (cents) |
| currency | STRING | Currency code |
| customer_email | STRING | Customer email |
| customer_name | STRING | Customer name |
| created | TIMESTAMP | Created date |
| due_date | TIMESTAMP | Due date |
| period_start | TIMESTAMP | Billing period start |
| period_end | TIMESTAMP | Billing period end |
| paid | BOOLEAN | Is paid |
| billing_reason | STRING | Why invoice was created |
| hosted_invoice_url | STRING | Payment link |

**Common Queries**:
```sql
-- Recent invoices
SELECT 
  number,
  customer_name,
  status,
  total / 100.0 as total_dollars,
  created,
  due_date
FROM stripe__invoice
WHERE created >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY created DESC
LIMIT 50

-- Revenue by month
SELECT 
  FORMAT_TIMESTAMP('%Y-%m', created) as month,
  SUM(amount_paid) / 100.0 as revenue
FROM stripe__invoice
WHERE status = 'paid'
GROUP BY month
ORDER BY month DESC
LIMIT 12
```

### stripe__customer
Customer records in Stripe.

**Key Columns**:
| Column | Type | Description |
|--------|------|-------------|
| id | STRING | Customer ID |
| name | STRING | Customer name |
| email | STRING | Email address |
| description | STRING | Description |
| created | TIMESTAMP | Created date |
| balance | INTEGER | Account balance (cents) |
| delinquent | BOOLEAN | Is delinquent |
| currency | STRING | Currency |
| metadata | STRING | JSON metadata |

---

## QuickBooks Tables

### quickbooks__invoice
Accounting invoices from QuickBooks.

**Key Columns**:
| Column | Type | Description |
|--------|------|-------------|
| id | STRING | Invoice ID |
| doc_number | STRING | Invoice number |
| txn_date | TIMESTAMP | Transaction date |
| due_date | TIMESTAMP | Due date |
| total_amt | FLOAT | Total amount |
| balance | FLOAT | Outstanding balance |
| customer_ref_name | STRING | Customer name |
| customer_ref_value | STRING | Customer ID |
| email_status | STRING | Email status |
| print_status | STRING | Print status |
| bill_email_address | STRING | Bill-to email |
| meta_data_create_time | TIMESTAMP | Created time |
| meta_data_last_updated_time | TIMESTAMP | Last updated |

**Common Queries**:
```sql
-- Outstanding invoices
SELECT 
  doc_number,
  customer_ref_name,
  total_amt,
  balance,
  due_date
FROM quickbooks__invoice
WHERE balance > 0
ORDER BY due_date ASC
LIMIT 50
```

---

## MCP Tool Reference

### Available Tools

1. **query** - Execute SQL queries
   ```
   query: "SELECT * FROM helpscout__conversation LIMIT 10"
   max_results: 1000 (optional, default 1000, max 10000)
   ```

2. **list_tables** - List all tables in WELD_RAW
   ```
   (no parameters needed)
   ```

3. **describe_table** - Get schema for a specific table
   ```
   table_name: "helpscout__conversation"
   ```

4. **get_table_preview** - Preview first N rows
   ```
   table_name: "helpscout__conversation"
   limit: 10 (optional, default 10, max 100)
   ```

5. **get_event_counts** - Count events (for Mixpanel)
   ```
   table_name: "mixpanel__events"
   event_column: "event_name"
   group_by: "event" | "day" | "week" | "month"
   start_date: "2026-01-01" (optional)
   end_date: "2026-02-01" (optional)
   event_name: "order_submitted" (optional filter)
   ```

6. **get_unique_event_names** - List distinct events
   ```
   table_name: "mixpanel__events"
   event_column: "event_name"
   limit: 100 (optional)
   ```

7. **get_config** - Get current BigQuery configuration
   ```
   (no parameters needed)
   ```

---

## Quick Reference Patterns

### Date Filtering
```sql
-- Last N days
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)

-- Specific date range
WHERE created_at BETWEEN '2026-01-01' AND '2026-01-31'

-- This month
WHERE FORMAT_TIMESTAMP('%Y-%m', created_at) = FORMAT_TIMESTAMP('%Y-%m', CURRENT_TIMESTAMP())
```

### Searching Text
```sql
-- Case-insensitive LIKE
WHERE LOWER(subject) LIKE '%error%'

-- Multiple terms
WHERE LOWER(body) LIKE '%error%' OR LOWER(body) LIKE '%issue%'

-- Exact match
WHERE status = 'active'
```

### Aggregations
```sql
-- Count with grouping
SELECT status, COUNT(*) as count
FROM table
GROUP BY status
ORDER BY count DESC

-- Date bucketing
SELECT 
  FORMAT_TIMESTAMP('%Y-%m', created_at) as month,
  COUNT(*) as count
FROM table
GROUP BY month
ORDER BY month DESC
```

### Joining Tables
```sql
-- HelpScout conversation with threads
SELECT c.number, c.subject, t.body
FROM helpscout__conversation c
JOIN helpscout__conversation_threads t 
  ON CAST(c.id AS STRING) = t.conversation_id
WHERE c.number = 12345

-- HubSpot deal with owner
SELECT d.properties_dealname, o.first_name, o.last_name
FROM hubspot__deal d
LEFT JOIN hubspot__owner o 
  ON d.properties_hubspot_owner_id = o.owner_id
```

---

## Troubleshooting

### Common Errors

1. **"Syntax error: Expected end of input but got '.'"**
   - You're using fully qualified table names. Remove the dataset prefix.
   - Wrong: `WELD_RAW.table_name`
   - Right: `table_name`

2. **"Unrecognized name: column_name"**
   - Column doesn't exist. Use `describe_table` to check schema.
   - For Fathom tables, column names have spaces - use backticks.

3. **"Query returned 0 rows"**
   - Check your filters. Views may show 0 rows in metadata but have data.
   - Try a simpler query first: `SELECT * FROM table LIMIT 1`

4. **Large result truncation**
   - Results are capped. Add `ORDER BY` and `LIMIT` to get relevant rows.
   - Use aggregations instead of raw data when possible.

---

## Data Freshness

| Source | Sync Frequency | Notes |
|--------|----------------|-------|
| HelpScout | Daily | Real-time via Hevo |
| Fathom | Daily | Synced nightly |
| HubSpot | Daily | Most views refresh 6am UTC |
| Mixpanel | Daily | Events sync overnight |
| Stripe | Daily | Transactional data |
| QuickBooks | Daily/Weekly | Invoice data at month start |

---

*Last updated: March 18, 2026*
