# Findings — building the ingestion runner, 2026-09-09

`ground-truth/` was read and **not modified**, per the brief. These are the
findings; where they belong in `OPEN_ITEMS.md` or `SCORECARD.md` is a
human's call.

Everything below was measured in this session. Where a claim came from the
brief and turned out to be stale, that is said explicitly rather than quietly
corrected.

---

## The four filed bugs

### 1. `build_ecat_files.py` writes into the client tree — CONFIRMED, fixed structurally

`build_ecat_files.py:31`

```python
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
```

and `grep argv` over the whole 1,537 lines returns **nothing**. So it is not
that it *ignores* `--out` — there is no argument parsing at all, and nothing for
it to ignore. Every one of its eleven outputs (`products.csv`, `stories.csv`,
`inventory.csv`, `TAXONOMY.md`, `group-category-map.csv`, three review
markdowns, …) is `os.path.join(OUTPUT_DIR, …)`, i.e. `Legrand/Build/`.

**Fix: the runner never invokes it.** It drives `mapping/mapper.py`, which takes
`out_path` as an argument. Every declared input is *copied* into a sandbox and
chmod'd `r--`; the build is pointed at the sandbox root, so the client tree is
not referenced during a build.

Copied rather than symlinked, which is where this departs from
`ecatlib/acceptance_legrand.py`. That file symlinks `Source Data` into its
sandbox, which is right for it — it must run the real script unmodified against
407 MB it cannot copy. But **a symlink is a write path**: a script that opens
`Source Data/x.csv` for writing writes through the link into the client tree.
A mapping declares its inputs by name, so the whole declared set can be copied
(3 MB for Legrand) and there is no link to follow. An input the mapping did NOT
declare is then absent from the sandbox, which turns a silent read of an
undeclared file into a loud failure.

And because a structural argument is only an argument, `sandbox.TreeGuard`
fingerprints the tree (sha256 + size, image extensions excluded and counted) and
reads `git status --porcelain`, before and after. Any change → exit 9. The 09-09
incident was a session that would have passed the structural argument on
inspection; it believed it was calling the mapping layer.

**Verified:** 12 runs of the runner (leg ×4, mer ×1, 5 sabotage runs, 2 partial)
left `SuperCat_Simple_Final` at **131 porcelain lines, identical to baseline,
zero tracked modifications**.

---

### 2. iCloud dataless placeholders — CONFIRMED, and verified against real ones

The filed claim: five of Legrand's eleven source files were dataless on 09-09,
`find -name '*.icloud'` does not see them, the `UF_DATALESS` flag does.

**Legrand is now hydrated** — 0 of 11 dataless, measured. So the original
instance is not reproducible. But three genuinely dataless files exist right now
in the same tree, which let the detector be tested against real state rather
than by construction:

```
02_Implementation/jcusa/Source Data/
  DATALESS  flags=0x40000060  size=1,022,920  Customer List.csv
  DATALESS  flags=0x40000060  size=  734,738  Customer List.xlsx
  DATALESS  flags=0x40000060  size=2,344,671  order_data-20260722_0900 (...).csv

find -name '*.icloud'  ->  0 hits, on that exact folder
```

Two corrections to the filed description, both minor and both worth having:

- the flag is **`SF_DATALESS` = `0x40000000`**, not `UF_DATALESS`. `0x40000060`
  is `SF_DATALESS | UF_TRACKED | UF_COMPRESSED`.
- `ls` reports full size for all three, so *size is not a signal either* — the
  only signal is the flag.

**Fix:** `preflight.check_dataless()` runs on every declared input, by flag,
every run. Without `--hydrate` it refuses (exit 3) and names each file. With
`--hydrate` it calls `brctl download` and then **polls the flag** rather than
trusting the exit code — `brctl` returns 0 for "queued" as readily as for
"done", and a queued file is still unreadable when the build opens it.

Verified end to end on `Customer List.xlsx`: dataless → `brctl download` →
flag cleared `0x40000060` → `0x00000040` in **2.2 s**, recheck passes.

**Still a hard blocker for a cron container, and hydration does not fix it.**
The fetch is unbounded, needs the network and needs iCloud running. The real fix
is to stage source folders outside iCloud; the check exists so the failure is
named at second 0 instead of appearing as a corrupt-file error deep in a build.

---

