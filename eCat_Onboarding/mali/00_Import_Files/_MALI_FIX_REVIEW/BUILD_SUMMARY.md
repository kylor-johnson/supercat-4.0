# mali — products.csv rebuild (post-verification)

**Output:** `products_FINAL.csv` (600 rows) — staged here; live `Ready_For_Import/products.csv` untouched.
Source: live `products.csv` (694) + AUG2025 ML/NSL price lists + client July-15 gap sheet + 119 image repoints.

## Result
| Metric | Value |
|---|---|
| Live products | 694 |
| **Kept** | **600** |
| Dropped — not in either AUG2025 price list | 87 |
| Dropped — client discontinue ("remove") | 7 |
| ML price (CAD) filled | 597 |
| NSL price (USD) filled | 578 |
| ML_UPC filled | 582 |
| NSL_UPC filled | 563 |
| Image repoints applied (of 119; rest were on dropped SKUs) | 104 |
| Kept rows still on placeholder/family image → **need photos** | 326 |

## Verification corrections applied
1. **87 drops, not 97.** 11 SKUs were format-drift matches to real pricebook codes (hyphen/slash/EC drift) — recovered with price + UPC instead of deleted:
   `ES-LS2835*` (4), `LV-V1V3-*` → `LV-V1/V3-*` (3), `LV-RD5455-EC/-WF` → `LV-RD54/55-*` (2), `LV-RD5455-EC-MC` → `LV-RD54/55-MC` (alias), `LTS-II-5-HW/WH` (double-slash pricebook typo).
2. **Sanitized BaseItemCodes kept** (e.g. `LV-V1V3-EC`), pricing bridged by normalized lookup — no `/` introduced into codes/image filenames.
3. **Float noise fixed** — all prices rounded to 2 dp (e.g. Brick Star SS = 207.00, not 206.999…).
4. NSL prices for divergent SKUs pulled via crosswalk (LEDBS-II→LBR-II, LEDSST-II→LST-II, LEDMD-S→LEDMDS, LEDMD-WH→LEDMD-CW).

## Still needs a human decision (does NOT block import)
- **22 kept rows have no NSL price** = 7 client-flagged ML-only + 15 `needs_nsl_pairing` (drivers `MLDR*`/`MLDRE*`/`LEDDR-12-20W-HW`, work lights `LWL-*`/`SWL-60W-50`, `NN-C10-8`, `LTP-001-OD-6FT`). Keep ML price; pair to NSL codes or confirm ML-only.
- **3 kept rows have no ML price** (NSL-only, e.g. `LES-TCJ-EI6-N`).
- **Rename requests** (left as-is, priced via gap-fill): `LMSH-001`→`LMSII-001` (LMSII-001 IS in pricebook), `LV-ALP-1605`↔`LV-ALP1605` (neither in pricebook). Confirm before renaming — affects inventory matching.
- **326 items on family/placeholder photos** — real photography required (see `BUILD_photos_needed_kept.csv`).

## Files
- `products_FINAL.csv` — the rebuilt import file (review, then promote to Ready_For_Import).
- `BUILD_dropped.csv` — 94 dropped SKUs + reason.
- `BUILD_photos_needed_kept.csv` — 326 kept SKUs still on a wrong/family image.
- `pricing_resolution.csv` — full per-SKU price resolution + source.
- `needs_nsl_pairing.csv` — 15 to pair to NSL codes.
