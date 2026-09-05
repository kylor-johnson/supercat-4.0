# KB Net-New Notion Final Update

**Purpose:** Standardize the Notion page structure after a Net-New KB article creation and validation are complete. This is the FINAL step that organizes all content into the correct Toggle Heading 1 format.

**When to Run:** After completing both:
1. `KB_Net_New_Article_Prompt_Final.md`
2. `KB_Merge_Content_Validation_Check_Final.md`

**Integration Reference:** See `KB_Integration_References_Final.md` for Notion API query templates.

---

## ⚠️ Notion API Reference

### Valid Status Values

The Notion database only accepts these exact status values:

| Status Value | When to Use |
|--------------|-------------|
| `Not started` | New backlog item |
| `On Hold` | Paused work |
| `In progress` | Currently being worked |
| `Archived (Consolidated)` | Content merged elsewhere |
| `Ready for Craft (Kyla Check)` | Draft ready for Kyla review |
| `Live in Craft - Kylor Push` | **Use this for completed Net-New workflow** |

**For Net-New workflow completion, set Status to:** `Live in Craft - Kylor Push`

### Extracting Page ID from URL

```
https://www.notion.so/svcapital/Page-Title-1c3231dbcd708074bb9cce4d98f3dd51?v=xxx
                                          └────────────── Page ID ──────────────┘

Use the 32-character hex string (with or without dashes) as the page_id parameter.
```

### Toggle Headings Limitation

**Note:** The Notion MCP tool uses markdown replacement, not the native block API. When using `replace_content`, H1 headings (`# Title`) are created as standard headings, not toggleable headings. The visual structure and content organization is preserved, but sections won't be collapsible in the Notion UI. If collapsible toggles are required, manually convert them in the Notion interface after the update.

---

## Required Notion Page Structure

All Net-New KB pages MUST have these 4 Toggle Heading 1 sections **in this exact order**:

```
▶ New Craft Article - [DATE]
▶ Full Article Content (Validated)
▶ VALIDATION REPORT - [DATE]
▶ Original Notion Draft
```

### Visual Reference

```
┌─────────────────────────────────────────────────────────────┐
│ Sales Quota Functionality                                    │
├─────────────────────────────────────────────────────────────┤
│ Category: How To                                            │
│ Status: Live in Craft - Kylor Push                          │
│ Action Type: Net-New                                        │
│ URL: supercatsolutions.com/kno...quotas                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ▶ New Craft Article - 2026-01-26                           │
│                                                             │
│ ▶ Full Article Content (Validated)                         │
│                                                             │
│ ▶ VALIDATION REPORT - 2026-01-26                           │
│                                                             │
│ ▶ Original Notion Draft                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Section 1: New Craft Article - [DATE]

**Toggle Heading 1 Title:** `New Craft Article - YYYY-MM-DD`

**Contains:**
```markdown
**Craft Entry URL:** [admin URL]
**Entry ID:** [ID]
**Slug:** [slug]
**Status:** Draft (Disabled)

---

## Article Summary

| Metric | Value |
|--------|-------|
| Title | [Article Title] |
| Article Type | [Troubleshooting / Feature Overview / How-To / Reference / Concept Explainer] |
| Template Used | [Template A/B/C/D/E/F] |
| Word count | ~XXX |
| Sections created | [list sections from template] |

---

## Content Sources
- **Primary:** Notion draft
- **Validation:** Help Scout ([X] tickets), Fathom ([X] calls), Codebase

## Related Articles Found
- [Article 1] - [relationship/cross-link candidate]
- [Article 2] - [relationship]

(Or: "No related articles found.")

---

## Action for Kyla
⚠️ [Any manual steps required before publishing]
```

---

## Section 2: Full Article Content (Validated)

**Toggle Heading 1 Title:** `Full Article Content (Validated)`

**Contains:** The COMPLETE article content exactly as it appears in the Craft entry.

```markdown
📄 This is the authoritative record of the new article created in Craft.

---

[Full article content with all sections from the chosen template]

Example for Feature Overview + Setup (Template B):
### Summary
[Full summary content]

### Overview
[What is this feature]

### How It Works
[Conceptual explanation]

### Prerequisites
[Requirements]

### How to Set Up
[Step-by-step setup]

### Troubleshooting
[All troubleshooting items]

Example for Concept Explainer (Template F):
### Overview
[Brief explanation]

### Key Behavior
[Core concepts and rules]

### Example Explanation
[How to explain to customers]

### Troubleshooting
[Common questions/misconceptions]

---
--- END OF ARTICLE CONTENT ---
```

**Critical:** This must be the COMPLETE article text, not a summary or "see Craft entry" link.

---

## Section 3: VALIDATION REPORT - [DATE]

**Toggle Heading 1 Title:** `VALIDATION REPORT - YYYY-MM-DD`

**Contains:**
```markdown
**Craft Entry URL:** [URL]
**Overall Confidence:** XX%
**Recommendation:** ✅ PUBLISH / ⚠️ PUBLISH WITH REVIEW / ❌ REVISE REQUIRED

---

## Validation Summary

| # | Claim/Section | Source | Status | Notes |
|---|---------------|--------|--------|-------|
| 1 | [Claim] | [Source] | ✅ Verified | |
| 2 | [Claim] | [Source] | ✅ Verified | |
| 3 | [Claim] | [Source] | ⚠️ 85% | [reason] |

---

## Corrections Applied
[List or "None required - draft content was accurate."]

---

