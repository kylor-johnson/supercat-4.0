# Phase 2 — the mapping layer. Six file types, complete.

**Nothing previously turned a client's source file into an eCat import file.**
Phase 0 (`profiler/`) says what a source folder contains. Phase 1 (`ecatlib/`)
transforms a value once you know what it is. Phase 2 is the statement between
them: *which source column feeds which eCat field, through which transform, in
which dialect.*

A build used to produce **a script** — sixty of them, ~15,000 lines, zero shared
modules. A build now produces **a mapping**, and the code is shared.

`mapping/mapper.py` is client-agnostic, stdlib + `ecatlib` only, and is the only
code that runs. No client build script is imported, patched or read.

**2b closed the gap that made "complete" a qualified word — and "complete"
stays qualified, differently.** All six eCat file types now MAP: `products`,
`inventory`, `options`, `option_groups`, `customers`, `stories`. The ingestion
agent can produce a full client build.

Four of the six are ready to upload. **The option stack is not**, and the reason
is data the folder does not contain rather than a mapping the layer cannot
express — see *PASS means no regression* below. "Six file types map" and "six
file types ship" are different claims and only the first one is true.

---

## The format

**TOML**, read with stdlib `tomllib`. Chosen, not defaulted into:

1. **YAML 1.1 parses bare `Y`, `N`, `NO`, `ON`, `OFF` as booleans.** This is a
   format whose subject matter is Y/N boolean dialects, country codes and
   taxonomy labels. `NewItem = N` silently becoming `False` is the exact class of
   silent rewrite the phase exists to stop.
2. **Zero dependencies** — the ingestion agent runs inside the VPN in a
   container, and PyYAML is not installable there (PEP 668).

JSON was never a candidate: a mapping is reviewed and approved by a human before
an upload, and a format without comments cannot carry *why*. About half of each
mapping is the reason.

**Two shapes, not one.** `kind = "row_map"` (the default) is column -> column,
one source row in, one output row out. `kind = "option_stack"` is N source
columns -> M rows in two other files plus a per-product reference. That second
shape is 2b's format change and it is described in MAPPING_FORMAT.md.

---

## What each file type cost, and what it taught

| file type | clients | shape | the lesson |
|---|---|---|---|
| `products.csv` | leg mer libco drf tcs | row_map | the **dialect** is load-bearing; `money` without saying *which* money is a coin flip |
| `inventory.csv` | leg | row_map | two feeds into one slot **union**, never compete (A8) |
| `options.csv` | tcs **(n=1)** | **option_stack** | a sideways block is **two sources**: the catalogue and the matrix |
| `option_groups.csv` | tcs **(n=1)** | **option_stack** | membership and code spelling are **two different scores** |
| `customers.csv` | tcs mali | row_map | a class-3 rule about not editing the client's text **does not survive contact with a validated field** |
| `stories.csv` | tcs | row_map | a prose field on a spec sheet is usually a **part**, not a candidate |

---

## Scores

**The blind score is the run before any post-unblind fix.** Numbers measured
after correcting against the answer key are reported separately and are not the
score.

### Reproduction (leg, mer) — still byte-identical after every 2b engine change

```
leg products.csv    404,798 bytes   byte-identical   (1,020 rows)
leg inventory.csv    35,067 bytes   byte-identical   (1,194 rows)
mer products.csv     40,995 bytes   byte-identical   (  102 rows)
```

`acceptance_mapping.py`: PASS, and **red under 11 mutated mapping entries**
across two structurally different clients.

### Blind (libco, drf, tcs)

| client | file | denominator | blind | after fixes |
|---|---|---|---|---|
| libco | products | 63 cols | 26 cols / **88.6%** cells / 97.3% semantic | 29 cols |
| drf | products | — | **no score, and that is the finding** | — |
| tcs | products | 60 cols | 7 cols / **66.2%** of 7,225 cells | 8 cols / 71.5% |
| tcs | options | 341 codes | **65.8%** of 990 cells | **96.1%** of 1,312 |
| tcs | option_groups | 311 member sets | **46.6%** recall | **91.0%** |
| tcs | **option availability, end to end** | 379 products | — | **0 of 379 exact**; 85.5% recall / 83.2% precision |
| tcs | customers | 721 rows / 23 cols | **83.1%** of 13,699 cells, 9 cols exact | **99.96%**, 14 cols exact |
| tcs | stories | 628 rows / 2 cols | **50.0%** of 758 cells | **100.0%** byte-identical |
| mali | customers | 3,418 rows / 16 cols | — (class 2) | **96.9%**, 6 of 16 columns CARRIED |

