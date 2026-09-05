# KB Merge Article Validation & Update Prompt

**Purpose:** Process Notion KB backlog articles tagged as `Action Type = Merge` by validating content, enhancing with additional context, and updating the existing Craft CMS article.

**Critical Rule:** MERGE means ENHANCE, not REPLACE. The existing Craft article is the foundation. Notion content ADDS to it. The final article should ALWAYS be >= the length of the original.

**Integration Reference:** See `KB_Integration_References_Final.md` for all BigQuery, Notion, and Craft CMS query templates.

---

## Article Structure & Tone Guidelines

### Target Audiences

KB articles serve **two audiences**:

| Audience | Need | How They Use Articles |
|----------|------|----------------------|
| **Self-service users** | Scan quickly, find answer, follow steps | Search KB directly |
| **Kyla sending links** | Jump to specific section, resolve in 1-2 touches | Links to specific sections in support replies |

### Article Type Classification

**Before structuring any article, classify its type using `2.0_Craft_CMS_Formatting_Guidelines.md`.**

| If the article... | Then use... |
|-------------------|-------------|
| Helps users fix an error or problem | **Template A: Troubleshooting Guide** |
| Explains what a feature is AND how to set it up | **Template B: Feature Overview + Setup** |
| Walks users through a specific task | **Template C/D: How-To Guide** |
| Documents multiple related items (errors, settings, concepts) | **Template E: Reference Guide** |
| Explains a concept or behavior (no setup required) | **Concept Explainer** (see below) |

**Concept Explainer Structure** (for explanatory articles like "Understanding Category Filters"):
```
## Overview
What is this? Brief explanation.

## Key Behavior / How It Works
Bullet points explaining the core concepts/rules.

## Example Explanation
How to explain this to customers in plain language.

## Troubleshooting
Common questions about this concept.
```

**📄 See `2.0_Craft_CMS_Formatting_Guidelines.md` for full template details and decision trees.**

**Note:** Do NOT include separate sections for FAQs, Common Mistakes, Need Help, or Related Articles. Combine all troubleshooting content into one "Troubleshooting" section. Craft auto-generates Related Articles.

### Writing Principles

| Principle | Do This | Not This |
|-----------|---------|----------|
| **Lead with USER BENEFIT** | "Capture customer interest so you can follow up later" | "Track demand before production for analysis" |
| **Lead with action** | "Go to Admin Console > Products" | "In many products, particularly those with customizable attributes..." |
| **Plain language** | "Click Save" | "Select Update mapping to persist your changes" |
| **Scannable headings** | "Step 1: Access Option Mappings" | "Accessing the Feature" |
| **Two paths** | Quick Start + Detailed sections | Single wall of text |
| **Specific navigation** | "Admin Console > Products > Option Mappings" | "Navigate to the option mappings area" |

### Summary Quality Rules

**Lead with USER BENEFIT, not technical mechanism:**

| ❌ Bad (Technical/Mechanical) | ✅ Good (User Benefit) |
|-------------------------------|------------------------|
| "Track customer demand before products go into production" | "Capture customer interest when they're not ready to order, so you can follow up later" |
| "Synchronizes data to the manufacturer for analysis" | "Keeps a record of who's interested in what, so nothing falls through the cracks" |
| "Enables field-based promotion pricing via product file" | "Apply discounts to selected items with a single tap at trade shows or promotions" |

**Plain Language Test:** Can you explain this feature to a non-technical user in one sentence? If not, rewrite.

**"So what?" Test:** After reading the Summary, would a user know WHY they'd want this feature?

### ⚠️ Common Mistake: Technical Documentation Bias

Technical docs and codebase comments often describe:
- HOW a feature works mechanically
- WHAT data it captures/stores
- WHERE it fits in the system architecture

But users care about:
- WHAT problem it solves for them
- WHY it makes their job easier
- WHEN they would use it

**Always validate your understanding of the feature's PURPOSE with Help Scout tickets, Fathom calls, or the live article before writing the Summary.**

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

**FORMATTING:** Before generating any HTML content, READ the file `prompts/2.0_Craft_CMS_Formatting_Guidelines.md` and apply all rules.

**INTEGRATION REFERENCE:** READ `KB Creation prompts/KB_Integration_References_Final.md` for all query templates (BigQuery, Notion, Craft CMS).

**ARTICLE STRUCTURE:** 
1. READ `2.0_Craft_CMS_Formatting_Guidelines.md` - "Article Type Classification" section
2. Classify this article's type based on its primary purpose
3. Apply the matching template structure from the guidelines
4. All articles should end with a Troubleshooting section (combines FAQs, common mistakes)

## Article Information

