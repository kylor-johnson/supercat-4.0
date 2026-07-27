# Terracotta Designs — eCat Client Profile

> Backfilled from prior Cursor sessions. Verify against latest source before acting.

## Identity
- **Org shortname:** `TCD`
- **Vertical:** furniture / home
- **Status / stage:** go-live blocked (customer import failed)

## Contacts
- **Client:** Scott; Bill; Angie (invoicing)
- **SuperCat:** Kylor Johnson

## Pricing — price level codes
- `dn` (Dealer Net), `imap` (IMAP), `ns` (Designer Price), `show50` (Showroom 50%).
- `DefaultPriceCode` must equal one of these exactly.

## The blocker (customer import)
- Customer upload failed: every row had **`DefaultPriceCode = 0`** →
  `Default price code '0' must be a valid price level code`. 0 customers imported.
- Fix: set each row's `DefaultPriceCode` to a valid code; remove `ShipToFax` (unknown
  field warning); `BuyerEmail`/`BuyerPhone` are bill-to contact; `BillToEmail`/
  `BillToPhone` are custom fields, not standard.

## Go-live gaps
- Inventory stale (last updated Dec 2025).
- Everyone in `DefaultUserGroup`; only 3 iPad logins, 5/7 users admin.
- Need: user groups, bulk rep invitations (Users → Invitations → Import from File),
  territory alignment, order email recipient, ≥3 PDF report formats, subscription.

## Sequence to live
1. Fix `DefaultPriceCode` → re-upload customers.csv (clean)
2. Create User Groups (min. "Sales Rep")
3. Invite reps (`user_type` = group name; `territory_codes` like `1,2` no spaces)
4. Refresh inventory; set order email; configure report formats; training call

## Open items
- [ ] Corrected customers.csv imported error-free
- [ ] Showroom accounts: confirm `show50` vs `dn` default