`acceptance_2b.py`: PASS, **red under 11 mutated mapping entries** across four
file types.

### PASS means no regression. It does not mean client-ready.

That distinction is load-bearing and the first version of this document got it
wrong: a 67.8% row sat in a summary table next to four 96–100% rows and read as
though options could ship. They cannot.

| file type | state | why |
|---|---|---|
| `stories.csv` | **ready** | byte-identical, 379 of 379 rows |
| `customers.csv` | **ready** | 13,693 of 13,699 cells; the 6 are named and each has a reason |
| `products.csv` / `inventory.csv` | **ready** (leg, mer) | byte-identical reproduction |
| `options.csv` | **BLOCKED** | 13 option codes exist in no file in the folder. `COPPER` is a finish on 375 of 379 products, and `options.csv` HARD-deletes |
| `option_groups.csv` | **BLOCKED** | **0 of 379 products have identical option availability.** 1,561 EXTRA offers — a rep can pick an option the build does not offer for that product |

**The metric that gates a client did not exist until it was asked for.**
`group_membership` counts DISTINCT member sets, and with per-product groups that
is a poor proxy for what a rep sees: the Finish family is 2 of 311 sets and
applies to 375 of 379 products. Membership read 91.0% while per-product option
availability was exact on **zero** products. Both numbers are true; only the
second one gates an upload. `acceptance_2b.py` now reports it and says so.

**The residual is characterised, not hand-waved** — one systematic cause at the
membership level (`LR`, 68 of 100 sets, worth 22 points) and a fully decomposed
28-set tail with four named causes, every one a superset/subset difference
*inside the correct axis*. See `mappings/tcs/SCORE_2b.md § the residual`.

**drf has no score and that is the finding.** Zero key overlap: the build is
keyed pattern × colourway (`ADELINA-UV-ASH`), the source carries only the pattern
(`ADELINA-UV`). A per-column score over an empty intersection is vacuous.

**Read the cell number, not the column number** — and read the coverage line
under both. Every score now states `evaluated N of M candidates`, because a
denominator that quietly excludes what could not be produced is how a check with
nothing to measure reports a pass.

**mali's 96.9% carries a denominator that matters:** 6 of its 16 columns are
carry-forward and are byte-identical *by definition* — copied from the file being
diffed against. The 10 derived columns are the evidence. Same rule, same reason
as mer's eleven.

### n = 1 on the option stack, and that is not a footnote

**`options` and `option_groups` have exactly ONE worked example.** tcs is the
only client in the set with both a transposed source and a trusted build.

- `pebl` ships both files. Its stated source — `ecat-options mapping.xlsx`,
  named in its own `IMPORT_README.md` — **is not in the repository.** A build
  with no recoverable source cannot be reproduced from a mapping, and scoring
  against it would measure nothing. Both files HARD-delete on import.
- `leg`, `mer`, `libco` and `drf` ship no option files at all.

**One client is evidence, not proof.** Everything the format asserts about
sideways option blocks — three readings, the catalogue/matrix split, the
per-code type override, eight axes falling out of a category column — rests on a
single sheet. The other five file types each survived a second, structurally
different client; this one has not, and the transposed shape is the one most
likely to differ next time.

Read the option numbers with that in front of them. `products.csv` earned its
confidence across five clients. The option stack has not earned any yet.

---

## The four findings from 2b worth carrying to the next client

**1. A sideways option block is TWO sources.** The catalogue says what the
options are (rows -> `options.csv`); the matrix says who can have which (columns
-> `option_groups.csv`). Collapsing them forces the mapping to invent the half it
is missing — names, prices, and worst of all the type partition. 338 of tcs's 341
options were rows of a sheet already in the folder, whose `Accessory Category`
column *is* the eight-way partition the blind run derived by hand.

