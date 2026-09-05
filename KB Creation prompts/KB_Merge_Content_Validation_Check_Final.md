# KB Content Validation - Final Check

**Purpose:** Final validation layer to verify KB article accuracy before publishing. Validates all technical claims, procedures, and error messages against authoritative sources.

**When to Use:** After formatting is complete, before publishing to Craft CMS. This is the "is this actually correct?" check.

**Target Confidence:** 90%+ accuracy on all technical claims

**Integration Reference:** See `KB_Integration_References_Final.md` for all query templates.

---

## INPUT: Craft CMS KB Draft URL

You will be provided with a **Craft CMS KB draft URL** to validate.

**Example Inputs:**
```
# Draft URL (has draftId parameter):
Validate this KB draft: https://supercatsolutions.com/admin/entries/knowledgeBase/2575?draftId=852

# Published article URL (no draftId):
Validate this KB article: https://supercatsolutions.com/admin/entries/knowledgeBase/41981
```

### Step 0: Fetch the Draft Content

**⚠️ CRITICAL: Draft vs Published Query Difference**

| URL Type | Example | Query To Use |
|----------|---------|--------------|
| **Draft** (has `?draftId=XXX`) | `/knowledgeBase/2575?draftId=852` | `knowledgeBaseEntries(draftId: 852)` |
| **Published** (no draftId) | `/knowledgeBase/41981` | `knowledgeBaseEntries(id: ["41981"])` |

**⛔ WARNING:** If you query by `id` when a `draftId` is present, you will get the **published version**, NOT the draft.

#### Extract IDs from the URL

```
URL: https://supercatsolutions.com/admin/entries/knowledgeBase/2575?draftId=852
                                                              ↑          ↑
                                                         Entry ID    Draft ID

If draftId present → Use draftId for query
If no draftId     → Use entry ID for query
```

See `KB_Integration_References_Final.md` for the exact GraphQL queries.

---

## STEP 0.5: VALIDATE FEATURE PURPOSE CLARITY (Before Technical Validation)

Before validating technical claims, validate the article's FRAMING. Technical accuracy means nothing if the article misleads users about WHY they'd use the feature.

### Purpose Clarity Check

Extract from the Summary and answer:

| Question | Article's Answer | Clear? |
|----------|------------------|--------|
| What problem does this solve for the user? | [extract from Summary] | ✅ / ❌ |
| Who benefits and how? | [extract] | ✅ / ❌ |
| Why use this vs. alternatives? | [extract or "missing"] | ✅ / ❌ |

### User Benefit Validation

Compare the article's Summary against:

1. **Live article (if exists):** Does the framing match how it's currently explained?
2. **Help Scout tickets:** Is this how users describe their need for this feature?
3. **Plain language test:** Would a new user understand WHY they'd want this?

### Red Flags to Check

| Phrase Pattern | Issue | Example Fix |
|----------------|-------|-------------|
| "before going into production" | Manufacturing jargon, may confuse | "when they're not ready to order yet" |
| "automatically sent to [system]" | Technical mechanism, not user benefit | "saved for follow-up" |
| "for analysis purposes" | Vague, doesn't explain user value | "so you can track who's interested" |
| "enables [technical process]" | Developer language | "lets you [user action]" |

### Purpose Clarity Output

```markdown
## Feature Purpose Validation

**Summary from article:** "[quote the Summary]"

**Purpose Clarity:**
- [ ] Problem solved is clear: [Yes/No - explain]
- [ ] User benefit is stated: [Yes/No - explain]  
- [ ] Plain language used: [Yes/No - flag jargon]

**Recommendation:** ✅ CLEAR / ⚠️ NEEDS REWRITE / ❌ MISLEADING

**If rewrite needed, suggested Summary:**
"[your suggested rewrite focusing on user benefit]"
```

---

## ⛔ CRITICAL: ANTI-HALLUCINATION RULES

### The Problem This Solves

KB articles may contain:
- Incorrect field names or casing
- Outdated feature behavior
- Inaccurate error messages
- Wrong navigation paths
- Missing edge cases
- Procedures that don't match actual system behavior

**You have close to zero product knowledge. You MUST validate everything against sources.**

### Mandatory Rules

```
⛔ FORBIDDEN: Approving ANY technical claim without source verification
⛔ FORBIDDEN: Assuming field names are correct without codebase check
⛔ FORBIDDEN: Trusting error message text without Help Scout validation
⛔ FORBIDDEN: Approving procedures without verifying against support patterns
⛔ FORBIDDEN: Marking "verified" without tool call evidence
```

---

