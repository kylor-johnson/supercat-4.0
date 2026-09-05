# KB Content Validation - Final Check

**Purpose:** Final validation layer to verify KB article accuracy before publishing. Validates all technical claims, procedures, and error messages against authoritative sources.

**When to Use:** After formatting is complete, before publishing to Craft CMS. This is the "is this actually correct?" check.

**Target Confidence:** 90%+ accuracy on all technical claims

---

## INPUT: Craft CMS KB Draft URL

You will be provided with a **Craft CMS KB draft URL** to validate.

**Example Input:**
```
Validate this KB draft: https://supercatsolutions.com/admin/entries/knowledgeBase/41981
```

### Step 0: Fetch the Draft Content

Before validating, fetch the article content from Craft CMS:

```bash
curl -s -H "Authorization: Bearer HF9F8pdP9YDpLvM8FRwTH0ytRXChgLaD" \
  https://supercatsolutions.com/actions/graphql/api \
  -H "Content-Type: application/json" \
  -d '{"query": "{ knowledgeBaseEntries(id: [\"ENTRY_ID\"], status: [\"disabled\", \"live\"]) { id title slug articleSections { __typename ... on text_Entry { id body } } } }"}'
```

**Extract the entry ID from the URL.** Example: `/knowledgeBase/41981` → ID is `41981`

**GraphQL Query:**
```graphql
{
  knowledgeBaseEntries(id: ["ENTRY_ID"], status: ["disabled", "live"]) {
    id
    title
    slug
    articleSections {
      __typename
      ... on text_Entry { 
        id 
        body 
      }
    }
  }
}
```

Once you have the article content, proceed to extract and validate all claims.

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
| 1 | **Codebase** | Field names, feature behavior, API structure | 🔴 ABSOLUTE (override all others) |
| 2 | **MCP Live Data** | Current system state, configuration options | 🟠 HIGH |
| 3 | **Help Scout Tickets** | Error messages, troubleshooting steps, edge cases | 🟡 MEDIUM-HIGH |
| 4 | **Fathom Calls** | How features are explained, common questions | 🟡 MEDIUM |
| 5 | **Existing KB Articles** | Consistency with published content | 🟢 REFERENCE ONLY |

