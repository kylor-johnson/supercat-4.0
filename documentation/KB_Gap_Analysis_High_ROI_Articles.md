# Knowledge Base Gap Analysis - High ROI Article Opportunities
**Analysis Date:** January 29, 2026  
**Data Sources:**
- L1 Support Tickets (180 days, 349 tickets)
- Current Craft CMS Knowledge Base (133 articles)

---

## Executive Summary

By comparing **349 L1 support tickets** against the **133 existing KB articles**, I've identified **10 high-ROI KB article opportunities** that could reduce manual support effort by **28-35%** (98-122 tickets over 180 days).

### Quick Wins (Highest ROI)

| Priority | Article Topic | Tickets Saved | Current Gap | Effort |
|----------|--------------|---------------|-------------|--------|
| 🔥 **#1** | Self-Service Password Reset Guide | 37 tickets | ❌ Missing | Low |
| 🔥 **#2** | iPad Email Configuration for eCat | 10 tickets | ❌ Missing | Low |
| 🔥 **#3** | Rep Enrollment Process (End-to-End) | 21 tickets | ⚠️ Partial | Medium |
| 🔥 **#4** | Price Level Configuration Wizard | 7 tickets | ⚠️ Partial | Medium |
| 🔥 **#5** | Missing Images Troubleshooting | 10 tickets | ✅ Exists but needs update | Low |

**Total Quick Win Impact: 85 tickets (24.4%)**

---

## Detailed Gap Analysis

### 🔥 Priority 1: Self-Service Password Reset Guide

**Support Volume:** 37 tickets (10.6% of L1 tickets)
- 11 voice messages (urgent)
- 7 email requests
- 19 general login issues

**Current KB Coverage:** ❌ **MISSING**
- Existing article: "Login Issues: Troubleshooting Guide" (ID: 41467)
- **Gap:** Doesn't cover self-service password reset process
- **Gap:** No "Forgot Password" flow documentation

**What Customers Actually Ask:**
- "User forgot password and can't log in"
- "Password reset email expired"
- "Can't receive password reset email"
- "How do I reset my password?"
- Voice messages: "I have a meeting at 10am and can't log in"

**Recommended Article Title:**
**"How to Reset Your Password in eCat"**

**Article Content Should Cover:**
1. **Self-Service Reset (Primary Path)**
   - Click "Forgot Password" on login page
   - Enter email address
   - Check email (including spam folder)
   - Click reset link (expires in 24 hours)
   - Create new password (requirements)

2. **Admin-Assisted Reset (Secondary Path)**
   - When to contact your eCat administrator
   - What info to provide (username, email)
   - Admin instructions: Users → Users → Send Password Reset Email

3. **Troubleshooting**
   - "I didn't receive the email" (check spam, verify email address)
   - "The link expired" (request new one)
   - "I'm getting an error" (contact support with screenshot)

4. **Common Mistakes**
   - Using different passwords for different vendors (eCat = one password for all)
   - Sharing logins (causes password reset loops)
   - IT password managers forcing resets

**Format:** Step-by-step with screenshots + 2-minute Loom video

**Estimated Impact:** Eliminate 30-35 tickets (85-95% reduction)

**Urgency:** 🔥 **CRITICAL** - Voice messages indicate time-sensitive needs

---

### 🔥 Priority 2: iPad Email Configuration for eCat

**Support Volume:** 10 tickets (2.9% of L1 tickets)

**Current KB Coverage:** ⚠️ **PARTIAL**
- Existing article: "Emailing Product Information with eCat" (ID: 2383)
- **Gap:** Doesn't cover iPad Mail app configuration
- **Gap:** No troubleshooting for "wrong email sending"

**What Customers Actually Ask:**
- "CC line showing personal email instead of work email"
- "Emails sending from wrong address"
- "How do I change the email address eCat uses?"
- "Using Gmail app but emails not working"

**Recommended Article Title:**
**"Configuring iPad Email Settings for eCat"**

**Article Content Should Cover:**
1. **Why This Matters**
   - eCat uses iPad's native Mail app
   - Multiple email accounts = confusion
   - Default account determines "From" address

2. **Step-by-Step Setup**
   - Open iPad Settings → Mail
   - Scroll to bottom → Select default account
   - Choose business email (not personal)
   - Verify in Mail app

