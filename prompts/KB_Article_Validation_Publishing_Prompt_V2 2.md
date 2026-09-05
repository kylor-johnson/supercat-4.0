# KB Article Validation & Publishing Prompt V2

> **Purpose:** Validate Notion KB draft and publish/merge to Craft CMS with enhancements  
> **Last Updated:** January 15, 2026  
> **Version:** 2.0 - Includes tested GraphQL patterns that actually work

---

## Task: Validate Notion KB Draft → Merge/Publish to Craft CMS

### Source
**Notion Draft URL:** [PASTE NOTION URL HERE]  
**Existing Craft Article URL (if merge):** [PASTE CRAFT URL HERE OR "NEW"]

---

## Workflow (Execute in Order)

### Phase 1: Discovery

**1. Fetch Notion Draft**
```
Use mcp_Notion_notion-fetch with the Notion URL
```
- Get full content and metadata
- Check the "Action Type" property: "New" or "Merge"
- Note the "userDefined:URL" if it links to an existing Craft article

**2. Find Existing Craft Article (if merge)**
```graphql
# Use the TYPED query - NOT generic entries() with inline fragments
{
  knowledgeBaseEntries(slug: ["your-article-slug"]) {
    id
    title
    slug
    enabled
    status
  }
}
```

**3. Get Full Article Content**
```graphql
# This pattern WORKS - use knowledgeBaseEntries, not entries()
{
  knowledgeBaseEntries(id: ["ENTRY_ID"]) {
    id
    title
    shortDescription
    articleSections {
      __typename
      ... on text_Entry {
        id
        body
      }
      ... on tableOfContents_Entry {
        id
      }
      ... on image_Entry {
        id
      }
    }
  }
}
```

---

### Phase 2: Validation

**4. Validate Against Codebase**
Search the codebase to verify:
- Technical accuracy of claims
- Feature availability (check for feature flags)
- Current implementation details
- Admin permissions required

**5. Query Related KB Articles**
```graphql
{
  entries(section: "knowledgeBase", search: "relevant keywords", limit: 10) {
    id
    title
    slug
  }
}
```

---

### Phase 3: Content Update

**6. Create Draft Revision (for existing articles)**
```graphql
mutation {
  createDraft(id: EXISTING_ENTRY_ID)
}
# Returns the draft ID - save this!
```

**7. Get Draft Content**
```graphql
{
  knowledgeBaseEntries(draftId: DRAFT_ID) {
    id
    title
    draftId
    articleSections {
      __typename
      ... on text_Entry { id body }
      ... on tableOfContents_Entry { id }
    }
  }
}
```

**8. Update Draft Content**

⚠️ **CRITICAL: Payload Size Limits**
- Do NOT send all content in one mutation
- Keep each text body under ~2000 characters
- If content is longer, simplify or split across multiple sections

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Draft(
    draftId: DRAFT_ID,
    title: "Article Title",
    articleSections: {
      entries: [
        { tableOfContents: { id: "EXISTING_TOC_ID" } },
        { text: { id: "EXISTING_TEXT_ID", body: "<h2>Section</h2><p>Content here...</p>" } },
        { text: { id: "ANOTHER_TEXT_ID", body: "<h2>Another Section</h2><p>More content...</p>" } }
      ]
    }
  ) {
    id
    title
  }
}
```

**Input Structure for articleSections:**
```
articleSections: {
  sortOrder: [...],  // Optional - array of IDs for ordering
  entries: [
    { tableOfContents: { id: "..." } },
    { text: { id: "...", body: "..." } },
    { image: { id: "..." } },
    { video: { id: "..." } },
    { code: { id: "..." } }
  ]
}
```

**Each entry type accepts:**
- `tableOfContents`: `{ id }`
- `text`: `{ id, body }` (body is HTML string)
- `image`: `{ id }` (images managed separately)
- `video`: `{ id }`
- `code`: `{ id }`

⚠️ **LIMITATION: Cannot add NEW matrix entries via GraphQL**
- You can only UPDATE existing entries (with their IDs)
- New sections (like Troubleshooting) must be added manually in Craft admin

---

### Phase 4: Finalize

**9. Verify Draft Updates**
```graphql
{
  knowledgeBaseEntries(draftId: DRAFT_ID) {
    articleSections {
      __typename
      ... on text_Entry { id body }
    }
  }
}
```

**10. Update Notion Status**
```
Use mcp_Notion_notion-update-page
Valid statuses: "Not started", "In progress", "Archived (Consolidated)", "Ready for Craft (Kyla Check)", "Live"
```

**11. Publishing**
- GraphQL `publishDraft` mutation typically fails due to API permissions
- **Manual publish required:** Provide admin URL for review and publish
- Admin URL format: `https://supercatsolutions.com/admin/entries/knowledgeBase/ENTRY_ID?draftId=DRAFT_ID`

---

## CRITICAL: CraftCMS GraphQL Rules

### ❌ NEVER DO THESE (They Fail)

```graphql
# 1. NEVER introspect full schema - causes timeout
{ __schema { types { name fields { name } } } }

# 2. NEVER use generic entries() with inline fragments for KB articles
{ entry(id: "41126") { 
  ... on knowledgeBase_knowledgeBase_Entry { shortDescription } 
} }

# 3. NEVER send large payloads (>2KB body content per section)
mutation { save_...(articleSections: { entries: [{ text: { body: "...huge content..." }}]}) }

# 4. NEVER try to add NEW matrix entries (no id field)
{ text: { body: "new section" } }  # This gets IGNORED
```

**IMAGES - NEVER:**
- Generate or create images yourself
- Add placeholder/dummy image URLs
- Assume images exist without verifying source

