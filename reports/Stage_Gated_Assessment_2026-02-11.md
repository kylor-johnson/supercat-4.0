# Stage-Gated Onboarding Assessment
## February 11th, 2026 - Full Product Suite

**Assessment Date:** February 11, 2026  
**Clients Assessed:** PEBL, MALI, TCD, CST, KRB, DCCL  
**Data Sources:**
- PostgreSQL (SuperCat production database) - Current as of Feb 11, 2026
- BigQuery (Fathom, Help Scout, Mixpanel) - **⚠️ STALE** (Last sync: Fathom Feb 4, Help Scout Feb 5)
- Manual Validation Data - Feb 5-10, 2026 (for CST, DCCL, MALI, TCD, KLL)

---

## ⚠️ DATA FRESHNESS ALERT

**BigQuery Data Staleness:**
- **Fathom:** Last sync February 4, 2026 (7 days stale)
- **Help Scout:** Last sync February 5, 2026 (6 days stale)
- **Mitigation:** Using manual validation data from `MANUAL_VALIDATION_DATA_2026-02-11.md` for recent activity

**Help Scout Sync Update:** Now syncing every 30 minutes (updated Feb 11, 2026)

---

## QUANTITATIVE DATA COLLECTION (Stage_Gated_Data_Collection.md)

### PEBL (Pebl)

**Organization Info:**
- **Name:** Pebl
- **Shortname:** pebl
- **Status:** onboarding
- **Created:** July 24, 2025
- **Days Active:** ~201 days

**Stage 1: Account Foundation**
- ✅ Organization exists: YES
- ✅ Order email configured: NO (blank)
- ✅ Company info complete: Minimal

**Stage 2: Catalog Setup**
- Products: 1,251
- Product images: 244 images
- Categories/taxonomies: 18
- Last update: N/A

**Stage 3: Pricing**
- Price levels: 0
- Price level names: None

**Stage 4: Options**
- Options configured: 15

**Stage 5: Customer & User Setup**
- Customers: 0
- Users (non-SuperCat): 4
- Admin users: 3
- User groups: 1

**Stage 6: Operations**
- Orders (all time): 0
- iPad activity (90 days): No data available (BigQuery stale)

**Stage 7: Order Ready**
- Submitted orders: 0

**Stage 8: eCat Online Site Setup**
- Site enabled: NO
- Web portal configured: NO
- Logo uploaded: Unknown

**Raw Metrics:**
```json
{
  "organization": "pebl",
  "created_at": "2025-07-24",
  "days_active": 201,
  "status": "onboarding",
  "products": 1251,
  "images": 244,
  "categories": 18,
  "price_levels": 0,
  "options": 15,
  "customers": 0,
  "users": 4,
  "admins": 3,
  "user_groups": 1,
  "orders": 0,
  "mobile_site_enabled": false,
  "web_portal_configured": false
}
```

---

### MALI (Magic Lite)

**Organization Info:**
- **Name:** Magic Lite
- **Shortname:** mali
- **Status:** onboarding
- **Created:** November 21, 2025
- **Days Active:** ~82 days

**Stage 1: Account Foundation**
- ✅ Organization exists: YES
- ✅ Order email configured: NO (blank)
- ✅ Company info complete: Minimal

**Stage 2: Catalog Setup**
- Products: 906
- Product images: 528 images
- Categories/taxonomies: 64
- Last update: N/A

**Stage 3: Pricing**
- Price levels: 0
- Price level names: None

**Stage 4: Options**
- Options configured: 0

**Stage 5: Customer & User Setup**
- Customers: 0
- Users (non-SuperCat): 7
- Admin users: 3
- User groups: 1

**Stage 6: Operations**
- Orders (all time): 0
- iPad activity (90 days): No data available (BigQuery stale)

**Stage 7: Order Ready**
- Submitted orders: 0

**Stage 8: eCat Online Site Setup**
- Site enabled: YES (enable_online_catalog = true)
- Web portal configured: NO (custom_cname = null, title = blank)
- Logo uploaded: Unknown