3. **Important Requirements**
   - ✅ Use Apple Mail (native app)
   - ❌ Don't use Gmail app
   - ❌ Don't use Outlook app
   - Why: Third-party apps don't integrate with eCat

4. **Changing Email Per-Message**
   - Tap email address in draft
   - Select different account from dropdown
   - Screenshot showing this

5. **Troubleshooting**
   - "I only see one email option" → Add business email to iPad
   - "Still sending from wrong email" → Check default in Settings
   - "Using Outlook app" → Switch to Apple Mail

**Format:** Visual guide with GIF showing Settings navigation + screenshots

**Estimated Impact:** Eliminate 8-9 tickets (80-90% reduction)

**Urgency:** 🔥 **HIGH** - Repetitive issue with same resolution every time

---

### 🔥 Priority 3: Rep Enrollment Process (End-to-End)

**Support Volume:** 21 tickets (6.0% of L1 tickets)

**Current KB Coverage:** ⚠️ **PARTIAL**
- Existing articles:
  - "User Enrollment" (ID: 722)
  - "Delegated Enrollment" (ID: 1883)
  - "eCat Online Quick Enrollment" (ID: 1627)
- **Gap:** No end-to-end rep perspective
- **Gap:** Doesn't clarify SuperCat vs Vendor roles
- **Gap:** No troubleshooting for "didn't receive enrollment link"

**What Customers Actually Ask:**
- "Rep needs access to 5 vendors but didn't receive links"
- "Can SuperCat grant vendor access?"
- "How do I enroll a new rep?"
- "Rep says they didn't get enrollment email"

**Recommended Article Title:**
**"Rep Enrollment: Complete Guide for Reps and Vendors"**

**Article Content Should Cover:**

