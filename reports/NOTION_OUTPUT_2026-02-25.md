# February 25th, 2026 - Full Product Suite

> **⚠️ DATA LIMITATION NOTICE:** eCat configuration data (products, customers, price levels, territories, options, categories, collections, inventory, import events, orders, mobile sites, report formats, user types) is **unavailable** due to PostgreSQL MCP permissions issue (`crunchy_reader` user lacks SELECT grants). Stage assessments for Stages 2-11 that depend on this data are marked with ❓. Assessments are based on HubSpot, MixPanel, Fathom, and HelpScout data only. Fix: `GRANT SELECT ON ALL TABLES IN SCHEMA public TO crunchy_reader;`

## Pipeline Overview

| Client | Product | Owner | V11 Stage | V11 Readiness | Biggest Blocker | Validation Status | Days Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **PEBL** | eCat | Brent | ❓ / 7 | ❓ | ❓ eCat config data unavailable - 0 orders, 0 iPad activity | 🔴 1 flag | ~240 |
| **HVUSA** | eCat | Chuck | ❓ / 7 | ❓ | ❓ eCat config data unavailable - 0 orders, minimal activity (5 events) | 🔴 1 flag | ~1890 (mature) |
| **TCD** | eCat | Brent | ❓ / 7 | ❓ | ❓ eCat config data unavailable - 0 orders, 0 iPad activity | 🔴 1 flag | ~615 |
| **MALI** | eCat | Brent | ❓ / 7 | ❓ | ❓ eCat config data unavailable - 0 orders, 7 events total | ⚠️ 1 flag | ~50 |
| **KRB** | eCat | Chuck | ❓ / 7 | ❓ | ❓ eCat config data unavailable - 0 orders, 264 api events | ⚠️ 1 flag | ❓ |
| **DCCL** | eOL | Chuck | ❓ / 8 | ❓ | Server caching issues on taxonomy (active support tickets) | ⚠️ 2 flags | ~660 |
| **CST** | eCat | Brent | ❓ / 7 | ❓ | ❓ eCat config data unavailable - 0 orders, 364 api events | ⚠️ 1 flag | ~395 |

## PIPELINE VIEW - Least Ready → Most Ready

═══════════════════════════════════════════════════════════════════

PEBL  ❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓  ❓%   Stage ❓ - Unknown             🔴 STALLED

HVUSA ❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓  ❓%   Stage ❓ - Unknown             🔴 STALLED

TCD   ❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓  ❓%   Stage ❓ - Unknown             🔴 STALLED

MALI  ❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓  ❓%   Stage ❓ - Unknown             ⚠️ ACTIVE ENGAGEMENT

KRB   ❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓  ❓%   Stage ❓ - Unknown             ⚠️ ACTIVE ENGAGEMENT

DCCL  ❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓  ❓%   Stage ❓ - Unknown             ⚠️ SUPPORT ACTIVE

CST   ❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓❓  ❓%   Stage ❓ - Unknown             ⚠️ ACTIVE ENGAGEMENT

═══════════════════════════════════════════════════════════════════

---

## PEBL (Pebl Furniture)

**V11 Assessment:** Stage ❓ | ❓% Ready | Products: eCat iPad
**HubSpot Lifecycle:** Customer (not Onboarding) | Domain: peblfurniture.com
**MixPanel Activity:** 19 total events, 4 unique users, 0 orders, 0 iPad orders

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied (org info, admin users) |
| 2 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied (product counts, categories, collections) |
| 3 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied (price levels) |
| 4 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied (options) |
| 5 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied (customers, users) |
| 6 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied (import events, inventory) |
| 7 | 🔴 | **0 iPad orders** (MixPanel), 0 orders submitted - confirmed via BigQuery |

🎯 **V11 Next Action:** ❓ Cannot determine next action - eCat configuration data unavailable. Resolve PostgreSQL permissions to complete assessment.

🔴 **Validation Flags (1)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | 🔴 ACTIVITY | Fathom + HelpScout | 0 Fathom calls in 30 days, 0 HelpScout tickets in 30 days |

**Validation Summary:** PEBL shows minimal engagement. HubSpot lists them as "Customer" not "Onboarding." MixPanel shows 19 events (all api_access) with 4 unique users but zero orders. No Fathom calls and no HelpScout tickets in the last 30 days.

---

## HVUSA (Hudson Valley Group)

**V11 Assessment:** Stage ❓ | ❓% Ready | Products: eCat
**HubSpot Lifecycle:** Customer | Domain: hvlgroup.com
**MixPanel Activity:** 5 total events, 3 unique users, 0 orders, 0 iPad orders

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 2 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 3 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 4 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 5 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 6 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 7 | 🔴 | **0 iPad orders** (MixPanel), 0 orders submitted - confirmed via BigQuery |

🎯 **V11 Next Action:** ❓ Cannot determine next action - eCat configuration data unavailable. Note: HVUSA is listed as "Customer" in HubSpot (not Onboarding).

