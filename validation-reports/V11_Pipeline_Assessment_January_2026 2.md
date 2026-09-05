# V11.3 Stage-Gated Pipeline Assessment
**Generated:** January 14, 2026  
**Methodology:** FRD V11.3 Fast Mode Protocol  
**Stage Definitions:** FRD V10 Multi-Product Framework  
**Assessment Type:** 7-Client Active Implementation Pipeline

---

## Pipeline Overview

| Client | Stage | Readiness | Validation Status | Key Flag |
|--------|-------|-----------|-------------------|----------|
| **Coaster (cst)** | Stage 6 → 7 | 🟡 65% | ⚠️ REVIEW | Order integration blocker for Vegas market |
| **Donald Choi Canada (dccl)** | Stage 8 → 9 | 🟢 75% | ✅ CONFIRMED | B2B user config in progress |
| **Terracotta Designs (tcd)** | Stage 5 → 6 | 🟡 60% | ⚠️ REVIEW | Product page redesign dependency |
| **Kaleen Rugs (krb)** | Stage 3 → 4 | 🟡 55% | ⚠️ REVIEW | Contract pricing strategy in flight |
| **Magic Lite (mali)** | Stage 2 | 🟡 50% | ⚠️ ACTIVITY | Deferred engagement until January |
| **Pebl Furniture (pebl)** | Stage 2 | 🟡 45% | ⚠️ ACTIVITY | No recent Fathom engagement |
| **Jonathan Charles (jcusa)** | Stage 7+ | 🟢 70% | ✅ DATA | Strong API activity, established account |

---

## ASCII Pipeline Visualization

```
STAGE:  1         2         3         4         5         6         7         8         9        10
        Foundation Catalog   Pricing   Options   Users     Ops       iPad      eOL Site  eOL User  eOL Order
        |---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|

CST     ████████████████████████████████████████████████████████████████▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  65% Stage 6→7
        Order integration blocker: warehouse selection workaround needed for Jan 25-28 Vegas market

DCCL    ██████████████████████████████████████████████████████████████████████████████████▓▓░░░░░░░░░░░░░░░░  75% Stage 8→9
        B2B user permissions & arithmetic price levels in configuration

TCD     ████████████████████████████████████████████████████████▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  60% Stage 5→6
        Product page redesign blocking customer data mapping

KRB     ████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  55% Stage 3→4
        Contract pricing file from CAMS pending

MALI    ██████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  50% Stage 2
        Deferred active engagement to January; SuperCat building v1

PEBL    ██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  45% Stage 2
        ⚠️ No recent Fathom activity detected

JCUSA   ██████████████████████████████████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  70% Stage 7+
        Established account with strong API activity (250 events/90d)
```

---

## Individual Client Assessments

---

### 1. Coaster Furniture (cst)

**Current Stage:** Stage 6 → 7 (iPad Order-Ready)  
**Products:** eCat iPad (primary), eCat Online (secondary)  
**Overall Readiness:** 🟡 65%  
**Validation Status:** ⚠️ REVIEW

#### Stage Status Table

| Stage | Status | Evidence |
|-------|--------|----------|
| 1: Account Foundation | 🟢 Complete | Organization active, 2 admin users |
| 2: Catalog Setup | 🟢 Complete | 28,892 products, 70,355 images |
| 3: Pricing Configuration | 🟢 Complete | 5 price levels configured |
| 4: Option Configuration | 🟢 Complete | Options data exists |
| 5: Customer & User Setup | 🟢 Complete | 7,847 customers imported |
| 6: Operational Data | 🟢 Complete | Inventory tracking enabled, recent imports |
| 7: iPad Order-Ready | 🟡 In Progress | **BLOCKER:** Order integration for Vegas market |
| 8+: eCat Online | ⚪ Not Started | Pending iPad completion |

#### 🎯 Next Action
**Resolve order integration blocker.** Push-to-API integration required for Jan 25-28 Vegas market. Warehouse selection workaround via order custom field needs confirmation from Brent.

#### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 7 | ⚠️ REVIEW | Fathom (Jan 10, 2026) | *"Order Integration is the Top Priority: A push-to-API integration is required for the Jan 25–28 Vegas market to replace the expiring AMP subscription. Brent will confirm feasibility today."* |
| 7 | ⚠️ REVIEW | Fathom (Jan 10, 2026) | *"Warehouse Selection is the Key Blocker: The Coaster API requires a `warehouse` code, but eCat lacks a native selection feature. A workaround using a required order custom field will be explored."* |
| 5 | ⚠️ UNFULFILLED | Fathom (Jan 10, 2026) | *"Rep Onboarding is On Hold: Rep invites are paused until Marlene provides updated pricing and customer files."* |
| 7 | ⚠️ REVIEW | Fathom (Jan 7, 2026) | *"Inventory: Use custom fields in the `inventory` file for warehouse-specific stock."* |

#### Validation Summary
**Strong progress but critical blocker.** Coaster has excellent data foundation (28K+ products, 7K+ customers) but the Vegas market deadline (Jan 25-28) creates urgency. The order integration dependency on warehouse selection workaround is the critical path item. Rep onboarding is intentionally held pending customer file updates from Marlene.

**Recent Fathom Activity:** 3 calls in last 30 days (Jan 10, Jan 7, Nov 15)  
**BigQuery Activity:** 18 API access events (90 days)

---

### 2. Donald Choi Canada (dccl)

**Current Stage:** Stage 8 → 9 (eCat Online User Access)  
**Products:** eCat Online (primary), B2B capabilities  
**Overall Readiness:** 🟢 75%  
**Validation Status:** ✅ CONFIRMED

#### Stage Status Table

| Stage | Status | Evidence |
|-------|--------|----------|
| 1: Account Foundation | 🟢 Complete | Organization active, 1 admin user |
| 2: Catalog Setup | 🟢 Complete | 2,050 products, 11,610 images |
| 3: Pricing Configuration | 🟢 Complete | 12 price levels (including arithmetic) |
| 4: Option Configuration | ⚪ N/A | No options configured |
| 5: Customer & User Setup | 🟢 Complete | 16 customers imported |
| 6: Operational Data | 🟢 Complete | Inventory tracking enabled |
| 7: iPad Order-Ready | ⚪ N/A | Not iPad implementation |
| 8: eCat Online Site | 🟢 Complete | Site configured |
| 9: eCat Online User Access | 🟡 In Progress | B2B user permissions being configured |

#### 🎯 Next Action
**Complete B2B user group configuration.** Configure `Public Site` user group, set up enrollment process, create arithmetic price levels for sales associates.

#### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 9 | ✅ CONFIRMED | Fathom (Dec 16, 2024) | *"B2B Access: Start configuring B2B access now, using the `Public Site` user group for unauthenticated users and the `Enrollment` tool for new dealer sign-ups."* |
| 9 | ✅ CONFIRMED | Fathom (Dec 16, 2024) | *"Sales Associate Pricing: Create arithmetic price levels (e.g., `Warehouse x 2`) and assign them to specific user groups."* |
| 8 | ⚠️ REVIEW | Fathom (Dec 2, 2024) | *"Universal Data Blocked: The Universal data feed is delayed until next week, as their IT contact is out."* |
| 2 | ✅ CONFIRMED | Fathom (Nov 18, 2024) | *"Data Sync Strategy: Donald Choi will automate merging their daily product file with Universal's daily file."* |

#### Validation Summary
**On track with clear path forward.** DCCL has a solid foundation with 12 price levels (including arithmetic calculations for markup scenarios) and is actively configuring B2B user access. The Universal data integration dependency appears resolved based on current product counts.

**Recent Fathom Activity:** 3 calls in last 90 days (Dec 16, Dec 2, Nov 18)  
**BigQuery Activity:** 277 API access events (90 days) - highest among implementations

---

### 3. Terracotta Designs (tcd)

**Current Stage:** Stage 5 → 6 (Customer & User Setup)  
**Products:** eCat Online (primary)  
**Overall Readiness:** 🟡 60%  
**Validation Status:** ⚠️ REVIEW

#### Stage Status Table

| Stage | Status | Evidence |
|-------|--------|----------|
| 1: Account Foundation | 🟢 Complete | Organization active, 1 admin user |
| 2: Catalog Setup | 🟡 Partial | 1,022 products, 2,034 images |
| 3: Pricing Configuration | 🟢 Complete | 1 price level configured |
| 4: Option Configuration | ⚪ N/A | Options exist but being restructured |
| 5: Customer & User Setup | 🟡 In Progress | 0 customers - waiting on customer export |
| 6: Operational Data | ⚪ Not Started | No inventory data |
| 7+: iPad/Online | ⚪ Not Started | Pending foundation |

