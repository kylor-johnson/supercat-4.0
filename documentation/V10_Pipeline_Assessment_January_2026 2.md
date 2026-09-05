# V10 Pipeline Assessment with Validation Flags - January 14, 2026

## Q1 2026 Onboarding Pipeline
### V10 Stage-Gated Model + Fathom Validation Layer
**Date:** January 14, 2026  
**Methodology:** V10 data-driven assessment via MCP + Fathom call validation (last 90 days)

---

## Pipeline Overview

| Client | V10 Stage | Readiness | Fathom Status | Key Finding |
|--------|-----------|-----------|---------------|-------------|
| **JCUSA** | 12 (Live) | 95% | ⚪ No recent calls | Mature - in maintenance mode |
| **DCCL** | 11 (Multi-Product) | 90% | ✅ Active (Dec 9) | B2B config in progress |
| **CST** | 9 (Testing) | 65% | 🔴 Blocker (Jan 13) | Order integration needed for Vegas |
| **TCD** | 5 (Customer Setup) | 45% | 🟡 Delayed (Dec 18) | Dallas Market pushed timeline |
| **KRB** | 5 (Pricing) | 40% | 🔴 Stalled (Dec 3) | Dec 15 target missed |
| **MALI** | 2 (Evaluation) | 20% | 🟡 Early (Oct 10) | Still in sales/evaluation |
| **PEBL** | 2 (Catalog) | 15% | 🔴 Stalled | No calls in 6+ months |

---

```
PIPELINE VIEW (V10 + Fathom Validation)
═══════════════════════════════════════════════════════════════

JCUSA ███████████████████░ 95%  Stage 12 - LIVE           ⚪ Maintenance
DCCL  ██████████████████░░ 90%  Stage 11 - Multi-Product  ✅ Active
CST   █████████████░░░░░░░ 65%  Stage 9 - Testing         🔴 BLOCKER
TCD   █████████░░░░░░░░░░░ 45%  Stage 5 - Customer Setup  🟡 Delayed
KRB   ████████░░░░░░░░░░░░ 40%  Stage 5 - Pricing         🔴 STALLED
MALI  ████░░░░░░░░░░░░░░░░ 20%  Stage 2 - Evaluation      🟡 Early
PEBL  ███░░░░░░░░░░░░░░░░░ 15%  Stage 2 - Catalog         🔴 STALLED

═══════════════════════════════════════════════════════════════
```

---

# JCUSA (Jonathan Charles Designs)
## V10 Assessment: Stage 12 | 95% Ready

| Stage | Status | Evidence |
|-------|--------|----------|
| 1-6 | 🟢 | Foundation complete: 20,142 products, 8 price levels, 4,587 customers |
| 7 | 🟢 | iPad live: 112 orders, 18 unique users |
| 8-9 | 🟢 | Mobile site configured, enrollment enabled |
| 10-12 | 🟢 | **LIVE** - Full multi-product deployment |

**🎯 Next Action:** Standard maintenance - mature implementation

---

### Fathom Validation (Last 90 Days)

⚪ **No calls in last 90 days** - Expected for mature implementation in maintenance mode.

*Most recent call: Apr 10, 2025 (Training) - outside assessment window*

**Status:** ✅ CONFIRMED - No recent calls indicates stable, self-sufficient implementation

---

# DCCL (Donald Choi Canada)
## V10 Assessment: Stage 11 | 90% Ready

| Stage | Status | Evidence |
|-------|--------|----------|
| 1-6 | 🟢 | Foundation complete: 2,657 products, 3 price levels, 351 customers |
| 7 | 🟢 | iPad live: 149 orders, 6 unique users |
| 8-9 | 🟡 | Mobile site enabled, URL configuration pending |
| 10-11 | 🟢 | iPad LIVE, B2B/eCat Online in configuration |

**🎯 Next Action:** Complete eCat Online B2B configuration

---

### Fathom Validation (Last 90 Days)

| Date | Call Title | Key Findings |
|------|------------|--------------|
| **Dec 9, 2025** | eCat / Donald Choi | B2B configuration guidance |
| Nov 25, 2025 | eCat / Donald Choi | Ongoing implementation |
| Nov 17, 2025 | SuperCat Onboarding | Initial onboarding |

