# {CLIENT NAME} — SuperCat eCat Implementation

**Client:** {Client Name}  
**Platform:** SuperCat eCat  
**TradeNameCode:** `{CODE}`  
**Status:** In Progress  

---

## How to Use This Template

1. Copy this entire `_Template/` folder
2. Rename it to your client name (e.g., `Acme Lighting/`)
3. Find-and-replace `{CLIENT NAME}`, `{Client Name}`, `{CODE}` with real values
4. Read `LESSONS_LEARNED.md` before you start — it will save you hours
5. Follow the process in order: Admin Console setup → Scraping → Import → Review

---

## Folder Structure

```
{Client Name}/
├── README.md                              ← You are here (client overview + config)
├── LESSONS_LEARNED.md                     ← READ THIS FIRST — pitfalls from past clients
│
├── 00_Import_Files/                       ← IMPORT FILES + REFERENCE
│   ├── README.md                          ← Admin console setup, CategoryCodes, pricing
│   ├── IMPORT_PROCESS.md                  ← Step-by-step import guide
│   └── Ready_For_Import/
│       ├── products.csv                   ← Product data
│       ├── stories.csv                    ← Product stories
│       ├── customers.csv                  ← Customer accounts
│       ├── inventory.csv                  ← Inventory levels
│       └── pricing.csv                    ← Pricing data (if separate)
│
├── 01_Kickoff/                            ← Kickoff meeting notes, SOW
├── 02_Project_Plan/                       ← Timeline, milestones
├── 03_Data/                               ← Raw data from client (price lists, product files, etc.)
├── 04_Training/                           ← Training materials, recordings
├── 05_Go_Live/                            ← Go-live checklist, launch plan
├── 06_Notes/                              ← Meeting notes, decisions log
│
└── 07_Data_Scraping/                      ← Web scraping framework
    ├── README.md                          ← Scraping rules, image guidelines, Python templates
    ├── Scripts/                           ← Download/processing scripts
    └── Images/                            ← Downloaded product images
```

---

## SuperCat Configuration

Fill in as you discover the client's structure:

### Trade Names & Collections

```
TradeNameCode:  {CODE}

CollectionCodes:
  {COL1} → {Collection 1 Name}
  {COL2} → {Collection 2 Name}
  ...
```

### Groups & Categories

| Group | Code | Categories |
|-------|------|------------|
| Main | MAIN | LIGHT, ACCESSORIES, DRVRS, CNTRL |
| {Collection 1} | {COL1} | {sub1}, {sub2}, ... |
| {Collection 2} | {COL2} | {sub3}, {sub4}, ... |

### CategoryCodes Pattern

| Product Type | Pattern | Notes |
|-------------|---------|-------|
| Core lighting | `LIGHT,{sub}` | Visible in catalog browse |
| Accessories | `{sub},ACCESSORIES` | Hidden, shown via RelatedItems |
| Drivers | `MAIN,DRVRS` | Hidden, shared across collections |
| Controllers | `MAIN,CNTRL` | Hidden, shared across collections |

### Hideable Rules

| Rule | Hideable | Notes |
|------|----------|-------|
| ONE representative per product family | `N` | The "hero" variant customers browse to |
| All other sizes/finishes/variants | `Y` | Accessible via RelatedItems |
| ALL accessories | `Y` | |
| ALL drivers | `Y` | |
| ALL controllers | `Y` | |

---

## Process Overview

```
1. ADMIN CONSOLE SETUP       Define tradenames, collections, categories, price levels
       ↓
2. DATA GATHERING             Get product files, price lists, images from client
       ↓
3. SCRAPING (if needed)       Scrape manufacturer website for specs + images
       ↓
4. BUILD products.csv         Populate all columns, merge pricing, assign images
       ↓
5. BUILD stories.csv          One story per product (max 500 chars)
       ↓
6. DATA QUALITY AUDIT         Run validation scripts (see 07_Data_Scraping/README.md)
       ↓
7. IMAGE AUDIT                Verify all images exist, correct order, product photo first
       ↓
8. UPLOAD IMAGES              Upload to Admin Console image library
       ↓
9. IMPORT products.csv        Then stories, customers, inventory, pricing
       ↓
10. IPAD REVIEW               Check hero images, hideable, pricing, categories
       ↓
11. FIX & RE-IMPORT           Fix issues found in review, re-import, re-review
       ↓
12. GO LIVE                   Client approval, launch
```

**Budget for 2-3 review/fix cycles.** No import is perfect on the first try.

---

## Key Documents

| What you need | Where |
|---------------|-------|
| Common pitfalls and lessons learned | `LESSONS_LEARNED.md` |
| Admin console setup + import reference | `00_Import_Files/README.md` |
| Step-by-step import process | `00_Import_Files/IMPORT_PROCESS.md` |
| Scraping framework + image rules | `07_Data_Scraping/README.md` |
| Import-ready CSV files | `00_Import_Files/Ready_For_Import/` |
| Client source data | `03_Data/` |

---

## Resources

- **SuperCat Import Guide:** https://supercatsolutions.com/knowledgebase/import-product-file
- **SuperCat Pricing Guide:** https://supercatsolutions.com/knowledgebase/catalog-pricing
- **Tradenames & Collections:** https://supercatsolutions.com/knowledgebase/tradenames-collections
- **Groups & Categories:** https://supercatsolutions.com/knowledgebase/groups-categories
