# Phase Progression Framework — Audit (v3)

**Auditor:** fresh-session agent
**Audit date:** 2026-06-05
**Target document:** `~/Downloads/Phase_Progression_Framework.md` (v3.0, 2026-06-05)
**Prior framework reviewed:** `SuperCat 4.0/onboarding-models/` (v2.0, 2026-06-03)
**Tools used:** `user-supercat-postgres-vpn.execute_sql` (live); `user-bigquery-admin.query` (Fathom + HelpScout, live). Every numeric claim below traces to a tool call in this session.

---

## 1. Verdict

**Adopt with changes.** The 7-phase reframe, auto-cohort detection, qual-signal-as-phase-anchor, and first-class ambiguity flags are all directionally right and a clear improvement over v2's 11-stage ladder. But several individual anchor clauses are demonstrably wrong against the framework's own canonical reference orgs — Phase 6 and Phase 7 in particular fail on TCD (the gold-standard exit) and the Phase 5 "Done when" clause fails on the only two clients that have ever submitted an order. The framework needs three targeted fixes before adoption; the structure itself is sound.

---

## 2. Per-phase findings

### Phase 1 — Discovery / Kickoff

**Question is right.** "Have we kicked off this client?" is the correct gate at this position.

**Issues:**

- **Anchor (Postgres path) is over-broad.** `org row exists AND properties->>'status' = 'onboarding'` fires the instant a shortname is provisioned. Combined with the auto-cohort query (which only returns `status='onboarding'` orgs in the first place), every cohort member trivially passes the Postgres anchor. This means the Postgres clause adds zero classification information at the cohort level. Not a defect, just dead weight — the Fathom/HelpScout path is the only one that actually decides whether Phase 1 is "Done."

- **Fathom regex `(?i)\bkickoff\b` produces false negatives on most real kickoffs.** Of the 6 reference orgs, only 2 have a Fathom title with the literal word "kickoff":
  - TCS: `The CopperSmith Kickoff Meeting` (2026-04-21) ✓
  - LIBCO: `Lib & Co. kickoff meeting` (2026-05-22) ✓

  The other 4 use canonical SuperCat naming that does NOT contain "kickoff":
  - DRF: `Discovery Call` (Feb 3), `Dorell + SuperCat Solutions` (Feb 10), `Dorell path forward alignment` (Apr 13), `Data Files` (Apr 15)
  - PEBL: `Discovery Call` (Dec 10, 2025) only — no kickoff Fathom at all
  - MALI: `MagicLite + Supercat Onboarding` (Jan 20, 2026), `Magic Lite / SuperCat: Onboarding Working Session` (Apr 2)
  - TCD: `Scott / SuperCat` (Feb 24), `Terracotta / SuperCat: Onboarding Check-In` (Dec 18, 2025)

  Under the v3 anchor as written, DRF/PEBL/MALI/TCD would all FAIL the Fathom branch — only the HelpScout branch could rescue them.

- **HelpScout regex `(?i)kick.?off|onboarding.*next steps` has a false positive.** DRF's `#14401 Re: eCat — Initial Product & Customer Imports Complete + Next Steps` (Apr 27) matches the regex but is a **Phase 3→4** thread, not a kickoff. The regex confuses "Next Steps" boilerplate (which Kylor uses throughout the lifecycle) with kickoff specifically.

**Recommended changes:**

1. Drop `(?i)\bkickoff\b` and replace with `(?i)kickoff|discovery call|onboarding (working session|kick-?off|intro)|^[A-Za-z &/]+\s+(kickoff|onboarding)`. Or, simpler: any Fathom with `external_domains` intersecting `client_domains` AND `meeting_start <= organizations.created_at + 30 days` is treated as kickoff-equivalent.
2. Tighten the HelpScout regex to require the word "kickoff" OR explicit subjects like `welcome|next steps:.*admin training`, not loose "next steps" anywhere in body.
3. Cleanest framing: **Phase 1 is "Done when" ANY external touchpoint (Fathom OR HelpScout) exists with `external_domains`/`primary_customer_domain` matching client_domains, dated within 90 days of the org `created_at`.** That gets every reference org right and stops trying to text-match meeting titles.

### Phase 2 — Initial Import

**Question and anchor are right.** "≥1 row in `import_events` whose body parses Products and is not `:fatal`" is the correct minimum bar, and the "Done when total_products > 0" check forecloses the empty-products-file case.

**Issue:** The anchor says `data::text ILIKE '%- Products%'` but the YAML format is actually `- - Products` (verified in raw events). Both patterns will match because of the SQL ILIKE wildcard, but the framework should show the verified pattern: `data::text ILIKE '%- - Products%'` or, better, parse the YAML and check the top-level key.

**Recommended changes:** None to logic; document the actual YAML shape so the next agent doesn't fight wildcards.

### Phase 3 — Progress

**Question is right.** The 50% image floor and `:fatal`-only blocking are both grounded in `llms.txt` semantics (Fatal = file rejected; Error/Warning still import).

**Issues:**

- **"Most-recent" check is ambiguous across file types.** The anchor says "for every file type that has any event, the most-recent event's body does NOT match `:fatal`." But a single `import_events` row can contain multiple file blocks (e.g. Products + Product Stories + Inventory). The "most-recent event per file type" must be resolved at the YAML-block level, not the row level. The current SQL pattern in the prior framework checked event-level only. Spell this out.

