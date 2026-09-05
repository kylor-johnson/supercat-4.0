# KB Merge Article Validation & Update Prompt (Revised Article Structure)

**Purpose:** Process Notion KB backlog articles tagged as `Action Type = Merge` by validating content, enhancing with additional context, and updating the existing Craft CMS article. **MERGE means ENHANCE, not REPLACE.**

**This version includes:** Revised article structure guidelines for better readability and self-service support.

---

## Article Structure & Tone Guidelines

### Target Audiences

KB articles serve **two audiences**:

| Audience | Need | How They Use Articles |
|----------|------|----------------------|
| **Self-service users** | Scan quickly, find answer, follow steps | Search KB directly |
| **Kyla sending links** | Jump to specific section, resolve in 1-2 touches | Links to specific sections in support replies |

### Required Article Structure

All merged articles should follow this structure:

```
## Summary (2-3 sentences max)
What is this feature? When would I use it?

## Quick Start (for "just tell me what to click" users)
5-7 numbered steps to get started immediately
No theory, just actions

## How It Works (for "I want to understand" users)
Conceptual explanation with examples
Key rules and limitations
Visual diagram if helpful

## Step-by-Step Setup (detailed version)
Full walkthrough with context
Tips and best practices

## Before You Begin / Prerequisites
Link to related articles
Keep brief - don't overwhelm

## Troubleshooting
Common issues, FAQs, and mistakes - all combined in one section
End with "Need more help? Contact Support"
```

**Note:** Do NOT include separate sections for FAQs, Common Mistakes, Need Help, or Related Articles. Combine all troubleshooting content into one "Troubleshooting" section. Craft auto-generates Related Articles.

### Writing Principles

| Principle | Do This | Not This |
|-----------|---------|----------|
| **Lead with action** | "Go to Admin Console > Products" | "In many products, particularly those with customizable attributes..." |
| **Plain language** | "Click Save" | "Select Update mapping to persist your changes" |
| **Scannable headings** | "Step 1: Access Option Mappings" | "Accessing the Feature" |
| **Two paths** | Quick Start + Detailed sections | Single wall of text |
| **Specific navigation** | "Admin Console > Products > Option Mappings" | "Navigate to the option mappings area" |

### Formatting Rules

**📄 Follow the complete formatting guidelines in `2.0_Craft_CMS_Formatting_Guidelines.md`**

Key points:
- Navigation paths: **Admin Console > Products > Option Mappings**
- UI elements: Bold only clickable items (**Save**, **Actions**)
- Field names: Use single quotes with exact casing ('MappedBillToCode')
- Notes/Tips/Warnings: Always use blockquotes with 💡 or ⚠️ prefixes
- Do NOT include a Related Articles section (Craft auto-generates it)

### Complexity Guidelines

- **Summary:** 8th grade reading level - anyone can understand
- **Quick Start:** Action-oriented, minimal explanation
- **How It Works:** Can be more technical, but define jargon
- **Troubleshooting:** Direct answers, no fluff

---

## Prompt

```
You are helping me process a KB backlog article that needs to be MERGED into an existing Craft CMS Knowledge Base article.

**CRITICAL RULE:** MERGE means ENHANCE, not REPLACE. The existing Craft article is the foundation. Notion content ADDS to it. The final article should ALWAYS be >= the length of the original.

**FORMATTING:** Before generating any HTML content, READ the file `prompts/2.0_Craft_CMS_Formatting_Guidelines.md` and apply all rules (bold usage, field names in single quotes, blockquote callouts, step structure, article type templates, image placeholder format, etc.).

**ARTICLE STRUCTURE:** Follow the revised article structure guidelines. Every merged article should have:
1. Summary (2-3 sentences)
2. Quick Start (5-7 action steps)
3. How It Works (conceptual explanation)
4. Step-by-Step Setup (detailed walkthrough)
5. Prerequisites (brief, at end)
6. Troubleshooting (combines FAQs, common mistakes, need help)

## Article Information

**Notion Draft Article:** [PASTE NOTION URL]
**Target Craft CMS Article to Update:** [PASTE CRAFT KB URL FROM THE URL FIELD]

---

## Your Task

### Step 1: Review the Notion Draft
1. Fetch the Notion page content using the Notion MCP integration

2. **🛑 CHECK STATUS FIRST - Archived (Consolidated) Pages:**
   - If the page `Status` = **"Archived (Consolidated)"** → **STOP IMMEDIATELY**
   - This article's content has been rolled into a parent article
   - Look for the callout banner: `📦 **CONSOLIDATED:** This article's content has been incorporated into...`
   - The parent article link in that banner is the one to process instead
   - **Output:** "⏭️ SKIPPED: This article is archived (consolidated into [Parent Article Name]). Process the parent instead."
   - Do NOT continue with the merge workflow for archived pages

