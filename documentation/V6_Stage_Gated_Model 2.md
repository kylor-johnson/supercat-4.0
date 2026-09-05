# V6

# 7-Stage Onboarding Readiness Framework

## Overview

This framework tracks client progression through 7 sequential stages, from initial account setup through order-ready status. Each stage has specific validation checkpoints that determine readiness (🟢 GREEN), warnings (🟡 YELLOW), blockers (🔴 RED), or not applicable (⚪ N/A).

---

## Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

### Checklist

- [ ]  Company name filled in
- [ ]  At least 1 admin user exists (excluding internal test users: Kylor_Johnson, brentsanders, cwiebe)
- [ ]  Settings initialized with defaults

### Pass Criteria

- **🔴 RED (BLOCKER):** Any item above unchecked
- **🟢 GREEN (READY):** All items checked

### How to Validate

- Run: `get_organization_info`
- Run: `get_org_users` (verify `is_admin: true` exists)

---

## Stage 2: Catalog Setup

**Goal:** Products imported and browsable by users

### Checklist

- [ ]  At least 10 products imported
- [ ]  At least 10 products have images
- [ ]  At least 1 category configured
- [ ]  At least 1 collection exists
- [ ]  Products updated within last 30 days

### Pass Criteria

- **🔴 RED (BLOCKER):** Less than 10 products imported
- **🟡 YELLOW (WARNING):** 10-100 products OR no updates in 60+ days OR less than 10 products with images
- **🟢 GREEN (READY):** 100+ products AND updated within last 30 days

### How to Validate

- Run: `get_data_summary` (check `products.count`)
- Run: `get_categories`
- Run: `get_collections`
- Check: `last_product_update` date

---

## Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

### Checklist

- [ ]  Price levels configured
- [ ]  At least 2 price levels configured (recommended)
- [ ]  Price levels have descriptive names, not generic defaults like "Price Level 1" (recommended)
- [ ]  Price level codes assigned (recommended)

### Pass Criteria

- **🔴 RED (BLOCKER):** No price levels configured
- **🟡 YELLOW (WARNING):** Only 1 price level configured OR generic names like "Price Level 1" OR missing/duplicate codes
- **🟢 GREEN (READY):** 2+ price levels with descriptive names (e.g., "Dealer Net", "Wholesale", "Retail") AND unique codes assigned

### How to Validate

- Run: `get_price_levels`
- Sample products to verify pricing data completeness

---

## Stage 4: Option Configuration

**Goal:** If options enabled, CPQ/configurators are functional

### Check if Stage Applies

- [ ]  Run `get_options` - does it return any options?
    - **YES** → Continue with checklist below
    - **NO** → Mark stage as **⚪ N/A** and skip to Stage 5

### Checklist (If Options Enabled)

- [ ]  At least 1 option configured

### Pass Criteria

- **⚪ N/A:** Options disabled - skip this stage
- **🔴 RED (BLOCKER):** Options enabled but none configured
- **🟡 YELLOW (WARNING):** Less than 5 options configured
- **🟢 GREEN (READY):** 5+ options configured

### How to Validate

- Run: `get_options`
- Check: `require_valid_options_to_submit_orders` setting

---

## Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

### Check Assignment Model

- [ ]  Run `get_user_territories` - are territories configured?
    - **YES** → Use Territory Model checklist
    - **NO** → Use Direct Assignment checklist

### Checklist (Both Models)

- [ ]  At least 10 customers imported
- [ ]  At least 2 users configured
- [ ]  Multiple user types exist
- [ ]  Customers updated within last 30 days

### Additional Checklist: Territory Model

- [ ]  At least 1 territory exists
- [ ]  Users assigned to territories (via `territory_codes`)
- [ ]  Customers assigned to territories or users within territories

### Additional Checklist: Direct Assignment Model

- [ ]  Customers directly assigned to users
- [ ]  No territory structure required

### Pass Criteria

- **🔴 RED (BLOCKER):** Less than 10 customers OR no users configured
- **🟡 YELLOW (WARNING):** 10-100 customers OR no updates in 30+ days
- **🟢 GREEN (READY):** 100+ customers AND updated within last 30 days AND proper assignments configured

### How to Validate

- Run: `get_data_summary` (check `customers.count`)
- Run: `get_org_users`
- Run: `get_user_territories` (to determine assignment model)
- Check: `last_customer_update` date

---

## Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

### Check if Inventory Tracking Applies

- [ ]  Is inventory tracking enabled?
    - **YES** → Include inventory validation checks
    - **NO** → Skip inventory checks (mark **⚪ N/A**)

### Checklist (Always Required)

- [ ]  No critical import errors in last 30 days
- [ ]  Smart stacks configured OR feature disabled

### Additional Checklist: If Inventory Enabled

