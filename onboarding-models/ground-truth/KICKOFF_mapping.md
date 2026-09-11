# Kickoff — Phase 2, the mapping layer

Paste this into a fresh Claude Code session in the **SuperCat 4.0** workspace, VPN up.
Self-contained.

**Scope: Phase 2 only — the mapping layer.** Phase 0 (profiler) and Phase 1 (shared
library) are DONE; do not rebuild them. Phase 3 (acceptance harness) is built and in
repair; do not touch it.

`KICKOFF_ingestion.md` is the wrong door for this work — it is scoped to Phases 0 and 1
and says explicitly *"Do not attempt Phases 2–3."* Both of its phases have since passed
their own definitions of done. This file replaces it for what comes next.

---

## Read first

| file | why |
|---|---|
| `ground-truth/BUILD_SPEC.md` | §2 = the shared-library boundary and the DIALECT problem. §3 = the acceptance criteria your output must survive. This is the spec. |
| `ecatlib/README.md` | what Phase 1 actually built, what it deliberately did not, and the two suspicions it resolved differently |
| `profiler/SKILL.md` | what Phase 0 produces — this is your input |
| `ground-truth/SESSION_HANDOFF.md` § Things that will bite you | the traps, including three column pairs that look like one answer |
| `ground-truth/SCORECARD.md` §§ 8–12 | the incidents behind every rule. **§12 is retractions — two findings were wrong** |

Canonical implementation tree is **`SuperCat_Simple_Final/02_Implementation/<Client Name>/`**
(full names, not shortnames). `SuperCat 4.0/eCat_Onboarding/` is archived — do not build
from it.

---

## The one sentence this phase exists for

**Nothing currently turns a client's source file into `products.csv`.**

Phase 0 tells you what a source folder contains. Phase 1 gives you the twelve primitives
that transform a value once you know what it is. Between them sits the thing that has been
written sixty times by hand and never once shared: the statement of *which source column
feeds which eCat field, and through which transform.*

---

## The load-bearing division, and it is the whole point

> **The agent proposes the mapping and flags what it cannot map.
> The agent does not write transform code.**

Today a build produces **a script**, which is why there are sixty of them and a long tail
of `fix_*.py`, `repair_*.py`, `exact_fixes.py`. The target is a build producing **a
mapping**, with the code shared.

Every time you are tempted to emit Python for a client, that is the signal that either
(a) a primitive is missing from `ecatlib` and should be added there, or (b) the source
genuinely needs a bespoke loader, which is a named and budgeted category — see
§ *The escape hatch is budgeted*.

---

## State of play — what already exists, verified

### Phase 0: `profiler/` — DONE

Two modes, folder first. `folder_mode.py` answers *which of these files is the one*;
`file_mode.py` answers *what is in it and what does it map to*. Its four-file
definition-of-done passes: it detects a file named `.csv` whose content is xlsx, finds a
header at row 7 behind six banner rows, names the sheets it did **not** profile, and
reports that two columns are unique so only the client can say which is the key.

**This is your input.** `file_mode.py` already emits a proposed source-column → eCat-field
mapping with a confidence per field. Phase 2 consumes that; it does not re-derive it.

Read `profiler/REVIEW_LOG.md` before trusting any of it — six bugs were found *by the
data*, and two of them are the shape you will hit again: *a false certain is worse than an
honest moderate*, and *per-division files merge, they never compete*.

### Phase 1: `ecatlib/` — DONE, acceptance test passing

Seventeen primitives delegated. Legrand's `products.csv` — 1,020 rows, live in production,
produced by a 1,537-line script — rebuilt through the library and **byte-identical**
(404,798 bytes). `inventory.csv` likewise. A mutation test proves the acceptance test can
go red: changing `parse_money` from 2dp to 3dp fails it.

### Phase 3: `acceptance/` — built, in repair

Nine of ten §3 criteria shipped. Do not touch it; another session is working on it. What
matters to you is §3 itself, which is the standard your output has to pass.

---

## The DIALECT problem — read this before merging anything

BUILD_SPEC §2 reads as though extraction were mechanical: twelve primitives, three
reimplementations, merge them. **It is not.** The three builds disagree on *output*, not
merely on style:

| primitive | Legrand | libco | tcs |
|---|---|---|---|
| money | `4058.00` — always 2dp | `4058` — integer dollars drop the `.00` | passthrough after stripping `$` and `,` |
| boolean | `Y` / `""` | `Yes` / `No` | — |
| weight | unit-aware; `500 g` → `1.102311` | first number found; `500 g` → `500` | — |
| dimensions | `3.5 in H x 2 in W x 1 in L`, `N/A` when empty | — | `18.75"H x 10.5"W`, `""` when empty |

