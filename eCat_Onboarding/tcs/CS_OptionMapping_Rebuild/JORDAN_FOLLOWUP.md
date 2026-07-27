# CopperSmith — image follow-ups for Jordan

Generated from the synced import CSVs (`options.csv`, `option_groups.csv`, `products.csv`)
after the PNG→JPG + FTP fix. Everything below is **left blank on purpose** per your
"don't inherit a sibling's image" rule — these codes are *selectable* in the builder but
have **no source render in any file** (master sheet, Accessories tab, or corrections sheet).
To show a swatch/photo, send a Catsy image link (or drop the file) for each.

No action needed to import — the beta will just show no image for these until you supply one.

---

## 1. Dead Catsy links (image exists in the sheet but the URL 403s)

| Code | Where | What we did | Need from you |
|---|---|---|---|
| `PFP36` (product) + `PFPAU` (option) | Post Fitter for GT36 / Austin36 Post Fitter | **Blanked** — every `PFP` variant (`.jpg` and `.png`) returns 403 on Catsy | A working image link or file for the Post Fitter |
| `BRASS` (option, group `FIN002`) | "Brass" finish swatch | **Blanked** — no brass swatch image exists in any source | Confirm Brass should show a swatch; if so, send one |

> FYI (no action): `TE20E` and `CS43E` had dead `.jpg` master links — both recovered
> (TE20E from its PNG, CS43E from a working JPG). `COY12`/`COY13` repointed to the working
> Contemporary Yoke JPG the other COY rows use.

---

## 2. Referenced-but-blank OPTION swatches (24 codes, no source image)

These option codes are members of live option groups but have no swatch image anywhere.

| Code | Name | Example group(s) |
|---|---|---|
| `CHM36` | Chain Mount 36" | CM001, CM003, … (25 groups) |
| `CHM72` | Chain Mount 72" | CM005, CM011, … (11 groups) |
| `HCHM` | Heavy Chain Mount | CM005, CM011, … |
| `QCHM` | Quick Chain Mount | CM028, CM030, … (55 groups) |
| `GPR` | Gas Pressure Regulator | GAS001–GAS007, GE003–GE012 |
| `SPT` | (gas) | GE008 |
| `WG` | (gas) | GE008 |
| `FH` | Flat Hook (?) | W057, W058, … |
| `BFHG15` | | W090, W091, WA036 |
| `BSG15` | | W090, W091, WA036 |
| `FHG15` | | W090, W091, WA036 |
| `CPMG15` | | PP026, PP090, PP091 |
| `CYG15` | | CM080, CM090, CM091 |
| `PFG15` | | PP026, PP090, PP091 |
| `PF36` | | PP028, PP100, PP101 |
| `BS` | | WA_HL30 |
| `BSW` | | WA_HL30 |
| `RBS` | | WA_HL30 |
| `BSM` | | CM157, CM159, CM164 |
| `CHMCO18` | | DC_CO18 |
| `DSMC` | | WM022, WM103 |
| `G1` | | WM027, WM154, WM155 |
| `SML` | | WM026, WM152, WM153 |
| `SMS` | | WM059, WM060, … |

(Full group membership is in `option_groups.csv`.)

---

## 3. Referenced-but-blank ACCESSORY products (8 SKUs, no source image)

These appear as accessory products with no photo.

| SKU | Name |
|---|---|
| `AHC` | Additional Heavy Chain |
| `ELI3.5` | Electronic Igniter |
| `FBBM1` | Flame Bulb Battery Module |
| `PFA36` | Post Fitter Adaptor for GT36 |
| `PFP36` | Post Fitter for GT36 *(also #1 above — dead PFP link)* |
| `SBP` | Solid Copper Back Panels |
| `SPF` | Spider Post Fitter |
| `VNG50FH` | High Flame Burner *(you flagged this one to stay blank)* |

---

## 4. Confirm already on the server (eCat-only mount-meta)

`WALL` / `CEIL` / `POST` use local swatches `wall-mount.jpg` / `ceiling-mount.jpg` /
`post-mount.jpg`. They are **not** in the Accessories tab, so we didn't restage them —
please confirm they already exist in `/option_images` on the FTP (they should from a prior pass).

---

## Longer-term (engineering, optional)

eCat's image sync rejects PNG (requires `.jpg`/`.jpeg` + `image/jpeg`). CopperSmith's
asset library is largely PNG, so today we convert + FTP per image. If engineering adds
`image/png` support to `CdnImageSync`, the PNG links would sync directly with no FTP step.