## VALIDATION HIERARCHY (Sources of Truth)

| Priority | Source | What It Validates | Authority Level |
|----------|--------|-------------------|-----------------|
| 0 | **User Understanding** | Feature purpose, user benefit, plain language framing | 🟣 FOUNDATIONAL |
| 1 | **Codebase** | Field names, feature behavior, API structure | 🔴 ABSOLUTE (override all others) |
| 2 | **MCP Live Data** | Current system state, configuration options | 🟠 HIGH |
| 3 | **Help Scout Tickets** | Error messages, troubleshooting steps, edge cases | 🟡 MEDIUM-HIGH |
| 4 | **Fathom Calls** | How features are explained, common questions | 🟡 MEDIUM |
| 5 | **Existing KB Articles** | Consistency with published content | 🟢 REFERENCE ONLY |

**Rule:** If sources conflict, higher priority wins. Always flag conflicts.

**Priority 0 Note:** Technical accuracy means nothing if the article misleads users about WHY they'd use the feature.

---

## STEP 1: EXTRACT CLAIMS FROM ARTICLE

Before validating, extract ALL verifiable claims from the KB article:

### Claim Categories

| Category | Example | Validation Source |
|----------|---------|-------------------|
| **Field Names** | 'ImageFileName', 'MappedBillToCode' | Codebase |
| **Error Messages** | "ImageFileName: [filename] is not valid" | Help Scout + Codebase |
| **Navigation Paths** | Admin Console > Products > Option Mappings | MCP + Codebase |
| **Feature Behavior** | "Maximum 6 images per product" | Codebase |
| **File Formats** | "Supported: JPG, PNG, GIF, TIF" | Codebase |
| **Procedures** | "Download the Missing Images report" | Help Scout + Fathom |
| **Limitations** | "Cannot add new matrix entries via GraphQL" | Codebase |
| **Numeric Limits** | "15 MB for source images, 4 MB processed" | Codebase |

### Extraction Template

```markdown
## Claims Extracted from Article: [ARTICLE TITLE]

### Field Names Mentioned
| Field Name | Context | Line/Section |

### Error Messages Quoted
| Error Message | Context | Line/Section |

### Procedures Described
| Procedure | Steps | Line/Section |

### Numeric Claims
| Claim | Value | Line/Section |

### Feature Behaviors
| Feature | Claimed Behavior | Line/Section |
```

---

## STEP 2: CODEBASE VALIDATION (HIGHEST PRIORITY)

### 2A: Field Name Verification

For EVERY field name mentioned in the article:

```bash
# Search codebase for exact field name
grep -r "FieldName" --include="*.py" --include="*.js" --include="*.ts" .

# Search for variations (case-insensitive)
grep -ri "fieldname" --include="*.py" --include="*.js" .
```

**Validation Criteria:**
- ✅ VERIFIED: Exact match found in codebase
- ⚠️ CASE MISMATCH: Found but different casing (FIX REQUIRED)
- ❌ NOT FOUND: Field name doesn't exist (BLOCKER)

### 2B: Feature Behavior Verification

For EVERY feature behavior claim, search for implementation and configuration constants.

### 2C: Error Message Verification

For EVERY error message quoted, search for exact error text in codebase.

### Codebase Validation Output

```markdown
## Codebase Validation Results

### Field Names
| Field | Article Says | Codebase Says | Status |

### Feature Behaviors
| Claim | Article Says | Codebase Evidence | Status |

### Error Messages
| Error | Article Says | Codebase Says | Status |
```

---

## STEP 3: HELP SCOUT VALIDATION

### 3A: Error Message Pattern Matching

Search Help Scout for tickets containing the error messages mentioned in the article. Use queries from Integration Reference.

### 3B: Troubleshooting Step Validation

Search for how support actually resolves these issues. Look for:
- Do support responses match the article's troubleshooting steps?
- Are there additional steps support recommends that aren't in the article?
- Are there edge cases mentioned in tickets not covered?

### 3C: Error Frequency Analysis

Count how often each error type appears to validate article coverage.

### Help Scout Validation Output

```markdown
## Help Scout Validation Results

### Error Messages Confirmed
| Error Type | Article Text | Help Scout Evidence | Ticket Count | Status |

### Troubleshooting Steps Confirmed
| Step | Article Says | Support Actually Does | Status |

### Missing Edge Cases (Found in Tickets, Not in Article)
| Edge Case | Ticket Evidence | Recommendation |
```

---

## STEP 4: FATHOM CALL VALIDATION

