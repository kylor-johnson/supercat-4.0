# Magic Lite Import Process — Start to Finish

Battle-tested. Every error in this doc is one we actually hit.

---

## Before You Touch the Admin Console

### Gather These Files

| File | Location | Purpose |
|------|----------|---------|
| Product images (JPG) | `~/Downloads/magic_lite_images/` | 370 unique files |
| `products.csv` | `Ready_For_Import/` | 694 products, 51 columns |
| `stories.csv` | `Ready_For_Import/` | 694 product stories |
| `customers.csv` | `Ready_For_Import/` | Customer accounts |
| `inventory.csv` | `Ready_For_Import/` | Inventory levels |
| `ML_NSL_Combined_Price_List.csv` | `../03_Data/` | Reference only (already merged into products.csv) |
| `ML_products_3.0 (2).csv` | `../03_Data/` | Reference only (already merged into products.csv) |

### Verify products.csv is Clean

```python
import csv
with open('products.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
print(f"Total rows: {len(rows)}")
print(f"Columns: {len(rows[0])}")
print(f"Visible: {sum(1 for r in rows if r['Hideable'] == 'N')}")
print(f"With images: {sum(1 for r in rows if r['ImageFileName'].strip())}")
print(f"With price: {sum(1 for r in rows if r.get('price_net_price','').strip())}")
```

Expected: 694 rows, 51 columns, 61 visible, 694 with images, 652+ with price.

---

## Step 1: Configure Admin Console

**DO THIS FIRST. Import will fail if codes don't exist.**

### 1a. Trade Names & Collections

**Admin > Trade Names & Collections**

Create tradename `ML` (Magic Lite) with collections:

| Code | Name |
|------|------|
| `LL` | Linear Lighting |
| `UCL` | Under Cabinet Lighting |
| `DL` | Down Lighting |
| `LAND` | Landscape Lighting |
| `IL` | Industrial Lighting |

### 1b. Groups & Categories

**Admin > Groups & Categories**

Create each Group, then add all Category codes under it. See `README.md` in this folder for the complete list. Key requirement: **every code used in the `CategoryCodes` column of products.csv must exist here.**

### 1c. Custom Price Levels (if applicable)

Create `ml_list`, `ml_dn`, `nsl_list`, `nsl_dn` as custom price level codes.

---

## Step 2: Upload Images

**Admin > Products > Images** (or bulk image upload)

1. Upload ALL JPG files from `~/Downloads/magic_lite_images/` (370 files)
2. Wait for upload to complete fully
3. Spot-check: search for `LTSPRO-9-WH.jpg`, `ST-ID-30K-HP-20-B0.jpg`, `TLE-2X2-K40-3065.jpg`
4. Verify they appear in the image library

**Why first:** products.csv references image filenames. If images don't exist when products import, the product will have no images and you'll need to re-import after uploading.

---

## Step 3: Import Products

**Admin > Tools > Import Data > Products**

1. Select `products.csv`
2. Map all columns (BaseItemCode, ShortDesc, LongDesc, etc.)
3. Run import
4. Review import log carefully

### What You'll See

**Warnings (safe to ignore):**
```
Warning: Custom field 'MountingType' not configured — skipped
Warning: Custom field 'Wattage_W' not configured — skipped
```
These mean the CSV has columns the admin console doesn't have custom fields for. Products still import fine — the data is just skipped for those columns.

**Errors (MUST FIX before re-importing):**

| Error | What Happened | Fix |
|-------|--------------|-----|
| `Invalid CategoryCodes code: 'UCL'` | Category code not defined in admin | Add it in Groups & Categories |
| `Invalid CollectionCodes code: 'IND'` | Collection not defined | Add it in Trade Names & Collections |
| `Invalid value: field=price_net_price` | Non-numeric value in price column | Check for data shifted into wrong column |
| `Invalid TradeNameCode: 'ML'` | Tradename not configured | Add in Trade Names & Collections |
| `BaseItemCode exceeds 20 characters` | Code too long | Shorten the BaseItemCode |

### Real Errors We Hit (Magic Lite)

1. **`UCL` as a CategoryCode AND CollectionCode** — we originally used `UCL` as both. The system treats them differently. CollectionCodes = top-level browsing. CategoryCodes = filtering within collections. Make sure codes are defined in the RIGHT place.

2. **`IND` not defined as a CollectionCode** — Industrial Lighting was `IL` as a collection but some products had `IND` as a CollectionCode. Fix: either add `IND` as a collection or change products to use `IL`.

