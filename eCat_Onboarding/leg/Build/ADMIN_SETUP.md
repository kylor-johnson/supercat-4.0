# Legrand Admin Console Setup
**Last updated: 2026-07-23 — post-session #2 (library uploads complete)**

Live org: `leg` (id 273). All initial imports ran on 2026-07-14 (Warning-only,
no Fatals/Errors). 1,020 active products, 5 price levels, 1,194 inventory rows.

---

## Status snapshot

| Component | Status |
|---|---|
| Price levels (5) | ✅ Live — `retail`, `imap`, `canet`, `caimap`, `camsrp` |
| Products (1,020) | ✅ Live — last import 2026-07-14 18:34 (Warning-only) |
| Stories (1,020) | ✅ Live — last import 2026-07-14 22:06 (clean) |
| Inventory (1,194) | ✅ Live — last import 2026-07-14 18:47 (Warning-only) |
| Spec custom fields | ✅ Registered + send_to_ipad=true — all 18 fields live 2026-07-23; hidden from details until data arrives |
| Carton custom fields | ❌ Not registered — stripped from products.csv to eliminate warnings; register if needed |
| Category → Group assignments | ✅ Done 2026-07-23 — all 36 categories assigned via API |
| Quick View (catalog tile) | 🔄 **Update to LongDesc** — currently ShortDesc+Finish; switch Line 2 → `long_description` (see below) |
| Trade Names | 🔄 **Rebuild ready** — `products.csv` now uses adorne/radiant as Trade Names (not Legrand→collections). Import to apply. |
| Territory banner image | ✅ Done (Kylor replaced) |
| User groups | ⚠️ One group only ("Lighting Showrooms") — needs US/Canada split before beta |
| Customers | ⚠️ Test customer only — real file not yet built |
| Library | ✅ 88 entries live — all file uploads done 2026-07-23; 9 video/oversized links still need hosted URLs from Legrand |
| Images | ⚠️ 175 active products with no image — `no-image-skus.csv` generated |
| Filters | ✅ Done 2026-07-23 — voltage, wattage, numberofgangs, CountryOfOrigin, switchtype, mountingtype, numberofswitches, bulbcompatibility, Color set as multi-select filters; rohscompliant/prop65 as binary filters |

---

## Pending admin tasks (your work)

### High priority — do before next Friday call