Search for training/onboarding calls on this topic. Look for:
- How is this feature/process actually explained to clients?
- What questions do clients ask?
- What common misunderstandings exist?
- Are there verbal instructions that differ from written documentation?

### Fathom Validation Output

```markdown
## Fathom Call Validation Results

### Relevant Calls Found
| Call ID | Date | Title | Relevance |

### Feature Explanations Compared
| Topic | Article Explains | Call Explained | Match? |

### Client Questions Not Addressed in Article
| Question from Call | Recommendation |
```

---

## STEP 5: MCP LIVE DATA VALIDATION

Verify features exist in system:
- `get_organization_info` → Check features are enabled/available
- `get_data_summary` → Check data types exist
- `get_options` → Verify options exist as described
- `get_mobile_sites` → Verify eCat settings
- `get_reports_config` → Verify report types

---

## STEP 6: CONFIDENCE SCORING

### Per-Claim Scoring

| Validation Level | Confidence | Criteria |
|------------------|------------|----------|
| ✅✅✅ **TRIPLE VERIFIED** | 95%+ | Codebase + Help Scout + Fathom all confirm |
| ✅✅ **DOUBLE VERIFIED** | 85%+ | Codebase + one other source confirms |
| ✅ **SINGLE VERIFIED** | 70% | Codebase confirms (or 2 secondary sources) |
| ⚠️ **PARTIALLY VERIFIED** | 50% | One secondary source confirms, codebase unclear |
| ❓ **UNVERIFIED** | 0% | No source confirmation found |
| ❌ **CONTRADICTED** | BLOCKER | Source says something different |

### Article-Level Scoring

```
Article Confidence = (Verified Claims / Total Claims) × 100

Target: 90%+ for publication
70-89%: Publish with review flag
<70%: DO NOT PUBLISH - requires revision
```

---

## STEP 7: AUTO-APPLY CORRECTIONS

**After validation, automatically apply corrections that do NOT require manual intervention.**

### What to Auto-Apply (No Manual Work)

✅ **AUTO-APPLY these corrections directly to Craft:**
- Missing error message variants
- Incorrect error message text
- Field name casing fixes
- Missing command-line examples
- Decision trees / quick identification guides
- Additional troubleshooting steps from Help Scout
- Numeric limit corrections
- Navigation path updates

### What to FLAG Only (Requires Manual Work)

⚠️ **FLAG but do NOT auto-apply:**
- Screenshots or video suggestions
- Images that need to be captured
- UI changes that need visual verification
- Content requiring human judgment/review

**⚠️ HARD LIMIT: Maximum 3 image placeholders per article.**

**Placeholder format in Craft draft:**
```html
<p><strong>⚠️ [PLACEHOLDER - DO NOT PUBLISH] Screenshot needed:</strong> <em>Description.</em></p>
```

### Auto-Apply Process

1. Identify the section ID from the article fetch
2. Prepare the updated HTML with correction applied
3. Push via GraphQL mutation (see Integration Reference)
4. Document what was changed

---

## STEP 8: PREPARE VALIDATION OUTPUT FOR NOTION

**⚠️ IMPORTANT:** Do NOT update Notion directly. Prepare output for `KB_Merge_Notion_Update_Final.md`.

```markdown
## VALIDATION OUTPUT (For Notion Final Update)

### VALIDATION REPORT - [DATE]

**Craft Draft URL:** [URL]
**Overall Confidence:** [X]%
**Recommendation:** ✅ PUBLISH / ⚠️ PUBLISH WITH REVIEW / ❌ REVISE REQUIRED

---

#### Validation Summary

| # | Section / Claim | Source | Status | Notes |
|---|-----------------|--------|--------|-------|
| 1 | [Section name] | Codebase | ✅ Verified | |
| 2 | [Error message claim] | Codebase + Help Scout | ✅ Verified | |
| 3 | [Missing item] | Codebase | ➕ Added | Was missing from draft |

---

#### Auto-Applied Corrections

| Section | What Was Changed | Source Evidence |
(Or: "None required - draft content is accurate.")

---

#### Flagged for Manual (Screenshots - MAX 3)

| Section | Screenshot Needed | Priority |
(Or: "No new screenshots needed.")

---

#### Action for Kyla

⚠️ [Any manual steps required]
```

**Next Step:** Run `KB_Merge_Notion_Update_Final.md` to structure the Notion page.

---

## STEP 9: OUTPUT TEMPLATE