**Rule:** If sources conflict, higher priority wins. Always flag conflicts.

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
|------------|---------|--------------|
| [field] | [how it's used] | [where] |

### Error Messages Quoted
| Error Message | Context | Line/Section |
|---------------|---------|--------------|
| "[exact text]" | [error type] | [where] |

### Procedures Described
| Procedure | Steps | Line/Section |
|-----------|-------|--------------|
| [action] | [step count] | [where] |

### Numeric Claims
| Claim | Value | Line/Section |
|-------|-------|--------------|
| [what] | [number] | [where] |

### Feature Behaviors
| Feature | Claimed Behavior | Line/Section |
|---------|------------------|--------------|
| [feature] | [behavior] | [where] |
```

---

## STEP 2: CODEBASE VALIDATION (HIGHEST PRIORITY)

### 2A: Field Name Verification

For EVERY field name mentioned in the article:

```bash
# Search codebase for exact field name
grep -r "FieldName" --include="*.py" --include="*.js" --include="*.ts" --include="*.rb" .

# Search for variations (case-insensitive)
grep -ri "fieldname" --include="*.py" --include="*.js" --include="*.ts" .

# Check database schemas
grep -r "FieldName" --include="*.sql" --include="*schema*" --include="*migration*" .
```

**Validation Criteria:**
- ✅ VERIFIED: Exact match found in codebase
- ⚠️ CASE MISMATCH: Found but different casing (FIX REQUIRED)
- ❌ NOT FOUND: Field name doesn't exist (BLOCKER)

### 2B: Feature Behavior Verification

For EVERY feature behavior claim:

```bash
# Search for feature implementation
grep -r "feature_name" --include="*.py" -A 10 -B 5 .

# Search for configuration constants
grep -r "MAX_IMAGES\|IMAGE_LIMIT\|LIMIT" --include="*.py" --include="*.config*" .

# Search for validation logic
grep -r "validate\|check\|verify" --include="*.py" -A 5 .
```

### 2C: Error Message Verification

For EVERY error message quoted:

```bash
# Search for exact error text
grep -r "error message text" --include="*.py" --include="*.js" .

# Search for error patterns
grep -r "ImageFileName.*not valid\|invalid.*filename" --include="*.py" .
```

### Codebase Validation Output

```markdown
## Codebase Validation Results

### Field Names
| Field | Article Says | Codebase Says | Status |
|-------|--------------|---------------|--------|
| [field] | 'FieldName' | `FieldName` | ✅ VERIFIED |
| [field] | 'fieldname' | `FieldName` | ⚠️ CASE MISMATCH |
| [field] | 'FakeField' | NOT FOUND | ❌ BLOCKER |

### Feature Behaviors
| Claim | Article Says | Codebase Evidence | Status |
|-------|--------------|-------------------|--------|
| Image limit | 6 per product | `MAX_IMAGES = 6` in config.py | ✅ VERIFIED |

### Error Messages
| Error | Article Says | Codebase Says | Status |
|-------|--------------|---------------|--------|
| Invalid filename | "is not valid" | "is not valid and will not be imported" | ⚠️ PARTIAL MATCH |
```

---

## STEP 3: HELP SCOUT VALIDATION

### 3A: Error Message Pattern Matching

Search Help Scout for tickets containing the error messages mentioned in the article:

```sql
-- Search for error message patterns in tickets
SELECT 
  ticket_number,
  ticket_subject,
  DATE(ticket_created_at) as created,
  LEFT(ticket_preview, 500) as preview
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE (
  LOWER(ticket_subject) LIKE '%image%error%'
  OR LOWER(ticket_preview) LIKE '%image%error%'
  OR LOWER(ticket_preview) LIKE '%[EXACT ERROR TEXT]%'
)
AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
ORDER BY ticket_created_at DESC
LIMIT 30
```

### 3B: Troubleshooting Step Validation

Search for how support actually resolves these issues:

```sql
-- Get thread details for relevant tickets
SELECT 
  conversation_id,
  SUBSTR(body, 1, 1500) as response_text,
  type,
  created_at
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.conversation_threads`
WHERE CAST(conversation_id AS INT64) IN ([TICKET_IDS])
  AND type = 'message'  -- Support responses
ORDER BY conversation_id, created_at
LIMIT 50
```

**Look for:**
- Do support responses match the article's troubleshooting steps?
- Are there additional steps support recommends that aren't in the article?
- Are there edge cases mentioned in tickets not covered?

### 3C: Error Frequency Analysis

```sql
-- Count how often each error type appears
SELECT 
  CASE 
    WHEN LOWER(ticket_preview) LIKE '%missing image%' THEN 'Missing Image'
    WHEN LOWER(ticket_preview) LIKE '%invalid filename%' THEN 'Invalid Filename'
    WHEN LOWER(ticket_preview) LIKE '%not found%image%' THEN 'Image Not Found'
    ELSE 'Other'
  END as error_type,
  COUNT(*) as ticket_count
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE LOWER(ticket_preview) LIKE '%image%'
AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
GROUP BY 1
ORDER BY 2 DESC
```

**Validation:** If article covers "7 common errors" but Help Scout shows a different distribution, flag for review.

### Help Scout Validation Output

```markdown
## Help Scout Validation Results

### Error Messages Confirmed
| Error Type | Article Text | Help Scout Evidence | Ticket Count | Status |
|------------|--------------|---------------------|--------------|--------|
| Missing Image | "Missing image: [filename]" | Ticket #12345: "Missing image: ABC.jpg" | 47 | ✅ VERIFIED |

### Troubleshooting Steps Confirmed
| Step | Article Says | Support Actually Does | Status |
|------|--------------|----------------------|--------|
| Download report | "Download Missing Images report" | Ticket #12345: "Please download the report from..." | ✅ VERIFIED |

### Missing Edge Cases (Found in Tickets, Not in Article)
| Edge Case | Ticket Evidence | Recommendation |
|-----------|-----------------|----------------|
| [case] | Ticket #XXXXX | ADD TO ARTICLE |
```

---

## STEP 4: FATHOM CALL VALIDATION

### 4A: Search for Training/Onboarding Calls on This Topic

```python
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'integrations/fathom'))
from fathom_api import get_meetings, get_summary

# Get all meetings
meetings = get_meetings(limit=200, paginate=True)

# Filter for relevant topics
keywords = ['image', 'import', 'error', 'product file', 'csv', 'training', 'onboarding']
relevant = [m for m in meetings 
            if any(k.lower() in (m.get('meeting_title') or '').lower() for k in keywords)]

for m in relevant[:20]:
    print(f"{m.get('recording_id')} | {m.get('recording_start_time', '')[:10]} | {m.get('meeting_title')}")
```

### 4B: Get Summaries for Relevant Calls

```python
from fathom_api import get_summary

summary = get_summary([RECORDING_ID])
print(summary.get('summary', {}).get('markdown_formatted', '')[:3000])
```

**Look for:**
- How is this feature/process actually explained to clients?
- What questions do clients ask?
- What common misunderstandings exist?
- Are there verbal instructions that differ from written documentation?

### Fathom Validation Output

```markdown
## Fathom Call Validation Results

### Relevant Calls Found
| Call ID | Date | Title | Relevance |
|---------|------|-------|-----------|
| [ID] | [date] | [title] | Training on image imports |

### Feature Explanations Compared
| Topic | Article Explains | Call Explained | Match? |
|-------|------------------|----------------|--------|
| [topic] | [article version] | [verbal version] | ✅ / ⚠️ / ❌ |

### Client Questions Not Addressed in Article
| Question from Call | Recommendation |
|--------------------|----------------|
| "[question]" | ADD FAQ / ADD SECTION |
```

---

## STEP 5: MCP LIVE DATA VALIDATION

### 5A: Verify Feature Exists in System

```
get_organization_info(org_shortname)
→ Check: Features mentioned in article are actually enabled/available

get_data_summary(org_shortname)
→ Check: Data types mentioned exist

get_options(org_shortname)
→ Check: If article discusses options, verify options exist
```

### 5B: Verify Navigation Paths

```
get_mobile_sites(org_shortname)
→ Verify: eCat Online settings exist as described

get_reports_config(org_shortname)
→ Verify: Report types mentioned exist
```

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
- Missing error message variants (add to error message lists)
- Incorrect error message text (update to match codebase)
- Field name casing fixes (correct to codebase casing)
- Missing command-line examples (add exiftool, mogrify, etc.)
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

**⚠️ HARD LIMIT: Maximum 3 image placeholders per article.** Prioritize:
1. Most common issue/use case
2. Complex navigation that's hard to describe
3. Before/after comparisons

**Placeholder format in Craft draft:**
```html
<p><strong>⚠️ [PLACEHOLDER - DO NOT PUBLISH] Screenshot needed:</strong> <em>Description.</em></p>
```

### Auto-Apply Process

For each correction that can be auto-applied:

1. **Identify the section ID** from the article fetch (Step 0)
2. **Prepare the updated HTML** with the correction applied
3. **Push via GraphQL mutation:**

```graphql
mutation {
  save_text_Entry(
    id: "[SECTION_ID]"
    body: "[UPDATED_HTML_CONTENT]"
  ) {
    id
    dateUpdated
  }
}
```

4. **Document what was changed** in the validation report

### Auto-Apply Output

```markdown
## Auto-Applied Corrections

| Section | Change Made | Source Evidence | Status |
|---------|-------------|-----------------|--------|
| Error Type 4 | Added "Spaces only" error message | Codebase: validation.py:234 | ✅ Applied |
| Error Type 7 | Added exiftool/mogrify commands | Validated version reference | ✅ Applied |
| Troubleshooting | Added decision tree | Best practice from validation | ✅ Applied |

## Flagged for Manual Review (Images/Videos)

| Section | Suggestion | Why Manual | Priority |
|---------|------------|------------|----------|
| Error Type 1 | Screenshot of import log | Requires screen capture | MEDIUM |
```

---

## STEP 8: UPDATE NOTION WITH VALIDATION RESULTS

**After validation and auto-applying corrections, update the Notion page with a complete audit trail.**

### Notion Update Location

Add to the **TOP** of the Notion page (after any existing header/metadata) so the audit trail follows **newest to oldest** order.

### Required Notion Content

Insert this structure at the TOP of the Notion page (simple table format):

```markdown
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
| 4 | [Incorrect item] | Codebase | ✅ Corrected | Was wrong format |
| ... | [Continue for all sections and claims] | | | |

---

#### Auto-Applied Additions

| Section | What Was Added | Why |
|---------|----------------|-----|
| [Section] | [Description] | [Source evidence] |

---

#### Flagged for Manual (Screenshots - MAX 3)

**⚠️ These are marked in the Craft draft as: `⚠️ [PLACEHOLDER - DO NOT PUBLISH] Screenshot needed:`**

Search for "PLACEHOLDER" in the Craft draft to find all locations.

| Section | Screenshot Needed | Priority |
|---------|-------------------|----------|
| [Section] | [What to capture] | HIGH/MEDIUM/LOW |
```

**Note:** Do NOT include the full draft content in Notion. The validation table is the audit trail. Full content is in Craft.

**⚠️ Image Placeholder Format in Craft:**
```html
<p><strong>⚠️ [PLACEHOLDER - DO NOT PUBLISH] Screenshot needed:</strong> <em>Description.</em></p>
```
This format is impossible to miss and Kyla can search for "PLACEHOLDER" to find all items needing attention.

### Notion Update Process

1. Use Notion MCP to insert at TOP of page
2. Include validation table (sections + claims)
3. Include auto-applied additions table
4. Include flagged items table (screenshots only)
5. Do NOT include full draft content (that lives in Craft)

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
| 1 | [claim] | Field Name | Codebase | [evidence] | 95% | ✅ Verified |
| 2 | [claim] | Error Msg | Help Scout | [evidence] | 85% | ⚠️ Corrected |
| 3 | [claim] | Procedure | Fathom | [evidence] | 90% | ✅ Verified |
| 4 | [missing] | Gap | Codebase | [evidence] | N/A | ➕ Added |
| 5 | [visual] | Image | N/A | Best practice | N/A | 📸 Flagged |

---

## Critical Issues (Must Fix Before Publishing)

| Issue | Location | Source Evidence | Required Fix |
|-------|----------|-----------------|--------------|
| [issue] | [section] | [source says X] | [what to change] |

---

## Auto-Applied Corrections

| Section | Change | Source Evidence | Status |
|---------|--------|-----------------|--------|
| [section] | [change] | [source] | ✅ Applied |

---

## Flagged for Manual Review (Images/Videos Only)

| Section | Suggestion | Why Manual | Priority |
|---------|------------|------------|----------|
| [section] | [what to add] | Requires capture | HIGH/MEDIUM/LOW |

---

## Verification Details

### Codebase Validation
[Results from Step 2]

### Help Scout Validation  
[Results from Step 3]

### Fathom Validation
[Results from Step 4]

### MCP Validation
[Results from Step 5]

---

## Missing Content (Recommended Additions)

| Topic | Source | Evidence | Priority | Auto-Applied? |
|-------|--------|----------|----------|---------------|
| [topic] | [source] | [evidence] | HIGH | ✅ Yes |
| [topic] | [source] | [evidence] | MEDIUM | 📸 Manual |

---

## Validation Certification

I certify that:
- [ ] ALL field names verified against codebase
- [ ] ALL error messages verified against Help Scout OR codebase
- [ ] ALL procedures verified against support patterns
- [ ] ALL numeric claims verified against codebase
- [ ] NO claims approved without tool call evidence
- [ ] ALL non-manual corrections auto-applied to Craft
- [ ] Validation table added to Notion page (TOP)

**Validator:** [AI Model]
**Date:** [DATE]
```

---

## QUICK REFERENCE: Validation Queries

### Codebase Search Commands

```bash
# Field name search
grep -r "FIELD_NAME" --include="*.py" --include="*.js" .

# Error message search
grep -r "error text" --include="*.py" .

# Configuration constants
grep -r "MAX_\|LIMIT_\|DEFAULT_" --include="*.py" --include="*.config*" .

# Feature flags
grep -r "enable_\|feature_\|flag_" --include="*.py" .
```

### BigQuery Templates

```sql
-- Error pattern search
SELECT ticket_number, ticket_subject, LEFT(ticket_preview, 300)
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE LOWER(ticket_preview) LIKE '%[SEARCH_TERM]%'
AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
LIMIT 30

-- Support response search
SELECT conversation_id, SUBSTR(body, 1, 1000), type
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.conversation_threads`
WHERE LOWER(body) LIKE '%[SEARCH_TERM]%'
AND type = 'message'
LIMIT 30
```

### Fathom API Commands

```python
# Get meetings
from fathom_api import get_meetings
meetings = get_meetings(limit=200, paginate=True)

# Get summary
from fathom_api import get_summary
summary = get_summary([RECORDING_ID])

# Get transcript
from fathom_api import get_transcript
transcript = get_transcript([RECORDING_ID])
```

---

## WORKFLOW SUMMARY

```
0. FETCH article content from Craft CMS URL (GraphQL)
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
8. UPDATE Notion with validation table + full draft
   ↓
9. CALCULATE confidence score
   ↓
10. GENERATE validation report
   ↓
11. DECISION: Publish / Review / Revise
```

### Auto-Apply Decision Tree

```
For each issue found:
  ↓
Is it a text/content correction?
  ├── YES: Can be fixed without screenshots/videos?
  │         ├── YES → AUTO-APPLY to Craft
  │         └── NO → FLAG for manual review
  └── NO: Is it a missing image/video?
          └── YES → FLAG for manual review (📸)
```

---

## COMMON VALIDATION FAILURES

### Failure 1: Field Name Casing
**Problem:** Article says 'imagefile' but codebase has 'ImageFile'
**Impact:** Users can't find the field
**Fix:** Always use exact casing from codebase

### Failure 2: Outdated Error Messages
**Problem:** Error text was updated in recent release
**Detection:** Help Scout shows new error text, article has old
**Fix:** Update to current error message text

### Failure 3: Missing Edge Cases
**Problem:** Article covers happy path but not exceptions
**Detection:** Help Scout tickets show repeated questions about edge case
**Fix:** Add troubleshooting section for edge case

### Failure 4: Incorrect Limits
**Problem:** Article says "6 images max" but system allows 12
**Detection:** Codebase shows configurable limit, some orgs have 12
**Fix:** Update to "6 images (or 12 if extended limit enabled)"

### Failure 5: Wrong Navigation Path
**Problem:** UI was reorganized, old path doesn't work
**Detection:** MCP/codebase shows different menu structure
**Fix:** Update navigation path to current UI

---

**Document Status:** Production Ready
**Version:** 1.1
**Created:** January 18, 2026
**Updated:** January 19, 2026
**Author:** SuperCat KB Validation Pipeline

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 18, 2026 | Initial release |
| 1.1 | Jan 19, 2026 | Added: Step 7 (Auto-Apply Corrections), Step 8 (Notion Update with validation table + full draft), Auto-Apply decision tree, Enhanced output template |