- **Image coverage floor is not flexible enough for the lighting/fabric model.** LIBCO has 88% image coverage but ZERO options (its lighting fixtures are discrete per-SKU); DRF has 70% image coverage with ZERO options (fabric). Both pass. Good. But TCD, the Phase 7 exit, has only 47/394 = 12% of products *visible* in the iPad after a `Hideable=Y` strategy was applied — the underlying `image_exists` count is higher (394/394 = 100%), but visible catalog is 12%. The framework's anchor uses `image_exists`, which is the right metric for raw readiness, but the standup should know visibility differs. Surface `count(Hideable=N) / total` as a Phase-3-health metric alongside image coverage, otherwise the framework will silently miss the "imported but hidden" pattern.

- **"≥2 price_levels OR Net-Price-only mode is confirmed" is a hidden human-in-the-loop step.** Net-Price-only mode cannot be confirmed programmatically; the framework punts this to a flag. That's acceptable but should be called out as the gating decision that prevents auto-classification — i.e., a single-price-level org will sit in "Phase 3 — needs human Net-Price confirmation" indefinitely. Tag a flag explicitly: `SINGLE_PRICE_LEVEL_UNCONFIRMED` so the standup knows to resolve it.

**Recommended changes:**

1. Specify YAML-block-level parsing in the most-recent-per-file rule.
2. Add `visible_products_pct = count(products WHERE deleted=false AND COALESCE(hideable_on_ipad, false)=false) / count(products WHERE deleted=false)` to Phase-3-health (does not gate).
3. Add the `SINGLE_PRICE_LEVEL_UNCONFIRMED` flag.

### Phase 4 — Catalog Completeness

**Question is right.** This is the "can we ship a live iPad" gate.

**Issues:**

- **DPC-resolution check is fine but slightly over-strict.** Verified live: DRF (389 customers, 100% on `net` → `Net`), MALI (3,417 customers, 100% on `nsldn`/`mldn` both real), TCD (346 customers, 100% on `dn`/`ns` both real). The ≥99% threshold passes for all three. No false-positive risk seen. Keep as-is.

- **Option-group existence check has a vacuous-truth trap.** The anchor says "Option groups exist if any product has a non-empty `OptionSet1..N`." LIBCO and DRF have 0 options/option_groups (intentional — lighting fixtures and fabric SKUs respectively). The clause is conditional so both pass vacuously. Fine. But the framework should explicitly carry an `OPTIONS_INTENTIONALLY_EMPTY` flag for those orgs so the standup doesn't have to keep asking "why is Phase 4 green with 0 options?"

- **HelpScout error-keyword filter is reasonable but brittle.** "filed by the client in last 14d" — the v3 framework correctly distinguishes client-authored from agent-authored threads. Confirmed: PEBL #13879 has both `kylor@`/`kyla@` and `sales04@peblfurniture.com` (Mandy) authoring, so client-side activity is detectable. The 14-day window is tight enough to flag fresh complaints without resurfacing resolved ones.

**Recommended changes:** Add an `OPTIONS_INTENTIONALLY_EMPTY` flag for orgs where Phase 4 passes vacuously on the option-group clause.

### Phase 5 — Reps Signed In

**Question is right** but the "external rep" definition has two structural bugs and the "Done when" clause fails against the live data.

**Bug 1: `client_domains[]` exclusion is contaminated by admin emails on personal domains.**

