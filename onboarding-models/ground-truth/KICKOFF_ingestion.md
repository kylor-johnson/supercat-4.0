# Kickoff — the ingestion layer, Phase 0 and Phase 1

Paste this into a fresh Claude Code session in the **SuperCat 4.0** workspace, VPN up.
Self-contained.

**Scope of this session: Phase 0 (source profiler) and the start of Phase 1 (shared
library).** Do not attempt Phases 2–3. Read § "Why this order" before disagreeing with it.

---

## Read first

| file | why |
|---|---|
| `onboarding-models/ground-truth/BUILD_SPEC.md` | §2 = the shared-library boundary, §3 = the acceptance criteria. This is the spec. |
| `onboarding-models/ground-truth/SESSION_HANDOFF.md` | the traps, and the three constraints |
| `onboarding-models/ground-truth/SCORECARD.md` §§ 8–12 | the incidents behind every rule. **§12 is retractions — two findings were wrong** |

Canonical implementation tree is **`SuperCat_Simple_Final/02_Implementation/<Client Name>/`**
(full names, not shortnames). `SuperCat 4.0/eCat_Onboarding/` is archived — don't build from it.

---

## Why this order

BUILD_SPEC §2 identifies a shared transformer hiding in ~60 bespoke scripts, and the
obvious move is to extract it first. **That is the wrong opening move.**

Where the time actually went, from five blind audits:

- **drf** — five source files, a 30,000-SKU dump against ~130 images. Two weeks lost, Showtime missed. The blind read's verdict: *"the data question was never actually settled before the build started."*
- **tcs** — six sheets to reconcile (Master, Weiyan LED, Accessories, Parts, Dealers, Navigation)
- **leg** — 12 source files, 407MB, four separate price lists
- **pebl** — three complete catalogue generations, two item-code migrations

None of those are transform bugs. They are **specification failures** — nobody established
what the source contained before building on it. The 60 scripts and their long tail of
`fix_*.py`, `repair_*.py`, `exact_fixes.py` are the symptom.

So: profile before you transform.

---

## Phase 0 — the source profiler

### Two modes, and folder mode comes first

Surveyed 2026-09-03 across six clients' real source folders. The expensive question is
not "how do I parse this column" — it is **"which of these files is the one, and is this
even catalog source?"**

**Legrand's `Source Data/` is 91% not source data:**

```
132 files    12 csv/xlsx =   3.0 MB   <- the actual catalog source
             65 PDFs     = 175.0 MB   <- Library content (brochures, CEU decks, catalogs)
             55 other
```

**mali has two customer files that are indistinguishable by name, header or date:**

| file | rows | headers | modified |
|---|---|---|---|
| `ML + NSL CUSTOMERS COMBINED 2.0.csv` | 3,518 | BillToCode, BillToName... | 2026-03-11 |
| `ML CUSTOMER LIST REVISED - UPDATED.csv` | 421 | BillToCode, BillToName... | 2026-03-11 |

Same headers, same date, 8x the rows. The live org has 3,418 customers, so "COMBINED 2.0"
is the one — but nothing in the folder says so. mali also has four overlapping price-list
variants (`FLAT WITH DN`, `FLAT DISCONTINUED`, `Combined`, `Pricing_Gaps`).

**So folder mode answers, before any column is parsed:**

1. Which files are catalog source vs Library content vs noise
2. Where files are near-duplicates, which is authoritative — by row count, key overlap, and reconciliation against the live org
3. Which eCat file each candidate is trying to be (products / customers / inventory / stories / options)
4. What is missing entirely

### Three input classes — detect which, they need different handling

| class | seen at | what to do |
|---|---|---|
| **Raw ERP export** | `mer` (NetSuite, 56 cols: Internal ID, Display Name, Primary Units Type), `drf`'s binary-encoded customer listing | map it |
| **Pre-mapped by a human** | `libco` (whole set, mapped by sales), `drf` customers (`BillToCode`, `TerritoryCodes`) | **validate, do not transform.** The mapping is already done; the job is checking it. |
| **Industry / third-party template** | `tcd` ("LightsAmerica Data Template", "KANOVA-Data") | map, but the template is the contract |

Detect the class by testing headers against the known eCat field names. A file whose
headers are already `BaseItemCode` / `BillToCode` is class 2 and must not be re-mapped.

Watch for hybrids: `drf`'s "Characteristics ... eCat MAPPED" carries eCat headers
*and* client-domain columns (`Origin`, `Content`, `CleaningCode`, `Direction`) side by side.
And `libco`'s spec master has a column literally named `?????` plus `Custom1`–`Custom5`.

**Build `ecat-source-profile`** (skill, or a script the skill drives — your call, but the
skill is the interface). Point it at a file or folder the client sent. It answers:

1. **What is this?** rows, columns, encoding, delimiter, where the header actually is
2. **What's populated?** fill rate per column — a column that's 3% populated is not a field
3. **What looks like a key?** candidate SKU/item columns by uniqueness and format
4. **What maps to eCat?** proposed source-column → eCat-field mapping, with confidence
5. **What's missing?** eCat-required fields with no plausible source column
6. **What doesn't add up?** SKU count vs image count vs price rows — the drf check

