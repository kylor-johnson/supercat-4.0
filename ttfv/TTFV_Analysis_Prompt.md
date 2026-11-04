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
Two clocks exist. Do not mix them in one average.

- **Monthly trailing series:** HubSpot `properties_closedate`. This is the series in the two CSVs. Instructions are `TTFV_MONTHLY_UPDATE_README.md`.
- **This prompt, full-book snapshot only:** `MIN(subscriptions.start_date)` where the subscription is active. An org with no subscription stays in the output with a blank clock. `organizations.created_at` is not a clock.

### Required Steps (MUST FOLLOW IN ORDER)

**Step 1: Get the org universe, then the clock**
The org list is Organization Status, not a subscription. Use the same query as Step 0 in `ttfv/TTFV_MONTHLY_UPDATE_README.md`: status `active` or `onboarding`, `sandbox_of_id` null, shortname not matching test/demo/staging/sandbox/template, plus the hard-coded junk list.

For this full-book snapshot, left-join `subscriptions` and use `MIN(start_date)` where `s.status = 'active'` as the clock. An org in the universe with no active subscription stays in the output with start date blank and TTFV blank. Do not drop it.

The monthly trailing series does not use this clock. It uses the HubSpot close date. Run that from `TTFV_MONTHLY_UPDATE_README.md`.

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
- Membership is Organization Status `active` or `onboarding`, after the junk filters in Step 1. A missing subscription does not remove the org
- Use `MIN(start_date)` per org if multiple active subscription rows exist. If none exist, leave the full-book clock blank

### Output Format
Format the report using `ttfv/TTFV_Report_Format_Template.md`
```

---

## Data Sources

| Source | Table | Purpose |
|--------|-------|---------|
| Postgres | `organizations` | Who is in the run (`properties->>'status'`) |
| Postgres | `subscriptions` | Full-book clock only (`start_date`), when a row exists |
| Postgres | `org_users` + `users` | Get admin users, validate TTFV users |
| BigQuery | `supercat-data-pipeline.mixpanel.events` | Get TTFV events |

---

## Notes

- The monthly trailing series uses the HubSpot close date as the clock. See `TTFV_MONTHLY_UPDATE_README.md`
- This prompt's full-book clock is `subscriptions.start_date` when an active row exists. It is not the membership test
- `organizations.created_at` is not a clock
- The `is_admin` flag in Postgres `org_users` table is the source of truth for admin status
- Users without an `org_users` record should be excluded (may be deleted users)
- Run this monthly to track TTFV for new clients
- Orgs that are Active or Onboarding and have no subscription row stay in the run. 111Mercer (`mer`), Wind River (`wr`), and Legrand US (`leg`) were dropped by the old subscription filter. That filter is retired
