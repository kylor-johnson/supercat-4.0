# Internal Intelligence Brief — Query Library

Version: 1.0
Implements: DESIGN.md v1.0

---

## 0. Prerequisites

Before running any queries:
1. Confirm `org_shortname` from Health V2 CSV or org_summary
2. Resolve email domains for HelpScout attribution (from `pg_domain_map.csv`)
3. Confirm Jira `cloudId` via `getAccessibleAtlassianResources`

---

## 1. Health V2 Data (Local File Read)

### Q-IB-HEALTH: Client Health Row

**Source**: Health V2 CSV — `Health V2/runs/{latest}/client_health_scores_{date}.csv`

**Method**: Read CSV, filter to `org_shortname = '{shortname}'`

**Required columns**:
```
org_shortname, org_name, parent_entity, bundle, arr, health_score, health_band,
growth_score, growth_band, classification, churn_risk, churn_risk_severity,
expansion_ready, expansion_type, healthy_complete, engagement_score,
adoption_score, value_delivery_score, operational_health_score, trajectory_score,
bundle_upgrade_signal, feature_gap_score, customer_headroom_score,
peer_benchmark_gap, risk_modifier_applied, scoring_status, missing_data_flags,
score_explanation, hs_lifecycle_stale, hs_join_missing, arr_data_gap
```

**If client not found**: STOP. Cannot generate brief without health data.

---

## 2. org_summary Reference (BigQuery)

### Q-IB-ORG: Org Identity & Config

**Source**: BigQuery — `supercat-data-pipeline.insightful_product.org_summary`
**MCP**: `user-bigquery-admin` → `query` (takes `sql`; migrated 2026-06-04 from `user-bigquery-vpn`)

```sql
SELECT
  org_shortname,
  org_name,
  has_clicky_portal,
  portal_visitors_daily
FROM `supercat-data-pipeline.insightful_product.org_summary`
WHERE org_shortname = '{shortname}'
```

**Output**: Config flags needed for Section 5 (Clicky enablement action item) and Section 2 (bundle context).

---

## 3. Email Domain Resolution

### Q-IB-DOMAIN: Client Email Domains

**Primary source**: `pg_domain_map.csv` from the Health V2 cache directory.

Filter to `org_shortname = '{shortname}'` to get all email domains associated with this client.

**If cache unavailable**, query Postgres directly:

**Source**: Postgres — `users` + `org_users` + `organizations`
**MCP**: `user-supercat-postgres-vpn` → `execute_sql`

```sql
SELECT DISTINCT LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) AS domain
FROM users u
JOIN org_users ou ON ou.user_id = u.id
JOIN organizations o ON ou.organization_id = o.id
WHERE o.shortname = '{shortname}'
  AND u.email::text LIKE '%@%'
  AND LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) NOT IN (
    'gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'outlook.com',
    'icloud.com', 'supercatsolutions.com', 'comcast.net', 'msn.com',
    'me.com', 'att.net', 'live.com', 'sbcglobal.net', 'verizon.net',
    'bellsouth.net', 'charter.net', 'cox.net', 'earthlink.net',
    'ymail.com', 'mac.com', 'protonmail.com', 'lojic.com',
    'railsfever.com', 'samedis.com', 'jimmythrasher.com',
    'upwardtechnologies.com'
  )
```

**Output**: List of email domains (e.g., `['curreyco.com']`) used as the `IN` clause for all HelpScout queries.

---

## 4. HelpScout Queries (BigQuery)

All HelpScout queries use `user-bigquery-admin` → `query` (the `sql` param) against native `supercat-data-pipeline.helpscout.*` — migrated 2026-06-04 from `user-bigquery-vpn`. Schema + JSON functions below validated against admin on 2026-06-04 (`tags`, `primaryCustomer`, `createdAt`, `status`, `threads` all confirmed).

### HelpScout Schema Reference

