# Magic Lite / NSL (`mali`, org 285) — Execution Handoff · HS #14727

**Created:** 2026-07-23 · **For:** a fresh agent to review, finalize, and execute the import + image upload.
**Supersedes for build/execution:** `HANDOFF_2026-07-23_HS14727_recovery.md` (read that first for the architectural truth and importer guardrails; this doc is the *do-the-work* layer on top of it).

> ⚠️ Read the recovery handoff §2 (architecture), §5 (hidden products — do NOT blanket-unhide), and §9 (importer guardrails) before touching anything. This doc adds: the rebuilt product file, two completed image scrapes, and a full mapping of the HelpScout thread to concrete actions.

---

## 0. What changed since the recovery handoff (all verified 2026-07-23)

Three parallel work products now exist and must be **merged** before import:

1. **Rebuilt product file** — `_MALI_FIX_REVIEW/products.csv` (600 rows, 55 cols). Newer than `Ready_For_Import/products.csv` (they differ on every row). Prices rounded/crosswalked/gap-filled; 104 image repoints applied.
2. **Magic Lite website scrape** — `~/Downloads/Mali_Mismatched_Images/scrape_out/` → **98** FTP-ready JPGs + `products_imagefilename_patch.csv`.
3. **NSL website scrape** — `~/Downloads/Mali_Mismatched_Images/scrape_out_nsl/` → **32** more JPGs + `nsl_imagefilename_patch.csv`. Residual needing studio photography: **111**.

**The job:** fold the 130 scraped-image filenames into the rebuilt `products.csv`, upload the 130 JPGs to FTP `/images`, resolve the open decisions in §5, then import in order and verify.

---

## 1. Asset inventory (verified paths + state)

| Asset | Path | State |
|---|---|---|
| **Rebuilt products** (use this as base) | `00_Import_Files/_MALI_FIX_REVIEW/products.csv` | 600 rows; ML 597/600, NSL 578/600 priced; net_price 600/600; 104 repoints applied |
| Stale products (do NOT use) | `00_Import_Files/Ready_For_Import/products.csv` | superseded; 25 raw gaps, float noise |
| Build notes | `_MALI_FIX_REVIEW/BUILD_SUMMARY.md` | documents drops, prices, repoints |
| Verification prompt (context) | `_MALI_FIX_REVIEW/MALI_VERIFICATION_PROMPT.md` | the skeptic pass spec; see §5 conflict |
| Dropped SKUs (the "94 ghosts") | `_MALI_FIX_REVIEW/BUILD_dropped.csv` | 87 not-in-pricebook + 7 discontinue |
| **94-ghost triage** (new, 2026-07-23) | `_MALI_FIX_REVIEW/dropped_94_triage.csv` | 76 discontinued-priced / 7 web / 11 remove |
| Price resolution audit | `_MALI_FIX_REVIEW/pricing_resolution.csv` | per-SKU price + source |
| NSL pairing to-do | `_MALI_FIX_REVIEW/needs_nsl_pairing.csv` | 15 rows needing NSL price/code |
| Repoints (already applied) | `_MALI_FIX_REVIEW/image_repoints_119.csv` | 119 repoints (104 landed on kept SKUs) |
| Photos still needed (build view) | `_MALI_FIX_REVIEW/BUILD_photos_needed_kept.csv` | 326 kept rows on family/placeholder |
| **ML scrape images** | `~/Downloads/Mali_Mismatched_Images/scrape_out/images_ready/` | **98** JPGs, `<code>.jpg`, case-correct |
| ML scrape patch | `…/scrape_out/products_imagefilename_patch.csv` | 98 rows (BaseItemCode → Proposed) |
| **NSL scrape images** | `~/Downloads/Mali_Mismatched_Images/scrape_out_nsl/images_ready_nsl/` | **32** JPGs, `<code>.jpg`, case-correct |
| NSL scrape patch | `…/scrape_out_nsl/nsl_imagefilename_patch.csv` | 32 rows |
| Residual photography list | `…/scrape_out_nsl/NEEDS_PHOTOGRAPHY_RESIDUAL.csv` | **111** SKUs → client studio shots |
| inventory / stories / customers | `Ready_For_Import/` | inventory 694, stories 694, customers 3,418 — still carry the 94 ghost codes |
| AUG2025 price lists | `~/Downloads/Attachments (10)/ML|NSL PRICE LIST AUG2025 FLAT WITH DN.xlsx` | source of truth for prices/UPC |
| Client gap workbook | `~/Downloads/Attachments (9)/Copy of Mali_Pricing_Gaps_July15.xlsx` | already partially merged |
| Backend code | `/Users/kylorjohnson/supercat-code/supercat_server` | importer + eOL/iPad logic |

