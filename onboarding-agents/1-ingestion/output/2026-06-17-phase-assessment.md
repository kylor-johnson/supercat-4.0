# June 17, 2026 — Onboarding Phase Assessment

## Where everyone is

| Client | Phase (of 7) | Working on | Days in onboarding | Integration | One thing to resolve |
|---|---|---|---|---|---|
| TCS (The Coppersmith) | 3 — Building the catalog | Catalog ready | 58 | Them (Certified) | Import the customer file |
| PEBL (Skyard furniture / Pebl) | 3 — Building the catalog | Catalog ready | ~328 | — | Import customers |
| DRF (Dorell Fabrics) | 4 — Catalog ready | Reps using the iPad | 63 | — | Set up rep user groups |
| LIBCO (Lib and Co.) | 4 — Catalog ready | Reps using the iPad | 86 | Us (Managed) | Add reps to user groups before Lightovation |

## Standup agenda

### 🔴 Resolve this week

- **Lib and Co. — add reps to the user groups before Lightovation (June 22).** The catalog is complete, customers are loaded, and the rep training invite is out for Thursday — but the Canadian Reps and US Reps groups are still empty. Reps must be added and the Business Central integration permissions sorted before market.
- **The Coppersmith — import the customer file.** The catalog (424 products, 97% with images), options (366 options across 863 groups), and image mapping are in great shape after yesterday's working session. Jillian is preparing the customer list and six beta rep groups are ready to test mid-next week.
- **Pebl — import customers.** The catalog (687 products, 96% with images) and options (135 options, 356 groups) are solid. The team is actively importing and testing — but with zero customers loaded, the catalog can't be marked ready.

### ⚠️ Discuss / decide

*(None this week.)*

### ✅ On track (nothing to resolve)

- **Dorell Fabrics** — catalog is complete (1,676 products, 84% with images, every customer matched to a price list). Uses single net pricing (confirmed as intentional). No product options (by design). Needs rep user groups and an order email destination set up next.

---

## TCS (The Coppersmith)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding 58 days** · Talking weekly, data moving fast

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off April 21 with Jon, Kylor, and the Coppersmith team. |
| 2 · First import | 🟢 | Products imported clean — 424 active products, warnings only (missing UPC values). |
| 3 · Building the catalog | 🟢 | Three file types imported today (products, options, option groups), 97% image coverage, two price levels (MAP and MSRP). |
| 4 · Catalog ready | ⚪ | No customers loaded yet — that is the one thing blocking this step. |
| 5 · Reps using the iPad | ⚪ | No rep user groups defined and no reps invited. |
| 6 · Admin trained | ⚪ | No handoff to support yet. Order email not set. |
| 7 · Live | ⚪ | Not yet. |

*Client is building their own integration with Odoo (Certified Pipeline); we certify it when ready.*

### Next step

Import the customer file — Jillian is preparing the updated list with six beta rep groups and territory codes for mid-next week.

### Things to flag (1)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No customers loaded yet | Database | 0 customers in the system — the customer file hasn't been imported. |

Only 30% of products are visible on the iPad (129 of 424). The remaining 295 are marked hidden — this appears intentional based on the conversation about product type filtering, but worth confirming.

### Recent activity
- **Meetings:** 5 in the last 90 days — last was "The Coppersmith + SuperCat: Onboarding Check-In" on June 16
- **Support:** 47 email threads, 1 still open — last reply June 16
- **Imports:** Products, options, and option groups all imported today (June 17)

### Bottom line

The Coppersmith's catalog build is moving fast — options and images are in excellent shape, and the team is engaged with weekly calls. The single missing piece is the customer file, which Jillian is preparing. Once customers are in and beta reps are invited (expected mid-next week), this client will jump from Phase 3 straight to Phase 5 testing.

---

## PEBL (Skyard furniture Co Ltd.)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding ~328 days** since the account was created (project kicked off January 2026) · Active over email, no recent calls — team managing their own imports

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Project started January 2026 via HelpScout (ticket 13879). |
| 2 · First import | 🟢 | Products imported clean — 687 active products, warnings only (custom field names not registered). |
| 3 · Building the catalog | 🟢 | Products, options, and option groups all imported today, 96% image coverage, seven price levels configured. |
| 4 · Catalog ready | ⚪ | No customers loaded — customer file has never been imported. |
| 5 · Reps using the iPad | ⚪ | Seven non-admin users are actively logging in (arne, sales01, sales06, sales13, sales15, tomdewulf, vincent) — but all are in the default group, not a custom rep group. |
| 6 · Admin trained | ⚪ | Order email is set (info@peblfurniture.com), and a Zebra Group user type exists. No handoff to support yet. |
| 7 · Live | ⚪ | Not yet. |

