# February 4th, 2026 - Full Product Suite

## Pipeline Overview

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **PEBL** | eCat iPad | Brent | 2 / 7 | 29% | 0 images, 0 price levels, 0 customers | ✅ Active onboarding | 195 |
| **MALI** | eCat iPad + eOL | Brent | 2 / 9 | 22% | 0 price levels, 0 customers | ✅ Active onboarding | 75 |
| **TCD** | eCat iPad | Brent | 4 / 7 | 57% | 0 customers | ⚠️ Stalled 79 days | 111 |
| **CST** | eCat iPad | Brent | 7 / 7 | 100% | Product search bug, customer data errors | ⚠️ Pre-launch fixes | 55 |
| **KRB** | eCat iPad | Chuck | 7 / 7 | 100% | 0 images, no engagement 99 days | 🔴 Abandoned | 532 |
| **DCCL** | eCat iPad + eOL | Chuck | 10 / 10 | 100% | None - production ready | ✅ Confirmed | 589 |

## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

PEBL  ██████░░░░░░░░░░░░░░ 30%  Stage 2 / 7 (eCat iPad)        ✅ ACTIVE ONBOARDING

MALI  ████░░░░░░░░░░░░░░░░ 20%  Stage 2 / 9 (iPad + eOL)       ✅ ACTIVE ONBOARDING

TCD   ███████████░░░░░░░░░ 55%  Stage 4 / 7 (eCat iPad)        ⚠️ STALLED

CST   ████████████████████ 100% Stage 7 / 7 (eCat iPad)        ⚠️ PRE-LAUNCH FIXES

KRB   ████████████████████ 100% Stage 7 / 7 (eCat iPad)        🔴 ABANDONED

DCCL  ████████████████████ 100% Stage 10 / 10 (iPad + eOL)     ✅ CONFIRMED

═══════════════════════════════════════════════════════════════════

## PEBL (Pebl)

**V11 Assessment:** Stage 2 / 7 | 29% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, 5 admin users |
| 2 | 🟡 | 123 products, 6 categories, 5 collections - but 0 images (0%) |
| 3 | 🔴 | **0 price levels** (Stage 3 blocker) |
| 4 | 🟢 | 15 options configured |
| 5 | 🔴 | **0 customers** (Stage 5 blocker) |
| 6 | ⚫ | N/A - No inventory tracking |
| 7 | 🔴 | No orders, 0 iPad orders, 1 report format, Order email: EMPTY |

🎯 **V11 Next Action:** Follow up on Jan 24 questions - awaiting client response on full product list, images, pricing, and Options structure

✅ **Validation Flags (1) - CORRECTED**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ✅ ACTIVE | Help Scout #13879 (Jan 21-29) | Onboarding ticket: "Assistance with eCAT System – Getting You Up to Speed" - 4 threads, last update Jan 29 (6 days ago) |

**Additional Help Scout Context (Ticket #13879):**

- **Jan 24:** Kylor sent comprehensive onboarding email to Mandy (new contact at PEBL)
- **Product File:** Haven & Wave line imported, product file template created and attached
- **Account Access:** Invite sent to `sales04@peblfurniture.com`, customer confirmed login working (Jan 21)
- **CC'd Contacts:** `vincent@peblfurniture.com`, `sales07@peblfurniture.com`
- **Resources Shared:** 4 Loom videos (Product File Overview, Product File Changes, Options, Price Levels), KB articles
- **Last Import Activity:** September 2025 - paused to align on Options structure
- **Next Steps Defined:** Review import, prepare product images, answer questions about full product list, pricing, and Options vs separate SKUs

**Validation Summary:** CORRECTED ASSESSMENT - PEBL has active onboarding engagement:

- **Jan 21-29:** Active HelpScout ticket with 4 threads (last update 6 days ago)
- **Jan 29:** Last product update (6 days ago)
- **Jan 22:** Referenced in Coaster meeting ("Pebble: A product file template was created")
- **Recent Activity:** 3 imports in last 30 days
- **Current Status:** Waiting on client response to questions about full product list, images, pricing, and Options structure
- Stage 2 blocker (0 images) is accurate, but client is actively engaged in onboarding process

---

## MALI (Magic Lite)

**V11 Assessment:** Stage 2 / 9 | 22% Ready | Products: eCat iPad + eCat Online (Closed Site, no B2B ordering)

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, status: onboarding, 6 admin users |
| 2 | 🟢 | 906 products, 357 with images (39%), 12 categories, 50 collections - Last update: Jan 26 (9 days ago) |
| 3 | 🔴 | **0 price levels** (Stage 3 criteria: RED BLOCKER - Cannot proceed without price level configured) |
| 4 | ⚫ | N/A - 0 options (disabled) |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER - Cannot proceed without customer import) |
| 6 | ⚫ | N/A - No inventory tracking |
| 7 | 🔴 | No orders, 0 iPad orders, 0 report formats, Order email: EMPTY |
| 8 | 🟡 | eCat Online site enabled (catalog only), Authenticated users only (closed site) |
| 9 | 🔴 | Only 6 admin users, 0 non-admin users (Stage 9 blocker for closed site) |
| 10 | ⚫ | N/A - B2B ordering not enabled (catalog-only site) |

