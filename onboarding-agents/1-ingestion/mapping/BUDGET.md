# The escape-hatch budget, re-derived

**2026-09-04.** The budget of 3 was derived from BUILD_SPEC §2's list of
"genuinely client-specific" functions. That list is wrong in a way that matters:
it mixes together three different kinds of thing, and only one of them is what
the budget counts.

This re-derives the number from what three builds actually needed, now that the
parameterised readers and the current `ecatlib` exist.

---

## The old basis

> Legrand 2 (`load_us_radiant_prices`, `load_ca_adorne_prices`), libco 2
> (`load_spec_master`, `apply_discontinued_promo`), tcs 3
> (`stage2_lantern_rebuild`, `stage4_parts_and_kits`, `sku_ignition`).
> Three is the observed ceiling, not a guess.

Seven functions. The budget counts **per-field transforms**. Only two of the
seven are per-field transforms.

## What the seven actually are

| function | client | what it really is | still code? |
|---|---|---|---|
| `load_us_radiant_prices` | leg | xlsx, data from row 2, price columns at indices 4/5/6 | **no** — parameters |
| `load_ca_adorne_prices` | leg | xlsx, data from row 8, indices 5/6/7 (msrp and imap swapped vs radiant) | **no** — parameters |
| `load_spec_master` | libco | csv, second row is a label row, columns by index | **no** — parameters (`skip_rows_after_header`) |
| `stage2_lantern_rebuild` | tcs | decides which rows take Master vs Weiyan fields, across two files | **loader** — row/file assembly |
| `stage4_parts_and_kits` | tcs | removes Parts rows and corrupt SKUs, adds part rows | **loader** — decides which rows exist |
| `apply_discontinued_promo` | libco | writes `PromotionPrice` from a discontinued SKU set | **transform** — one field's value |
| `sku_ignition` | tcs | derives a value from the SKU's last character | **transform** — one field's value |

Three of the seven are readers that are now declarative — **demonstrated, not
argued**: leg's four price books and libco's spec master are all declared as
parameters in their mappings, and leg reproduces byte-identical with **zero**
bespoke loaders. Two are row-selection loaders, which the rule already says are
named-but-not-budgeted. Two are per-field transforms.

So §2's list supports a ceiling of **2**, not 3, on its own terms — and it omits
transforms that the builds genuinely needed but §2 never listed.

## The measured basis

Per-field transforms actually required, after parameterised readers, lookup
tables held as data, and the current `ecatlib`:

| client | per-field transforms | how known |
|---|---|---|
| **leg** | **1** — `packed_volume_cuft` | measured; the mapping reproduces `products.csv` and `inventory.csv` byte-identical |
| **mer** | **3** — `image_filename_from_code`, `sample_counterpart`, `design_family_key` | measured; reproduces byte-identical |
| **libco** | **1** — `apply_discontinued_promo` | read from the answer key after the blind run |
| **tcs** | **2** — `sku_ignition`, `fix_sku_code` | read from the script; tcs has not been mapped |

Ceiling: **3**, at mer.

## The number stays at 3. The basis changes, and so do two rules.

The old number was right by coincidence — derived from a list that conflated
loaders with transforms, and landing on 3 anyway. It now rests on four measured
counts instead of one miscounted list.

Two things change with it:

**1. Bespoke loaders get a budget too, and it is 0.**
The old rule said loaders are "named, not budgeted", which in practice meant
unbounded. Three of the four clients examined need **zero** — every reader they
required is expressible as parameters. tcs needs two, and both are genuine
row-selection. So: **a bespoke loader is now an exception that must be justified
in the mapping, not a free category.** An unbudgeted category becomes the sixty
scripts renamed, which is exactly what §2's own framing warns about.

**2. Hand-written manifests are DATA, not code, and not hatches.**
libco's `FORCE_ADD_PRODUCTS` (SKUs cloned from a template row with overrides)
and `FORCE_DROP_SKUS = {"10131-06"}` — annotated *"drop regardless of qty
(sold-per-Silvio)"* — are neither transforms nor loaders. They are a person's
decisions written into a Python file. They belong in the mapping as a table,
where they are reviewable, and they should count against **nothing**. A
constant containing a colleague's name is the clearest possible signal that the
data could not answer the question.

**Caveat on mer's 3, stated because it is the number that sets the ceiling.**
mer hit 3 partly because the format lacked expressive power at the time: a
lowercase-and-suffix filename template, a SKU-suffix toggle, and a
regex-normalised grouping key. If any of those became a primitive or an
operator, mer drops to 0–1 and the observed ceiling falls to 2. **3 is an upper
bound on today's format, not a property of the clients.** Re-derive it again
after the next client.

## What the budget is for

Not to ration effort. It is a **detector**: a client that needs a fourth
per-field transform is telling you the library is missing a primitive. That has
now happened four times and the library gained four primitives —
`parse_int`, `round_decimals`, `strip_float_tail`, and the ISO-datetime branch
of `normalize_date` — each found by a mapping that could not express something,
each added once, each free to every client after.