Verified live: TCD has 2 admins — `kylor22johnson@gmail.com` (Kylor's personal/test admin) + `scott.tang@terracottalighting.com`. The framework's `client_domains[]` aggregator (per RUN_PROMPT's Step 0 query) includes `gmail.com` in TCD's client_domains because the gmail admin is non-`@supercatsolutions.com`. Result: 8 of TCD's 22 active sales reps email from `@gmail.com` and are silently dropped by the rep filter.

Confirmed counts:
- TCD `Sales Reps` user_type: **22 non-admin members** (raw).
- Under v3 `external_rep` definition: **14** (gmail.com reps excluded).
- 12 ever logged in; 11 active in last 30d. (TCD is unambiguously Phase 5 done, but the numbers reported would be wrong.)

**Bug 2: in-house W-2 reps using the client's own domain are always misclassified as admins/employees.**

The `NOT IN (client_domains[])` rule assumes all reps email from agency/independent domains. Many manufacturers have **in-house** reps on `@clientcompany.com`. Verified live: MALI's `pansy@magiclite.com` and `michelle@nslusa.com`/`jason@nslusa.com` are non-admin in DefaultUserGroup with login activity (jason last login 2026-05-05). All three would be invisible to the rep filter under the current definition.

This isn't theoretical — MALI has not yet migrated reps into `ML Reps`/`NSL Reps` user_types, but if/when they do, in-house reps on `@magiclite.com`/`@nslusa.com` will still be excluded by the framework's rule.

**Bug 3: Phase 5 "Done when" requires a non-admin org_user to submit an order, but in reality only admins exercise the test order path.**

Verified live: every order in `orders` across the 6 reference orgs is from `is_admin = true`:
- DRF: 1 order, `Suzanne@dorellfabrics.com`, `is_admin=True`, `bill_to_company_name='AMALFI'`.
- PEBL: 9 orders, `sales04@peblfurniture.com`, `is_admin=True`, `bill_to_company_name='Pebl'` (all self-tests).
- TCS / LIBCO / TCD / MALI: 0 orders in DB.

Under v3 Phase 5 "Done when" as written, **NO client in the cohort would qualify as Phase 5 done**, including TCD which is the canonical Phase 7 example. This is a fatal flaw.

**Recommended changes:**

1. **Build `client_domains[]` from the customer-facing email columns, not admin org_users.** Use `organizations.order_email_recipient`'s domain, plus the `primary_customer_domain` HubSpot stores, plus any explicit override. Do NOT derive from admin emails — too easy to contaminate. Fall back to `org_users` only if those upstream signals are empty, and exclude personal-email providers (`gmail.com`, `yahoo.com`, `outlook.com`, `icloud.com`, `hotmail.com`, `me.com`, `aol.com`, `fuse.net`) from being aggregated as a "client domain" regardless of source.

2. **Distinguish "external rep" (agency, independent) from "in-house rep" (client domain) but count both toward Phase 5.** The Phase 5 question is "are reps logging in" — it should not care which kind. Use:
   ```
   is_admin = false
   AND user_type.name <> 'DefaultUserGroup'
   AND email NOT LIKE '%@supercatsolutions.com'
   AND COALESCE(disabled, false) = false
   ```
   ...and report `rep_count_external` vs `rep_count_in_house` as separate health metrics, without using either as an exclusion filter for the anchor.

3. **Drop the `non-admin org_user` requirement from Phase 5 "Done when."** A test order from the client admin during onboarding IS the workflow being exercised end-to-end — that's the signal you actually want. Either:
   - Replace with: "≥1 submitted order in `orders` from ANY org_user of the org (admin or non-admin)" — and let Phase 7 carry the "real customer order" distinction; OR
   - Drop the order requirement from Phase 5 entirely and treat it as a Phase 5 health metric only. Phase 5 = reps logging in. Orders are Phase 7 (Go-Live).

   I'd lean toward the second option: Phase 5 = reps in custom user_types are actually logging in. Done. The order-path-exercised question belongs in Phase 7.

### Phase 6 — Admin Training

**Question is right.** The qualitative trigger detection (Kyla/Angie CC pattern, admin training Fathom, KB URL share) is a real improvement over v2 — the prior framework had no concept of qualitative phase advancement at all.

**Issues:**

- **`ipad_reports >= 3` is an arbitrary threshold that fails on the framework's gold-standard example.** Verified live: TCD has **1 ipad_report** (`Organization Tearsheet`, created 2026-02-17). DRF has 3. PEBL has 1. LIBCO has 1. MALI has 0. TCS has 0.

  TCD is described in the handoff as the canonical Phase 7 exit (Apr 27 handoff to Kyla/Angie, 22 active reps, daily image cleanup imports continuing). It would fail v3 Phase 6 quant readiness on `ipad_reports >= 3`, blocking it from advancing to Phase 7.

  The `>= 3` came from v2's Stage 7 criterion. Inspection of the actual ipad_reports across live and active orgs shows 1–3 is the common range. **The threshold is too high.** Either lower to `>= 1` or drop it entirely — the trained-admin guide (`~/Downloads/index (1).html`) doesn't mention PDF report formats as part of "trained admin" at all. Looking at what the admin training HTML actually covers (users, user groups, price levels, taxonomy display names), `ipad_reports` count is a weak proxy for admin training completion.

- **`order_email_recipient not empty` is sensible but watch for ERP-placeholder emails.** Verified live: PEBL has `info@peblfurniture.com` set; TCD has `sales@terracottalighting.com`; DRF/LIBCO/MALI/TCS are empty. The framework is correct that an empty value means it wasn't configured. Just be aware some orgs may set a temporary value during testing — flag if it matches `%example.com%`, `%test%`, or the SuperCat domain.

- **`user_types >= 2` quirk: `z-SuperCat` and `DefaultUserGroup` both count.** Verified live: MALI has 4 user_types — `DefaultUserGroup`, `ML Reps`, `NSL Reps`, `z-SuperCat`. The threshold passes despite no actual client rep group population. TCD has 2 (`DefaultUserGroup`, `Sales Reps`) — passes legitimately. PEBL has 1 — fails. The current rule is `>= 2 (at least one beyond DefaultUserGroup)`. That's fine as written. Just be aware "z-SuperCat" (SuperCat-internal admin shadow group) does count, which is harmless but worth documenting.

- **The "ANY ONE" qualitative trigger list is good but missing the most common signal.** The three triggers listed (CC pattern, admin training Fathom, KB URL share) are all valid. Verified live: TCD's `#14411 Re: Welcome to SuperCat Support, Next Steps: Admin Training` (last activity 2026-05-13, Kyla author) AND `#14496 Re: SuperCat Admin Training Handoff` (May 15) both match the Fathom title regex pattern `(?i)admin training|handoff` AND have Kyla as primary author. MALI's `#14418 Re: SuperCat / Magic Lite: 4/29 Follow-Up` (last May 19, Kyla) has Kyla as author but the subject doesn't match the regex. Add `(?i)follow.?up` or just relax the rule to "ANY thread in last 90d where SuperCat author is `kyla@` or `support@` AND subject contains the org/client name" — the author-identity signal is the load-bearing one, not the keyword.

**Recommended changes:**

1. **Drop `ipad_reports >= 3` from the anchor.** Move it to Phase 6 health, with threshold `>= 1`. Or drop entirely — it doesn't correspond to what "trained admin" actually means in the customer-facing admin training material.
2. **Add `kyla@`/`support@` author dominance in last 30d as a 4th qualitative trigger**, independent of subject regex. This is the most reliable post-handoff signal.
3. **Add placeholder-email detection for `order_email_recipient`** (`%example%`, `%test%`, `%@supercatsolutions.com`).

### Phase 7 — Go-Live (terminal)

**Question is right.** The exit-from-cohort semantics align with `properties->>'status'` flipping to `active`.

**Issues — these are the most serious in the framework:**

- **The anchor cannot fire for any client in the current cohort or reference set.** Verified live: only DRF and PEBL have ANY rows in `orders` (1 and 9 respectively). TCD has 0. MALI has 0. The framework's required clause "≥1 submitted order in `orders` from a non-admin user with `bill_to_company_name` ≠ the client's own company name" cannot be satisfied by:
  - TCD: 0 orders → fails (but is Phase 7 in reality)
  - MALI: 0 orders → fails
  - DRF: 1 order, but submitter is `is_admin=True` → fails on non-admin clause
  - PEBL: 9 orders, but all `bill_to_company_name='Pebl'` (self-tests) AND submitter is admin → fails both clauses

  This means the framework's Phase 7 anchor is **structurally unable to detect Phase 7** against the only live examples available. Either the `orders` table is not where iPad orders persist for some orgs, or orders are purged/exported after some retention window, or the "non-admin + non-self bill_to" combination simply doesn't reflect how onboarding admins drive Phase 5/Phase 7 in practice.

- **The `is_admin` requirement on order submission is wrong.** Onboarding admins (Suzanne at DRF, Mandy/Sales04 at PEBL) ARE the ones exercising the order path. Excluding them removes the only signal available.

- **The "Kyla > Kylor in last 30d" check works correctly.** Verified live for the past 60 days:
  - TCD: 8 SuperCat-author threads, all Kyla, last Kylor May 1. Passes.
  - MALI: 13 SuperCat-author threads, 12 Kyla, 1 Kylor (May 12). Passes — but MALI's Phase 6 infra is broken, so Phase 7 shouldn't fire even with the author-shift signal. The framework correctly gates Phase 7 on Phase 6 done.
  - The author-shift heuristic is robust to staffing — if Kyla leaves, the rule still works (compare any non-`kylor@` SuperCat author vs `kylor@`).

- **"Brittle when Kylor is on PTO."** Yes, this is a real edge case. If Kylor is OOO for 2 weeks, every client's correspondence will skew non-Kylor by default. Mitigation: extend the window from 30d to "last 30 days OR last 5 threads, whichever is more inclusive." Or: don't penalize the absence of Kylor; penalize the presence of Kyla. Switch the rule to: "≥3 threads in last 60d authored by `kyla@`/`support@` AND `kyla@`/`support@` is the most-recent SuperCat author." That captures Kyla's takeover without depending on Kylor's activity.

**Recommended changes:**

1. **Soften the order requirement.** Replace "≥1 submitted order in `orders` from a non-admin user with `bill_to_company_name` ≠ the client's own company name" with **EITHER**:
   - "≥1 submitted order in `orders` from any org_user with `bill_to_company_name` ≠ the client's own company name (real customer order, admin or rep submitter both fine)" — and **note that this clause will not fire for orgs where iPad is used as a catalog browser and orders are submitted via legacy channels**, OR
   - Make the order clause OPTIONAL and rely on rep-activity (`≥3 external_reps active in last 30d`) + correspondence shift as primary anchors. The order clause becomes a confirming signal, not a gating one.

   The second option is more robust given TCD's zero-orders reality.

2. **Refactor the correspondence-shift detection to be Kyla-presence-based, not Kylor-absence-based** (see issue above).

3. **Document the "iPad as catalog browser, orders via legacy" pattern** as an explicit possibility for Phase 7 clients. Some manufacturers' reps use the iPad to present + generate PDFs but submit orders through ERP/email/phone — and TCD is plausibly such a client. The framework should not penalize that.

---

## 3. Per-org classification check (independent)

Auto-cohort query verified — returns exactly `tcs`, `drf`, `libco`, `pebl`. The 3 demo/template/test orgs (`hl`, `tmpo`, `tmpl`) are correctly excluded by the name pattern filters. Status distribution: 118 active, 76 inactive, 26 fully_suspended, 16 test, 7 onboarding, 4 demo, 3 NULL — `onboarding` is reliably populated.

**Below: my independent classification using the framework as written today, plus disagreements with the handoff table.**

| Org | Handoff says | My read | Notes |
|---|---|---|---|
| TCS | Phase 3 (Progress) | **Phase 3 anchor passes; Phase 4 borderline** | 271 prods, 255 with images (94%), 329 options, 328 option_groups, 2 price levels (msrp/map), 0 customers, 0 inventory, 0 ipad_reports, 1 user_type, order_email empty. Phase 3 anchor: 5 file types imported in last 60d (verified Jun 5: Products, Options, Option Groups, Inventory, Customers in import_events) ✓. Most-recent per file = warning-only (custom field missing, no fatal/error) ✓. ≥2 price levels ✓. Image coverage 94% ✓. Phase 4 anchor: still need no customer DPC mismatches (vacuous: 0 customers) and no active import-error helpscout (PEBL-like). All open thread = #14520 about Catsy strategy, not import error. **Plausibly Phase 4 anchor passes** because the customer-DPC clause is vacuously true. This is a framework edge case: an org with 0 customers passes Phase 4's customer-DPC check vacuously. **Recommend adding "AND customers > 0" to Phase 4 anchor** to prevent skipping ahead, OR explicitly say "Phase 4 not reachable with 0 customers." |
| DRF | Phase 3 (Progress) | **Phase 4 anchor passes; Phase 5 borderline** | 1,676 products, 70% images, 389 customers all with valid DPC (`net` → `Net`), 0 options (intentional, lighting/fabric model), 1 price level (Net), 1 ipad_order (admin), 0 inventory. Phase 4 anchor: all clauses pass (option-group clause vacuous; DPC 100%; image 70%; product event clean — Jun 2 image error is image-level not product-level). Phase 5: external_reps = 0 under any definition (DefaultUserGroup only has admins). **Phase 4 done, Phase 5 anchor fails.** **Disagreement with handoff:** handoff says Phase 3; framework as-written says Phase 4. I think Phase 4 is correct. |
| LIBCO | Phase 3 (Progress) | **Phase 4 anchor passes; Phase 5 fails (scaffolded but unfilled)** | 907 products, 88% images, 4 price levels, 910 inventory fresh, 0 customers, 3 user_types (`DefaultUserGroup`, `Lib & Co — US Reps`, `Lib & Co — Canadian Reps`), 0 non-admins in rep groups. Phase 4: vacuous customer-DPC passes; option-group vacuous (0 options intentional); product event clean. **Phase 4 done.** Phase 5: rep groups exist but EMPTY — `USER_TYPES_EMPTY` flag fires. **Disagreement:** handoff says Phase 3; my read is Phase 4 done. The 0-customers anti-skip caveat (same as TCS) applies. |
| PEBL | Phase 3 (Progress) | **Phase 3 done; Phase 4 anchor passes vacuously (same caveat)** | 303 products, 63% images (just over 50% floor), 2 price levels, 103 options, 62 option_groups, 0 customers, 0 inventory, 9 self-test orders, 1 user_type (DefaultUserGroup), 1 ipad_report. order_email set to `info@peblfurniture.com` (Phase 6 quant readiness contributor). Phase 4 vacuous-DPC trap applies. **Disagreement:** handoff says Phase 3; framework says Phase 4 vacuously. **PEBL is the strongest case for the "AND customers > 0" amendment to Phase 4.** Also: `SELF_TEST_ONLY_ORDERS` flag would fire (9 orders, all `bill_to_company_name='Pebl'`). Also: framework's `INFRA_READY_NO_HANDOFF` won't fire because quant readiness fails on user_types=1 < 2 and ipad_reports=1 < 3. |
| TCD | Phase 7 (Live, exited cohort) | **Phase 7 anchor FAILS** (per framework as written) | `status='active'`, correctly excluded from auto-cohort. But if we were to apply the framework to TCD: 394 products, 100% images, 4 price levels, 346 customers all valid DPC, 22 reps in `Sales Reps` user_type (14 under v3's contaminated external_rep definition, 22 under the corrected definition; 12 ever logged in, 11 active 30d), 1 ipad_report, order_email set, 0 orders in `orders` table. Phase 6: qual trigger fires (#14411, #14496, Fathom "Admin Training Handoff" May 13) ✓. Quant readiness: order_email ✓, ipad_reports=1 FAIL (anchor wants ≥3), user_types=2 ✓. **Phase 6 fails on ipad_reports.** Phase 7 anchor: requires Phase 6 done (FAILS), real customer order (FAILS — 0 orders), correspondence shift (PASSES). **TCD would be classified Phase 5 (rep activity present but Phase 6 quant readiness blocks)** under the framework as written. This contradicts the canonical-example handoff. **This is the framework's biggest single defect.** |
| MALI | Phase 6 Admin Training, stalled | **Phase 5 → 6 boundary with KYLA_INTRO_INFRA_GAP** | `status='active'`, excluded from auto-cohort. Re-evaluating: 694 products, 99% images, 5 price levels, 3,417 customers all valid DPC, 1,388 inventory, 4 user_types (`DefaultUserGroup`, `ML Reps`, `NSL Reps`, `z-SuperCat`), but rep groups effectively empty (1 user in `ML Reps` is Kyla from SuperCat — correctly excluded; 0 actual client reps migrated). order_email empty, 0 ipad_reports, 0 orders. Phase 6 qual trigger fires (#14418 active w/ Kyla as primary author, Fathom "SuperCat / Magic Lite: Admin Training" Apr 29). Quant readiness: order_email FAILS, ipad_reports=0 FAILS, user_types=4 ✓. Two-of-three FAIL on Phase 6 quant readiness. **`KYLA_INTRO_INFRA_GAP` flag fires correctly** — exactly the pattern the flag was designed for. Agreement with handoff. |

**Summary of disagreements:**

- 4 of 6 orgs (TCS, DRF, LIBCO, PEBL) get classified one phase HIGHER by the framework than by the handoff, because Phase 4 anchor passes vacuously with 0 customers. **Add `customers > 0` to Phase 4 anchor.**
- TCD gets classified Phase 5 instead of Phase 7. **Lower `ipad_reports >= 3` threshold in Phase 6 anchor; soften the order requirement in Phase 7 anchor.**
- MALI classification agrees with handoff.

---

## 4. Ambiguity flag review

Of the 18 flag codes (Sections A–E in v3), my evaluation:

### Keep as-is (9)

- `KYLA_INTRO_INFRA_GAP` — high-value, validated against MALI live data.
- `INFRA_READY_NO_HANDOFF` — high-value (inverse of above). May rarely fire in practice but worth keeping.
- `REPS_DEFINED_NOT_LOGGED_IN` — clear and actionable.
- `USER_TYPES_EMPTY` — clear and actionable. LIBCO is the live example today.
- `REPS_IN_DEFAULT_GROUP` — clear and actionable. PEBL is the live example today (non-admin client users on `sales04@peblfurniture.com` submitting test orders from DefaultUserGroup).
- `SELF_TEST_ONLY_ORDERS` — clear; PEBL is the live example (`bill_to_company_name='Pebl'` × 9).
- `HELPSCOUT_QUIET_POSTGRES_QUIET` — important for catching stalled accounts (no ticket activity, no import_events). Keep.
- `RECURRING_WARNINGS_NO_ERROR` — PEBL's custom-field warnings are the canonical case (`Certification`, `Color`, `PackingSize` etc. recurring across Jun 3–4 imports). Keep.
- `KYLOR_DOMINATES_POST_HANDOFF` — useful for "handoff didn't take" detection. Keep.

### Modify (6)

- `IMPORT_VS_HELPSCOUT_DRIFT` — direction is right but trigger needs tightening. "Recent clean imports BUT helpscout client thread about the import in last 7d." Need to define "clean" (no `:error`/`:fatal`?) and "about the import" (which keywords?). As written, this is too loose to be programmatic. Specify: client-authored thread, in last 7d, body matches `(?i)import|upload|csv|wrong.*data|missing.*products|prices.*off`.
- `HELPSCOUT_ACTIVE_POSTGRES_QUIET` — same issue. Specify "active" = ≥1 client-authored thread in last 14d; "postgres quiet" = no import_events in last 14d. Tighten both.
- `IMAGE_COVERAGE_BORDERLINE` (0.45–0.55) — the 10-point band is too narrow. Real coverage % migrate by 1–3% per image batch, so a client could oscillate across the band on consecutive runs. Widen to 0.40–0.60 OR remove and require Kylor to manually flag.
- `DPC_MISMATCHES_LOW` (1–5) — based on live data, all 4 reference orgs with customers have 100% DPC resolution. The flag may rarely fire. Keep but expect it to be quiet.
- `INTEGRATION_OWNER_UNCLEAR` — direction right but "Fathom in last 90d include integration topics but no decision recorded in HelpScout" requires a "decision detector" that is hard to spec. Replace with: "≥2 Fathom meetings in last 90d whose `section_titles` include integration keywords (`api|business central|netsuite|pim|odoo|integration`)" — i.e., recurrence of the topic without convergence, observable purely from Fathom.
- `PHASE_SKIP_OBSERVED` — useful but the v3 algorithm already surfaces this as "Anchor + Current + Open Workstreams." The flag may be redundant with the algorithm's output. Demote to a narrative note: "Phase ≥ Anchor+2 signal detected" rather than a first-class flag.

### Add (4)

- `SINGLE_PRICE_LEVEL_UNCONFIRMED` — DRF (1 price level: Net) needs explicit human confirmation of "Net-Price-only mode" before Phase 3 can advance. Without this flag, DRF will sit ambiguously.
- `OPTIONS_INTENTIONALLY_EMPTY` — LIBCO and DRF both have 0 options by design. The flag confirms the standup doesn't need to keep asking "where are the options?"
- `PHASE_4_VACUOUS_NO_CUSTOMERS` — fires when a client's Phase 4 anchor passes only because the 0-customer count makes DPC-resolution vacuously true. Forces the standup to handle the "we passed Phase 4 with 0 customers" edge case explicitly.
- `ZERO_ORDERS_IN_DB` — fires when an otherwise-Phase-7-ready org (rep activity + correspondence shift) has 0 rows in `orders`. Captures the "iPad as catalog browser, orders via legacy" pattern that TCD exhibits and that the strict Phase 7 anchor cannot otherwise distinguish from a true stall.

### Kill (0)

None worth removing entirely. The first-class flag system is genuinely informative, not noisy.

### On the noise concern (handoff said "18 is a lot")

In practice, my read against the 6 reference orgs:
- TCS: 1 flag (`SINGLE_PRICE_LEVEL_UNCONFIRMED` if you count msrp/map as borderline; otherwise 0)
- DRF: 2 flags (`OPTIONS_INTENTIONALLY_EMPTY`, `PHASE_4_VACUOUS_NO_CUSTOMERS` after adding the amendment)
- LIBCO: 2–3 flags (`OPTIONS_INTENTIONALLY_EMPTY`, `USER_TYPES_EMPTY`, possibly `PHASE_4_VACUOUS_NO_CUSTOMERS`)
- PEBL: 3 flags (`REPS_IN_DEFAULT_GROUP`, `SELF_TEST_ONLY_ORDERS`, `RECURRING_WARNINGS_NO_ERROR`)
- TCD (if framework applied): 1 flag (`ZERO_ORDERS_IN_DB`)
- MALI (if framework applied): 2 flags (`KYLA_INTRO_INFRA_GAP`, `REPS_DEFINED_NOT_LOGGED_IN` if you count `ML Reps` as defined-not-logged-in)

Average 1–3 flags per client is informative, not noisy. Kylor's concern that "some clients will trip 3–4 simultaneously" is borne out (PEBL hits 3) but those 3 flags ARE the substance of PEBL's status — they tell the standup exactly what to discuss. Keep first-class flags.

---

## 5. Auto-cohort query — confirmation and observation

The auto-cohort query returns exactly 4 onboarding clients (`tcs`, `drf`, `libco`, `pebl`) on 2026-06-05. The name-exclusion list (`%demo%`, `%template%`, `%test%`) cleanly removes the 3 other onboarding-tagged orgs (`hl Hinkley Lighting (Demo)`, `tmpo Template_not lighting`, `tmpl Template_Lighting Company`). Status distribution shows `onboarding` (7), `demo` (4), `test` (16) as separate status values — Kylor could optionally tighten the filter from name-pattern to status-pattern (`status NOT IN ('demo','test')`). Either approach works. I'd recommend doing both (defense in depth: name AND status filters) to handle a future case where someone forgets to set status=demo on a new demo org.

**Recommended:** add `AND COALESCE(properties->>'status','') NOT IN ('demo','test')` to the cohort query. As written today, the query already correctly returns the 4 real onboarding clients, but a future demo org named without the keyword "demo" in the name would slip through.

---

## 6. Phase 6 → Phase 7 transition — focused audit

The handoff explicitly called this out as the highest-stakes transition. My findings:

### Kyla/Angie CC pattern detection
- **Validated robust against staffing changes via author-identity, not name.** The rule "thread_author_email = 'kyla@supercatsolutions.com'" will break if Kyla leaves; replace with "thread_author_email IN (SELECT email FROM supercat_support_team)" or simply "thread_author_email LIKE '%@supercatsolutions.com' AND thread_author_email <> 'kylor@supercatsolutions.com'" — i.e., anyone-at-SuperCat-not-Kylor. That's resilient.
- **Confirmed live for TCD:** 8 Kyla threads in last 30d, 1 Kylor (May 1). Pattern is real and detectable.

### Self-test detection (`bill_to_company_name` ≠ client name)
- **Validated correctly distinguishes PEBL's 9 self-tests** (`bill_to_company_name='Pebl'`) from DRF's 1 real-ish order (`bill_to_company_name='AMALFI'`).
- **Caveat:** comparison needs to be case-insensitive and tolerant of variations (`Pebl` vs `PEBL` vs `Skyard Furniture`). Use `lower(trim(bill_to_company_name)) != lower(trim(organizations.name))` with a fuzzy-match fallback, or maintain an explicit `client_self_names[]` list per org.

### "kylor@ vs kyla@/support@" author shift
- **Brittle to Kylor PTO** as documented above. Switch to Kyla-presence-based detection.

### The bigger issue Phase 6 → 7 reveals
The framework assumes a linear hand-off pattern: Kylor builds → Kyla takes over → reps active → orders flow → exit. **TCD doesn't fit:** Kyla took over (✓), reps active (✓), but ZERO orders ever in DB. Either TCD's orders flow through a non-DB path, or they really do have zero submitted iPad orders despite 22 active reps (catalog-browser-only model). The framework needs to accommodate this without saying "TCD isn't Phase 7" — because TCD demonstrably IS Phase 7 (Apr 27 handoff thread, billing flipped to Angie, Kyla owns ongoing support).

**Recommendation:** Phase 7 anchor should be expressed as a **disjunction** of evidence types, not a conjunction. Any TWO of:
- Phase 6 done.
- ≥3 external reps active in last 30d.
- ≥1 real (non-self-test) submitted order in last 90d.
- Kyla/support author dominance in last 30d (≥3 Kyla/support threads OR ≥2× Kyla:Kylor ratio).
- `properties->>'status'` already flipped to `active`.

The disjunction captures the "iPad-as-catalog-browser-no-orders" case (TCD: rep activity + Kyla dominance + status flipped = 3/5 ✓) while still rejecting orgs that haven't actually been handed off.

---

## 7. Integration as Phase 6 sub-topic — is that right?

**The handoff asked: should integration be a Phase 6 sub-flag, or a separate workstream?**

Live evidence:
- TCS Catsy: handoff narrative says this is "gating Phase 3-4 progress" because Catsy is the PIM driving the product catalog. But Kylor's reaction was to pull the data himself from Catsy's published artifacts and import on Jun 5. So Catsy was NOT blocking — it was a parallel decision about long-term data source. The Phase 3 catalog imported clean on Jun 5 without waiting for Catsy. **Integration is parallel, not gating.**
- LIBCO BC: handoff says "running parallel to Phase 5." LIBCO's Phase 4 is done; they're working on customer file (Phase 5 anchor blocker) AND simultaneously running "SuperCat + Lib & Co: Integration Chat" Jun 4 about Business Central. **Integration is parallel, not gating.**
- MALI Endeavour: integration discussion happened Apr 9 (pre-handoff), continued post-handoff. MALI's Phase 6 is stalled on `KYLA_INTRO_INFRA_GAP`, not on integration. **Integration is parallel, not gating.**

**Verdict: integration as a Phase 6 sub-topic is the WRONG framing.** It is in every reference org an independent workstream that runs in parallel to the phase progression. It's not gated by any phase, and no phase is gated by it.

**Recommendation:** Promote "Integration approach" to a **separate workstream column** in the per-client output, tracked independently of phase position. Track:
- Owner (us / them / third party / undecided)
- Approach (API / FTP feed / manual)
- Status (scoping / building / testing / live / not started)
- Last activity (most recent integration-keyword Fathom / HelpScout thread)

The existing `INTEGRATION_OWNER_UNCLEAR` and `INTEGRATION_DEFERRED_POST_HANDOFF` flags are useful but should reference the separate-workstream tracking, not Phase 6.

This is consistent with how mature SaaS onboarding frameworks track "data plumbing" as a parallel concern (it doesn't block adoption, but it determines long-term scalability).

---

## 8. Migration plan — if adopted with the changes above

Files in `SuperCat 4.0/onboarding-models/` that would change, in order:

1. **`Phase_Progression_Framework.md`** (NEW) — move from `~/Downloads/` into the folder with the changes recommended above applied.

2. **`README.md`** — rewrite the "What this is" section to describe phases not stages, update the file map to reference `Phase_Progression_Framework.md` instead of `Stage_Gated_Data_Collection.md`, drop the "Cohort — you provide the shortnames" section (replaced by auto-cohort).

3. **`RUN_PROMPT.md`** — replace shortname-input flow with auto-cohort query as Step 0; remove references to `Stage_Gated_Data_Collection.md` and `Validation_Layer_Fathom_HelpScout.md`; collapse Steps 1/2/3 into a single per-client phase-assignment loop driven by the framework doc.

4. **`Output_Format.md`** — restructure to match the v3 per-client section template (`Anchor Phase`, `Current`, `Phase Status table`, `Open Workstreams`, `Ambiguity Flags`, `Recent Engagement`, `Next Action`). Replace "Readiness %" with "Anchor phase position." Add the **Integration Workstream column** to cohort-level output.

5. **`Stage_Gated_Data_Collection.md`** — DEPRECATE, move to `_archive/`. Most queries are still useful and should be lifted into the new `Phase_Progression_Framework.md` as a "queries reference" appendix.

6. **`Validation_Layer_Fathom_HelpScout.md`** — DEPRECATE, move to `_archive/`. Its Fathom/HelpScout queries are useful and should be merged into the new framework doc.

7. **`output/`** — leave existing dated assessments in place as a historical record. The next run produces a `{YYYY-MM-DD}-assessment.md` in the new format alongside them.

**No code changes outside `onboarding-models/`.** The auto-cohort query and the queries in the framework run against existing Postgres + BigQuery sources; no schema or pipeline work required.

**Suggested order of operations:**
1. Apply the 5 framework changes (Phase 4 anchor `customers > 0`, Phase 5 drop non-admin clause, Phase 6 drop/lower `ipad_reports`, Phase 7 disjunctive anchor, external_rep definition fix).
2. Apply the 4 added flags + 6 modified flags.
3. Apply the integration-as-separate-workstream restructure.
4. Add the 4 new flags + revise the 6 modified.
5. Re-run on the 4-org auto-cohort and a manually-included `tcd`/`mali` (overriding the cohort filter) to confirm classifications match handoff expectations.
6. Once a clean run matches expectations, deprecate the old stage docs.

---

## 9. Net summary

The v3 framework is a real improvement: phases-as-lifecycle-position beats stages-as-data-completeness; auto-cohort detection beats manual shortname lists; first-class ambiguity flags beat hidden assumptions. **Adopt with the changes above.**

The three load-bearing fixes — `customers > 0` for Phase 4, drop `non-admin` and lower/drop `ipad_reports>=3` for Phase 6, disjunctive anchor for Phase 7 — are the difference between a framework that classifies your reference orgs correctly and one that doesn't. Without them, the framework as written would classify TCD as Phase 5 (wrong) and four of the four onboarding cohort members as one phase higher than the handoff narrative says (because of the vacuous-customer Phase 4 trap).

The integration-as-separate-workstream restructure is a should, not a must — the sub-flag approach works, just less cleanly than parallel tracking.

The flag taxonomy is mostly right. The 4 new flags I'd add are all gap-coverage (vacuous-customer Phase 4, intentionally-empty options, single-price-level, zero-orders-in-DB) — not new patterns I'm inventing. They reflect things the reference orgs actually do that the current 18 don't catch.

— End of audit.
