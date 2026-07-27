# Legrand (adorne + radiant) — eCat Client Profile

> The one file a new chat reads to get full context. Keep it current. Pair with
> `HANDOFF.md` (generated per session by the `ecat-session-handoff` skill).

## Identity
- **Org shortname:** `leg`
- **Admin Console:** supercatsolutions.com/leg
- **TradeNameCode:** `Legrand` (Trade Name); Collections: `adorne`, `radiant`
- **Domain / vertical:** Designer electrical devices (switches, outlets, dimmers)
- **Status / stage:** onboarding — build complete, awaiting client confirmations + Admin custom-field registration

## Archetype & applicability
- **Archetype:** standard
- **Product line:** ecat-ipad
- **Flags:** `options: none`
- **File owner mode:** generator
- **Image mode:** ftp
- **Source cutover date:** 2025-07-08
- **Sub-brands:** none

- **`options: none` despite 29 options and 11 option groups existing in the org.** All of
  them were written inside a single 0.15-second import on 2025-06-16 — POC residue from
  before the cutover — and **zero of 1,020 active products reference any option**. This is
  cleanup hygiene, not an options architecture, and it must not be read as evidence that
  Legrand needs one. The dead config never clears on its own, because option cleanup only
  happens when you *send* `options.csv`, and this build emits none.
- **Generator-owned (Mode A), and this is the healthy reference case.** Corrections live
  inside `Build/build_ecat_files.py` as named tables (`CATEGORY_FIXES`, `FINISH_FIXES`,
  `PRODUCT_NAME_FIXES`), so regeneration is reproducible and loses nothing. Do not
  hand-edit the output CSVs.
- **The cutover date is load-bearing here.** Everything before 2025-07-08 is demo data: the
  four 2025-06-19 customer-import failures ran against POC data, and the only recent
  customer import (2026-06-18) was **clean**. The single live customer is an org *waiting on
  the client's real file*, not an unfixed validation failure.

## Contacts
- **Client:** Legrand North America (adorne + radiant product lines)
- **SuperCat:** Kylor Johnson

## Systems
- **ERP / PIM:** Client Excel exports — `adorne & radiant US/CAD Data File`
- **Integration posture:** Generator-owned (Mode A). All build logic in `Build/build_ecat_files.py`. Do NOT hand-edit the output CSVs; codify fixes as named tables in the script.

## Taxonomy decisions
- **Method:** Auto-Create — Collection/Category strings ARE the iPad labels
- **Collections → :** `adorne`, `radiant` (matches the two product lines)
- **Categories → :** 40 functional categories from source (see `Build/TAXONOMY.md`)
- **Custom fields:** 14 custom fields — all must be pre-registered in Admin before import (see `Build/custom-fields-setup.md`)

## Pricing
- **Model:** Imported levels (5 codes)
- **Price levels (codes):** `net`, `retail`, `imap`, `canet`, `caimap`, `camsrp`
- **Divisions:** US vs Canada (separate price columns per region)
- **List price hidden?** TBD per user group setup

## Images
- **Naming convention:** Legrand image URL-based (see `Build/image_filename_map.csv`)
- **Delivery mode:** FTP-based; images downloaded by `Build/download_images.py` to `Build/images/` (gitignored — 4,732 files)
- **Which rows get images:** All 1,020 active products; 20 still missing as of last run (see `Build/missing_images_gap_final.txt`)

## Files & paths
- **Working folder:** `eCat_Onboarding/leg/Build/`
- **Generated outputs:** `Build/products.csv`, `Build/stories.csv`, `Build/inventory.csv`
- **Current source of truth:** Client XLSX in `Build/Source Data/` (gitignored)
- **Build script:** `Build/build_ecat_files.py` — run `cd Build && python3 build_ecat_files.py` to regenerate

## Snowflake quirks
- **No options.** Every finish is its own orderable SKU; finish variants modeled as `RelatedItems` (872 SKUs across 173 families). Do NOT build options.csv or OptionSet columns.
- **Applicability flag: `options: none`** — skip options/group/mapping gates entirely.
- **RelatedItems** strategy: SKUs differing only by finish grouped together; every member lists full family including itself.
- **FINISH_FIXES** applied in script: unambiguous typos only. Do NOT merge `Gloss White` vs `Gloss White-on-White` (confirmed distinct on legrand.us).
- **35/35 source columns land in products.csv.** Hard rule: every non-blank source column must land — verified.
- **LongDesc overflow:** 668 SKUs exceed 50 chars; this is correct (real limit is 255; import produces warnings only, not errors).

## Import history
| Date | File | Rows | Result / notes |
|------|------|------|----------------|
| 2026-06-18 | customers.csv | 1 | Clean — zero errors, zero warnings. Single test customer `4444 / eCat Test`. Real customer file pending from client. |
| 2026-07-14 | products.csv | 1,020 | Warnings: unknown `carton1_h/l/w` fields + `rohscompliant`/`Color`/`voltage` custom fields missing (not yet registered) |
| 2026-07-14 | inventory.csv | 1,194 | 247 `Product not found` warnings (pre-cutover POC residue; not a bug in current build) |
| 2026-07-23 | products.csv | 1,020 | Warnings: `rohscompliant`, `Color`, `voltage` still missing — custom field registration required |

## Open items / client confirmations
- [ ] Register all 14 custom fields in Admin → Products → Custom Fields (see `Build/custom-fields-setup.md`)
- [ ] Client to confirm: `Gloss White` vs `Gloss White-on-White` — are these distinct or should they merge?
- [ ] Client to confirm: Mirror/Brushed-Stainless finish family groupings
- [ ] Client to provide real customer file (current org has only 1 test customer)
- [ ] Resolve 20 products still missing image URLs (see `Build/missing_images_gap_final.txt`)
