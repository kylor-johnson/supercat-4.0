# Data Scraping Framework

Generic framework for scraping manufacturer websites into SuperCat eCat format. Adapt URLs, selectors, and product structure for each client.

---

## When to Scrape

Scrape when the client doesn't provide a clean product file with all required fields. Common scenario: client has basic item numbers and prices, but no images, specs, or descriptions. Their website has everything.

---

## Decision Tree

```
Is the item in the manufacturer's spec sheet / brochure?
├── YES → Add to products.csv (or update CategoryCodes if it exists)
└── NO
    ├── On website but not in official docs? → SKIP
    ├── Pattern/template code (XX variables)? → NOT a product. Skip.
    ├── Says "Custom" or "Assembly Code"? → NOT a product. Skip.
    └── "Replaces" / "Superseded by" reference? → Cross-reference only.

Already in CSV?
├── YES → Update CategoryCodes. Never duplicate rows.
└── NO → Add new row with full data.
```

---

## Scraping Process

### Phase 1: Gather Sources

1. **Identify product structure** from the website
   - How are products organized? (collections → categories → individual products)
   - What's the URL pattern?

2. **Download spec sheets / brochures**
   - These are the source of truth for which accessories, drivers, controllers belong to a product
   - Website Accessories tabs often show generic items — don't trust them

3. **Fetch product pages** for specs and images

### Phase 2: Build products.csv

For each product:
- Extract specs from HTML tables
- Map to SuperCat CSV columns (see column reference below)
- Assign CategoryCodes based on product type
- Build RelatedItems from brochure data
- Download and process images

### Phase 3: Data Quality

- Run validation script (see below)
- Check for duplicates, missing fields, invalid codes
- Verify image files exist on disk

---

## Image Rules

**Learned the hard way across multiple clients. Follow exactly.**

### Golden Rules

1. **Image 1 = product photo on white/transparent background. ALWAYS.**
2. **Max 5 images per product** (eCat importer limit)
3. **All images must be JPG** (convert PNG with `sips` on macOS)
4. **Naming:** `{BaseItemCode}.jpg`, `{BaseItemCode}-2.jpg`, etc.

### NEVER Use as Hero Image (Image 1)

- Kitchen/room/lifestyle application photos
- Installation photos
- Certification logos (cULus, ETL, Energy Star)
- Color temperature charts or spec drawings
- Marketing banners

These are fine as images 2-5, just never image 1.

### How to Detect Application Photos

| Signal | Likely Application Photo |
|--------|------------------------|
| File size > 4x the next image | Room/environment shot |
| Landscape aspect ratio with large dimensions | Scene photo |
| Filename contains: kitchen, application, condo, showroom, room, install | Yes |
| Resolution > 2000px for a small product | Room photo at high res |

### Scraping Images from Website Carousel

**Use Python. Shell/grep is unreliable for this.**

```python
import re, urllib.request, os, subprocess, time

def get_carousel_images(url):
    """Get product image URLs from a website page carousel."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    
    # Adjust this regex for the client's website image URL pattern
    imgs = re.findall(
        r'(https://example\.com/wp-content/uploads/[^"\'>\s]+\.(?:jpg|jpeg|png))',
        html, re.IGNORECASE
    )
    
    # Filter non-product images (adjust keywords per client)
    skip = ['logo', 'cropped-', 'icon', 'favicon', 'android-chrome',
            'Catalogue', 'Featured', 'featured', 'banner']
    
    cleaned = []
    for img in imgs:
        if any(s.lower() in img.lower() for s in skip):
            continue
        clean = re.sub(r'-\d+x\d+', '', img)  # Remove WordPress size suffixes
        if clean not in cleaned:
            cleaned.append(clean)
    return cleaned

def download_image(url, dest_jpg):
    """Download image, convert PNG to JPG if needed."""
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

### Comprehensive Image Audit Script

Run BEFORE every import:

```python
import os, csv

IMG_DIR = "path/to/images"
CSV_PATH = "products.csv"

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

issues = []
for r in rows:
    bic = r['BaseItemCode']
    imgs = r['ImageFileName'].strip()
    
    if not imgs:
        issues.append(f"NO IMAGES: {bic}")
        continue
    
    parts = [i.strip() for i in imgs.split(',') if i.strip()]
    if len(parts) > 5:
        issues.append(f"TOO MANY IMAGES ({len(parts)}): {bic}")
    
    for img in parts:
        path = os.path.join(IMG_DIR, img)
        if not os.path.exists(path):
            issues.append(f"MISSING: {bic} -> {img}")
        elif os.path.getsize(path) < 500:
            issues.append(f"CORRUPT: {bic} -> {img}")

print(f"Products: {len(rows)}")
print(f"Issues: {len(issues)}")
for i in issues:
    print(f"  {i}")
```

### Key Lesson: Always Audit Comprehensively

Never fix images one product at a time. When you find one product with a wrong hero image, audit ALL products. The same issue (application photo as hero, carousel order mismatch, etc.) always affects multiple products.

---

## Data Quality Audit Script

Run before every import:

```python
import csv, re

