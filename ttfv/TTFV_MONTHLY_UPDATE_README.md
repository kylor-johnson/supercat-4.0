# TTFV Monthly Update - Complete Guide

## Quick Start (Copy This Prompt)

```
Read @ttfv/TTFV_MONTHLY_UPDATE_README.md and run the monthly TTFV update for [MONTH YEAR]
```

---

## What This Updates

Two CSV files track the trailing 90-day TTFV metric:

- **Main:** `ttfv/2026_clients_trailing_90day_ttfv.csv` — trailing 90-day average as Excel-style formula
- **Detail:** `ttfv/2026_clients_trailing_90day_ttfv_calculation_detail.csv` — breakdown by client
- **Frequency:** Run monthly (first week of new month for prior month)

---

## How the Metric Works

**TTFV** = days between a client's **HubSpot deal close date** and the first time a non-admin sales rep performs a qualifying value action in Mixpanel.

**Trailing 90-Day Window:** A client appears in month M's calculation if their **first value date** (first qualifying Mixpanel event after their close date) falls within the 90 days ending on the last day of month M.

- Client enters the window the month their first value date falls in
- Client exits the window once their first value date is more than 90 days before the end of the month
- Clients with no qualifying Mixpanel events yet are excluded (still onboarding)

**Value Actions (Mixpanel Events):**
- `item_added_via_magic_button` — rep added a product to a presentation
- `document_email_drafted` or `item_email_drafted` — rep drafted a customer email

Only non-admin users count. Admin activity (setup, training, testing) does not qualify.

---

## Monthly Update Process

### Step 0: Start from the subscription list, then add new clients who have no subscription yet

Do this every run. Do not start from a saved CSV.

**The MAL** is every org with `subscriptions.status = 'active'`. That is the client book. **The clock** is still the HubSpot closed-won date.

Some new clients are already Active or Onboarding in admin and do not have a subscription row yet. Add those too, but only when they have a closed-won deal. Organization Status by itself is not membership. An Active shell with no won deal is not a client.

As of 2026-11-04 the gap is `mer` (111Mercer, Active, closed won 2026-08-04) and `leg` (Legrand US, Onboarding, closed won 2026-06-11). `libco` and `drf` already have active subscriptions, so they are on the MAL. Wind River (`wr`) is Active and has no subscription, and it is not part of this gap: no org users, and neither HubSpot deal is closed-won.

Candidate orgs to check for that gap:

```sql
SELECT
  o.shortname,
  btrim(o.name) AS name,
  o.properties->>'status' AS org_status,
  o.created_at::date AS created_at
FROM organizations o
WHERE o.properties->>'status' IN ('active', 'onboarding')
  AND o.sandbox_of_id IS NULL
  AND o.shortname !~* '(test|demo|staging|sandbox|template)'
  AND o.shortname NOT IN (
    'bmc2','bmc3','temp','tmpl','tmpo','tech','tle','vc','wmo',
    'demo','demo1','demo2','demo3','demolighting','ei','hl','kylademo',
    'emerydemo','waledemo',
    'ahtest','bc2','bri_test','clctest','pf_test','wwtest','ufitest',
    'ufistaging','mhstage','fmsstaging','tlastaging','vcgstaging',
    'fccstaging','bpstaging','tam-staging','cfsd','slusa',
    'gww','sc_test','sic','ctest','test1','omc'
  )
ORDER BY o.created_at
```

Why both statuses: `active` is the rule. `onboarding` stays in because a real new client can sit there before anyone flips the status. As of 2026-11-04 the only real Onboarding org after the junk filter is Legrand US (`leg`). `tmpl`, `tmpo`, and `hl` are templates or a demo and the filters above remove them.

Status values that stay out: `demo`, `test`, `inactive`, `sync_suspended`, `fully_suspended`. The shortname filter is still required, because some staging orgs are marked Active (`ihw_staging`, `ufistaging`, `tam-staging`, `demo1`).

Then get HubSpot close dates for that universe. Use the earliest closed-won deal that is the initial go-live, not an upsell.

Query BigQuery for closed-won deals with an org ID in the last 18 months:

```sql
SELECT
  properties_existing_client_org_id AS org_shortname,
  properties_dealname AS deal_name,
  DATE(properties_closedate) AS close_date
FROM `supercat-data-pipeline.hubspot.deal`
WHERE properties_hs_is_closed_won = true
  AND properties_existing_client_org_id IS NOT NULL
  AND DATE(properties_closedate) >= DATE_SUB(CURRENT_DATE(), INTERVAL 18 MONTH)
ORDER BY close_date DESC
```

This gives you the client list and their TTFV clock start dates. Use the **earliest closed-won deal** per org if an org has multiple deals.

**Note:** Some orgs have multiple deals (expansions, add-ons). For TTFV, use the deal that represents the client's initial go-live, not upsells. Use judgment or the deal name to identify the primary onboarding deal.

**ALSO query for orphan closed-won deals missing the org_id link.** Newer deals are often created in HubSpot before `properties_existing_client_org_id` is set, so they get silently dropped from the cohort:

```sql
SELECT properties_dealname AS deal_name, DATE(properties_closedate) AS close_date
FROM `supercat-data-pipeline.hubspot.deal`
WHERE properties_hs_is_closed_won = true
  AND properties_existing_client_org_id IS NULL
  AND DATE(properties_closedate) >= DATE_SUB(CURRENT_DATE(), INTERVAL 18 MONTH)
ORDER BY close_date DESC
```

For each orphan, map the deal name to a Postgres `organizations.shortname` (search by `name`) and use that close date as the clock. If that org has no subscription row and its status is Active or Onboarding, add it. Examples: `mer` (111Mercer, closed won 2026-08-04, org id still blank), and earlier `drf`, `libco`, and `mali`. Flag these to HubSpot ops so the org id gets populated. A deal that is not closed-won does not add an org.

**Watch for parent/sub-org mismatches.** When a deal's `properties_existing_client_org_id` points at the parent (e.g. `ta` Theodore Alexander) but a separate Postgres org exists for the location/subsidiary (e.g. `tam` Theodore Alexander Manhasset), use the Postgres shortname that actually matches the deal name and was provisioned for that engagement.

---

### Step 1: Get Admin Users

For each org from Step 0, get the list of admin usernames to exclude from Mixpanel:

```sql
SELECT LOWER(u.username) AS username, o.shortname
FROM users u
JOIN org_users ou ON ou.user_id = u.id
JOIN organizations o ON o.id = ou.organization_id
WHERE ou.is_admin = true
  AND o.shortname IN ([ORG_SHORTNAMES_FROM_STEP_0])
ORDER BY o.shortname, u.username
```

---

### Step 2: Get First Value Dates from Mixpanel

For each org, find the first qualifying event by a non-admin user **on or after their HubSpot close date**:

```sql
SELECT org_shortname, MIN(event_date) AS first_value_date
FROM (
  SELECT
    LOWER(COALESCE(
      NULLIF(organization_shortname, ''),
      NULLIF(current_organization_shortname, '')
    )) AS org_shortname,
    DATE(TIMESTAMP_SECONDS(CAST(time AS INT64))) AS event_date
  FROM `supercat-data-pipeline.mixpanel.events`
  WHERE event_name IN ('item_added_via_magic_button', 'document_email_drafted', 'item_email_drafted')
    AND LOWER(username) NOT IN ([ADMIN_LIST_FROM_STEP_1])
    AND LOWER(COALESCE(
      NULLIF(organization_shortname, ''),
      NULLIF(current_organization_shortname, '')
    )) IN ([ORG_SHORTNAMES_FROM_STEP_0])
    AND DATE(TIMESTAMP_SECONDS(CAST(time AS INT64))) >= [HUBSPOT_CLOSE_DATE_FOR_THAT_ORG]
)
GROUP BY org_shortname
```

Then compute:
```
TTFV_days = first_value_date - hubspot_close_date
```

---

### Step 3: Determine Who Is In the Trailing 90-Day Window

For month M (e.g., April 2026 = window Feb 1 – Apr 30, 2026):

A client is **in the window** if:
- They have achieved TTFV (first value date exists), AND
- Their first value date falls between `(last day of M) - 90 days` and `last day of M`

A client is **not in the window** if:
- No qualifying Mixpanel event exists yet (still onboarding), OR
- Their first value date is outside the 90-day range

**Calculate the average:**
```
Trailing_90Day_TTFV = Sum of TTFV days for all in-window clients / Count of in-window clients
```

Leave the cell **blank** (not zero) if no clients are in the window.

