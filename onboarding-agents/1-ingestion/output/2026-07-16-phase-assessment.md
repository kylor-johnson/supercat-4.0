# July 16, 2026 — Onboarding Phase Assessment

## Where everyone is

| Client | Phase (of 7) | Working on | Days in onboarding | Integration | One thing to resolve |
|---|---|---|---|---|---|
| Legrand US | 3 — Building the catalog | Catalog ready | 401 | — | Fix the one customer's price code |
| Dorell Fabrics | 4 — Catalog ready | Reps using the iPad | 92 | — | Create rep user groups and invite the first reps |
| Lib & Co. | 7 — Live | — | 115 | Us (Managed) | Confirm go-live and flip the account to active |

## Standup agenda

### 🔴 Resolve this week

- **Dorell Fabrics — remove the outdated "single net price" setting and get the first reps invited.** The config still says DRF uses only one net price; they now have 11 price levels loaded (confirmed Jul 2). Separately, no rep user groups have been created at all — no sales rep can log into the app yet.

### ⚠️ Discuss / decide

- **Lib & Co. — Phase 7 criteria met; decide whether to flip the account to go-live now or wait for the Business Central integration.** Active reps, a real customer order placed July 10, and the full catalog are all in place. The integration is still mid-build (Brent + Ernest at TrulieSMB). Confirm whether the status flip can happen now or whether you want to hold until the integration is live.

### ✅ On track (nothing to resolve)

- **Legrand US** — Building the catalog, working toward catalog readiness. One customer on file has a price code that doesn't match any of the 5 price levels; fixing that record unlocks the next phase. Three showroom reps are already active on the iPad ahead of schedule.

---

## LEG (Legrand US)

**Phase 3 of 7 — Building the catalog** · working on **Catalog ready** · eCat iPad
**In onboarding 401 days** · Active — first full working session July 14, email threads going

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Org created June 2025; first full working session held July 14, 2026, with weekly Friday check-ins now on the calendar. |
| 2 · First import | 🟢 | 1,020 active products, inventory, and a customer record are all in the system. |
| 3 · Building the catalog | 🟢 | 1,020 products loaded, 83% with photos, 5 price levels configured, and inventory updating daily. |
| 4 · Catalog ready | 🟡 | The one customer on file has a price code that doesn't match any of the 5 price levels — that's the one thing left before this step is done. |
| 5 · Reps using the iPad | ⚪ | Three showroom reps are already logged in and active — two used the app this week — ahead of schedule. |
| 6 · Admin trained | ⚪ | Not started. |
| 7 · Live | ⚪ | Not started. |

### Next step

Correct (or confirm and remove) the one customer record whose price code doesn't match the 5 price levels, so the catalog passes its readiness check.

### Things to flag (1)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | One customer with a mismatched price code | Database | 1 of 1 customers has a price code that isn't in the org's 5 price levels — this is the only thing blocking catalog readiness. |

Three showroom reps are active on the iPad even though catalog readiness isn't confirmed yet — that's an encouraging early signal, but the price code fix still needs to happen first.

### Recent activity

- **Meetings:** 1 in last 90 days — last was "eCat Implementation" on July 14
- **Support:** 4 ticket threads — last reply July 15 (Kylor reply to Trey)
- **Imports:** Products, customers, and inventory all imported within the last 30 days

### Bottom line

Legrand's catalog is in solid shape — 1,020 products, 83% with images, and inventory updating daily. Three showroom reps are already using the iPad even though the formal readiness check isn't done yet. One quick fix — correcting the price code on the single customer record — unblocks everything and moves the project into active rep selling.

---

