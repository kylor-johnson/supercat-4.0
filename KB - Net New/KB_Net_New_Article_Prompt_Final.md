# KB Net-New Article Creation Prompt

**Purpose:** Process Notion KB backlog articles tagged as `Action Type = Net-New` by validating content, enhancing with additional context, and creating a brand new Craft CMS Knowledge Base article.

**Key Difference from Merge:** There is NO existing Craft article. The Notion draft is the primary source, enhanced with Help Scout, Fathom, and codebase validation.

**Integration Reference:** See `KB_Integration_References_Final.md` for all BigQuery, Notion, and Craft CMS query templates.

### BigQuery MCP Query Tips

The BigQuery MCP tool can be sensitive to query complexity. For best results:

- **Keep queries simple:** Avoid complex WHERE clauses with many OR conditions in a single query
- **Break up searches:** Run multiple simpler queries rather than one complex query
- **If a query fails:** Simplify it (e.g., search for one keyword at a time instead of multiple)
- **Backtick-quoted table names work:** `hevo_dataset_supercat_data_pipeline_Slhk.conversation`

---

## ⚠️ TWO-PHASE WORKFLOW (Required for Automation)

**Why Two Phases?** The Craft CMS GraphQL API has a limitation: it cannot reliably CREATE new Matrix field entries (articleSections). However, it CAN reliably UPDATE existing sections. Therefore, this workflow pauses after analysis so Kyla can create a template entry with the correct number of sections.

### Phase 1: Analysis & Template Requirements
- Steps 1-6: Validate content, classify article type, prepare HTML content
- **PAUSE** at Step 7: Output template requirements for Kyla
- Kyla creates the template entry in Craft with blank sections

### Phase 2: Content Population (After Kyla Provides Entry ID)
- Step 8: Create draft from template entry
- Step 9: Query draft for section IDs
- Step 10: Populate sections with content via GraphQL
- Step 11: Verify and output results

**The workflow MUST pause between phases.** Do not attempt to create article sections via GraphQL without an existing template entry.

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

**Always validate your understanding of the feature's PURPOSE with Help Scout tickets, Fathom calls, or similar features before writing the Summary.**

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

## ⛔ CRITICAL: ANTI-HALLUCINATION RULES

**You have close to zero product knowledge. You MUST validate everything against sources.**

```
⛔ FORBIDDEN: Approving ANY technical claim without source verification
⛔ FORBIDDEN: Assuming field names are correct without codebase check
⛔ FORBIDDEN: Trusting error message text without Help Scout validation
⛔ FORBIDDEN: Approving procedures without verifying against support patterns
⛔ FORBIDDEN: Making up features, settings, or behaviors not found in sources
```

### Validation Hierarchy (Sources of Truth)

| Priority | Source | What It Validates | Authority Level |
|----------|--------|-------------------|-----------------|
| 0 | **User Understanding** | Feature purpose, user benefit, plain language framing | 🟣 FOUNDATIONAL |
| 1 | **Codebase** | Field names, feature behavior, API structure | 🔴 ABSOLUTE (override all others) |
| 2 | **MCP Live Data** | Current system state, configuration options | 🟠 HIGH |
| 3 | **Help Scout Tickets** | Error messages, troubleshooting steps, edge cases | 🟡 MEDIUM-HIGH |
| 4 | **Fathom Calls** | How features are explained, common questions | 🟡 MEDIUM |
| 5 | **Existing KB Articles** | Consistency with published content | 🟢 REFERENCE ONLY |

**Rule:** If sources conflict, higher priority wins. Always flag conflicts.

---

## Prompt

