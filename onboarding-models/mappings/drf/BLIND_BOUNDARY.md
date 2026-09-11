# drf (Dorell / Loomcraft) — blind-run boundary

Declared BEFORE any file was opened. Written 2026-09-05.

## Why drf

leg, mer and libco are all conventional catalogues: a SKU, a price, an image, a
description. drf is the archetype that actually broke an onboarding — **two
weeks lost, Showtime missed** — and the blind read's verdict was *"the data
question was never actually settled before the build started."*

It is shaped differently in four ways that the layer has never been tested on:

- **presentation-only.** No order submission.
- **fabrics**, not fixtures — pattern/colourway, not SKU/finish.
- **~30,000 SKUs against ~130 images.**
- **pricing lives in `stories.csv`**, not in `products.csv`.

The last one matters most: it means the target file's shape is not the one every
previous mapping assumed.

## Permitted — `Source Data/` only

- `Characteristics Interwoven spring 2026_eCat MAPPED (1).csv`
- `Dorell_Loomcraft_customers_eCat (1).csv`
- `customer Listing 4-7-26.csv`

Plus programme references that are not drf answers: `ecat_vocab` /
`limits_generated`, `profiler/`, `ecatlib/`.

## FORBIDDEN until the mapping is written and on disk

- `products.csv` (917 KB — the built target)
- `stories.csv`, `stories.csv.20260703-0215.csv`, `_stories_preview.html`
- `build_stories_with_pricing.py` — the answer key
- `customers.csv` (built)
- `HANDOFF.md`, `CLIENT_PROFILE.md`
- the live `drf` org in Postgres, including product and image counts
- SCORECARD's drf narrative and OPEN_ITEMS A9/A10/A16, which were written from
  the build

## The check I expect to earn its keep

The profiler's **"what doesn't add up"** — SKU count vs image count vs price
rows. drf is the client it was written for. The prediction, recorded before
looking: the product source will not contain enough rows to explain the built
catalogue, and that discrepancy — not any column mapping — will be the finding.

## Scoring

Same three buckets: right / wrong / unknowable, plus not-produced, summing to a
named denominator. Comparison targets get pinned via `mapping/bless.py
--reference` BEFORE scoring; `score_blind.py` refuses otherwise. That rule
exists because scoring libco against an unpinned stale file produced two
findings that had to be retracted.
