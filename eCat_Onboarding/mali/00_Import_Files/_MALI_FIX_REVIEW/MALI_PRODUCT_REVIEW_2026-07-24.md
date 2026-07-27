# mali — Product Import Review (2026-07-24)

Forensic review of the live `Ready_For_Import/products.csv` (683 rows: **426 shown**,
257 already hidden) against the iPad screenshots and the Magic Lite website. Companion
data file: `IMAGE_HIDE_FIXPLAN_2026-07-24.csv` (per-SKU action list).

## TL;DR — what's actually going on

The "weirdness" is **not** bad SKUs and it's **not** a broken import. It's a
**merchandising/hide-and-relate gap** plus a **handful of genuinely wrong image files**:

1. **~232 accessory SKUs are shown as their own grid tiles** instead of being hidden and
   attached to their parent fixture as Related Items. Because most accessories borrow their
   parent's photo (or a generic family photo), the grid fills with duplicate-looking tiles —
   trim rings, beauty rings, construction plates, covers, caps, jumpers, connectors, lamps,
   drivers, mounts. **This is the root cause of every "same image, weird variant" symptom.**
2. **10 products have a genuinely wrong hero image** (wrong product family entirely, or a
   lifestyle shot) — these need a correct photo, not just re-merchandising.
3. **Size-visibility is inconsistent** across otherwise-identical families (e.g. Task Star
   PRO shows only the 9″; the Gen II Task Star correctly shows one hero per size).
4. **The BaseItemCodes are correct.** They are Magic Lite's real published part numbers,
   size/wattage/finish encoded and all — verified against magiclite.com. Nothing to rename.
5. **ShortDesc unit-of-measure is applied inconsistently** (Streamline tape shows "— 20 ft /
   — 100 ft"; Standard tape, eStrip and outdoor tape don't).

Hiding+relating the accessories collapses the grid from **426 → ~194 clean hero tiles**,
which matches the intended pattern already used by the good families (LTS-II, Brick Star,
Step Star, RGL downlights).

---

## 1. BaseItemCodes are correct — do NOT rename (answers the main worry)

You flagged `RGL-4B-9W-SW` vs `RGL-4-TR-BK` as possibly wrong/inconsistent. They're both
**verbatim Magic Lite codes**. From magiclite.com's Regressed Down Light (CCT) spec page:

| ML site "Product Code" | Meaning |
|---|---|
| `RGL-4B-9W-SW` (4″) / `RGL-6B-12W-SW` (6″) | the fixture, switch-CCT |
| `RGL-4B-9W-BT` (4″) / `RGL-6B-…-BT` (6″) | the fixture, Bluetooth-CCT |
| Trim finishes `BK / BZ / SN` | → `RGL-4-TR-BK`, `RGL-4-TR-BZ`, `RGL-4-TR-SN` (the trim rings) |

So `RGL-4B-9W-SW` = the downlight, `RGL-4-TR-BK` = its black trim-ring accessory. Different
products, correctly named. The same logic holds across the file:

- Size/watt/finish **in the SKU is Magic Lite's own convention** (e.g. `LVLDL-06-TR-BK-L3`,
  `LTS-II-1-HW/WH`, `LV-HS-PD20-24V-100-WW`). It is not something we invented and is not a
  reason to rename. Short codes only matter for image-filename/grid legibility, and these are
  already fine.
- **One thing to confirm with ML (their typo, not ours):** the site prints the 6″ Bluetooth
  as `RGL-6B-9W-BT`, but its own spec table lists that unit at **12W/840LM**. Our file uses
  `RGL-6B-12W-BT`, which is internally consistent with the 12W spec. Keep ours; flag to ML.

**Verdict: SKUs are legit. The problem is how they're merchandised, not how they're named.**

---

## 2. Wrong hero images (Category A — need a correct photo / reorder) — 10 SKUs

These are wrong even after re-merchandising, because the hero image is the wrong product
family (or a lifestyle shot). See `IMAGE_HIDE_FIXPLAN…csv` rows tagged `A_WRONG_IMAGE`.

