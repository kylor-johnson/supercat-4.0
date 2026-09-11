# The mapping format — Phase 2

**Status: acceptance test PASSES.** Three live eCat files regenerated
byte-identical from mappings alone, with the client build scripts discarded, and
red under 11 mutated mapping entries across two structurally different clients.

```
leg products.csv    404,798 bytes   byte-identical   (1,020 rows)
leg inventory.csv    35,067 bytes   byte-identical   (1,194 rows)
mer products.csv     40,995 bytes   byte-identical   (  102 rows)
```

---

## The one sentence

A build used to produce **a script**, which is why there are sixty of them.
A build now produces **a mapping**, and the code is shared.

`mapping/mapper.py` is ~450 lines, client-agnostic, and is the only code that
runs. Legrand's 1,537-line `build_ecat_files.py` is not imported, patched, or
read. Everything Legrand-specific is 470 lines of TOML.

---

## Why TOML

The format had to be chosen, not defaulted into. YAML was the obvious candidate
and lost on two counts.

**1. YAML 1.1 parses `Y`, `N`, `NO`, `ON` and `OFF` as booleans.** This is a
format whose entire subject matter is Y/N boolean dialects, country codes,
finish names and taxonomy labels. `NewItem = N` silently becoming `False` is
precisely the class of silent rewrite this phase exists to prevent, and it would
be found — if at all — as a wrong value on a rep's iPad. TOML has one string
type and no such coercion.

**2. `tomllib` is in the standard library; PyYAML is not installed here and
cannot be** (the Homebrew Python is PEP 668 externally-managed). The ingestion
agent was settled on 2026-09-04 as ~5,900 loc that runs *inside the VPN* next to
the database, in a container on a cron. Zero dependencies is worth real money
there, and it matches `ecatlib`, which is stdlib plus `openpyxl`.

JSON was never a candidate: a mapping is a document a human reviews and approves
before an upload, and a format without comments cannot carry the reason a
decision was made. Roughly half of each mapping file is the *why*.

---

## Anatomy

```toml
client = "leg"   org_name = "Legrand"   org_id = 273
target = "products.csv"
dialect = "legrand"              # NEVER inferred
line_terminator = "crlf"         # part of the client's file contract
tables_files = ["tables.toml"]
primary_input = "product_file"

[inputs.<name>]                  # csv | csv_multi | xlsx
[escape_hatch]                   # module + declared fns + budget
[carry_forward]                  # source, key_column, require
[[derived]]                      # ordered intermediates, not emitted
[related_items]                  # the family pass
[[fields]]                       # ORDERED — this is the file's column order
```

Per field, the format carries what the definition of done requires: **source
column, eCat field, primitive, dialect, parameters, and `carry_forward`.**

### Operators

`const` `ref` `column` `apply` `source` `source_switch` `lookup` `contains`
`equals` `starts_with` `ends_with` `concat` `coalesce` `branch` `custom`

Plus per-step `only_when` / `otherwise_value` gating, `override_by_key` for
per-SKU corrections, and file-level `skip_row_when_blank`, `dedupe`, `sort_by`,
`row_order`.

`otherwise_value` (a literal) and `branch`'s `otherwise` (a scope name) are
deliberately different keys. Collapsing them emits the *name* instead of the
value — a bug this format hit once and now cannot express.

### Primitives

Named, never a Python path: `trim money weight boolean date clean_text clean_na
clean_country clean_lookup clean_integer integer round dimensions long_desc
short_desc variant_key`. Each resolves to `ecatlib`. **Adding a primitive is an
`ecatlib` change, not a mapping change.**

---

## The dialect is the point

BUILD_SPEC §2 reads as though extraction were mechanical. It is not — the builds
disagree on *output*:

| primitive | legrand | libco | tcs |
|---|---|---|---|
| money | `4058.00`, always 2dp | `4058`, integers drop `.00` | passthrough after stripping `$` `,` |
| boolean | `Y` / `""` | `Yes` / `No` | — |
| weight | unit-aware, `500 g` → `1.102311` | first number, `500 g` → `500` | — |

**This was not theoretical for one minute of this build.** mer's mapping first
declared `legrand`. The diff against the live file refuted it: four columns
disagreed, all prices, all the same shape —

```
NetPrice         live 25      mapping 25.00
Price_trade      live 15      mapping 15.00
Price_dropship   live 12.5    mapping 12.50
Price_wholesale  live 10      mapping 10.00
```

mer is **passthrough** (`tcs`). 137 values across three price levels differ
between the two choices. Every one of them is a valid, plausible price under
either dialect; no importer would reject them and no clean import would notice.
The only thing that caught it was diffing against a build that is already live.

