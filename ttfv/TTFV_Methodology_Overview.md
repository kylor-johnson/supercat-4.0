# Time to First Value (TTFV) Methodology

## What It Measures

TTFV measures how quickly a new client's sales team starts actively using SuperCat after their deal closes. It answers: **How long does it take before a real sales rep does something meaningful in the platform?**

**Formula:**
```
TTFV = First Value Date - HubSpot Deal Close Date (in days)
```

---

## TTFV Start Date

**Source: HubSpot deal close date** (`supercat-data-pipeline.hubspot.deal.properties_closedate`)

This is the date the contract was signed. It is the TTFV clock start for all clients.

**Do not use:**
- `subscriptions.start_date` from Postgres — this reflects when a subscription was provisioned or renewed, which may lag the close date or be updated independently
- `organizations.created_at` from Postgres — this is when the org record was created, not when the client signed

If a client has multiple HubSpot deals (expansions, add-ons), use the deal representing their original go-live, not upsells.

---

## TTFV End Date (First Value)

**Source: Mixpanel events** (`supercat-data-pipeline.mixpanel.events`)

The first date a **non-admin** user performs a qualifying value action after the close date:

| Event | What It Means |
|-------|---------------|
| `item_added_via_magic_button` | Rep added a product to a presentation |
| `document_email_drafted` | Rep drafted a customer-facing email |
| `item_email_drafted` | Rep drafted a customer-facing email (item-level) |

Admin users (identified via Postgres `org_users.is_admin = true`) are excluded. Admin activity during setup, training, or testing does not represent real sales adoption.

If a client has qualifying activity **before** their close date (pilot period), TTFV will be negative — this is valid and included in calculations.

---

## Trailing 90-Day Window

The monthly metric is a **trailing 90-day average**: the average TTFV across all clients whose **first value date** falls within the 90-day period ending on the last day of the month.

- A client **enters** the window in the month their first value date falls in
- A client **exits** the window once their first value date is more than 90 days before the end of the current month
- Clients with no first value date yet are excluded (still onboarding)

Example — April 2026 (window: Feb 1 – Apr 30, 2026):
- Include clients whose first value date is between Feb 1 and Apr 30
- Exclude clients whose first value date is before Feb 1 or who haven't hit first value yet

---

## What TTFV Tells Us

| Result | Indication |
|--------|------------|
| Low (< 60 days) | Smooth onboarding, engaged sales team |
| Medium (60–120 days) | Normal ramp — monitor |
| High (> 150 days) | Onboarding friction, training gaps, or adoption challenges — CS follow-up recommended |
| No TTFV yet | Client still ramping, or may need enablement support |

---

## Data Sources

| Data | Source | Field |
|------|--------|-------|
| TTFV start (close date) | `supercat-data-pipeline.hubspot.deal` | `properties_closedate` |
| Org shortname | `supercat-data-pipeline.hubspot.deal` | `properties_existing_client_org_id` |
| First value events | `supercat-data-pipeline.mixpanel.events` | `event_name`, `username`, `time` |
| Admin exclusions | SuperCat Postgres `org_users` | `is_admin = true` |

---

## Known Limitations

- **Mixpanel tracking started Nov 2024** — clients who achieved first value before then have no Mixpanel record; TTFV is unmeasurable for them
- **Multiple deals per org** — expansions and add-ons create multiple HubSpot deals; use the original go-live deal for TTFV
- **Admin-only orgs** — small clients with only admin users are unmeasurable
- **Pilot activity** — pre-close Mixpanel events produce negative TTFV; this is expected and included

---

## Future Enhancements

- Segment TTFV by client size, product type, or vertical
- Track "Time to Second Value" for sustained adoption measurement
- Consider adding `create_stack` as a qualifying event if we can confirm a product was added to the stack (currently excluded because an empty stack creation doesn't indicate value)

---

Last updated: May 11, 2026
