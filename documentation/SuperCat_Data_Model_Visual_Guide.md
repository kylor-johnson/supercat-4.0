# SuperCat Data Model: Visual Guide

**Purpose:** Client-facing reference for understanding how data flows through SuperCat  
**Audience:** Onboarding clients, CSMs, Support team  
**Last Updated:** February 5, 2026

---

## 🏢 The Big Picture: How Your Data Connects

```
┌─────────────────────────────────────────────────────────────────┐
│                     YOUR ORGANIZATION                            │
│                    (e.g., "Kuzco Lighting")                      │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├─────────────────────────────────────────────────────┐
             │                                                     │
             ▼                                                     ▼
    ┌────────────────┐                                   ┌─────────────────┐
    │   PRODUCTS     │                                   │   TERRITORIES   │
    │                │                                   │                 │
    │ • Item Numbers │                                   │ • Territory Code│
    │ • Descriptions │                                   │ • Territory Name│
    │ • Prices       │                                   │                 │
    │ • Images       │                                   │ Examples:       │
    │                │                                   │ • TRINITY       │
    │ 8,000 items    │                                   │ • SUNBURST      │
    └────────────────┘                                   │ • BCLIGHTS      │
                                                         └────────┬────────┘
                                                                  │
             ┌────────────────────────────────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                        CUSTOMERS                             │
    │                                                              │
    │  Each customer has:                                          │
    │  • Customer Code (e.g., "ACME-001")                         │
    │  • Company Name                                              │
    │  • Billing Address                                           │
    │  • Territory Assignment ← Links to Territories               │
    │  • Default Price Level                                       │
    │                                                              │
    │  2,698 customers                                             │
    └──────────────────────┬───────────────────────────────────────┘
                           │
                           │ Referenced by "Customer Code"
                           │
                           ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                         ORDERS                               │
    │                                                              │
    │  Each order includes:                                        │
    │  • Order Number                                              │
    │  • Customer Code ← Links to Customer                         │
    │  • Rep Name (who placed it)                                  │
    │  • Order Date                                                │
    │  • Line Items (products ordered)                             │
    │  • Total Amount                                              │
    │                                                              │
    │  856 orders                                                  │
    └─────────────────────────────────────────────────────────────┘
                           │
                           │ Contains Product Item Numbers
                           │
                           ▼
                  [Links back to PRODUCTS]


    ┌─────────────────────────────────────────────────────────────┐
    │                          USERS                               │
    │                                                              │
    │  Each user has:                                              │
    │  • Email & Name                                              │
    │  • User Type (Rep, Admin, Customer Portal, etc.)            │
    │  • Territory Access ← Links to Territories                   │
    │  • Customer Assignment (for portal users)                    │
    │                                                              │
    │  837 users                                                   │
    └─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Key Relationships Explained

### 1. **Customer → Order Relationship**

**The Connection:** `orders.customer_num` = `customers.code`

```
CUSTOMER FILE:                    ORDER FILE:
┌──────────────────┐             ┌──────────────────┐
│ Code: "ACME-001" │────────────▶│ Customer: "ACME-001"
│ Name: "Acme Co"  │             │ Order #: 12345   │
│ Territory: "LSL" │             │ Total: $5,432    │
│ Price: "GOLD"    │             │ Date: 2/1/26     │
└──────────────────┘             └──────────────────┘
```

**What this means:**
- Every order must reference a valid customer code
- If a customer code changes in your system, orders may break
- Customer billing info flows into orders automatically

---

### 2. **Territory → Customer → User Relationship**

**The Connection:** Territory codes link customers to sales reps

```
TERRITORY:                CUSTOMER:                 USER (Rep):
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Code: "LSL"  │◀────────│ Territory:   │         │ Territories: │
│ Name: "LSL"  │         │   "LSL"      │         │  ["LSL",     │
└──────────────┘         │              │         │   "TRINITY"] │
                         │ Code: "ACME" │         │              │
                         └──────────────┘         │ Name: "John" │
                                                  └──────────────┘