**Why it was missed is the reusable part, and it generalises past options.**

Classification is not a property of a source file. It is a property of the pair
**(source file -> target file type)**, and the profiler, the kickoff and my own
head all treated it as the former.

`Accessories-Table 1.csv` was classified once, on the products run, as a source
of products. That was correct — 46 of its 419 rows ship as products. It is ALSO
the option catalogue: 338 of the build's 341 options are its rows, and its
`Accessory Category` column *is* the eight-way option-type partition the blind
mapping spent a paragraph deriving from column names. Having answered "what is
this sheet" once, nobody asked it again for a different target.

```
WRONG:  sheet          -> one classification
RIGHT:  (sheet, target file type) -> one classification, per pair
```

**This will recur on the next multi-sheet client**, and it is cheap to prevent:
a class-3 folder with S sheets and 6 target file types has 6S questions, not S.
Phase 0's target coverage answers "which sheet feeds products.csv" and then
stops; the same sheet feeding `options.csv`, `stories.csv` or `customers.csv` is
a question it never asks. The transposed-stack detector closed one cell of that
grid by accident. The grid itself is still not enumerated anywhere — filed as
gap 10 below.

**2. `DefaultPriceCode` case is not cosmetic.** The blind run predicted `MAP`;
the live value is `map`. It must match an Admin price level code *exactly*, and a
mismatch rejects every row and loads zero customers. Everything about that
failure looks like a file-format problem and none of it is.

**3. The catalogue's type is per CODE; the matrix's type is per COLUMN.** When
one option code appears in source columns of two different types the catalogue
cannot say so, and the code lands in exactly one axis. tcs's `LR` is that code —
the client files it under POST & PIER MOUNT and it is a ceiling mount — and it
alone was **68 of the 100 member sets the mapping got wrong, 22 of the 32 points
of missing recall**, because per-product groups multiply one bad row across every
product that offers it (171 of 379).

`option_type_overrides` expresses the correction as declared data with a reason.
Never inferred: a mapping that silently re-filed a client's own categories would
be the class-2 failure in a new costume. Reverting it is a gated mutation.

**4. An empty `TerritoryCodes` needs a declared default.** It is KB-required and
NOT importer-fatal, so a blank imports clean and the customer is then invisible
to every rep in a "show only associated customers" group. `pebl` sits at BLOCKING
with 171 of 171 blank; tcs had 8 of 724, which is the dangerous size — too few to
notice, enough to lose eight dealers from every territory-scoped rep's list.
`required_check.py` now fails a customers mapping whose `TerritoryCodes` has no
default.

---

## Import order, and why the mapping prints it

```
options -> option_groups -> products -> stories -> inventory -> customers
                ^ re-send option_groups AFTER options
```

Three of the six **hard-delete**: `options.csv` (and it nulls group membership),
`option_groups.csv`, and `customers.csv` (all customers *and* ship-tos).
`stories.csv` sets story = NULL without deleting the product. Only
`products.csv` soft-deletes.

And the deletes only run on a **WARNING-ONLY** import — a single Error row
suppresses them, which is why "the delete didn't happen" is usually an Error row
nobody read.

### The option stack's third artifact is NOT an import file

`options.csv` and `option_groups.csv` are the only two files the importer reads
here. **There is no importer slot for a product-to-group table** — a product
references a group through `OptionSet1..20` columns INSIDE `products.csv`.

So the third artifact is an internal intermediate that is merged into
`products.csv` before upload, and it is named `_INTERMEDIATE_option_assignments.csv`
so nobody FTPs it. It looks exactly like an import file, it lands next to two
real ones, and three of the six file types hard-delete — so the name has to make
the mistake impossible rather than unlikely:

- the engine **refuses** an `emit.assignments` name that matches any importer
  target (`products.csv`, `options.csv`, `option_groups.csv`, `inventory.csv`,
  `customers.csv`, `stories.csv`, `matrix_options.csv`, `taxonomies.csv`)
- it **warns** on any name not prefixed `_INTERMEDIATE`
- and every run prints *"UPLOAD: options.csv and option_groups.csv ONLY"*

