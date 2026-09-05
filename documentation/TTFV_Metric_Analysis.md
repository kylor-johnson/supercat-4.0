# TTFV (Time to First Value) Metric

## Definition

**TTFV** = The earliest date when a non-admin sales rep performed either:
1. `item_added_via_magic_button` - Added a product to a list (customer list or maybe list)
2. `document_email_drafted` OR `item_email_drafted` - Drafted an email to share product info

This represents the moment a rep first used eCat to do real work (curating products for customers or sharing product information).

---

## How to Calculate TTFV

### Data Sources
- **Mixpanel events** in BigQuery: `supercat-data-pipeline.WELD_RAW.mixpanel__events`
- Filter by `current_organization_shortname` for specific clients

### Excluding Admin/Test Users
To ensure we only measure real sales rep usage, exclude these SuperCat internal usernames who are admins across many client orgs:

```
swt, kjael, cwiebe, angie, kylor_johnson, mcp-admin, brentsanders, 
chuck-admin, sarahm, jthrasher, jlowe1, support, jonv, chuck-user, 
brucew, badkins, ognezdyonova, kyla, mridge, wale
```

These users are admins in 50-160+ orgs each and are primarily used for testing/support.

---

## TTFV Query

```sql
SELECT 
  LOWER(username) as username,
  LOWER(current_organization_shortname) as org,
  MIN(CASE WHEN event_name = 'item_added_via_magic_button' 
      THEN TIMESTAMP_SECONDS(CAST(time AS INT64)) END) as first_add_to_list,
  MIN(CASE WHEN event_name IN ('document_email_drafted', 'item_email_drafted') 
      THEN TIMESTAMP_SECONDS(CAST(time AS INT64)) END) as first_email_drafted,
  LEAST(
    MIN(CASE WHEN event_name = 'item_added_via_magic_button' 
        THEN TIMESTAMP_SECONDS(CAST(time AS INT64)) END),
    MIN(CASE WHEN event_name IN ('document_email_drafted', 'item_email_drafted') 
        THEN TIMESTAMP_SECONDS(CAST(time AS INT64)) END)
  ) as ttfv_date
FROM mixpanel__events
WHERE event_name IN ('item_added_via_magic_button', 'document_email_drafted', 'item_email_drafted')
  AND current_organization_shortname IS NOT NULL
  -- Exclude SuperCat internal admin/test users
  AND LOWER(username) NOT IN (
    'swt', 'kjael', 'cwiebe', 'angie', 'kylor_johnson', 
    'mcp-admin', 'brentsanders', 'chuck-admin', 'sarahm', 'jthrasher', 
    'jlowe1', 'support', 'jonv', 'chuck-user', 'brucew', 
    'badkins', 'ognezdyonova', 'kyla', 'mridge', 'wale'
  )
GROUP BY LOWER(username), LOWER(current_organization_shortname)
HAVING ttfv_date IS NOT NULL
ORDER BY ttfv_date DESC;
```

### For a Specific Organization

Add a filter for the org shortname:

```sql
AND LOWER(current_organization_shortname) = 'cci'
```

### For New Clients (Last 90 Days)

```sql
HAVING ttfv_date >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
```

---

## Monthly TTFV Report Prompt

Use this prompt to generate TTFV metrics for new clients:

> Calculate the TTFV (Time to First Value) for new clients from the last [X] days/months.
> 
> TTFV is defined as the earliest date a non-admin user either:
> 1. Added a product to a list (item_added_via_magic_button event)
> 2. Drafted an email (document_email_drafted or item_email_drafted events)
> 
> Use the BigQuery mixpanel__events table and exclude these SuperCat internal usernames:
> swt, kjael, cwiebe, angie, kylor_johnson, mcp-admin, brentsanders, chuck-admin, sarahm, jthrasher, jlowe1, support, jonv, chuck-user, brucew, badkins, ognezdyonova, kyla, mridge, wale
> 
> Group by username and org, and show the TTFV date for each rep.

---

## Output Columns

| Column | Description |
|--------|-------------|
| `username` | The user's login username |
| `org` | Organization shortname |
| `first_add_to_list` | First time they added a product to a list |
| `first_email_drafted` | First time they drafted an email |
| `ttfv_date` | **TTFV** - the earlier of the two dates above |

---

## Notes

- The `type` field in the magic button event shows what kind of list: `customer` (customer-specific list), `maybe` (maybe list), or `user` (personal list)
- TTFV is calculated per user per organization (a user could have different TTFV dates in different orgs)
- The exclusion list covers SuperCat staff; individual client admins testing during implementation are not excluded but typically represent minimal noise once reps are onboarded