**For Reps:**
1. **How Enrollment Works**
   - Vendor must invite you (SuperCat can't grant access)
   - Each vendor sends separate enrollment link
   - One eCat account = access to all your vendors

2. **What to Expect**
   - Email from vendor with "Enroll in [Vendor Name]" link
   - Click link → Create password (first time only)
   - Subsequent vendors use same login

3. **If You Don't Receive Enrollment Email**
   - Check spam folder
   - Verify vendor has correct email address
   - Contact vendor directly (not SuperCat)
   - Provide: Your name, email, company name

4. **Troubleshooting**
   - "Link expired" → Ask vendor to resend
   - "Already have account" → Use existing login
   - "Different email for different vendors" → Contact SuperCat to merge

**For Vendors:**
1. **How to Enroll a Rep**
   - Admin Console → Users → Add User
   - Enter rep's email address
   - System sends enrollment email automatically
   - Rep creates password on first login

2. **What SuperCat Can Do**
   - Create account "shell" with username
   - Send password reset emails
   - Verify enrollment email was sent

3. **What SuperCat Cannot Do**
   - Grant vendor access (only you can)
   - Enroll reps without your permission
   - See rep's password

**Format:** Two-section article with flowchart showing process + screenshots

**Estimated Impact:** Eliminate 15-18 tickets (70-85% reduction)

**Urgency:** 🔥 **HIGH** - Common confusion, clear process can eliminate

---

### 🔥 Priority 4: Price Level Configuration Wizard

**Support Volume:** 7 tickets (2.0% of L1 tickets)

**Current KB Coverage:** ⚠️ **PARTIAL**
- Existing articles:
  - "Price Levels" (ID: 519)
  - "Catalog Pricing" (ID: 2531)
  - "Comparison Price Level" (ID: 1778)
- **Gap:** No step-by-step wizard/guide
- **Gap:** Doesn't explain user group vs customer contract pricing
- **Gap:** No currency configuration guidance

**What Customers Actually Ask:**
- "How do I configure price levels?"
- "Where is my second price level?"
- "Currency showing wrong (USD vs CAD)"
- "Price level not showing for customer"

**Recommended Article Title:**
**"Price Level Setup: Step-by-Step Guide"**

**Article Content Should Cover:**

1. **Understanding Price Levels**
   - Base price level (required)
   - Additional price levels (optional, up to 3)
   - User group default vs customer-specific

2. **Step-by-Step Setup**
   
   **Step 1: Define Price Levels**
   - Company Settings → Price Levels
   - Name each level (e.g., "MSRP", "Net", "Dealer")
   - Set currency (USD, CAD, EUR, etc.)
   - Screenshot of configuration

   **Step 2: Configure User Group Defaults**
   - User Groups → Select group
   - Product Fields tab
   - Check which price levels to display
   - Set default price level
   - Screenshot showing checkboxes

   **Step 3: Set Customer-Specific Pricing (Optional)**
   - Import contract prices via CSV
   - Or set manually in Customer Inquiry
   - Overrides user group defaults

3. **Common Scenarios**
   - **Scenario 1:** Show MSRP and Net to all reps
   - **Scenario 2:** Show different pricing to different rep groups
   - **Scenario 3:** Customer-specific contract pricing
   - **Scenario 4:** Multi-currency setup

4. **Troubleshooting**
   - "Second price level not showing" → Check user group Product Fields
   - "Wrong currency" → Company Settings → Price Levels
   - "Customer seeing wrong price" → Check contract prices

**Format:** Step-by-step wizard with decision tree + screenshots for each step

**Estimated Impact:** Eliminate 5-6 tickets (70-85% reduction)

**Urgency:** 🔥 **MEDIUM-HIGH** - Complex topic, high back-and-forth

---

### 🔥 Priority 5: Missing Images Troubleshooting (Update Existing)

**Support Volume:** 10 tickets (2.9% of L1 tickets)

**Current KB Coverage:** ✅ **EXISTS BUT NEEDS UPDATE**
- Existing article: "Missing Images Report" (ID: 538)
- **Gap:** Doesn't explain the TWO types of missing image errors
- **Gap:** No visual guide showing how to fix each type
- **Gap:** No Loom video walkthrough

**What Customers Actually Ask:**
- "Images not showing up after I uploaded them"
- "10+ SKUs with missing images"
- "How do I fix missing images?"

**Recommended Article Update:**
**"Missing Images Troubleshooting: Complete Guide"**

**Updated Article Content Should Cover:**

1. **Understanding Missing Image Errors**
   - Two distinct error types (not the same!)
   - How to identify which type you have

2. **Error Type 1: No Filename Specified (Yellow)**
   - **What it means:** ImageFileName column is empty in product file
   - **How to fix:**
     1. Export products CSV
     2. Add filename to ImageFileName column (e.g., "SKU123.jpg")
     3. Re-import product file
   - **Screenshot:** Product file with ImageFileName column highlighted

3. **Error Type 2: Filename Specified but File Missing (Green)**
   - **What it means:** ImageFileName says "SKU123.jpg" but file not uploaded
   - **How to fix:**
     1. Check filename spelling (case-sensitive!)
     2. Verify file was uploaded to FTP
     3. Check file extension (.jpg vs .JPG)
     4. Re-upload image if needed
   - **Screenshot:** FTP folder showing uploaded images

4. **Using the Missing Images Report**
   - Tools → Missing Images
   - Export to CSV for bulk fixing
   - Filter by error type
   - Screenshot of report

5. **Prevention Tips**
   - Upload images BEFORE importing product file
   - Use consistent naming convention
   - Verify uploads in FTP client

**Format:** Step-by-step guide with color-coded screenshots + 3-minute Loom video

**Estimated Impact:** Eliminate 7-8 tickets (70-80% reduction)

**Urgency:** 🔥 **MEDIUM** - Existing article needs enhancement

---

### 🟡 Priority 6: Account Email/Username Changes

**Support Volume:** 25 tickets (7.2% of L1 tickets)

**Current KB Coverage:** ⚠️ **PARTIAL**
- Existing article: "Updating Account Email" (ID: 3033)
- **Gap:** Doesn't cover complex scenarios (multiple accounts, vendor associations)
- **Gap:** No explanation of when users can vs can't change email

**What Customers Actually Ask:**
- "How do I change my email address?"
- "Getting error when trying to update email"
- "New owner, need to change account email"
- "Have multiple accounts, want to merge"

**Recommended Article Title:**
**"Changing Your Account Email or Username"**

**Article Content Should Cover:**

1. **Self-Service Email Change (For Reps)**
   - Login to eCat
   - Tap gear icon → My Account
   - Tap "Update Email Address"
   - Confirm via email link
   - **When this works:** Single vendor, no other associations

2. **Admin-Assisted Email Change (For Vendors)**
   - Admin Console → Users → Edit User
   - Update email address
   - **When this works:** User only associated with your org

3. **When You Can't Change Email**
   - User is associated with multiple vendors
   - User must update themselves (see #1)
   - Why: Prevents accidental lockout from other vendors

4. **Account Ownership Changes**
   - New owner scenario (e.g., company acquisition)
   - Can't merge accounts (data loss)
   - Workarounds:
     1. Update primary account, delete secondary
     2. Keep both accounts separate
     3. Contact each vendor individually

5. **Troubleshooting**
   - "Error when changing email" → Likely multi-vendor user
   - "Want to merge accounts" → Not possible, choose workaround
   - "Lost access after email change" → Contact admin

**Format:** Decision tree flowchart + step-by-step for each scenario

**Estimated Impact:** Eliminate 15-18 tickets (60-70% reduction)

**Urgency:** 🟡 **MEDIUM** - Complex topic, but lower volume than top 5

---

### 🟡 Priority 7: Barcode Scanning Setup (Two Methods)

**Support Volume:** 2 tickets (0.6% of L1 tickets)

**Current KB Coverage:** ✅ **EXISTS BUT INCOMPLETE**
- Existing articles:
  - "Group Scanning" (ID: 2363)
  - "Scanning Orders with eCat" (ID: 848)
  - "Scan Items to Lists" (ID: 3081)
- **Gap:** Doesn't clearly explain TWO different scanning methods
- **Gap:** No decision guide for which method to use

**What Customers Actually Ask:**
- "Added ScanValue to file but can't search for it"
- "How do I set up barcode scanning?"
- "Can I scan one tag to pull up entire product family?"

**Recommended Article Title:**
**"Barcode Scanning Setup: Complete Guide"**

**Article Content Should Cover:**

1. **Two Scanning Methods (Choose One or Both)**

   **Method 1: Search Bar Scanning**
   - **Use case:** Find products by scanning in search
   - **Setup:** Add barcode value to `keywords` field in product file
   - **How to use:** All Products → Search bar → Scan
   - **Screenshot:** Search bar with scan icon

   **Method 2: Direct-to-Order Scanning**
   - **Use case:** Scan items directly onto customer order
   - **Setup:** Add barcode value to `ScanValue` field in product file
   - **How to use:** Select customer → View Order → Tap scan button → Scan
   - **Screenshot:** Order page with scan button

2. **Group Scanning (Scan One Tag for Entire Family)**
   - **Use case:** 400 new intros, don't want 400 tags
   - **Setup:** Add `ScanGroupCode` field to product file
   - **Populate with:** Family name or group identifier
   - **How to use:** Scan tag → All products in group appear
   - **Example:** "KORDAN" group code shows all Kordan products

3. **Decision Guide**
   - Use Search Bar Scanning if: Reps search for products
   - Use Direct-to-Order Scanning if: Showroom ordering
   - Use Group Scanning if: Want one tag per family

4. **Product File Setup**
   - Column names: `keywords`, `ScanValue`, `ScanGroupCode`
   - Example values
   - Import process

**Format:** Comparison table + step-by-step for each method + Loom video

**Estimated Impact:** Eliminate 1-2 tickets (50-100% reduction) + prevent future growth

**Urgency:** 🟡 **LOW-MEDIUM** - Low volume but high confusion when it happens

---

### 🟡 Priority 8: Report Generation Guide

**Support Volume:** 5 tickets (1.4% of L1 tickets)

**Current KB Coverage:** ⚠️ **SCATTERED**
- Existing articles:
  - "Feature Usage Report" (ID: 1454)
  - "Summary Usage Report" (ID: 534)
  - "Detailed Usage Report" (ID: 529)
  - "Market Reports" (ID: 39317)
- **Gap:** No single "how to generate reports" guide
- **Gap:** Doesn't explain what reports are available

**What Customers Actually Ask:**
- "How do I generate reports?"
- "What reports are available?"
- "How do I export customer order data?"
- "Where do I find rep usage data?"

**Recommended Article Title:**
**"Reports in eCat: Complete Guide"**

**Article Content Should Cover:**

1. **Available Reports Overview**
   - Usage reports (rep activity)
   - Order reports (customer orders)
   - Feature reports (what features used)
   - Market reports (market performance)
   - Import reports (data sync status)

2. **How to Generate Reports**
   - Tools menu → Reports
   - Or Orders → Reports
   - Select report type
   - Set date range
   - Export to CSV
   - Screenshots for each report type

3. **Common Report Scenarios**
   - **Scenario 1:** "Which reps are most active?"
     - Use: Summary Usage Report
   - **Scenario 2:** "What did customer X order?"
     - Use: Orders → Filter by customer → Export
   - **Scenario 3:** "How many orders during market?"
     - Use: Market Reports
   - **Scenario 4:** "Did my data import successfully?"
     - Use: Import Status Report

4. **Exporting Data**
   - CSV export button location
   - Opening in Excel
   - Data format explanation

**Format:** Report catalog with screenshots + use case examples

**Estimated Impact:** Eliminate 3-4 tickets (60-80% reduction)

**Urgency:** 🟡 **LOW-MEDIUM** - Lower volume, existing articles just need consolidation

---

### 🟡 Priority 9: Logo/Branding Image Upload

**Support Volume:** 5 tickets (1.4% of L1 tickets)

**Current KB Coverage:** ✅ **EXISTS**
- Existing articles:
  - "Import Navigation Panel Logo" (ID: 554)
  - "Import Logo Button Image" (ID: 560)
  - "Import Branding Image" (ID: 556)
  - "Import Document Logo" (ID: 558)
- **Gap:** Four separate articles, confusing which to use
- **Gap:** No consolidated guide

**What Customers Actually Ask:**
- "How do I upload logo?"
- "Where do I upload branding images?"
- "What's the difference between logo types?"

**Recommended Article Title:**
**"Uploading Logos and Branding Images"**

**Article Content Should Cover:**

1. **Four Logo Types Explained**
   - **Navigation Panel Logo:** Top-left corner of eCat
   - **Logo Button:** Button in toolbar
   - **Branding Image:** Full-width header image
   - **Document Logo:** Appears on printed orders/quotes

2. **Upload Process (Same for All)**
   - Tools → Import Images
   - Select logo type
   - Choose file
   - Upload
   - Verify in eCat

3. **Image Requirements**
   - File formats: PNG, JPG
   - Recommended sizes for each type
   - Transparent background (PNG recommended)

4. **Visual Guide**
   - Screenshot showing where each logo appears
   - Side-by-side comparison

**Format:** Consolidated guide with visual examples

**Estimated Impact:** Eliminate 3-4 tickets (60-80% reduction)

**Urgency:** 🟡 **LOW** - Existing articles just need consolidation

---

### 🟡 Priority 10: Order Integration (How Orders Flow)

**Support Volume:** 6 tickets (1.7% of L1 tickets)

**Current KB Coverage:** ✅ **EXISTS BUT TECHNICAL**
- Existing articles:
  - "JSON Real Time Order Export API (Push)" (ID: 390)
  - "JSON Batch Order Export API (Pull)" (ID: 117)
  - "Order Download API" (ID: 1635)
- **Gap:** Too technical for non-technical users
- **Gap:** No plain-English explanation

**What Customers Actually Ask:**
- "How do orders flow into our ERP?"
- "What's the difference between push and pull?"
- "Do I need an API?"

**Recommended Article Title:**
**"How eCat Orders Flow Into Your System"**

**Article Content Should Cover:**

1. **Two Integration Methods**
   
   **Push (Real-Time)**
   - Orders sent immediately when submitted
   - Your system receives JSON data
   - Requires: Endpoint URL, authentication
   - Best for: Real-time order processing

   **Pull (Batch)**
   - You retrieve orders on schedule (hourly, daily)
   - Your system calls SuperCat API
   - Requires: API credentials
   - Best for: Batch processing systems

2. **Plain-English Explanation**
   - Push = "We send you orders"
   - Pull = "You fetch orders from us"
   - Both deliver same data, different timing

3. **What You Need**
   - Technical contact at your company
   - System that can receive/send JSON
   - API credentials (SuperCat provides)

4. **Setup Process**
   - Contact SuperCat support
   - Provide technical requirements
   - Test integration
   - Go live

**Format:** Simple comparison + flowchart + "Next Steps"

**Estimated Impact:** Eliminate 3-4 tickets (50-65% reduction)

**Urgency:** 🟡 **LOW** - Lower volume, technical topic

---

## ROI Summary

### Total Potential Ticket Reduction

| Priority | Article | Tickets Saved | % of L1 Volume |
|----------|---------|---------------|----------------|
| 🔥 #1 | Self-Service Password Reset | 30-35 | 8.6-10.0% |
| 🔥 #2 | iPad Email Configuration | 8-9 | 2.3-2.6% |
| 🔥 #3 | Rep Enrollment Process | 15-18 | 4.3-5.2% |
| 🔥 #4 | Price Level Configuration | 5-6 | 1.4-1.7% |
| 🔥 #5 | Missing Images Troubleshooting | 7-8 | 2.0-2.3% |
| 🟡 #6 | Account Email Changes | 15-18 | 4.3-5.2% |
| 🟡 #7 | Barcode Scanning Setup | 1-2 | 0.3-0.6% |
| 🟡 #8 | Report Generation Guide | 3-4 | 0.9-1.1% |
| 🟡 #9 | Logo Upload Consolidation | 3-4 | 0.9-1.1% |
| 🟡 #10 | Order Integration Explained | 3-4 | 0.9-1.1% |
| **TOTAL** | **All 10 Articles** | **90-108** | **25.8-30.9%** |

### Conservative Estimate
- **Tickets saved:** 90-100 tickets per 180 days
- **Percentage reduction:** 26-29% of L1 volume
- **Annual impact:** 180-200 tickets per year

### Optimistic Estimate
- **Tickets saved:** 100-122 tickets per 180 days
- **Percentage reduction:** 29-35% of L1 volume
- **Annual impact:** 200-244 tickets per year

---

## Implementation Roadmap

### Phase 1: Quick Wins (Weeks 1-4)
**Goal:** Eliminate 65-75 tickets (18-21%)**

1. **Week 1:** Self-Service Password Reset Guide
   - Effort: 4-6 hours
   - Format: Step-by-step + 2-min video
   - Impact: 30-35 tickets

2. **Week 2:** iPad Email Configuration
   - Effort: 3-4 hours
   - Format: Visual guide with GIF
   - Impact: 8-9 tickets

3. **Week 3:** Missing Images Update
   - Effort: 3-4 hours
   - Format: Update existing article + 3-min video
   - Impact: 7-8 tickets

4. **Week 4:** Rep Enrollment Process
   - Effort: 6-8 hours
   - Format: Two-section guide + flowchart
   - Impact: 15-18 tickets

**Phase 1 Total:** 16-22 hours, 60-70 tickets saved

---

### Phase 2: Medium Complexity (Weeks 5-8)
**Goal:** Eliminate additional 20-30 tickets (6-9%)**

5. **Week 5:** Price Level Configuration
   - Effort: 8-10 hours
   - Format: Step-by-step wizard + decision tree
   - Impact: 5-6 tickets

6. **Week 6:** Account Email Changes
   - Effort: 6-8 hours
   - Format: Decision tree + scenarios
   - Impact: 15-18 tickets

**Phase 2 Total:** 14-18 hours, 20-24 tickets saved

---

### Phase 3: Consolidation & Enhancement (Weeks 9-12)
**Goal:** Eliminate additional 10-15 tickets (3-4%)**

7. **Week 9:** Barcode Scanning Setup
   - Effort: 6-8 hours
   - Format: Comparison guide + video
   - Impact: 1-2 tickets (+ prevent future)

8. **Week 10:** Report Generation Guide
   - Effort: 4-6 hours
   - Format: Consolidate existing articles
   - Impact: 3-4 tickets

9. **Week 11:** Logo Upload Consolidation
   - Effort: 3-4 hours
   - Format: Consolidate 4 articles into 1
   - Impact: 3-4 tickets

10. **Week 12:** Order Integration Explained
    - Effort: 4-6 hours
    - Format: Plain-English guide
    - Impact: 3-4 tickets

**Phase 3 Total:** 17-24 hours, 10-14 tickets saved

---

## Total Implementation

**Total Effort:** 47-64 hours (6-8 days of work)
**Total Impact:** 90-108 tickets saved (26-31% reduction)
**ROI:** ~1.5 tickets saved per hour of work

---

## Success Metrics

### Ticket Volume Tracking
- **Baseline:** 349 L1 tickets per 180 days
- **Target after Phase 1:** 279-289 tickets (20% reduction)
- **Target after Phase 2:** 255-269 tickets (23-27% reduction)
- **Target after Phase 3:** 241-259 tickets (26-31% reduction)

### KB Article Metrics
- **Page views** for each new article
- **Time on page** (indicates usefulness)
- **Search queries** leading to article
- **Support tickets** linking to article

### Support Team Metrics
- **Time saved** per ticket (avg 15-30 min)
- **Total hours saved** per month
- **Tickets resolved** with KB link only

---

## Article Format Best Practices

Based on L1 ticket analysis, effective KB articles should include:

### 1. Visual Elements
- ✅ Screenshots with highlights/arrows
- ✅ GIFs showing navigation
- ✅ 2-5 minute Loom videos
- ✅ Flowcharts for decision trees
- ❌ Text-only explanations

### 2. Structure
- ✅ "What You'll Learn" at top
- ✅ Step-by-step numbered lists
- ✅ "Common Mistakes" section
- ✅ "Troubleshooting" section
- ✅ "Next Steps" at bottom

### 3. Tone
- ✅ Plain English (not technical jargon)
- ✅ "You" language (conversational)
- ✅ Empathetic ("We know this is confusing...")
- ❌ Formal/corporate language

### 4. Searchability
- ✅ Customer language in title ("How do I..." not "Configuring...")
- ✅ Common error messages quoted
- ✅ Alternative terms (e.g., "password reset" = "forgot password")

---

## Appendix: Existing KB Articles by Category

### User Management (10 articles)
- ✅ Managing eCat Users (ID: 501)
- ✅ User Groups (ID: 503)
- ✅ User Enrollment (ID: 722)
- ✅ Updating Account Email (ID: 3033)
- ✅ Delegated Enrollment (ID: 1883)
- ⚠️ **Gap:** Self-service password reset
- ⚠️ **Gap:** iPad email configuration
- ⚠️ **Gap:** Rep enrollment (end-to-end)

### Scanning (6 articles)
- ✅ Group Scanning (ID: 2363)
- ✅ Scanning Orders with eCat (ID: 848)
- ✅ Scan Items to Lists (ID: 3081)
- ✅ Showroom Tips: Scanning (ID: 3079)
- ✅ Test Your Scanner (ID: 3083)
- ⚠️ **Gap:** Two scanning methods comparison

### Pricing (5 articles)
- ✅ Price Levels (ID: 519)
- ✅ Catalog Pricing (ID: 2531)
- ✅ Comparison Price Level (ID: 1778)
- ✅ Special Promotion Pricing (ID: 97)
- ⚠️ **Gap:** Step-by-step configuration wizard

### Images (6 articles)
- ✅ Missing Images Report (ID: 538)
- ✅ Import Product Photo (ID: 550)
- ✅ Import Navigation Panel Logo (ID: 554)
- ✅ Import Logo Button Image (ID: 560)
- ✅ Import Branding Image (ID: 556)
- ⚠️ **Gap:** Two types of missing image errors

### Reports (5 articles)
- ✅ Feature Usage Report (ID: 1454)
- ✅ Summary Usage Report (ID: 534)
- ✅ Detailed Usage Report (ID: 529)
- ✅ Market Reports (ID: 39317)
- ⚠️ **Gap:** Consolidated "how to generate reports"

### Orders (4 articles)
- ✅ JSON Real Time Order Export API (ID: 390)
- ✅ JSON Batch Order Export API (ID: 117)
- ✅ Order Download API (ID: 1635)
- ⚠️ **Gap:** Plain-English explanation

---

## Conclusion

By creating **10 targeted KB articles** addressing the most common L1 support requests, SuperCat can reduce manual support effort by **26-31%** (90-108 tickets per 180 days).

### Highest ROI Opportunities:
1. **Self-Service Password Reset** - 30-35 tickets (10%)
2. **Rep Enrollment Process** - 15-18 tickets (5%)
3. **Account Email Changes** - 15-18 tickets (5%)
4. **iPad Email Configuration** - 8-9 tickets (2.5%)
5. **Missing Images Troubleshooting** - 7-8 tickets (2%)

**These top 5 articles alone would eliminate 75-88 tickets (21-25% of L1 volume).**

### Implementation Priority:
- **Phase 1 (Weeks 1-4):** Focus on top 4 quick wins
- **Phase 2 (Weeks 5-8):** Add medium-complexity articles
- **Phase 3 (Weeks 9-12):** Consolidate and enhance existing articles

**Total effort: 47-64 hours (6-8 days) for 26-31% ticket reduction.**

---

**Next Steps:**
1. Review and approve article priorities
2. Assign content creation to team member(s)
3. Create article templates based on best practices
4. Begin Phase 1 implementation
5. Track metrics after each article launch

---

**Report Generated:** January 29, 2026  
**Data Sources:** 349 L1 tickets (180 days) + 133 existing KB articles  
**Methodology:** Gap analysis comparing support volume to KB coverage