**Notion Draft Article:** [PASTE NOTION URL]
**Target Craft CMS Article to Update:** [PASTE CRAFT KB URL FROM THE URL FIELD]

---

## Your Task

### Step 1: Review the Notion Draft

1. Fetch the Notion page content using the Notion Direct API

2. **🛑 CHECK STATUS FIRST - Archived (Consolidated) Pages:**
   - If the page `Status` = **"Archived (Consolidated)"** → **STOP IMMEDIATELY**
   - This article's content has been rolled into a parent article
   - Look for the callout banner: `📦 **CONSOLIDATED:** This article's content has been incorporated into...`
   - **Output:** "⏭️ SKIPPED: This article is archived (consolidated into [Parent Article Name]). Process the parent instead."

3. **Check for Prepared Draft:** If the page has a "### Prepared Draft - [DATE]" section at the top, use ONLY that section as the Notion source content.

4. **📦 Check for Consolidated Source Content (Parent Pages):**
   - Look for a section titled **"📦 Consolidated Source Content"**
   - If found, this page is a **parent** that absorbed one or more child articles
   - **CRITICAL:** The consolidated content is EQUALLY IMPORTANT source material
   - Extract and include ALL content from the consolidated section when merging

5. Identify the key topics, features, and troubleshooting steps covered
6. Note any gaps or areas that seem incomplete

### Step 1.5: Compare Both Sources First (REQUIRED)

Before doing any research or edits:

1. **Fetch BOTH** the Notion draft AND the existing Craft CMS article

2. **Terminology Consistency Check:**
   
   | Term Type | Craft Article (Authority) | Notion Draft | Action |
   |-----------|---------------------------|--------------|--------|
   | Feature name (title) | [exact title] | [Notion title] | [Standardize to Craft / Flag] |
   | Technical terms | [list key terms] | [list key terms] | [Note differences] |
   | Field names | [e.g., `FieldName`] | [e.g., `FieldName`] | [Verify exact match] |
   
   **Terminology Rules:**
   - **Feature/Title name:** The Craft article's official name is authoritative
   - **First reference:** Use the full official name, optionally noting the short form
   - **Field names:** Always use exact casing from codebase

3. **Quick Related Article Check:** Search Craft for other articles with similar topic keywords. If any found beyond the target, note them for the output flag.

4. **Create a side-by-side comparison:**

| Aspect | Craft Article (Existing) | Notion Draft | Consolidated Content (if any) |
|--------|--------------------------|--------------|-------------------------------|
| Sections | [list all section headers] | [list all section headers] | [list consolidated sources] |
| Word Count (approx) | [estimate] | [estimate] | [estimate] |
| Unique Content | [what Craft has that Notion doesn't] | [what Notion has that Craft doesn't] | [unique topics from consolidated] |

5. **Identify the merge plan:**
   - Content to KEEP from Craft: [list]
   - Content to ADD from Notion: [list]
   - Content to ADD from Consolidated Sources: [list]
   - Sections to ENHANCE with Notion details: [list]

6. **CONFIRM before proceeding:** The merge should result in MORE content, not less.

### Step 1.6: Validate Feature Purpose (REQUIRED Before Writing Summary)

**⚠️ CRITICAL:** Before writing or approving any Summary content, validate the feature's PURPOSE from the user's perspective.

**Answer these questions:**

| Question | Your Answer |
|----------|-------------|
| **WHO** uses this feature? | [specific user role] |
| **WHAT problem** does it solve for them? | [plain language] |
| **WHY** would they use it instead of alternatives? | [key benefit] |
| **WHEN/WHERE** do they use it? | [context] |

**Validate against at least 2 sources:**
- [ ] Help Scout tickets: How do users describe their need?
- [ ] Fathom calls: How does support/sales explain it?
- [ ] Live article (if exists): How is it currently framed?

**Red Flags - Rewrite Summary if:**
- Summary describes mechanism but not benefit
- Summary uses jargon without context
- A non-technical user would ask "so what?" after reading it

### Step 2: Validate & Enhance with Context

**2A. Query Help Scout Tickets (BigQuery)**
Search for related tickets to validate accuracy and find additional context. Use queries from Integration Reference.

Look for in thread details:
- Common user questions/confusion points
- Solutions provided by support team
- Internal notes with valuable context
- Edge cases or exceptions mentioned

**Use these insights to populate the Troubleshooting/FAQs section.**

**2B. Validate with Codebase**
Search the codebase to verify:
- Feature behavior matches documentation
- Settings/configuration options are accurate
- Any technical details are correct

**2C. Query Fathom Call Summaries (BigQuery)**
Search for relevant customer calls. Look for:
- Customer training/onboarding discussions
- Feedback, confusion, or feature requests
- Real-world use cases mentioned