---

### Step 4: Update Both CSVs

**1. Main CSV** — `ttfv/2026_clients_trailing_90day_ttfv.csv`

Add the new month column with an Excel-style formula showing the calculation:
```
=(ttfv_org1 + ttfv_org2 + ...)/client_count
```
Example: `=(205)/1` for one client with 205-day TTFV.

**2. Calculation Detail CSV** — `ttfv/2026_clients_trailing_90day_ttfv_calculation_detail.csv`

Add the new month column across all four rows:
- `Trailing_90Day_TTFV` — computed average (numeric)
- `Clients_in_Window` — count
- `Total_Days_in_Window` — sum of individual TTFV values
- `Clients` — org shortnames separated by `+`

---

## Data Sources

| Data | Source | Field |
|------|--------|-------|
| Who is in the run | SuperCat Postgres `subscriptions` | `status = 'active'`, plus a closed-won Active or Onboarding org that has no subscription yet |
| TTFV start date (close date) | `supercat-data-pipeline.hubspot.deal` | `properties_closedate` |
| Org shortname on the deal | `supercat-data-pipeline.hubspot.deal` | `properties_existing_client_org_id` (blank does not drop the org) |
| First value events | `supercat-data-pipeline.mixpanel.events` | `event_name`, `username`, `time` |
| Admin exclusions | SuperCat Postgres `org_users` | `is_admin = true` |

---

## Success Criteria

1. New month column added to both CSVs
2. Main CSV formula shows the calculation breakdown
3. Detail CSV has all four rows populated
4. Value is reasonable — flag anything above 150 days for CS team review
5. Blank cells only where no clients have a first value date in the window

---

## Troubleshooting

### "Unexpected org in results (e.g., a legacy client)"
- Check `properties_existing_client_org_id` in HubSpot — the deal's close date may have been updated recently, making an old client look new
- Verify `properties_closedate` is the original deal close, not a renewal

### "Client expected to appear but doesn't"
- Re-run Step 0. The MAL is orgs with an active subscription. Also add an Active or Onboarding org that has a closed-won deal and no subscription row yet
- Check if they have qualifying Mixpanel events after their close date by a non-admin user who has an `org_users` row
- Confirm their first value date is within the trailing 90-day window for this month
- If the HubSpot org id is blank, match the deal name to the shortname and use that close date anyway

### "TTFV seems too high (>150 days)"
- Client may have had onboarding delays or training gaps
- Check whether all non-admin users have been correctly identified
- Flag for CS team follow-up

### "Negative TTFV values"
- Normal — client had qualifying activity before deal close (pilot period)
- Include in calculation

---

## File Structure

```
ttfv/
├── TTFV_MONTHLY_UPDATE_README.md                              # This file — run instructions
├── TTFV_Methodology_Overview.md                               # Background on what/why
├── 2026_clients_trailing_90day_ttfv.csv                       # Main output — formula per month
└── 2026_clients_trailing_90day_ttfv_calculation_detail.csv    # Detail — clients, counts, totals per month
```

---

## Complete Monthly Update Prompt

Copy and paste this each month:

```
Read @ttfv/TTFV_MONTHLY_UPDATE_README.md

Run the monthly TTFV update for [MONTH YEAR]:

Step 0: Start from orgs with an active subscription (the MAL). Then add Active or
Onboarding orgs that have a closed-won deal and no subscription row yet. That query
is in this file. Attach HubSpot closed-won dates, including deals whose org id is
still blank. Use properties_closedate as the TTFV start. Do not add an Active org
that has no closed-won deal.

Step 1: Query Postgres org_users to get admin usernames for each org from Step 0.

Step 2: Query Mixpanel (BigQuery) for first qualifying value event per org, by non-admin
users only, on or after the org's HubSpot close date.

Step 3: Identify which orgs have a first value date in the trailing 90-day window ending
[LAST DAY OF MONTH]. Calculate average TTFV for those orgs.

Step 4: Update both CSVs:
- ttfv/2026_clients_trailing_90day_ttfv.csv — add [MONTH] column with formula
- ttfv/2026_clients_trailing_90day_ttfv_calculation_detail.csv — add [MONTH] column with breakdown

Step 5: Show the calculation and flag any clients with TTFV > 150 days or still no first value event.
```

---

Last updated: November 4, 2026