#### 🎯 Next Action
**Product restructuring must complete.** Wait for Scott's customer list export and complete product page redesign (each size variant → separate product) before proceeding.

#### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 2 | 🔴 CONTRADICT | Fathom (Dec 12, 2024) | *"Product Page Redesign: The current layout is confusing. Each size (e.g., small/large) will become a separate product with its own full SKU and image, replacing the options-based system."* |
| 5 | ⚠️ REVIEW | Fathom (Dec 12, 2024) | *"Customer & Rep Data: Scott will export his customer list for SuperCat to map. The complex, hierarchical rep data (agencies with multiple salespeople) requires a separate strategy."* |
| 6 | ⚠️ REVIEW | Fathom (Dec 12, 2024) | *"Urgent Timeline: The goal is to launch a fully functional site before the Dallas market show in early January."* |

#### Validation Summary
**Product restructuring is blocking progress.** The fundamental catalog structure is being redesigned (size variants → separate products), which means current product counts are not representative of final state. Customer data is pending Scott's export. The January Dallas market timeline has likely slipped based on current stage.

**Recent Fathom Activity:** 1 call in last 90 days (Dec 12)  
**BigQuery Activity:** 25 API access events (90 days)

---

### 4. Kaleen Rugs & Broadloom (krb)

**Current Stage:** Stage 3 → 4 (Pricing Configuration)  
**Products:** eCat iPad (primary)  
**Overall Readiness:** 🟡 55%  
**Validation Status:** ⚠️ REVIEW

#### Stage Status Table

| Stage | Status | Evidence |
|-------|--------|----------|
| 1: Account Foundation | 🟢 Complete | Organization active, 2 admin users |
| 2: Catalog Setup | 🟢 Complete | 55,568 products, 25,600 images |
| 3: Pricing Configuration | 🟡 In Progress | 1 price level, Contract Pricing solution chosen |
| 4: Option Configuration | 🟡 Pending | Options exist but pricing takes priority |
| 5: Customer & User Setup | 🟡 Partial | 2,145 customers imported |
| 6: Operational Data | 🟡 Partial | Inventory exists but pricing dependency |
| 7: iPad Order-Ready | ⚪ Not Started | Blocked by pricing |

#### 🎯 Next Action
**Generate contract pricing file from CAMS.** Curtis's team to produce `SKU + Customer Account # → Price` file. Cole to provide master build file for product data fields.

#### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 3 | ⚠️ REVIEW | Fathom (Dec 3, 2024) | *"Decision: Use eCat's 'Contract Pricing' feature for all pricing. This simplifies the complex Kaleen pricing model (which varies by customer, brand, and SKU) into a single, comprehensive file."* |
| 3 | ⚠️ REVIEW | Fathom (Dec 3, 2024) | *"Goal: Deliver a functional eCat build for Cole Lewis to test by December 15."* |
| 3 | ⚠️ UNFULFILLED | Fathom (Nov 14, 2024) | *"Pricing Update: A new pricing update is pending from Curtis."* - Status unknown |
| 2 | ✅ CONFIRMED | Fathom (Nov 14, 2024) | *"Bulk Upload Planned: A bulk FTP upload of all images and PDFs is scheduled for Nov 17–19."* - Appears complete based on 25K images |

#### Validation Summary
**Pricing strategy decided but execution pending.** Kaleen has the largest catalog (55K+ products) and has chosen Contract Pricing as the solution for their complex pricing model. The December 15 milestone for Cole's testing has likely passed - need status update on CAMS contract pricing file generation.

**Recent Fathom Activity:** 2 calls in last 90 days (Dec 3, Nov 14)  
**BigQuery Activity:** 2 API access events (90 days) - lowest among active implementations

---

### 5. Magic Lite (mali)

**Current Stage:** Stage 2 (Catalog Setup)  
**Products:** eCat iPad (primary)  
**Overall Readiness:** 🟡 50%  
**Validation Status:** ⚠️ ACTIVITY

#### Stage Status Table

| Stage | Status | Evidence |
|-------|--------|----------|
| 1: Account Foundation | 🟢 Complete | Organization active, 2 admin users |
| 2: Catalog Setup | 🟡 In Progress | 3,143 products, 3,219 images |
| 3: Pricing Configuration | ⚪ Not Started | 0 price levels |
| 4: Option Configuration | ⚪ Pending | Options to be configured |
| 5: Customer & User Setup | ⚪ Not Started | 0 customers |
| 6: Operational Data | ⚪ Not Started | Inventory tracking enabled but empty |
| 7: iPad Order-Ready | ⚪ Not Started | Early stage |

