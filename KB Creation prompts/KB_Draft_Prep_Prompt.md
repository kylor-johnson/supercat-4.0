# KB Draft Prep Prompt

**Purpose:** Process rough/incomplete Notion KB draft articles by organizing, validating, and polishing them BEFORE running through the KB Merge prompt. This is the "cleanup" step for messy drafts.

**When to Use:** When a Notion KB draft is disorganized, incomplete, has duplicate content, or needs significant restructuring before it can be properly merged with an existing Craft article.

**⚠️ IMPORTANT:** All validation notes, changes, and audit trail go at the **TOP of the Notion page**. Do NOT create separate validation files.

---

## Article Structure & Tone Guidelines

### Target Audiences

KB articles serve **two audiences**:

| Audience | Need | How They Use Articles |
|----------|------|----------------------|
| **Self-service users** | Scan quickly, find answer, follow steps | Search KB directly |
| **Kyla sending links** | Jump to specific section, resolve in 1-2 touches | Links to specific sections in support replies |

### Required Article Structure

All prepared drafts should follow this structure (same as Merge prompt):

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
You are helping me prepare a rough KB draft article for merging. This draft needs to be ORGANIZED, VALIDATED, and POLISHED before it can be properly merged with an existing Craft CMS article.

**CRITICAL RULE:** Keep the ORIGINAL draft content untouched. Save all improvements to the TOP of the Notion page as audit trail.

**FORMATTING:** Before generating any content, READ the file `prompts/2.0_Craft_CMS_Formatting_Guidelines.md` and apply all rules (bold usage, field names in single quotes, blockquote callouts, step structure, article type templates, image placeholder format, etc.).

## Article Information

**Notion Draft Article:** [PASTE NOTION URL]
**Target Craft CMS Article (for context):** [PASTE CRAFT KB URL IF AVAILABLE]

---

## Your Task

### Step 1: Analyze the Current Draft

1. Fetch the Notion page content using the Notion Direct API (see Integration Reference below)

2. **Quick Related Article Check:** Search Craft for other articles with similar topic keywords beyond the target article:
```graphql
{
  entries(section: "knowledgeBase", search: "[TOPIC KEYWORDS]", limit: 10) {
    title
    slug
  }
}
```
If any potentially related articles found, note them for the output flag.

3. Create an analysis of the current state:

| Aspect | Current State |
|--------|---------------|
| Total sections | [count] |
| Estimated word count | [approx] |
| Organization | [Good / Needs work / Messy] |
| Duplicate content | [Yes / No - describe if yes] |
| Missing obvious sections | [list any gaps] |
| Audience clarity | [Clear / Mixed - who is this for?] |
| Formatting consistency | [Consistent / Inconsistent] |

4. **Terminology Check (if target Craft article provided):**

   If a target Craft article URL is provided, compare terminology:
   
   | Term Type | Craft Article (Authority) | Notion Draft | Action Needed |
   |-----------|---------------------------|--------------|---------------|
   | Feature name (title) | [exact title] | [Notion title] | [Standardize / Flag] |
   | Technical terms | [list key terms] | [list key terms] | [Note differences] |
   
   **Rule:** The Craft article's terminology is authoritative. If the Notion draft uses different names for the same concepts, the prepared draft should adopt Craft's terminology to ensure consistency when merged.
   
   **Pattern to follow:**
   - **First reference:** Use full official name (e.g., "Grade Jump Riser Pricing")
   - **Subsequent references:** Short form is acceptable if Craft uses it (e.g., "riser pricing")
   - **Field names:** Always use exact casing from codebase

5. Identify the main issues that need fixing:
   - [ ] Out of order sections
   - [ ] Duplicate content
   - [ ] Incomplete sections
   - [ ] Mixed audiences (admin vs end-user vs developer)
   - [ ] Formatting inconsistencies
   - [ ] Missing context or explanations
   - [ ] Terminology mismatches with target Craft article

### Step 2: Research & Validate Content

**2A. Query Help Scout Tickets (BigQuery)**
Search for related tickets to validate accuracy and find missing context:

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
- Internal notes with context (type = 'note') - often most valuable!
- Edge cases or exceptions mentioned

