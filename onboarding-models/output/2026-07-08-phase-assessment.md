# July 8, 2026 — Onboarding Phase Assessment

## Where everyone is

| Client | Phase (of 7) | Working on | Days in onboarding | Integration | One thing to resolve |
|---|---|---|---|---|---|
| Dorell Fabrics (drf) | 4 — Catalog ready | Reps using the iPad | 84 | — | Set up rep accounts and invite reps — the catalog and customers are ready for them. |
| The Coppersmith (tcs) | 4 — Catalog ready | Reps using the iPad | 79 | Them (Certified) | Fill the empty rep group and invite reps. |
| Lib and Co. (libco) | 7 — Live | Live | 107 | Us (Managed) | Confirm go-live and flip them to active; close one open thread about a few missing item numbers. |
| Skyard / Pebl (pebl) | 7 — Live | Live | ~349 | — | Wrapping up one last item before the formal handoff to support. |

## Standup agenda

### 🔴 Resolve this week

- **Dorell Fabrics — set up and invite reps.** The catalog is built, all 389 customers are matched to a price list, and an admin has already run a real customer order through the app. The only thing left before reps can sell is creating rep accounts and inviting them. (Also retire the old "single net price" note — they now run 11 price lists.)
- **The Coppersmith — fill the rep group and invite reps.** Catalog is built (720 customers loaded, 99% of products have a photo). A rep group was created but has nobody in it yet.

### ⚠️ Discuss / decide

- **Lib and Co. has hit every go-live signal — confirm go-live.** Thirty-one reps are actively using the iPad (through today), real customer orders are flowing, and support has shifted to Kyla. One open support thread reports a handful of missing item numbers — close that, then flip them to active and hand the integration build off to ongoing tracking.

### ✅ On track (nothing to resolve)

- **Skyard / Pebl** is live and selling (12 active reps, 87 orders). Kylor is wrapping up one last item before the formal handoff to our support team.

---

## drf (Dorell Fabrics)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 84 days** · Active over support email; last call was the May 18 implementation check-in

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off in April; path-forward and implementation calls done. |
| 2 · First import | 🟢 | 1,627 products loaded. |
| 3 · Building the catalog | 🟢 | 96% of products have a photo; 11 price lists now set up (List, Net, Retail, Canadian, FOB, C2C, and more). |
| 4 · Catalog ready | 🟢 | 389 customers loaded and every one is matched to a price list; an admin has run a real customer order (AMALFI) through the app. |
| 5 · Reps using the iPad | ⚪ | No rep group created yet — the three non-admin users are still in the default group. |
| 6 · Admin trained | ⚪ | Order-confirmation email isn't set yet; no handoff to our support team. |
| 7 · Live | ⚪ | Not live. |

### Next step
Create rep groups, add the reps, and send invitations — the catalog and customers are ready for them.

