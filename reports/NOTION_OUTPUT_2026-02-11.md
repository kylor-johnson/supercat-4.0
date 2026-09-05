# February 11th, 2026 - Full Product Suite

## Pipeline Overview

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **PEBL** | eCat | Brent | 2 / 7 | 20% | 0 price levels, 0 customers, 0 engagement | 🔴 2 flags | ~201 |
| **MALI** | eCat | Brent | 2 / 7 | 30% | 0 price levels, 0 customers | ⚠️ 2 flags | ~82 |
| **TCD** | eCat | Brent | 3 / 7 | 35% | 0 customers, client overwhelmed | ⚠️ 2 flags | ~118 |
| **KRB** | eCat | Chuck | 7 / 7 | 75% | Minimal activity, CAMS integration pending | ⚠️ 2 flags | 365+ |
| **CST** | eCat | Brent | 7 / 7 | 85% | Image import failures, customer file errors | 🔴 2 flags | ~62 |
| **DCCL** | eOL | Chuck | 8 / 8 | 95% | None - ready for customer onboarding | ✅ Confirmed | 365+ |

## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

PEBL  ████░░░░░░░░░░░░░░░░ 20%  Stage 2 - Catalog Setup        🔴 STALLED

MALI  ██████░░░░░░░░░░░░░░ 30%  Stage 2 - Catalog Setup        ⚠️ ACTIVE ENGAGEMENT

TCD   ███████░░░░░░░░░░░░░ 35%  Stage 3 - Pricing              ⚠️ DELAYED

KRB   ███████████████░░░░░ 75%  Stage 7 - Order Ready          ⚠️ REVIEW

CST   █████████████████░░░ 85%  Stage 7 - Order Ready          ⚠️ ACTIVE ENGAGEMENT

DCCL  ███████████████████░ 95%  Stage 8 - eCat Online Site     ✅ CONFIRMED

═══════════════════════════════════════════════════════════════════

## PEBL (Pebl)

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

🎯 **V11 Next Action:** 🚫 OUTREACH REQUIRED - Confirm client engagement (201 days since account creation, no activity)

🔴 **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | 🔴 STALLED | Database | 201 days since account creation, 0 orders, 0 price levels, 0 customers |
| - | 🔴 STALLED | BigQuery (stale) | No Fathom calls or Help Scout tickets found in last 180 days |

**Validation Summary:** PEBL has zero activity across ALL sources. This is a confirmed disengaged client. Account created July 24, 2025 (201 days ago) with no progress beyond catalog upload.

---

## MALI (Magic Lite)

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

## TCD (Terracotta Designs)

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
| - | ⚠️ ACTIVITY | Help Scout #13448 (Feb 5) | "Apologies for slow progress. Just returned from China last week. Overwhelmed catching up on backlog. Hopes to have dedicated time next week." |
| - | ⚠️ TIMELINE | Help Scout #13448 (Feb 5) | Delayed - hopes to work on it "next week" (vague timeline) |

**Validation Summary:** Stage 5 blocker confirmed. Client overwhelmed with other priorities after returning from China trip. Apologetic tone suggests awareness of delay. May need follow-up to re-engage. Data source: Manual entry (BigQuery stale as of Feb 5).

---

## KRB (Kaleen Rugs & Broadloom)

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

## CST (Coaster Furniture)

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

## DCCL (Donald Choi Canada)

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

## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| PEBL | - | Zero activity (201 days) | 0 Fathom + 0 Help Scout + 0 orders | Confirm engagement |
| MALI | 3 | No price levels | 0 price levels configured | Configure pricing |
| MALI | 5 | No customers | 0 customers imported | Import customer data |
| TCD | 5 | No customers | 0 customers imported | Import customer data |
| CST | 2 | Image import failures | "6-image limit and API format mismatch" | Create mapping tool |
| CST | 5 | Customer file validation | "Invalid emails, missing international data" | Provide cleanup script |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| MALI | - | Data mapping questions | "Multiple data mapping questions need resolution" | Clarify requirements |
| TCD | - | Delayed engagement | "Overwhelmed, hopes to have time next week" | Follow-up to re-engage |
| CST | 7 | UI/UX gaps | "Non-intuitive scanning, incorrect variants" | Address UX feedback |
| KRB | - | Near launch | "Ever so close to full launch moment" | Schedule alignment call |
| DCCL | 8 | Onboarding collateral | "Admin guides and customer materials needed" | Send collateral |

### ✅ Confirmed (No Critical Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| DCCL | Stage 8 | 95% | Launch blockers resolved, ready for customer onboarding |