**2B. Validate with Codebase**
Search the codebase to verify:
- Feature behavior matches documentation
- Settings/configuration options are accurate
- Any technical details are correct
- API endpoints and parameters are current
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

### Step 3: Create Reorganization Plan

Based on your analysis, create a plan for reorganizing the content:

**3A. Determine the Target Audience(s)**
Who is this article for?
- [ ] End users (sales reps using iPad app)
- [ ] Admins (setting up features in admin portal)
- [ ] Both (separate sections clearly)
- [ ] Developers (API usage)

**3B. Define the Logical Section Order**
Create an outline of how the article SHOULD flow:

```
PROPOSED STRUCTURE
==================
1. [Section Name] - [What it covers]
2. [Section Name] - [What it covers]
3. [Section Name] - [What it covers]
...
```

**3C. Map Existing Content to New Structure**
For each section in your proposed structure:

| New Section | Source Content | Action Needed |
|-------------|----------------|---------------|
| Overview | Scattered intro paragraphs | Consolidate |
| Setup (Admin) | "Step 1: Enable..." section | Move & expand |
| How to Use | "Using Mobile Apps" + "Enter Commitments" | Combine |
| Troubleshooting | FAQ + Common Mistakes + Need Help sections | Combine into one |
| [New section] | N/A | Create from research |

### Step 4: Create the Polished Draft

**IMPORTANT:** Do NOT edit the original Notion draft. Create the polished version as a NEW section.

**4A. Apply These Organization Rules:**

✅ **DO:**
- Start with "What is [Feature]?" or "Overview"
- Group content by audience (Admin Setup → End User Usage)
- Use consistent heading hierarchy (H2 for main sections, H3 for subsections)
- Include clear transitions between sections
- Add context where the original was too terse
- Remove or consolidate duplicate content
- Fix formatting inconsistencies

❌ **DO NOT:**
- Remove content that might be useful (consolidate instead)
- Change technical accuracy without validation
- Add information you're not sure about
- Over-simplify complex but necessary details

**4B. Required Article Structure:**

Reorganize content to match this structure (same as Merge prompt expects):

```
## Summary (2-3 sentences max)
What is this feature? When would I use it?

## Quick Start (5-7 numbered steps)
Get started immediately - no theory, just actions.
For "just tell me what to click" users.

## How It Works
Conceptual explanation with examples.
Key rules and limitations.
For "I want to understand" users.

## Step-by-Step Setup (detailed version)
Full walkthrough with context.
Tips and best practices.

## Before You Begin / Prerequisites
Link to related articles.
Keep brief - don't overwhelm.

## Troubleshooting
Common issues, FAQs, and mistakes - all in one section.
End with "Need more help? Contact Support"
```

**Formatting Rules:**
- Navigation paths: Use `>` symbols → `Admin Console > Products > Option Mappings`
- UI elements: Bold the exact text → Click **Save**
- Lists: Numbered for sequential steps, bullets for non-sequential
- Tables: Use for comparisons, rules, quick-reference

**4C. Incorporate Research Findings:**
- Add context from Help Scout tickets (common questions, edge cases)
- Include real-world examples from Fathom calls
- Correct any inaccuracies found during validation
- Fill gaps identified during codebase review

### Step 5: Visual Asset Recommendations (Only If Crucial)

**Philosophy: Minimize visual assets. Only suggest images/videos if CRUCIAL to understanding.**

Before recommending ANY visual, ask yourself:
1. Is this concept impossible to understand from text alone?
2. Would an experienced admin user really need a screenshot for this?
3. Is there a complex workflow that truly cannot be explained in text?

**If you answered NO to all 3 → Do NOT suggest an image.**

**⚠️ HARD LIMIT: Maximum 3 images per article.** Most articles need 0-1. Prioritize:
1. Most common issue/use case
2. Complex navigation that's hard to describe
3. Before/after comparisons

**When you DO suggest a visual (rare), note it inline:**

