# June 3rd, 2026 — Onboarding Assessment (v2 — Validation Run)

> **Validation run.** Independent re-run of the same cohort (`pebl`, `tcs`, `drf`, `libco`) on the same date to verify reproducibility against `2026-06-03-assessment.md`. All metrics below were re-pulled from Postgres (`user-supercat-postgres-vpn`) and BigQuery (`user-bigquery-admin`). See **Validation Run Notes (v2 vs v1)** at the bottom for the diff. Stage/readiness numbers are held identical to v1 where the underlying metrics reproduced, for clean comparison.

## Pipeline Overview

| Client | Product | Owner | Stage | Readiness | Biggest Blocker | Validation | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **TCS** | eCat iPad | Kylor | 2 / 7 | 30% | 0 price levels; Catsy/PIM export stalled | ⚠️ 2 flags | ~44 |
| **PEBL** | eCat iPad | Kylor | 4 / 7 | 55% | 0 customers, 0 inventory | ⚠️ 2 flags | ~314 |
| **LIBCO** | eCat iPad | Kylor | 4 / 7 | 60% | 0 customers, 0 DB orders, Lightovation deadline | 🔴 2 flags | ~72 |
| **DRF** | eCat iPad | Kylor | 5 / 7 | 65% | Jun 2 image import error, 0 inventory, 1 price level | ⚠️ 2 flags | ~49 |

## PIPELINE VIEW — Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

TCS   ██████░░░░░░░░░░░░░░ 30%  Stage 3 - Pricing              ⚠️ ACTIVE ENGAGEMENT

PEBL  ███████████░░░░░░░░░ 55%  Stage 5 - Customer Setup       ⚠️ ACTIVE ENGAGEMENT

LIBCO ████████████░░░░░░░░ 60%  Stage 5 - Customer Setup       🔴 FLAGGED

DRF   █████████████░░░░░░░ 65%  Stage 6 - Operations           ⚠️ FLAGGED

═══════════════════════════════════════════════════════════════════

---

## TCS (The Coppersmith)

**Assessment:** Stage 2 | 30% Ready | Products: eCat iPad only
**Days Active:** ~44 (created Apr 20, 2026) · **Domains:** thecoppersmith.net

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | 4 users, all admin; company active (Apr 20, 2026) |
| 2 | 🟢 | 283 products, 253 with images (89%), 3 categories, 48 collections — last update May 5 |
| 3 | 🔴 | **0 price levels — BLOCKER** (cannot proceed without pricing configured) |
| 4 | 🟢 | 390 options (out of sequence — Stage 3 still gates progression) |
| 5 | 🔴 | **0 customers — BLOCKER** |
| 6 | 🔴 | **0 inventory; no imports since May 5** (29 days); 48 import events all-time, 3 with errors |
| 7 | 🔴 | 0 DB orders, 0 iPad orders (90d), 0 report formats, order email empty |

🎯 **Next Action:** Unblock the Catsy → eCat data path. Configure price levels (Stage 3 gate); awaiting Catsy working session to finalize accessory attribute groups before a clean export is possible. Align on the master sheet as source of truth per the Jun 2 thread.

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 3 | ⚠️ CATSY DEPENDENCY | HelpScout #14520 May 28 (digital@thecoppersmith.net) | "We are currently waiting on our next Catsy working session to update the accessory attribute groups so they align with our newly updated master sheet and to finalize a few remaining data organization details." |
| 3 | ⚠️ APPROACH CONFLICT | HelpScout #14520 Jun 2 (digital@thecoppersmith.net) | "What we are trying to avoid is creating manual steps, duplicate formatting work, or a second structure on the eCat side that does not translate back to what we are trying to streamline through our PIM. The SKU Builder is a working prototype…" |

**Validation Summary:** Reproduces v1. TCS is actively engaged — ticket #14520 is a dense thread, client followed up "Any updates with this?" Jun 2 (jillian.beranek@thecoppersmith.net). Catalog work is strong (283 products, 89% image coverage, 390 options) but the account is structurally blocked by (1) the Catsy PIM update gating a clean product/option/pricing export, and (2) alignment on master-sheet-vs-SKU-Builder as the primary source. No imports in 29 days; 0 price levels and 0 customers are the hard gates.

