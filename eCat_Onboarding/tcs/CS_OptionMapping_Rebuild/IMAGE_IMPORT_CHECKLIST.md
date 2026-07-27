# Image Fix Import Checklist (tcs, org 291)

Files ready in this folder after `sync_from_june_source.py` + `validate_source_truth.py` (must pass).

## Pre-import

- [ ] Run `python3 validate_source_truth.py` — must print `VALIDATION PASSED`
- [ ] Review [SOURCE_SYNC_CHANGELOG.md](SOURCE_SYNC_CHANGELOG.md) (753 logged changes)
- [ ] Share [FIELD_MAPPING.md](FIELD_MAPPING.md) with Jordan

## FTP upload order

Upload to `/data/` on org FTP (`tcs`):

1. `options.csv`
2. `option_groups.csv`
3. `products.csv`
4. `stories.csv` (optional but recommended for LL-TUBE6A/8A + CHSI renames)

Wait ~2 min between files. Check **Tools → Admin Reports → File Import Status** after each — all must be clean (warnings OK, no errors).

```bash
cd "CS_OptionMapping_Rebuild"
FTP_PASS='...' ./upload_image_fixes.sh   # password from Admin Console → Company Settings
```

## Post-import verification

### Admin Console

- File Import Status: all four files green
- Import event log: **Option Downloads** and **Product Downloads** entries from CDN sync (new Catsy URLs)

### iPad spot-check (after full sync)

| SKU | Expected |
|-----|----------|
| `VNG50FH` | Blank image (no double-burner) |
| `VNG` | Single-burner (`VNG.png`) |
| `GH1-GPF` / `GH2-GPF` | Distinct GPF images (not PF bracket) |
| `HSI1` / `HSI2` | Different shade images |
| `CHSI` | Cylinder Hammered Shade (replaces CSHI) |
| `LL-TUBE6A` / `LL-TUBE8A` | Tube bulb images (old LL-TUBE6/8 gone) |

### Postgres spot-check (org_id 291)

```sql
-- Accessory product images (CDN sync stores basename in images_json)
SELECT item_number,
       images_json->0->>'file_name' AS primary_image,
       deleted
FROM products
WHERE organization_id = 291
  AND item_number IN ('VNG','VNG50FH','GH1-GPF','GH2-GPF','HSI1','HSI2','CHSI','CSHI','LL-TUBE6A','LL-TUBE8A','LL-TUBE6','LL-TUBE8')
ORDER BY item_number;

-- Option swatches
SELECT code, image_name
FROM options
WHERE organization_id = 291
  AND code IN ('CHSI','CSHI','HSI1','HSI2','WY','HSCM','PF1','BMPM','CHB','PFA')
ORDER BY code;

-- Recent imports (File Import Status source of truth)
SELECT created_at, left(data, 2000) AS data
FROM import_events
WHERE organization_id = 291
ORDER BY created_at DESC
LIMIT 8;
```

Run `python3 verify_post_import.py` for the full expected-value checklist.

Expected post-import: `VNG50FH` blank; `VNG` → `VNG.png`; parent options (`BMPM`, `CHB`, `PFA`) blank; `CHSI` exists; `CSHI` gone; `LL-TUBE6A`/`LL-TUBE8A` replace old tube SKUs; finish swatches CDN (`BLK` → `Finishes_BLK.jpg`); `ShortDesc` under SKU matches source (e.g. AM29E → `Handcrafted sol`).

Pre-import live baseline: [PRE_IMPORT_BASELINE.md](PRE_IMPORT_BASELINE.md).

## Client reply (Jordan Q4)

Images are imported from Catsy URLs in our CSV files via CDN sync — not pulled live on every view. Admin shows the cached internal filename (e.g. `VNG.png`) after download. Import-managed product images cannot be swapped in Admin; we update the CSV and re-import.