3. **`TLE` undefined as a CategoryCode** — T-Edge Lights category wasn't created before import. Fix: add it in Groups & Categories before re-importing.

---

## Step 4: Import Stories

**Admin > Tools > Import Data > Stories**

1. Select `stories.csv`
2. Map `BaseItemCode` and `ProductStory` columns
3. Run import

Products must already exist (Step 3). Stories match on BaseItemCode.

---

## Step 5: Import Customers

**Admin > Tools > Import Data > Customers**

1. Select `customers.csv`
2. Map all columns (BillToCode, BillToName, DefaultPriceCode, TerritoryCodes, etc.)
3. Run import

Required fields: `BillToCode`, `BillToName`, `DefaultPriceCode`, `TerritoryCodes`, `ShipToAddress1`, `ShipToCity`, `ShipToState`, `ShipToPostCode`

---

## Step 6: Import Inventory

**Admin > Tools > Import Data > Inventory**

1. Select `inventory.csv`
2. Map `BaseItemCode` and quantity fields
3. Run import

Products must already exist (Step 3).

---

## Step 7: Post-Import Verification (iPad)

**THIS IS CRITICAL.** Every time we imported, the iPad review found issues. Budget time for 2-3 review cycles.

### Check 1: Image Order

Open the catalog on iPad. For every visible product, verify:
- [ ] Hero image is a **product photo** (product on white/transparent background)
- [ ] Hero image is NOT a kitchen scene, room application, installation photo, color chart, or certification logo
- [ ] If wrong: the image files need to be re-ordered on disk and re-uploaded

**Products that had image order issues (Magic Lite):**
- `LTSPRO` — kitchen photo was hero (LTSPro-kitchen.jpg)
- `TLE` — office application photo was hero
- `ST-ID` — room/application photo was hero
- `DL-FR` — color temperature chart was hero
- `MGST` — outdoor patio application photo was hero (206KB landscape image)
- `WF-CB` — bollard application photo in the set

### Check 2: Hideable

- [ ] Only 61 products visible in browse
- [ ] No accessories, drivers, or controllers showing in main browse
- [ ] Only one representative per product family visible (e.g., one LTSPRO size, not all 24)
- [ ] Hidden products accessible via RelatedItems on the visible product

### Check 3: Pricing

- [ ] Visible products show prices (not $0.00 or blank)
- [ ] Products with custom levels show correct prices for the logged-in customer's price code
- [ ] Products without pricing show appropriately (blank or contact for pricing)

### Check 4: General

- [ ] Categories and collections filter correctly
- [ ] Product stories display on detail pages
- [ ] Search returns relevant products
- [ ] RelatedItems links navigate correctly

---

## Re-Import Process

When you need to fix data and re-import:

1. Fix the CSV locally
2. Re-upload any changed images (if image files changed)
3. Re-import products.csv — it will **update** existing products (matched on BaseItemCode)
4. Re-import stories.csv if stories changed
5. Re-verify on iPad

Products matched by BaseItemCode are updated in-place. You don't need to delete and re-create.

---

## Pricing Data Flow

```
ML_NSL_Combined_Price_List.csv    ML_products_3.0 (2).csv
         │                                  │
         ▼                                  ▼
    ┌─────────┐                      ┌─────────────┐
    │ Pass 1  │                      │   Pass 2    │
    │ Custom  │                      │  NetPrice   │
    │ Levels  │                      │  Fallback   │
    └────┬────┘                      └──────┬──────┘
         │                                  │
         ▼                                  ▼
    ┌──────────────────────────────────────────┐
    │            products.csv                   │
    │  Price_ml_list, Price_ml_dn,              │
    │  Price_nsl_list, Price_nsl_dn,            │
    │  ML_UPC, NSL_UPC, price_net_price         │
    └──────────────────────────────────────────┘
```

Pass 1 matches on BaseItemCode → Combined Price List (87 products matched)  
Pass 2 matches remaining on BaseItemCode → ML 3.0 NetPrice (565 products matched)  
Pass 3 backfills price_net_price for Pass 1 products that also exist in ML 3.0  
42 products have no price data (leave blank)

---

## Resources

- **SuperCat Import Guide:** https://supercatsolutions.com/knowledgebase/import-product-file
- **SuperCat Pricing Guide:** https://supercatsolutions.com/knowledgebase/catalog-pricing
- **Tradenames & Collections:** https://supercatsolutions.com/knowledgebase/tradenames-collections
- **Groups & Categories:** https://supercatsolutions.com/knowledgebase/groups-categories
