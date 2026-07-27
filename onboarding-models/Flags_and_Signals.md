# Flags and Signals

This file defines the ambiguity flag taxonomy. Every flag must have a trigger, a source, and (where the trigger requires) a verbatim quote. See `Phase_Anchors.md` for what a phase IS; this file is about edge cases between or within phases.

## Hard rules (non-negotiable)

- No metric without a tool call. No estimates / `~` / "approximately."
- No inference from prior knowledge or user-provided docs.
- Failed query → `❓ QUERY FAILED: [error]`. Never substitute.
- BigQuery is `SELECT`-only against source data.
- Verifiable-quote rule: every quote in a flag must appear verbatim in the retrieved `summary` / `thread_body` text. No reconstruction.
- No-activity certification: "no Fathom" / "no tickets" requires running the matching query and getting zero rows. Never an assumption.

## Ambiguity flags (the standup agenda)

These are the patterns the agent must raise for the weekly standup. Each flag includes the client, the contradicting signals, and a one-line "what to discuss." There is no "right answer" the agent picks — humans resolve these.

### Actionable vs informational (v3.2 — feeds the Confirmed bucket)

Every flag below is one of:

- **Actionable** — fires on a state that blocks phase advancement, requires a data/config fix, or requires a standup decision. Disqualifies a client from the cohort-level "✅ Confirmed (no actionable flags)" bucket (`Output_Contract.md § Cohort-level output`).
- **Informational** — surfaces a state for awareness; either by-design (e.g. confirmed per-SKU model), borderline-threshold, or a noise-reducing guard. Does NOT disqualify from the Confirmed bucket.

| Flag | Section | Type |
|---|---|---|
| `KYLA_INTRO_INFRA_GAP` | A | actionable |
| `INFRA_READY_NO_HANDOFF` | A | actionable |
| `REPS_DEFINED_NOT_LOGGED_IN` | A | actionable |
| `USER_TYPES_EMPTY` | A | actionable |
| `REPS_IN_DEFAULT_GROUP` | A | actionable |
| `SELF_TEST_ONLY_ORDERS` | A | actionable |
| `IMPORT_VS_HELPSCOUT_DRIFT` | B | actionable |
| `HELPSCOUT_QUIET_POSTGRES_QUIET` | B | actionable |
| `HELPSCOUT_ACTIVE_POSTGRES_QUIET` | B | actionable |
| `KYLOR_DOMINATES_POST_HANDOFF` | B | actionable |
| `MULTI_DOMAIN_FALLBACK_UNVERIFIED` | B | informational |
| `IMAGE_COVERAGE_BORDERLINE` | C | informational |
| `DPC_MISMATCHES_LOW` | C | informational |
| `RECURRING_WARNINGS_NO_ERROR` | C | actionable |
| `INTEGRATION_OWNER_UNCLEAR` | D | actionable |
| `INTEGRATION_DEFERRED_POST_HANDOFF` | D | actionable |
| `SINGLE_PRICE_LEVEL_UNCONFIRMED` | F | actionable |
| `OPTIONS_INTENTIONALLY_EMPTY` | F | informational |
| `PHASE_4_VACUOUS_NO_CUSTOMERS` | F | actionable |
| `CUSTOMER_IMPORT_PRICE_CODE_MISMATCH` | F | actionable |
| `ZERO_ORDERS_IN_DB` | F | actionable |
| `SELF_TEST_SUSPECTED_NOT_CUSTOMER` | F | actionable |
| `STALE_OVERRIDE` | F | actionable |
| `PROJECT_START_MISMATCH` | F | informational |

### A. Phase-narrative vs phase-infra mismatch

| Flag | Trigger | What to discuss |
|---|---|---|
| `KYLA_INTRO_INFRA_GAP` | Phase 6 qual trigger fired but `order_email_recipient` is empty/placeholder OR `user_types < 2` | Did handoff actually happen, or was it announced ahead of readiness? |
| `INFRA_READY_NO_HANDOFF` | Phase 6 quant readiness fired but no Kyla intro thread or non-`kylor@` author dominance visible | Did handoff happen on a call we didn't capture? Verify with Kyla. |
| `REPS_DEFINED_NOT_LOGGED_IN` | rep count > 0 but `last_ipad_login_at IS NOT NULL` count = 0 | Rep onboarding stalled — invitations sent but not actioned? |
| `USER_TYPES_EMPTY` | user_types beyond DefaultUserGroup exist but 0 users in them | Scaffolding built; rep migration not run. Whose action? |
| `REPS_IN_DEFAULT_GROUP` | non-admin client users logging into iPad but all in DefaultUserGroup | Custom user_type not yet created — Phase 5 looks closer than it is. |
| `SELF_TEST_ONLY_ORDERS` | ≥1 submitted order AND NO order satisfies Phase 7 clause 3 (no `bill_to_company_name` matches an existing `customers` row for this org per the v3.2 allowlist rule) | Workflow exercised but no real customer orders — Phase 5 yes, Phase 7 clause-3 no. |

