# Pebl (pebl) — Option Import Package

**Generated:** 2026-05-28  
**Org:** Skyard furniture Co Ltd. (`pebl`)

## Import order (critical — do not reorder)

1. **`options.csv`** → FTP `/data/options.csv` → Admin Console import **Options**
2. **`option_groups.csv`** → FTP `/data/option_groups.csv` → import **Option Groups**
3. **`products.csv`** → FTP `/data/products.csv` → import **Products**
4. **Option Mapping** → Admin Console **Products → Option Mappings** (see `option_mappings_spec.json`)  
   - Or apply via DB update if already done by SuperCat support

Wait for each import to finish before starting the next. After all imports, trigger an iPad catalog sync on Wi‑Fi.

## What changed

### options.csv
- Renamed 3 codes that exceeded the 15-character limit (import was failing):
  - `DGREEN_GLAZED_CER` → `DGREEN_GLAZ_CER`
  - `WBROWN_GLAZED_CER` → `WBROWN_GLAZ_CER`
  - `OCHRE_GLAZED_CER` → `OCHRE_GLAZ_CER`

### option_groups.csv
- Kept all 24 existing Haven/Wave groups unchanged
- Added **38 new groups** for new collections (frame colors, ceramics, cushions)
- Applied **PriceAddend** on groups (not matrix options):
  - `MT_W150_SAND` = -70
  - `MT_W100_SAND` = -16
  - `MT_ALB_SAND` = -32
  - `CU_NPT_UV931` = -50
  - `CU_ALU_SLG_SJ` = +10

### products.csv
- Removed all `FRAMECOLOR` / `MATCOLOR` / `CUSHFABRIC` placeholders
- Set explicit option group codes per product per Mandy's mapping spreadsheet
- Fixed products that had OptionSet2/3 required but no groups defined (Hilo, Bistro, Albatros, etc.)

### Option Mapping
- Extended Admin Console mapping for new frame colors: Olive Green, Teak, Dark Brown (Tube ceramic)
- Product OptionSets narrow which groups appear; mapping controls frame → material/cushion cascade

## Assumptions (confirm with client)

See `option_mappings_spec.json` → `assumptions` array.

## Files in this folder

| File | Purpose |
|------|---------|
| `options.csv` | Option values + swatch image filenames |
| `option_groups.csv` | Option groups + price addends |
| `products.csv` | Product catalog with corrected OptionSet columns |
| `option_mappings_spec.json` | Admin Console Option Mapping reference |
| `ecat-options mapping.xlsx` | Client's source mapping document |