| Column | Type | Notes |
|--------|------|-------|
| `id` | NUMERIC | Conversation ID |
| `subject` | STRING | |
| `status` | STRING | `active`, `closed`, `spam`, etc. |
| `state` | STRING | `published`, etc. |
| `createdAt` | STRING | ISO 8601 timestamp as string |
| `tags` | JSON | Array of tag objects: `[{"tag": "l1 - handled by frontline support", ...}]` |
| `threads` | NUMERIC | Thread count |
| `primaryCustomer` | JSON | Contains `.email` |
| `userUpdatedAt` | STRING | Last updated timestamp |

**Tag extraction**: Use `JSON_EXTRACT_SCALAR(tag, '$.tag')` after `UNNEST(JSON_QUERY_ARRAY(tags))`.

**Tag serialization for LIKE matching**: Use `TO_JSON_STRING(tags)` — `CAST(tags AS STRING)` fails.

### Q-IB-HELP-DETAIL: Support Conversations with Tags

Returns individual conversations for this client with full tag detail.

```sql
SELECT
  id,
  subject,
  status,
  createdAt,
  threads,
  TO_JSON_STRING(tags) AS tags_json
FROM `supercat-data-pipeline.helpscout.conversations`
WHERE PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', LEFT(createdAt, 19))
      >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  AND status != 'spam'
  AND LOWER(REGEXP_EXTRACT(SAFE.STRING(primaryCustomer.email), r'@(.+)$'))
      IN ({client_email_domains})
ORDER BY createdAt DESC
```

**Parameters**: `{client_email_domains}` = comma-separated quoted list from Q-IB-DOMAIN.

### Q-IB-HELP-THEMES: Tag Distribution for Theme Analysis

Groups conversations by tag dimension to identify recurring patterns.

```sql
SELECT
  tag_dimension,
  tag_value,
  COUNT(DISTINCT conversation_id) AS convo_count
FROM (
  SELECT
    id AS conversation_id,
    JSON_EXTRACT_SCALAR(tag, '$.tag') AS tag_value,
    CASE
      WHEN JSON_EXTRACT_SCALAR(tag, '$.tag') LIKE 'type:%' THEN 'type'
      WHEN JSON_EXTRACT_SCALAR(tag, '$.tag') LIKE 'product -%' THEN 'product'
      WHEN JSON_EXTRACT_SCALAR(tag, '$.tag') LIKE 'product%' THEN 'product'
      WHEN JSON_EXTRACT_SCALAR(tag, '$.tag') LIKE 'l_ -%' THEN 'escalation'
      WHEN JSON_EXTRACT_SCALAR(tag, '$.tag') LIKE 's_ -%' THEN 'severity'
      WHEN JSON_EXTRACT_SCALAR(tag, '$.tag') LIKE 'status:%' THEN 'status'
      ELSE 'other'
    END AS tag_dimension
  FROM `supercat-data-pipeline.helpscout.conversations`,
       UNNEST(JSON_QUERY_ARRAY(tags)) AS tag
  WHERE PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', LEFT(createdAt, 19))
        >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
    AND status != 'spam'
    AND LOWER(REGEXP_EXTRACT(SAFE.STRING(primaryCustomer.email), r'@(.+)$'))
        IN ({client_email_domains})
)
GROUP BY tag_dimension, tag_value
ORDER BY tag_dimension, convo_count DESC
```

**Usage**: The operator reads this output and synthesizes themes from the `type` dimension. The `escalation` and `severity` dimensions feed the Escalation Profile. The `status` dimension identifies Jira-linked tickets.

### Q-IB-HELP-AGG: Support Summary Metrics

Single-row summary for the one-liner.

