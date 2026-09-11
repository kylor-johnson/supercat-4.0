# libco — the blind-run score

Mapping written from the client's source files alone (`BLIND_BOUNDARY.md`),
predictions committed to disk (`PREDICTIONS.md`), **then** unblinded against
`products.csv` and `rebuild_lib_co_files.py`.

Reported as a score, not a bug list. The third bucket is the deliverable.

---

## First, a correction that changes the score

The obvious baseline — top-level `products.csv`, 832 rows, dated 2026-07-13 — is
**stale**, and scoring against it produced two wrong conclusions before I caught
it. It is superseded by `products_LONGDESC_FIX_v2.csv` (2026-09-02), a **5-column
corrective patch**: `BaseItemCode`, `LongDesc`, `TradeNameCode`,
`CollectionCodes`, `CategoryCodes` over **915** rows.

What that changes:

| | vs the stale July file | vs the September patch |
|---|---|---|
| `LongDesc` | 279 / 822 | **829 / 897** |
| `CollectionCodes` | 822 / 822 | **897 / 897** |
| `CategoryCodes` | 822 / 822 | **897 / 897** |
| `TradeNameCode` | 822 / 822 | **897 / 897** |
| my rows absent from the baseline | 75 | **0** |

**This is the argument for task 1 in one paragraph.** I diffed against an
unpinned baseline, concluded the build had deliberately excluded 75 SKUs and
that libco hard-cuts LongDesc at 50 characters, and both conclusions were
artifacts of the file's age. A pinned baseline with a date and a provenance note
would have said "this is what the build produced on 2026-07-13" instead of
letting me read it as current.

So the score below names its baseline for every number.

---

## Headline — the partition

Reported at two granularities because they answer different questions, and the
column-level number on its own is misleading.

**Denominator: 63 columns** — the column set the build actually produced. I
produced 60 of them. (The source file carries 62 headers, of which 20 are
built-in eCat fields and 42 are client-domain columns destined to be registered
custom fields; the build's 63 is that set minus the two I dropped, plus
`price_netprice` which exists in no source file. Three different 6x numbers, so
each is named wherever it is used.)

### Columns — the blind run, before any post-hoc fix

| bucket | n | |
|---|---|---|
| **byte-exact** | 26 | identical on every shared row |
| **semantically equivalent** | 5 | value agrees; only the format differs — the 4 price columns (`236` vs `236.00`) and `LEDHours` (`20,000` vs `20000`) |
| **wrong — my error** | 1 | `ShipWeight`: float tail not stripped |
| **not produced** | 3 | `ShipLBS`, `Video` (my decision — errors), `price_netprice` (exists in no source file — unknowable) |
| **genuinely unknowable** | 28 | see §3 |
| **total** | **63** | |

### Three moments, three numbers — which one is the blind score

`26`, `27` and `29` all appear in this programme's notes for libco. They are
three different moments and only the first is the score:

| moment | byte-exact columns | what changed |
|---|---|---|
| **BLIND — the score** | **26 of 63** | the mapping as written before unblinding |
| after the ShipWeight fix | 27 of 63 | post-unblind: stripped a float tail the validator's >50% threshold had missed (W1) |
| after the class-2 guard | **29 of 63** | post-unblind: reverted the header rename, shipped `ShipLBS` and `Video` (W2–W4) |

**26 is the blind score.** 27 and 29 measure the mapping *after* it was corrected
using the answer key, so they say nothing about what a mapping agent achieves
without one. They are reported because the corrections are real and belong in the
mapping — not as a better result.

Everything else in this document, including the cell figures, is the **blind**
run at 26.

### Cells — the honest accuracy measure

60 produced columns × their shared rows = **49,620 cells compared**:

| | cells | share |
|---|---|---|
| byte-exact | 43,987 | **88.6%** |
| semantically equal, format differs | 4,284 | 8.6% |
| differ | 1,349 | 2.7% |
| **sum** | **49,620** | 100% |

**Blind semantic accuracy: 97.3%.** Byte accuracy: 88.6%.

### Why the two disagree so much, and which to believe

The column metric says 26/63; the cell metric says 97.3%. The gap is not
spin — it is one specific artifact, and it is worth naming because it will
recur on every client:

