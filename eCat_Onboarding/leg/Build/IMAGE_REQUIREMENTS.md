# Legrand Image Strategy

## Decision: FTP Upload (no CDN integration available)

eCat stores images on S3 via Paperclip and serves them through its own Fastly CDN.
There is NO mechanism to reference external URLs as image sources.
Images must be downloaded from Legrand's distributor CDN and re-uploaded via FTP.

## Source

- **CDN:** `media.distributordatasolutions.com/legrand_synd/2025q4/images/large/`
- **Format:** PNG
- **Coverage:** 1001 of 1020 products have images (98%)
- **Depth:** Avg 8.4 images per product (capped to 6 for eCat default limit)

## Workflow

1. Run `download_images.py` to batch-download and rename images:
   ```
   python3 download_images.py              # full download (~4836 files)
   python3 download_images.py --limit 100  # test with first 100
   python3 download_images.py --dry-run    # preview only
   ```

2. Images are saved to `./images/` as `{ItemID}.jpg`, `{ItemID}_2.jpg`, etc.

3. Upload to FTP `/images` in batches of 500 (30-45 min processing per batch):
   - Batch 1: items starting A-D
   - Batch 2: items starting E-R
   - etc.

4. After upload, run Admin Console: Tools > Import Images > Product Photos

## File Naming Convention

| Image | Filename |
|-------|----------|
| Primary | `{BaseItemCode}.jpg` |
| Alternate 2 | `{BaseItemCode}_2.jpg` |
| Alternate 3 | `{BaseItemCode}_3.jpg` |
| ... up to 6 | `{BaseItemCode}_6.jpg` |

## Stats

- Total image files: ~4,836 (4,816 verified on disk across `images/` + the
  `images_batch_0X_NEW/` folders — merge these into `images/` before FTP upload)
- FTP batches needed: ~10 (at 500/batch)
- Products with multiple images: 937
- Products with single image: 83
- Products with NO images (20): `ImageFileName` is left **blank** for these in
  `products.csv` (fixed 2026-07-14 — a prior build guessed a `{code}.jpg`
  filename for these instead, which pointed at a file that doesn't exist on
  disk). They'll show the iPad's placeholder either way; blank is just honest
  about it. Codes: `ARPTR152GW2`, `AFGF152TR`, `AFGF152TRBK`, `AFGF152TRI`,
  `AFGF152TRLA`, `AFGF152TRW`, `AFGF202TR`, `AFGF202TRBK`, `AFGF202TRGRY`,
  `AFGF202TRI`, `AFGF202TRLA`, `HMKITBK`, `1597TRBK`, `1597TRUSBAA`,
  `1597TRUSBCCI`, `1597TRUSBCCLA`, `1597TRWRUSBCCBK`, `1597TRWRUSBCCW`,
  `R26USBPD65WCC6`, `3894`. Confirm with Legrand whether real images exist for
  these before going live.

## Note on PNG format

The source images are PNG. eCat validates content_type for `image/png` in addition
to `image/jpeg`, so PNG files with a `.jpg` extension will still upload successfully.
However, if this causes issues, add `--convert-to-jpg` flag to download_images.py
(requires Pillow: `pip3 install Pillow`).
