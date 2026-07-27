# Notion Output Format

**Purpose:** Format all assessment data into exact Notion output  
**Input:** Data from `Stage_Gated_Data_Collection.md` + `Validation_Layer_Fathom_HelpScout.md`  
**Output:** Copy-paste ready content for Notion page

---

## ⛔ THIS DOCUMENT RUNS LAST

**Prerequisites:**
1. ✅ `Stage_Gated_Data_Collection.md` completed (all MCP/BigQuery metrics)
2. ✅ `Validation_Layer_Fathom_HelpScout.md` completed (all validation flags)

**If prerequisites not met:** STOP. Complete previous documents first.

---

## NOTION PAGE TO UPDATE

**Page URL:** https://www.notion.so/svcapital/Working-Notion-Stage-Gated-Document-2ef231dbcd708035a168c4336a3afc6c

**Page ID:** `2ef231dbcd708035a168c4336a3afc6c`

**Reference Format Page:** https://www.notion.so/svcapital/Desired-Output-For-Cursor-2e8231dbcd7080308e08dac6449094e7

**Update Method:** Replace the entire content below the page title with the formatted output from this document.

---

## ⛔ FORMATTING RULES

```
⛔ FORBIDDEN: Adding commentary or explanations not in templates
⛔ FORBIDDEN: Changing table column order
⛔ FORBIDDEN: Omitting any section from the template
⛔ FORBIDDEN: Using different emoji or status indicators
⛔ FORBIDDEN: Changing the date format (must be "Month DDth, YYYY")
⛔ FORBIDDEN: Changing section headers or their order
```

**Rule:** Copy templates EXACTLY. Only replace `[PLACEHOLDERS]` with actual data.

---

## SECTION 1: PAGE HEADER

**Format:** Use the assessment date in format "Month DDth, YYYY - Full Product Suite"

```markdown
# [Month] [DD]th, [YYYY] - Full Product Suite
```

**Example:** `# January 21st, 2026 - Full Product Suite`

**Date suffix rules:**
- 1st, 21st, 31st
- 2nd, 22nd
- 3rd, 23rd
- All others: th (4th, 5th, 6th, etc.)

---

## SECTION 2: PIPELINE OVERVIEW TABLE

### Table Format (Copy Exactly)

```markdown
## Pipeline Overview

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **[SHORTNAME]** | [Product] | [Owner] | [X] / [Y] | [X]% | [Blocker text] | [Status] | [Days] |
```

### Column Definitions

| Column | Format | Example |
|--------|--------|---------|
| Client | **Bold shortname** (all caps) | **PEBL** |
| Product | eCat / eOL / Sales Portal | eCat |
| Owner | CSM first name | Brent |
| V11 Stage | Current / Total (with space around /) | 2 / 7 |
| V11 Readiness | Percentage with % | 40% |
| Biggest Blocker | Specific blocker description | 0 price levels, 0 customers |
| Validation Status | Flag count with emoji | 🔴 2 flags / ⚠️ 2 flags / ✅ Confirmed |
| Days Active | Days since account created | ~90 / 180+ (dormant) / 365+ |

### Biggest Blocker Text Examples

| Situation | Biggest Blocker Text |
|-----------|----------------------|
| Missing pricing | 0 price levels, 0 customers, 0 engagement |
| Missing customers | 0 customers, 0 sales reps |
| Pricing not configured | 0 price levels configured |
| Pricing mismatch | Contract Pricing not configured (using standard levels) |
| eCat Online issues | Server caching issues on taxonomy |
| Integration blocker | Push-to-API integration for warehouse code |
| Verification pending | Stage 11-12: Portal data verification pending |

### Validation Status Format

| Condition | Format |
|-----------|--------|
| Critical flags present | 🔴 X flags |
| Warning flags present | ⚠️ X flags |
| No flags / confirmed | ✅ Confirmed |

### Days Active Format

| Situation | Format |
|-----------|--------|
| Normal active | ~90 |
| Long-standing client | 365+ |
| Dormant client | 180+ (dormant) |

### Sorting Rule

**Sort by V11 Readiness percentage ascending** (lowest at top, highest at bottom)

---

## SECTION 3: PIPELINE VIEW VISUALIZATION

### Format (Copy Exactly)

```markdown
## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

[SHORTNAME] [PROGRESS_BAR] [XX]%  Stage [X] - [Stage Name]    [STATUS_EMOJI] [STATUS_TEXT]

═══════════════════════════════════════════════════════════════════
```

