# Legrand — Client Confirmation Checklist

Prepared for the client meeting. Based on the live org (`leg`, id 273) audited in
Postgres and the current build (1,020 products) in this `Build/` folder.

**Ground truth (re-audited 2026-07-14):** live `leg` now has **1,020 active
products**, **5 price levels** (`retail`, `imap`, `canet`, `caimap`, `camsrp`),
**~1,194 inventory rows**, **1 test customer**, and a large custom-field schema
left over from the POC. Library work is **in progress** (sections created;
Catalogs + first Sell Sheets uploaded — see §G). Confirm whether the live
product file is already this build or still needs a full replace before go-live.

Companion docs: `TAXONOMY.md` (full Group→Category sheet), `group-category-map.csv`,
`custom-fields-setup.md`, `related-items-review.md`, `longdesc-review.md`,
`inventory-review.md`, `pricing-review.md`, `library-plan.md` (Other Source
collateral — Library vs products, gap list, hosting/conversion).

## Fixed since first pass (2026-07-14 internal QA)

- **`LongDesc` exceeded eCat's 50-char limit on 668/1,020 rows** (avg 61, max
  143) — the first pass copied the source `Product Name` in verbatim, and
  `ShortDesc` was left blank everywhere. Now cleaned (brand/trademark/
  "with Microban" boilerplate stripped, Finish anchored to the end so
  truncation never drops the color) and truncated at a word boundary where
  still needed. 0 rows now exceed 50 chars; `ShortDesc` is populated on all
  1,020. See `longdesc-review.md` for every row that got truncated plus 73
  SKUs where the source `Finish` column disagrees with the color word in
  `Product Name` (flag to Legrand's data team).
- **`ASPD1531W277` (White, 277V half-size switch) was missing from its own
  RelatedItems family** — traced to a source typo ("227V" instead of "277V"
  in `Product Name`) that broke the finish-stripped grouping key. Fixed in
  the build; confirm the source typo with Legrand. See `related-items-review.md`
  for why we fixed this one case by hand rather than adding fuzzy/similarity
  matching (tested it — too many false positives on this catalog, e.g. it
  wants to merge 15A/20A and 1-gang/2-gang product families).
- **20 SKUs had a guessed `ImageFileName`** (`{code}.jpg`) that matched no
  real downloaded file. Now left blank for those 20 rather than shipping an
  unverified filename — see `IMAGE_REQUIREMENTS.md` for the list; confirm
  with Legrand whether images exist for them.
- **Pricing gaps traced to source, not the script.** Checked all 32 SKUs with a
  missing US or CA net price against every sheet of all 4 Legrand price
  workbooks (not just the active sheet). All 32 are explained: 4 are on
  Legrand's CA "Discontinued" sheet and absent from every US sheet too (likely
  fully EOL); 1 (`AWP6GBL1`) is a real, priced Canada-only color; 1
  (`R26USBPD65WCC6`) is a brand-new SKU priced in Canada before the US; the
  remaining 26 CA-only gaps split into "discontinued in Canada only, still
  active in the US" (6) and "US-only product line, never listed in the CA
  files at all" (20 — AFCI/GFCI combo devices + Microban/screwless-plate
  SKUs). Also confirmed CA radiant iMAP is `"N/A"` on literally every radiant
  row in the Canadian file — not a parsing gap, Legrand doesn't publish it.
  Full SKU-by-SKU evidence in `pricing-review.md`.

---

## A. Taxonomy — decisions

Structure built: **Trade Name = Legrand → Collections = adorne (455) / radiant (565)**,
**36 categories** mapped into the client's **5 existing Admin groups**.

1. **Confirm the brand model.** We use Legrand as the trade name with adorne/radiant
   as collections (matches public branding). The POC had adorne/radiant as *trade
   names* — those go empty and auto‑prune on import. OK?
2. **7 category group placements to confirm** (best‑guessed — see CONFIRM rows in
   `TAXONOMY.md`):
   - `Connectivity`, `Night Lights`, `Antimicrobial Devices`, `EV Charging`,
     `Locator Light` → currently **Switches & Outlets**
   - `Fan Control` → currently **Dimmers**
   - `Smart Dimmer` → currently **Smart Technology**
   - **Or** add a 6th **Accessories** group for the odd ones.
3. **`Light Switch` vs `Switches`** — kept separate (adorne vs radiant wording).
   Merge into one category?
4. FYI (already applied, no action): merged `Outlet`→`Outlets`, `Night Light`→`Night Lights`.

## B. Pricing & currency — decisions

Six price streams built: **US** Net / Retail(MSRP) / iMAP, **Canada** Net / iMAP / MSRP.

