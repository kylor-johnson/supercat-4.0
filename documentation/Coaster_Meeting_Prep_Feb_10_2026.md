# Coaster (CST) Meeting Prep - February 10, 2026

## Meeting Context
- **Last Call**: February 3, 2026 (38 mins)
- **Attendees Last Time**: Brent Sanders (SuperCat), Marlene Vidal, Kevin Tang
- **Today**: Brent unavailable - you're covering

---

## 🎯 Current Project Status

### ✅ Completed/Working
1. **Subcategories Fixed** - Dining room now properly shows all dining subcategories
2. **Related Items Integration** - Now pulling related items fields from API
3. **Scan Groups** - NOW WORKING! Updated to use Coaster's group numbers
4. **Matrix Options** - Implemented for bedroom sets (select size + piece count → generates correct SKU/price)
5. **Order Submission** - Tested before market, no issues (though no real orders yet)

### 🎥 Latest Updates (From Brent's Follow-up Videos)

#### **Group Scanning - WORKING** ✅
- Brent updated data file to use Coaster's group numbers
- When you scan a SKU (e.g., 551895), it shows:
  - Main scanned item first
  - All related products below (e.g., sectional corners, left arm, chaise)
- Can add multiple items from scan group to order in one flow
- **Status**: Ready for testing
- **Note**: Some new items missing descriptions/pricing in API data

#### **Matrix Options Implementation** ✅
- Example: Antonella bedroom set
  - Select: Black + Eastern King → generates correct SKU (224781-BK-EK) and price
  - Options dynamically update SKU and pricing
- **Display Issue**: Still using parent code (e.g., P1113313) as placeholder
- **Brent's Question**: Which SKU should display? Common digits from variants? Lowest SKU?

### 🔴 Critical Issues Being Worked On

#### 1. **Parent Code Display Issue** (SOLVED! ✅)
**The Issue**: Matrix option products showing parent codes (e.g., P1113313) instead of recognizable SKUs

**THE SOLUTION - From Coaster's Email**:
Coaster has a **Parent Flag** field in their system!

**How It Works**:
- Each parent code family has ONE child SKU marked `Parent Flag = TRUE`
- All other child SKUs marked `Parent Flag = FALSE`
- **Use the Parent Flag = TRUE SKU for display, image, and price**

**Example from their email**:
- Parent Code: P1113883
- Child SKUs: 223091NVYQ, 223091GRYKE, 223091GRYQ, 223091NVYKE
- **Primary SKU**: 223091NVYQ (Parent Flag = TRUE) ← Use this one!

**What This Means**:
- ✅ No more guessing which SKU to display
- ✅ Use Coaster's designated primary SKU
- ✅ Pull image and price from the Parent Flag = TRUE SKU
- ✅ Reps will see recognizable SKUs, not P codes

**Status**: ✅ **SOLUTION IDENTIFIED - Brent needs to implement Parent Flag logic**

**Action Item**: Confirm with Kevin that Parent Flag field is available in the API feed

---

#### 2. **Sparse Options Problem** (NEEDS APPROVAL)
**The Issue**: Some bedroom sets have incomplete option matrices

**Example**: Antonella Collection
- Eastern King: Available in 4-piece AND 5-piece ✅
- Queen: Available in 4-piece AND 5-piece ✅
- California King: ONLY available in 4-piece ❌ (no 5-piece)

**Current Problem**: 
- User can select "California King + 5-piece" but product doesn't exist
- Creates bad UX / broken experience

**Brent's Proposed Solution**:
- Remove California King 5-piece from option matrix
- Make it a separate standalone product
- Only show options that are fully compatible

**Status**: ⚠️ **NEEDS MARLENE'S APPROVAL**

---

#### 3. **Individual SKU Search/Scan** (PARTIALLY RESOLVED)
**Original Issue**: Products with variants couldn't be searched by individual SKU

