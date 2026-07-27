# Q1 2026 Onboarding Pipeline
## V10 Multi-Product Stage-Gated Model + Validation Flags

**Date:** January 14, 2026  
**Methodology:** V10 data-driven assessment with Fathom/Help Scout contradiction flags

---

## Pipeline Overview

| Client | V10 Stage | V10 Readiness | Validation Status | Key Flag |
|--------|-----------|---------------|-------------------|----------|
| **JCUSA** | 10 (Live) | 95% | ✅ No flags | Flagship - mature deployment |
| **DCCL** | 8 (eCat Online) | 75% | ⚠️ 1 flag | Cache issues affecting eCat Online |
| **KRB** | 7 (iPad Ready) | 80% | ⚠️ 1 flag | Stale inventory (326 days) |
| **CST** | 5 (Customer Setup) | 60% | 🔴 2 flags | STALLED - [Hold] meetings |
| **TCD** | 5 (Customer Setup) | 35% | 🔴 3 flags | 0 customers + churn risk |
| **MALI** | 3 (Pricing) | 25% | ✅ No flags | Early stage - confirmed |
| **PEBL** | 3 (Pricing) | 20% | 🔴 1 flag | ACTIVITY - 131 days no update |

---

```
PIPELINE VIEW (V10 Assessment)
═══════════════════════════════════════════════════════════════

JCUSA ███████████████████░ 95%  Stage 10 - Live       ✅ CONFIRMED
DCCL  ███████████████░░░░░ 75%  Stage 8 - eCat Online ⚠️ FLAGGED
KRB   ████████████████░░░░ 80%  Stage 7 - iPad Ready  ⚠️ FLAGGED
CST   ████████████░░░░░░░░ 60%  Stage 5 - Customers   🔴 STALLED
TCD   ███████░░░░░░░░░░░░░ 35%  Stage 5 - Customers   🔴 FLAGGED
MALI  █████░░░░░░░░░░░░░░░ 25%  Stage 3 - Pricing     ✅ CONFIRMED
PEBL  ████░░░░░░░░░░░░░░░░ 20%  Stage 3 - Pricing     🔴 FLAGGED

═══════════════════════════════════════════════════════════════
```

---

# JCUSA (Jonathan Charles Designs Inc.)
## V10 Assessment: Stage 10 | 95% Ready

| Stage | Status | V10 Evidence |
|-------|--------|--------------|
| 1 | 🟢 | Company active since 2018, multiple admins |
| 2 | 🟢 | 20,142 products, 30 collections, updated today |
| 3 | 🟢 | 8 price levels configured |
| 4 | 🟢 | 566 options configured |
| 5 | 🟢 | 4,587 customers, 2,553 users |
| 6 | 🟢 | 1,387 inventory records, updated yesterday |
| 7 | 🟢 | 112 iPad orders, 18 unique iPad users |
| 8 | 🟢 | eCat Online site enabled |
| 9 | 🟢 | 2,553 users enrolled |
| 10 | 🟢 | 2,211 total orders, 14 in last 30 days |

---

### ✅ No Validation Flags

Fathom calls and Help Scout tickets **confirm** V10 assessment:
- Help Scout tickets show routine Sales Portal check-ins, invoice updates
- No blocking issues or negative sentiment detected
- Portal dashboard enabled and actively used

**Validation Summary:** V10 assessment confirmed. JCUSA is a flagship deployment operating at full capacity across iPad and eCat Online.

---

# DCCL (Donald Choi Canada)
## V10 Assessment: Stage 8 | 75% Ready

| Stage | Status | V10 Evidence |
|-------|--------|--------------|
| 1 | 🟢 | Company active, admin configured (Valerie) |
| 2 | 🟢 | 2,657 products, 194 collections, updated yesterday |
| 3 | 🟢 | 3 price levels configured |
| 4 | 🟢 | 2 options configured |
| 5 | 🟢 | 351 customers, 23 users |
| 6 | 🟢 | 329 inventory records, updated yesterday |
| 7 | 🟢 | 149 iPad orders, 6 unique iPad users |
| 8 | 🟡 | eCat Online site enabled BUT cache issues |
| 9 | 🟡 | Enrollment configured but testing needed |
| 10 | ⚪ N/A | B2B ordering not primary focus |

