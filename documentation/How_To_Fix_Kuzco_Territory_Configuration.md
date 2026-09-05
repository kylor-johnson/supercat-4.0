# How To Fix Kuzco (KLL) Territory Configuration for Sales Portal

**Date:** February 2, 2026  
**Status:** 🔴 CRITICAL - Sales Portal broken due to missing territory configuration  
**Estimated Time to Fix:** 30-60 minutes

---

## The Problem

**Sales Portal requires the `territories` table to be populated, but Kuzco has 0 territories configured.**

### Current State:
- ✅ **Customers have territory codes** - 53 unique territories across 3,000+ customers
- ✅ **Users have territory codes** - 77 users with territory assignments
- ❌ **`territories` table is empty** - 0 rows for organization_id = 166
- ❌ **Sales Portal can't work** - it reads from `territories` table to filter data

### Why This Happened:
We sold them Sales Portal in October 2025 but never migrated their existing territory data from the `customers.territory_codes` field into the `territories` table. This is a standard data migration step we skipped.

---

## The Solution: 3 Options

### Option 1: SQL Migration Script (FASTEST - 30 minutes)

**Best for:** Quick fix to get Sales Portal working immediately

**Steps:**

1. **Extract unique territory codes from existing customer data**
2. **Insert into `territories` table**
3. **Validate and test**

**SQL Script:**

```sql
-- Step 1: Preview what will be created
SELECT DISTINCT
  jsonb_array_elements_text(territory_codes::jsonb) as code,
  COUNT(*) as customer_count
FROM customers 
WHERE organization_id = 166 
  AND territory_codes IS NOT NULL 
  AND territory_codes::text != '[]'
GROUP BY jsonb_array_elements_text(territory_codes::jsonb)
ORDER BY customer_count DESC;

-- Step 2: Insert territories (run this in production)
INSERT INTO territories (organization_id, code, name, created_at, updated_at)
SELECT DISTINCT 
  166 as organization_id,
  jsonb_array_elements_text(territory_codes::jsonb) as code,
  jsonb_array_elements_text(territory_codes::jsonb) as name,  -- Use code as name initially
  NOW() as created_at,
  NOW() as updated_at
FROM customers 
WHERE organization_id = 166 
  AND territory_codes IS NOT NULL 
  AND territory_codes::text != '[]'
ON CONFLICT DO NOTHING;  -- In case of duplicates

-- Step 3: Validate
SELECT * FROM territories WHERE organization_id = 166 ORDER BY code;
```

**Expected Result:** ~53 territories created

**Pros:**
- ✅ Fast (5 minutes to run)
- ✅ Uses existing data (no manual entry)
- ✅ Sales Portal works immediately

**Cons:**
- ⚠️ Territory names = territory codes (not descriptive)
- ⚠️ May include legacy/unused territories
- ⚠️ Doesn't clean up data inconsistencies

---

### Option 2: Admin Console Manual Entry (CLEANEST - 2-4 hours)

**Best for:** Proper cleanup and documentation of territory structure

**Steps:**

1. **Get territory list from Kevin/Katy**
   - Ask: "Which territories are currently active for your 75 reps?"
   - Ask: "What's the proper name for each territory code?"
   - Example: `NUVO` → "Nuvo Lighting Agency - Northeast"

2. **Clean up legacy territories**
   - Remove: LEGACYSALES, Kuzco (lowercase), Sunburst (if not active)
   - Consolidate: Any duplicate/similar codes

3. **Enter in Admin Console**
   - Navigate to: Admin Console > Organization Settings > Territories (or similar)
   - Add each territory with proper code and descriptive name
   - **Note:** If no UI exists, escalate to engineering to build it

4. **Validate**
   - Test Sales Portal with a rep user
   - Confirm they only see their territory's customers

**Pros:**
- ✅ Clean, documented territory structure
- ✅ Removes legacy/unused territories
- ✅ Proper descriptive names
- ✅ Kevin/Katy involved (they learn the system)

**Cons:**
- ⏱️ Time-consuming (2-4 hours)
- ⚠️ Requires Kevin/Katy availability
- ⚠️ May reveal Admin Console UI doesn't exist for territories

---

### Option 3: Hybrid Approach (RECOMMENDED - 1-2 hours)

**Best for:** Balance of speed and quality

**Steps:**

1. **Run SQL migration to get Sales Portal working NOW** (Option 1)
   - This unblocks them immediately
   - Resolves Help Scout ticket #13878

2. **Schedule cleanup session with Kevin/Katy next week** (Option 2)
   - Review all 53 territories
   - Identify which are active vs legacy
   - Update names to be descriptive
   - Remove unused territories

3. **Document the final territory structure**
   - Create a reference doc: "Kuzco Territory Structure"
   - Include: Code, Name, Rep(s) assigned, Customer count
   - Store in their account notes

**Timeline:**
- **Today:** Run SQL script (30 min)
- **This week:** Test with Kevin/validate it works (30 min)
- **Next week:** Cleanup session with Kevin/Katy (1-2 hours)

