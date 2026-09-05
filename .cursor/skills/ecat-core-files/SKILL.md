---
name: ecat-core-files
description: Reference for the eCat iPad import files (products, stories, inventory) — required fields, lengths, validation, and the build workflow. Use when building, mapping, or troubleshooting products.csv / stories.csv / inventory.csv, or translating a client export into eCat format.
---

# eCat Core Files Reference (iPad)

Always-on rules `ecat-ground-truth` and `ecat-import-ops` cover delete-semantics,
import order, FTP folders, and error tiers — don't repeat them; apply them.
Customers, pricing, options, images, and smartlists have their own skills.

## Build workflow

```
- [ ] Read the client source export; identify the BaseItemCode column (master key)
- [ ] Map to required fields (tables below); fill placeholders for required-but-missing
- [ ] Resolve taxonomy (Standard codes vs Auto-Create labels — see ecat-ground-truth).
      Scan the distinct CollectionCodes/CategoryCodes/TradeNameCode values for
      near-duplicates (singular/plural, typos, casing — e.g. "Outlet" vs "Outlets",
      "Night Light" vs "Night Lighs"). Groups never auto-merge, so a typo becomes two
      permanent iPad labels. Flag suspected duplicates to the client instead of guessing.
- [ ] Validate: 0 dup BaseItemCode, 0 blank required, lengths OK, no line breaks
- [ ] Write to 00_Import_Files/Ready_For_Import/ and a *-review.md flagging assumptions
- [ ] Import in order; verify File Import Status is error-free
```

Never invent values you can't source (image names, ERP SKUs, color families) — flag
them for the client instead.

## products.csv — required fields

> **Field lengths below are sourced from `Product::ATTR_LENGTHS` in
> `supercat_server/app/models/product.rb`. Do not transcribe from other docs —
> the earlier documented values (LongDesc 50, ShortDesc 15, TradeNameCode 5,
> BaseItemCode 20) were all wrong and caused real data loss.**
>
> Two tiers: `ATTRS_TO_TRUNCATE` fields warn and truncate; everything else raises
> a validation error. Truncation columns: `LongDesc`, `ShortDesc`, `MediumDesc`,
> `Materials`, `Features`, `Dimensions`.

| Field | Type | Len | Behavior over limit | Notes |
|-------|------|-----|---------------------|-------|
| BaseItemCode | S | **40** | **Validation error** | Master key; letters/numbers/`-`/`_` only; must match inventory.csv + stories.csv |
| LongDesc | S | 255 | Warn + truncate | Primary catalog name |
| ShortDesc | S | 255 | Warn + truncate | Compact name for admin/order forms; falls back to LongDesc if blank |
| MediumDesc | S | 255 | Warn + truncate | plist description |
| ImageFileName | S | — | Warn + skip | No length cap. Filename must match `\A[^/()]*\z` (no slashes or parentheses) or the image is skipped with a warning; over the 6/12 cap, extras are dropped with a warning. Comma list, primary first, `.jpg` lowercase, exact filename match; or full HTTPS URL (fetched by eCat at import) |
| Dimensions | S | 50 | Warn + truncate | Required |
| Materials | S | 50 | Warn + truncate | Optional |
| Features | S | 50 | Warn + truncate | Optional |
| PackedVolume | F | — | — | Required; float column, no length limit; `0` if no cube data |
| PackQuantity | I | — | **Warn + coerced to 1** | Integer; `≤0` imports as `1` with a warning, it does not reject the row |
| MinimumQuantity | I | — | **Warn + coerced to 1** | Integer; `≤0` imports as `1` with a warning, it does not reject the row |
| TradeNameCode | S | **255** | Validation error | One per item |
| CollectionCodes | S | — | — | Comma list (Standard); all codes are SmartList-queryable unless the query also references an inventory qty field, in which case only the first matches |
| CategoryCodes | S | — | — | Comma list (Standard); all codes are SmartList-queryable unless the query also references an inventory qty field, in which case only the first matches |
| NewItem | B | 1 | — | `Y`/blank |
| NetPrice | M | 8 | — | Base price; no `$` or commas |
| PromotionPrice | M | 8 | — | KB marks required; blank/`0` = no promo |