### Progress Bar Construction

- Total width: 20 characters
- Filled portion: █ (solid block)
- Empty portion: ░ (light shade) or blank space with gray background
- Round percentage to nearest 5%

| Percentage | Filled Blocks | Bar |
|------------|---------------|-----|
| 10% | 2 | ██░░░░░░░░░░░░░░░░░░ |
| 25% | 5 | █████░░░░░░░░░░░░░░░ |
| 40% | 8 | ████████░░░░░░░░░░░░ |
| 50% | 10 | ██████████░░░░░░░░░░ |
| 60% | 12 | ████████████░░░░░░░░ |
| 70% | 14 | ██████████████░░░░░░ |
| 85% | 17 | █████████████████░░░ |
| 95% | 19 | ███████████████████░ |

### Status Labels (Use These Exactly)

| Condition | Status |
|-----------|--------|
| 🔴 flags OR no activity 30+ days | 🔴 STALLED |
| 🔴 flags (active engagement) | 🔴 FLAGGED |
| Recent activity with warnings | ⚠️ ACTIVE ENGAGEMENT |
| Yellow flags present | ⚠️ FLAGGED |
| Support tickets active | ⚠️ SUPPORT ACTIVE |
| Market/launch prep | ⚠️ MARKET PREP |
| All green, confirmed | ✅ CONFIRMED |

### Stage Names

| Stage | Name |
|-------|------|
| 1 | Account Foundation |
| 2 | Catalog Setup |
| 3 | Pricing |
| 4 | Options |
| 5 | Customer Setup |
| 6 | Operations |
| 7 | Order Ready |
| 8 | eCat Online Site |
| 9 | eCat Online Access |
| 10 | eCat Online Ordering |
| 11 | Sales Portal Data |

---

## SECTION 4: PER-CLIENT ASSESSMENTS

### Template (Repeat for Each Client, Sorted by Readiness)

```markdown
## [SHORTNAME] ([Full Company Name])

**V11 Assessment:** Stage [X] | [X]% Ready | Products: [Product list]

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | [🟢/🟡/🔴] | [evidence text] |
| 2 | [🟢/🟡/🔴] | [evidence text] |
| 3 | [🟢/🟡/🔴] | [evidence text] |
| 4 | [🟢/🟡/🔴/⚫] | [evidence text or "N/A"] |
| 5 | [🟢/🟡/🔴] | [evidence text] |
| 6 | [🟢/🟡/🔴] | [evidence text] |
| 7 | [🟢/🟡/🔴/⚫] | [evidence text] |

🎯 **V11 Next Action:** [Specific action item]

[FLAG_SECTION]

**Validation Summary:** [2-3 sentence summary]
```

### Status Emoji Rules

| Status | Emoji | When to Use |
|--------|-------|-------------|
| Pass | 🟢 | Stage fully passed |
| Warning | 🟡 | Stage passed with warnings/caveats |
| Fail/Blocker | 🔴 | Stage failed, blocker identified |
| N/A | ⚫ | Stage not applicable (use gray circle) |

### Evidence Text Formatting

**For RED blockers, use bold and include criteria:**
```
**0 price levels** (Stage 3 criteria: RED BLOCKER - Cannot proceed)
```

**For YELLOW warnings, include context:**
```
222 options - but being removed entirely (Stage 4 criteria: Options "removing size options entirely" - current data will be invalidated)
```

**For GREEN passes, keep brief:**
```
Company exists
1,183 products
4 price levels (Dealer Net, Designer, IMAP, Showroom)
```

**For stages with additional Fathom/Help Scout context:**
```
19 price levels configured - but Fathom Dec 3 indicates client wants Contract Pricing feature instead (Stage 3 criteria: Price levels exist but may not align - 🔴 CONTRADICT with Fathom)
```

### V11 Next Action Formatting

Always start with `🎯 **V11 Next Action:**`

**Examples:**
- `🎯 **V11 Next Action:** 🚫 OUTREACH REQUIRED - Confirm client engagement`
- `🎯 **V11 Next Action:** Import customer data (Stage 5 blocker) - but wait for product restructure to complete first`
- `🎯 **V11 Next Action:** Configure price levels (Stage 3 blocker) - client is actively engaged`
- `🎯 **V11 Next Action:** Complete push-to-API order integration for Jan 25-28 Vegas Market launch`
- `🎯 **V11 Next Action:** Validate Stage 11-12 (Sales Portal) - verify data import against ERP, configure user groups with portal access permissions, test SSO`

