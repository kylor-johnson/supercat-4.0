# June 3rd, 2026 - Full Product Suite

## Pipeline Overview

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **TCS** | eCat | Kylor | 2 / 7 | 30% | 0 price levels, Catsy/PIM dependency stalling data export | ⚠️ 2 flags | ~44 |
| **PEBL** | eCat | Kylor | 4 / 7 | 55% | 0 customers, 0 inventory | ⚠️ 2 flags | 314 |
| **LIBCO** | eCat | Kylor | 4 / 7 | 60% | 0 customers, 0 DB orders (5 MixPanel events), 13 days to Lightovation market | 🔴 2 flags | ~72 |
| **DRF** | eCat | Kylor | 5 / 7 | 65% | Import error (Jun 2, invalid image type), 0 inventory, 1 price level | ⚠️ 2 flags | ~49 |

## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

TCS   ██████░░░░░░░░░░░░░░ 30%  Stage 3 - Pricing              ⚠️ ACTIVE ENGAGEMENT

PEBL  ███████████░░░░░░░░░ 55%  Stage 5 - Customer Setup       ⚠️ ACTIVE ENGAGEMENT

LIBCO ████████████░░░░░░░░ 60%  Stage 5 - Customer Setup       🔴 FLAGGED

DRF   █████████████░░░░░░░ 65%  Stage 6 - Operations           ⚠️ FLAGGED

═══════════════════════════════════════════════════════════════════

---

## TCS (The Coppersmith)

**V11 Assessment:** Stage 2 | 30% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | 4 admin users, company active (Apr 20, 2026) |
| 2 | 🟢 | 283 products, 253 with images (89%), 48 collections — last update May 5 |
| 3 | 🔴 | **0 price levels** (Stage 3 criteria: RED BLOCKER — Cannot proceed without pricing configured) |
| 4 | 🟢 | 390 options (out of sequence — Stage 3 blocks progression) |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER — Cannot proceed) |
| 6 | 🔴 | **0 inventory**, no imports since May 5 (29 days) |
| 7 | 🔴 | 0 orders, 0 report formats, 0 iPad activity |

🎯 **V11 Next Action:** Configure price levels (Stage 3 blocker) — awaiting Catsy working session to finalize accessory attribute groups before clean data export is possible; align on master sheet as source of truth per TCS Jun 2 clarification

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 3 | ⚠️ CATSY DEPENDENCY | Help Scout May 28 | "We are currently waiting on our next Catsy working session to update the accessory attribute groups so they align with our newly updated master sheet and to finalize a few remaining data organization details." |
| 3 | ⚠️ APPROACH CONFLICT | Help Scout Jun 2 | "The SKU Builder is a working prototype we created to help explain CopperSmith's SKU logic...It is intended as a reference point...but the master sheet is the source of truth and the builder is a reference." |

**Additional Help Scout Context (Jun 2):**

- TCS client followed up "Any updates with this?" Jun 2 — client is pushing for progress, ticket #14520 status: pending
- Kylor had built a first-pass iPad catalog (283 products, full finish/mount/decorative option model) using the SKU Builder as source of truth — TCS pushed back that this created potential duplicate structures vs. their PIM
- Next step: Kylor acknowledged the master sheet + URL approach and committed to importing examples for TCS to visualize

**Validation Summary:** TCS is actively engaged — dense HelpScout thread as of Jun 2, client following up proactively. However, the account is structurally blocked by two converging issues: (1) Catsy PIM must be updated before a clean product/option export is possible, and (2) TCS and the CSM need to align on the master sheet as primary source vs. the SKU Builder. Catalog work is impressive (283 products, 89% image coverage, 390 options) but the Catsy → eCat pipeline has not opened. No imports in 29 days.

---

## PEBL (Skyard Furniture Co Ltd.)

**V11 Assessment:** Stage 4 | 55% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | 3 admin users, company active (Jul 24, 2025 — 314 days) |
| 2 | 🟢 | 299 products (+255 since last assess), 188 with images (63%), 11 categories, 28 collections — actively importing TODAY Jun 3 |
| 3 | 🟢 | 2 price levels (Normal/FOB, Project) |
| 4 | 🟢 | 103 options (+19 since last assess) |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER — Cannot proceed without customer import) |
| 6 | 🔴 | **0 inventory** |
| 7 | 🔴 | 2 DB orders, 2 MixPanel orders (last May 29), 1 report format — pre-stage 7 requirements not met |

