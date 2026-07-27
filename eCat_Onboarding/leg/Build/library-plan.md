# Legrand — Library (Shared Resources) Plan

Covers marketing/technical collateral in `Source Data/Other Source/`
(**120 files**, ~406 MB) that is **not** part of `products.csv`.

Companion: `client-confirmation-checklist.md` §G (client decisions).

## Library vs products — decision

| Put in… | What | Why |
|---|---|---|
| **Library** (Admin → Library) | Sell sheets, catalogs, brochures, training, CEU, wiring, competitor conversion, Netatmo how‑tos, display kits | Org-level collateral; iPad PDF viewer + email/share |
| **Product custom fields** | Spec *text* only (if ever provided) | Text columns only — no file upload / PDF viewer |
| **FTP `/images`** | SKU catalog photos | Not for sell sheets or B+ campaign packs |

Source CAD columns `Instruction` / `Parts Diagram` / `Spec Sheet` are **empty on
all 1,020 rows**. Per-SKU docs on the product detail would need a later
**SKU → URL map** — out of scope unless they provide it.

There is **no CSV/FTP importer** for Library. Manual Admin uploads (or Links).

## How Shared Resources works (code-verified)

- Types: **Directory** (Section), **File**, **Link**
- Two levels only: Sections → entries (no nested folders)
- Allowed uploads: `pdf, docx, doc, pptx, xls, xlsx, xlsm, csv, jpg, png, txt, pages, webloc`
- **Not allowed as File:** `mp4`, `pptm` (`.jpeg` → rename to `.jpg`)
- Hard upload cap: **30 MB** (unless flipbook/admin exception)
- Files **>5 MB**: still upload; iPad views **online only**
- Entries assignable to user groups; group Library auth = All / Selected / None

## Live `leg` status (2026-07-14)

| Section | Entries | Action |
|---|---:|---|
| Catalogs & Brochures | 2 | Done (2026 Collections + Consumer Brochure June 2026) |
| Sell Sheets and Literature | 5 | In progress — continue remaining sell sheets |
| adorne Displays | 3 | Done — skip Other Source copies |
| Wiring Diagram | 3 | Done — skip Other Source copies |
| radiant Advance Dimmers | 8 (6 files + 2 links) | Leave older set; new LED pack → **LED Advanced Dimmer** |
| Canadian Price List | 2 | Done |
| LED Advanced Dimmer | 0 | Upload gap |
| Technical Help | 0 | Upload gap |
| Training | 0 | Upload gap |
| CEU | 0 | Upload gap |
| Competitor Conversion | 0 | Upload gap |
| Videos (Promo) | 0 | Waiting on hosted URLs |
| Videos (Install) | 0 | Waiting on hosted URLs |

**Skip:** `BR1896-PS-radiant.pdf` (already under radiant Advance Dimmers).

## Must host → Library Link

| Asset | Why |
|---|---|
| 8 Netatmo `.mp4` how‑tos | Video not an uploadable type |
| `CEU/The Art of Resi Lighting 11-6-25.pptx` (~56 MB) | Over 30 MB cap |

Need public `https://` URLs (YouTube / Vimeo / SharePoint).

## Must convert before upload

| Asset | Fix |
|---|---|
| `Training Presentations/TU & LED Adavanced Dimmer TW.pptm` | Re-save as `.pptx` |

Display `.jpeg`s already live as `.jpg` — no rename needed.

## Dedupe / optional / revision

- Upload `BR1796-PS-adorne-Consumer.pdf` and `CAT3438R4-PS-DSO.pdf` **once** in
  Sell Sheets; skip LED-pack copies.
- **Optional:** skip LED `B+ Images/` (~29 JPGs) unless reps need them.
- **Revision check:** live `EWS-PS-SS-3871-…` vs local `SS3871-PS-LED-Advanced-Dimmer-Offering.pdf` — keep newer only.
- Under-cab wiring: live has PDF; local Other Source has DOCX — leave unless DOCX is newer.

## Sell Sheets and Literature — Labels

Section name live: **Sell Sheets and Literature**