---

## PEBL (Skyard Furniture Co Ltd.)

**Assessment:** Stage 4 | 55% Ready | Products: eCat iPad only
**Days Active:** ~314 (created Jul 24, 2025) · **Domains:** peblfurniture.com
**Enrichment:** segment Catalog-Focused · health 0.5 (Needs Attention) · ARR $8,700

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | 3 users, all admin; company active |
| 2 | 🟢 | 299 products, 188 with images (63%), 11 categories, 28 collections — actively importing TODAY (Jun 3) |
| 3 | 🟢 | 2 price levels (Normal/fob, Project) |
| 4 | 🟢 | 103 options |
| 5 | 🔴 | **0 customers — BLOCKER**; only 1 user type (DefaultUserGroup) |
| 6 | 🔴 | **0 inventory**; 194 import events (last today Jun 3), recent product imports throwing custom-field warnings + option-code-length errors |
| 7 | 🔴 | 2 DB orders, 2 iPad orders (90d, last May 29), 1 report format, order email empty |

🎯 **Next Action:** Import the customer file (Stage 5 gate) and provide an inventory file. Align the products.csv template to the registered custom fields to clear recurring import warnings. PEBL is in an active catalog-build sprint ahead of SPOGA.

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 2 | ⚠️ DATA GAP | Import Jun 3 11:56 | Product import warnings: custom fields `Certification`, `Color` (and more) missing on Line 1 — metadata template not yet aligned; option imports earlier hit `:error` "Code is too long (maximum is 15 characters)" (May 28) |
| 2 | ✅ ACTIVE | HelpScout #13879 Jun 3 (sales04@peblfurniture.com) | "Attached is the updated products.csv, today we upload more collections. I will update the file of option mapping asap." — client confirmed all 6 option-mapping assumptions; Kylor completed Frame Color → cushion/material configuration |

**Validation Summary:** Reproduces v1. PEBL is the most actively-importing account in the cohort — 194 import events, last one today (Jun 3 11:56). Catalog and pricing are green; options are configured (103). The structural blockers are 0 customers (Stage 5 gate) and 0 inventory. The product-import warnings are template-alignment issues (missing custom fields) rather than data loss. Client (Mandy Mai) is engaged and pushing toward SPOGA.

---

## LIBCO (Lib and Co.)

**Assessment:** Stage 4 | 60% Ready | Products: eCat iPad only
**Days Active:** ~72 (created Mar 23, 2026) · **Domains:** libandco.com

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | 3 users (2 admin, 1 non-admin rep); 3 user-type groups (DefaultUserGroup, US Reps, Canadian Reps) |
| 2 | 🟢 | 907 products, 802 with images (88%), 5 categories, 62 collections — last update Jun 2 |
| 3 | 🟢 | 4 price levels (CAD_WSP, CAD_IMAP, USA_IMAP, USA_WSP) — dual-currency WSP + IMAP tiers |
| 4 | ⚫ | N/A — lighting fixtures; per-SKU catalog, no configurable options (0 options intentional) |
| 5 | 🔴 | **0 customers — BLOCKER** (showroom-as-account structure + territory codes defined May 28, not yet imported) |
| 6 | 🟢 | 910 inventory records, last update Jun 2 — FRESH (only client in cohort with Stage 6 green) |
| 7 | 🔴 | **0 DB orders AND 0 iPad orders (90d / all-time)** — corroborated by `org_feature_usage_report` (`submit_order` 0, `view_ipad_orders` 0, only 15 logins); 1 report format (<3); order email empty |

🎯 **Next Action:** 🚨 URGENT — Import the customer file (showroom-as-account + territory codes, confirmed May 28); complete the Business Central integration call with Brent (CTO); progress rep onboarding ahead of the June Dallas/Lightovation market. **On the Jun 4 BC call, have a rep submit one test order and confirm it lands in both MixPanel (`order_submitted`) and the Postgres `orders` table** — the order path has never been exercised (0 orders ever), and it sits on the Lightovation critical path.

