# KB Merge Workflow

**Purpose:** Visual guide showing how all KB merge prompts work together to process Notion backlog articles into validated Craft CMS articles.

**Last Updated:** January 26, 2026

---

## Quick Reference: Which Prompt to Use

| Notion Page Status | Action Type | Start With |
|--------------------|-------------|------------|
| **Clean draft, want FULL pipeline** | Merge | → **KB_Complete_Merge_and_Validate_Prompt.md** ⭐ |
| Messy/incomplete draft | Needs Prep | → **KB_Draft_Prep_Prompt.md** |
| Clean draft, existing Craft article | Merge (step-by-step) | → **KB_Merge_Article_Prompt_Final.md** |
| Draft already in Craft, needs accuracy check | Validate | → **KB_Merge_Content_Validation_Check_Final.md** |
| After Merge + Validation complete | Notion cleanup | → **KB_Merge_Notion_Update_Final.md** |

### ⭐ Recommended: One-Prompt Full Pipeline

**For most Merge articles, use the chained prompt:**

```
Complete KB workflow for this Notion article:

**Notion URL:** [PASTE URL]

1. Run @KB_Merge_Article_Prompt_Final.md fully
2. Then run @KB_Merge_Content_Validation_Check_Final.md on the Craft draft created in step 1
3. Then run @KB_Merge_Notion_Update_Final.md to structure the Notion page

Provide final summary with Craft draft URL, confidence score, and next steps for Kyla.
```

This runs Merge + Validation + Notion Update in one execution.