**📞 Latest Call (Dec 9, 2025):**
> **Purpose:** Configure eCat navigation and B2B user permissions
>
> **Key Takeaways:**
> - Use `Expand Groups` in Company Settings to nest categories under Collections
> - B2B Access: Start configuring now using `Public Site` user group
> - Sales Associate Pricing: Create arithmetic price levels (e.g., `Warehouse x 2`)
> - **Universal Integration: ON HOLD pending data from Universal**

**Status:** ✅ CONFIRMED - Active implementation with clear next steps

---

# CST (Coaster Furniture)
## V10 Assessment: Stage 9 | 65% Ready | 🔴 CRITICAL BLOCKER

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 | 🟡 | Company created Dec 11, 2025 - missing company info |
| 2-6 | 🟢 | Data loaded: 4,067 products, 34 price levels, 6,420 customers |
| 7 | 🟡 | Testing: 2 orders |
| 8-9 | 🟢 | Mobile site configured |
| 10 | 🔴 | **BLOCKED** - Order integration required for Vegas Market |

**🎯 Next Action:** 🔴 URGENT - Complete order integration by Jan 25

---

### Fathom Validation (Last 90 Days)

| Date | Call Title | Key Findings |
|------|------------|--------------|
| **Jan 13, 2026** | [Hold] eCat x Coaster Standup | Critical blockers identified |
| **Jan 7, 2026** | Coaster Customer File & Territory Setup | Territory logic defined |
| Jan 6, 2026 | [Hold] eCat x Coaster Standup | Ongoing standup |
| Dec 30, 2025 | [Hold] eCat x Coaster Standup | Ongoing standup |
| Dec 23, 2025 | [Hold] eCat x Coaster Standup | Ongoing standup |
| Dec 16, 2025 | [Hold] eCat x Coaster Standup | Ongoing standup |
| Nov 26, 2025 | SuperCat / Coaster - Status Update | Status review |
| Nov 18, 2025 | SuperCat / Coaster - Tech Talk | Technical discussion |

**📞 Latest Call (Jan 13, 2026):**
> **Purpose:** Finalize eCat setup and resolve critical order integration blockers
>
> **🔴 Critical Blockers Identified:**
> 1. **Order Integration is TOP PRIORITY:** *"A push-to-API integration is required for the Jan 25-28 Vegas market to replace the expiring AMP subscription. Brent will confirm feasibility today, as the integration was not in the original scope."*
> 2. **Warehouse Selection BLOCKER:** *"The Coaster API requires a warehouse code, but eCat lacks a native selection feature. A workaround using a required order custom field will be explored."*
> 3. **Rep Onboarding ON HOLD:** *"Rep invites are paused until Marlene provides updated pricing and customer files."*

**📞 Jan 7, 2026 Call:**
> - **Inventory:** Use custom fields in inventory file for warehouse-specific stock
> - **Territories:** Assign reps via user file, user group settings control access
> - **Ship-to Territories:** Use `ship_to_territory_code` for multi-location accounts

---

### 🔴 Validation Flags

| Flag | Evidence | Action |
|------|----------|--------|
| 🔴 **ORDER INTEGRATION** | *"Push-to-API integration required for Vegas market"* | Brent confirming TODAY |
| 🔴 **WAREHOUSE SELECTION** | *"eCat lacks a native selection feature"* | Custom field workaround |
| 🟡 **REP ONBOARDING HOLD** | *"Paused until Marlene provides files"* | Waiting on Marlene |

**Status:** 🔴 CRITICAL - 11 days until Vegas Market. Weekly standups show active engagement but major blockers remain.

---

# TCD (Terracotta Designs)
## V10 Assessment: Stage 5 | 45% Ready | 🟡 DELAYED

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 | 🟡 | Company inactive, missing company info |
| 2-4 | 🟢 | Catalog: 441 products, 4 price levels, 222 options |
| 5 | 🔴 | **BLOCKER: 0 customers, 0 sales reps** |
| 6 | 🟢 | 348 inventory records |
| 7-12 | 🔴 | Blocked at Stage 5 |

**🎯 Next Action:** Follow up on customer list delivery post-Dallas Market (Jan 20+)

---

### Fathom Validation (Last 90 Days)

| Date | Call Title | Key Findings |
|------|------------|--------------|
| **Dec 18, 2025** | Terracotta / SuperCat: Onboarding Check-In | Product structure decisions |

