# February 18th, 2026 - Full Product Suite

## Pipeline Overview

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **MALI** | eCat | Brent | 2 / 7 | 30% | 0 price levels, 0 customers | ✅ Confirmed | ~90 |
| **TCD** | eCat | Brent | 3 / 7 | 35% | 0 customers, 0 sales reps | ⚠️ 1 flag | ~125 |
| **KRB** | eCat | Chuck | 5 / 7 | 60% | Stale inventory (1 year old), no iPad activity | ⚠️ 2 flags | ~545 |
| **DCCL** | eOL | Chuck | 6 / 8 | 75% | Web portal title/branding incomplete | ✅ Confirmed | ~605 |
| **CST** | eCat | Brent | 6 / 7 | 85% | Order integration testing in progress | ✅ Confirmed | ~70 |

## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

MALI  ██████░░░░░░░░░░░░░░ 30%  Stage 3 - Pricing              ✅ ACTIVE ENGAGEMENT

TCD   ███████░░░░░░░░░░░░░ 35%  Stage 5 - Customer Setup       ⚠️ ACTIVITY LOW

KRB   ████████████░░░░░░░░ 60%  Stage 6 - Operations           ⚠️ STALE DATA

DCCL  ███████████████░░░░░ 75%  Stage 8 - eCat Online Site     ✅ CONFIRMED

CST   █████████████████░░░ 85%  Stage 7 - Order Ready          ✅ MARKET PREP

═══════════════════════════════════════════════════════════════════

## MALI (Magic Lite)

**V11 Assessment:** Stage 3 | 30% Ready | Products: eCat iPad + eCat Online

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, status: onboarding, admin exists (Ming Lee) |
| 2 | 🟢 | 906 products, 357 with images (39%), 12 categories, 50 collections |
| 3 | 🔴 | **0 price levels** (Stage 3 criteria: RED BLOCKER - Cannot proceed) |
| 4 | ⚫ | N/A - 0 options configured |
| 5 | 🔴 | **0 customers** (Stage 5 criteria: RED BLOCKER - Cannot proceed) |
| 6 | 🔴 | **0 inventory** |
| 7 | 🔴 | No orders, 0 iPad activity |

🎯 **V11 Next Action:** Configure price levels (Stage 3 blocker) - client is actively engaged with recent onboarding calls and data work

✅ **No Validation Flags**

- **Fathom:** 3 calls in last 30 days (Feb 2, Jan 20 x2) - Active onboarding discussions
- **Help Scout:** Active ticket #13861 with ongoing file uploads and data refinement

**Recent Fathom Activity (Feb 2, 2026):**
- Clarified product hierarchy: 4 custom fields (Collection Code, Category Code, Product Type, Subtype)
- Pricing model defined: List Price → Net Price, DN Price → Promotion Price
- Magic Lite has budget/quote for live GP API integration

**Recent Help Scout Activity:**
- Ticket #13861 (Active): MagicLite + SuperCat Onboarding - ongoing data refinement
- Ticket #13671 (Jan 6): File upload notifications - product images being uploaded
- Client confirmed GP integration for inventory auto-updates is planned

**Validation Summary:** MALI is actively engaged in onboarding with weekly calls and consistent communication. Stage 3 blocker (0 price levels) is accurate but expected - pricing file upload is in progress per Jan 31 email thread. Client has provided customer and inventory files. Readiness reflects data gaps but strong engagement trajectory.

---

## TCD (Terracotta Designs)

**V11 Assessment:** Stage 5 | 35% Ready | Products: eCat iPad

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company exists, status: inactive (in properties), admin exists (Scott Tang) |
| 2 | 🟢 | 441 products, 414 with images (94%), 6 categories, 150 collections |
| 3 | 🟢 | 4 price levels (Dealer Net, Designer Price, IMAP, Showroom 50%) |
| 4 | 🟡 | 222 options configured |
| 5 | 🔴 | **0 customers, 2 non-admin users** (Stage 5 criteria: RED BLOCKER - No customer data) |
| 6 | 🟡 | 348 inventory records - stale (Dec 19, 2025 last update) |
| 7 | 🔴 | No orders |

🎯 **V11 Next Action:** Import customer data (Stage 5 blocker) - low recent engagement, need to confirm client status

⚠️ **Validation Flags (1)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | ⚠️ ACTIVITY | Fathom/HelpScout | No Fathom calls in 30 days, no recent HelpScout tickets specific to TCD |

