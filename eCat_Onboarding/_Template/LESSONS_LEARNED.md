# Lessons Learned — SuperCat eCat Implementation

Compiled from real client implementations. Read this BEFORE starting a new client. Every lesson here cost time to learn.

---

## Table of Contents

1. [Admin Console Setup](#1-admin-console-setup)
2. [Product Data (products.csv)](#2-product-data)
3. [Image Management](#3-image-management)
4. [Pricing](#4-pricing)
5. [Hideable Strategy](#5-hideable-strategy)
6. [Web Scraping](#6-web-scraping)
7. [Import Process](#7-import-process)
8. [Post-Import Review](#8-post-import-review)
9. [Process & Workflow](#9-process--workflow)

---

## 1. Admin Console Setup

### CRITICAL: Define ALL Codes Before Import (unless Auto-Create is on)

**What happened:** Imported products.csv with CategoryCodes `UCL`, `TLE`, `IND` and CollectionCodes `IND` that weren't defined in the Admin Console. The import failed with errors and those rows were rejected.

**Root cause + nuance:** There are TWO taxonomy methods:
- **Standard method** (most orgs): tradenames/collections/categories must be **pre-created** in Admin Console or rows error out. Use short codes ≤5 chars; supports multiple comma-separated codes per item.
- **Auto-Create method** (if enabled for the org): tradenames/collections/categories **are** created automatically from whatever strings are in the CSV — codes can exceed 5 chars — BUT each item is then limited to a **single** collection and a single category, and the string you ship becomes the **iPad label** (so never ship cryptic codes like `COL126`).
- **Groups NEVER auto-create** from a product import under either method — create them first; categories live under groups.

**Rule:** Confirm which method the org uses. Under Standard, run the validation script that prints all unique CollectionCodes/CategoryCodes and create every one in the Admin Console FIRST.

```python
import csv
with open('products.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
collections = set()
categories = set()
for r in rows:
    for c in r['CollectionCodes'].split(','):
        collections.add(c.strip())
    for c in r['CategoryCodes'].split(','):
        categories.add(c.strip())
print(f"CollectionCodes to verify: {sorted(collections)}")
print(f"CategoryCodes to verify: {sorted(categories)}")
```

### Codes Should be Max 5 Characters (Standard method)

Under the Standard taxonomy method, CollectionCodes and CategoryCodes should be 5 characters or fewer and pre-created in Admin. Design short codes early. (Under Auto-Create, codes can be longer but become the iPad label — see above.)

### CollectionCodes vs CategoryCodes Are Different Entities

A code like `UCL` can be BOTH a CollectionCode (top-level browsing) AND a CategoryCode (filtering). They're configured in different places:
- CollectionCodes → Admin > Trade Names & Collections
- CategoryCodes → Admin > Groups & Categories

If a code appears in both columns of your CSV, create it in BOTH places.

---

## 2. Product Data

### One Row Per Product, No Duplicates

**What happened:** A shared driver appeared in two brochures. It was added twice to the CSV with different CategoryCodes.

**Rule:** One row per BaseItemCode. If a driver/controller serves multiple subcategories, update its CategoryCodes to include all: `SL,ST,DRVRS` instead of creating two rows.

### BaseItemCode: Max 20 Characters

Alphanumeric, hyphens, underscores only. No slashes, no spaces, no special characters.

**What happened:** Product `LTS-II-1-HW/WH` had a slash. Invalid for filenames and potentially for the importer.

**Fix:** Sanitize: replace `/` with `-` → `LTS-II-1-HW-WH`

### Stories: Max 500 Characters

ProductStory in stories.csv should be the first paragraph from the manufacturer's website product description, truncated to 500 characters. If no website description, generate from LongDesc.

### RelatedItems: Only on Core Products

Only core products (CategoryCodes starting with `LIGHT,`) should have RelatedItems populated. Accessories, drivers, controllers → leave RelatedItems empty. Source associations from the manufacturer's official brochure/spec sheet, NOT the website's generic accessories tab.

---

## 3. Image Management

### The Hero Image Problem (Most Time-Consuming Issue)

**What happened:** After import, the iPad catalog showed kitchen photos, office scenes, and application lifestyle images as the primary product photo for ~30% of visible products. This required 6+ rounds of review and fixing.

**Root cause:** Manufacturer websites often place application/lifestyle photos FIRST in their carousel because they're more visually appealing. The eCat catalog displays the first image in `ImageFileName` as the hero. If you blindly download in carousel order, you get kitchen scenes as hero images.

**Rules:**
1. Image 1 MUST be the product cutout on a white/transparent background
2. Application photos (kitchens, rooms, installations) are OK as images 2-6, NEVER image 1
3. After downloading, ALWAYS verify the hero image is actually a product photo
4. When in doubt, check file size — application photos are typically much larger (4x+) than product cutouts

### Application Photo Detection Heuristics

| Signal | Indicates Application Photo |
|--------|----------------------------|
| File size > 150KB AND > 4x bigger than next image | Very likely room/scene shot |
| Landscape orientation with large dimensions | Scene composition |
| Filename keywords: kitchen, application, condo, showroom, room, install, house | Yes |
| Very high resolution (> 2000px) for a small physical product | High-res scene |

### Max 6 Images Per Product (12 with paid flag)

The eCat importer supports **6 images per product by default**, or **12** if the org has the paid `enable_twelve_product_images` flag turned on. `ImageFileName` is a comma-separated list, primary first; names over the limit are truncated with a warning.

### All Images Must Be JPG

Convert PNGs with `sips` on macOS:
```bash
sips -s format jpeg -s formatOptions 90 input.png --out output.jpg
```

### Always Audit Comprehensively

**What happened:** We fixed LTSPRO's hero image. Next iPad review: TLE had the same issue. Fixed TLE. Next review: ST-ID had it too. Fixed ST-ID. Then found 25+ more families with the same issue.

**Rule:** When you find one product with an image issue, audit ALL products immediately. The same root cause (carousel order mismatch, application photo first) always affects multiple products. Fix them ALL in one sweep.

### Image Files with < 500 Bytes Are Error Pages

Downloaded "images" that are only 146-500 bytes are typically 404 error pages, not actual images. Always filter by file size after downloading.

### Remove WordPress Size Suffixes

WordPress URLs often include size variants: `photo-300x300.jpg`, `photo-1024x768.jpg`. These are thumbnails. Remove the suffix to get the full-size image:

```python
import re
full_url = re.sub(r'-\d+x\d+', '', thumbnail_url)
```

---

## 4. Pricing

### Products With Custom Levels Still Need NetPrice

**What happened:** 87 products had custom price levels (ml_list, ml_dn, etc.) but empty `price_net_price`. When viewed in Net Price display mode, these products showed $0.00 or blank.

**Rule:** ALWAYS populate `price_net_price` for every product that has a price, regardless of whether it also has custom levels. Net Price mode uses `price_net_price`, not custom levels.

### Pricing Merge Order Matters

When a client provides multiple price sources:

1. **Pass 1:** Custom price levels (client-specific tiers, most specific)
2. **Pass 2:** NetPrice fallback for remaining products
3. **Pass 3:** Backfill NetPrice for Pass 1 products from the fallback source

Never derive prices (no calculations, no markup percentages). Use ONLY the values from the source files.

### Some Products Won't Have Prices

That's OK. Leave price columns blank for products without pricing data. The catalog handles this gracefully.

---

## 5. Hideable Strategy

### Start Strict, Loosen Later

**What happened:** Initially set only accessories/drivers/controllers as hidden. iPad review: way too many products visible (all LTSPRO sizes, all bollard variants, all extrusion accessories). Had to go through 3 rounds of tightening Hideable flags.

**Better approach:** Start with MAXIMUM hiding:
- ONE representative per product family → `Hideable: N`
- Everything else → `Hideable: Y`

It's much easier to make a hidden product visible than to realize you have 200 products cluttering the browse screen and needing to hide 180 of them.

### What Makes a Good "Representative"

Choose the most common/popular variant as the visible one:
- Middle size (not smallest, not largest)
- Most popular finish (usually white)
- Standard color temperature (usually 3000K or 4000K)

### ALL Accessories, Drivers, Controllers Should Be Hidden

No exceptions. They're accessed via RelatedItems on the core product, not by browsing.

---

## 6. Web Scraping

### Python Over Shell (Always)

**What happened:** Used `grep`, `awk`, and custom shell functions to extract image URLs. They timed out, failed silently on encoding issues, and produced incomplete results.

**Rule:** Use Python `urllib.request` + `re` for ALL scraping. Never shell commands.

### Rate Limiting Prevention

**What happened:** Bulk downloading 200+ images with no delay → 429 Too Many Requests.

**Rule:** Always add `time.sleep(0.3)` minimum between HTTP requests.

### URLs Change and Go 404

**What happened:** Scraped product page URLs, came back weeks later to re-download images, and 30% of URLs returned 404. Manufacturer restructured their website.

**Rule:** Save the full image URLs (not just the page URL) when you first scrape them. Consider saving to a JSON file so you have a reference. If re-scraping, try alternate URL patterns:
- `/product/{old-path}/` → 404
- `/product/{new-path}/` → 200
- Slug may have changed (e.g., added words, changed hyphens)

### Use User-Agent Headers

**What happened:** Raw `urllib.request` without headers → 403 Forbidden on some manufacturer sites.

**Fix:** Always set User-Agent:
```python
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
```

### Product Brochure PDFs Are the Source of Truth

**What happened:** Website Accessories tab listed generic items that didn't belong to the specific product family. Led to incorrect RelatedItems associations.

**Rule:** For product relationships (which accessories, drivers, controllers go with which product), ALWAYS use the manufacturer's Product Brochure PDF — not the website.

---

## 7. Import Process

### Image Upload BEFORE Product Import

**Why:** products.csv references image filenames. If images aren't uploaded when products import, products won't have images. You'd need to re-import after uploading.

### Re-Import Updates, Doesn't Duplicate

Products are matched by BaseItemCode. If you re-import a CSV with the same BaseItemCodes, it updates existing products — it doesn't create duplicates. This is your friend for fix cycles.

### Custom Fields Cause Warnings, Not Errors

If products.csv has columns that aren't configured as custom fields in the Admin Console (e.g., `MountingType`, `Wattage_W`), the importer shows warnings but still imports the product. The unrecognized columns are simply skipped.

### Check the Import Log

The import log is your feedback loop. Read every warning and error. Don't assume "it worked" without checking.

---

## 8. Post-Import Review

### iPad Review Is Non-Negotiable

**What happened:** Every single import had issues visible on the iPad that weren't apparent from the CSV data alone: wrong hero images, too many visible products, missing prices, wrong category assignments.

**Rule:** Budget 30 minutes per review cycle. Plan for 2-3 cycles minimum.

### Take Screenshots

When reviewing on iPad, take screenshots of issues. They're essential for communicating what's wrong and verifying fixes.

### Review Checklist

1. **Hero images:** Product photo on white background (not lifestyle/application)
2. **Visibility:** Right number of products in browse (not too many, not too few)
3. **Pricing:** Visible products show prices (not blank or $0.00)
4. **RelatedItems:** Core products link to accessories/drivers/controllers
5. **Categories:** Filters show correct product subsets
6. **Search:** Returns relevant results
7. **Stories:** Display on product detail page

---

## 9. Process & Workflow

### Process Entire Collections at Once

**What happened:** Scraped products one at a time, leading to inconsistent handling, missed shared drivers, and repeated work.

**Better approach:** Process an entire collection (all products in "Linear Lighting") in one session. You catch shared accessories, identify drivers/controllers that appear across subcategories, and apply consistent naming.

### Document Everything

Every decision, every CategoryCode mapping, every quirk of the client's data. You WILL come back to this months later and wonder "why did we do it this way?"

### The 80/20 of Time Spent

From real experience, here's where time actually goes:

| Task | Estimated % | Notes |
|------|------------|-------|
| Initial scraping + CSV population | 25% | The "fun" part |
| Image management (download, order, audit) | 35% | THE biggest time sink |
| Admin console config + import troubleshooting | 15% | Mostly fixing codes |
| Post-import review + fix cycles | 20% | iPad review + CSV fixes |
| Pricing merge | 5% | Straightforward once logic is defined |

**Image management takes 35% of total time.** Plan accordingly.

### Don't Trust "It Looks Right in the CSV"

The CSV can look perfect and still have issues visible only in the catalog:
- Hero image wrong (file exists but content is an application photo)
- Hideable logic correct but too many products showing
- Pricing populated but not displaying in the right mode

**Always verify on the actual device (iPad).**

---

## Quick Reference: Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Undefined CategoryCode in CSV | Fatal import error | Create in Admin Console first |
| Application photo as hero image | Unprofessional catalog | Audit ALL images, swap order |
| Missing `price_net_price` on priced products | $0 in Net Price mode | Backfill from price source |
| Duplicate BaseItemCode rows | Import confusion | One row per product, update CategoryCodes |
| BaseItemCode > 20 chars | Import rejection | Shorten the code |
| > 6 images per product | Import truncation/warning | Limit to 6 (or 12 with `enable_twelve_product_images`), choose best ones |
| Hideable = N on accessories | Cluttered browse | Set to Y for all accessories/drivers/controllers |
| Using website Accessories tab for RelatedItems | Wrong associations | Use manufacturer brochure PDF |
| Shell scraping (grep/awk) | Silent failures | Python urllib + re |
| Downloading thumbnails instead of full images | Blurry catalog photos | Remove -NNNxNNN from URLs |
| SmartList item list pasted comma-separated | Treated as one giant invalid item number | Paste item codes **newline-separated** (KB says comma — KB is wrong for the UI) |
| Customer/inventory/options file imported partial | HARD-deletes everything not in the file | Always send the FULL file; see delete-semantics in `ecat-ground-truth` |
| Expected deletes didn't happen | An `Error` row was present | Fix all Errors — deletes only run on a clean (warnings-only) import |