🎯 **V11 Next Action:** Import customer file (Stage 5 gate) + provide inventory file — client is in active catalog-build sprint; customers and inventory are the next structural unlocks

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ⚠️ DATA GAP | Import Jun 3 | Warnings across all product imports: custom fields Certification, Color, PackingSize, Materials1, FrameColor missing — client sending updated CSVs but metadata template not yet aligned |
| 2 | ✅ ACTIVE | Help Scout Jun 3 + Import Jun 3 | Mandy Mai (sales04@peblfurniture.com) sent updated products.csv today — "today we upload more collections / I will update the file of option mapping asap"; Kylor completed Frame Color → cushion/material option configuration May 28 |

**Validation Summary:** PEBL has made dramatic progress since the last assessment — 44 → 299 products (6× growth), 2 → 28 collections, 84 → 103 options, Stage 2 upgraded from 🟡 to 🟢. Client is actively importing this morning (194 total import events). The remaining blockers are 0 customers and 0 inventory — structural next steps rather than data quality issues. Custom field warnings should be resolved by aligning the products.csv template with eCat's custom field configuration.

---

## LIBCO (Lib and Co.)

**V11 Assessment:** Stage 4 | 60% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | 3 users (2 admin, 1 non-admin rep), 3 user type groups (DefaultUserGroup, Lib & Co — US Reps, Lib & Co — Canadian Reps) |
| 2 | 🟢 | 907 products, 802 with images (88%), 5 categories, 62 collections — last update Jun 2 |
| 3 | 🟢 | 4 price levels (CAD_WSP, CAD_IMAP, USA_IMAP, USA_WSP) — dual-currency, WSP + IMAP tiers for US and Canadian reps |
| 4 | ⚫ | N/A — lighting fixtures; per-SKU catalog approach, no configurable options required |
| 5 | 🔴 | **0 customers** (showroom structure defined May 28 — each showroom = distinct account with territory codes — but not yet imported) |
| 6 | 🟢 | 910 inventory records, last update Jun 2 — FRESH (only client in cohort with Stage 6 green) |
| 7 | 🔴 | 0 DB orders (5 MixPanel order events — last May 22 — order pipeline not writing to DB), 1 report format (<3 required), order email empty |

🎯 **V11 Next Action:** 🚨 URGENT — Import customer file using showroom-as-account structure + territory codes (confirmed May 28); investigate order pipeline (5 MixPanel events vs 0 DB orders); complete BC integration call with Brent Jun 4 — 13 business days remain to Lightovation market (~Jun 22-23)

🔴 **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | 🔴 TIMELINE | Fathom May 20 (60 min) | "Hard deadline: Be live by June market (Dallas/Lightovation). Silvio leaves June 19 for California; wants daily/near-daily working sessions to hit the date. Reps expecting SuperCat; market is the launch." — 13 days remain, rep training targeted Jun 16 |
| 7 | 🔴 ORDER PIPELINE | BigQuery May 22 | 5 MixPanel `order_submitted` events vs 0 records in DB `orders` table — orders not persisting; need to determine if test mode or live pipeline issue |

**Additional Help Scout Context (May 28 – Jun 2):**

- Ticket #14554: "Lib & Co — got the files cleaned up + imported, few asks before tomorrow" — data imported, Kylor building structure off call notes
- Business Central (Dynamics 365) integration scoped for Jun 4 call with CTO Brent: order/quote pushback to BC, live inventory + sales data pipelines, BC product-type filters controlling what flows into eCat
- "Discontinued" smart list planned: in-stock discontinued items surfaced to reps at 25% promo price
- Unmatched inventory SKU (10193-02) flagged for review — missing from product file

