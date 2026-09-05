# KB Complete Merge & Validate Prompt (Chained Workflow)

**Purpose:** Single prompt that runs the COMPLETE KB article update workflow - merge Notion content into Craft, then validate for accuracy. Two prompts, one execution.

**Use When:** You have a Notion KB backlog article (Action Type = Merge) and want to run the full pipeline in one go.

---

## Quick Start

Just paste this into Cursor with your Notion URL:

```
Run the complete KB merge and validation workflow:

**Notion URL:** [PASTE NOTION URL HERE]

Execute both steps in sequence:
1. @KB_Merge_Article_Validation_Prompt_Revised_Article_Structure.md - Merge Notion into Craft draft
2. @KB_Content_Validation_Final_Check.md - Validate the draft and auto-apply corrections

After Step 1 completes, use the Craft draft ID/URL that was created to run Step 2.
Update Notion with findings from BOTH steps.
```

---

## Full Prompt (Copy This)

```
You are running a CHAINED KB article workflow. This combines two prompts into a single execution.

**CRITICAL:** Complete Step 1 fully before starting Step 2. Step 2 uses the Craft draft created in Step 1.

---

## Input

**Notion URL:** [PASTE NOTION URL]

---

## STEP 1: MERGE WORKFLOW

Run the complete workflow from @KB_Merge_Article_Validation_Prompt_Revised_Article_Structure.md

### Required Actions:
1. Fetch the Notion page content
2. Check status (skip if Archived/Consolidated)
3. Check for Prepared Draft section (use if exists)
4. Check for Consolidated Source Content (include if exists)
5. Fetch the existing Craft CMS article from the URL field
6. Compare both sources side-by-side (terminology, sections, word counts)
7. Create merge plan (KEEP + ADD + ENHANCE)
8. Query Help Scout for relevant tickets
9. Query Fathom for relevant calls
10. Validate against codebase
11. Create Craft draft with merged content following article structure:
    - Summary (2-3 sentences)
    - Quick Start (5-7 steps)
    - How It Works
    - Step-by-Step Setup
    - Prerequisites
    - Troubleshooting (combines FAQs, mistakes, help)
12. Save merged content to TOP of Notion page
13. Update Notion status to "Ready for Craft (Kyla Check)"

### Output Checkpoint (Required Before Step 2):
- [ ] Craft Draft ID: _____
- [ ] Craft Draft URL: _____
- [ ] Notion updated with merged content: ✅
- [ ] Merge word count >= original word count: ✅

**⚠️ DO NOT proceed to Step 2 until the above are confirmed.**

---

## STEP 2: VALIDATION WORKFLOW

Run the complete workflow from @KB_Content_Validation_Final_Check.md using the Craft draft created in Step 1.

### Required Actions:
1. Fetch the Craft draft content (use Draft ID from Step 1)
2. Extract ALL verifiable claims:
   - Field names
   - Error messages
   - Navigation paths
   - Feature behaviors
   - Numeric limits
   - Procedures
3. Validate each claim against:
   - Codebase (highest priority - REQUIRED)
   - Help Scout tickets
   - Fathom calls
   - MCP live data
4. Calculate confidence scores per claim
5. AUTO-APPLY text/content corrections to Craft draft:
   - Field name casing fixes
   - Error message corrections
   - Missing troubleshooting steps
   - Decision trees / quick guides
6. FLAG (do not auto-apply) items needing manual work:
   - Screenshots (MAX 3)
   - Videos
   - UI verification
7. Calculate overall article confidence (target: 90%+)
8. Add VALIDATION REPORT to TOP of Notion page (above the merged content from Step 1)

### Validation Report Format for Notion:
```
### VALIDATION REPORT - [DATE]

**Craft Draft URL:** [URL]
**Overall Confidence:** [X]%
**Recommendation:** ✅ PUBLISH / ⚠️ PUBLISH WITH REVIEW / ❌ REVISE REQUIRED

---

#### Validation Summary

| # | Section / Claim | Source | Status | Notes |
|---|-----------------|--------|--------|-------|
| 1 | [claim] | Codebase | ✅ Verified | |
| 2 | [claim] | Help Scout | ✅ Verified | |
| 3 | [missing item] | Codebase | ➕ Added | Was missing |
| 4 | [incorrect item] | Codebase | ✅ Corrected | Fixed casing |

---

#### Auto-Applied Corrections

| Section | What Changed | Source Evidence |
|---------|--------------|-----------------|
| [section] | [change] | [source] |

---

#### Flagged for Manual (Screenshots - MAX 3)

**Search "PLACEHOLDER" in Craft draft to find all locations.**

| Section | Screenshot Needed | Priority |
|---------|-------------------|----------|
| [section] | [description] | HIGH/MED/LOW |
```

---

## FINAL OUTPUT SUMMARY

After completing BOTH steps, provide this summary:

```
# KB COMPLETE WORKFLOW SUMMARY

## Article Information
- **Notion Page:** [Title]
- **Notion URL:** [URL]
- **Craft Article:** [Title]
- **Craft Draft ID:** [ID]
- **Craft Draft URL:** [URL]

## Step 1: Merge Results
- **Original Craft word count:** [X]
- **Final merged word count:** [Y]
- **Content KEPT:** [list]
- **Content ADDED:** [list]
- **Content ENHANCED:** [list]
- **Consolidated sources included:** [list or N/A]

## Step 2: Validation Results
- **Total claims validated:** [X]
- **Verified:** [X] ([X]%)
- **Corrections auto-applied:** [X]
- **Flagged for manual (screenshots):** [X]
- **Overall confidence:** [X]%
- **Recommendation:** ✅ / ⚠️ / ❌

## Notion Updates
- [x] Merged content added (Step 1)
- [x] Validation report added (Step 2)
- [x] Status: Ready for Craft (Kyla Check)

## Next Steps for Kyla
1. Review Craft draft: [URL]
2. Search "PLACEHOLDER" for screenshot locations
3. Add screenshots (if flagged)
4. Final review and PUBLISH
```

---

## Error Handling

### If Step 1 fails:
- Document the failure reason
- Do NOT proceed to Step 2
- Output what was attempted and where it failed

### If Step 2 validation is <70%:
- Complete the validation anyway
- Auto-apply what can be fixed
- Flag the article as ❌ REVISE REQUIRED
- Document specific issues that need human attention

### If Notion page is Archived (Consolidated):
- STOP immediately
- Output: "⏭️ SKIPPED: This article is archived (consolidated into [Parent]). Process the parent instead."
- Provide the parent article URL

---

## Important Notes

- **Do NOT publish** - save as Craft draft only
- **Do NOT edit original Notion draft** - add new sections at TOP
- **MERGE means ENHANCE** - final article >= original length
- **Auto-apply text fixes** - only flag screenshots for manual work
- **MAX 3 screenshots** per article
- **Target 90%+ confidence** before recommending publish
```

---

## Even Shorter Version

If you want the absolute minimum to paste:

```
Complete KB workflow for this Notion article:

**Notion URL:** [PASTE URL]

1. Run @KB_Merge_Article_Validation_Prompt_Revised_Article_Structure.md fully
2. Then run @KB_Content_Validation_Final_Check.md on the Craft draft created in step 1
3. Update Notion with results from both steps

Provide final summary with Craft draft URL, confidence score, and next steps for Kyla.
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 18, 2026 | Initial chained workflow prompt |
