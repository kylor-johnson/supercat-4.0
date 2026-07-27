# Launch Readiness Checklist — Magic Lite / NSL (`mali`, org 285)

| Field | Value |
|---|---|
| **Client** | Magic Lite (ML, CAD) + National Specialty Lighting (NSL, USD) |
| **Org** | `mali` · id **285** |
| **Decision date** | 2026-07-23 |
| **Target meeting** | Next call with Jen Zorony / Jen Penton (Jen P back next week) |
| **Ticket** | HelpScout #14727 |
| **Launch scope under decision** | (A) beta reps in-hands on **iPad**, and/or (B) **eCat Online** public |

### Overall recommendation

**CONDITIONAL GO — iPad beta only.**  
**NO-GO — eCat Online public** until Dev confirms inventory rendering + pricing workflow, and pack-size discoverability is verified on a rep profile (both sites now hide `hideable` products).

**Conditions for iPad beta GO:**
1. Create Jen Z’s missing **ML Reps** login (NSL Reps alias already exists; clear `is_admin` on +user aliases or use a clean NSL reviewer) and complete brand-separation verify on both profiles.
2. Confirm with Jen that pack/length variants are findable enough via related products (do **not** blanket-unhide).
3. Set expectation in writing: live qty on **eOL product detail is not available yet** (iPad shows brand qty fields). Tape spool labeling is **live** on the 8 Streamline SKUs (ShortDesc/LongDesc); optional UOM field still open.
4. Send the **311** shared-primary residual photography list (`RESIDUAL_SHARED_PRIMARY_IMAGES_2026-07-23.csv`); accept incomplete imagery on those SKUs for beta. Do **not** cite 68/111.
5. Book Brittni / Endeavour-IT this week for SFTP + GP export fix (ops sustainability, not day-1 catalog block).

---

## Checklist