```
You are helping me create a brand new KB article from a Notion draft. This is a NET-NEW article - there is NO existing Craft article to merge with.

**FORMATTING:** Before generating any HTML content, READ the file `prompts/2.0_Craft_CMS_Formatting_Guidelines.md` and apply all rules.

**INTEGRATION REFERENCE:** READ `KB Creation prompts/KB_Integration_References_Final.md` for all query templates (BigQuery, Notion, Craft CMS).

**ARTICLE STRUCTURE:** 
1. READ `2.0_Craft_CMS_Formatting_Guidelines.md` - "Article Type Classification" section
2. Classify this article's type based on its primary purpose
3. Apply the matching template structure from the guidelines
4. All articles should end with a Troubleshooting section (combines FAQs, common mistakes)

## Article Information

**Notion Draft Article:** [PASTE NOTION URL]

---

## Your Task

### Step 1: Review the Notion Draft

1. Fetch the Notion page content using the Notion Direct API

2. **Verify Action Type:** Confirm the page has `Action Type = Net-New`
   - If it's `Merge`, STOP and use `KB_Merge_Article_Prompt_Final.md` instead
   - If it's `Archived (Consolidated)`, STOP - content lives elsewhere

3. **Extract the draft content:**
   - If the page has a "### Prepared Draft - [DATE]" section, use ONLY that as source
   - Otherwise, use the full page content

4. **Document what exists in the draft:**
   - List all sections/topics covered
   - Identify the feature(s) being documented
   - Note any gaps or areas that seem incomplete
   - Flag any technical claims that need verification

### Step 2: Validate Feature Purpose (REQUIRED Before Writing Summary)

**⚠️ CRITICAL:** Before writing the Summary, validate the feature's PURPOSE from the user's perspective.

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
- [ ] Similar existing KB articles: How are related features framed?

**Red Flags - Rewrite if the draft Summary:**
- Describes mechanism but not benefit
- Uses jargon without context
- Would make a non-technical user ask "so what?"

**Jargon Patterns to Fix:**

| Phrase Pattern | Issue | Fix |
|----------------|-------|-----|
| "before going into production" | Manufacturing jargon | "when they're not ready to order yet" |
| "automatically sent to [system]" | Technical mechanism | "saved for follow-up" |
| "for analysis purposes" | Vague | "so you can track who's interested" |
| "enables [technical process]" | Developer language | "lets you [user action]" |

### Step 3: Validate & Enhance with Context

**3A. Query Help Scout Tickets (BigQuery)**

Search for related tickets to validate accuracy and find additional context. Use queries from Integration Reference.

**What types of claims need validation:**

| Claim Type | Validation Source |
|------------|-------------------|
| Field Names | Codebase (exact casing required) |
| Error Messages | Help Scout + Codebase |
| Navigation Paths | Codebase + MCP |
| Feature Behavior | Codebase |
| Numeric Limits | Codebase |
| Procedures | Help Scout + Fathom |

Look for in Help Scout threads:
- Common user questions/confusion points
- Solutions provided by support team
- Internal notes with valuable context
- Edge cases or exceptions mentioned

**Use these insights to populate the Troubleshooting section.**

**3B. Validate with Codebase**

Search the codebase to verify:
- Feature behavior matches the draft
- Field names use exact casing
- Settings/configuration options are accurate
- Any technical details are correct

**3C. Query Fathom Call Summaries (BigQuery)**

Search for relevant customer calls. Look for:
- Customer training/onboarding discussions
- Feedback, confusion, or feature requests
- Real-world use cases mentioned

**3D. Check for Related KB Articles**

Search Craft for existing articles on similar topics:

```graphql
{
  entries(section: "knowledgeBase", search: "[TOPIC KEYWORDS]", limit: 10) {
    title
    slug
  }
}
```

If related articles exist:
- Note them for cross-linking
- Check for terminology consistency
- Avoid duplicating content that already exists elsewhere

**3E. MCP Live Data Validation (if applicable)**

Verify features exist in system:
- `get_organization_info` → Check features are enabled/available
- `get_data_summary` → Check data types exist
- `get_options` → Verify options exist as described

### Step 4: Document Validation Findings

Create a validation summary:

```markdown
## Validation Findings

### Claims Verified
| Claim | Source | Evidence | Status |
|-------|--------|----------|--------|
| [claim] | Codebase | [file/line] | ✅ Verified |
| [claim] | Help Scout | Ticket #XXX | ✅ Verified |