**Raw Metrics:**
```json
{
  "organization": "mali",
  "created_at": "2025-11-21",
  "days_active": 82,
  "status": "onboarding",
  "products": 906,
  "images": 528,
  "categories": 64,
  "price_levels": 0,
  "options": 0,
  "customers": 0,
  "users": 7,
  "admins": 3,
  "user_groups": 1,
  "orders": 0,
  "mobile_site_enabled": true,
  "web_portal_configured": false
}
```

---

### TCD (Terracotta Designs)

**Organization Info:**
- **Name:** Terracotta Designs
- **Shortname:** tcd
- **Status:** inactive
- **Created:** October 16, 2025
- **Days Active:** ~118 days

**Stage 1: Account Foundation**
- ✅ Organization exists: YES
- ✅ Order email configured: NO (blank)
- ✅ Company info complete: Minimal

**Stage 2: Catalog Setup**
- Products: 441
- Product images: 638 images
- Categories/taxonomies: 159
- Last update: N/A

**Stage 3: Pricing**
- Price levels: 4
- Price level names: Dealer Net, Designer Price, IMAP, Showroom 50%

**Stage 4: Options**
- Options configured: 222

**Stage 5: Customer & User Setup**
- Customers: 0
- Users (non-SuperCat): 4
- Admin users: 2
- User groups: 1

**Stage 6: Operations**
- Orders (all time): 0
- iPad activity (90 days): No data available (BigQuery stale)

**Stage 7: Order Ready**
- Submitted orders: 0

**Stage 8: eCat Online Site Setup**
- Site enabled: NO
- Web portal configured: NO
- Logo uploaded: Unknown

**Raw Metrics:**
```json
{
  "organization": "tcd",
  "created_at": "2025-10-16",
  "days_active": 118,
  "status": "inactive",
  "products": 441,
  "images": 638,
  "categories": 159,
  "price_levels": 4,
  "price_level_names": "Dealer Net, Designer Price, IMAP, Showroom 50%",
  "options": 222,
  "customers": 0,
  "users": 4,
  "admins": 2,
  "user_groups": 1,
  "orders": 0,
  "mobile_site_enabled": false,
  "web_portal_configured": false
}
```

---

### CST (Coaster Furniture)

**Organization Info:**
- **Name:** Coaster Furniture
- **Shortname:** cst
- **Status:** inactive
- **Created:** December 11, 2025
- **Days Active:** ~62 days

**Stage 1: Account Foundation**
- ✅ Organization exists: YES
- ✅ Order email configured: NO (blank)
- ✅ Company info complete: Partial

**Stage 2: Catalog Setup**
- Products: 7,551
- Product images: Unknown (query timed out)
- Categories/taxonomies: 1,338
- Last update: N/A

**Stage 3: Pricing**
- Price levels: 31
- Price level names: BCK, BM, CDN, DSFOB, DSFOB (C4), DSFOB (C6), Landed Pricing Pricelist, M1 Z1-Z3, M2 Z1-Z3, M3 Z1-Z3, M4 Z1-Z3, M5 Z1-Z3, M10 Zone 1-3, Z1T1-T2, Z2T1-T2, Z3T1-T2

**Stage 4: Options**
- Options configured: 2,308

**Stage 5: Customer & User Setup**
- Customers: 6,294
- Last customer update: January 21, 2026
- Users (non-SuperCat): 55
- Admin users: 6
- User groups: 8

**Stage 6: Operations**
- Orders (all time): 7
- iPad activity (90 days): No data available (BigQuery stale)

**Stage 7: Order Ready**
- Submitted orders: 7

**Stage 8: eCat Online Site Setup**
- Site enabled: YES (enable_online_catalog = true)
- Web portal configured: NO (custom_cname = null, title = blank)
- Logo uploaded: Unknown

**Raw Metrics:**
```json
{
  "organization": "cst",
  "created_at": "2025-12-11",
  "days_active": 62,
  "status": "inactive",
  "products": 7551,
  "images": "unknown",
  "categories": 1338,
  "price_levels": 31,
  "options": 2308,
  "customers": 6294,
  "last_customer_update": "2026-01-21",
  "users": 55,
  "admins": 6,
  "user_groups": 8,
  "orders": 7,
  "mobile_site_enabled": true,
  "web_portal_configured": false
}
```