### Step 3: Document Validation Findings (DO NOT Edit Original Draft)

**IMPORTANT:** Do NOT edit the original Notion draft content. Keep it pristine for auditing.

Document the following findings:
1. **Inaccuracies found** that need correction
2. **Missing context** from Help Scout tickets to add
3. **Real-world examples** from Fathom calls to include
4. **Outdated information** based on codebase
5. **Clarity improvements** based on common support questions
6. **FAQ items** to add based on common ticket themes

### Step 4: Visual Asset Recommendations (Only If Crucial)

**Philosophy: Minimize visual assets. Only suggest images/videos if CRUCIAL to understanding.**

Before recommending ANY visual, ask yourself:
1. Is this concept impossible to understand from text alone?
2. Does an image already exist in the article that covers this?
3. Would an experienced admin user really need a screenshot for this?

**If you answered NO to all 3 → Do NOT suggest an image.**

**⚠️ HARD LIMIT: Maximum 3 images per article.** Most articles need 0-1.

**When you DO suggest a visual (rare), embed INLINE in the Craft draft:**
```
[📸 IMAGE SUGGESTION FOR KYLA]
Type: Screenshot / Video
Capture: [exact screen/page]
Callouts: [specific arrows, highlights needed]
Why crucial: [brief justification]
[END IMAGE SUGGESTION]
```

### Step 5: Update Craft CMS (MERGE, Don't Replace)

#### 5.1 Review the Existing Craft Article Structure
Fetch and document all existing sections, structure, and special elements.

#### 5.2 Classify Article Type and Apply Template

**Step A: Classify the article type**

| If the content... | Article Type |
|-------------------|--------------|
| Fixes an error/problem | Troubleshooting Guide |
| Explains feature + setup | Feature Overview + Setup |
| Walks through a task | How-To Guide |
| Documents multiple items/concepts | Reference Guide |
| Explains behavior (no setup) | Concept Explainer |

**Step B: Apply the matching template from `2.0_Craft_CMS_Formatting_Guidelines.md`**

**Step C: Map existing content to the template structure**

| Template Section | Source Content |
|------------------|----------------|
| [Section from chosen template] | [from Craft/Notion] |
| Troubleshooting | [combine: FAQs + Help Scout insights] |

#### 5.3 Apply These Merge Rules (MANDATORY)

✅ **DO:**
- KEEP all existing Craft content unless factually incorrect
- ADD new sections from Notion that don't exist in Craft
- ENHANCE existing Craft sections by APPENDING Notion details
- RESTRUCTURE to match the chosen article type template
- ADD Troubleshooting section based on Help Scout insights (all article types)
- MAINTAIN all existing images, links, and formatting