### Flag Section Templates

**If client has 🔴 critical flags:**
```markdown
🔴 **Validation Flags ([X])**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| [X] | 🔴 [FLAG_TYPE] | [Source] [Date] | "[Quote or description]" |
```

**If client has ⚠️ review flags only:**
```markdown
⚠️ **Validation Flags ([X])**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| [X] | ⚠️ [FLAG_TYPE] | [Source] [Date] | "[Quote or description]" |
```

**If client has ⚠️ flags with "CORRECTED" status:**
```markdown
⚠️ **Validation Flags ([X]) - CORRECTED**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| [X] | ✅ ACTIVE | [Source] [Date] | [Description] |
```

**If client has no flags:**
```markdown
✅ **No Validation Flags**

- **Fathom:** No calls in [X] days (mature production client - normal)
- **Help Scout:** No recent tickets (stable production - normal)
```

### Sentiment Flag (Add When Negative Sentiment Detected)

```markdown
🚨 **Sentiment Flag:**

| Source | Evidence |
| --- | --- |
| [Source] [Date] | "[Exact quote showing negative sentiment]" |
```

### Additional Context Section (Add When Helpful)

```markdown
**Additional Help Scout Context ([Date]):**

- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]
```

### Validation Summary with Bullets (For Corrected Assessments)

```markdown
**Validation Summary:** CORRECTED ASSESSMENT - [CLIENT] is actively engaged, NOT stalled:

- **[Date]:** [Activity description]
- **[Date]:** [Activity description]
- [Additional context point]
- Readiness raised from [X]% to [Y]% due to active engagement
```

---

## SECTION 5: VALIDATION FLAGS SUMMARY

### Template (Copy Exactly)

```markdown
## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| [SHORTNAME] | [X] | [Issue description] | "[Quote]" | [Action required] |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| [SHORTNAME] | [X] | [Issue description] | "[Quote]" | [Action required] |

### ✅ Confirmed (No Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| [SHORTNAME] | Stage [X] | [X]% | [Brief status] |
```

### Issue Text Examples

| Type | Issue Text |
|------|------------|
| No activity | Zero activity (6 months) |
| Restructure | Product restructure |
| Churn risk | Churn risk |
| Pricing conflict | Pricing contradiction |
| Meeting scheduled | Meeting scheduled |
| Deadline passed | Dec 15 deadline passed |
| Caching issues | eCat Online caching |
| Timeline pressure | Vegas market deadline |
| Technical blocker | Warehouse workaround |
| Portal expansion | Sales Portal expansion |

### Action Text Examples

| Type | Action Text |
|------|-------------|
| Confirm engagement | Confirm engagement |
| Pause | Pause until complete |
| Executive attention | Executive escalation |
| CSM clarification | CSM clarification required |
| Track | Track follow-up |
| Confirm status | Confirm current status |
| Monitor | Monitor resolution |
| Daily monitoring | Monitor daily |
| Confirm completion | Confirm completion |
| Validate criteria | Validate Stage 11-12 criteria |

---

## FULL OUTPUT ASSEMBLY ORDER

Assemble sections in this exact order:

1. **Section 1:** Page Header (date with "Full Product Suite")
2. **Section 2:** Pipeline Overview Table
3. **Section 3:** Pipeline View Visualization
4. **Section 4:** Per-Client Assessments (sorted by readiness, lowest first)
5. **Section 5:** Validation Flags Summary

---

## PRE-OUTPUT CHECKLIST

Before copying to Notion, verify:

- [ ] Header date uses format "Month DDth, YYYY - Full Product Suite"
- [ ] Pipeline Overview table has all 8 columns: Client, Product, Owner, V11 Stage, V11 Readiness, Biggest Blocker, Validation Status, Days Active
- [ ] Pipeline Overview table sorted by V11 Readiness (ascending)
- [ ] Pipeline View bars match percentages
- [ ] All clients from HubSpot are included
- [ ] Per-client assessments sorted by V11 Readiness (ascending)
- [ ] Per-client header uses "V11 Assessment:" format
- [ ] Stage statuses use correct emoji (🟢/🟡/🔴/⚫)
- [ ] RED blockers are **bold** with criteria explanation
- [ ] Next Action starts with 🎯 **V11 Next Action:**
- [ ] Flag sections use correct header format
- [ ] Validation Flags Summary has all three subsections
- [ ] No sections are missing