| # | Item | Domain | Status | Launch gate? | Owner | Evidence (query / ticket / screen) | Next action + ETA |
|---|---|---|---|---|---|---|---|
| 1 | Active catalog loaded & clean | Data integrity | ✅ Ready | MUST-PASS | SuperCat | Postgres: **683** active. Latest products import **2026-07-23 21:22 UTC** (warnings only for unused custom fields). Tape spool ShortDesc/LongDesc + LP MaxLength=40Ft confirmed live on 8 Streamline SKUs. | None — keep sending full products file on every import. |
| 2 | Inventory restored & matched to products | Data integrity | ✅ Ready | MUST-PASS | SuperCat | Earlier wrong-file import (`1902114`, foreign codes e.g. `1597`) was overwritten. Restored import verified 2026-07-23: **683** inventory rows, **683** match active products, `MGWL-06-6000K` present. All 683 carry `ML_QtyAvailable` / `NSL_QtyAvailable`. **Two 7/23 corrections applied and re-imported (verified 20:45 UTC):** (a) **GA warehouse folded into NSL** — NSL qty = NSL(Tonawanda) + GA(Atlanta) per Jen Z HS #13861 (see row 16); live DB confirms `ES-120V-EC` NSL=52, `SL-ID-30K-LP-20-A8` NSL=405. (b) **Backorder landed** — headers renamed `*_qtybackordered` → `ML_QtyOnBackorder` / `NSL_QtyOnBackorder`; all 683 rows carry the keys, **41 SKUs backorder>0** (e.g. `SL-ID-30K-LP-20-A8` ML=8, `LV-ALP007` NSL=127). 0 negatives / 0 decimals / 0 ghosts. | None — inventory data is complete and warning-free. Sustained refresh depends on Brittni SFTP + GP export (row 23). |
| 3 | Stories present for active SKUs | Data integrity | ✅ Ready | Nice-to-have | SuperCat | **683 / 683** active products have non-empty `story`. Stories import `1902111` clean. | None. |
| 4 | Customers loaded with DefaultPriceCode | Data integrity | ✅ Ready | MUST-PASS | SuperCat | **3,418** customers; `DefaultPriceCode` = `nsldn` ×3,003 / `mldn` ×415 (zero blanks). | None for launch; invite coverage limited by missing emails (row 20). |
| 5 | Zero ghost inventory codes / zero dangling RelatedItems | Data integrity | ✅ Ready | MUST-PASS | SuperCat | `inv_matching_products = 683`; RelatedItems JSON refs: **0** dangling / **2,016** valid. | Keep related-items scrub when dropping SKUs. |
| 6 | ML CAD / NSL USD price levels correct; `net_price` retired | Pricing | ✅ Ready | MUST-PASS | SuperCat | Price levels: `mldn`/`mllist` = **CAD**, `nsldn`/`nsllist` = **USD**; **`net_price` level gone**. No `net_price` key in any active `prices_json`. Groups: ML Reps → mldn,mllist; NSL Reps → nsldn,nsllist; eOL sites match. | None. |
| 7 | Price coverage gaps (intentional vs missing) | Pricing | 🟡 At-risk | Nice-to-have | SuperCat / Client | Active priced: ML **673/683**, NSL **578/683**. Gaps are mostly ML-only / discontinued / TBD web SKUs from the 83 re-add — not a failed NSL list import. HS #14727 (7/21): “Was the NSL price list used?” → yes (AUG2025 NSL + crosswalk). | Publish gap list to Jen; confirm leave-blank is OK for ML-only / clearance. ETA: before next meeting. |
| 8 | eCat Online per-customer pricing workflow | Pricing | 🧑‍⚖️ Decision needed | MUST-PASS *(eOL)* | Dev / SuperCat | HS #14727 item 1 + Jul 22 call: logged-in customer with DN should see **their** DN; list is public default. Code caveat (recovery): eOL can fall to **user-group** default unless an associated customer exists — needs Dev confirmation before promising Jen. | Dev confirms behavior on a test customer login; then update Jen. Blocks eOL public GO, not iPad beta. |
| 9 | Jen's ML + NSL review profiles (not Admin) | Brand separation & rep experience | 🟡 At-risk | MUST-PASS | SuperCat | Live 2026-07-23: `jen@magiclite.com`=Admin; `jen+user@magiclite.com`=**NSL Reps but `is_admin=true`**; **no Jen ML Reps alias**. Same for Jen P (`jen.penton+user` = NSL Reps + `is_admin=true`). Clean NSL-only reviewers exist (`jason@nslusa.com`, `michelle@nslusa.com` with `is_admin=false`). | Create Jen ML Reps alias; prefer review on non-admin NSL user (or clear `is_admin` on +user) so brand field/library checks are valid. |
| 10 | Cut sheets / instructions brand-restricted | Brand separation & rep experience | 👀 Verify-on-rep-profile | MUST-PASS | SuperCat | DB: `CutSheetML`/`InstructionsML` → ML Reps + eOL ML; `CutSheetNSL`/`InstructionsNSL` → NSL Reps + eOL NSL. Admin sees both (HS items 5a / Admin-site confirm). July 22: also rename bad NSL cut-sheet filename (“IP20 + Chinese characters + date”) on first item. | Verify on `jen+user` (NSL) + new ML profile; rename flagged NSL asset. |
| 11 | UPC fields brand-restricted | Brand separation & rep experience | 👀 Verify-on-rep-profile | MUST-PASS | SuperCat | DB: `ML_UPC` → ML groups; `NSL_UPC` → NSL groups. HS item 5c (“both UPCs showing”) is Admin-view. | Confirm only one UPC on each rep profile. |
| 12 | Library ML-under-ML / NSL-under-NSL | Brand separation & rep experience | ✅ Ready *(DB)* / 👀 Verify-on-rep-profile | MUST-PASS | SuperCat | **Postgres 2026-07-23:** ML Reps = **46** library files (all `magiclite.com` URLs); NSL Reps = **131** files (all `nslusa.com` URLs). **0** resources authorized to both ML+NSL Reps. Admin `shared_resources_auth='a'` sees everything — matches HS “library is all ML” when reviewing as Admin. | Verify once on `jen+user` (NSL) after clearing `is_admin` if possible; create ML alias for ML-side check. |
| 13 | Admin-view brand mixing understood / mitigated | Brand separation & rep experience | 🧑‍⚖️ Decision needed | Nice-to-have | Dev / SuperCat | July 22: propose Admin switch/separate views so Admin doesn’t merge brands. Root cause of most “broken” reports. | Document “review as rep, not Admin” as process; optional Dev UX later. Does not block iPad beta if row 9 done. |
| 14 | 130 corrected images uploaded & pointed | Images | ✅ Ready | MUST-PASS | SuperCat | **130** JPGs staged (`~/Downloads/Mali_Mismatched_Images/_FTP_UPLOAD/images/`); Image import events 7/23 (`1902054`–`1902067`); `image_exists=true` on **681/683** active. Spot-check: `DR-96-24-TM-5N1D`, `ACC-DT`, `LEDDR-12-60W` have `image_exists=true`. | Confirm 2 missing `image_exists` SKUs; re-upload if needed. |
| 15 | Residual photography (client) | Images | 🟡 At-risk | Nice-to-have *(iPad beta)* / MUST-PASS *(public polish)* | Client | **Corrected 2026-07-23 (data-grounded):** `NEEDS_PHOTOGRAPHY_RESIDUAL.csv` / “111” was stale/missing. Live evidence from current `products.csv`: **311** active SKUs share a primary image with ≥1 other SKU (`_MALI_FIX_REVIEW/RESIDUAL_SHARED_PRIMARY_IMAGES_2026-07-23.csv`, 43 shared primaries). Separately, **87** active SKUs still point at a primary that is byte-identical to another file in the 130-file FTP upload set (filename unique ≠ photo unique). Client-named still-shared: `LBR-II-KIT`/`SL-CC`→`TLWMV153WMBK.jpg` (17-way); `LST-II-KIT`→`LEDSST-II-WH-P-WH.jpg` (13-way); `SX-TP-*`→`SX-12V-DD-60W.jpg`. Unique-filename but content-unverified without visual QA: `DR-96…`, `YH-SIGNAL-AMP`, `ES-EXT-ENDCAPS`, `ACC-*`, etc. | Send Jen the shared-primary CSV (311) + call out byte-identical FTP groups; do not cite 111. |
| 16 | Inventory per pack/length accurate in data | Inventory accuracy / pack-size | ✅ Ready | MUST-PASS | SuperCat | Per-SKU rows present with GA now folded in, e.g. `SL-ID-30K-LP-20-A8` NSL_QtyAvailable **405** (was 375; +30 GA) / QtyAvailable 405; `SDL-5CCT-4-WH-6P` NSL 651 / ML 474 / std 1125. Pack variants exist as separate SKUs (`SDL-5CCT-*-1P/6P/12P/24P`, `SL-ID-*-LP-20/-LP-100`). **GA fold-in reconciled to source:** ML matched `ML INV LIST.xlsx` exactly on all 580 overlaps; NSL = NSL+GA per **HS #13861** (GA = "NSL warehouse in Atlanta") — **~4,328 NSL available units** were previously hidden. | Send Jen example inventory file clarifying units (feet vs spools). |
| 17 | Units label (feet vs spools / pack) | Inventory accuracy / pack-size | ✅ Ready *(desc)* / 🟡 optional UOM | MUST-PASS *(messaging)* | SuperCat | **Live after 21:22 UTC products import:** 8 Streamline SKUs now have spool length in ShortDesc/LongDesc (e.g. `Low Power Indoor (3000K) — 20 ft`). LP MaxLength=`40Ft (12M)` live. Price list UOM=`Each` (spools). Optional: register Admin `UOM` custom field + import. HP MaxLength still conflicted (ask Jen). | Optional UOM field; ask Jen HP Max Length if it comes up. |
| 18 | eOL inventory render on product detail | Inventory accuracy / pack-size | 🔴 Blocked | MUST-PASS *(eOL)* | Dev | Code-verified (recovery §4): eOL builds inventory only from optioned `qty_available`; mali uses inventory **custom fields** → eOL detail shows no live qty. iPad serializer **does** emit custom fields → iPad OK. `display_quantity_available=true` on both sites does **not** fix product-detail. | Dev: render selected inventory custom fields on eOL **or** set written expectation “live qty = iPad only.” Blocks eOL public. |
| 19 | Hidden pack/finish variants discoverable (no blanket unhide) | Variants / discoverability | 👀 Verify-on-rep-profile | MUST-PASS | SuperCat / Client | **257** active `hideable=true`. Both eOL sites now have `hide_products_marked_hideable=true` (site 12 ML / 13 NSL) — hidden SKUs **do not** appear in eOL grid. Related-products still link families (e.g. LP-20 ↔ LP-100). Example: `SDL-5CCT-4-WH-1P` visible; `-6P/-12P/-24P` hideable; `SL-ID-30K-LP-20` visible, `-LP-100` hideable. | On Jen’s rep profiles: confirm related-products path is acceptable. Only then consider selective unhide of **priced** pack/length variants — never blanket 257. |
| 20 | Rep invitations / BuyerEmail coverage | Client enablement | 🟡 At-risk | Nice-to-have | Client / SuperCat | **1,274** customers missing `BuyerEmail` — limits bulk invite, not catalog import. | Client fills emails for priority reps/buyers before mass invite. |
| 21 | Users / user groups for ML & NSL | Client enablement | ✅ Ready | MUST-PASS | SuperCat | Groups live: ML Reps (5 users), NSL Reps (6), eOL ML/NSL public sites, Admin. Price auth correct (row 6). | Add Jen ML alias (row 9); invite beta reps when ready. |
| 22 | NSL divergent codes (~57) — training / `NSL_Code` field | Client enablement | 🧑‍⚖️ Decision needed | Nice-to-have | SuperCat / Client | Decided path (execution §5.1): Option 1 — shared headline code + optional `NSL_Code` custom field for ~57 divergent SKUs; Option 2 (two orgs) later. Field **not built** yet. Verify confusion on NSL rep profile first. | After row 9 verify: if still confusing, add `NSL_Code` + train on ~57. Not a day-1 iPad block if training accepted. |
| 23 | Brittni SFTP + GP export automation | Integration / automation | 🔴 Blocked | MUST-PASS *(ops)* | Endeavour-IT (Brittni) / SuperCat | HS threads 7/6–7/22: Permission denied / path errors; Brittni missed 7/22 call (“didn’t see response on SFTP denied”). Needs `/data/inventory.csv`, `PortNumber=22`, GP `ROUND()`/int cast + null-filter. Without this, inventory stays manual. | Kyla books Brittni call this week; SuperCat re-sends corrected script + path. |
| 24 | eOL inventory rendering (Dev decision) | Open dev decisions | 🔴 Blocked | MUST-PASS *(eOL)* | Dev | Same evidence as row 18. | Approve small code change **or** iPad-only expectation letter. |
| 25 | eOL pricing model (Dev decision) | Open dev decisions | 🧑‍⚖️ Decision needed | MUST-PASS *(eOL)* | Dev | Same evidence as row 8. | Confirm public list vs logged-in customer DN; document for Jen. |

