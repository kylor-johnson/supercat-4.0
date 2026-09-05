# eCat Data Model: Understanding Your Data Files

## The Big Picture: From Your Systems to eCat

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│                         YOUR SOURCE DATA                                            │
│                    (Where your data lives today)                                    │
│                                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │              │    │              │    │              │    │              │      │
│  │     ERP      │    │     CRM      │    │ Spreadsheets │    │   Warehouse  │      │
│  │   System     │    │   System     │    │   (Excel)    │    │   System     │      │
│  │              │    │              │    │              │    │              │      │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                    │                    │           │
│         │                    │                    │                    │           │
│         └────────────────────┴────────────────────┴────────────────────┘           │
│                                       │                                            │
│                                       │                                            │
│                              Export to CSV files                                   │
│                                       │                                            │
│                                       ▼                                            │
│                                                                                     │
│                      SUPERCAT DATA TEMPLATES                                        │
│                    (Simple CSV files you upload)                                    │
│                                                                                     │
│                                                                                     │
│                              CORE FILES                                             │
│         ┌──────────────┬──────────────┬──────────────┬──────────────┐             │
│         │              │              │              │              │             │
│         ▼              ▼              ▼              ▼              ▼             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐                       │
│  │          │   │          │   │          │   │          │                       │
│  │ products │   │customers │   │inventory │   │ stories  │                       │
│  │   .csv   │   │   .csv   │   │   .csv   │   │   .csv   │                       │
│  │          │   │          │   │          │   │          │                       │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘                       │
│                                                                                     │
│                            OPTIONAL FILES                                           │
│         ┌──────────────┬──────────────┬──────────────┬──────────────┐             │
│         │              │              │              │              │             │
│         ▼              ▼              ▼              ▼              ▼             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐       │
│  │ order_   │   │ invoice_ │   │ options  │   │ option_  │   │ (more)   │       │
│  │ data     │   │ data     │   │   .csv   │   │ groups   │   │          │       │
│  │   .csv   │   │   .csv   │   │          │   │   .csv   │   │          │       │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘       │
│                                                                                     │
│                                       │                                            │
│                              Upload to Admin Console                               │
│                                       │                                            │
│                                       ▼                                            │
│                                                                                     │
│                         ┌─────────────────────────┐                                │
│                         │                         │                                │
│                         │    ADMIN CONSOLE        │                                │
│                         │  (Validates & Connects) │                                │
│                         │                         │                                │
│                         └───────────┬─────────────┘                                │
│                                     │                                              │
│                                     │ Sync                                         │
│                                     ▼                                              │
│                         ┌─────────────────────────┐                                │
│                         │                         │                                │
│                         │      eCat iPad          │                                │
│                         │   (Field Sales App)     │                                │
│                         │                         │                                │
│                         └─────────────────────────┘                                │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## How the Files Connect: The Simple Version

**Think of it like this:** Your product catalog is the center of everything. The other files just add information to it.

```
                                 ┌─────────────────────┐
                                 │                     │
                                 │   PRODUCTS.CSV      │
                                 │   "The Catalog"     │
                                 │                     │
                                 │   What you sell     │
                                 │                     │
                                 └──────────┬──────────┘
                                            │
                                            │ Product SKU connects to...
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
        ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
        │                   │   │                   │   │                   │
        │  INVENTORY.CSV    │   │  STORIES.CSV      │   │  ORDER_DATA.CSV   │
        │  "Stock Levels"   │   │  "Product Stories"│   │  "Sales History"  │
        │                   │   │                   │   │                   │
        │  How many you     │   │  Extended product │   │  What was sold    │
        │  have in stock    │   │  descriptions     │   │  to whom          │
        │                   │   │                   │   │                   │
        └───────────────────┘   └───────────────────┘   └───────────────────┘


                              ┌─────────────────────┐
                              │                     │
                              │  CUSTOMERS.CSV      │
                              │  "Your Accounts"    │
                              │                     │
                              │  Who can buy        │
                              │  & their pricing    │
                              │                     │
                              └─────────────────────┘
```

---

## Understanding Each File: What Goes Where

### 1. PRODUCTS.CSV - Your Product Catalog

**What it is:** The complete list of everything you sell

