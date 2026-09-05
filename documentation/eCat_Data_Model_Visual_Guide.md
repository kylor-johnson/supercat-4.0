# eCat Data Model: Understanding Your Data Files

## The Big Picture: From Your Systems to eCat

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│                         YOUR SOURCE DATA                                            │
│                    (Where your data lives today)                                    │
│                                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │              │    │              │    │              │    │              │    │
│  │     ERP      │    │     CRM      │    │ Spreadsheets │    │   Warehouse  │    │
│  │   System     │    │   System     │    │   (Excel)    │    │   System     │    │
│  │              │    │              │    │              │    │              │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    │
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
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐                       │
│  │          │   │          │   │          │   │          │                       │
│  │  orders  │   │ invoices │   │ options  │   │ (more)   │                       │
│  │   .csv   │   │   .csv   │   │   .csv   │   │          │                       │
│  │          │   │          │   │          │   │          │                       │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘                       │
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
        │  INVENTORY.CSV    │   │  STORIES.CSV      │   │  ORDERS.CSV       │
        │  "Stock Levels"   │   │  "Long Descriptions"│ │  "Sales History"  │
        │                   │   │                   │   │                   │
        │  How many you     │   │  Product details, │   │  What was sold    │
        │  have in stock    │   │  specs, care info │   │  to whom          │
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
- Products > Products (edit individual items)
- Products > Trade Names & Collections (organize by brand/line)
- Products > Groups & Categories (organize by type)

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
- Users > Customers (manage accounts)

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
products.csv:   BaseItemCode = "H0019-11559"
                ↓
inventory.csv:  BaseItemCode = "H0019-11559", QtyAvailable = 5
                ↓
Result:         Product shows "5 Available" in eCat
```

**Where to manage in Admin Console:**
- Tools > Import Data > Inventory (upload only, no manual editing)

---

### 4. STORIES.CSV - Long Product Descriptions

**What it is:** Extended product information like specs, care instructions, and marketing copy

**Where it comes from:** Your product database, marketing materials, or content management system

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
products.csv:   BaseItemCode = "1000"
                LongDesc = "Wine Storage Chest"
                ↓
stories.csv:    BaseItemCode = "1000"
                productstory = [500+ character detailed description]
                ↓
Result:         Product shows short name in grid, full story in detail view
```

**Where to manage in Admin Console:**
- Tools > Import Data > Product Stories

---

## Optional Files

### 5. ORDERS.CSV - Sales History

**What it is:** Record of what was sold, to whom, and when

**Where it comes from:** Orders created in eCat iPad export to this format

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  EACH ORDER CONTAINS:                LINKS TO:                          │
│  • Order number                      • Customer (via BillToCode)       │
│  • Order date                        • Products (via BaseItemCode)     │
│  • Customer info                                                       │
│  • Products ordered                  This file flows FROM eCat          │
│  • Quantities & prices               back to your ERP/system            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Example Rows:**
```
ordernumber: O214764
customerbilltonumber: 12902  ← Links to customers.csv
itemnumber: 21445B           ← Links to products.csv
unitprice: 1542.50
quantityordered: 1
```

**Where to manage in Admin Console:**
- Orders > Orders (view history)
- Orders > Reports (analytics)

---

### 6. INVOICES.CSV - Invoicing Details

**What it is:** Invoice records showing what was billed and shipped

**Where it comes from:** Your ERP or accounting system

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  REQUIRED:                           LINKS TO:                          │
│  • Invoice number                    • Orders (via ordernumber)        │
│  • Order number                      • Customer (via BillToCode)       │
│  • Invoice date                      • Products (via BaseItemCode)     │
│  • Quantities invoiced                                                 │
│  • Net amount                        Shows what was actually           │
│                                      shipped and billed                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Example Row:**
```
invoicenumber: I275267
ordernumber: O233051      ← Links to orders.csv
invoicedate: 2022-01-05
itemnumber: F3018/3AGB    ← Links to products.csv
quantityinvoiced: 1
netamount: 245.0
```

**How it connects:**
```
orders.csv:    ordernumber = "O233051"
               ↓
invoices.csv:  ordernumber = "O233051"
               Shows what was actually invoiced/shipped
```

**Where to manage in Admin Console:**
- Orders > Invoices (if enabled)

---

### 7. OPTIONS.CSV - Product Variations

**What it is:** Colors, finishes, sizes, fabrics - any way a product can be customized

**Where it comes from:** Your product configuration system or master options list

**Key Information:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  REQUIRED:                           OPTIONAL:                          │
│  • Option Code (e.g., "100")         • Price adjustment                │
│  • Option Name (e.g., "Black")       • Image file                      │
│                                      • Description                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**How it works:**
```
Step 1: Define options
        Code: 100 = "Black"
        Code: 101 = "White"
        Code: 102 = "Gold"

Step 2: Group them (in Admin Console)
        Group "FIN" = Finishes
        Contains: 100, 101, 102

Step 3: Assign to products
        products.csv: OptionSet1 = "FIN"
        
Step 4: User selects when ordering
        Picks "Black" → Price adjusts automatically
```

**Where to manage in Admin Console:**
- Products > Options (manage options and groups)

---

## The Three Critical Connections

These are the "magic links" that make everything work together:

### Connection #1: Product SKU Links Everything

**The BaseItemCode (Product SKU) is your master key**

```
products.csv:    BaseItemCode = "H0019-11559"
                 LongDesc = "Floor Lamp"
                 NetPrice = $150
                           │
                           ├──────────────────────┬──────────────────────┐
                           │                      │                      │
                           ▼                      ▼                      ▼
inventory.csv:   BaseItemCode = "H0019-11559"    orders.csv:           options.csv:
                 QtyAvailable = 5                itemnumber = "H0019"   OptionSet1
                                                 qty = 1                references
```

**Result:** When a rep views product H0019-11559, they see the name, price, stock level, and available options - all linked by that one SKU.

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
│  • products.csv, customers.csv, inventory.csv, options.csv              │
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
Your product SKU is the master key that links products to inventory, options, and orders.

### 2. Two Critical Codes Control Access
- **Territory Code** = Which customers a rep sees
- **Price Code** = What pricing a customer gets

### 3. Simple 4-Step Flow
Upload files → System connects them → Reps sync → Orders flow back

---

**Document Version:** 2.0 (Simplified)  
**Created:** February 11, 2026  
**Purpose:** Admin training primer - Understanding data file relationships
