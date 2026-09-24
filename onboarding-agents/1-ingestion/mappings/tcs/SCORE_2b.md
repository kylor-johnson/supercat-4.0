# tcs Phase 2b — the blind-run score

Mappings written from `Source Data/` alone (`BLIND_BOUNDARY_2b.md`), predictions
committed (`PREDICTIONS_2b.md`), answer keys **pinned before scoring**:

```
CS_eCat_Rebuild/options.csv                18,118 bytes   341 rows
CS_eCat_Rebuild/option_groups.csv          42,056 bytes   764 rows
CS_eCat_Rebuild/stories.csv               368,386 bytes   628 rows
CS_OptionMapping_Rebuild/customers.csv    177,742 bytes   721 rows
```

**The blind score is the number before any post-unblind fix.** The v2 mappings
are reported separately and are not the score.

---

## Headline

| file | denominator | blind | after correction |
|---|---|---|---|
| `options.csv` | 341 codes / 7 cols | 330 codes shared, **65.8%** of 990 cells | **96.1%** of 1,312 cells, 328 of 341 codes |
| `option_groups.csv` | 311 member sets | **46.6%** recall, 45.9% precision | **91.0%** / 90.7% |
| **option availability, end to end** | 379 products | — | **0 of 379 exact**; 85.5% recall / 83.2% precision |
| `customers.csv` | 721 rows / 23 cols | 721 of 721 rows, **83.1%** of 13,699 cells, 9 cols byte-exact | **99.96%**, 14 cols byte-exact |
| `stories.csv` | 628 rows / 2 cols | 379 rows shared, **50.0%** of 758 cells | **100.0%**, byte-identical |

Coverage, stated because §3.4 now requires it:

- options: evaluated 4 of 7 reference columns. `ImageName`, `SortValue` and
  `PriceFactor` are **not derivable from this folder** and are excluded by name.
- customers: evaluated 19 of 23 columns over 721 of 721 rows. The 4 unproduced
  are `BillToShortname`, `ShipToCode`, `ShipToName`, `ShipInstructions`.
- stories: evaluated 379 of 628 reference rows. The other 249 are accessories
  and kits whose prose exists nowhere in the folder.
- option_groups: evaluated 311 of 311 reference sets. **Group Code is not
  scored at all** — key overlap is literally zero and `score_blind.py` refuses.
- option availability: evaluated 379 of 425 reference products. The other 46 are
  accessories and kits outside the two lantern sheets.

---

## 1. The option stack, and the thing the blind run got structurally wrong

**RIGHT — the reading.** `per_product` was predicted (P1) and is what the build
does: `CM001 Ceiling Mount 001` holds `HSCM,BMY9,BMCHM,BMSM`, a granular group
for one product's combination. `per_column` would have shown a product carrying
`PF3` all five post fitters.

**RIGHT — eight axes.** Predicted eight from the column names; the build has
exactly eight option types. The count agreeing was luck; the partition was not
the same one.

**RIGHT — `Weiyan` should not be an option** (P4). Shipped deliberately unfixed
under "the cell is the code", producing an option coded `Yes`. The key excludes
it. The fix belonged in the mapping, not in the engine, and that is where it is.

**WRONG, and this is the finding: the option stack has TWO sources.**

338 of the build's 341 options are rows of `Accessories-Table 1.csv`:

| source column | eCat field | agreement |
|---|---|---|
| `Accessory SKU` | `options.Code` | 338 of 341 |
| `Accessory Name` | `options.Name` | 303 of 341 byte-exact |
| `Accessory Dealer Net` | `options.PriceAddend` | 338 of 341 |
| `Accessory Category` | `options.Description` | **the type partition itself** |

`Accessory Category` holds GAS, ELECTRIC, FINISHES, DECORATIVE OPTIONS, WALL
ACCESSORIES, CEILING MOUNT, WALL MOUNT, POST & PIER MOUNT. Eight option types.
I spent a paragraph of the blind mapping deriving that partition by hand, and
the client had already written it down in a column.