```sql
SELECT
  COUNT(*) AS total_conversations,
  COUNTIF(status = 'active') AS open_conversations,
  COUNTIF(status = 'closed') AS closed_conversations,
  COUNTIF(
    LOWER(TO_JSON_STRING(tags)) LIKE '%l2 -%'
    OR LOWER(TO_JSON_STRING(tags)) LIKE '%l3 -%'
    OR LOWER(TO_JSON_STRING(tags)) LIKE '%l4 -%'
  ) AS escalations_l2_plus,
  COUNTIF(
    LOWER(TO_JSON_STRING(tags)) LIKE '%s1 -%'
    OR LOWER(TO_JSON_STRING(tags)) LIKE '%s2 -%'
  ) AS high_severity_count,
  COUNTIF(
    LOWER(TO_JSON_STRING(tags)) LIKE '%status: logged on jira%'
  ) AS jira_linked
FROM `supercat-data-pipeline.helpscout.conversations`
WHERE PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', LEFT(createdAt, 19))
      >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  AND status != 'spam'
  AND LOWER(REGEXP_EXTRACT(SAFE.STRING(primaryCustomer.email), r'@(.+)$'))
      IN ({client_email_domains})
```

### Q-IB-HELP-AGING: Open Ticket Aging

All currently open tickets for this client, sorted by age (oldest first).

```sql
SELECT
  id,
  subject,
  status,
  createdAt,
  TIMESTAMP_DIFF(
    CURRENT_TIMESTAMP(),
    PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', LEFT(createdAt, 19)),
    DAY
  ) AS days_open,
  TO_JSON_STRING(tags) AS tags_json
FROM `supercat-data-pipeline.helpscout.conversations`
WHERE status = 'active'
  AND LOWER(REGEXP_EXTRACT(SAFE.STRING(primaryCustomer.email), r'@(.+)$'))
      IN ({client_email_domains})
ORDER BY createdAt ASC
```

**Note**: No time window filter — shows ALL open tickets regardless of when they were created.

### Q-IB-HELP-EXTENDED: 180-Day Context (conditional)

Run ONLY if Q-IB-HELP-AGG returns < 3 total conversations in 90 days. Extends the window to 180 days for theme analysis.

```sql
-- Same as Q-IB-HELP-THEMES but with INTERVAL 180 DAY
-- Same as Q-IB-HELP-DETAIL but with INTERVAL 180 DAY
```

---

## 5. Jira Queries (Atlassian MCP)

### Q-IB-JIRA-DISCOVER: Get Cloud ID

**MCP**: `plugin-atlassian-atlassian` → `getAccessibleAtlassianResources`

No parameters. Returns list of accessible Atlassian sites with cloud IDs.

Cache the `cloudId` for subsequent queries.

### Q-IB-JIRA-SEARCH: Client Tickets

**MCP**: `plugin-atlassian-atlassian` → `searchJiraIssuesUsingJql`

**Strategy**: Try multiple JQL queries in order. Use the first one that returns results.

**Attempt 1** — search by client name in text:
```
cloudId: {cloud_id}
jql: "text ~ \"{client_name}\" AND statusCategory != Done ORDER BY created DESC"
fields: ["summary", "status", "priority", "created", "updated", "assignee", "issuetype", "project"]
maxResults: 20
```

**Attempt 2** — search by shortname:
```
cloudId: {cloud_id}
jql: "text ~ \"{shortname}\" AND statusCategory != Done ORDER BY created DESC"
fields: ["summary", "status", "priority", "created", "updated", "assignee", "issuetype", "project"]
maxResults: 20
```

**Attempt 3** — search in CSP project (client-specific):
```
cloudId: {cloud_id}
jql: "project = CSP AND text ~ \"{client_name}\" ORDER BY created DESC"
fields: ["summary", "status", "priority", "created", "updated", "assignee", "issuetype"]
maxResults: 20
```

**Output**: Filter results to only those genuinely related to this client (text search may return false positives). Flag:
- Any ticket with `priority` = "Highest" or "High"
- Any ticket where `updated` is > 14 days ago (stale)
- Any ticket with status containing "blocked"

### Q-IB-JIRA-FALLBACK: ~~BigQuery Jira~~ — RETIRED 2026-06-04

There is **no BigQuery fallback for Jira.** Jira's only source is the Atlassian MCP
(`plugin-atlassian-atlassian`, used by Q-IB-JIRA-DISCOVER / Q-IB-JIRA-SEARCH above).