**Pros:**
- ✅ Immediate fix (Sales Portal works today)
- ✅ Proper cleanup happens (but doesn't block them)
- ✅ Kevin/Katy involved in cleanup (they learn)
- ✅ Documented for future reference

**Cons:**
- ⚠️ Two-step process (not one-and-done)

---

## Current Territory Data (From Database)

### Top 30 Territories by Customer Count:

| Territory Code | Customer Count | Notes |
|---------------|---------------|-------|
| KUZCO | 446 | Largest - likely house accounts or default |
| NUVO | 154 | Nuvo Lighting Agency |
| GRILLO INC | 150 | Grillo Inc |
| LES | 140 | |
| STONEHOUSE | 129 | |
| PORTER | 128 | |
| BCLIGHTS | 109 | BC Lights |
| TRINITY | 108 | Trinity (11 users assigned) |
| FLETCHER | 98 | |
| SANDD2 | 97 | |
| HARRY | 96 | |
| BRETZING | 95 | |
| ELA | 95 | |
| GANNONSALES | 91 | Gannon Sales |
| MARTIN | 83 | |
| SLA | 79 | |
| ERIC | 66 | |
| MIDATLANTIC | 65 | Mid-Atlantic |
| FLL | 57 | |
| AZ | 49 | Arizona |
| RICHARD | 45 | |
| ELITELIGHT | 42 | Elite Lighting |
| CRL | 37 | |
| THESGROUP | 36 | |
| LSM | 34 | |
| **LEGACYSALES** | 30 | ⚠️ Legacy - from Help Scout ticket #12797 |
| DOEREN | 29 | |
| **SUNBURST** | 20 | ⚠️ This is the one that broke during training |
| Kuzco | 20 | ⚠️ Lowercase - likely duplicate of KUZCO |
| LSL | 18 | |

**Total Unique Territories:** 53

### User Territory Assignments:

- **734 users** have NO territories assigned (empty array)
- **77 users** have territories assigned
- **Top user territories:** TRINITY (11 users), BCLIGHTS (7), NUVO (6), GRILLO INC (6)

---

## Validation Steps After Fix

### 1. Database Validation

```sql
-- Confirm territories were created
SELECT COUNT(*) FROM territories WHERE organization_id = 166;
-- Expected: ~53

-- Show all territories
SELECT code, name FROM territories 
WHERE organization_id = 166 
ORDER BY code;
```

### 2. Sales Portal Testing

**Test with a real rep user:**

1. Find a user with territory assigned:
   ```sql
   SELECT u.id, u.email, ou.territory_codes 
   FROM users u 
   JOIN org_users ou ON u.id = ou.user_id 
   WHERE ou.organization_id = 166 
     AND ou.territory_codes::text != '[]' 
   LIMIT 5;
   ```

2. Log in as that user (or have Kevin test)

3. Navigate to Sales Portal

4. **Verify:**
   - ✅ Portal dashboard loads (no error)
   - ✅ User only sees customers in their territory
   - ✅ Invoice/order data displays correctly
   - ✅ No "Sunburst showing all customers" issue

### 3. Edge Case Testing

**Test user with NO territory assigned:**
- Should see: No customers (or appropriate message)
- Should NOT see: All customers

**Test user with multiple territories:**
- Should see: Customers from ALL their assigned territories
- Example: User with `["LSL", "RICHARD"]` sees customers from both

---

## Known Issues to Watch For

### Issue 1: Territory Code Case Sensitivity

**Problem:** Database has both "KUZCO" (446 customers) and "Kuzco" (20 customers)

**Fix:**
```sql
-- Standardize to uppercase
UPDATE customers 
SET territory_codes = '["KUZCO"]'::jsonb
WHERE organization_id = 166 
  AND territory_codes::text = '["Kuzco"]';
```

### Issue 2: LEGACYSALES Territory

**From Help Scout Ticket #12797 (July 2025):**
> "At some point a while back the 'TerritoryCode' field on the customer file changed from 'DALE' to 'LEGACYSALES' for Wasatch Lighting. But Libby's territory code is still set to 'DALE'."

**Fix:**
- Determine if LEGACYSALES is still active
- If yes: Update Libby's user record to LEGACYSALES
- If no: Migrate customers from LEGACYSALES to correct territory

### Issue 3: Sunburst Territory

**From Fathom Call (Jan 30):**
> "Live test in 'ZSuperCat' group FAILED - showed all customers instead of restricting to 'Sunburst' territory"

**Root Cause:** `territories` table was empty, so Sales Portal couldn't filter

**After Fix:** Sunburst territory will exist in `territories` table, filtering will work

---

## Communication Plan

### To Kevin/Katy (After Fix):

**Email Template:**

> **Subject:** Sales Portal Territory Configuration - FIXED
> 
> Hi Kevin and Katy,
> 
> Good news - I've fixed the Sales Portal territory configuration issue we discovered during training.
> 
> **What I did:**
> - Migrated your 53 territory codes from eCat into the Sales Portal system
> - Validated that the portal now correctly filters customers by territory
> - Tested with [specific user] to confirm it's working
> 
> **What this means:**
> - Sales Portal is now functional for your reps
> - Reps will only see customers in their assigned territories
> - The "Sunburst showing all customers" issue is resolved
> 
> **Next steps:**
> - Please test with 2-3 of your reps this week
> - Let me know if you see any issues
> - Next week, let's schedule 30 minutes to review the territory list and clean up any legacy codes
> 
> **To test:**
> 1. Log in as a rep user (not admin)
> 2. Go to Sales Portal
> 3. Confirm you only see customers in your territory
> 4. Check that invoices/orders display correctly
> 
> Let me know if you have any questions!
> 
> [Your name]

### To Internal Team:

**Slack/Email:**

> **Kuzco (KLL) - Sales Portal territory issue RESOLVED**
> 
> **Problem:** Sales Portal sold in Oct 2025, but `territories` table never populated (0 rows). Portal couldn't work without it.
> 
> **Fix:** Ran SQL migration to extract 53 unique territory codes from customer data and populate `territories` table.
> 
> **Status:** ✅ Fixed - Sales Portal now functional
> 
> **Follow-up:** Scheduling cleanup session with client next week to review territory list and remove legacy codes.
> 
> **Lesson learned:** Add "Populate territories table" to Sales Portal implementation checklist.

---

## Prevention: Add to Implementation Checklist

**Sales Portal Implementation Checklist:**

- [ ] **Territory Configuration**
  - [ ] Verify customer data has territory codes
  - [ ] Extract unique territory codes
  - [ ] Populate `territories` table
  - [ ] Validate territory count matches expectation
  - [ ] Test Sales Portal with rep user (territory filtering works)
  - [ ] Document territory structure with client
  - [ ] Train admin on territory management

**Add this step BEFORE go-live, not after.**

---

## SQL Reference Scripts

### Check Current State:

```sql
-- How many territories exist?
SELECT COUNT(*) FROM territories WHERE organization_id = 166;

-- What territories exist in customer data?
SELECT 
  jsonb_array_elements_text(territory_codes::jsonb) as territory_code,
  COUNT(*) as customer_count
FROM customers 
WHERE organization_id = 166 
  AND territory_codes IS NOT NULL 
  AND territory_codes::text != '[]'
GROUP BY jsonb_array_elements_text(territory_codes::jsonb)
ORDER BY customer_count DESC;

-- Which users have territories assigned?
SELECT 
  u.email,
  ou.territory_codes
FROM users u
JOIN org_users ou ON u.id = ou.user_id
WHERE ou.organization_id = 166
  AND ou.territory_codes::text != '[]'
ORDER BY u.email;
```

### Migration Script:

```sql
-- PRODUCTION: Run this to fix Kuzco's Sales Portal
BEGIN;

-- Insert territories from customer data
INSERT INTO territories (organization_id, code, name, created_at, updated_at)
SELECT DISTINCT 
  166 as organization_id,
  jsonb_array_elements_text(territory_codes::jsonb) as code,
  jsonb_array_elements_text(territory_codes::jsonb) as name,
  NOW() as created_at,
  NOW() as updated_at
FROM customers 
WHERE organization_id = 166 
  AND territory_codes IS NOT NULL 
  AND territory_codes::text != '[]'
ON CONFLICT DO NOTHING;

-- Validate
SELECT COUNT(*) as territories_created FROM territories WHERE organization_id = 166;

-- Show what was created
SELECT code, name FROM territories WHERE organization_id = 166 ORDER BY code;

COMMIT;
```

### Cleanup Scripts (Run Later with Kevin):

```sql
-- Remove duplicate lowercase "Kuzco" (keep uppercase "KUZCO")
UPDATE customers 
SET territory_codes = '["KUZCO"]'::jsonb
WHERE organization_id = 166 
  AND territory_codes::text = '["Kuzco"]';

-- Update territory name to be descriptive (example)
UPDATE territories 
SET name = 'Nuvo Lighting Agency - Northeast',
    updated_at = NOW()
WHERE organization_id = 166 
  AND code = 'NUVO';

-- Delete unused territory (example - confirm with client first!)
DELETE FROM territories 
WHERE organization_id = 166 
  AND code = 'LEGACYSALES';
```

---

## Bottom Line

**The Fix:** Run the SQL migration script (5 minutes)

**The Test:** Have Kevin test Sales Portal with a rep user (15 minutes)

**The Cleanup:** Schedule session with Kevin/Katy next week to review and clean up territory list (1-2 hours)

**Total Time to Unblock:** 30 minutes

**This should have been done in October 2025 during implementation.**

---

**Next Actions:**
1. ✅ Get approval to run SQL migration in production
2. ✅ Run migration script
3. ✅ Validate in database
4. ✅ Test with Kevin
5. ✅ Update Help Scout ticket #13878 as resolved
6. ✅ Email Kevin/Katy with good news
7. ✅ Schedule cleanup session for next week
8. ✅ Update Sales Portal implementation checklist