with open('products.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

issues = []
for r in rows:
    bic = r['BaseItemCode']
    
    if len(bic) > 20:
        issues.append(f"BIC too long ({len(bic)}): {bic}")
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
    
    h = r.get('Hideable', '').strip()
    if h not in ('Y', 'N'):
        issues.append(f"Invalid Hideable '{h}': {bic}")

# Duplicate check
bics = [r['BaseItemCode'] for r in rows]
dupes = set(b for b in bics if bics.count(b) > 1)
if dupes:
    issues.append(f"DUPLICATES: {dupes}")

# Code inventory (print these — verify they exist in Admin Console)
collections = set()
categories = set()
for r in rows:
    for c in r['CollectionCodes'].split(','):
        collections.add(c.strip())
    for c in r['CategoryCodes'].split(','):
        categories.add(c.strip())

print(f"Rows: {len(rows)}, Issues: {len(issues)}")
print(f"CollectionCodes: {sorted(collections)}")
print(f"CategoryCodes: {sorted(categories)}")
for i in issues:
    print(f"  {i}")
```

---

## products.csv Column Reference

### Required Columns

| Column | Description | Example |
|--------|------------|---------|
| `BaseItemCode` | Unique product identifier (max 20 chars) | `LTSPRO-9-WH` |
| `TradeNameCode` | Client trade name code | `ML` |
| `CollectionCodes` | Collection the product belongs to | `LL` |
| `CategoryCodes` | Category classification | `LIGHT,TLS` |
| `ShortDesc` | Short name for admin/order views | `LED Task Star Pro 9" White` |
| `LongDesc` | Full product name for catalog display | `LED Task Star Pro - 9 Inch - White` |
| `ImageFileName` | Comma-separated image filenames | `LTSPRO-9-WH.jpg,LTSPRO-9-WH-2.jpg` |
| `Hideable` | `Y` = hidden from browse, `N` = visible | `N` |
| `NewItem` | Mark as new item | `Y` |

### Spec Columns (populate when available)

| Column | Maps to Website |
|--------|----------------|
| `InputVoltage` | "Input Voltage" |
| `PowerConsumption_W` | "Power Consumption" |
| `ColorTemperature_K` | "Colour Temperature" |
| `LumenOutput` | "Lumen Output" |
| `BeamAngle_Deg` | "Beam Angle" |
| `CRI` | "CRI" |
| `Dimmable` | "Dimmable" |
| `IPrating` | "IP Rating" |
| `Warranty_Years` | "Warranty" |
| `Approvals` | "Approvals" |

### Pricing Columns

| Column | Description |
|--------|------------|
| `price_net_price` | Base net price (required for NP display) |
| `Price_{level}` | Custom price level columns |

### Relationship Columns

| Column | Description |
|--------|------------|
| `RelatedItems` | Comma-separated BaseItemCodes of related products |

---

## stories.csv Format

```csv
BaseItemCode,ProductStory
LTSPRO-9-WH,"The LED Task Star Pro delivers efficient under-cabinet illumination..."
```

- One row per product
- Max 500 characters
- Source: first paragraph from manufacturer website product description
- Fallback: generate from LongDesc if no website description available

---

## What Works vs What Fails

### Works

| Approach | Why |
|----------|-----|
| Python `urllib.request` + `re` for scraping | Reliable, handles encoding, easy delays |
| `sips` for image conversion (macOS) | Built-in, fast, no extra dependencies |
| Python `csv` module for all CSV ops | Proper encoding, quoting, UTF-8 |
| Product brochure/spec sheet as source of truth | Definitive for product associations |
| Processing entire collections at once | Consistent results, fewer context switches |
| Comprehensive audits over one-off fixes | Catches systemic issues |
| File size heuristic for application photos | Large landscape files = room shots |
| Adding `time.sleep(0.3)` between requests | Avoids rate limiting |

### Fails

| Approach | Why | Use Instead |
|----------|-----|-------------|
| `grep`/shell for image extraction | Timeouts, encoding issues | Python `urllib` + `re` |
| `curl` without delays | 429 rate limiting | Add sleep between requests |
| Fixing one image at a time | Same issue affects multiple products | Comprehensive audit |
| Website accessories tab as source | Shows generic items | Manufacturer brochure/spec sheet |
| Python `requests` library | 403 on some sites | `urllib.request` with User-Agent |
| Trusting carousel order blindly | Some sites put app photos first | Verify; swap if needed |
| Downloading thumbnail URLs | Small/blurry images | Remove size suffixes from URLs |
| Assuming admin console has codes | Fatal import errors | Verify ALL codes before import |

---

## Troubleshooting

### 403 Forbidden
```python
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})
```

### Rate Limiting (429)
```python
import time
time.sleep(0.3)  # Minimum 300ms between requests
```

### Invalid Characters in Filenames
```python
safe_name = base_item_code.replace('/', '-').replace('\\', '-')
```

### Image Conversion
```bash
sips -s format jpeg -s formatOptions 90 input.png --out output.jpg
```

### CSV Encoding
```python
with open('file.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
```
