# KB Merge Article Validation & Update Prompt

**Purpose:** Process Notion KB backlog articles tagged as `Action Type = Merge` by validating content, enhancing with additional context, and updating the existing Craft CMS article.

---

## Prompt

```
You are helping me process a KB backlog article that needs to be MERGED into an existing Craft CMS Knowledge Base article.

## Article Information

**Notion Draft Article:** [PASTE NOTION URL]
**Target Craft CMS Article to Update:** [PASTE CRAFT KB URL FROM THE URL FIELD]

---

## Your Task

### Step 1: Review the Notion Draft
1. Fetch the Notion page content using the Notion MCP integration
2. Identify the key topics, features, and troubleshooting steps covered
3. Note any gaps or areas that seem incomplete

### Step 2: Validate & Enhance with Context

**2A. Query Help Scout Tickets (BigQuery)**
Search for related tickets to validate accuracy and find additional context:

```sql
-- Query Help Scout tickets from both inboxes
SELECT 
  conversation_id,
  subject,
  status,
  mailbox_name,
  created_at,
  closed_at,
  tags,
  customer_email
FROM `helpscout.conversations`
WHERE 
  (LOWER(subject) LIKE '%[TOPIC KEYWORD]%' 
   OR LOWER(tags) LIKE '%[TOPIC KEYWORD]%')
  AND created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 YEAR)
  AND mailbox_name IN ('Support', 'Onboarding')
ORDER BY created_at DESC
LIMIT 50
```

For promising tickets, fetch thread details to understand:
- Common user questions/confusion points
- Solutions provided by support team
- Edge cases or exceptions mentioned
- Any corrections or clarifications made

**2B. Validate with Codebase**
Search the codebase to verify:
- Feature behavior matches documentation
- Settings/configuration options are accurate
- Any technical details are correct
- No outdated information

**2C. Query Fathom Call Summaries**
Use the Fathom API integration to find relevant customer calls:
- Search call summaries from the last 2 years
- Look for discussions about this topic
- Note any customer feedback, confusion, or feature requests
- Identify real-world use cases mentioned

### Step 3: Edit the Notion Draft

Based on your validation and research:
1. **Correct** any inaccuracies found
2. **Add** missing context from Help Scout tickets
3. **Enhance** with real-world examples from Fathom calls
4. **Update** any outdated information based on codebase
5. **Improve** clarity based on common support questions

Update the Notion page content directly using the Notion MCP integration.

### Step 4: Image Recommendations

Identify up to **2 areas** (or fewer if not needed) where images would help:
1. Complex UI workflows
2. Settings/configuration screens
3. Before/after comparisons
4. Error messages or status indicators

**4A. Search Help Scout for Existing Images**
Query BigQuery for tickets with attachments:

```sql
SELECT 
  conversation_id,
  subject,
  attachments,
  created_at
FROM `helpscout.conversations`
WHERE 
  (LOWER(subject) LIKE '%[TOPIC]%' OR LOWER(tags) LIKE '%[TOPIC]%')
  AND attachments IS NOT NULL
  AND created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 YEAR)
ORDER BY created_at DESC
LIMIT 20
```

Look for reusable screenshots in ticket attachments.

**4B. If No Existing Images**
Based on the content and codebase, suggest:
- Exact screen/page to screenshot
- What state/data should be visible
- What to highlight or annotate
- Any specific user role or permissions needed

**Save image suggestions to:**
`/kb-articles/IMAGE_SUGGESTIONS_[ARTICLE_NAME].md`

### Step 5: Update Craft CMS

1. Fetch the existing Craft CMS article using the Craft CMS GraphQL integration
2. Identify where the new content should be inserted (new section, enhancement to existing section, etc.)
3. Merge the validated Notion content into the existing article structure
4. Use the Craft CMS mutation to update the article and **save as DRAFT** (do not publish)

### Step 6: Update Notion Status

Update the Notion page properties:
- Set `Status` to "Ready for Craft (Kyla Check)"
- Ensure `URL` field contains the Craft CMS article URL

---

## Output Format

Provide a summary of:

### Validation Results
- [ ] Help Scout tickets reviewed: [count]
- [ ] Key insights found: [list]
- [ ] Codebase validation: [pass/issues found]
- [ ] Fathom calls reviewed: [count]
- [ ] Customer feedback themes: [list]

### Changes Made to Notion Draft
- [List of edits/additions made]

### Image Recommendations
- **Image 1:** [Description, location in article, source/screenshot suggestion]
- **Image 2:** [Description, location in article, source/screenshot suggestion]
- (Or: No images needed for this content)

### Craft CMS Update
- Article updated: [URL]
- Status: Saved as Draft
- New sections added: [list]
- Existing sections enhanced: [list]

### Notion Status
- Updated to: Ready for Craft (Kyla Check)

---

## Important Notes

- Do NOT publish the Craft CMS article - save as draft only
- Do NOT create any local files except the image suggestions document
- All edits should be made directly in Notion and Craft CMS via their integrations
- If validation reveals significant issues with the draft, flag them before proceeding
- Preserve the existing article structure - add/enhance, don't restructure
```

---

## Integration Reference

### BigQuery (Help Scout)
- Tables: `helpscout.conversations`, `helpscout.threads`
- Inboxes: Support, Onboarding
- Timeframe: Last 2 years

### Fathom API
- Endpoint: Call summaries
- Timeframe: Last 2 years
- Search: Topic keywords in summary notes

### Notion MCP
- Fetch: `notion-fetch` with page ID
- Update: `notion-update-page` for content and properties

### Craft CMS GraphQL
- Query: `entries(section: "knowledgeBase")` 
- Mutation: Update entry, save as draft

---

## Usage

1. Copy the prompt above
2. Replace `[PASTE NOTION URL]` with the Notion draft article URL
3. Replace `[PASTE CRAFT KB URL FROM THE URL FIELD]` with the target Craft article URL
4. Replace `[TOPIC KEYWORD]` and `[TOPIC]` with relevant search terms
5. Run in Cursor

---

## Batch Processing

To process multiple Merge articles:

1. First, get the list of Merge articles from Notion:
```
Use the Notion MCP to search the KB Backlog database for all articles where Action Type = "Merge" and Status = "In progress"
```

2. Process each article one at a time using the prompt above

3. Track progress in Notion by checking Status updates
