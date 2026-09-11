# Phase Anchors

This file defines the 7 phases of the SuperCat onboarding lifecycle. See `Phase_Progression_Framework.md` for the change log and `RUN_PROMPT.md` for execution. The ambiguity-flag taxonomy lives in `Flags_and_Signals.md`; the phase-assignment algorithm and output structures live in `Output_Contract.md`.

> **Done-when convention.** Most phases below carry a separate `**Done when:**` block immediately after the Anchor. Phase 4 and Phase 7 are exceptions — for those two, the Anchor block IS the Done-when (Phase 4 uses `**Anchor (all must be true):**`, Phase 7 uses `**Anchor — disjunctive (any TWO of the following are true):**`). When evaluating a phase, treat the Anchor block as the Done-when whenever no separate Done-when block is present.

## The cohort — auto-detected

Replace the manual shortname list with a postgres query. The `organizations.properties->>'status'` field is reliable and well-populated.

```sql
SELECT o.shortname, o.name, o.created_at
FROM organizations o
WHERE o.properties->>'status' = 'onboarding'
  AND o.name NOT ILIKE '%demo%'
  AND o.name NOT ILIKE '%template%'
  AND o.name NOT ILIKE '%test%'
  AND COALESCE(o.properties->>'status','') NOT IN ('demo','test')
ORDER BY o.created_at DESC
```

The first `status='onboarding'` filter and the second `status NOT IN ('demo','test')` belt-and-suspenders are intentional: the first selects the cohort; the second is defense-in-depth against a future status taxonomy change that could let a demo/test org through.

As of 2026-06-05 this returns: `tcs`, `drf`, `libco`, `pebl` (the 4 real onboarding clients). Status `onboarding` also tags `hl` (Hinkley Demo), `tmpo`, `tmpl` — caught by the name exclusions. Live clients (TCD, MALI) carry `status='active'` and correctly fall out of the cohort, matching the v3 rule that Phase 7 is terminal.

HubSpot is dropped as a cohort source. It can still feed Phase 1 readiness metadata (the onboarding readiness fields), but is not authoritative for who is in the cohort.

## Resolving `client_domains[]`

`client_domains[]` is used by every Fathom / HelpScout / rep filter downstream. Build it from customer-facing identifiers, NOT from admin email aggregation (which is contaminated by personal-email admins, e.g. `kylor22johnson@gmail.com` on TCD).

Resolution order — **the first non-empty SOURCE wins outright; within that one source include all of its distinct non-personal domains; do NOT merge domains across sources** (v3.4 — the old "first non-empty wins; concatenate non-empty results" wording was self-contradictory: it said both "stop at the first source" and "combine sources." Pick one source, take everything it has):

