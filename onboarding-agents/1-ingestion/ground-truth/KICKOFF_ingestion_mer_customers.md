# Kickoff — net-new source test: 111 Mercer customer list

Paste this into a **fresh** Cursor / Claude Code session with the
`SuperCat.code-workspace` open (ops repo `~/repos/supercat-4.0`). VPN up.
Self-contained. One pass.

This is a **blind test of the ingestion layer**, not a client-build session.
A human will review only your report. Do not ask clarifying questions you can
answer by reading a file or running a tool.

---

## Why this test exists

Phase 0 (`profiler/`) and the ingestion runner (`runner/run_ingestion.py`) were
built so a new file from a client is **profiled before anyone writes a mapping
or a CSV**. The expensive question is never "how do I parse this column." It is
"what is this, which eCat file is it trying to be, and what is missing."

A net-new workbook just landed in a live client's `Source Data/` folder. That
is the case the profiler was built for. This session is the first time a fresh
agent, with no prior context on this file, has been pointed at it.

---

## Workspace and paths — do not mix these up

| what | where |
|---|---|
| **Work here** | `~/repos/supercat-4.0` (git working tree) |
| Ingestion agent | `onboarding-agents/1-ingestion/profiler/` · `onboarding-agents/1-ingestion/runner/` · `onboarding-agents/1-ingestion/mappings/` |
| Live client files | iCloud `SuperCat_Simple_Final/02_Implementation/<Client Name>/` (full names) |
| This client's folder | `…/02_Implementation/111Mercer/` |
| **Do not build from** | iCloud `SuperCat 4.0/eCat_Onboarding/` — pointers + a 2026-09-03 archive. Not the implementation tree. Not the agent. |

Org: **111Mercer**, shortname **`mer`**, org_id **302**. Pin all three. Two orgs
have been named "legrand"; nothing in a CSV says which org it belongs to.
Confirm `organizations.shortname = 'mer'` AND `id = 302` before treating any
live number as this client's.

Interpreter (mandatory):

```bash
/opt/homebrew/bin/python3
```

`/usr/bin/python3` is 3.9.6 and cannot import `tomllib`. Preflight exists
because this has already wasted sessions.

---

## Read first, in this order, then stop reading

| file | why |
|---|---|
| `onboarding-agents/1-ingestion/profiler/SKILL.md` | the interface. Two modes, folder first. The rules the report must obey. |
| `onboarding-agents/1-ingestion/profiler/REVIEW_LOG.md` | bugs found *by the data*. The shapes you will hit again. |
| `onboarding-agents/1-ingestion/ground-truth/KICKOFF_ingestion.md` | why profile-before-transform, the three input classes, the traps. |
| `.cursor/skills/ecat-customers-build/SKILL.md` | `customers.csv` required fields, HARD-delete, ship-to rule, DefaultPriceCode. |
| `.cursor/skills/ecat-postgres-audit/SKILL.md` | how to read live org state. Read-only. |
| `onboarding-agents/1-ingestion/runner/clients.toml` `[clients.mer]` | what mer is already registered to produce. Read it before assuming the runner will ingest this file. |
| `onboarding-agents/1-ingestion/mappings/mercer/products.toml` (header comments only) | mer already has a **products** mapping from a NetSuite item export. This new file is not that. |

Do **not** read frozen `_museums/`, do not read `eCat_Onboarding/_ARCHIVE_*`,
do not open Insightful 2.0/3.0. Do not re-read the whole SCORECARD unless a
profiler rule cites a specific section.

Always-on rules already loaded: `ecat-ground-truth`, `ecat-import-ops`,
`ecat-data-model`. Jira is read-only. Write nothing to Postgres or Admin.

---

## The source

```
…/02_Implementation/111Mercer/Source Data/111 Mercer Customer List(Sheet1).xlsx
```

It arrived in a folder that already holds other files. **Folder mode first,
always.** File mode on the wrong file is wasted work.

You are allowed to look at the rest of `111Mercer/` for context (BUILD_NOTES,
existing `Import Files/`, the NetSuite item export) so you do not confuse this
workbook with the products build. Those files are context. They are not this
file.

---

## What you are testing

The existing ingestion tools, driven by you:

1. **`profiler/folder_mode.py`** on the whole `111Mercer/Source Data/` folder.
2. **`profiler/file_mode.py`** on the customer workbook (and only that file in
   file mode).