### 3. `openpyxl` interpreter pin — **the filed shape is STALE; the real constraint is tighter**

Filed: *"openpyxl is on `/usr/bin/python3` and NOT on
`/opt/homebrew/bin/python3.12`."*

Measured now:

| interpreter | version | `openpyxl` | `tomllib` | `psycopg2` |
|---|---|---|---|---|
| `/opt/homebrew/bin/python3.12` | **does not exist** | — | — | — |
| `/usr/bin/python3` | 3.9.6 | **yes** | **NO** | no |
| `/opt/homebrew/bin/python3` → 3.14 | 3.14.2 | **yes** | **yes** | no |

Homebrew has moved to 3.14.2 and it *does* have `openpyxl`. So the filed
statement no longer describes the machine — and acting on it would have picked
the **broken** interpreter, because `mapper.py` imports `tomllib` at module
level and `tomllib` is stdlib only from 3.11. `/usr/bin/python3`, the one with
openpyxl, cannot import the mapping engine at all.

The requirement is **both**, so `preflight.check_interpreter()` checks both by
import, names the missing one, and refuses. `psycopg2` is reported and never
fatal — only `--use-db` needs it and the documented path is the MCP; saying so
stops a container operator concluding the gate is broken when it is merely
credential-less.

---

### 4. Hardcoded `~/Downloads` input, warn-then-continue — CONFIRMED

`build_ecat_files.py:39`

```python
IMAGE_SOURCE_FILE = "/Users/kylorjohnson/Downloads/adorne & radiant image & video links.xlsx - Image Files.csv"
```

and at 535–538, when it is absent: two `WARNING` prints and `return mapping` —
an **empty dict**. Same class as `HIDEABLE_CARRYFORWARD_FILE`, which cost
Legrand 19 products' images. It degrades quietly because it prefers
`image_filename_map.csv` when that exists, so nobody sees the warning fire.

**Fix, three parts:**

- `preflight.collect_declared_paths()` walks the whole parsed mapping TOML for
  `path` and `source` values — rather than enumerating the keys that carry them
  today — resolves each to an absolute path, and checks existence, readability
  and non-zero size **before the build starts**. Missing → exit 3, named.
- `sandbox.stage()` **refuses a mapping that declares an absolute input path**,
  because such an input cannot be relocated into a sandbox and a build that
  reads one input from outside the sandbox has no sandbox. That is the
  `~/Downloads` shape, refused by construction.
- `mapper.py` already raised on a missing input (`_resolve`, line 118) — that
  part needed nothing.

---

## Five more defects found while building, four of them in existing code

### 5. **The gate reported column blanking and exited clean.** The worst one.

`--break-phase gate` blanks one populated column in the produced file. B6 found
it and printed, under a heading that literally says *read this first*:

```
  BLANKED columns (had a value, now empty) — read this first:
     LongDesc                  1020 of 1020 rows   e.g. 064875, 067695, ...
```