---

### KRB (Kaleen Rugs & Broadloom)

**Organization Info:**
- **Name:** Kaleen Rugs & Broadloom
- **Shortname:** krb
- **Status:** active
- **Created:** August 21, 2024
- **Days Active:** ~539 days (365+)

**Stage 1: Account Foundation**
- ✅ Organization exists: YES
- ✅ Order email configured: NO (blank)
- ✅ Company info complete: YES (GA address)

**Stage 2: Catalog Setup**
- Products: 7,665
- Product images: Unknown (query timed out)
- Categories/taxonomies: 35
- Last update: N/A

**Stage 3: Pricing**
- Price levels: 19
- Price level names: 10%, 12%, 15%, 2011 Price List 12%, 5% MGMT ONLY, 8%, CAN 10%, CAN 8%, CCA, Luxe 10%, Luxe 12%, Luxe 15%, Luxe 5% MGMT Only, Luxe 8%, eCommerce 10%, eCommerce 8%

**Stage 4: Options**
- Options configured: 0

**Stage 5: Customer & User Setup**
- Customers: 2,208
- Last customer update: September 9, 2025
- Users (non-SuperCat): 38
- Admin users: 9
- User groups: 5

**Stage 6: Operations**
- Orders (all time): 2
- iPad activity (90 days): No data available (BigQuery stale)

**Stage 7: Order Ready**
- Submitted orders: 2

**Stage 8: eCat Online Site Setup**
- Site enabled: NO
- Web portal configured: NO
- Logo uploaded: Unknown

**Raw Metrics:**
```json
{
  "organization": "krb",
  "created_at": "2024-08-21",
  "days_active": 539,
  "status": "active",
  "products": 7665,
  "images": "unknown",
  "categories": 35,
  "price_levels": 19,
  "options": 0,
  "customers": 2208,
  "last_customer_update": "2025-09-09",
  "users": 38,
  "admins": 9,
  "user_groups": 5,
  "orders": 2,
  "mobile_site_enabled": false,
  "web_portal_configured": false
}
```

---

### DCCL (Donald Choi Canada)

**Organization Info:**
- **Name:** Donald Choi Canada
- **Shortname:** dccl
- **Status:** active
- **Created:** June 25, 2024
- **Days Active:** ~596 days (365+)

**Stage 1: Account Foundation**
- ✅ Organization exists: YES
- ✅ Order email configured: YES (customerservice@donaldchoi.com)
- ✅ Company info complete: YES (ON address)

**Stage 2: Catalog Setup**
- Products: 2,682
- Product images: Unknown (query timed out)
- Categories/taxonomies: 283
- Last update: N/A

**Stage 3: Pricing**
- Price levels: 3
- Price level names: Designer Price, Warehouse Price, warehouse2

**Stage 4: Options**
- Options configured: 2

**Stage 5: Customer & User Setup**
- Customers: 351
- Last customer update: February 9, 2026
- Users (non-SuperCat): 19
- Admin users: 8
- User groups: 4

**Stage 6: Operations**
- Orders (all time): 400
- iPad activity (90 days): No data available (BigQuery stale)

**Stage 7: Order Ready**
- Submitted orders: 400

**Stage 8: eCat Online Site Setup**
- Site enabled: YES (enable_online_catalog = true)
- Web portal configured: YES (custom_cname = b2b.choihome.ca)
- Logo uploaded: Unknown

**Raw Metrics:**
```json
{
  "organization": "dccl",
  "created_at": "2024-06-25",
  "days_active": 596,
  "status": "active",
  "products": 2682,
  "images": "unknown",
  "categories": 283,
  "price_levels": 3,
  "price_level_names": "Designer Price, Warehouse Price, warehouse2",
  "options": 2,
  "customers": 351,
  "last_customer_update": "2026-02-09",
  "users": 19,
  "admins": 8,
  "user_groups": 4,
  "orders": 400,
  "mobile_site_enabled": true,
  "web_portal_configured": true,
  "custom_cname": "b2b.choihome.ca"
}
```

---

## STAGE-GATED ASSESSMENT RESULTS

### PEBL (Pebl)