**Data access:** Postgres MCP `user-supercat-postgres-vpn` (read-only, org id **285**). HelpScout via BigQuery `user-bigquery-admin` (`helpscout.conversations`, `number = 14727`). **Jira is READ-ONLY.**

---

## 2. Image reconciliation (verified) — what actually needs to happen

- 130 scraped SKUs = 98 ML + 32 NSL. **All 130 are in the kept 600.** None are ghosts.
- **Filenames are case-correct** (`ACC-DT.jpg`, `DR-96-24-TM-5N1D.jpg`); extension lowercase; matches `ImageFileName` exactly. No rename needed.
- Only **20 of 130** already carry the correct `ImageFileName` in `_MALI_FIX_REVIEW/products.csv`. The other **110 still point at wrong/family images** (e.g. `LEDDR-12-60W` → `MLDRE-40-24-DM.jpg`). These 110 are the visible "wrong picture" complaints.
- Overlap between the 119 repoints and the 130 scrape patches = **1**. They're complementary; **where they overlap, the scrape patch (real scraped photo) wins.**
- Some patch rows are `add-missing` where `ImageFileName` is unchanged but the **file** was wrong → just overwrite the file on FTP (e.g. `SL-OD-BWBC-6`).

**➡️ Two coupled actions, neither optional:**
1. **Patch `products.csv`:** for each of the 130, set `ImageFileName = <BaseItemCode>.jpg` (single hero; drop the borrowed `-2/-3` gallery entries). Apply scrape patches over the 104 repoints on conflict.
2. **Upload all 130 JPGs** to FTP `/images` (flat root). Any `ImageFileName` value that has no matching uploaded file will render blank — verify 1:1.

---

## 3. Execution plan (order matters)

### Step 1 — Finalize `products.csv` (Bucket A + images)
Working from `_MALI_FIX_REVIEW/products.csv`:
1. Apply the 130 image patches (§2) → set single correct `ImageFileName` per SKU.
2. Resolve the 25 price blanks per §5 decision (or leave ML-only rows blank NSL intentionally — that is valid, not an error).
3. **Retire `net_price`** level (USD currency holding CAD/ML values — see recovery §3). Confirm nothing renders it before removing.
4. **94 dropped SKUs (§5.2 — triaged, see `dropped_94_triage.csv`):** re-add the **83 legitimate** ones to `products.csv` (76 priced from the DISCONTINUED list + mark clearance/EOL; 7 web-only with price=TBD), and **remove the 11 "nowhere" codes** from `inventory.csv`/`stories.csv`. This brings products to ~683 and eliminates the ghost warnings. (This supersedes any "trim to 600" instruction.)
5. Fix inventory numerics in `inventory.csv`: `MGWL-06-6000K = 258.5` (→ round) and **13 negative cells / 7 rows** (→ clamp to 0). *(Live DB currently holds an older import: 258.0 and 11 neg cells — the staged file is what will overwrite it.)*

### Step 2 — Promote & stage
Copy the finalized files into `Ready_For_Import/`. Keep a dated backup of what you replace.

