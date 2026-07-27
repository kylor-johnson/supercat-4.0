# June 10, 2026 — Onboarding Phase Assessment

## Where everyone is

| Client | Phase (of 7) | Working on | Days in onboarding | Integration | One thing to resolve |
|---|---|---|---|---|---|
| The Coppersmith (tcs) | 3 — Building the catalog | Catalog ready | 51 | Them (Certified) | Load the customer list |
| Lib & Co. (libco) | 3 — Building the catalog | Catalog ready | 79 | Us (Managed) | Customer file is being rejected on price codes |
| Pebl / Skyard (pebl) | 3 — Building the catalog | Catalog ready | ~321 | — | Load the customer list |
| Dorell Fabrics (drf) | 4 — Catalog ready | Reps using the iPad | 56 | — | Set up rep logins (only admins are on it so far) |

All four are still mid-onboarding; none have gone live. Three of the four are stuck at the same gate: the catalog is built, but no customers are loaded yet. Dorell Fabrics is the furthest along — its catalog and customers are in, and the next step is getting reps onto the iPad.

## Standup agenda

### 🔴 Resolve this week

- **Lib & Co. — the customer file is bouncing on price codes.** Every customer row points at a price code (`cad-wsp`, `us-wsp`) that isn't set up as a price list in Admin, so the whole file is being rejected and zero customers have loaded. Fix the price codes in the file or create the matching price lists, then re-import. (Also worth a quick decision: we sold them a managed integration but aren't tracking its status anywhere — see their section.)
- **The Coppersmith — no customer list loaded yet.** Catalog looks great (271 products, 94% with photos), but the customer file hasn't been imported, which is the one thing holding them at this step. (The client is also reviewing finish options and flagged a missing "CLEAR" finish — see their section.)
- **Pebl — no customer list loaded yet, and every order so far is an internal test.** Catalog is built (656 products, 79% with photos) but no customers are in, and all 16 orders placed to date are test orders, not real customer orders.

### ⚠️ Discuss / decide

None as a standalone item this week. The two open judgment calls — Lib & Co.'s integration ownership tracking and The Coppersmith's configurator finish review — belong to clients already in the Resolve list above, so they're captured in those clients' sections rather than repeated here.

### ✅ On track (nothing blocking)

- **Dorell Fabrics — catalog and customers are in; next is rep logins.** 389 customers loaded and every one is matched to a price list. They run a single net price (confirmed intentional) and carry no product options (by design for a fabric catalog), so neither of those is a problem. They've even placed one real customer order already. The only thing left before reps can use it is setting up rep user accounts — right now only admins are on the account.

---

## The Coppersmith (tcs)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding 51 days** · Talking regularly (email plus a recent technical call)

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off Apr 21; regular calls since. |
| 2 · First import | 🟢 | 271 products loaded with no blocking errors. |
| 3 · Building the catalog | 🟢 | Products, options, option groups and stories all imported clean; 94% of products have a photo. |
| 4 · Catalog ready | 🟡 | Blocked — no customer list has been loaded yet. |
| 5 · Reps using the iPad | ⚪ | No rep user accounts yet; only admins are on the account. |
| 6 · Admin trained | ⚪ | Not started. |
| 7 · Live | ⚪ | Not started. |

Status key: 🟢 done · 🟡 in progress / partial · ⚪ not started.

