# CopperSmith — Source Column → eCat Field Mapping

Source of truth: **June 2026 UPDATE** master files in `~/Downloads/CS_Master_Product_List_June_2026_UPDATE/` plus `~/Downloads/eCat Image Corrections.csv`.

This document is for Jordan: where each imported value appears on the iPad.

---

## Lantern & Weiyan products (`products.csv`)

| Source column (Master / Weiyan tab) | eCat CSV column | iPad display |
|-------------------------------------|-----------------|--------------|
| `Retailer Product Name` | `LongDesc` (≤255 chars) | **Catalog title** — full product name in grid, list, and order line |
| **`Short Description`** | **`ShortDesc` (≤255 chars)** | **Subtitle under SKU** on configure / quick-view screens (full sentence, not a 15-char fragment) |
| `Marketing Copy` | `MarketingCopy` (custom field) | Admin / reporting; not the main catalog title |
| `Marketing Copy` (BU) + `Long Description` (BT) + `Feature 1`–`Feature 6` | `stories.csv` → `ProductStory` | **Product detail** romance copy: product marketing, then collection history, then bullet features |
| `Main Image File Link` (+ RA views 1–7, finish views) | `ImageFileName` | Primary product photo(s); CDN downloads on import |
| `Material` | `materials` | Spec / detail fields |
| Height/Width/Depth (inches) | `dimensions` | Spec sheet style dimensions string |
| `Shipping Weight (lbs)` / `Weight` | `shipweight` | Shipping weight |
| `UPC` / `UPC/GTIN` | `UPCValue` | Barcode / UPC field |
| `Dealer Net` | `NetPrice` | Net pricing level |
| `MAP/ IMAP` | `Price_MAP` | MAP pricing level |
| `MSRP/ List Price` | `Price_MSRP` | List/MSRP pricing level |
| `Primary Genre/ Style`, `Fixture Type` / Weiyan `Fixture Style` | `Genre`, `Subcategory` | Filtering / taxonomy helpers |
| `Power Source` | `GasElectricDual` | Electric vs gas label |
| Bulb, wattage, voltage, compliance columns | Same-named product columns | Spec / compliance blocks on detail |
| `Spec Sheet URL` | `SpecSheet` | Linked spec sheet |
| `Installation` | `Installation` | Installation notes / link |
| `Warranty`, `Country of Origin`, `Product Tags` | Same-named columns | Detail / tags |

**Weiyan LED tab** uses the same mapping; genre/subcategory reads `Fixture Style` where noted in the sync script.

---

## Accessory product rows (`products.csv`)

| Source column (Accessories tab) | eCat CSV column | iPad display |
|---------------------------------|-----------------|--------------|
| `Accessory Name` | `LongDesc` (50) / `ShortDesc` (15) | Accessory catalog name and configure subtitle |
| `Accessory Image Link` | `ImageFileName` | Accessory product photo (blank link → no image) |
| `Accessory GTIN` | `UPCValue` | UPC |
| `Accessory Application Link` | `Installation` | Install / application PDF link |
| `Accessory Dealer Net` / `MAP` / `MSRP` | `NetPrice` / `Price_MAP` / `Price_MSRP` | Pricing |

---

## Parts product rows (`products.csv`)

| Source column (Parts tab) | eCat CSV column | iPad display |
|---------------------------|-----------------|--------------|
| Column 3 (part name) | `LongDesc` / `ShortDesc` | Parts catalog name |
| Column 10 (image link) | `ImageFileName` | Part image (blank → no image) |
| GTIN / net / MAP / MSRP columns | `UPCValue`, price columns | Pricing & identification |

---

## Options (`options.csv`)

| Source | eCat column | iPad display |
|--------|-------------|--------------|
| Accessories tab `Accessory Image Link` (by `Accessory SKU` = option `Code`) | `ImageName` | **Finish / accessory swatch** on configure screen |
| `eCat Image Corrections.csv` | `ImageName` | Override when listed (HSI1/2, PF1–7, WY, etc.) |
| Blank source link | blank `ImageName` | No swatch (parent options BMPM, CHB, PFA, etc.) |

**Only `.jpg`/`.jpeg` HTTPS URLs CDN-sync** on import. PNG sources do NOT (see below) — the sync rewrites every `.png` link to a plain `{basename}.jpg` filename that must be FTP'd to `/option_images` (options) or `/images` (products).

