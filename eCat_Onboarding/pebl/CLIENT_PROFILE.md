# Pebl — eCat Client Profile

> Backfilled from prior Cursor sessions. Verify against latest source before acting.

## Identity
- **Org shortname:** `pebl`
- **Domain:** peblfurniture.com
- **Vertical:** outdoor furniture
- **Status / stage:** build/review — catalog + options near-ready; transactional stack empty
- **Event:** SPOGA (June)

## Archetype & applicability
- **Archetype:** standard
- **Product line:** ecat-ipad
- **Flags:** none
- **File owner mode:** csv
- **Image mode:** ftp
- **Source cutover date:** unknown
- **Sub-brands:** none

- **No flags set — every gate applies.** Options are the primary complexity here (151
  options / 382 groups live), pricing is live (8 levels), and there are 171 customers with
  91 orders. Inventory shows **0 rows live**, but that is *not* declared `inventory: n/a`
  because nothing confirms it is intentional. An undeclared subsystem stays checked; only
  declare a flag you can cite.
- **This client is why the two-tier length check exists.** 16 of 24 option groups were
  rejected in one shot at the 15-char `Code` limit, and **all 171 customer rows** were
  rejected on lengths — `Terms` over 30 (*"30% T/T Advance, Balance Against Copy of Bill of
  Lading"*, **55** characters, not the 62 `IMPLEMENTATION_PLAN.md` 6.4 asserts), plus
  `BillToAddress1` over 60 on ~45 rows, `BillToCity` on ~8, and `BillToName` on 3. None of
  these were missing required fields, which is why a required-field check alone would have
  missed the whole event. `Terms` in particular is a structural mismatch needing a client
  decision, not a truncation — it was resolved by hand as `30% TT Adv, Bal on B/L` (22).
- **That import is also the cleanest confirmation of the delete rule:** because it landed
  at `Error` tier, **no customers loaded and nothing was deleted** — the org stayed at 0.
  Deletes run only on an error-free import.
- **Option groups were once imported before options**, which nulls membership. The order
  check refuses that sequence and appends the mandatory second `option_groups.csv` pass.
- **Precedent worth reusing:** this org's populated `option_mappings` is the working
  reference when another client needs a cascade.

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