🔴 **Validation Flags (1)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | 🔴 ACTIVITY | Fathom + HelpScout | 0 Fathom calls in 30 days, 0 HelpScout tickets in 30 days, only 5 MixPanel events total |

**Validation Summary:** HVUSA is a long-standing customer (created Dec 2020). Very low MixPanel activity (5 events, all api_access). HubSpot lifecycle = "Customer" not "Onboarding." No Fathom calls or HelpScout tickets in 30 days.

---

## TCD (Terracotta Designs)

**V11 Assessment:** Stage ❓ | ❓% Ready | Products: eCat iPad
**HubSpot Lifecycle:** Onboarding (evangelist) since Dec 30, 2025 | Domain: terracottalighting.com
**MixPanel Activity:** 31 total events, 3 unique users, 0 orders, 0 iPad orders

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 2 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 3 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 4 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 5 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 6 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 7 | 🔴 | **0 iPad orders** (MixPanel), 0 orders submitted - confirmed via BigQuery |

🎯 **V11 Next Action:** ❓ Cannot determine next action - eCat configuration data unavailable. TCD entered onboarding Dec 30, 2025 (~57 days ago).

🔴 **Validation Flags (1)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | 🔴 ACTIVITY | Fathom + HelpScout | 0 Fathom calls in 30 days, 0 HelpScout tickets in 30 days |

**Validation Summary:** TCD entered onboarding status in HubSpot Dec 30, 2025. Shows 31 MixPanel events (all api_access) from 3 users, indicating some platform interaction. Zero Fathom calls and zero HelpScout tickets in last 30 days.

---

## MALI (Magic Lite)

**V11 Assessment:** Stage ❓ | ❓% Ready | Products: eCat iPad
**HubSpot Lifecycle:** Onboarding (evangelist) since Jan 6, 2026 | Domain: magiclite.com
**MixPanel Activity:** 7 total events, 3 unique users, 0 orders, 0 iPad orders

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 2 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 3 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 4 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 5 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 6 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 7 | 🔴 | **0 iPad orders** (MixPanel), 0 orders submitted - confirmed via BigQuery |

🎯 **V11 Next Action:** ❓ Cannot determine specific stage blocker - eCat configuration data unavailable. MALI is a newer onboarding client (Jan 6, 2026).

⚠️ **Validation Flags (1)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | ⚠️ ACTIVITY | Fathom + HelpScout | 0 Fathom calls in 30 days, 0 HelpScout tickets in 30 days - but client is only ~50 days into onboarding |

**Validation Summary:** MALI entered onboarding Jan 6, 2026 (~50 days ago). Only 7 MixPanel events from 3 users. No Fathom calls or HelpScout tickets in last 30 days. Activity is low but client is still early in onboarding lifecycle.

---

## KRB

**V11 Assessment:** Stage ❓ | ❓% Ready | Products: eCat
**HubSpot Lifecycle:** ❓ Not found in HubSpot under "KRB"
**MixPanel Activity:** 264 total events, 8 unique users, 0 orders, 0 iPad orders

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 2 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 3 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 4 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 5 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 6 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 7 | 🔴 | **0 iPad orders** (MixPanel), 0 orders submitted - confirmed via BigQuery |

🎯 **V11 Next Action:** ❓ Cannot determine - eCat config data unavailable. KRB has 264 MixPanel events (all api_access) from 8 users, indicating active API integration.

⚠️ **Validation Flags (1)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | ⚠️ REVIEW | HubSpot | KRB not found in HubSpot. Cannot determine lifecycle stage or onboarding status. |

**Validation Summary:** KRB has moderate MixPanel activity (264 events, 8 unique users) but all events are api_access. Not found in HubSpot under "KRB" name. No Fathom calls or HelpScout tickets in last 30 days.

---

## DCCL (Donald Choi Canada)

**V11 Assessment:** Stage ❓ | ❓% Ready | Products: eCat Online
**HubSpot Lifecycle:** Customer | Domain: donaldchoi.com
**MixPanel Activity:** 1,313 total events, 18 unique users, 0 orders, 0 iPad orders

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 2 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 3 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 4 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 5 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 6 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 8 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied (mobile_sites) |

🎯 **V11 Next Action:** Resolve server caching issues on eCat Online taxonomy - active support tickets pending

⚠️ **Validation Flags (2)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| 8 | ⚠️ REVIEW | HelpScout #13785, #13792, #13794 (Jan 8) | Server cache issue: "eCat Online not updating trade names and collections" - taxonomy changes not reflecting on public site |
| 9 | ⚠️ REVIEW | HelpScout #14027 (Feb 20) | User enrollment question: "Can you filter out inventory records based on whatever SKUs you have?" - onboarding active |

**Additional HelpScout Context (Jan-Feb 2026):**