A mapping that says "money" without saying *which* money is not a mapping. It is
a coin flip across three clients' files.

---

## The escape hatch is budgeted

**Two categories, and only one is budgeted.**

**Per-field custom transforms — 3 per client.** A field whose transform is not
`primitive + dialect + parameters`. Past three, **stop**: that is evidence the
library is missing a primitive. File it against `ecatlib`, add it there, and the
next client gets it free. Never fork a primitive into a client's mapping.

**Bespoke source loaders — named, not budgeted.** They answer *how do I assemble
the input*, not *how do I transform a value*.

**The rule that separates them:** if it touches a single field's value it is a
transform and it is budgeted. If it decides which rows and files exist at all,
it is a loader.

### Usage against the budget of 3

| client | per-field transforms | loaders |
|---|---|---|
| **leg** | **1 of 3** — `packed_volume_cuft` | **0** |
| **mer** | **3 of 3** — `image_filename_from_code`, `sample_counterpart`, `design_family_key` | **0** |

**leg needs zero bespoke loaders**, which contradicts BUILD_SPEC §2. It lists
`load_us_radiant_prices` and `load_ca_adorne_prices` as "genuinely
client-specific". They are not: the four price books differ only in the row the
data starts on and which column index holds which price. That is *parameters*,
and one shared `xlsx` reader covers all four. The same is true of the two
inventory files, which the `csv_multi` reader unions.

mer is **at budget**. A fourth transform is not permitted there; it would be
filed against `ecatlib` instead. Two primitives were filed and added exactly
that way while writing these mappings:

- **`values.parse_int`** — a signed integer with no floor. `clean_integer`
  clamps to 1 because `MinimumQuantity` must; a stock count must not. leg has
  23 negative on-hand rows, one at **−12,643**, and clamping them would invent
  stock that does not exist.
- **`values.round_decimals`** — round and drop trailing zeros. `parse_money`
  *pads* because a price's width is part of its contract; a weight is a
  measurement. mer's `0.008` lb ships as `0.01` while `6.5` must stay `6.5`.

Both additions were re-run against Phase 1's acceptance test: still
byte-identical, 404,798 bytes.

---

## The option stack — a second SHAPE, not another mapping

Everything above is column -> column: one source row in, one output row out.
The option stack is not, and that is a **format change**.

tcs's 72 columns between `Propane Tip` and `Seeded Replacement Glass - SRG` are
the option stack transposed sideways into the product sheet — each header an
option NAME, each cell an option CODE. N source columns have to become M rows in
two other files plus a per-product reference back. `[[fields]]` cannot say that.

```toml
kind = "option_stack"

[option_catalogue]          # OPTIONAL — the client's own option LIST
input = "accessories"
code  = "Accessory SKU"
name  = "Accessory Name"
type  = "Accessory Category"
emit  = "referenced"        # referenced | all
fields = { PriceAddend = "Accessory Dealer Net" }

matrix_columns = [...]      # the transposed block: WHO can have which

[[axis]]
code = "CM"   name = "Ceiling Mount"   option_set = 7   required = "N"
option_types = ["CEILING MOUNT"]     # ... or `columns = [...]`, never both
grouping   = "per_product"           # per_product | per_column | single
group_code = "CM{n}"   group_name = "Ceiling Mount {n}"
```

### Three readings, and the format refuses to default

| `grouping` | the group is | right when |
|---|---|---|
| `per_column` | one source column | the cell is the same code on every row |
| `single` | the whole axis | the choice is catalogue-wide |
| `per_product` | one product's COMBINATION of codes | the cell VARIES by row |

The test is in the data: `Gas Pressure Regulator` is `GPR` on all 125 populated
rows; `Post Fitter` is PF1..PF5, PFPAU, PFG15. A varying cell can only mean
*this product's post fitter is PF3*, which is a per-product statement. Choose
`per_column` there and a product carrying PF3 is offered all five.

There is **no default**, for the same reason `dedupe.keep` has none: with a
sideways block the reading is a client decision and the file cannot be built
without answering it.

### A sideways block is TWO sources

```
the CATALOGUE   what the options ARE      rows    -> options.csv
the MATRIX      who can HAVE which        columns -> option_groups.csv
```

This is the lesson of the tcs 2b run and it cost 30 points. Written blind, the
mapping treated the 72 columns as the whole stack and derived the eight-way type
partition by hand from the column names. 338 of the build's 341 options are rows
of `Accessories-Table 1.csv` — with `Accessory Name`, `Accessory Dealer Net` as
the PriceAddend on 338 of 341, and `Accessory Category` holding the eight option
types the mapping had spent a paragraph inventing.