```

**What this means:**
- Reps can only see customers in their assigned territories
- **Sales Portal requires territories to be configured**
- If territories are missing, reps see ALL customers or NO customers

---

### 3. **Product → Order Relationship**

**The Connection:** Orders contain product item numbers in JSON format

```
PRODUCT FILE:                 ORDER LINE ITEMS:
┌───────────────────┐        ┌────────────────────────┐
│ Item: "ABC-123"   │◀───────│ [                      │
│ Description: "..." │        │   {                    │
│ Price GOLD: $99   │        │     "item": "ABC-123", │
│ Price PLAT: $89   │        │     "qty": 5,          │
└───────────────────┘        │     "price": $99       │
                             │   }                    │
                             │ ]                      │
                             └────────────────────────┘
```

**What this means:**
- Order line items reference product item numbers
- If a product is deleted, historical orders still show it
- Pricing is captured at time of order

---

## 🚨 Common Issues & How Data Relates

### Issue: "Rep can't see their customers in Sales Portal"

**Root Cause:** Territory mismatch

```
❌ BROKEN:
User Territory: ["TRINITY"]
Customer Territory: "SUNBURST"
Result: Customer hidden from user

✅ FIXED:
User Territory: ["TRINITY", "SUNBURST"]
Customer Territory: "SUNBURST"
Result: Customer visible to user
```

---

### Issue: "Order shows wrong customer name"

**Root Cause:** Customer code mismatch

```
❌ BROKEN:
Order Customer Code: "ACME-001"
Customer File Code: "ACME-1" (changed)
Result: Order can't find customer

✅ FIXED:
Order Customer Code: "ACME-001"
Customer File Code: "ACME-001"
Result: Order displays correctly
```

---

### Issue: "Products not showing for user"

**Root Cause:** Collection/Trade Name restrictions

```
❌ BROKEN:
User Collections: ["MODERN"]
Product Collection: "TRADITIONAL"
Result: Product hidden from user

✅ FIXED:
User Collections: ["MODERN", "TRADITIONAL"]
Product Collection: "TRADITIONAL"
Result: Product visible to user
```

---

## 📊 Data Flow: From Import to Order

```
1. IMPORT FILES                    2. SUPERCAT PROCESSES
┌─────────────────┐               ┌──────────────────┐
│ Products.csv    │──────────────▶│ products table   │
│ Customers.csv   │──────────────▶│ customers table  │
│ Inventory.csv   │──────────────▶│ inventories table│
└─────────────────┘               └──────────────────┘
                                           │
                                           │
                                           ▼
3. USERS ACCESS DATA              4. ORDERS CREATED
┌─────────────────┐               ┌──────────────────┐
│ Rep logs into   │               │ Order references:│
│ iPad/Portal     │               │ • Customer Code  │
│                 │               │ • Product Items  │
│ Sees filtered:  │               │ • Price Level    │
│ • Customers     │──────────────▶│ • Territory      │
│ • Products      │               │                  │
│ • Pricing       │               │ Saved to orders  │
└─────────────────┘               └──────────────────┘
                                           │
                                           │
                                           ▼