**🎯 V10 Next Action:** Resolve eCat Online cache issues

---

### ⚠️ Validation Flags (1)

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 8 | ⚠️ REVIEW | Help Scout (Jan 8) | *"eCat Online not updating trade names and collections"* - Server cache issues affecting eCat Online experience. Multiple related tickets: #3192889039, #3192870303, #3192455491 |

**Additional Context:** Help Scout (Nov 17): *"You should be able to see your online catalog here. The permissions used to determine the 'public' user are based on this user group."* - Active configuration work ongoing.

**Validation Summary:** V10 correctly shows Stage 8 in progress. Cache issues need resolution before eCat Online can be marked complete. iPad deployment is stable with 149 orders.

---

# KRB (Kaleen Rugs & Broadloom)
## V10 Assessment: Stage 7 | 80% Ready

| Stage | Status | V10 Evidence |
|-------|--------|--------------|
| 1 | 🟢 | Company active, multiple admins |
| 2 | 🟢 | 7,740 products, 28 collections |
| 3 | 🟢 | 19 price levels configured (Contract Pricing enabled) |
| 4 | ⚪ N/A | Options not required |
| 5 | 🟢 | 2,208 customers, 40 users |
| 6 | 🟡 | 2,509 inventory records BUT **326 days stale** |
| 7 | 🟡 | 1 iPad order, no eCat Online site |
| 8 | ⚪ N/A | eCat Online not being implemented |
| 9 | ⚪ N/A | - |
| 10 | ⚪ N/A | - |

**🎯 V10 Next Action:** Refresh stale inventory data, configure order notifications

---

### ⚠️ Validation Flags (1)

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 6 | ⚠️ STALE | MCP Data | Last inventory update: Feb 23, 2025 (326 days ago). This exceeds the 7-day freshness threshold. |

**Additional Context from Fathom:** Multiple "Kaleen / eCat" calls in history suggest active engagement, but implementation appears to be in extended testing phase.

**Validation Summary:** V10 shows Stage 7 ready with 1 iPad order confirmed. Critical issue: inventory data is extremely stale (326 days). Recommend immediate inventory refresh before go-live push.

---

# CST (Coaster Furniture)
## V10 Assessment: Stage 5 | 60% Ready | 🔴 STALLED

| Stage | Status | V10 Evidence |
|-------|--------|--------------|
| 1 | 🟢 | Company exists (status: inactive), admin configured |
| 2 | 🟢 | 4,067 products, 2,117 collections, updated Jan 8 |
| 3 | 🟢 | 34 price levels configured |
| 4 | 🟢 | 2,491 options configured |
| 5 | 🔴 | 6,420 customers BUT **price levels corrupted** |
| 6 | 🟢 | 4,814 inventory records, updated Jan 8 |
| 7 | 🔴 | eCat Online site enabled BUT **0 iPad orders** |
| 8 | ⚪ | eCat Online site exists but not active focus |
| 9 | ⚪ | - |
| 10 | ⚪ | - |

**🎯 V10 Next Action:** Resolve customer data issues and restart implementation

---

### 🔴 Validation Flags (2)

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| ALL | 🔴 STALLED | Fathom | **Multiple meetings titled "[Hold] eCat x Coaster Standup"** - Implementation paused. Despite 6,420 customers loaded, 0 iPad orders exist. The "[Hold]" prefix signals waiting on client action. |
| 5 | 🔴 CONTRADICT | Previous Assessment | *"Customer data requires re-import. A script clobbered customer-specific price levels (e.g., DSFOB C6) with default (Z3T1)."* - Customer data exists but price level assignments are incorrect. |

