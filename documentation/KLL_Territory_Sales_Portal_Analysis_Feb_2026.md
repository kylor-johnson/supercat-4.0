# KLL Territory & Sales Portal Analysis

**Date:** February 3, 2026  
**Organization:** Kuzco Lighting Inc. (shortname: `kll`)  
**Database Query Time:** Live data from production database

---

## Executive Summary

### Territory Assignment Status

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Users** | 849 | 100% |
| **Users WITHOUT Territory** | 768 | **90.5%** |
| **Users WITH Territory** | 81 | 9.5% |

### Sales Portal Access Status

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Users** | 849 | 100% |
| **Sales Portal ENABLED** | 79 | 9.3% |
| **Sales Portal DISABLED** | 740 | 87.2% |
| **Sales Portal NULL (not set)** | 30 | 3.5% |

---

## Critical Finding: Sales Portal Users Without Territories

**9 users have Sales Portal access enabled but NO territory defined.**

This is a critical configuration issue because:
- Sales Portal requires territories to filter customer data
- Without territories, these users either see ALL customers or NO customers
- This was the root cause of the "Sunburst showing all customers" issue from Jan 30 training

### Users with Sales Portal Enabled but NO Territory:

| Email | First Name | Last Name | User Type | Territory Codes |
|-------|------------|-----------|-----------|-----------------|
| briancarlisle@rocketmail.com | Brian | Carlisle | US Reps | [] |
| elite-lights@elite-lights.com | Rick | Taylor | US Reps | [] |
| julie@elite-lights.com | Julie - Elite Lights | Jenkins | US Reps | [] |
| kjael@supercatsolutions.com | Kjael | Skaalerud | US Reps | [] |
| shoproycecollection@gmail.com | Tanya | Royce | US Reps | [] |
| steve@supercatsolutions.com | Steve | Thrasher | US Reps | [] |
| chuck+kuzco@supercatsolutions.com | Chuck | Wiebe | US Reps | [] |
| brent+mcp-admin@supercatsolutions.com | MCP | MCP | z-SuperCat | NULL |
| chuck+b@supercatsolutions.com | Chuck | Wiebe | z-SuperCat | [] |

**Note:** The last 3 users are SuperCat internal accounts (z-SuperCat user type).

---

## Users Without Sales Portal Access

**770 users do NOT have Sales Portal access enabled** (either disabled or NULL).

This includes:
- 740 users with `enable_sales_portal: false`
- 30 users with `enable_sales_portal: NULL` (not set)

These users are primarily:
- Premier Designer tier customers
- Trade tier customers (Gold, Platinum, Diamond)
- CAD Reps
- Admin users

Sample of users WITHOUT Sales Portal (first 50 shown in query results):
- Most are designer/trade customers who use eCat for ordering but don't need Sales Portal
- User types: Premier Designer, Trade Platinum, Trade Gold, Trade Diamond, CAD Reps, Admin

---

## Breakdown by User Type

### User Types with Sales Portal ENABLED:

Based on the 9 users identified:
- **US Reps:** 6 users (should have territories assigned)
- **z-SuperCat:** 3 users (internal SuperCat accounts)

### User Types with Sales Portal DISABLED:

Most common user types (from sample):
- Premier Designer
- Trade Platinum
- Trade Gold
- Trade Diamond
- CAD Reps
- Admin

---

## Territory Distribution (Users WITH Territories)

**81 users have territories assigned.**

Top territories by user count (from documentation):
- TRINITY: 11 users
- BCLIGHTS: 7 users
- NUVO: 6 users
- GRILLO INC: 6 users

---

## Recommendations

### Immediate Actions Required:

1. **Assign territories to the 6 US Rep users** who have Sales Portal enabled but no territory:
   - briancarlisle@rocketmail.com
   - elite-lights@elite-lights.com
   - julie@elite-lights.com
   - kjael@supercatsolutions.com
   - shoproycecollection@gmail.com
   - steve@supercatsolutions.com
   - chuck+kuzco@supercatsolutions.com

