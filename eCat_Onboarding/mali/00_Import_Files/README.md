# Import Files — Magic Lite

All CSV files ready for SuperCat eCat import live in `Ready_For_Import/`.

---

## Files Overview

| File | Records | Description |
|------|---------|-------------|
| `products.csv` | 694 rows | 51-column product file — all collections, pricing, images |
| `stories.csv` | 694 rows | Product stories (max 500 chars, from website or LongDesc) |
| `customers.csv` | — | Customer accounts (BillTo/ShipTo) |
| `inventory.csv` | — | Inventory levels by BaseItemCode |
| `pricing.csv` | — | Additional pricing data |

---

## Import Order

Import in this exact order. Violating this causes dependency failures.

```
1. Images         Upload JPGs to Admin Console FIRST (products reference them)
2. products.csv   Requires images to already exist
3. stories.csv    Requires products to exist (matches on BaseItemCode)
4. customers.csv  Independent — can import anytime
5. inventory.csv  Requires products to exist
6. pricing.csv    Requires products to exist
```

---

## Admin Console Setup (MUST DO BEFORE IMPORT)

Every CollectionCode and CategoryCode in `products.csv` must already exist in the admin console. **Undefined codes cause fatal import errors — not warnings, ERRORS.** The import will reject the entire file.

### Step 1: Trade Names & Collections

Navigate to **Admin > Trade Names & Collections**

| TradeNameCode | Name | CollectionCodes |
|---------------|------|-----------------|
| `ML` | Magic Lite | `LL`, `UCL`, `DL`, `LAND`, `IL` |

Create each collection:

| Code | Name |
|------|------|
| `LL` | Linear Lighting |
| `UCL` | Under Cabinet Lighting |
| `DL` | Down Lighting |
| `LAND` | Landscape Lighting |
| `IL` | Industrial Lighting |

### Step 2: Groups & Categories

Navigate to **Admin > Groups & Categories**

Create these Groups, then add Categories under each:

**Group: MAIN**

| Category Code | Name |
|---------------|------|
| `LIGHT` | Lighting Products |
| `ACCESSORIES` | Accessories |
| `DRVRS` | Drivers |
| `CNTRL` | Controllers |

**Group: LL (Linear Lighting sub-categories)**

| Category Code | Name |
|---------------|------|
| `SL` | Streamline Tape |
| `ST` | Standard Tape |
| `ES` | Rope Light |
| `NF` | Neon Flex |
| `STRING` | String Lights |
| `WW` | Wall Washer |
| `EXT` | Extrusions |

**Group: UCL (Under Cabinet sub-categories)**

| Category Code | Name |
|---------------|------|
| `TLS` | LED Task Star |
| `RGSD` | Regressed/Slim Down |
| `GIM` | Gimbal |
| `SMD` | Surface Mount |
| `FR` | Fire Rated |
| `UCL` | Under Cabinet (general) |

**Group: DL (Down Lighting sub-categories)**

| Category Code | Name |
|---------------|------|
| `TL` | Thin Lines |
| `RGL` | Regressed Gimbal |
| `GDL` | Gimbal Downlight |
| `SM` | Surface Mount |
| `TLE` | T-Edge Lights |

**Group: LAND (Landscape sub-categories)**

| Category Code | Name |
|---------------|------|
| `FSL` | Flood & Spot Lights |
| `PL` | Pathway Lights |
| `WDL` | Wall & Deck Lights |
| `IGL` | In-Ground Lights |
| `TA` | Transformers & Accessories |

**Group: IL (Industrial sub-categories)**

| Category Code | Name |
|---------------|------|
| `IND` | Industrial |

### Step 3: Custom Price Levels

Navigate to **Admin > Pricing** (or equivalent)

Create these custom price levels if using multi-tier pricing:

| Price Level Code | Name |
|-----------------|------|
| `ml_list` | Magic Lite List Price |
| `ml_dn` | Magic Lite Dealer Net |
| `nsl_list` | NSL List Price |
| `nsl_dn` | NSL Dealer Net |

---

## CategoryCodes Reference

### Pattern

```
Core products:     LIGHT,{subcategory}
Accessories:       {subcategory},ACCESSORIES  (or ACCESSORIES,{subcategory})
Drivers:           MAIN,DRVRS  (or {sub1},{sub2},DRVRS for shared)
Controllers:       MAIN,CNTRL  (or {sub1},{sub2},CNTRL for shared)
Extrusions:        ACCESSORIES,EXT
```

### Actual Codes in products.csv (694 products)

