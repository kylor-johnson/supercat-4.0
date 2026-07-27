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
- [ ] Resolve taxonomy (Standard codes vs Auto-Create labels — see ecat-ground-truth)
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
| ImageFileName | S | 255 | — | Comma list, primary first, `.jpg` lowercase, exact filename match; or full HTTPS URL (fetched by eCat at import) |
| Dimensions | S | 50 | Warn + truncate | Required |
| Materials | S | 50 | Warn + truncate | Optional |
| Features | S | 50 | Warn + truncate | Optional |
| PackedVolume | F | 8 | Validation error | Required; `0` if no cube data |
| PackQuantity | I | 5 | Validation error | Integer > 0; `1` to not enforce case packs |
| MinimumQuantity | I | 5 | Validation error | Integer > 0; `1` to not enforce MOQ |
| TradeNameCode | S | **255** | Validation error | One per item |
| CollectionCodes | S | — | — | Comma list (Standard); only first is SmartList-queryable |
| CategoryCodes | S | — | — | Comma list (Standard); only first is SmartList-queryable |
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

## Common build gotchas

- Required-but-unmappable numeric fields → use `0`/`1` placeholders, not blank.
- Strip secondary header rows and `$`/commas from monetary columns.
- Inventory row whose SKU has no product → orphan; the qty can't be ordered.
- `Materials`/`Features` text won't clear by omission — send empty column to clear.
