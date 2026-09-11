# Phase 2 — the mapping layer

**Nothing previously turned a client's source file into `products.csv`.** Phase 0
(`profiler/`) says what a source folder contains. Phase 1 (`ecatlib/`) transforms
a value once you know what it is. This is the statement in between: *which source
column feeds which eCat field, through which transform, in which dialect.*

```
mapping/
  mapper.py                  the engine — CLIENT-AGNOSTIC, the only code that runs
  acceptance_mapping.py      the acceptance test: green AND red, both clients
  preupload_check.py         B6 regeneration diff, then A1 org fingerprint
  extract_tables.py          one-off: read a client script's lookup tables out as data
  extract_mer_tables.py      one-off: read mer's taxonomy roll-up out of its live build
  MAPPING_FORMAT.md          THE SPEC — read this one

mappings/<client>/
  products.toml  inventory.toml   the mapping (data)
  tables.toml                     generated lookup tables
  custom.py                       budgeted per-field escape hatches
```

## Result

```
leg products.csv    404,798 bytes   byte-identical   1,020 rows
leg inventory.csv    35,067 bytes   byte-identical   1,194 rows
mer products.csv     40,995 bytes   byte-identical     102 rows

red under 11 mutated mapping entries across both clients
escape hatches: leg 1 of 3, mer 3 of 3.  Bespoke loaders: 0 and 0.
```

`build_ecat_files.py` (1,537 lines) is not imported, patched or read by any of
this. Reproduce:

```bash
python3 mapping/acceptance_mapping.py \
  ".../02_Implementation/Legrand" ".../02_Implementation/111Mercer"
```

## Read `MAPPING_FORMAT.md` before editing a mapping

It carries the format, the operator list, why TOML, the dialect argument, the
escape-hatch budget, and — importantly — **what the acceptance test does not
prove**. mer's byte-identity is weaker evidence than leg's: 11 of its 31 columns
are carried forward rather than derived, and carried columns match by definition.

## Two things that changed in `ecatlib`

Both are additions, both were found by a mapping that could not express a
transform, and both were re-run against Phase 1's acceptance test (still
byte-identical, 404,798 bytes). This is the intended flywheel: a mapping over
budget is evidence of a missing primitive, and it lands in the library where the
next client gets it free.

- `values.parse_int` — signed integer, no floor. `clean_integer` clamps to 1
  because `MinimumQuantity` must; a stock count must not. leg has 23 negative
  on-hand rows, one at −12,643.
- `values.round_decimals` — round and drop trailing zeros. `parse_money` pads
  because a price's width is contractual; a weight is a measurement.

## Open items this phase produced

Findings, with their measurements separated from their consequences. None have
been acted on; none should be without the client.

**1 — leg's `LongDesc` is capped at 50 where the importer allows 255.**
*Measurement:* `build_ecat_files.py` sets `LONGDESC_LIMIT = 50` and
`SHORTDESC_LIMIT = 15`. `preflight/limits_generated.py`, generated from
`supercat_server` (sha `d4a0e7d`), gives `longdesc` **255** and `shortdesc`
**255**, both `truncate` tier. In the produced file, max `LongDesc` length is
exactly 50 and 382 of 1,020 rows sit at ≥45 characters; the build reports 386
of 1,020 word-boundary truncated. Specimen: `ASVS12G4` ships
`Motion Sensor Switch, Manual On/Auto Off, Graphite` (50 chars) with `ShortDesc`
`Motion Sensor` (13).
*Not established:* whether 50 was chosen deliberately for grid legibility or
believed to be the importer's limit. The script comments read as the latter, but
**structure is not intent** — ask before changing it. The mapping pins 50/15
because reproduction demands it; changing them is a separate, deliberate act.

**2 — leg's two Canadian adorne price columns are one price level.**
*Measurement:* in `adorne_ca.xlsx`, columns 6 and 7 hold identical values on all
448 rows. `Price_camsrp` and `Price_caimap` therefore carry the same number for
every adorne SKU. `radiant_ca.xlsx`'s equivalents differ on all 631 rows, so
this is specific to the adorne book. (The profiler's `SKILL.md` records the same
shape from the raw files: "`MSRP CDN` and `IMAP CDN` hold the same 448 values".)
*Not established:* whether that is a duplicated export column or two genuinely
equal price levels. Building two levels where the client has one is a config
error nobody notices until a rep sees the wrong number.

**3 — BUILD_SPEC §2 overstates what is client-specific.**
It lists `load_us_radiant_prices` and `load_ca_adorne_prices` as "genuinely
client-specific". They are not. The four price books differ only in the data
start row and which column index holds which price — parameters, not code. One
shared `xlsx` reader covers all four, and leg needs **zero** bespoke loaders.
Worth correcting, because the §2 list is what the escape-hatch budget of 3 was
calibrated against.

**4 — the line terminator is part of the client's file contract.**
leg's live `products.csv` is CRLF (1,021 of them). mer's is LF on all 103 lines.
Both are live and both import clean, so neither is "the" right answer — which
makes it exactly the kind of thing that must be declared per client rather than
inherited from whatever wrote the file last. It is now `line_terminator` in the
mapping, and a mutation of it goes red.

## Scope

Read-only throughout. This phase produces **files and mappings**; a human decides
what is uploaded, after `a1_fingerprint.py` has run against the produced file.
Nothing here writes to Postgres or the Admin Console.

`acceptance/` is another session's; it was read, never modified.
