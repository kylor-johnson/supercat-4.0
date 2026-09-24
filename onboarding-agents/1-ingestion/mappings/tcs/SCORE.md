# tcs — the blind-run score

Mapping written from `Source Data/` alone (`BLIND_BOUNDARY.md`), predictions
committed (`PREDICTIONS.md`), answer key **pinned before scoring**
(`CS_eCat_Rebuild/products.csv`, 595,741 bytes, pinned 2026-09-04).

Input class 3 — the first the layer has seen.

---

## Headline

**Denominator: 60 columns** (the build's own column set). Blind, before any
post-unblind fix:

| bucket | n |
|---|---|
| byte-exact | 7 |
| semantically equivalent | 0 |
| differ | 10 |
| not produced | 43 |
| **sum** | **60** |

Cells, over the 17 name-matched columns × 425 shared rows = **7,225**:

| | cells | share |
|---|---|---|
| byte-exact | 4,785 | **66.2%** |
| differ | 2,440 | 33.8% |

**Blind accuracy 66.2%** — the lowest of the four clients, and the reason is
structural rather than sloppy: I emitted 28 columns and the build emits 60, so
43 of its columns had no counterpart in mine at all.

Row set: I produced **1,032**; the build ships **425**. All 425 are inside mine.

---

## 1. RIGHT — the reconciliation, which was the point

The prediction in `BLIND_BOUNDARY.md` was that *the multi-sheet reconciliation is
the work and the column mapping is not*. That held, and the reconciliation is
where the run scored best.

**Which sheet feeds which eCat file** — all six correct:

| sheet | rows | header row | verdict |
|---|---|---|---|
| Master Sheet E+G | 283 | 2 | products.csv ✔ |
| Weiyan LED | 96 | 2 | products.csv ✔ |
| Accessories | 420 | 2 | products.csv ✔ |
| Parts | 234 | 2 | products.csv — **wrong, see §2** |
| Dealers_eCat | 724 | 1 | customers.csv ✔ |
| eCat Navigation | 18 | **9** | contract, not data ✔ |

**Which sheet is authoritative where two disagree: none of them disagree** —
correct, and measured rather than assumed. Master ∩ Weiyan = **0** of 283/96;
Accessories ∩ Parts = **0** of 420/234. Both pairs are complementary partitions.
The build keeps **all 283 master and all 96 weiyan rows**, confirming that
choosing between them — the mali failure — would have dropped a whole line.

**D2, the finding I am most confident was worth the run: union BY NAME, never by
position.** From index 99 the option block is reordered — Master's four finish
columns (`Matte Black`, `Oil Rubbed Bronze`, `Graphite Gray`, `Clear Coat`) sit
at 99–102, Weiyan's at 152–155. A positional union puts Weiyan's `Wall Yoke`
values into Master's `Matte Black` column: a mounting option silently becomes a
finish, on 96 rows, in a file that imports clean.

**D4 — duplicate headers.** Both sheets repeat `Pier Mount` and `Turtle
Friendly`. A dict-based reader keeps the last and drops the first without a word.

**D9 — the 57 option columns are the option stack, not product fields.** Each
header is an option NAME and each cell an option CODE (`WY`, `TS1`, `CHM`) when
available for that SKU. Folder mode reported `options.csv` and
`option_groups.csv` as MISSING from the folder; they are not missing, they are
transposed inside the Master sheet. **Confirmed:** the build emits
`OptionSet1`–`OptionSet8` on products.csv.

Byte-exact columns: `BaseItemCode` `ShipWeight` `Dimensions` `Materials`
`LocationRating` `Certifications` `CountryOfOrigin` — all 425/425. Plus
`Price_MAP` and `Price_MSRP` at **424 of 425**.

---

## 2. WRONG — the source could have told me

**W1 — Parts are not products. 234 rows, and the build ships zero of them.**
It also ships only **46 of 419 accessories**. My D1 unioned all four sheets;
the correct union is Master + Weiyan + a 46-row slice of Accessories. The signal
was in the source and I read past it: `Parts-Table 1.csv` has `Accessory Parent
SKU` = the single value `RG` on all 234 rows, `Accessory Category` = the single
value `PARTS`, and twelve rows annotated *"Price not listed in source PDF"*. A
sheet where every row shares one parent and one category, with prices missing, is
a replacement-parts list, not a catalogue. **607 of my 1,032 rows should not
exist.**

**W2 — `Dealer Net ` has a trailing space in Master, and my reader strips
headers.** So `NetPrice` came back blank on 379 of 425 rows. My own reader
normalised the header and my own mapping declared the un-normalised name. Two
correct decisions that were not made in the same place.

**W3 — `CollectionCodes` is not the brand.** I read the navigation contract as
*Collections = CopperSmith / Biltmore* and shipped `Brand Name`. The build ships
`Turtle Friendly Wall Sconces` — a product family. 0 of 425. The contract's
indentation was ambiguous and I resolved it confidently in one direction without
recording that as an assumption.

**W4 — `ShortDesc`, 0 of 425.** I used the source's `Short Description` column;
the build derives a short label from the product name. Reading a column because
its name matches is the target-blind trap the profiler warns about.

---

## 3. UNKNOWABLE

| # | question | what unblinding showed |
|---|---|---|
| U1 | is `.jpg` the right image extension? | **Neither.** The build ships full S3 URLs. The source's `16WST` is not a filename at all. 12 of 425. |
| U2 | what is a "buildable SKU"? | 283 SKUs over 91 parents; the build resolves it via `OptionSet1-8` |
| U3 | do the option columns become options.csv, OptionSet#, or matrix_options? | **OptionSet# columns.** All three were legal; nothing in the source chooses. |
| U4 | are Parts orderable? | no — excluded entirely (this made W1 knowable in hindsight, not in advance) |
| U5 | `Distributor Net Pricing` carries `#` | the build drops the column |
| U6 | accessory `GTIN` holds `----` and `8.43E+11` | `UPCValue` 304/425 |
| U7 | which price level is rep-facing? | still open |
| U8 | Smart Lists "Ready to Ship (In stock inventory)" | still open — **no inventory file exists in the folder** |

The 43 not-produced columns are mostly this bucket: `Genre`, `Subcategory`,
`GasElectricDual`, `MarineGrade`, `DarkSky`, `Title20/24`, `Prop65`,
`Installation`, `RelatedItems1-3`. Every one exists in the Master sheet as a
column I could see; **which of 157 source columns become registered custom
fields is a client decision, and the class-3 contract file — which is the thing
that should say — covers navigation only.**

---

## What class 3 taught the layer

The template is the contract, and **the contract was the highest-value file in
the folder at 711 bytes.** It gave the category leaves exactly (`Fixture
Sub-Type`'s 9 values are its Outdoor Lighting list) and it named the
buildable/accessory split — *"Accessories (only items that aren't lantern
configurations)"*.

It also has a limit worth writing down: **a navigation contract specifies what
the rep sees, not what the file contains.** It said nothing about the 43 columns
the build emits, nothing about which price level is default, and nothing about
Parts. Class 3's rule — *the template is the contract* — is true and is not
sufficient.

Two tooling defects found and fixed by this run:

1. **`score_blind.py` matched column names case-sensitively.** The build spells
   five headers differently (`materials`, `dimensions`, `shipweight`,
   `Price_MAP`, `Price_MSRP`); all five scored as "not produced" and the run
   read 52.2% when it was 66.2%. Now folded, with casing differences reported.
2. `csv_multi_named` strips header whitespace — correct — but nothing warned
   that a mapping declaring the raw name would silently miss. W2.