…and `preupload_check` **exited 0**. Its exit code only ever reflected
`not_checked` and (after this session's earlier change) `emitted_only`. No B6
finding, of any size, could make the gate refuse.

That is the Legrand-19-images failure mode exactly: a regenerated file that
empties a column imports CLEAN, so nothing downstream objects. On `leg` the
regression byte-check happens to catch it. **No new client has a regression
byte-check.**

**Fix:** `_verdict()` gained a fourth state and `preupload_check` now returns
**exit 4** when a check RAN and FOUND something.

- every blanked column → BLOCKING, for every file type, since blanking is
  unaffected by delete semantics;
- dropped keys → BLOCKING when the file HARD-deletes (nothing left to reverse),
  WARN when it SOFT-deletes (`deleted=true` is reversible);
- B7's `blocking` and A1's `fatal` now route here too — they had been appended
  to `not_checked`, which reported a *found defect* as a *skipped check*.

Precedence: **BLOCKING (4) > NOT CHECKED (2) > EMITTED ONLY (3) > 0.** A check
that ran and found something outranks a check that could not run; the first is
certain and actionable, the second is an absence.

### 6. **The gate exited 0 having only PRINTED the B7 and A1 SQL.**

Before this session `preupload_check` exited 0 once B6 had diffed and an `--org`
was given, with B7 and A1 only *emitted*. An operator reading `exit 0` could not
tell "B7 ran clean" from "B7 printed a query nobody ran" — the two states that
matter most. Same defect the harness exists to catch, turned on the harness.

**Fix:** three explicit states — RAN / EMITTED ONLY / NOT CHECKED — with
**exit 3** for emitted-only, plus a `--use-db` path that actually runs them.

### 7. **B7's stage-1 density SQL could not run at all on any org with images.**

```
ERROR:  invalid input syntax for type json
```

`products.images` is `text`; `products.images_json` is **`json`**. So
`COALESCE(images_json,'')` is not a wrong answer — it aborts the whole stage-1
statement, taking all seven columns with it. **B7's per-column density had never
executed against a real org carrying an `ImageFileName` column**: the check most
concerned with blanked images could not measure images.

It survived review because the expression *looks* symmetric, and because
`JSONISH` — the other kind that COALESCEs a collection — happens to sit on
`text` columns (`territory_codes`, `trade_name_codes`, `collection_codes`,
`category_codes`: all `text`, verified live). One kind was right by luck and its
neighbour was broken.

**Fix:** `::text` on every kind, not just the one that failed. A no-op on text,
correct on json/jsonb/numeric/timestamp. Removes the class, not the instance.

Found by *running* the emitted SQL through the MCP instead of reading it.

### 8. **B7 reported 100% disagreement on two columns of a byte-identical file.**

With #7 fixed, B7 ran for real against `leg` and reported:

```
ImageFileName   10 of 10 disagree (100%)
TradeNameCode   10 of 10 disagree (100%)
```

on a `products.csv` that is **byte-identical to the file that produced the live
state**. Both were false positives, with different causes:

**`ImageFileName`** — the file carries `A.jpg,A_2.jpg,A_3.jpg`; live
`images_json` carries `[{"file_name":"A.jpg","last_modified_at":"…"}, …]`. Same
fact, two encodings. `norm()`'s docstring already describes this exact defect
being found and fixed against `mali` — for a JSON array of *scalars*. The
`PAIR` kind, in the same function, four lines away, was never given the same
treatment, and `images_json` is an array of *objects*. Fixed: extract
`file_name` in order, join, and normalise the file side's trailing comma.
`last_modified_at` is server state no file can carry and is not compared.

**`TradeNameCode`** — the file carries `adorne` / `radiant`;
`products.trade_name_code` carries `TN2` / `TN3`. **The live column stores an
internal taxonomy code and the file carries the taxonomy name.** Verified:

```
item_number   trade_name_code   taxonomies.code  taxonomies.name  type
ADSM703HW2    TN2               TN2              adorne           TradeName
1597TRUSBCCW  TN3               TN3              radiant          TradeName
```

The importer auto-creates taxonomy from whatever string the file carries and
stores a generated code with that string as the NAME — which is the documented
behaviour (CLAUDE.md: *"whatever string you put in `TradeNameCode` becomes the
iPad label"*), read from the wrong end. So the file and the column are two
vocabularies for one fact, and B7 was comparing them directly.

This mattered more than one column: B7 would have emitted a 100%-disagreement
WARN on `TradeNameCode` for **every org, forever, on every correct file**. A
check that cries wolf on every run is a check nobody reads, which is worse than
a missed finding.

**Fix:** a new `TAXO` column kind, spelled `column@Type`, that resolves the code
through `taxonomies(organization_id, code, type)` in SQL. Qualified `t.` —
an unqualified `organization_id` inside that subquery binds to `taxonomies` and
would compare every product against every org's taxonomy. Density stays on the
raw column: a code is a value, and resolution is a stage-2 concern.

**After both fixes, on real live rows: 0 of 10 disagree on all 7 columns,
VERDICT PASS.** Twenty bogus WARNs → zero, on a file provably correct.

`CollectionCodes` and `CategoryCodes` are multi-valued and remain unmapped
(NOT CHECKED) — the same `TAXO` shape would apply and is not done here.

### 9. `b7_<org>.sql` was overwritten when one run gated two files.

Gating `products.csv` then `inventory.csv` for `leg` wrote both to `b7_leg.sql`;
the second silently replaced the first, so an operator would run inventory's SQL
believing it covered products. Now `b7_<org>_<type>.sql`. Mine, found by gating
two files in one run.

---

## The database half

`collector.py:197-217` and `rawstate.py:216-227` had a working `DATABASE_URL` +
psycopg2 path since August. The four modules that gate an upload had **none** —
`--emit-sql` / `--from-results` only, which means a human carries rows between
two commands. Workable at a desk, impossible on a cron: the gate could not run
in the same container that produced the file it was meant to gate. **A replica
credential alone would not have fixed that; the credential had nowhere to go.**

Written **once** in `acceptance/dbexec.py` rather than copied four times, with
each module keeping and assembling its own `--from-results` shape:

| module | flag | assembles |
|---|---|---|
| `a1_fingerprint.py` | `--use-db` | `{summary, rivals}` — split on the `-- rival orgs:` comment, not on `;` |
| `b7_lossy.py` | `--use-db` | `{meta, density{table: rows}, spotcheck}` — table read from the statement's own comment |
| `state_checks.py` | `--use-db` | `{header, a2, a3, b3, b5}` via one `_statements()` shared with `--emit-sql` |
| `import_log.py` | `--use-db` | a row list, via one `_statement()` shared with `--emit-sql` |

`--use-db` runs the **same statements** `--emit-sql` prints and builds the
**same dict** `--from-results` loads, so the two paths cannot drift into
disagreeing about what was measured. `state_checks` and `import_log` were
refactored so one function serves both; the F6 `_key()` defect
(`file:option_groups` never matching `Option Groups`, 73 windows sitting at WARN
while *looking* evaluated) was a mismatch of exactly that kind.

**Read-only is enforced three times**, not asserted once:
`set_session(readonly=True)`, `SET default_transaction_read_only = on`, and a
per-statement text guard refusing anything that is not a single
`SELECT`/`WITH`/`EXPLAIN`/`SHOW`. Three, because the first two are promises made
to the driver about a DSN whose privileges nobody here can inspect.

### Which steps need the database

| step | Postgres | evidence |
|---|---|---|
| `profiler/` | **no** | only writes on `--json`; no DB import anywhere |
| `ecatlib/` | **no** | 19 value primitives; no DB import anywhere |
| `mapping/mapper.py` | **no** | declarative mapping → CSV |
| `preflight` · `sandbox` · regression | **no** | filesystem and bytes |
| **B6** | **no** | file vs the PREVIOUS FILE |
| **B7** | **YES** | file vs LIVE STATE |
| **A1** | **YES** | file vs the ORG |

Four of six phases and the whole file-production path are container-ready with
no credential. **Only the gate needs Postgres, and only for its two strongest
checks.** Without it the run exits **10**, distinct from the exit **7** that
means a check found something wrong with the file.

### What is verified, and what is not

`psycopg2` is installed on **neither** interpreter and there is **no**
`DATABASE_URL`, so the `--use-db` code path cannot execute here. Untested
plumbing inside an upload gate is the exact failure mode this programme exists
to stop, so `acceptance/test_dbexec_wiring.py` substitutes a fake driver and
runs the real paths: **21 of 21 assertions pass.** It establishes that every
statement sent is a read, the session is opened read-only and closed, the
assembled dicts match the `--from-results` shapes, the downstream report
functions consume them, statement keys agree between `--emit-sql` banners and
`--use-db` dict keys, an unrecognised statement raises rather than being
skipped, and a missing DSN refuses loudly and names what is missing.

**NOT CHECKED, and it needs the credential:** that psycopg2 accepts these
strings, and that a replica DSN has the privileges. The SQL itself *is* verified
— it was run through the `supercat-postgres-vpn` MCP, which is how #7 and #8
were found.

`pip install psycopg2-binary` on `/opt/homebrew/bin/python3` is the one remaining
step before `--use-db` is live.

---

## Two more defects, both mine, both the same shape

### 10. `VERIFY` printed `PASS  regression bytes match` for clients with nothing pinned

`tcs` and `drf` have no `expect_bytes`. `phase_verify()` returned early with a
correct NOT CHECKED paragraph in the report — and `main()` then printed
`VERIFY  PASS  regression bytes match` on the summary line, because it treated
"did not raise" as "passed". A green line for a measurement that never happened,
which is BUILD_SPEC §3.4 in its purest form, written by the same session that
had just fixed two instances of it in someone else's code.

Fixed: `phase_verify()` returns `None` when nothing was compared — including the
case where every pinned name missed the produced set — and the summary line
reads `VERIFY  NOT CHECKED  no trusted bytes pinned for this client`.

### 11. B6 graded row loss on delete semantics alone, ignoring scale

`drf`'s run: 1,627 keys dropped of 1,627, 72 added, **0 rows shared**. B6 called
it a WARN, because `products.csv` soft-deletes and a soft delete is reversible.

Reversible is not the same as intended, and a 100% drop is not a large version
of a small one — it means the two files do not share a key space. Fixed to
BLOCK at ≥50% dropped regardless of delete semantics, and to say so explicitly
when zero rows are shared. **The 50% threshold is A1's own** (`pct_org < 50` is
already fatal there); two checks reading the same shape should not disagree
about whether it is serious. After the fix `drf` refuses at GATE with exit 7
instead of reporting exit 10 for want of a credential it did not need.

### And three wrong paths in my own registry

The first `clients.toml` assumed `Source Data/` and `Build/` for every client.
Measured:

| client | source | build |
|---|---|---|
| `libco` | **no `Source Data/` at all** — files loose in the client root | client root |
| `mali` | `03_Data/` (organised by phase: `00_Import_Files`, `01_Kickoff`, …) | `00_Import_Files/` |
| `tcs` | `Source Data/` | **`CS_eCat_Rebuild/`**, not `Build/` |
| `drf` | `Source Data/` | client root |

This is the KICKOFF's "three of six clients have no `Source Data/` folder"
arriving as a concrete failure. The assumption failed *loudly* for libco and
mali (PROFILE refused, exit 4) and **quietly** for tcs and drf — a missing build
directory means B6 has no previous file, which reports NOT CHECKED. Which is
precisely why the runner exits 10 on NOT CHECKED rather than 0.

### The `_v2` mapping preference is load-bearing, not tidiness

`required_check.py` over all 18 mapping files reports **1 unmapped required
field**, which contradicts the handoff's "no client has a required field lacking
a plausible source column". Located: it is `mappings/tcs/customers.toml` —
the **superseded v1** — whose `TerritoryCodes` has no declared default.
`customers_v2.toml` has one.

So the handoff's claim is true of the mappings in use and false of the tree,
because the superseded v1 files (`customers.toml`, `stories.toml`,
`options.toml`) are still sitting beside their replacements. `find_mapping()`
prefers `<target>_v2.toml` and prints which it chose; had it taken the
alphabetically-first or the shorter name, tcs would refuse at RESOLVE on a
mapping nobody intends to use. An empty `TerritoryCodes` imports clean and makes
the customer invisible to every rep in a "show only associated customers" group
— pebl sits at 171 of 171 blank on exactly that.

Worth either deleting the v1 files or marking them superseded in-file; a
`required_check` run that reports a real-looking failure against a dead mapping
is the "check with nothing to measure" pattern pointed the other way.

---

## Client findings from the first full run of all six

Every one of these is a B6 diff against the client's own previous file. **Whether
that previous file is what produced live state is unverified** for tcs, libco and
drf — B7 against live is the check that would settle it, and it needs the
credential. Read these as "the mapping's output differs from the file sitting in
the client folder", not yet as "this would damage the live org".

**`tcs` — GATE refused, exit 7.** 799 rows produced against 425 previous, and on
the 425 shared rows **18 columns blanked**, including:

```
RelatedItems         424 of 799      Price_MAP    424 of 799
Price_MSRP           424 of 799      OptionSet1   379 of 799
MarketingCopy        379 of 799      materials    379 of 799
dimensions           379 of 799      Warranty     379 of 799
```

Two whole price levels and the OptionSet axis. `PHASE2_COMPLETE.md` scores tcs
products at 8 columns exact / 71.5% of cells and calls only `stories` and
`customers` ready; this is that number expressed as what an upload would do.

**`libco` — GATE refused, exit 7.** `price_netprice` blanked on **822 of 897
rows** — the entire net-price column — plus `RelatedItems` on 202 and
`PromotionPrice` on 34. libco's mapping is class-2 (pre-mapped by the client's
sales team, validate-don't-transform), which makes a blanked price column the
most likely kind of defect there and the least likely to be noticed: it imports
clean.

**`drf` — GATE refused, exit 7.** B6 reproduced the documented zero-overlap
finding **independently and from the file alone**: 1,627 dropped, 72 added,
0 shared, "not a deletion, a different key space". The build is keyed
pattern × colourway (`ADELINA-UV-ASH`) and the source carries only the pattern
(`ADELINA-UV`). This is the fourth independent route to that finding and the
first that needs no database and no corpus.

**`mali` — exit 10.** Builds `customers.csv`; `00_Import_Files/` holds no
previous `customers.csv`, so B6 is NOT CHECKED. This is the case B7 exists for
and B7 needs the credential — and mali is the client B7 was calibrated on
(`BillToAddress1` on 21.3% of rows where live holds 100%, every customer on a
LIST price code where live has dealer-net). The gate correctly refuses to guess.

**`leg`, `mer` — exit 10.** Byte-identical, B6 clean, B7 and A1 emitted only.

---

## Verification, in numbers

```
leg  products.csv    404,798 bytes   BYTE-IDENTICAL (sha256)   1,020 rows
leg  inventory.csv    35,067 bytes   BYTE-IDENTICAL (sha256)   1,194 rows
mer  products.csv     40,995 bytes   BYTE-IDENTICAL (sha256)     102 rows

B6  leg products : 1,020 of 1,020 compared, 0 blanked, 0 dropped, 0 changed
B7  leg products : 7 of 41 columns density-evaluated (34 have no live
                   counterpart, each named), 10 of 50 sampled keys spot-checked,
                   0 of 10 disagree on all 7 columns.  VERDICT PASS
A1  mer -> mer   : 102 file keys, 102 live, 102 matched, 0 would be deleted,
                   rival scan: mer 100.0%.  VERDICT PASS, exit 0
A1  mer -> leg   : 0 of 102 matched, 1,020 of 1,020 would be SOFT-DELETED,
                   rival scan says the file belongs to mer.
                   2 BLOCKING, VERDICT DO NOT UPLOAD, exit 1
                   — the 2026-08-18 shape, caught

sabotage: 5 of 5 phases refused at the right phase with a distinct exit code
          inputs 3 | mapping 5 | build 6 | gate 7 | regression 8
clients:  6 of 6 run end to end
          leg 10 | mer 10 | tcs 7 | libco 7 | drf 7 | mali 10
          0 of 6 exit 0 — and every refusal is correct: two need the
          credential, three found real B6 findings, one has no previous file
guard:    dbexec read-only guard 11 of 11 cases; --use-db wiring 21 of 21
tree:     131 porcelain lines before and after; 0 tracked modifications
          ground-truth/ mtimes unchanged — read, never written
```

`stories.csv` was deliberately **not** pinned and leg has no stories mapping:
`fix_stories_encoding.py` post-processes the committed file, so byte-identity
would mean reproducing the post-process rather than the build.

## Scope limits, stated

- **Coverage of the tree guard**: image and binary extensions are not hashed
  (Legrand's `Build/` holds ~1 GB of images). Count reported every run. A write
  to a `.jpg` would be caught by `git status` and not by the manifest.
- **B7 stage-1 columns**: 7 of 41 for leg products. The other 34 have no live
  counterpart mapped, each named. That is a real limit on what B7 can see —
  `Price_dn`, `Price_retail`, `Finish`, `CollectionCodes` and 30 more are
  unmeasured.
- **The option stack is not gated.** `preupload_check` keys on one produced
  file; an `option_stack` emits two importer files plus an intermediate. The
  runner reports it NOT CHECKED rather than passed, and `tcs`'s registry entry
  deliberately omits `options` — 0 of 379 products have identical option
  availability and there are 1,561 EXTRA offers.
- **No client reaches exit 0**, and that is the honest state rather than a
  failure of the runner. `leg` and `mer` are byte-identical and blocked only on
  the credential; `tcs`, `libco` and `drf` have real B6 findings; `mali` has no
  previous file. Nothing here is ready to upload today.
- **The previous-file provenance is unverified** for `tcs`, `libco` and `drf`.
  Their build directories hold `.bak`, `.bak2` and `_audit_fix` variants
  alongside the file B6 diffed against, and nothing in the folder says which one
  produced live state — the mali problem from KICKOFF §"folder mode", in a
  different folder. B7 against live is what settles it.
- **`b7_lossy.py`, `preupload_check.py` and `severity.py` are untracked in git**
  (never committed — 09-09 work). Edits to them have no git baseline to diff
  against, so the equivalence of the `--emit-sql` refactors was verified by
  running a reverted copy side by side instead: 9 of 9 variants byte-identical.