### Step 3 — FTP upload
- 130 product JPGs → `/images` (flat root; subfolders ignored). ≤500/batch, 30–45 min processing.
- CSVs → `/data`.

### Step 4 — Import (mandatory order, full files)
`options.csv` → `option_groups.csv` → `products.csv` → `stories.csv` → `inventory.csv` → `customers.csv`
- `products.csv`: omitted rows **soft-delete on a clean import**; skipped if ANY error row. Send the **full** file.
- `inventory.csv`: **hard-deletes all inventory + reloads** — must be clean (this is why Step 1.5 matters).
- Re-send `option_groups.csv` after `options.csv`.

### Step 5 — Verify every import
Tools → Admin Reports → **File Import Status**. Blue-link timestamp = problems (open for line numbers). Fatal = whole file rejected; Error = imports good rows but **skips deletes**; Warning = imports + deletes omitted.

### Step 6 — Prove it on a rep profile (highest leverage)
Create Jen's **ML** and **NSL** eOL/rep profiles and re-check the client's complaints there. Most are Admin-view artifacts (see §4).

---

## 4. HelpScout #14727 — every item mapped

Legend: ✅ done/verified · 🔧 action in this pass · 🧑‍⚖️ needs Kylor decision · 👀 verify on rep profile · 📷 client photography · 🛠️ dev

### Deep-dive "wrong picture" list
| Client item | Status | Notes |
|---|---|---|
| NSL codes are actually ML codes; "was NSL price list used?" | 🧑‍⚖️ | **Doc conflict — see §5.1.** NSL levels ARE USD (verified). "NSL price list used?" → yes, crosswalk + AUG2025 NSL list applied. |
| Library shows ML info for NSL (catalogue/instructions/product list) | 👀 | `shared_resources` split claimed; **verify NSL folders restricted to NSL user types** (§6 SQL). Likely also an Admin-view artifact. |
| `DR-96-24-TM-5N1D` pic wrong | 🔧 | Fixed in scrape (content-fix). In the 130 patch. |
| Outdoor Streamline connectors — no picture | 🔧 | `SL-OD-B2BC / BWBC-6 / W2BC-72` imaged. |
| `YH-SIGNAL-AMP` shows eStrip | 📷 | Needs photography (not on either site). |
| eStrip connector pics = the eStrip | 🔧/📷 | `LES-*` closed via NSL `MLS-*` naming; remainder residual. |
| Neon Flex accessory pics = the Neon Flex | 📷 | Mostly residual. |
| Wedge light lamp pics = Wall Washer | 🧑‍⚖️/📷 | Item may be out-of-pricebook (check drop list). |
| `ES-EXT-ENDCAPS` = the extrusion | 🔧 | Fixed. |
| Non-dimmable driver pics = dimmable | 🔧 | Repointed in scrape. |
| Hard Strip power feed = the fixture | 🔧/📷 | PC/PF partly closed via NSL; some drawings. |
| `LV-HS-MC30` wrong pic | 📷 | Needs photography. |
| `ACC-12G-2C-BUR` wrong pic | 🔧 | In NSL patch. |
| All flood-light accessory pics wrong (`FL-*`) | 🔧/📷 | `FL-SH/WG` real art; `FL-Y/ADM` drawings; some out-of-pricebook. |
| `ACC-DT / ACC-PC / ACC-WIFI` wrong | 🔧 | Imaged (ML scrape). |
| RGB controllers/amplifiers = old codes+pics | 🧑‍⚖️ | "old codes" → confirm current code set before imaging. |
| Outdoor sconce pics = `SL-CC` | 🧑‍⚖️/📷 | Check pricebook status. |
| `LBR-II-KIT`, `LST-II-KIT`, `BL-CC`, `SL-CC` pics wrong | 📷 | Largely residual/finish. |
| Wire types (minidisc & disc) pics wrong | 📷 | `LW-*` wire = accessory, residual. |
| Construction plates / square trims / surface-mount trims / fire-rated trims & beauty rings | 📷 | `LVLDL*` trims — NSL doesn't picture; residual. |
| `LV-DL-EX-10-L / -30-L` wrong | 📷 | Residual. |
| `WSL-15-30K-BN`, `SL66-4FT-40W-40` | ✅/📷 | In the **DISCONTINUED** price list (real EOL) → re-add per §5.2, mark clearance; needs photo. |
| Work Light & Tri-proof accessories | 🔧/📷 | `LWL-MM/FM/TM` closed from NSL Catalog 2025; rest residual. |
| "Why is Switchex (`SX-*`) there?" | ✅ | **Answered:** `SX-*` are in the DISCONTINUED price list (clearance / "while qty lasts"). Keep as clearance or drop — client's call. |
| Aluminum extrusion accessory pics wrong | 🔧/📷 | Some closed; `LV-ALP2908-EC`-type cross-family maps were rejected → residual. |
| Tape page contradiction: `SL-ID-30K-LP-20-A8` "20 or 100 ft", qty 374 | 🛠️/🧑‍⚖️ | Units ambiguity (feet vs spools) + the **eOL inventory-render gap** (recovery §4). Needs a units label decision + dev call on live qty. |

