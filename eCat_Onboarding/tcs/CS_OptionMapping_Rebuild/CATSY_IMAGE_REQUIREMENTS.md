# CopperSmith — Image Requirements for FTP-Free (CDN) Updates

**Goal:** let CopperSmith update product/option images by changing them **on Catsy**, with
the new image flowing into eCat automatically on the next data sync — **no FTP step**.

## How eCat images work today

eCat already pulls images straight from your Catsy CDN links. When a product/option row's
image link is a Catsy URL, eCat downloads it on import and re-pulls it when the Catsy file
changes. **That is the CDN integration — it's already on.** There is no separate FTP upload
for CDN images. FTP is only a *fallback* we use for images Catsy serves in a form eCat can't
accept.

## The 3 rules an image must meet to auto-pull from Catsy

For eCat to CDN-pull a link with no FTP, the image must be:

1. **A `.jpg` / `.jpeg`** — not `.png`. (eCat rejects PNG: wrong extension and non
   `image/jpeg` content type.)
2. **Served as `image/jpeg`** content-type (normal for a real `.jpg` on Catsy).
3. **A clean filename** — letters, numbers, `.`, `-`, `_` only. **No** parentheses `()`,
   **no** spaces, **no** `+`, **no** `%`, **no** `/` in the filename.
   - eCat's image-filename rule explicitly forbids `(` `)` `/`, and spaces/`+`/`%` break the
     served image URL.
   - Example that FAILS: `ES-63(FGPFPC8P2-10FT).jpg`, `wide+top.jpg`, `GT20W (LA).jpg`
   - Example that WORKS: `ES-63_FGPFPC8P2-10FT.jpg`, `wide-top.jpg`, `GT20W-LA.jpg`

A 4th, softer one: keep images free of corrupt embedded XMP metadata — a malformed XMP
profile makes eCat's thumbnail generator reject the image. (On our converted copies we strip
all metadata automatically.)

## What's currently non-compliant (and how we handled it for now)

Two classes of Catsy assets don't meet the rules, so they can't CDN-pull:

- **PNG renders** (~handful of product/option codes saved as `.png`).
- **`.jpg` files with parentheses / spaces / `+` in the filename** (~26 unique source
  images, e.g. the `BMTS*` Top Scroll swatch `wide+top.jpg`, the lamp-post images
  `ES-63(FGPFPC8P2-10FT).jpg` / `GT-27(FGC8P2-6FT).jpg`, and product photos like
  `DN-23(FE-TB9).jpg`, `J4F(Center).jpg`, `GT20W(LA).jpg`).

**Interim fix (done):** we downloaded each of these, converted to clean `.jpg`, stripped
metadata, and FTP'd them under clean filenames — so they display correctly in eCat now. This
is the same fallback we used for the PNGs.

## To go fully FTP-free (your side, on Catsy)

1. Re-save the non-compliant renders on Catsy as **`.jpg`** with **clean filenames** (no
   parentheses/spaces/`+`/`%`). A consistent scheme keyed to the SKU/option code is ideal,
   e.g. `CSP6.jpg`, `CSP10.jpg`, `BMTS-wide-top.jpg`.
2. Point the **Master Product Sheet** image links at those clean Catsy URLs.
3. Send us the updated master; we re-import, eCat CDN-pulls everything, and the FTP copies
   become unnecessary.

After that, any image you change on Catsy flows into eCat on the next sync — no FTP, no
conversion, no involvement from us.

## Quick reference

| Want to… | Compliant? | Result |
|---|---|---|
| `Foo.jpg` clean name on Catsy | ✅ | CDN auto-pull, no FTP |
| `Foo.png` | ❌ | must convert + FTP |
| `Foo (LA).jpg` / `Foo(LA).jpg` / `a+b.jpg` | ❌ | must rename + FTP |
| Update an existing compliant `.jpg` on Catsy | ✅ | re-pulls on next sync |