**Current Status**: 
- Matrix options now working (select options → generates correct SKU/price)
- Group scanning working (scan one item → shows all related)
- **Still unclear**: Can individual variant SKUs be searched directly?

**Testing Needed**: 
- Can Marlene search "224781-BK-EK" directly?
- Can she scan individual barcodes for specific variants?

**Status**: Needs testing confirmation

---

#### 2. **Missing Products** (HIGH PRIORITY)
**Example**: SKU `552091` (Ashlyn Fabric Upholstered Track Arm Sofa)
- Shows in Coaster's API feed
- Not appearing in eCat catalog
- Issue: Has a parent code, so it's being treated as a virtual/option product

**Root Cause**: Products with parent codes are being collapsed into option groups and removed from main catalog

**Related Issue**: When searching "Ashlyn", it shows parent code (P1) instead of actual SKU numbers
- No common SKU pattern between variants (552091 vs 509891)
- Brent was trying to use common identifiers but many products don't have them

**Solution Direction**: 
- Include all variants as hidden/searchable products
- Display lowest SKU number for hierarchy
- Ensure both search AND scan functionality work

---

#### 3. **Data Feed Mapping Issues**
**Catalog Year vs PIA Product Line**:
- Some products showing "Open" in catalog year field
- Kevin discovered: "In our system it's inactive" for certain SKUs
- Mapping may be reversed between catalog year and PIA product line

**Action Item from Last Call**: Kevin to fix mapping and update Brent/Marlene

---

#### 4. **Missing Images**
- Newer items (especially Vegas market products) missing images
- Getting 404 errors
- Expected for new items, but needs monitoring

---

#### 5. **Missing Content**
- Product descriptions/stories not showing for some items
- Brent mentioned he hasn't uploaded latest content yet
- Should have content for everything except newest Vegas market items

---

### 📋 Outstanding Action Items

#### ✅ Completed Since Last Call:
1. **Brent** → ✅ Sent Loom videos showing:
   - Matrix options implementation (bedroom sets with size/piece selection)
   - Group scanning functionality (scan one item → shows related products)
2. **Brent** → ✅ Updated category listings and descriptions
3. **Brent** → ✅ Implemented scan groups using Coaster's group numbers

#### 🔴 Still Outstanding:
1. **Kevin** → Fix catalog year/product line mapping, send update
2. **Kyler (YOU)** → Email Marlene/Brent customer data cleanup template + notes
   - Document script that cleans up:
     - Bad/missing emails
     - Missing state codes for international customers
     - Missing zip codes
     - Data validation rules

#### ⚠️ NEW - Needs Decision/Approval:
1. ~~**Marlene** → Decide which SKU format to use for parent codes~~ ✅ **SOLVED** - Use Parent Flag field
2. **Marlene** → Approve "sparse options" approach (remove incomplete variants, make separate products)
3. **Marlene** → Test and confirm:
   - Group scanning works as expected
   - Matrix options generate correct SKUs/prices
   - Individual variant SKUs are searchable (if needed)

#### 🆕 NEW Action Items (From Parent Flag Email):
1. **Kevin** → Confirm Parent Flag field is available in API feed
2. **Brent** → Implement logic to use Parent Flag = TRUE SKU for display/image/price
3. **Brent** → Update matrix options to show primary SKU instead of parent codes

---

## 🗂️ Customer Data Import Issue

**Background**: Need to import Coaster customer list with ship-to addresses

**Problem**: 
- Steven's CSV file from Coaster has data quality issues:
  - Bad/missing emails
  - Missing state codes (international customers)
  - Missing zip codes
  - No flag for international customers
  
**Current Process**:
- Kyler runs cleanup script to validate data before import
- Script does: email validation, address standardization, international flagging

**API Option Explored**:
- Kevin has customer ship-to data available via API (`get customers` endpoint)
- BUT: Missing pricing code mapping to SuperCat system
- Conclusion: Still need CSV approach with cleanup