3. **Check for Prepared Draft:** If the page has a "### Prepared Draft - [DATE]" section at the top (from running the Draft Prep prompt), use ONLY that section as the Notion source content. Ignore the original draft content below it.

4. **📦 Check for Consolidated Source Content (Parent Pages):**
   - Look for a section titled **"📦 Consolidated Source Content"** (often in a toggle/collapsible block)
   - If found, this page is a **parent** that absorbed one or more child articles
   - **CRITICAL:** The consolidated content is EQUALLY IMPORTANT source material
   - Extract and include ALL content from the consolidated section when merging
   - Document each consolidated source in your merge plan
   
   **Example structure in parent pages:**
   ```
   ▶ 📦 Consolidated Source Content
      ▶ Source: [Child Article Name]
         [Content from that child article]
      ▶ Source: [Another Child Article Name]
         [Content from that child article]
   ```

5. Identify the key topics, features, and troubleshooting steps covered
6. Note any gaps or areas that seem incomplete

### Step 1.5: Compare Both Sources First (REQUIRED)

Before doing any research or edits:

1. **Fetch BOTH** the Notion draft AND the existing Craft CMS article

2. **Terminology Consistency Check:**
   
   Extract and compare key terminology between Craft and Notion:
   
   | Term Type | Craft Article (Authority) | Notion Draft | Action |
   |-----------|---------------------------|--------------|--------|
   | Feature name (title) | [exact title] | [Notion title] | [Standardize to Craft / Flag] |
   | Technical terms | [list key terms] | [list key terms] | [Note differences] |
   | Field names | [e.g., `FieldName`] | [e.g., `FieldName`] | [Verify exact match] |
   
   **Terminology Rules:**
   - **Feature/Title name:** The Craft article's official name is authoritative (it's published, SEO-indexed)
   - **First reference in merged article:** Use the full official name, optionally noting the short form: "Grade Jump Riser Pricing (also called riser pricing)"
   - **Body references:** Follow Craft's existing usage pattern - if Craft uses a short form in body text, the merged article can too
   - **Field names:** Always use exact casing from codebase (e.g., `DiscountPriceLevelCode` not "discount price level code")
   
   **If Notion uses different terminology:** Standardize to Craft's terms unless the Notion term is clearly more accurate (e.g., reflects a product rename) - in that case, flag for Kyla's review.

3. **Quick Related Article Check:** Search Craft for other articles with similar topic keywords:
```graphql
{
  entries(section: "knowledgeBase", search: "[TOPIC KEYWORDS]", limit: 10) {
    title
    slug
  }
}
```
If any related articles found beyond the target, note them for the output flag.

4. **Create a side-by-side comparison:**

| Aspect | Craft Article (Existing) | Notion Draft | Consolidated Content (if any) |
|--------|--------------------------|--------------|-------------------------------|
| Sections | [list all section headers] | [list all section headers] | [list consolidated sources] |
| Word Count (approx) | [estimate] | [estimate] | [estimate] |
| Unique Content | [what Craft has that Notion doesn't] | [what Notion has that Craft doesn't] | [unique topics from consolidated] |
| Detail Level | [more/less detailed per section] | [more/less detailed per section] | [detail level] |

5. **Identify the merge plan:**
   - Content to KEEP from Craft: [list]
   - Content to ADD from Notion (main draft): [list]
   - Content to ADD from Consolidated Sources: [list each source and what it contributes]
   - Sections to ENHANCE with Notion details: [list]

6. **CONFIRM before proceeding:** The merge should result in MORE content, not less. If Notion has LESS detail than Craft in any area, the Craft content is kept. Consolidated source content should be fully incorporated.

### Step 2: Validate & Enhance with Context

**2A. Query Help Scout Tickets (BigQuery)**
Search for related tickets to validate accuracy and find additional context:

```sql
-- Step 1: Find relevant conversations
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

For promising tickets, fetch thread details:

```sql
-- Step 2: Get thread details (use IDs from step 1)
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

Look for in thread details:
- Common user questions/confusion points
- Solutions provided by support team (type = 'message')
- Internal notes with valuable context (type = 'note')
- Edge cases or exceptions mentioned

**Use these insights to populate the Troubleshooting/FAQs section.**

**2B. Validate with Codebase**
Search the codebase to verify:
- Feature behavior matches documentation
- Settings/configuration options are accurate
- Any technical details are correct
- No outdated information

**2C. Query Fathom Call Summaries (BigQuery)**
Search for relevant customer calls:

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

Look for:
- Customer training/onboarding discussions
- Feedback, confusion, or feature requests
- Real-world use cases mentioned

### Step 3: Document Validation Findings (DO NOT Edit Original Draft)

**IMPORTANT:** Do NOT edit the original Notion draft content. Keep it pristine for Kyla's auditing purposes.

Based on your validation and research, **document** the following findings (these will be applied in Step 6):

1. **Inaccuracies found** that need correction
2. **Missing context** from Help Scout tickets to add
3. **Real-world examples** from Fathom calls to include
4. **Outdated information** based on codebase that needs updating
5. **Clarity improvements** based on common support questions
6. **FAQ items** to add based on common ticket themes

Create a clear list of changes that will be applied when creating the merged article. The original Notion draft remains unchanged for audit trail purposes.

### Step 4: Visual Asset Recommendations (Only If Crucial)

**Philosophy: Minimize visual assets. Only suggest images/videos if CRUCIAL to understanding.**

Before recommending ANY visual, ask yourself:
1. Is this concept impossible to understand from text alone?
2. Does an image already exist in the article that covers this?
3. Would an experienced admin user really need a screenshot for this?

**If you answered NO to all 3 → Do NOT suggest an image.**

**Only suggest visuals when:**
- A complex workflow truly cannot be explained in text
- The UI is unintuitive and text instructions would confuse users
- There's a critical element that users frequently miss or overlook

**Do NOT suggest visuals for:**
- Basic navigation (admin users know how menus work)
- Standard buttons like "Save", "New", "Update"
- Concepts already covered by existing images in the article
- Step-by-step instructions that are clear in text form

**If on the fence:** Skip it. Kyla can always add images later if needed.

**When you DO suggest a visual (rare), embed INLINE in the Craft draft:**
- Insert at the exact location where it would appear
- Use this format:

```
[📸 IMAGE SUGGESTION FOR KYLA]
Type: Screenshot / Video
Capture: [exact screen/page]
Callouts: [specific arrows, highlights needed]
Why crucial: [brief justification - why text alone won't work]
[END IMAGE SUGGESTION]
```

**Goal: Make this quick for Kyla. Fewer images = faster turnaround.**

**⚠️ HARD LIMIT: Maximum 3 images per article.** Most articles need 0-1. Only suggest if CRUCIAL.

### Step 5: Update Craft CMS (MERGE, Don't Replace)

**This is the most critical step. Follow these rules exactly:**

#### 5.1 Review the Existing Craft Article Structure
Fetch and document:
- All existing sections and their content
- The overall structure and flow
- Any images, code blocks, or special elements

#### 5.2 Restructure to Match Required Format

Map existing content to the required structure:

| Required Section | Source Content |
|------------------|----------------|
| **Summary** | [from Craft/Notion - keep brief] |
| **Quick Start** | [extract key steps or CREATE if missing] |
| **How It Works** | [from existing Overview/explanation sections] |
| **Step-by-Step Setup** | [from existing setup instructions] |
| **Prerequisites** | [move to end if currently at beginning] |
| **Troubleshooting** | [combine: FAQs + Common Mistakes + Need Help + Help Scout insights] |

#### 5.3 Apply These Merge Rules (MANDATORY)

✅ **DO:**
- KEEP all existing Craft content unless it's factually incorrect
- ADD new sections from Notion that don't exist in Craft
- ENHANCE existing Craft sections by APPENDING Notion details
- RESTRUCTURE to match the required article format
- ADD a Quick Start section if one doesn't exist
- ADD Troubleshooting/FAQs based on Help Scout insights
- MAINTAIN all existing images, links, and formatting

