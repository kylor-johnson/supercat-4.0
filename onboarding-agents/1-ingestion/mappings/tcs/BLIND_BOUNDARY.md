# tcs (The CopperSmith) — blind-run boundary

Declared BEFORE any file was opened. Written 2026-09-05.
Fourth and last blind run; same protocol as libco and drf.

## Why tcs

**Input class 3 — industry / third-party template, and the template is the
contract.** The first class-3 client the layer has seen, which is the only
reason Phase 2 is not already finished.

It is also the hardest source in the set:

- **six sheets** to reconcile: Master, Weiyan LED, Accessories, Parts, Dealers,
  Navigation
- `Master Sheet E+G-Table 1.csv` — **157+ columns**
- `Parts-Table 1.csv` — **header is row 2**; row 1 is a banner whose *third*
  cell holds `**DO NOT CHANGE COLUMN HEADERS!`, an instruction to a human
  embedded in the data
- **buildable SKUs** — BUILD_SPEC §2 lists `stage2_lantern_rebuild`,
  `stage4_parts_and_kits` and `sku_ignition` as genuinely client-specific

## Permitted — `Source Data/` only

```
Master Sheet E+G-Table 1.csv          941 KB
Weiyan LED-Table 1.csv                369 KB
Dealers_eCat-Table 1.csv              157 KB
Accessories-Table 1.csv                58 KB
Parts-Table 1.csv                      18 KB
eCat Navigation and Filtering (1).csv 711 B
```

Plus programme references that are not tcs answers: `ecat_vocab` /
`limits_generated`, `profiler/`, `ecatlib/`.

## FORBIDDEN until the mapping is written and on disk

- `CS_eCat_Rebuild/rebuild_perfection.py` — the answer key (656 lines)
- everything else in `CS_eCat_Rebuild/`: `products.csv`, `options.csv`,
  `option_groups.csv`, `stories.csv`, `taxonomies.csv`, the `*_audit_fix.csv`
  files, `build_parts.py`, `build_kits.py`, `sync_from_source.py`,
  `merge_weiyan_groups.py`, `apply_tuesday_fixes.py`, `fix_*.py`, `validate.py`,
  and every `.md` report in it
- all of `CS_OptionMapping_Rebuild/`
- `CLIENT_PROFILE.md`
- the live `tcs` org in Postgres, including product, option and taxonomy counts
- BUILD_SPEC §2's tcs dialect row and the tcs entries in `mapping/BUDGET.md`,
  both of which were written by reading the answer key

## The prediction, recorded before looking

**The multi-sheet reconciliation is the work; the column mapping is not.** This
is mali's "COMBINED 2.0" problem at six-sheet scale — two files indistinguishable
by name, header or date, where the wrong choice silently deletes a division.

Specifically I expect to have to answer, from the data alone:

1. **which sheet feeds which eCat file** — the six are not six products.csv
   candidates; some are customers, some are options, one is a taxonomy contract
2. **which sheet is authoritative where two disagree** — Master vs Weiyan LED
   overlap is the mali question, and the profiler's rule is *containment before
   Jaccard, and per-division files MERGE rather than compete*
3. **what "buildable SKU" means here**, and whether it is a loader (which rows
   exist) or a transform (one field's value)

## Scoring

Same buckets: byte-exact / semantically equivalent / wrong / not produced /
genuinely unknowable, summing to a named denominator, at both column and cell
granularity. **The blind score is the number before any post-unblind fix** —
libco's is 26, not 27 or 29, and this run will label its moments the same way.

Answer keys pinned via `bless.py --reference` BEFORE scoring; `score_blind.py`
refuses otherwise, and refuses again if the key overlap is empty.