**No transformation. No writes. It reads and reports.**

### Test it against these four, because they are all genuinely different

All under `02_Implementation/`:

| file | the shape it tests |
|---|---|
| `Legrand/Source Data/Canadian Price Lists/adorne Collection Price List Update_06.04.26_CA.csv` | **not valid UTF-8** — `tr` throws "illegal byte sequence". Detect and report encoding; don't crash. |
| `111Mercer/Source Data/111Mercer-ItemExport .csv` | ERP export. Note the numbered price columns (`1. Tempaper.com Price`) and the leading-space-in-filename. |
| `The CopperSmith/Source Data/Master Sheet E+G-Table 1.csv` | 157+ columns, wide spec sheet |
| `The CopperSmith/Source Data/Parts-Table 1.csv` | **header is not row 1** — it is row 2. Row 1 is a banner whose *third cell* holds `**DO NOT CHANGE COLUMN HEADERS!`, an instruction to a human. (Corrected 2026-09-04: previously said row 3, conflating the row with the cell.) |

If it handles those four it handles most of what arrives.

### Definition of done for Phase 0

- Runs clean on all four without crashing
- Correctly locates the header row in the Parts file
- Reports the Legrand encoding problem rather than dying on it
- Proposes a mapping for 111Mercer that a human agrees with
- Every unmapped required field is named, with the reason

---

## Phase 1 — extract the shared library

BUILD_SPEC §2 lists twelve primitives that `build_ecat_files.py` (Legrand, 1,537 lines),
`rebuild_lib_co_files.py` (libco, 1,277) and `rebuild_perfection.py` (tcs, 656)
**each independently reimplement**. That convergence is the evidence for the boundary.

Money parsing · weight parsing · dimension assembly · Y/N booleans · date normalisation ·
LongDesc truncation · text hygiene · RelatedItems · variant grouping · taxonomy mapping ·
CSV IO · carry-forward.

Field lengths and enums are **already generated** in `preflight/limits_generated.py` from
`ATTR_LENGTHS` in `supercat_server`. Do not retype a limit from a KB article — several
documented numbers are wrong.

### The acceptance test, and it is the point

**The library must reproduce a build that is already trusted.**

Target: Legrand's `products.csv` — 1,020 rows, live in production, produced by a
1,537-line script. Rebuild it using the library and diff against
`02_Implementation/Legrand/Build/products.csv`.

**Done = byte-identical, or every single difference explained and accepted.**

Until that passes, the library is not trustworthy enough to point at a new client. Do not
skip this to save time; it is the only thing standing between a shared library and
script #61.

`load_carryforward` matters more than its size suggests — when regenerating a file,
values the generator cannot derive (`Hideable`, and `ImageFileName` for images uploaded
after the last build) must be carried forward by key or regeneration silently destroys
them. It already cost Legrand 19 products' images once.

---

## Phases 2–3 — not this session, but build toward them

**Phase 2, mapping layer.** Per client: source column → eCat field + transform.
Declarative, with a code escape hatch for the genuinely bespoke — Legrand's four price
files merged by region × brand, tcs's buildable SKUs, libco's spec master.

**The agent proposes the mapping and flags what it cannot map. The agent does not write
transform code.** That division is the whole point. Today a build produces *a script*,
which is why there are sixty of them; the target is a build producing *a mapping*, with
the code shared.

**Phase 3, acceptance harness.** BUILD_SPEC §3's criteria, run **after** import.

The rule underneath it, confirmed independently on three clients: **a clean import proves
the file parsed and nothing else.** drf ran 18 days of images at clean tier with doubled
`.jpg.jpg` extensions that could never match. mali ran 86 consecutive clean image imports
with ~200 wrong photos. leg ran nine clean imports while 13 announced filter fields sat
empty. **Never treat import success as done.**

---

## Traps

- Source files arrive in **any** encoding, with headers **anywhere**, and sometimes with instructions to humans embedded in them.
- `products.csv` **soft-deletes** omitted rows on a clean import. `customers.csv`, `inventory.csv`, `options.csv`, `option_groups.csv` **hard-delete**. Deletes only run on a warnings-only import — an `Error` row suppresses them.
- Import order: `options` → `option_groups` → `products` → `stories` → `inventory` → `customers`, and re-send `option_groups` after `options` (importing options nulls group membership).
- **Confirm the target org before any upload.** Legrand's 1,020-row file was imported into 111Mercer on 2026-08-18, soft-deleting all 102 of their products. Second occurrence of that failure mode.
- Both `qty_available` and `qty_on_hand` are used live across the fleet. **Which one displays is configurable** — read it, never assume (SCORECARD §12 R1).

---

## Out of scope

- The config-check skill — separate, already built
- Anything in eve — it cannot reach Postgres, and the snapshot bridge comes later
- Writing to Postgres or the Admin Console
- Phases 2 and 3

---

## Gathering source data — do it *through* the profiler

Three of six clients have no `Source Data/` folder at all. Don't run a manual cataloguing
pass to fix that. Build the profiler, then run it on whatever turns up; its output is the
inventory.

Priority: **current builds only** (`leg`, `mer`) plus one representative file per shape for
design. Historical sources for clients already live have little value — the transform
worked, they shipped.