**Validation Summary:** LIBCO is the highest-urgency account in the cohort with a hard Lightovation market deadline (~Jun 22-23) and only ~13 business days to go-live. Data posture is the strongest in the cohort — Stage 6 green is unique (910 inventory records, fresh Jun 2; dual-currency pricing; 3 user type groups) — but customers are not yet imported and the BC integration has not started. The order pipeline discrepancy (5 MixPanel vs 0 DB orders) needs immediate investigation. BC integration call Jun 4 with Brent is the next critical milestone.

---

## DRF (Dorell Fabrics)

**V11 Assessment:** Stage 5 | 65% Ready | Products: eCat iPad only

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | 4 admin users, company active (Apr 15, 2026) |
| 2 | 🟢 | 1,676 products, 1,180 with images (70%), 10 categories, 99 collections — last update Jun 2 |
| 3 | 🟡 | 1 price level (Net only) — functional but thin; fabric manufacturer likely needs dealer/volume tier (Stage 3 criteria: YELLOW — 1 price level passes minimum but risks pricing structure completeness) |
| 4 | ⚫ | N/A — fabric colors are discrete SKUs, no configurable options required; 0 options is intentional |
| 5 | 🟢 | 389 customers loaded (last update Apr 27); all 9 territory codes assigned to Suzanne for full iPad visibility |
| 6 | 🔴 | **Import error Jun 2:** "Validation failed: Product image content type is invalid, Product image is invalid" — blocking image imports; **0 inventory records** |
| 7 | 🔴 | 1 DB order, 1 MixPanel order (last May 18); 3 report formats ✅; 1 user type (DefaultUserGroup only) ❌; order email empty ❌ |

🎯 **V11 Next Action:** Fix Jun 2 image import error (identify and re-upload invalid file format), configure order email recipient, add second price level (dealer/volume tier), check in with client (23 days since last HelpScout contact)

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 6 | ⚠️ IMPORT ERROR | Import Jun 2 | `:error` entry: "Validation failed: Product image content type is invalid, Product image is invalid" — one or more image files uploaded in unsupported format; needs re-upload |
| - | ⚠️ COMMUNICATION GAP | Fathom + Help Scout | No HelpScout activity since May 11 (23 days); last Fathom call May 18 (16 days ago) — catalog imports are continuing (Loomcraft/Brian Frankel appears to be driving data work) but no direct client communication |

**Validation Summary:** DRF is the most structurally advanced client in the cohort — 389 customers, 1,676 products, 3 report formats, 1 DB order, Stage 5 green. However, Stage 6 is newly blocked by a Jun 2 image import error and persistent 0 inventory. Communication from the client side has gone quiet (23 days). Active catalog imports (107 total events, last Jun 2) confirm Loomcraft is continuing data work autonomously, but a direct check-in with Suzanne/Christine is overdue to confirm path forward on inventory and whether a second price level is planned.

---

## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| LIBCO | - | Market deadline in 13 days | "Be live by June market; Silvio leaves June 19" (Fathom May 20) | Daily monitoring — customer import + BC integration are on critical path |
| LIBCO | 7 | Order pipeline not closing to DB | 5 MixPanel orders vs 0 DB orders (last event May 22) | Investigate immediately — confirm test mode vs live pipeline issue |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| TCS | 3 | Catsy dependency stalling export | "Waiting on Catsy working session to update accessory attribute groups" (HS May 28) | Confirm Catsy session date; unblock pricing data export |
| TCS | 3 | Data approach conflict | "SKU Builder is a working prototype...master sheet is the source of truth" (HS Jun 2) | Align on master sheet + Catsy export as primary source; rebuild accordingly |
| PEBL | 2 | Missing custom fields in product imports | Warning: Certification, Color, PackingSize, Materials1, FrameColor missing (Import Jun 3) | Share custom field format template with Mandy Mai |
| DRF | 6 | Image import error Jun 2 | "Product image content type is invalid" (Import Jun 2) | Identify invalid image file, re-upload in supported format |
| DRF | - | Communication gap (23 days) | No HelpScout since May 11, last Fathom May 18 | Check-in with Suzanne/Christine — confirm inventory plan and pricing tier roadmap |

### ✅ Confirmed (No Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| - | - | - | No clients in this cohort are fully confirmed — all have active flags |