🎯 **V11 Next Action:** Import price levels (List Price → Net Price, DN Price → Promotion Price) and customer data - client is actively engaged

⚠️ **Validation Flags (2) - CORRECTED**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ✅ ACTIVE | Fathom Feb 2 | "Onboarding Check-In: Product Hierarchy - Use 4 custom fields (Collection Code, Category Code, Product Type, Subtype) to map Magic Lite's unique product hierarchy" |
| 2 | ✅ ACTIVE | Help Scout Onboarding (Jan 6) | 49 product image file uploads in single session. Files include: "FR-LED-4-S12W-5CCT-PL", "TLE-2X2", "GDL gimbal lights", "LEDD downlights", etc. |

**Additional Help Scout Context (Jan 20):**

- **Onboarding Action Items Ticket:** "MagicLite + SuperCat Onboarding - Next Steps & Action Items"
- **Action Items for Kylor:** Send updated product file with 4 custom hierarchy columns and Related Items column, confirm GP API integration scope with Brent
- **Action Items for Jen (Magic Lite):** Populate updated product file with hierarchy data, spot-check and correct all accessory images

**Validation Summary:** CORRECTED ASSESSMENT - MALI is actively engaged, NOT stalled:

- **Feb 2:** Recent Fathom onboarding check-in call (2 days ago)
- **Jan 20:** Action items ticket with clear next steps
- **Jan 6:** 49 product image files uploaded to onboarding portal
- **Pricing Structure Defined:** List Price → Net Price, DN Price → Promotion Price
- **API Integration Planned:** Client has budget for GP API integration
- Stage 3 blocker (0 price levels) is accurate, but client is actively progressing
- Readiness at 18% due to early stage, but trajectory is positive

---

## KRB (Kaleen Rugs & Broadloom)

**V11 Assessment:** Stage 7 / 7 | 100% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: active, 11 admin users |
| 2 | 🟡 | 1,493 products, 2 categories, 28 collections - but **0 images (0%)** |
| 3 | 🟢 | 21 price levels (CCA, CAN, Luxe, eCommerce tiers) |
| 4 | ⚫ | N/A - 0 options (disabled) |
| 5 | 🟢 | 2,208 customers, 40 users (11 admin, 29 non-admin), 5 user types |
| 6 | 🟢 | 2,509 inventory records |
| 7 | 🟡 | 2 orders in DB, 1 iPad order (Feb 17, 2025), 1 report format - but Order email: EMPTY |

🎯 **V11 Next Action:** 🚫 URGENT - Contact client to determine account status (99 days no contact, no images, stale data)

🔴 **Validation Flags (3)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | 🔴 BLOCKER | Data | 0 product images - never resolved (1,493 products) |
| - | 🔴 ABANDONED | Multiple | 99 days since last contact (Help Scout: Oct 28), 0 imports in 30 days, last iPad order 352 days ago |
| - | ⚠️ DATA STALE | Multiple | Product data 63 days old, customer data 148 days old, inventory 346 days old |

**Validation Summary:** KRB passed Stages 1-7 but shows signs of abandonment:

- **99 days since last contact** (Help Scout: Oct 28, 2025 - "FW: Status Update for Kaleen")
- **All HelpScout tickets closed** (no open issues)
- **Data getting stale:** Inventory 346 days old, customers 148 days old, products 63 days old, 0 imports in 30 days
- **Minimal usage:** Only 1 iPad order in system (Feb 17, 2025 - 352 days ago)
- **Critical blocker never resolved:** 0 product images (1,493 products)
- **Last known status (Oct 28):** Calendar invite scheduled for follow-up meeting (never happened)
- **Stages 1-7 technically passed** but account appears abandoned - requires immediate intervention to determine if active or should be closed

---

## TCD (Terracotta Designs)

**V11 Assessment:** Stage 4 / 7 | 57% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: inactive, 5 admin users |
| 2 | 🟢 | 358 products, 347 with images (97%), 6 categories, 150 collections, Last update: Dec 22 (44 days old) |
| 3 | 🟢 | 4 price levels (Dealer Net, IMAP, Designer Price, Showroom 50%) |
| 4 | 🟢 | 222 options configured |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER - Cannot proceed without customer import), 7 users |
| 6 | 🟡 | 348 inventory records (last update: Dec 19 - 47 days old), 0 imports in 30 days |
| 7 | 🔴 | No orders, 0 iPad orders, 0 report formats, Order email: EMPTY |

