# Tuesday Changes Summary (2026-06-12)

Surgical edits to [`products.csv`](products.csv) via [`apply_tuesday_fixes.py`](apply_tuesday_fixes.py) (one-time helper — re-run only from `products.csv.bak` if needed).

## products.csv

| Change | Before | After |
|--------|--------|-------|
| Taxonomy | Auto-create strings (`The CopperSmith`, `Mount Vernon`) | Standard codes `TN1`, `COL34`, `CAT5`, etc. |
| RelatedItems | Accessories only on many gas SKUs | Size siblings same ignition |
| RelatedItems2 + TabName | Missing | Accessories tab; 347 products |
| OptionSet7 on gas | ~94 SKUs with ELE003 | 0 |
| OptionSet8 on electric/W | Some bleed | Cleared on E/W appropriately |
| Hideable | Inconsistent | One hero per Parent SKU + ignition |
| ImageFileName | Mix of filenames + URLs | 378/382 full Catsy URLs |

### Spot-check rows

- **MV19G:** `RelatedItems=MV19G,MV25G,MV30G` · `RelatedItems2=WGS,GLC` · no OptionSet7
- **MV19E:** sizes + electric accessories in RelatedItems2
- **MV19W:** `CAT7` · sizes + `FB1,FB12V` accessories only

## stories.csv

- Added 15 accessory product stories (382 rows, all ≤500 chars)

## Unchanged (Tuesday pass)

- `options.csv`, `taxonomies.csv`

## Source sync correction (2026-06-12, post-Tuesday)

[`sync_from_source.py`](sync_from_source.py) re-aligned build files to client source:

| Change | Before | After |
|--------|--------|-------|
| Option wiring | 267/271 SKUs wrong (invented WM010/WA017 groups) | 271/271 match source `products (4).csv` + `option_groups (1).csv` |
| option_groups.csv | 314 generic split groups | 634 groups from source M→WM/CM/PP split |
| Taxonomy columns | `TN1`, `COL11`, `CAT5` codes | Display names: `The CopperSmith`, `Bayou Street`, `Gas Lanterns` (FurnishWeb) |
| BS61G example | WA017 = TSW19,TS19 | W046 = BFH3, BS1, BSW1, RBS1, TS3, TSW3 |

Preserved from Tuesday: RelatedItems, RelatedItems2, Hideable, CDN URLs, Weiyan rows.

## Manual follow-up

- [`ADMIN_PREFLIGHT.md`](ADMIN_PREFLIGHT.md) — enable nav drill-down flags
- [`IMPORT_AND_VERIFY.md`](IMPORT_AND_VERIFY.md) — upload **all four CSVs** in order
- [`CLIENT_EMAIL_DRAFT.md`](CLIENT_EMAIL_DRAFT.md) — send to Jordan/Jillian