2. **Populate the `territories` table** (currently has 0 rows for org_id 166)
   - Run SQL migration from "How_To_Fix_Kuzco_Territory_Configuration.md"
   - This will create ~53 territories from existing customer data

3. **Test Sales Portal** with each of the 6 US Rep users after territory assignment

### Follow-up Actions:

4. **Review the 30 users with NULL sales portal setting**
   - Determine if they should have access or not
   - Set explicit true/false values

5. **Audit the 740 users with Sales Portal disabled**
   - Confirm these are correctly configured
   - Most appear to be designer/trade customers who shouldn't have Sales Portal

6. **Schedule cleanup session with Kevin/Katy**
   - Review all 53 territories
   - Identify active vs legacy territories
   - Update territory names to be descriptive
   - Remove unused territories

---

## Database Schema Reference

### Sales Portal Flag Location:
- **Table:** `user_types`
- **Column:** `properties` (JSONB)
- **Path:** `properties->flags->enable_sales_portal`
- **Values:** `true`, `false`, or `NULL`

### Territory Assignment Location:
- **Table:** `org_users`
- **Column:** `territory_codes` (JSONB array)
- **Format:** `["TERRITORY1", "TERRITORY2"]` or `[]` for none

### Territories Master Table:
- **Table:** `territories`
- **Current Status:** 0 rows for organization_id = 166 (THIS IS THE PROBLEM)
- **Required:** Must be populated for Sales Portal to function

---

## SQL Queries Used

### Count users without territories:
```sql
SELECT COUNT(*) 
FROM org_users ou 
JOIN organizations o ON ou.organization_id = o.id 
WHERE o.shortname = 'kll' 
  AND (ou.territory_codes IS NULL OR ou.territory_codes::text = '[]');
```

### Count users by sales portal status:
```sql
SELECT 
  COUNT(CASE WHEN ut.properties->'flags'->>'enable_sales_portal' = 'true' THEN 1 END) as enabled,
  COUNT(CASE WHEN ut.properties->'flags'->>'enable_sales_portal' = 'false' THEN 1 END) as disabled,
  COUNT(CASE WHEN ut.properties->'flags'->>'enable_sales_portal' IS NULL THEN 1 END) as null_value
FROM users u 
JOIN org_users ou ON u.id = ou.user_id 
JOIN organizations o ON ou.organization_id = o.id 
JOIN user_types ut ON ou.user_type_id = ut.id 
WHERE o.shortname = 'kll';
```

### Find users with Sales Portal but no territory:
```sql
SELECT u.email, u.first_name, u.last_name, ut.name as user_type, ou.territory_codes 
FROM users u 
JOIN org_users ou ON u.id = ou.user_id 
JOIN organizations o ON ou.organization_id = o.id 
JOIN user_types ut ON ou.user_type_id = ut.id 
WHERE o.shortname = 'kll' 
  AND ut.properties->'flags'->>'enable_sales_portal' = 'true' 
  AND (ou.territory_codes IS NULL OR ou.territory_codes::text = '[]');
```

---

## Related Documentation

- [How_To_Fix_Kuzco_Territory_Configuration.md](./How_To_Fix_Kuzco_Territory_Configuration.md) - Step-by-step fix guide
- [Kuzco_KLL_Comprehensive_Account_Assessment_Feb_2026.md](./Kuzco_KLL_Comprehensive_Account_Assessment_Feb_2026.md) - Full account analysis
- [Kuzco_KLL_Executive_Handoff_Report.md](./Kuzco_KLL_Executive_Handoff_Report.md) - Executive summary

---

**Next Steps:**
1. ✅ Data analysis complete
2. ⏳ Assign territories to 6 US Rep users
3. ⏳ Populate territories table (run SQL migration)
4. ⏳ Test Sales Portal functionality
5. ⏳ Update Help Scout ticket #13878
