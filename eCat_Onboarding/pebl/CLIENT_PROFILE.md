# Pebl — eCat Client Profile

> Backfilled from prior Cursor sessions. Verify against latest source before acting.

## Identity
- **Org shortname:** `pebl`
- **Domain:** peblfurniture.com
- **Vertical:** outdoor furniture
- **Status / stage:** build/review — catalog + options near-ready; transactional stack empty
- **Event:** SPOGA (June)

## Contacts
- **Client:** Mandy Mai (sales04@peblfurniture.com); CC vincent@, sales07@
- **Help Scout:** thread #13879

## Catalog
- **Collections:** HAVEN, WAVE (live) + Orbit, Horizon, Newport, Hilo, Bold, Levl, Bistro, Butler, Tube, Albatros (newer)

## Options + Option Mapping (primary complexity)
- **OptionSet1 = Frame Color, OptionSet2 = Material Color, OptionSet3 = Cushion Fabric.**
- **Granular per-choice groups** (`FRAME_MOCHA`, `MAT_NEO_MOCHA`, …) — NOT one big
  `FRAMECOLOR`/`MATCOLOR`/`CUSHFABRIC` (that breaks the cascade).
- **Option Mapping** configured in Admin on **OptionSet1** (add connections, don't
  create a new mapping under OptionSet2). Enabled by SuperCat Support.
- Codes ≤15 chars (shorten e.g. `DGREEN_GLAZED_CER` → `DGREEN_GLAZ_CER`).
- Pricing via group `PriceAddend` (not matrix).

## Images
- Product photos → FTP `/images`; option swatches (300×300) → `/option_images`.
- Filename normalization: no spaces (`_`), no dots in `Alu.`/`Dia.`, `+`→`-`, `.JPG`→`.jpg`.

## Gaps / quirks
- **0 customers, 0 price levels, 0 inventory** — catalog-strong, transaction-empty.
- Client edits old local CSVs and re-uploads coarse `option_groups.csv` → Option
  Mapping "internal error". Always: download current file from FTP `/data` first.
- Known missing images: 343cm dining table + Wave covers.

## Files & paths
- **Working folder:** 02_Implementation/Pebl/00_Import_Files/Ready_For_Import/
- Mapping spec: `ecat-options mapping.xlsx` (authoritative business rules).

## Open items
- [ ] Customers + price levels + inventory before fair-ready selling
- [ ] Confirm assumption rows (Tube/Butler/Bold/Orbit) + xlsx price deltas
- [ ] Remaining missing images