Useful optional: `Hideable`(B), `RelatedItems`(255, comma list of in-file BaseItemCodes),
`DiscountPriceLevelCode`, `OptionSet#`/`OptionSet#Required`/`OptionSet#Matrixed`,
`UPCValue`, `Keywords` (needs a custom field named `keywords`), `Price_<code>`.
Room shots: `ProductType=suite` + `SuiteGroup=<group code>` (non-orderable).

**Image delivery modes:** (1) FTP `.jpg` files to `/images` (flat root, no subfolders);
(2) full HTTPS URL in `ImageFileName` — eCat fetches bytes at import time. CDN mode
caches at import (not live-rendered); replace stale images with a versioned filename
(`-v2`). PNG URLs fail silently — `CdnImageSync` requires `.jpg`/`.jpeg` extension and
`image/jpeg` content-type. Default **6 images** per product; 12 only with paid
`enable_twelve_product_images` flag.

## stories.csv

Columns: `BaseItemCode`, `ProductStory`. ProductStory is romance copy shown in
Details / tear sheets / PDF / email — NOT the product name. Omitting a product sets
its `story=null` (does not delete the product).

## inventory.csv

Required: `BaseItemCode` (must match products.csv). Quantities: `QtyAvailable`,
`QtyOnHand`, `QtyReserved`, `QtyInTransit`, `QtyOnBackorder`, `QtyOnPOrder`,
`QtyOverseas`, `QtyInShowroom` (all integers). `NextReceiptDate` = real date
(`M/D/YYYY` or `YYYY-MM-DD`), blank if unknown — prose like "Discontinued" fails.
`NextReceiptQty` integer. `Option1..20` only if the SKU uses options. `DistributionCenter`
column = **do not use**. Custom inventory fields must be pre-registered in Admin.

**Multi-division (multi-brand / multi-warehouse) orgs** use **per-division quantity
columns**, one set per division: `ML_QtyOnHand`, `ML_QtyAvailable`, `NSL_QtyOnHand`,
`NSL_QtyAvailable`, … (division prefix + qty field). Put `0` — not blank — where a
division has no stock for that SKU. This mirrors the `Price_ml_list` / `Price_nsl_list`
per-division pricing pattern in `ecat-pricing-levels`; the division prefixes should match
across the inventory and pricing files.

## Common build gotchas

- Required-but-unmappable numeric fields → use `0`/`1` placeholders, not blank.
- A **decimal in an Integer-type qty field** (e.g. `2.5` in `QtyOnHand`) is a **HARD
  validation error** — the row is rejected, not truncated-and-warned. Round/clean qty
  columns to whole integers before import.
- Required-but-missing TEXT fields (e.g. `Dimensions`) have no safe placeholder —
  don't invent one. Count the blanks and put the number in the review as a blocker.
- Strip secondary header rows and `$`/commas from monetary columns.
- Inventory row whose SKU has no product → orphan; the qty can't be ordered.
- `inventory.csv` / `stories.csv` / `matrix_options.csv` / `contract_prices.csv` rows
  **silently warn-and-skip** when the `BaseItemCode` isn't an **active product** — this
  is the root cause of "products imported clean but inventory has warnings." Load
  `products.csv` first and confirm it's error-free before chasing inventory warnings.
- `Materials`/`Features` text won't clear by omission — send empty column to clear.
- **Import file HEADERS must match the expected column names exactly.** A client header
  like `Item Number` instead of the expected `BaseItemCode` triggers a **fatal
  unrecognized-column error** (whole file rejected) — rename headers to the eCat field
  names before import; don't rely on the importer to infer them.
