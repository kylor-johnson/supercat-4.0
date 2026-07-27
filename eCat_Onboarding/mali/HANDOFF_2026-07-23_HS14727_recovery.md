# Magic Lite / NSL (`mali`, org 285) — Recovery Handoff · HS #14727

**Created:** 2026-07-23 · **For:** a fresh agent to review and execute where directed.
**Read first:** `CLIENT_PROFILE.md`, `HANDOFF.md` (Library-specific). This doc supersedes the Library handoff for scope beyond the Library.

> ⚠️ **Do not run off and "unhide 224 products" or "re-import to fix pricing" without reading the "Hidden products — corrected" and "Importer guardrails" sections. Several earlier assumptions were wrong; this doc records what was actually verified in code + Postgres on 2026-07-23.**

---

## 1. Situation

- One eCat org `mali` (id **285**) serves **two brands**: Magic Lite (ML, Canada, CAD) and National Specialty Lighting (NSL, US, USD).
- **Escalated relationship.** Original launch was March; still not in beta reps' hands late July. Client (CFO Jen Zorony; COO Jen Penton, back next week; Brittni Pryputniski = Endeavour/GP IT) is at "if and how we conclude this project." Internal directive: *"we cannot keep missing."*
- **The recurring own-goal:** the client reviews everything logged in as **Admin**, which merges both brands (all price levels, all custom fields, both UPCs, both libraries). Most "it's broken" reports are Admin-view artifacts, but we keep failing to prove that because Jen has **no rep/customer profile**.

### Source of truth (files)
| What | Path |
|---|---|
| Working import files | `02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/` |
| products.csv (600 rows, 55 cols) | `…/Ready_For_Import/products.csv` |
| inventory.csv (694 rows) | `…/Ready_For_Import/inventory.csv` |
| customers.csv (3,418 rows) | `…/Ready_For_Import/customers.csv` |
| stories.csv (694 rows) | `…/Ready_For_Import/stories.csv` |
| ML / NSL price lists | `…/Magic Lite/ML PRICE LIST AUG2025 FLAT WITH DN.xlsx`, `NSL PRICE LIST AUG2025 FLAT WITH DN.xlsx` |
| Backend codebase | `/Users/kylorjohnson/supercat-code/supercat_server` |

### Data access
- Postgres MCP: `user-supercat-postgres-vpn` → `execute_sql` (read-only). Org id = **285**.
- HelpScout ticket via BigQuery MCP `user-bigquery-admin`: `helpscout.conversations` / thread data in `_embedded.threads`, conversation `number = 14727`.
- **Jira is READ-ONLY** (workspace rule). Do not write to any ticket.

---

## 2. THE architectural truth (root of almost everything)

Two brands + hundreds of **priced/stocked variants** run through a **single flat catalog with NO option/variant mechanism** (only **2 option records org-wide**). Brand separation works via user-group authorization. Variant handling does **not** exist — each color/finish/pack/length is a separate flat SKU. "Dedup" was done by setting `hideable=true`, not by collapsing variants into a selector. Every open item traces back to this.

---

## 3. Verified live state (Postgres, 2026-07-23)

- Products: **600 active**, 357 soft-deleted. All 600 are `trade_name_code = ML` (no product tagged NSL; brand split is by group auth + custom fields, not trade name).
- Prices: all 600 have all levels populated in `products.prices_json`. Levels: `mldn`/`mllist` = **CAD**, `nsldn`/`nsllist` = **USD**, `net_price` = USD (stopgap, holds ML list/CAD values → `net_price == mllist` on 597/597 — retire it).
- ML DN ≠ NSL DN on **575/575** items with both present (pricing genuinely differs; only 13 intentionally equal).
- Custom fields correctly group-restricted: `CutSheetML`/`InstructionsML`/`ML_UPC` → ML groups; `CutSheetNSL`/`InstructionsNSL`/`NSL_UPC` → NSL groups. **There is NO NSL item-code custom field** (only cutsheets/instructions/UPCs).
- User groups + authorized price levels: `ML Reps` → mldn,mllist · `NSL Reps` → nsldn,nsllist · `eOL ML Public Site` → mldn,mllist · `eOL NSL Public Site` → nsldn,nsllist · `Admin` → (none/all).
- Mobile sites: `12` = ML, `13` = NSL. Org `collection_related_items = true` (related products DO render on eOL detail).
- **Mobile-site flags for both sites are unset → defaults apply:** `hide_products_marked_hideable` = **false**, `display_quantity_available` = **true**, `display_quantity_backordered` = **true**. (Stored in `mobile_sites.properties` jsonb; both null for mali.)
- Inventory: 694 rows, all have ML/NSL quantities in `inventories.custom_fields`. Standard `qty_available` populated on **0/694**; rows with options **0/694**. Inventory custom fields created 2026-07-22 as `ML_QtyAvailable`, `NSL_QtyAvailable`, etc. (case-insensitive match to CSV `ML_qtyavailable` headers — data landed fine, incl. the `258.5` decimal, stored as float).
- Customers: `DefaultPriceCode` set on all 3,418 (nsldn ×3,003 / mldn ×415). ~1,274 missing BuyerEmail (limits invites, not fatal).