**A naive merge silently rewrites three clients' files.** So every divergent primitive
takes an explicit `dialect`, selected per client **in config and never inferred**.
`values.LEGRAND` is byte-exact with `build_ecat_files.py`, which is the only reason the
acceptance test is possible at all.

The same holds at finer grain: Legrand's `clean_category` does *not* null-map (a literal
`"0"` category stays `"0"`) while `normalize_finish` does. Same primitive, different null
policy, so the policy is a parameter — `clean_lookup(..., null_tokens=...)`.

**Therefore the mapping format must carry the dialect explicitly.** A mapping that says
"money" without saying "which money" is not a mapping; it is a coin flip across three
clients' live files.

*(Divergence is also evidence. Comparing the dialects surfaced a live defect — libco
normalises booleans to `Yes`/`No` while eCat boolean filters match `Y`/`y`/`T`/`t`/1–9.
See `OPEN_ITEMS A5`. Note the standing caveat: whether eCat's matcher is first-character
or exact has **not** been settled from the product side. `Rating` — registered binary,
907 values of `Damp`/`Dry` — is unambiguous; the `Yes`/`No` three are not.)*

---

## The three input classes — detect which, they need different handling

| class | seen at | what to do |
|---|---|---|
| **1 · raw ERP export** | `mer` (NetSuite, 56 cols: Internal ID, Display Name, Primary Units Type), `drf`'s binary-encoded customer listing | map it |
| **2 · pre-mapped by a human** | `libco` (whole set, mapped by sales), `drf` customers (`BillToCode`, `TerritoryCodes`) | **validate, do not transform** |
| **3 · industry / third-party template** | `tcd` ("LightsAmerica Data Template", "KANOVA-Data") | map, but the template is the contract |

**Class 2 is the one that gets this wrong.** A file whose headers are already
`BaseItemCode` / `BillToCode` has had its mapping done by a human. Re-mapping it means
overriding a decision someone already made, usually silently, usually wrongly. The job on
a class-2 file is **checking** the existing mapping — fill rates, value shapes, required
fields — and reporting where the human's mapping disagrees with what eCat will accept.
Detect the class by testing headers against known eCat field names before anything else.

**Watch for hybrids.** `drf`'s "Characteristics … eCat MAPPED" carries eCat headers *and*
client-domain columns (`Origin`, `Content`, `CleaningCode`, `Direction`) side by side.
libco's spec master has a column literally named `?????` plus `Custom1`–`Custom5`.

---

## Phase 2's acceptance test — the direct analogue of Phase 1's

Phase 1 earned trust by reproducing a build that was already trusted. Phase 2 must do the
same thing one level up, or it produces **mapping file #61**.

> **Discard Legrand's 1,537-line `build_ecat_files.py` entirely. Express what it does as a
> declarative mapping. Regenerate `products.csv` through `ecatlib` driven by that mapping
> alone. Diff against `02_Implementation/Legrand/Build/products.csv`.**
>
> **Done = byte-identical, or every single difference explained and accepted.**

This is not a formality and it is not optional. Legrand is the hardest case in the set —
four separate price files merged by region × brand, a carry-forward rule, a non-null-mapping
category cleaner — and a mapping format that cannot express Legrand is a format that will
be abandoned at the first real client.

Two things that make the test honest, both already established in Phase 1 and worth
repeating:

- **Confirm the baseline reproduces first.** Run the unmodified script against current
  source and confirm byte-identity with the committed file *before* changing anything.
  Otherwise a diff is measuring source drift and is unattributable.
- **Prove the test can go red.** Mutate one mapping entry — a dialect, a column
  assignment — and confirm the diff fails. A green test that cannot go red proves nothing.

`stories.csv` is **not** a valid target: the committed artifact is post-processed by
`fix_stories_encoding.py` to repair mojibake, so it differs from generator output and the
unpatched original differs from it too. Acceptance is `products.csv` + `inventory.csv`.

---

## The escape hatch is budgeted, or it becomes the sixty scripts renamed

A declarative mapping needs a code escape hatch for the genuinely bespoke. Unbudgeted, the
hatch *is* the script, and Phase 2 has achieved a rename.

**Two separate categories, and only one of them is budgeted.**

**Per-field custom transforms — budget 3 per client.** A field whose transform cannot be
expressed as `primitive + dialect + parameters`. Beyond three, stop: **that is evidence the
library is missing a primitive.** File it against `ecatlib`, add it there, and the next
client gets it free. Never fork the primitive into a client's mapping.

*The budget is not arbitrary.* BUILD_SPEC §2's "genuinely client-specific" list, across the
three largest builds, is: Legrand 2 (`load_us_radiant_prices`, `load_ca_adorne_prices`),
libco 2 (`load_spec_master`, `apply_discontinued_promo`), tcs 3 (`stage2_lantern_rebuild`,
`stage4_parts_and_kits`, `sku_ignition`). Three is the observed ceiling, not a guess.