---

## MUST-PASS gate list (determines GO)

| Gate | Status | Blocks |
|---|---|---|
| G1. Catalog + inventory integrity (matched, no ghosts, RelatedItems clean) | ✅ | — |
| G2. `net_price` retired; ML=CAD / NSL=USD levels authorized correctly | ✅ | — |
| G3. Jen can review as **ML Reps** and **NSL Reps** (not only Admin) | 🟡 NSL exists; **ML missing** | iPad beta sign-off |
| G4. Brand fields + library verified on those rep profiles | 👀 Pending G3 | iPad beta sign-off |
| G5. Pack/length discoverability accepted (related products; no blanket unhide) | 👀 | iPad + eOL |
| G6. Units label (feet/spools/pack) decided with client | ✅ desc live; UOM optional | Messaging polish |
| G7. eOL live inventory path decided (build vs iPad-only expectation) | 🔴 | **eOL public** |
| G8. eOL per-customer DN pricing confirmed with Dev | 🧑‍⚖️ | **eOL public** |
| G9. Brittni SFTP + GP integer export working | 🔴 | Sustained ops / auto inventory |

**Verdict math:** G1–G2 pass → data is launchable on iPad. G3–G6 are the client-facing closeout. G7–G8 keep eOL public at NO-GO. G9 is the ops “big one” from the July 22 call.