3. A **live-org reconcile** (read-only Postgres) for the things the file cannot
   decide: org identity, existing customer count, Admin price-level **codes**.
4. A written verdict: proposed source → eCat mapping **with confidence**,
   every unmapped required field **named with a reason**, and whether a
   `customers.csv` may be produced.

The tools are the system under test. Run them. Quote them. Then say where the
tool output is incomplete, wrong, or silent — with a specimen. A hand-rolled
pandas profile that never invoked `folder_mode.py` / `file_mode.py` is not this
test; it is a bypass.

---

## What you are not doing

- **No `customers.csv`.** mer has no customers mapping. An absent mapping means
  an absent file, not an empty one. `customers.csv` HARD-deletes every customer
  and every ship-to on a clean import. Emitting a partial file is the incident
  this layer exists to prevent.
- **Do not add `customers` to `runner/clients.toml`.** Do not write
  `mappings/mercer/customers.toml`. The agent proposes a mapping and flags what
  it cannot map. It does not write transform code, and it does not register a
  target that would HARD-delete.
- **Do not treat `run_ingestion.py --client mer` as the test of this workbook.**
  That registry entry builds **products** from `111Mercer-ItemExport .csv`.
  Running it is allowed only as a *negative* check: PROFILE should notice the
  new file, BUILD must still be products, TREE must stay CLEAN. A products
  PASS is not a customers ingest.
- **No upload. No Admin write. No FTP. No Jira write.**
- **No writes into `02_Implementation/111Mercer/`.** Report goes under
  `onboarding-agents/1-ingestion/` only (path below). If you run the runner, it sandboxes
  itself; do not copy its output into the client tree.
- **Do not "fix" filenames, sheet names, or nbsp in the source.** Profile what
  arrived.

---

## Procedure (run in order; verify between steps)

### 0 — Confirm the file is actually on disk

iCloud dataless placeholders look like real files to `ls` (full size, no
`*.icloud` name). The flag is `SF_DATALESS`. If the workbook will not open,
that is a preflight finding, not a parse bug. Name it and stop that path;
continue with everything else.

### 1 — Folder mode

```bash
cd ~/repos/supercat-4.0/onboarding-agents/1-ingestion/profiler
/opt/homebrew/bin/python3 folder_mode.py \
  "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/111Mercer/Source Data"
```

Capture the full stdout into the report. Then answer, from that output plus
what you verify:

- Which files are catalog source vs template/derived vs noise
- Which eCat target each candidate is trying to be
- How the new workbook **relates** to the item export already in the folder
  (rival / superseded / complementary / mapping-pair / key-linked / format
  twins / unrelated). Use the taxonomy in `profiler/SKILL.md`. Do not call two
  different eCat targets "duplicates."
- What eCat file types are still missing from the folder entirely

### 2 — File mode on the workbook

```bash
/opt/homebrew/bin/python3 file_mode.py \
  "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/111Mercer/Source Data/111 Mercer Customer List(Sheet1).xlsx"
```

Capture the full stdout. Then walk the six questions the tool claims to
answer, and **check the tool**:

1. What is this — format vs extension, sheet(s) profiled vs not, where the
   header is, row/column counts
2. What's populated — fill rate; a column at ~2% is not a field
3. What looks like a key — and whether uniqueness matches **customer** key
   semantics (bill-to plus ship-to continuation rows *may* repeat a code)
4. What maps to eCat — every proposal **with confidence**. A false certain is
   worse than an honest moderate. Scope exact-name matches to the detected
   target (`Name` is an options.csv field; it is not automatically BillToName)
5. What's missing — every importer-required `customers.csv` field with no
   plausible source, each with a reason
6. What doesn't add up — internal contradictions, with a specimen each

**Every count ships with a specimen.** A fill rate, a duplicate, a "blank"
row, a mapped field, a missing field — each needs at least one example from
the file. If you cannot produce the specimen, the count is not reportable.

**Whitespace that is not empty is a measurement.** If a cell is populated
according to the tool but the specimen is `\\xa0`, NBSP, or a placeholder
phrase, say so. Do not call that a value.

**Partitions must sum.** If you break rows into "real / empty / other", the
parts are counted separately and add back to the sheet's row count.

### 3 — Live org (read-only), because the file cannot settle these

Via `supercat-postgres-vpn`, scoped to org 302 / `mer`:

- Confirm shortname + id.
- Customer count and shipping-location count (join `shipping_locations` through
  `customers`; `shipping_locations` has `customer_id`, not `organization_id`).
- `price_levels.code` and `price_levels.name` — these are different columns.
  `DefaultPriceCode` must match the **code**. Report both. Do not assume a
  source value that looks like a display name is the code, and do not assume
  it isn't, until you have compared them.
- Whether any `customers` import_events exist.

A first-ever customer file against **zero** live customers is the case B6
cannot see (no previous file) and B7 exists for. You will not run B7 in this
session. You will **say** that, rather than treating "no previous file" as
clearance to build.

### 4 — Mapping proposal (data, not code)

For each source column: eCat field or `unmapped`, confidence, why, fill rate,
specimen. Then the required-field gap table. Then the questions only the
client can answer — flagged, not guessed.

If two source columns could feed the same eCat field, name both and do not
pick. If a mapping would require splitting or stripping, that is a transform:
propose it, do not implement it.

Input class: raw ERP / pre-mapped / hybrid / industry template. Detect by
testing headers against known eCat names. Headers that are already
`BillToCode` / `BillToName` are class 2 and must not be re-mapped.

### 5 — Verdict

One of:

- **REFUSE TO BUILD** — required source is absent; name it. This is a passing
  outcome for the agent if the refusal is specific.
- **VALIDATE ONLY** — file is already eCat-shaped; do not transform.
- **MAP, BUT NOT YET** — mapping is proposable, gaps remain; list the minimum
  client ask that would unblock a `customers.csv`.

State the HARD-delete consequence in one sentence so a later session cannot
"just generate the file."

---

## Output (this is the deliverable)

Write **one** report:

```
onboarding-agents/1-ingestion/profiler/RUN_2026-09-16_mer_customers.txt
```

Plain text, same general shape as `profiler/RUN_2026-09-04_file_mode_four_tests.txt`:
tool stdout captured, then your interpretation, then the verdict.

Also put a short chat summary on top of the same facts: target, input class,
row count (with specimen of what you excluded), required-field gaps, live
customer count, verdict. No adjectives that are not measurements.

In chat, additionally list **tool defects** (if any) separately from **file
findings**. Mixing them is how a profiler bug becomes a client report.

---

## Definition of done

- Folder mode ran on `Source Data/`, file mode ran on the xlsx, both with
  `/opt/homebrew/bin/python3`, neither crashed.
- The report exists at the path above.
- Every numeric claim has a specimen.
- Every importer-required customers field is either mapped (with confidence)
  or listed as missing (with reason).
- Live `mer` / 302 customer count and price-level codes were read, not
  remembered.
- `02_Implementation/111Mercer/` is byte-for-byte unchanged (`git status` /
  a before-after listing).
- No `customers.csv` was written anywhere that a human might upload.
- No mapping TOML was added under `mappings/mercer/`.

A session that produces a plausible `customers.csv` from this file has
**failed the test**, even if the CSV looks neat.

---

## Traps already paid for (do not rediscover by breaking data)

- Route on magic bytes, not the extension. XLSX named `.csv` is a ZIP.
- Take the most populated worksheet, not sheet 1, and **name the sheets you
  did not profile**.
- mtime in this tree is worthless (bulk merge stamped almost everything
  2026-09-03).
- `products.csv` soft-deletes; `customers.csv` HARD-deletes. Deletes only run
  on a warnings-only import.
- Confirm the target org. Legrand's 1,020-row products.csv was imported into
  **this** org on 2026-08-18 and soft-deleted all 102 of its products. The
  file that did it is still in `111Mercer/Import Files/`.
- A clean import proves the file parsed and nothing else.
- `TerritoryCodes` is KB-required and **not** importer-fatal; it is still
  required for reps in a "show only associated customers" group.
- A customer with zero ship-to rows is destroyed with an error — every
  customer needs at least its own address as the first ship-to.
- Measurement ≠ consequence. Fill rate is a measurement. "Reps will see X"
  is a consequence and needs a separate proof.

---

## Out of scope

- Building or repairing `products.csv` / `inventory.csv` for mer
- Phase 1 library work, Phase 2 mapping-engine work, Phase 3 acceptance
- Config-check, correspondence, session-prep
- Asking Ryan or Jen anything in this session — write the questions in the
  report; do not draft the email unless the verdict section needs the
  exact ask listed