**Bespoke source loaders — named, not budgeted.** Legrand's four price files merged by
region × brand, tcs's buildable SKUs, libco's spec master. These are legitimately
client-specific: they answer *how do I assemble the input*, not *how do I transform a
value*. They sit outside the mapping, are named in it, and do not count against the budget.

**The rule that separates them:** if it touches a single field's value, it is a transform
and it is budgeted. If it decides which rows and files exist at all, it is a loader.

---

## Carry-forward survives into the mapping layer

`load_carryforward` exists in exactly one of the sixty scripts and encodes a rule that
applies to all of them:

> **When regenerating a file, values the generator cannot derive must be carried forward by
> key, or regeneration silently destroys them.**

The two that matter:

- **`Hideable`** — set by hand in Admin. Nothing in the source knows about it.
- **`ImageFileName`** — for images uploaded *after* the last build.

It has already cost Legrand **19 products' live images** once. `products.csv` soft-deletes
omitted rows on a clean import, so a regeneration that blanks a column looks like a
successful import.

**A mapping layer is exactly where this recurs**, because a mapping describes
source → target and carry-forward has no source. So:

- The mapping format must have a first-class **`carry_forward`** declaration per field —
  not a footnote, not a post-step someone remembers.
- `ecatlib.carryforward.load_carryforward` returns `(dict, warning)` and **must never be
  called with its warning discarded.** The original bug was a bare relative path resolving
  against the working directory, returning a silent `{}` and carrying nothing forward.
- Pass absolute paths. Always.
- `ecatlib.carryforward.diff_against_previous` implements BUILD_SPEC B6 and counts
  **blanked** columns separately, because blanking is the dangerous direction. Run it on
  every regeneration and read the blanked count before uploading anything.

---

## Two clients, two different jobs

| org | role | why it is the right one |
|---|---|---|
| **`leg`** Legrand | **regression test** | current build, live in production, byte-identical baseline exists. If the mapping cannot reproduce it, the mapping is wrong. |
| **`mer`** 111Mercer | **new-client test** | class-1 raw NetSuite export, live build, 102 products. Nothing has been mapped yet, so it tests the thing Phase 2 exists for. |

`mer`'s source is `111Mercer/Source Data/111Mercer-ItemExport .csv` — note the numbered
price columns (`1. Tempaper.com Price`) and the **leading space in the filename**.
`mer` is a Tempaper brand, not a standalone company; all three client users are
`@tempaper.com`, so a domain that looks like a placeholder against the org *name* is
correct — see `config_intent.toml § mer`.

Historical sources for clients already live have little value: the transform worked, they
shipped. Priority is current builds only.

---

## Your output has to survive §3 — read it as the target, not as someone else's problem

The acceptance harness runs **after** import and will be pointed at whatever you produce.
The four that bear directly on mapping:

- **A1 · org fingerprint.** Confirm the target org before any upload. **This is not
  theoretical:** Legrand's 1,020-row `products.csv` was imported into 111Mercer on
  2026-08-18, soft-deleting all 102 of their products. Second occurrence of that failure
  mode (`leg` → `mali` previously). Both times the file was valid and the import was clean;
  the org was wrong, and nothing in the file says which org it belongs to. **Mapping
  produces a file, the file gets uploaded, and that upload is where this happens.** Run
  `acceptance/a1_fingerprint.py` before every upload, not after.
- **B1b · registered custom fields.** A column in the file that is not registered in Admin
  is silently dropped by the importer. Populated + unregistered = data discarded on every
  import. The mapping must emit the registration list alongside the file.
- **B5 · inventory display.** Which quantity field the app shows is configured in
  `custom_fields.alias`, and **both `qty_available` and `qty_on_hand` run live across the
  fleet.** Read it, never assume — assuming it is what produced SCORECARD §12 R1, which
  reached a client and was false.
- **B6 · carry-forward.** Above.

And the rule underneath all of them, confirmed independently on three clients:

> **A clean import proves the file parsed. It proves nothing about whether it was right.**

`drf` ran 18 days of images at clean tier with doubled `.jpg.jpg` extensions that could
never match. `mali` ran 86 consecutive clean image imports with ~200 wrong photos. `leg`
ran nine clean imports while 13 announced filter fields sat empty.

---

## Inbound files arrive by email, and the spec does not describe this

**Found 2026-09-05, not previously documented anywhere.**

Client source files reach SuperCat as **email attachments**, recorded in
`active_storage_blobs` (97 rows, 88 of them `.csv`/`.xls`/`.xlsx`/`.txt`/`.zip`) via
`active_storage_attachments` with `record_type = 'InboundEmail'`.