5. **Confirm the levels + labels** and that these are all reps should see.
6. **Coverage gaps — root-caused, need business decisions (see `pricing-review.md`):**
   - US iMAP on **592 / 1,020**; Canada iMAP on **455 / 1,020** — **confirmed** (not a
     parsing miss): every one of the 565 radiant rows in the CA price file has literal
     `"N/A"` in the iMAP column. adorne CA iMAP is full coverage (455/455). Hide the CA
     iMAP level for Canadian radiant reps, or is a real number coming?
   - **6 SKUs have no US net** (import as 0.00) — 4 look fully EOL (on Legrand's CA
     Discontinued sheet, absent from every US sheet too — drop from the file?), 1 is a
     real Canada-only color (`AWP6GBL1`), 1 is a new SKU priced in CA before the US
     (`R26USBPD65WCC6`, needs an updated US price list).
   - **26 SKUs have no Canadian net** — 6 discontinued-in-Canada-only (still active/priced
     in the US), 20 are US-only product lines (AFCI/GFCI combo devices + Microban/
     screwless-plate SKUs) that never appear in any CA sheet — confirm these aren't sold
     in Canada.
   - No promotional prices at all (0 of 1,020) — none needed now?
7. **US vs Canada separation:** Divisions (US div / Canada div) or User Groups
   controlling visible price levels? Canadian customers must default to a **CAD**
   level, never the built‑in US Net.

## C. Product content — the big gap

8. **Rich spec fields are empty in the source.** The POC org is set up for
   `voltage, wattage, switch type, works‑with, wire size, mounting type,
   number of switches/gangs, bulb compatibility, warranty, product line, color,
   Prop 65, ROHS`. **Do they have this data to provide, or launch blank?**
   *(Document/PDF columns — cut sheets, install guides, brochures — are a
   separate decision: see §G. Recommendation = Library, not product fields.)*
9. **Product stories:** 908 / 1,020 have romance copy. OK to launch the other ~112 blank?
10. **`Finish` near‑duplicates** (each is its own filter facet — merge any?):
    - `Mirror` / `Mirror White` / `Mirror Black`
    - `Gloss White` / `Gloss White on White` / `Powder White` / `Matte White`
    - `Brushed Stainless` / `Brushed Stainless Steel` / `Stainless Steel` / `Spiraled Stainless`
    - (already auto‑fixed: `Grahite`→`Graphite`, `Tri Color`→`Tri‑Color`)

## D. Catalog completeness & inventory

11. **247 inventory SKUs are not in the product file** (e.g. `1597`, `1597BKCCD12`).
    Discontinued/components to leave out, or missing sellable items to add?
12. **73 products have no inventory row** — show no stock until their export includes them. OK?
13. **Inventory semantics:** we set `QtyAvailable = QtyOnHand` (no separate
    backorder/reserved columns in source). Correct? (63 negative on‑hand rows all
    correspond to "to be sched" items; 101 blank next‑receipt dates.)
14. **`NewItem` = "N" on all 1,020** — flag any as new?

## E. Handling / misc fields

15. **`drop_ship` = "Y" on every item** — entire catalog really drop‑ship?
16. **`shipped_via` = literal "Fedex or Truck" on every item** — real value or placeholder?
17. **`order_uom`:** UNIT (843), blank (169), MASTER (8) — blanks/MASTER intentional?
18. **`UPCValue`** present on all 1,020 — accurate?

## F. Customers (next file)

19. Real customer file still needed: source/format, each customer's
    **DefaultPriceCode** in its own currency (US vs CAD), and **territory/rep**
    assignment for filtering. (Only customer in the org now is "eCat Test" with
    invalid price code `0`.)

## G. Library / collateral (the "Other Source" files)

Source: `Source Data/Other Source/` — **120 files** (~406 MB: PDFs, images,
PowerPoints, videos, docx). Full ops plan in `library-plan.md`.

### Library vs products — recommendation (confirm)

| Put in… | What | Why |
|---|---|---|
| **Library (Admin → Library)** | Sell sheets, catalogs, brochures, training, CEU, wiring, competitor conversion, Netatmo how‑tos, display kits | Org-level collateral; iPad PDF viewer + email/share; **no CSV/FTP bulk import** |
| **Product file / custom fields** | Spec *text* only (voltage, finish, etc.) if they ever provide it | Custom fields are **text columns** — no file upload, no PDF viewer on the product |
| **Product images (FTP `/images`)** | SKU catalog photos only | Not for sell sheets / B+ campaign packs |

**Do not** map Other Source PDFs into product custom fields. The CAD source’s
`Instruction` / `Parts Diagram` / `Spec Sheet` columns are **empty on all 1,020
rows**, so there is nothing to attach per SKU today. If they later want
cut sheets on the product detail screen, they must provide a **SKU → document
URL** map — that is a separate, later workstream (text URL in a custom field is
a weak stopgap; Library remains the right home for browse/email).

### Already live in `leg` (skip re-upload)