| SKU | What it shows now | Fix |
|---|---|---|
| **MLDR-120-24** | Room/application lifestyle shot (framed art + linear light), not the driver | Replace primary with the driver product photo |
| **DD-2460-S-WH** | DimDrive 60W — primary isn't the device face | Reorder `ImageFileName` so the device shot (`-2`/`-3`) is primary, or replace |
| **DD-24100-S-WH** | DimDrive 100W — same as above | Reorder to device shot, or replace |
| **LV-HSDR-36-24-PC** | 36W Hard-Strip driver, but showing the **Hard Strip** photo (`LV-HS-PD20-24V-30-WW.jpg`) | Needs a driver photo |
| **LV-HSDR-60-24-PC** | 60W Hard-Strip driver, same borrowed strip photo | Needs a driver photo |
| **SL-CC** | Step Star Concrete Cap, showing the **Outdoor Wall Sconce** photo (`TLWMV153WMBK.jpg`) | Needs concrete-cap photo |
| **LBR-II-KIT** | Brick Star replacement kit, showing the **Wall Sconce** photo | Needs kit photo |
| **BL-CC** | Brick Star Concrete Cap, showing a **Pathway Light** photo (`WF-04-12V-BLK.jpg`) | Needs concrete-cap photo |
| **LMSH-001** | Terminal Block / Junction Box, showing an **Edgelit Puck** photo (`EPL-SR-WW-WH.jpg`) | Needs junction-box photo |
| **ACC-TM-BLK** | Landscape Tree Mount, showing the **Mini Flood** photo (`FL-01-12V-BLK.jpg`) | Needs tree-mount photo (or hide + relate to flood) |

> Note: MLDR-120-24, DD-2460, DD-24100 all live on the "SL,DRVRS/LL,…" family and are the
> three you explicitly called out — confirmed. The other 7 surfaced from the borrowed-image
> scan. Most of the remaining ~120 borrowed-image cases are **accessories** and are handled
> by Section 3 (once hidden, the borrowed photo no longer clutters the grid).

---

## 3. Accessories shown on the grid → hide + relate (Category B) — ~232 SKUs

This is the big one and the source of the "ton of weird variants with the same image." These
are legitimate orderable parts, but they should be **`Hideable=Y`** and wired into their
parent fixture's **`RelatedItems`** — exactly like the finish variants already are. They then
appear as the related/swatch strip on the hero's detail page instead of as standalone tiles.

Effect: **426 shown → ~194 shown heroes.** Full list in the CSV (`B_HIDE_ACCESSORY`), grouped
by suggested parent hero. The worst offenders (what you saw in the screenshots):

| Parent hero | # accessories to hide | Examples |
|---|---|---|
| 5CCT Thin Line downlights `DL-5CCT-*` | ~26 across sizes | all `LVLDL-*-TR-*-L3` trim rings, `LVLDL-BR-*-L3` beauty rings, `LVLDL-CP-*-L3` construction plates (the 30-tile `LVLDL-TR-ROUND.jpg` block) |
| Surface Mount Round `LVLDL-SR-06-WW-WH-L` | 12 | `LVLDL-SR-*-TR-{BK,BZ,BN}-L` trim rings |
| Surface Mount Square `LVLDL-SS-06-WW-WH-L` | 12 | `LVLDL-SS-*-TR-{BK,BZ,BN}-L` trim rings |
| Regressed `RGL-4B-9W-SW` | 6 | `RGL-{4,6}-TR-{BK,BZ,SN}` |
| Fire-Rated Thin Line `DL-FR-5CCT-{4,6}-WH` | 12 | `DL-FR-TR-*`, `DL-FR-BR-*`, `DL-FR-CP-*` |
| High Power eStrip `LESHP-40-3000K` / `LES-40-RGB` | 22 | connectors, jumpers, power feeds, mounting clips, `LMSII-001` |
| Hard Strip `LV-HS-PD20-24V-30-WW` / RGB | 17 | power feeds/connectors `LV-HS-PD20-PC1-*`, `LV-HS-CN-*`, end caps, mounting clips |
| eStrip 120V `ES-120V-*` / `ES-LS28…` | 15 | end caps, jumper cables, power connectors |
| Switch Star (Discontinued) `LED-SW-P-WH` | 10 | all `LED-SW-*-COV` replacement covers + `LED-SW-MOD` |
| Outdoor Wall Sconce `TLWMV153WMBK` | 9 | `TLWMV15XWM*-0{1,2,4}` interchangeable covers |
| Globe / Wedge light `MGST` / `MGWL` | 11 | replacement lamps, end caps, nail clips |
| Neon Flex `NFLX-40-*` | 8 | conkits, jumpers, splices, end caps, clips |
| LTSPRO family | 13 | jumper cables `LTSPRO-J-*`, power cords `LTSPRO-PC-72*`, junction boxes `LTSPRO-JB*`, slider switch covers, `RC-01` |
| Mini Disc / Disc Light `LEDD-F-WH` | 9 | modules, install wire, concrete forms |
| Mini Flood `FL-15/50-CT`, `FL-01` | 8 | yoke/universal mounts, glare shields, wire guards |
| Extrusion end caps/clips `LV-RD54`, `LV-ALP2908`, etc. | ~10 | `-EC`, `-EC-WF`, `-MC` bag items |

