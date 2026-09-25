# June 26, 2026 — Onboarding Phase Assessment

## Where everyone is

| Client | Phase (of 7) | Working on | Days in onboarding | Integration | One thing to resolve |
|---|---|---|---|---|---|
| PEBL (Skyard Furniture / Pebl) | 3 — Building the catalog | Catalog ready | ~337 | — | Import the customer file |
| TCS (The Coppersmith) | 4 — Catalog ready | Reps using the iPad | 67 | Them (Certified) | Create rep user groups and invite beta reps |
| DRF (Dorell Fabrics) | 4 — Catalog ready | Reps using the iPad | 72 | — | Set up rep user groups and order email |
| LIBCO (Lib and Co.) | 7 — Live | Live | 95 | Us (Managed) | Record Business Central integration status |

## Standup agenda

### 🔴 Resolve this week

- **Pebl — import the customer file.** Reps are actively logging in and submitting orders at trade shows, but zero customers are loaded — every order fails to match a real account.
- **The Coppersmith — create rep user groups and invite beta reps.** The catalog is complete (425 products, 98% with photos, 720 customers loaded), but no custom rep groups exist and nobody has logged into the iPad yet.

### ⚠️ Discuss / decide

- **Lib and Co. — record the managed integration and flip status to active.** They hit go-live criteria this week (rep training done, 27 reps active, real customer orders at market). We still aren't tracking the Business Central build in `overrides.yml`, and their org status is still `onboarding`.

### ✅ On track (nothing to resolve)

- **Dorell Fabrics** — catalog complete (1,676 products, 84% with images, 389 customers, every customer matched to the net price list). Single net price (confirmed). No product options (by design). Next step is rep user groups and an order email destination.

---

## PEBL (Skyard Furniture Co Ltd.)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding ~337 days** since the account was created (project kicked off January 2026) · Very active — reps logging in daily, heavy order volume over email

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Project started January 2026 via Help Scout (ticket 13879). |
| 2 · First import | 🟢 | Products imported clean — 713 active products, warnings only (custom field names not registered). |
| 3 · Building the catalog | 🟢 | Products, options (147), and option groups (379) all imported in the last week; 97% image coverage; six price levels configured. |
| 4 · Catalog ready | ⚪ | No customers loaded — the customer file has never been imported. |
| 5 · Reps using the iPad | 🟡 | Fourteen reps in custom groups (Peblers and Timmermans); nine logged in within the last 30 days — but with no customer accounts to sell to. |
| 6 · Admin trained | 🟡 | Order email is set (info@peblfurniture.com). Kyla is actively handling support threads post-SPOGA. No formal admin-training handoff captured. |
| 7 · Live | ⚪ | Not yet. |

### Next step

Import the customer file — reps are already submitting orders at trade shows, but without customers loaded none of those orders tie to real accounts.

### Things to flag (3)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No customers loaded yet | Database | 0 customers in the system — no customer import event exists. |
| 3 | Same warning on every product import | Database | "Line 1: Custom field 'Certification' is missing." — plus Color, PackingSize, Materials1, FrameColor, and six others. At least 67 product imports since June 1 carry the same warnings. |
| 5 | Only test orders so far | Database | 76 submitted orders — none match a customer record because no customers exist. Bill-to names include "Pebl," product-set names, and trade-show entries. |

Reps moved out of the default group into Peblers and Timmermans — that gap from last week is closed. The team is running hard at SPOGA without a customer file; Kyla updated their order email templates June 23.

### Recent activity
- **Meetings:** None in the last 90 days
- **Support:** 63 email threads, none open — last reply June 23
- **Imports:** Products imported June 23; options and option groups June 18

### Bottom line

Pebl's team is the most self-sufficient in the cohort — nine reps are actively using the iPad, custom user groups are set up, and order volume is high. The one structural gap is the customer file: until it lands, every order is orphaned and Phase 4 cannot advance. The recurring custom-field warnings should also be cleaned up (register the fields or remove them from the file).

---