## DRF (Dorell Fabrics)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 92 days** · Active via email; no calls in 2 months

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kickoff and four implementation calls held April–May 2026. |
| 2 · First import | 🟢 | 1,627 active products, 11 price levels, product stories, and 389 customers all imported. |
| 3 · Building the catalog | 🟢 | 96% of products have photos; product stories and pricing are fully loaded. |
| 4 · Catalog ready | 🟢 | 389 customers on file, every one matched to a valid price list. |
| 5 · Reps using the iPad | 🟡 | No rep user groups have been created yet — no one outside the admin can log in to the app. |
| 6 · Admin trained | ⚪ | Not started. |
| 7 · Live | ⚪ | Not started. |

### Next step

Create at least one rep user group, invite the first reps, and confirm where submitted orders should go (order destination email).

### Things to flag (4)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 3 | Outdated "single net price" setting in our config | HelpScout #14638 (Jul 2) | The config still says DRF uses only one net price. Per the July 2 thread, 11 price levels are now confirmed — List, MFR, WHS, FOB Low/High, C2C, Canadian, and Retail/Net. The setting should be removed. |
| 5 | Test orders filed under the admin's first name | Database | 6 of 7 submitted orders have bill_to = "Suzanne" — that doesn't match any real customer record. One real order (Amalfi) was submitted by the same admin. |
| 5 | Two admin email domains, second unverified | Database | Admin accounts come from dorellfabrics.com and loomcraft.com — confirm whether loomcraft.com is a parent company, a DBA, or unrelated. |
| 3 | No product options — by design | Database | Zero options and zero option groups; the per-SKU fabric model means this is intentional. |

### Recent activity

- **Meetings:** 4 in last 90 days — last was "Implementation Check-In" on May 18 (59 days ago)
- **Support:** Active email threads — last client reply July 9 (Christine asking about line breaks in product stories)
- **Imports:** Products refreshed July 6; product stories loaded July 8

### Bottom line

Dorell Fabrics has a clean, complete catalog — 1,627 products, 96% with images, 11 price levels, and 389 customers all matched to a price list. The project stalls here because no rep user groups have been created and no sales reps have been invited to the app. Once the first user group is set up and reps receive their invitations, the project moves into active selling.

---

## LIBCO (Lib & Co.)

**Phase 7 of 7 — Live** · eCat iPad
**In onboarding 115 days** · Highly active — daily inventory feeds, teams fully engaged

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kickoff held March 2026; weekly working cadence established. |
| 2 · First import | 🟢 | Full product, customer, and inventory data loaded across multiple import cycles. |
| 3 · Building the catalog | 🟢 | 1,620 active products, 99% with photos, 4 price levels fully configured. |
| 4 · Catalog ready | 🟢 | 231 customers on file, every one matched to a valid price list. |
| 5 · Reps using the iPad | 🟢 | 56 reps active across 3 user groups; multiple logged in this week. |
| 6 · Admin trained | 🟢 | Kyla is handling daily inventory feeds and support threads; team handoff is underway. |
| 7 · Live | 🟢 | Real customer order placed July 10 (Lighting Interiors & More); reps are selling. |
| Integration | 🟡 | Business Central API integration in progress — Brent (SuperCat CTO) building the connection; Ernest at TrulieSMB validating. Daily inventory sync will replace the manual upload once this is live. |

### Next step

Confirm go-live with the team, flip the account status to active, and continue tracking the Business Central integration separately from account status.

### Things to flag (2)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| Integration | Business Central integration in progress after go-live criteria were met | HubSpot + overrides config | The Managed Integration Build line item is on the deal; Brent and Ernest are mid-build. This won't block the status flip, but it needs its own tracking lane post-go-live. |
| 3 | No product options — by design | Database | Zero options and zero option groups; the per-SKU lighting model means this is intentional. |

Phase 7 qualified independently on two clear signals: three or more reps have been active in the last 30 days, and a real customer order came in July 10. The admin-handoff signal (the ratio of Kyla and Brent threads vs. Kylor threads) also crossed its threshold at 40%, though most of those non-Kylor threads are automated daily inventory feed ticket closures rather than direct client conversations. Phase 7 stands on the reps-and-orders evidence regardless.

### Recent activity