---

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KB MERGE WORKFLOW                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │   NOTION PAGE    │
                              │  (KB Backlog)    │
                              └────────┬─────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────────┐
                    │  CHECK 1: Is Status "Archived        │
                    │  (Consolidated)"?                    │
                    └──────────────────────────────────────┘
                                       │
                    YES ───────────────┼─────────────── NO
                     │                                   │
                     ▼                                   ▼
           ┌─────────────────┐              ┌──────────────────────────┐
           │ ⏭️ SKIP - Find  │              │  CHECK 2: Is the draft   │
           │ parent article  │              │  messy/incomplete?       │
           └─────────────────┘              └──────────────────────────┘
                                                        │
                                         YES ───────────┼─────────── NO
                                          │                          │
                                          ▼                          │
                            ┌─────────────────────┐                  │
                            │ STEP 0: PREP DRAFT  │                  │
                            │ (Optional)          │                  │
                            ├─────────────────────┤                  │
                            │ KB_Draft_Prep_      │                  │
                            │ Prompt.md           │                  │
                            ├─────────────────────┤                  │
                            │ • Organize content  │                  │
                            │ • Validate accuracy │                  │
                            │ • Research Help     │                  │
                            │   Scout + Fathom    │                  │
                            │ • Add "Prepared     │                  │
                            │   Draft" at TOP     │                  │
                            │ • Status → "Ready   │                  │
                            │   for Merge"        │                  │
                            └──────────┬──────────┘                  │
                                       │                             │
                                       └──────────────┬──────────────┘
                                                      │
                                                      ▼
                                   ┌─────────────────────────────┐
                                   │  READ FIRST:                │
                                   │  KB_Integration_References_ │
                                   │  Final.md                   │
                                   │  (BigQuery, Notion, Craft)  │
                                   └──────────────┬──────────────┘
                                                  │
                                                  ▼
                            ┌─────────────────────────────────────┐
                            │   STEP 1: MERGE INTO CRAFT          │
                            ├─────────────────────────────────────┤
                            │ KB_Merge_Article_Prompt_Final.md    │
                            ├─────────────────────────────────────┤
                            │ 1.0 Check for Prepared Draft        │
                            │ 1.5 Compare Notion vs Craft         │
                            │     (terminology, sections, counts) │
                            │ 1.6 Validate Feature PURPOSE        │
                            │     (user benefit, not mechanism!)  │
                            │ 2.  Research Help Scout + Fathom    │
                            │ 3.  Document validation findings    │
                            │ 4.  Classify article type + template│
                            │ 5.  Create merge plan (KEEP/ADD/    │
                            │     ENHANCE - never REMOVE)         │
                            │ 6.  Execute merge → Craft DRAFT     │
                            │ 7.  PREPARE output for Notion       │
                            │     (do NOT update Notion directly) │
                            └──────────────┬──────────────────────┘
                                           │
                            OUTPUT: Merge Output block with:
                            • Craft Draft URL + IDs
                            • Merge Summary (word counts)
                            • Content lists (kept/added/enhanced)
                            • Full Merged Content
                                           │
                                           ▼
                            ┌─────────────────────────────────────┐
                            │   STEP 2: VALIDATE ACCURACY         │
                            ├─────────────────────────────────────┤
                            │ KB_Merge_Content_Validation_        │
                            │ Check_Final.md                      │
                            ├─────────────────────────────────────┤
                            │ 0.  Fetch Craft draft (use draftId!)│
                            │ 0.5 Validate feature PURPOSE        │
                            │     (user benefit framing)          │
                            │ 1.  Extract ALL verifiable claims   │
                            │ 2.  Validate vs codebase (REQUIRED) │
                            │ 3.  Validate vs Help Scout          │
                            │ 4.  Validate vs Fathom calls        │
                            │ 5.  Validate vs MCP live data       │
                            │ 6.  Calculate confidence (aim 90%+) │
                            │ 7.  AUTO-APPLY text corrections     │
                            │ 8.  FLAG screenshots (MAX 3)        │
                            │ 9.  PREPARE output for Notion       │
                            │     (do NOT update Notion directly) │
                            └──────────────┬──────────────────────┘
                                           │
                            OUTPUT: Validation Output block with:
                            • Overall Confidence %
                            • Recommendation (✅/⚠️/❌)
                            • Validation Summary table
                            • Auto-Applied Corrections
                            • Flagged for Manual
                                           │
                                           ▼
                            ┌─────────────────────────────────────┐
                            │   STEP 3: STRUCTURE NOTION PAGE     │
                            ├─────────────────────────────────────┤
                            │ KB_Merge_Notion_Update_Final.md     │
                            ├─────────────────────────────────────┤
                            │ Creates 4 Toggle Heading 1 sections │
                            │ in this exact order:                │
                            │                                     │
                            │ ▶ Updated Craft Article - [DATE]    │
                            │   (URLs, merge summary, content     │
                            │    lists, action items)             │
                            │                                     │
                            │ ▶ Full Merged Content (Validated)   │
                            │   (COMPLETE article text - NOT a    │
                            │    link, the actual content)        │
                            │                                     │
                            │ ▶ VALIDATION REPORT - [DATE]        │
                            │   (confidence, claims table,        │
                            │    corrections, flagged items)      │
                            │                                     │
                            │ ▶ [Original Content Name]           │
                            │   (preserved for audit trail)       │
                            │                                     │
                            │ Status → "Live"                     │
                            └──────────────┬──────────────────────┘
                                           │
                                           ▼
                            ┌─────────────────────────────────────┐
                            │   KYLA REVIEW                       │
                            ├─────────────────────────────────────┤
                            │ • Review Craft draft URL            │
                            │ • Search "PLACEHOLDER" for          │
                            │   screenshot locations (MAX 3)      │
                            │ • Add screenshots if needed         │
                            │ • Final approval                    │
                            │ • PUBLISH                           │
                            └─────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                    CRITICAL RULES (APPLY THROUGHOUT)
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📖 KB_Integration_References_Final.md                                       │
│ READ THIS FIRST - Contains all query templates                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ • BigQuery: Help Scout tickets, Fathom calls                                │
│ • Notion API: Fetch, update, create toggles                                 │
│ • Craft CMS: GraphQL queries for drafts, articles, mutations                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📄 2.0_Craft_CMS_Formatting_Guidelines.md                                   │
│ Apply to ALL Craft content                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Article Type Templates (Troubleshoot, Feature, How-To, Reference)         │
│ • Formatting: Bold UI (**Save**), 'FieldName', blockquotes for notes        │
│ • Max 3 images per article                                                  │
│ • ONE Troubleshooting section (combines FAQs, mistakes)                     │
│ • NO Related Articles section (Craft auto-generates)                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚠️ MERGE = ENHANCE, NOT REPLACE                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Existing Craft article is the FOUNDATION                                  │
│ • Notion content ADDS to it                                                 │
│ • Final article MUST be >= original length                                  │
│ • When in doubt, KEEP existing content                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🎯 FEATURE PURPOSE VALIDATION                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Lead with USER BENEFIT, not technical mechanism:                            │
│                                                                             │
│ ❌ "Track customer demand before products go into production"               │
│ ✅ "Capture customer interest so you can follow up later"                   │
│                                                                             │
│ ❌ "Enables field-based promotion pricing via product file"                 │
│ ✅ "Apply discounts with a single tap at trade shows"                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Step Descriptions

### Step 0: KB Draft Prep (Optional)

**File:** `KB_Draft_Prep_Prompt.md`

**When to Use:**
- Notion draft is messy, disorganized, or incomplete
- Content is scattered or has duplicates
- Needs significant restructuring before merging

**What It Does:**
1. Analyzes current draft state
2. Researches Help Scout + Fathom for additional context
3. Validates against codebase
4. Reorganizes into proper structure
5. Adds "Prepared Draft" section at TOP of Notion page
6. Sets status to "Ready for Merge"

