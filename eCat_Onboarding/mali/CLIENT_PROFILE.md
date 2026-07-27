# Magic Lite — eCat Client Profile

> Updated 2026-07-20. Verify against live Postgres (`mali`) and Ready_For_Import before acting.

## Identity
- **Org shortname:** `mali` (single org — Magic Lite Canada + NSL US)
- **Sites:** eCat Online “Magic Lite” (`url_key` 12) and “National Specialty Lighting” (`url_key` 13)
- **Domains:** magiclite.com · nslusa.com
- **Vertical:** lighting (linear, strip, undercabinet, downlight, landscape, industrial, drivers/controllers)
- **Status / stage:** live / dual-brand maintenance

## Archetype & applicability
- **Archetype:** standard
- **Product line:** ecat-ipad, eol
- **Flags:** none
- **File owner mode:** csv
- **Image mode:** ftp
- **Source cutover date:** unknown
- **Sub-brands:** ML,NSL

- **Standard with a sub-brand flag** — Open Decision 3 in `IMPLEMENTATION_PLAN.md` asks
  whether this org is snowflake instead. The data path is ordinary; what is unusual is that
  two brands (Magic Lite / NSL) live in one org, separated by user group, described on the
  2026-05-13 call as *"a workaround for the platform's current lack of native sub-brand
  support."* Collections, price levels, email templates, and branding all diverge per
  group, so **any check that assumes one brand per org must read the user-group layer
  here.** Either way this annotates; it never blocks.
- **No flags set.** Options are live (2 options / 2 groups), inventory is live (694 rows
  matching all 683 active products), pricing is live (4 levels) — every gate applies.
- **The org fingerprint check exists because of this client.** On 2026-07-23 Legrand's
  1,194-row inventory file was imported here; inventory hard-deletes then reloads, so
  mali's real inventory was replaced with rows matching zero mali products. Resolved the
  same day. Never upload an inventory file without confirming the key overlap first.
- **Rep-view vs Admin-view is a go-live gate for this client**, not a nicety: six of nine
  escalated items were not defects, just Admin-view artifacts. The client needs a non-Admin
  rep profile **per brand**.

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
