# KB Notion Final Update

**Purpose:** Standardize the Notion page structure after KB merge and validation are complete. This is the FINAL step that organizes all content into the correct Toggle Heading 1 format.

**When to Run:** After completing both:
1. `KB_Merge_Article_Validation_Prompt_Revised_Article_Structure.md`
2. `KB_Content_Validation_Final_Check.md`

**Version:** 1.0  
**Created:** January 19, 2026

---

## Required Notion Page Structure

All KB pages MUST have these 4 Toggle Heading 1 sections **in this exact order**:

```
▶ Updated Craft Article - [DATE]
▶ Full Merged Content (Validated)
▶ VALIDATION REPORT - [DATE]
▶ [Original Content Name] (preserved for audit trail)
```

### Visual Reference

```
┌─────────────────────────────────────────────────────────────┐
│ Enable Ordering for Customer Users (eCat Online)            │
├─────────────────────────────────────────────────────────────┤
│ Category: Trouble Shooting                                  │
│ Status: Live in Craft - Kylor Push                         │
│ Action Type: Merge                                          │
│ URL: supercatsolutions.com/kno...g-cart                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ▶ Updated Craft Article - 2026-01-19                       │
│                                                             │
│ ▶ Full Merged Content (Validated)                          │
│                                                             │
│ ▶ VALIDATION REPORT - 2026-01-19                           │
│                                                             │
│ ▶ Kyla Original Draft                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Section 1: Updated Craft Article - [DATE]

**Toggle Heading 1 Title:** `Updated Craft Article - YYYY-MM-DD`

**Contains:**
```markdown
**Craft Draft URL:** [URL with draftId]
**Entry ID:** [ID]
**Draft ID:** [ID]

---

## Merge Summary

| Metric | Value |
|--------|-------|
| Original Craft word count | ~XXX |
| Final word count | ~XXX |
| Change | +XX% ✅ |

---

## Content KEPT from Craft
- [Item 1]
- [Item 2]
- [Existing images]

## Content ADDED from Notion
- [New section 1]
- [New section 2]
- [Troubleshooting items]

## Content ENHANCED
- [Section]: [what was added]

---

## Action for Kyla
⚠️ [Any manual steps required before publishing]
```

---

## Section 2: Full Merged Content (Validated)

**Toggle Heading 1 Title:** `Full Merged Content (Validated)`

**Contains:** The COMPLETE article content exactly as it appears in the Craft draft.

```markdown
📄 This is the authoritative record of what was merged into the Craft draft.

---

### Summary
[Full summary content]

### Quick Start
[Full quick start content with numbered steps]

### How It Works
[Full how it works content]

### Before You Begin
[Full prerequisites]

### Step-by-Step Setup
[Full setup steps]

### Troubleshooting
[All troubleshooting items]

### Need More Help?
[Contact support section]

---
--- END OF MERGED CONTENT ---
```

**Critical:** This must be the COMPLETE article text, not a summary or "see Craft draft" link.

---

## Section 3: VALIDATION REPORT - [DATE]

**Toggle Heading 1 Title:** `VALIDATION REPORT - YYYY-MM-DD`

**Contains:**
```markdown
**Craft Draft URL:** [URL]
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

## Auto-Applied Corrections
[List or "None required - draft content is accurate."]

---

## Flagged for Manual (Screenshots)
[List or "No new screenshots needed."]

---

## Action for Kyla
⚠️ [Any manual steps, e.g., split body sections]
```

---

## Section 4: Original Content (Audit Trail)

**Toggle Heading 1 Title:** Use a descriptive name based on what was there:
- `Kyla Original Draft` (if Kyla created it)
- `V2` or `V3` (if versioned)
- `Original Notion Draft` (generic)

**Contains:** Whatever content was originally in the Notion page BEFORE the merge workflow ran. This is preserved unchanged for:
- Audit trail
- Future reference
- Comparing original vs final

**Rule:** NEVER delete or modify this section. Only rename the toggle title if needed for clarity.

---

## Prompt

```
You are finalizing a KB article's Notion page after the merge and validation workflows have completed.

**Notion Page URL:** [PASTE NOTION URL]

---

## Your Task

### Step 1: Identify Existing Content

Fetch the Notion page and identify:
1. What content currently exists on the page
2. What the original draft content is (to preserve as "Original Draft")
3. Whether merge summary and validation report already exist (from previous runs)

### Step 2: Gather Required Content

You need these 4 pieces of content:

| Section | Source |
|---------|--------|
| Updated Craft Article | From KB_Merge output (Craft URLs, word counts, content lists) |
| Full Merged Content | From Craft draft (complete article HTML/text) |
| Validation Report | From KB_Validation output (confidence, claims table) |
| Original Content | Already on Notion page (preserve as-is) |

### Step 3: Restructure the Page

Using the Notion API, restructure the page to have exactly 4 Toggle Heading 1 sections in this order:

1. **Updated Craft Article - [TODAY'S DATE]**
2. **Full Merged Content (Validated)**
3. **VALIDATION REPORT - [TODAY'S DATE]**
4. **[Original Content Name]**

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

Then add child blocks under each toggle:

```javascript
// After creating the toggle heading, add children to it
await notionRequest('/blocks/[TOGGLE_BLOCK_ID]/children', 'PATCH', {
  children: [
    // Child blocks go here
  ]
});
```

### Step 5: Populate Each Section

**Section 1 (Updated Craft Article):** Add as children:
- Paragraph with Craft URLs and IDs
- Divider
- Heading 2: "Merge Summary"
- Table or bullet points with word counts
- Heading 3: "Content KEPT from Craft"
- Bullet list
- Heading 3: "Content ADDED from Notion"
- Bullet list
- Callout with action items for Kyla

**Section 2 (Full Merged Content):** Add as children:
- Callout: "This is the authoritative record..."
- Divider
- Full article content (all H2/H3 sections, lists, etc.)
- Paragraph: "--- END OF MERGED CONTENT ---"

**Section 3 (Validation Report):** Add as children:
- Paragraphs with Craft URL, confidence, recommendation
- Divider
- Heading 2: "Validation Summary"
- Numbered list or table with all validated claims
- Heading 2: "Auto-Applied Corrections"
- Content or "None required"
- Heading 2: "Flagged for Manual"
- Content or "No screenshots needed"
- Callout with action items

**Section 4 (Original Content):** 
- If original content exists as a toggle, rename it
- If original content is loose blocks, wrap in a new toggle
- Preserve ALL original content unchanged

### Step 6: Update Page Status

Update the Notion page properties:
- Status: "Live in Craft - Kylor Push" (or appropriate status)

### Step 7: Verify Structure

Re-fetch the page and confirm:
- [ ] Exactly 4 Toggle Heading 1 sections exist
- [ ] Sections are in correct order
- [ ] All content is inside toggles (not loose on page)
- [ ] Original content is preserved

---

## Output

Provide confirmation:

```markdown
## ✅ Notion Page Restructured

**Page:** [Title]
**URL:** [URL]

### Structure Verified
- [x] Toggle 1: Updated Craft Article - [DATE]
- [x] Toggle 2: Full Merged Content (Validated)
- [x] Toggle 3: VALIDATION REPORT - [DATE]
- [x] Toggle 4: [Original Content Name]

### Status Updated
- Status: [New status]

### Ready for Kyla
- [Any action items listed]
```
```

---

## Integration Reference

### Notion Direct API

**Location:** `notion_direct_access.js` in workspace root  
**Documentation:** `documentation/setup-guides/NOTION_API_SETUP.md`

### Creating Toggle Heading 1

```javascript
import { notionRequest } from './notion_direct_access.js';

// Create a toggle heading 1
const toggleBlock = {
  object: 'block',
  type: 'heading_1',
  heading_1: {
    rich_text: [{ type: 'text', text: { content: 'Updated Craft Article - 2026-01-19' } }],
    is_toggleable: true
  }
};

// Add to page
const response = await notionRequest('/blocks/PAGE_ID/children', 'PATCH', {
  children: [toggleBlock]
});

// Get the new block's ID
const toggleId = response.results[0].id;

// Add children to the toggle
await notionRequest('/blocks/' + toggleId + '/children', 'PATCH', {
  children: [
    { object: 'block', type: 'paragraph', paragraph: { rich_text: [{ type: 'text', text: { content: 'Content inside toggle' } }] } }
  ]
});
```

### Renaming Existing Toggle

```javascript
// Update an existing block's text
await notionRequest('/blocks/BLOCK_ID', 'PATCH', {
  heading_1: {
    rich_text: [{ type: 'text', text: { content: 'Kyla Original Draft' } }]
  }
});
```

### Moving Blocks (Reordering)

Notion API doesn't support direct reordering. To reorder:
1. Read all blocks
2. Delete blocks (or archive page content)
3. Re-create in correct order

**Alternative:** Create new toggles in correct order, move content into them.

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
**Recovery:** Check Notion page history (if available) or restore from backup

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 19, 2026 | Initial release - standardized Notion page structure with 4 Toggle Heading 1 sections |