**Output Location:** TOP of Notion page

**Skip If:** Draft is already clean and well-organized

---

### Step 1: KB Merge into Craft

**File:** `KB_Merge_Article_Prompt_Final.md`

**When to Use:**
- Always (this is the core workflow)
- After Draft Prep (if used)

**What It Does:**

| Sub-Step | Action |
|----------|--------|
| 1.0 | Check for "Prepared Draft" section (use if exists) |
| 1.5 | **Compare Notion vs Craft** - terminology, sections, word counts |
| 1.6 | **Validate Feature PURPOSE** - user benefit, not mechanism! |
| 2A | Query Help Scout for tickets |
| 2B | Validate against codebase |
| 2C | Query Fathom for calls |
| 3 | Document validation findings (DO NOT edit original draft) |
| 4 | Visual asset recommendations (MAX 3, only if crucial) |
| 5.1 | Review existing Craft structure |
| 5.2 | Classify article type and apply template |
| 5.3 | Apply merge rules (KEEP/ADD/ENHANCE - never remove) |
| 5.4 | Output merge plan confirmation |
| 5.5 | Execute merge → Create Craft DRAFT |
| 6 | **PREPARE output for Notion** (do NOT update directly) |

**Critical Rules:**
- Final article MUST be >= original length
- Use Craft's terminology as authoritative
- Classify article type before structuring
- Include consolidated sources if present

**Output:** Merge Output block for next step

---

### Step 2: Validate Accuracy

**File:** `KB_Merge_Content_Validation_Check_Final.md`

**When to Use:**
- After Step 1 (Merge)
- Before Kyla review
- To verify 90%+ accuracy

**What It Does:**

| Sub-Step | Action |
|----------|--------|
| 0 | Fetch Craft draft content (⚠️ use draftId if present!) |
| 0.5 | **Validate Feature PURPOSE** - clarity, user benefit |
| 1 | Extract ALL verifiable claims (fields, errors, paths, limits) |
| 2 | Validate vs codebase (HIGHEST PRIORITY - required) |
| 3 | Validate vs Help Scout tickets |
| 4 | Validate vs Fathom calls |
| 5 | Validate vs MCP live data |
| 6 | Calculate confidence scores |
| 7 | **AUTO-APPLY** text corrections to Craft |
| 8 | **FLAG** screenshots (MAX 3, use placeholder format) |
| 9 | **PREPARE output for Notion** (do NOT update directly) |

**Validation Hierarchy:**
| Priority | Source | Authority |
|----------|--------|-----------|
| 0 | User Understanding | 🟣 FOUNDATIONAL |
| 1 | Codebase | 🔴 ABSOLUTE |
| 2 | MCP Live Data | 🟠 HIGH |
| 3 | Help Scout | 🟡 MEDIUM-HIGH |
| 4 | Fathom Calls | 🟡 MEDIUM |
| 5 | Existing KB | 🟢 REFERENCE ONLY |

**Confidence Thresholds:**
| Score | Status | Action |
|-------|--------|--------|
| 90%+ | ✅ Ready to publish | Proceed |
| 70-89% | ⚠️ Publish with review | Flag for Kyla |
| <70% | ❌ Requires revision | Do NOT publish |

**Output:** Validation Output block for next step

---

### Step 3: Structure Notion Page

**File:** `KB_Merge_Notion_Update_Final.md`

**When to Use:**
- After Step 1 (Merge) AND Step 2 (Validation) complete
- Final step before Kyla review

**What It Does:**

Creates exactly 4 Toggle Heading 1 sections in this order:

```
▶ Updated Craft Article - [DATE]
   • Craft Draft URL, Entry ID, Draft ID
   • Merge Summary (word counts, % change)
   • Content KEPT from Craft
   • Content ADDED from Notion
   • Content ENHANCED
   • Action for Kyla

▶ Full Merged Content (Validated)
   • 📄 "This is the authoritative record..."
   • COMPLETE article text (all sections)
   • --- END OF MERGED CONTENT ---

▶ VALIDATION REPORT - [DATE]
   • Overall Confidence %
   • Recommendation (✅/⚠️/❌)
   • Validation Summary table
   • Auto-Applied Corrections
   • Flagged for Manual (screenshots)
   • Action for Kyla

▶ [Original Content Name]
   • Preserved unchanged for audit trail
```

**Status Update:** → "Live"

---

## Quick Decision Tree

