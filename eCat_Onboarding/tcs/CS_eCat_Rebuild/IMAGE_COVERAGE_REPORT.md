# eCat Image Coverage & Scrape Report — CopperSmith (org 291)

Generated from the June 2026 source workbook vs. the live org. All filenames lowercased per FTP convention.

## TL;DR

| Bucket | Count | Source has URL? | Action |
|---|---|---|---|
| Gas/electric products already imaged (live) | 255 | yes (S3) | none — already on iPad |
| Gas/electric products **missing** image (live) | **16** | yes (S3) | **DOWNLOADED → upload to `/images`** |
| Weiyan LED products | **96** | **NO** | **client must supply images** |
| Option swatches already pointed at a live file | 8 | n/a | kept |
| Option codes re-pointed to an existing live swatch | **163** | n/a (reuse) | **fixed in `options.csv`** |
| Option codes flagged for review | 35 | n/a | review `option_swatch_map.csv` |
| Option codes with no existing swatch | 125 | NO | optional upload (mount hardware) |

The new source workbook only carries **direct image URLs for the gas/electric line** (Master Sheet col `Main Image File Link`, S3/catsy). The **Weiyan tab's image-link column is empty**, and the `Image Family Links` tab only has **Dropbox/Google-Drive folder links** (not auto-scrapeable). So scraping fills the 16 real product gaps but cannot fill Weiyan or option swatches.

## 1. Product images — DONE (16 of 16)

These were the only live products with `image_exists = false`. Pulled from the Master Sheet S3 links, validated as JPEG, staged in `images_to_upload/`:

`16wst, 16wsth, 9wst, 9wsth, ah36e, ah36g, hl15e, hl15g, hl18e, hl18g, hl21e, hl21g, hl30e, hl30g, mo29e, mo29g`

→ **Upload `images_to_upload/*.jpg` to FTP `/images` (flat root)**, then Admin → Tools → Import Images → Product Photos. ~30–45 min processing, then verify in File Import Status.

## 2. Weiyan LED (96) — BLOCKED, needs client

No image URLs anywhere in the Weiyan tab. Full list with expected filenames in **`weiyan_images_needed.csv`**. Send to client and ask for either direct image files named `{sku}.jpg` or a flat folder. Until then the 96 Weiyan SKUs import as data-only (no photo).

## 3. Option swatches — reused existing library

The live option library already holds generic family swatches (`gnp.jpg`, `cy.jpg`, `chm.jpg`, `chb.jpg`, `bs.jpg`, `ts.jpg`, finishes, etc.), but the rebuilt `options.csv` left `ImageName` blank on the mount/decorative codes — so those swatches existed but never rendered.

- **163 codes** re-pointed to the matching existing swatch (high confidence) — now render with **no new uploads**.
- **35 codes** flagged (medium confidence or an existing reference whose file is missing live, e.g. `ADS.jpg`, `CSHI.jpg`) — see `option_swatch_map.csv`.
- **125 codes** (Biltmore variants `BM*`, lamp posts `CSP*`, `WY`, `CLEAR`, `GH1/2`, post fitters, etc.) have no existing swatch — optional client uploads; they otherwise show no thumbnail (acceptable for mount hardware).

Every change is logged in **`option_swatch_map.csv`** (Code, CurrentImageName, ProposedImageName, SwatchExistsLive, Confidence, Action) — fully reversible.

## 4. Not scraped (by design)

- `Image Family Links` tab → Dropbox/GDrive **folder** links, require auth/manual export.
- Accessories tab S3 links → bulbs/parts/kits, not part of the current 367-product build.
- The 255 already-imaged products → not re-downloaded (avoids an unnecessary full image reset).

## Files produced
- `images_to_upload/` — 16 product JPEGs ready for `/images`
- `weiyan_images_needed.csv` — 96 SKUs to request from client
- `option_swatch_map.csv` — full swatch mapping/audit
- `options.csv` — updated with 163 swatch assignments
