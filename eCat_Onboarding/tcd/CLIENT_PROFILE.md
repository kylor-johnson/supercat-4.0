# Terracotta Designs — eCat Client Profile

> Backfilled from prior Cursor sessions. Verify against latest source before acting.

## Identity
- **Org shortname:** `TCD`
- **Vertical:** furniture / home
- **Status / stage:** live — 346 customers imported (the header below is stale; see the
  blocker section)

## Archetype & applicability
- **Archetype:** standard
- **Product line:** ecat-ipad
- **Flags:** `options: none`
- **File owner mode:** csv
- **Image mode:** ftp
- **Source cutover date:** unknown
- **Sub-brands:** none

- **This profile's own status line is wrong and stays visible as a lesson.** "0 customers
  imported / go-live blocked" was true when written; the org is `active` with **346
  customers** and 7 orders. Counts belong in query results with a timestamp, never in prose.
- **`options: none` despite 222 options and 98 groups live** — the same shape as `leg` at
  larger scale: **zero of 396 products reference any of them**. Cleanup hygiene, not an
  options architecture, and not evidence this client needs one.
- **The `DefaultPriceCode` gate is named after this client.** Every customer row carried
  `DefaultPriceCode = 0`, an ERP placeholder rather than a price level, and 100% of rows were
  rejected. It is the canonical case in `validate_customers.py`'s docstring and it is
  reproducible today — which is exactly why the check ships enabled here.
- **30 orphan inventory rows** are live (inventory 425 rows / 395 matched), so the cross-file
  referential check has real work to do on this org.

## Contacts
- **Client:** Scott; Bill; Angie (invoicing)
- **SuperCat:** Kylor Johnson

## Pricing — price level codes
- `dn` (Dealer Net), `imap` (IMAP), `ns` (Designer Price), `show50` (Showroom 50%).
- `DefaultPriceCode` must equal one of these exactly.

## The blocker (customer import) — RESOLVED
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