### B. Source-of-truth contradictions

| Flag | Trigger | What to discuss |
|---|---|---|
| `IMPORT_VS_HELPSCOUT_DRIFT` | Postgres shows clean (no `:error`/`:fatal` in last 7d) Products imports AND ≥1 client-authored (`thread_created_by_type='customer'`) HelpScout thread in last 7d whose body matches a defect-sentiment pattern `(?i)(wrong\|incorrect\|missing\|broken\|doesn'?t (show\|work)\|not (showing\|working)\|can'?t (see\|find)\|prices?.*(off\|wrong)\|error\|isn'?t (there\|right))` AND does NOT consist solely of a file-attachment/handoff sentence. Bare `import\|upload\|csv` tokens removed in v3.2 — they fired on routine onboarding collaboration (3-of-3 false positives in the 2026-06-08 run). | Either client doesn't see what we shipped, or we missed something. |
| `HELPSCOUT_QUIET_POSTGRES_QUIET` | No client-side HelpScout activity in last 30d AND no `import_events` in last 30d AND not yet Phase 7 | Stalled. Who reaches out? |
| `HELPSCOUT_ACTIVE_POSTGRES_QUIET` | ≥1 client-authored HelpScout thread in last 14d AND no `import_events` rows in last 14d | Conversation moving but no work landing — what's the actual blocker? |
| `KYLOR_DOMINATES_POST_HANDOFF` | Phase 6 anchor fired ≥30d ago but in last 30d `kylor@` replies > non-`kylor@` `@supercatsolutions.com` replies | Handoff didn't take. Does Kyla need re-engaging? |
| `MULTI_DOMAIN_FALLBACK_UNVERIFIED` | `client_domains[]` was resolved via the step-4 admin-email fallback AND yielded ≥2 distinct non-personal domains AND the shortname is not listed under `onboarding-models/overrides.yml § client_domains` | Confirm the second domain is a real parent/DBA, not contamination; once confirmed, add the shortname to `overrides.yml § client_domains` and it short-circuits the fallback (flag stops). (v3.4: override now lives in `overrides.yml`, not a DB table. v3.2 origin — DRF/loomcraft.com case showed the fallback can absorb a legitimate parent OR a contaminant identically; this flag forces human verification before it can silently absorb a wrong domain.) |

### C. Quantitative threshold borderlines

| Flag | Trigger | What to discuss |
|---|---|---|
| `IMAGE_COVERAGE_BORDERLINE` | image_exists / total_products between 0.40 and 0.60 | Is 50% the right threshold for this client? (Band widened from 0.45–0.55 to reduce oscillation noise across consecutive runs.) |
| `DPC_MISMATCHES_LOW` | 1–5 customers with `default_price_code` not in `price_levels` | Worth chasing or accept as noise? (Expected to be quiet — live data shows 100% resolution across reference orgs.) |
| `RECURRING_WARNINGS_NO_ERROR` | Same `:warning` text appears in 5+ consecutive product imports (e.g. PEBL custom-field warnings) | Decide: register the custom field, remove from file, or accept the warning. |

### D. Integration / ownership ambiguity (workstream flags)

| Flag | Trigger | What to discuss |
|---|---|---|
| `INTEGRATION_OWNER_UNCLEAR` | The client's HubSpot deal carries a **`Managed Integration`** line item (Owner = us, per `Phase_Anchors.md § Integration Workstream`) AND no integration status is recorded for the shortname under `integration_status:` in `onboarding-models/overrides.yml`. | We sold a managed integration but aren't tracking the build — record approach/status once in `overrides.yml` and the flag stops recurring. **Does NOT fire for `Certified Pipeline` (client-owned) or no-integration (self-serve FTP) clients** — for those, ownership is already settled by the deal, so there is nothing unclear. (v3.4: status now lives in `overrides.yml § integration_status` — there is no `integration_workstream` DB table; the legacy reference to one made this flag impossible to clear. v3.3: retriggered off the deal line items; the legacy "≥2 integration Fathom meetings" trigger produced false ownership flags on TCS/LIBCO whose ownership the deal already answered. Name kept for continuity; read as "managed integration sold but untracked.") |
| `INTEGRATION_DEFERRED_POST_HANDOFF` | Phase 7 reached AND Owner = us (Managed) AND the shortname's `status` under `overrides.yml § integration_status` is `scoping` or `building` (or unrecorded) | Track separately; not a Phase-7 blocker but standup awareness. |

