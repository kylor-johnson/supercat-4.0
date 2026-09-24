# What BUILD_SPEC §3 costs to implement, now that ecatlib exists

**Written 2026-09-04, after Phase 1 passed.** Every judgement below was checked
against the live schema rather than estimated from the spec — the schema probes
are named so they can be re-run.

## Headline

**Nine of the ten criteria are implementable today. One is blocked, and not on
effort.** The library helped less than expected: §3 is almost entirely a
*read-the-live-org* problem, not a transform problem. What ecatlib actually
contributes is `csvio` (read the file being judged) and `carryforward`
(B6, already built).

The real prerequisite was **knowing where the config lives**, and for B5 that was
genuinely unknown until today — see below.

| # | criterion | status | cost | needs |
|---|---|---|---|---|
| A1 | org fingerprint | ready | **S** | file keys + 1 query |
| A2 | placeholder pricing | ready | **S** | 1 query |
| A3 | references resolve | ready *(except images)* | **M** | 1 query per reference class |
| A4 | import order | ready | **M** | YAML parse of `import_events.data` |
| B1 | registered fields populated | ready | **M** | `custom_fields` + two storage shapes |
| B2 | image filenames match FTP | **BLOCKED** | — | FTP listing; no access from here |
| B3 | territory codes | ready | **S** | 1 query |
| B4 | feeds overwriting | ready | **M** | `import_events` + `inventories.updated_at` |
| B5 | inventory config vs data | **ready — newly unblocked** | **S** | `custom_fields.alias` |
| B6 | carry-forward diff | **done** | — | `ecatlib.carryforward.diff_against_previous` |

S ≈ a query and a wrapper. M ≈ a day, mostly parsing or edge cases.

---

## B5 — the one that was actually unknown, now solved

BUILD_SPEC B5 says the displayed inventory field "must be read from config, never
assumed", but never says *where that config is*. R1 was retracted precisely
because the field was assumed. So the first question was whether such a config is
readable at all.

**It was being looked for in the wrong table.** `organizations.inventory_management`
is empty for 10 of 11 orgs checked and does not discriminate — `ta` (on-hand) and
`cl` (available) both hold `''`.

The config is **`custom_fields.alias`**:

| org | registered alias | qty_available populated | qty_on_hand populated |
|---|---|---|---|
| cf | `i.qty_available` | 5,312 | 0 |
| cl | `i.qty_available` | 378 | 0 |
| libco | `i.qty_available` | 834 | 0 |
| tcd | `i.qty_available` | 325 | 0 |
| etl | `i.qty_on_hand` (+3) | 0 | 648 |
| ol | `i.qty_on_hand` (+2) | 0 | 76 |
| ta | `i.qty_on_hand` (+3) | 0 | 1,056 |
| tam | `i.qty_on_hand` | 0 | 1,058 |

**8 of 8 agree.** This reproduces R1's fleet table — which was derived from data
alone — and supplies the configuration that explains it. The check is one query:
compare `alias LIKE 'i.qty_%' AND send_to_ipad` against which column is actually
populated.

Multi-division orgs use the `ic.` prefix for inventory *custom* fields:
`mali` registers `ic.ML_QtyOnHand`, `ic.NSL_QtyAvailable` and eight more, which is
why both standard columns read zero for it. Any implementation must handle both
prefixes or it will report a false zero on every division org.

### What this says about three current orgs — measurement only

`leg` (755 inventory rows, 727 with `qty_on_hand`), `mer` (102 rows, 57/57) and
`mali` (703 rows) have **no `i.qty_*` alias registered**; mali has `ic.` aliases
instead.

**That is the measurement. The consequence is NOT established here.** Whether a
rep sees no inventory on `leg` requires knowing what the iPad renders when no
alias is registered, and this analysis does not show that. What would settle it:
the Rails view/sync code, or a sync payload for `leg`. Given R1, that inference is
exactly the one not to make twice.

---

## Where the effort actually is

**A4 and B4 both hinge on parsing `import_events.data`,** which is a Ruby YAML
blob:

```yaml
---
- - Inventory
  - - - :warning
      - 'Line 2: Product not found, record ignored., BaseItemCode=1597'
```

File type is the first element; then (severity, message) pairs. Regular enough to
parse, but **PyYAML is not installed** in this environment, so it needs either a
dependency or a small line parser. Budget the parser once — A4, B4 and any
future import-log work all consume it.

**B4 is already demonstrably detectable.** leg's three most recent inventory
imports: 2026-09-04 06:01 and 09-03 19:51 both warn `Product not found` for
`1597`, `1597BK` (radiant codes), while 09-03 18:23 warns for `ADPD453LM2`,
`ADTP700MMTUM2` (adorne). The two feeds are alternating and each warns against the
other brand's catalogue — the B4 signature, visible from `import_events` alone.
Folder mode independently found the same thing structurally: the two inventory
files share **zero** item numbers.

**B1 has a shape trap.** Custom fields are stored two ways — `db_column_name`
(`ecat_custom_field_N`, a real column) and `alias` (a pointer to an existing
field, no storage of its own). A populated-ness check that only looks at one
misreports the other. `cl` alone uses both shapes in the same org.

---

## The one that is blocked

**B2 — image filenames must match FTP byte-for-byte.** Requires listing the FTP
`/images` root; nothing in this environment can reach it, and Postgres only
carries `products.image_exists`, which is the importer's own opinion. A partial
check (`ImageFileName` non-empty vs `image_exists`) is cheap but is **not** B2 —
`pebl`'s 18 days of `.jpg.jpg` filenames would have satisfied it. Either wire up
FTP credentials or record B2 as unimplemented; do not ship the partial and call
it done.

---

## What this does and does not close

§3.3's rule — *a clean import proves the file parsed and nothing else* — is the
D10 limit, and D10 was recorded as "not fixable from Postgres". **That was too
pessimistic, but only just.** Nine of ten criteria are post-import state checks
that Postgres can answer, so the acceptance harness genuinely does close most of
the gap between "imported clean" and "correct".

What it does not close is the drf case that produced D10: a correct-looking wrong
catalogue. Every product parsed, every reference resolved, every registered field
populated — and the colours were still wrong. **No §3 criterion detects that**, and
none can, because correctness there is a claim about the client's intent, which
lives only in the conversation record. Keep D10's limit stated; §3 narrows it, it
does not remove it.

## Suggested order

1. **A1** first, alone. It is an S, and it is the check that would have stopped
   Legrand's 1,020-row file soft-deleting 111Mercer's 102 products — a failure
   that has now happened twice.
2. **B5, A2, B3** — three more S-sized queries, all now fully specified.
3. The **`import_events` parser**, then A4 and B4 on top of it.
4. **B1**, handling both storage shapes.
5. **A3**, one reference class at a time.
6. **B2** only once FTP access exists.