### Jen's action list
| # | Item | Status |
|---|---|---|
| 1 | Set customer pricing defaults | ✅ `DefaultPriceCode` set on all 3,418 (nsldn ×3,003 / mldn ×415). 👀 confirm eOL uses it (code caveat: eOL falls to *group* default unless an associated customer exists — recovery §6). |
| 2 | Add USD pricing to NSL | ✅ nsldn/nsllist = USD, 578/600 filled; 22 pending (§5). |
| 3 | Library ML-under-ML / NSL-under-NSL | 👀 verify `shared_resources_user_types` (§6). |
| 4 | Quantities & item codes per pack size | 🛠️ eOL inventory-render gap (recovery §4) + units label; 🧑‍⚖️ variant strategy (recovery §7). |
| 5a | Cut sheets/instructions NSL-only | ✅ `CutSheetNSL/InstructionsNSL` → NSL groups (verified). 👀 confirm on rep profile (Admin sees both). |
| 5b | Library NSL-for-NSL | 👀 same as #3. |
| 5c | ML & NSL UPC both showing | ✅ `ML_UPC`→ML groups, `NSL_UPC`→NSL groups (verified). Both visible only in **Admin view**. 👀 confirm on rep profile. |
| 6 | Confirm all product images corrected | 🔧 130 fixed this pass; 📷 **111 residual** need client photography (`NEEDS_PHOTOGRAPHY_RESIDUAL.csv`). |
| 7 | Confirm NSL item codes corrected | ✅ Decided (§5.1): ~57 codes differ (585 identical) → rep-profile verify first, then `NSL_Code` field + train reps on those ~57. Codebase confirms ML headline code can't be hidden per group (that's Option 2 / multi-org later). |

**Pattern:** items 1, 3, 5a–5c, and half of the "wrong code/UPC/library" complaints are **Admin-view artifacts**. Creating Jen's rep profiles (Step 6) retires most of them without any data change.

---

## 5. Open decisions for Kylor (resolve before/at import)

**5.1 — NSL item codes (elite POV; resolves the two-doc conflict).**
Grounding facts (verified from the two AUG2025 lists, 2026-07-23): **585 codes identical** across ML & NSL, **66 ML-only, 57 NSL-only** → Jen's "most are the same, some differ" is exactly right; the real divergent set is ~57 NSL codes (Brick Star `LEDBS-II`↔`LBR-II`, Step Star `LEDSST-II`↔`LST-II`, Mini Disc `LEDMD-S`↔`LEDMDS`, transformers `DLT-*-347`↔`DLT-277`/`TR-*`). Crosswalk source: `recon_shared_family.csv` (113 ML→NSL family matches).

