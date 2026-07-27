# Onboarding Assessment — Weekly Run Prompt

Reusable prompt for producing the weekly onboarding stage-gated assessment. Hand the prompt body to a capable agent in Cursor and it runs the full flow: resolve shortnames → collect metrics → validate against calls/tickets → write the dated markdown.

**When to use:** weekly, or any time you need a fresh readiness read on the onboarding cohort.

**Prerequisites:**

- Cursor with `user-supercat-postgres-vpn` and `user-bigquery-admin` MCPs enabled. VPN active (both require it).
- The list of org **shortnames** you want assessed this week.

**Rough runtime:** 10–20 min depending on cohort size.

**Hard rules:**

- **Anti-hallucination (non-negotiable):** never produce a numeric metric without a tool call; no estimates/"~"; never infer from prior knowledge or user docs; if a query fails, mark `❓ QUERY FAILED: [error]` and move on — never substitute a value.
- **BigQuery is `SELECT`-only** against source data. The only writes allowed are `CREATE OR REPLACE VIEW` inside `onboarding_assessment` (and you should not need even those for a normal run — the views already exist).
- If anything is ambiguous, stop and ask. Do not invent SQL — the validated queries live in the stage docs and the `onboarding_assessment` views.

---

## The prompt

Everything below the line is the prompt body. Copy from the line break to the end of file, paste in your shortnames at the top, and hand it to the agent.

---

You are producing this week's onboarding stage-gated assessment. Read this entire prompt before starting.

**Clients to assess this run (shortnames):** `[PASTE SHORTNAMES HERE, e.g. tcs, pebl, libco, drf]`

## Authoritative docs

Before doing anything, read:

1. `onboarding-models/README.md` — sources, views, rules, output contract.
2. `onboarding-models/Stage_Gated_Data_Collection.md` — Stage 1 queries + stage gating.
3. `onboarding-models/Validation_Layer_Fathom_HelpScout.md` — Stage 2 validation.
4. `onboarding-models/Output_Format.md` — Stage 3 assembly + the output file contract.

Do not paraphrase SQL from memory. Run the queries as written in those docs, or `SELECT` from the `onboarding_assessment` views.

## Step 0 — Determine the run date and resolve each client

1. Run `date -u +%F` for the run date `$RUN_DATE` (used in the output filename).
2. For **each shortname** provided, resolve the real org and its email domain(s) from Postgres (`user-supercat-postgres-vpn`):

```sql
SELECT o.shortname, o.name, o.created_at,
  ARRAY_AGG(DISTINCT LOWER(split_part(u.email, '@', 2))) AS client_domains
FROM organizations o
JOIN org_users ou ON ou.organization_id = o.id
JOIN users u ON ou.user_id = u.id
WHERE o.shortname = '[SHORTNAME]'
  AND u.email NOT LIKE '%@supercatsolutions.com'
GROUP BY o.shortname, o.name, o.created_at
```

If a shortname returns no rows, stop and confirm the correct shortname with the user before proceeding (the label used in conversation is not always the eCat shortname — e.g. "LIBCO" may not be `libco`). Record each client's `client_domains` — Stage 2 matches Fathom/HelpScout on these.

## Step 1 — Data collection (per client)

Follow `Stage_Gated_Data_Collection.md` exactly:

- Postgres (`user-supercat-postgres-vpn`): eCat configuration metrics (products, images, price levels, customers, users, user types, options, territories, inventory, import events, mobile sites, orders, order email). Batch across the cohort where the doc shows the batch pattern.
- BigQuery (`user-bigquery-admin`): usage breadth from `mixpanel.org_feature_usage_report`, precise windowed iPad orders from `mixpanel.events`, and enrichment from `insightful_product.org_summary`.
- Apply the stage validation criteria to assign each stage 🔴/🟡/🟢/⚫ and compute current stage + readiness %.

## Step 2 — Validation (per client)

Follow `Validation_Layer_Fathom_HelpScout.md` exactly, matching on each client's `client_domains` from Step 0:

- Fathom: `SELECT` from `onboarding_assessment.fathom_recent_meetings`, match domains against `external_domains` / `invitee_emails`.
- HelpScout: `SELECT` from `onboarding_assessment.helpscout_tickets`, match on `primary_customer_domain`; use `thread_created_at` for last-activity and `thread_body` for sentiment/keywords.
- Emit validation flags and a confidence read per client. Complete the "no activity" certifications before stating a client has none.

## Step 3 — Assemble and write the output

Follow `Output_Format.md`. Assemble the per-client assessment (Pipeline Overview, pipeline view, per-client stage tables + narratives, Validation Flags Summary), sorted by readiness ascending.

**Write the result to `onboarding-models/output/$RUN_DATE-assessment.md`.** This file is the deliverable. (Do not publish to Notion; the HTML view is a later step.)

## Step 4 — Sanity check before declaring done

- Every client in the provided shortname list appears in the output (or is explicitly noted as unresolved).
- Every numeric metric came from a tool call; no `❓ QUERY FAILED` left unaddressed.
- Readiness % and current stage are consistent with the stage table for each client.
- Output file written at the correct dated path.

If any check fails, fix it or report — do not ship a partial assessment silently.
