# ecatlib — Phase 1 result

**Status: acceptance test PASSES, byte-identical.** 2026-09-04.

```
primitives delegated to ecatlib: 17
ACCEPTANCE: PASS - byte-identical (404798 bytes)
```

Legrand's `products.csv` — 1,020 rows, live in production, produced by a
1,537-line script — rebuilt with the twelve primitives replaced by `ecatlib`
calls. `inventory.csv` is byte-identical too.

Reproduce:

```bash
python3 ecatlib/acceptance_legrand.py \
  "<...>/02_Implementation/Legrand" /tmp/accept \
  "<...>/02_Implementation/Legrand/Build/products.csv"
```

## Three things that had to be established first

**1. The baseline is reproducible.** Before extracting anything, the unmodified
`build_ecat_files.py` was run against current source: byte-identical to the
committed `products.csv`. Without that, a library diff would be measuring source
drift rather than the library, and any difference would be unattributable.

**2. The test is not vacuous.** Mutating one library function — `parse_money`
from 2dp to 3dp, a single character — fails the test (410,875 bytes vs 404,798).
A green test that cannot go red proves nothing.

**3. `stories.csv` is not a valid target.** The committed `stories.csv` differs
from the generator's raw output, and **the unpatched original script differs from
it too** — so this is pre-existing, not caused by the library. Cause:
`fix_stories_encoding.py` post-processes it to repair mojibake (1,792 `Â®`, 126
`â€"`, …) and rewrites it with LF endings. The committed artifact is a repaired
file, not generator output. Acceptance is `products.csv` + `inventory.csv`.

## The finding that shaped the design

BUILD_SPEC §2 reads as though extraction were mechanical — twelve primitives,
three reimplementations, merge them. **It is not.** The three builds disagree on
*output*, not just style:

| primitive | Legrand | libco | tcs |
|---|---|---|---|
| money | `"4058.00"` always 2dp | `"4058"` integer dollars drop `.00` | passthrough after stripping `$` `,` |
| boolean | `"Y"` / `""` | `"Yes"` / `"No"` | — |
| weight | unit-aware, `"500 g"` → `1.102311` | first number, `"500 g"` → `"500"` | — |
| dimensions | `3.5 in H x 2 in W x 1 in L`, `N/A` when empty | — | `18.75"H x 10.5"W`, `""` when empty |

Merging those into one function silently rewrites three clients' files. So every
divergent primitive takes an explicit **`dialect`**, chosen per client in config
and never guessed. `values.LEGRAND` is byte-exact with `build_ecat_files.py`,
which is what makes the acceptance test possible at all.

The same applies at finer grain: Legrand's `clean_category` does *not* null-map
(a literal `"0"` category stays `"0"`) while `normalize_finish` does. Same
primitive, different null policy — hence `clean_lookup(..., null_tokens=...)`.

## Two suspicions, resolved differently — and the difference is the point

Both were preserved so their builds reproduce, and **flagged rather than silently
"fixed"**. Verified against live 2026-09-04, and they did not land the same way:

**libco's boolean — CONFIRMED live defect.** `to_boolean(dialect=LIBCO)` returns
`Yes`/`No`, but eCat boolean filters match only `Y`/`y`/`T`/`t`/digits 1–9. Three
registered binary filter fields carry Yes/No values: **`Dimmable` 880,
`SlopeCeilingCompatible` 786, `MotionSensor` 162 — 1,828 values across three
filter chips that cannot match.** Same shape as leg's 13 registered-but-empty
filter fields (BUILD_SPEC B1). A fourth, `Rating`, is registered binary with 907
values that are neither Yes nor No: a different problem in the same family.

**libco's weight — code hazard, NOT a live defect.** Ignoring units would be 453×
wrong on a gram value, and the code genuinely permits it. **The data does not
show it:** 915 products, min 1.32, max 392, mean 46.16 lb, zero ≥ 400.
Grams-as-pounds would show hundreds to thousands.

Keeping those two labels distinct is the §12 R1 discipline. "The code can produce
a wrong value" and "the data contains a wrong value" are two claims; the first
does not establish the second. Reporting the weight hazard as a defect would have
been R1 again — a real measurement, an unverified consequence.

## One reproducibility bug in the original

`HIDEABLE_CARRYFORWARD_FILE = "products.aug06-live.csv"` is a **bare relative
path**, resolved against the current working directory rather than the script's
directory. Run the build from anywhere else and carry-forward silently returns
nothing — which is exactly the failure that blanked `ImageFileName` on 19
products with live images. `ecatlib.load_carryforward` returns an explicit
warning instead of a silent `{}`; callers should pass an absolute path.

## The twelve

| # | primitive | where |
|---|---|---|
| 1 | money | `values.parse_money` |
| 2 | weight | `values.parse_weight_lb` |
| 3 | dimensions | `values.build_dimensions` |
| 4 | Y/N booleans | `values.to_boolean` |
| 5 | dates | `values.normalize_date` |
| 6 | LongDesc truncation | `desc.build_long_desc` / `build_short_desc` |
| 7 | text hygiene | `values.clean_text` / `clean_na` / `clean_lookup` / `clean_country` |
| 8 | RelatedItems | `related.build_related_items` / `merge_related` |
| 9 | variant grouping | `related.variant_key_by_name` / `variant_key_by_sku_suffix` |
| 10 | taxonomy | `carryforward.rollup_taxonomy` |
| 11 | CSV IO | `csvio.read_rows` / `write_rows` |
| 12 | carry-forward | `carryforward.load_carryforward` / `apply_carryforward` |

Field lengths and enums are **not** here — they are generated into
`preflight/limits_generated.py` from `supercat_server`. Callers pass limits in;
several documented numbers are wrong and a transcribed limit is a build error.

`carryforward.diff_against_previous` implements BUILD_SPEC B6 — it enumerates
dropped/added keys and per-column changes, counting **blanked** columns
separately, because blanking is the dangerous direction.

## Not yet done

- libco and tcs have **not** been rebuilt against the library. Their dialects are
  encoded from reading their source, not proven by reproduction. Legrand is the
  only client with a passing acceptance test.
- The client-specific loaders (`load_us_radiant_prices`, `load_spec_master`,
  `stage2_lantern_rebuild`, …) remain client-specific and correctly so.