**Why I missed it: I had already answered "what is this sheet".** On the
products run, `Accessories-Table 1.csv` was classified as a source of products —
correctly; 46 of its 419 rows ship as products. Having answered that question
once, I never asked it again for a different file type. A sheet can feed two
eCat files, and classifying it for one does not classify it for the other.

**The format lesson, which is not tcs-specific:**

```
the CATALOGUE   what the options ARE      rows    -> options.csv
the MATRIX      who can HAVE which        columns -> option_groups.csv
```

A sideways option block is two sources. Collapsing them forces the mapping to
invent the half it is missing — names, prices, and worst of all the type
partition. **Before declaring a partition, look for the column that already
carries it.**

## 2. customers.csv — 83.1% blind, and three of the four corrections are rules

721 of 721 rows matched on the first try. Three columns carried 96% of the
misses:

**`DefaultPriceCode` is `map`, lower case.** I predicted `MAP` and the substance
was right. Case is not cosmetic in this field: it must match an Admin price
level code *exactly*, and a mismatch rejects every row and loads zero customers.

**`BillToState` is the two-character code**, not `Florida`. Blind I kept the
full name on the class-2/3 principle that editing a client's text is a transform
nobody asked for. That cost 1,440 cells, 62% of all differences in the file. The
principle is right and **it does not survive contact with a field the importer
validates.**

**`BuyerEmail` is ONE address**; 128 of 721 source cells hold several. Shipping
the whole cell imports clean and bounces every order confirmation silently.
`values.split_first` was filed against `ecatlib` rather than taken as an escape
hatch.

**`clean_text` was wrong on names and addresses.** It collapses double spaces,
and seven rows genuinely carry them (`301-A  Brogdon Rd`, `P.O. Box  2088`). On
a class-3 template the whitespace is the client's. `trim` only.

Six cells remain and each has a reason:

| what | why it is not derivable |
|---|---|
| 1 postcode | blank in the source, `30540` in the build. Somebody looked it up. |
| 2 state cells | `Ontario` — the build spells one Canadian province out and abbreviates the others. An inconsistency in the build, reproduced faithfully by neither choice. |
| 2 email cells | the build ships a trailing comma on one and two addresses on another. Both are defects it carries. |

**`TerritoryCodes` was blank on 8 of 724 and the build fills all 8 with `100`.**
That is derivable, not invented: `Territory # = 100` is exactly the `Inside
Sales` agency on all 129 of its rows, and a dealer with no assigned agency is an
inside-sales account. It is `pebl`'s BLOCKING finding at 1.1% instead of 100%,
and eight is the dangerous size — too few to notice, enough to lose eight
dealers from every territory-scoped rep's list.

## 3. stories.csv — the column was right and the composition was missed

`ProductStory` scored **0 of 379** and the source column choice was correct.

The build's story is `Marketing Copy` + a blank line + `Feature 1..6` as a
bullet list with blanks omitted. Blind I emitted `Marketing Copy` alone: 272
characters of an 858-character story — a correct prefix of every single row, and
byte-exact on none.

Corrected, it is **byte-identical on 379 of 379 rows, both columns.**

The narrow lesson: **a prose field on a spec sheet is usually a PART.** Four
prose columns plus six feature columns is a components list, not four rival
candidates. The question to ask a class-3 template is which parts assemble, not
which column wins.

And the distinction the mapping now states in full, because these three collapse
into each other constantly:

```
LongDesc      products.csv   the CATALOGUE NAME the rep browses
ShortDesc     products.csv   the compact ADMIN / ORDER-FORM name
ProductStory  stories.csv    MARKETING COPY — prose, not a name
```

tcs's source makes this worse by shipping a `Short Description` column that is a
98-character sentence. It is not `ShortDesc`. Reading it as one would repeat W4
from the products run — reading a column because its name matched.

## 4. Unknowable

| # | question | what unblinding showed |
|---|---|---|
| U1 | where do option swatch filenames come from? | a hand-built map. Only **31 of 341** are `{code}.jpg`. Blind I emitted the default and would have been wrong on 322. |
| U2 | option `SortValue` and `PriceFactor` | empty in the build; nothing in the source proposes either |
| U3 | 13 option codes in no source file | `BRASS`, `COPPER`, `COY4/5/8`, `CY06/07/18/20`, `GNP7`, `PFA`, `COY12`, `COY13` — added by hand from outside the folder |
| U4 | 249 stories for accessories and kits | no prose columns exist for them in this folder |
| U5 | one invented postcode | not a mapping's job |