The merge is a mapping, not a script: `mappings/tcs/products_optionsets.toml`
reads the intermediate keyed on `SKU` with `op = "source"` and emits
`OptionSet1..8`. A production `products.toml` declares those same fields inline
alongside its other 60, so ONE file goes to the FTP.

**The ceiling is `OptionSet1..20`, not 5.** Fleet max is 20; 30 orgs use more
than 5, and 37,803 references sit above `OptionSet5` (verified 2026-09-05 —
CLAUDE.md previously said 5 and was wrong). The engine never capped, which was
right and was untested; slots 13–20 are now exercised and emit correctly. It
also never *refused* an out-of-range slot, which was not right: `OptionSet21` is
not a column, a `products.csv` carrying one imports with that column silently
ignored, and the whole axis vanishes while the file reads clean. Out of range
now refuses at build time.

`mapper.py` prints the import order on every option-stack run, and the engine
checks integrity on the output first: *evaluated 1,322 of 1,322 group-membership
references and 1,992 of 1,992 OptionSet references; 0 unresolved.* That is the
A4 condition `mali` fails.

---

## Escape hatches against the budget of 3

```
leg 1 of 3   mer 3 of 3 (at budget)   libco 0 of 3   drf 0 of 3   tcs 2 of 3
mali 0 of 3
options / option_groups / customers / stories:  0 across every client
bespoke loaders: 0 across all six mappings
```

Two primitives and one operator extension were filed rather than taken as
hatches, and each is free to every client after:

- **`values.split_first`** — first value from a multi-valued contact cell. An ERP
  `Email` column holding everything anyone ever typed is universal; eCat's
  `BuyerEmail` is ONE address. 128 of tcs's 721 dealers.
- **`concat` gained `skip_blank` and `prefix_each`** — tcs's `ProductStory` is
  `Marketing Copy` + a blank line + `Feature 1..6` as a bullet list with blanks
  omitted. Six optional columns would have cost six hatches against a budget of
  three. Every catalogue has a features block.

Phase 1's and Phase 2's acceptance tests still pass byte-identical after all of
it.

---

## Phase 0's false negative is fixed

Folder mode reported `options.csv` MISSING for tcs. It was not missing — it was
sideways, inside the Master sheet. **A check whose whole job is saying what a
source folder contains, reporting absent when the thing is present, does not
merely fail to help: it sends someone to ask the client for a file they already
sent.**

`detect_transposed_options()` now reports:

```
options.csv        PRESENT, TRANSPOSED  inside Master Sheet E+G-Table 1.csv
                     66 contiguous columns, Propane Tip .. Braided Brass Ring
                     (index 87-155), 358 distinct codes over 283 rows
                     e.g. Propane Tip -> SPT, SPTL, SPTS
                     the header is the option NAME, the cell is the option CODE.
                     NOT missing. Do not ask the client for it.

OPTION CATALOGUE — the codes in that block resolve against:
  Accessories-Table 1.csv  column 'Accessory SKU'  contains 94% of the codes
```

That second half is the thing the blind run missed, produced automatically.

Each clause of the detector is there because dropping it produced a false
positive on a real folder: sparse-and-few-distinct alone matched mer's nine
price-list columns; requiring a digit matched them too (239.4); requiring a
LETTER killed them. `Country of Origin`/`China` and `Weiyan`/`Yes` are excluded
because **a code is not an ordinary word**. Empty columns are neutral rather than
breaks — treating them as breaks cut a 72-column stack into a 21-column one.

Fires on tcs. **0 false positives across 3,400+ files** in leg, mer, drf, libco
and mali folders.

---

## Running it

```bash
python3 mapping/mapper.py <mapping.toml> <client root> out.csv       # row_map
python3 mapping/mapper.py mappings/tcs/options_v2.toml <root> outdir # option_stack
python3 mapping/acceptance_mapping.py "<Legrand>" "<111Mercer>"      # green AND red
python3 mapping/acceptance_2b.py "<The CopperSmith>"                 # green AND red
python3 mapping/score_blind.py produced.csv reference.csv            # refuses if unpinned
python3 mapping/score_blind.py g.csv ref.csv --key Code --membership Options
python3 mapping/preupload_check.py out.csv previous.csv --org leg    # B6 then A1
python3 mapping/required_check.py mappings/*/*.toml
python3 profiler/folder_mode.py "<client Source Data>"               # transposed stacks
```