- **Meetings:** 11 in last 90 days — last was "Sales Portal Review" on July 8
- **Support:** Dozens of threads (daily inventory feeds + active onboarding support) — last reply July 16
- **Imports:** Products updated July 13; customers July 15 (some individual rows failing validation); inventory updated July 6

### Bottom line

Lib & Co. has cleared every go-live marker — active reps, a real customer order on July 10, and the catalog in great shape across 1,620 products. The one open item is the Business Central inventory integration that Brent and Ernest are finishing; it runs independently of the account status. The question for the standup is whether to flip the account to active now or wait for the integration to come online.

---

---

## Appendix

### Run metadata

*Framework v3.5 · Run date 2026-07-16 · All metrics from live tool calls (Postgres + BigQuery) at run time.*

### Resolution and override notes

- **DRF** is listed under `net_price_only_confirmed` in `overrides.yml`. This override is now stale — DRF has 11 price levels confirmed per HelpScout thread #14638 (Jul 2). The entry should be removed from the override file.
- **LIBCO** integration ownership comes from HubSpot deal line items ("Managed Integration Build" + "Managed Integration Hosting" on the Lib & Co. deal) and is corroborated by the `integration_status` override in `overrides.yml` (approach: API, status: building, note: Business Central / Brent / TrulieSMB).
- **DRF and LEG** have no Managed Integration or Certified Pipeline line items on their HubSpot deals; the Integration column is suppressed for both.
- **DRF** `client_domains[]` resolved via admin-email fallback (two distinct domains: `dorellfabrics.com`, `loomcraft.com`). `MULTI_DOMAIN_FALLBACK_UNVERIFIED` fired; once confirmed, fold the canonical list into `overrides.yml § client_domains`.
- **LIBCO** `client_domains[]` = `[libandco.com]`, resolved from `order_email_recipient` (silvio@libandco.com).
- **LEG** `client_domains[]` = `[legrand.com]`, resolved from admin-email fallback (single non-personal domain; `MULTI_DOMAIN_FALLBACK_UNVERIFIED` does NOT fire with a single domain).

### Framework feedback

1. **Phase 6 qual trigger #4 (Kyla-presence ratio) is noisy when the client has automated pipeline tickets.** For LIBCO, 40.3% of SuperCat-authored threads in the last 30 days are from non-Kylor authors — but the majority are daily inventory feed ticket closures by kyla@, not substantive client-facing conversations. The ratio fires as written, but it barely clears the 40% threshold for the wrong reason. Consider excluding tickets whose subject matches an "automated feed" pattern, or requiring at least one non-automated non-Kylor thread as a secondary gate.

2. **`DPC_MISMATCHES_LOW` informational classification is wrong at 100% mismatch rate.** The flag was designed for "a handful of mismatches in a large customer file" and is classified informational. For LEG, 1 of 1 customers (100%) has a mismatched price code. At a 100% rate, this is effectively a blocking issue, not background noise. Consider adding a mismatch-rate threshold (e.g. "fire as actionable when mismatch rate ≥ 50% OR mismatch count = total customer count") so the framework surfaces the severity correctly.

3. **`next_phase_name` has no natural value when `phase_n = 7` (terminal).** The schema requires the field but Phase 8 doesn't exist. This run uses "—" as a sentinel; the schema could formalize this by allowing an empty string or a `null` when anchor = 7.

### Flag-reference map

| Plain-English issue title | Internal flag code |
|---|---|
| Outdated "single net price" setting in our config | `STALE_OVERRIDE` |
| Test orders filed under the admin's first name | `SELF_TEST_SUSPECTED_NOT_CUSTOMER` |
| Two admin email domains, second unverified | `MULTI_DOMAIN_FALLBACK_UNVERIFIED` |
| One customer with a mismatched price code | `DPC_MISMATCHES_LOW` |
| Business Central integration in progress after go-live criteria were met | `INTEGRATION_DEFERRED_POST_HANDOFF` |