**U1 is the one worth carrying.** Emitting `{code}.jpg` was not a harmless
default — it is Legrand's 19 destroyed images in a different file. A value the
generator cannot derive must come from the last known-good file or a
regeneration destroys it. v2 does not emit `ImageName` at all.

## 5. Tooling defects found and fixed by this run

1. **`score_blind.py` had no coverage statement.** It was the sixth instance of
   the §3.4 failure across two codebases — its own case-sensitive column match
   was the fifth. Every section now says `evaluated N of M candidates`, and the
   cell metric names how many rows contributed nothing.
2. **`score_blind.py` could not score `option_groups.csv` at all** and correctly
   refused: key overlap on Code is exactly zero. `--membership` scores set
   equality with code spelling ignored, both recall and precision.
3. **A cell metric cannot see over-production.** `emit = "all"` adds 86
   unorderable options and the cell number does not move, because it only looks
   at shared keys. `acceptance_2b.py` gates precision separately.
4. **TOML scoping, twice.** A bare key written after `[[axis]]` or `[inputs.x]`
   binds to that table. `options_columns` at the bottom of the mapping silently
   became a key of the last axis and `ImageName` vanished from the output with
   no error. The engine now refuses unknown keys in both places.
5. **`null_tokens = []` changes nothing on a catalogue-driven mapping** — the
   catalogue lookup filters `----` before the null check runs. Recorded in
   `acceptance_2b.py` rather than left as a mutation that silently tests
   nothing.
6. **Phase 0's false negative is fixed.** Folder mode now reports
   `options.csv PRESENT, TRANSPOSED inside <sheet>` with the column span and
   specimens, and names the file whose key column carries the codes — which is
   the catalogue this run missed. It fires on tcs and on **0 of 3,400+ files**
   across leg, mer, drf, libco and pebl.

---

# THE RESIDUAL — asked as a closeout, and the answer changed the verdict

`option_groups.csv` hard-deletes every group and reloads. It was the weakest
number in the programme by a wide margin and it was reading as a green row. Two
things came out of characterising it.

## 1. At the membership level: ONE systematic cause, and it was one option code

Of the 100 member sets reproduced wrongly, **94 differed from my nearest set by
exactly one code**, and **68 differed by exactly `LR`**.

```
symmetric-difference size vs my nearest set:  1 -> 94   2 -> 3   10/11/20 -> 1 each
```

**Specimen.** Six consecutive Ceiling Mount groups, each missing only `LR`:

```
REF CM028  ['CHM','CY05','HSCM','LR','PY12','SM']    MINE CM27  [... no LR]  J=0.83
REF CM029  ['CY05','LR','PY12']                       MINE CM28  [... no LR]  J=0.67
REF CM030  ['CHM','CY11','HSCM','LR','PY6','SM']      MINE CM29  [... no LR]  J=0.83
```

The cause is one row of the client's own catalogue:

```
catalogue    LR | Ladder Rests | POST & PIER MOUNT     <- the client's category
matrix       `Ladder Rests`      LR  on 171 rows       <- a CEILING mount
             `Post Ladder Rest`  PLR on 156, LR on 3   <- those 3 are typos
live build   LR -> Ceiling Mount                       <- corrected by hand
```

**The structural point, which is a format gap and not a tcs fact: the
catalogue's type is per CODE, the matrix's type is per COLUMN.** When one code
appears in columns of two different types, the catalogue cannot say so and the
code lands in exactly one axis. `option_type_overrides` now expresses the
correction as declared data with a reason — never inferred, because a mapping
that silently re-filed a client's own categories would be the class-2 failure in
a new costume.

**One catalogue row moved a whole-file metric by 22 points**, because per-product
groups multiply it across every product that offers the code: 171 of 379.

```
membership recall   67.8%  ->  91.0%
precision           67.4%  ->  90.7%
```