Architectural constraint: `mali` is **one org, one `products` row per SKU, one `item_number`** (the master key linking products↔inventory↔stories↔images↔orders). You cannot show two different *primary* codes from the same row. The catalog was built from ML's catalog → divergent SKUs carry the ML code → NSL reps see it. That is the root complaint.

Three options:
1. **Shared ML code + `NSL_Code` custom field + rep training (DECIDED — start here to buy time).** NSL-group-restricted field, populated only for the ~57 divergent SKUs from the crosswalk. Non-breaking, fast, fits a late-stage project. Frame to the client as: *the headline code is the shared catalog code; your NSL code is shown in the "NSL Code" field* — a short training exercise for just those ~57 SKUs (the 585 shared codes are identical, no confusion).
2. **Two separate orgs (deliberate later step).** Dedicated NSL org, NSL BaseItemCodes, USD-only, own library/inventory. Only path where NSL customers *never* see an ML code. Second full build + double maintenance — plan it as the follow-on once the relationship is stabilized, not now.
3. Rebuild the shared catalog on NSL codes — **not viable** (one row/one code; breaks ML).

**Codebase verification (2026-07-23, why Option 1 can't fully hide the ML code):**
- eOL product detail renders the code unconditionally: `ecat_products/show.html.erb:19` → `<h2><%= @product.item_number %></h2>` (no user-type gate). Same in the grid (`_product_grid_meta.html.erb:4`) and product table.
- **No per-user-group control exists** to hide/relabel `item_number`. Every `display_item_number*` in the code is unrelated: `configured_item_number_builder`/`order_item.display_item_number` = order-line *construction*; `display_item_number_price_row` = iPad *report/tearsheet* layout; `sort_helper.item_number_label` = column-header text. None is a per-brand swap.
- Custom fields **are** user-type restricted (`custom_fields_user_types`, verified), so `NSL_Code` shows only to NSL — **as an added row, not a replacement** for the headline code.
- `item_number` is the **master order/inventory/story/image key**, so swapping what the iPad API sends per user is **unsafe** (breaks order submission + inventory matching) and the iPad is a compiled app anyway. → A quick per-group code toggle is NOT a safe option; genuine ML-code suppression = Option 2.

**Net:** Option 1 gives NSL reps their code (visible only to them) but the ML code still appears as the product headline for everyone. That's acceptable as a time-buyer + training; escalate to Option 2 if/when Jen requires the ML code to disappear entirely.

**Biggest lever first:** the transcript says the confusion is that *"the admin portal was showing both brands mixed together."* `NSL_UPC`/`CutSheetNSL`/`InstructionsNSL` are already correctly NSL-group-restricted (verified). So **create Jen's NSL rep/customer login and re-verify there before any code build** — that alone retires most of HS item 7, UPC-mixing, cut-sheet, and library complaints. Only the ~57 divergent codes remain, and Option 1 covers them.

**5.2 — The 94 dropped SKUs (`BUILD_dropped.csv`) — triaged; Kylor's call = "add what we have, flag for review".**
The build dropped these against the *active* lists only, but there are **separate DISCONTINUED price lists** — which is why they're in inventory but had "no price." Triage (active + discontinued lists + both websites, 2026-07-23):

Full per-SKU breakdown: **`_MALI_FIX_REVIEW/dropped_94_triage.csv`** (bucket, discontinued-list price+DN, website hit, recommended action).

| Bucket | Count | Handling |
|---|--:|---|
| **In DISCONTINUED price list** (has list+DN price) | **76** | Re-add, price from discontinued sheet, mark clearance/EOL (incl. Switchex `SX-*` → answers HS "why is Switchex there?") |
| **On website, not in any list** | **7** | Re-add, price = TBD → client confirms (`IG-01-12V-*`, `NFLX-RGB-CK-6FT-O`, `YH-HRF50CA120S505060`, `LT-WIFI-RM`; `FL-ADM/SH/WG-15` match at family level) |
| **Nowhere** (no list, no site) | **11** | Remove from `inventory.csv`/`stories.csv` too (kills ghost warnings) |

So only 11 of 94 are true junk. Re-add the 83 (76 priced from discontinued list + 7 price-TBD); source images via the same scrape/photography flow; flag all for client review. This replaces the "trim to 600" path in Step 1.4 with "re-add 83, remove 11."

**5.3 — eOL live inventory (dev).** eOL has no code path to render inventory custom fields (recovery §4, code-verified). Either approve a small dev change or set the expectation that live qty is **iPad-only**. Drives HS item 4.

**5.4 — Variant strategy (recovery §7).** Un-hide priced variants vs build a real options/matrix vs rely on related-products. Confirm UX preference with Jen; do **not** blanket-unhide.

**5.5 — `net_price` retirement.** Confirm safe to remove (nothing should render a USD-labeled level holding CAD values).

---

## 6. Verification SQL (read-only, org 285)

```sql
-- Library split: NSL folders restricted to NSL user types?
select sr.id, sr.name, array_agg(ut.name order by ut.name) as visible_to
from shared_resources sr
left join shared_resources_user_types srut on srut.shared_resource_id = sr.id
left join user_types ut on ut.id = srut.user_type_id
where sr.organization_id = 285
group by sr.id, sr.name order by sr.name;

-- Confirm image references resolve (after patch): every ImageFileName should have an uploaded file
select item_number, images_json from products
where organization_id = 285 and not deleted and item_number in ('LEDDR-12-60W','DR-96-24-TM-5N1D');

-- Price levels + currency (net_price should be the only oddball)
select code, name, currency_code from price_levels where organization_id = 285 order by position;

-- Custom-field group restriction spot-check (UPC / cut sheets)
select cf.field_name, array_agg(ut.name order by ut.name)
from custom_fields cf
left join custom_fields_user_types cfut on cfut.custom_field_id = cf.id
left join user_types ut on ut.id = cfut.user_type_id
where cf.organization_id = 285 and cf.field_name in ('ML_UPC','NSL_UPC','CutSheetNSL','InstructionsNSL')
group by cf.field_name;
```

Confirmed-live baseline (2026-07-23) to diff against: 600 active products (all `trade_name_code=ML`), 224 hideable, options=2, inventory 694 (qty_available null 0/694), customers 3,418, user-type auth ML→mldn/mllist · NSL→nsldn/nsllist · eOL sites likewise · Admin=none, mobile sites `12`=ML/`13`=NSL with all property flags at default.

---

## 7. Definition of done

- [ ] `products.csv` finalized: 130 image patches applied, 25 price blanks resolved-or-intentional, net_price retired, 94-ghost decision reflected.
- [ ] `inventory.csv`/`stories.csv` trimmed (or ghosts re-added w/ prices), numerics rounded/clamped.
- [ ] 130 JPGs uploaded to `/images`; every `ImageFileName` has a matching file.
- [ ] Imported in order; **File Import Status clean** (no blue links / Error rows).
- [ ] Jen's ML + NSL rep profiles created; Admin-view complaints re-checked on them.
- [ ] §5 decisions recorded (esp. NSL codes 5.1); `NEEDS_PHOTOGRAPHY_RESIDUAL.csv` (111) sent to client.
- [ ] Nothing written to Jira; no legacy folders touched.

## 8. Guardrails (do not violate)
Full product file every time (omitted = soft-delete on clean import). Inventory hard-deletes+reloads. Custom fields must be pre-registered ("Send to iPad"), matched case-insensitively. Images: `.jpg`, flat `/images` root, name == `ImageFileName` exactly, ≤15 MB, ≤500/batch. Jira read-only. Do not read/run anything in frozen Insightful legacy folders.
