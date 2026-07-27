# Onboarding Phase Progression Framework

**Version:** 3.0 (Phase-based, qual-integrated)
**Date drafted:** 2026-06-05
**Status:** Proposal — pending fresh-agent audit before adoption.
**Supersedes:** `Stage_Gated_Data_Collection.md` (the old 11-stage ladder).
**Companion docs:** `Validation_Layer_Fathom_HelpScout.md`, `Output_Format.md`, `RUN_PROMPT.md`.

## What this is

A weekly read on every onboarding client answering one question per client:

> Where are they in the onboarding lifecycle, and what is the next concrete thing that has to happen to advance?

Output: one dated markdown file at `output/{YYYY-MM-DD}-assessment.md`.

## What changed vs the old model

- "Stages 1–11" → "Phases 1–7", terminating at Go-Live. Once a client hits Phase 7 they leave the cohort entirely. Post-live monitoring is a separate concern, not this framework's problem.
- The 11 old stages were data-completeness facets graded in parallel; the framework forced them into a linear ladder, which produced "out of sequence" apologies in the v2 output. The 7 phases are an actual lifecycle position. Within a phase, postgres facets are graded; that keeps the quantitative signal without the false-ladder artifact.
- HelpScout + Fathom signals are PART of the phase definition, not bolted on as a separate "validation layer." A phase like Admin Training is detected from HelpScout author/recipient patterns directly. The HelpScout/Fathom mix is itself a phase signal.
- Ambiguity is a first-class output. Cases where signals contradict are surfaced as flags, not silently smoothed. The standup decides; the agent doesn't.

## The cohort — auto-detected

Replace the manual shortname list with a postgres query. The `organizations.properties->>'status'` field is reliable and well-populated.

```sql
SELECT o.shortname, o.name, o.created_at
FROM organizations o
WHERE o.properties->>'status' = 'onboarding'
  AND o.name NOT ILIKE '%demo%'
  AND o.name NOT ILIKE '%template%'
  AND o.name NOT ILIKE '%test%'
ORDER BY o.created_at DESC
```

As of 2026-06-05 this returns: `tcs`, `drf`, `libco`, `pebl` (the 4 real onboarding clients). Status `onboarding` also tags `hl` (Hinkley Demo), `tmpo`, `tmpl` — caught by the name exclusions. Live clients (TCD, MALI) carry `status='active'` and correctly fall out of the cohort, matching the v3 rule that Phase 7 is terminal.

HubSpot is dropped as a cohort source. It can still feed Phase 1 readiness metadata (the onboarding readiness fields), but is not authoritative for who is in the cohort.

## Sources

| Source | MCP | Used for |
|---|---|---|
| Postgres | `user-supercat-postgres-vpn` | All eCat config: products, customers, options, price_levels, inventory, ipad_reports, orders, user_types, org_users (rep classification), `import_events`, cohort detection |
| BigQuery — `onboarding_assessment.fathom_recent_meetings` | `user-bigquery-admin` | Meeting titles/dates/`external_domains[]`/`invitee_emails[]`/`summary` |
| BigQuery — `onboarding_assessment.helpscout_tickets` | `user-bigquery-admin` | Tickets denormalized to ticket × thread with `thread_created_at`, `thread_created_by_type`, `thread_author_email`, `thread_body`, `primary_customer_domain`, `tags` |
| BigQuery — `mixpanel.events` | `user-bigquery-admin` | `event_name='order_submitted'` for rep activity (90d window) |

## Hard rules (non-negotiable)

- No metric without a tool call. No estimates / `~` / "approximately."
- No inference from prior knowledge or user-provided docs.
- Failed query → `❓ QUERY FAILED: [error]`. Never substitute.
- BigQuery is `SELECT`-only against source data.
- Verifiable-quote rule: every quote in a flag must appear verbatim in the retrieved `summary` / `thread_body` text. No reconstruction.
- No-activity certification: "no Fathom" / "no tickets" requires running the matching query and getting zero rows. Never an assumption.

---

## The 7 phases