| CategoryCodes | Count | Description |
|--------------|-------|-------------|
| `LIGHT,SL` | — | Streamline Tape core products |
| `LIGHT,ST` | — | Standard Tape core products |
| `LIGHT,TLS` | — | LED Task Star core products |
| `LIGHT,UCL` | — | Under Cabinet general core |
| `LIGHT,IND` | — | Industrial core products |
| `LIGHT,TLE` | — | T-Edge Lights core |
| `LIGHT,FR` | — | Fire Rated core |
| `MAIN,DRVRS` | — | Drivers (shared across collections) |
| `MAIN,CNTRL` | — | Controllers (shared across collections) |
| `ACCESSORIES,EXT` | — | Extrusion products |
| `{sub},ACCESSORIES` | — | Collection-specific accessories |

### Shared Drivers/Controllers

Drivers and controllers that serve multiple subcategories list all subcategories before the type:

```
SL,DRVRS           → serves only Streamline Tape
SL,ST,DRVRS        → serves Streamline + Standard Tape
MAIN,DRVRS         → serves all collections
MAIN,CNTRL         → serves all collections
```

Only ONE row per product. When a driver appears in a new brochure, update its CategoryCodes — never duplicate the row.

---

## Pricing Columns in products.csv

The products.csv includes pricing directly in the file (no separate pricing.csv needed for these):

| Column | Source File | Lookup Key | Notes |
|--------|-----------|------------|-------|
| `price_net_price` | `ML_products_3.0 (2).csv` | `Item Number` → `NetPrice` | Required for Net Price display mode |
| `Price_ml_list` | `ML_NSL_Combined_Price_List.csv` | `Item Number` → `ML List` | Custom level |
| `Price_ml_dn` | `ML_NSL_Combined_Price_List.csv` | `Item Number` → `ML D/N` | Custom level |
| `Price_nsl_list` | `ML_NSL_Combined_Price_List.csv` | `Item Number` → `NSL List` | Custom level |
| `Price_nsl_dn` | `ML_NSL_Combined_Price_List.csv` | `Item Number` → `NSL D/N` | Custom level |
| `ML_UPC` | `ML_NSL_Combined_Price_List.csv` | `Item Number` → `ML UPC` | UPC code |
| `NSL_UPC` | `ML_NSL_Combined_Price_List.csv` | `Item Number` → `NSL UPC` | UPC code |

### Pricing Merge Logic

```
Pass 1: Match BaseItemCode against ML_NSL_Combined_Price_List.csv
        → Populate Price_ml_list, Price_ml_dn, Price_nsl_list, Price_nsl_dn, ML_UPC, NSL_UPC

Pass 2: For products NOT matched in Pass 1, match against ML_products_3.0.csv
        → Populate price_net_price only

Pass 3: For products matched in Pass 1 but MISSING price_net_price,
        also look up NetPrice from ML_products_3.0.csv
        → Ensures ALL priced products display in Net Price mode

Result: 87 products with custom levels, 565 with NetPrice only, 42 with no price data
```

---

## RelatedItems Rules

- **Only core products** (`LIGHT,{sub}`) get RelatedItems
- Accessories, drivers, controllers → empty RelatedItems
- Cross-link paired core products FIRST (e.g., 2700K lists 3000K variant first)
- Then: accessories, drivers, controllers — all from Product Brochure PDF
- Format: comma-separated BaseItemCodes, no spaces

---

## Hideable Strategy

| Rule | Hideable | Example |
|------|----------|---------|
| ONE representative per product family | `N` | `LTSPRO-9-WH` (visible) |
| All other sizes/finishes of that family | `Y` | `LTSPRO-12-WH`, `LTSPRO-9-BK` (hidden) |
| ALL accessories | `Y` | `ST-10MM-BWBC-6` |
| ALL drivers | `Y` | `DR-96-24-TM-5N1D` |
| ALL controllers | `Y` | `CNTRL-0-10V-DIM` |
| ALL extrusions | `N` | `LV-ALP1605` (browsable) |

---

## Post-Import Verification Checklist

- [ ] Products visible in catalog (iPad + web)
- [ ] Hero images are product photos (NOT application/kitchen/room shots)
- [ ] Image order correct (product cutout first, application photos secondary)
- [ ] RelatedItems links work on core products
- [ ] Hideable products hidden from browse, visible via RelatedItems
- [ ] Category and collection filters work
- [ ] Pricing displays correctly (Net Price mode + custom levels)
- [ ] Product stories display on detail pages
- [ ] Search returns correct products
- [ ] No accessories/drivers/controllers showing in main browse

---

## Resources

- **SuperCat Import Guide:** https://supercatsolutions.com/knowledgebase/import-product-file
- **SuperCat Pricing Guide:** https://supercatsolutions.com/knowledgebase/catalog-pricing
- **Tradenames & Collections:** https://supercatsolutions.com/knowledgebase/tradenames-collections
- **Groups & Categories:** https://supercatsolutions.com/knowledgebase/groups-categories
- **Scraping Process:** See `../07_Data_Scraping/README.md`
