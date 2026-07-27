# Onboarding Models — Stage-Gated Assessment

**Version:** 2.0 (BigQuery-native)
**Updated:** 2026-06-03
**Status:** Production. Data plumbing migrated from the stale Weld views to the native `supercat-data-pipeline` BigQuery datasets + normalized views in `onboarding_assessment`. eCat configuration metrics still come from Postgres.

> **Running this week's assessment?** Use `RUN_PROMPT.md` — one copy-paste prompt that orchestrates the full flow (resolve shortnames → collect → validate → write the dated output). This README is the source of truth for *what* the system does and *which* sources it reads; the prompts orchestrate by reference.

---

## What this is

A weekly readiness assessment for the clients currently in onboarding. For each client it produces a stage-by-stage scorecard (Account Foundation → … → live), the biggest blocker, validation flags from recent calls and support tickets, and a per-client narrative. Output is one markdown file per run in `output/`.

The question it answers: **for each onboarding client, what stage are they at, what's blocking them, and what does CS need to do next?**

## Cohort — you provide the shortnames

The weekly cohort is **curated, not auto-derived**. When you run it, you hand the agent the list of org shortnames to assess (e.g. `tcs, pebl, libco, drf`). HubSpot's `evangelist` lifecycle list is noisy (mislabeled stages, dupes, already-live orgs), so it is only a *suggestion* surfaced by the `onboarding_clients` view — never the authoritative cohort.

## The flow (3 stages, 1 orchestrator)

| Stage | Doc | What it does | Sources |
|---|---|---|---|
| 0 | (in RUN_PROMPT) | Resolve each shortname → real org + email domain(s) | Postgres |
| 1 | `Stage_Gated_Data_Collection.md` | Quantitative metrics + stage gating | Postgres (eCat config) + BigQuery (usage) |
| 2 | `Validation_Layer_Fathom_HelpScout.md` | Qualitative validation from calls + tickets | BigQuery views |
| 3 | `Output_Format.md` | Assemble the per-client assessment markdown | — |

Output lands at `output/{YYYY-MM-DD}-assessment.md`. (Notion/HTML publishing is a later, separate concern — the markdown file is the contract.)

## Data sources

### Postgres — `user-supercat-postgres-vpn` (VPN required)

**Authoritative for eCat configuration / stage-readiness** — there is no BigQuery mirror of this config data. Products, images, price levels, customers, users, user types, options, territories, inventory, import events, mobile sites, orders, order-email config. Also used in Stage 0 to resolve each shortname's real org row and email domain(s).

### BigQuery — `user-bigquery-admin` (project `supercat-data-pipeline`, VPN required)

Full-admin local MCP. **For onboarding, only `SELECT` from sources and only `CREATE OR REPLACE` inside `onboarding_assessment`. Never modify source tables.**

Normalized views (source-of-truth SQL lives in these views, not in prose):

| View | Grain | Purpose |
|---|---|---|
| `onboarding_assessment.onboarding_clients` | org | HubSpot evangelist list + best-effort shortname/segment/ARR. **Helper only** — generic domains filtered out. |
| `onboarding_assessment.fathom_recent_meetings` | recording | Fathom summaries with attendees pre-parsed into `invitee_emails[]` / `external_domains[]` arrays. |
| `onboarding_assessment.helpscout_tickets` | ticket × thread | Denormalized tickets+threads: `thread_created_at` (true last activity), `thread_created_by_type` (customer vs agent), HTML-stripped `thread_body`, `primary_customer_domain`, `tags`. |

Direct native tables/views also used:

| Object | Purpose |
|---|---|
| `mixpanel.org_feature_usage_report` | Per-org usage **breadth** (logins, submit_order, view_ipad_orders, access_sales_portal, etc.). Window is all-time-ish — use for "do they use X," not precise recency. |
| `mixpanel.events` | Precise **windowed** activity. iPad orders = `event_name = 'order_submitted'`; `time` is FLOAT unix-seconds; org via `COALESCE(NULLIF(organization_shortname,''), NULLIF(current_organization_shortname,''))` (100% attributed — no `api_access` join needed). |
| `insightful_product.org_summary` | Enrichment for established orgs: segment, health_score, ARR, peer standing. Often empty for brand-new onboarding orgs. |

## Freshness (verified 2026-06-03)

Fathom (`Fathom.ai-summaries`, `Fathom.call-transcripts`), HelpScout (`helpscout.conversations`), HubSpot (`hubspot.company`), and Mixpanel (`mixpanel.events`) are all synced current. The old "`fathom__ai_summaries` stale since Feb 4" problem is gone — that was a Weld-view issue; the native tables are fresh daily.

## Anti-hallucination rules (unchanged, still non-negotiable)

- Never produce a numeric metric without a tool call. No "approximately"/"~"/estimates.
- Never infer values from context, prior knowledge, or user-provided docs.
- If a query fails, mark the metric `❓ QUERY FAILED: [error]` — do not substitute a plausible value.

## File map

```
onboarding-models/
├── README.md                              ← this file (source of truth)
├── RUN_PROMPT.md                          ← weekly orchestrator (copy-paste)
├── Stage_Gated_Data_Collection.md         ← Stage 1: metrics + gating
├── Validation_Layer_Fathom_HelpScout.md   ← Stage 2: call/ticket validation
├── Output_Format.md                       ← Stage 3: assemble the markdown
├── Client_Facing_Data_Questionnaire.md    ← reference (client-facing)
├── Sales_Data_Scoping_Framework_MVP.md    ← reference
├── output/
│   └── {YYYY-MM-DD}-assessment.md          ← one deliverable per run
└── _archive/                               ← frozen baseline + superseded versions
```

## Open items / roadmap

- **HTML "WoW" view** — the prettier presentation layer is deferred. The dated markdown is the current deliverable; HTML gets built from the same structured output later.
- **Support fire-flags** — `helpscout_tickets.tags` exposes `l3/l4/s1/s2` severity/escalation tags (same scheme Health V3 uses). Not yet wired into the assessment; candidate enhancement.
- **Retire `user-bigquery-vpn`** — NOT yet safe. As of 2026-06-03, onboarding-models and Health V3 are off it, but it is still load-bearing for `Insightful Product 2.0`, `Health V3 Backfill`, `Migration-Health Artifacts`, and `Health V2`. The old read-only MCP must stay until all of those migrate too.