---

## HelpScout #14727 → checklist map

| Client item (collapsed) | Checklist row | Session status |
|---|---|---|
| Set customer pricing defaults | #4, #8 | Data ✅; eOL workflow 🧑‍⚖️ |
| Add USD pricing to NSL | #6, #7 | Levels ✅; coverage gaps 🟡 |
| Library ML / NSL separation | #12 | DB split ✅; verify on rep 👀 |
| Quantities & codes per pack size | #16–#19, #24 | Data ✅; eOL render 🔴; units 🧑‍⚖️; hide discoverability 👀 |
| Cut sheets / instructions NSL-only (Admin confirm) | #10 | DB ✅; Admin-artifact → verify 👀 |
| Library NSL-for-NSL (Admin confirm) | #12 | same |
| ML & NSL UPC both showing (Admin confirm) | #11 | DB ✅; Admin-artifact → verify 👀 |
| All product images corrected | #14, #15 | 130 uploaded; **311** shared-primary residual (not 68/111) |
| NSL item codes corrected | #22 | Option 1 deferred; verify on NSL profile first |
| Deep-dive wrong-picture list (DR-96, connectors, drivers, etc.) | #14, #15 | Closed via scrape where possible; remainder in 111 CSV |
| Tape page “374 of what?” | #17, #18 | Spool desc **live**; eOL qty render still 🔴; UOM optional |
| SFTP / Brittni automation | #23 | Still blocked on Endeavour-IT |
| Create Jen eOL profiles per company | #9 | NSL alias ✅; ML alias ❌ |
| Notes / meet Jen P next week | (process) | Schedule after checklist send |