## Flagged for Manual (Screenshots)
[List or "No new screenshots needed."]

---

## Action for Kyla
⚠️ [Any manual steps, e.g., add images, verify navigation paths]
```

---

## Section 4: Original Notion Draft

**Toggle Heading 1 Title:** `Original Notion Draft`

**Contains:** The original Notion draft content BEFORE the Net-New workflow ran. This is preserved unchanged for:
- Audit trail
- Future reference
- Comparing original draft vs final article

**Rule:** NEVER delete or modify this section.

---

## Prompt

```
You are finalizing a Net-New KB article's Notion page after the creation and validation workflows have completed.

**Notion Page URL:** [PASTE NOTION URL]

**Integration Reference:** READ `KB Creation prompts/KB_Integration_References_Final.md` for Notion API templates.

---

## Your Task

### Step 1: Identify Existing Content

Fetch the Notion page and identify:
1. What content currently exists on the page
2. What the original draft content is (to preserve as "Original Notion Draft")
3. Whether any previous workflow outputs exist (from previous runs)

### Step 2: Gather Required Content

You need these 4 pieces of content:

| Section | Source |
|---------|--------|
| New Craft Article | From KB_Net_New output (Craft URLs, entry info, article summary) |
| Full Article Content | From Craft entry (complete article HTML/text) |
| Validation Report | From KB_Validation output (confidence, claims table) |
| Original Draft | Already on Notion page (preserve as-is) |

### Step 3: Restructure the Page

Using the Notion API, restructure the page to have exactly 4 Toggle Heading 1 sections in this order:

1. **New Craft Article - [TODAY'S DATE]**
2. **Full Article Content (Validated)**
3. **VALIDATION REPORT - [TODAY'S DATE]**
4. **Original Notion Draft**

### Step 4: Create Toggle Heading 1 Blocks

Use this Notion API structure for toggle headings:

```javascript
{
  object: 'block',
  type: 'heading_1',
  heading_1: {
    rich_text: [{ type: 'text', text: { content: 'Section Title' } }],
    is_toggleable: true  // This makes it a toggle!
  }
}
```

Then add child blocks under each toggle.

### Step 5: Populate Each Section

**Section 1 (New Craft Article):** Add as children:
- Paragraph with Craft URLs and IDs
- Divider
- Heading 2: "Article Summary"
- Table with title, article type, template, word count, sections
- Heading 2: "Content Sources"
- Bullet list of sources used
- Heading 2: "Related Articles Found" (if any)
- Callout with action items for Kyla

**Section 2 (Full Article Content):** Add as children:
- Callout: "This is the authoritative record..."
- Divider
- Full article content (all sections from the chosen template)
- Paragraph: "--- END OF ARTICLE CONTENT ---"

**Section 3 (Validation Report):** Add as children:
- Paragraphs with Craft URL, confidence, recommendation
- Divider
- Heading 2: "Validation Summary"
- Table with all validated claims
- Heading 2: "Corrections Applied"
- Content or "None required"
- Heading 2: "Flagged for Manual"
- Content or "No screenshots needed"
- Callout with action items

**Section 4 (Original Notion Draft):** 
- If original content exists as a toggle, rename it to "Original Notion Draft"
- If original content is loose blocks, wrap in a new toggle
- Preserve ALL original content unchanged

### Step 6: Update Page Properties

Update the Notion page properties:
- Status: `Live in Craft - Kylor Push`
- URL: [Craft article URL once published]

### Step 7: Verify Structure

Re-fetch the page and confirm:
- [ ] Exactly 4 Toggle Heading 1 sections exist
- [ ] Sections are in correct order
- [ ] All content is inside toggles (not loose on page)
- [ ] Original draft content is preserved

---

## Output

Provide confirmation:

```markdown
## ✅ Notion Page Restructured

**Page:** [Title]
**URL:** [URL]

### Structure Verified
- [x] Toggle 1: New Craft Article - [DATE]
- [x] Toggle 2: Full Article Content (Validated)
- [x] Toggle 3: VALIDATION REPORT - [DATE]
- [x] Toggle 4: Original Notion Draft

### Article Info
- **Article Type:** [type]
- **Template:** [template]
- **Craft Entry ID:** [ID]

### Status Updated
- Status: [New status]

### Ready for Kyla
- [Any action items listed]
```
```

---

## Troubleshooting

### Toggle Not Collapsible
**Problem:** Created heading_1 but it's not toggleable
**Fix:** Ensure `is_toggleable: true` is set in the heading_1 object

### Content Outside Toggles
**Problem:** Some content is loose on the page, not inside toggles
**Fix:** Create a toggle and move/copy content as children

### Wrong Order
**Problem:** Sections are in wrong order
**Fix:** Notion appends to end. Create blocks in the order you want them, or delete and recreate.

### Original Content Lost
**Problem:** Original draft content was overwritten
**Prevention:** ALWAYS identify and preserve original content BEFORE making changes
**Recovery:** Check Notion page history (if available)

---

## Differences from Merge Notion Update

| Aspect | Merge | Net-New |
|--------|-------|---------|
| Toggle 1 Title | "Updated Craft Article" | "New Craft Article" |
| Toggle 1 Content | Merge summary (kept/added/enhanced) | Creation summary (sources, article type) |
| Toggle 2 Title | "Full Merged Content" | "Full Article Content" |
| Toggle 4 Title | Variable (Kyla Original Draft, etc.) | "Original Notion Draft" |
| Word count comparison | Yes (original vs final) | No (new article) |