| # | Phase | The question |
|---|---|---|
| 1 | Discovery / Kickoff | Have we kicked off this client? |
| 2 | Initial Import | Has at least the products file been imported? |
| 3 | Progress | Is more than one core file in, with no fatal errors on the most-recent of each? |
| 4 | Catalog Completeness | Is the catalog actually buildable as a live iPad? |
| 5 | Reps Signed In | Are external users (in custom user_types) actually logging into the iPad? |
| 6 | Admin Training | Has the admin been trained, with integration approach + ongoing-ops covered? |
| 7 | Go-Live (terminal) | Did the formal handoff to support happen? |

## Phase 1 — Discovery / Kickoff

**Question:** Have we kicked off this client?

**Anchor (any one is sufficient):**
- Postgres `organizations` row exists AND `properties->>'status' = 'onboarding'`.
- Fathom meeting in last 180d where the title matches `(?i)\bkickoff\b` AND `external_domains` intersects the resolved `client_domains`.
- HelpScout thread where `thread_author_email = 'kylor@supercatsolutions.com'` AND `thread_body` matches `(?i)kick.?off|onboarding.*next steps`.

**Done when:** the org row is non-disabled AND a kickoff Fathom recording OR explicit HelpScout kickoff thread exists. The org row alone is the anchor (every audited org has one), but advancing OUT of Phase 1 requires the qual signal too — otherwise we don't know if the project actually started or someone just spun up an empty shortname.

## Phase 2 — Initial Import

**Question:** Has at least the products file been imported?

**Anchor (required):**
- ≥1 row in `import_events` for this org with `data::text ILIKE '%- Products%'` AND that row's body does NOT match `:fatal`.

That's it. There is no programmatic "did the client send the file" signal — we can't see that. The import event IS the proxy. A warnings-only or even errors-but-not-fatal first import counts.

**Done when:** the most-recent products `import_events` row has no `:fatal` token AND `total_products` (`products` where `deleted = false`) > 0.

**Phase-2 health (graded but not gating):** product count; whether the import threw `:error` or only `:warning`.

## Phase 3 — Progress

**Question:** Is more than one core file imported, with no fatal errors on the most-recent of each?

**Anchor (all must be true):**
- ≥2 of {`Products`, `Customers`, `Options`, `Inventory`, `Product Stories`} have at least one import event in last 60d.
- For **every** file type that has any event, the **most-recent** event's body does NOT match `:fatal`. (Per llms.txt: Fatal = entire file rejected, nothing changes. Errors and warnings are tolerable here.)
- At least half of products have an image: `count(products where image_exists = true) / count(products where deleted = false) >= 0.5`.

**Done when:** anchor passes AND the products file's most-recent event is not Fatal AND ≥2 price_levels exist OR Net-Price-only mode is confirmed (catalog uses `NetPrice` only, no `Price_<code>` levels — flag for standup if ambiguous).

**Phase-3 health (graded):** most-recent event tier per file type; image coverage %; customer count (informational, not gating); count of customers whose `default_price_code` doesn't resolve to a real `price_levels.code` (flag for standup).

## Phase 4 — Catalog Completeness

**Question:** Is the catalog actually buildable as a live iPad?

**Anchor (all must be true):**
- All Phase 3 anchors still hold.
- Image coverage ≥50% (per spec — no per-segment thresholds; half is the floor).
- Most-recent products event is `:warning`-only or clean (no `:error`).
- Every customer's `default_price_code` resolves to a real `price_levels.code` for ≥99% of rows. (1% tolerance for ERP placeholders the client can clean up.)
- Option groups exist if any product has a non-empty `OptionSet1..N`. If true, `options_count > 0` AND option_groups exist.
- HelpScout has no thread with `ticket_status = 'active'` whose subject or recent body matches `(?i)import error|missing|wrong price|catalog.*broken` filed by the client in last 14d.

**Phase-4 health:** image coverage % (over the 50% floor); products with no `Price_<code>` populated where org has imported price levels; open HelpScout tickets with import-related keywords.

## Phase 5 — Reps Signed In

**Question:** Are external users (in custom user_types) logging into the iPad?

**Definition of "external rep" (the corrected one):**