```
START: You have a Notion KB page to process
       │
       ▼
Is Status = "Archived (Consolidated)"?
       │
  YES ─┼─ NO
   │       │
   ▼       │
⏭️ STOP    │
Find parent│
article    │
           ▼
Is the draft messy/incomplete?
           │
    YES ───┼─── NO
     │           │
     ▼           │
Run KB_Draft_    │
Prep_Prompt.md   │
     │           │
     ▼           │
"Prepared Draft" │
section created  │
     │           │
     └─────┬─────┘
           │
           ▼
┌─────────────────────────┐
│ STEP 1: MERGE           │
│ KB_Merge_Article_       │
│ Prompt_Final.md         │
└───────────┬─────────────┘
            │
            ▼
    Did merge succeed?
    Draft created?
            │
     YES ───┼─── NO
      │           │
      │           ▼
      │        TROUBLESHOOT
      │        (check errors)
      │
      ▼
┌─────────────────────────┐
│ STEP 2: VALIDATE        │
│ KB_Merge_Content_       │
│ Validation_Check_       │
│ Final.md                │
└───────────┬─────────────┘
            │
            ▼
    Confidence 90%+?
            │
     YES ───┼─── NO
      │           │
      │           ▼
      │      70-89%: ⚠️ Flag for review
      │      <70%:  ❌ REVISE
      │
      ▼
┌─────────────────────────┐
│ STEP 3: NOTION UPDATE   │
│ KB_Merge_Notion_        │
│ Update_Final.md         │
└───────────┬─────────────┘
            │
            ▼
    ✅ READY FOR KYLA
    
    • Review Craft draft
    • Search "PLACEHOLDER"
    • Add screenshots
    • PUBLISH
```

---

## File Summary

| File | Purpose | Input | Output |
|------|---------|-------|--------|
| **KB_Integration_References_Final.md** | 📖 Query templates (BigQuery, Notion, Craft) | N/A | Reference doc |
| **2.0_Craft_CMS_Formatting_Guidelines.md** | 📄 Formatting + article type templates | N/A | Reference doc |
| **KB_Complete_Merge_and_Validate_Prompt.md** | ⭐ Full pipeline in one prompt | Notion URL | All outputs combined |
| **KB_Draft_Prep_Prompt.md** | Clean up messy drafts | Notion URL | Prepared draft in Notion |
| **KB_Merge_Article_Prompt_Final.md** | Step 1: Merge Notion → Craft | Notion URL + Craft URL | Merge Output block |
| **KB_Merge_Content_Validation_Check_Final.md** | Step 2: Validate accuracy | Craft draft URL | Validation Output block |
| **KB_Merge_Notion_Update_Final.md** | Step 3: Structure Notion page | Notion URL + outputs | 4 Toggle H1 sections |

---

## Handling Special Cases

### Consolidated Articles

**If Notion page Status = "Archived (Consolidated)":**
- ⏭️ STOP immediately
- Find the parent article (look for callout banner)
- Process the parent instead

**If Notion page has "📦 Consolidated Source Content" section:**
- This is a PARENT article that absorbed child articles
- Include ALL consolidated content in the merge
- Document each source in the merge plan

### Terminology Conflicts

| Scenario | Action |
|----------|--------|
| Craft and Notion use different feature names | Use Craft's name (authoritative) |
| Notion term seems more accurate | Flag for Kyla's review |
| Field name casing differs | Use codebase (absolute truth) |

### Draft vs Published Query

| URL Type | How to Identify | Query Method |
|----------|-----------------|--------------|
| Draft | Has `?draftId=XXX` | `knowledgeBaseEntries(draftId: XXX)` |
| Published | No draftId param | `knowledgeBaseEntries(id: ["ENTRY_ID"])` |

⚠️ **WARNING:** If you query by `id` when `draftId` is present, you get the PUBLISHED version, not the draft!

---

## Anti-Hallucination Rules

```
⛔ FORBIDDEN: Approving ANY technical claim without source verification
⛔ FORBIDDEN: Assuming field names are correct without codebase check
⛔ FORBIDDEN: Trusting error message text without Help Scout validation
⛔ FORBIDDEN: Approving procedures without verifying against support patterns
⛔ FORBIDDEN: Marking "verified" without tool call evidence
⛔ FORBIDDEN: Writing Summary that describes mechanism instead of user benefit
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 19, 2026 | Initial workflow diagram |
| 1.1 | Jan 18, 2026 | Added KB_Complete_Merge_and_Validate_Prompt.md |
| 1.2 | Jan 19, 2026 | Added Step 4: KB_Notion_Final_Update.md |
| 2.0 | Jan 26, 2026 | **Major update:** Renamed to "KB Merge Workflow". Updated all file references to _Final.md versions. Added Integration References. Added Feature Purpose Validation (Step 1.6, 0.5). Added consolidated content handling. Restructured as 3-step workflow with dedicated Notion update step. Added detailed output blocks between steps. Added anti-hallucination rules. Updated special case handling. |
