# V11.3 Stage-Gated Pipeline Assessment Prompt

**Purpose:** Use this prompt to run a complete onboarding pipeline assessment with Fathom + Help Scout validation.

**Last Updated:** January 14, 2026

---

## 📋 COPY THIS PROMPT:

```
Run a V11.3 Stage-Gated Pipeline Assessment for the following active implementations:

**Clients to assess:**
- [Client 1 Name] (shortname: xxx)
- [Client 2 Name] (shortname: xxx)
- [Client 3 Name] (shortname: xxx)
[add more as needed]

**Reference Documents:**
- @Onboarding Readiness Models/FRD_V11_Fast_Stage_Gated_Onboarding.md (methodology)
- @Onboarding Readiness Models/FRD_V10_Stage_Gated_Onboarding.md (stage definitions)

**Required Data Sources (ALL MANDATORY):**

1. **MCP Endpoints** - Run in parallel batches:
   - Batch 1: get_organization_info, get_org_users, get_data_summary
   - Batch 2: get_price_levels, get_categories, get_collections, get_options
   - Batch 3: get_user_territories, get_import_events, get_inventories
   - Batch 4: get_mobile_sites, get_reports_config, get_orders

2. **BigQuery** - Consolidated query:
   - Mixpanel iPad activity (order_submitted events)
   - Help Scout tickets (BOTH Support AND Onboarding mailboxes, last 90 days)

3. **Fathom API** (MANDATORY - via /fathom/fathom_api.py):
   - Run get_meetings() for ALL clients
   - Run get_summary() for EVERY call found (not just titles)
   - NEVER assume status from meeting titles - "[Hold]" is a calendar placeholder, NOT implementation status
   - Extract exact quotes with dates for validation flags

4. **Help Scout BigQuery** (MANDATORY - BOTH mailboxes):
   - Query SuperCat Support mailbox
   - Query SuperCat Onboarding mailbox (file uploads are critical engagement indicators!)
   - Never conclude "no activity" without checking both

**Output Format:**
Match exactly the V7 Notion page format:
https://www.notion.so/svcapital/V7-Pipeline-Assessment-with-Validation-Flags-January-7-2026-2e2231dbcd708166bdced7eaab6d3963

Include:
1. Pipeline Overview table (Client | Stage | Readiness | Validation Status | Key Flag)
2. ASCII pipeline visualization with progress bars
3. Per-client sections with:
   - Stage table (Stage | Status | Evidence)
   - 🎯 Next Action
   - Validation Flags table (Stage | Flag | Source | Evidence) with EXACT QUOTES and dates
   - Validation Summary
4. Validation Flags Summary (Critical, Review, Confirmed sections)
5. Key Takeaways

**Critical Rules:**
- Every validation flag MUST include the actual quote from the source with date
- NEVER skip Fathom summary retrieval - get_summary() for every call found
- NEVER skip Help Scout - file uploads in Onboarding mailbox are engagement indicators
- NEVER assume "[Hold]" in meeting title means implementation is stalled
- NEVER conclude "no activity" without checking Fathom + Help Scout Support + Help Scout Onboarding
```

---

## 📝 EXAMPLE (FILLED IN):