## TCS (The Coppersmith)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 67 days** · Talking weekly — major data push this week

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off April 21 with Jon, Kylor, and the Coppersmith team. |
| 2 · First import | 🟢 | Products imported clean — 425 active products, warnings only (unknown Feature fields, missing UPC values). |
| 3 · Building the catalog | 🟢 | Five file types imported this week (products, customers, options, option groups, stories), 98% image coverage, two price levels (MAP and MSRP). |
| 4 · Catalog ready | 🟢 | 720 customers loaded, every customer matched to a price list. Latest products import is warning-only. One error row on today's customer re-import (invalid buyer email, line 231). |
| 5 · Reps using the iPad | ⚪ | Only the default user group exists — no custom rep groups defined and no reps have logged in. |
| 6 · Admin trained | ⚪ | Order email not set. No handoff to support. |
| 7 · Live | ⚪ | Not yet. |

*Client is building their own integration with Odoo (Certified Pipeline); we certify it when ready.*

### Next step

Create the six beta rep user groups Jillian prepared and invite reps to the iPad — the catalog side is done.

### Things to flag

*(None — operational next step is rep setup, not a triggered ambiguity flag.)*

Only 31% of products are visible on the iPad (130 of 425). The remaining 295 are marked hidden — this appears intentional based on prior conversations about product-type filtering, but worth confirming.

### Recent activity
- **Meetings:** 5 in the last 90 days — last was "The Coppersmith + SuperCat: Onboarding Check-In" on June 16
- **Support:** 62 email threads, 4 still open — last reply today (June 26)
- **Imports:** Full catalog push June 26 — products, customers, options, option groups, and stories all imported today

### Bottom line

The Coppersmith jumped two phases in one week — customers are in, options are configured, and image coverage is excellent. The catalog is ready. The entire focus now shifts to rep enablement: create the beta rep groups, set an order email destination, and get reps onto the iPad. Jillian flagged incorrect images on the Weiyan LED tab in Help Scout ticket 14520 — worth addressing before beta launch.

---

## DRF (Dorell Fabrics)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 72 days** · Quiet since mid-June — last Help Scout reply June 18

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off April 15 with Jon and Suzanne. |
| 2 · First import | 🟢 | Products imported clean — 1,676 active products, no errors. |
| 3 · Building the catalog | 🟢 | Products and customers imported, 84% image coverage (1,404 of 1,676), single net price (confirmed as intentional). |
| 4 · Catalog ready | 🟢 | All 389 customers matched to the net price list. No product options (by design). Latest products import is clean. One real customer order exists (bill-to "AMALFI" matches a customer record). |
| 5 · Reps using the iPad | ⚪ | No custom rep user groups — everyone is in the default group. No reps defined outside the default group. |
| 6 · Admin trained | ⚪ | Order email not set. Only one user group (default). No handoff to support. |
| 7 · Live | ⚪ | Not yet. |

### Next step

Set up rep user groups and an order email destination — the catalog side is complete.

### Things to flag (2)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 3/4 | No product options — by design | Database | 0 options and 0 option groups. Expected for Dorell's per-SKU fabric catalog model. |
| 1 | Second company domain needs confirmation | Database | Client domains resolved to both dorellfabrics.com and loomcraft.com via admin-email fallback. Fathom notes confirm "Loomcraft Textiles, DBA Dorrell Fabrics" — likely legitimate. |

### Recent activity
- **Meetings:** 5 in the last 90 days — last was "SuperCat / Dorell: Implementation Check-In" on May 18
- **Support:** 11 email threads, none open — last reply June 18
- **Imports:** Products imported June 12; customers last imported April 27

### Bottom line

Dorell's catalog is in great shape and has been for weeks. What's missing is entirely operational: custom rep user groups, an order email destination, and getting reps invited to the iPad. No urgency flag, but the gap between catalog readiness and rep setup has been open since late May.

---

## LIBCO (Lib and Co.)

**Phase 7 of 7 — Live** · working on **Live** · eCat iPad
**In onboarding 95 days** · Very active — rep training done, Dallas market in full swing

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off May 22 with Jon, Kjael, and Silvio. |
| 2 · First import | 🟢 | Products imported clean — 872 active products, warnings only. |
| 3 · Building the catalog | 🟢 | Products, customers, inventory, and stories all loaded; 92% image coverage; four price levels. |
| 4 · Catalog ready | 🟢 | 265 customers loaded, every customer matched to a price list. No product options (by design). |
| 5 · Reps using the iPad | 🟢 | 55 reps across US Reps and Canadian Reps groups; 27 logged in within the last 30 days. |
| 6 · Admin trained | 🟢 | Rep training session held June 18. Order email set (silvio@libandco.com). Three user groups configured. |
| 7 · Live | 🟢 | Go-live criteria met — admin trained, 27 active reps, real customer orders at market. |
| Integration | 🟡 | We own the Business Central integration (Managed Integration Build + Hosting). API permissions still being sorted — Brent and Ernest (Truly SMB) working with Silvio. |

