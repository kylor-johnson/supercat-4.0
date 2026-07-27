# CopperSmith Perfection Pass — Validation Report

**Date:** 2026-06-15  
**Org:** `tcs` (id 291)  
**Pipeline:** `rebuild_perfection.py` → `validate.py after`

## Result

**PASS — 0 errors**

| File | Rows |
|------|------|
| `products.csv` | 628 |
| `stories.csv` | 628 (1:1 with products) |
| `options.csv` | 330 (+FT parent) |
| `option_groups.csv` | 764 |

## Fixes applied

| Stage | What changed |
|-------|----------------|
| 1 SKU integrity | 9 corrupt codes fixed (`WST 16.00`→`16WST`, `SRG 41.00`→`SRG41`, etc.) |
| 2 Lantern rebuild | 379 rows synced from Master + Weiyan (collection, category, Genre, CDN images, shipweight where source has data) |
| 3 Options | BMPM 113, PMAU 157, FT added; option_groups re-synced + Weiyan merge |
| 4 Parts/kits | 234 parts re-built from `Parts-Table 1.csv`; 12 kits → `RLM Lighting,Pendant Lights` |
| 5 Related/Hideable | Size siblings, gas ADS+TLA on RelatedItems2, hero Hideable per parent+ignition |
| 6 Stories | Full 1:1 sync with products |

## Spot checks

- `16WST` / `9WST` present; corrupt `WST *.00` gone
- `TR31G` → `TradeNameCode = The CopperSmith Biltmore®`, `CollectionCodes = Traveler`
- `SRG41` literal part SKU; RelatedItems3 on AS41G resolves
- `AS41G` RelatedItems2 includes `ADS,TLA` (+ WGS, GLC)

## Known client blockers (not invented)

These accessory SKUs are referenced in option groups but **not** in the Accessories tab — need client confirmation before adding:

- `CHM36`, `CHM72`, `QCHM`

## Shipweight note

111 lantern SKUs have **no** Shipping Weight or Weight in Master/Weiyan source — left blank intentionally. Validator only fails when source has weight data but products.csv does not.

## Source sync (`sync_all_source_fields.py`)

Populates **existing** `products.csv` columns from source tabs. **Only net-new columns:** `Feature1`–`Feature6`, `ProductTags` (67 columns total). Gallery URLs merge into existing `ImageFileName`. Feature bullets also in `stories.csv`.

```bash
python3 rebuild_perfection.py   # full pipeline + backups (*.pre_perfection_bak)
python3 validate.py after       # gate only
```

Import order: `options.csv` → `option_groups.csv` → `products.csv` → `stories.csv`