```
Run a V11.3 Stage-Gated Pipeline Assessment for the following active implementations:

**Clients to assess:**
- Donald Choi Canada (shortname: dccl)
- Terracotta Designs (shortname: tcd)
- Pebl Furniture (shortname: pebl)
- Magic Lite (shortname: mali)
- Kaleen Rugs & Broadloom (shortname: krb)
- Coaster Furniture (shortname: cst)
- Jonathan Charles Design (shortname: jcusa)

**Reference Documents:**
- @Onboarding Readiness Models/FRD_V11_Fast_Stage_Gated_Onboarding.md (methodology)
- @Onboarding Readiness Models/FRD_V10_Stage_Gated_Onboarding.md (stage definitions)

**Required Data Sources (ALL MANDATORY):**

1. **MCP Endpoints** - Run in parallel batches:
   - Batch 1: get_organization_info, get_org_users, get_data_summary
   - Batch 2: get_price_levels, get_categories, get_collections, get_options
   - Batch 3: get_user_territories, get_import_events, get_inventories
   - Batch 4: get_mobile_sites, get_reports_config, get_orders

2. **BigQuery** - Consolidated query:
   - Mixpanel iPad activity (order_submitted events)
   - Help Scout tickets (BOTH Support AND Onboarding mailboxes, last 90 days)

3. **Fathom API** (MANDATORY - via /fathom/fathom_api.py):
   - Run get_meetings() for ALL clients
   - Run get_summary() for EVERY call found (not just titles)
   - NEVER assume status from meeting titles - "[Hold]" is a calendar placeholder, NOT implementation status
   - Extract exact quotes with dates for validation flags

4. **Help Scout BigQuery** (MANDATORY - BOTH mailboxes):
   - Query SuperCat Support mailbox
   - Query SuperCat Onboarding mailbox (file uploads are critical engagement indicators!)
   - Never conclude "no activity" without checking both

**Output Format:**
Match exactly the V7 Notion page format:
https://www.notion.so/svcapital/V7-Pipeline-Assessment-with-Validation-Flags-January-7-2026-2e2231dbcd708166bdced7eaab6d3963

Include:
1. Pipeline Overview table (Client | Stage | Readiness | Validation Status | Key Flag)
2. ASCII pipeline visualization with progress bars
3. Per-client sections with:
   - Stage table (Stage | Status | Evidence)
   - 🎯 Next Action
   - Validation Flags table (Stage | Flag | Source | Evidence) with EXACT QUOTES and dates
   - Validation Summary
4. Validation Flags Summary (Critical, Review, Confirmed sections)
5. Key Takeaways

**Critical Rules:**
- Every validation flag MUST include the actual quote from the source with date
- NEVER skip Fathom summary retrieval - get_summary() for every call found
- NEVER skip Help Scout - file uploads in Onboarding mailbox are engagement indicators
- NEVER assume "[Hold]" in meeting title means implementation is stalled
- NEVER conclude "no activity" without checking Fathom + Help Scout Support + Help Scout Onboarding
```

---

## 🚨 LESSONS LEARNED (Why These Rules Exist)

### 1. "[Hold]" in Meeting Titles
**Problem:** Assumed "[Hold] eCat x Coaster Standup" meant implementation was paused.
**Reality:** "[Hold]" is just a calendar placeholder for recurring meetings. The actual call showed ACTIVE progress toward Vegas market launch.
**Fix:** ALWAYS retrieve `get_summary()` for every call - never assume from title.

### 2. Help Scout Onboarding Mailbox
**Problem:** Only checked Fathom and concluded Magic Lite had "no activity."
**Reality:** Magic Lite uploaded 30+ product images on Jan 6 and was scheduling a meeting.
**Fix:** Query BOTH Help Scout mailboxes (Support + Onboarding). File uploads are critical engagement indicators.

### 3. Validation Without Evidence
**Problem:** Flagged issues without actual quotes.
**Reality:** Flags without evidence are not actionable.
**Fix:** Every flag MUST include the exact quote, source, and date.

---

## 📊 Expected Output Format

The output should look like this:

```
# Q1 2026 Onboarding Pipeline Assessment
## V11.3 Fast Mode Stage-Gated Model + Fathom + Help Scout Validation

**Date:** [Today's Date]
**Methodology:** V11.3 Fast Mode (MCP + BigQuery + Fathom API + Help Scout BOTH Mailboxes)

---

## Pipeline Overview

| Client | V11 Stage | V11 Readiness | Validation Status | Key Flag |
|--------|-----------|---------------|-------------------|----------|
| **XXX** | X (Stage Name) | XX% | ✅/⚠️/🔴 X flags | Key issue summary |

---

PIPELINE VIEW (V11.3 Fast Mode Assessment)
═══════════════════════════════════════════════════════════════════

XXX   ██████████████████░░ 90%  Stage X - Name  ✅ STATUS

═══════════════════════════════════════════════════════════════════

[Per-client sections...]

[Validation Flags Summary...]

[Key Takeaways...]
```

---

## 🔗 Related Documents

- `/Onboarding Readiness Models/FRD_V11_Fast_Stage_Gated_Onboarding.md` - Full methodology
- `/Onboarding Readiness Models/FRD_V10_Stage_Gated_Onboarding.md` - Stage definitions
- `/Onboarding Readiness Models/V10_Stage_Gated_Checklist.md` - Checklist version