**Current Stage:** 2 / 7  
**Readiness:** 20%  
**Status:** 🔴 STALLED

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟢 | 1,251 products, 244 images, 18 categories |
| 3 | 🔴 | **0 price levels** (RED BLOCKER - Cannot proceed) |
| 4 | 🟢 | 15 options |
| 5 | 🔴 | **0 customers** (RED BLOCKER - Cannot proceed) |
| 6 | 🔴 | **0 orders** |
| 7 | 🔴 | **No iPad activity** |

**Biggest Blocker:** 0 price levels, 0 customers, 0 engagement

**Validation Status:** 🔴 2 flags

**🎯 V11 Next Action:** 🚫 OUTREACH REQUIRED - Confirm client engagement (201 days since account creation, no activity)

---

### MALI (Magic Lite)

**Current Stage:** 2 / 7  
**Readiness:** 30%  
**Status:** ⚠️ ACTIVE ENGAGEMENT

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: onboarding |
| 2 | 🟢 | 906 products, 528 images, 64 categories |
| 3 | 🔴 | **0 price levels** (RED BLOCKER - Cannot proceed) |
| 4 | ⚫ | N/A - Options not configured |
| 5 | 🔴 | **0 customers** (RED BLOCKER - Cannot proceed) |
| 6 | 🔴 | **0 orders** |
| 7 | 🔴 | **No iPad activity** |
| 8 | 🟡 | Site enabled but no web portal branding |

**Biggest Blocker:** 0 price levels, 0 customers - but actively working on data files

**Validation Status:** ⚠️ 2 flags (ACTIVE)

**🎯 V11 Next Action:** Configure price levels and import customer data - client is actively engaged with multi-party collaboration (Magic Lite, SuperCat, Endeavour Solutions)

---

### TCD (Terracotta Designs)

**Current Stage:** 3 / 7  
**Readiness:** 35%  
**Status:** ⚠️ DELAYED

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟡 | 441 products, 638 images, 159 categories - but status "inactive" |
| 3 | 🟢 | 4 price levels (Dealer Net, Designer Price, IMAP, Showroom 50%) |
| 4 | 🟢 | 222 options |
| 5 | 🔴 | **0 customers** (RED BLOCKER - Cannot proceed) |
| 6 | 🔴 | **0 orders** |
| 7 | 🔴 | **No iPad activity** |

**Biggest Blocker:** 0 customers, client overwhelmed with other priorities

**Validation Status:** ⚠️ 2 flags

**🎯 V11 Next Action:** Import customer data (Stage 5 blocker) - client apologized for delay, hopes to have time "next week"

---

### CST (Coaster Furniture)

**Current Stage:** 7 / 7  
**Readiness:** 85%  
**Status:** ⚠️ ACTIVE ENGAGEMENT (BLOCKERS)

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟢 | 7,551 products, 1,338 categories |
| 3 | 🟢 | 31 price levels configured |
| 4 | 🟢 | 2,308 options |
| 5 | 🟢 | 6,294 customers (last updated Jan 21, 2026) |
| 6 | 🟢 | 55 users, 8 user groups |
| 7 | 🟡 | 7 orders submitted - but image import failures and customer file validation errors |
| 8 | 🟡 | Site enabled but no web portal branding |

**Biggest Blocker:** Image import failures, customer file validation errors blocking full launch

**Validation Status:** 🔴 2 flags / ⚠️ 2 flags

**🎯 V11 Next Action:** Resolve image import failures (6-image limit, API format mismatch) and customer file validation errors - actively working with weekly standups

---

### KRB (Kaleen Rugs & Broadloom)

**Current Stage:** 7 / 7  
**Readiness:** 75%  
**Status:** ⚠️ REVIEW (NEAR LAUNCH)

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: active |
| 2 | 🟢 | 7,665 products, 35 categories |
| 3 | 🟢 | 19 price levels configured |
| 4 | ⚫ | N/A - Options not configured |
| 5 | 🟢 | 2,208 customers (last updated Sep 9, 2025) |
| 6 | 🟢 | 38 users, 5 user groups |
| 7 | 🟡 | 2 orders submitted - minimal activity |

