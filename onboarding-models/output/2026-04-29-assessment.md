# April 29th, 2026 - Full Product Suite

## Pipeline Overview

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **TCS** | eCat + eOL | Kylor | 1 / 10 | 10% | No data imported (9 days old, kickoff complete) | ✅ Confirmed | ~9 |
| **KRB** | eCat | Kylor | 4 / 7 | 40% | 0 product images, stale product/inventory data | ⚠️ 2 flags | 617+ |
| **DRF** | eCat | Kylor | 5 / 7 | 45% | 0 inventory, 1 price level, 1 user type | ✅ Confirmed | ~14 |
| **PEBL** | eCat | Kylor | 4 / 7 | 50% | 0 customers, 0 inventory, 0 non-admin users | ⚠️ 2 flags | ~280 |
| **HVUSA** | eCat | Kyla | 5 / 7 | 60% | Stale customer/inventory data (2022), 0 iPad orders, no order email | ⚠️ 2 flags | 2059+ (migration) |
| **MALI** | eCat + eOL | Kylor | 7 / 10 | 70% | No iPad reports, eCat Online needs branding, stale inventory | ✅ Confirmed | ~160 |
| **TCD** | eCat | Kylor/Kyla | 6 / 7 | 85% | 0 iPad orders, 1 report format, 0 territories | ✅ Confirmed | ~196 |

## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

TCS   ██░░░░░░░░░░░░░░░░░░ 10%  Stage 1 - Account Foundation    ✅ CONFIRMED

KRB   ████████░░░░░░░░░░░░ 40%  Stage 2 - Catalog Setup         ⚠️ FLAGGED

DRF   █████████░░░░░░░░░░░ 45%  Stage 6 - Operations            ✅ CONFIRMED

PEBL  ██████████░░░░░░░░░░ 50%  Stage 5 - Customer Setup        ⚠️ ACTIVE ENGAGEMENT

HVUSA ████████████░░░░░░░░ 60%  Stage 7 - Order Ready           ⚠️ FLAGGED

MALI  ██████████████░░░░░░ 70%  Stage 8 - eCat Online Site      ✅ CONFIRMED

TCD   █████████████████░░░ 85%  Stage 7 - Order Ready           ✅ CONFIRMED

═══════════════════════════════════════════════════════════════════

## TCS (The Coppersmith)

**V11 Assessment:** Stage 1 | 10% Ready | Products: eCat iPad + eCat Online

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, 1 admin user |
| 2 | 🔴 | **0 products** (Stage 2 criteria: RED BLOCKER - No products imported yet) |
| 3 | 🔴 | **0 price levels** (Stage 3 criteria: RED BLOCKER) |
| 4 | ⚫ | N/A - Options TBD pending data import |
| 5 | 🔴 | **0 customers, 1 user** (Stage 5 criteria: RED BLOCKER) |
| 6 | 🔴 | **0 inventory** |
| 7 | 🔴 | No iPad configuration |
| 8 | 🔴 | No mobile site configured |
| 9 | 🔴 | No user access configured |
| 10 | ⚫ | N/A - B2B ordering TBD |

🎯 **V11 Next Action:** Import initial product file from CATC PIM - customer to provide updated product/media data with live CATC URLs by end of April

✅ **No Validation Flags**

