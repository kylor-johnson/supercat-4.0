# Stage-Gated Onboarding Assessment + Validation Layer

**Generated:** 2026-03-02
**Assessment Scope:** 7 clients — pebl, mali, tcd, cst, dccl, hvusa, krb
**Data Sources:** PostgreSQL (eCat production), BigQuery (HubSpot, MixPanel, Fathom, HelpScout)
**Compared Against:** NOTION_OUTPUT_2026-02-18

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| **Phase-Completion Velocity (avg)** | 0.18 phases/wk |
| **Stuck Projects (idle > 7 days)** | **3** — PEBL (32d), KRB (25d), HVUSA (stale data, active imports but 99% errors) |
| **Fastest Mover** | CST — 0.52 phases/wk |
| **Most At-Risk** | PEBL — 0.03 phases/wk, 32 days idle, Stage 1 only |
| **Progressed Stages (since Feb 18)** | **1 client** — MALI (+2 stages) |
| **Regressed** | **1 client** — KRB (4,445 products bulk-deleted, lost images) |

---

## STAGE PROGRESSION (Feb 18 → Mar 2)

| Client | Feb 18 Stage | Mar 2 Stage | Delta | What Changed |
|--------|-------------|-------------|-------|--------------|
| **MALI** | 3 (30%) | **5 (30%)** | **+2** | Price levels added (0→4). Now blocked at customers |
| **TCD** | 5 (35%) | 5 (57%) | 0 | No stage change. Options strengthened (🟡→🟢). Readiness up |
| **CST** | 7 (85%) | 7 (60%) | 0 | Stable. 251 imports in 30d. Still needs order email |
| **DCCL** | 8 (75%) | 8 (80%) | 0 | Stable. Daily automated imports. Nearly complete |
| **KRB** | 6 (60%) | **2 (35%)** | **-4** | REGRESSION: 4,445 products deleted, 0 images remain. 30% import error rate |
| PEBL | N/A | 2 (14%) | -- | First full assessment |
| HVUSA | N/A | 6 (45%) | -- | First full assessment. Mature client (2020), severe data staleness |

**Clients that progressed: 1** (MALI)
**Clients that regressed: 1** (KRB — critical)
**Clients stable: 3** (TCD, CST, DCCL)

---

## PHASE-COMPLETION VELOCITY

| Client | Created | Weeks Active | Stages Passed | Velocity (phases/wk) | Trend |
|--------|---------|-------------|---------------|---------------------|-------|
| **CST** | 2025-12-11 | 11.6 | 6 | **0.52** | Rapid — daily imports active |
| **MALI** | 2025-11-21 | 14.4 | 3 | **0.21** | Moderate — catalog done, stuck at customers |
| **TCD** | 2025-10-16 | 19.6 | 4 | **0.20** | Moderate — catalog + pricing solid |
| **DCCL** | 2024-06-25 | 88.0 | 8 | **0.09** | Mature — nearly complete, slow polish |
| **HVUSA** | 2020-09-09 | 285.0 | 5 | **0.02** | Legacy client — catastrophic import errors |
| **KRB** | 2024-08-21 | 79.9 | 4 | **0.05** | Stalled — critical gaps persist |
| **PEBL** | 2025-07-24 | 31.3 | 1 | **0.03** | Stalled — minimal progress in 7+ months |

---

## STUCK PROJECTS (Idle > 7 Days)

| Client | Last Activity | Days Idle | Last Activity Type | Blocker |
|--------|--------------|-----------|-------------------|---------|
| **PEBL** | 2026-01-29 | **32 days** | Product import | No images, no customers, no pricing |
| **KRB** | 2026-02-05 | **25 days** | HelpScout ticket (onboarding intro) | 0 product images, inventory 12+ months stale |
| **HVUSA** | 2026-02-25 | **5 days** (imports) | Auto-import (99% errors) | Customer/inventory data 3.5 years stale, 99.3% import error rate |

### Borderline Watch