```
[📸 IMAGE SUGGESTION FOR KYLA]
Type: Screenshot / Video
Capture: [exact screen/page]
Why crucial: [brief justification]
[END IMAGE SUGGESTION]
```

### Step 6: Save Prepared Draft to Notion (TOP of page)

**Save the polished draft back to Notion for review and as audit trail:**

**IMPORTANT:** Insert at the TOP of the page so the audit trail follows **newest to oldest** order.

1. At the **TOP** of the existing Notion page content, add a new section:

```
### Prepared Draft - [DATE]

**Status:** Ready for KB Merge Prompt

**What Was Fixed:**
- [List main changes made]
- [e.g., "Reorganized sections into logical flow"]
- [e.g., "Consolidated duplicate content"]
- [e.g., "Added missing troubleshooting section"]

**Research Summary:**
- Help Scout tickets reviewed: [count]
- Key insights: [brief list]
- Codebase validation: [pass/issues found]
- Fathom calls reviewed: [count]

**Visual Asset Decision:**
- [Decision + reasoning]

---

## [POLISHED ARTICLE CONTENT STARTS HERE]

[Full reorganized, validated article content]

---
### END PREPARED DRAFT
```

2. This allows Kyla to:
   - See exactly what was changed
   - Review the polished content before running Merge prompt
   - Maintain audit trail of the article evolution

### Step 7: Update Notion Status

Update the Notion page properties:
- Set `Status` to "Ready for Merge"

---

## Output Format

**All output goes at the TOP of the Notion page as the audit trail.** Do NOT create separate validation files.

Provide a summary of:

### 📌 Related Article Note (only if found)
If related articles were found beyond the target:
```
📌 **Related Article Note:** Found [Article Name] (/slug) which covers [related topic]. 
**Recommendation:** [Combine with target / Keep separate because X]
```

**If recommending COMBINE:** Flag for the Merge prompt:
```
⚠️ **MERGE PROMPT NOTE:** The following article(s) will be AUTO-UNPUBLISHED when merged:
- [Article Name] (/slug) - ID: XXXX
  Reason: Content will be merged into /[target-slug]
```

If none found, skip this section.

### Draft Analysis
- Original state: [messy/incomplete/disorganized]
- Main issues found: [list]
- Word count before: [approx]
- Word count after: [approx]

### Research Results
- [ ] Help Scout tickets reviewed: [count]
- [ ] Key insights found: [list]
- [ ] Codebase validation: [pass/issues found]
- [ ] Fathom calls reviewed: [count]

### Article Structure Applied
- [ ] Summary (2-3 sentences)
- [ ] Quick Start (5-7 steps)
- [ ] How It Works
- [ ] Step-by-Step Setup
- [ ] Before You Begin / Prerequisites
- [ ] Troubleshooting (combines FAQs, common mistakes, need help)

### Terminology Standardization (if target Craft article provided)
| Notion Term (Original) | Standardized To | Reasoning |
|------------------------|-----------------|-----------|
| [term] | [Craft term] | [why - e.g., "matches published article title"] |

### Changes Made
- **Reorganized:** [what was moved/restructured]
- **Consolidated:** [what duplicates were merged]
- **Added:** [what new content was created from research]
- **Corrected:** [what inaccuracies were fixed]
- **Terminology standardized:** [what terms were aligned to Craft article]
- **Removed:** [what was deleted, if anything, and why]

### Visual Asset Decision
- **Decision:** [Images suggested / No images needed]
- **Reasoning:** [2-3 sentences explaining WHY]

### Prepared Draft Saved
- Added "Prepared Draft" section at TOP of page: ✅
- Full polished content preserved for review: ✅
- Audit trail maintained: ✅

### Notion Status
- Updated to: Ready for Merge

### Next Step
Run the **KB Merge Article Validation Prompt** to merge this prepared draft with the existing Craft CMS article.

---

## ⚠️ MANDATORY: Final Output Checklist

**Before completing this workflow, verify ALL of these are included in your Notion update:**