### Things to flag (3)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 3 | Old "single net price" note is now out of date | Database | They now have 11 price lists set up (List, Net, Retail, Canadian List/Lowest, FOB List/Lowest, C2C List/Lowest, MFR, WHS). The saved note that says they run one net price by design should be retired. |
| 4 | No product options — by design | Database | Zero options and zero option groups; this is the expected per-SKU fabric model, not a gap. |
| 5 | Extra test orders billed to "Suzanne" | Database | Four submitted orders are billed to "Suzanne" (the admin's own name) and don't match any customer — these look like admin test orders. The one real customer order (AMALFI) is separate and genuine. |

The order path is already being exercised — one real customer order has gone through — even though reps aren't set up yet. That's a good sign; the remaining gap is purely getting reps into the app.

### Recent activity
- **Meetings:** 6 in the last 90 days — last was "SuperCat / Dorell: Implementation Check-In" on May 18.
- **Support:** 4 email threads (39 messages, 1 still open) — last reply July 7.
- **Imports:** Products re-uploaded July 6 (clean) and product stories July 8; customers were loaded back in late April (warning-only).

### Bottom line
Dorell Fabrics is the furthest along of the three that are still building — catalog built, all 389 customers matched to a price list, and a real customer order already run through by an admin. The single open item is reps: none are set up yet. Two housekeeping notes: they've moved to a full 11-price-list setup (so the old "single net price" note should be dropped), and their lack of product options is intentional.

---

## tcs (The Coppersmith)

**Phase 4 of 7 — Catalog ready** · working on **Reps using the iPad** · eCat iPad
**In onboarding 79 days** · Talking regularly — a call today and email through today

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off April 21; check-ins running, most recently a "Path Forward" call today. |
| 2 · First import | 🟢 | 395 products loaded. |
| 3 · Building the catalog | 🟢 | 99% of products have a photo; options and stories loaded; two price lists set up. |
| 4 · Catalog ready | 🟢 | 720 customers loaded and every one is matched to a price list. |
| 5 · Reps using the iPad | 🟡 | A "Rep Group" was created but nobody's been added to it yet. |
| 6 · Admin trained | ⚪ | Order-confirmation email isn't set yet; no handoff to our support team. |
| 7 · Live | ⚪ | Not live. |

### Next step
Add reps to the "Rep Group" and send invitations so reps can start using the iPad.

### Things to flag (2)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 5 | Rep group created but empty | Database | A "Rep Group" exists with zero members — the scaffolding is built but no reps have been added. |
| 3 | Same warnings on every product import | Database | 27 of 51 product imports carry "Field name Feature1 is unknown" (Feature1–5), and 37 carry "Missing UPCValue." Decide: register those custom fields, drop them from the file, or accept the warnings. |

Two smaller notes: only 129 of 395 products are set to show on the iPad (the rest are intentionally hidden), and one customer row was skipped on the last import because its buyer email was invalid — worth a quick confirm that both are expected.

### Recent activity
- **Meetings:** 6 in the last 90 days — last was "CopperSmith / SuperCat: Path Forward" today, July 8.
- **Support:** 9 email threads (70 messages, 2 still open) — last reply July 8.
- **Imports:** Products, options, option groups, and stories all re-loaded July 6 (products warning-only on unknown fields); customers loaded June 26.

### Bottom line
The Coppersmith's catalog is built, image-rich, and now has 720 customers all matched to a price list. The one thing holding them at "catalog ready" is reps — a rep group exists but is empty, so nobody's using the iPad yet. They're building their own integration (we just certify it), so there's nothing for us to build there. The recurring custom-field warnings are worth cleaning up but aren't blocking anything.

---

## libco (Lib and Co.)

**Phase 7 of 7 — Live** · working on **Live** · eCat iPad
**In onboarding 107 days** · Very active — reps trained and using the app, heavy support email, last check-in July 2

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Kicked off in May; kickoff, path-to-live, and rep-training calls all done. |
| 2 · First import | 🟢 | 872 products loaded. |
| 3 · Building the catalog | 🟢 | 92% of products have a photo; inventory and stories loaded; four price lists set up. |
| 4 · Catalog ready | 🟢 | 265 customers loaded and every one is matched to a price list. |
| 5 · Reps using the iPad | 🟢 | 31 reps have logged in — many today — out of 56 set up across US and Canadian rep groups. |
| 6 · Admin trained | 🟢 | Order email is set, rep training happened June 18, and support has shifted to Kyla (half of our recent replies are now hers). |
| 7 · Live | 🟢 | Reps are placing real customer orders (e.g. Franklin Lighting Inc.). |
| Integration | 🟡 | Managed Business Central integration is ours to run and is still in the build stage (Brent building). |

### Next step
Confirm go-live and flip them to active, close the open "missing item numbers" thread, and keep the Business Central integration build tracked as the one remaining workstream.

### Things to flag (3)

| Step | Issue | Where it's from | What they said / what we see |
|---|---|---|---|
| 4 | A few item numbers reported missing | Help Scout #14691 | "Good Morning, We're working on scanning an order in the showroom, and it looks like we're missing some items. Example: 12351-02 Can you look into this for me." Reps are actively ordering off the catalog, so this reads as a small data-cleanup item, not a broken catalog. |
| Integration | Integration still in build at go-live | HubSpot deal "Lib & Co - TIER 2" | The Managed Business Central integration (Build + Hosting) is ours and is still being built by Brent — track it separately now that they're live. |
| 3 | No product options — by design | Database | Zero options and zero option groups; expected for their per-SKU lighting model. |

Note on how they're classified: reps are actively using the iPad (31 logged in, many today), real customer orders are flowing, and support has moved to Kyla — so Lib and Co. has met the go-live bar. A strict, mechanical read of the "catalog ready" step would hold them back because of the open "missing items" support thread, but that's clearly a data-cleanup question, not a sign the catalog is unusable. See the framework note in the appendix.

### Recent activity
- **Meetings:** 12 in the last 90 days — including rep training on June 18; last was "Lib & Co / SuperCat: Onboarding Check-In" on July 2.
- **Support:** 13 email threads (146 messages, 6 still open) — last reply July 8.
- **Imports:** Inventory re-loaded July 6; products June 22 (warning-only); customers June 17 (clean); stories June 15.

### Bottom line
Lib and Co. has effectively gone live: 31 reps are actively using the iPad (many logged in today), real customer orders are flowing through reps, and day-to-day support has shifted to Kyla. The customer-import problem from earlier is fully resolved — 265 customers loaded and all matched to price lists. Two things to close out: a support thread about a few missing item numbers, and the Managed Business Central integration, which is still in the build stage. Recommend confirming go-live and flipping their status to active so they drop out of next week's onboarding read.

---

## pebl (Skyard / Pebl)

**Phase 7 of 7 — Live** · working on **Live** · eCat iPad
**In onboarding ~349 days** since the account was created (project active since late January 2026) · Live and selling; very active over support email, last reply July 2

### Where they are

| Step | Status | What we see |
|---|---|---|
| 1 · Kickoff | 🟢 | Long-running relationship; the project ran in earnest from late January 2026. |
| 2 · First import | 🟢 | 713 products loaded. |
| 3 · Building the catalog | 🟢 | 97% of products have a photo; options loaded; eight price lists set up. |
| 4 · Catalog ready | 🟢 | 171 customers loaded and every one is matched to a price list. |
| 5 · Reps using the iPad | 🟢 | 12 reps are set up and all 12 have logged in within the last 30 days. |
| 6 · Admin trained | 🟢 | Reps trained and order email set; Kylor is finishing one last item before the formal support handoff. |
| 7 · Live | 🟢 | Live — reps are placing real customer orders (87 submitted to date). |

### Next step
Wrap up the one remaining item, then hand Pebl off to our support team.

### Recent activity
- **Meetings:** No recorded calls in the last 90 days — the relationship runs almost entirely over support email.
- **Support:** 2 email threads (65 messages, 1 still open) — last reply July 2.
- **Imports:** Full catalog in place — 713 products, options, and 171 customers all loaded and price-matched.

### Bottom line
Skyard / Pebl is live and selling — 12 reps active in the app and 87 orders placed to date, with the full catalog and all customers loaded and price-matched. Kylor is wrapping up one final item before formally handing the account off to our support team, at which point it's fully off the onboarding list.

---

*Framework v3.5 · run 2026-07-08 · all metrics pulled from live Postgres, BigQuery (Fathom / Help Scout), and HubSpot at run time.*

### Resolution / override notes
- **libco:** integration ownership read from the HubSpot deal "Lib & Co - TIER 2" (Managed Integration Build + Hosting = ours); status tracked in `overrides.yml § integration_status` (Business Central, building, Brent), so `INTEGRATION_OWNER_UNCLEAR` does not fire.
- **tcs:** integration ownership read from the HubSpot deal "The Coppersmith - TIER 3" (Certified Pipeline = theirs); shown as an informational note only, no integration flag.
- **drf:** no integration line item on the deal → self-serve, integration suppressed. `client_domains[]` resolved from the HubSpot company primary domain (`dorellfabrics.com`); Loomcraft is a separate HubSpot company, so no multi-domain fallback flag this run.
- **drf:** `net_price_only_confirmed: drf` in `overrides.yml` is now contradicted by live data (11 price levels). Recommend removing the override.
- **pebl:** included at operator request. Pebl has already flipped to `status = 'active'` and so is out of the auto-cohort; it is shown here as live/handing-off for visibility, not because the framework selected it.

### Framework feedback
- **`import_events` schema does not match the v3.5 query.** `RUN_PROMPT.md § Step 1` selects `ie.file_type`, `ie.num_warnings`, `ie.num_errors`, `ie.warning_message`, `ie.error_message`, but the live table has only `id`, `created_at`, `organization_id`, `data` (YAML text). The per-file-type query fails with "column ie.file_type does not exist." Parsed the YAML `data` with `position('- - <FileType>' in data)` instead (matching the Phase 2/3 anchors, which already reference `data::text`). Recommend rewriting the Step 1 primitive to parse `data`.
- **`CROSS JOIN LATERAL` is still rejected by the Postgres MCP tool.** The lateral form fails validation; a `UNION ALL` of six `DISTINCT ON (shortname)` selects works. Consistent with prior runs' feedback.
- **Phase 4's "no active 'missing' support thread" clause, combined with the contiguous-anchor rule, can drag a live client back to Phase 3.** Lib and Co. has 31 active reps, real orders, and a completed handoff, but an active client thread whose subject contains "missing" ("Missing Item numbers") literally trips the Phase 4 anchor's 7th clause. Read mechanically, the contiguous "last fully-Done phase" rule would then classify a demonstrably live client as "Phase 3 — Building the catalog," which is clearly wrong. Recommend scoping that clause (e.g. only block when the thread indicates the catalog is unusable, or suppress it once reps are actively submitting orders off the catalog).
- **The Phase 4 defect regex false-matches on the bare word "missing."** Both Lib and Co. (a showroom SKU question) and Dorell Fabrics (a reassuring "your price upload did go through" reply) matched the clause without being catalog defects. The regex needs a tighter defect-sentiment scope, like the one `IMPORT_VS_HELPSCOUT_DRIFT` already uses.

### Flag-reference map
| Plain-English title | Internal flag code |
|---|---|
| Old "single net price" note is now out of date | STALE_OVERRIDE |
| No product options — by design | OPTIONS_INTENTIONALLY_EMPTY |
| Extra test orders billed to "Suzanne" | SELF_TEST_SUSPECTED_NOT_CUSTOMER |
| Rep group created but empty | USER_TYPES_EMPTY |
| Same warnings on every product import | RECURRING_WARNINGS_NO_ERROR |
| Integration still in build at go-live | INTEGRATION_DEFERRED_POST_HANDOFF |