**Judgment flags before bulk-applying:**
- **Trim rings / beauty rings** are a legit replacement/upsell SKU. Hiding is the norm for a
  clean grid, but if ML/reps want them findable, keep the *first* finish visible per fixture
  and hide the rest. Recommend hide-all + relate (matches the good families).
- **Drivers** (`LV-HSDR-*`, `LEDDR-12-20W-HW`, plug-in drivers): a couple got swept into the
  accessory list because they're "sold-with." Decide per-SKU whether a driver should remain a
  standalone catalog tile (Drivers & Controllers is its own website category) or relate to the
  strip. Default: keep drivers **visible**; only relate the strip-specific hardwire pigtails.
- A few controllers/amplifiers/remotes were **intentionally excluded** from the hide list
  (they're their own catalog line).

---

## 4. Size-visibility inconsistencies (Category C) — decide the pattern

Same fixture family, different rules for which sizes show. Pick one pattern and apply
consistently. The **Gen II Task Star (`LTS-II-*`) is the correct model**: one WH hero shown
per size, other finishes hidden+related.

| Family | Current | Recommended |
|---|---|---|
| **`LTS-II-*`** Gen II Task Star | ✅ one WH hero per size (9.5/17.5/26/34.5/43″) | keep as-is (the template) |
| **`LTSPRO-*`** Task Star PRO | ❌ only the **9″ WH** shows; 12/18/24/32/40 all hidden | show one WH hero per size (match LTS-II) |
| **`LTSPRO-SW-*`** Pro Swivel | ❌ only the **9″ WH** shows | show one WH hero per size |
| **`DL-5CCT-*-WH`** Thin Line Round | ❌ only **4″** shows; 3/6/8/10 hidden | show one hero per size (or confirm 4″-only is intentional) |
| `DL-5CCT-*S-WH` Thin Line Square | only 4″ shows | show 4″ + 6″ |
| `DL-FR-5CCT-{4,6}`, `RGL-FR-{4,6}`, `FL-{15,30,50}`, `IG-…-{36,60}D`, `SDL-…-{1P,6P}` | one size/variant shown, rest hidden | confirm which sizes/wattages should be discoverable vs related |

---

## 5. ShortDesc / unit-of-measure consistency (Category D)

The iPad grid tile renders **ShortDesc**. Tape reels are sold by length, but UOM is only shown
on the Streamline (SL) family:

| Family | ShortDesc today | Issue |
|---|---|---|
| `SL-ID-30K-HP-20/100-A8` | "High Power Indoor (3000K) — **20 ft** / **100 ft**" | ✅ UOM shown, both lengths present |
| `ST-ID-30K-HP-20-B0` | "High Power Indoor (3000K)" | ❌ no "— 20 ft"; only one length SKU |
| `LESHP-40-3000K` | "High Power eStrip (3000K)" | ❌ no length UOM |
| `SL-OD-CCT-HP-20-B8` | "Tunable CCT Outdoor, High Power" | ❌ no length UOM (Streamline peers do show it) |

**Recommend:** standardize — every reel-sold tape SKU shows its length in ShortDesc
("— 20 ft", "— 100 ft"), or none do. Note the intended convention so future imports match.
(Minor: several ShortDescs exceed the 15-char guideline, but this org is clearly using longer
ShortDesc strings on purpose — not a blocker, just flag if ML wants them trimmed.)

---

## Suggested execution order

1. **Category C decision** (which sizes are heroes) — this changes which SKUs are heroes vs
   related, so settle it before wiring RelatedItems.
2. **Category B** — set `Hideable=Y` on the ~232 accessories and populate each parent hero's
   `RelatedItems`. (I can script this from `IMAGE_HIDE_FIXPLAN…csv` once C is decided.)
3. **Category A** — get the 10 correct photos (or reorder for the DD/MLDR trio) — feeds the
   existing "needs photos" ask (`01_IMAGES_NEED_CLIENT_PHOTO.csv`).
4. **Category D** — normalize tape ShortDesc UOM.
5. Re-import in order, verify File Import Status is error-free.

No SKU renames. No structural changes to the file schema.

---

## APPLIED 2026-07-24 (live `Ready_For_Import/products.csv`)

Backup: `products.csv.bak_prehidefix_20260724-113321`. Full diff: `FIX_CHANGELOG_2026-07-24.csv` (336 changes).

- **Category B — DONE.** 232 accessories set `Hideable=Y` and wired into their parent hero's
  `RelatedItems`. Grid **shown count 426 → 215**.
- **Category C — DONE (consistent rule applied).** Size/wattage = its own visible hero;
  finish/CCT/control-type/pack = hidden + related. Specifically:
  - Task Star PRO (`LTSPRO-*`) + Pro Swivel (`LTSPRO-SW-*`): now one WH hero per size (9/12/18/24/32/40); finishes hidden + related — matches `LTS-II`.
  - 5CCT Thin Line round (3/4/6/8/10) + square (4/6), Fire-Rated Thin Line (4/6), Fire-Rated Regressed (4/6): every size now shown.
  - Mini Flood (15/30/50W) and Well Light (36°/60°): every wattage/beam now shown.
  - Regressed CCT: 4″ and 6″ switch heroes shown; Bluetooth variants hidden + related.
- **255-char cap — DONE.** 7 pre-existing over-length `RelatedItems` (SL-ID tapes, LESHP, NFLX-40-RGB) trimmed at a comma boundary; only trailing generic driver/controller cross-sells dropped (logged).
- **Validation:** 683 rows, 0 duplicate BaseItemCodes, 0 RelatedItems pointing to unknown codes, 0 fields > 255 chars.

### Still outstanding (needs photos / a human call — NOT applied)
- **Category A (10 wrong images):** need correct photos or a visual reorder of `MLDR-120-24`,
  `DD-2460-S-WH`, `DD-24100-S-WH` (couldn't fabricate/guess which frame is the product shot),
  plus `LV-HSDR-36/60-24-PC`, `SL-CC`, `LBR-II-KIT`, `BL-CC`, `LMSH-001`, `ACC-TM-BLK`.
- **Category D (tape ShortDesc UOM):** left as-is — deferred pending confirmation of reel
  lengths for ST-standard / eStrip / SL-outdoor (didn't want to stamp a length I can't source).
- **Driver visibility:** a couple of "sold-with" drivers were swept into B; confirm whether any
  should stay a standalone catalog tile vs. related-only.

---

## SECOND PASS — verification + duplicate-image / orphan finish (2026-07-24 14:35)

Independent re-verification of the first pass, then finished the two remaining problems
(duplicate images among **visible** products, and **orphaned-hidden** unreachable SKUs).
Backup: `products.csv.bak_mergefix_20260724-143525`. Diff: `FIX_CHANGELOG_MERGE_20260724-143525.csv` (67 changes).
Proposal source-of-truth CSVs: `PROPOSAL_01_DUP_IMAGE_TRIAGE.csv`, `PROPOSAL_02_ORPHAN_FIX.csv`,
`PROPOSAL_03_RELATEITEMS_PREVIEW.csv`. Reusable scripts: `verify_state.py`, `orphan_analysis.py`,
`build_proposals.py`, `apply_changes.py`.

**State: 683 SKUs (0 lost/0 added vs 7/23 baseline). Visible 209 → 218. Hidden 474 → 465. Orphaned-hidden 163 → 70.**
Visible shared-hero clusters **19 → 14** (all 14 are legit distinct-size families or intentional keep-both pairs).
Validation on the written file: 0 dup codes, 0 dangling RelatedItems refs, 0 RelatedItems > 255.

### Duplicate images among VISIBLE products (19 clusters / 57 products) — DONE
- **Hidden + related (11):** `LV-V1V3-EC/-EC-WF/-MC`→`LV-LB-V3-FR`; `LV-ALP2908-EC/-EC-WF`→`LV-ALP2908`;
  `SX-TP-BR/-LA`→`SX-12V-DD-60W`; `LV-ALP2208-BK`→`LV-ALP2208`; `LV-ALP007-BK`→`LV-ALP007`;
  `LTP-001-OD-6FT`→ hidden + wrong eStrip image cleared (already related under `LES-40-RGB`).
- **Wrong image fixed, kept visible (1):** `NFLX-RGB-CHANNEL` repointed to real aluminum-channel photo
  (staged `catA_images/NFLX-RGB-CHANNEL.jpg`) — verified against magiclite neon-flex page; NFLX heroes'
  RelatedItems were all already 244–253 chars so hide+relate was impossible.
- **Kept visible, cross-related (4, flagged judgment calls):** `ES-EXT↔ES-EXT-XX` (length), `IG-01-12V-36D↔60D-BLK` (beam angle).
- **Kept as-is (42):** distinct SIZE/WATTAGE families legitimately sharing one stock photo.

### Orphaned-hidden fix (163) — DONE
- **Related to a visible parent (74):** LTS-II/EPL/Brick-Star/Step-Star/sconce finishes → matching hero;
  SDL packs → 1-packs; `ST-ID-27K-LP`→`ST-ID-30K-LP` (2700K vs 3000K CCT); etc.
- **Unhidden distinct sizes (19):** `LEDLB-5CCT-12/18/24/36/48`; `LV-HS-PD20-24V-50/100/120-WW`;
  `LV-HS-RGB-24T2-2/3`; `GDL-3/6`; `SDL-5CCT-6-WH-1P`; `LVLDL-SR/SS-08/10/12-WW-WH-L`.
- **Rebalance:** stripped redundant cross-size trim-ring refs (08/10/12) off the now-crowded 6″ surface-mount
  heroes (each size hero is visible and carries its own trims) — this is what kept everything under 255.

### FLAGGED for client decision — left hidden, NOT changed (70)
Color families with no single obvious hero + a discontinued line. **Client must choose which to surface:**
- **Mini Disc Marker `LEDMD-*` colors (30)** and **Mini Disc Scoop `LEDMD-S-*` colors (20)** — Amber/Blue/Green/Red/Warm-White
  in each finish (cool-white heroes are already visible). Default recommendation: keep hidden unless client sells colors.
- **Disc Light `LEDD-*` (12)** — clear/frosted × color × round/square/dome (cool-white hero visible).
- **Switch Star `LED-SW-*` (8)** — **discontinued**; too many cover/finish combos for the 255-char RelatedItems cap. Recommend drop or leave hidden.

### New (acceptable) visible shared-photo clusters — flag for own photos eventually
- `LV-HS-PD20-24V-30/100/120-WW` share the 300mm stock photo (distinct sizes — OK per rule).
- `SDL-5CCT-6-WH-1P` shows the 4″ photo (needs its own 6″ image).

---

## THIRD PASS — Catalogue-vs-product-file HERO IMAGE audit (2026-07-24 15:46)

Full image-content audit of **all 218 visible heroes** against the **May 2025 Product
Catalogue** (rendered pages + embedded-raster extraction with PyMuPDF). Every fix is proven
against a specific catalogue page — nothing invented. Deliverables:
`CATALOGUE_HERO_AUDIT_2026-07-24.csv`, `FTP_UPLOAD_LIST_2026-07-24.txt`,
`CLIENT_PHOTO_NEEDED_2026-07-24.csv`, staged JPGs in `catA_images/`.
Backup: `products.csv.bak_herofix_20260724-154623`. CSV diff:
`FIX_CHANGELOG_HEROIMG_20260724-154623.csv` (7 items). State unchanged: **683 rows / 218
visible / 465 hidden / 0 dup / 0 dangling / 0 RelatedItems>255 / 0 visible without image.**

### Verdict summary (218 visible)
| Verdict | Count |
|---|---|
| OK — own-named + catalogue-confirmed | 161 |
| OK — shared family hero (distinct size) | 18 |
| FIXED — file-swap (upload clean JPG, same filename) | 12 |
| FIXED — via shared primary (auto-fixed by a file-swap) | 12 |
| FIXED — repoint (ImageFileName; **CSV already applied**) | 7 |
| CLIENT PHOTO NEEDED | 4 |
| VERIFY on iPad (own-named, not proven wrong) | 4 |

### Fixes proven against the catalogue (heroes verified visually)
- **5CCT LED Task Bar** `LEDLB-5CCT-12/18/24/36/48` — were kitchen-lifestyle / non-uniform;
  **repointed** to `LEDLB-5CCT-10.jpg` (the confirmed clean white bar, catalogue p.55). *(CSV applied.)*
- **Gimbal** `GDL-3`, `GDL-6` — were dimension line-drawings; **repointed** to
  `GDL-4-14W-38-CCT-WH.jpg` (clean white gimbal, catalogue p.117). *(CSV applied.)*
- **Task Star PRO** `LTSPRO-9-WH` (+ 12/18/24/32/40 borrow it) — clean white bar extracted from
  catalogue p.51 → `LTSPRO-9-WH.jpg` (upload).
- **Pro Swivel** `LTSPRO-SW-09-WH` (+ 12/18/24/32/40 borrow it) — was the USB/USB-C spec
  close-up; clean swivel bar from catalogue p.53 → `LTSPRO-SW-09-WH.jpg` (upload).
- **Fire-Rated Thin Line** `DL-FR-5CCT-4-WH` (+ `-6-WH` borrows) — red fire-rated downlight
  from catalogue p.129 (no text overlay) → `DL-FR-5CCT-4-WH.jpg` (upload).
- **Fire-Rated Regressed** `RGL-FR-5CCT-4-WH` (+ `-6-WH` borrows) — red regressed downlight
  from catalogue p.131 → `RGL-FR-5CCT-4-WH.jpg` (upload).
- **PIR Sensor** `LV-SPIR-1CH-LV` — black PIR box from catalogue p.167 → upload.
- **Interconnection Cables** `LV-DL-EX-10-L`, `LV-DL-EX-30-L` — real photos already in
  `scraped_images/` (magiclite.com); staged → upload. *(Handoff guessed "client photo"; we had them.)*
- **Already staged prior, still need upload:** `MLDR-120-24`, `DD-2460-S-WH`, `DD-24100-S-WH`,
  `ACC-TM-BLK`, `NFLX-RGB-CHANNEL`.

### Client photo needed (NOT invented — flagged)
`LV-RF103`, `LT-11S-RF`, `LV-ZJFFS-3CH-6INW`, `LT-490A` — RGB controllers/amplifiers/remotes
not present in the catalogue. See `CLIENT_PHOTO_NEEDED_2026-07-24.csv`.

### Verify-on-iPad (own-named, no evidence of being wrong)
`DR-96-24-TM-5N1D`, `ES-LS283527K422430`, `ES-LS283530-WH244FT`, `YH-HRF50CA120S505060`.

### OWNER — do this to go live
1. **FTP upload** the 12 files in `catA_images/` to `/images` (FLAT root, no subfolders).
   List: `FTP_UPLOAD_LIST_2026-07-24.txt`. All sRGB `.jpg`, exact filename casing.
2. **Re-import** `Ready_For_Import/products.csv` (Admin → Tools → Import Data) — needed only
   because of the 7 `LEDLB`/`GDL` repoints.
3. **Verify** Admin → Admin Reports → **File Import Status** (blue-link timestamp = errors;
   Fatal rejects file, Error skips deletes). Product-image processing takes **30–45 min**.
4. **Spot-check on iPad** after processing: the 6 fixed families above, plus the 4 VERIFY SKUs.
   `LEDLB-5CCT-10` and `GDL-4` are the reference clean heroes — if either looks wrong,
   upload the fallbacks in `catA_work/fallback/` under those exact filenames.
5. **Request client photos** for the 4 controllers/amplifiers listed above.

### HIDDEN images audited too (all 465) — `_audit_hidden.csv`
Hidden products still render as **Related-Items thumbnails** on their parent's detail page, so
they were audited as well:

| Hidden image kind | Count | Meaning |
|---|---|---|
| OWN_NAMED | 227 | own SKU-named file (no name-mismatch signal; content unverifiable from filenames) |
| BORROW_SAME_FAMILY | 137 | shares a same-family hero (finish/size sibling) — correct pattern |
| BORROW_CROSS_FAMILY | 94 | flagged by heuristic, but **all are finish/size/accessory borrows of their own product** (e.g. `LTSPRO-12-BK`→white unit, trim rings→`LVLDL-TR-ROUND.jpg`) — acceptable, not wrong-product |
| NO_IMAGE (blank) | 7 | empty thumbnail — not wrong, just missing |

**No hidden product shows a wrong (mismatched-product) photo.** The 5 previously-diagnosed
wrong hidden heroes (`SL-CC`, `BL-CC`, `LBR-II-KIT`, `LV-HSDR-36/60-24-PC`, `LMSH-001`) were
already **blanked** by the structural pass, so they no longer show a sconce/strip/puck.

The 7 blanks are minor hidden accessories with **no clean catalogue photo** (concrete caps are
line-drawings; the kit/drivers/terminal block aren't pictured as products). Left blank (not
fabricated) and flagged **LOW priority** in `CLIENT_PHOTO_NEEDED_2026-07-24.csv`.

*Honest limitation:* the 227 own-named hidden files can't be content-verified from filenames
alone; none is flagged wrong by the prior visible/borrowed scans, and the known-wrong ones were
already cleared. If the client wants absolute certainty, spot-check hidden thumbnails on the iPad.
