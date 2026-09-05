# KB Article Validation & Publishing Prompt

> **Purpose:** Validate Notion KB draft and publish to Craft CMS with enhancements  
> **Last Updated:** January 15, 2026

---

## Task: Validate Notion KB Draft → Publish to Craft CMS

### Source
**Notion Draft URL:** [PASTE NOTION URL HERE]

### Workflow (Execute in Order)

1. **Fetch Notion Draft**
   - Get full content and metadata
   
2. **Query Help Scout Tickets (BigQuery)**
   - Dataset: `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk`
   - Table: `help_scout_tickets`
   - Query BOTH inboxes: `onboarding` AND `support`
   - Include ALL statuses: open AND closed
   - Get thread details for relevant tickets
   - Look for: customer pain points, edge cases, terminology used, common mistakes

3. **Review Existing Craft CMS KB Articles**
   - Search for related articles
   - Check for contradictions
   - Find linking opportunities
   - Identify reusable images/screenshots

4. **Validate Against Codebase**
   - Verify technical accuracy
   - Confirm feature availability
   - Check current implementation

5. **Enhance Article Content**
   Based on validation findings, ADD:
   - Missing steps or clarifications
   - Troubleshooting section (from Help Scout tickets)
   - Common mistakes section (from Help Scout tickets)
   - Comparison tables where helpful
   - Related article links

6. **Add Screenshot Placeholders**
   For each placeholder, provide:
   - Section where it belongs
   - Description of what to capture
   - EXACT location to capture it (Admin Console path, eCat screen, etc.)
   - OR existing KB article with reusable image
   - OR Help Scout ticket with relevant screenshot

7. **Publish to Craft CMS**
   - Create as DRAFT (disabled status)
   - Author: Kyla Bosch (39645)
   - Include all sections with proper HTML formatting

8. **Update Notion**
   - Set status to "Ready for Craft"

9. **Save Documentation**
   - Save validation report to: `/Agent Chat History/`
   - Save chat history to: `/Agent Chat History/`

---

### CRITICAL: Craft CMS GraphQL Rules

When working with CraftCMS GraphQL, **NEVER** introspect the full schema - it causes timeouts and context overflow.

❌ **NEVER DO THIS** (causes timeouts):
```graphql
{ __schema { types { name fields { name } } } }
```

✅ **ALWAYS USE TARGETED INTROSPECTION:**

**1. Test connection:**
```graphql
{ ping }
```

**2. Introspect ONE type at a time:**
```graphql
{ __type(name: "knowledgeBase_knowledgeBase_Entry") { 
  fields { name type { name kind } } 
} }
```

**3. List mutation names only:**
```graphql
{ __type(name: "Mutation") { 
  fields { name } 
} }
```

**4. Sample real entries to discover structure:**
```graphql
{ entries(section: "knowledgeBase", limit: 1) { 
  id title 
  ... on knowledgeBase_knowledgeBase_Entry { 
    articleSections { 
      __typename 
      ... on text_Entry { id body } 
    } 
  } 
} }
```

**Key Principles:**
- Query ONE type at a time using `__type(name: "TypeName")`
- Never request all fields from all types
- Use inline fragments for union types
- Request only fields you actually need

---

## Quick Reference

| What | Value |
|------|-------|
| BigQuery Dataset | `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk` |
| Help Scout Table | `help_scout_tickets` |
| Notion Valid Statuses | "Not started", "In progress", "Archived (Consolidated)", "Ready for Craft (Kyla Check)", "Live" |
| Craft Author ID | 39645 (Kyla Bosch) |
| Save Location | `/Agent Chat History/` |

---

## Expected Output

1. ✅ Craft CMS draft article with validated/enhanced content
2. ✅ Screenshot placeholders with capture locations
3. ✅ Notion card updated to "Ready for Craft"
4. ✅ Validation report saved
5. ✅ Summary of changes made