**Biggest Blocker:** Minimal order activity despite 365+ days active, waiting on CAMS integration

**Validation Status:** ⚠️ 2 flags

**🎯 V11 Next Action:** Schedule alignment call with Cole (Kaleen) - client believes "ever so close to full launch moment" after CAMS meeting

---

### DCCL (Donald Choi Canada)

**Current Stage:** 8 / 8  
**Readiness:** 95%  
**Status:** ✅ CONFIRMED (READY FOR CUSTOMER ONBOARDING)

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: active |
| 2 | 🟢 | 2,682 products, 283 categories |
| 3 | 🟢 | 3 price levels configured |
| 4 | 🟢 | 2 options |
| 5 | 🟢 | 351 customers (last updated Feb 9, 2026) |
| 6 | 🟢 | 19 users, 4 user groups |
| 7 | 🟢 | 400 orders submitted |
| 8 | 🟢 | Site enabled, web portal configured (b2b.choihome.ca) |

**Biggest Blocker:** None - launch blockers resolved, ready for customer onboarding

**Validation Status:** ✅ Confirmed / ⚠️ 1 flag (onboarding collateral needed)

**🎯 V11 Next Action:** Send onboarding collateral (admin guides, customer-facing materials) and schedule follow-up in one week

---

## VALIDATION FLAGS SUMMARY (Validation_Layer_Fathom_HelpScout.md)

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| PEBL | - | Zero activity (201 days) | 0 Fathom + 0 Help Scout + 0 orders | Confirm engagement |
| MALI | 3 | No price levels | 0 price levels configured | Configure pricing |
| MALI | 5 | No customers | 0 customers imported | Import customer data |
| TCD | 5 | No customers | 0 customers imported | Import customer data |
| CST | 2 | Image import failures | "Image imports failing due to 6-image limit and API format mismatch" (Fathom Feb 10) | Create mapping tool |
| CST | 5 | Customer file validation | "Customer file import blocked by validation errors" (Fathom Feb 10) | Provide cleanup script |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| MALI | - | Data mapping questions | "Multiple data mapping questions need resolution" (Help Scout #13861, Feb 10) | Clarify customer/inventory file requirements |
| TCD | - | Delayed engagement | "Overwhelmed catching up on backlog, hopes to have time next week" (Help Scout #13448, Feb 5) | Follow-up to re-engage |
| CST | 7 | UI/UX gaps | "Non-intuitive scanning workflow, incorrect product variant displays" (Fathom Feb 10) | Address UX feedback |
| KRB | - | Near launch | "Ever so close to full launch moment" after CAMS meeting (Help Scout #13963, Feb 10) | Schedule alignment call |
| DCCL | 8 | Onboarding collateral | "Onboarding collateral needs to be created and sent" (Fathom Feb 10) | Send admin guides and customer materials |

### ✅ Confirmed (No Critical Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| DCCL | Stage 8 | 95% | Launch blockers resolved, ready for customer onboarding |

---

## PIPELINE OVERVIEW TABLE

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **PEBL** | eCat | Brent | 2 / 7 | 20% | 0 price levels, 0 customers, 0 engagement | 🔴 2 flags | ~201 |
| **MALI** | eCat | Brent | 2 / 7 | 30% | 0 price levels, 0 customers | ⚠️ 2 flags | ~82 |
| **TCD** | eCat | Brent | 3 / 7 | 35% | 0 customers, client overwhelmed | ⚠️ 2 flags | ~118 |
| **KRB** | eCat | Chuck | 7 / 7 | 75% | Minimal activity, CAMS integration pending | ⚠️ 2 flags | 365+ |
| **CST** | eCat | Brent | 7 / 7 | 85% | Image import failures, customer file errors | 🔴 2 flags / ⚠️ 2 flags | ~62 |
| **DCCL** | eOL | Chuck | 8 / 8 | 95% | None - ready for customer onboarding | ✅ Confirmed | 365+ |

---

## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

PEBL  ████░░░░░░░░░░░░░░░░ 20%  Stage 2 - Catalog Setup        🔴 STALLED

MALI  ██████░░░░░░░░░░░░░░ 30%  Stage 2 - Catalog Setup        ⚠️ ACTIVE ENGAGEMENT

TCD   ███████░░░░░░░░░░░░░ 35%  Stage 3 - Pricing              ⚠️ DELAYED

KRB   ███████████████░░░░░ 75%  Stage 7 - Order Ready          ⚠️ REVIEW (NEAR LAUNCH)

CST   █████████████████░░░ 85%  Stage 7 - Order Ready          ⚠️ ACTIVE ENGAGEMENT (BLOCKERS)

DCCL  ███████████████████░ 95%  Stage 8 - eCat Online Site     ✅ CONFIRMED

═══════════════════════════════════════════════════════════════════

---

## DETAILED CLIENT ASSESSMENTS

### PEBL (Pebl)

**V11 Assessment:** Stage 2 | 20% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟢 | 1,251 products, 244 images, 18 categories |
| 3 | 🔴 | **0 price levels** (Stage 3 criteria: RED BLOCKER - Cannot proceed) |
| 4 | 🟢 | 15 options |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER - Cannot proceed) |
| 6 | 🔴 | **0 inventory/orders** |
| 7 | 🔴 | No orders |

🎯 **V11 Next Action:** 🚫 OUTREACH REQUIRED - Confirm client engagement

🔴 **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | 🔴 STALLED | Database | 201 days since account creation, 0 orders, 0 price levels, 0 customers |
| - | 🔴 STALLED | BigQuery (stale) | No Fathom calls or Help Scout tickets found in last 180 days |

**Validation Summary:** PEBL has zero activity across ALL sources. This is a confirmed disengaged client. Account created July 24, 2025 (201 days ago) with no progress beyond catalog upload.

---

### MALI (Magic Lite)

**V11 Assessment:** Stage 2 | 30% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: onboarding |
| 2 | 🟢 | 906 products, 528 images, 64 categories |
| 3 | 🔴 | **0 price levels** (Stage 3 criteria: RED BLOCKER - Cannot proceed) |
| 4 | ⚫ | N/A - Options not configured |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER - Cannot proceed) |
| 6 | 🔴 | **0 inventory/orders** |
| 7 | 🔴 | No orders |
| 8 | 🟡 | Site enabled but no web portal branding |

🎯 **V11 Next Action:** Configure price levels and import customer data - client is actively engaged

⚠️ **Validation Flags (2) - ACTIVE**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ✅ ACTIVE | Help Scout #13861 (Feb 5-10) | Multi-thread conversation about customer files, inventory files, and product categorization. Jen (Magic Lite) sent customer lists, inventory lists. Kylor requested additional info (sales rep codes, price levels, shipping addresses). Marquel added to help expedite. |
| - | ⚠️ REVIEW | Help Scout #13861 (Feb 10) | Multiple data mapping questions need resolution: "Do all columns need to be filled in? Applications column for filtering? Related Products column format?" |

**Additional Help Scout Context (Feb 5-10):**

- **Feb 5:** Jen sent customer lists (NSL and ML) and inventory lists with multiple Site IDs (ML: Burlington ON, NSL: Tonawanda NY, GA: Atlanta GA)
- **Feb 6:** Kylor requested sales rep/territory codes, price levels per customer, shipping addresses, country codes
- **Feb 10:** Jen glad Jen Z and Endeavour Solutions connected, questions about product file columns

**Validation Summary:** CORRECTED ASSESSMENT - MALI is actively engaged, NOT stalled. Multi-party collaboration (Magic Lite, SuperCat, Endeavour Solutions) working through customer file requirements and inventory mapping. Stage 3 blocker (0 price levels) is accurate, but client is actively progressing. Data source: Manual entry (BigQuery stale as of Feb 5).

---

### TCD (Terracotta Designs)

**V11 Assessment:** Stage 3 | 35% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟡 | 441 products, 638 images, 159 categories - but status "inactive" |
| 3 | 🟢 | 4 price levels (Dealer Net, Designer Price, IMAP, Showroom 50%) |
| 4 | 🟢 | 222 options |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER - Cannot proceed) |
| 6 | 🔴 | **0 inventory/orders** |
| 7 | 🔴 | No orders |