Reverting the override is now a gated mutation in `acceptance_2b.py`, and the
floor moved 0.65 -> 0.88. A floor that accommodates a known systematic defect
protects nothing.

## 2. The remaining 9.0% is a genuine long tail, fully decomposed

28 sets, every one a **superset/subset difference inside the correct axis**.
After the `LR` fix there is **no remaining wrong-type placement anywhere.**

| cause | sets | derivable? |
|---|---|---|
| the build offers the FULL family where the matrix names one per product | 21 | no — a hand decision |
| I offer more than the build does | 3 | no |
| the 13 codes with no source file (`COPPER`, `BRASS`, …) | 2 | no — already P2 |
| an unsuffixed base code the build excludes (`WG`) | 1 | no — already filed |
| mixed | 1 | no |

Specimen of the dominant pattern — the build offers all eleven Farm House Hooks
where the matrix names one:

```
REF WA014  ['BS5','BSW5','FH1','FH10','FH11','FH2','FH3','FH4','FH5','FH6',
            'FH7','FH8','FH9','RBS3','TS6','TSW6']
ref-only:  FH1 FH10 FH11 FH2 FH3 FH4 FH5 FH6 FH7 FH8 FH9     mine-only: (none)
```

## 3. And the number that actually gates a client did not exist

**`group_membership` was the wrong metric to gate on.** It counts DISTINCT
member sets. With per-product groups that is a poor proxy for what a rep sees:
the Finish family is **2 of 311 sets** and it applies to **375 of 379 products**.
Membership read 91.0% while the thing a rep experiences had never been measured.

Resolving both sides' `OptionSet` columns through their own `option_groups` — so
invented group codes do not matter — gives:

```
0 of 379 products have identical option availability
7,749 correct offers   1,312 MISSING   1,561 EXTRA
recall 85.5%   precision 83.2%
COVERAGE — evaluated 379 of 425 reference products
```

**Direction matters more than the percentage.** 1,312 MISSING means a rep cannot
pick something the build offers — visible, and a rep complains. **1,561 EXTRA
means a rep CAN pick an option the build does not offer for that product** — a
configuration that may not physically fit, and nothing in the import objects.

Two independent causes, neither derivable from the folder:

| bucket | offers | what it is |
|---|---|---|
| MISSING — no source file for the code | 379 | `COPPER` alone is 375. It is a FINISH, on nearly every product, and one of the 13 hand-added codes (P2) |
| MISSING — in the source, my group omits it | 933 | the "full family" pattern above |
| EXTRA — build emits the code, just not for this product | 1,540 | the build NARROWS what the matrix states. `ADS` 94, `TLA` 85, `WY` 53 |
| EXTRA — unsuffixed base codes | 21 | `WG` etc., already filed |

**The narrowing is not a parent-SKU rollup** — tested and refuted: the build
varies option sets within a parent SKU on 99 of 120 parents, exactly as much as
the matrix does (21 of 120 uniform on both sides). It is consistent with the
build's own `option_groups_audit_fix.csv` and `apply_tuesday_fixes.py`, i.e.
corrections applied outside the folder.

Supplying the 13 missing codes would take per-product exactness only to
**51.2%** (offer recall 89.3%, precision unchanged at 83.2%). The extras are the
real blocker and they are a client question.

## VERDICT — options cannot go to a client on this mapping

`stories.csv` is byte-identical and ready. `customers.csv` is ready with six
named cells. **The option stack is BLOCKED, on two things that are asks rather
than bugs:**

1. **The 13 option codes that exist in no file in the folder** — `BRASS`,
   `COPPER`, `COY4/5/8`, `CY06/07/18/20`, `GNP7`, `PFA`, `COY12`, `COY13`.
   `COPPER` is a finish on 375 of 379 products, and `options.csv` HARD-deletes.
2. **1,561 extra offers** where the matrix says a product can take an option and
   the build says it cannot. Either the matrix is stale or the build's audit
   fixes are the truth; the folder cannot say which.

`acceptance_2b.py` now reports the end-to-end number and states in as many words
that PASS means no regression and not client-ready. That is the specific thing
the earlier summary got wrong: a 91% row on a hard-deleting file type read as
though options could ship.