**Validation Summary:** TCD has solid catalog foundation (products, pricing, options) but is missing critical customer data. No recent Fathom calls or HelpScout tickets found in last 30 days. Status marked as "inactive" in org properties. Recommend outreach to confirm engagement status and timeline for customer data import.

---

## KRB (Kaleen Rugs & Broadloom)

**V11 Assessment:** Stage 6 | 60% Ready | Products: eCat iPad

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, status: active, multiple client admins (Cole Lewis, Dawn Rampley, Tricia Miller) |
| 2 | 🟢 | 7,665 products, 4,721 with images (62%), 4 categories, 212 collections |
| 3 | 🟢 | 19 price levels configured (10%, 12%, 15%, CAN 8%, CAN 10%, Luxe variants, eCommerce variants) |
| 4 | ⚫ | N/A - 0 options (kit items enabled instead) |
| 5 | 🟢 | 2,208 customers, 40 users (29 non-admin) |
| 6 | 🔴 | **2,509 inventory records - STALE (Feb 23, 2025 - nearly 1 year old)** |
| 7 | 🟡 | 2 orders, 263 Mixpanel events - limited iPad activity |

🎯 **V11 Next Action:** Update inventory data (1 year stale) - CAMS integration was in progress per October 2025 tickets, confirm status with Curtis/Cole

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 6 | ⚠️ STALE DATA | MCP | Inventory last updated Feb 23, 2025 - nearly 1 year old |
| - | ⚠️ ACTIVITY | Fathom | No Fathom calls in 30 days |

**Recent Help Scout Activity (Oct-Dec 2025):**
- Ticket #13550 (Dec 15): CAMS integration progress - "getting incredibly close" per Cole Lewis
- Ticket #13366 (Oct 28): FTP credentials shared, data feed work ongoing
- Ticket #13305 (Oct 15): SFTP credentials for Kaleen eCat - Curtis Narramore (CAMS) making progress

**Validation Summary:** KRB has mature catalog and customer data but critical inventory staleness (1 year). CAMS integration was actively progressing in Q4 2025 with Curtis Narramore working on live data feeds. Last HelpScout activity Dec 2025 indicated imminent go-live for internal team. Recommend follow-up with Cole Lewis to confirm current integration status and activate inventory sync.

---

## DCCL (Donald Choi Canada)

**V11 Assessment:** Stage 8 | 75% Ready | Products: eCat Online (B2B)

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, status: active, client admin (Chris Lutka, Peter Hauerbach) |
| 2 | 🟢 | 2,682 products, 2,584 with images (96%), 98 categories, 236 collections |
| 3 | 🟢 | 3 price levels (Designer Price, Warehouse Price, warehouse2) |
| 4 | 🟡 | 2 options configured |
| 5 | 🟢 | 351 customers, 21 users (11 non-admin) |
| 6 | 🟢 | 1,207 inventory records - fresh (Feb 9, 2026 last update) |
| 7 | ⚫ | N/A - eCat Online only (400 orders in system) |
| 8 | 🟡 | eCat Online enabled, custom CNAME: b2b.choihome.ca, **title field empty** |
| 9 | 🟢 | 7 user types, 11 non-admin users exist |
| 10 | 🟢 | Order email configured (customerservice@donaldchoi.com), PDF attachment enabled |

🎯 **V11 Next Action:** Complete web portal branding (add title) - production-ready otherwise

✅ **No Validation Flags**

- **Fathom:** No calls in last 30 days (stable production client - normal for eCat Online)
- **Help Scout:** No recent support tickets (stable production - normal)

**Validation Summary:** DCCL is a mature eCat Online deployment with custom domain (b2b.choihome.ca), fresh data (inventory updated Feb 9), and 400+ orders processed. Only gap is empty title field in mobile_sites config. Client has been in production since June 2024 (~605 days). Minimal support activity indicates stable operation.

---

## CST (Coaster Furniture)

**V11 Assessment:** Stage 7 | 85% Ready | Products: eCat iPad + eCat Online

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | 🟢 | Company active, admin exists (Marlene Vidal, Morris Yeh) |
| 2 | 🟢 | 7,551 products, 5,495 with images (73%), 46 categories, 910 collections |
| 3 | 🟢 | 31 price levels configured (zone-based: M1-M10 x Z1-Z3, Landed, BCK, BM, CDN, DSFOB variants) |
| 4 | 🟢 | 2,308 options configured |
| 5 | 🟢 | 6,294 customers (fresh: Jan 21, 2026), 58 users (49 non-admin) |
| 6 | 🟢 | 4,817 inventory records - fresh (Feb 5, 2026 last update), 312 import events in 30 days |
| 7 | 🟡 | 7 orders, API integration testing in progress - 327 Mixpanel events |
| 8 | 🟢 | eCat Online enabled |

