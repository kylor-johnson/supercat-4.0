# Magic Lite (mali) — Catalogue-vs-Product-File Image & Relationship Audit — HANDOFF

**Created:** 2026-07-24 by prior agent · **For:** fresh agent, clean context
**Bar:** This has been wrong before. Do not guess. Prove every hero image against the
catalogue PDF. When you can't prove it, flag it — do not invent.

---

## 0. Your job (the whole ask, in one paragraph)

Compare the **entire** Magic Lite product file against the **May 2025 Product Catalogue**
(the client's own source of truth) and make every **visible** product show the correct
**clean hero image**, with correct **relationships** (variants/accessories relate to the
right hero). The relate/hide/unhide structural pass is already DONE and live (218 visible
/ 465 hidden, verified). What remains is an **image-content audit**: many visible heroes
currently display a lifestyle room-shot, a spec-callout graphic, a dimension line-drawing,
a blank, or a multi-finish family array instead of a clean single-product photo. Fix those
by sourcing the clean hero from the catalogue, plus sanity-check relationships against the
catalogue's product groupings.

---

## 1. Source of truth (in priority order)

1. **Catalogue PDF** (authoritative for hero image, families, relationships, structure):
   `_MALI_FIX_REVIEW/catalogue/ML_Catalogue_May2025.pdf` (92 pages, 18MB)
   - Also mirrored as text: uploads `Magic-Lite-Catalogue_May-2025.pdf-0.md`
     (7806 lines; Appendix/item-locations start ~line 7739).
2. **magiclite.com** product pages (secondary; use `curl` via `https://r.jina.ai/` proxy to
   beat Cloudflare) — only when the catalogue image is ambiguous.
3. **Product file being edited (LIVE working file):**
   `02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv`
   - 683 rows · 218 visible (`Hideable` != Y) · 465 hidden.
   - Header/columns confirmed; hero-relevant columns: `BaseItemCode`, `ShortDesc`,
     `Hideable`, `ImageFileName`, `RelatedItems`.
4. Baseline for diffing: `/Users/kylorjohnson/Downloads/products.csv.20260723-2122.csv`.

Everything else in `_MALI_FIX_REVIEW/` is prior-pass reference (proposals, changelogs).

---

## 2. Critical mechanics you MUST understand before touching anything

### 2a. How the iPad picks the hero
- `ImageFileName` is **comma-separated, primary first**: `SKU.jpg,SKU-2.jpg,SKU-3.jpg`.
- The iPad grid **hero = the FIRST filename**.
- Images live on **FTP `/images` (flat root only — subfolders ignored)**. On import the
  app matches `ImageFileName` to the uploaded file by **exact name**.

### 2b. THE KEY INSIGHT — most fixes need NO CSV edit
The wrong heroes almost all have a filename that already equals the SKU
(e.g. `LEDLB-5CCT-12.jpg`). **The filename is right; the picture inside the file is wrong.**
So the fix is usually: **produce the correct clean JPG under the same filename and re-upload
to `/images`.** No products.csv change.

Only edit `products.csv` `ImageFileName` when:
- you want a size-family to **share one** clean hero file (e.g. point all `GDL` sizes at
  one gimbal photo), or
- the current filename is genuinely wrong/missing.

Only edit `RelatedItems` when the catalogue shows a variant/accessory that isn't related.
`RelatedItems` is comma-separated, **hard cap 255 chars** — see guardrails.

### 2c. Extraction method that WORKS (proven this session)
Render any catalogue page to PNG with PyMuPDF and read it:
```python
import fitz
d = fitz.open('catalogue/ML_Catalogue_May2025.pdf')
d[IDX].get_pixmap(dpi=110).save(f'catalogue/page_{IDX:03d}.png')   # then Read the PNG
```
- **PDF page INDEX != printed page number.** Find pages by text, but the FIRST text hit is
  often a selection-guide/replacement-chart/appendix mention, NOT the product's main page.
  Verify visually. (Confirmed good renders this session: idx 29=LEDLB task bar,
  60=Gimbal, 66=DL-FR fire-rated thin line, 67=RGL-FR regressed.)
- To get a clean cut-out hero, either (a) extract embedded raster images on that page
  (`page.get_images()` / `doc.extract_image(xref)`) and pick the product one, or
  (b) crop the rendered PNG. Then save as **sRGB `.jpg`, lowercase-safe name, primary-first**.
- Catalogue pages cleanly separate: **hero product photo** vs **lifestyle room shot** vs
  **dimension DIAGRAM (line art)** vs **accessory thumbnails**. Only the hero product photo
  is a valid hero.

---

## 3. Confirmed wrong/weak VISIBLE heroes (already diagnosed — start here)

Verified against rendered catalogue pages. "Fix type" = file-swap (same filename) unless noted.

| SKU(s) | Showing now (wrong) | Correct hero | Cat. printed pg | Fix type |
|---|---|---|---|---|
| `LEDLB-5CCT-12`, `-18`, `-24` | kitchen lifestyle | clean white task bar (as `-10` has) | 55 | file-swap (or repoint to `LEDLB-5CCT-10.jpg`) |
| `DL-FR-5CCT-4-WH`, `-6-WH` | bathroom lifestyle | red fire-rated downlight | 129 | file-swap |
| `RGL-FR-5CCT-4-WH`, `-6-WH` | flame "2-HOUR" graphic | red regressed downlight | 131 | file-swap |
| `GDL-3-8W-38-CCT-WH` | dimension line-drawing | white gimbal (as `GDL-4` has) | 117 | file-swap or repoint to `GDL-4-14W-38-CCT-WH.jpg` |
| `GDL-6-18W-38-CCT-WH` | dimension line-drawing | white gimbal | 117 | file-swap or repoint |
| `MLDR-120-24` | old/wrong shot | driver photo — **already staged** at `catA_images/MLDR-120-24.jpg` | 143+ | UPLOAD staged file |
| `LTSPRO-SW-09/12/18/24/32/40-WH` | "USB/USB-C port" spec graphic | clean swivel task-light photo | 53 | file-swap |
| `LTSPRO-32-WH`, `-40-WH` | 4-finish family array | single white unit | 51 | file-swap |
| `LV-DL-EX-10-L`, `-30-L` | blank | interconnection-cable photo | — | **likely CLIENT PHOTO** (not in catalogue) |
| `LV-RF103`, `LT-11S-RF`, `LV-SPIR-1CH-LV`, `LV-ZJFFS-3CH-6INW` | shared "controller-box stack" marketing shot | individual controller/remote photo | 143+ | file-swap if catalogue has it, else CLIENT PHOTO |

Everything else visible in the 2026-07-24 iPad screenshots (strips, extrusions, floods, disc
markers, downlights, wall washers, well lights, drivers, connectors, step cords) was a
legitimate clean product photo — leave alone unless the full audit says otherwise.

---

## 4. Do the FULL audit (all 218 visible heroes) — required, "cannot be wrong again"

Do not stop at Section 3. Go through **every** visible product:

1. Build the visible list from `products.csv` (`Hideable != Y`).
2. Group into families by SKU stem + `ShortDesc` (e.g. all `GDL-*`, all `DL-FR-*`).
3. For each family, find its catalogue page (render + view). Identify the ONE clean hero
   product photo.
4. For each visible SKU, decide: is its current hero the clean product photo? If it's a
   lifestyle/graphic/diagram/blank/family-array → queue a fix.
5. Cross-check relationships: does the catalogue show accessories/variants (trim rings,
   jumpers, cords, beauty rings, construction plates, finishes, CCT/wattage variants) that
   should be in the hero's `RelatedItems`? Queue relate fixes (respect the 255 cap).
6. Produce a single decision CSV: `SKU, family, current_hero_kind, verdict, fix_type,
   correct_image_source (cat page / client), relate_changes, reason`.

Reference for families→pages: catalogue Appendix (md ~line 7739) + "Product Categories at a
Glance" (md ~line 45). Under-cabinet 49–63, Down Lighting 107–131, Landscape 65–105,
Linear 3–47, Industrial 133, Drivers/Controllers 143–168, Tokistar 169+.

---

## 5. Guardrails (NON-NEGOTIABLE — validate before every write)

- **Backup first:** copy `products.csv` to a timestamped backup before any write.
- **SKU set must not change:** 683 rows in == 683 rows out; no added/dropped `BaseItemCode`.
- **0 duplicate `BaseItemCode`.**
- **`RelatedItems` <= 255 chars** per row, and **no dangling refs** (every related code must
  exist as a `BaseItemCode`). If adding a relate overflows 255, rebalance (drop a redundant
  cross-size ref) or leave the item visible instead of forcing it — do NOT truncate mid-code.
- **Never unhide/hide** as part of the image pass unless the catalogue clearly demands it;
  the structural pass is done. Image fixes should be image-only where possible.
- **Dry-run then write:** reuse `apply_changes.py` pattern (has dry-run + validation).
  Re-run `verify_state.py` after writing; expect `VALIDATION ERRORS: 0`.
- **Do not create random backup files** scattered around; keep outputs in `_MALI_FIX_REVIEW/`.
- **Images:** `.jpg`, lowercase extension, sRGB, name = exact `ImageFileName` entry,
  primary first, <=15MB, <=500/batch. FTP `/images` **flat** (no subfolders).

---

## 6. Current state / what's already DONE (do NOT redo)

- Structural relate/hide/unhide pass applied & verified: **218 visible / 465 hidden / 70
  orphaned-hidden / 0 validation errors**. Shared-hero clusters among visible dropped to
  ~14 clusters / 44 products (down from 19/57), and remaining shares are legit same-family.
- 5 corrected images **staged but NOT yet uploaded** in `catA_images/`:
  `ACC-TM-BLK.jpg`, `DD-2460-S-WH.jpg`, `DD-24100-S-WH.jpg`, `MLDR-120-24.jpg`,
  `NFLX-RGB-CHANNEL.jpg`. **These still need FTP upload + import.**
- Hero audit script exists: `hero_image_audit.py` (own-named vs borrowed image check).
- Prior proposals/changelogs: `PROPOSAL_01/02/03_*.csv`, `FIX_CHANGELOG_2026-07-24.csv`,
  `MALI_PRODUCT_REVIEW_2026-07-24.md` (append your pass; don't overwrite).
- Known-bad to avoid: don't re-point NFLX heroes' RelatedItems (already at 244–253 chars,
  full); `NFLX-RGB-CHANNEL` intentionally kept VISIBLE with corrected image.

---

## 7. Deliverables for this pass

1. `CATALOGUE_HERO_AUDIT_<date>.csv` — every visible SKU, verdict, correct image source.
2. Staged corrected JPGs in `catA_images/` (SKU-named, sRGB), extracted from catalogue.
3. `FTP_UPLOAD_LIST_<date>.txt` — exact filenames to drop in `/images` (incl. the 5 already
   staged).
4. `CLIENT_PHOTO_NEEDED_<date>.csv` — SKUs with no clean catalogue image (e.g. `LV-DL-EX`
   cables, some individual controllers) — flag, do NOT guess.
5. If any `ImageFileName`/`RelatedItems` repoints are needed: apply to `products.csv` (backup
   + dry-run + `verify_state.py` clean), regenerate a FIX_CHANGELOG, append to the review MD.
6. Owner instructions: which files to upload to FTP `/images`, then re-import `products.csv`
   (only if CSV changed) via Admin → Tools → Import Data, then verify Admin → Admin Reports →
   **File Import Status** (blue-link timestamp = errors; Fatal rejects file, Error skips
   deletes). Product-image processing takes 30–45 min.

---

## 8. First 15 minutes (suggested)

1. `verify_state.py` → confirm 218/465/0-errors baseline still holds.
2. Render the Section-3 pages you haven't seen (LTSPRO 51/53, drivers/controllers 143+) and
   confirm the correct heroes.
3. Extract + stage the Section-3 clean heroes as SKU-named JPGs.
4. Then begin the full family-by-family sweep (Section 4), one category at a time.
5. Present the audit CSV for approval before applying any products.csv repoints.