🎯 **V11 Next Action:** Import customer data (Stage 5 blocker) - client apologized for delay, hopes to have time "next week"

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | ⚠️ ACTIVITY | Help Scout #13448 (Feb 5) | Scott Tang (Terracotta): "Apologies for slow progress. Just returned from China last week. Overwhelmed catching up on backlog. Hopes to have dedicated time next week." |
| - | ⚠️ TIMELINE | Help Scout #13448 (Feb 5) | Delayed - hopes to work on it "next week" (vague timeline) |

**Validation Summary:** Stage 5 blocker confirmed. Client overwhelmed with other priorities after returning from China trip. Apologetic tone suggests awareness of delay. May need follow-up to re-engage. Data source: Manual entry (BigQuery stale as of Feb 5).

---

### CST (Coaster Furniture)

**V11 Assessment:** Stage 7 | 85% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists |
| 2 | 🟢 | 7,551 products, 1,338 categories |
| 3 | 🟢 | 31 price levels configured |
| 4 | 🟢 | 2,308 options |
| 5 | 🟡 | 6,294 customers (last updated Jan 21, 2026) - but customer file import blocked by validation errors |
| 6 | 🟢 | 55 users, 8 user groups |
| 7 | 🟡 | 7 orders submitted - but image import failures and UX gaps |
| 8 | 🟡 | Site enabled but no web portal branding |

