# Data Scraping — Magic Lite

Comprehensive guide for scraping product data from magiclite.com into SuperCat eCat format. Covers the full pipeline: product specs, image downloading, pricing merge, data quality audit, and post-import review.

---

## Table of Contents

1. [Decision Tree](#decision-tree)
2. [Scraping a New Product Page](#scraping-a-new-product-page)
3. [Image Rules (CRITICAL)](#image-rules)
4. [Python Script Templates](#python-script-templates)
5. [Pricing Merge Process](#pricing-merge-process)
6. [Data Quality Audit](#data-quality-audit)
7. [Post-Import Review Checklist](#post-import-review-checklist)
8. [What Works vs What Fails](#what-works-vs-what-fails)
9. [Troubleshooting](#troubleshooting)

---

## Decision Tree

Run through this EVERY time before asking a clarifying question. If the answer is here, execute.

```
Is the item in the Product Brochure PDF?
├── YES → Add it (or update CategoryCodes if it already exists)
└── NO
    ├── On website Accessories tab but NOT in brochure? → SKIP
    ├── Pattern code with XX/YY variables? → NOT a product. Skip.
    ├── Says "Custom" or "Assembly Code"? → NOT a product. Skip.
    └── "Replaces the following" reference? → Cross-reference only. NOT a new product.

Is the item already in the CSV?
├── YES → Update CategoryCodes to include new subcategory. NO duplicate rows.
└── NO → Add new row with full data.

Need specs for a new driver or controller?
├── Has its own product page? → Use that page for specs + images.
└── No dedicated page? → Use Product Drivers PDF or Product Controllers PDF.
```

---

## Scraping a New Product Page

### Phase 1: Gather Sources (DO ALL before writing any CSV)

1. **Identify subcategory** from URL path
   ```
   /product/linear-lighting/standard-tape/...  → ST
   /product/under-cabinet-lighting/...          → UCL (or specific sub like TLS)
   /product/landscape-lighting/...              → LAND (or specific sub like FSL)
   ```

2. **Download ALL PDFs** from the page:
   - Product Brochure (source of truth for associations)
   - Product Drivers PDF (specs for new drivers)
   - Product Controllers PDF (specs for new controllers)

3. **Read the Product Brochure PDF** → extract the definitive list of accessories, drivers, controllers

4. **Fetch the page** with WebFetch or curl → extract specs table, carousel images

5. **Read Product Drivers / Controllers PDFs** if brochure lists any not already in CSV

### Phase 2: Cross-Reference Against Existing CSV

```python
import csv
with open('products.csv', 'r', encoding='utf-8') as f:
    existing = {row['BaseItemCode'] for row in csv.DictReader(f)}
```

- Existing products → note which need CategoryCodes updates
- New products → need full data population
- Apply Decision Tree — if not in brochure, skip silently

### Phase 3: Execute CSV Updates

- [ ] Add new core products with full specs
- [ ] Add new accessories with `{subcategory},ACCESSORIES`
- [ ] Add new drivers with `MAIN,DRVRS` (or `{sub},DRVRS`)
- [ ] Add new controllers with `MAIN,CNTRL` (or `{sub},CNTRL`)
- [ ] Update CategoryCodes on existing shared items
- [ ] Build RelatedItems for each core product
- [ ] Download and process all images (see Image Rules below)
- [ ] Generate stories for new products (first paragraph from website, max 500 chars)
- [ ] Update ImageFileName in CSV

---

## Image Rules

**This section is the result of 6+ rounds of iPad review and fixing. Follow it exactly.**

### The Golden Rules

1. **First image = product cutout on white/transparent background. ALWAYS.**
2. **Max 5 images per product** (eCat importer limit)
3. **NEVER use as hero image:**
   - Kitchen/room application photos
   - Installation/lifestyle photos
   - Certification logos (cULus, ETL, etc.)
   - Color temperature charts
   - Spec dimension drawings (OK as image 2-5, never image 1)
4. **Application photos are OK as images 2-5**, just never image 1
5. **All images must be JPG** — convert PNG with `sips`
6. **Image naming:** `{BaseItemCode}.jpg`, `{BaseItemCode}-2.jpg`, `{BaseItemCode}-3.jpg`

### How to Identify Application Photos

Application photos are larger files with landscape aspect ratios showing the product installed in a real environment. Heuristics:

| Signal | Likely Application Photo |
|--------|------------------------|
| File size > 150KB AND > 4x bigger than image 2 | Yes |
| Landscape aspect ratio (width > height significantly) | Likely |
| Filename contains "kitchen", "application", "condo", "showroom", "room" | Yes |
| Very high resolution (> 2000px in any dimension) for a reel/spool product | Likely |

### Scraping Carousel Order

**Use Python, not grep/shell.** Shell-based image extraction is unreliable (timeouts, silent failures, encoding issues).

```python
import re, urllib.request

def get_carousel_images(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    imgs = re.findall(
        r'(https://magiclite\.com/wp-content/uploads/[^"\'>\s]+\.(?:jpg|jpeg|png))',
        html, re.IGNORECASE
    )
    
    # Filter non-product images
    skip = ['logo', 'cropped-', 'icon', 'favicon', 'android-chrome',
            'Catalogue', '350x210', 'Featured', 'featured', 'explore',
            'Click-to', 'click-to', 'MagicLite_Catalogue', 'SDL-Ultra']
    
    cleaned = []
    for img in imgs:
        if any(s.lower() in img.lower() for s in skip):
            continue
        clean = re.sub(r'-\d+x\d+', '', img)  # Remove size suffixes
        if clean not in cleaned:
            cleaned.append(clean)
    return cleaned
```

### Downloading and Converting Images

```python
import os, urllib.request, subprocess

def download_image(url, dest_jpg):
    """Download image URL, convert PNG to JPG if needed."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read()
    
    if len(data) < 500:
        return False
    
    is_png = url.lower().endswith('.png') or data[:4] == b'\x89PNG'
    if is_png:
        tmp = dest_jpg + '.tmp.png'
        with open(tmp, 'wb') as f:
            f.write(data)
        subprocess.run([
            'sips', '-s', 'format', 'jpeg',
            '-s', 'formatOptions', '90',
            tmp, '--out', dest_jpg
        ], capture_output=True, timeout=10)
        os.remove(tmp)
    else:
        with open(dest_jpg, 'wb') as f:
            f.write(data)
    
    return os.path.exists(dest_jpg) and os.path.getsize(dest_jpg) > 500
```

### Comprehensive Image Audit

After downloading, run this to verify ALL products have valid images:

```python
import os, csv

IMG_DIR = os.path.expanduser("~/Downloads/magic_lite_images")
PRODUCTS_CSV = "products.csv"

with open(PRODUCTS_CSV, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

issues = []
for r in rows:
    bic = r['BaseItemCode']
    imgs = r['ImageFileName'].strip()
    if not imgs:
        issues.append(f"NO IMAGES: {bic}")
        continue
    for img in imgs.split(','):
        img = img.strip()
        path = os.path.join(IMG_DIR, img)
        if not os.path.exists(path):
            issues.append(f"MISSING FILE: {bic} -> {img}")
        elif os.path.getsize(path) < 500:
            issues.append(f"CORRUPT/TINY: {bic} -> {img} ({os.path.getsize(path)}b)")

visible = [r for r in rows if r.get('Hideable') == 'N']
print(f"Total: {len(rows)}, Visible: {len(visible)}, Issues: {len(issues)}")
for issue in issues:
    print(f"  {issue}")
```

### Products That Had Image Issues (Magic Lite)

| Product | Issue | Root Cause | Fix |
|---------|-------|-----------|-----|
| LTSPRO | Kitchen photo as hero | `LTSPro-kitchen.jpg` was carousel image 3, but downloaded as image 1 | Re-download excluding kitchen photo entirely |
| TLE | Office application as hero | Website carousel had application photo first | Swap image 1 and 2 |
| ST-ID | Room photo as hero | Thumbnail-quality download had wrong content | Re-download from correct full-size URLs |
| DL-FR | Color chart as hero | `5CCT-Colour-Temperature-Chart.png` was carousel image 1 | Reorder: product photo first, chart last |
| MGST | Patio application as hero | 206KB landscape image (vs 17KB product photo) | Swap based on file size ratio |
| MGWL | Large application image | 140KB hero vs 25KB product photo | Re-download from fresh carousel data |
| WF-CB | Application photo in set | `Round-Head-Bollards-Application.png` | Filter out files with "Application" in name |
| LTSPRO-SW | Kitchen application in set | `LTS-PRO-Swivel-Application-In-the-kitchen-setting.png` | Filter out files with "Application" in name |
| LEDLB-5CCT | Kitchen photo in set | `House-Kitchen-web.jpg` | Filter out files with "Kitchen"/"House" in name |
| LTS-II | Condo application in set | `3000K-tom-condo-sm.jpg` | Filter out files with "condo" in name |

### Lesson: ALWAYS Do a Comprehensive Audit

Never fix images one at a time. Every time we fixed one product, the next iPad review found another with the same issue. **Fix ALL products in one sweep:**

1. Scrape ALL product pages for carousel order
2. Filter out application/lifestyle photos by filename keywords
3. Re-download ALL images from source URLs
4. Verify ALL 694 products have valid images on disk
5. Then import

---

## Pricing Merge Process

### Source Files

| File | Contains | Key Column |
|------|----------|------------|
| `ML_NSL_Combined_Price_List.csv` | Custom price levels (ml_list, ml_dn, nsl_list, nsl_dn) + UPC codes | `Item Number` |
| `ML_products_3.0 (2).csv` | NetPrice (base price) | `Item Number` |

### Merge Script Template

```python
import csv

PRODUCTS = 'products.csv'
CUSTOM = 'ML_NSL_Combined_Price_List.csv'
ML30 = 'ML_products_3.0 (2).csv'

# Load custom price list
custom = {}
with open(CUSTOM, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        custom[row['Item Number'].strip()] = row

# Load ML 3.0 for NetPrice fallback
ml30 = {}
with open(ML30, 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        ml30[row['Item Number'].strip()] = row

# Load and update products
with open(PRODUCTS, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

for row in rows:
    bic = row['BaseItemCode']
    
    if bic in custom:
        row['Price_ml_list'] = custom[bic].get('ML List', '')
        row['Price_ml_dn'] = custom[bic].get('ML D/N', '')
        row['Price_nsl_list'] = custom[bic].get('NSL List', '')
        row['Price_nsl_dn'] = custom[bic].get('NSL D/N', '')
        row['ML_UPC'] = custom[bic].get('ML UPC', '')
        row['NSL_UPC'] = custom[bic].get('NSL UPC', '')
    
    if bic in ml30 and not row.get('price_net_price', '').strip():
        row['price_net_price'] = ml30[bic].get('NetPrice', '')

with open(PRODUCTS, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
```

**Key lesson:** Products with custom price levels STILL need `price_net_price` populated. Without it, they won't display a price in Net Price viewing mode. Always run a backfill pass.

---

## Data Quality Audit

Run this before every import to catch inconsistencies:

```python
import csv, re

with open('products.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

issues = []

for r in rows:
    bic = r['BaseItemCode']
    
    # BaseItemCode rules
    if len(bic) > 20:
        issues.append(f"BIC too long ({len(bic)}): {bic}")
    if re.search(r'[^A-Za-z0-9\-_/]', bic):
        issues.append(f"BIC has invalid chars: {bic}")
    
    # Required fields
    if not r.get('TradeNameCode', '').strip():
        issues.append(f"Missing TradeNameCode: {bic}")
    if not r.get('CollectionCodes', '').strip():
        issues.append(f"Missing CollectionCodes: {bic}")
    if not r.get('CategoryCodes', '').strip():
        issues.append(f"Missing CategoryCodes: {bic}")
    if not r.get('LongDesc', '').strip():
        issues.append(f"Missing LongDesc: {bic}")
    if not r.get('ImageFileName', '').strip():
        issues.append(f"Missing ImageFileName: {bic}")
    
    # Image count <= 5
    imgs = [i.strip() for i in r.get('ImageFileName', '').split(',') if i.strip()]
    if len(imgs) > 5:
        issues.append(f"Too many images ({len(imgs)}): {bic}")
    
    # Hideable must be Y or N
    h = r.get('Hideable', '').strip()
    if h not in ('Y', 'N'):
        issues.append(f"Invalid Hideable '{h}': {bic}")
    
    # Visible products should have descriptions
    if h == 'N' and not r.get('ShortDesc', '').strip():
        issues.append(f"Visible product missing ShortDesc: {bic}")

# Duplicate check
bics = [r['BaseItemCode'] for r in rows]
dupes = [b for b in bics if bics.count(b) > 1]
if dupes:
    issues.append(f"DUPLICATE BaseItemCodes: {set(dupes)}")

print(f"Rows: {len(rows)}, Issues: {len(issues)}")
for i in issues:
    print(f"  {i}")
```

---

## Post-Import Review Checklist

Use this on an iPad after EVERY import:

### Round 1: Quick Scan
- [ ] Open catalog, browse each collection
- [ ] Are the right products visible? (not too many, not too few)
- [ ] Do hero images look correct? (product photos, not application shots)
- [ ] Are prices showing for visible products?

### Round 2: Deep Dive (per collection)
- [ ] Tap into each visible product
- [ ] Check image carousel order (product photo first)
- [ ] Verify RelatedItems show accessories/drivers/controllers
- [ ] Verify hidden variants are accessible via RelatedItems
- [ ] Check product story displays

### Round 3: Edge Cases
- [ ] Search for a product by name — does it return?
- [ ] Filter by category — do the right products appear?
- [ ] Check a product with custom pricing — correct price shown?
- [ ] Check a product with NetPrice only — price shown?

---

## What Works vs What Fails

### What Works

| Approach | Why |
|----------|-----|
| Python `urllib.request` for scraping | Reliable, handles redirects, easy to add delays |
| `sips` for PNG→JPG conversion | Built into macOS, fast, no dependencies |
| Python `csv` module for all CSV ops | Handles encoding, quoting, UTF-8 correctly |
| Product Brochure PDF as source of truth | Definitive for accessories/drivers/controllers |
| Batch processing entire collections | Fewer context switches, consistent results |
| Scraping carousel order from HTML | `re.findall` for image URLs is reliable |
| File size heuristic for application photos | Large landscape files are almost always room shots |
| Comprehensive sweeps over one-off fixes | Catches all issues in one pass |

### What Fails

| Approach | Why It Fails | Use Instead |
|----------|-------------|-------------|
| `grep`/shell for image URL extraction | Timeouts, encoding issues, silent failures | Python `urllib` + `re` |
| `curl` bulk downloads without delays | 429 rate limiting, 404 on some URLs | Add `time.sleep(0.3)` between requests |
| Fixing images one product at a time | Next iPad review finds more with same issue | Comprehensive audit of ALL products |
| Using website Accessories tab as source | Shows generic items not specific to product | Product Brochure PDF |
| Direct Python `requests` to magiclite.com | 403 Forbidden | `urllib.request` with User-Agent header |
| Trusting carousel order = correct hero | Some pages have application photo first | Always verify; swap if needed |
| Downloading thumbnail-size images | 500x370 images look bad in catalog | Download full-size (remove `-300x300` suffix) |
| Assuming all CategoryCodes exist | Fatal import errors | Verify in Admin Console FIRST |

---

## Troubleshooting

### 403 Forbidden on Scrape
```python
# Always use User-Agent header
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
```

### Rate Limiting (429)
```python
import time
time.sleep(0.3)  # 300ms between requests minimum
```

### PNG → JPG Conversion Fails
```bash
sips -s format jpeg -s formatOptions 90 input.png --out output.jpg
```

### Invalid Characters in BaseItemCode for Filenames
```python
# BaseItemCode like LTS-II-1-HW/WH has / which is invalid in filenames
safe_name = base_item_code.replace('/', '-')
# LTS-II-1-HW/WH → LTS-II-1-HW-WH.jpg
```

### iCloud Folder Permission Errors
Save images to `~/Downloads/magic_lite_images/` first, then move manually. Automated writes to iCloud paths can fail silently.

### CSV Encoding
Always UTF-8:
```python
with open('file.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
```

### Image Shows as Broken in Catalog
1. Check file exists on disk: `ls ~/Downloads/magic_lite_images/{filename}`
2. Check file size > 500 bytes (146-byte files are error pages)
3. Check it was uploaded to Admin Console image library
4. Check `ImageFileName` in CSV matches exactly (case-sensitive)

---

## Website Structure (Magic Lite)

### URL Patterns
```
Product pages:     /product/{category}/{subcategory}/{product-name}/
Category indexes:  /product/{category}/
```

### Key Category URLs

| Category | URL |
|----------|-----|
| Linear Lighting | `/product/linear-lighting/` |
| Streamline Tape | `/product/linear-lighting/streamline-tape-sl/` |
| Standard Tape | `/product/linear-lighting/standard-tape/` |
| Under Cabinet | `/product/under-cabinet-lighting/` |
| Down Lighting | `/product/down-lighting-recessed-and-surface/` |
| Landscape | `/product/landscape-lighting/` |
| Industrial | `/product/industrial-lighting/` |
| Drivers & Controllers | `/products/led-drivers-and-led-controllers/` |

### Image URL Pattern
```
https://magiclite.com/wp-content/uploads/{YYYY}/{MM}/{filename}.{ext}
```

Remove size suffixes in URLs (e.g., `-300x300`, `-1024x768`) to get full-size images.