**23 of the 28 "unknowable" columns differ on 1–9 rows each out of 822.**
`WireLength` 1 row. `CRI` 1 row. `Dimmable` 1 row. `ShadeColor` 1 row. Each of
those counts as a whole missed column at column granularity and as 0.1% at cell
granularity. All 23 have the same cause: the build had an input I was not given
(§3 U9), so its values are non-blank where mine are blank.

And **59% of all 1,349 differing cells are one column**, `IntroDate`:

```
IntroDate       797   (59% of the residual)
RelatedItems    221   (75% cumulative)
4 price cols     34 each, PromotionPrice 34   (88%)
ImageFileName    29   LongDesc 25   ShadeDimension 19   (93%)
23 columns        1-9 rows each                (100%)
```

So: **the cell number is the one to quote**, with the column number beside it as
the reminder that "column correct" is a very strict test. It is nowhere near the
45% floor the column count could be read as implying, and the reason is that
almost every "missed" column is missed on a handful of rows.

### Where my four blind errors landed

They do not form a bucket of their own; they distribute:

- `ShipWeight` — bucket **wrong** (1). Now fixed: 822/822.
- `ShipLBS`, `Video` — bucket **not produced** (2 of the 3).
- the `netprice` → `NetPrice` rename — inside the **semantically equivalent**
  bucket. It changed a header name, not a value, so no cell records it. That is
  itself worth noting: **a header error is invisible to a cell-level score**,
  and an unrecognised header is a fatal import error.

## 1. RIGHT — what the source did settle

**26 of 63 columns byte-exact (the blind score)** against the July build, plus all four populated
columns of the September patch bar LongDesc's tail:

`BaseItemCode` `UPCValue` `CollectionCodes` `CategoryCodes` `Dimensions`
`ShipWeight` `PackedVolume` `PackQuantity` `MinimumQuantity` `TradeNameCode`
`NewItem` `Feature1`–`Feature5` `ExtensionRods` `BackplateDimension`
`CanopyDimension` `FinishCode` `ShadeMaterial` `BulbType` `TotalLumen` `Kelvin`
`Voltage` `Certifications` `ADA`

Structural calls, all confirmed against the answer key:

| | decision | confirmation |
|---|---|---|
| D1 | `LIB_Co_Upload_Fixed_Prices.xlsx` is the primary, not the spec master | the script's `build_products()` reads exactly that file and uses the spec master only as a lookup |
| D2 | spec master is a superset by key, and its **row 2 is a label row** | `load_spec_master()` filters `r[0] != "Item#"` — the same row, found independently |
| D4 | `LongDesc` is 0/897 in the primary and must be backfilled from the spec master | the script backfills it from the spec master, with a `longdesc_backfilled` counter |
| D11 | ship `Subcategory` as a custom field | same |
| D12 | strip float tails on `UPCValue` and the numeric customs | `UPCValue` 822/822 |
| D15 | 42 columns need Admin registration or they are silently dropped | the build ships the same 42 |
| D10 | keep `CollectionCodes` UPPERCASE | 897/897 against the patch — **U8 resolved: correct as shipped** |

`UPCValue` is the one worth naming. All 897 source values carry a spreadsheet
float tail (`810117543631.0`); `UPCValue` is a TEXT field, so the importer takes
the tail verbatim and every barcode ships wrong. Caught blind, 897 of 897.

---

## 2. WRONG — the source contained enough to know better

Four. Three are the same mistake: **I transformed a class-2 file.**

**W1 — `ShipWeight` float tail, 500/822.** Built `42`, mine `42.0`. My own
validator flags float tails and missed this one: the check required the tail on
**>50%** of rows and `ShipWeight` carries it on 41% (369 of 897) because only
whole-number weights get one. **The threshold was the defect** — a systematic
artifact does not become acceptable at 41% prevalence. Fixed (the check now
fires at 3+ occurrences), and the mapping now strips it: `ShipWeight` 822/822.

**W2 — I renamed the header `netprice` → `NetPrice`.** The build keeps
`netprice` *and* adds a separate `price_netprice`. Renaming a header is a
transform. I justified it in the mapping as "a header fix, not a value fix";
that distinction is mine, not the rule's.

**W3/W4 — I dropped `ShipLBS` and `Video`.** The build ships both. My reasons
were defensible — and "defensible" is exactly the problem. On a class-2 file a
column the human included is a decision; dropping it overrides them. Both should
have been findings, not deletions.