---

## 4. eOL inventory NOT showing — ROOT CAUSE (code-verified)

**The data is present.** The problem is eOL has **no code path that renders inventory custom fields.**

- `ecat_products_controller#show` (line ~69) builds inventory only from `Inventory.option_inventory(org, item_number)`.
- `Inventory.option_inventory` (`app/models/inventory.rb:180-190`) returns a qty **only if `qty_available` is present AND the row has options.** Mali has neither → returns empty for every product.
- The detail template (`_product_option_inventory.html.erb`) renders only that.
- The **iPad API serializer** (`inventory.rb:236-242`) **does** emit inventory custom fields → **inventory WILL show on the iPad, not on eOL.**
- `display_quantity_available` (default true) only affects the **order-history** view (`ecat_orders/_order.html.erb`), which reads `order_item.quantity_available` from imported order data — **not** product-detail live inventory.

**Fix options (needs a dev decision — NOT a config toggle):**
- (a) small code change to render selected inventory custom fields on eOL detail (right long-term fix); or
- (b) surface qty as a product-level custom field (eOL renders `@product_custom_fields`) — but it goes stale vs the live inventory feed.

➡️ **Escalate to dev. Do not promise Jen an eOL live-inventory date until decided.** This — not the hide flag — is what makes her "374 of what? / I don't see a quantity" complaint real, and it affects **visible** products too.

---

## 5. Hidden products — CORRECTED (previous "unhide 224" advice was wrong)

Verified in code + DB:
- 224 of 600 products have `hideable = true`.
- `hide_products_marked_hideable` is **false** on both eOL sites (default) → on eOL, hidden products **still appear** in grid, related products, and detail. (`query_for_catalog.rb:57` only filters when the flag is on.)
- `get_related_products.rb` does **NOT** filter on `hideable`, and the show page has no hideable filter → **hidden products are reachable and orderable via related products** (org `collection_related_items = true`).
- The iPad app has its own built-in behavior for `hideable` (typically hides from browse, shows as related), which can differ from eOL — **verify per surface.**

**What the hidden set actually is** (a mix, NOT just "HP vs LP"):
- Same-price **color/CCT** variants: `MGWL-06-*`, `MGST-12-*`, `NFLX-40-*` (all identical price — pure "pick a color").
- **Finish** variants: `LEDMD-*`, `LTSPRO-*` (BK/BZ/SN), `LTS-II-*` (/AL/BK/BZ), `LEDBS-II-*` (must be individually orderable).
- **Pack/length** variants: `SDL-5CCT-*` (6P/12P/24P), `SL-ID/ST-ID -100` tape, `LEDLB-5CCT` sizes, `LV-HS-PD20-24V` lengths, `ES-120V` temps — **different prices, different stock.**
- Note: `SL-ID-30K-HP-20` and `-LP-20` are **both visible** — the dedup ran on **length/pack**, not HP/LP.
- Variants share **one web page / one cut-sheet PDF** per family (e.g. all `MGWL-06` colors → one PDF; all `LV-HS-PD20` lengths → one PDF). So the public websites have **no per-variant image/page** — the 68 missing/mismatched images and any per-variant differentiation must come from **client internal assets**, not scraping.

**What Jen actually asked** (email item 6 + transcript): *"Ensure all item codes are displayed and inventory levels are accurate for each pack size … quantities listed individually."* That is **two things, neither of which is "unhide everything":**
1. **Quantity per SKU** → the **eOL inventory-rendering gap** (§4). Un-hiding will NOT make quantities show. This is the real fix.
2. **Discoverability** → whether each pack size is findable. Since (a) hidden SKUs already show via related products and (b) the eOL hide flag is off anyway, "only seeing one" is most likely **admin-view confusion or an iPad-vs-eOL difference**, not the hide flag.

➡️ **DO NOT blanket-unhide.** Correct sequence: fix §4, then **verify on Jen's rep profile** whether related-products discoverability is acceptable, then — only if needed — decide between un-hiding the priced variants or building a real options/variant structure. Confirm the UX preference with the client; do not assume.

---

## 6. Work buckets