❌ **DO NOT:**
- REMOVE existing Craft content (even if Notion doesn't have it)
- SIMPLIFY or SUMMARIZE existing detailed content
- REPLACE Craft sections with shorter Notion versions
- REDUCE the overall word count
- Force a How-To structure on explanatory/conceptual content

#### 5.4 Output the Merge Plan Before Saving

```
MERGE PLAN CONFIRMATION
=======================
Existing Craft article word count: [X]
Expected final word count: [Y] (should be >= X)

KEEPING from Craft:
- [Section 1]: [reason]

ADDING from Notion:
- [New Section]: [what it adds]

📦 CONSOLIDATED SOURCES INCLUDED: [if applicable]
- Source: [Child Article Name] - Adding to: [sections]

ENHANCING with Notion details:
- [Section]: [what details being added]

DELETIONS: NONE (confirm no content is being removed)
```

#### 5.5 Execute the Merge

**Step A:** Create the draft
**Step B:** Re-fetch the draft to get NEW section IDs (they change after draft creation)
**Step C:** Update the draft with merged content
**Step D:** Verify - Re-fetch draft to confirm content saved correctly

**Remember:** 
- Replace special characters (→ to ">", smart quotes to regular)
- Do NOT publish - save as draft only

### Step 6: Prepare Output for Notion Final Update

**⚠️ IMPORTANT:** Do NOT update Notion directly. Prepare output for `KB_Merge_Notion_Update_Final.md`.

```markdown
## MERGE OUTPUT (For Notion Final Update)

### Craft Draft Info
- **Craft Draft URL:** [URL with draftId]
- **Entry ID:** [ID]
- **Draft ID:** [ID]

### Merge Summary
- **Original word count:** [X]
- **Final word count:** [Y]
- **Change:** [+XX%]

### Content Lists
**KEPT from Craft:** [list]
**ADDED from Notion:** [list]
**ENHANCED:** [list]

### Visual Asset Decision
- **Decision:** [Images suggested / No images needed]
- **Reasoning:** [2-3 sentences]

### Terminology Standardization (if any)
| Craft Term | Notion Term | Reasoning |

### Full Merged Content
[COMPLETE article content - all sections]
```

---

## Output Format

### 📌 Related Article Note (only if found)
If related articles were found beyond the target, document and recommend action.

### Terminology Standardization
| Craft Term (Used) | Notion Term (Original) | Reasoning |

### Source Comparison
- Craft article sections: [list]
- Notion draft sections: [list]
- Consolidated sources: [list or "None"]
- Word counts and merge approach

### 📦 Consolidated Content (if applicable)
Document all consolidated sources processed and where content was integrated.

### Validation Results
- [ ] Help Scout tickets reviewed: [count]
- [ ] Key insights found: [list]
- [ ] Codebase validation: [pass/issues found]
- [ ] Fathom calls reviewed: [count]

### Article Type & Structure Applied
- **Article Type:** [Troubleshooting / Feature Overview / How-To / Reference / Concept Explainer]
- **Template Used:** [Template A/B/C/D/E from formatting guidelines]
- **Sections Created:** [list sections from the chosen template]
- [ ] Troubleshooting section included

### Visual Asset Decision
- **Decision:** [Images suggested / No images needed]
- **Reasoning:** [explain]

### Craft CMS Merge Summary
- Article updated: [URL]
- Status: Saved as Draft
- **Original word count:** [X]
- **Final word count:** [Y]
- Content KEPT/ADDED/ENHANCED/REMOVED lists

### Notion Update
- **Status:** Pending - Run `KB_Merge_Notion_Update_Final.md` after validation

---

## ⚠️ MANDATORY: Final Output Checklist

Before completing this workflow, verify ALL of these:

- [ ] Article type classified and template applied
- [ ] Craft draft created and saved (NOT published)
- [ ] Craft Draft URL and Draft ID documented
- [ ] Merge Summary prepared (word counts, content lists)
- [ ] All sections from chosen template present
- [ ] Troubleshooting section included
- [ ] Full Merged Content output for Notion
- [ ] Source Comparison documented
- [ ] Validation Results documented

**Next Step:** Run `KB_Merge_Content_Validation_Check_Final.md` then `KB_Merge_Notion_Update_Final.md`
```

---

## Important Notes

- **MERGE means ENHANCE, not REPLACE** - Existing Craft article is the base
- **Follow the required article structure** - Summary, Quick Start, How It Works, Setup, Prerequisites, Troubleshooting
- If existing Craft content is more detailed than Notion, KEEP the Craft version
- Final article should ALWAYS be >= the length of the original
- Do NOT publish - save as draft only
- Do NOT edit the original Notion draft
- Do NOT create local files - all content goes to Craft draft
- Image suggestions ONLY if crucial (max 3)
- **If in doubt, KEEP existing content**

---

## Troubleshooting

### If the merge results in LESS content than the original:
- STOP and review - something went wrong
- Revert to the previous Craft revision and try again

### If Notion content conflicts with Craft content:
- Flag the conflict for manual review
- Do NOT automatically choose one over the other

### Terminology Mismatch Between Craft and Notion
- **Default:** Use Craft's terminology (published, authoritative source)
- **If Notion term seems more accurate:** Flag for Kyla's review
- **Document all terminology decisions**

### Consolidated Articles - Common Scenarios

**Scenario 1: "Archived (Consolidated)" page**
- STOP - do not process
- Find and process the parent article instead

**Scenario 2: Parent page has "📦 Consolidated Source Content"**
- Treat consolidated content as equally important source material
- Document each consolidated source in merge plan

**Scenario 3: Two Notion pages point to same Craft URL**
- Check Status fields - one should be archived, one active
- Only process the active parent

### New articleSections Entries Not Saving

**Problem:** New sections without existing `id` may silently fail to save.

**Solution - Two-Pass Approach:**
1. First mutation: Update all EXISTING sections
2. Second mutation: Re-fetch, then save with NEW sections added

**Verification:** ALWAYS re-fetch after saving to confirm all sections created.

---

## Example: Well-Structured KB Article

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

<h2>Step-by-Step Setup</h2>
<h3>Step 1: Access Option Mappings</h3>
<p>Go to <strong>Admin Console > Products > Option Mappings</strong></p>

<h2>Before You Begin</h2>
<p>Option Mapping requires your product options to be configured first.</p>

<h2>Troubleshooting</h2>
<h3>"I don't see Option Mappings in my menu"</h3>
<p>Make sure you're logged in as an Org Admin or Super Admin.</p>
```