### Corrections Needed
| Original Draft Says | Should Be | Source |
|---------------------|-----------|--------|
| [incorrect] | [correct] | [source] |

### Content to Add (from validation)
- Troubleshooting item: [from Help Scout]
- Edge case: [from tickets]
- Real-world example: [from Fathom]

### Gaps Identified
- [Missing topic/section]
- [Incomplete explanation]
```

### Step 5: Classify Article Type and Structure Content

**Step A: Classify the article type**

| If the content... | Article Type | Template |
|-------------------|--------------|----------|
| Fixes an error/problem | Troubleshooting Guide | Template A |
| Explains feature + setup | Feature Overview + Setup | Template B |
| Walks through a task | How-To Guide | Template C/D |
| Documents multiple items/concepts | Reference Guide | Template E |
| Explains behavior (no setup) | Concept Explainer | See guidelines |

**Step B: Apply the matching template from `2.0_Craft_CMS_Formatting_Guidelines.md`**

**Step C: Map draft content to the template structure**

| Template Section | Draft Content Source | Notes |
|------------------|---------------------|-------|
| [Section from chosen template] | [draft content] | [adjustments needed] |
| Troubleshooting | [Help Scout insights + draft FAQs] | Required for all types |

**If sections are missing from the draft:**
- Build from Help Scout tickets and Fathom call insights
- Use codebase understanding to fill gaps
- Flag significant gaps in output for Kyla to review

### Step 6: Visual Asset Recommendations (Only If Crucial)

**Philosophy: Minimize visual assets. Only suggest images/videos if CRUCIAL to understanding.**

Before recommending ANY visual, ask:
1. Is this concept impossible to understand from text alone?
2. Would an experienced admin user really need a screenshot for this?
3. Does a similar article already have images you could reference?

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

### Step 7: PHASE 1 COMPLETE - Output Template Requirements (⏸️ PAUSE HERE)

**⚠️ CRITICAL: Do NOT attempt to create article sections via GraphQL directly. The API cannot reliably create new Matrix entries.**

At this point, you have:
- ✅ Validated the Notion draft content
- ✅ Verified claims against codebase/Help Scout/Fathom
- ✅ Classified the article type
- ✅ Prepared HTML content for each section

**Now output the template requirements and STOP:**

```markdown
---
## ⏸️ PHASE 1 COMPLETE - ACTION REQUIRED

### Template Entry Requirements

**Article Title:** [Title]
**Suggested Slug:** [slug]
**Summary:** [Brief summary for listings]

**This article requires the following sections:**

| # | Section Type | Section Name |
|---|--------------|--------------|
| 1 | text | Summary |
| 2 | text | [Section name based on article type] |
| 3 | text | [Section name] |
| ... | text | ... |
| N | text | Need More Help? |

**Total text sections needed:** [X]

**Note:** Do NOT add a Table of Contents block. The TOC is auto-generated from H2/H3 headings.

### Action Required

Please create a new KB entry in Craft CMS:

1. Go to **Entries > Knowledge Base > + New entry**
2. Set **Title:** [Title]
3. Set **Summary:** [Summary text]
4. Under **Article Sections**, click **+ New entry** and add:
   - [X]x **Text** entries (leave body empty for now)
   - Do NOT add a Table of Contents entry (it's auto-generated)
5. **⚠️ CRITICAL: Save as a CANONICAL ENTRY, not a provisional draft:**
   - Click **Save** (or **Create entry**)
   - If the URL shows `?draftId=XXX`, you need to **Apply the draft** first
   - The URL should be `/entries/knowledgeBase/XXXXX-slug` WITHOUT a `?draftId` parameter
   - You can disable/unpublish the entry after saving (that's fine)
6. Copy the **Entry ID** from the URL (e.g., `/entries/knowledgeBase/42287-slug` → ID is `42287`)

**Why this matters:** GraphQL can only query canonical entries, not provisional drafts. If the entry only exists as a draft, I cannot retrieve the section IDs needed to populate content.

**Reply with the Entry ID to continue to Phase 2.**

---
```

### Validation Results (Phase 1)
[Include all validation findings, article type classification, and prepared HTML content here so it's available for Phase 2]

---

## PHASE 2: Content Population (After Kyla Provides Entry ID)

**Resume here after Kyla provides the Entry ID.**

### Step 8: Create Draft from Template Entry

```graphql
mutation {
  createDraft(
    id: [ENTRY_ID_FROM_KYLA]
    name: "Net-New Content Population"
  )
}
```

This returns a `draftId` (e.g., `1050`).

### Step 9: Query Draft for Section IDs

**⚠️ CRITICAL:** After creating a draft, section IDs CHANGE. You MUST query the draft to get the new IDs.

```graphql
{
  entries(draftId: [DRAFT_ID]) {
    id
    title
    ... on knowledgeBase_knowledgeBase_Entry {
      articleSections {
        __typename
        ... on text_Entry { id }
        ... on tableOfContents_Entry { id }
      }
    }
  }
}
```

**Map the returned IDs to your sections:**

| Section # | Section Name | Section ID |
|-----------|--------------|------------|
| 1 | Summary | [from query] |
| 2 | Overview | [from query] |
| 3 | [Section] | [from query] |
| ... | ... | ... |

### Step 10: Populate Sections with Content

Now update each text section with its HTML content using the IDs from Step 9:

```graphql
mutation {
  save_knowledgeBase_knowledgeBase_Draft(
    draftId: [DRAFT_ID]
    articleSections: {
      entries: [
        { text: { id: "[SECTION_1_ID]", body: "[Summary HTML]" } },
        { text: { id: "[SECTION_2_ID]", body: "[Overview HTML]" } },
        { text: { id: "[SECTION_3_ID]", body: "[Before You Begin HTML]" } },
        { text: { id: "[SECTION_4_ID]", body: "[How-To HTML]" } },
        { text: { id: "[SECTION_5_ID]", body: "[Additional Section HTML]" } },
        { text: { id: "[SECTION_6_ID]", body: "[Troubleshooting HTML]" } },
        { text: { id: "[SECTION_7_ID]", body: "[Need More Help HTML]" } }
      ]
    }
  ) {
    id
    draftId
  }
}
```

**Remember:** 
- Replace special characters (→ to ">", smart quotes to regular)
- Use the EXACT section IDs from Step 9
- Include the `id` field for each text entry

### Step 11: Verify and Prepare Final Output

**11A. Verify the draft content saved:**

```graphql
{
  entries(draftId: [DRAFT_ID]) {
    id
    title
    ... on knowledgeBase_knowledgeBase_Entry {
      articleSections {
        __typename
        ... on text_Entry { id body }
      }
    }
  }
}
```

**11B. Prepare output for Notion Final Update:**

**⚠️ IMPORTANT:** Do NOT update Notion directly. Prepare output for `KB_Net_New_Notion_Update_Final.md`.

```markdown
## NET-NEW OUTPUT (For Notion Final Update)

### Craft Entry Info
- **Craft Entry URL:** [admin URL]
- **Entry ID:** [ID from Kyla's template]
- **Draft ID:** [ID from createDraft mutation]
- **Slug:** [slug]
- **Status:** Draft (content populated, ready for review)

### Article Summary
- **Title:** [title]
- **Word count:** [approx]
- **Sections populated:** [list with section IDs]

### Validation Summary
- **Help Scout tickets reviewed:** [count]
- **Fathom calls reviewed:** [count]
- **Codebase validations:** [count]
- **Corrections applied:** [count]

### Content Added from Validation
- [Item 1 - source]
- [Item 2 - source]

### Visual Asset Decision
- **Decision:** [Images suggested / No images needed]
- **Reasoning:** [2-3 sentences]

### Related Articles Found
- [Article 1] - [relationship]
- [Article 2] - [relationship]

### Full Article Content
[COMPLETE article content - all sections in HTML]
```

---

## Output Format

### Phase 1 Output (Template Requirements)

```markdown
## ⏸️ PHASE 1 COMPLETE - ACTION REQUIRED

### Template Entry Requirements
- **Article Title:** [Title]
- **Suggested Slug:** [slug]
- **Summary:** [Summary text]
- **Text sections needed:** [X]

### Section List
| # | Type | Section Name |
|---|------|--------------|
| 1 | text | Summary |
| 2 | text | Overview |
| ... | text | ... |

**Note:** No TOC block needed - it's auto-generated from headings.

### Validation Results
- [ ] Feature purpose validated against Help Scout/Fathom
- [ ] Field names verified against codebase
- [ ] Help Scout tickets reviewed: [count]
- [ ] Fathom calls reviewed: [count]

### Prepared HTML Content
[Include all HTML sections here for use in Phase 2]

**Reply with the Entry ID to continue.**
```

### Phase 2 Output (Final Results)

```markdown
## ✅ PHASE 2 COMPLETE - Content Populated

### Craft Entry Info
- **Entry URL:** [admin URL]
- **Entry ID:** [ID from Kyla]
- **Draft ID:** [ID from createDraft]
- **Status:** Draft (ready for review)

### Sections Populated
| # | Section Name | Section ID | Status |
|---|--------------|------------|--------|
| 1 | Summary | [id] | ✅ |
| 2 | Overview | [id] | ✅ |
| ... | ... | ... | ... |

### Notion Update
- **Status:** Pending - Run `KB_Net_New_Notion_Update_Final.md`
```

---

## ⚠️ MANDATORY: Checklist by Phase

### Phase 1 Checklist (Before Pausing)
- [ ] Notion draft fetched and Action Type verified
- [ ] Feature purpose validated (user-benefit focused)
- [ ] All technical claims verified against codebase
- [ ] Article type classified and template selected
- [ ] HTML content prepared for all sections
- [ ] Template requirements output with section count
- [ ] PAUSED and waiting for Entry ID from Kyla

### Phase 2 Checklist (After Receiving Entry ID)
- [ ] Draft created from template entry
- [ ] Section IDs queried from draft
- [ ] All sections populated with content
- [ ] Content verified via query
- [ ] Final output prepared for Notion update

**Next Step:** Run `KB_Merge_Content_Validation_Check_Final.md` then `KB_Net_New_Notion_Update_Final.md`
```

---

## Important Notes

- **Net-New = Build from scratch** - The Notion draft is your primary source
- **Two-Phase Workflow Required** - MUST pause after Phase 1 for Kyla to create template entry
- **Template entry MUST be canonical** - Save as entry (not provisional draft) so GraphQL can query section IDs
- **Validate everything** - You have no product knowledge; verify all claims
- **Follow the required article structure** - Sections vary by article type (see templates)
- **Do NOT publish to live site** - Entry can be disabled/unpublished, but must exist as canonical entry
- **Do NOT edit the original Notion draft** - Keep it pristine for auditing
- **Do NOT create local files** - All content goes to Craft
- **Do NOT skip the pause** - GraphQL cannot reliably create new Matrix entries
- **Image suggestions ONLY if crucial** (max 3)

---

## Troubleshooting

### GraphQL returns success but sections are empty
**This is a known limitation.** The Craft CMS GraphQL API cannot reliably CREATE new Matrix field entries (articleSections). Mutations appear to succeed but content doesn't persist.

**Solution:** Follow the two-phase workflow:
1. Phase 1: Prepare content, output template requirements, PAUSE
2. Kyla creates template entry with blank sections in Craft admin
3. Phase 2: Create draft, query section IDs, UPDATE existing sections

**Never attempt to create articleSections directly via GraphQL for net-new entries.**

### Can't query the entry or section IDs

**Most common cause:** The entry exists only as a provisional draft, not a canonical entry.

**How to check:** Look at the Craft admin URL:
- ❌ `?draftId=1060` in URL → It's a provisional draft (not queryable)
- ✅ No `?draftId` parameter → It's a canonical entry (queryable)

**How to fix:**
1. In Craft admin, click **Apply draft** or find the revision menu
2. This converts the draft into a canonical entry
3. The entry can be disabled/unpublished (that's fine for querying)
4. Then query will work: `entries(id: ["XXXXX"], status: ["live", "disabled"])`

**Alternative query formats:**
```graphql
# By ID with status filter
{ entries(id: ["42287"], status: ["live", "disabled"]) { ... } }

# By slug
{ entries(section: "knowledgeBase", slug: "article-slug", status: ["live", "disabled"]) { ... } }
```

### Draft content is incomplete or vague
- Use Help Scout tickets to understand real user questions
- Use Fathom calls to understand how the feature is explained
- Search codebase for feature documentation
- Flag gaps in your output for Kyla to review

### Can't verify a claim in the draft
- Do NOT include unverified claims in the final article
- Flag the claim in your output: "⚠️ UNVERIFIED: [claim] - could not find source"
- Kyla will verify manually or remove

### Feature doesn't seem to exist
- Double-check search terms (try variations)
- Check if it's an upcoming/beta feature
- Flag for Kyla: "⚠️ FEATURE NOT FOUND: [feature name] - may be deprecated or renamed"

### Similar article already exists
- If the existing article covers the SAME topic: Flag for Kyla - may be a duplicate
- If the existing article covers a RELATED topic: Note for cross-linking, proceed with new article

### Draft has conflicting information
- Use the Validation Hierarchy to resolve conflicts
- Codebase always wins for technical details
- Flag significant conflicts for Kyla's review

### Section count mismatch
If Kyla created a template with a different number of sections than required:
- **Too few sections:** Ask Kyla to add more blank text entries
- **Too many sections:** Extra sections can be deleted in Craft admin after content is populated, or leave them empty (they won't display if body is blank)

---

## Example: Net-New Article Two-Phase Workflow

### Phase 1 Output Example

```markdown
---
## ⏸️ PHASE 1 COMPLETE - ACTION REQUIRED

### Template Entry Requirements

**Article Title:** Sales Quota Setup
**Suggested Slug:** sales-quota-setup
**Summary:** Set revenue targets for each territory and track performance against goals in your dashboard.

**This article requires the following sections:**

| # | Section Type | Section Name |
|---|--------------|--------------|
| 1 | text | Summary |
| 2 | text | Overview |
| 3 | text | Before You Begin |
| 4 | text | How to Set Up Sales Quotas |
| 5 | text | Viewing Quota Reports |
| 6 | text | Troubleshooting |
| 7 | text | Need More Help? |

**Total text sections needed:** 7

**Note:** No TOC block needed - it's auto-generated from H2/H3 headings.

### Action Required

Please create a new KB entry in Craft CMS:
1. Go to **Entries > Knowledge Base > + New entry**
2. Set **Title:** Sales Quota Setup
3. Set **Summary:** Set revenue targets for each territory and track performance against goals in your dashboard.
4. Under **Article Sections**, click **+ New entry** and add:
   - 7x **Text** entries (leave body empty for now)
   - Do NOT add a Table of Contents entry
5. **Save as canonical entry** (click Save/Create entry, NOT "Save as draft")
   - If URL shows `?draftId=XXX`, click **Apply draft** first
   - URL should be `/entries/knowledgeBase/42287-sales-quota-setup` (no draftId)
6. Copy the **Entry ID** from the URL (42287 in this example)

**Reply with the Entry ID to continue to Phase 2.**
---

### Prepared HTML Content

<h2>Summary</h2>
<p>Sales Quotas let you set revenue targets for each territory...</p>

[... rest of HTML sections ...]
```

### Phase 2 (After Kyla replies with Entry ID: 42500)

**Step 8:** Create draft → `draftId: 1055`

**Step 9:** Query section IDs:
| # | Section Name | Section ID |
|---|--------------|------------|
| 1 | Summary | 42501 |
| 2 | Overview | 42502 |
| 3 | Before You Begin | 42503 |
| 4 | How to Set Up | 42504 |
| 5 | Viewing Reports | 42505 |
| 6 | Troubleshooting | 42506 |
| 7 | Need More Help | 42507 |

**Step 10:** Populate sections using IDs above

**Step 11:** Verify and output final results
