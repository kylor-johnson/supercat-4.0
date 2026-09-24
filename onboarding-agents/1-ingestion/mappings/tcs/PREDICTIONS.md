# tcs — what I decided blind, and what I could not

Committed BEFORE opening `rebuild_perfection.py` or anything in
`CS_eCat_Rebuild/`.

## The six-sheet reconciliation — the answer I am committing to

| sheet | rows | header row | → eCat file |
|---|---|---|---|
| Master Sheet E+G | 283 | **2** | products.csv (+ options) |
| Weiyan LED | 96 | **2** | products.csv (+ options) |
| Accessories | 420 | **2** | products.csv |
| Parts | 234 | **2** | products.csv |
| Dealers_eCat | 724 | 1 | customers.csv |
| eCat Navigation and Filtering | 18 | **9** | **contract, not data** |

**Which sheet is authoritative where two disagree: none of them disagree.**
Measured both pairs — Master∩Weiyan = **0 of 283/96**, Accessories∩Parts =
**0 of 420/234**. Zero overlap in both. These are complementary partitions, not
rival versions. Union all four; choosing any one drops a whole product line.
Total **1,033** products.

## Decisions

| # | decision | evidence |
|---|---|---|
| D1 | union the four catalogue sheets, 1,033 rows | 0 key overlap in both pairs |
| D2 | **union BY NAME, never by position** | from index 99 the option block is REORDERED: Master's 4 finish columns sit at 99–102, Weiyan's at 152–155. A positional union puts Weiyan's `Wall Yoke` into Master's `Matte Black`. |
| D3 | **8 alias pairs** between Master and Weiyan | `UPC`/`UPC/GTIN`, `Voltage`/`Total Voltage`, `MSRP`, `Fixture Style`, and three that differ **only by a double space** |
| D4 | duplicate headers disambiguated positionally | both sheets repeat `Pier Mount` and `Turtle Friendly`; a dict reader silently keeps the last and drops a populated column |
| D5 | `CollectionCodes` = Brand Name | the navigation file: "Collections >>>>> CopperSmith / CS \| Biltmore" |
| D6 | `CategoryCodes` = `Fixture Sub-Type` for lanterns | its 9 values ARE the navigation file's Outdoor Lighting leaves |
| D7 | money dialect = **tcs** (passthrough) | prices are bare integers (`1017`, `1004`); no currency decoration anywhere |
| D8 | `ImageFileName` needs `.jpg` appended | source holds `16WST` with no extension on all 283 rows |
| D9 | the 57 option columns are **options.csv / option_groups.csv**, not product fields | each header is an option NAME and each cell an option CODE (`WY`, `TS1`, `CHM`) when available for that SKU |

## Unknowable from the source

| # | question |
|---|---|
| U1 | **Is `.jpg` the right extension?** Nothing states it; the accessory sheets use S3 URLs instead. |
| U2 | **What is a "buildable SKU"?** 283 SKUs across 91 `Parent SKU` values. Whether eCat should model these as products, matrix options, or option sets is a product decision. |
| U3 | **Do the 57 option columns become `options.csv`, `OptionSet#` columns, or `matrix_options.csv`?** All three are legal; they behave very differently and `matrix_options.csv` hard-deletes. |
| U4 | **Are Parts orderable?** 234 rows, one `Parent SKU` (`RG`), 12 with "Price not listed in source PDF". |
| U5 | **`Distributor Net Pricing` carries the literal `#`** on some rows. Null token or a real annotation? |
| U6 | **Accessory `GTIN` holds `----` and `8.43E+11`** — a null token and scientific notation in a text field. |
| U7 | **Which of the 4 price levels is the rep-facing default?** |
| U8 | **Smart Lists.** The contract asks for "New Arrivals" and "Ready to Ship (In stock inventory)" — neither derivable without an inventory feed, and no inventory file exists in the folder. |

## Predicted score

I expect D1–D4 to be right — the data forced them. I expect to be wrong about
the exact output column set, because a class-3 template says what the navigation
must look like and says nothing about which eCat columns the build chose to emit.