**Next Step**: Kyler to share cleanup template/script requirements with Coaster team

---

## 🔍 Technical Details to Know

### Hidden Products Functionality
- **Scanning**: Hidden products CAN be found via barcode scan
- **Searching**: Hidden products CANNOT be found in regular search
- **Toggle**: User can click "Show Hidden Products" (being renamed to "Show All Variants")
- **Default**: Toggle is OFF by default (not configurable per user group or company)

### Product Hierarchy Logic
- When variants have no common SKU pattern → use lowest SKU number
- Lower SKU = older/primary version
- Higher SKU = newer variant

### Related Items
- Now showing in eCat
- Most important for dining section (tables + chairs pairings)
- Collection view shows everything in a product collection

---

## 💬 Key Contacts & Dynamics

**Marlene Vidal** (Primary Contact)
- Concerned about user experience
- Emphasized: "If they can't search/scan immediately, they'll think it's not there and get turned off"
- Wants both variant display AND individual SKU searchability

**Kevin Tang** (Technical Contact)
- Handles API/data feed
- Discovered inactive item issue
- Working on mapping fixes

**Steven** (Data Contact)
- Provides customer CSV exports
- Data needs cleanup before import

---

## 🎤 Talking Points for Today's Call

### Opening
1. "Brent sends his apologies - I'm Kyler, covering for him today. I've reviewed the last call and Brent's follow-up videos."
2. "Good news: Group scanning is working and matrix options are implemented. But we need a couple decisions from you to move forward."

### 🔥 CRITICAL - Need Decisions Today

#### ~~Decision #1: Parent Code Display~~ ✅ SOLVED!
**Context**: "Brent has matrix options working - you can select Black + Eastern King and it generates the right SKU and price. But the product was showing as 'P1113313' which reps won't recognize."

**SOLUTION**: "Great news - we got your email about the Parent Flag field! So we'll use the SKU marked Parent Flag = TRUE for display, image, and price. This solves it perfectly."

**Follow-up Question**: "Kevin - can you confirm the Parent Flag field is in the API feed? Brent will need that to implement this."

#### Decision #2: Sparse Options (Incomplete Matrices)
**Context**: "Brent found that some bedroom sets don't have all combinations. For example, Antonella has California King in 4-piece but NOT 5-piece."

**Question**: "Brent proposes removing the California King from the 5-piece option selector and making it a separate product. Does that work for you, or do you want a different approach?"

### Key Questions to Ask
1. **Have you watched Brent's two Loom videos?** (Group scanning + Matrix options)
2. **Have you tested the group scanning?** Scan a SKU like 551895 and see if related products show up correctly
3. **Matrix options** - Does the select-and-generate-SKU approach work for your reps?
4. **Customer data import** - I need to send you the cleanup template. What's your timeline?
5. **Missing data** - Brent noted some new items missing descriptions/pricing in the API. Is Kevin aware?

### What to Communicate
1. **Group scanning is LIVE** - Uses Coaster's group numbers, shows main item + related products
2. **Matrix options working** - Select size/piece count → generates correct SKU/price
3. **Customer data template** - I'll send this week (action item on me)
4. **Two decisions needed** - Parent code display format + sparse options approach
5. **Testing needed** - Please test scanning and matrix options, give feedback

