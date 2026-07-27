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

```
1. Images          Upload ALL JPGs to Admin Console FIRST
2. products.csv    Requires images to exist
3. stories.csv     Requires products to exist
4. customers.csv   Independent
5. inventory.csv   Requires products to exist
6. pricing.csv     Requires products to exist
```

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
