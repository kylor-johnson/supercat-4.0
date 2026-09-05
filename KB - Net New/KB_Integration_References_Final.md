# KB Integration References

**Purpose:** Consolidated reference for all integrations used in the KB creation workflow. Read this file once at the start of a KB processing session.

---

## BigQuery - Windmill MCP Connection

**MCP Server:** `bigquery-vpn` (Windmill-based cloud connection)  
**Project:** `supercat-data-pipeline`  
**Dataset:** `WELD_RAW` (automatically scoped)

### ⚠️ CRITICAL SYNTAX RULES

1. **DO NOT use fully qualified table names with dots** - The MCP connection is scoped to WELD_RAW dataset
   ```sql
   -- ❌ WRONG: Will fail with syntax error
   SELECT * FROM WELD_RAW.helpscout__conversation
   
   -- ✅ CORRECT: Use table name directly
   SELECT * FROM helpscout__conversation
   ```

2. **Column names with spaces require backticks** - Fathom tables have spaces in column names
   ```sql
   -- Fathom tables need backticks
   SELECT `Meeting Title`, `Fathom User Email` FROM fathom__ai_summaries LIMIT 10
   ```

3. **Always use LIMIT** - Never run unbounded queries

4. **Use MCP tools for schema discovery** - INFORMATION_SCHEMA queries are not supported

### Available MCP Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `query` | Execute SQL queries | `query: "SELECT * FROM helpscout__conversation LIMIT 10"` |
| `list_tables` | List all available tables | No parameters needed |
| `describe_table` | Get schema for specific table | `table_name: "helpscout__conversation"` |
| `get_table_preview` | Preview first N rows | `table_name: "helpscout__conversation", limit: 10` |
| `get_event_counts` | Count events by time period | For Mixpanel analytics |
| `get_unique_event_names` | List distinct event names | For Mixpanel analytics |
| `get_config` | Get BigQuery configuration | No parameters needed |

---

## BigQuery - Help Scout Data

**Tables:** `helpscout__conversation`, `helpscout__conversation_threads`, `helpscout__help_scout_tickets`

### Find Relevant Conversations

```sql
SELECT 
  id,
  number,
  subject,
  preview,
  status,
  created_at,
  closed_at
FROM helpscout__conversation
WHERE 
  (LOWER(subject) LIKE '%[TOPIC KEYWORD]%' 
   OR LOWER(preview) LIKE '%[TOPIC KEYWORD]%')
  AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 730 DAY)
ORDER BY created_at DESC
LIMIT 30
```

### Get Thread Details

```sql
SELECT 
  conversation_id,
  type,
  SUBSTR(body, 1, 1000) as body_preview,
  created_at,
  created_by_type
FROM helpscout__conversation_threads
WHERE CAST(conversation_id AS INT64) IN ([ID1], [ID2], [ID3])
ORDER BY conversation_id, created_at
LIMIT 30
```

### Search Ticket Content (Recommended - Pre-Joined View)

```sql
-- Use helpscout__help_scout_tickets for most queries (denormalized view)
SELECT 
  ticket_number,
  ticket_subject,
  ticket_status,
  agent_name,
  mailbox_name,
  ticket_created_at,
  thread_body
FROM helpscout__help_scout_tickets
WHERE LOWER(thread_body) LIKE '%[TOPIC KEYWORD]%'
  OR LOWER(ticket_subject) LIKE '%[TOPIC KEYWORD]%'
ORDER BY ticket_created_at DESC
LIMIT 30
```

**Thread types:** 
- `customer` - from customer
- `message` - support reply
- `note` - internal (often most valuable!)

**Expected Results:** Most common features will have 10-50+ relevant tickets. If 0 results, try alternate keywords before concluding no tickets exist.

---

## BigQuery - Fathom Call Summaries

**Tables:** `fathom__ai_summaries`, `fathom__call_transcripts`, `fathom__sales_meetings_from_fathom_hubspot`

### Search Call Summaries

```sql
SELECT 
  ID as recording_id,
  `Meeting Title` as title,
  `Meeting Start Time` as meeting_date,
  `Fathom User Name` as host,
  `External Domain Names` as customer,
  SUBSTR(`AI Summary Plaintext Formatted`, 1, 800) as summary_preview
FROM fathom__ai_summaries
WHERE 
  (LOWER(`AI Summary Plaintext Formatted`) LIKE '%[TOPIC KEYWORD]%' 
   OR LOWER(`Meeting Title`) LIKE '%[TOPIC KEYWORD]%')
  AND `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 730 DAY)
