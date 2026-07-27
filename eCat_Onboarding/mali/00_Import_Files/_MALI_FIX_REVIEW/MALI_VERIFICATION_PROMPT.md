# Independent Verification — org `mali` (Magic Lite | NSL) dual-brand catalog

You are a fresh agent with no prior context. **Do not trust the claims below — verify each one independently** against the live database, the price-list files, and the codebase, then return a point-by-point verdict: `VERIFIED`, `INCORRECT` (with evidence), or `UNCERTAIN` (with what you'd need). Be skeptical; the point of this pass is to catch anything wrong before we rebuild the product file.

## Resources available to you
- **Postgres** (read-only MCP, `user-supercat-postgres-vpn`). Org is `mali`, `organizations.id = 285`. Key tables: `organizations`, `distribution_centers`, `price_levels`, `price_levels_user_types`, `distribution_centers_user_types`, `user_types`, `products` (`item_number`, `long_description`, `trade_name_code`, `prices_json`, `images_json`, `deleted`), `product_images` (`product_image_file_name`, `product_image_fingerprint`), `shared_resources` (+`_user_types`), `custom_fields`, `import_events`.
  - Follow the CraftCMS/Postgres rules: never introspect the full schema; query one table/thing at a time.
- **Codebase**: `/Users/kylorjohnson/supercat-code` (importer logic in `supercat_server`).
- **Authoritative AUG2025 price lists** (client-supplied):
  - ML: `/Users/kylorjohnson/Downloads/Attachments (10)/ML PRICE LIST  AUG2025 FLAT WITH DN.xlsx` (CAD; cols: CLASS ID, ITEM NUMBER, ITEM DESCRIPTION, UNIT OF MEASURE, LIST PRICE, DN, UPC)
  - NSL: `/Users/kylorjohnson/Downloads/Attachments (10)/NSL PRICE LIST AUG2025 FLAT WITH DN.xlsx` (USD; same cols)
  - Client gap workbook: `/Users/kylorjohnson/Downloads/Attachments (9)/Copy of Mali_Pricing_Gaps_July15.xlsx` (3 sheets: No Pricing 18, Missing NSL 73, Missing ML 1)
- **Current build catalog**: `…/SuperCat_Simple_Final/02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/products.csv` (694 rows)
- **Prior analysis outputs to check** (in `…/00_Import_Files/_MALI_FIX_REVIEW/`): `pricing_resolution.csv`, `needs_nsl_pairing.csv`, `not_in_pricebook.csv`, `products_IMAGEFIX.csv`, `image_repoints_119.csv`, `images_need_photos.csv`, `recon_*.csv`.
- **KB**: user groups → https://supercatsolutions.com/knowledgebase/user-groups

## Confirmed business decisions (treat as ground truth, but sanity-check feasibility)
1. **NSL vs Magic Lite reps are separated by User Groups (permissions)**, plus Distribution Centers for pricing/inventory. So the catalog keeps **ML BaseItemCodes as the single shared code** — NSL reps do **not** need to see NSL-specific codes on the iPad. Verify the user-group ↔ DC ↔ price-level wiring actually enforces this split.
2. **If a SKU is not in either AUG2025 price list, it should NOT be in the product file** (drop it, don't re-photograph). Verify the "not in price book" list is correct before we delete anything.

## Claims to verify

### A. Architecture
- `mali` (id 285) is one org, two brands "Magic Lite | NSL", separated by `distribution_centers` `ml` and `nsl`.
- Price levels: **Magic Lite = CAD, NSL = USD**. ML reps' user group is authorized to CAD levels + `ml` DC; NSL reps' group to USD levels + `nsl` DC. (Original complaint: "Is the NSL pricing supposed to say CAD?" — NSL should be **USD**; if NSL currently shows CAD that's the bug.)

### B. Code divergence (the "NSL codes are actually ML codes" complaint)
Claim: ~564 item numbers are identical across both price lists; **78 NSL-only, 87 ML-only**. The same physical product often has a different SKU per brand. Verify these specific pairings exist in the price lists (ML list uses the first, NSL list uses the second):
- Brick Star: `LEDBS-II-WH-{L|P|S}-{fin}` (ML) ↔ `LBR-II-{L|P|S}-WH-{fin}` (NSL)
- Step Star: `LEDSST-II-WH-…` ↔ `LST-II-…`
- Mini Disc Scoop: `LEDMD-S-{color}-{fin}` ↔ `LEDMDS-{color}-{fin}` (and ML `…-WH-…` cool white ↔ NSL `LEDMDS-CW-…`)
- Mini Disc Marker: `LEDMD-WH-…` ↔ `LEDMD-CW-…`
- Transformers: ML `DLT-*-347` (347V) ↔ NSL `DLT-277` + `TR-12-*` / `TR-24-*` (277V, US)
Confirm ML price list has **0** `LBR-II`/`LST-II` finish variants and NSL has **0** `LEDBS-II`/`LEDSST-II` (i.e., truly non-overlapping).

### C. Pricing reconciliation (of the 694 catalog rows)
Claim (from `pricing_resolution.csv`): **ML price present = 586, NSL price present = 568**, broken down as:
- 499 NSL exact-code match, 55 NSL via crosswalk, 14 NSL via client gap-sheet fill
- 7 client-flagged discontinue, 7 client-flagged ML-only (blank NSL is correct)
- 15 `NEEDS_NSL_PAIRING` (has ML price, no auto NSL match — mostly drivers `MLDR*`/`MLDRE*`/`LEDDR-12-20W-HW`, work lights `LWL-*`/`SWL-60W-50`, `NN-C10-8`, `LTP-001-OD-6FT`)
- **97 `NOT_IN_PRICEBOOK`** (in neither AUG2025 list → candidates to drop per decision #2)
Verify: recompute independently from the two xlsx + products.csv and confirm the counts. Spot-check 5 crosswalk rows against the NSL xlsx prices. Confirm the 97 not-in-pricebook are genuinely absent from BOTH lists (watch for hyphen/format drift, e.g. `LV-ALP1605` vs `LV-ALP-1605`, `LEDMD-S` vs `LEDMDS`) so we don't wrongly delete a mislabeled-but-real SKU.
- Also verify original complaint "Was the NSL price list used to import?" — check `products.prices_json` / `import_events` for how NSL prices currently look (blank, zero, or copied ML/CAD values).

### D. Attached image (Admin Console product detail — verify against DB)
The screenshot is product **"Low Power Indoor (3000K)"**, item `SL-ID-30K-…`, Trade Name `Magic Lite | NSL (ML)`. Red-boxed fields:
- **Item Dimensions** = `24 X 100 Feet 3000K`
- **Qty Available 374 / Qty On Hand 542 / Qty Reserved 6 / Qty On Backorder 3**
Two separate **Cut Sheet / Instructions** links are shown — one set on `megsofta.com` (ML) and one on `nslusa.com` (NSL).
Verify:
- This is the **units/quantity contradiction** from the complaint (code says `-20` or `-100` feet, qty shows 374). Determine from the DB whether qty is spools or feet, and whether `Item Dimensions` / `Units per Carton` actually disambiguate it. Is this a data-quality issue (not a system bug)?
- Confirm the product genuinely carries **brand-specific Cut Sheet/Instructions** (ML→megsofta, NSL→nslusa), which supports the "library is now split by brand" claim.

### E. Library / shared_resources (complaint: "library is there for NSL but it's all ML info")
Claim: `shared_resources` now has NSL-specific folders (e.g., "NSL — Catalogues", "NSL — Installation Instructions", "NSL — Product Cut Sheets") restricted to NSL user types via `shared_resources_user_types`, separate from ML folders. Verify the folders exist AND the access restrictions are actually applied (not visible to ML, and vice-versa).

### F. Image complaints — verify each against `product_images` (filename + fingerprint) and `images_json`
The client listed wrong/missing photos. For each, determine: (i) does the item exist & is it in the AUG2025 price list (else it's dropped anyway), (ii) does its `images_json` point to a file whose `product_image_fingerprint` is shared with an unrelated product (= placeholder/wrong photo), (iii) is a correct dedicated photo available. Cross-check against `products_IMAGEFIX.csv` (119 repoints) and `images_need_photos.csv` (392 needing new photography).
Complaint list to check item-by-item:
1. `DR-96-24-TM-5N1D` picture wrong
2. Outdoor Streamline connectors — no picture
3. `YH-SIGNAL-AMP` shows the 120V eStrip, not the amplifier
4. eStrip connector pics are just the eStrip
5. Neon Flex accessory pics are just the Neon Flex
6. Wedge light lamp pics are Wall Washer
7. `ES-EXT-ENDCAPS` pic is the extrusion, not end caps
8. Non-dimmable driver pics are dimmable drivers
9. Hard Strip power feed pics are the Hard Strip fixture
10. `LV-HS-MC30` wrong pic
11. `ACC-12G-2C-BUR` wrong pic
12. All flood light accessory pics wrong
13. `ACC-DT`, `ACC-PC`, `ACC-WIFI` pics wrong
14. RGB controllers/amplifiers are old codes + pics
15. All outdoor sconce pics (incl. application photos) are `SL-CC` (wrong)
16. `LBR-II-KIT` pic wrong
17. `BL-CC` all pics wrong
18. `LST-II-KIT` pic wrong
19. `SL-CC` all pics wrong
20. Both wire types (minidisc & disc section) pics wrong
21. All construction plates in downlight section — pics wrong
22. Square trims in downlights — pics wrong
23. `LV-DL-EX-10-L`, `LV-DL-EX-30-L` pics wrong
24. Surface-mount downlight trims (circle & square) pics wrong
25. `WSL-15-30K-BN` all pics wrong (shows wall washer)
26. Fire-rated downlight trims & beauty rings pics wrong
27. `SL66-4FT-40W-40` all pics wrong
28. Work Light & Tri-proof accessory pics wrong
29. "Why do we have Switchex (`SX-*`) on there?" — should these be removed?
30. All aluminum extrusion accessory pics wrong
Note which of these items fall in the **97 not-in-pricebook** set (e.g., `WSL-15-30K-BN`, `SL66-4FT-40W-40`, outdoor sconces `LED-SW-*`, flood `FL-*`, `RGL-*`, `SX-*`) — those get dropped, so their photos are moot. Flag any complaint item that is still a live/priced product and genuinely needs a corrected photo.

## Output format
Return a table: `Claim | Verdict (VERIFIED/INCORRECT/UNCERTAIN) | Evidence`. Group by section A–F. End with:
- A list of anything you found **INCORRECT** in the prior analysis.
- The corrected counts if any differ.
- Any item wrongly slated for deletion (real product that just has a code/format mismatch).
- Remaining open questions for Kylor.