```sql
is_admin = false
AND user_type.name <> 'DefaultUserGroup'
AND email NOT LIKE '%@supercatsolutions.com'
AND lower(split_part(email,'@',2)) NOT IN (client_domains[])
AND COALESCE(disabled, false) = false
```

**Anchor (all must be true):**
- ≥1 `external_rep` row exists.
- ≥1 `external_rep` has `last_ipad_login_at IS NOT NULL` (ever logged in).
- ≥1 `external_rep` has `last_ipad_login_at >= NOW() - INTERVAL '30 days'` (active in last 30d).

**Done when:** anchor passes AND ≥1 submitted order in `orders` from a non-admin org_user (real or self-test both count — an exercised order path is sufficient signal that the workflow is plumbed end-to-end).

**Phase-5 health:** external_rep count / count active 30d; submitted orders by external_reps (real customer vs self-billed — if all self-billed, flag as "Phase-5 yes, Phase-7 no").

**Common ambiguity:**
- external_rep defined but not logging in → rep-onboarding stalled (MALI pattern). Flag.
- user_types defined but no users in them yet (LIBCO pattern). Not Phase 5 — flag as "scaffolded but unfilled."
- non-admin client users logging in but all in DefaultUserGroup (PEBL pattern). Not Phase 5 — flag as "users testing but not in a real group."

## Phase 6 — Admin Training

**Question:** Has the admin been trained, with integration approach and ongoing operations covered?

**Anchor — qualitative trigger (required, ANY ONE):**
- HelpScout thread where Kylor's reply CCs `kyla@supercatsolutions.com` or `support@supercatsolutions.com` AND thread body matches `(?i)admin training|handoff|primary point of contact|now that your reps`.
- Fathom meeting in last 60d with title matching `(?i)admin training|handoff` AND `external_domains` intersects `client_domains`.
- HelpScout thread containing a URL matching `supercat\.supercatsolutions\.com/.*onboarding/|knowledgebase/admin-console` sent FROM a SuperCat author TO a client domain (admin training HTML / llms.txt being shared = handoff signal).

**Anchor — quantitative readiness (required):**
- `organizations.order_email_recipient` not empty.
- `ipad_reports` count ≥ 3.
- `user_types` count ≥ 2 (at least one beyond `DefaultUserGroup`).

**Integration approach (Phase 6 sub-topic — surfaced, not gated):**
The integration discussion (API vs FTP feed vs manual; us-managed vs client-managed) belongs to Phase 6 because it can happen anywhere — early scoping (LIBCO Business Central), mid-build (TCS Catsy/Odoo), or post-handoff (MALI Endeavour). If a Fathom meeting in last 90d has a section title matching `(?i)integration|business central|netsuite|pim|api|odoo`, surface it as a Phase 6 sub-signal. Do NOT block Phase 6 closure on integration completion — integration is its own workstream that may finish after handoff.

**Done when:** both qualitative trigger AND quantitative readiness pass.

**Common ambiguity:**
- Kyla intro email sent but order email + PDFs not configured (MALI pattern): narrative says "handed off"; infra says "not ready." Flag.
- PDF formats + order email set but no Kyla intro thread visible. Maybe handoff happened on a call we didn't capture — flag as "verify with Kyla."
- Integration discussions still active months after Phase 6 anchor → not a blocker, just informational.

## Phase 7 — Go-Live (terminal)

**Question:** Has the formal handoff to support happened, with ongoing client activity?

**Anchor (all must be true):**
- Phase 6 done.
- ≥1 submitted order in `orders` from a non-admin user with `bill_to_company_name` ≠ the client's own company name (real customer order, not self-test).
- HelpScout thread author/CC pattern shifted: in last 30d, primary SuperCat correspondent is `kyla@` or `support@`, NOT `kylor@`. Compute: `count(threads_last_30d WHERE thread_created_by_type='user' AND author IN ('kyla@','support@'))` > `count(... AND author='kylor@')`.

**Outcome:** client exits the framework. `properties->>'status'` should be flipping to `active` around this time. Remove from next run's cohort. Any post-live concerns belong to a separate post-live health framework.

---