🎯 **V11 Next Action:** Import customer data (Stage 5 blocker) - but first confirm client engagement after missed 1/25 deadline

🔴 **Validation Flags (3)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 5 | 🔴 BLOCKER | Data | 0 customers - blocking Stage 5 |
| - | 🔴 STALLED | Help Scout Nov 17 | "I am still in China now. will back home after tomorrow... I will pick it up right after I back home on 1/25" |
| - | ⚠️ TIMELINE | Help Scout Nov 17 | Promised to resume after 1/25/2026 - **deadline passed 10 days ago** with no follow-up |

**Additional Help Scout Context:**

- **Nov 17:** Client (Scott Tang) in China, paused onboarding, promised to resume after 1/25/2026
- **Nov 11:** Onboarding kickoff meeting held, Loom video shared
- **Oct 31:** File upload + questionnaire completed

**Validation Summary:** TCD has strong technical foundation (358 products, 97% with images, pricing configured, 222 options) but is stalled:

- **79 days since last contact** (Nov 17, 2025)
- **Deadline passed:** Client promised to resume after 1/25/2026, now 10 days past with no follow-up
- **Critical blocker:** No customer data (only remaining blocker for Stage 5)
- **Data getting stale:** Product and inventory data 44-47 days old, 0 imports in 30 days
- Requires immediate follow-up to assess if client is ready to proceed

---

## CST (Coaster Furniture)

**V11 Assessment:** Stage 7 / 7 | 100% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, 9 admin users |
| 2 | 🟢 | 2,388 products, 2,036 with images (85%), 45 categories, 823 collections, Last update: Feb 2 (2 days ago) |
| 3 | 🟢 | 31 price levels with descriptive names (zone-based: M1-M10 Z1-Z3, DSFOB, CDN, etc.) |
| 4 | 🟢 | 2,308 options configured |
| 5 | 🟢 | 6,294 customers (updated Jan 21), 58 users (9 admin, 49 non-admin), 8 user types |
| 6 | 🟡 | 4,827 inventory records (last update: Jan 22 - 13 days old), 418 imports in 30 days (highly active) |
| 7 | 🟡 | 7 orders in DB, **3 iPad orders** (1 user, last: Jan 13), 3 report formats, **Order email: EMPTY** |
| 8 | ⚫ | N/A - eCat Online not being implemented |
| 9 | ⚫ | N/A - eCat Online not being implemented |
| 10 | ⚫ | N/A - eCat Online not being implemented |

🎯 **V11 Next Action:** Deploy product search fix and customer data corrections for pre-launch - configure order email recipient

⚠️ **Validation Flags (4) - PRE-LAUNCH FIXES**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ⚠️ BUG | Fathom Feb 3 | "Product Search Broken: Grouping variants breaks direct SKU search" - Solution defined: hidden products |
| 2 | ⚠️ BUG | Fathom Feb 3 | "Data Feed Issues: API missing active SKUs, incorrect field mappings" - Kevin investigating |
| 5 | ⚠️ DATA | Fathom Jan 27 | "Customer Data: Off-by-one address error, ~60 records missing city/zip" - Marlene sending corrected file |
| 7 | ⚠️ CONFIG | Data | Order email recipient not configured (blocking Stage 7 completion) |

**Additional Fathom Context (Feb 3 - Most Recent):**

- **Solution Defined:** All individual variant SKUs will be imported as "hidden products" to enable direct search/scan while preserving clean grouped display
- **Action Items for Brent:** Implement hidden products solution, rename "Show Hidden Products" toggle to "Show All Variants", send Loom video demonstrating scanning
- **Action Items for Kevin:** Correct API field mapping for catalog year, investigate why active SKU 223-521-KW-S4 is missing from API feed

**Additional Fathom Context (Jan 27):**

- **Variant Logic Fixed:** The parent_code API field is now live, enabling proper parent-child product grouping (API fixed during meeting)
- **UI Clutter Reduced:** The item_type: component filter will be removed to hide non-sellable parts
- **Scanning UX Overhauled:** New "scan group" UI will replace current inefficient flow
- **Customer Data:** Marlene will send corrected customer data file

**Additional Help Scout Context (Jan 27):**

- **Ticket #13910:** Kevin adding RelatedGroup to API (pending)
- **Multiple Onboarding Questionnaires:** 6+ questionnaire completion notifications (Jan 16-22)
- **Ticket #13863:** Action items and territory code updates (22 threads)

**Validation Summary:** CST is in active pre-launch phase with bugs being resolved:

- **Highly Active:** 5 Fathom meetings in last 14 days (Feb 3, Jan 27 x2, Jan 23, Jan 22)
- **10 HelpScout tickets** (9 open) showing active support
- **Pre-Launch Blockers Being Resolved:** Product search fix, customer data corrections, API fixes
- **Solutions Defined:** Hidden products for variants, scan group UI, customer CSV import
- **API Fixes Deployed:** parent_code field fixed during Jan 27 meeting
- **Strong Foundation:** 2,388 products (85% with images), 31 price levels, 6,294 customers
- **Market Deadline:** Target launch appears to be late January 2026 (market show)
- **Status:** Database shows "inactive" but account is actually **highly active** pre-launch

---

## DCCL (Donald Choi Canada)

**V11 Assessment:** Stage 10 / 10 | 100% Ready | Products: eCat iPad + eCat Online with B2B Ordering

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, 10 admin users |
| 2 | 🟢 | 334 products, 302 with images (90%), 12 categories, 3 collections, Last update: Feb 4 (TODAY) |
| 3 | 🟢 | 4 price levels (Designer Price, Warehouse Price, warehouse2, wh2) |
| 4 | 🟡 | Only 2 options configured |
| 5 | 🟢 | 350 customers (updated Feb 2), 22 users (10 admin, 12 non-admin), 7 user types |
| 6 | 🟢 | 334 inventory records (last update: Feb 2 - 2 days old), 54 imports in 30 days |
| 7 | 🟢 | 400 orders in DB, **336 iPad orders** (7 users, last: Feb 2 - 2 days ago), 5 report formats, Order email: customerservice@donaldchoi.com |
| 8 | 🟢 | eCat Online site enabled (catalog + ordering), Authenticated + unauthenticated users |
| 9 | 🟢 | 7 user types (CDN Reps EN/FR, Managers, eOL Public Site, stores), 12 non-admin users |
| 10 | 🟢 | Order email configured, PDF attachment enabled |
| 11 | ⚫ | N/A - Sales Portal not being implemented |

🎯 **V11 Next Action:** Monitor cache issue resolution (Jira tickets) - maintain production environment

✅ **No Validation Flags**

- **Fathom:** No calls in last 14 days (mature production client - self-sufficient operation is normal)
- **Help Scout:** 7 tickets in last 180 days, 5 open (minor configuration questions and cache issues being tracked)

**Additional Help Scout Context:**

- **Jan 19:** Image upload request completed successfully - "Thank you for the image upload last night. The files went in and look great on our site"
- **Jan 13:** eCat Online setting questions (closed)
- **Jan 8:** Server cache issues with trade names and collections (3 tickets - pending, logged on Jira for engineering)
- **Public Site:** Client operates public catalog at https://b2b.choihome.ca/

**Validation Summary:** DCCL is fully operational and self-sufficient:

- **Active iPad Usage:** 336 orders, 7 active users, last order 2 days ago
- **Fresh Data:** All metrics updated within 2-4 days (products: today, customers: 2 days, inventory: 2 days)
- **Self-Service:** Client handling own image uploads and configurations
- **Minimal Support Needs:** Recent tickets are minor configuration questions
- **Technical Issues Being Tracked:** Cache issues identified and logged for engineering resolution
- **Production Ready:** 100% readiness, Stage 10 of 10 complete (Sales Portal N/A)

---

## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| KRB | 2 | No product images | 0 out of 1,493 products | Urgent intervention |
| KRB | - | Account abandoned | 99 days no contact, last order 352 days ago | Confirm active or close |
| TCD | 5 | No customers | 0 customers imported (Stage 5 blocker) | Import customer data |
| TCD | - | Deadline passed | Promised 1/25, now 10 days late | Follow up immediately |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| PEBL | 2 | Awaiting client response | Ticket #13879 (Jan 24 questions) | Follow up on product list, images, pricing |
| MALI | 3 | Pricing import pending | List Price → Net Price, DN Price → Promotion | Import price levels |
| CST | 2 | Product search bug | Variant grouping breaks search | Deploy hidden products fix |
| CST | 5 | Customer data errors | Off-by-one address error, ~60 records | Import corrected file |
| CST | 7 | Order email missing | Not configured | Configure email recipient |
| DCCL | 8 | Cache issues | Server cache on taxonomy | Monitor Jira resolution |
| KRB | - | Data stale | 63-346 days old across all metrics | Refresh if account active |

### ✅ Confirmed Active (Positive Engagement)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| DCCL | Stage 10 / 10 | 100% | Production live - 336 iPad orders, 7 active users, self-sufficient |
| CST | Stage 7 / 7 | 100% | Active pre-launch - 5 meetings in 14 days, bugs being resolved |
| PEBL | Stage 2 / 7 | 29% | Active onboarding - HelpScout ticket #13879 (Jan 21-29), awaiting client response |
| MALI | Stage 2 / 9 | 22% | Active onboarding - Recent Fathom call (Feb 2), 49 file uploads (Jan 6) |