(The Coppersmith is building their own data integration and we certify it — not a SuperCat build, so there's no integration workstream for us to track here.)

### Next step
Import the customer list. The catalog is otherwise ready, so loading customers is the single thing that moves them to the next step.

### Things to flag (2)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No customers loaded yet | Database | 0 customers; no customer import has been attempted. |
| 3/4 | Client flagged a missing finish in the configurator | Help Scout #14520 (Jun 9) | "FIN001, the copper finish set, is missing CLEAR." |

The configurator note is most likely routine setup collaboration (the client is reviewing finishes against their own SKU logic), but it's a "client doesn't see what they expected" signal, so it's worth a quick confirm rather than assuming.

### Recent activity
- **Meetings:** 3 in last 90 days — last was "SuperCat / Coppersmith: Technical Q&A" on May 14.
- **Support:** 26 email threads (1 still open) — last reply Jun 9.
- **Imports:** Products, options, option groups and stories all loaded in the last week; customers not yet.

### Bottom line
The Coppersmith's catalog is in good shape and they're engaged. They're held at "building the catalog" only because no customers are loaded. Get the customer file in and confirm the finish question, and they advance cleanly.

---

## Lib & Co. (libco)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding 79 days** · Talking very regularly (active email and weekly calls)

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off May 22; weekly calls since. |
| 2 · First import | 🟢 | 907 products loaded with no blocking errors. |
| 3 · Building the catalog | 🟢 | Products and inventory in; 88% of products have a photo; four price lists set up. |
| 4 · Catalog ready | 🟡 | Blocked — the customer file is being rejected on price codes, so no customers loaded. |
| 5 · Reps using the iPad | ⚪ | Two rep groups ("US Reps", "Canadian Reps") exist but have no reps in them yet. |
| 6 · Admin trained | ⚪ | Not started. |
| 7 · Live | ⚪ | Not started. |
| Integration | 🟡 | We own this build (Managed Integration), but its status isn't recorded anywhere yet. |

Status key: 🟢 done · 🟡 in progress / partial · ⚪ not started.

### Next step
Fix the customer file's price codes (or create the matching price lists in Admin) and re-import — that's what's blocking customers from loading. In parallel, record who's driving the integration and where it stands.

### Things to flag (4)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | Customer import is failing on price codes | Import log (May 28) | "Default price code 'cad-wsp' must be a valid price level code" |
| 5 | Rep groups exist but are empty | Database | "US Reps" and "Canadian Reps" groups created, but no reps assigned to either. |
| Integration | We own the integration but aren't tracking it | HubSpot deal + database | Deal includes "Managed Integration Build" and "Managed Integration Hosting", but no status is recorded for it. |
| 4 | No product options | Database | 0 options and 0 option groups — confirmed by-design (lighting sold per item). |

### Recent activity
- **Meetings:** ~8 in last 90 days — last was "Lib&CO Ecat" on Jun 9, with an integration planning call Jun 4.
- **Support:** 30 email threads (16 from the client, 2 still open) — last reply Jun 10.
- **Imports:** Products and inventory loaded recently; the customer file has been attempted but rejected.

### Bottom line
Lib & Co. is active and close on the catalog, but the customer file is bouncing because its price codes don't match the price lists in Admin — that's the real reason "no customers" shows up, and it's the thing to fix this week. Separately, this is a managed-integration client (their backend is Microsoft Business Central, with their partner "Truly" in the mix); we should record who's driving that build and its status so it stops looking unowned.

---

## Pebl / Skyard (pebl)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding ~321 days** · Very active by email (no recent meetings) · provisioned July 2025; project active again this year

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Long-running project; heavy email history. |
| 2 · First import | 🟢 | 656 products loaded with no blocking errors. |
| 3 · Building the catalog | 🟢 | Products and options in; 79% of products have a photo; two price lists set up. |
| 4 · Catalog ready | 🟡 | Blocked — no customer list has been loaded yet. |
| 5 · Reps using the iPad | 🟡 | Five client users are logging in, but all sit in the default group, not a real rep group. |
| 6 · Admin trained | ⚪ | Not started. |
| 7 · Live | ⚪ | Not started. |

Status key: 🟢 done · 🟡 in progress / partial · ⚪ not started.

(No SuperCat-owned integration — self-serve file uploads, so there's no integration workstream to track here.)

### Next step
Import the customer list. Until customers are in, the iPad can't be used for real orders — which is why all the order activity so far is internal testing.

### Things to flag (5)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | No customers loaded yet | Database | 0 customers; no customer import has been attempted. |
| 4 | Same product warnings keep repeating | Import log (last 8 product imports, through Jun 10) | "Custom field 'Certification' is missing." — appears on every recent import. Decide: register the custom fields, drop them from the file, or accept the warning. |
| 5 | Orders so far are all internal tests | Database | 16 submitted orders, none tied to a real customer (e.g. "Pebl", "Test"). |
| 5 | Test orders placed under an admin login | Database | 6 orders billed to "Test", submitted by an admin (kylor22johnson@gmail.com) — confirms these are self-tests, not customer orders. |
| 5 | Reps logging in but not in a real group | Database | 5 non-admin users active, all still in the default group — no rep group created yet. |

### Recent activity
- **Meetings:** 0 in last 90 days — engagement is entirely by email.
- **Support:** 52 email threads (30 from the client, 0 still open) — last reply Jun 9.
- **Imports:** Products and options loaded repeatedly (most recently Jun 10), with recurring custom-field warnings; customers not yet.

### Bottom line
Pebl's catalog is built and they're clearly exercising the app — but every order to date is a self-test, and no real customers are loaded. The unblock is importing the customer file. While there, decide what to do about the repeating custom-field warnings and move the active users into a real rep group.

---

## Dorell Fabrics (drf)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 56 days** · Quiet for ~3 weeks (last touch mid-May)

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off mid-April; several working sessions through May. |
| 2 · First import | 🟢 | 1,676 products loaded with no blocking errors. |
| 3 · Building the catalog | 🟢 | Products clean; 73% of products have a photo; single net price (confirmed intentional). |
| 4 · Catalog ready | 🟢 | 389 customers loaded and every one is matched to a price list; catalog is buildable. |
| 5 · Reps using the iPad | ⚪ | No rep user accounts yet; only admins are on the account. |
| 6 · Admin trained | ⚪ | Not started. |
| 7 · Live | ⚪ | Not started. |

Status key: 🟢 done · 🟡 in progress / partial · ⚪ not started.

(No SuperCat-owned integration — self-serve file uploads, so there's no integration workstream to track here.)

### Next step
Set up rep user accounts and invite the reps. The catalog and customers are ready; reps logging in is the next milestone.

### Things to flag (2)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 3 | Single net price | Database + confirmed override | One price list, confirmed intentional for this fabric catalog — not a problem. |
| 4 | No product options | Database | 0 options and 0 option groups — confirmed by-design (fabric sold per item). |

Out of the usual order: a real customer order ("AMALFI") has already been placed even though reps aren't set up yet — a go-live-stage signal showing up early. Worth noting, not a blocker.

### Recent activity
- **Meetings:** 6 in last 90 days — last was "SuperCat / Dorell: Implementation Check-In" on May 18.
- **Support:** 9 email threads (1 from the client, 0 open) — last reply May 5.
- **Imports:** Products refreshed Jun 9; customers loaded in late April.

### Bottom line
Dorell Fabrics is the furthest along — catalog and customers are both in and fully priced, and they've already placed a real order. The only thing between them and reps using the iPad is creating rep logins. They've also gone quiet for about three weeks, so a check-in to keep momentum (and to start rep setup) is the move.

---

## Appendix: run metadata & framework feedback

*Framework v3.4 · run date 2026-06-10 · all metrics from live Postgres (eCat), BigQuery (Fathom/Help Scout), and HubSpot tool calls.*

### Cohort
Auto-detected from `organizations.status = 'onboarding'` (with demo/test exclusions): `tcs`, `drf`, `libco`, `pebl` — the same 4 as the prior run. TCD and MALI remain `active` and correctly out of the cohort.

### Resolution / override notes
- **Resolved domains** (used for all Fathom / Help Scout / rep matching): tcs → `thecoppersmith.net`, drf → `dorellfabrics.com`, libco → `libandco.com`, pebl → `peblfurniture.com`.
- pebl resolved from its order-email recipient (`info@peblfurniture.com`); the other three resolved from their HubSpot company primary domain.
- **drf: single net price** confirmed intentional (`overrides.yml § net_price_only_confirmed`) — so the single-price flag was suppressed and Phase 3's price requirement is satisfied.
- **Integration ownership** (from HubSpot deal line items): libco = **us** (Managed Integration Build + Hosting); tcs = **them** (Certified Pipeline); drf and pebl = none (self-serve, integration block suppressed).

### Framework feedback (for the maintainer)
1. **`client_domains[]` resolution now lands on HubSpot (source 3), not the admin-email fallback — and this quietly suppresses the multi-domain flag the v3.1 caveats expected for DRF.** DRF's admin emails contain both `dorellfabrics.com` and `loomcraft.com`, which under the old fallback path would have raised `MULTI_DOMAIN_FALLBACK_UNVERIFIED`. But HubSpot has a "Dorell Fabrics" company with primary domain `dorellfabrics.com`, and source 3 wins before the fallback ever runs — so the flag does **not** fire this run. This is arguably correct (cleaner result), but it's a behavior change from the documented caveat, and it means the legitimate parent/DBA `loomcraft.com` is now *invisible* to the run. It happens to be harmless here because every DRF Fathom that tags `loomcraft.com` also tags `dorellfabrics.com` (verified: the May 5 and May 18 meetings carry both), so nothing is lost. But a future DRF meeting tagged **only** `loomcraft.com` would be silently missed. Suggest the framework explicitly note that source-3 resolution can mask a real second domain, and consider folding `loomcraft.com` into `overrides.yml § client_domains` for DRF so both are always matched. The "Data Files" Fathom (Apr 15) confirms verbatim: "Loomcraft Textiles, DBA Dorrell Fabrics."
2. **The import-events SQL primitive in `RUN_PROMPT.md § Step 1` still does not run as-written against the Postgres MCP tool.** The v3.4 `file_types` CTE + `CROSS JOIN` form was rejected with an opaque "Error validating query" (same failure the v3.3 `CROSS JOIN LATERAL (VALUES …)` form hit). The tool also rejected a precomputed-pattern CTE variant. What worked was a plain per-file-type `UNION ALL` of six `… ORDER BY created_at DESC LIMIT 1` subqueries per org (no CTE, no window function, no `CROSS JOIN`). The validator appears to reject `CROSS JOIN` and/or windowed CTEs, not the `- - <FileType>` literal (a single-org query containing that literal ran fine). Recommend replacing the primitive with the `UNION ALL` form, which is portable and ran first try.
3. **`CUSTOMER_IMPORT_PRICE_CODE_MISMATCH` (new in v3.4) fired exactly as designed on LIBCO** — the customer file's `cad-wsp`/`us-wsp` codes don't match any Admin price level, the import errored row-by-row, and zero customers loaded. This correctly replaced the generic "no customers" flag and names the actual cause. Good addition; no change needed.
4. **The Phase 7 clause-3 allowlist (real-customer match) worked cleanly on both DRF and PEBL.** DRF's lone order ("AMALFI") matched a real customer row, so it counts as a real order (surfaced as an out-of-order note since reps/Phase 5 aren't done). PEBL's 16 orders matched no customer (it has 0), so clause 3 correctly didn't fire and the self-test flags carried it instead. The structural coupling to `customers > 0` behaved as intended.
5. **Minor:** `customers` has no `company_name` column — the real column is `name`. The handoff's Phase 7 clause-3 description references `customers.company_name`; the live column is `customers.name`. Worth correcting so the next agent doesn't hit the same failed query.

### Flag-reference map (plain title → internal code)
| Plain-English issue title | Internal flag code |
|---|---|
| No customers loaded yet | `PHASE_4_VACUOUS_NO_CUSTOMERS` |
| Customer import is failing on price codes | `CUSTOMER_IMPORT_PRICE_CODE_MISMATCH` |
| Client flagged a missing finish in the configurator | `IMPORT_VS_HELPSCOUT_DRIFT` |
| Same product warnings keep repeating | `RECURRING_WARNINGS_NO_ERROR` |
| Orders so far are all internal tests | `SELF_TEST_ONLY_ORDERS` |
| Test orders placed under an admin login | `SELF_TEST_SUSPECTED_NOT_CUSTOMER` |
| Reps logging in but not in a real group | `REPS_IN_DEFAULT_GROUP` |
| Rep groups exist but are empty | `USER_TYPES_EMPTY` |
| No product options | `OPTIONS_INTENTIONALLY_EMPTY` |
| Single net price | `SINGLE_PRICE_LEVEL_UNCONFIRMED` (suppressed — confirmed by-design) |
| We own the integration but aren't tracking it | `INTEGRATION_OWNER_UNCLEAR` |