## Phase assignment algorithm

For each client:

1. Evaluate phases 1 → 7 in order.
2. **Anchor phase** = highest phase whose `Done when` clause passes.
3. **Current phase** = `Anchor phase + 1`, capped at 7. (If anchor = 7, client is Live and exits.)
4. **Open workstreams** = any phase ≤ Anchor whose health metrics show incomplete or degraded items (not gating, but called out in narrative).
5. **Ambiguity flags** = the contradiction patterns enumerated below.

Phases are NOT strictly sequential in completion. A client can have Phase 6 qualitative anchor fired (Kyla intro email) while Phase 5 reps haven't logged in yet. In that case the Anchor is still Phase 4 (last fully-Done), Current = Phase 5, but Phase 6 qual signal is surfaced as an "out of sequence" ambiguity flag because it suggests we got ahead of ourselves on the narrative. The linear-ladder fiction is what the v2 framework apologized for — we just bake the non-linearity into the output.

---

## Ambiguity flags (the standup agenda)

These are the patterns the agent must raise for the weekly standup. Each flag includes the client, the contradicting signals, and a one-line "what to discuss." There is no "right answer" the agent picks — humans resolve these.

### A. Phase-narrative vs phase-infra mismatch

| Flag | Trigger | What to discuss |
|---|---|---|
| `KYLA_INTRO_INFRA_GAP` | Phase 6 qual trigger fired but order_email_recipient empty OR ipad_reports < 3 OR user_types < 2 | Did handoff actually happen, or was it announced ahead of readiness? |
| `INFRA_READY_NO_HANDOFF` | Phase 6 quant readiness fired but no Kyla intro thread visible | Did handoff happen on a call we didn't capture? Verify with Kyla. |
| `REPS_DEFINED_NOT_LOGGED_IN` | external_rep count > 0 but ipad_logged_in_ever = 0 | Rep onboarding stalled — invitations sent but not actioned? |
| `USER_TYPES_EMPTY` | user_types beyond DefaultUserGroup exist but 0 users in them | Scaffolding built; rep migration not run. Whose action? |
| `REPS_IN_DEFAULT_GROUP` | non-admin client users logging into iPad but all in DefaultUserGroup | Custom user_type not yet created — Phase 5 looks closer than it is. |
| `SELF_TEST_ONLY_ORDERS` | ≥1 submitted order but ALL orders' bill_to_company_name = client's own company | Workflow exercised but no real orders yet — Phase 5 yes, Phase 7 no. |

### B. Source-of-truth contradictions

| Flag | Trigger | What to discuss |
|---|---|---|
| `IMPORT_VS_HELPSCOUT_DRIFT` | Postgres shows recent clean imports but HelpScout has client thread complaining about the import in last 7d | Either client doesn't see what we shipped, or we missed something. |
| `HELPSCOUT_QUIET_POSTGRES_QUIET` | No client-side HelpScout activity in last 30d AND no import_events in last 30d AND not yet Phase 7 | Stalled. Who reaches out? |
| `HELPSCOUT_ACTIVE_POSTGRES_QUIET` | Active HelpScout thread but no import_events in last 14d | Conversation moving but no work landing — what's the actual blocker? |
| `KYLOR_DOMINATES_POST_HANDOFF` | Phase 6 anchor fired ≥30d ago but in last 30d kylor@ replies > kyla@/support@ replies | Handoff didn't take. Does Kyla need re-engaging? |

### C. Quantitative threshold borderlines

| Flag | Trigger | What to discuss |
|---|---|---|
| `IMAGE_COVERAGE_BORDERLINE` | image_exists / total_products between 0.45 and 0.55 | Is 50% the right threshold for this client? |
| `DPC_MISMATCHES_LOW` | 1–5 customers with default_price_code not in price_levels | Worth chasing or accept as noise? |
| `RECURRING_WARNINGS_NO_ERROR` | Same `:warning` text appears in 5+ consecutive product imports (e.g. PEBL custom-field warnings) | Decide: register the custom field, remove from file, or accept the warning. |

### D. Integration / ownership ambiguity (Phase 6 sub-flags)