- **Jan 8 (#13785):** "Over the last two days I have been testing many changes to our tradenames, collections, groups, and categories... these changes do appear to be handled correctly within the admin console but they are not being reflected on eCat Online"
- **Jan 8 (#13792):** Server cache issue recurring: "The server cache thing may be happening now"
- **Jan 8 (#13794):** Ongoing cache investigation with Chuck
- **Jan 13 (#13823):** eCat Online settings discussion - drill-down navigation feature request for public site
- **Jan 19 (#13850):** Image upload completed successfully, Universal Furniture data integration progressing
- **Feb 20 (#14027):** User enrollment process question - actively onboarding new users

**Validation Summary:** DCCL is the most actively engaged client of the 7. Significant HelpScout activity across both Support and Onboarding mailboxes. Primary technical issue is server caching affecting eCat Online taxonomy updates. Chris Lutka (donaldchoi.com) is the primary contact, working with Chuck. 1,313 MixPanel events from 18 users indicates strong platform adoption. HubSpot shows "Customer" lifecycle (not "Onboarding").

---

## CST (Coaster Fine Furniture)

**V11 Assessment:** Stage ❓ | ❓% Ready | Products: eCat
**HubSpot Lifecycle:** Onboarding (evangelist) since Dec 5, 2025 | Domain: coasterfurniture.com
**MixPanel Activity:** 364 total events, 49 unique users, 0 orders, 0 iPad orders
**Note:** Coasteramer (coasteramer.com) also in Onboarding since Dec 5, 2025 - related entity

| Stage | Status | Evidence |
| --- | --- | --- |
| 1 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 2 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 3 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 4 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 5 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 6 | ❓ | ❓ **Cannot determine** - PostgreSQL MCP permission denied |
| 7 | 🔴 | **0 iPad orders** (MixPanel), 0 orders submitted - but 49 unique users indicates large user base, confirmed via BigQuery |

🎯 **V11 Next Action:** ❓ Cannot determine specific stage blocker - eCat configuration data unavailable. CST has 49 unique users which is significant for onboarding.

⚠️ **Validation Flags (1)**

| Stage | Flag | Source | Evidence |
| --- | --- | --- | --- |
| - | ⚠️ ACTIVITY | Fathom + HelpScout | 0 Fathom calls in 30 days, 0 HelpScout tickets in 30 days - but 49 unique MixPanel users suggests active engagement |

**Validation Summary:** CST entered onboarding Dec 5, 2025 (~82 days ago). Highest unique user count of all 7 clients (49 users), indicating significant organizational adoption. 364 MixPanel events (all api_access). Coasteramer is a related entity also in onboarding. No Fathom calls or HelpScout tickets in last 30 days despite high user count.

---

## Validation Flags Summary

### 🔴 Critical Flags (Require Immediate Action)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| PEBL | - | Zero activity (30 days) | 0 Fathom + 0 HelpScout + minimal MixPanel | Confirm engagement |
| HVUSA | - | Zero activity (30 days) | 0 Fathom + 0 HelpScout + 5 MixPanel events | Confirm engagement |
| TCD | - | Zero activity (30 days) | 0 Fathom + 0 HelpScout, entered onboarding Dec 30 | Confirm engagement |
| ALL | - | **eCat config data unavailable** | PostgreSQL `crunchy_reader` lacks SELECT permissions | **Engineering fix required** |

### ⚠️ Review Flags (Need Clarification)

| Client | Stage | Issue | Evidence | Action |
| --- | --- | --- | --- | --- |
| MALI | - | Low activity for onboarding client | 7 events, 0 calls, 0 tickets in 30 days | Track follow-up |
| KRB | - | Not found in HubSpot | Cannot determine lifecycle stage | CSM clarification required |
| DCCL | 8 | eCat Online caching | Server cache affecting taxonomy updates | Monitor resolution |
| DCCL | 9 | User enrollment process | Active onboarding, user access questions | Track follow-up |
| CST | - | No calls/tickets despite 49 users | High user count but no support engagement | Confirm current status |

### ✅ Confirmed (No Flags)

| Client | Stage | Readiness | Status |
| --- | --- | --- | --- |
| - | - | - | No clients can be confirmed due to missing eCat configuration data |

---

## ⚠️ ENGINEERING ACTION REQUIRED

**The following must be resolved before a complete assessment can be produced:**

The PostgreSQL MCP connection (`user-supercat-postgres-vpn`) connects as user `crunchy_reader` to the `supercatprod` database but lacks SELECT permissions on all application tables.

**Fix (one-time, run by DBA):**
```sql
GRANT SELECT ON ALL TABLES IN SCHEMA public TO crunchy_reader;
```

**Tables needed:**
organizations, products, customers, org_users, users, price_levels, categories, collections, options, territories, import_events, inventories, mobile_sites, ipad_reports, orders, user_types

**Once fixed, re-run this assessment to populate all ❓ fields with actual configuration data.**
