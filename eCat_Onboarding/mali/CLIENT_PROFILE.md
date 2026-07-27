# Magic Lite — eCat Client Profile

> Updated 2026-07-20. Verify against live Postgres (`mali`) and Ready_For_Import before acting.

## Identity
- **Org shortname:** `mali` (single org — Magic Lite Canada + NSL US)
- **Sites:** eCat Online “Magic Lite” (`url_key` 12) and “National Specialty Lighting” (`url_key` 13)
- **Domains:** magiclite.com · nslusa.com
- **Vertical:** lighting (linear, strip, undercabinet, downlight, landscape, industrial, drivers/controllers)
- **Status / stage:** live / dual-brand maintenance

## Catalog
- **Working products:** `00_Import_Files/Ready_For_Import/products.csv` (~694 rows)
- **Collection codes:** `LL`, `UCL`, `DL`, `LAND`, `IL`
- **TradeNameCode:** currently all `ML` in file (brand split is via price levels + custom fields + user groups, not separate tradenames)
- **Tokistar (`TL`):** out of scope

## Pricing — dual division
- **Levels:** `mllist` / `mldn` (**CAD**), `nsllist` / `nsldn` (**USD**), `net_price` (avoid authorizing for brand groups)
- **Visibility:** ML Reps + eOL ML → ML levels only; NSL Reps + eOL NSL → NSL levels only
- **2026-07-20:** Jen’s pricing-gaps sheet applied to Ready_For_Import products (backup `products.backup_20260720_162000.csv`). **Re-import pending.** ~70 SKUs still ML-only / wrong NSL codes per client notes.

## Product docs (custom fields — done)
- `CutSheetML`, `InstructionsML`, `CutSheetNSL`, `InstructionsNSL`
- Authorized per brand user group; do not confuse with Library

## Library (done 2026-07-20 — see LIBRARY-BUILD-CHECKLIST.md)
- **No CSV import** — Admin Console Resource Library only ([KB](https://supercatsolutions.com/knowledgebase/document-library))
- Dual libraries: ML sections (43 links) + `NSL — *` sections (128 `nslusa.com` links)
- Brand groups Library auth **Selected**: ML Reps / eOL ML Public Site → ML only; NSL Reps / eOL NSL Public Site → NSL only
- Admin / z-SuperCat / DefaultUserGroup remain Library **All**
- Source maps: `07_Data_Scraping/pdf_links/` (+ `nsl/`); apply script: `scripts/apply_library_brand_split.py`
- **Human QA still needed:** brand-login check on each eOL site (not Admin)

## Distribution centers
- Two DCs: `ML`, `NSL`; inventory = 2 rows per SKU when both stocked
- DC restriction = order ship-from selector (org `tcgcd` false)

## Files & paths
- **Working folder:** `02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/`
- **Handoff for next agent:** `HANDOFF.md`
- Price lists (root + `03_Data/`): ML/NSL AUG2025 FLAT WITH DN / DISCONTINUED xlsx

## Open items
- [ ] Import updated `products.csv` (pricing gaps + ALP renames + hides)
- [x] Library: brand-split sections/entries + set ML/NSL groups to Selected (see LIBRARY-BUILD-CHECKLIST.md)
- [ ] Resolve ~70 ML-only / incorrect-NSL-code SKUs with client NSL price list
- [ ] Point site enrollment Default User Group to eOL ML / eOL NSL Public Site (not DefaultUserGroup)
- [ ] QA with brand logins (not Admin) — Admin sees all prices/fields/library