### Next step

Import customers — the catalog and options are solid, and the team is actively testing. A customer file with bill-to/ship-to data and DefaultPriceCode values is the gap.

### Things to flag (4)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No customers loaded yet | Database | 0 customers — customer file has never been imported. |
| 3 | Custom field warnings on every product import | Database | Every product import shows the same warnings: custom fields Certification, Color, PackingSize, Materials1, and FrameColor are not registered. This has appeared on at least 6 consecutive imports. |
| 5 | Users logging in from the default group | Database | 7 non-admin users are actively logging in but are all in the default user group, not a custom rep group. The Zebra Group exists but has no users in it. |
| 5 | All orders are self-tests | Database | 22 submitted orders — all bill-to names are "Pebl," "Test," or "dsbs." None match a customer record (0 customers exist). |

SPOGA starts June 22 — Mandy confirmed the team is still preparing. The catalog is being used as a trade-show tool even without a customer file imported.

### Recent activity
- **Meetings:** None in the last 90 days
- **Support:** 56 email threads, 2 still open (1 active) — last reply today (June 17)
- **Imports:** Products, options, and option groups imported multiple times today

### Bottom line

Pebl's team is impressively self-sufficient — Mandy and the sales reps are actively importing, configuring options, and testing the iPad ahead of the SPOGA fair next week. The catalog and options are in great shape. The main gap is the customer file: once customers are loaded and users moved from the default group into the Zebra Group (or a new rep group), this client will be much closer to a production setup. The recurring custom-field warnings should be cleaned up — either register the fields or remove them from the file.

---

## DRF (Dorell Fabrics)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 63 days** · Quiet since late May — check-in email sent today

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off April 15 with Jon and Suzanne. |
| 2 · First import | 🟢 | Products imported clean — 1,676 active products, no errors. |
| 3 · Building the catalog | 🟢 | Two file types imported in the last 60 days (products and customers), 84% image coverage (1,404 of 1,676), single net price (confirmed as intentional). |
| 4 · Catalog ready | 🟢 | All 389 customers matched to the net price list. No product options (by design — per-SKU fabric catalog). Latest products import is clean. One real customer order exists (bill-to "AMALFI" matches a customer record). |
| 5 · Reps using the iPad | ⚪ | No rep user groups exist — everyone is in the default group. No reps defined. |
| 6 · Admin trained | ⚪ | Order email not set. Only one user group (default). No handoff to support. |
| 7 · Live | ⚪ | Not yet. |

### Next step

Set up rep user groups — Kylor's check-in email today asked about target timeline, rep list (names, emails, territory codes), and where submitted orders should land.

### Things to flag (1)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 3/4 | No product options — by design | Database | 0 options and 0 option groups. This is expected for Dorell's per-SKU fabric catalog model. |

### Recent activity
- **Meetings:** 5 in the last 90 days — last was "SuperCat / Dorell: Implementation Check-In" on May 18
- **Support:** 10 email threads, 1 pending — last reply today (June 17)
- **Imports:** Products imported multiple times in early-to-mid June

### Bottom line

Dorell's catalog is in great shape — 1,676 products, solid image coverage, all customers matched to pricing, and clean imports. The product side is done. What's missing is entirely operational: rep user groups, an order email destination, and getting reps invited to the iPad. Kylor sent a status check-in today to get the ball rolling on that next step. No urgency flag, but the gap between catalog readiness and rep setup has been open for a few weeks.

---

## LIBCO (Lib and Co.)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 86 days** · Meeting weekly, integration build in progress

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off May 22 with Jon, Kjael, and Silvio. |
| 2 · First import | 🟢 | Products imported clean — 872 active products, warnings only (missing UPC for one SKU). |
| 3 · Building the catalog | 🟢 | Four file types imported June 15 (products, customers, inventory, stories), 92% image coverage (802 of 872), four price levels (US and Canadian wholesale plus IMAP). |
| 4 · Catalog ready | 🟢 | 263 customers loaded, all matched to price lists (188 US wholesale, 75 Canadian). Customer import has one error row (customer name too long, line 29). No product options (by design — lighting model). Latest products import is clean. |
| 5 · Reps using the iPad | ⚪ | Two rep groups defined (US Reps and Canadian Reps) but both are empty — no reps have been added yet. |
| 6 · Admin trained | ⚪ | Order email not set. User groups exist (≥2) but no handoff to support. |
| 7 · Live | ⚪ | Not yet. |
| Integration | 🟡 | We own the Business Central integration (Managed Integration Build + Hosting). API permissions are stalled — Azure OAuth is working but Business Central application permissions need Silvio to grant consent. Brent is driving the technical setup with Ernest (Truly SMB). |