| Label | File | Status |
|---|---|---|
| radiant USB Charger Spec Sheet | `1936-18 PASS Radiant USB Charger SS SF20299-3.pdf` | Live |
| adorne Consumer Brochure | `BR1796-PS-adorne-Consumer.pdf` | Live |
| Raise the Bar | `BR3077-PS-RaisetheBar.pdf` | Live |
| DSO Look Book | `BR3315-PS-DSOLookBook.pdf` | Live |
| DSO Catalog | `CAT3438R4-PS-DSO.pdf` | Live |
| — | `BR1896-PS-radiant.pdf` | **Skip** (live elsewhere) |
| Universal Dimmer Q&A Fact Sheet | `Fact Sheet_UniversalDimmer_Q&A.pdf` | Todo |
| Champions Flyer Welcome 2023 | `FL3483-PS-ChampionsFlyerWelcome2023.pdf` | Todo |
| adorne Display Name Instructions | `FL3541-PS-adorneDisplayNameInstructions.pdf` | Todo |
| A Closer Look at GFCI USB | `PC3360-PS-ACloserLookatGFCIUSB.pdf` | Todo |
| Installing GFCI USB | `PC3361-PS-InstallingGFCIUSB.pdf` | Todo |
| Whole Home Cost | `PC3409R1-PS-WholeHomeCost.pdf` | Todo |
| radiant AFCI Receptacles Cut Sheet | `PS-radiant-cutsheet-AFCI-Receptacles_SF20222.pdf` | Todo |
| radiant Commercial Spec-Grade TR Receptacles | `radiant-Commercial-Spec-Grade-TR-Receptacles-Spec-Sheet-SF20215.pdf` | Todo |
| radiant WWP10 Cut Sheet | `radiant-cutsheet-wwp10.pdf` | Todo |
| radiant WWP20 Cut Sheet | `radiant-cutsheet-wwp20.pdf` | Todo |
| radiant WWRL10 Cut Sheet | `radiant-cutsheet-wwrl10.pdf` | Todo |
| radiant WWRL50 Cut Sheet | `radiant-cutsheet-wwrl50.pdf` | Todo |
| radiant Paddle Switches | `radiant-PaddleSwitches.pdf` | Todo |
| radiant Screwless Wall Plates | `radiant-ScrewlessWallPlates.pdf` | Todo |
| radiant Ultra-Fast USB Charging Receptacles | `radiant-spec-Ultra-Fast-USB-Charging-Receptacles.pdf` | Todo |
| radiant Weather-Resistant USB Spec Sheet | `radiantWRUSBSS1119.pdf` | Todo |
| radiant Self-Test GFCI Spec Sheet (1597/2097) | `SF20278 radiant Self-Test GFCI Spec Sheet….pdf` | Todo |
| radiant Self-Test GFCI Spec Sheet (Dec 2018) | `SF20278-radiant-Self-Test-GFCI-Spec-Sheet-121318.pdf` | Todo (or pick one revision) |
| Smart System WiFi Sell Sheet | `SS1962-PS-Smart-System-WiFi.pdf` | Todo |
| Wireless Charger Sell Sheet | `SS3190-PS-Wireless-Charger.pdf` | Todo |
| GFCI USB Sell Sheet | `SS3293-PS-GFCIUSB.pdf` | Todo |
| adorne Planogram with Pricing (Canada) | `SS3329R2-PS-adorne-PlanOGram-price-CA.pdf` | Todo |
| adorne Planogram with Pricing (US) | `SS3329R2-PS-adorne-PlanOGram-price.pdf` | Todo |
| adorne Planogram | `SS3329R2-PS-adorne-PlanOGram.pdf` | Todo |
| In-Wall Relocation Outlet Sell Sheet | `SS3428-PS-InWallRelocationOutlet.pdf` | Todo |
| Power Delivery Sell Sheet | `SS3446-PS-Power-Delivery.pdf` | Todo |
| radiant Wave Sell Sheet | `SS3523-PS-radiant-Wave.pdf` | Todo |
| DSO Wave Sell Sheet | `SS3524-PS-DSO-Wave.pdf` | Todo |
| Cleaner Spaces Sell Sheet | `SS3624-PS-Cleaner-Spaces.pdf` | Todo |
| Wall Plate Sell Sheet | `SS3810-PS-WallPlate-NEW.pdf` | Todo |

## Remaining section uploads (gap)

| Section | What to load |
|---|---|
| **LED Advanced Dimmer** | Cut sheets, install PDFs, CAD, guide specs, price sheets, ID cards, BR3597, PC3753, SS3588, codes — skip B+, skip BR1796/CAT3438 dupes, SS3871 only if replacing live |
| **Technical Help** | All 7 files (incl. `adorne-Install-4-Way Paddle.pdf` — not the wiring PNG) |
| **Training** | Display training pptx, Netatmo remotes pptx, converted TU/LED pptx; optional Netatmo Wired Remotes pptx from Netatmo folder |
| **CEU** | 3 small files as File; big pptx as Link |
| **Competitor Conversion** | Program PDF + Disposition xls |
| **Videos (Install / Promo)** | 8 Netatmo links once hosted |

Rough remaining: **~60–65 File uploads + ~9 Links** if B+ images are skipped.

## Client decisions

1. Confirm Library (not product fields) for Other Source — OK?
2. Finish full gap vs curated subset?
3. Hosted URLs for 8 videos + oversized CEU pptx, or skip?
4. User-group restrictions for Competitor Conversion + priced planograms?
5. Per-SKU document URLs later? (needs their map)

## Admin work order

1. Convert `.pptm` → `.pptx`; get hosted URLs for videos + big CEU.
2. Finish **Sell Sheets and Literature** labels above.
3. Load LED / Technical / Training / CEU / Competitor.
4. Add Video + CEU **Links**.
5. Restrict internal entries by user group as decided.
