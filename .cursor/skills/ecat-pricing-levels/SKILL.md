---
name: ecat-pricing-levels
description: Configure eCat iPad pricing — imported vs arithmetic price levels, Price_<code> columns, DefaultPriceCode, promo/discount levels, user-group price visibility, divisions, and matrix pricing. Use when setting up price levels, mapping price lists, hiding list price, or diagnosing wrong/blank prices on the iPad.
---

# eCat iPad Pricing

Scope: iPad. Ignore the Catalog Pricing KB's "My Account" per-browser markup — that
is eCat Online.

## How a price reaches the iPad

Rep selects a customer → the customer's `DefaultPriceCode` sets the active price
level → the rep's **User Group** controls which levels they may see/select. To hide
list/net price from a group, **do not authorize `net_price`** for that group.

## Two price level types (Admin → Products → Price Levels)

| Type | How it prices | Product file |
|------|---------------|--------------|
| **Imported / Ad-Hoc** | Uses the exact value you supply | one `Price_<code>` column per level; do NOT set a factor |
| **Arithmetic** | `factor` × base (NetPrice or a chosen ad-hoc level), optional rounding | no column — computed |
| **Quantity Break** | maps qty tiers to other levels | `qty_<code>` on product |

- `Price_<code>` columns and the level's Code must match (e.g. code `cad` →
  `Price_cad`). Pre-create the level before importing the column.
- **Always populate `NetPrice`** even when custom levels exist — Net Price display
  mode reads `net_price`; blank shows $0.
- Use ONLY values from source files; never derive prices with markup math unless the
  level is explicitly arithmetic.

## Divisions / dual-brand (e.g. ML vs NSL)

Per-division imported levels: `Price_ml_list`, `Price_ml_dn`, `Price_nsl_list`,
`Price_nsl_dn`. Authorize each User Group to only its division's levels. Empty
columns = blank price even when groups are configured correctly. A "DISCONTINUED"
price list does NOT cover active SKUs — request the current list for live lines.

## Promotions

`DiscountPriceLevelCode` on the product points to a promo price level. The discount
button appears on the iPad order pad only if the code is valid AND the user's group
authorizes that level. One promo per item. Keep promo level names short.

## Matrix pricing

For graded fabrics/finishes where price depends on the product+option combo: set
`OptionSet#Matrixed=Y` and supply `matrix_options.csv` with an `OptionGroup#` per
`OptionSet#` and a row (incl. NetPrice) for every combination. See
`ecat-options-and-mapping`.

## Quick diagnosis

| Symptom | Likely cause |
|---------|--------------|
| Product shows $0 / blank | `Price_<code>` empty, or `net_price` blank in Net mode |
| Rep sees only one level | a customer number on the rep profile overrides rep-level access |
| Promo button missing | invalid `DiscountPriceLevelCode` or group not authorized |
| Wrong price per customer | customer `DefaultPriceCode` mismatch |