### E. Phase-skip / out-of-order

`PHASE_SKIP_OBSERVED` is no longer a first-class flag. The phase-assignment algorithm (step 4 in `Output_Contract.md § Phase assignment algorithm`) emits an automatic narrative note whenever a Phase ≥ Anchor+2 has qual or quant signal firing while Anchor+1 hasn't been completed. Keep the observation; drop the flag overlap.

### F. Catalog edge cases (new in v3.1)

| Flag | Trigger | What to discuss |
|---|---|---|
| `SINGLE_PRICE_LEVEL_UNCONFIRMED` | Org has exactly 1 price level AND Net-Price-only mode has not been confirmed. **Confirmation lives in `onboarding-models/overrides.yml` under `net_price_only_confirmed:` (a committed list of shortnames).** If the shortname is listed there, the org runs single net pricing **by design** — do NOT fire this flag; instead treat Phase 3's price requirement as satisfied and note "single net price (confirmed)" as informational. | Only fires when single-price is *unconfirmed*. Confirm once by adding the shortname to `overrides.yml`; it then stops recurring every run (DRF precedent — a single-net fabric model that was being re-flagged weekly). |
| `OPTIONS_INTENTIONALLY_EMPTY` | `options_count = 0` AND `option_groups count = 0`. (There is no `OptionSet1..N` column in Postgres and `products.options` is always `--- :custom: false`; with zero option groups no product can reference one, so the two counts are the complete queryable signal — v3.2 wording.) | Confirms per-SKU model by design (LIBCO/DRF pattern). Suppresses "why are options empty?" from the standup. |
| `PHASE_4_VACUOUS_NO_CUSTOMERS` | Phase 4 anchor would pass if `customers > 0` were removed AND `customers = 0` | Customer file not yet imported — Phase 3 hold reason. Drives "import customers next" action. |
| `CUSTOMER_IMPORT_PRICE_CODE_MISMATCH` | A `customers` import event in the last 30d carries an `:error`/`:fatal` status whose message references a price/`DefaultPriceCode` mismatch — i.e. customer rows point at a price code that isn't an Admin price level (regex on the import message: `(?i)(default[_ ]?price[_ ]?code\|price[_ ]?(code\|level)).*(not (found\|valid\|recognized)\|unknown\|no match\|mismatch\|missing)`). This is the specific cause behind a stuck Phase 3→4: the customer file is *being sent* but the rows are rejected on price codes, so customers never land. | The customer file is failing on price codes — the codes in the file don't match the price levels set up in Admin. Decide: fix the DefaultPriceCode values in the file, or add the missing price level. Distinct from `DPC_MISMATCHES_LOW` (§C), which is about a handful of *already-loaded* customers; this one is the *import itself* being rejected. Distinct from the generic `PHASE_4_VACUOUS_NO_CUSTOMERS` (no customers at all, cause unknown) — surface this instead when the import log names a price-code error. |
| `ZERO_ORDERS_IN_DB` | Phase 7 anchor passes via clauses {1, 2, 4} (any combination not including clause 3) AND `orders` count for this org = 0 | iPad-as-catalog-browser pattern (TCD live example) OR genuine zero-orders stall. Confirm with rep activity. |
| `SELF_TEST_SUSPECTED_NOT_CUSTOMER` | ≥1 submitted order whose `bill_to_company_name` does NOT match the self-name set AND does NOT resolve to a real `customers` row for the org AND submitter `is_admin = true` | Probable self-test the alias/customer match missed (PEBL precedent: `bill_to='Pebl'` vs legal name "Skyard furniture Co Ltd."). Confirms clause 3 should NOT fire; seed `client_self_names` or verify the customer record. (New in v3.2 — pairs with the Phase 7 clause 3 allowlist rule. Distinct from `SELF_TEST_ONLY_ORDERS` (§A) which fires when self-tests are correctly identified.) |
| `STALE_OVERRIDE` | An active override in `overrides.yml` is contradicted by recent external evidence (HelpScout email, Fathom transcript, or import data from the last 30 days). Example: `net_price_only_confirmed: true` for DRF, but a recent client email asks about adding 10 price levels. | Surface for human confirmation — keep or remove the override. The override was correct when set but new evidence suggests the client's situation may have changed. |
| `PROJECT_START_MISMATCH` | `organizations.created_at` is >90 days before the earliest substantive import event (products, customers, or inventory — not just options or test imports), AND no `project_start_date` override exists in `overrides.yml`. | Suggest adding a `project_start_date` to `overrides.yml` so the "days in onboarding" metric reflects the real project timeline instead of the account provisioning date. |