ORDER BY `Meeting Start Time` DESC
LIMIT 15
```

### Search Call Transcripts

```sql
SELECT 
  ID,
  `Meeting Title`,
  `Fathom User Name`,
  `Meeting Scheduled Start Time`,
  SUBSTR(`Transcript Plaintext`, 1, 500) as transcript_preview
FROM fathom__call_transcripts
WHERE LOWER(`Transcript Plaintext`) LIKE '%[TOPIC KEYWORD]%'
ORDER BY `Meeting Scheduled Start Time` DESC
LIMIT 10
```

**Note:** Column names have spaces - always use backticks!

**Expected Results:** Common features often appear in onboarding/training calls. If 0 results, try alternate keywords.

---

## Notion API

**Use MCP tool:** `notion-fetch` and `notion-update-page`

### Extract Page ID from URL

```
https://www.notion.so/workspace/Page-Title-240231dbcd70806c81f9f432ce26b2f8
→ Page ID: 240231dbcd70806c81f9f432ce26b2f8
```

### Update Page Status

```javascript
// Update to "Live"
await updatePage('PAGE_ID', {
  'Status': { status: { name: 'Live' } }
});
```

### Create Toggle Heading 1

```javascript
{
  object: 'block',
  type: 'heading_1',
  heading_1: {
    rich_text: [{ type: 'text', text: { content: 'Section Title' } }],
    is_toggleable: true
  }
}
```

---

## Craft CMS GraphQL

**Important:** Do NOT introspect full schema - causes timeouts. Use targeted queries.

### Query Article by Slug

```graphql
{
  entries(section: "knowledgeBase", slug: "article-slug", limit: 1) {
    id
    title
    articleSections {
      __typename
      ... on text_Entry { id body }
    }
  }
}
```

### Query Draft by ID

```graphql
{
  entries(draftId: 829) {
    id
    title
    articleSections {
      __typename
      ... on text_Entry { id body }
    }
  }
}
```

### Query Published Article by ID

```graphql
{
  knowledgeBaseEntries(id: ["41981"], status: ["disabled", "live"]) {
    id
    title
    slug
    summary
    articleSections {
      __typename
      ... on text_Entry { id body }
    }
  }
}
```

### Create a Draft

```graphql
mutation {
  createDraft(
    id: 41126,
    name: "KB Merge - Description",
    notes: "Merge notes here"
  )
}
```

### Update Draft Content

**Critical:** After creating a draft, section IDs CHANGE. You MUST:
1. Create the draft first
2. Re-fetch the draft to get NEW section IDs
3. Use those new IDs when updating

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Draft(
    draftId: 829
    articleSections: {
      entries: [
        { text: { id: "41761", body: "<h2>Title</h2><p>Content...</p>" } },
        { text: { id: "41762", body: "<h2>Section 2</h2><p>More content...</p>" } }
      ]
    }
  ) {
    id
    draftId
  }
}
```

### Special Characters to Avoid

Replace these in GraphQL strings:
- Arrow symbols (→) → Use ">" or "->"
- Smart quotes ("") → Use regular quotes
- Em dashes (—) → Use regular dashes (-)
- Ampersands in HTML → Use `&amp;`

### Search for Related Articles

```graphql
{
  entries(section: "knowledgeBase", search: "[TOPIC KEYWORDS]", limit: 10) {
    title
    slug
  }
}
```

### Unpublish an Article

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Entry(
    id: [ARTICLE_ID]
    enabled: false
  ) {
    id
    enabled
  }
}
```

---

## Troubleshooting

### GraphQL Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Expected ':' found Name" | Special characters in string | Replace arrows, smart quotes, em dashes |
| "Something went wrong" | Query structure wrong | Use `entries()` not `entry()`, use inline fragments for Matrix fields |
| Draft sections don't save | Using old section IDs | Re-fetch draft after creation to get new IDs |

### Help Scout Returns 0 Results

1. Try alternate keywords
2. Broaden the search with partial terms
3. Check both mailboxes (Support AND Onboarding)
4. Ensure ALL statuses included
5. Document: "No relevant tickets found after searching: [keywords tried]"

### Fathom Returns No Results

1. Try alternate keywords
2. Check recent onboarding calls
3. Note: Niche/admin-only features may have few calls
4. Document: "No relevant calls found after searching: [keywords tried]"

### Notion "Multiple matches found" Error

- Use longer, more specific snippets
- Include unique text like dates, IDs, or specific phrases
