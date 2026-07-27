---
name: ecat-images-ftp
description: Upload and assign eCat iPad product and option images via FTP, normalize filenames, and troubleshoot missing images. Use when images aren't showing on the iPad, assigning ImageFileName, uploading to FTP /images or /option_images, or diagnosing missing/extra images.
---

# eCat Images & FTP (iPad)

## The two-step model

An image only shows when BOTH are true: (1) the file is uploaded and processed, and
(2) `ImageFileName` (products.csv) or `ImageName` (options.csv) matches the filename
**exactly**. Re-uploading images alone fixes a missing image — no product re-import
needed if the filename already matches.

## FTP folders

| Asset | Folder | Spec |
|-------|--------|------|
| Product images | `/images` — **flat root only; subfolders are ignored** | `.jpg` lowercase, sRGB, ≤6 (or 12), primary first |
| Option swatches | `/option_images` | square **300×300**, default name `{code}.jpg` |
| CSV files | `/data` | — |

- Processed files are **deleted from FTP on success** (looks like data loss; it's not).
- ≤500 images/batch, ≤15 MB each, **30–45 min** processing. Then iPad sync (close/
  reopen or pull-to-refresh).
- Admin one-offs: Tools → Import Images → Product Photos / Option Photo.

## Filename normalization (match CSV exactly)

- No spaces (use `_`), no punctuation except `-`/`_`, no dots inside names (`Alu.`→`Alu`).
- `+` → `-`; `.JPG` → `.jpg`. Case-sensitive match.
- Strip WordPress size suffixes: `photo-300x300.jpg` → `photo.jpg`.
- Files < ~500 bytes are usually 404 error pages, not images.

## Troubleshooting

| Tool / signal | Meaning |
|---------------|---------|
| `/{shortname}/tools/missing_images` | products referencing a not-yet-imported filename |
| `/{shortname}/tools/extra_images` | imported images not tied to an active product (often a filename mismatch) |
| File Import Status | confirms what processed and when |
| Postgres `image_exists` / `image_digests` | consultant-only ground truth |

Common causes: images dropped in subfolders under `/images`; filename ≠ CSV (case/
spaces/typo); client edited an old local CSV instead of the current `/data` copy.

## Hero image discipline

Image 1 must be the product cutout on white — never a lifestyle/room shot. When you
find one wrong hero, audit ALL products (the root cause always affects many).
