---
name: ecat-smartlists
description: Build eCat iPad SmartLists — query-based (SQL over product/inventory fields) and hand-picked item lists, with publishing and user-group authorization. Use when creating SmartLists, featured/promo/closeout lists, showroom walk-throughs, or diagnosing a SmartList not appearing on the iPad.
---

# eCat SmartLists (iPad)

A SmartList is a named product selection sent to the iPad, optionally per user group.

## Two kinds

**Query-type** — a SQL `WHERE` fragment over product + inventory DB columns;
self-maintaining as data changes. **Two naming conventions both work**: import-style
header names (`qtyavailable`, `baseitemcode`, `promotionprice`) are translated to DB
columns automatically, and snake_case DB names (`qty_available`, `item_number`,
`promotional_price`) pass through unchanged. Custom fields are queried by their Admin
display name, not `ecat_custom_field_N`. Don't write JOINs — referencing any inventory
qty field automatically targets a view that joins and SUMs inventory per product.

**The multi-code trap:** all values in `CollectionCodes`/`CategoryCodes` are queryable
for a **product-only** query. The moment the query references an inventory qty field, it
switches to the inventory view and only the **first** code per product matches. So
`((qtyavailable + qtyintransit) - qtyonbackorder) > 0 and categorycode = 'DiningChair'`
silently misses products whose `DiningChair` code isn't first.

Common queryable fields: `item_number`, `long_description`, `net_price`,
`promotional_price`, `new_item`, `trade_name_code`, `collection_code`,
`category_code`, `qty_available`, `qty_in_showroom`, `qty_in_transit`,
`qty_on_backorder`. Examples:

```
promotionprice > 0 and qtyavailable = 1
((qtyavailable + qtyintransit) - qtyonbackorder) > 0 and categorycode = 'DiningChair'
baseitemcode in ('123','321','456')
room = '1'    -- custom field for a showroom walk-through
```

**Item-list** — hand-picked SKUs. **Paste them NEWLINE-separated, not
comma-separated.** (The KB says comma; the UI treats a comma list as one giant invalid
item number.) Items must be active products; deleted SKUs are rejected. List order =
iPad display order.

## Publish + authorize (why it's not showing)

iPad visibility = SmartList items ∩ the user's authorized products. To appear, a
SmartList must be: published, authorized to the user's user group, and synced to the
iPad. If a rep can't see it, check: right user group? list published? user not stuck
in DefaultUserGroup? device synced on Wi-Fi?

A query that returns nothing may have gone **dormant**: if a referenced column stops
resolving after save (renamed custom field, dropped column), the SmartList returns zero
items and the system emails an error rather than failing loudly on the iPad. A brand-new
query can't have this problem — bad columns fail validation at save time, as does any
query containing `;`, `/*`, `*/`, or `--`.

## Not a catalog filter

A SmartList curates a subset; it does NOT restrict the full catalog. Restricting what
exists in eCat is the **product file's** job, not a SmartList.