❌ **DO NOT:**
- REMOVE existing Craft content (even if Notion doesn't have it)
- SIMPLIFY or SUMMARIZE existing detailed content
- REPLACE Craft sections with shorter Notion versions
- REDUCE the overall word count

#### 5.4 Output the Merge Plan Before Saving

Before making any changes, output:

```
MERGE PLAN CONFIRMATION
=======================
Existing Craft article word count: [X]
Expected final word count: [Y] (should be >= X)

RESTRUCTURING TO:
1. Summary: [source]
2. Quick Start: [new/existing]
3. How It Works: [source sections being combined]
4. Step-by-Step Setup: [source]
5. Prerequisites: [moved from/kept at end]
6. Troubleshooting: [new items from Help Scout + existing]

KEEPING from Craft:
- [Section 1]: [reason]
- [Section 2]: [reason]

ADDING from Notion (main draft):
- [New Section]: [what it adds]

📦 CONSOLIDATED SOURCES INCLUDED: [if applicable]
- Source: [Child Article Name]
  - Content: [summary of what this source contributes]
  - Adding to section(s): [where this content will be integrated]
- Source: [Another Child Article Name]
  - Content: [summary of what this source contributes]
  - Adding to section(s): [where this content will be integrated]
(If no consolidated sources, write "N/A - No consolidated content")

ENHANCING with Notion details:
- [Section]: [what details being added]

NEW CONTENT CREATED:
- Quick Start: [if didn't exist]
- Troubleshooting items: [from Help Scout]

DELETIONS: NONE (confirm no content is being removed)
```

#### 5.5 Execute the Merge (Follow This Order Exactly)

**Step A: Create the draft**
```graphql
mutation {
  createDraft(id: [ENTRY_ID], name: "KB Merge - [Article Name]", notes: "...") {
    draftId
  }
}
```

**Step B: Re-fetch the draft to get NEW section IDs**
```graphql
{
  entries(draftId: [DRAFT_ID]) {
    articleSections {
      __typename
      ... on text_Entry { id body }
    }
  }
}
```
⚠️ The section IDs will be DIFFERENT from the original article. Use these new IDs.

**Step C: Update the draft with merged content**
```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Draft(
    draftId: [DRAFT_ID]
    articleSections: {
      entries: [
        { tableOfContents: {} },
        { text: { id: "[NEW_ID_1]", body: "[Summary HTML]" } },
        { text: { id: "[NEW_ID_2]", body: "[Quick Start HTML]" } },
        { text: { id: "[NEW_ID_3]", body: "[How It Works HTML]" } },
        { text: { id: "[NEW_ID_4]", body: "[Step-by-Step HTML]" } },
        { text: { id: "[NEW_ID_5]", body: "[Prerequisites HTML]" } },
        { text: { id: "[NEW_ID_6]", body: "[Troubleshooting HTML]" } }
      ]
    }
  ) { id }
}
```

**Step D: Verify**
- Re-fetch draft to confirm content saved correctly
- Check word count is >= original
- Verify all required sections are present

**Remember:** 
- Replace special characters (→ to ">", smart quotes to regular)
- Do NOT publish - save as draft only
- Include inline image suggestions only if crucial (most articles: none)

### Step 6: Save Merged Content to Notion (TOP of page)

**Save the final merged article content back to Notion for review and history:**

**IMPORTANT:** Insert at the TOP of the page (after any existing header/metadata) so that the audit trail follows **newest to oldest** order.

1. At the **TOP** of the existing Notion page content, add a new section with the heading:
   ```
   ### Updated Craft Article - [DATE]
   ```

2. Below this heading, include IN THIS ORDER:
   - **Craft Draft URL:** Link to the draft in Craft admin
   - **Draft ID:** The draft ID number
   
   - **Visual Asset Decision:**
     - State whether images/videos were suggested or not
     - **Include your reasoning** for Kyla's context (2-3 sentences explaining why)
     - Example: "No additional images needed. The existing conceptual diagram sufficiently explains the If→Then mapping relationship. Text instructions for navigation are clear enough for admin users."
   
   - **Consolidated Sources Processed:** (if applicable)
     - List each source and what it contributed
     - Note which sections it was integrated into
   
   - **Terminology Standardization Applied:** (if any terms were standardized)
     - Include a table showing: Craft Term (Used) | Notion Term (Original) | Reasoning
     - This documents decisions for Kyla's review
   
   - **Merged Content (Validated):** The **COMPLETE** merged article content
     - **CRITICAL:** Include the FULL article text, not a summary or "see draft" link
     - Include ALL sections (Summary, Quick Start, How It Works, Setup, Prerequisites, Troubleshooting)
     - Preserve all formatting, links, and structure
     - This is the authoritative record of what was merged

3. This allows Kyla to:
   - Review the full merged content in Notion without opening Craft
   - Add comments and suggestions directly in Notion
   - Verify terminology standardization decisions
   - Provide feedback for prompt improvements
   - Maintain a complete history of the article evolution (newest at top)

### Step 7: Update Notion Status

Update the Notion page properties:
- Set `Status` to "Ready for Craft (Kyla Check)"
- Ensure `URL` field contains the Craft CMS article URL

---

## Output Format

Provide a summary of:

### 📌 Related Article Note (only if found)
If related articles were found beyond the target:
```
📌 **Related Article Note:** Found [Article Name] (/slug) which covers [related topic]. 
**Recommendation:** [Combine with target / Keep separate because X]
```

**If COMBINING:** You MUST also:
1. List the article(s) being absorbed: `/slug` (ID: XXXX)
2. **UNPUBLISH the absorbed article automatically:**
```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Entry(
    id: [ABSORBED_ARTICLE_ID]
    enabled: false
  ) {
    id
    enabled
  }
}
```
3. Document what was unpublished in the output

```
✅ **ABSORBED ARTICLE UNPUBLISHED:**
- [Article Name] (/slug) - ID: XXXX - Status: DISABLED
  Reason: Content merged into /[target-slug]
  Note: Can be re-enabled or deleted in Craft admin if needed
```

If none found, skip this section.

### Terminology Standardization
| Craft Term (Used) | Notion Term (Original) | Reasoning |
|-------------------|------------------------|-----------|
| [term] | [term] | [why Craft term was used / why flagged] |

### Source Comparison (from Step 1.5)
- Craft article sections: [list]
- Notion draft sections: [list]
- Consolidated sources: [list child articles absorbed, or "None"]
- Craft word count: [approx]
- Notion word count (including consolidated): [approx]
- Merge approach: [summary]

### 📦 Consolidated Content (if applicable)
If the parent page contains consolidated sources:
```
CONSOLIDATED SOURCES PROCESSED:
- [Child Article Name]: [summary of content contributed]
  - Integrated into: [which sections]
- [Another Child Article Name]: [summary of content contributed]
  - Integrated into: [which sections]

Related Archived Pages (do not process separately):
- [Child Article Notion URL] - Status: Archived (Consolidated)
```
If no consolidated content, skip this section.

### Validation Results
- [ ] Help Scout tickets reviewed: [count]
- [ ] Key insights found: [list]
- [ ] Codebase validation: [pass/issues found]
- [ ] Fathom calls reviewed: [count]
- [ ] Customer feedback themes: [list]

### Validation Findings (To Be Applied in Merged Article)
- **Inaccuracies to correct:** [list]
- **Context to add from Help Scout:** [list]
- **Examples from Fathom:** [list]
- **Outdated info to update:** [list]
- **Clarity improvements:** [list]
- **Troubleshooting items to add:** [list]

*(Original Notion draft remains unchanged for auditing)*

### Article Structure Applied
- [ ] Summary (2-3 sentences)
- [ ] Quick Start (5-7 steps)
- [ ] How It Works
- [ ] Step-by-Step Setup
- [ ] Prerequisites
- [ ] Troubleshooting (combines FAQs, common mistakes, need help)

### Visual Asset Decision
- **Decision:** [Images suggested / No images needed]
- **Reasoning:** [2-3 sentences explaining WHY - this helps Kyla understand your thinking]
- Example reasoning: "No additional images needed. The existing diagram covers the core concept. Navigation instructions are clear for admin users."

### Craft CMS Merge Summary
- Article updated: [URL]
- Status: Saved as Draft
- **Original word count:** [X]
- **Final word count:** [Y]
- Content KEPT from original: [list sections]
- Content ADDED from Notion: [list sections]
- Content ENHANCED: [list sections with what was added]
- Content REMOVED: NONE

### Notion Content Saved
- Added "Updated Craft Article" section at TOP of page: ✅
- **Full merged content preserved** (complete article text, not summary): ✅
- Terminology standardization table included: ✅
- Consolidated sources documented (if applicable): ✅
- Audit trail order: Newest to oldest

### Notion Status
- Updated to: Ready for Craft (Kyla Check)

---

## ⚠️ MANDATORY: Final Output Checklist

**Before completing this workflow, verify ALL of these are included in your Notion update:**

- [ ] "### Updated Craft Article - [DATE]" heading at TOP of Notion page
- [ ] Craft Draft URL and Draft ID
- [ ] **Full Validation Summary:**
  - [ ] Terminology Standardization table
  - [ ] Source Comparison (sections, word counts, merge approach)
  - [ ] Validation Results (tickets reviewed, key insights, all checkboxes)
  - [ ] Validation Findings Applied (context added, clarity improvements, troubleshooting items)
  - [ ] Article Structure Applied (all checkboxes)
  - [ ] Visual Asset Decision with reasoning (2-3 sentences)
  - [ ] Craft CMS Merge Summary table (entry ID, draft ID, word counts)
  - [ ] Content KEPT/ADDED/ENHANCED/REMOVED lists
- [ ] **Full Merged Content** (complete article text - NOT a summary or "see draft" link)
- [ ] Notion Status updated to "Ready for Craft (Kyla Check)"

**⛔ DO NOT provide partial output. DO NOT skip sections. The Notion update MUST include ALL items above.**

---

## Important Notes

- **MERGE means ENHANCE, not REPLACE** - The existing Craft article is the base. Notion content supplements it.
- **Follow the required article structure** - Summary, Quick Start, How It Works, Setup, Prerequisites, Troubleshooting
- If the existing Craft content is more detailed than Notion in any section, KEEP the Craft version
- The final article should ALWAYS be >= the length of the original (never shorter)
- Do NOT publish the Craft CMS article - save as draft only
- Do NOT edit the original Notion draft - keep it pristine for auditing
- Do NOT create any local files - all content goes to Craft draft or Notion
- Merged content and corrections go in the "Updated Craft Article" section at the TOP of the Notion page
- Image/video suggestions ONLY if crucial (MAXIMUM 3 per article, most need 0-1)
- If validation reveals significant issues with the draft, flag them before proceeding
- **If in doubt, KEEP existing content** - it's easier to remove later than to recreate
- **Save merged content to Notion** - Always save the final merged article under "### Updated Craft Article" for review and history
- **📦 Consolidated Articles:** Skip pages with status "Archived (Consolidated)" - their content lives in a parent page
- **📦 Parent Pages with Consolidated Content:** Always include the "Consolidated Source Content" section as source material when merging
```

---

## Integration Reference

### BigQuery (Help Scout)

**Dataset:** `hevo_dataset_supercat_data_pipeline_Slhk`
**Tables:** `conversation`, `conversation_threads`

**Step 1: Find relevant conversations**
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
  (LOWER(subject) LIKE '%[topic]%' 
   OR LOWER(subject) LIKE '%[alternate keyword]%')
  AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 730 DAY)
ORDER BY created_at DESC
LIMIT 30
```

**Step 2: Get thread details for relevant tickets**
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

**Thread types:** `customer` (from customer), `message` (support reply), `note` (internal - often most valuable!)

**Expected:** Most common features will have 10-50+ relevant tickets. If 0 results, try alternate keywords or broader search terms before concluding no tickets exist.

**Use ticket insights for:** Troubleshooting section, FAQs, common confusion points

### BigQuery (Fathom Call Summaries)

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
  (LOWER(`Ai Summary Plaintext Formatted`) LIKE '%[topic]%' 
   OR LOWER(`Meeting Title`) LIKE '%[topic]%')
  AND `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 730 DAY)
ORDER BY `Meeting Start Time` DESC
LIMIT 15
```

**Expected:** Common features often appear in onboarding/training calls. If 0 results, try alternate keywords before concluding no calls exist.

### Fathom API (Alternative)

For direct API access if needed:
```python
# Run from: SuperCat 4.0/integrations/fathom/
from fathom_api import get_meetings, get_summary
meetings = get_meetings(limit=200, paginate=True)
# Filter for relevant topic keywords in titles
```

### Notion MCP Integration

#### Fetching Page Content
Use the Notion MCP integration to fetch page content by ID or URL.

#### Updating Page Content

**Insert at TOP of page (for audit trail):**
- Use content replacement to add new sections at the top
- Preserve existing content below
- Selection must be UNIQUE - use longer snippets if needed

**Replace a section:**
- Select the section by its unique heading and ending text
- Replace with new content

**⚠️ CRITICAL:** Selection strings must be UNIQUE. If you get "Multiple matches found" error:
- Use longer snippets (more than 10 chars on each end)
- Include unique identifiers like dates or IDs

#### Updating Properties
Update the Status property to "Ready for Craft (Kyla Check)" using the Notion MCP integration.

### Craft CMS GraphQL (DETAILED - Read Before Executing)

**⚠️ IMPORTANT: Do NOT introspect full schema - causes timeouts. Use targeted queries.**

#### Querying Articles

```graphql
# Get article by slug (CORRECT)
{
  entries(section: "knowledgeBase", slug: "article-slug", limit: 1) {
    id
    title
    articleSections {
      __typename
      ... on text_Entry { id body }
      ... on tableOfContents_Entry { id }
    }
  }
}

# Get draft by ID
{
  entries(draftId: 829) {
    id
    title
    articleSections { ... }
  }
}
```

**❌ WRONG:** `entry(id: "41126")` - use `entries()` with filters instead

#### Creating a Draft

```graphql
mutation {
  createDraft(
    id: 41126,
    name: "KB Merge - Description",
    notes: "Merge notes here"
  ) {
    draftId
    id
  }
}
```

#### Updating Draft Content (articleSections)

**CRITICAL:** After creating a draft, the section IDs CHANGE. You MUST:
1. Create the draft first
2. Re-fetch the draft to get NEW section IDs
3. Use those new IDs when updating

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Draft(
    draftId: 829
    articleSections: {
      entries: [
        { tableOfContents: {} },
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

#### Special Characters in GraphQL Strings

**AVOID these characters** - they cause syntax errors:
- Arrow symbols (→) → Replace with ">" or "->"
- Smart quotes ("") → Replace with regular quotes or remove
- Em dashes (—) → Replace with regular dashes (-)
- Ampersands in HTML → Use `&amp;`

#### Updating Draft Metadata (Not Content)

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Draft(
    draftId: 829
    adminSummary: "Internal notes here"
    draftNotes: "Draft description"
  ) {
    id
  }
}
```

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

2. **Filter out consolidated/archived articles:**
   - SKIP any articles with Status = "Archived (Consolidated)"
   - These have already been absorbed into parent articles
   - Only process parent articles (Status = "In progress" or similar active status)

3. Process each article one at a time using the prompt above

4. Track progress in Notion by checking Status updates

**Note:** If you see multiple articles pointing to the same Craft URL, check their statuses. One should be the parent (active), others should be archived (consolidated). Only process the parent.

---

## Troubleshooting

### If the merge results in LESS content than the original:
- STOP and review - something went wrong
- The merge rules were not followed correctly
- Revert to the previous Craft revision and try again

### If Notion content conflicts with Craft content:
- Flag the conflict for manual review
- Do NOT automatically choose one over the other
- Document both versions in the output

### If the existing Craft article has outdated information:
- Flag it explicitly in the output
- Still KEEP the content but note it needs review
- Do NOT silently remove or "fix" it without approval

### Terminology Mismatch Between Craft and Notion
- **Default:** Use Craft's terminology (it's the published, authoritative source)
- **If Notion term seems more accurate:** Flag for Kyla's review, don't auto-change
- **Document all terminology decisions** in the output under "Terminology Standardization"
- **First reference pattern:** Use full official name, then short form is acceptable in body text

### GraphQL Syntax Errors
- **"Expected ':' found Name"** → Special characters in string. Replace arrows (→), smart quotes, em dashes
- **"Something went wrong"** → Query structure wrong. Use `entries()` not `entry()`, use inline fragments for Matrix fields

### New articleSections Entries Not Saving (Adding Sections)

**Problem:** When adding NEW sections to an article (e.g., Before You Begin, Troubleshooting), entries without an existing `id` may silently fail to save.

**Symptom:** You save the draft, re-fetch it, and the new sections are missing.

**Root Cause:** Craft's GraphQL mutation for articleSections has inconsistent behavior when mixing entries with IDs (updates) and entries without IDs (creates).

**Solution - Two-Pass Approach:**
1. **First mutation:** Update all EXISTING sections (those with IDs from the draft)
2. **Second mutation:** Re-fetch the draft, then save again with the NEW sections added

**Alternative - Pre-allocate IDs:**
If the original article has fewer sections than needed, you may need to:
1. Save the draft with existing sections first
2. Re-fetch to see what IDs exist
3. Add new `{ text: { body: "..." } }` entries (without id) in a separate mutation

**Verification:** ALWAYS re-fetch the draft after saving to confirm all sections were created. Count the sections and compare to expected.

```graphql
# After saving, verify with:
{
  entries(draftId: [DRAFT_ID]) {
    articleSections {
      __typename
      ... on text_Entry { id }
    }
  }
}
```

### Notion "Multiple matches found" Error
- Your selection_with_ellipsis matched more than one place in the document
- Use longer, more specific snippets on both ends
- Include unique text like dates, IDs, or specific phrases

### Draft Section IDs Don't Match
- After `createDraft`, the article sections get NEW IDs
- You MUST re-fetch the draft to get the new section IDs before updating content
- Old IDs from the original article will NOT work

### Help Scout Returns 0 Results
- **Try alternate keywords** - the topic may be referred to differently by customers
- **Broaden the search** - try partial terms or related concepts
- Check both mailboxes (Support AND Onboarding) are included
- Ensure ALL statuses are included (not just closed)
- If still 0 after trying alternates, document: "No relevant tickets found after searching: [list keywords tried]"

### Fathom Returns No Relevant Calls
- **Try alternate keywords** - customers may describe features differently
- Check recent onboarding calls - new features often discussed there
- If still 0 after trying alternates, document: "No relevant calls found after searching: [list keywords tried]"
- Note: Niche/admin-only features (like Option Mapping) may genuinely have few customer calls

### Consolidated Articles - Common Scenarios

**Scenario 1: You encounter an "Archived (Consolidated)" page**
- STOP - do not process this article
- Find the parent article (linked in the consolidation banner)
- Process the parent article instead
- Output: "⏭️ SKIPPED: Archived (Consolidated) - content lives in [Parent Article Name]"

**Scenario 2: Parent page has "📦 Consolidated Source Content" section**
- This is a parent that absorbed child article(s)
- Expand/read the consolidated section completely
- Treat all consolidated content as equally important source material
- Document each consolidated source in your merge plan
- The parent + consolidated content = complete source material for merging

**Scenario 3: Two Notion pages point to the same Craft URL**
- Check the Status field on each:
  - If one is "Archived (Consolidated)" → skip it, process the other (parent)
  - If both are "In progress" → flag for Kyla (manual consolidation may be needed)
- Never process both separately - this would cause duplicate work

**Scenario 4: Consolidated content contradicts main draft content**
- Parent's main content takes priority (it's the curated version)
- Consolidated content should supplement, not override
- If significant contradiction, flag for Kyla's review

---

## Example: Revised Article Structure

Here's what a well-structured KB article looks like:

```html
<h2>Summary</h2>
<p>Option Mapping lets you create dependencies between product options—when a 
customer selects one option, it automatically filters what's available in the 
next option set.</p>

<h2>Quick Start</h2>
<p>Already have your product options set up? Here's how to create a mapping:</p>
<ol>
  <li>Go to <strong>Admin Console > Products > Option Mappings</strong></li>
  <li>Click <strong>New Option Mapping</strong></li>
  <li>Select your first option type (e.g., Fabric)</li>
  <li>Click <strong>Add Mapping Connection</strong></li>
  <li>Choose an Option Group, then select the target option type</li>
  <li>Click <strong>Update mapping</strong> to save</li>
</ol>

<h2>How It Works</h2>
<h3>The Basic Concept</h3>
<p>Think of it like a filter chain...</p>
[detailed explanation with examples]

<h2>Step-by-Step Setup</h2>
<h3>Step 1: Access Option Mappings</h3>
<p>Go to <strong>Admin Console > Products > Option Mappings</strong></p>
[full walkthrough]

<h2>Before You Begin</h2>
<p>Option Mapping requires your product options to be configured first.</p>
<p>📖 <strong>Need help?</strong> See <a href="...">Product Options Guide</a></p>

<h2>Troubleshooting</h2>
<h3>"I don't see Option Mappings in my menu"</h3>
<p>Make sure you're logged in as an Org Admin or Super Admin.</p>
[more FAQ items from Help Scout insights]
```