### ✅ ALWAYS DO THESE (They Work)

```graphql
# 1. Test connection first
{ ping }

# 2. Use TYPED queries for KB articles
{ knowledgeBaseEntries(id: ["41126"]) { title articleSections { __typename } } }

# 3. Introspect ONE type at a time
{ __type(name: "articleSections_MatrixInput") { inputFields { name type { name } } } }

# 4. List mutations
{ __type(name: "Mutation") { fields { name } } }

# 5. Discover input structure for matrix fields
{ __type(name: "articleSections_MatrixEntryContainerInput") { inputFields { name } } }
{ __type(name: "articleSections_text_MatrixEntryInput") { inputFields { name } } }

# 6. Create drafts before editing live articles
mutation { createDraft(id: ENTRY_ID) }

# 7. Update drafts incrementally with reasonable payload sizes
mutation { save_knowledgeBase_knowledgeBase_Draft(draftId: X, title: "...", articleSections: {...}) }
```

---

## Quick Reference

| What | Value/Pattern |
|------|---------------|
| **Test Connection** | `{ ping }` |
| **Get KB Article** | `knowledgeBaseEntries(id: ["ID"])` or `knowledgeBaseEntries(slug: ["slug"])` |
| **Get Draft** | `knowledgeBaseEntries(draftId: DRAFT_ID)` |
| **Create Draft** | `mutation { createDraft(id: ENTRY_ID) }` |
| **Update Draft** | `save_knowledgeBase_knowledgeBase_Draft(draftId: X, ...)` |
| **Notion Statuses** | "Not started", "In progress", "Archived (Consolidated)", "Ready for Craft (Kyla Check)", "Live" |
| **Craft Author ID** | 39645 (Kyla Bosch) |
| **Save Location** | `/chat-history/` |

---

## Categories Reference

```graphql
{
  categories(group: "knowledgeBase", limit: 20) {
    id
    title
    slug
  }
}
```

Common categories:
- 1380: Products
- 1382: Users  
- 1406: Pricing
- 1404: Troubleshooting
- 1407: Setup

---

## Troubleshooting

### "Something went wrong when processing the GraphQL query"
- **Cause:** Usually payload too large or malformed content
- **Fix:** Reduce content size, remove special characters (→, quotes), use variables for long strings

### Inline fragments returning null
- **Cause:** Using generic `entries()` or `entry()` queries
- **Fix:** Use typed queries like `knowledgeBaseEntries()`

### Draft changes not appearing on live site
- **Cause:** Draft not published
- **Fix:** Publish manually via Craft admin - GraphQL can't publish

### New sections not being created
- **Cause:** GraphQL can't add new matrix entries
- **Fix:** Add new sections manually in Craft admin

---

---

## Image Handling - CRITICAL

### ❌ NEVER DO
- Generate or create images
- Assume images exist
- Add placeholder image URLs

### ✅ ALWAYS DO
1. **Identify** what images would help the article (max 3 per article)
2. **Search Help Scout tickets** for relevant screenshots from real support cases
3. **Search existing KB articles** for reusable images
4. **Document** image placeholders with:
   - Section where image belongs
   - Description of what's needed
   - Source ticket # or KB article # with matching image
   - Actual image URL from source

### Image Mapping Format
```markdown
### Image 1: [Descriptive Name]

| Source | Asset |
|--------|-------|
| **Help Scout Ticket #XXXXX** | Description of what the image shows |
| **Image URL** | https://d33v4339jhl8k0.cloudfront.net/inline/... |
```

### Image Sources (in order of preference)
1. **Help Scout tickets** - Real screenshots from actual support cases
   - CloudFront URLs: `https://d33v4339jhl8k0.cloudfront.net/inline/40956/...`
2. **Existing KB articles** - Already approved images
   - SuperCat URLs: `https://supercatsolutions.com/assets/images/screenshots/...`
3. **Manual capture needed** - Document exact Admin Console path

### Reference
See `/kb-articles/IMAGE_MAPPING_FOR_DRAFT_ARTICLES.md` for examples

---

## Expected Output

1. ✅ Craft CMS draft with validated/enhanced content
2. ✅ Codebase validation findings documented
3. ✅ **Image mapping document** with sources (max 3 images)
4. ✅ Notion card updated to "Ready for Craft (Kyla Check)"
5. ✅ Admin URL provided for manual review/publish
6. ✅ Validation report saved to `/chat-history/`
7. ✅ Chat history saved to `/chat-history/`

---

## Sample Complete Workflow

```javascript
// 1. Fetch Notion draft
mcp_Notion_notion-fetch({ id: "NOTION_URL" })

// 2. Find existing Craft article
{ knowledgeBaseEntries(slug: ["article-slug"]) { id title } }

// 3. Get full content
{ knowledgeBaseEntries(id: ["ENTRY_ID"]) { articleSections { ... } } }

// 4. Validate against codebase
codebase_search("how does feature X work")

// 5. Create draft
mutation { createDraft(id: ENTRY_ID) }

// 6. Update draft sections
mutation { save_knowledgeBase_knowledgeBase_Draft(draftId: X, articleSections: {...}) }

// 7. Verify updates
{ knowledgeBaseEntries(draftId: X) { articleSections { ... } } }

// 8. Update Notion
mcp_Notion_notion-update-page({ page_id: "...", properties: { Status: "Ready for Craft (Kyla Check)" }})

// 9. Provide admin URL for manual publish
// https://supercatsolutions.com/admin/entries/knowledgeBase/ENTRY_ID?draftId=DRAFT_ID
```