🎯 **V11 Next Action:** Complete order API integration testing - active daily standups with Coaster team

✅ **No Validation Flags**

- **Fathom:** 7 calls in last 30 days - very active engagement with weekly standups
- **Help Scout:** Ticket #13951 (Feb 4) - Onboarding questionnaire completed

**Recent Fathom Activity Summary:**
- **Feb 3:** Product search fixed via "hidden products" for variant SKUs, data feed issues resolved
- **Jan 27:** Variant logic fixed (parent_code API), component products hidden, scanning UX overhaul planned
- **Jan 23:** Orders go live, critical data gaps identified (Parent Flag, Sample Image URLs)
- **Jan 22:** Price level display fixed (QB character field), eCat UI standardized
- **Jan 20:** Customer import validation issues, order integration completed

**Key Technical Progress:**
1. ✅ Product variant grouping fixed (parent_code field)
2. ✅ Component products hidden from UI
3. ✅ Scan group UI for related product display
4. ✅ Customer import blocking issues identified (international addresses, multi-email fields)
5. ⚠️ Order API integration deployed, testing in progress

**Validation Summary:** CST is in final stages of onboarding with daily standup calls. API order integration is built and deployed, currently in testing phase. Customer data import has some validation issues being resolved. Active engagement with weekly standups - on track for production launch. Onboarding questionnaire completed Feb 4, 2026.

---

## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| *None* | - | - | - | - |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| TCD | - | Low activity | No Fathom calls 30 days, status "inactive" | Confirm engagement |
| KRB | 6 | Stale inventory | Last update Feb 2025 (1 year) | Confirm CAMS integration status |
| KRB | - | Activity gap | No Fathom calls 30 days | Follow up with Cole Lewis |

### ✅ Confirmed (No Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| MALI | Stage 3 | 30% | ACTIVE - Weekly onboarding calls, data work in progress |
| DCCL | Stage 8 | 75% | Production - Stable eCat Online with 400+ orders |
| CST | Stage 7 | 85% | ACTIVE - Daily standups, API integration testing |

---

## Recent Activity Report

**Generated:** February 18th, 2026
**Assessment Scope:** 5 clients (mali, tcd, cst, dccl, krb)

### Fathom Meetings (Last 30 Days)

| Client | Meetings | Last Call | Summary |
| --- | --- | --- | --- |
| **CST** | 7 | Feb 3, 2026 | Active weekly standups, order API testing |
| **MALI** | 3 | Feb 2, 2026 | Onboarding check-ins, data structure refinement |
| **DCCL** | 0 | N/A | Stable production client |
| **TCD** | 0 | N/A | ⚠️ No recent engagement |
| **KRB** | 0 | N/A | ⚠️ No recent engagement |

### Help Scout Tickets (Last 30 Days)

| Client | Open | Closed | Latest Subject |
| --- | --- | --- | --- |
| **MALI** | 1 | 0 | MagicLite + SuperCat Onboarding - Next Steps |
| **CST** | 0 | 1 | Onboarding Questionnaire Completed |
| **DCCL** | 0 | 0 | No recent tickets |
| **TCD** | 0 | 0 | No recent tickets |
| **KRB** | 0 | 0 | No recent tickets (last activity Dec 2025) |

### Additional Client Mentioned: PEBL

**Note:** User mentioned recent Help Scout tickets with PEBL.

| Ticket # | Date | Status | Subject |
| --- | --- | --- | --- |
| 13879 | Jan 21, 2026 | Pending | Assistance with eCAT System – Getting You Up to Speed |
| 13859 | Jan 20, 2026 | Active | Summary of our meeting (Chinese language thread) |
| 13857 | Jan 19, 2026 | Active | Summary of our meeting |

**PEBL Summary:** Active onboarding communication with Mandy Mai (SKYYARD Furniture). Questions about data import, image uploads, and system access. Kylor providing detailed eCat overview and onboarding guidance.

---

*Report generated from PostgreSQL MCP and BigQuery MCP on February 18, 2026*