1. Explicit per-client override in `onboarding-models/overrides.toml § client_domains` (a committed map of shortname → domain list). If listed, use that list verbatim and stop — it is authoritative.
2. `organizations.order_email_recipient` domain, if set and not a placeholder.
3. ~~HubSpot company primary domain~~ — **REMOVED 2026-08-18.** HubSpot resolves 3 of 7 clients (`drf`/`libco`/`tcs` have no `hubspot_company_id` in `insightful_product.org_master`; `leg`'s points at a company row that no longer exists). Postgres alone resolves 7 of 7 via steps 2 and 4. Do not reintroduce it.
4. **Fallback only:** admin `org_users.users.email` domains, EXCLUDING the personal-email providers below. If the fallback returns ≥2 distinct non-personal domains, emit `MULTI_DOMAIN_FALLBACK_UNVERIFIED` (`Flags_and_Signals.md § B`) to surface the second domain for standup verification; do not silently absorb it. Once a second domain is confirmed a real parent/DBA, add it to `overrides.toml § client_domains` so source 1 short-circuits the fallback on future runs and the flag stops recurring.

**Personal-email providers — never treated as client_domains, regardless of source:**

```
gmail.com, yahoo.com, outlook.com, icloud.com, hotmail.com, me.com, aol.com, fuse.net, proton.me, protonmail.com
```

## Sources

| Source | MCP | Used for |
|---|---|---|
| Postgres | `user-supercat-postgres-vpn` | All eCat config: products, customers, options, price_levels, inventory, ipad_reports, orders, user_types, org_users (rep classification), `import_events`, cohort detection |
| BigQuery — `onboarding_assessment.fathom_recent_meetings` | `user-bigquery-admin` | Meeting titles/dates/`external_domains[]`/`invitee_emails[]`/`summary` |
| BigQuery — `onboarding_assessment.helpscout_tickets` | `user-bigquery-admin` | Tickets denormalized to ticket × thread with `thread_created_at`, `thread_created_by_type`, `thread_author_email`, `thread_body`, `primary_customer_domain`, `tags` |
| BigQuery — `mixpanel.events` | `user-bigquery-admin` | `event_name='order_submitted'` for rep activity (90d window) |

## The 7 phases

| # | Phase | The question |
|---|---|---|
| 1 | Discovery / Kickoff | Have we kicked off this client? |
| 2 | Initial Import | Has at least the products file been imported? |
| 3 | Progress | Is more than one core file in, with no fatal errors on the most-recent of each? |
| 4 | Catalog Completeness | Is the catalog actually buildable as a live iPad? |
| 5 | Reps Signed In | Are reps (in custom user_types) actually logging into the iPad? |
| 6 | Admin Training | Has the admin been trained, with ongoing-ops covered? |
| 7 | Go-Live (terminal) | Has the formal handoff to support happened, with ongoing client activity? |

## Counting HelpScout threads (v3.6, 2026-08-18)

Every rule that counts threads must apply both of these first. They were added because
TCD's Phase 7 clause 4 fired at **100% non-Kylor on a denominator of 2** — a single Kyla
reply satisfying a rule meant to detect a support handoff.

**1. Deduplicate tickets.** The same conversation is captured under several ticket
numbers. For TCD, **21 of 31 tickets collapse to 9 distinct conversations** — worst case
"terracotta onboarding kickoff follow ups" exists as 13421, 13448 and 14280 across 69
threads. Collapse on the subject with a leading `re:` / `fwd:` / `fw:` stripped and
lowercased, before counting anything.

This matters beyond arithmetic: one of TCD's duplicated subjects is
`"welcome to supercat support, next steps: admin training"` — the Phase 6 qualitative
trigger regex, counted twice from one email.

**2. Apply a volume floor.** A ratio over fewer than 5 deduplicated threads is not a
signal. Emit `INSUFFICIENT_THREAD_VOLUME` naming the actual count rather than firing or
silently failing the clause.

## Phase regression — the at-risk state (v3.6, 2026-08-18)

**A phase is not a ratchet.** Anchors are evaluated against a rolling window, so a
client that stops sending files can stop satisfying a clause it previously satisfied.
The framework must say so rather than silently holding the old phase or quietly
reporting a lower one.

Rule:

- Record the highest phase ever reached (`phase_high_water`) alongside the phase whose
  anchor passes today (`phase_current`).
- If `phase_current < phase_high_water`, report
  **`Phase <high_water> — AT RISK (regressed to <current>)`** and raise
  `PHASE_REGRESSED` naming the clause that stopped passing and the date it last passed.
- Never report a bare lower phase. "TCD moved from 3 to 2" reads as a data error;
  "TCD is at risk, Phase 3 clause 1 has failed since 2026-02-20" reads as the escalation
  it actually is.

**Why this exists — the verified case.** TCD's `core_types_60d` (Phase 3 clause 1,
which needs >=2) ran: 3 on 2026-01-15, 2 on 2026-02-01, **1 through all of March 2026**,
back to 2 on 2026-04-01. That is a real failure of a real clause for roughly six weeks.

Independently, a blind read of the same client's Fathom + HelpScout record — with no
access to these metrics — placed a near-churn at 2025-12-27 to 2026-04-19, evidenced by
the client writing that eCat "feels less like a mature commercial product and more like
an early-stage amateur implementation." **Two methods with no shared evidence converged
on the same window.** The signal was present in the data the whole time and v3.5 had no
way to express it. See `ground-truth/SCORECARD.md` § D1.

An at-risk client is the single most actionable output this framework can produce.
Do not let it be the one thing it cannot say.

## Phase 1 — Discovery / Kickoff

**Question:** Have we kicked off this client?

**Anchor (any one is sufficient):**
- Postgres `organizations` row exists AND `properties->>'status' = 'onboarding'`.
- Fathom meeting where `external_domains` intersects `client_domains[]` (title-agnostic — kickoff Fathoms use too many variant titles to regex reliably).
- HelpScout thread where `thread_author_email = 'kylor@supercatsolutions.com'` AND `thread_body` matches `(?i)kickoff|welcome.*supercat|next steps:?\s*admin training|next steps.*(import|onboarding)` AND `primary_customer_domain` intersects `client_domains[]`.