### Next step

Add reps to the Canadian Reps and US Reps groups — Silvio sent the rep list and training invite for Thursday. Lightovation is June 22.

### Things to flag (3)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 5 | Rep groups built but empty | Database | US Reps and Canadian Reps user groups exist but have zero users. Silvio sent the rep list June 15. |
| 3/4 | No product options — by design | Database | 0 options and 0 option groups. Expected for Lib and Co.'s lighting catalog. |
| Integration | Integration sold but not yet tracked | Database / HubSpot | Managed Integration Build and Managed Integration Hosting are on the deal. The build is actively in progress (Brent and Ernest working on Business Central API permissions) but the status hasn't been recorded yet. |

The most recent customer import (June 15) had one error: customer C00079's name exceeds the 60-character limit. The remaining 263 customers imported successfully. This is a data-quality fix, not a structural blocker.

### Recent activity
- **Meetings:** 5 in the last 90 days — last was "Lib&CO Ecat" on June 9
- **Support:** 52 email threads, 3 open (1 active) — last reply today (June 17)
- **Imports:** Products, customers, inventory, and stories all imported June 15

### Bottom line

Lib and Co.'s catalog is complete and the customer file is loaded. The two blockers before Lightovation (June 22) are: (1) adding reps to the two empty user groups — Silvio sent the list and the training invite is out for Thursday, and (2) unblocking the Business Central integration permissions so Brent can finish the API connection. The clock is tight but the pieces are in place.

---

## Appendix

*Framework v3.4 · Run date 2026-06-17 · All metrics from live Postgres and BigQuery tool calls.*

**Overrides applied this run:**
- `drf`: listed under `net_price_only_confirmed` — single net price confirmed as intentional. Phase 3 price requirement satisfied; informational note only.
- Integration ownership from HubSpot deal line items: LIBCO = Managed Integration Build + Hosting (us); TCS = Certified Pipeline (them); DRF and PEBL = no integration line item (self-serve FTP, suppressed).
- `integration_status` in `overrides.yml` is empty — LIBCO's managed integration is not yet tracked there, so the "integration sold but not yet tracked" flag fires. Once the approach/status is recorded, the flag will stop recurring.

**Framework feedback:**
- The `import_events` CTE query from `RUN_PROMPT.md § Step 1` (using `file_types` CTE + `CROSS JOIN`) was rejected by the Postgres MCP tool with "Error validating query." Falling back to individual per-org queries with `OR`-chained `ILIKE` filters worked. The CTE syntax may need further adjustment for this tool's SQL parser.
- The `customers` table column for company name is `name`, not `company_name`. The Phase 7 clause 3 description references `customers.company_name`, but the actual Postgres column is `customers.name`. Consider updating `Phase_Anchors.md § Phase 7` to reflect the actual column name.
- DRF's customer import (April 27) is 51 days old — just barely within the 60-day window for Phase 3's "≥2 file types in 60d" clause. If next week's run happens on June 24+, that import will fall outside the window unless a new customer file is uploaded. Worth noting but not actionable this week.
- PEBL's `created_at` (July 24, 2025) is 328 days ago, but the project formally started January 2026. The framework doesn't have a "project start date" override, so `created_at` is the only computable value. The `days_qualifier` field in the JSON schema handles this gracefully.
- No clauses were found ambiguous or contradicted by live data this run. The v3.4 framework applied cleanly.

**Flag-reference map:**

| Plain-English title used above | Internal flag code |
|---|---|
| No customers loaded yet | `PHASE_4_VACUOUS_NO_CUSTOMERS` |
| No product options — by design | `OPTIONS_INTENTIONALLY_EMPTY` |
| Custom field warnings on every product import | `RECURRING_WARNINGS_NO_ERROR` |
| Users logging in from the default group | `REPS_IN_DEFAULT_GROUP` |
| All orders are self-tests | `SELF_TEST_ONLY_ORDERS` |
| Rep groups built but empty | `USER_TYPES_EMPTY` |
| Integration sold but not yet tracked | `INTEGRATION_OWNER_UNCLEAR` |
