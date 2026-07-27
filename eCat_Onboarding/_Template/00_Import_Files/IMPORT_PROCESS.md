# Import Process — Start to Finish

Generic process for importing any client into SuperCat eCat. Adapted from battle-tested Magic Lite implementation.

---

## Pre-Flight

### Files Ready?

| File | Check |
|------|-------|
| Product images (JPG) | All exist on disk, correct naming, product photo first |
| `products.csv` | All columns populated, data quality audit passed |
| `stories.csv` | One row per product, max 500 chars |
| `customers.csv` | Required fields: BillToCode, BillToName, DefaultPriceCode, TerritoryCodes |
| `inventory.csv` | BaseItemCode + quantity fields |

### Admin Console Configured?

- [ ] Confirm taxonomy method: **Standard** (pre-create codes) vs **Auto-Create** (codes auto-create from CSV strings, single collection+category per item)
- [ ] TradeNameCode exists (Standard method)
- [ ] ALL CollectionCodes exist (Standard method — check EVERY unique value in products.csv)
- [ ] ALL CategoryCodes exist (Standard method — check EVERY unique value)
- [ ] Groups exist (Groups NEVER auto-create from a product import; categories live under groups)
- [ ] Custom fields pre-registered in Admin (Products → Custom Fields, "Send to iPad")
- [ ] Custom price levels created (if applicable)

### Quick Validation Script

```python
import csv
with open('products.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Collect all unique codes
collections = set()
categories = set()
for r in rows:
    for c in r['CollectionCodes'].split(','):
        collections.add(c.strip())
    for c in r['CategoryCodes'].split(','):
        categories.add(c.strip())

print(f"Products: {len(rows)}")
print(f"CollectionCodes to create: {sorted(collections)}")
print(f"CategoryCodes to create: {sorted(categories)}")
print(f"Visible: {sum(1 for r in rows if r['Hideable'] == 'N')}")
print(f"With images: {sum(1 for r in rows if r['ImageFileName'].strip())}")
```

Run this BEFORE import. Create every code it lists in the Admin Console.

---

## Step 1: Upload Images

1. Navigate to **Admin > Products > Images** (or bulk upload)
2. Upload ALL JPG files
3. Wait for upload to complete
4. Spot-check a few images appear in the library

**Why first:** products.csv references filenames. Missing images = products with no photos.

---

## Step 2: Import Products

1. **Admin > Tools > Import Data > Products**
2. Select `products.csv`
3. Map columns
4. Run import
5. **Read the import log carefully**

### Expected Warnings (safe to ignore)

```
Warning: Custom field 'MountingType' not configured — skipped
```

CSV has columns the admin console doesn't have custom fields for. Data is skipped for those columns only. Products still import.

### Fatal Errors (MUST fix)

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid CategoryCodes code: 'XX'` | Code not in Admin Console | Add in Groups & Categories |
| `Invalid CollectionCodes code: 'XX'` | Collection not defined | Add in Trade Names & Collections |
| `Invalid TradeNameCode: 'XX'` | Tradename not created | Add in Trade Names & Collections |
| `BaseItemCode exceeds 20 characters` | Code too long | Shorten it (alphanumeric + hyphens + underscores only) |
| `Invalid value: field=price_net_price` | Non-numeric price value | Check for data in wrong column |
| `Duplicate BaseItemCode: 'XX'` | Two rows with same code | Remove the duplicate |
| More than 6 images on a product | Over default image limit | Limit to 6 (or 12 if org has the paid twelve-image flag) |

### After Successful Import

Products are matched by BaseItemCode. Re-importing updates existing products in place — no need to delete first.

---

## Step 3: Import Stories

1. **Admin > Tools > Import Data > Stories**
2. Select `stories.csv`
3. Map BaseItemCode and ProductStory
4. Run import

---

## Step 4: Import Customers

1. **Admin > Tools > Import Data > Customers**
2. Select `customers.csv`
3. Map all columns
4. Run import

Required: BillToCode, BillToName, DefaultPriceCode, TerritoryCodes

---

## Step 5: Import Inventory

1. **Admin > Tools > Import Data > Inventory**
2. Select `inventory.csv`
3. Map BaseItemCode + quantity fields
4. Run import

---

## Step 6: iPad Review

**DO NOT SKIP THIS.** Every import needs at least one iPad review cycle.

### Round 1: Browse Check (5 min)
- [ ] Open catalog, scroll through each collection
- [ ] Correct number of visible products?
- [ ] Hero images are product photos? (not lifestyle/application shots)
- [ ] Prices showing?

### Round 2: Detail Check (15 min)
- [ ] Tap 5-10 products across different collections
- [ ] Image carousel order correct?
- [ ] RelatedItems showing accessories/variants?
- [ ] Product story displays?
- [ ] Price correct for customer type?

### Round 3: Edge Cases (10 min)
- [ ] Search by product name
- [ ] Filter by category
- [ ] Check a hidden product is accessible via RelatedItems
- [ ] Check a product with no price (should show blank or "contact us")

### Common Issues Found in Review

| Issue | Cause | Fix |
|-------|-------|-----|
| Application photo as hero | Wrong image order in CSV or on disk | Re-download images, product cutout first |
| Too many products visible | Hideable flags wrong | Set Y for variants/accessories |
| No prices showing | `price_net_price` empty | Populate from price source |
| Accessories in main browse | Hideable = N on accessories | Set to Y |
| Wrong category filter results | CategoryCodes incorrect | Fix codes, re-import |

---

## Re-Import Cycle

When iPad review finds issues:

1. Fix the CSV (products.csv, stories.csv, etc.)
2. Re-upload any changed image files
3. Re-import the CSV — updates existing products by BaseItemCode
4. Re-verify on iPad
5. Repeat until clean

**Budget 2-3 cycles minimum.** The first import is never perfect.

---

## Pricing Implementation Options

### Option 1: NetPrice Only (Simplest)

Every product gets one price in `price_net_price`. All customers see the same price.

### Option 2: NetPrice + Custom Levels

- `price_net_price` = base/default price
- `Price_{level}` columns for customer-specific pricing
- Customer's `DefaultPriceCode` determines which level they see

### Option 3: Separate pricing.csv

For complex pricing that changes independently of products.

### Key Rule

**Products with custom price levels STILL need `price_net_price` populated.** Without it, the product shows no price in Net Price viewing mode. Always backfill.
