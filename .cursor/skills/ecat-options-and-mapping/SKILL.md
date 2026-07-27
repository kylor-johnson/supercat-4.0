---
name: ecat-options-and-mapping
description: Build the eCat iPad options stack (options.csv, option_groups.csv, OptionSet columns) and configure Admin Console Option Mapping cascades. Use when setting up product options, finishes/fabrics/sizes, configurable products, option swatches, or frame→material→cushion style filtering.
---

# eCat Options & Option Mapping (iPad)

## The four levels

1. **Option Type** — the label (Finish, Fabric, Mount); numbered 1–20 = iPad display
   order; set in Tools → Company Settings → Option Types.
2. **Option Set** — `OptionSet#` columns in products.csv listing which group code(s)
   apply to a product.
3. **Option Group** — a code grouping options of the same type AND same price impact.
4. **Option** — an individual value (code, name, image, optional price).

## Files (import order matters)

Import **`options.csv` → `option_groups.csv` → `products.csv`**, and ALWAYS re-send
option_groups after options (importing options nulls group membership). Each import
fully replaces that file's set. Admin manual entry and file import are mutually
exclusive — pick one.

**options.csv**: `Code`(DB allows 15), `Name`(50), optional `SortValue` (explicit
display order), `Description`, `ImageName` (defaults to `{code}.jpg`), `PriceAddend`,
`PriceFactor`.

**option_groups.csv**: `Code`(15), `Name`(50), `Options` (comma list of option codes
in display order, no length limit), optional `PriceAddend`/`PriceFactor`.

**products.csv**: `OptionSet#` = comma list of group codes (no spaces);
`OptionSet#Required` = `Y`/`N`; `OptionSet#Matrixed` = `Y` to price from
`matrix_options.csv`.

## Pricing rule

If both an option and its group carry a price, the **group wins**. Use `PriceAddend`
(fixed) or `PriceFactor` (e.g. 1.25 = +25%). For combination pricing that varies by
product, use matrix pricing (see `ecat-pricing-levels`).

## Option Mapping (Admin Console only — not importable)

Makes one selection cascade-filter another (e.g. Frame Color → only matching Material
Colors). Must be enabled by SuperCat Support for the org.

**Critical structure**: you cannot cascade from one big group. Use **granular
per-choice groups** — `FRAME_MOCHA` containing only Mocha, mapped to `MAT_NEO_MOCHA`,
etc. — NOT a single `FRAMECOLOR` group.

Setup: Products → Option Mappings → New → Option Type = **OptionSet1** → add one
connection per frame group pointing to the allowed OptionSet2/OptionSet3 groups →
Create Mapping. It filters the universe the product's OptionSet columns already allow;
it does not set price. Top-down only.

## Gotchas

- Client re-uploading an old coarse `option_groups.csv` deletes the granular groups →
  Option Mapping "internal error". Resend the correct group file, recreate the mapping.
- UI trap: adding a new mapping under OptionSet2 instead of adding a connection to the
  existing OptionSet1 mapping.
- Option swatches: square 300×300 `.jpg` in FTP `/option_images` (see `ecat-images-ftp`).
- Codes over 15 chars fail import — shorten (`DGREEN_GLAZED_CER` → `DGREEN_GLAZ_CER`).