🎯 **V11 Next Action:** Resolve image import failures (6-image limit, API format mismatch) and customer file validation errors - actively working with weekly standups

🔴 **Validation Flags (2)** / ⚠️ **Review Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | 🔴 BLOCKER | Fathom (Feb 10) | "Image imports failing due to 6-image-per-product limit and API format mismatch (full URLs vs. filenames). Coaster cannot change API format (used by other applications). SuperCat will create mapping tool." |
| 5 | 🔴 BLOCKER | Fathom (Feb 10) | "Customer file import blocked by validation errors (invalid emails, missing international address data). SuperCat will provide cleanup script." |
| 7 | ⚠️ UX | Fathom (Feb 10) | "Non-intuitive scanning workflow and incorrect product variant displays. Reps expect quick scanning with auto-incrementing quantities (like previous AMP app)." |
| - | ⚠️ TIMELINE | Fathom (Feb 10) | "Next standup moved to Thursday, Feb 19, 12 PM PST (9 days out)" |

**Additional Fathom Context (Feb 10):**

**Data Import Issues:**
- **Image Import Failures:** Hard limit of 6 images per product being exceeded; Coaster's API provides full URLs but eCat requires simple filenames; SuperCat creating mapping tool
- **Customer File Import Failures:** Invalid email formats (trailing dots, apostrophes, multiple emails, "NA" placeholders); missing address data for international customers; SuperCat providing cleanup script

**App UI/UX Feedback:**
- **Scanning Workflow:** Non-intuitive; reps must manually tap "barcode" button and enter quantities; workaround is "add to list" feature
- **Product Variant Display:** Inconsistent and confusing (wrong color variants, missing products, thumbnail issues)

**Additional Help Scout Context (Feb 10):**

- Kylor sent detailed recap of customer file cleanup logic (email cleaning, international address handling)
- Steven (Coaster) sent updated customers list same day
- Steven asked if SuperCat records upload/update/change date (useful for identifying stale data)

**Validation Summary:** Stage 7 near completion but blocked by technical issues. Client is actively engaged with weekly standups and immediate follow-up. "Nearing finish line" per Help Scout ticket. Data source: Manual entry (BigQuery stale as of Feb 4-5).

---

### KRB (Kaleen Rugs & Broadloom)

**V11 Assessment:** Stage 7 | 75% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: active |
| 2 | 🟢 | 7,665 products, 35 categories |
| 3 | 🟢 | 19 price levels configured |
| 4 | ⚫ | N/A - Options not configured |
| 5 | 🟡 | 2,208 customers (last updated Sep 9, 2025 - 5 months stale) |
| 6 | 🟢 | 38 users, 5 user groups |
| 7 | 🟡 | 2 orders submitted - minimal activity despite 365+ days active |