- [ ]  Inventory data exists (`inventories.count > 0`)
- [ ]  Inventory updated within last 7 days

### Pass Criteria

- **🔴 RED (BLOCKER):** Inventory enabled but no data OR critical import errors present
- **🟡 YELLOW (WARNING):** Stale inventory (7+ days old) OR minor import warnings
- **🟢 GREEN (READY):** Fresh data (updated within 7 days) AND no import errors

### How to Validate

- Run: `get_data_summary` (check `inventories.count`)
- Run: `get_import_events` (review last 30 days)
- Run: `get_smart_stacks`
- Check: `last_inventory_update` date

---

## Stage 7: Order-Ready

**Goal:** System can receive, process, and fulfill orders end-to-end

### Critical Blockers (Must Pass)

- [ ]  1+ user types exist (more than just Default User Group - e.g., Sales Rep or Customer)
- [ ]  Mobile site configured (at least 1 enabled)
- [ ]  Report formats configured (minimum 3 required)
- [ ]  Test order processed (at least 1 order exists)

### Recommended (Should Pass)

- [ ]  Order notification email configured
- [ ]  Export type configured (if ERP integration needed)

### Post-Launch Health Check

- [ ]  Orders placed within last 30 days (after launch)

### Pass Criteria

- **🔴 RED (BLOCKER):** Any critical blocker unchecked
- **🟡 YELLOW (WARNING):** All critical blockers pass but recommended items missing OR no recent orders
- **🟢 GREEN (READY):** All criteria pass AND recent order activity

### How to Validate

- Run: `get_mobile_sites` (verify `count >= 1` AND `enabled: true`)
- Run: `get_reports_config` (verify `count >= 3`)
- Run: `get_orders` (verify `count >= 1`)
- Check: `order_email_recipient` is not empty
- Check: `export_type` is not empty (if ERP integration required)
- Check: `orders_last_30_days > 0`

---

## Quick Reference: Status Colors

| Status | Meaning | Action Required |
| --- | --- | --- |
| 🔴 RED | Launch Blocker | Stop - must resolve before proceeding |
| 🟡 YELLOW | Warning | Can launch but requires CS follow-up |
| 🟢 GREEN | Ready | Proceed to next stage |
| ⚪ N/A | Not Applicable | Feature disabled - skip validation |

---

## Quick Reference: Critical Launch Blockers

**Cannot launch without these:**

1. **Price levels configured** (Stage 3)
2. **Customers imported** (Stage 5)
3. **Mobile site enabled** (Stage 7)
4. **Report formats configured** (Stage 7)
5. **Test order processed** (Stage 7)

## Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

### ✅ Checklist

- [ ]  Company name filled in
- [ ]  At least 1 admin user exists (not including the usernames Kylor_Johnson, brentsanders, or cwiebe)
- [ ]  Settings initialized with defaults

### 🎯 Pass Criteria

**RED (BLOCKER):** Any item above unchecked
**GREEN (READY):** All items checked

### 🔍 How to Check

- Run: `get_organization_info`
- Run: `get_org_users` (look for is_admin: true)

---

## Stage 2: Catalog Setup

**Goal:** Products imported and browsable by users

### ✅ Checklist

- [ ]  At least 10 products imported
- [ ]  At least 50% of products have images
- [ ]  At least 1 category configured
- [ ]  At least 1 collection exists
- [ ]  Products updated within last 30 days

### 🎯 Pass Criteria

**RED (BLOCKER):** Less than 10 products
**YELLOW (WARNING):** 10-100 products OR no update in 60+ days
**GREEN (READY):** 100+ products AND recent update within last 30 days

### 🔍 How to Check

- Run: `get_data_summary` (products.count)
- Run: `get_categories`
- Run: `get_collections`
- Check: `last_product_update` date

---

## Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

### ✅ Checklist

- [ ]  Price levels configured
- [ ]  At least 2 price levels configured (recommended)
- [ ]  Price levels named, not generic e.g. “Price Level 1” (recommended)
- [ ]  Price level codes assigned (recommended)

### 🎯 Pass Criteria

**RED (BLOCKER):** No price levels configured
**YELLOW (WARNING):** Only 1 price level configured OR Generic names like "Price Level 1" (functional but unprofessional) OR Missing codes or duplicate codes

**GREEN (READY):** 2+ price levels with complete pricing data AND Descriptive names like "Dealer Net", "Wholesale", "Retail” AND All price levels have unique codes

### 🔍 How to Check

- Run: `get_price_levels`
- Sample products to verify pricing data

---

## Stage 4: Option Configuration

**Goal:** If options enabled, CPQ/configurators are functional

### 🔀 First: Check if This Stage Applies

- [ ]  Run `get_options` - does it return any options?
    - **YES** → Continue with checklist below
    - **NO** → Mark stage as **N/A** and skip to Stage 5