**Done when:** the org row is non-disabled AND ANY external touchpoint (Fathom OR HelpScout) exists with `external_domains` / `primary_customer_domain` intersecting `client_domains[]`. No timing constraint relative to `created_at` — verified live: PEBL was provisioned 2025-07-24 but the project formally started 2026-01-24 (HS #13879). A timing window keyed off `created_at` would falsely block PEBL despite 57 threads of evidence. The domain-intersection requirement is the load-bearing constraint; timing isn't needed.

**Rationale for change:** v3.0's `(?i)\bkickoff\b` Fathom regex matched only 2 of the 6 reference orgs (TCS, LIBCO). DRF/PEBL/MALI/TCD use titles like "Discovery Call", "Implementation Check-In", "Onboarding Working Session", "Scott / SuperCat" — none contain "kickoff" verbatim. Replacing the keyword with "any Fathom whose `external_domains` intersects `client_domains[]`" captures all of them. Phase 1 Done-when then enforces the touchpoint existence (Fathom OR HelpScout) without imposing a fragile timing window.

## Phase 2 — Initial Import

**Question:** Has at least the products file been imported?

**Anchor (required):**
- ≥1 row in `import_events` for this org whose `data::text` contains a Products block AND that row's body does NOT match `:fatal`.

```sql
-- The verified YAML shape: top-level keyed lists, e.g.
--   ---
--   - - Products
--     - - - :warning
--         - 'Line 1: Custom field ''Certification'' is missing.'
-- Use `data::text ILIKE '%- - Products%'` to match a Products block specifically.
-- A single import_events row may contain multiple top-level blocks
-- (Products + Inventory + Stories, etc.) — see Phase 3 for block-level parsing.
```

That's it. There is no programmatic "did the client send the file" signal — we can't see that. The import event IS the proxy. A warnings-only or even errors-but-not-fatal first import counts.

**Done when:** the most-recent products `import_events` row has no `:fatal` token AND `total_products` (`products` where `deleted = false`) > 0.

**Phase-2 health (graded but not gating):** product count; whether the import threw `:error` or only `:warning`.

## Phase 3 — Progress

**Question:** Is more than one core file imported, with no fatal errors on the most-recent of each?

**Anchor (all must be true):**
- ≥2 of {`Products`, `Customers`, `Options`, `Inventory`, `Product Stories`} have at least one import event in last 60d.
- For **every** file type that has any event, the **most-recent block** of that file type does NOT match `:fatal`. (Per llms.txt: Fatal = entire file rejected, nothing changes. Errors and warnings are tolerable here.)
- At least half of products have an image: `count(products where image_exists = true) / count(products where deleted = false) >= 0.5`.

**Most-recent-per-file rule (block-level):** an `import_events` row may contain multiple top-level YAML blocks (e.g. `- - Products`, `- - Inventory`, `- - Product Stories` in the same row). Resolve "most-recent" at the YAML-block level — for each file type, find the most recent row whose body contains that file type's block, and inspect THAT block (not the row's entire body) for `:fatal`/`:error`/`:warning`. Row-level "most recent" alone will miss the case where today's row has clean Inventory but a stale row had a fatal Products import. **Do not rely on a fixed recent-row window of `import_events` (e.g. the 30 most-recent rows) — image-import events dominate the recent history for image-heavy orgs and hide core-file events. See `RUN_PROMPT.md § Step 1 — Import events` primitive for the per-file-type query that materializes this rule.**

**Done when:** anchor passes AND the products file's most-recent block is not Fatal AND (≥2 price_levels exist OR Net-Price-only mode is confirmed). Net-Price-only is "confirmed" when the org's shortname is listed under `net_price_only_confirmed:` in `onboarding-models/overrides.toml` (a small committed config — no DB write needed). If the org has exactly 1 price level and is NOT listed there, this requirement is unmet and `SINGLE_PRICE_LEVEL_UNCONFIRMED` fires for standup. Once confirmed (shortname added to `overrides.toml`), single net pricing satisfies this clause and the flag stops recurring.