### Bucket A — Fix now (we control; low risk)
- **Trim 94 ghost SKUs:** `inventory.csv`/`stories.csv` (694) carry 94 codes not in `products.csv` (600) → import warnings "Product not found, record ignored." Reduce to the 600 live SKUs (or add the products if they should exist).
- **Fix inventory numerics:** `MGWL-06-6000K = 258.5` (decimal) + 13 negatives. Round/clamp at source (also part of Brittni's export fix).
- **Fill price gaps:** 22 products missing NSL price, 3 missing ML (pre-gap-sheet). Jen returned the completed gap sheet 2026-07-20 — merge & re-import; confirm it covers all 25.
- **Retire `net_price` level** (USD currency holding ML/CAD values — landmine).
- **Rename the bad NSL cut-sheet asset** Jen flagged ("IP20 + Chinese chars + date").
- **Continue image QA** only where we have a correct source image.

### Bucket B — Need from client (blockers)
- **68 replacement product images** (Kyla to email the list). Website has one image per family → cannot scrape per-variant. **Blocked until client supplies.**
- **NSL item codes** for SKUs where NSL ≠ ML. No NSL item-code field exists today. Get ML→NSL mapping (likely extractable from the NSL price list) → add `NSL_Code` custom field restricted to NSL groups. ⚠️ Kyla told Jen this was "fixed" — it was NOT (she fixed NSL *prices* + *cut-sheet URLs*, not the displayed code).
- **Brittni SFTP + export fix:** still "Permission denied." Needs remote path `/data/inventory.csv` + `PortNumber=22`, and `ROUND()`/integer cast + null-filter in the GP SQL export. Kyla to get her on a call this week ("the big one").
- **Pack-size inventory mapping sign-off** (Kyla to send an example inventory file).

### Bucket C — Verify (perception / behavior)
- **Create Jen's ML + NSL eOL profiles** ⭐highest leverage — retires most of email items 5, 7, and part of 4. She currently grades as Admin.
- **Confirm eOL customer default pricing** (email item 3): `renders_product_details.price_level_for_rendering` → falls to `org_user.default_price_level` = the **user group's** default level (not automatically the customer's `DefaultPriceCode`). Validate with a real customer login. If eOL uses the group default for public browse, set each site's group default to the DN level; true per-customer pricing needs customer accounts. **Confirm workflow with dev before promising.**
- **Confirm hidden/related behavior on rep profiles** (§5) before any hide changes.

### Bucket D — Dev decision
- **eOL inventory rendering** (§4a) — approve code change or set expectation that live qty is iPad-only.

---

## 7. Open decisions for a human (get Kylor's call before executing)
1. **Variant strategy** — Option A: un-hide priced pack/length/finish variants (more tiles, all orderable) · Option B: build options/matrix so one tile per family exposes selectable variants each with own price + qty (proper, bigger rebuild; also solves eOL inventory-per-variant) · Option C: leave hidden and rely on related-products discovery. **Confirm the UX preference with Jen first (§5).**
2. **eOL live inventory** — dev change vs iPad-only expectation.
3. **eOL pricing model** — public group-default vs per-customer accounts.

## 8. Suggested execution order
1. Today (client-facing): create Jen's 2 eOL profiles; email 68-image list + NSL-code request; book Brittni call.
2. Get Kylor's decisions (§7).
3. Build pass (Bucket A): trim ghosts, fix numerics, merge price gaps, retire net_price, rename asset → re-import **full** products.csv + inventory.csv → **verify File Import Status**.
4. Dev decisions (Bucket D + eOL pricing).
5. On client delivery: import NSL codes + add `NSL_Code` field; drop in replacement images; finalize pack-size inventory mapping.

---

## 9. Importer guardrails (workspace rules — do not violate)
- `products.csv`: omitted rows are **soft-deleted on a clean import**; deletes are **skipped if ANY error row** exists. Always send the **full** product file.
- `inventory.csv`: **hard-deletes all inventory and reloads.** Must be clean.
- Custom fields must be pre-registered in Admin ("Send to iPad") before import; matched case-insensitively.
- **Verify every import:** Tools → Admin Reports → File Import Status (blue-link timestamp = problems).
- Import order: options → option_groups → products → stories → inventory → customers. Re-send option_groups after options.

## 10. Handy read-only SQL
```sql
-- org + settings
select id, shortname, collection_related_items from organizations where id = 285;
select id, url_key,
       properties->>'hide_products_marked_hideable' as hide_hideable,
       properties->>'display_quantity_available'    as disp_qty
from mobile_sites where organization_id = 285 order by id;

-- hidden products
select item_number, hideable, trade_name_code
from products where organization_id = 285 and not deleted and hideable
order by item_number;

-- inventory custom-field data present but not shown on eOL
select base_item_code, custom_fields
from inventories where organization_id = 285
and base_item_code = 'SDL-5CCT-4-WH-1P';

-- price levels + group auth
select id, code, name, currency_code, pl_type from price_levels where organization_id = 285 order by position;
```

## 11. Key code references (supercat_server)
- eOL product detail: `app/controllers/ecat_products_controller.rb` (`show`, `current_price_level`).
- Inventory on eOL: `app/models/inventory.rb:180-190` (`option_inventory`) and `:234-242` (API to_hash — iPad path).
- Hidden filter: `app/services/products/query_for_catalog.rb:57`; related: `app/services/products/get_related_products.rb`.
- Price resolution: `app/models/renders_product_details.rb:262-300`; `app/models/org_user.rb:413-449`.
- Mobile-site flags: `app/models/mobile_site.rb:214-242`.