For `leg`, every day including weekends, 2026-08-20 → 09-04:

```
LegrandAdorneInventory.xlsx    ~51 KB   one per day
LegrandRadiantInventory.xlsx   ~65 KB   one per day
                                        -> ONE leg Inventory import event per day
```

Two files in, one import slot out. That is `OPEN_ITEMS A8` — *"two inventory files overwrite
each other daily"* — visible by filename, which is the mechanism A8 never had.

**Why this matters to Phase 2:** the mapping layer's input arrives through a channel the
build spec does not describe. If two files land in one importer's slot, the mapping has to
either merge them into one file or declare which one wins — and `inventory.csv`
hard-deletes and reloads, so only one file's rows survive either way.

**Limits, all real, do not overstate this:**
- `record_type 'InboundEmail'` has **no backing table** in this schema. Blobs are
  **unattributable to an org in-DB** — leg's are identifiable only by the string "Legrand"
  in the filename and by date correlation.
- 97 blobs total. A handful of orgs, not the fleet.
- It records what **arrived**, never what the importer **consumed**.
- FTP is the other delivery path, is how most orgs deliver, and records nothing.
- A third daily attachment, `inventory-report-<date>.xlsx` (~154 KB), is **weekday-only**
  where the Legrand pair is seven-day. Different source. **Do not attribute it to `leg`.**

---

## Traps

- Source files arrive in **any** encoding, with headers **anywhere**, and sometimes with
  instructions to humans embedded in them. `The CopperSmith/Source Data/Parts-Table 1.csv`
  has its header on **row 2**; row 1 is a banner whose *third cell* reads
  `**DO NOT CHANGE COLUMN HEADERS!`.
- A file named `.csv` may be **xlsx** (`504b0304`). Route on magic bytes, never on
  extension — decoding a ZIP as mac_roman returns confident garbage.
- Profile the **most populated sheet** and name the ones you did not profile. A 646-row
  data sheet behind a 25-row cover sheet reads as a 25-row file.
- **Omitted-record behaviour differs per file.** `products.csv` **soft**-deletes;
  `customers.csv`, `inventory.csv`, `options.csv`, `option_groups.csv`, `matrix_options.csv`
  **hard**-delete. Deletes run only on a warnings-only import — an `Error` row suppresses
  them.
- **Import order:** `options` → `option_groups` → `products` → `stories` → `inventory` →
  `customers`, and **re-send `option_groups` after `options`** — importing options nulls
  group membership.
- **Auto-Create taxonomy:** whatever string you put in `CollectionCodes` / `CategoryCodes` /
  `TradeNameCode` becomes the **iPad label**. Never ship cryptic internal codes
  (`COL126`, `TN1`). Groups never auto-create — create them first.
- **`BaseItemCode`** importer cap is **40 chars**, not the 20 the KB says. Keep codes short
  for image filenames and grid display, but only reject a row past 40.
- **Missing a standard text column does not clear it** — send the column with empty values
  to clear.
- Three column pairs in this schema look like they answer one question and do not:
  `qty_available`/`qty_on_hand`, the two login columns plus `login_events`, and
  `orders.submit_date`/`created_at`. **Before using any column as *the* answer, look for its
  sibling.**

---

## Definition of done for Phase 2

1. A mapping format that carries, per field: source column, eCat field, primitive,
   **dialect**, parameters, and `carry_forward` where it applies.
2. **Legrand reproduces byte-identical** from the mapping alone, with the 1,537-line script
   discarded — and the test demonstrated red under a mutated mapping entry.
3. `mer` maps end to end from the raw NetSuite export, with every unmapped required field
   named and the reason given.
4. Escape-hatch usage counted and reported per client. Any client over 3 per-field
   transforms files a missing-primitive issue against `ecatlib` instead.
5. `a1_fingerprint.py` run against the produced file **before** any upload is proposed.
6. Carry-forward declared, and `diff_against_previous` run on every regeneration with the
   **blanked** count read before upload.

---

## Out of scope

- Rebuilding the profiler or `ecatlib` — both are done and both have passing acceptance
  tests
- The acceptance harness (`acceptance/`) — another session is repairing it
- The config-check skill — separate, already built
- Anything in eve. Settled 2026-09-04: the ingestion agent is **not** an eve target. It is
  ~5,900 loc of deterministic Python and SQL that has to sit next to the database, so it
  runs inside the VPN (Agent SDK in a container, on a cron), and the snapshot bridge is off
  its critical path entirely. eve is for the session-prep and correspondence agents, whose
  sources (BigQuery, HelpScout) are already portable. Build for a local runtime.
- **Writing to Postgres or the Admin Console.** Read-only throughout.
- Uploading anything. Phase 2 produces files and mappings; a human decides what is
  uploaded, after A1.