🎯 **V11 Next Action:** Schedule alignment call with Cole (Kaleen) - client believes "ever so close to full launch moment" after CAMS meeting

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | ✅ ACTIVE | Help Scout #13963 (Feb 5-10) | Kylor introduced himself as new primary contact. Cole (Kaleen) responded positively: "Nice to meet you. Found email in junk folder. Has meeting with CAMS guys next Monday. Will ask for substantive update on progress. Believes they are 'getting ever so close to the full launch moment.' So excited!" |
| - | ⚠️ MEETING | Help Scout #13963 (Feb 10) | Meeting with CAMS (integration partner?) next Monday for progress update |

**Validation Summary:** Client is engaged and positive about launch. Waiting on CAMS integration completion. Need to schedule alignment call with Cole to chart path forward. Data source: Manual entry (BigQuery stale as of Feb 5).

---

### DCCL (Donald Choi Canada)

**V11 Assessment:** Stage 8 | 95% Ready | Products: eCat Online

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: active |
| 2 | 🟢 | 2,682 products, 283 categories |
| 3 | 🟢 | 3 price levels configured |
| 4 | 🟢 | 2 options |
| 5 | 🟢 | 351 customers (last updated Feb 9, 2026) |
| 6 | 🟢 | 19 users, 4 user groups |
| 7 | 🟢 | 400 orders submitted |
| 8 | 🟢 | Site enabled, web portal configured (b2b.choihome.ca) |

🎯 **V11 Next Action:** Send onboarding collateral (admin guides, customer-facing materials) and schedule follow-up in one week

✅ **No Critical Flags** / ⚠️ **Review Flags (1)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 8 | ⚠️ UNFULFILLED | Fathom (Feb 10) | "Onboarding collateral needed: Internal admin guides and customer-facing materials (PDF or video). Kyla Bosch will send documentation on customer enrollments, general eCat Online overview PDF, and create tailored Loom video." |

**Additional Fathom Context (Feb 10):**

**Launch Readiness:**
- Status: eCat Online is live with daily automated updates
- Remaining Work: Donald Choi resolving inventory sync errors from merging data files
- Testing Plan: Using email aliases (chris+test@domain.com) to simulate different customer user groups

**Customer Onboarding:**
- Goal: Onboard small group of customers for testing, targeting start date of next week
- User Group Strategy: Ordering Admins (full ordering) vs. Sales Associates (pricing-only, no ordering)

**Next Steps:**
- **Kyla Bosch:** Send customer enrollment documentation, eCat Online overview PDF, create Loom video, offer 30-min live training
- **Kylor Johnson:** Follow up in one week
- **Donald Choi:** Resolve inventory sync errors, configure user groups, test permissions

**Validation Summary:** CONFIRMED - Launch blockers resolved, ready for customer onboarding. Client targeting start date of next week. Need to send onboarding collateral promptly. Data source: Manual entry (BigQuery stale as of Feb 4).

---

## SUMMARY & RECOMMENDATIONS

### High Priority Actions

1. **PEBL:** Confirm engagement status - 201 days with no activity
2. **CST:** Resolve image import failures and customer file validation errors - blocking launch
3. **DCCL:** Send onboarding collateral immediately - client ready to launch next week
4. **MALI:** Continue supporting customer/inventory file mapping with Endeavour Solutions
5. **TCD:** Follow-up to re-engage after client returns from China trip

### Medium Priority Actions

1. **KRB:** Schedule alignment call with Cole after CAMS meeting
2. **CST:** Address UI/UX feedback (scanning workflow, product variant display)
3. **MALI:** Clarify product file column requirements and related products format

### Data Quality Notes

- **BigQuery Sync:** Currently 6-7 days stale; Help Scout now syncing every 30 minutes
- **Manual Validation:** Used for CST, DCCL, MALI, TCD, KRB (Feb 5-10, 2026)
- **Product Images:** Query timeouts prevented image counts for CST, KRB, DCCL
- **Mixpanel:** Unable to query iPad activity due to BigQuery staleness

---

**Assessment Completed:** February 11, 2026  
**Next Assessment:** After BigQuery sync is current (check daily)  
**Created By:** Cursor AI Agent (Stage-Gated Onboarding Assessment)
