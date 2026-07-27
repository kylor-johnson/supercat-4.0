# Import Files — {Client Name}

All CSV files ready for SuperCat eCat import live in `Ready_For_Import/`.

---

## Files

| File | Description |
|------|-------------|
| `products.csv` | Product data (all columns populated) |
| `stories.csv` | Product stories (BaseItemCode + ProductStory, max 500 chars) |
| `customers.csv` | Customer accounts (BillTo/ShipTo) |
| `inventory.csv` | Inventory levels by BaseItemCode |
| `pricing.csv` | Additional pricing data (if not embedded in products.csv) |

---

## Import Order (STRICT)

Images are uploaded to Admin Console separately (not part of the CSV sequence below).

```
1. options.csv         Hard-deletes all options on re-import; nulls group membership
2. option_groups.csv   Must always follow options.csv to restore membership
3. products.csv        Omitted products soft-deleted on a clean import
4. stories.csv         Requires products to exist; omitted rows set story=null
5. inventory.csv       Hard-deletes all inventory on re-import
6. customers.csv       Hard-deletes ALL customers on re-import
7. matrix_options.csv  Hard-deletes all matrix pricing on re-import (if used)
```

Skip `options.csv` / `option_groups.csv` only if the org genuinely has no options
(declare in `CLIENT_PROFILE.md`). `matrix_options.csv` only if org uses matrix pricing.

Additional files (import independently as needed):

| File | Behavior | Notes |
|------|----------|-------|
| `contract_prices.csv` | Hard-deletes all contract prices | Org-specific pricing overrides |
| `riser_prices.csv` | Hard-deletes all riser prices | Regional surcharge pricing |
| `products_N.csv` + `sentinel.csv` | Multi-file merge (see below) | Supplement columns for large catalogs |

**Multi-file product merge:** Upload `products.csv` + `products_1.csv`, `products_2.csv`…
then `sentinel.csv` to trigger merge. Supplemental files add columns to existing rows
by `BaseItemCode`; they do NOT trigger soft-deletes.

**Sales Portal files** (`order_data.csv`, `invoice_data.csv`) — import via
Tools → Import Data (separate from the iPad file set). Four hard rules:
1. Date fields must be date-only — `4-16-2026 12:00:00 AM` is rejected; use `4-16-2026`.
2. No extra columns — a stray `fiscal month` column fails the entire file.
3. Line items must be contiguous by order number — the importer reads top-to-bottom and
   treats any order-number gap as end-of-order; re-appearing order numbers = error.
   Sort by order number before exporting.
4. Exact filenames — `Order_Data.csv` and `Invoice_Data.csv`; a `TBL_` prefix fails.

---

## Admin Console Setup (DO THIS BEFORE IMPORT)

**Every CollectionCode and CategoryCode in products.csv MUST exist in the admin console before import. Undefined codes = FATAL errors, not warnings.**

### Step 1: Trade Names & Collections

**Admin > Trade Names & Collections**

| TradeNameCode | Name | CollectionCodes |
|---------------|------|-----------------|
| `{CODE}` | {Client Name} | `{COL1}`, `{COL2}`, ... |

### Step 2: Groups & Categories

**Admin > Groups & Categories**

Create these Groups and add Categories under each:

| Group | Categories to Create |
|-------|---------------------|
| MAIN | `LIGHT`, `ACCESSORIES`, `DRVRS`, `CNTRL` |
| {COL1} | `{sub1}`, `{sub2}`, ... |
| {COL2} | `{sub3}`, `{sub4}`, ... |

### Step 3: Custom Price Levels (if applicable)

Create any custom price level codes needed for this client.

---

## CategoryCodes Reference

### Standard Pattern

| Product Type | CategoryCodes | Hideable |
|-------------|---------------|----------|
| Core lighting | `LIGHT,{subcategory}` | `N` (one per family) |
| Accessories | `{subcategory},ACCESSORIES` | `Y` |
| Drivers | `MAIN,DRVRS` | `Y` |
| Controllers | `MAIN,CNTRL` | `Y` |

### Shared Items

When a driver/controller serves multiple subcategories, list all in CategoryCodes:
```
SL,DRVRS         → serves only subcategory SL
SL,ST,DRVRS      → serves SL and ST
MAIN,DRVRS       → serves all
```

One row per product. Update CategoryCodes — never duplicate rows.

---

## Pricing Options

### Option A: Pricing in products.csv (recommended for simplicity)

Add price columns directly to products.csv:
- `price_net_price` — base net price (required for Net Price display mode)
- `Price_{level_code}` — custom price levels (one column per level)

### Option B: Separate pricing.csv

Use when pricing is complex or changes frequently independent of products.

### Pricing Merge Process

If client provides separate price lists:

1. **Pass 1:** Match BaseItemCode against primary price list → populate custom levels
2. **Pass 2:** Match remaining against fallback price source → populate NetPrice
3. **Pass 3:** Backfill NetPrice for Pass 1 products that also exist in fallback source
4. **Verify:** Products with custom levels STILL need `price_net_price` for Net Price display mode

---

## RelatedItems Rules

- Only core products (`LIGHT,{sub}`) get RelatedItems
- Accessories, drivers, controllers = empty RelatedItems
- Cross-link paired variants FIRST (e.g., 2700K lists 3000K)
- Then accessories, drivers, controllers
- Source: Product Brochure PDF (manufacturer's cut sheet)
- Format: comma-separated BaseItemCodes, no spaces

---

## Post-Import Checklist

- [ ] Products visible in catalog (iPad + web)
- [ ] Hero images are product photos (NOT application/room/lifestyle shots)
- [ ] Image order correct in carousel
- [ ] Only intended products visible (check Hideable)
- [ ] Pricing displays correctly
- [ ] RelatedItems work
- [ ] Category filters work
- [ ] Search returns correct results
- [ ] Product stories display
- [ ] No accessories/drivers in main browse

**Budget 2-3 review cycles.** See `../LESSONS_LEARNED.md` for common issues.