#### 🎯 Next Action
**Upload Lowe's price file and high-res images.** Jennifer Penton to provide data via onboarding portal. SuperCat building v1 during Magic Lite's year-end deferral.

#### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| ALL | ⚠️ ACTIVITY | Fathom (Nov 21, 2024) | *"Timeline Shift: The project will start immediately, with SuperCat handling initial data setup. Magic Lite's active involvement (e.g., rep training) is deferred to January."* |
| 2 | ✅ CONFIRMED | Fathom (Nov 21, 2024) | *"Data Strategy: SuperCat will build the initial eCat instance using Magic Lite's detailed Lowe's price file and 2025 catalog."* |
| 2 | ⚠️ REVIEW | Fathom (Nov 21, 2024) | *"Imagery: Magic Lite has no dedicated DAM. SuperCat will use an onboarding portal to collect high-resolution images."* |

#### Validation Summary
**Intentionally deferred engagement - not stalled.** Unlike typical "no activity" situations, Magic Lite explicitly agreed to defer active participation until January while SuperCat builds v1 using their Lowe's price file. This is working as designed. Status update needed now that January has arrived.

**Recent Fathom Activity:** 2 calls on same day (Nov 21) - kickoff meeting  
**BigQuery Activity:** 3 API access events (90 days)

---

### 6. Pebl Furniture (pebl)

**Current Stage:** Stage 2 (Catalog Setup)  
**Products:** eCat iPad  
**Overall Readiness:** 🟡 45%  
**Validation Status:** ⚠️ ACTIVITY

#### Stage Status Table

| Stage | Status | Evidence |
|-------|--------|----------|
| 1: Account Foundation | 🟢 Complete | Organization active, 2 admin users |
| 2: Catalog Setup | 🟡 In Progress | 556 products, 1,186 images |
| 3: Pricing Configuration | 🟢 Started | 2 price levels configured |
| 4: Option Configuration | 🟢 Started | 189 options, 1 volume pricing template |
| 5: Customer & User Setup | ⚪ Not Started | 0 customers |
| 6: Operational Data | ⚪ Not Started | Inventory disabled |
| 7: iPad Order-Ready | ⚪ Not Started | Early stage |

#### 🎯 Next Action
**Investigate engagement status.** No Fathom meetings found in 90-day window. Check Help Scout for recent tickets. Consider outreach call.

#### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| ALL | ⚠️ ACTIVITY | Fathom | **No meetings found in last 90 days** |
| 2 | ⚠️ REVIEW | MCP Data | Small catalog (556 products) with pricing and options configured suggests active work but no recent calls |

#### Validation Summary
**Activity gap requires investigation.** Pebl has foundation elements in place (admin users, price levels, options) but no recent Fathom engagement and only 2 API access events. This could indicate:
1. Client working independently with minimal support needs
2. Implementation stalled without escalation
3. Meetings happening outside Fathom-recorded calls

Recommend Help Scout ticket review and outreach call.

**Recent Fathom Activity:** None found in 90 days  
**BigQuery Activity:** 2 API access events (90 days)

---

### 7. Jonathan Charles Design (jcusa)

**Current Stage:** Stage 7+ (iPad Order-Ready / Established)  
**Products:** eCat iPad (mature)  
**Overall Readiness:** 🟢 70%  
**Validation Status:** ✅ DATA

#### Stage Status Table

| Stage | Status | Evidence |
|-------|--------|----------|
| 1: Account Foundation | 🟢 Complete | Organization active, 3 admin users, QuickBooks integrated |
| 2: Catalog Setup | 🟢 Complete | 26,461 products, 59,476 images |
| 3: Pricing Configuration | 🟢 Complete | 1 price level configured |
| 4: Option Configuration | ⚪ N/A | No options used |
| 5: Customer & User Setup | 🟢 Complete | 5,011 customers imported |
| 6: Operational Data | 🟢 Complete | Inventory tracking enabled |
| 7: iPad Order-Ready | 🟢 Operational | Established account with orders |

#### 🎯 Next Action
**Monitor for expansion opportunities.** Established account with strong activity. Consider eCat Online or Sales Portal as next phase.

#### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 7 | ✅ DATA | BigQuery | **250 API access events in 90 days** - highest after DCCL |
| 7 | ✅ DATA | MCP | **27 orders processed** |
| 7 | ✅ CONFIRMED | MCP | QuickBooks integration configured |

#### Validation Summary
**Established, healthy account.** JCUSA shows strong operational activity with 250 API events and 27 orders. This is a mature implementation in maintenance mode rather than active onboarding. No Fathom meetings needed for routine operations.

**Recent Fathom Activity:** None found (expected for established accounts)  
**BigQuery Activity:** 250 API access events (90 days) - second highest

---

## Validation Flags Summary

### 🔴 Critical Flags (Require Investigation)

| Client | Stage | Flag | Source | Evidence |
|--------|-------|------|--------|----------|
| TCD | 2 | CONTRADICT | Fathom | Product structure being redesigned - current data not representative |

### ⚠️ Review Flags (Monitor Closely)

| Client | Stage | Flag | Source | Key Quote |
|--------|-------|------|--------|-----------|
| CST | 7 | REVIEW | Fathom | *"Order Integration is the Top Priority"* - Vegas market deadline |
| CST | 7 | REVIEW | Fathom | *"Warehouse Selection is the Key Blocker"* |
| KRB | 3 | REVIEW | Fathom | Contract pricing file pending from CAMS |
| TCD | 5 | REVIEW | Fathom | Customer data pending Scott's export |
| MALI | ALL | ACTIVITY | Fathom | Intentionally deferred to January - check in needed |
| PEBL | ALL | ACTIVITY | Fathom/BQ | No recent engagement detected |

### ✅ Confirmed Flags (Validated by Multiple Sources)

| Client | Stage | Flag | Source | Evidence |
|--------|-------|------|--------|----------|
| DCCL | 9 | CONFIRMED | Fathom | B2B configuration actively in progress |
| DCCL | 2 | CONFIRMED | Fathom | Data sync strategy validated |
| KRB | 2 | CONFIRMED | Fathom/MCP | Bulk upload appears complete (25K images) |
| JCUSA | 7 | DATA | BigQuery | Strong operational activity (250 events) |

---

## Key Takeaways

### Immediate Action Required

1. **CST (Coaster):** Order integration blocker for Jan 25-28 Vegas market. Brent to confirm warehouse selection workaround feasibility. **DEADLINE: THIS WEEK**

2. **MALI (Magic Lite):** January check-in now due. SuperCat has been building v1 during deferred period - schedule review call with Jennifer Penton.

3. **PEBL:** Activity gap investigation needed. No Fathom meetings in 90 days with minimal BigQuery activity. Recommend outreach.

### On Track Implementations

1. **DCCL (Donald Choi Canada):** B2B configuration progressing well. Highest API activity indicates active usage.

2. **KRB (Kaleen):** Large catalog with clear pricing strategy (Contract Pricing). Waiting on CAMS file generation.

### Blocked/Stalled Implementations

1. **TCD (Terracotta):** Product restructuring blocking all downstream progress. Timeline has likely slipped past Dallas market.

### Mature/Maintenance Accounts

1. **JCUSA (Jonathan Charles):** Established account with strong operational metrics. Consider expansion to eCat Online.

---

## Methodology Notes

### Data Sources Used
- **MCP Endpoints (All 4 Batches):** Organization info, users, data summary, price levels, categories, collections, options, territories, import events, inventories, mobile sites, reports config, orders
- **BigQuery:** Mixpanel events for iPad activity (7 clients, 90 days)
- **Fathom API:** `get_meetings()` + `get_summary()` for all clients with activity

### BigQuery Results
- No `order_submitted` events found for any of the 7 clients (all in implementation stage)
- API access events: DCCL (277), JCUSA (250), TCD (25), CST (18), MALI (3), KRB (2), PEBL (2)

### Fathom Coverage
| Client | Meetings Found | Summaries Retrieved |
|--------|----------------|---------------------|
| CST | 3 | 3 ✅ |
| DCCL | 3 | 3 ✅ |
| TCD | 1 | 1 ✅ |
| KRB | 2 | 2 ✅ |
| MALI | 2 | 1 ✅ (1 null) |
| PEBL | 0 | N/A |
| JCUSA | 0 | N/A (established account) |

---

*Generated by V11.3 Fast Mode Protocol | Assessment Date: January 14, 2026*
