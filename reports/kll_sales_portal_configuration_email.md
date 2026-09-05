# Email to Kevin at Kuzco - Agenda for Upcoming Meeting

**To:** Kevin Batkiewicz (kevin.b@kuzcolighting.com)  
**CC:** Katy Tipton (katy.t@kuzcolighting.com), Holly Graves (holly.g@kuzcolighting.com)  
**From:** [Your Name]  
**Subject:** Agenda for Our Upcoming Meeting  
**Date:** February 4, 2026

---

Hi Kevin,

Looking forward to our upcoming session. I want to make sure we use our time together effectively, so here's what I'd like to cover:

## Meeting Agenda

### 1. Clarify Roles & Responsibilities
- Confirm who your primary admins are and their current comfort level with the system
- Identify other stakeholders who should be involved in different areas
- Understand what training you've received and where you need more support

### 2. Training & Support
Based on what we learn about your team's needs, we'll cover:
- **Data foundations:** Products, customers, inventory
- **User management:** Setup, permissions, user types
- **Catalog management:** Collections, groups, organization

### 3. Sales Portal - Resolve Blocker & Plan Rollout
We need to get Sales Portal working properly. Here's what we'll address:

**Immediate issue:** 6 users need territory assignments before Sales Portal can work:
- briancarlisle@rocketmail.com - Brian Carlisle
- elite-lights@elite-lights.com - Rick Taylor  
- julie@elite-lights.com - Julie Jenkins
- shoproycecollection@gmail.com - Tanya Royce

**We'll discuss:**
- Territory assignments for these users
- Review of your 53 territory codes (which are active vs. legacy?)
- Confirmation of your 79 Sales Portal users
- Plan for Sales Portal orientation and rollout training for your reps

---

Please come prepared with any questions or concerns you have. I want to make sure we get Sales Portal working properly and that you have everything you need going forward.

See you soon,  
[Your Name]

---

## Active User Analysis

**Note:** Database queries for login activity are timing out. Based on available data:
- **Total Users:** 849
- **Sales Portal Enabled:** 79 users
- **Recent Order Activity:** 81 orders in last 30 days, 108 orders in last 90 days
- **User Types:** 76 US Reps, 207 Premier Designers, 249 Trade Platinum, 101 Trade Diamond, 90 Trade Gold

**Recommendation:** During the meeting, ask Kevin which users are actively using the system vs. inactive legacy accounts that could be archived.

---

## Quick Reference - Users Needing Territories

**Full list of 6 users:**
1. briancarlisle@rocketmail.com - Brian Carlisle
2. elite-lights@elite-lights.com - Rick Taylor  
3. julie@elite-lights.com - Julie Jenkins
4. kjael@supercatsolutions.com - Kjael Skaalerud (SuperCat internal)
5. shoproycecollection@gmail.com - Tanya Royce
6. steve@supercatsolutions.com - Steve Thrasher (SuperCat internal)
7. chuck+kuzco@supercatsolutions.com - Chuck Wiebe (SuperCat internal)

**Note:** Last 3 are SuperCat internal accounts - focus on the first 4 for your reps.

---

## Supporting Documentation

- [KLL Territory & Sales Portal Analysis](/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/documentation/KLL_Territory_Sales_Portal_Analysis_Feb_2026.md)
- [How To Fix Kuzco Territory Configuration](/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/documentation/How_To_Fix_Kuzco_Territory_Configuration.md)
- [Kuzco Comprehensive Account Assessment](/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/documentation/Kuzco_KLL_Comprehensive_Account_Assessment_Feb_2026.md)

---

## Internal Notes (Do Not Include in Email)

### Additional Context
- **Help Scout Ticket #13878** (Jan 21-26, PENDING): Users can't see Sales Portal button or invoices/orders
- **Fathom Call (Jan 30):** Discovered "Sunburst" territory showing all customers during live training
- **Root Cause:** Territories table has 0 rows for organization_id 166 (Kuzco)
- **Financial Impact:** They're paying $4,740/year + $2,250 implementation for a Sales Portal that doesn't work

### Users with Sales Portal Enabled (79 total)
- **US Reps:** 76 users (6 need territories assigned)
- **z-SuperCat:** 3 users (internal SuperCat accounts)

### Users WITHOUT Sales Portal (770 total)
- **Premier Designer:** ~200 users
- **Trade Platinum/Gold/Diamond:** ~400 users
- **CAD Reps:** ~50 users
- **Admin:** ~24 users
- **Other:** ~96 users

These users are correctly configured - they use eCat for ordering but don't need Sales Portal.

### Database Query Results

**Results:**
- Total users: 849
- Sales Portal enabled: 79
- No territory: 768
- Sales Portal enabled but no territory: 9 (6 US Reps + 3 SuperCat internal)

### Territory Data Summary

**Territories in customer data:** 53 unique codes  
**Territories in territories table:** 0 (THIS IS THE BLOCKER)  
**Users with territories assigned:** 77  
**Users without territories:** 772

**Top 10 territories by customer count:**
1. KUZCO: 446
2. NUVO: 154
3. GRILLO INC: 150
4. LES: 140
5. STONEHOUSE: 129
6. PORTER: 128
7. BCLIGHTS: 109
8. TRINITY: 108
9. FLETCHER: 98
10. SANDD2: 97

### Known Territory Issues (Historical)

1. **LEGACYSALES vs DALE** (July 2025, Ticket #12797)
   - Territory code changed from "DALE" to "LEGACYSALES" for Wasatch Lighting
   - Libby's territory code still set to "DALE"
   - Never fully resolved

2. **Sunburst Territory** (January 2026, Fathom training)
   - Showed all customers instead of filtering
   - Root cause: territories table empty

3. **Case Sensitivity** (Current)
   - "KUZCO" (446 customers) vs "Kuzco" (20 customers)
   - Should be standardized to uppercase

### Configuration Steps (After Kevin Responds)

1. **Populate territories table** with the 53 existing territory codes from customer data
2. **Assign territories to users** based on Kevin's provided assignments
3. **Test Sales Portal** with sample users to validate territory filtering
4. **Go live** with all reps

### Follow-up Actions After Email Response

1. ✅ Receive territory assignments from Kevin
2. ⏳ Configure territories in system (populate territories table with 53 codes)
3. ⏳ Assign territories to 6 users based on Kevin's input
4. ⏳ Test Sales Portal with Kevin's team
5. ⏳ Update Help Scout ticket #13878 as resolved
6. ⏳ Schedule cleanup session for territory optimization
7. ⏳ Document final territory structure
8. ⏳ Update Sales Portal implementation checklist to prevent this in future

### Success Metrics

- ✅ All 6 US Rep users have territories assigned
- ✅ Territories table populated (53 territories)
- ✅ Sales Portal functional for all 79 enabled users
- ✅ No "showing all customers" issues
- ✅ Help Scout ticket #13878 resolved
- ✅ Kevin rates support experience 8+ out of 10
