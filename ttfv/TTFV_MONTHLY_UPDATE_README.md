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

### Step 0: Get Recent Closed-Won Clients from HubSpot (Do This First)

The TTFV cohort is defined by **HubSpot closed-won deals**, not Postgres subscriptions. Postgres `subscriptions.start_date` reflects when a subscription was provisioned or renewed — it is not the TTFV clock. Use HubSpot close date as the TTFV start.

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

For each orphan, map the deal name to a Postgres `organizations.shortname` (search by `name`) and add it to the master list manually. Examples that bit us in past runs: `drf` (Dorell Fabrics), `tcs` (The Coppersmith), `libco` (Lib and Co.), `mali` (Magic Lite | NSL). Flag these to HubSpot ops so the org_id gets populated upstream.

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
| TTFV start date (close date) | `supercat-data-pipeline.hubspot.deal` | `properties_closedate` |
| Org shortname | `supercat-data-pipeline.hubspot.deal` | `properties_existing_client_org_id` |
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
- Check if they have qualifying Mixpanel events after their close date by a non-admin user
- Confirm their first value date is within the trailing 90-day window for this month
- Check that their HubSpot deal has `properties_existing_client_org_id` populated

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

Step 0: Query `supercat-data-pipeline.hubspot.deal` for closed-won deals with a non-null
properties_existing_client_org_id, closed in the last 18 months. Use properties_closedate
as the TTFV start date for each org.

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

Last updated: June 2, 2026