### Demo Flow (If Needed)
1. Show how group scanning works (scan → related products appear)
2. Show matrix options (select options → SKU/price updates)
3. Show parent code issue (P1113313 vs recognizable SKU)
4. Show sparse options problem (California King 5-piece doesn't exist)

### If They Ask About Timeline
- Focus on: "What needs to work for you to launch?"
- Prioritize: Search/scan functionality (critical for rep experience)
- Secondary: Content upload, related items refinement

---

## 🚨 Red Flags to Watch For

1. If they mention **more missing products** - get specific SKUs to investigate
2. If **inactive items** are showing up - Kevin needs to check data feed filters
3. If they're **frustrated with pace** - acknowledge and get clear on launch blockers

---

## 📊 Success Metrics to Discuss

- How many reps will be using this?
- What's the rollout plan? (Pilot group vs full launch)
- What's the #1 feature they need working perfectly for launch?

---

## Quick Reference: How Features Work Now

### Group Scanning Flow
```
Rep scans barcode (e.g., 551895)
    ↓
eCat looks up Coaster's group number
    ↓
Shows main scanned item FIRST
    ↓
Shows all related products below
    ↓
Rep can add multiple items to order
```

### Matrix Options Flow
```
Rep finds bedroom set (e.g., Antonella)
    ↓
Sees dropdown options: Size (EK/Q/CK) + Pieces (4/5)
    ↓
Selects: Black + Eastern King + 5-piece
    ↓
SKU updates: 224781-BK-EK-5
Price updates: $X,XXX
    ↓
Add to order with correct SKU/price
```

### Current Architecture
```
Coaster API Feed
    ↓
SuperCat Ingestion (filters out components, applies rules)
    ↓
Product Optioning Logic (creates matrix options using parent codes)
    ↓
Scan Groups (uses Coaster's group numbers)
    ↓
eCat Catalog Display
    ↓
Search/Scan Functionality
```

**Current issue**: Parent codes (P1113313) displaying instead of recognizable SKUs

---

## Follow-Up Actions for You

After today's call:
1. ✅ Send customer data cleanup template to Marlene (HIGH PRIORITY)
2. ✅ Relay Marlene's decisions to Brent:
   - Which SKU format to use for parent codes
   - Approval/changes for sparse options approach
3. ✅ Check in with Kevin on catalog year/product line mapping fix status
4. ✅ Document any new issues/SKUs they report
5. ✅ Confirm testing timeline for:
   - Group scanning functionality
   - Matrix options accuracy
   - Individual SKU search (if still needed)

---

## 📹 Video Transcript Key Quotes

### Video 1 - Matrix Options
> "You can select options, you can choose black, eastern king, and then the correct SKU will get generated. And price."

> "It begs the question, though, what should I use for the parent object? Because I know the reps are going to look for 224781, maybe? You know, is that what we should do?"

> "I identified there is no five piece California King. So, in cases like this, what I wanted to propose is I think it would be best to remove the California King five piece from this option selection and just make it a separate product."

### Video 2 - Group Scanning
> "I updated the data file to use just your group numbers, because they seem to be the most indicative of what, uh, like how things are grouped, and it already seems to be correct."

> "When you scan, it'll give you all the related stuff. So, I think this is the flow we want, where it's like, okay, I want two corners, I want a left, I want a chaise, and you can add all that stuff to the order."

> "The one thing about this product, though, is there's no descriptions of pricing, and that's in the data, that's in the API, so, if it looks weird, that's because it's missing a bunch of data."

---

## 📧 Email - Parent Flag Solution

**From**: Coaster Team  
**Subject**: Parent Code Display Logic

> "In your example, P1113883 maps to the following SKUs:
> - 223091NVYQ
> - 223091GRYKE
> - 223091GRYQ
> - 223091NVYKE
> 
> This represents the same bed model offered in two sizes (Q, KE) and two colors (NVY, GRY).
> 
> In our system, one child SKU within each Parent Code family is designated as the primary item using a **Parent Flag**. For this case, **223091NVYQ should be marked Parent Flag = TRUE**, with all other child SKUs marked Parent Flag = FALSE. **The image and price should be sourced from the SKU flagged TRUE.**
> 
> Other than that, your assumptions look good!"

**Key Takeaway**: Use the `Parent Flag = TRUE` SKU for display, image, and pricing on matrix option products.

---

## Personal Notes
- Marlene has a 4-year-old (common ground with Brent's kids)
- Team is California-based (watch time zones)
- They're dealing with Vegas market new products (recent trade show)
- Order submission tested but no real orders yet = still in setup phase