**Phase-3 health (graded):**
- most-recent block tier per file type;
- image coverage %;
- `visible_products_pct = count(products WHERE deleted=false AND COALESCE(hideable,false)=false) / count(products WHERE deleted=false)` — informational (catches the "imported but hidden via Hideable strategy" pattern that TCD exhibits);
- customer count (informational, not gating);
- count of customers whose `default_price_code` doesn't resolve to a real `price_levels.code` (flag for standup).

**Common ambiguity:**
- Org has exactly 1 price level and no explicit confirmation of Net-Price-only mode → `SINGLE_PRICE_LEVEL_UNCONFIRMED` flag. Cannot programmatically distinguish "real single-tier pricing" from "pricing not yet finished." Standup decides.

## Phase 4 — Catalog Completeness

**Question:** Is the catalog actually buildable as a live iPad?

**Anchor (all must be true):**
- Phase 3 is **Done** — its `Done when` clause passes (anchor sub-bullets AND the ≥2 `price_levels` OR confirmed Net-Price-only requirement), not merely the Phase 3 Anchor sub-bullets. A single-price-level org with `SINGLE_PRICE_LEVEL_UNCONFIRMED` open does NOT clear this clause even if the rest of Phase 4 holds.
- `total_customers > 0`. (Closes the vacuous-pass loophole: with zero customers, the DPC-resolution check below is trivially true and Phase 4 falsely advances. Verified live: TCS/LIBCO/PEBL all sit at 0 customers; this clause keeps them at Phase 3 until customers actually exist.)
- Image coverage ≥50% (per spec — no per-segment thresholds; half is the floor).
- Most-recent products block is `:warning`-only or clean (no `:error`).
- Every customer's `default_price_code` resolves to a real `price_levels.code` for ≥99% of rows. (1% tolerance for ERP placeholders the client can clean up.)
- If `option_groups count > 0` then `options_count > 0` must also hold (no empty option scaffolding). If `option_groups count = 0` this clause passes vacuously — surface via `OPTIONS_INTENTIONALLY_EMPTY` flag. (Restated in v3.2 from the original "any product references `OptionSet1..N`", which is not queryable — no such column exists in Postgres; `products.options` is always `--- :custom: false`.)
- HelpScout has no thread with `ticket_status = 'active'` whose subject or recent body matches `(?i)import error|missing|wrong price|catalog.*broken` filed by the client (`thread_created_by_type='customer'`) in last 14d.

**Phase-4 health:** image coverage % (over the 50% floor); products with no `Price_<code>` populated where org has imported price levels; open HelpScout tickets with import-related keywords.

**Common ambiguity:**
- Phase 4 anchor blocked solely by `customers = 0` → `PHASE_4_VACUOUS_NO_CUSTOMERS` flag explains the hold to the standup.
- Org has `options_count = 0` AND `option_groups count = 0` → `OPTIONS_INTENTIONALLY_EMPTY` flag confirms by-design per-SKU model (LIBCO lighting, DRF fabric).

## Phase 5 — Reps Signed In

**Question:** Are reps (in custom user_types) logging into the iPad?

**Definition of "rep" (the corrected, contamination-free one):**

```sql
is_admin = false
AND user_type.name <> 'DefaultUserGroup'
AND email NOT LIKE '%@supercatsolutions.com'
AND COALESCE(disabled, false) = false
```

`client_domains[]` is **not** an exclusion filter in this rule. It's used only to compute the informational `rep_subtype`:

- `external` — domain not in `client_domains[]` AND not in the personal-email-providers list.
- `in_house` — domain in `client_domains[]` (W-2 reps on the client's own domain — common in manufacturer-direct sales).
- `personal_email` — domain in the personal-email-providers list (gmail.com, yahoo.com, etc.).

All three subtypes count toward the Phase 5 anchor. The breakdown is reported in health, not used for gating.

**Rationale for the contamination fix:** v3.0 used `lower(split_part(email,'@',2)) NOT IN (client_domains[])` as an exclusion filter. Verified live, this dropped 8 of TCD's 22 active sales reps because Kylor's personal `kylor22johnson@gmail.com` admin contaminated TCD's `client_domains[]` with `gmail.com`. It also structurally excluded MALI's in-house reps on `@magiclite.com`/`@nslusa.com`. Both bugs are fixed by removing the exclusion from the gating rule and reporting subtype as a downstream attribute.

**Anchor (all must be true):**
- ≥1 `rep` row exists (any subtype).
- ≥1 `rep` has `last_ipad_login_at IS NOT NULL` (ever logged in).
- ≥1 `rep` has `last_ipad_login_at >= NOW() - INTERVAL '30 days'` (active in last 30d).

**Done when:** anchor passes.

**Rationale for dropping the order-from-non-admin clause:** v3.0 required "≥1 submitted order in `orders` from a non-admin org_user." Verified live, every order in `orders` across the 6 reference orgs is from `is_admin=True` — onboarding admins (Suzanne at DRF, sales04 at PEBL) ARE the ones exercising the order path during onboarding. The clause was unable to fire for any client. Order-path-exercised is now a Phase 7 signal where it correctly distinguishes self-tests from real customer orders.

**Phase-5 health:**
- `rep_count` by subtype (`external` / `in_house` / `personal_email`);
- count ever-logged-in;
- count active in last 30d;
- submitted orders count by org_user (admin and non-admin, real and self-test) — informational only.

**Common ambiguity:**
- rep defined but not logging in → rep-onboarding stalled (MALI pattern) → `REPS_DEFINED_NOT_LOGGED_IN`.
- user_types defined but no users in them yet (LIBCO pattern) → `USER_TYPES_EMPTY`. Not Phase 5 yet — scaffolded but unfilled.
- non-admin client users logging in but all in DefaultUserGroup (PEBL pattern) → `REPS_IN_DEFAULT_GROUP`. Not Phase 5 — users testing but not in a real group.

## Phase 6 — Admin Training

**Question:** Has the admin been trained, with ongoing operations covered?

**Anchor — qualitative trigger (required, ANY ONE):**
- HelpScout thread where Kylor's reply CCs `kyla@supercatsolutions.com` or `support@supercatsolutions.com` AND thread body matches `(?i)admin training|handoff|primary point of contact|now that your reps`.
- Fathom meeting in last 60d with title matching `(?i)admin training|handoff` AND `external_domains` intersects `client_domains[]`.
- HelpScout thread containing a URL matching `supercat\.supercatsolutions\.com/.*onboarding/|knowledgebase/admin-console` sent FROM a SuperCat author TO a client domain (admin training HTML / llms.txt being shared = handoff signal).
- **Trigger #4 — Support handoff signal:** ≥40% of SuperCat-authored HelpScout threads in the last 30 days are by non-Kylor authors, **and at least 5 such threads exist after deduplication** (see § Counting HelpScout threads). Below the floor, emit `INSUFFICIENT_THREAD_VOLUME` and do not fire the trigger (i.e. non-`kylor@` `@supercatsolutions.com` addresses such as `kyla@`, `support@`). This is the load-bearing post-handoff author-shift signal and is robust to Kylor PTO (it's Kyla-presence-based, not Kylor-absence-based). (Replaces the previous "most recent author is non-Kylor" test, which was too sensitive to a single late reply resetting the signal.)

> **Email-engagement fallback for meeting-dependent signals:** If 0 Fathom meetings exist in the last 90 days but ≥5 HelpScout threads from the client exist in the last 30 days, treat email engagement as equivalent to call engagement for Phase 6 qualitative evaluation. Some clients (e.g., PEBL) interact exclusively via email.

**Anchor — quantitative readiness (required):**
- `organizations.order_email_recipient` is set AND is NOT a placeholder. Placeholder patterns rejected: `%@example.com`, `%test%`, `%@supercatsolutions.com`.
- `user_types` count ≥ 2 (at least one beyond `DefaultUserGroup`). Note: SuperCat-internal user_types like `z-SuperCat` do count toward the threshold — harmless but worth knowing.

**Rationale for dropping `ipad_reports >= 3`:** v3.0 required `ipad_reports >= 3`. Verified live: TCD (canonical Phase 7 exit) has 1; PEBL/LIBCO 1; MALI/TCS 0; DRF 3. The threshold has no basis in the admin-training material (`~/Downloads/index (1).html` covers users, user groups, price levels, and taxonomy display names — not PDF report formats). The clause structurally blocked TCD from advancing through Phase 6 under the v3.0 anchor. Moved to Phase 6 health (`>= 1` is the soft informational signal).

**Done when:** both qualitative trigger AND quantitative readiness pass.

**Phase-6 health (informational, not gating):** `ipad_reports` count; whether `send_order_email_on_submit` is enabled; count of customers without `TerritoryCodes`.

**Common ambiguity:**
- Kyla intro email sent (qual trigger fires) but order_email empty or user_types < 2 → `KYLA_INTRO_INFRA_GAP`. Narrative says "handed off"; infra says "not ready."
- order_email + user_types are set but no Kyla intro thread visible → `INFRA_READY_NO_HANDOFF`. Maybe handoff happened on a call we didn't capture — verify with Kyla.
- Integration discussions still active months after Phase 6 anchor → **not a Phase-6 ambiguity anymore.** Tracked in § Integration Workstream (parallel) within this file.

## Phase 7 — Go-Live (terminal)

**Question:** Has the formal handoff to support happened, with ongoing client activity?

**Anchor — disjunctive (any TWO of the following are true):**

1. **Phase 6 done** (both qual and quant readiness pass).
2. **≥3 reps active in last 30d** (per the Phase 5 rep definition, any subtype).
3. **≥1 real customer order in last 90d** — a submitted order in `orders` whose `lower(trim(bill_to_company_name))` matches an existing `customers` row for this org (`lower(trim(customers.name))` — **the column is `name`; there is no `company_name` on `customers`. Verified against information_schema 2026-08-18; the previous wording threw UndefinedColumn on every Phase 7 evaluation**) AND does NOT match the self-name set (`[organizations.name]` ∪ brand/order-email root ∪ `client_self_names[]`). Requiring a positive match to a real customer is the load-bearing signal; mere mismatch against `organizations.name` is NOT sufficient (it fails unsafe when brand ≠ legal name — see PEBL precedent). Submitter admin or non-admin both fine. **Failure mode is recoverable:** an unmatched order under-advances the client (recoverable next run) rather than false-advancing them to terminal Go-Live.
4. **Kyla-presence author dominance in last 30d** — ≥40% of SuperCat-authored HelpScout threads in the last 30 days are by non-Kylor authors, **with a minimum of 5 deduplicated threads** (see § Counting HelpScout threads); below that, the clause does not fire (non-`kylor@` `@supercatsolutions.com` addresses). (Same rule as the Phase 6 4th qualitative trigger; reused here because Phase 7 also wants to see ongoing non-Kylor SuperCat correspondence. Replaces the previous "most recent author is non-Kylor" test.)

`organizations.properties->>'status' = 'active'` is **not** a Phase 7 anchor clause. It is the cohort-exclusion mechanism (a status flip removes the org from auto-cohort and from further weekly assessment) — but it is operator-set and noisy. Verified live: MALI has `status='active'` while being stalled at Phase 6 (`order_email_recipient` empty, 0 reps migrated). If status were a clause, MALI would falsely advance to Phase 7 on {Kyla-presence + status} = 2-of-5. Status is treated as a routing signal only.

**Rationale for the disjunctive anchor:** v3.0 required all of {Phase 6 done, non-admin order with non-self bill_to, kylor-vs-kyla author shift}. Verified live, this failed for TCD — the canonical Phase 7 exit — because TCD has 0 rows in `orders` despite 22 active reps (iPad-as-catalog-browser pattern; orders submitted via legacy channels). The disjunctive any-two-of-four anchor captures TCD via {Phase 6 done + rep activity + Kyla dominance} = 3/4 ✓, while correctly rejecting MALI (only Kyla-dominance fires → 1/4 → does not exit).

**Author-shift signal — Kyla-presence-based (robust to PTO):** count threads from non-`kylor@` `@supercatsolutions.com` authors. Do NOT use "absence of kylor@" as the trigger — when Kylor is on PTO every client's correspondence skews non-Kylor by default and the rule produces false positives. The presence-based formulation requires Kyla/support@ to be actively engaging, which is the actual handoff signal.

**Self-test handling under the allowlist model (Phase 7, clause 3):** clause 3 requires a positive match against an existing `customers` row, so self-tests naturally fail to satisfy clause 3 without needing an alias denylist. If `client_self_names[]` is set in `onboarding_assessment.client_self_names`, it is used as an additional exclusion — a `customers` row whose name appears in the self-name set is treated as a self-name match and does NOT satisfy clause 3. PEBL's 9 `bill_to_company_name='Pebl'` orders: 0 customers exist for PEBL, so no order can match a customer row → clause 3 does not fire (fail-safe). Suspicious admin orders that don't match any customer are surfaced via `SELF_TEST_SUSPECTED_NOT_CUSTOMER` (`Flags_and_Signals.md § F`). **Rationale for the allowlist (v3.2 change):** v3.1 used a denylist (`bill_to != organizations.name`) that failed unsafe — PEBL's brand "Pebl" differs from legal name "Skyard furniture Co Ltd.", so 9 self-tests scored as real orders and erroneously fired clause 3. PEBL avoided false Go-Live only because clauses 2 and 4 didn't fire. Requiring a real customer match removes dependence on a hand-maintained alias table and couples clause 3 structurally to Phase 4 (`customers > 0`) — a 0-customer org is now structurally incapable of false-firing clause 3.

**Outcome:** client exits the framework. `properties->>'status'` should be flipping to `active` around this time. Remove from next run's cohort. Any post-live concerns belong to a separate post-live health framework.

**Common ambiguity:**
- Phase 7 anchor passes via clauses {1, 2, 4} (Phase 6 done + reps + Kyla-presence) without clause 3 firing AND `orders` count = 0 → `ZERO_ORDERS_IN_DB` flag. Captures the iPad-as-catalog-browser pattern (TCD live example). Standup confirms whether orders flow through a legacy channel or are genuinely missing.

---

## Integration Workstream (parallel)

Integration is tracked as a **parallel workstream**, independent of phase position. In no case does integration gate or get gated by a phase. The first question is not "what are they discussing?" but **"did the client buy an integration from us, and whose job is it?"** — and that is answered authoritatively by the **HubSpot deal line items**, not by inferring from meeting keywords.

### Source of truth: the HubSpot deal line items (v3.3)

For each client, match the org to its HubSpot company by domain, find the associated deal(s), and read the line-item names (`hubspot.deal` → `hubspot.line_item_deal` → `hubspot.line_item`; the exact query is the integration primitive in `RUN_PROMPT.md § Step 2`). SuperCat sells exactly three integration postures, and the line item tells you which:

| Line item on the deal | Posture | Owner | How to report it |
|---|---|---|---|
| `Managed Integration Build` and/or `Managed Integration Hosting` | **Managed** — we build and run it (SLA) | **us** | **Show** the Integration row + block; this is our workstream to track. |
| `Certified Pipeline` | **Certified** — client/their vendor builds it, we certify | **them** | **One informational line only** ("Client is building their own integration; we certify it"). Do NOT show an open SuperCat workstream; do NOT raise an ownership flag. |
| *(none — self-serve FTP is the included default)* | **Self-serve** | **client** | **Suppress entirely.** No Integration row, no block, no flag. There is nothing for us to track. |

If a client has multiple deals, the **highest posture present wins** (Managed > Certified > none). Approach detail (Business Central / NetSuite / Catsy / API / FTP) is enriched from the most recent integration-keyword Fathom/HelpScout, but **Owner is set by the line item, never by inference.**

### Status and last activity (only when we show the block)

| Field | Source | Values |
|---|---|---|
| Owner | HubSpot deal line item (table above) — authoritative | `us` / `them` / `client` |
| Approach | Enriched from Fathom `section_titles` / HelpScout body keywords (color only) | `API` / `FTP feed` / `manual` / `PIM (Catsy, etc.)` / `Business Central` / `unset` |
| Status | Recorded per shortname in `onboarding-models/overrides.toml § integration_status` (committed config; `unset` if absent — there is no `integration_workstream` DB table). A managed client with no entry here raises `INTEGRATION_OWNER_UNCLEAR`. | `scoping` / `building` / `live` (free-form note alongside) |
| Last activity | Most recent Fathom OR HelpScout matching the integration keyword regex below | timestamp + source (`fathom` / `helpscout`) |

**Integration keyword regex** (for *last-activity* enrichment only — not for ownership):

```
(?i)integration|business central|netsuite|pim|api|odoo|catsy|endeavour|endeavor|truly smb|trulysmb
```

**Flags that reference integration** (`INTEGRATION_OWNER_UNCLEAR`, `INTEGRATION_DEFERRED_POST_HANDOFF`) point at this workstream, and now fire **only for Managed (us-owned) integrations** — see `Flags_and_Signals.md § D`. A Certified or self-serve client never raises an integration flag.

The Integration column/row appears in the cohort-level and per-client output **only when Owner = us (Managed)** (a one-line informational mention is allowed for Certified). It is reported but does not influence Anchor / Current phase computation.