### ✅ Checklist (If Options Enabled)

- [ ]  At least 1 option configured

### 🎯 Pass Criteria

**N/A:** Options disabled - skip this stage
**RED (BLOCKER):** Options enabled but none configured
**YELLOW (WARNING):** Less than 5 options 
**GREEN (READY):** 5+ options

### 🔍 How to Check

- Run: `get_options`
- Check: `require_valid_options_to_submit_orders` setting

---

## Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

### 🔀 First: Check Assignment Model

- [ ]  Run `get_user_territories` - are territories configured?
    - **YES** → Use Territory Model checklist
    - **NO** → Use Direct Assignment checklist

### ✅ Checklist (Both Models)

- [ ]  At least 10 customers imported
- [ ]  At least 2 users configured
- [ ]  Multiple user types exist
- [ ]  Customers updated within last 30 days

### ✅ Additional: Territory Model

- [ ]  At least 1 territory exists
- [ ]  Users assigned to territories (via territory_codes)
- [ ]  Customers assigned to territories or users within territories

### ✅ Additional: Direct Assignment Model

- [ ]  Customers directly assigned to users
- [ ]  No territory structure required

### 🎯 Pass Criteria

**RED (BLOCKER):** Less than 10 customers OR no users configured
**YELLOW (WARNING):** 10-100 customers OR no update in 30+ days
**GREEN (READY):** 100+ customers AND recent update AND proper assignments

### 🔍 How to Check

- Run: `get_data_summary` (customers.count)
- Run: `get_org_users`
- Run: `get_user_territories` (to determine model)
- Check: `last_customer_update` date

---

## Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

### 🔀 First: Check Inventory Tracking

- [ ]  Is inventory tracking enabled?
    - **YES** → Include inventory checks
    - **NO** → Skip inventory checks (mark N/A)

### ✅ Checklist (Always Required)

- [ ]  No critical import errors in last 30 days
- [ ]  Smart stacks configured OR feature disabled

### ✅ Checklist (If Inventory Enabled)

- [ ]  Inventory data exists (inventories.count > 0)
- [ ]  Inventory updated within last 7 days

### 🎯 Pass Criteria

**RED (BLOCKER):** Inventory enabled but no data OR critical import errors
**YELLOW (WARNING):** Stale inventory (7+ days old) OR minor import warnings
**GREEN (READY):** Fresh data AND no import errors

### 🔍 How to Check

- Run: `get_data_summary` (inventories.count)
- Run: `get_import_events` (last 30 days)
- Run: `get_smart_stacks`
- Check: `last_inventory_update` date

---

## Stage 7: Order-Ready

**Goal:** System can receive, process, and fulfill orders end-to-end

### ✅ Critical Blockers (Must Pass)

- [ ]  1+ user types exist (more than just Default User Group e.g. Sales Rep or Customer)
- [ ]  **Mobile site configured** (at least 1 enabled)
- [ ]  **Report formats configured** (minimum 3 required)
- [ ]  **Test order processed** (at least 1 order exists)

### ✅ Recommended (Should Pass)

- [ ]  Order notification email configured
- [ ]  Export type configured (if ERP integration needed)

### ✅ Post-Launch Health Check

- [ ]  Orders placed within last 30 days (after launch)

### 🎯 Pass Criteria

**RED (BLOCKER):** Any critical blocker unchecked
**YELLOW (WARNING):** All blockers pass but recommended items missing OR no recent orders
**GREEN (READY):** All criteria pass + recent order activity

### 🔍 How to Check

- Run: `get_mobile_sites` (count >= 1 AND enabled: true)
- Run: `get_reports_config` (count >= 3)
- Run: `get_orders` (count >= 1)
- Check: `order_email_recipient` not empty
- Check: `export_type` not empty (if needed)
- Check: `orders_last_30_days` > 0

---

## Quick Reference: Status Colors

| Color | Meaning | What to Do |
| --- | --- | --- |
| 🔴 RED | Launch Blocker | Stop - must fix before proceeding |
| 🟡 YELLOW | Warning | Can launch but needs CS follow-up |
| 🟢 GREEN | Ready | Proceed to next stage |
| ⚪ N/A | Not Applicable | Feature disabled - skip this check |

---

## Quick Reference: Critical Blockers

**Cannot launch without these:**

1. Price levels configured (Stage 3)
2. Customers imported (Stage 5)
3. Mobile site enabled (Stage 7)
4. Report formats configured (Stage 7)
5. Test order processed (Stage 7)

```markdown
Develop a standardized "Stage 7 Launch Checklist" workflow that CS team triggers when Stages 1-6 are complete. This should include:
1. Mobile site template deployment
2. Standard report format library installation
3. Guided test order walkthrough with client
```