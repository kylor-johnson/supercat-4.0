# `runner/` — agent 1, one command

```bash
/opt/homebrew/bin/python3 runner/run_ingestion.py --client leg
/opt/homebrew/bin/python3 runner/run_ingestion.py --list
```

A client folder in; eCat files, a report and an upload proposal out. Nothing
uploads, ever — the runner produces files and a verdict, and a human decides.

**Pin the interpreter.** `/opt/homebrew/bin/python3` (3.14.2) is the only one on
this machine that has both `tomllib` and `openpyxl`. `/usr/bin/python3` is 3.9.6:
it has `openpyxl` and no `tomllib`, so `mapper.py` will not import. Preflight
checks this and refuses rather than failing later with a confusing error.

```
runner/
  run_ingestion.py   the entrypoint — six phases, exit codes, the report
  preflight.py       interpreter · iCloud dataless placeholders · declared inputs
  sandbox.py         input staging + the client-tree write guard
  clients.toml       the client registry (DATA: folder names, build dirs, org ids)
```

## The six phases

| | phase | what refuses it | database |
|---|---|---|---|
| 1 | `PREFLIGHT` | wrong interpreter, an iCloud placeholder, a missing input | no |
| 2 | `PROFILE` | the source folder cannot be read | no |
| 3 | `RESOLVE` | no mapping, an unmapped required field, org_id mismatch | no |
| 4 | `BUILD` | a mapping cannot be evaluated | no |
| 5 | `GATE` | B6 blanking · B7 lossy · A1 wrong org | **B7 and A1 yes** |
| 6 | `VERIFY` | produced bytes ≠ the trusted file; then the tree guard | no |

Phases 5 and 6 are independent and both run even if the other refuses — the
regression check needs no credential and its answer is worth having on a run the
gate stopped.

## Exit codes — one meaning each

```
 0  PASS. Every phase EVALUATED. Upload proposal in the report.
 1  internal error (a bug in the runner, not a finding about the client)
 2  usage / registry error — unknown client, no mapping directory
 3  PREFLIGHT failed   environment or inputs
 4  PROFILE failed     the source folder could not be read
 5  MAPPING refused    cannot map, and it names what
 6  BUILD failed       a mapping could not be evaluated
 7  GATE refused       a FINDING. Something is wrong with the FILE.
 8  REGRESSION failed  produced bytes != the trusted file
 9  CLIENT TREE MODIFIED   overrides every other code
10  GATE NOT EVALUATED needs Postgres and had none. An OPS problem, not a
                       data one — nothing is known to be wrong with the file,
                       and nothing is known to be right either.
```

**7 and 10 are deliberately different numbers.** A cron that cannot tell "the
file is wrong" from "I had no credential" pages the wrong person.

## What needs the database, and what does not

Measured, not assumed:

| step | Postgres | why |
|---|---|---|
| `profiler/` (phase 2) | **no** | reads files, reports. Never connects. |
| `ecatlib/` (phase 3–4) | **no** | transforms values. Never connects. |
| `mapping/mapper.py` (phase 4) | **no** | declarative mapping → CSV |
| `preflight` / `sandbox` / `VERIFY` | **no** | filesystem and bytes |
| **B6** regeneration diff | **no** | file vs the PREVIOUS FILE |
| **B7** lossy-regeneration gate | **YES** | file vs LIVE STATE |
| **A1** org fingerprint | **YES** | file vs the ORG |

Four of six phases and the entire file-production path are container-ready with
no credential at all. Only the two strongest gate checks need Postgres.

**Three ways to satisfy them, in order of preference for a container:**

1. `--use-db` with a read-only `DATABASE_URL`. Added 2026-09-09 to
   `a1_fingerprint`, `b7_lossy`, `import_log` and `state_checks` via
   `acceptance/dbexec.py`. Needs `psycopg2`, which is installed on **neither**
   interpreter here — `pip install psycopg2-binary` first.
2. The MCP round trip: the gate writes `b7_<org>_<type>.sql`; run it read-only
   through `supercat-postgres-vpn`, then feed the rows back with
   `--from-results`.
3. Neither → the run exits **10** and says the credential is what is missing.

Read-only is enforced three times in `dbexec`: `set_session(readonly=True)`,
`SET default_transaction_read_only = on`, and a per-statement text guard that
refuses anything that is not a single `SELECT`/`WITH`. Three because the first
two are promises about a DSN whose privileges nobody here can inspect.

## The client tree is never written to

Two defences, because one is an argument and the other is a measurement.

**Structural.** The runner never executes a script from a client tree. It drives
`mapping/mapper.py`, which takes its output path as an argument. Every input a
mapping declares is **copied** into a sandbox and chmod'd `r--`, and the build is
pointed at the sandbox root — so during a build the client tree is not merely
unwritten, it is not referenced.

`build_ecat_files.py:31` sets `OUTPUT_DIR` from `__file__` and takes no
arguments at all, so anything invoking it in place writes into
`Legrand/Build/`. It is not invoked, imported, patched or read by this runner.

**Empirical.** `sandbox.TreeGuard` fingerprints the client tree (sha256 + size
per file, image/binary extensions excluded and counted) and reads
`git status --porcelain`, before and after. Any change fails the run with exit 9.
The 09-09 incident was a session that would have passed the structural argument
on inspection — it believed it was calling the mapping layer — so the argument
alone is not enough.

## Proving it refuses

`--break-phase` sabotages exactly one phase, in the sandbox only, and never
touches `mappings/` or a client tree. Verified 2026-09-09 on `leg`:

```
--break-phase inputs      -> PREFLIGHT  refused, exit 3
--break-phase mapping     -> RESOLVE    refused, exit 5  ("baseitemcode is ABSENT")
--break-phase build       -> BUILD      refused, exit 6
--break-phase gate        -> GATE       refused, exit 7  (B6: LongDesc blanked 1020/1020)
--break-phase regression  -> REGRESSION refused, exit 8  (404,817 vs 404,798)
```

Every one reported `TREE CLEAN`.

## The registry

`clients.toml` carries the three things a mapping cannot: which directory the
client's folder is, which subdirectory holds its trusted output, and the org id.
None are derivable —

- the org is `leg`, the folder is `Legrand`, the mapping dir is `legrand`;
- Legrand's outputs live in `Build/`, 111Mercer's in `Import Files/`;
- two orgs are named "legrand" (live `leg` id 273; `lna` id 93 is a dead 2015
  org), so `org_id` is pinned here and cross-checked against the mapping's own.

`expect_bytes` is the regression contract. `stories.csv` is deliberately absent:
`fix_stories_encoding.py` post-processes the committed file, so pinning it would
encode a post-process the mapping does not perform.

## Adding a client

1. Add a `[clients.<shortname>]` block: `client_dir`, `build_dir`, `mapping_dir`,
   `org_id`, `targets`.
2. `targets` lists only slots that have a mapping. **An absent mapping means an
   absent file, not an empty one** — three of the six file types HARD-delete, so
   emitting an empty `customers.csv` deletes every customer and every ship-to.
   The runner prints what it is NOT producing for exactly this reason.
3. Run it. A new client with no previous build has nothing for B6 to diff, so
   the gate reports NOT CHECKED and exits 10 — correctly. B7 against live state
   is the check designed for that case, and it needs the database.
