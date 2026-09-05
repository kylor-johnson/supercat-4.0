# BigQuery Reference — `supercat-data-pipeline` (canonical)

> **This is the single source of truth for querying SuperCat's data warehouse.**
> If another doc disagrees with this file, this file wins. Facts here were verified
> against the live warehouse on **2026-06-03** via the `user-bigquery-admin` MCP.
>
> **Migration status (who's on which layer):** [`integrations/bigquery/MIGRATION_STATUS.md`](integrations/bigquery/MIGRATION_STATUS.md)

---

## 1. Which connection do I use?

Three BigQuery MCP servers exist (all → project `supercat-data-pipeline`, location `US`):

| Use this… | When | `query` tool param | Capability |
|---|---|---|---|
| **`user-bigquery-admin`** ✅ default | Almost always — reads **and** view creation | **`sql`** (+ optional `maximumBytesBilled`) | Full DDL/DML |
| `user-bigquery-direct` | A plain SELECT, if admin is unavailable | `query` | SELECT only |
| `user-bigquery-vpn` ⚠️ legacy | Only inside consumers **not yet migrated** (see registry) | `query` (+ `max_results`) | Read-only, **stale `WELD_RAW` Weld views** |

> ⚠️ **The parameter name differs.** Admin's `query` tool takes **`sql`**; vpn/direct take **`query`**.
> A prompt/script written for vpn will *error*, not silently work, against admin. Rewrite the call, don't assume.
>
> ⚠️ **vpn reads a different, stale dataset (`WELD_RAW`) with different table names.** It is *not*
> a drop-in alias for admin. The classic "Fathom stuck at ~Feb 4" bug is a vpn/Weld artifact —
> it does not exist on the native tables below.

### Safety rules (non-negotiable)

- **`SELECT` only against source datasets.** Never `INSERT/UPDATE/DELETE/DROP/ALTER` a source table.
- The only writes allowed are **`CREATE OR REPLACE VIEW`** (or curated tables) **inside purpose-built
  datasets** you own: `onboarding_assessment`, `insightful_product` (curated outputs), `scorecard`, `sales_ops`.
- Push source-of-truth SQL **into a view in one of those datasets**, then have prompts reference the view.
  Do not embed brittle, drift-prone SQL in agent prompts.
- Always bound expensive scans (`time`/date filters, `LIMIT`, or `maximumBytesBilled`).

---

## 2. Naming: native (correct) vs Weld (legacy)

Native tables are **fully qualified** `dataset.table` and must be backtick-wrapped as a whole path.
Anything matching the middle/left columns below is **stale** — translate it.

| Gen-1 (Hevo, oldest) | Gen-2 (Weld / vpn) | ✅ Gen-3 (native / admin) |
|---|---|---|
| `hevo_dataset_…_Slhk.help_scout_tickets` | `helpscout__conversation` / `helpscout__help_scout_tickets` | `helpscout.conversations` + `helpscout.conversation_threads` |
| — | `fathom__ai_summaries` / `fathom__call_transcripts` | `` `Fathom.ai-summaries` `` / `` `Fathom.call-transcripts` `` *(hyphens → backtick the path)* |
| — | `mixpanel__events` | `mixpanel.events` |
| — | `hubspot__company` / `__deal` / `__contact` / `__owner` | `hubspot.company` / `.deal` / `.contact` / `.owner` |
| — | `stripe__invoice`, `quickbooks__invoice` | `stripe.invoice`, `quickbooks.invoice` |
| MCP `@ergut/mcp-bigquery-server` (Hevo) | MCP URL `bigquery-cli-staging.k8s…:3003` | MCP `user-bigquery-admin` (local) |

**Dead patterns — flag on sight:**
- ❌ The `api_access`-event join to attribute org. **Dead** — use the `COALESCE` in §4.
- ⚠️ `_weld_synced` as a freshness signal. It *still exists* as a column on `mixpanel.events`, but it is
  **not** the freshness contract — filter on **`time`** (events) / native timestamps instead.

---

## 3. Live datasets (verified 2026-06-03)

Native, fresh: `Fathom`, `helpscout`, `hubspot` (+ `hubspot_views`), `mixpanel`, `stripe`, `quickbooks`,
`insightful_product`, `onboarding_assessment`, `scorecard`, `sales_ops`, `google_analytics_4`
(+ `google_analytics_ecat`, `_ecat_online`, `_supercat_website`), `facebook_ads`, `linkedin_ads`,
`clicky_analytics`. · Legacy: **`WELD_RAW`** (what vpn reads — avoid).

### Tables you'll actually use

**`mixpanel`** — product analytics (eCat app)
| Object | Type | Notes |
|---|---|---|
| `mixpanel.events` | TABLE (~9.6M rows, fresh to today) | Precise **windowed** activity. See §4. |
| `mixpanel.org_feature_usage_report` | VIEW | Per-org usage **breadth** (logins, submit_order, view_ipad_orders, access_sales_portal…). All-time-ish — use for "do they use X," not recency. |
| `mixpanel.user_feature_usage_report` | VIEW | Per-user equivalent. |
| `mixpanel.organization_customer_mapping` / `user_org_mapping` / `people` | TABLE | Mapping/enrichment helpers. |

**`helpscout`** — support
| Object | Notes |
|---|---|
| `helpscout.conversations` (~5.1k) | Ticket headers. |
| `helpscout.conversation_threads` (~39k) | Individual messages/notes; join on conversation id. |
| `helpscout.customers`, `.tags`, `.inboxes`, `.users`, `.team_members` | Dimensions. Severity/escalation tags (`l3/l4/s1/s2`) live in `tags`. |

**`Fathom`** — call intelligence *(column names contain spaces; table names contain hyphens — backtick everything)*
| Object | Notes |
|---|---|
| `` `Fathom.ai-summaries` `` (~708) | AI summaries. Attendees are **comma-delimited strings** → split before use. |
| `` `Fathom.call-transcripts` `` (~501) | Full transcripts. |
| `Fathom.ai_summaries_parsed` | VIEW — pre-parsed convenience layer. |

**`insightful_product`** — curated org analytics (read; curated writes OK)
| Object | Notes |
|---|---|
| `insightful_product.org_master` / `org_master_with_segments` | VIEW — canonical org dimension. |
| `insightful_product.org_summary` | VIEW — segment, health, ARR, peer standing. Often empty for brand-new onboarding orgs. |
| `insightful_product.segment_*`, `at_risk_accounts`, `expansion_candidates`, `portal_*` | VIEWs — segment/benchmark analytics. |

**`onboarding_assessment`** — normalized views for the weekly onboarding assessment
| Object | Notes |
|---|---|
| `onboarding_assessment.onboarding_clients` | HubSpot evangelist list + best-effort shortname/segment/ARR. **Helper only**, not an authoritative cohort. |
| `onboarding_assessment.fathom_recent_meetings` | Fathom summaries with attendees pre-parsed into `invitee_emails[]` / `external_domains[]`. |
| `onboarding_assessment.helpscout_tickets` | Tickets × threads denormalized: `thread_created_at`, `thread_created_by_type`, HTML-stripped `thread_body`, `primary_customer_domain`, `tags`. |

> `hubspot.{company,contact,deal,owner,engagement}` are wide views — **always select specific columns, never `SELECT *`.**

---

## 4. Validated facts (use these; don't re-derive)

**Org attribution on `mixpanel.events`** — the table carries both `organization_shortname` and
`current_organization_shortname` (plus `organization_id` / `current_organization_id`). Attribution is
~100% (verified **98,797 / 98,828 = 99.97%** over the last 7 days). Always attribute with:

```sql
COALESCE(NULLIF(organization_shortname, ''), NULLIF(current_organization_shortname, '')) AS org_shortname
```

**Time** — `mixpanel.events.time` is `FLOAT` unix-**seconds**:

```sql
TIMESTAMP_SECONDS(CAST(time AS INT64)) AS event_ts
-- window filter (cheap):
WHERE time >= UNIX_SECONDS(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY))
```

**iPad order event** — `event_name = 'order_submitted'` (`order_total`, `item_count`, `item_numbers` carry detail).

**Freshness** — verified `MAX(event_ts) = 2026-06-03` (current day) at write time. Native datasets are synced daily.

### Canonical snippet — active orgs, last 30 days

```sql
SELECT
  COALESCE(NULLIF(organization_shortname, ''), NULLIF(current_organization_shortname, '')) AS org_shortname,
  COUNT(*) AS events,
  COUNTIF(event_name = 'order_submitted') AS ipad_orders,
  COUNT(DISTINCT username) AS users,
  MAX(TIMESTAMP_SECONDS(CAST(time AS INT64))) AS last_seen
FROM `supercat-data-pipeline.mixpanel.events`
WHERE time >= UNIX_SECONDS(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY))
GROUP BY org_shortname
HAVING org_shortname IS NOT NULL
ORDER BY events DESC
```

---

## 5. eCat configuration data is NOT in BigQuery

Products, images, price levels, customers, users, options, territories, inventory, import events,
orders, order-email config → **Postgres only** (`user-supercat-postgres-vpn`, VPN required). There is no
BigQuery mirror of eCat config. (A Postgres→BQ `ecat.*` sync is *planned* per
`documentation/BQ_Operationalization_Handoff_Kev.md` but is not the source of truth yet.)

---

## 6. Anti-hallucination rules

- Never emit a numeric metric without a tool call. No "~"/"approximately"/estimates.
- Never infer values from context, prior knowledge, or user-provided docs.
- If a query fails, mark the metric `❓ QUERY FAILED: [error]` — do not substitute a plausible value.

---

*Canonical since 2026-06-03. Supersedes `BIGQUERY_WINDMILL_MCP_REFERENCE.md` (Weld/vpn era).*
