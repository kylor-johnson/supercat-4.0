---
name: ecat-go-live
description: Take an eCat iPad org from data-loaded to rep-ready — users, user groups, rep invitations, territory alignment, order email, PDF report formats, and the go-live checklist. Use when setting up reps/users, user groups, bulk invitations, territories, or assessing go-live readiness.
---

# eCat iPad Go-Live

Catalog + pricing loaded is not "live." Reps need accounts, groups, territories, and
an order path.

## Sequence

1. **customers.csv imported clean** — no reps-to-customers without it (see
   `ecat-customers-build`).
2. **User Groups** — Users → User Groups → New. Set price-level visibility (see
   `ecat-pricing-levels`), PDF formats, and "show all customers" vs "show only
   associated customers."
3. **Invite reps** — Users → Invitations → Invite Users → Import from File.
4. **Territory alignment** — customer `TerritoryCodes` must match the rep's
   Rep/Territory Numbers when the group is "show only associated customers."
5. **Order email** — set the order email recipient so submitted orders are delivered.
6. **PDF report formats** — configure at least ~3 usable formats on the user group.
7. **iPad test** — presentations, pricing per customer, related items, options,
   smartlists. Then go live.

## Rep invitation CSV

Columns: `email, username, first_name, last_name, user_type, territory_codes,
customer_number`.
- Only `email` is required.
- `user_type` must **exactly match a User Group name** (e.g. `Sales Rep`).
- `territory_codes` comma-separated, no spaces (e.g. `1,2`).
- Leave `customer_number` blank for reps — a customer number on a profile overrides
  rep-level price access (the rep gets treated like that customer).

## Order email subject

Set at **Admin Console → Company Settings → Email Templates → "Order email subject."**
Accepts tokens like `%OrderNumber%` — token matching is **case-insensitive** and
**dashes/underscores are stripped before matching** (`%order_number%`, `%Order-Number%`,
and `%OrderNumber%` all resolve the same). A **user group can override** the subject:
a group-level override **shadows the org-level setting** for reps in that group, so if
one rep's order emails look different, check the group override before the company setting.

## Go-live checklist

```
- [ ] customers.csv imported error-free (DefaultPriceCode valid on every row)
- [ ] inventory refreshed (not months stale)
- [ ] User Groups created (not everyone in DefaultUserGroup)
- [ ] Price-level visibility set per group
- [ ] Reps invited; territory codes aligned to customers
- [ ] Order email recipient set
- [ ] >= 3 PDF report formats
- [ ] Subscription/plan provisioned (internal)
- [ ] iPad acceptance test passed
- [ ] Training call scheduled
```

## Common go-live blockers

- Every real user still in `DefaultUserGroup` → permissions/territory filters never apply.
- DC user-group restriction controls order ship-from, not catalog inventory counts —
  test at order creation, not catalog view.
- A user group with no member synced since the last import shows a stale catalog.