**Additional Context:** 
- Fathom shows "SuperCat / Coaster - Tech Talk" and "Coaster Customer File & Territory Setup" calls occurred
- 2 test orders exist (created Jan 13) but these are admin tests, not rep orders
- No iPad activity (`ipad_order_count = 0`) despite full data load

**Validation Summary:** V10 correctly identifies Stage 5 blocker. Implementation is **STALLED** - the "[Hold]" meeting pattern confirms pause state. Customer data exists but needs re-import before rep training. Requires clarification on blocker and reactivation timeline.

---

# TCD (Terracotta Designs)
## V10 Assessment: Stage 5 | 35% Ready | 🔴 CRITICAL

| Stage | Status | V10 Evidence |
|-------|--------|--------------|
| 1 | 🟢 | Company exists (status: **inactive**) |
| 2 | 🟢 | 441 products, 150 collections, 6 categories |
| 3 | 🟢 | 4 price levels configured |
| 4 | 🟢 | 222 options configured |
| 5 | 🔴 | **0 customers, 0 sales reps** |
| 6 | 🟡 | 348 inventory records, 26 days stale |
| 7 | 🔴 | 0 orders, no eCat Online site |
| 8 | ⚪ N/A | - |
| 9 | ⚪ N/A | - |
| 10 | ⚪ N/A | - |

**🎯 V10 Next Action:** Import customer data (CRITICAL BLOCKER)

---

### 🔴 Validation Flags (3)

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | 🔴 CONTRADICT | MCP Data | **0 customers after 3 months in onboarding** - System shows 441 products loaded but no customer data. This is a Stage 5 absolute blocker. |
| 5 | ⚠️ UNFULFILLED | Help Scout (Historical) | Client previously promised customer list file - still not delivered. Last product update: Dec 22, 2025 (23 days ago). |
| - | 🔴 SENTIMENT | Help Scout (Historical) | *"The tool feels less like a mature commercial product and more like an early-stage amateur implementation. Had I known this earlier, I likely would not have signed up."* - **CHURN RISK** |

**🚨 Sentiment Flag:**

| Source | Evidence |
|--------|----------|
| Help Scout (Historical) | *"The tool feels less like a mature commercial product and more like an early-stage amateur implementation."* |

**Additional Context:** 
- Help Scout (Nov 17): *"I'd love the opportunity to meet and speak with you in person at Dallas Market, showroom #3751"* - Client engagement attempted
- Fathom shows "Terracotta / SuperCat: Onboarding Check-In" calls occurred
- Organization status is **inactive** - may indicate implementation pause or client decision

**Validation Summary:** V10 correctly flags Stage 5 blocker (0 customers). Combined with sentiment flag, this represents a **CHURN RISK**. Requires immediate executive attention.

---

# MALI (Magic Lite)
## V10 Assessment: Stage 3 | 25% Ready

| Stage | Status | V10 Evidence |
|-------|--------|--------------|
| 1 | 🟢 | Company exists, status: onboarding |
| 2 | 🟢 | 906 products, 50 collections, 12 categories |
| 3 | 🔴 | **0 price levels configured** |
| 4 | ⚪ N/A | 0 options (not required) |
| 5 | 🔴 | 0 customers |
| 6 | 🔴 | 0 inventory |
| 7 | 🔴 | 0 orders, no eCat Online site |
| 8 | ⚪ N/A | - |
| 9 | ⚪ N/A | - |
| 10 | ⚪ N/A | - |

**🎯 V10 Next Action:** Configure price levels (critical blocker)

---

### ✅ No Validation Flags

Fathom calls **confirm** V10 assessment:
- Multiple calls: "SuperCat / Magic Lite - Product Demonstration", "Huddle & Next Steps", "Intro Call"
- Active engagement confirmed
- Early stage implementation - Stage 3 blocker (0 price levels) is accurate