---

## Option section layout (`OptionSet1`–`OptionSet8` → iPad configure screen)

Each `OptionSetN` column on a product points at an **option group** (from `option_groups.csv`); on the iPad each populated set renders as its own collapsible section, in order, with the heading set by the Admin Console **Option Type label** for that slot.

| products.csv column | Option Type label (Admin) | iPad section |
|---------------------|---------------------------|--------------|
| `OptionSet1` | Finish | **Finish** swatches |
| `OptionSet2` | Wall Mount | **Wall Mount** hardware |
| `OptionSet3` | Ceiling Mount | **Ceiling Mount** hardware |
| `OptionSet4` | Post & Pier Mount | **Post & Pier Mount** hardware |
| `OptionSet5` | Wall Accessories | **Wall Accessories** |
| `OptionSet6` | Decorative Accessories | **Decorative Accessories** |
| `OptionSet7` | Electric Options | **Electric Options** |
| `OptionSet8` | Gas Options | **Gas Options** |

The three mount families are **separate sections** (not a "Mount Type" picker). There is no `MT_*` group and no `WALL/CEIL/POST` option — those were removed. A product only fills the mount sets it actually offers, so reps see only relevant sections.

---

## Image delivery: `.jpg` URL (CDN) vs PNG (convert + FTP)

`CdnImageSync` (`supercat_server/app/services/cdn_image_sync.rb`) only downloads an
image when the derived filename ends in `.jpg`/`.jpeg` **and** the URL returns
`Content-Type: image/jpeg`. **PNG fails both checks** — the option/product silently
keeps pointing at a `Foo.png` that never downloads (root cause of the "very old / wrong
image" complaints). CopperSmith's source images for ~71 codes exist only as PNG.

So the pipeline splits image refs two ways:

- **`.jpg` HTTPS URL** → left as-is in the CSV; eCat CDN-downloads it on import. No FTP.
- **`.png` source** → `sync_from_june_source.py` rewrites it to a plain `{basename}.jpg`
  filename. `build_jpg_images.py` downloads the PNG, `sips`-converts it to JPG, and stages
  it in `images_upload/` (products) / `option_images_upload/` (options). Those JPGs are
  FTP'd to `/images` / `/option_images` (`upload_image_fixes.sh images`), then applied via
  Admin → Tools → Import Images.

Dead links handled via override maps in the sync script: `PFP*` (403 everywhere → blank,
pending Jordan), `COY12/13` (bare filename → working COY URL), `TE20E` (recovered from PNG),
`CS43E` (recovered working JPG URL).

---

## Image authority (all SKUs and option codes)

1. **Corrections sheet** → use URL exactly (blank entry clears image)
2. **Accessories tab** → `Accessory Image Link` exactly (blank clears)
3. **Master / Weiyan** → `Main Image File Link` (+ additional views per sync)
4. **Parts tab** → parts image link (blank clears)
5. Never inherit sibling/parent images
6. Any `.png` from sources 1–4 is converted to JPG + FTP'd (CDN can't take PNG)

After CDN sync, Admin and Postgres show the **downloaded basename** (e.g. `Finishes_BLK.jpg`).
Converted PNGs show as the FTP'd `{basename}.jpg` (e.g. `VNG.jpg`, never `VNG.png`).

---

## Three name fields (common confusion)

| Field | File | iPad role |
|-------|------|-----------|
| `LongDesc` | `products.csv` | Main product name in catalog |
| `ShortDesc` | `products.csv` | Short line under SKU on configure |
| `ProductStory` | `stories.csv` | Long marketing description on detail page |

`Long Description` (BT) from the master sheet is **not** used for the `LongDesc` catalog title (that's the `Retailer Product Name`). BT is the collection romance/history and now always feeds `ProductStory`, placed after the `Marketing Copy` paragraph.

**eCat field lengths (verified against the importer):** `long_description`, `short_description`, and `plist_description` are all `varchar(255)` — the importer only warns + truncates past 255, never errors. The earlier "max 50 / max 15" caps were incorrect and caused mid-word truncation (e.g. `ShortDesc = "Handcrafted sol"`).

---

## Regenerating import files

```bash
python3 sync_from_june_source.py   # sync from June UPDATE paths
python3 validate_source_truth.py   # must print VALIDATION PASSED
```

Change log for Jordan: `SOURCE_SYNC_CHANGELOG.md`.
