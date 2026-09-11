# Phase 2b blind-run boundary — tcs option stack, customers, stories

Declared BEFORE any 2b answer key was opened. Written 2026-09-04.
Same protocol as the Phase 2 runs (`BLIND_BOUNDARY.md`). This file is the
pin: everything below "FORBIDDEN" was unread when it was written.

## Why tcs is the primary client for options

It is the only client in the set with **both** a real option source and a
trusted build to score against.

- `pebl` ships `options.csv` and `option_groups.csv` but its stated source,
  `ecat-options mapping.xlsx`, **is not in the folder** (`IMPORT_README.md`
  names it; `find` returns nothing). A build with no recoverable source cannot
  be reproduced from a mapping, and scoring against it would measure nothing.
  Filed as a finding, not mapped.
- `leg`, `mer`, `libco`, `drf` ship no option files at all.

So the transposed-option problem has exactly one worked example, and the format
has to be designed not to encode it.

## Permitted — `Source Data/` only, same as the Phase 2 run

```
Master Sheet E+G-Table 1.csv          941 KB   283 rows, header row 2, 162 cols
Weiyan LED-Table 1.csv                369 KB    96 rows, header row 2, 162 cols
Accessories-Table 1.csv                58 KB
Parts-Table 1.csv                      18 KB
Dealers_eCat-Table 1.csv              157 KB   724 rows  -> customers.csv
eCat Navigation and Filtering (1).csv 711 B    the class-3 contract
```

Plus programme references that are not tcs answers: `ecatlib/`, `profiler/`,
`mapping/`, the eCat field-limit reference, and the Phase 2 `SCORE.md` for tcs
(which is my own prior output, not the key).

**Carried in from Phase 2 unblinding, and declared as carried** — these are
already-spent facts about tcs, not new key reads:

- Parts are excluded from products.csv; Accessories contribute 46 of 419 rows.
- The build emits `OptionSet1`-`OptionSet8` on products.csv.
- 425 product rows ship.

They bound the *product* side. They say nothing about the contents of
`options.csv` or `option_groups.csv`, which is what this run predicts.

## FORBIDDEN until the mappings are written and on disk

- `CS_eCat_Rebuild/options.csv`
- `CS_eCat_Rebuild/option_groups.csv`
- `CS_eCat_Rebuild/options_audit_fix.csv`, `option_groups_audit_fix.csv`
- `CS_eCat_Rebuild/stories.csv`
- `CS_OptionMapping_Rebuild/` in its entirety — options, option_groups,
  customers, stories, and every script in it
- `CS_eCat_Rebuild/rebuild_perfection.py` and every other script there
- `CLIENT_PROFILE.md`
- the live `tcs` org in Postgres — option, group, customer and story counts

## The prediction, recorded before looking

### 1. The shape question, which is the whole run

72 source columns sit between `Propane Tip` and `Seeded Replacement Glass -
SRG`. Each **header is an option name**; each **cell is an option code** (`WY`,
`GH1`, `BLK`) or blank or the null token `----`.

Three readings are legal and the source does not choose between them
(this is U3 from the Phase 2 run, still open):

  **A. one column = one group.** Group `POST_FITTER` holds PF1..PF5. A product
     with `PF3` in that column then sees all five. Rep-facing wrong.
  **B. one column = one option, groups are semantic clusters** (the four finish
     columns are "Finish"). Needs a cluster declaration the source does not
     carry, and group membership then varies per product.
  **C. per-product groups.** The group is the distinct combination of codes one
     product offers within a type; identical combinations share a group code.
     This is the granular pattern the Admin Console's Option Mapping requires.

**I predict C**, on two grounds available in the source: `OptionSet1-8` is eight
slots, so the types are coarse and the groups are many; and a cell that varies
per row (`PF3` vs `PF2`) can only mean *this product's post fitter is PF3*,
which is a per-product membership statement, not a catalogue-wide one.

**I predict the format has to express A, B and C** rather than pick one, because
the next client's sideways sheet will not be shaped like this one.

### 2. What I expect to get wrong

- **The type partition.** Nothing in the source says which of the 72 columns are
  "Finish" and which are "Mount". I will have to declare it by reading the
  names, and a wrong partition is invisible in a clean import.
- **Group codes.** 15 characters. Any scheme I invent will not be the scheme a
  human invented, so `option_groups.Code` is likely 0% byte-exact even where the
  membership is right. **I will score membership separately from code spelling**
  and say which is which.
- **`----` and the empty columns.** `Weiyan`, `Single 12-V Base`, `Pier Mount`
  (the first of the two) and the three `Replacement Glass` columns are empty in
  Master; Weiyan LED fills six of them with `----` on all 96 rows. `----` is a
  null token, not a code. If I am wrong about that, six options enter the file.

### 3. Union by name, carried forward as a hard rule

Master's finish block sits at 99-102 and Weiyan's at 152-155. Both sheets repeat
`Pier Mount` and `Turtle Friendly`. Any reader here unions **by name with
positional disambiguation of repeats**, never by index, and never through a
plain dict. This is settled, not re-decided.

## Scoring

Per file type, per client. Buckets: byte-exact / semantically equivalent /
wrong / not produced / genuinely unknowable, summing to a named denominator, at
both row and cell granularity, **and every score states its coverage** —
`evaluated N of M candidates`, BUILD_SPEC §3.4.

Answer keys pinned via `bless.py --reference` BEFORE scoring. `score_blind.py`
refuses an unpinned key and refuses an empty key overlap.

The blind score is the number **before** any post-unblind fix.
