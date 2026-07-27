# July 1, 2026 — Onboarding Phase Assessment

## Where everyone is

| Client | Phase (of 7) | Working on | Days in onboarding | Integration | One thing to resolve |
|---|---|---|---|---|---|
| Skyard (Pebl) | 3 — Building the catalog | Catalog ready | ~342 | — | Import the customer file |
| Dorell Fabrics | 4 — Catalog ready | Reps using the iPad | 77 | — | Set up rep groups and invite reps |
| The Coppersmith | 4 — Catalog ready | Reps using the iPad | 72 | Them (Certified) | Invite reps into the Rep Group |
| Lib and Co. | 5 — Reps using the iPad | Admin trained | 100 | Us (Managed) | Schedule admin training and record integration status |

## Standup agenda

### 🔴 Resolve this week

- **Skyard (Pebl) — import the customer file.** Mandy sent a customers.csv on July 1 with seven accounts and a rep lookup table. Once imported and validated, the catalog-ready gate clears and several downstream phases can be evaluated.
- **The Coppersmith — invite reps into the Rep Group.** The group exists but has zero members. Six beta rep groups were discussed on the June 16 onboarding call and are ready for access.

### ⚠️ Discuss / decide

- **Lib and Co. — record the integration status and confirm admin handoff.** SuperCat sold a Managed Integration (Business Central) but the build status isn't tracked yet. Separately, all the infrastructure for admin handoff is in place (order email set, two rep groups active, 28 reps logging in) but no formal admin training session has been captured. Confirm whether handoff happened on a call we didn't record.

### ✅ On track (nothing to resolve)

- **Dorell Fabrics** — catalog is complete (1,676 products, 84% with images, 389 customers matched to pricing). Single net price confirmed as intentional. No product options by design. Next step is setting up rep groups. Note: Christine's June 30 email mentions wanting to add 10 price levels per product — the single-net-price override may need revisiting.

---

## PEBL (Skyard Furniture Co Ltd.)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding ~342 days** since the account was created (project formally started January 2026) · Active via email, no calls scheduled

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Account created July 2025; active HelpScout correspondence since January 2026. |
| 2 · First import | 🟢 | Products imported today (July 1) — 713 products, warnings only (missing custom fields). |
| 3 · Building the catalog | 🟢 | Three file types imported in the last 60 days (products, options, option groups). 97% of products have images. Seven price levels configured. |
| 4 · Catalog ready | 🟡 | Catalog looks strong but zero customers are loaded — the customer file is the one missing piece. |
| 5 · Reps using the iPad | ⚪ | 14 reps exist in two groups (Peblers, Timmermans); 13 active in the last 30 days. Reps are already using the app ahead of the customer file. |
| 6 · Admin trained | ⚪ | Order email is set (info@peblfurniture.com). No admin training session recorded yet. |
| 7 · Live | ⚪ | Not yet. |

### Next step

Import Mandy's customer file (sent July 1), validate the DefaultPriceCode values against the seven configured price levels, and clear the catalog-ready gate.

### Things to flag (3)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No customers loaded yet | Database | 0 customers in the system. Mandy's file arrived today — needs importing. |
| 3/4 | Orders without matching customers | Database — 85 submitted orders | 85 orders exist but none match a loaded customer record (because there are none). Reps are placing what appear to be real orders (ESUN International, Ocean Import & Export, Everything Under The Sun) alongside test orders. |
| 3 | Recurring custom-field warnings on every product import | Database — products import July 1 | Custom fields Certification, Color, PackingSize, Materials1, FrameColor, MaterialColor, and CushionFabric are flagged as missing on every import. Decide: register these custom fields in Admin, remove the columns from the file, or accept the warnings. |

Reps are significantly ahead of the customer data — 13 of 14 reps logged in within the last 30 days and are actively submitting orders, even though no customer master is loaded. Once the customer file lands, Pebl could advance through Phases 4 and 5 in one assessment cycle.

### Recent activity