| Flag | Trigger | What to discuss |
|---|---|---|
| `INTEGRATION_OWNER_UNCLEAR` | Fathom meetings in last 90d include integration topics but no decision recorded in HelpScout | Who owns the integration build — us, them, or a third party? |
| `INTEGRATION_DEFERRED_POST_HANDOFF` | Phase 6 done but integration still in scope per recent Fathom | Track separately; not a Phase-6 blocker but standup awareness. |

### E. Phase-skip / out-of-order

| Flag | Trigger | What to discuss |
|---|---|---|
| `PHASE_SKIP_OBSERVED` | A Phase ≥ Anchor+2 has its qual or quant signal firing while Anchor+1 hasn't been completed | Are we ahead of ourselves, or did we genuinely skip a step? |

---

## Per-client output structure

Substance over formatting; reproduce these sections per client, sorted by Anchor phase ascending.

```
## {SHORTNAME} ({Company Name})

**Anchor Phase:** {N — Phase Name} · **Current:** {N+1 — Phase Name}
**Days Active:** {from organizations.created_at}
**Domains:** {client_domains}
**Engagement mix:** {Fathom-heavy / HelpScout-heavy / Mixed / Quiet}

### Phase Status

| Phase | Done? | Evidence (1 line) |
|---|---|---|
| 1 Discovery | ✅ / 🟡 / ⚪ | {kickoff Fathom date or HelpScout intake thread #} |
| 2 Initial Import | ✅ / 🟡 / ⚪ | {first products import_events date, tier, count} |
| 3 Progress | ✅ / 🟡 / ⚪ | {file types imported, most-recent tier each, image %, price levels} |
| 4 Catalog Complete | ✅ / 🟡 / ⚪ | {image %, DPC validity %, open HS tickets} |
| 5 Reps Signed In | ✅ / 🟡 / ⚪ | {external_rep count / logged in / active 30d / orders} |
| 6 Admin Training | ✅ / 🟡 / ⚪ | {Kyla intro thread # or training Fathom; order email; PDFs; user_types} |
| 7 Go-Live | ✅ / ⚪ | {real customer order date; correspondence shift to Kyla} |

### Open Workstreams (within or below Anchor)
- {Phase N: specific open item with metric}

### Ambiguity Flags for Standup
- **{FLAG_CODE}**: {one-line context} → "{verbatim quote, source #}"

### Recent Engagement
**Fathom (last 90d):** {N meetings} — last "{title}" {date} ({recording_url})
**HelpScout (last 90d):** {N threads, M open} — last activity {date} ({last author})
**Imports (last 60d):** {tally by file type, with most-recent tier}

### 🎯 Next Action
{The single most important next step driven by Anchor → Current. If there's an unresolved ambiguity flag, the next action is to resolve THAT in standup, not plow ahead.}
```

## Cohort-level output (top of file)

```
# {Month D, YYYY} — Onboarding Phase Assessment

## Pipeline Overview
| Client | Anchor | Current | Engagement | Days Active | Top Flag |

## Pipeline View — by Anchor (least far → most far)
{ASCII bar viz; bar = phase position 1–7, not "readiness %"}

## Standup Agenda — Ambiguity Flags

### 🔴 Resolve this week
{Flags blocking phase advancement}

### ⚠️ Discuss / decide
{Flags about thresholds, ownership, integration approach}

### ✅ Confirmed (no flags)
{Clients whose phase is unambiguous}
```

---

## What this framework deliberately does NOT do

- Does not predict go-live dates. Anchor + Current tells you where, not when.
- Does not score "health" of post-live clients. Phase 7 is terminal.
- Does not auto-resolve ambiguity flags. That's the standup's job.
- Does not assume linear progression. Out-of-order signals are surfaced, not smoothed.

## Run mechanics

- `RUN_PROMPT.md` orchestrates: auto-cohort detection → phase assignment per client → ambiguity flag emission → output assembly.
- Output: `output/{YYYY-MM-DD}-assessment.md`. The dated markdown is the deliverable.
- Phase 7 clients are dropped from the next run's cohort. Operations / health surveillance picks them up downstream.
