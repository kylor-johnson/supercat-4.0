# libco — blind-run boundary

Declared BEFORE any file was opened, so the score at the end means something.
Written 2026-09-04.

## Why blind

leg and mer were both reproductions. A reproduction tests whether the layer can
re-express a decision **someone already made**. It cannot test whether the layer
can decide what a source MEANS when nobody has decided yet — and that is the
question that cost drf two weeks: *"the data question was never actually settled
before the build started."*

libco has an answer key (`rebuild_lib_co_files.py`, 1,277 lines, and a live org
with 288 products). Reading it first would make this a fourth reproduction and
would prove nothing new.

## Permitted — files the CLIENT sent

- `Lib_Co_Spec_Master_eCat_Mapped - ....csv (2).csv`
- `Lib & Co Inventory with eCat Headers.xlsx`
- `LIB_Co_Upload_Fixed_Prices.xlsx`
- `LIB_Customers_eCat_Mapped.xlsx`
- `Discontinued inventory-report-July_10th-_2026.xlsx`
- `Rep List.csv`
- image directories (`1_ Collection Images/`, `FTP_Upload_Images/`) — filenames only

Plus programme-level references that are not libco answers: `ecat_vocab.py` /
`limits_generated.py` (the eCat field vocabulary), `profiler/`, `ecatlib/`.

## FORBIDDEN until the mapping is written and on disk

Anything that encodes a decision already made about libco:

- `rebuild_lib_co_files.py`               the answer key
- `apply_libco_jun15_updates.py`
- `products.csv`                          the built target
- `products_LONGDESC_FIX.csv`, `products_LONGDESC_FIX_v2.csv`
- `README-products_LONGDESC_FIX.md`
- `output/`, `libco_deliverables_2026-08-25/`
- `MISSING-SKUS-2026-invoiced.csv`        our analysis, not client source
- `HANDOFF.md`, `ACTION-PLAN-BEFORE-WED.md`, `PRE-MEETING-CHECKLIST-*.md`,
  `VERIFICATION-2026-08-31.md`, `CLIENT_PROFILE.md`
- the live `libco` org in Postgres — including product counts and taxonomy
- BUILD_SPEC's libco dialect table, which was derived FROM the answer key

Also forbidden: `ecatlib.values` docstrings naming libco's dialect behaviour.
Those were written by reading `rebuild_lib_co_files.py`. The libco dialect must
be DERIVED FROM THE SOURCE here, then checked against them at scoring time.

## The three buckets the score must separate

1. **Right** — the mapping matches the built file.
2. **Wrong** — the mapping disagrees and the source contained enough to know
   better. This is a defect in the mapping layer or in my reading.
3. **Unknowable** — the mapping disagrees and NOTHING in the source could have
   settled it. This is the valuable bucket: it is the empirical answer to *what
   must a human still tell us*, and no reproduction test can produce it.

Bucket 3 is the deliverable. Buckets 1 and 2 are the cost of getting it.
