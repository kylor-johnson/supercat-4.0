# Knowledge Base Consolidation Implementation Playbook

**Version:** 1.0  
**Created:** January 15, 2026  
**Purpose:** Operational guide for consolidating Notion KB backlog articles into Craft CMS

---

## Overview

This playbook outlines how to operationalize the KB consolidation analysis using your existing integrations:

| Integration | Purpose in Workflow |
|-------------|---------------------|
| **Notion MCP** | Read/combine backlog draft articles |
| **BigQuery** | Query Help Scout tickets for validation data |
| **SuperCat CS Tools MCP** | Access org data for accuracy checks |
| **Craft CMS GraphQL** | Push finalized drafts as KB articles |

---

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KB CONSOLIDATION WORKFLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │   PHASE 1    │    │   PHASE 2    │    │   PHASE 3    │    │  PHASE 4   │ │
│  │   Triage &   │───▶│   Combine &  │───▶│   Validate   │───▶│   Publish  │ │
│  │  Prioritize  │    │    Draft     │    │   & Review   │    │  to Craft  │ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └────────────┘ │
│        │                    │                   │                   │        │
│        ▼                    ▼                   ▼                   ▼        │
│   Notion Board         Notion MCP          BigQuery +          Craft CMS    │
│   Status Update        Fetch/Combine       Help Scout          GraphQL      │
│                                            Ticket Data                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Triage & Prioritization

### 1.1 Update Notion Board Status

Before starting any article work, update the Notion backlog board to reflect consolidation decisions:

**Status Mapping:**
| Decision Type | Set Notion Status To | Notes |
|---------------|---------------------|-------|
| Net-New Standalone | `In progress` | Ready for drafting |
| Merge into Existing | `In progress` | Note target article in URL field |
| Consolidate Together | `In progress` | Note consolidation group in Notes |
| Already Live | `Live` | Link existing Craft article |
| Low Priority/Defer | `On hold` | Document reason |

### 1.2 Prioritization Criteria

Process articles in this order:

1. **Priority 1 articles** marked in Notion
2. **Frequently referenced in Help Scout** (validate with BigQuery)
3. **Category groupings** (complete one topic area before moving on)
4. **Dependencies** (e.g., create "Image Guide" before linking to it)

### 1.3 Cursor Prompt for Triage Check

```
Review the Notion KB backlog article at [URL] and determine:
1. Current status and priority
2. Related existing Craft CMS articles
3. Help Scout ticket volume for this topic (use BigQuery)
4. Recommended consolidation action
```

---

## Phase 2: Combine & Draft

### 2A: Net-New Standalone Articles

**When to use:** Article covers unique topic with no KB overlap.

**Process:**

1. **Fetch the Notion draft:**
   ```
   Fetch the Notion page at [NOTION_URL] and review the current draft content
   ```

2. **Validate against Help Scout tickets:**
   ```
   Query BigQuery for Help Scout tickets related to "[TOPIC]" from the past 6 months.
   Identify common questions, edge cases, and missing information.
   ```

3. **Enhance the draft:**
   - Add missing scenarios from ticket data
   - Ensure troubleshooting steps are complete
   - Add "Related Articles" section (link to existing KB)
   - Remove internal notes/TODOs

4. **Save locally before pushing:**
   - Save to `/kb-articles/[article-slug].md`
   - This creates a backup and allows review

5. **Update Notion status:** `Ready for Craft (Kyla Check)`

---

### 2B: Merge into Existing KB Articles

**When to use:** Backlog article enhances an existing Craft CMS article.

**Process:**

1. **Fetch BOTH sources:**
   ```
   1. Fetch the Notion backlog draft at [NOTION_URL]
   2. Query the existing Craft CMS article with slug "[SLUG]"
   ```

2. **Identify merge points:**
   - What sections in the backlog are NEW vs duplicative?
   - What existing content should be preserved?
   - What order makes sense for the combined content?

3. **Create merged draft:**
   - Start with existing Craft article structure
   - Weave in new content from Notion at appropriate points
   - Deduplicate any overlapping content
   - Update "Last Updated" date

4. **Validate merged content:**
   ```
   Query BigQuery for Help Scout tickets about "[TOPIC]" to ensure 
   the merged article addresses common questions.
   ```

5. **Push as UPDATE to Craft CMS** (not new article)

6. **Update Notion:**
   - Set status to `Live`
   - Add Craft URL to `Live Link` field

---

### 2C: Consolidate Multiple Backlog Articles Together