- [ ] "### Prepared Draft - [DATE]" heading at TOP of Notion page
- [ ] **Full Validation Summary:**
  - [ ] Terminology Standardization table (if applicable)
  - [ ] Research sources documented (Help Scout, Fathom, Codebase)
  - [ ] Content organization changes documented
  - [ ] Visual Asset Decision with reasoning
- [ ] **Full Prepared Draft** (complete reorganized article text - NOT a summary)
- [ ] Original draft content preserved below (untouched)
- [ ] Notion Status updated to "Ready for Merge"

**⛔ DO NOT provide partial output. DO NOT skip sections. The Notion update MUST include ALL items above.**

---

## Important Notes

- **Keep original draft untouched** - All changes go in the "Prepared Draft" section at TOP
- **Prepared Draft = Newest at top** - Maintains audit trail order
- **NO SEPARATE FILES** - All validation notes, changes, and audit trail go in the Notion page, NOT in separate local files
- **This is PREP, not MERGE** - We're fixing the Notion draft, not touching Craft yet
- **Don't over-edit** - The goal is organization and validation, not rewriting
- **Preserve useful content** - When in doubt, keep it and reorganize rather than delete
- **Image suggestions are rare** - Most articles need 0-1 additional images
- **If validation reveals major issues** - Flag them clearly before reorganizing
```

---

## Integration Reference

### BigQuery (Help Scout)

**Dataset:** `hevo_dataset_supercat_data_pipeline_Slhk`
**Tables:**
- `conversation` - Main ticket/conversation data
- `conversation_threads` - Thread details and messages

**Step 1: Find relevant conversations**
```sql
-- Query Help Scout conversations
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
-- Get thread details (replace IDs with actual conversation IDs found)
SELECT 
  conversation_id,
  SUBSTR(body, 1, 1000) as body_preview,
  created_at,
  type
FROM `hevo_dataset_supercat_data_pipeline_Slhk.conversation_threads`
WHERE CAST(conversation_id AS INT64) IN (123456789, 987654321)
ORDER BY conversation_id, created_at
LIMIT 30
```

**Thread types:**
- `customer` - Message from customer
- `message` - Reply from support
- `note` - Internal note (often contains valuable context!)
- `lineitem` - Status change

### BigQuery (Fathom Call Summaries)

**Dataset:** `Fathom`
**Table:** `ai_summaries_parsed`

```sql
-- Search Fathom AI summaries for topic-related discussions
SELECT 
  ID as recording_id,
  `Meeting Title` as title,
  `Meeting Start Time` as meeting_date,
  `Fathom User Name` as host,
  SUBSTR(`Ai Summary Plaintext Formatted`, 1, 800) as summary_preview
FROM `Fathom.ai_summaries_parsed`
WHERE 
  (LOWER(`Ai Summary Plaintext Formatted`) LIKE '%[topic]%' 
   OR LOWER(`Ai Summary Plaintext Formatted`) LIKE '%[alternate keyword]%'
   OR LOWER(`Meeting Title`) LIKE '%[topic]%')
  AND `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 730 DAY)
ORDER BY `Meeting Start Time` DESC
LIMIT 15
```

**Key columns in Fathom:**
- `Meeting Title` - Title of the call
- `Meeting Start Time` - When the call happened
- `Ai Summary Plaintext Formatted` - Full AI summary text
- `Fathom User Name` - Who hosted the call
- `Recording URL` - Link to the recording
- `Situation`, `Pain`, `Next Steps` - MEDDIC fields (if populated)

### Fathom API (Alternative)