- **Fathom:** Kickoff meeting Apr 21 - strong engagement, clear timeline, go-live target June 1
- **Help Scout:** Kickoff recap sent Apr 21 (Ticket #14351) - admin invites, FTP credentials, data templates all dispatched

**Validation Summary:** TCS kicked off April 21 with strong team engagement (5 client stakeholders identified). Go-live target is June 1, 2026 ahead of Lightovation market June 24. Account is 9 days old — zero data is expected and on-track. CATC PIM integration and Odoo ERP planned. Bi-weekly working sessions starting May 15.

---

## KRB (Kaleen Rugs & Broadloom)

**V11 Assessment:** Stage 2 | 40% Ready | Products: eCat iPad

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, 6 admin users |
| 2 | 🔴 | **1,493 products but 0 images** (Stage 2 criteria: RED BLOCKER - Products exist but no images matched. 1,500-1,600 images uploaded via FTP Apr 22 but not yet linked in product file) |
| 3 | 🟢 | 19 price levels (CCA, CAN 8%, CAN 10%, Luxe 5-15%, eCommerce 8-10%, 2011 Price List, 5%/8%/10%/12%/15% MGMT) |
| 4 | ⚫ | N/A - 0 options configured |
| 5 | 🟢 | 2,208 customers, 34 users (6 admin, 28 non-admin), 5 user types |
| 6 | 🔴 | **2,509 inventory records but last update Feb 2025** (Stage 6 criteria: Inventory stale >14 months). 104 import errors in history. |
| 7 | 🟡 | 5 user types ✅, 1 iPad order (Feb 2025) ✅, 1 report format (need ≥3) ❌, 2 orders ✅, no order email ❌ |

🎯 **V11 Next Action:** Update product file to include image filenames matching FTP uploads, then refresh inventory/product data from CAMS ERP

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ⚠️ REVIEW | Help Scout Apr 27 (#14359) | "uploaded about 15-1600 images in the last day and they aren't showing" - images uploaded to FTP but need product file update to link them |
| 6 | ⚠️ TIMELINE | Help Scout Mar 31 (#13963) | CAMS ERP team "working on merging information" and "hoped to show everything" - data automation dependency on third-party ERP vendor |

**Additional Help Scout Context (Apr 2026):**

- Apr 27: Kylor responded with guidance on linking images in product file via naming convention
- Apr 23: Met at HPMKT (High Point Market) - Kaleen team was present
- Apr 14: FTP credentials sent for image uploads
- Mar 31: Cole confirmed CAMS meeting went well, data integration "last big hurdle"

**Validation Summary:** KRB has strong data foundations (1,493 products, 2,208 customers, 19 price levels, 5 user types) but the critical blocker is 0 product images showing in the app. 1,500+ images were uploaded Apr 22 but need the product file updated with correct image filenames. Inventory data is 14 months stale pending CAMS ERP automation. Active engagement — Cole Lewis responsive, met at HPMKT.

---

## DRF (Dorell Fabrics)

**V11 Assessment:** Stage 5 | 45% Ready | Products: eCat iPad

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active (Loomcraft Textiles DBA Dorell Fabrics), 2 admin users |
| 2 | 🟡 | 80 products, 79 images, 2 categories, 8 collections - intentionally a subset (only patterns with photos imported); more patterns available in original file |
| 3 | 🟡 | 1 price level (Net) - only single price level configured |
| 4 | ⚫ | N/A - 0 options |
| 5 | 🟡 | 389 customers imported, 2 users (both admin), 1 user type (DefaultUserGroup) - territory codes configured (9 territories via customer file) |
| 6 | 🔴 | **0 inventory records**, customer import had errors ("Default price code 'net' must be a valid price level code" on some rows) |
| 7 | 🔴 | 1 user type ❌, 3 report formats ✅, 0 orders ❌, no order email ❌ |

🎯 **V11 Next Action:** Admin training session Wednesday Apr 30 - review iPad, expand product catalog with additional patterns, configure additional user types for reps. Target: Showtime market end of May.

✅ **No Validation Flags**

- **Fathom:** 2 calls in last 16 days - "Data Files" (Apr 15) and "Dorell path forward alignment" (Apr 13, with Kylor)
- **Help Scout:** Ticket #14401 (Apr 27) - "Initial Product & Customer Imports Complete" - active correspondence, meeting Wednesday

**Validation Summary:** DRF is a brand-new account (14 days old) progressing rapidly. Phase 1 deployment targeting Showtime market end of May. 80 products imported (subset with photos), 389 customers loaded, territory codes configured. Admin training scheduled for Wednesday. Engagement is strong — Suzanne (merch lead) and Christine (IT) are responsive. Key risk: tight timeline to end-of-May market.

---

## PEBL (Pebl Furniture)

**V11 Assessment:** Stage 5 | 50% Ready | Products: eCat iPad

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, 3 admin users |
| 2 | 🟡 | 44 products, 32 images, 6 categories, 2 collections - product file updated Apr 28. Haven & Wave collections imported as starting point. |
| 3 | 🟢 | 2 price levels (Normal, Project) |
| 4 | 🟢 | 19 options configured |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER), 3 users (all admin, 0 non-admin), 1 user type |
| 6 | 🔴 | **0 inventory records**, 12 import errors in history |
| 7 | 🔴 | 0 orders, 1 report format, 0 iPad activity, no order email |

🎯 **V11 Next Action:** Import customer file (Stage 5 blocker) - client is actively engaged on product/image setup, customer import is next milestone

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ⚠️ REVIEW | Help Scout Apr 28 (#13879) | Client asking about product-specific color combinations: "Only list the available colors for each product" and "only need to choose frame color, then cushion fabric comes out automatically" - complex options/variant logic requested |
| 5 | ⚠️ ACTIVITY | Help Scout Apr 28 (#13879) | Active engagement but 0 customers imported after 280 days. Client based in China (Foshan), potential timezone/pace factor. |

**Additional Help Scout Context (Apr 2026):**

- Apr 28: Mandy (client) sent detailed follow-up on product options logic, confirming images now displaying after VPN fix
- Apr 27: Kylor sent iPad screenshots, troubleshooting guidance for catalog sync
- Apr 22: Client reported images still not displaying, VPN confirmed as the issue
- Apr 9-10: Image prep completed (134 photos), filename corrections applied, FTP instructions sent
- Continuous engagement since Jan 21 across 20+ thread entries

**Validation Summary:** PEBL is actively engaged with frequent Help Scout correspondence (latest Apr 28). Client Mandy Mai is hands-on but learning — working through product file structure, image uploads (now resolved via VPN), and complex options configuration. The 0 customers after 280 days is a concern, but the pace reflects a self-service Chinese client with timezone challenges. Product catalog is small (44 items) but growing as they learn the system.

---

## HVUSA (Hudson Valley Group - USA)

**V11 Assessment:** Stage 5 | 60% Ready | Products: eCat iPad

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active (legacy account since 2020), 3 admin users + 1 non-admin |
| 2 | 🟢 | 4,942 products, 2,896 images, 16 categories, 1,578 collections - product data updated Apr 24 |
| 3 | 🟢 | 5 price levels (IMAP, Wholesale +12%, DN, Confidential Net +25%, Designer Net +50%) |
| 4 | ⚫ | N/A - 0 options |
| 5 | 🟡 | 14,224 customers but **last customer update Aug 2022** (4+ years stale), 4 users, 2 user types (Admins, Reps) |
| 6 | 🟡 | 4,999 inventory records but **last update Aug 2022** (4+ years stale). Product data recently refreshed (Apr 24). |
| 7 | 🔴 | **0 iPad orders, 0 orders in system**, 5 report formats ✅, 2 user types ✅, no order email ❌ |

🎯 **V11 Next Action:** Refresh customer and inventory data from new consolidated HVLG source - last check-in Mar 30 went unanswered

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | ⚠️ ACTIVITY | Help Scout Mar 30 (#14223) | Last outreach from Kylor "wanted to touch base quickly and see how things are going on your end re the new org migration" - no response from Chris K. as of Apr 29 |
| 6 | ⚠️ REVIEW | Help Scout Feb 11-13 (#13991) | HVLG eCat Consolidation project - Chris uploaded product/stories files to new HVUSA org, SFTP configured. Kyla assigned as new POC. Migration in progress but stalled since March. |

**Validation Summary:** HVUSA is a legacy mature account (5+ years) undergoing a consolidation/migration project. Chris K. from Hudson Valley Group uploaded product/stories files and began SFTP image work in Feb 2026. Product data was refreshed Apr 24, but customer and inventory data remain from 2022. Last check-in Mar 30 went unanswered — 30 days of silence is a concern. This is not a standard onboarding but a re-platform/consolidation effort.

---

## MALI (Magic Lite)

**V11 Assessment:** Stage 7 | 70% Ready | Products: eCat iPad + eCat Online

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, 2 admin users + 3 non-admin |
| 2 | 🟢 | 694 products, 691 images, 22 categories, 5 collections - updated Apr 28 |
| 3 | 🟢 | 5 price levels (ML DN, ML List, Net Price, NSL DN, NSL List) |
| 4 | 🟡 | 2 options configured (minimal) |
| 5 | 🟢 | 3,417 customers (NSL + ML merged), 5 users, 3 user types (DefaultUserGroup, ML Reps, NSL Reps) - customer import completed Apr 28 with no errors |
| 6 | 🟡 | 694 inventory records, last update Mar 26 (34 days ago - stale >7 days) |
| 7 | 🔴 | **0 iPad reports configured, 0 orders, 0 iPad activity, no order email** |
| 8 | 🟡 | eCat Online enabled (2 sites) but **no branding** - no custom cname, no title, no logo uploaded |
| 9 | 🟢 | 3 non-admin users, 3 user types including ML Reps and NSL Reps |
| 10 | ⚫ | N/A - B2B ordering not yet configured (no order email) |

🎯 **V11 Next Action:** Meeting tomorrow (Apr 30) to review eCat Online, configure branding/ordering, and plan iPad report templates and rep training

✅ **No Validation Flags**

- **Fathom:** No calls in last 30 days (all engagement via Help Scout onboarding thread)
- **Help Scout:** Extremely active - Ticket #14329 with 10+ threads in last 14 days

**Additional Help Scout Context (Apr 28-29):**

- Apr 29: Kylor sent progress update: "Customer file imported - all 3,418 customers live with correct price codes. eCat Online is live. User groups created."
- Apr 28: Magic Lite COO Jen Penton added 10 internal staff to eCat access (Craig, Jason, Jen, Marquel, Michelle, Pansy, Patricia, Tom, Priya)
- Apr 28: Kylor confirmed "making updates and doing the final import so we can review the final product tomorrow"
- Apr 27: Rep user files with emails and clarifications exchanged

**Validation Summary:** MALI is in the final stretch of onboarding with exceptional momentum. eCat Online went live, 3,417 customers imported error-free, user groups configured for both Magic Lite and NSL brands. Meeting scheduled for tomorrow (Apr 30) to review eCat Online branding, ordering settings, and iPad report configuration. Client engagement is outstanding — COO directly involved, 10 internal staff being onboarded.

---

## TCD (Terracotta Designs)

**V11 Assessment:** Stage 7 | 85% Ready | Products: eCat iPad

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, 2 admin + 15 non-admin users |
| 2 | 🟢 | 380 products, 378 images, 6 categories, 172 collections - updated today (Apr 29) |
| 3 | 🟢 | 4 price levels (Dealer Net, IMAP, Designer Price, Showroom 50%) |
| 4 | 🟢 | 222 options configured |
| 5 | 🟢 | 346 customers, 17 users, 2 user types (DefaultUserGroup, Sales Reps) |
| 6 | 🟢 | 397 inventory records, last update Apr 22 (7 days ago - within threshold) |
| 7 | 🟡 | 2 user types ✅, order email configured (sales@terracottalighting.com) ✅, send_order_email_on_submit ✅, but **0 iPad orders, 1 report format (need ≥3), 0 territories** |

🎯 **V11 Next Action:** Admin training with Scott Tang (new POC) — configure additional report formats, set up territories, begin rep iPad training

✅ **No Validation Flags**

- **Fathom:** No calls in last 30 days (onboarding completed via Help Scout/email)
- **Help Scout:** Onboarding declared complete Apr 28 - transitioned from Kylor to Kyla

**Additional Help Scout Context (Apr 27-28):**

- Apr 28: Kyla sent "Welcome to SuperCat Support" to Scott Tang: "Your onboarding is now complete. Your product catalog (with images), pricing, options, customers, and inventory have all been imported and are live. Reps have been invited, and your user groups and territory codes are configured."
- Apr 28: Scott submitted "Data Update - status" ticket about lifestyle images not appearing after FTP upload
- Apr 27: Image format guidance (JPG-only requirement) sent to Scott
- Apr 27: Admin training and go-live next steps communicated

**Validation Summary:** TCD onboarding has been officially declared complete and transitioned from Kylor (onboarding) to Kyla (support). All core data is imported and live — 380 products with images, 4 price levels, 222 options, 346 customers, 397 inventory records. Scott Tang is the active client contact. Minor gaps remain: 0 iPad orders (reps just invited), only 1 report format, and 0 territories configured. Client is actively engaged — submitted a support ticket about lifestyle images within hours of handoff.

---

## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| - | - | - | No critical flags identified | - |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| KRB | 2 | Image linking | "uploaded 15-1600 images but aren't showing" - need product file update | Guide image filename convention |
| KRB | 6 | CAMS ERP dependency | Data automation dependent on third-party ERP vendor (Chadwick/CAMS) | Monitor CAMS progress |
| PEBL | 2 | Complex options logic | Client requesting product-specific color combinations with auto-selection | Clarify options/variant approach |
| PEBL | 5 | 0 customers after 280 days | Active but slow - China-based client, timezone/self-service pace | Push customer import as next step |
| HVUSA | - | Migration stalled 30+ days | Last check-in Mar 30 went unanswered, consolidation project | Follow up with Chris K. |
| HVUSA | 6 | Stale data (2022) | Customer and inventory data 4+ years old, product data refreshed Apr 24 | Confirm data refresh timeline |

### ✅ Confirmed (No Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| TCS | Stage 1 | 10% | ACTIVE - Kickoff Apr 21, go-live June 1, Lightovation June 24 |
| DRF | Stage 5 | 45% | ACTIVE - 14 days old, meeting Wednesday, Showtime market end of May |
| MALI | Stage 7 | 70% | ACTIVE - eCat Online live, 3,417 customers imported, meeting tomorrow |
| TCD | Stage 7 | 85% | COMPLETE - Onboarding declared complete, transitioned to support |