**Image count reconciliation (corrected):** older “68” / “111” lists are stale. Authoritative grounded counts from current catalog: **311** SKUs with shared primary (`RESIDUAL_SHARED_PRIMARY_IMAGES_2026-07-23.csv`); **87** SKUs whose primary is in a byte-identical FTP upload group. Visual content QA still required for unique-filename SKUs.

---

## What changed since last review (2026-07-23)

| Change | Detail |
|---|---|
| Products re-import | **683** active (600 kept + 83 discontinued/web re-adds); RelatedItems dangling scrubbed to **0**. |
| Inventory incident | Wrong org-**273** (`leg`) file briefly wiped mali inventory → **restored** same day with correct 683-row file. |
| `net_price` | Level **removed** from Admin; column absent from products file; no residual keys in `prices_json`. |
| Images | **130** files imported; residual = **311** shared-primary (see row 15). |
| eOL hide flag | Both sites now `hide_products_marked_hideable=true` (was default/false in earlier recovery note) — raises pack-variant discoverability stakes. |
| Jen profiles | NSL Reps alias **created** (`jen+user@magiclite.com`); ML Reps alias still missing. |
| Pricing | CAD/USD levels correct; NSL price blanks remain on non-NSL / clearance SKUs. |
| **GA warehouse (NEW)** | NSL availability now = **Tonawanda (NSL) + Atlanta (GA)** per Jen Z, HS #13861. 64 SKUs affected; **~4,328 NSL units** previously omitted are now counted. ML = Burlington only (unchanged, matched source exactly). |
| **Backorder fields (NEW)** | Inventory headers corrected `*_qtybackordered` → `ML_QtyOnBackorder` / `NSL_QtyOnBackorder` (match registered fields) and **re-imported 20:45 UTC — landed, 41 SKUs backorder>0, zero warnings**. No Admin work needed. |
| **Tape units / MaxLength (NEW)** | Products re-imported **21:22 UTC** — spool ShortDesc/LongDesc + LP MaxLength=40Ft **live** on 8 SKUs. Residual image list = shared-primary CSV (**311**). |

---

## Suggested agenda for next client meeting

1. Walk this checklist top-to-bottom (10 min) — GO conditions for iPad beta.
2. Log Jen into **NSL** alias + new **ML** alias; tick rows 10–12 and 19 live.
3. Agree units label + whether related-products is enough for pack sizes.
4. Confirm eOL expectation: public launch waits on Dev (inventory + pricing).
5. Hand Jen P the 111 photography list + Brittni call status.