**1. 🔄 Quick View — switch Line 2 to LongDesc (do before / on today's call)**

Postgres MCP is read-only, so flip this in Admin (both places — group override
wins over org default):

1. **Users → User Groups → Lighting Showrooms** → iPad custom views / Quick View  
   - Line 2, slot 1: change `short_description` → **`long_description`**  
   - Line 2/3 Finish (`c.Finish`) stays  
   - Clear any leftover `c.voltage` / `c.warranty` slots if still showing blank
2. **Company Settings** (org-wide Quick View default) — same change for consistency

Why: KB ShortDesc is 15 chars; LongDesc is the cleaned ≤50-char name and reads
cleanly on the grid with Finish on the next line.

**2. Enable filters**
Fields are registered and `send_to_ipad = true` but no filters are active on the
iPad. Enable the following in Admin → Products → Custom Fields (edit each field,
toggle "Use as Filter"):

| Field | Filter type | Priority |
|---|---|---|
| `Finish` | Multi-select | High — 51 distinct values |
| `CountryOfOrigin` | Multi-select | Medium |
| `numberofgangs` | Multi-select | High — key differentiator on call |
| `voltage` / `wattage` | Multi-select | Medium (no data yet) |

**3. ✅ DONE — Territory/admin background image**
Replaced (Kylor, 2026-07-23).

**4. Hide POC document custom fields from details view**
The following fields are registered, `send_to_ipad = true`, but are completely
blank on all 1,020 products. Toggle `hide_from_details_view` on each in Admin →
Products → Custom Fields until data is available:

rohscompliant / Color / voltage / wattage / switchtype / workswith / wiresize /
mountingtype / prop65 / warranty / numberofswitches / bulbcompatibility / numberofgangs /
ProductLine / bulbcompatibility

*(Note: the 21 document-related fields were deleted 2026-07-16. These 15 spec
fields remain — hide from iPad view until spec data arrives.)*

### Before beta invites

**5. User group structure — US vs Canada**
Currently one group ("Lighting Showrooms"). Before any real reps are invited:
- Create a US User Group with access to: Net (built-in) + `retail` + `imap`
- Create a Canada User Group with access to: `canet` + `caimap` + `camsrp` only
  (must never see the US Net column)
- Assign invited reps to the correct group

**6. ✅ DONE — Category → Group assignments**
Done 2026-07-23 via API. All 36 categories now assigned:
- **Dimmers (DIM):** Dimmer, Dimmer Kit, Fan Control
- **Switches & Outlets (SWT):** GFCI, Outlets, USB Outlet, Light Switch, AFCI Devices,
  GFCI/USB, Combination Devices, Switches, Night Lights, Locator Light, Connectivity,
  Antimicrobial Devices, EV Charging, Countertop Outlet (14 total)
- **Sensors & Timers (ST):** Occupancy Sensor, Timer Switch, Vacancy Sensor
- **Plates, Boxes & Blanks (WPB):** all 7 plate/sub-frame/insert categories
- **Smart Technology (GRP1):** all 9 Netatmo/smart categories
- Default Group: empty

**7. Brand-first navigation (adorne / radiant as Trade Names)**
`products.csv` rebuilt 2026-07-24: `TradeNameCode` = `adorne`|`radiant`,
`CollectionCodes` mirrors the same. After import, confirm in
**Products → Trade Names & Collections** that Legrand/COL1/COL2 are gone and
adorne + radiant are top-level trade names. Re-check Group→Category assignments
if any categories land in Default Group.

### When data is available

**8. Carton fields (optional)**
Carton data is in the source file but was stripped from `products.csv` to
eliminate import warnings. If Legrand wants that data on the iPad (useful for
order/freight reference):
- Register in Admin → Products → Custom Fields with `hide_from_details_view = true`
- Re-run `build_ecat_files.py` with carton output enabled (or restore from
  `products.csv.bak-cartons`), then re-import

Fields needed: `carton1_h`, `carton1_l`, `carton1_w`, `carton1_wt`,
`carton2_h`, `carton2_l`, `carton2_w`, `carton3_h`, `carton3_l`, `carton3_w`,
`carton3_wt`, `cartons_per_unit`

---

## Image gap — updated 2026-07-24

Pulled `Image Files` tab from Legrand’s xlsx → downloaded **613** JPGs for
**155** of the 175 live no-image SKUs → wrote `ImageFileName` into
`products.csv`. Staging: `images_missing_batch/` (also split as
`images_ftp_batch_01` = 500, `images_ftp_batch_02` = 113). See
`FTP_IMAGE_UPLOAD.md`.

| Status | Count | Action |
|---|---|---|
| Ready for FTP + products import | **155** | Upload staged JPGs to `/images`, then import `products.csv` |
| Still blank `ImageFileName` | **20** | Chase Legrand — list in `missing_images_gap_final.txt` |

The 20 gaps are Trey’s “still need links” SKUs + `HMKITBK` (YouTube embed only,
no product photo URL).

---

## Import notes

**Expected warnings on products.csv import (all harmless):**
- `Custom field 'X' is missing` × ~35 — POC fields registered in Admin but not
  in our CSV (we don't have that data). Safe to ignore; does not affect data import.
- `Field name drop_ship is unknown` / `shipped_via` / `order_uom` — these ARE
  registered as custom fields; the warning text can be misleading. Data lands.

**Inventory warnings (expected):**
- `Product not found, BaseItemCode=1597…` × 247 — these SKUs are in Legrand's
  inventory export but not in our product file (discontinued/components). Normal.
  Because these are `:warning` (not `:error`), omitted products are still
  hard-deleted from inventory on each import — this is correct behavior.

---

## Import order for re-imports

Always run in this order:
1. `products.csv` → FTP `/data`
2. `stories.csv` → FTP `/data`
3. `inventory.csv` → FTP `/data`
4. Check Tools → Admin Reports → File Import Status (blue timestamp = problems)

Customers: not yet — build real file first (see checklist §F).

---

## Clean-up (low urgency)

- **29 legacy options** from the POC scrape exist in the org. They're detached
  (no product references them). Delete via Admin → Options when convenient.
