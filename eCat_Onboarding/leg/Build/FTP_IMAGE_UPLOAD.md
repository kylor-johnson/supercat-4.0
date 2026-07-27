# Legrand — FTP image upload (missing batch)

Generated 2026-07-24.

## What was prepared
- **155** live no-image SKUs now have verified CDN downloads + `ImageFileName` in `products.csv`
- **613** JPG files staged (primary + up to 5 alts, eCat max 6)
- **20** SKUs still have blank `ImageFileName` (no usable image URL in Image Files sheet)

## Upload (you)
1. FTP flat into `/images` (no subfolders):
   - `images_ftp_batch_01/` → 500 files
   - `images_ftp_batch_02/` → 113 files
   - Or upload all of `images_missing_batch/` (613 files) in ≤500/batch
2. Wait **30–45 min** per batch for processing
3. Admin → Tools → Import Images → Product Photos is alternative; FTP is fine
4. Import `products.csv` to `/data` (after or with images — `ImageFileName` must match filenames exactly)
5. Check Admin Reports → File Import Status, then `/{shortname}/tools/missing_images`

## Still need links from Legrand (20)
See `missing_images_gap_final.txt`:
- 1597TRBK
- 1597TRUSBAA
- 1597TRUSBCCI
- 1597TRUSBCCLA
- 1597TRWRUSBCCBK
- 1597TRWRUSBCCW
- 3894
- AFGF152TR
- AFGF152TRBK
- AFGF152TRI
- AFGF152TRLA
- AFGF152TRW
- AFGF202TR
- AFGF202TRBK
- AFGF202TRGRY
- AFGF202TRI
- AFGF202TRLA
- ARPTR152GW2
- HMKITBK
- R26USBPD65WCC6

Notes:
- `HMKITBK` only has a YouTube embed on the Image Files sheet (not a product photo).
- The other 19 match Trey’s “still need links” list (AFGF*, 1597TR*, 3894, ARPTR152GW2, R26USBPD65WCC6).
