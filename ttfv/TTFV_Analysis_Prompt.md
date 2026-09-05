# TTFV Analysis Prompt

Use this prompt to calculate validated TTFV (Time to First Value) for any set of clients.

---

## Reference Files

| File | Purpose |
|------|---------|
| `ttfv/TTFV_Report_Format_Template.md` | Report formatting template |

> **Note:** `active_orgs.csv` is a legacy static file. The authoritative active client list is now derived live from Postgres — see Step 1 below.

---

## Prompt

```
Calculate the TTFV (Time to First Value) for the following clients: [LIST CLIENT NAMES HERE]

To run for ALL active clients, use: "Calculate the TTFV for all active clients" and follow Step 1 below to query Postgres directly.

### TTFV Definition
TTFV = Days from Start Date to the first time a NON-ADMIN sales rep performed either:
1. `item_added_via_magic_button` - Added a product to a list (Presentation/Stack)
2. `document_email_drafted` OR `item_email_drafted` - Drafted an email (Email Draft)

### Start Date
- **Source of truth**: `subscriptions.start_date` from Postgres — the date the org's subscription became active
- This replaces HubSpot deal close date and `organizations.created_at` as the TTFV clock start
- Use `MIN(start_date)` per org in case multiple subscription rows exist

### Required Steps (MUST FOLLOW IN ORDER)

**Step 1: Get Active Org List and Start Dates**
Query Postgres to get all active, non-demo/test orgs and their subscription start dates:
```sql
SELECT
  o.shortname AS org_shortname,
  o.name AS org_name,
  MIN(s.start_date) AS start_date
FROM organizations o
JOIN subscriptions s ON s.organization_id = o.id
WHERE s.status = 'active'
  AND LOWER(o.shortname) NOT SIMILAR TO '%(test|demo|staging|sandbox|template)%'
  AND o.shortname NOT IN (
    'bmc2','bmc3','temp','tmpl','tmpo','tech','tle','vc','wmo',
    'demo','demo1','demo2','demo3','demolighting','ei','hl','kylademo',
    'emerydemo','waledemo',
    'ahtest','bc2','bri_test','clctest','pf_test','wwtest','ufitest',
    'ufistaging','mhstage','fmsstaging','tlastaging','vcgstaging',
    'fccstaging','bpstaging','tam-staging','cfsd','slusa',
    'gww','sc_test','sic','ctest','test1','omc'
  )
GROUP BY o.shortname, o.name
ORDER BY start_date
```

If analyzing a **specific cohort year** (e.g., 2025 new clients), add a date filter:
```sql
  AND s.start_date >= '2025-01-01' AND s.start_date < '2026-01-01'
```

If analyzing **specific named clients**, filter by shortname:
```sql
  AND o.shortname IN ('mlg', 'wag', 'luc')  -- replace with target orgs
```

**Step 2: Get Admin Users Per Org**
Query Postgres to get ALL admin usernames for each org:
```sql
SELECT u.username, o.shortname as org
FROM org_users ou
JOIN users u ON ou.user_id = u.id
JOIN organizations o ON ou.organization_id = o.id
WHERE ou.is_admin = true
  AND o.shortname IN ([ORG_SHORTNAMES])
```

**Step 3: Calculate TTFV Per Org**
For EACH org separately, query BigQuery `supercat-data-pipeline.mixpanel.events`:
- Filter by the org's shortname
- Exclude ALL admin usernames from Step 2 for that specific org
- Find the MIN timestamp for qualifying events
- Determine first action type (Presentation vs Email Draft)

**Step 4: Identify the TTFV User**
For each org, get the specific username whose event is being used:
```sql
SELECT username, event_name, DATE(TIMESTAMP_SECONDS(CAST(time AS INT64))) as event_date
FROM supercat-data-pipeline.mixpanel.events
WHERE event_name IN ('item_added_via_magic_button', 'document_email_drafted', 'item_email_drafted')
  AND LOWER(current_organization_shortname) = '[ORG]'
  AND LOWER(username) NOT IN ([ADMIN_LIST_FOR_ORG])
ORDER BY time ASC
LIMIT 1
```

**Step 5: Validate TTFV User is Non-Admin**
Query Postgres to confirm EACH TTFV user has `is_admin = FALSE`:
```sql
SELECT u.username, o.shortname, ou.is_admin
FROM org_users ou
JOIN users u ON ou.user_id = u.id
JOIN organizations o ON ou.organization_id = o.id
WHERE LOWER(u.username) = '[USERNAME]' AND o.shortname = '[ORG]'
```
- If user has no org_users record, EXCLUDE them and use the next earliest user
- Only users with `is_admin = FALSE` are valid

**Step 6: Calculate Days**
TTFV (Days) = First Action Date - Start Date (from Step 1)

### Key Rules
- MUST exclude both SuperCat admins AND client admins (use `is_admin` flag from Postgres)
- MUST validate each TTFV user exists in org_users with is_admin = FALSE
- If a user has Mixpanel events but no org_users record, they are INVALID - use next user
- Orgs with no subscription row or no `active` subscription are NOT eligible — do not include them
- Use `MIN(start_date)` per org if multiple active subscription rows exist

### Output Format
Format the report using `ttfv/TTFV_Report_Format_Template.md`
```

---

## Data Sources

| Source | Table | Purpose |
|--------|-------|---------|
| Postgres | `organizations` + `subscriptions` | Active client list and TTFV Start Date (`start_date`) |
| Postgres | `org_users` + `users` | Get admin users, validate TTFV users |
| BigQuery | `supercat-data-pipeline.mixpanel.events` | Get TTFV events |

---

## Notes

- `subscriptions.start_date` is the authoritative TTFV clock start — it reflects when the org actually went live as a paying customer
- HubSpot deal close dates and `organizations.created_at` are no longer used as start dates
- The `is_admin` flag in Postgres `org_users` table is the source of truth for admin status
- Users without an `org_users` record should be excluded (may be deleted users)
- Run this monthly to track TTFV for new clients
- Orgs that appear "active" in the admin console but have no `subscriptions` row with `status = 'active'` are not yet billable and should be excluded until their subscription is provisioned