**When to use:** Multiple backlog articles cover related topics and should become ONE comprehensive article.

**Consolidation Groups:**

| Group ID | Articles to Combine | Target Article Title |
|----------|--------------------|-----------------------|
| **IMG** | Missing/Orphan Images + Image Errors + CMYK/sRGB | "Complete Guide to Image Management in SuperCat" |
| **SML** | Suppress Products + Sorting Logic + Region Visibility | "Smart Lists: Complete Guide to Product Visibility" |
| **HID** | Hide Discontinued + Trade Names Toggle + Hideable Products | "Product Visibility & Hiding Options" |

**Process:**

1. **Fetch ALL articles in the group:**
   ```
   Fetch these Notion pages and combine into a single comprehensive draft:
   - [URL1]
   - [URL2]
   - [URL3]
   ```

2. **Create unified outline:**
   - Identify the logical flow across all source articles
   - Create section headings that cover all topics
   - Map source content to new sections

3. **Merge content intelligently:**
   ```
   Combine the fetched articles into a single comprehensive article with:
   - One "Overview" section
   - Logical topic progression
   - No duplicate content
   - Unified troubleshooting section
   - Single "Best Practices" section
   ```

4. **Validate comprehensive coverage:**
   ```
   Query BigQuery for Help Scout tickets about [TOPIC AREA] 
   to ensure the consolidated article addresses all common scenarios.
   ```

5. **Push as NEW article to Craft CMS**

6. **Update ALL source Notion pages:**
   - Set status to `Live`
   - Add same Craft URL to all
   - Note in each: "Consolidated into: [Article Title]"

---

## Phase 3: Validate & Review

### 3.1 BigQuery Validation Queries

**Find related Help Scout tickets:**
```sql
SELECT 
  id,
  subject,
  created_at,
  preview
FROM `help_scout.conversations`
WHERE 
  LOWER(subject) LIKE '%image%' 
  OR LOWER(preview) LIKE '%missing image%'
  AND created_at > DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH)
ORDER BY created_at DESC
LIMIT 50
```

**Find ticket volume by topic:**
```sql
SELECT 
  DATE_TRUNC(created_at, MONTH) as month,
  COUNT(*) as ticket_count
FROM `help_scout.conversations`
WHERE LOWER(subject) LIKE '%[TOPIC]%'
GROUP BY 1
ORDER BY 1 DESC
```

### 3.2 Validation Checklist

Before pushing to Craft CMS, verify:

- [ ] **Accuracy:** Technical steps are correct (test against real org if needed)
- [ ] **Completeness:** All scenarios from Help Scout tickets are addressed
- [ ] **Clarity:** Non-technical users can follow instructions
- [ ] **Links:** All referenced articles exist in KB
- [ ] **Images:** Screenshot references are noted (for Kyla to add)
- [ ] **Formatting:** Headers, tables, callouts are properly structured
- [ ] **Metadata:** Short description, category tags are defined

### 3.3 Cursor Validation Prompt

```
Validate this KB article draft against Help Scout ticket data:

1. Query BigQuery for tickets about "[TOPIC]" from the past 6 months
2. Identify any common questions NOT addressed in the draft
3. Check for any outdated information based on recent tickets
4. Recommend specific additions or corrections

Article draft:
[PASTE DRAFT OR REFERENCE FILE]
```

---

## Phase 4: Publish to Craft CMS

### 4.1 Craft CMS Article Structure

When pushing to Craft, include these fields:

```graphql
mutation CreateKnowledgeBaseEntry {
  save_knowledgeBase_knowledgeBase_Entry(
    title: "Article Title Here"
    slug: "article-title-here"
    shortDescription: "One-line summary for search results"
    articleSections: [
      {
        # Section content as nested entries
      }
    ]
  ) {
    id
    url
  }
}
```

### 4.2 Push as DRAFT

Always push articles as **drafts** first:

```
Push this article to Craft CMS as a DRAFT (not published):
- Title: [TITLE]
- Slug: [SLUG]
- Short Description: [DESCRIPTION]
- Content: [CONTENT]

This allows Kyla/Brent/Chuck to review before publishing.
```

### 4.3 Post-Publish Checklist

After Craft CMS draft is created:

- [ ] Update Notion status to `Ready for Craft (Kyla Check)`
- [ ] Add Craft admin URL to Notion `URL` field
- [ ] Notify reviewer (Slack/Teams message)
- [ ] Track in weekly KB update log

---

## Consolidation Tracking Template

Use this format to track progress:

```markdown
## Consolidation Session: [DATE]

### Articles Processed:
| Notion Article | Action | Target | Status |
|----------------|--------|--------|--------|
| [Article Name] | Net-New | N/A | ✅ Pushed to Craft |
| [Article Name] | Merge | Article #XXXX | ✅ Merged |
| [Article Name] | Consolidate | IMG Group | ⏳ In Progress |

### Validation Notes:
- Queried X Help Scout tickets for [topic]
- Found Y edge cases to add
- [Other notes]

### Next Steps:
- [ ] Item 1
- [ ] Item 2
```

---

## Quick Reference: Cursor Prompts by Phase

### Phase 1 - Triage
```
Review the Notion KB backlog database and identify:
1. Articles marked Priority 1 that are not yet Live
2. Any articles that should be merged with existing KB content
3. Groups of related articles that could be consolidated
```

### Phase 2A - Net-New Draft
```
Fetch the Notion article "[TITLE]" and:
1. Review the current draft content
2. Query Help Scout tickets for this topic
3. Enhance the draft with missing information
4. Format for Craft CMS publishing
```

### Phase 2B - Merge with Existing
```
I need to merge Notion article "[TITLE]" into existing Craft KB article "[SLUG]":
1. Fetch both articles
2. Identify new content to add
3. Create merged draft preserving existing structure
4. Highlight what's new vs existing
```

### Phase 2C - Consolidate Multiple
```
Consolidate these Notion articles into one comprehensive article:
- [URL1]: [Title1]
- [URL2]: [Title2]
- [URL3]: [Title3]

Create unified draft with:
- Single overview
- Logical section flow
- No duplicate content
- Combined troubleshooting section
```

### Phase 3 - Validate
```
Validate this KB article against Help Scout data:
1. Query BigQuery for related tickets (past 6 months)
2. Check if common questions are answered
3. Identify any gaps or outdated info
4. Provide specific enhancement recommendations
```

### Phase 4 - Publish
```
Push this article to Craft CMS as a draft:
- Title: [TITLE]
- Slug: [SLUG]
- Short Description: [DESCRIPTION]

After pushing, provide:
1. The Craft CMS admin URL
2. Next steps for reviewer notification
```

---

## Appendix: Article Consolidation Map

### Net-New Standalone (10 articles)
1. Shared Orders in SuperCat eCat
2. How Order Editing Works: Replacing vs. Updating Orders
3. Managing Rep-Created Customers (Local Customers)
4. Sales quota functionality
5. How to Manage FTP Access: Password Resets & Folder Setup
6. Account Setup & Merge Policy
7. Portal User Login Notifications: How "Primary Rep" Works
8. OrderXpert
9. Backlog Total Logic
10. Known Limitation: Inventory Custom Fields

### Merge into Existing (16 articles)
| Backlog | → Target Craft Article |
|---------|------------------------|
| Riser Pricing Troubleshooting | → Grade Jump Riser Pricing (#2575) |
| Promotion Pricing (simple vs rules) | → Special Promotion Pricing (#97) |
| Pricing Architecture Overview | → Catalog Pricing (#2531) |
| Price Levels: eCat vs iPad | → Comparison Price Level (#1778) |
| Emailing Product Info | → Emailing Product Information (#2383) |
| Configurable Options | → Import Matrix Options (#700) |
| Nested Kits | → Kitting (#846) |
| Option mapping MVP | → Option Mapping (#41126) |
| eCat Online Category Filters | → eCat Online Overview (#942) |
| Enable Ordering Customer Users | → eCat Online B2B shopping cart (#986) |
| Display Inventory | → Display Inventory Setup (#1231) |
| Collection Name Reports | → Settings (#1386) |
| QR Code Scanning | → Showroom Tips: Scanning (#3079) |
| Share Customers Markets | → Get-Ready Checklist (#39651) |
| Commitments & Interests | → Commitments (#1598) |
| UPC Codes Duplicates | → Import Product Supplement (#720) |

### Consolidation Groups (11 → 4 articles)
| Group | Source Articles | Target Title |
|-------|-----------------|--------------|
| **IMG** | Missing/Orphan + Errors + CMYK | Complete Guide to Image Management |
| **SML** | Suppress + Sorting + Region | Smart Lists: Product Visibility Guide |
| **HID** | Discontinued + Trade Names + Hideable | Product Visibility & Hiding Options |
| **EOL** | Saving Cart + Projects | Working with Carts & Projects in eCat Online |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-15 | Initial playbook created |