5. ORDER EXPORT                   6. BACK TO YOUR SYSTEM
┌─────────────────┐               ┌──────────────────┐
│ Order exported  │               │ Order appears in:│
│ via:            │──────────────▶│ • ERP            │
│ • Email         │               │ • Order System   │
│ • API           │               │ • QuickBooks     │
│ • FTP           │               │                  │
└─────────────────┘               └──────────────────┘
```

---

## 🔑 Critical Fields That Must Match

### Between Customer File and Orders:

| Customer File Field | Order Field      | Must Match? |
|---------------------|------------------|-------------|
| `code`              | `customer_num`   | ✅ YES      |
| `territory_codes`   | (inherited)      | ℹ️ Info     |
| `default_price_code`| `price_level`    | ℹ️ Info     |

### Between Products and Orders:

| Product File Field | Order Line Item  | Must Match? |
|--------------------|------------------|-------------|
| `item_number`      | `item`           | ✅ YES      |
| `prices`           | `price`          | ℹ️ Snapshot |

### Between Territories and Users:

| Territory Field | User Field         | Must Match? |
|-----------------|-------------------|-------------|
| `code`          | `territory_codes` | ✅ YES      |

---

## 📋 Onboarding Checklist: Data Setup

Use this checklist to ensure all relationships are properly configured:

### ✅ Step 1: Upload Core Data
- [ ] Products file uploaded (with item numbers, prices, images)
- [ ] Customers file uploaded (with codes, names, territories)
- [ ] Inventory file uploaded (optional, for stock levels)

### ✅ Step 2: Configure Territories (if using Sales Portal)
- [ ] Extract unique territory codes from customer file
- [ ] Create territories in SuperCat
- [ ] Verify territory codes match exactly (case-sensitive!)

### ✅ Step 3: Set Up Users
- [ ] Create user accounts (or import user file)
- [ ] Assign user types (Rep, Admin, Customer Portal, etc.)
- [ ] Assign territories to reps (must match customer territories)
- [ ] Assign collections/trade names (if applicable)

### ✅ Step 4: Test Relationships
- [ ] Rep logs in and sees correct customers (territory filter works)
- [ ] Rep can see correct products (collection filter works)
- [ ] Rep can place test order (customer code resolves)
- [ ] Order exports successfully (all fields map correctly)

### ✅ Step 5: Validate Data Integrity
- [ ] No orphaned orders (all customer codes exist)
- [ ] No missing territories (all customer territories defined)
- [ ] No duplicate customer codes
- [ ] All product item numbers are unique

---

## 🆘 Troubleshooting Guide

### "I can't see any customers in Sales Portal"

**Check:**
1. Does your user have territories assigned?
2. Do those territories exist in the Territories table?
3. Do customers have matching territory codes?

**SQL to verify:**
```sql
-- Check user territories
SELECT territory_codes FROM org_users WHERE user_id = [YOUR_USER_ID];

-- Check if territories exist
SELECT code FROM territories WHERE organization_id = [YOUR_ORG_ID];

-- Check customer territories
SELECT DISTINCT territory_codes FROM customers WHERE organization_id = [YOUR_ORG_ID];
```

---

### "Orders are showing wrong customer information"

**Check:**
1. Does the order's `customer_num` match a customer's `code`?
2. Has the customer code changed since the order was placed?
3. Was the customer deleted?

**SQL to verify:**
```sql
-- Find orders with missing customers
SELECT o.order_number, o.customer_num
FROM orders o
LEFT JOIN customers c ON o.customer_num = c.code 
  AND o.organization_id = c.organization_id
WHERE c.id IS NULL
  AND o.organization_id = [YOUR_ORG_ID];
```

---

### "Products not appearing for certain users"

**Check:**
1. User Type permissions (which collections/trade names are allowed)
2. Product collection codes match user's authorized collections
3. Product is not marked as deleted

**SQL to verify:**
```sql
-- Check user's authorized collections
SELECT user_type_id FROM org_users WHERE user_id = [YOUR_USER_ID];

-- Check which collections that user type can see
SELECT * FROM collections_user_types WHERE user_type_id = [USER_TYPE_ID];
```

---

## 📞 Need Help?

If you're experiencing data relationship issues:

1. **Check this guide first** - Most issues are territory or code mismatches
2. **Run the SQL queries** - Verify the data relationships
3. **Contact Support** - Provide specific examples (customer codes, order numbers, user emails)

**Support Email:** support@supercat.com  
**Documentation:** https://help.supercat.com

---

**Version:** 1.0  
**Created:** February 5, 2026  
**Maintained By:** SuperCat Customer Success Team
