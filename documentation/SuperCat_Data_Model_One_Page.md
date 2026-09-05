# SuperCat Data Model: One-Page Reference

**Quick reference for understanding how your data connects in SuperCat**

---

## The 4 Core Data Files & How They Connect

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                          YOUR ORGANIZATION                                  │
│                         (e.g., "Kuzco Lighting")                           │
│                                                                             │
└──────────────────┬──────────────────────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┬──────────────────┬─────────────────┐
        │          │          │                  │                 │
        ▼          ▼          ▼                  ▼                 ▼
   ┌────────┐ ┌─────────┐ ┌──────────┐    ┌──────────┐    ┌──────────┐
   │PRODUCTS│ │CUSTOMERS│ │TERRITORIES│    │  USERS   │    │  ORDERS  │
   └────────┘ └─────────┘ └──────────┘    └──────────┘    └──────────┘
        │          │            │               │               │
        │          │            └───────┬───────┘               │
        │          │                    │                       │
        │          └────────────────────┼───────────────────────┘
        │                               │
        └───────────────────────────────┘
```

---

## 🔗 The 3 Critical Relationships

### 1️⃣ **CUSTOMER → ORDER**
```
┌─────────────────────┐           ┌──────────────────────┐
│   CUSTOMER FILE     │           │     ORDER FILE       │
│                     │           │                      │
│  Code: "ACME-001" ──┼──────────▶│  Customer: "ACME-001"│
│  Name: "Acme Co"    │  Links    │  Order #: 12345      │
│  Territory: "LSL"   │    by     │  Total: $5,432       │
│  Price: "GOLD"      │   Code    │  Date: 2/1/26        │
└─────────────────────┘           └──────────────────────┘
```
**Key Point:** Order's `customer_num` MUST match Customer's `code`

---

### 2️⃣ **TERRITORY → CUSTOMER → USER**
```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  TERRITORY   │         │   CUSTOMER   │         │  USER (Rep)  │
│              │         │              │         │              │
│ Code: "LSL"  │◀────────│ Territory:   │         │ Territories: │
│ Name: "LSL"  │ Assigned│   "LSL"      │ Filters │  ["LSL"]     │
│              │    to   │              │  what   │              │
└──────────────┘         │ Code: "ACME" │  user   │ Name: "John" │
                         └──────────────┘  sees   └──────────────┘
```
**Key Point:** User can only see customers in their assigned territories

---

### 3️⃣ **PRODUCT → ORDER LINE ITEMS**
```
┌───────────────────┐        ┌────────────────────────┐
│   PRODUCT FILE    │        │   ORDER LINE ITEMS     │
│                   │        │                        │
│ Item: "ABC-123" ──┼───────▶│ [                      │
│ Desc: "Widget"    │ Links  │   {                    │
│ Price: $99        │   by   │     "item": "ABC-123", │
│                   │  Item  │     "qty": 5,          │
└───────────────────┘ Number │     "price": $99       │
                             │   }                    │
                             │ ]                      │
                             └────────────────────────┘
```
**Key Point:** Order line items reference product item numbers

---

## 🚨 Top 3 Issues & Quick Fixes

### ❌ Issue #1: "Rep can't see customers in Sales Portal"
**Cause:** Territory codes don't match  
**Fix:** Ensure user's territory codes match customer's territory codes exactly

```
User Territories:     ["TRINITY"]
Customer Territory:   "SUNBURST"  ← MISMATCH!

Fix: Add "SUNBURST" to user's territories
```

---

### ❌ Issue #2: "Order shows wrong/missing customer"
**Cause:** Customer code changed or deleted  
**Fix:** Customer codes must remain stable

```
Order Customer Code:  "ACME-001"
Customer File Code:   "ACME-1"    ← CHANGED!

Fix: Keep customer codes consistent or update orders
```

---

### ❌ Issue #3: "Sales Portal shows ALL customers (not filtered)"
**Cause:** Territories table is empty  
**Fix:** Populate territories table from customer data

```
Territories Table:    0 rows      ← EMPTY!
Customer Territories: 53 unique codes exist

Fix: Run SQL migration to create territory records
```

---

## ✅ Onboarding Quick Checklist

**Before Go-Live:**

- [ ] **Products uploaded** with unique item numbers
- [ ] **Customers uploaded** with unique codes and territory assignments
- [ ] **Territories created** (if using Sales Portal)
- [ ] **Users created** with correct territory assignments
- [ ] **Test order placed** and exported successfully
- [ ] **Rep can see** only their assigned customers
- [ ] **Customer codes** match between customer file and test orders

---

## 🔑 Field Mapping Cheat Sheet

| What You Need | Customer File | Order File | Must Match? |
|---------------|---------------|------------|-------------|
| Link customer to order | `code` | `customer_num` | ✅ YES |
| Filter by territory | `territory_codes` | (inherited) | ℹ️ Info |
| Apply pricing | `default_price_code` | `price_level` | ℹ️ Info |

| What You Need | Product File | Order Line Item | Must Match? |
|---------------|--------------|-----------------|-------------|
| Link product to order | `item_number` | `item` | ✅ YES |
| Show price | `prices` | `price` | ℹ️ Snapshot |

| What You Need | Territory Table | User Record | Must Match? |
|---------------|-----------------|-------------|-------------|
| Filter customers | `code` | `territory_codes` | ✅ YES |

---

## 📞 Quick Support

**Issue?** Check these 3 things first:
1. Do the codes match? (customer code, item number, territory code)
2. Are territories configured? (required for Sales Portal)
3. Is the user assigned to the right territories?

**Still stuck?** Contact support@supercat.com with:
- Specific customer code or order number
- User email address
- Screenshot of the issue

---

**Print this page and keep it handy during onboarding!**

*Version 1.0 | February 2026 | SuperCat Customer Success*