Read-only throughout. Phase 2 produces files and mappings; a human decides what is
uploaded, after `a1_fingerprint.py`. Nothing here writes to Postgres or the Admin
Console. `acceptance/` and `ground-truth/` were read, never modified.

---

# What a SIXTH client would need that the layer still does not have

Ranked by how likely it is to bite. Items 1, 2 and 8 from the Phase 2 list are
now closed; what follows is what is actually left.

**1. Nothing checks a mapping against the live ORG.** Still the largest hole,
and 2b widened it. `a1_fingerprint` checks the produced file. Nothing checks that
the option TYPES a mapping declares exist in Tools → Company Settings → Option
Types, that `DefaultPriceCode` matches a live price level, that
`TerritoryCodes` values match live territories, or that `CollectionCodes` match
the taxonomy already live. Every one of those is a clean import that ships
nothing usable, and the case matters — `map` against `MAP` rejects 721 rows.
**This is the next thing to build.**

**2. `options` and `option_groups` are n=1.** Stated in full above, under *n = 1
on the option stack*, because it belongs in the body rather than in a gap list.
Short version: tcs is the only worked example, `pebl`'s source is missing from
the repository, and one client is evidence, not proof.

**3. Row selection is still not expressible when it is a human's list.** mali
drops 105 of 3,517 customers and no rule in the source selects them — not blank
addresses, not duplicates, not one division. tcs's build drops 373 of 419
accessories and adds 13 option codes that appear in no source file. The format
can say *which rows exist* only when a predicate exists. It needs an
`[[exclude]]`/`[[include]]` table of keys with a reason each, so a curated list
is DATA in the mapping instead of a difference nobody can explain later.

**4. Multi-output transforms.** Unchanged from Phase 2: one function filling five
columns costs five hatches. 2b did the reverse — multi-INPUT composition — with
`concat`'s `skip_blank`/`prefix_each`, and that turned tcs's stories from 0% to
byte-identical. The other direction is still missing.

**5. `libco` and `tcs` dialects are still unproven by reproduction.** `leg` and
`mer` remain the only clients with a byte-identical products test. 2b adds
byte-identical `stories` and 99.96% `customers` for tcs, which is real evidence
for tcs's TEXT handling and none at all for its money dialect.

**6. The class-3 contract has no machine-readable form.** tcs's 711-byte
navigation file was again the highest-value artifact in the folder and again was
parsed by a human reading it. 2b also found its limit twice over: it specifies
what the rep BROWSES and says nothing about what the rep CONFIGURES. It gave no
option types, no price level, and — the expensive one — it did not say that
`Accessory Category` was the option-type partition.

**7. Row-level provenance.** Unchanged. With four sheets unioned nothing in the
output says which sheet a row came from.

**8. An enriched-source ASK is not a first-class output.** mali's live addresses
come from an export that is not in the folder; libco's `ProductStory` has no
source in the folder at all; 249 of tcs's 628 stories are written somewhere else.
The mapping can carry these forward, and carry-forward makes them byte-identical
*by definition* and therefore not evidence. What the mapping should also emit is
**the list of what to ask the client for** — the same way §3 B1b asks for a
custom-field registration list alongside the file. Right now that ask lives in a
comment.

**10. Nothing enumerates the (source file x target file type) grid.** Phase 0's
target coverage answers "which sheet feeds products.csv" and stops. A class-3
folder with S sheets and 6 target file types poses 6S questions, and the layer
asks S of them. That is the F-a miss made systematic, and it is the cheapest
remaining item: fold the grid into folder mode's coverage line so an unanswered
cell is visible rather than assumed. The transposed-stack detector closed one
cell of it by accident.

**11. `null_tokens` is dead weight on a catalogue-driven mapping** and the format
does not say so. The catalogue lookup filters `----` before the null check runs.
Harmless here, and exactly the shape of a declaration that reads as though it
applies and does not — which is the recurring defect of this whole programme.
