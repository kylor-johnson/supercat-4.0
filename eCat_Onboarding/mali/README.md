# Magic Lite — SuperCat eCat Implementation

**Client:** Magic Lite  
**Platform:** SuperCat eCat  
**TradeNameCode:** `ML`  
**Status:** Live — 694 products, 5 collections, full pricing  
**Image Store:** `~/Downloads/magic_lite_images/` (370 unique JPG files)

---

## Current State

| Metric | Value |
|--------|-------|
| Total products | 694 |
| Visible products (Hideable=N) | 61 |
| Hidden products (Hideable=Y) | 633 |
| Collections | 5 (LL, UCL, DL, LAND, IL) |
| Unique image files | 370 |
| Stories | 694 (one per product) |
| Pricing sources | ML/NSL custom levels + NetPrice fallback |

---

## Folder Structure

```
Magic Lite/
├── README.md                              ← You are here
│
├── 00_Import_Files/                       ← IMPORT FILES + REFERENCE
│   ├── README.md                          ← Admin console config, CategoryCodes, pricing columns
│   ├── IMPORT_PROCESS_START_TO_FINISH.md  ← Step-by-step import guide (with real error fixes)
│   └── Ready_For_Import/
│       ├── products.csv                   ← 694 products, 51 columns
│       ├── stories.csv                    ← 694 product stories
│       ├── customers.csv
│       ├── inventory.csv
│       └── pricing.csv
│
├── 01_Kickoff/
├── 02_Project_Plan/
├── 03_Data/                               ← Source data from client
│   ├── ML_NSL_Combined_Price_List.csv     ← Custom price levels (ml_list, ml_dn, nsl_list, nsl_dn)
│   ├── ML_products_3.0 (2).csv           ← NetPrice fallback source
│   ├── ML + NSL COMBINED.csv             ← Combined customer list
│   └── Magic Lite Test Photos/            ← Test images from client
├── 04_Training/
├── 05_Go_Live/
├── 06_Notes/
│
└── 07_Data_Scraping/                      ← Scraping framework + scripts
    ├── README.md                          ← COMPLETE scraping reference (image rules, Python templates)
    ├── Streamline_Tape/
    └── Archive/
```

---

## SuperCat Configuration

### Trade Names & Collections

```
TradeNameCode:  ML (Magic Lite)

CollectionCodes:
  LL   → Linear Lighting
  UCL  → Under Cabinet Lighting
  DL   → Down Lighting
  LAND → Landscape Lighting
  IL   → Industrial Lighting
```

### Groups & Categories (Admin Console)

These MUST exist in the admin console before import. Undefined codes cause fatal errors.

| Group | Code | Categories |
|-------|------|------------|
| Main | MAIN | LIGHT, ACCESSORIES, DRVRS, CNTRL |
| Linear Lighting | LL | SL, ST, ES, NF, STRING, WW, EXT |
| Under Cabinet | UCL | TLS, RGSD, GIM, SMD, FR, UCL (sub-category) |
| Down Lighting | DL | TL, RGL, GDL, SM, TLE, FR |
| Landscape | LAND | FSL, PL, WDL, IGL, TA |
| Industrial | IL | IND |

### CategoryCodes by Product Type

| Product Type | Pattern | Examples |
|-------------|---------|----------|
| Core lighting | `LIGHT,{sub}` | `LIGHT,SL`, `LIGHT,TLS`, `LIGHT,IND` |
| Accessories | `{sub},ACCESSORIES` or `ACCESSORIES,{sub}` | `SL,ACCESSORIES`, `ACCESSORIES,EXT` |
| Drivers | `MAIN,DRVRS` or `{sub},DRVRS` | `MAIN,DRVRS`, `SL,ST,DRVRS` |
| Controllers | `MAIN,CNTRL` or `{sub},CNTRL` | `MAIN,CNTRL`, `SL,ST,CNTRL` |
| Extrusions | `ACCESSORIES,EXT` | All extrusion products |

### Pricing Columns

| Column | Source | Description |
|--------|--------|-------------|
| `price_net_price` | ML_products_3.0 | Base net price (required for NP display mode) |
| `Price_ml_list` | ML_NSL_Combined_Price_List | Magic Lite list price |
| `Price_ml_dn` | ML_NSL_Combined_Price_List | Magic Lite dealer net |
| `Price_nsl_list` | ML_NSL_Combined_Price_List | NSL list price |
| `Price_nsl_dn` | ML_NSL_Combined_Price_List | NSL dealer net |
| `ML_UPC` | ML_NSL_Combined_Price_List | Magic Lite UPC code |
| `NSL_UPC` | ML_NSL_Combined_Price_List | NSL UPC code |

### Hideable Strategy

| Rule | Hideable |
|------|----------|
| ONE representative per product family (e.g., LTSPRO-9-WH) | `N` |
| All other sizes/finishes of that family | `Y` |
| ALL accessories | `Y` |
| ALL drivers | `Y` |
| ALL controllers | `Y` |
| ALL extrusion products | `N` (browsable) |

---

## Key Documents

| What you need | Where |
|---------------|-------|
| Admin console setup + CategoryCodes reference | `00_Import_Files/README.md` |
| Step-by-step import with real error fixes | `00_Import_Files/IMPORT_PROCESS_START_TO_FINISH.md` |
| How to scrape products + image rules | `07_Data_Scraping/README.md` |
| Import-ready CSV files | `00_Import_Files/Ready_For_Import/` |
| Client source pricing data | `03_Data/` |

---

## Resources

- **Magic Lite Website:** https://magiclite.com/
- **Magic Lite Catalog 2025:** https://magiclite.com/wp-content/uploads/2025/04/Magic-Lite-Catalogue_May-2025.pdf
- **SuperCat Import Guide:** https://supercatsolutions.com/knowledgebase/import-product-file
- **SuperCat Pricing Guide:** https://supercatsolutions.com/knowledgebase/catalog-pricing
- **Tradenames & Collections:** https://supercatsolutions.com/knowledgebase/tradenames-collections
- **Groups & Categories:** https://supercatsolutions.com/knowledgebase/groups-categories