🔴 **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | 🔴 TIMELINE | Fathom May 20 "Lib & Co Onboarding - Path to going live" (60 min) | "The goal is to be live for the June Dallas market. SuperCat will use existing data files to get reps selling immediately, then build the automated BC integration in the background." ([recording](https://fathom.video/share/4xrjwLC6xFom_cHzWFopWtrgKJcTD-Ss)) |
| 5/7 | 🔴 CUSTOMERS + ORDERS NEVER STARTED | Postgres + BigQuery | 0 customers imported; **0 orders ever submitted, triple-confirmed** — Postgres `orders` 0, `org_feature_usage_report` `submit_order`/`view_ipad_orders` 0, `mixpanel.events` `order_submitted` 0 all-time (corrects v1 — see notes). The order path has never been exercised, not even a test. |

**Validation Summary:** Highest-urgency account — hard June Dallas/Lightovation market deadline (May 20 call) and customers not yet imported. Data posture is the cohort's strongest: Stage 6 is uniquely green (910 inventory records, fresh Jun 2), dual-currency pricing, 3 user-type groups, showroom-as-account structure defined (May 28 Fathom + HelpScout #14554). The BC integration with CTO Brent is the next critical milestone. **Correction vs v1:** this run finds **0** MixPanel `order_submitted` events for libco (v1 reported 5, last May 22) — under standard attribution none are reproducible, and the zero is corroborated by `org_feature_usage_report` (`submit_order` 0, `view_ipad_orders` 0). So no order has ever been submitted on the iPad — test or live — rather than an order-persistence gap. Stage 7 stays 🔴 either way. Because order submission is on the Lightovation critical path, a rep should submit one test order at/before the Jun 4 BC call and confirm it lands in both MixPanel and the `orders` table.

---

## DRF (Dorell Fabrics)

**Assessment:** Stage 5 | 65% Ready | Products: eCat iPad only
**Days Active:** ~49 (created Apr 15, 2026) · **Domains:** dorellfabrics.com, loomcraft.com

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | 4 users, all admin; company active (Apr 15, 2026) |
| 2 | 🟢 | 1,676 products, 1,180 with images (70%), 10 categories, 99 collections — last update Jun 2 |
| 3 | 🟡 | 1 price level (Net only) — passes minimum but thin; a fabric manufacturer likely needs a dealer/volume tier |
| 4 | ⚫ | N/A — fabric colors are discrete SKUs, no configurable options (0 options intentional) |
| 5 | 🟢 | 389 customers (last update Apr 27) |
| 6 | 🔴 | **Import error Jun 2:** "Validation failed: Product image content type is invalid, Product image is invalid"; **0 inventory**; 107 events all-time (2 error, 1 historic fatal deadlock May 5) |
| 7 | 🔴 | 1 DB order, 1 iPad order (90d, last May 18); 3 report formats ✅; 1 user type ❌; order email empty ❌ |

🎯 **Next Action:** Fix the Jun 2 image import error (identify/re-upload the invalid-format file), configure an order-email recipient, consider a second price level (dealer/volume), and check in with the client — no direct touchpoint since early May.

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 6 | ⚠️ IMPORT ERROR | Import Jun 2 21:49 | `:error` — "Validation failed: Product image content type is invalid, Product image is invalid" — one or more images uploaded in unsupported format; needs re-upload |
| - | 🔄 COMMUNICATION GAP | Fathom May 18 / HelpScout #14438 last May 5 | No HelpScout client thread since May 5; last Fathom "SuperCat / Dorell: Implementation Check-In" May 18 (loomcraft.com). Catalog imports continue (last Jun 2) — Loomcraft appears to be driving data work — but no recent direct client communication |

**Validation Summary:** Reproduces v1. DRF is the most structurally advanced account — 389 customers, 1,676 products, 3 report formats, 1 live DB/iPad order, Stage 5 green. Stage 6 is blocked by a Jun 2 image content-type error and persistent 0 inventory. Active imports (107 events, last Jun 2) confirm data work continues via Loomcraft, but a direct check-in with Suzanne/Christine is overdue to confirm the inventory plan and whether a second price level is coming. The May 5 fatal deadlock is historic (outside the recent window) and not a current blocker.

---

## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| LIBCO | - | June Dallas/Lightovation market deadline | "The goal is to be live for the June Dallas market" (Fathom May 20) | Daily monitoring — customer import + BC integration on critical path |
| LIBCO | 5/7 | Customers not imported; order path never exercised | 0 customers; 0 orders ever (Postgres + `org_feature_usage_report` + `mixpanel.events` all 0) | Import showroom-as-account customer file; **submit one test order at the Jun 4 BC call and confirm it lands in MixPanel + the `orders` table** |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| TCS | 3 | Catsy dependency stalling export | "Waiting on our next Catsy working session…" (HS #14520 May 28) | Confirm Catsy session date; unblock pricing/product export |
| TCS | 3 | Data approach conflict | "SKU Builder is a working prototype…avoid a second structure on the eCat side" (HS #14520 Jun 2) | Align on master sheet + Catsy export as primary source |
| PEBL | 2 | Missing custom fields + option-code length | Warnings: `Certification`, `Color` missing (Import Jun 3); `:error` option Code >15 chars (May 28) | Share custom-field template; trim option codes to ≤15 chars |
| DRF | 6 | Image import error Jun 2 | "Product image content type is invalid" (Import Jun 2) | Identify invalid image file, re-upload in supported format |
| DRF | - | Communication gap | No HelpScout client thread since May 5; last Fathom May 18 | Check in with Suzanne/Christine — inventory plan + pricing tier roadmap |

### ✅ Confirmed (No Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| - | - | - | No clients in this cohort are fully confirmed — all have active flags |

---

## Validation Run Notes (v2 vs v1)

This run independently reproduced `2026-06-03-assessment.md`. Findings:

- **Reproduced cleanly:** All Postgres config metrics matched v1 — products (TCS 283, PEBL 299, LIBCO 907, DRF 1,676), images, categories/collections, price levels, options (PEBL 103, TCS 390), customers (DRF 389; others 0), users/user-types, inventory (LIBCO 910 fresh Jun 2; others 0), report formats, DB orders (DRF 1, PEBL 2), and import-event recency. Stage assignments and readiness % are unchanged.
- **One genuine correction — LIBCO MixPanel orders:** v1 reported "5 MixPanel `order_submitted` events, last May 22." This run finds **0** such events for `libco` — both in the 90-day window and all-time — under the documented attribution (`COALESCE(organization_shortname, current_organization_shortname)`), and corroborated by a third source: `org_feature_usage_report` shows `submit_order` 0, `view_ipad_orders` 0, only 15 logins. The real eCat shortname was confirmed as `libco` (Lib and Co., created Mar 23 2026; Postgres `orders` 0, `customers` 0), so this is not a shortname-mismatch artifact. v1's stated "5 MixPanel vs 0 DB orders pipeline discrepancy" is **not reproducible** — the likely cause of v1's 5 is the retired `api_access`-join attribution heuristic. The accurate read: no order has ever been submitted on the iPad, test or live. Stage 7 (🔴) and readiness (60%) unchanged, but the blocker narrative shifts from "orders not persisting to DB" to "order path never exercised — verify with a test order before the market."
- **Process note (this run, not a data issue):** the initial batched import-events query used `LIMIT 120` ordered by shortname, which let `drf`+`libco` consume the cap and truncated `pebl`/`tcs`. Re-running per client confirmed PEBL = 194 events (last Jun 3) and TCS = 48 events (last May 5), consistent with v1. Future runs should aggregate counts or window per-org rather than a single global LIMIT.
- **LIBCO timeline quote:** v1 cited "Silvio leaves June 19 for California." That exact phrasing was not in the retrievable May 20 Fathom summary; the verifiable quote used here is "The goal is to be live for the June Dallas market." The June-market deadline itself is corroborated.

**Sources this run:** Postgres `user-supercat-postgres-vpn`; BigQuery `user-bigquery-admin` (`mixpanel.org_feature_usage_report`, `mixpanel.events`, `insightful_product.org_summary`, `onboarding_assessment.fathom_recent_meetings`, `onboarding_assessment.helpscout_tickets`). Run date 2026-06-03 (UTC).