- **Meetings:** 0 in the last 90 days — no Fathom meetings recorded.
- **Support:** 2 tickets, 1 still open — last reply July 1 (Mandy's customer file and rep lookup table).
- **Imports:** Products imported today; options and option groups imported June 29. 229 import events in the last 30 days (mostly product and image updates).

### Bottom line

Pebl's catalog is in strong shape — 713 products, 97% image coverage, seven price levels, and 151 options across 381 groups. The single blocker is the customer file, which Mandy sent today. Once it imports cleanly, the catalog-ready gate should clear and reps (13 of 14 already active) are ready to go.

---

## DRF (Dorell Fabrics)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 77 days** · Re-engaged after a quiet stretch

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Account created April 15; six Fathom meetings and active HelpScout correspondence. |
| 2 · First import | 🟢 | Products imported June 12 — 1,676 products, clean import (no warnings or errors). |
| 3 · Building the catalog | 🟢 | Products and product stories imported in the last 60 days. 84% of products have images (1,404 of 1,676). Single net price confirmed as intentional. |
| 4 · Catalog ready | 🟢 | All 389 customers matched to the net price level (100% DefaultPriceCode resolution). No product options by design (per-SKU fabric catalog). |
| 5 · Reps using the iPad | ⚪ | Only the DefaultUserGroup exists — no custom rep groups have been created yet and no reps are set up. |
| 6 · Admin trained | ⚪ | Order email is not set. Three iPad report templates exist. |
| 7 · Live | ⚪ | Not yet. |

### Next step

Create custom rep groups in Admin, invite sales reps, and set the order email address.

### Things to flag (1)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No product options — by design | Database | 0 options and 0 option groups. Dorell is a per-SKU fabric catalog; options are not part of their model. |

Christine's June 30 email says they want to add 10 price levels per product. This may mean the single-net-price override needs revisiting — if they're building out a multi-tier price list, the override should be removed and additional price levels configured before the customer file is updated.

### Recent activity

- **Meetings:** 6 in the last 90 days — last was "SuperCat / Dorell: Implementation Check-In" on May 18.
- **Support:** 2 tickets, 2 still open — last reply June 30 (Kyla forwarded Christine's email about pricing).
- **Imports:** Products and stories imported in June. 91 import events in the last 30 days (mostly image updates).

### Bottom line

Dorell's catalog is complete and all customers are matched to pricing. The next step is creating rep groups and inviting sales reps — something Christine and Suzanne need to drive from their side. The potential shift from single net price to 10 price levels is worth confirming before proceeding.

---

## TCS (The Coppersmith)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 72 days** · Talking regularly (calls and email)

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Account created April 20; five Fathom meetings and active HelpScout correspondence. |
| 2 · First import | 🟢 | Products imported June 30 — 396 products with warnings only (unknown field names like Feature1–Feature6). |
| 3 · Building the catalog | 🟢 | Five file types imported in the last 60 days (products, customers, options, option groups, product stories). Nearly 100% image coverage (395 of 396). Two price levels (MAP, MSRP). |
| 4 · Catalog ready | 🟢 | 720 customers loaded with 100% DefaultPriceCode resolution. 367 options across 324 groups. Most recent customer import had one error row (invalid buyer email on line 231) but 720 customers loaded successfully. |
| 5 · Reps using the iPad | ⚪ | "Rep Group" exists but has zero members — the group was created but no reps have been invited yet. |
| 6 · Admin trained | ⚪ | Order email is not set. One iPad report template exists. |
| 7 · Live | ⚪ | Not yet. |

*Integration: The Coppersmith has a Certified Pipeline (Odoo) — they are building their own integration; we certify it.*

### Next step

Invite the six beta reps (discussed on the June 16 onboarding call) into the Rep Group so they can start testing the iPad.

### Things to flag (1)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 5 | Rep Group exists but has no members | Database | The "Rep Group" user type was created but has 0 users assigned. Jillian was to send the list of six beta reps — check if that's been received. |

Only 130 of 396 products are visible (the rest are hidden via the Hideable flag) — this is intentional product staging, not a data issue.

### Recent activity

- **Meetings:** 5 in the last 90 days — last was "The Coppersmith + SuperCat: Onboarding Check-In" on June 16.
- **Support:** 4 tickets, 2 still open — last reply June 30 (clarification on option group changes).
- **Imports:** All five core file types imported in the last 30 days. 217 import events in the last 30 days (heavy image and data iteration).

### Bottom line

The Coppersmith's catalog is well-built — 396 products, near-perfect image coverage, 720 customers, and a rich options structure. The single next step is inviting reps into the empty Rep Group. An Odoo integration is being built by their team (Certified Pipeline); we certify it but don't own the build.

---

## LIBCO (Lib and Co.)

**Phase 5 of 7 — Reps using the iPad** · working on **Admin trained** · eCat iPad
**In onboarding 100 days** · Highly active — daily email and regular calls

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Account created March 23; twelve Fathom meetings and very active HelpScout correspondence (118 threads in the last 30 days). |
| 2 · First import | 🟢 | Products imported June 22 — 872 products with warnings only (related items not found, missing UPC). |
| 3 · Building the catalog | 🟢 | Four file types imported in the last 60 days (products, customers, inventory, product stories). 92% image coverage (802 of 872). Four price levels configured (USA wholesale, USA IMAP, CAD wholesale, CAD IMAP). |
| 4 · Catalog ready | 🟢 | 265 customers loaded with 100% DefaultPriceCode resolution. 912 inventory records. No product options by design (lighting catalog with per-SKU model). |
| 5 · Reps using the iPad | 🟢 | 55 reps across two groups (US Reps: 48, Canadian Reps: 7). 28 active in the last 30 days. Three real customer orders placed (including one matching a loaded customer — Franklin Lighting Inc.). |
| 6 · Admin trained | 🟡 | Order email is set (silvio@libandco.com). Two custom rep groups active. But no formal admin training session captured yet — Silvio has admin access and is self-configuring, but the handoff to support hasn't been formalized. |
| 7 · Live | ⚪ | Not yet. |
| Integration | 🟡 | SuperCat owns a Managed Integration with Business Central. Brent is actively working on inventory feeds; production switchover discussed June 30. Status not yet recorded. |

### Next step

Schedule a formal admin training session for Silvio and record the Business Central integration status so both items stop carrying forward.

### Things to flag (3)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 6 | Infrastructure ready but no formal handoff captured | Database + HelpScout | Order email is set, rep groups are active, 28 reps logging in — but no admin training meeting or handoff email has been recorded. Silvio may already be self-sufficient; confirm with Kyla. |
| Integration | Managed integration sold but build status not tracked | HubSpot deal — "Lib & Co - TIER 2" | The deal includes Managed Integration Build and Managed Integration Hosting. Brent is actively building the Business Central integration (inventory feed switchover to production discussed June 30) but the status isn't recorded in overrides. Record it once and this stops recurring. |
| 4 | No product options — by design | Database | 0 options and 0 option groups. Lib and Co. is a lighting catalog with a per-SKU model; options are not part of their product structure. |

Phase 7 signals are already firing out of order: 28 reps are active (clause 2) and a real customer order exists for Franklin Lighting Inc. (clause 3). Once admin training is captured, Lib and Co. could advance quickly.

### Recent activity

- **Meetings:** 12 in the last 90 days — last was "Jon Vanderberg's Zoom Meeting" on June 18 (platform issues and action plan review with Silvio).
- **Support:** 8 tickets, 3 still open — last reply July 1 (Silvio coordinating with Ernest on integration).
- **Imports:** Products, customers, inventory, and stories all imported in the last 60 days. 13 import events in the last 30 days.

### Bottom line

Lib and Co. is the most advanced onboarding client — reps are actively logging in, real customer orders are landing, and the Business Central integration is nearing production. The two items holding Phase 6 are formalizing the admin handoff (which may have already happened informally) and recording the integration build status. Both are quick to close.

---

## Appendix

*Framework v3.4 · Run date 2026-07-01 · All metrics from live Postgres and BigQuery tool calls.*

### Overrides applied

- <code>drf</code>: single net price confirmed intentional (<code>overrides.yml § net_price_only_confirmed</code>). Note: Christine's June 30 email asks about adding 10 price levels — the override may need revisiting.
- Integration ownership read from HubSpot deal line items: <code>libco</code> = Managed Integration Build + Hosting (deal "Lib & Co - TIER 2"); <code>tcs</code> = Certified Pipeline (deal "The Coppersmith - TIER 3"); <code>drf</code> and <code>pebl</code> = no integration line items (self-serve FTP).
- <code>client_domains[]</code> resolved: <code>tcs</code> → thecoppersmith.net (HubSpot), <code>drf</code> → dorellfabrics.com (HubSpot), <code>libco</code> → libandco.com (order_email), <code>pebl</code> → peblfurniture.com (order_email). No fallback needed; no <code>MULTI_DOMAIN_FALLBACK_UNVERIFIED</code> fired.

### Framework feedback

- The import-events CTE query with <code>CROSS JOIN</code> fails validation on the Postgres MCP tool (same issue as the v3.4 changelog noted for v3.3). Individual per-file-type queries using correlated subqueries work reliably. Consider updating <code>RUN_PROMPT.md</code> to document both approaches.
- DRF's <code>net_price_only_confirmed</code> override may be stale: Christine's June 30 HelpScout email explicitly asks about adding 10 price levels. If DRF moves to multi-tier pricing, the override should be removed and additional price levels configured. Recommend confirming with Kylor before the next run.
- PEBL's account was created July 2025 (~342 days ago) but the project formally started January 2026. The "days in onboarding" metric is misleading at face value. Consider adding an optional <code>project_start_date</code> override to <code>overrides.yml</code> for cases where provisioning significantly preceded kickoff.
- PEBL has 0 Fathom meetings in 90 days despite active email engagement. All interaction happens via HelpScout. The Phase 1 touchpoint detection correctly handles this (HelpScout satisfies the requirement), but it's worth noting that the meeting-centric health signals (Phase 6 qualitative triggers) may not capture engagement for email-only clients.
- LIBCO's Phase 6 qualitative trigger #4 (Kyla-presence dominance) fails because Kylor is the most recent SuperCat author (June 30, 18:10), even though non-Kylor SuperCat authors posted 27 threads in 30 days (vs Kylor's 31). The "most recent author is non-Kylor" clause is sensitive to a single late Kylor reply resetting the signal. This may be working as designed (the handoff hasn't fully happened if Kylor is still the last word), or it may be too brittle for an active shared-inbox model like LIBCO.

### Flag reference map

| Plain-English title (used above) | Internal code |
|---|---|
| No customers loaded yet | PHASE_4_VACUOUS_NO_CUSTOMERS |
| Orders without matching customers | SELF_TEST_ONLY_ORDERS |
| Recurring custom-field warnings on every product import | RECURRING_WARNINGS_NO_ERROR |
| No product options — by design | OPTIONS_INTENTIONALLY_EMPTY |
| Rep Group exists but has no members | USER_TYPES_EMPTY |
| Infrastructure ready but no formal handoff captured | INFRA_READY_NO_HANDOFF |
| Managed integration sold but build status not tracked | INTEGRATION_OWNER_UNCLEAR |