### Next step

Record the Business Central integration status in `overrides.yml` and flip the org status to `active` so Lib and Co. exits the onboarding cohort next run.

### Things to flag (2)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| Integration | We own the integration but aren't tracking it | HubSpot deal "Lib & Co - TIER 2" | Deal includes "Managed Integration Build" + "Managed Integration Hosting" — ours to run — but no status is recorded in overrides. |
| Integration | Integration still in progress at go-live | Fathom June 18 | "Critical Blocker: The integration with Business Central is stalled" — Azure OAuth working but Business Central application permissions need Silvio to grant consent. |
| 3/4 | No product options — by design | Database | 0 options and 0 option groups. Expected for Lib and Co.'s lighting catalog. |

Real customer orders are flowing — Franklin Lighting Inc. (June 24) and others submitted by reps during Dallas market week.

### Recent activity
- **Meetings:** 9 in the last 90 days — last was "Jon Vanderberg's Zoom Meeting" on June 18
- **Support:** 101 email threads, none open — last reply June 25
- **Imports:** Products imported June 22; inventory June 19; customers June 17

### Bottom line

Lib and Co. crossed the go-live line this week. Rep training happened June 18, 27 reps are actively using the iPad at Dallas market, and real customer orders are coming through. The Business Central integration is still being built in parallel — that does not block go-live, but we need to start tracking it and flip their org status to active. This client should drop from next week's assessment.

---

## Appendix

*Framework v3.4 · Run date 2026-06-26 · All metrics from live Postgres and BigQuery tool calls.*

**Overrides applied this run:**
- `drf`: listed under `net_price_only_confirmed` — single net price confirmed as intentional.
- Integration ownership from HubSpot deal line items: LIBCO = Managed Integration Build + Hosting (us); TCS = Certified Pipeline (them); DRF and PEBL = no integration line item (self-serve FTP, suppressed).
- `integration_status` in `overrides.yml` is empty — LIBCO's managed integration is not yet tracked there.
- `drf` client domains resolved via admin-email fallback to `dorellfabrics.com` and `loomcraft.com` (meetings confirm Loomcraft as parent/DBA).

**Framework feedback:**
- The `import_events` CTE + `CROSS JOIN` query from `RUN_PROMPT.md § Step 1` was rejected again by the Postgres MCP tool ("Error validating query"). Per-file-type UNION ALL subqueries worked as a fallback — same issue reported on the June 17 run.
- `Phase_Anchors.md § Phase 7` references `customers.company_name` but the actual Postgres column is `customers.name`. The order-matching query must use `name`.
- LIBCO's Phase 7 classification is a significant jump from the June 17 run (Phase 4 then → Phase 7 now). The driver is rep training (Fathom June 18), 27 active reps, and real customer orders — all verified live. Recommend operator confirm go-live and flip `status` to `active`.
- PEBL's out-of-order signal is stronger than ever: Phase 5 rep activity (9 active in 30 days, 76 orders) while Anchor remains Phase 3 (zero customers). The framework surfaces this correctly but the standup read may surprise — reps are effectively live-testing without a customer file.
- No other clauses found ambiguous or contradicted by live data.

**Flag-reference map:**

| Plain-English title used above | Internal flag code |
|---|---|
| No customers loaded yet | `PHASE_4_VACUOUS_NO_CUSTOMERS` |
| Same warning on every product import | `RECURRING_WARNINGS_NO_ERROR` |
| Only test orders so far | `SELF_TEST_ONLY_ORDERS` |
| No product options — by design | `OPTIONS_INTENTIONALLY_EMPTY` |
| Second company domain needs confirmation | `MULTI_DOMAIN_FALLBACK_UNVERIFIED` |
| We own the integration but aren't tracking it | `INTEGRATION_OWNER_UNCLEAR` |
| Integration still in progress at go-live | `INTEGRATION_DEFERRED_POST_HANDOFF` |