The former fallback queried `WELD_RAW.jira_issues` via the legacy `user-bigquery-vpn` (Weld) connection.
That table exists only in the stale `WELD_RAW` dataset — there is **no `jira` dataset** in
`supercat-data-pipeline` (verified 2026-06-04) — and the Weld layer is being decommissioned.

**If the Atlassian MCP is unavailable**: note Jira as unavailable and fall back to the HelpScout
`status: logged on jira` tag signal (the `jira_linked` count from Q-IB-HELP-AGG). Do **not** query
BigQuery for Jira.

---

## 6. MAL CSV (Local File Read — Optional)

### Q-IB-MAL: Cohort Year

**Source**: `Health V2/inputs/master_account_list_{date}_canonical.csv`

**Method**: Read CSV, match on company name or org_shortname.

**Required columns**: `cohort_year`

**If unavailable**: Omit cohort year from Account Snapshot. Not blocking.

---

## Query Execution Order

```
Step 1: Q-IB-HEALTH     → Load health data (blocking — cannot proceed without it)
Step 2: Q-IB-ORG         → org_summary config flags
        Q-IB-DOMAIN      → Email domains for HelpScout attribution
Step 3: Q-IB-HELP-AGG    → Support summary metrics
        Q-IB-HELP-DETAIL → Individual conversations
        Q-IB-HELP-THEMES → Tag distribution for theme analysis
        Q-IB-HELP-AGING  → Open ticket aging
        (All HelpScout queries can run in parallel)
Step 4: Q-IB-JIRA-DISCOVER → Get cloud ID
        Q-IB-JIRA-SEARCH   → Search for client tickets (sequential — needs cloud ID)
Step 5: Q-IB-MAL         → Cohort year (optional)
Step 6: Generate sections 2-5
Step 7: Generate section 1 (Verdict — written last)
```

Steps 2 and 3 can run in parallel. Step 4 depends on the cloud ID from DISCOVER. Steps 2-5 are all independent of each other.

---

## Tag Vocabulary Reference

Discovered from production HelpScout data (2026-04-20). All `type:` and escalation tags available for theme analysis.

### Escalation Levels
| Tag | Meaning |
|-----|---------|
| `l1 - handled by frontline support` | Resolved by support team |
| `l2 - requires internal collaboration` | Needed internal team input |
| `l3 - engineering intervention` | Required engineering work |
| `l4 - strategic decision or executive involvement` | Executive escalation |

### Severity Levels
| Tag | Meaning |
|-----|---------|
| `s1 - critical` | Critical issue |
| `s2 - high` | High severity |
| `s3 - medium` | Medium severity |
| `s4 - low` | Low severity |

### Type Tags (for theme grouping)
| Tag | Description |
|-----|-------------|
| `type: training` | How-to, workflow questions |
| `type: user management` | Account access, permissions |
| `type: data-sync imports and exports` | Import/export issues |
| `type: bug` | Software defects |
| `type: feature request` | Enhancement requests |
| `type: config issue` | Configuration problems |
| `type: orders invoices and pmt integration` | Order/payment integration |
| `type: image asset` | Product image issues |
| `type: manual work` | Tasks requiring manual intervention |
| `type: sales and finance` | Sales/billing related |

### Product Tags
| Tag | Description |
|-----|-------------|
| `product - admin console` | Backend management |
| `product - ecat` | iPad app |
| `product - eol` | eCat Online |
| `product - sales portal` | Sales Portal |
| `product - staging` | Staging environment |

### Status Tags (workflow state)
| Tag | Description |
|-----|-------------|
| `status: logged on jira` | Issue tracked in Jira |
| `status: blocked` | Blocked on something |
| `status: investigating` | Under investigation |
| `status: waiting on client` | Waiting for client response |
| `status: support project` | Ongoing support project |
| `status: meeting scheduled` | Meeting planned |