| Client | Last Activity | Days Idle | Notes |
|--------|--------------|-----------|-------|
| TCD | 2026-02-24 | 6 days | Product import ran — still active but at threshold |
| HVUSA | 2026-02-25 | 5 days | Imports running but 99.3% fail — active automation but broken pipeline |

---

## RECENT ACTIVITY REPORT

### Fathom Meetings (Last 30 Days)

**0 meetings** matched to any of the 6 target clients. All 9 meetings in the last 14 days were either internal or unrelated external (EGLO, Luho Design House, Loomcraft/Dorell).

- Clients with NO Fathom calls (30 days): **PEBL, MALI, TCD, CST, DCCL, KRB** (all six)

### HelpScout Tickets (Last 180 Days)

| Client | Total Tickets | Open/Pending | Most Recent | Channel |
|--------|--------------|-------------|-------------|---------|
| **DCCL** | 10 | 1 pending (#13962, 2/5) | #14027 - User enrollment (2/20) | Onboarding |
| **MALI** | 4 | 2 pending (#13861, #14005) | #14005 - Customer File Updates (2/16) | Onboarding |
| **KRB** | 5 | 1 pending (#13963, 2/5) | #13963 - Quick Intro (2/5) | Onboarding |
| **TCD** | 3 | 0 | #14011 - iPad entry page display (2/17) | Onboarding |
| **CST** | 2 | 1 pending (#13985, 2/10) | #13985 - Coaster/SuperCat: 2/10 Recap (2/10) | Onboarding |
| **PEBL** | 1 | 1 pending (#13879, 1/21) | #13879 - Assistance with eCAT (1/21) | Onboarding |

---

## CLIENT: PEBL (Pebl)

**Data Collection Date:** 2026-03-02
**Days Active:** 223
**Product(s):** eCat iPad (presumed)

### Stage Results

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 - Account Foundation | 🟢 | Org exists, 3 admin users |
| 2 - Catalog Setup | 🟡 | 123 products, 0 images, 6 categories, 5 collections |
| 3 - Pricing Configuration | 🔴 | 0 price levels |
| 4 - Option Configuration | 🟢 | 15 options configured |
| 5 - Customer & User Setup | 🔴 | 0 customers, 3 users (all admin), 1 user type |
| 6 - Operational Data | 🔴 | 0 inventory, 11 import errors, last import 2026-01-29 |
| 7 - iPad Order-Ready | 🔴 | 0 orders, 1 report format, 0 iPad activity, no order email |
| 8 - eCat Online Site | ⚪ | No mobile site configured |
| 9 - eCat Online Access | ⚪ | N/A |
| 10 - eCat Online Ordering | ⚪ | N/A |
| 11 - Sales Portal | ⚪ | N/A |

### Raw Metrics

- **Products:** 123
- **Products with Images:** 0
- **Categories:** 6
- **Collections:** 5
- **Price Levels:** 0
- **Options:** 15 records
- **Customers:** 0
- **Users:** 3 (3 admin, 0 non-admin)
- **User Types:** 1 (DefaultUserGroup)
- **Web Portal Configured:** No
- **Territories:** 0
- **Orders:** 0
- **iPad Orders (MixPanel):** 0
- **Report Formats:** 1
- **Last Product Update:** 2026-01-29
- **Last Customer Update:** N/A
- **Last Inventory Update:** N/A
- **Import Errors (total):** 11 of 26 events

### Current Stage & Readiness

- **Current Stage:** 2 - Catalog Setup (blocked by images + pricing)
- **Stages Passed:** 1 / 7
- **Readiness:** 14%

### Blockers Identified

1. **0 product images** — 123 products loaded but zero have images
2. **0 price levels** — No pricing configuration at all
3. **0 customers** — Customer file never imported
4. **0 inventory** — No inventory data
5. **No order email** — Order routing not configured
6. **32 days idle** — No import activity since Jan 29

### Validation Flags

| Flag | Source | Evidence |
|------|--------|----------|
| ⚠️ ACTIVITY | System | No Fathom calls in 30 days, last HelpScout ticket 1/21 (pending) |
| 🔴 STALLED | System | 32 days since last data activity |
| ⚠️ REVIEW | HelpScout #13879 | "Assistance with eCAT System" pending since 1/21 — unanswered? |

---

## CLIENT: MALI (Magic Lite)

**Data Collection Date:** 2026-03-02
**Days Active:** 101
**Product(s):** eCat iPad + eCat Online

### Stage Results

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 - Account Foundation | 🟢 | Org exists, 2 admin users |
| 2 - Catalog Setup | 🟢 | 906 products, 357 images, 12 categories, 50 collections. Updated 2/27 |
| 3 - Pricing Configuration | 🟢 | 4 price levels: ML DN, ML List, NSL DN, NSL List |
| 4 - Option Configuration | ⚪ | 0 options — N/A (not using options) |
| 5 - Customer & User Setup | 🔴 | 0 customers, 5 users (2 admin, 3 non-admin), 1 user type |
| 6 - Operational Data | 🟡 | 0 inventory, 9 import errors of 27 events, imports active thru 2/27 |
| 7 - iPad Order-Ready | 🔴 | 0 orders, 0 reports, 0 iPad activity, no order email |
| 8 - eCat Online Site | 🔴 | Site enabled but no cname, no title, no logo |
| 9 - eCat Online Access | 🟡 | 3 non-admin users exist, but only 1 user type |
| 10 - eCat Online Ordering | 🔴 | No order email configured |
| 11 - Sales Portal | ⚪ | Not enabled |

### Raw Metrics

- **Products:** 906
- **Products with Images:** 357
- **Categories:** 12
- **Collections:** 50
- **Price Levels:** 4 (ML DN, ML List, NSL DN, NSL List)
- **Options:** 0 records
- **Customers:** 0
- **Users:** 5 (2 admin, 3 non-admin)
- **User Types:** 1 (DefaultUserGroup)
- **Web Portal Configured:** Partially (enabled, no branding)
- **Territories:** 0
- **Orders:** 0
- **iPad Orders (MixPanel):** 0
- **Report Formats:** 0
- **Last Product Update:** 2026-02-27
- **Last Customer Update:** N/A
- **Last Inventory Update:** N/A
- **Import Errors (total):** 9 of 27 events

### Current Stage & Readiness

- **Current Stage:** 5 - Customer & User Setup (blocked by 0 customers)
- **Stages Passed:** 3 / 10 (iPad + eCat Online path)
- **Readiness:** 30%

### Blockers Identified

1. **0 customers** — Customer file never imported
2. **0 inventory** — No inventory data loaded
3. **Only 1 user type** — Need to configure user types beyond DefaultUserGroup
4. **eCat Online site has no branding** — No cname, title, or logo
5. **No order email** — Order routing not configured

### Validation Flags

| Flag | Source | Evidence |
|------|--------|----------|
| ✅ ACTIVE | System | Product imports running thru 2/27 — catalog work ongoing |
| ⚠️ ACTIVITY | Fathom | No Fathom calls in 30 days |
| ⚠️ REVIEW | HelpScout #14005 | "Customer File Updates" (2/16, pending) — actively working on customer data |
| ⚠️ REVIEW | HelpScout #13861 | "MagicLite + SuperCat Onboarding - Next Steps" (1/20, pending) |

---

## CLIENT: TCD (Terracotta Designs)

**Data Collection Date:** 2026-03-02
**Days Active:** 137
**Product(s):** eCat iPad

### Stage Results

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 - Account Foundation | 🟢 | Org exists, 2 admin users |
| 2 - Catalog Setup | 🟢 | 358 products, 348 images, 6 categories, 150 collections. Updated 2/24 |
| 3 - Pricing Configuration | 🟢 | 4 price levels: Dealer Net, IMAP, Designer Price, Showroom 50% |
| 4 - Option Configuration | 🟢 | 222 options configured |
| 5 - Customer & User Setup | 🔴 | 0 customers, 2 users (all admin), 1 user type |
| 6 - Operational Data | 🟡 | 348 inventory (stale: 2025-12-19 = 73 days), 9 errors of 40 events |
| 7 - iPad Order-Ready | 🔴 | 0 orders, 1 report format, 0 iPad activity, order email = ✅ |
| 8 - eCat Online Site | ⚪ | No mobile site configured |
| 9 - eCat Online Access | ⚪ | N/A |
| 10 - eCat Online Ordering | ⚪ | N/A |
| 11 - Sales Portal | ⚪ | N/A |

### Raw Metrics

- **Products:** 358
- **Products with Images:** 348
- **Categories:** 6
- **Collections:** 150
- **Price Levels:** 4 (Dealer Net, IMAP, Designer Price, Showroom 50%)
- **Options:** 222 records
- **Customers:** 0
- **Users:** 2 (2 admin, 0 non-admin)
- **User Types:** 1 (DefaultUserGroup)
- **Web Portal Configured:** No
- **Territories:** 0
- **Orders:** 0
- **iPad Orders (MixPanel):** 0
- **Report Formats:** 1
- **Last Product Update:** 2026-02-24
- **Last Customer Update:** N/A
- **Last Inventory Update:** 2025-12-19 (73 days stale)
- **Import Errors (total):** 9 of 40 events

### Current Stage & Readiness

- **Current Stage:** 5 - Customer & User Setup (blocked by 0 customers)
- **Stages Passed:** 4 / 7
- **Readiness:** 57%

### Blockers Identified

1. **0 customers** — Customer file never imported
2. **Only 2 users, both admin** — No rep/non-admin users
3. **Only 1 user type** — Need to configure user types
4. **Inventory stale** — Last updated 73 days ago (2025-12-19)
5. **Only 1 report format** — Need at least 3 for iPad readiness

### Validation Flags

| Flag | Source | Evidence |
|------|--------|----------|
| ✅ ACTIVE | System | Product imports running thru 2/24 — catalog maintained |
| ⚠️ ACTIVITY | Fathom | No Fathom calls in 30 days |
| ✅ ACTIVE | HelpScout #14011 | "iPad entry page display" (2/17, closed) — actively testing iPad |
| ⚠️ TIMELINE | HelpScout | Onboarding kickoff was 2025-11-11 — 16 weeks ago, still at Stage 5 |

---

## CLIENT: CST (Coaster Furniture)

**Data Collection Date:** 2026-03-02
**Days Active:** 81
**Product(s):** eCat iPad + eCat Online

### Stage Results

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 - Account Foundation | 🟢 | Org exists, 3 admin users |
| 2 - Catalog Setup | 🟢 | 5,359 products, 5,126 images, 44 categories, 1,286 collections. Updated 2/27 |
| 3 - Pricing Configuration | 🟢 | 34 price levels (zone/tier pricing system) |
| 4 - Option Configuration | 🟢 | 2,257 options configured |
| 5 - Customer & User Setup | 🟢 | 6,176 customers, 53 users (3 admin, 50 non-admin), 8 user types. Updated 2/24 |
| 6 - Operational Data | 🟢 | 4,622 inventory records, updated 2/24. 251 imports in 30d, 35 with minor warnings |
| 7 - iPad Order-Ready | 🟡 | 8 user types ✓, 3 report formats ✓, 8 orders ✓, but 0 MixPanel iPad activity, no order email |
| 8 - eCat Online Site | 🟡 | Site enabled, but no cname, title, or logo |
| 9 - eCat Online Access | 🟢 | 50 non-admin users, 8 user types |
| 10 - eCat Online Ordering | 🔴 | No order email configured |
| 11 - Sales Portal | ⚪ | Not enabled |

### Raw Metrics

- **Products:** 5,359
- **Products with Images:** 5,126
- **Categories:** 44
- **Collections:** 1,286
- **Price Levels:** 34 (Landed, BCK, BM, CDN, DSFOB, M1-M10 zones, Z1-Z3 tiers)
- **Options:** 2,257 records
- **Customers:** 6,176
- **Users:** 53 (3 admin, 50 non-admin)
- **User Types:** 8 (Admins, Canada, FL + Landed, Sales Reps Zone 1-3 LD/CH/TX/FL/NJ)
- **Web Portal Configured:** Partially (enabled, no branding)
- **Territories:** 0
- **Orders:** 8
- **iPad Orders (MixPanel):** 0
- **Report Formats:** 3
- **Last Product Update:** 2026-02-27
- **Last Customer Update:** 2026-02-24
- **Last Inventory Update:** 2026-02-24
- **Import Errors (30 days):** 35 of 251 events (warnings: unknown field names, sRGB colorspace)

### Current Stage & Readiness

- **Current Stage:** 7 - iPad Order-Ready (blocked by order email + iPad testing)
- **Stages Passed:** 6 / 10 (iPad + eCat Online path)
- **Readiness:** 60%

### Blockers Identified

1. **No order email configured** — Blocks both iPad ordering (Stage 7) and eCat Online ordering (Stage 10)
2. **0 MixPanel iPad orders** — iPad app not yet tested with real orders
3. **eCat Online has no branding** — No cname, title, or logo configured
4. **Import warnings** — Unknown field names (bulbincluded, bulbwattage, etc.) and sRGB colorspace issues

### Validation Flags

| Flag | Source | Evidence |
|------|--------|----------|
| ✅ ACTIVE | System | Continuous imports — 251 events in 30 days, last 2/27 |
| ⚠️ ACTIVITY | Fathom | No Fathom calls in 30 days |
| ⚠️ REVIEW | HelpScout #13985 | "Coaster / SuperCat: 2/10 Recap" (pending since 2/10) — 20 days with no follow-up |
| ⚠️ UNFULFILLED | System | 0 territories configured — needed if Sales Portal is planned |

---

## CLIENT: DCCL (Donald Choi Canada)

**Data Collection Date:** 2026-03-02
**Days Active:** 616
**Product(s):** eCat iPad + eCat Online

### Stage Results

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 - Account Foundation | 🟢 | Org exists, 3 admin users |
| 2 - Catalog Setup | 🟢 | 2,367 products, 2,271 images, 74 categories, 184 collections. Updated 2/17 |
| 3 - Pricing Configuration | 🟢 | 3 price levels: Designer Price, Warehouse Price, warehouse2 |
| 4 - Option Configuration | 🟡 | 2 options (> 0 but < 5) |
| 5 - Customer & User Setup | 🟢 | 353 customers, 14 users (3 admin, 11 non-admin), 7 user types. Customer updated today |
| 6 - Operational Data | 🟢 | 1,213 inventory, updated today. 3 errors in 36 imports (30d) — minor warnings |
| 7 - iPad Order-Ready | 🟡 | 7 user types ✓, 5 reports ✓, 409 orders ✓, order email ✓, but 0 MixPanel iPad activity |
| 8 - eCat Online Site | 🟡 | Site enabled, cname = b2b.choihome.ca ✓, no title, no logo |
| 9 - eCat Online Access | 🟢 | 11 non-admin users, 7 user types (incl. eOL Public Site, stores_full) |
| 10 - eCat Online Ordering | 🟢 | Order email: customerservice@donaldchoi.com ✓, send_on_submit = true ✓ |
| 11 - Sales Portal | ⚪ | Not enabled |

### Raw Metrics

- **Products:** 2,367
- **Products with Images:** 2,271
- **Categories:** 74
- **Collections:** 184
- **Price Levels:** 3 (Designer Price, Warehouse Price, warehouse2)
- **Options:** 2 records
- **Customers:** 353
- **Users:** 14 (3 admin, 11 non-admin)
- **User Types:** 7 (CDN Reps EN, CDN Reps FR, Default, Managers, eOL Public Site, stores_full, stores_staff_wh2.0)
- **Web Portal Configured:** Yes (b2b.choihome.ca)
- **Territories:** 0
- **Orders:** 409
- **iPad Orders (MixPanel):** 0
- **Report Formats:** 5
- **Last Product Update:** 2026-02-17
- **Last Customer Update:** 2026-03-02 (today)
- **Last Inventory Update:** 2026-03-02 (today)
- **Import Errors (30 days):** 3 of 36 events (warnings: product not found for 2-3 BaseItemCodes)

### Current Stage & Readiness

- **Current Stage:** 8 - eCat Online Site (finishing branding polish)
- **Stages Passed:** 8 / 10 (iPad + eCat Online path)
- **Readiness:** 80%

### Blockers Identified

1. **eCat Online site missing logo** — document_logo_file_name is null
2. **Options only 2 configured** — May not be a blocker if options aren't used extensively
3. **0 MixPanel iPad activity** — iPad may not be the primary channel; 409 orders exist

### Validation Flags

| Flag | Source | Evidence |
|------|--------|----------|
| ✅ ACTIVE | System | Automated imports running daily (customers, inventory, sales data updated today) |
| ✅ CONFIRMED | HelpScout #14027 | "User enrollment" (2/20, closed) — actively configuring user access |
| ⚠️ REVIEW | HelpScout #13962 | "Quick SuperCat Update" (2/5, pending) — 25 days pending |
| ⚠️ REVIEW | Import | DCCL import on 2/6 had :error entries in Sales Data (base item codes not matching products) |

---

## CLIENT: KRB (Kaleen Rugs & Broadloom)

**Data Collection Date:** 2026-03-02
**Days Active:** 559
**Product(s):** eCat iPad (presumed)

### Stage Results

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 - Account Foundation | 🟢 | Org exists, 6 admin users |
| 2 - Catalog Setup | 🟡 | 1,493 products but **0 images**, 2 categories, 28 collections. Last update 2025-12-03 |
| 3 - Pricing Configuration | 🟢 | 18 price levels (CCA, CAN, Luxe, eCommerce tiers) |
| 4 - Option Configuration | ⚪ | 0 options — N/A |
| 5 - Customer & User Setup | 🟢 | 2,208 customers, 35 users (6 admin, 29 non-admin), 5 user types. BUT customers stale (2025-09-09) |
| 6 - Operational Data | 🔴 | 2,509 inventory but **12+ months stale** (2025-02-23). 103 errors of 345 imports (30% error rate). Last import 2025-12-03 |
| 7 - iPad Order-Ready | 🔴 | 5 user types ✓, 0 iPad ✗, 1 report ✗, 2 orders (test?), no order email ✗ |
| 8 - eCat Online Site | ⚪ | No mobile site configured |
| 9 - eCat Online Access | ⚪ | N/A |
| 10 - eCat Online Ordering | ⚪ | N/A |
| 11 - Sales Portal | ⚪ | N/A |

### Raw Metrics

- **Products:** 1,493
- **Products with Images:** 0
- **Categories:** 2
- **Collections:** 28
- **Price Levels:** 18 (CCA x4, CAN 8/10%, Luxe 5/8/10/12/15%, eCommerce 8/10%, 2011 Price List, 5/8/10/12/15%)
- **Options:** 0 records
- **Customers:** 2,208
- **Users:** 35 (6 admin, 29 non-admin)
- **User Types:** 5 (All Products - All Price Levels, BL & Luxe Standard Levels, BL Only Group, CAN ONLY, Luxe Only)
- **Web Portal Configured:** No
- **Territories:** 0
- **Orders:** 2
- **iPad Orders (MixPanel):** 0
- **Report Formats:** 1
- **Last Product Update:** 2025-12-03 (89 days stale)
- **Last Customer Update:** 2025-09-09 (174 days stale)
- **Last Inventory Update:** 2025-02-23 (372 days stale)
- **Import Errors (all time):** 103 of 345 events (30% error rate)

### Current Stage & Readiness

- **Current Stage:** 2 - Catalog Setup (blocked by 0 images + stale data across the board)
- **Stages Passed:** 4 / 7 (but with critical data freshness gaps)
- **Readiness:** 35%

### Blockers Identified

1. **0 product images** — 1,493 products with zero images
2. **Inventory 12+ months stale** — Last updated 2025-02-23
3. **Customer data 6 months stale** — Last updated 2025-09-09
4. **Product data 3 months stale** — Last updated 2025-12-03
5. **30% import error rate** — 103 errors across 345 import events
6. **No order email** — Order routing not configured
7. **Only 1 report format** — Need at least 3 for iPad readiness
8. **25 days idle** — No import activity since Dec 3, 2025; last HelpScout was a "Quick Intro" on Feb 5

### Validation Flags

| Flag | Source | Evidence |
|------|--------|----------|
| 🔴 STALLED | System | 89 days since last import, all data going stale |
| ⚠️ ACTIVITY | Fathom | No Fathom calls in 30 days |
| ⚠️ REVIEW | HelpScout #13963 | "Quick Intro - SuperCat Onboarding" (2/5, pending) — re-engagement attempt? |
| ⚠️ TIMELINE | HelpScout | Historical: "Status Update for Kaleen" (10/28), "eCat checklist" (10/31), "today's meeting" (12/15) — sporadic engagement |

---

## CLIENT: HVUSA (Hudson Valley Group - USA)

**Data Collection Date:** 2026-03-02
**Days Active:** 1,999 (created 2020-09-09)
**HubSpot Lifecycle:** Customer (not Onboarding) — mature/legacy client
**Product(s):** eCat iPad

### Stage Results

| Stage | Status | Evidence |
|-------|--------|----------|
| 1 - Account Foundation | 🟢 | Org exists, 3 admin users |
| 2 - Catalog Setup | 🟢 | 11,715 products, 4,074 images (35%), 22 categories, 2,605 collections. Updated 2/25 |
| 3 - Pricing Configuration | 🟢 | 5 price levels: IMAP, Wholesale +12%, DN, Confidential Net +25%, Designer Net +50% |
| 4 - Option Configuration | ⚪ | 0 options — N/A |
| 5 - Customer & User Setup | 🟡 | 14,224 customers, 4 users (3 admin, 1 non-admin), 2 user types. BUT customer data 3.5 years stale (2022-08-08) |
| 6 - Operational Data | 🔴 | 4,999 inventory — **3.5 years stale** (2022-08-08). 7,905 of 7,963 imports have errors (**99.3% error rate**) |
| 7 - iPad Order-Ready | 🔴 | 2 user types ✓, 5 report formats ✓, but 0 orders, 0 iPad activity, no order email |
| 8 - eCat Online Site | ⚪ | No mobile site configured |
| 9 - eCat Online Access | ⚪ | N/A |
| 10 - eCat Online Ordering | ⚪ | N/A |
| 11 - Sales Portal | ⚪ | N/A |

### Raw Metrics

- **Products:** 11,715
- **Products with Images:** 4,074
- **Categories:** 22
- **Collections:** 2,605
- **Price Levels:** 5 (IMAP, Wholesale +12%, DN, Confidential Net +25%, Designer Net +50%)
- **Options:** 0 records
- **Customers:** 14,224
- **Users:** 4 (3 admin, 1 non-admin)
- **User Types:** 2 (Admins, Reps)
- **Web Portal Configured:** No
- **Territories:** 0
- **Orders:** 0
- **iPad Orders (MixPanel):** 0
- **Report Formats:** 5
- **Last Product Update:** 2026-02-25
- **Last Customer Update:** 2022-08-08 (3.5 years stale)
- **Last Inventory Update:** 2022-08-08 (3.5 years stale)
- **Import Events:** 7,963 total, 7,905 with errors (99.3% error rate)
- **Last Import:** 2026-02-25 (5 days ago — auto-imports are running)

### Current Stage & Readiness

- **Current Stage:** 6 - Operational Data (blocked by catastrophic import errors + stale inventory/customers)
- **Stages Passed:** 5 / 7
- **Readiness:** 45%

### Blockers Identified

1. **99.3% import error rate** — 7,905 of 7,963 import events have errors. Automated pipeline is broken
2. **Customer data 3.5 years stale** — Last updated 2022-08-08
3. **Inventory data 3.5 years stale** — Last updated 2022-08-08
4. **No order email** — Order routing not configured
5. **0 orders, 0 iPad activity** — Platform never reached active usage
6. **Only 4 users** — Low adoption for a 5-year-old account with 14,224 customers

### Validation Flags

| Flag | Source | Evidence |
|------|--------|----------|
| 🔴 STALLED | System | Customer + inventory data unchanged since Aug 2022 |
| 🔴 BLOCKER | System | 99.3% import error rate — automated pipeline running but broken |
| ⚠️ ACTIVITY | Fathom | 0 Fathom calls in 30 days |
| ⚠️ REVIEW | HelpScout #13991 | "HVLG eCat Consolidation" (2/11, closed) — consolidation may explain data state |

---

## VELOCITY + STUCK ANALYSIS

### Phase-Completion Velocity Detail

```
CST   ████████████████████████████████████████████████████  0.52 ph/wk  ← Leader
MALI  █████████████████████                                 0.21 ph/wk
TCD   ████████████████████                                  0.20 ph/wk
DCCL  █████████                                             0.09 ph/wk  ← Mature
KRB   █████                                                 0.05 ph/wk  ← Stalled
PEBL  ███                                                   0.03 ph/wk  ← Stalled
HVUSA ██                                                    0.02 ph/wk  ← Legacy/Broken
```

### Stuck Project Risk Matrix

| Client | Days Idle | Stages Passed | Risk Level | Recommended Action |
|--------|-----------|---------------|------------|-------------------|
| **PEBL** | 32 | 1 / 7 | 🔴 HIGH | Immediate outreach — may be churning. Only 1 pending ticket since Jan |
| **KRB** | 25 | 4 / 7 | 🔴 HIGH | Re-engagement call needed. Images are the #1 blocker — 559 days in, 0 images. **4,445 products deleted since Feb 18** |
| **HVUSA** | 5* | 5 / 7 | 🔴 HIGH | Import pipeline catastrophically broken (99.3% errors). Customer + inventory 3.5 years stale. Consolidation ticket suggests restructuring underway |
| **CST** | 3 | 6 / 10 | 🟡 MEDIUM | Active imports but no order email configured — single blocker for 2 stages |
| **TCD** | 6 | 4 / 7 | 🟡 MEDIUM | Catalog is solid. Customer import is the gate — prioritize file request |
| **MALI** | 3 | 3 / 10 | 🟡 MEDIUM | Customer file thread open (#14005, pending) — follow up to unblock Stage 5 |
| **DCCL** | 0 | 8 / 10 | 🟢 LOW | Automated imports running daily. Polish items: logo upload, site branding |

*HVUSA: imports run every few days but 99.3% fail — "active" but broken

### Cohort Benchmarks

| Cohort | Clients | Avg Velocity | Avg Readiness |
|--------|---------|-------------|---------------|
| On Track (active, > 0.15 ph/wk) | CST, MALI, TCD | 0.31 ph/wk | 49% |
| Mature (> 6 months, > 70% ready) | DCCL | 0.09 ph/wk | 80% |
| Stalled (idle > 7d or < 0.06 ph/wk) | PEBL, KRB, HVUSA | 0.03 ph/wk | 31% |

---

## NEXT STEPS (Recommended)

1. **PEBL** — Schedule an intervention call. 32 days idle + 7 months in with only Stage 1 passed = at-risk.
2. **KRB** — Investigate 4,445 bulk product deletions. Image delivery is the #1 blocker. 559 days in, 0 images on active products.
3. **HVUSA** — Diagnose import pipeline (99.3% error rate). Customer + inventory data 3.5 years stale. "eCat Consolidation" ticket (2/11) may mean restructuring — confirm status with Chris K.
4. **CST** — Request order email recipient. This single config change unblocks Stage 7 and Stage 10.
5. **MALI** — Follow up on HelpScout #14005 (Customer File Updates). Customer import unblocks Stage 5.
6. **TCD** — Request customer file. Catalog + pricing are strong; customers are the only gate.
7. **DCCL** — Upload logo and set site title to complete eCat Online branding.