---

## COMPLETE EXAMPLE (Reference Only)

This shows what a completed output looks like. Match this structure exactly.

```markdown
# January 21st, 2026 - Full Product Suite

## Pipeline Overview

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **PEBL** | eCat | Brent | 0 / 7 | 10% | 0 price levels, 0 customers, 0 engagement | 🔴 2 flags | 180+ (dormant) |
| **TCD** | eCat | Brent | 4 / 7 | 25% | 0 customers, 0 sales reps | 🔴 3 flags | ~90 |
| **MALI** | eCat | Brent | 2 / 7 | 40% | 0 price levels configured | ⚠️ 2 flags | ~30 |
| **KRB** | eCat | Chuck | 6 / 7 | 60% | Contract Pricing not configured (using standard levels) | ⚠️ 2 flags | ~90 |
| **DCCL** | eOL | Chuck | 6 / 8 | 70% | Server caching issues on taxonomy | ⚠️ 2 flags | ~120 |
| **CST** | eCat | Brent | 7 / 7 | 85% | Push-to-API integration for warehouse code | ⚠️ 2 flags | ~180 |
| **JCUSA** | Sales Portal | Chuck | 9 / 9 | 95% | Stage 11-12: Portal data verification pending | ✅ Confirmed | 365+ |

## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

PEBL  ██░░░░░░░░░░░░░░░░░░ 10%  Stage 3 - Pricing              🔴 STALLED

TCD   █████░░░░░░░░░░░░░░░ 25%  Stage 5 - Customer Setup       🔴 FLAGGED

MALI  ████████░░░░░░░░░░░░ 40%  Stage 3 - Pricing              ⚠️ ACTIVE ENGAGEMENT

KRB   ████████████░░░░░░░░ 60%  Stage 7 - Order Ready          ⚠️ FLAGGED

DCCL  ██████████████░░░░░░ 70%  Stage 8 - eCat Online Site     ⚠️ SUPPORT ACTIVE

CST   █████████████████░░░ 85%  Stage 7 - Order Ready          ⚠️ MARKET PREP

JCUSA ███████████████████░ 95%  Stage 11 - Sales Portal Data   ✅ CONFIRMED

═══════════════════════════════════════════════════════════════════

## PEBL (Pebl Furniture)

**V11 Assessment:** Stage 3 | 10% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟢 | 1,183 products |
| 3 | 🔴 | **0 price levels** (Stage 3 criteria: RED BLOCKER - Cannot proceed) |
| 4 | 🟢 | 15 options |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER - Cannot proceed) |
| 6 | 🔴 | **0 inventory** |
| 7 | 🔴 | No orders |

🎯 **V11 Next Action:** 🚫 OUTREACH REQUIRED - Confirm client engagement

🔴 **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | 🔴 STALLED | Fathom | Only 1 call in 6 months (July 2025 demo) |
| - | 🔴 STALLED | Help Scout | 0 tickets found in last 180 days - no Onboarding/Support activity |

**Validation Summary:** PEBL has zero activity across ALL sources (Fathom + Help Scout Support + Help Scout Onboarding). This is a confirmed disengaged client. Last known: "Radio silence since notice of ERP transition."

---

## TCD (Terracotta Designs)

**V11 Assessment:** Stage 5 | 25% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active |
| 2 | 🟡 | 441 products - but restructure planned (Stage 2 criteria: Product "Each size will become separate product" per Fathom Dec 18) |
| 3 | 🟢 | 4 price levels (Dealer Net, Designer, IMAP, Showroom) |
| 4 | 🟡 | 222 options - but being removed entirely (Stage 4 criteria: Options "removing size options entirely" - current data will be invalidated) |
| 5 | 🔴 | **0 customers, 0 sales reps** (Stage 5 criteria: RED BLOCKER - Cannot proceed without customers and 2 users) |
| 6 | 🟡 | 348 inventory records - may need refresh after product restructure |
| 7 | 🔴 | No orders |

🎯 **V11 Next Action:** Import customer data (Stage 5 blocker) - but wait for product restructure to complete first

🔴 **Validation Flags (3)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | 🔴 CONTRADICT | Fathom Dec 18 | "Product Page Redesign: Each size will become separate product" |
| 4 | 🔴 CONTRADICT | Fathom Dec 18 | "Removing size options entirely." |
| 7 | ⚠️ TIMELINE | Help Scout Dec 27 | "We may need to push this to later next month." |

🚨 **Sentiment Flag:**

| Source | Evidence |
| --- | --- |
| Help Scout Dec 21 | "The tool feels less like a mature commercial product and more like an early-stage amateur implementation." |

**Validation Summary:** Stage 5 blocker confirmed. Product restructure pending. Churn risk - recommend executive attention.

---

## MALI (Magic Lite)

**V11 Assessment:** Stage 3 | 40% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, status: onboarding |
| 2 | 🟢 | 906 products, 12 categories - actively uploading images (30+ files uploaded Jan 6) |
| 3 | 🔴 | **0 price levels** (Stage 3 criteria: RED BLOCKER - Cannot proceed without price level configured) |
| 4 | ⚫ N/A | Options not configured |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER - Cannot proceed without customer import) |
| 6 | 🔴 | **0 inventory** |
| 7 | 🔴 | No orders |

🎯 **V11 Next Action:** Configure price levels (Stage 3 blocker) - client is actively engaged

⚠️ **Validation Flags (2) - CORRECTED**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ✅ ACTIVE | Help Scout Onboarding (Jan 6) | 30+ file uploads - product images being uploaded. Files include: "FR-LED-4-S12W-5CCT-PL", "TLE-1625-XXK-BN", "GDL gimbal lights", etc. |
| - | ⚠️ MEETING | Help Scout (Jan 14) | Brent scheduling meeting with Magic Lite to review progress |

**Validation Summary:** CORRECTED ASSESSMENT - MALI is actively engaged, NOT stalled:

- **Jan 6:** 30+ product images uploaded to onboarding portal
- **Jan 14:** Meeting being scheduled with Brent
- Stage 3 blocker (0 price levels) is accurate, but client is actively progressing on Stage 2 (catalog)
- Readiness raised from 25% to 40% due to active engagement

---

## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| PEBL | - | Zero activity (6 months) | 0 Fathom + 0 Help Scout | Confirm engagement |
| TCD | 2 | Product restructure | "Each size becomes separate product" | Pause until complete |
| TCD | - | Churn risk | "Amateur implementation" | Executive escalation |
| KRB | 3 | Pricing contradiction | Fathom: "Use Contract Pricing" vs System: 19 standard levels | CSM clarification required |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| MALI | - | Meeting scheduled | Brent scheduling review | Track follow-up |
| KRB | 7 | Dec 15 deadline passed | "Deliver by December 15" | Confirm current status |
| DCCL | 8 | eCat Online caching | Support investigating | Monitor resolution |
| CST | 7 | Vegas market deadline | "Jan 25-28 market" | Monitor daily |
| CST | 7 | Warehouse workaround | Custom field in progress | Confirm completion |
| JCUSA | 11-12 | Sales Portal expansion | Data/user verification pending | Validate Stage 11-12 criteria |

### ✅ Confirmed (No Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| MALI | Stage 3 | 40% | ACTIVE - 30+ file uploads, meeting scheduled |
| CST | Stage 7 | 85% | Active market prep |
| JCUSA | Stage 11 | 95% | Production live |
```

---

## TROUBLESHOOTING

### Issue: Emoji Not Rendering Correctly

Use these exact Unicode characters:
- Green circle: 🟢 (U+1F7E2)
- Yellow circle: 🟡 (U+1F7E1)
- Red circle: 🔴 (U+1F534)
- Black circle (N/A): ⚫ (U+26AB)
- Target: 🎯 (U+1F3AF)
- Warning: ⚠️ (U+26A0 U+FE0F)
- Check: ✅ (U+2705)
- No entry: 🚫 (U+1F6AB)
- Siren: 🚨 (U+1F6A8)

### Issue: Progress Bar Alignment

Ensure:
- SHORTNAME is left-padded to 5 characters
- Percentage is right-padded to 3 characters
- Stage name is consistent

### Issue: Tables Not Rendering

Ensure:
- Header row has `| --- |` separator
- All rows have same number of columns
- No empty cells (use "-" if needed)

---

**Document Purpose:** Output formatting only  
**Target Page:** https://www.notion.so/svcapital/Working-Notion-Stage-Gated-Document-2ef231dbcd708035a168c4336a3afc6c  
**Page ID:** 2ef231dbcd708035a168c4336a3afc6c