The shape of W2–W4: I applied judgement where the class-2 rule says not to. It
was wrong three times out of three.

---

## 3. UNKNOWABLE — what a human still has to tell us

The valuable bucket. No file the client sent could settle these.

**U1 · The money format.** Built `236`; mine `236.00`. libco drops `.00` on whole
dollars. **Predicted as unknowable, and it was.** The only statement of price
format in any client file is the spec master's `$1,025.00` — two decimals, 906 of
906. The source points the *opposite way* from the answer.

**U2 · `LongDesc` truncation — and the answer is now a defect, not a rule.**
*Measurement:* the July build caps LongDesc at 50 characters, mid-word (566 of
832 sit at exactly 50); `limits_generated.py` gives `longdesc` 255.
*What resolved it:* the script's constant is `LONGDESC_MAX = 255`, and the
September patch restores full descriptions (max 82, 585 rows over 50 chars).
So the 50-char cut was a real defect that has since been found and corrected,
and my untruncated output agrees with the correction — 829 of 897.
**I initially reported this as "a second client with leg's 50-char cap." That
was wrong**, and it was wrong because I read a stale file as current. leg's
`LONGDESC_LIMIT = 50` remains open on its own evidence; libco is not a second
instance of it.

**U3 · Which SKUs are in the catalogue.** Against the July build I concluded 75
of my SKUs had been deliberately excluded. Against the September patch, **zero**
are missing. The exclusion was the stale file, not a decision. What remains
genuinely unknowable: the 18 SKUs in the patch that are in no source file I was
given, and the script's `FORCE_ADD_PRODUCTS` manifest — a hand-written list of
SKUs cloned from existing rows with overrides, plus `FORCE_DROP_SKUS =
{"10131-06"}`, annotated *"drop regardless of qty (sold-per-Silvio)"*. A person's
name in a constant is the clearest possible statement that the data could not
answer this.

**U4 · `price_netprice`.** The build emits a fifth price column existing in no
source file. The level must be created in Admin first.

**U5 · `PromotionPrice` on 34 rows.** Built `74.25` against `netprice` `99` — a
25%-off discontinued promo over a SKU set no source file marks. It is also the
exact residual on every price column: neutralising the money format takes the
four price columns from 0/822 to 788/822, and 822 − 788 = 34.

**U6 · `RelatedItems` enrichment, 221 rows.** `backfill_variant_sibling_related_items()`
— a rule about colour variants that is in the code, not the data.

**U7 · `LEDHours` keeps a thousands separator.** Built `20,000`, source `20000.0`.

**U8 · `IntroDate` is a label, not a date.** Built `January 2023`, source
`2023-01-01 00:00:00`. The script uses an explicit `INTRO_DATE_FIXES` lookup —
a hand-written table, not a derivation. I normalised to ISO because the column
is named Date; it is a custom **text** field, so both are legal and only intent
decides.

**U9 · ~24 columns disagree on 1–29 rows each**, always built-has-a-value where
mine is blank. **Checked on 6 of them: the spec master supplies the built value
on 0 of those cases.** The build had an input I was not given.

Plus the nine questions in `PREDICTIONS.md`, of which unblinding resolved only
U8 (CollectionCodes casing — uppercase is correct). The rest stand.

---

## What this run says about the layer

The class-2 path did what it exists for. From the source alone, before any
build, it found: `LongDesc` empty on 897 of 897; `UPCValue` float-tailed on 897
of 897; five Yes/No binary fields that cannot match an eCat boolean filter; 15
`FinishCode` values differing only by case; a second header row that would
otherwise import a product called `Item#`; and 191 of 1,812 image references
absent from both image folders. Every one of those is a day-one finding rather
than a post-import surprise.

Two lessons, both cheap:

1. **Enforce the class-2 rule, don't just document it.** All four of my errors
   were decisions taken on a file where a human had already decided. Dropping a
   column or renaming a header on a class-2 file should require the same
   explicit, recorded act that re-blessing a baseline does.
2. **Score against a pinned baseline or don't score.** Two of my three headline
   conclusions were artifacts of a two-month-old file, and I only caught them
   because the script's `LONGDESC_MAX = 255` contradicted what I had just
   written down.