| Section | Status |
|---|---|
| **adorne Displays** | 3 entries — done |
| **Wiring Diagram** | 3 entries — done |
| **radiant Advance Dimmers** | 6 files + 2 video links (older radiant/LED set) — leave; new LED pack goes in **LED Advanced Dimmer** |
| **Canadian Price List** | 2 CA price xlsx — done (not from Other Source) |
| **Catalogs & Brochures** | 2 entries — 2026 Collections Catalog + adorne Consumer Brochure June 2026 — done |
| **Sell Sheets and Literature** | 5 started (USB charger, Raise the Bar, DSO Look Book, DSO Catalog, adorne Consumer Brochure) — continue |
| **LED Advanced Dimmer / Technical Help / Training / CEU / Competitor Conversion** | Sections exist, **0 entries** — still to load |
| **Videos (Promo) / Videos (Install)** | Sections exist, **0 entries** — waiting on hosted URLs |

Also skip: `BR1896-PS-radiant.pdf` (already under radiant Advance Dimmers).

### Must host externally → Library **Link** (not File)

| Asset | Why |
|---|---|
| **8 Netatmo `.mp4` how‑tos** | `.mp4` is not an allowed Library file type |
| **`CEU/The Art of Resi Lighting 11-6-25.pptx`** (~56 MB) | Hard **30 MB** upload cap |

Need public `https://` URLs (YouTube / Vimeo / SharePoint — they already use
SharePoint for one radiant video link). Put Install how‑tos in **Videos (Install)**;
voice/access how‑tos in **Videos (Promo)**.

### Must convert before upload

| Asset | Fix |
|---|---|
| `Training Presentations/TU & LED Adavanced Dimmer TW.pptm` | Re-save as **`.pptx`** (`.pptm` rejected) |

*(Display `.jpeg`s already live as `.jpg` — no rename needed.)*

### Other upload rules

- Allowed types: `pdf, pptx, docx, doc, xls, xlsx, jpg, png, …`
- Files **>5 MB** still upload but iPad views them **online only** (email OK offline)
- **Dedupe:** upload `BR1796` + `CAT3438` once in Sell Sheets; skip copies inside the LED pack
- **Optional skip:** LED pack `B+ Images/` (~29 JPGs) unless reps need them in Library
- **One revision check:** live `EWS-PS-SS-3871-LED-Advanced-Dimmer-Offering.pdf` vs local `SS3871-PS-…` — keep newer, don’t double
- Sell-sheet **Labels** (rep-facing names): see working list in chat / continue matching the 5 already uploaded (`Raise the Bar`, `DSO Catalog`, etc.)

### Client decisions

20. **Confirm Library (not product fields)** for Other Source collateral — OK?
21. **Scope:** finish loading the gap (~65–70 uploads + ~9 links if we skip B+ images), or a smaller curated subset?
22. **Videos + oversized CEU pptx:** provide hosted URLs, or skip those entries?
23. **Restricted visibility:** Competitor Conversion (agent program) and price-bearing
    planograms (`SS3329R2…PlanOGram-price`, `…price-CA`) — which user groups see these?
24. **Per-SKU documents later:** only if they deliver a SKU → URL map for cut sheets /
    install guides on the product detail (out of scope otherwise).

---

## Appendix — our Admin setup (no client input needed)

- **Price levels — DONE live:** `retail`, `imap` (USD); `canet`, `caimap`, `camsrp`
  (CAD). Built‑in Net receives the US `NetPrice` column. Confirm labels/visibility
  with client (§B); no need to re-create.
- **Register custom fields** (`Send to iPad`) per `custom-fields-setup.md` —
  at minimum anything still missing for this build (`Finish` / COO may already
  exist). Carton/freight: register but prefer Hide from details unless they want
  them on-screen.
- **Groups + Categories — DONE 2026-07-23:** all 36 categories assigned to their
  5 groups via API. Default Group is empty. See ADMIN_SETUP.md §6 for the full map.
- **Quick View — DONE 2026-07-23:** Line 2 = Short Desc, Line 3 = Finish. POC
  artifact labels ("Watts", "Available") cleared.
- **Territory banner — DONE 2026-07-23.**
- **No-image list — DONE:** `no-image-skus.csv` generated (175 SKUs; 144 are
  Netatmo cluster WNRL*/WNAL*/WNRCB* etc.; 31 are AFGF/AWP/misc. Send to Legrand
  asking if images exist in WebDAM.)
- **Library sections — DONE (88 entries live, 2026-07-23):** All 6 remaining
  sections uploaded: Sell Sheets and Literature (34), LED Advanced Dimmer (20),
  radiant Advance Dimmers (8), Technical Help (7), Training (3), CEU (3),
  Competitor Conversion (2), plus existing Catalogs & Brochures, adorne Displays,
  Wiring Diagram, Canadian Price List, eCat Tutorials. Still pending: 9 video/
  oversized items that need hosted URLs from Legrand (8 Netatmo videos + 56 MB
  CEU pptx). Those go in as Link entries once Legrand sends hosted URLs.
- **Import order:** Products → Stories → Inventory → Customers. Verify each in
  **Tools → Admin Reports → File Import Status** (blue‑link timestamp = problems).
  *(If options/option_groups are ever added: options → option_groups → products.)*