With a catalogue present the partition is not a judgement call at all.
**Before declaring a partition, look for the column that already carries it.**

### Per-code type override — the catalogue cannot always say

The catalogue's type is per **CODE**. The matrix's type is per **COLUMN**. When
one code appears in columns of two different types the catalogue cannot express
it and the code lands in exactly one axis.

```toml
[option_type_overrides]
"LR" = "CEILING MOUNT"      # the client files it under POST & PIER MOUNT
```

tcs's `LR` is `Ladder Rests` in the catalogue, filed under POST & PIER MOUNT, and
used in the `Ladder Rests` column (171 rows, a ceiling mount) as well as in
`Post Ladder Rest` (3 rows, where the other 156 are `PLR` — a source typo). That
one row was **68 of 100 wrong member sets and 22 points of recall**, because
per-product groups multiply it across every product offering the code.

Declared data with a reason, never inferred. A mapping that silently re-filed a
client's own categories is the class-2 failure in a new costume.

### One mapping, three artifacts — and the third is NOT an import file

`options.csv`, `option_groups.csv` and the per-product
`_INTERMEDIATE_option_assignments.csv` come out of ONE traversal, deliberately.

**Only the first two are import files.** There is no importer slot for a
product-to-group table: a product references a group through `OptionSet1..20`
columns INSIDE `products.csv`. The third is an intermediate that gets merged into
products.csv before upload. Because it looks exactly like an import file and
lands next to two real ones, the engine **refuses** an `emit.assignments` name
matching any importer target and **warns** on any name not prefixed
`_INTERMEDIATE`. Every run prints *UPLOAD: options.csv and option_groups.csv
ONLY*.

`option_set` accepts **1..20** and refuses anything else. Fleet max is 20; 30
orgs use more than 5 and 37,803 references sit above `OptionSet5`. The engine
never capped — slots 13–20 are exercised — but `OptionSet21` is not a column,
and a products.csv carrying one imports with that column silently ignored,
taking the whole axis with it. Importing `options.csv` **nulls group
membership**, so `option_groups.csv` must be re-sent from the same traversal or
it references codes that no longer exist. `mali` sits at BLOCKING for exactly
that. Two mappings is how they drift.

The engine checks it on the output before anyone proposes an upload, and states
its coverage: *evaluated 1,322 of 1,322 group-membership references and 1,992 of
1,992 OptionSet references; 0 unresolved.*

### Field limits — the code, not the KB

```
option / option-group  Code max 15   Name max 50      (the KB says 8 / 25 and is wrong)
option images          square 300x300, /option_images, default {code}.jpg
```

Over-length **refuses at build time**. A long code fails the import outright.

`ImageName` is a trap dressed as a convenience. Only **31 of tcs's 341** options
use the `{code}.jpg` default; the rest are a hand-built swatch map that exists
nowhere in the source folder. Emitting the default would have been wrong on 322
of 328 rows — Legrand's 19 destroyed images in a different file. A value the
generator cannot derive comes from the last known-good file, or it is not
emitted at all.

### The import order is part of the output

```
options -> option_groups -> products -> stories -> inventory -> customers
                ^ re-send option_groups AFTER options
```

`mapper.py` prints it on every option-stack run, because the ordering is not
advice — three of these six files hard-delete:

| file | on import |
|---|---|
| `options.csv` | HARD-deletes all options AND nulls group membership |
| `option_groups.csv` | HARD-deletes all groups, then reloads |
| `customers.csv` | HARD-deletes ALL customers and ship-tos, then reloads |
| `stories.csv` | sets story = NULL (does NOT delete the product) |
| `products.csv` | soft-deletes |

And the deletes only run on a WARNING-ONLY import. A single Error row suppresses
them, which is why "the delete didn't happen" is usually an Error row nobody
read.

---

## A declared column that matches no header now warns