For direct API access (if BigQuery doesn't have recent calls):

```python
# Run from: SuperCat 4.0/integrations/fathom/
from fathom_api import get_meetings, get_summary

# Get recent meetings
meetings = get_meetings(limit=200, paginate=True)

# Filter for relevant keywords
keywords = ['[topic]', '[alternate keyword]', 'onboarding', 'training']
relevant = [m for m in meetings if any(kw in (m.get('title') or '').lower() for kw in keywords)]

# Get summary for a specific call
summary = get_summary(recording_id=12345678)
```

### Notion Direct API Integration

**Location:** `notion_direct_access.js` in workspace root  
**Documentation:** `documentation/setup-guides/NOTION_API_SETUP.md`

#### Fetching Page Content

Extract the page ID from the Notion URL:
```
https://www.notion.so/workspace/Page-Title-240231dbcd70806c81f9f432ce26b2f8
→ Page ID: 240231dbcd70806c81f9f432ce26b2f8 (or with dashes: 240231db-cd70-806c-81f9-f432ce26b2f8)
```

**Get page details:**
```javascript
import { getPage, getPageContent } from './notion_direct_access.js';

// Get page properties
const page = await getPage('PAGE_ID');
console.log(page.properties);

// Get page content blocks
const content = await getPageContent('PAGE_ID');
content.results.forEach(block => {
  if (block.type === 'paragraph') {
    console.log(block.paragraph.rich_text.map(t => t.plain_text).join(''));
  }
});
```

**Search for pages:**
```javascript
import { searchPages } from './notion_direct_access.js';

const results = await searchPages('KB Backlog');
results.results.forEach(page => {
  const title = Object.values(page.properties).find(p => p.type === 'title');
  console.log(title?.title.map(t => t.plain_text).join(''));
});
```

#### Updating Page Properties

**Update Status property:**
```javascript
import { updatePage } from './notion_direct_access.js';

await updatePage('PAGE_ID', {
  'Status': {
    status: {
      name: 'Ready for Merge'
    }
  }
});
```

#### Command Line Quick Test
```bash
# Test connection and list accessible pages
node notion_direct_access.js

# Update a page title
node update_notion_title.js "PAGE_ID" "New Title"
```

**Note:** The API token is embedded in the scripts. No additional setup required.

### Craft CMS GraphQL (For Context Only)

If a target Craft article URL is provided, fetch it for context on what the final merged article should look like:

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

---

## Usage

1. Copy the prompt above
2. Replace `[PASTE NOTION URL]` with the rough Notion draft URL
3. Optionally add the target Craft article URL for context
4. Replace `[TOPIC KEYWORD]` with relevant search terms
5. Run in Cursor
6. After completion, run the **KB Merge Article Validation Prompt** to merge with Craft

---

## When to Use This Prompt vs. Going Straight to Merge

| Draft State | Use This Prompt? | Then Merge? |
|-------------|------------------|-------------|
| Messy/disorganized | ✅ Yes | Then Merge |
| Incomplete sections | ✅ Yes | Then Merge |
| Duplicate content | ✅ Yes | Then Merge |
| Mixed audiences (jumbled) | ✅ Yes | Then Merge |
| Well-organized but needs validation | ⚠️ Maybe | Or go straight to Merge |
| Clean and complete | ❌ No | Go straight to Merge |

**Rule of thumb:** If you look at the Notion draft and think "this is a mess," use this Prep prompt first.

---

## Troubleshooting

### If the draft is VERY incomplete (just bullet points)
- Do more extensive research (Help Scout, Fathom, Codebase)
- Create content from research findings
- Flag in output that significant content was added
- Kyla should review carefully before merging

### If the draft has conflicting information
- Flag the conflict clearly
- Note what the codebase says vs. what the draft says
- Let Kyla decide which is correct

### If you can't determine the target audience
- Default to: Admin Setup section + End User section
- Separate them clearly with headers
- Note the ambiguity in your output

### Notion "Multiple matches found" Error
- Your selection_with_ellipsis matched more than one place
- Use longer, more specific snippets
- Include unique text like dates or specific phrases

### Help Scout Returns 0 Results
- Try alternate keywords
- Broaden the search
- If still 0, document: "No relevant tickets found after searching: [keywords tried]"

### Can't Find Feature in Codebase
- Try different search terms
- Check for alternate naming (the feature might be called something different in code)
- Note what you searched for in output

### Notion Draft Uses Different Terminology Than Craft Article
- **Default:** Standardize to Craft's terminology in the prepared draft
- **If Notion term seems more accurate:** Flag for Kyla's review with reasoning
- **Document changes:** List all terminology standardizations in output
- **Why this matters:** Consistent terminology improves searchability, reduces user confusion, and maintains brand consistency across the KB