**Where it comes from:** Your ERP, product database, or master spreadsheet

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  REQUIRED:                           OPTIONAL:                          │
│  • Product SKU (BaseItemCode)        • Product variations (OptionSets) │
│  • Product Name (LongDesc)           • Related products                │
│  • Brand (TradeNameCode)             • Custom fields                   │
│  • Category (CategoryCodes)          • Promo pricing                   │
│  • Price (NetPrice)                  • Marketing copy                  │
│  • Images (ImageFileName)                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Important Distinction:**
- **LongDesc** (in products.csv) = The product name/title shown in the catalog grid
- **ProductStory** (in stories.csv) = Extended marketing description shown in detail view
- These are two different fields in two different files!

**Example Row:**
```
BaseItemCode: H0019-11559
LongDesc: ABBERLEY 69'' HIGH 1-LIGHT FLOOR LAMP
TradeNameCode: ELK (Elk Lighting)
CategoryCodes: FLAMP (Floor Lamps)
NetPrice: 150.00
ImageFileName: H0019-11559.jpg
```

**Where to manage in Admin Console:**
- Products > Products (view product configuration)
- Products > Trade Names & Collections (organize by brand/line)
- Products > Groups & Categories (organize by type)

> **Note:** Individual product data cannot be edited directly in the Admin Console. Product changes must be made via CSV import.

---

### 2. CUSTOMERS.CSV - Your Customer Accounts

**What it is:** List of who can buy from you and where they want products shipped

**Where it comes from:** Your CRM, accounting system, or customer database

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  REQUIRED:                           IMPORTANT LINKS:                   │
│  • Customer Number (BillToCode)      • Territory Code → Assigns to rep │
│  • Customer Name                     • Price Code → Sets their pricing │
│  • Bill-To Address                                                     │
│  • Ship-To Address(es)               OPTIONAL:                          │
│                                      • Credit limit, quotas             │
│                                      • Contact info                     │
│                                      • Account status                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Example Rows:**
```
Row 1: BillToCode=188, BillToName="APPLE GOLD", TerritoryCodes=13, ShipToCode=1
       [Main account + first shipping location]

Row 2: BillToCode=188, ShipToCode=2
       [Same customer, second shipping location]

Row 3: BillToCode=188, ShipToCode=3
       [Same customer, third shipping location]
```

**The Key Connection:**
- **TerritoryCodes** = Which sales rep(s) see this customer
- **DefaultPriceCode** = What pricing level this customer gets

**Where to manage in Admin Console:**
- Customers > Customers (manage accounts)

> **Note:** Customer records can be edited directly in the Admin Console, or updated via CSV import.

---

### 3. INVENTORY.CSV - Stock Levels

**What it is:** How many of each product you have in stock

**Where it comes from:** Your warehouse system, ERP, or inventory spreadsheet

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  REQUIRED:                           OPTIONAL:                          │
│  • Product SKU (BaseItemCode)        • On order quantity                │
│    → MUST match products.csv         • Next receipt date                │
│  • Qty Available ⭐                   • Showroom quantity                │
│                                      • Warehouse location               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Example Row:**
```
BaseItemCode: H0019-11559
QtyAvailable: 5    ← What reps can sell
QtyOnHand: 10      ← Physical inventory
QtyReserved: 5     ← Already allocated to orders
```

**How it connects:**
```
products.csv:    BaseItemCode = "H0019-11559"
                              │
                              ▼
inventory.csv:   BaseItemCode = "H0019-11559", QtyAvailable = 5
                              │
                              ▼
Result:          Product shows "5 Available" in eCat
```

**Where to manage in Admin Console:**
- Tools > Import Data > Inventory (upload only, no manual editing)

> **Custom Inventory Fields:** You can configure custom inventory fields to display additional data such as Qty On Hand, Next Ship Date, or Next Available Qty. These custom fields are populated via your inventory file import.

---

### 4. STORIES.CSV - Product Stories (Extended Descriptions)

**What it is:** Extended product information like specs, care instructions, and marketing copy

**Where it comes from:** Your product database, marketing materials, or content management system