**Validation Summary:** V10 assessment confirmed. Stage 3 blocker (0 price levels) is accurate. Client actively engaged per Fathom call history. Products recently updated (Jan 7).

---

# PEBL (Pebl Furniture)
## V10 Assessment: Stage 3 | 20% Ready

| Stage | Status | V10 Evidence |
|-------|--------|--------------|
| 1 | 🟢 | Company exists, status: onboarding |
| 2 | 🟡 | 1,183 products, 76 collections BUT **131 days stale** |
| 3 | 🔴 | **0 price levels configured** |
| 4 | 🟢 | 15 options configured |
| 5 | 🔴 | 0 customers |
| 6 | 🔴 | 0 inventory |
| 7 | 🔴 | 0 orders, no eCat Online site |
| 8 | ⚪ N/A | - |
| 9 | ⚪ N/A | - |
| 10 | ⚪ N/A | - |

**🎯 V10 Next Action:** Confirm client engagement, configure price levels

---

### 🔴 Validation Flag (1)

| Flag | Source | Evidence |
|------|--------|----------|
| 🔴 ACTIVITY | Fathom + Help Scout | **0 Fathom calls, 0 Help Scout tickets** in recent history. Last product update: Sept 6, 2025 (131 days ago). No communication trail detected. |

**Additional Context:** 
- Fathom shows only 1 call: "eCat Demo for PEBL" (historical)
- No Help Scout tickets found for this client
- Historical note: "Radio silence since notice of ERP transition"

**Validation Summary:** V10 assessment may be accurate for data state, but zero activity signals **potential client disengagement or abandonment**. Recommend outreach to confirm engagement status.

---

# Validation Flags Summary

## 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
|--------|-------|-------|----------|--------|
| CST | ALL | STALLED | Multiple "[Hold] eCat x Coaster Standup" meetings | Clarify blocker and reactivation timeline |
| CST | 5 | Customer data corrupted | "Script clobbered customer-specific price levels" | Re-import before rep training |
| TCD | 5 | 0 customers | 3 months in onboarding with no customer data | Import customer file immediately |
| TCD | - | CHURN RISK | "amateur implementation" sentiment | Executive escalation |
| PEBL | - | ACTIVITY | 131 days no updates, 0 communication | Confirm client engagement |

## ⚠️ Review Flags (Need Follow-up)

| Client | Stage | Issue | Evidence | Action |
|--------|-------|-------|----------|--------|
| DCCL | 8 | Cache issues | "eCat Online not updating trade names" | Resolve server caching |
| KRB | 6 | Stale inventory | 326 days since last update | Refresh inventory data |

## ✅ Confirmed (No Flags)

| Client | V10 Stage | V10 Readiness | Status |
|--------|-----------|---------------|--------|
| JCUSA | Stage 10 | 95% | Flagship deployment - fully validated |
| MALI | Stage 3 | 25% | Early stage - system data confirmed |

---

# Key Takeaways

1. **V10 model accuracy:** 5 of 7 clients have flags requiring review. 2 fully validated (JCUSA, MALI).

2. **Most impactful flags:**
   - CST "[Hold]" pattern detection - V10 correctly identified stalled implementation
   - TCD churn risk - sentiment flag + 0 customers = critical escalation
   - PEBL abandonment risk - 131 days no activity

3. **Validation value:** 
   - Fathom "[Hold]" meeting pattern caught CST stall that MCP data alone couldn't detect
   - Help Scout cache tickets flagged DCCL eCat Online issues
   - Activity detection flagged PEBL potential abandonment

4. **Pipeline health:**
   - **Live:** JCUSA (95%)
   - **Near-ready:** DCCL (75%), KRB (80%)
   - **Blocked/Stalled:** CST, TCD
   - **Early/At-risk:** MALI, PEBL

---

*V10 Assessment: Data-driven via MCP + BigQuery Mixpanel*  
*Validation Layer: Fathom API + BigQuery Help Scout*  
*Model Version: V10 Multi-Product Stage-Gated Onboarding*