**📞 Latest Call (Dec 18, 2025):**
> **Purpose:** Review onboarding progress and define product page/data structure changes
>
> **Key Decisions:**
> 1. **Product Page Redesign:** *"Each size (e.g., small/large) will become a separate product with its own full SKU and image, replacing the options-based system."*
> 2. **Critical Data Display:** Key info (full SKU, dimensions, weight) must move to prominent right-side panel
> 3. **Customer & Rep Data:** *"Scott will export his customer list for SuperCat to map. The complex, hierarchical rep data requires a separate strategy."*
>
> **Timeline:** *"The goal is to launch a fully functional site before the Dallas market show in early January."*

---

### 🟡 Validation Flags

| Flag | Evidence | Action |
|------|----------|--------|
| 🟡 **UNFULFILLED** | *"Scott will export customer list"* - still pending | Follow up Jan 20+ |
| 🟡 **TIMELINE PUSHED** | Help Scout Dec 27: *"May need to push to later next month"* | Dallas Market prep |

**Status:** 🟡 DELAYED - Active engagement, known timeline. Customer list blocked by Dallas Market (Showroom #3751).

---

# KRB (Kaleen Rugs & Broadloom)
## V10 Assessment: Stage 5 | 40% Ready | 🔴 STALLED

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 | 🟢 | Company active with address configured |
| 2 | 🟢 | 7,740 products, 28 collections |
| 3 | 🟡 | 19 price levels - but complex pricing unresolved |
| 5 | 🟢 | 2,208 customers, 40 users |
| 6 | 🔴 | Inventory last updated Feb 2025 (11 months stale) |
| 7-12 | 🔴 | **STALLED** - No progress since Dec |

**🎯 Next Action:** 🔴 URGENT - Re-engagement call required

---

### Fathom Validation (Last 90 Days)

| Date | Call Title | Key Findings |
|------|------------|--------------|
| **Dec 3, 2025** | Kaleen / eCat | Pricing strategy defined |
| Nov 14, 2025 | eCat / Kaleen | Implementation call |
| Oct 30, 2025 | eCat / Kaleen | Implementation call |
| Oct 28, 2025 | eCat / Kaleen | Implementation call |

**📞 Latest Call (Dec 3, 2025) - 42 DAYS AGO:**
> **Purpose:** Define pricing strategy for Kaleen's eCat implementation
>
> **Key Decision:** *"Use eCat's Contract Pricing feature for all pricing. This simplifies the complex Kaleen pricing model into a single, comprehensive file."*
>
> **Target:** *"Goal: Deliver a functional eCat build for Cole Lewis to test by December 15."*
>
> **Data Prep:**
> - Curtis's team will generate contract pricing file from CAMS
> - Cole will provide "master build" file for product data fields

---

### 🔴 Validation Flags

| Flag | Evidence | Action |
|------|----------|--------|
| 🔴 **STALLED** | Last call Dec 3 (42 days). Dec 15 target missed by 30 days. | Immediate re-engagement |
| 🔴 **UNFULFILLED** | *"Deliver functional build by December 15"* - still pending | Follow up with Curtis |

**Status:** 🔴 STALLED - Despite extensive call history, implementation has stalled. Contract pricing solution defined but Dec 15 target missed. No calls in 6 weeks.

---

# MALI (Magic Lite)
## V10 Assessment: Stage 2 | 20% Ready | 🟡 EARLY STAGE

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 | 🟡 | Company since Nov 21, 2025 - missing company info |
| 2 | 🟢 | 906 products, 12 categories, 50 collections |
| 3 | 🔴 | **0 price levels** - Blocked |
| 5 | 🔴 | **0 customers** |
| 6-12 | 🔴 | Blocked at Stage 3 |

**🎯 Next Action:** Confirm contract signed, begin pricing/customer setup

---

### Fathom Validation (Last 90 Days)

| Date | Call Title | Key Findings |
|------|------------|--------------|
| **Oct 10, 2025** | SuperCat / Magic Lite - Huddle & Next Steps | Sales evaluation |

**📞 Latest Call (Oct 10, 2025) - 96 DAYS AGO:**
> **Meeting Type:** Sales (SPICED Framework)
>
> **Situation:** *"Jennifer Penton from Magic Lite is considering SuperCat Solutions for their e-commerce and sales rep enablement needs. SuperCat is currently the leading contender."*
>
> **Decision Process:**
> - Jennifer and Jen Zeroni have signing authority but need final approval from **Tom (Jennifer's father)**
> - Jennifer gathering feedback from reps to finalize requirements
>
> **Pain Points:** 50-60 hours/week on manual processes, lack of centralized data

---

### 🟡 Validation Flags

| Flag | Evidence | Action |
|------|----------|--------|
| 🟡 **EARLY STAGE** | Last Fathom call was sales-focused. Tom approval may be pending. | Confirm contract status |

**Status:** 🟡 EARLY - Company created Nov 21 suggests possible contract post-Oct call. Help Scout shows active file uploads (Jan 6). Confirm Tom approved.

---

# PEBL (Pebl Furniture)
## V10 Assessment: Stage 2 | 15% Ready | 🔴 STALLED

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 | 🟡 | Company since July 2025 - missing company info |
| 2 | 🟡 | 1,183 products - last update Sep 6, 2025 (130+ days stale) |
| 3-6 | 🔴 | **0 price levels, 0 customers, 0 inventory** |
| 7-12 | 🔴 | Blocked at Stage 3 |

**🎯 Next Action:** 🔴 URGENT - Determine if implementation should be closed

---

### Fathom Validation (Last 90 Days)

⚪ **No calls in last 90 days**

*Most recent call: Jul 10, 2025 (Demo) - 188 days ago*

**Historical Context from Jul 10 Demo:**
> - Target: Sep 10, 2025 trade show (**missed by 126 days**)
> - Decision makers: Vincent Lee, Trista Qiu
> - 2,000-3,000 SKUs planned, 10-12 users

---

### 🔴 Validation Flags

| Flag | Evidence | Action |
|------|----------|--------|
| 🔴 **STALLED** | 0 calls in 6 months. Sep 10 target missed. No progress. | Determine proceed/close |

**Status:** 🔴 STALLED - Single demo call July 2025, then radio silence. Organization 174 days old with zero progress. Recommend outreach to Vincent Lee.

---

# Validation Flags Summary

## 🔴 Critical Flags (Require Immediate Action)

| Client | Flag | Fathom Evidence | Action |
|--------|------|-----------------|--------|
| **CST** | ORDER INTEGRATION | *"Push-to-API integration required for Vegas Market Jan 25-28"* | Brent confirming today |
| **CST** | WAREHOUSE SELECTION | *"eCat lacks native warehouse selection"* | Custom field workaround |
| **KRB** | STALLED | Dec 3 last call, Dec 15 target missed | Urgent re-engagement |
| **PEBL** | STALLED | No calls in 6 months, Sep 10 target missed | Determine if close |

## 🟡 Review Flags (Need Follow-up)

| Client | Flag | Evidence | Action |
|--------|------|----------|--------|
| **CST** | REP ONBOARDING HOLD | Waiting on Marlene for files | Monitor |
| **TCD** | UNFULFILLED | Customer list promised, not delivered | Follow up Jan 20+ |
| **TCD** | TIMELINE PUSHED | Dallas Market prep | Expected |
| **MALI** | EARLY STAGE | Tom approval may be pending | Confirm contract |

## ✅ Confirmed (Active & Healthy)

| Client | Stage | Last Fathom Call | Status |
|--------|-------|------------------|--------|
| **JCUSA** | 12 | N/A (maintenance) | Mature implementation |
| **DCCL** | 11 | Dec 9, 2025 | B2B config in progress |

---

# Key Takeaways

1. **Most Urgent (11 days):** CST order integration for Vegas Market Jan 25-28
   - Fathom surfaced this blocker - not visible in MCP data alone

2. **Stalled Implementations:**
   - **KRB:** 42 days since last call, Dec 15 target missed
   - **PEBL:** 188 days since only call, likely abandoned

3. **Pipeline Health:**
   - **🟢 Healthy (2):** JCUSA, DCCL
   - **🟡 Active with delays (2):** CST (blockers), TCD (customer data)
   - **🔴 Stalled (2):** KRB, PEBL
   - **⚪ Early/Uncertain (1):** MALI

4. **Fathom Validation Value:** 
   - MCP showed CST "Stage 10" ready - Fathom revealed critical Vegas Market blockers
   - MCP showed KRB "data complete" - Fathom revealed Dec 15 target missed

---

*V10 Assessment: Data-driven via MCP*  
*Validation Layer: Fathom API (calls from last 90 days)*  
*Assessment Date: January 14, 2026*