**Important Clarification:**
- **stories.csv** contains the **ProductStory** field - extended "product romance" descriptions
- This is **different** from **LongDesc** in products.csv, which is just the product name/title
- Think of it as: LongDesc = "What it's called" vs ProductStory = "The full story about it"

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  REQUIRED:                           USE CASES:                         │
│  • Product SKU (BaseItemCode)        • Technical specifications        │
│    → MUST match products.csv         • Care & handling instructions    │
│  • Product Story (long text)         • "Product romance" copy          │
│                                      • Assembly instructions           │
│                                      • Warranty information             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Example Row:**
```
BaseItemCode: 1000
productstory: "Use this charming wine storage chest to add interest to 
               a kitchen or other entertainment area. Featuring hand 
               painted details of ancient Chinese court life and 
               exquisitely antiqued solid brass hardware..."
```

**How it connects:**
```
products.csv:    BaseItemCode = "1000"
                 LongDesc = "Wine Storage Chest"  ← Short name shown in grid
                              │
                              ▼
stories.csv:     BaseItemCode = "1000"
                 productstory = [500+ character detailed description]
                              │
                              ▼
Result:          Grid shows "Wine Storage Chest"
                 Detail view shows the full product story
```

**Where to manage in Admin Console:**
- Tools > Import Data > Product Stories

---

## Optional Files

### 5. ORDER_DATA.CSV - Portal Orders / Sales History

**What it is:** Imported order-history data used for Sales Portal-style "Orders" reporting (history/backlog/amounts). This is **separate from** orders submitted via the iPad app.