The cheapest item on the Phase 2 gap list, and it had already bitten three
times: case (`materials` / `Materials`), trailing whitespace (`Dealer Net ` in
tcs's Master), near-duplicates (`UPC` / `UPC/GTIN`). tcs W2 is the specimen —
the reader strips header whitespace, the mapping declared the raw name, and
`NetPrice` came back blank on 379 of 425 rows. Two correct decisions that were
not made in the same place.

Every run now reports:

```
declared_column.coverage   evaluated 16 of 16 declared columns against 16
                           headers; 0 matched nothing
```

and names a NEAR MISS where one exists, because "matched no header" is only half
an answer — `Dealer Net ` -> `Dealer Net` is the whole bug.

---

## The TOML scoping trap, now refused

A bare key written after `[[axis]]` or `[inputs.x]` binds to that table. Writing
`options_columns` at the bottom of a mapping silently made it a key of the last
axis; the emitter never saw it and `ImageName` vanished from the output with no
error anywhere. The engine now refuses an unknown key in either place and says
to move file-level settings above the first table.


---

## Carry-forward is first-class

A mapping describes source → target, and carry-forward **has no source**. That
is exactly why it recurs here, so it is a per-field declaration rather than a
post-step someone remembers.

```toml
carry_forward = { when = "blank" }              # derived value wins, this fills gaps
carry_forward = { when = "always", default = "N" }   # stored value is authoritative
```

- `load_carryforward` returns `(dict, warning)` and the engine **never discards
  the warning**. With `require = true` (the default) a missing source **aborts**
  rather than continuing with `{}`. The original bug was a bare relative path
  resolving against the working directory, silently carrying nothing. The engine
  resolves to an **absolute path, always.**
- On leg this is not decoration: the run restores **19** `ImageFileName` values,
  and removing the declaration turns the acceptance test red on exactly those 19
  rows. Those are the 19 products whose live images a regeneration destroyed
  once.

**Row order is carry-forward too.** mer's live row order came from an earlier
hand-built generation and no ordering of the NetSuite export reproduces it. The
importer does not care — but `diff_against_previous` does, and BUILD_SPEC B6
asks for a diff whose only differences are intended. That is unreadable if every
row moves. Same rule, same reason: a value the generator cannot derive comes
from the last known-good file or regeneration destroys it.

---

## What the acceptance test actually proves, and what it does not

Byte-identity is not equally strong for both clients, and the difference matters.

**leg — strong.** Every emitted column is derived from source. Only `Hideable`
and blank `ImageFileName` are carried. The mapping reproduces a file built by a
1,537-line script it never reads.

**mer — weaker, and here is the denominator.** Of 31 columns, **20 are derived
from source** and **11 are carried forward** (`MediumDesc`, `ShortDesc`,
`Dimensions`, `Materials`, `Features`, `Hideable`, `Design`, `Colorway`,
`Material`, `Format`, `Width`). The carried 11 are byte-identical *by
definition* — they are copied from the file being diffed against — so they are
**not evidence**. The 20 derived columns are, and each was measured at **102/102
rows** before carry-forward was introduced.

Row order is likewise carried, not derived.

**Why those 11 are not derivable, with the specimen:** they are human editorial
values, and the human was not consistent. `Design` is the design name from the
description, with a trailing "MURAL" sometimes removed and sometimes not —
`GK9194` ships as `Deep Sea` from a source reading `DEEP SEA MURAL`, while
`GC9193` ships as `Eden Chinoiserie Mural` and keeps it. The best mechanical
rule agrees on **32 of 102**. Shipping a derived value would silently overwrite
a human's editorial decision on ~70 rows.

Note the distinction that makes both true at once: the same normalisation
*is* correct for **grouping** — `RelatedItems` families keyed on the
MURAL-stripped design match **102/102**. Grouping and labelling are two
different questions, and the mapping answers them separately.

---

## What this format cannot do

Stated so the next client is not surprised.

- **One mapping produces one file.** Legrand's script also emits `stories.csv`,
  taxonomy worksheets and `custom-fields-setup.md`. Those are not mapped.
- **`stories.csv` is not a valid target at all** — the committed artifact is
  post-processed by `fix_stories_encoding.py` to repair mojibake, so it differs
  from generator output and the *unpatched original script* differs from it too.
- **No multi-output custom transform.** A single parse producing six fields
  costs six hatches, which is over budget by design — it is the signal to add a
  primitive.
- **`libco` and `tcs` are unproven.** Their dialects are encoded from reading
  their source, never from reproduction. `leg` and `mer` are the only clients
  with a passing acceptance test. Do not treat the libco/tcs dialect entries as
  verified.
- **Two clients is not a general claim.** The format survived a second client
  that it was not designed around, which is evidence, not proof.

---

## Running it

```bash
# build a file from a mapping
python3 mapping/mapper.py mappings/legrand/products.toml "<Legrand dir>" out.csv

# the acceptance test — green AND red, both clients
python3 mapping/acceptance_mapping.py "<Legrand dir>" "<111Mercer dir>"

# before proposing any upload: B6 regeneration diff, then A1 org fingerprint
python3 mapping/preupload_check.py out.csv <previous.csv> --org leg
```

Read-only throughout. Phase 2 produces files and mappings; a human decides what
is uploaded, after A1.
