# KB Integration References

**Purpose:** Consolidated reference for all integrations used in the KB creation workflow. Read this file once at the start of a KB processing session.

---

## BigQuery - Help Scout Data

**Dataset:** `hevo_dataset_supercat_data_pipeline_Slhk`  
**Tables:** `conversation`, `conversation_threads`

### Find Relevant Conversations

```sql
SELECT 
  id,
  subject,
  status,
  mailbox_id,
  created_at,
  closed_at
FROM `hevo_dataset_supercat_data_pipeline_Slhk.conversation`
WHERE 
  (LOWER(subject) LIKE '%[TOPIC KEYWORD]%' 
   OR LOWER(subject) LIKE '%[ALTERNATE KEYWORD]%')
  AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 730 DAY)
ORDER BY created_at DESC
LIMIT 30
```

### Get Thread Details

```sql
SELECT 
  conversation_id,
  SUBSTR(body, 1, 1000) as body_preview,
  created_at,
  type
FROM `hevo_dataset_supercat_data_pipeline_Slhk.conversation_threads`
WHERE CAST(conversation_id AS INT64) IN ([ID1], [ID2], [ID3])
ORDER BY conversation_id, created_at
LIMIT 30
```

**Thread types:** 
- `customer` - from customer
- `message` - support reply
- `note` - internal (often most valuable!)

**Expected Results:** Most common features will have 10-50+ relevant tickets. If 0 results, try alternate keywords before concluding no tickets exist.

---

## BigQuery - Fathom Call Summaries

**Dataset:** `Fathom`  
**Table:** `ai_summaries_parsed`

```sql
SELECT 
  ID as recording_id,
  `Meeting Title` as title,
  `Meeting Start Time` as meeting_date,
  SUBSTR(`Ai Summary Plaintext Formatted`, 1, 800) as summary_preview
FROM `Fathom.ai_summaries_parsed`
WHERE 
  (LOWER(`Ai Summary Plaintext Formatted`) LIKE '%[TOPIC KEYWORD]%' 
   OR LOWER(`Meeting Title`) LIKE '%[TOPIC KEYWORD]%')
  AND `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 730 DAY)
ORDER BY `Meeting Start Time` DESC
LIMIT 15
```

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
