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

| Field | Type | Len | Notes |
|-------|------|-----|-------|
| BaseItemCode | S | 20 | Master key; letters/numbers/`-`/`_` only; must match inventory.csv + stories.csv |
| LongDesc | S | 50 | Primary catalog name; over 50 truncates with a Warning |
| ImageFileName | S | 255 | Comma list, primary first, `.jpg` lowercase, exact filename match |
| Dimensions | S | 50 | Required |
| PackedVolume | F | 8 | Required; `0` if no cube data |
| PackQuantity | I | 5 | Integer > 0; `1` to not enforce case packs |
| MinimumQuantity | I | 5 | Integer > 0; `1` to not enforce MOQ |
| TradeNameCode | S | 5 | One per item |
| CollectionCodes | S | 5* | Comma list (Standard); only first is SmartList-queryable |
| CategoryCodes | S | 5* | Comma list (Standard); only first is SmartList-queryable |
| NewItem | B | 1 | `Y`/blank |
| NetPrice | M | 8 | Base price; no `$` or commas |
| PromotionPrice | M | 8 | KB marks required; blank/`0` = no promo |

Useful optional: `ShortDesc`(15), `MediumDesc`(25), `Materials`(50), `Features`(50),
`Hideable`(B), `RelatedItems`(255, comma list of in-file BaseItemCodes),
`DiscountPriceLevelCode`, `OptionSet#`/`OptionSet#Required`/`OptionSet#Matrixed`,
`UPCValue`, `Keywords` (needs a custom field named `keywords`), `Price_<code>`.
Room shots: `ProductType=suite` + `SuiteGroup=<group code>` (non-orderable).

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