**Where it comes from:** Your ERP, accounting system, or integration feed (uploaded/FTP'd as a data import file)

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  KEY FIELDS:                         LINKS TO:                          │
│  • OrderNumber (header key)          • Customer (via CustomerBillToNumber│
│  • OrderDate                           → corresponds to BillToCode)     │
│  • ShipDate                          • Products (via ItemNumber or      │
│  • Status                              optional eCatItemNumber)         │
│  • QuantityOrdered                                                      │
│  • QuantityInvoiced                  This file flows INTO eCat          │
│  • UnitPrice                         for reporting purposes             │
│  • TotalAmount                                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Example Row:**
```
OrderNumber: O214764
CustomerBillToNumber: 12902  ← Links to customers.csv (BillToCode)
ItemNumber: 21445B           ← Links to products.csv
OrderDate: 2025-11-15
Status: Shipped
UnitPrice: 1542.50
QuantityOrdered: 1
TotalAmount: 1542.50
```

**Where to manage in Admin Console:**
- Tools > Import Data > Portal Orders (upload order_data.csv)
- Orders > Orders (view history/reporting)
- Orders > Reports (analytics)

> **Important:** This file is for **imported order history** from your ERP. It is different from the orders.csv that eCat *exports* when reps submit orders from the iPad.

---

### 6. INVOICE_DATA.CSV - Portal Invoices / Invoicing Details

**What it is:** Imported invoice-history data used for Invoices reporting (what was billed/shipped). This is **separate from** iPad-submitted orders.

**Where it comes from:** Your ERP or accounting system (uploaded/FTP'd into Supercat as an import file)

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  KEY FIELDS:                         LINKS TO:                          │
│  • InvoiceNumber (header key)        • Orders (via OrderNumber)        │
│  • OrderNumber                       • Customer (via CustomerBillToNumber│
│  • InvoiceDate                         → corresponds to BillToCode)     │
│  • QuantityInvoiced                  • Products (via ItemNumber or      │
│  • UnitPrice                           optional eCatItemNumber)         │
│  • NetAmount                                                            │
│                                      Shows what was actually           │
│                                      shipped and billed                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Example Row:**
```
InvoiceNumber: I275267
OrderNumber: O233051         ← Links to order_data.csv
CustomerBillToNumber: 12902  ← Links to customers.csv
InvoiceDate: 2022-01-05
ItemNumber: F3018/3AGB       ← Links to products.csv
QuantityInvoiced: 1
NetAmount: 245.0
```

**How it connects:**
```
order_data.csv:    OrderNumber = "O233051"
                              │
                              ▼
invoice_data.csv:  OrderNumber = "O233051"
                   Shows what was actually invoiced/shipped
```

**Where to manage in Admin Console:**
- Tools > Import Data > Portal Invoices (upload invoice_data.csv)
- Orders > Invoices (view reporting)

> **Important Nuance:** Supercat can also *export* a file named invoices.csv from the Invoices screen, but that export is a summary (Invoice #/date/customer/order/amount) - it is **not** the same as this line-item import feed.

---

### 7. OPTIONS.CSV + OPTION_GROUPS.CSV - Product Variations

**What it is:** Colors, finishes, sizes, fabrics - any way a product can be customized

This feature uses **two files**:
- **options.csv** = Master list of individual selectable values (e.g., Black, White, Gold)
- **option_groups.csv** = Groups that contain collections of options (e.g., FIN = Finishes)

**Where it comes from:** Your product configuration system, master options list (ERP/PIM), or managed directly in Admin Console

**OPTIONS.CSV - Individual Option Values:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  REQUIRED:                           OPTIONAL:                          │
│  • Code (e.g., "100")                • PriceAddend (flat price adjust) │
│  • Name (e.g., "Black")              • PriceFactor (multiplier)        │
│                                      • Description                      │
│                                      • ImageName                        │
│                                      • SortValue                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**OPTION_GROUPS.CSV - Option Groupings:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  REQUIRED:                           OPTIONAL:                          │
│  • Code (e.g., "FIN")                • PriceAddend                      │
│  • Name (e.g., "Finishes")           • PriceFactor                      │
│  • Options (comma-separated codes)   • GradeJumpRiserCount              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**How it works:**

```
Step 1: Define option values (options.csv)
        ┌────────────────────────────┐
        │ Code   Name                │
        │ 100    Black               │
        │ 101    White               │
        │ 102    Gold                │
        └────────────────────────────┘

Step 2: Group them (option_groups.csv)
        ┌────────────────────────────────────┐
        │ Code   Name       Options          │
        │ FIN    Finishes   100,101,102      │
        └────────────────────────────────────┘

Step 3: Assign to products (products.csv)
        ┌────────────────────────────────────────────┐
        │ BaseItemCode   OptionSet1   OptionSet1Required │
        │ H0019-11559    FIN          true               │
        └────────────────────────────────────────────┘
        (Can assign up to 5 option sets: OptionSet1..OptionSet5)

Step 4: Pricing behavior
        • Non-matrixed option sets: Apply price addends/factors 
          from the option group or individual option
        • Matrixed option sets: Pricing comes from matrix_options.csv 
          (combination pricing for complex configurations)
```

**Where to manage in Admin Console:**
- Products > Options (manage Option Groups + individual Options)

---

## The Three Critical Connections

These are the "magic links" that make everything work together:

### Connection #1: Product SKU Links Everything

**The BaseItemCode (Product SKU) is your master key**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  products.csv                                                               │
│  ┌─────────────────────────────────────────┐                               │
│  │ BaseItemCode = "H0019-11559"            │                               │
│  │ LongDesc     = "Floor Lamp"             │                               │
│  │ NetPrice     = $150                     │                               │
│  │ OptionSet1   = "FIN"                    │                               │
│  └─────────────────────┬───────────────────┘                               │
│                        │                                                    │
│          ┌─────────────┼─────────────┬─────────────┐                       │
│          │             │             │             │                       │
│          ▼             ▼             ▼             ▼                       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐               │
│  │inventory  │  │stories    │  │order_data │  │options    │               │
│  │.csv       │  │.csv       │  │.csv       │  │.csv       │               │
│  │           │  │           │  │           │  │           │               │
│  │BaseItem   │  │BaseItem   │  │ItemNumber │  │(via       │               │
│  │Code =     │  │Code =     │  │= "H0019-  │  │OptionSet) │               │
│  │"H0019-    │  │"H0019-    │  │11559"     │  │           │               │
│  │11559"     │  │11559"     │  │           │  │           │               │
│  │           │  │           │  │           │  │           │               │
│  │QtyAvail   │  │product    │  │qty = 1    │  │100=Black  │               │
│  │= 5        │  │story =    │  │           │  │101=White  │               │
│  │           │  │[text]     │  │           │  │102=Gold   │               │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Result: When a rep views product H0019-11559, they see:
        • Name & price (from products.csv)
        • Stock level (from inventory.csv)  
        • Product story (from stories.csv)
        • Available options (from options.csv via OptionSet)
        All linked by that one SKU.
```

---

### Connection #2: Territory Code Assigns Customers to Reps

```
customers.csv:        TerritoryCodes = "13"
                      Customer: APPLE GOLD
                                │
                                │ Matches
                                ▼
Admin Console:        User: John Smith
                      TerritoryCode = "13"
```

**Result:** John Smith only sees customers assigned to territory 13 on his iPad.

---

### Connection #3: Price Code Sets Customer Pricing

```
customers.csv:        DefaultPriceCode = "4"
                      Customer: GRUPO CAOR
                                │
                                │ References
                                ▼
Admin Console:        Price Level "4" = Distributor
                      Calculation: 40% of NetPrice
                                │
                                │ Applied to
                                ▼
products.csv:         NetPrice = $1,542.50
                                │
                                ▼
                      Customer sees: $617.00
```

**Result:** Customer GRUPO CAOR automatically sees distributor pricing (40% off) on all products.

---

## What You Configure in Admin Console (Not in Files)

Some things you set up directly in the Admin Console, not in CSV files:

### 1. Users & Territories
**Location:** Users > Users

- Create user accounts
- Assign territory codes (links to customers.csv)
- Set permissions (what they can do)

### 2. User Groups
**Location:** Users > User Groups

- Control which products users see (by brand/category)
- Control which customers users see (all vs. territory-only)
- Set pricing permissions

### 3. Price Levels
**Location:** Products > Price Levels

- Define price codes (referenced in customers.csv)
- Set calculations (e.g., "Code 4 = 40% of NetPrice")

**Example:**
```
Code: 0  → Net (100% of NetPrice)
Code: 4  → Distributor (40% of NetPrice)
Code: R  → Retail (200% of NetPrice)
```

### 4. Taxonomy Display Names
**Location:** Products > Trade Names & Collections, Products > Groups & Categories

- Turn codes into friendly names
- Example: "ELK" → displays as "Elk Lighting"

---

## How It All Flows Together

### The Simple 4-Step Process

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  STEP 1: You Upload Files                                               │
│  ────────────────────────────────────────────────────────────────────   │
│                                                                         │
│  Admin Console > Tools > Import Data                                    │
│  • products.csv, customers.csv, inventory.csv, stories.csv              │
│  • options.csv, option_groups.csv                                       │
│  • order_data.csv, invoice_data.csv (for Portal reporting)              │
│  • Product images                                                       │
│                                                                         │
│                                ↓                                        │
│                                                                         │
│  STEP 2: System Connects Everything                                     │
│  ────────────────────────────────────────────────────────────────────   │
│                                                                         │
│  • Links inventory to products (via BaseItemCode)                       │
│  • Links customers to reps (via TerritoryCodes)                         │
│  • Links pricing to customers (via DefaultPriceCode)                    │
│  • Links options to products (via OptionSet1..5)                        │
│  • Validates all data                                                   │
│                                                                         │
│                                ↓                                        │
│                                                                         │
│  STEP 3: Rep Syncs iPad                                                 │
│  ────────────────────────────────────────────────────────────────────   │
│                                                                         │
│  Each rep gets a personalized package:                                  │
│  • Only their products (based on User Group)                            │
│  • Only their customers (based on Territory)                            │
│  • Correct pricing for each customer                                    │
│  • Current inventory levels                                             │
│  • Works offline                                                        │
│                                                                         │
│                                ↓                                        │
│                                                                         │
│  STEP 4: Orders Flow Back                                               │
│  ────────────────────────────────────────────────────────────────────   │
│                                                                         │
│  Rep creates order → Syncs to server → Exports to your ERP              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Summary: The Three Things to Remember

### 1. Product SKU (BaseItemCode) Connects Everything
Your product SKU is the master key that links products to inventory, stories, options, and orders.

### 2. Two Critical Codes Control Access
- **Territory Code** = Which customers a rep sees
- **Price Code** = What pricing a customer gets

### 3. Simple 4-Step Flow
Upload files → System connects them → Reps sync → Orders flow back

---

**Document Version:** 2.0  
**Created:** February 11, 2026  
**Updated:** February 15, 2026  
**Purpose:** Admin training primer - Understanding data file relationships