```markdown
# KB Content Validation Report

**Article:** [TITLE]
**Validation Date:** [DATE]
**Overall Confidence:** [X]%
**Recommendation:** ✅ PUBLISH / ⚠️ PUBLISH WITH REVIEW / ❌ REVISE REQUIRED

---

## Executive Summary

- **Total Claims Validated:** [X]
- **Verified (✅):** [X] ([X]%)
- **Partially Verified (⚠️):** [X] ([X]%)
- **Unverified (❓):** [X] ([X]%)
- **Contradicted (❌):** [X] ([X]%)
- **Auto-Applied Corrections:** [X]
- **Flagged for Manual Review:** [X]

---

## Validation Table (All Items)

| # | Claim/Item | Category | Source | Evidence | Confidence | Action |
|---|------------|----------|--------|----------|------------|--------|

---

## Critical Issues (Must Fix Before Publishing)

| Issue | Location | Source Evidence | Required Fix |

---

## Auto-Applied Corrections

| Section | Change | Source Evidence | Status |

---

## Flagged for Manual Review (Images/Videos Only)

| Section | Suggestion | Why Manual | Priority |

---

## Verification Details

### Codebase Validation
[Results]

### Help Scout Validation  
[Results]

### Fathom Validation
[Results]

### MCP Validation
[Results]

---

## Missing Content (Recommended Additions)

| Topic | Source | Evidence | Priority | Auto-Applied? |

---

## Validation Certification

I certify that:
- [ ] ALL field names verified against codebase
- [ ] ALL error messages verified against Help Scout OR codebase
- [ ] ALL procedures verified against support patterns
- [ ] ALL numeric claims verified against codebase
- [ ] NO claims approved without tool call evidence
- [ ] ALL non-manual corrections auto-applied to Craft

**Validator:** [AI Model]
**Date:** [DATE]
```

---

## WORKFLOW SUMMARY

```
0. FETCH article content from Craft CMS URL (GraphQL)
   ⚠️ CHECK: Does URL have ?draftId=XXX?
   - YES → Query with knowledgeBaseEntries(draftId: XXX)
   - NO  → Query with knowledgeBaseEntries(id: ["ENTRY_ID"])
   ↓
0.5. VALIDATE feature purpose clarity (BEFORE technical validation)
   ↓
1. EXTRACT all claims from article
   ↓
2. VALIDATE field names against codebase (REQUIRED)
   ↓
3. VALIDATE error messages against Help Scout + codebase
   ↓
4. VALIDATE procedures against support patterns
   ↓
5. CHECK Fathom calls for additional context
   ↓
6. VERIFY features exist via MCP
   ↓
7. AUTO-APPLY non-manual corrections to Craft
   ↓
8. PREPARE validation output for Notion
   ↓
9. CALCULATE confidence score
   ↓
10. GENERATE validation report
   ↓
11. DECISION: Publish / Review / Revise
   ↓
12. RUN KB_Merge_Notion_Update_Final.md to structure Notion page
```

---

## COMMON VALIDATION FAILURES

### Failure 0: Validating Published Article Instead of Draft
**Problem:** URL has `?draftId=852` but you queried by entry ID
**Impact:** Validation results are completely wrong
**Fix:** Check URL for `?draftId=XXX`, use `knowledgeBaseEntries(draftId: XXX)`

### Failure 1: Field Name Casing
**Problem:** Article says 'imagefile' but codebase has 'ImageFile'
**Fix:** Always use exact casing from codebase

### Failure 2: Outdated Error Messages
**Problem:** Error text was updated in recent release
**Fix:** Update to current error message text

### Failure 3: Missing Edge Cases
**Problem:** Article covers happy path but not exceptions
**Fix:** Add troubleshooting section for edge case

### Failure 4: Incorrect Limits
**Problem:** Article says "6 images max" but system allows 12
**Fix:** Update to "6 images (or 12 if extended limit enabled)"

### Failure 5: Wrong Navigation Path
**Problem:** UI was reorganized, old path doesn't work
**Fix:** Update navigation path to current UI

### Failure 6: Misleading Feature Purpose Framing
**Problem:** Summary is technically accurate but frames the feature's purpose incorrectly
**Example:** 
- Article says: "Track customer demand before products go into production"
- Reality: "Capture customer interest so sales reps can follow up later"
**Fix:** Rewrite Summary to lead with user benefit, not technical mechanism

### Failure 7: Jargon Without Context
**Problem:** Technical phrases that confuse users
**Examples:** "before going into production", "enables field-based pricing logic"
**Fix:** Replace jargon with plain language

### Failure 8: Mechanism vs. Benefit Confusion
**Problem:** Summary describes HOW the feature works instead of WHY a user would want it
**Fix:** Lead with the problem solved, then (optionally) explain the mechanism
