# L1 Frontline Support Analysis - 180 Day Lookback
**Analysis Period:** August 1, 2025 - January 29, 2026  
**Data Source:** Hevo Dataset - Help Scout Tickets  
**Inbox:** Support Only (`support@supercatsolutions.com`)  
**Filter:** L1 - Handled by Frontline Support OR First-Touch Resolved  
**Date Generated:** January 29, 2026

---

## Executive Summary

This analysis examines **349 L1/first-touch support tickets** over 180 days to identify the most common, straightforward support requests that don't require engineering intervention or complex troubleshooting.

### Key Metrics
- **Total L1 Tickets:** 349
- **Closed:** 340 (97.4%)
- **Average Thread Count:** 4.4 messages
- **Focus:** Non-nuanced, non-engineering support requests

---

## Top 10 Most Common Support Request Types

### 1. User Management (124 tickets - 35.5%)

**What Customers Actually Need:**

#### Password Resets (37 tickets)
- **Request:** "User forgot password and can't log in"
- **Example:** Ticket #13906 - "Saul needs username and password please" - User over 70 years old, has meeting at 10am, misplaced credentials
- **Example:** Ticket #13776 - "LOGIN issues" - Password reset email expired
- **Example:** Ticket #13656 - "cannot reset password" - Customer getting error during password reset
- **Voice Messages:** 11 tickets came through as voice messages (urgent password resets)
  - Pattern: Users call when they can't access system immediately
  - Example: "My e card is not opening up...it is 9AM, please answer the phone"
- **Resolution:** Send password reset email from admin console (Users → Users → Send Password Reset Email)
- **Time:** Same day, often within hours

#### New User Account Setup (13 tickets)
- **Request:** "Need to create account for new rep/employee"
- **Example:** Ticket #13842 - "New eCat User" - Rep needs access to 5 vendors (Varaluz, Kuzco/Alora, Accord, Buster + Punch, Hubbardton Forge)
- **Issue:** Rep didn't receive enrollment links from vendors
- **Resolution:** Create account, provide credentials, explain that vendors must grant access (SuperCat can't add without vendor consent)
- **Time:** 1-2 days

#### Email/Username Changes (25 tickets)
- **Request:** "Need to update user's email address or username"
- **Example:** Ticket #13826 - "Change web login" (8-message thread) - New owner, need to change email from vstone@villagedesigngroup.com to admin@villagedesigngroup.com
- **Complexity:** Discovered duplicate accounts (vstone and vstone4), can't merge accounts, must choose workaround
- **Example:** Ticket #13832 - "email address and phone number" - Rep's CC line showing personal email (darlarpritchard@gmail.com) instead of work email
- **Issue:** iPad using wrong default email in Mail app
- **Resolution:** Explain iPad Mail app settings, how to change default account
- **Time:** 1-3 days

#### Account Merging Requests (9 tickets)
- **Request:** "User has multiple accounts, want to merge them"
- **Example:** Ticket #13518 - "Issues logging in to Various Vendors" (9-message thread)
- **Issue:** User has accounts with different emails across vendors
- **Resolution:** Can't merge accounts from SuperCat side, must reach out to each vendor
- **Explanation:** Deleting accounts loses all unsaved data (projects, lists, local customers, unsubmitted orders)
- **Time:** 2-3 days

#### Removing Vendors from Account (3 tickets)
- **Request:** "Remove vendor X from my eCat"
- **Example:** Ticket #13541 - "Removing factories from my ecat"
- **Example:** Ticket #13544 - "eCat Account" - Remove Elk Home from multiple users
- **Resolution:** Disable user accounts for specific vendors
- **Time:** 1-2 days

#### Email Configuration Issues (4 tickets)
- **Request:** "Emails sending from wrong address"
- **Example:** Ticket #13640 - "E cat" - Emails sending from personal email instead of business
- **Example:** Ticket #13832 - CC line showing wrong email
- **Issue:** iPad has multiple email accounts, using wrong default
- **Resolution:** iPad Settings → Mail → set default account, use Apple Mail (not Gmail/Outlook apps)
- **Time:** Same day

---

### 2. Training / How-To Questions (70 tickets - 20.1%)

**What Customers Actually Need:**

#### Barcode/Scanning Questions (2 tickets)
- **Request:** "How do I set up barcode scanning?"
- **Example:** Ticket #13902 - "Syncing Barcode Values in Product Uploads"
- **Issue:** Added ScanValue to product file, but can't search for it in app
- **Explanation:** Two different scanning methods:
  1. Search bar scanning: Needs value in `keywords` field
  2. Direct-to-order scanning: Uses `ScanValue` field (select customer → view order → tap scan button)
- **Resolution:** Loom video with 5-step screenshot guide
- **Time:** 1-2 days

#### Group Scanning Setup (1 ticket)
- **Request:** "Can I scan one tag to pull up entire product family?"
- **Example:** Ticket #13901 - "Ecat Question" (9-message thread)
- **Issue:** 400 new intros, don't want 400 tags in showroom, want 1 tag per family (50 families)
- **Solution:** Use `ScanGroupCode` field in product file
- **Also suggested:** Smart lists in showroom walkthrough order
- **Resolution:** KB article + explanation of implementation
- **Time:** 3-4 days (back-and-forth on setup)

#### App Update Questions (1 ticket)
- **Request:** "How often does eCat update? Why isn't my data updating?"
- **Example:** Ticket #13894 - "ECAT and updates" (7-message thread)
- **Questions:**
  - "Do you charge extra for additional data pushes?"
  - "Why do some vendors update daily while others don't?"
  - "Should updates be automatic?"
- **Explanation:**
  - No charge for data pushes
  - Vendor controls update frequency
  - App auto-updates when you tap vendor (if online)
  - Manual refresh needed if you opened vendor while offline
- **Time:** 2-3 days

#### Price Level Configuration (6 tickets)
- **Request:** "How do I configure price levels?"
- **Example:** Ticket #13889 - "Price level issues" (11-message thread)
- **Example:** Ticket #13887 - "Schonbek eCat pricing issue" - Currency showing wrong (USD vs CAD)
- **Example:** Ticket #13867 - "FW: ECat" - Finding second price level configuration
- **Resolution:** Admin console screenshots, price level settings explanation
- **Time:** 2-5 days

#### Smart List Questions (2 tickets)
- **Request:** "How do I create/use smart lists?"
- **Example:** Ticket #13492 - "Smart list" (7-message thread)
- **Resolution:** Loom video walkthrough, resolved via meeting
- **Time:** 3-5 days

#### QR Code Generation (1 ticket)
- **Request:** "Can I create QR code for smart list?"
- **Example:** Ticket #13830 - "WAC Showroom: Lightovation"
- **Resolution:** Yes, KB article with instructions
- **Time:** 1 day

#### Inventory Display Setup (2 tickets)
- **Request:** "How do I show inventory to customers?"
- **Example:** Ticket #13579 - "Customer Inventory"
- **Example:** Ticket #13817 - "Before I forget" - Track showroom inventory during market
- **Resolution:** Display Inventory Setup documentation, ShowroomLocation field in customers.csv
- **Time:** 1-2 days

#### Report Generation (5 tickets)
- **Request:** "How do I generate reports? What reports are available?"
- **Example:** Ticket #13528 - "eCat standard reports"
- **Example:** Ticket #13885 - "Report Request" - Want rep usage data, customer order data
- **Resolution:** Tools menu screenshot, Orders → Reports, CSV export instructions
- **Time:** 1-2 days

#### Email Notification Configuration (2 tickets)
- **Request:** "How do I set up order email notifications?"
- **Example:** Ticket #13829 - "ET2 ECat email notification"
- **Resolution:** KB article on email configuration
- **Time:** 1 day

#### Feature Availability Questions (10 tickets)
- **Request:** "Can eCat do X?"
- **Example:** Ticket #13870 - "ECat" - "Can we show invoices and orders in eCat?"
- **Answer:** "No easy way without lots of manual work"
- **Example:** Ticket #13869 - "eCat Sales Portal check in" - "Can reps send suggested product lists based on purchase history?"
- **Resolution:** Explanation of current capabilities, workarounds if available
- **Time:** 1-2 days

#### Logo/Branding Upload (3 tickets)
- **Request:** "How do I upload logo/branding images?"
- **Example:** Ticket #13558 - "Support Request - Brand Image Upload"
- **Resolution:** Tools → Import Images → Nav Panel Logo / Logo Button / Branding Image
- **Time:** 1 day

#### Order Review Questions (2 tickets)
- **Request:** "How do I review orders?"
- **Example:** Ticket #13540 - "review order question"
- **Resolution:** Show where to find order review functionality
- **Time:** Same day

#### Hiding Price on Reports (1 ticket)
- **Request:** "How do I remove price from printed reports?"
- **Example:** Ticket #13495 - "how can i get rid of the price that shows up on this report?"
- **Resolution:** Checkbox settings explanation
- **Time:** 1 day

#### Territory Code Setup (1 ticket)
- **Request:** "How do I assign territory codes?"
- **Example:** Ticket #13339 - "Help please"
- **Resolution:** Customer file territory code field + admin console assignment
- **Time:** 1-2 days

---

### 3. Sales & Finance (46 tickets - 13.2%)

**What Customers Actually Need:**

#### Company Information Verification (2 tickets)
- **Request:** "Third party needs to verify SuperCat company info"
- **Example:** Ticket #13888 - "Verify Company Information - Ferguson" - Vendor Data Department needs info for ACH payment setup
- **Resolution:** Provide company information
- **Time:** Same day

#### Invoice Questions (10+ tickets)
- **Request:** "Questions about SuperCat invoices"
- **Example:** Ticket #13639 - "Fw: New invoice from SuperCat Solutions" - Customer negotiating annual discount
- **Example:** Ticket #13633 - "Fw: New invoice" - International wire payment confirmation
- **Example:** Ticket #13546 - "Fw: New invoice" - Request revised invoice with annual term date
- **Resolution:** Invoice modifications, payment confirmations
- **Time:** 1-2 days

#### Pricing Inquiries (5+ tickets)
- **Request:** "How much does eCat Online cost?"
- **Example:** Ticket #13828 - "eCat Online Pricing Request"
- **Resolution:** Overview of add-on services and pricing
- **Time:** Same day

#### Payment Processing (5+ tickets)
- **Request:** "Payment confirmations, remittance advice"
- **Example:** Ticket #13647 - "Confirmations pour la Transaction" - Forwarded to accounting
- **Resolution:** Forward to appropriate department
- **Time:** Same day

---

### 4. Data Sync / Imports (41 tickets - 11.7%)

**What Customers Actually Need:**

#### Import Error Troubleshooting (10 tickets)
- **Request:** "Getting error when importing file"
- **Example:** Ticket #13827 - "error on import"
- **Resolution:** Loom video showing how to read and fix validation errors
- **Time:** 1-2 days

#### FTP Credentials (2 tickets)
- **Request:** "Need FTP credentials to upload files"
- **Example:** Ticket #13532 - "Millennium Lighting - SFTP Credentials"
- **Resolution:** Provide FTP credentials via secure link (expires in 7 days)
- **Time:** Same day

#### File Upload Questions (5 tickets)
- **Request:** "How do I upload files? What format?"
- **Resolution:** KB articles on file formats, import process
- **Time:** 1-2 days

#### Collections Not Showing (3 tickets)
- **Request:** "Collections not appearing after upload"
- **Example:** Ticket #13908 - "Issues with Collections showing up in catalog"
- **Issue:** New collections don't auto-select into user groups
- **Resolution:** Manual selection required in admin console
- **Time:** 1 day

#### Order Integration Questions (2 tickets)
- **Request:** "How do orders flow into our system?"
- **Example:** Ticket #13642 - "eCat Orders"
- **Resolution:** Explanation of push vs pull API options
- **Time:** 1 day

---

### 5. Image Assets (20 tickets - 5.7%)

**What Customers Actually Need:**

#### Missing Images After Upload (10 tickets)
- **Request:** "Images not showing up after I uploaded them"
- **Example:** Ticket #13839 - "Some other questions!" - 10+ SKUs with missing images
- **Two error types:**
  1. **No filename specified** in ImageFileName column
  2. **Filename specified but file not uploaded** or name mismatch
- **Resolution:** Loom video showing missing images report (Tools → Missing Images), how to fix both error types
- **Time:** 1-3 days

#### Logo/Branding Image Updates (5 tickets)
- **Request:** "Need to update company logo"
- **Example:** Ticket #13651 - "Image/Logo change"
- **Resolution:** Tools → Import Images → Nav Panel Logo / Logo Button / Branding Image
- **Time:** Same day

#### Image File Format Issues (2 tickets)
- **Request:** "Images not importing correctly"
- **Example:** Ticket #13796 - "B+P Supercat Image Issues" - SVG files saved as JPG
- **Resolution:** Engineering deleted problematic files, guidance on proper formats
- **Time:** 1-2 days

#### Image Copy Requests (2 tickets)
- **Request:** "Copy images from one org to another"
- **Example:** Ticket #13850 - "Another eCat request" - Canadian distributor needs Universal's images
- **Resolution:** One-time image copy process (requires vendor permission)
- **Time:** 2-3 days

---

### 6. Feature Requests (16 tickets - 4.6%)

**What Customers Actually Want:**

#### Order Status Visibility
- **Request:** "Show order status in system"
- **Example:** Ticket #13900 - "Order status information"
- **Resolution:** Logged for product roadmap

#### Email Template Customization
- **Request:** "Can I customize order confirmation emails?"
- **Example:** Ticket #13851 - "FW: Wendover Order" - Want to use OrderType variable in emails
- **Resolution:** Yes, OrderType can change word between "Confirmed" and "Quote" but can't change sentences/layouts

#### Sales Portal Enhancements
- **Request:** "Can reps send suggested product lists based on purchase history?"
- **Example:** Ticket #13869 - "eCat Sales Portal check in"
- **Resolution:** Explanation of current capabilities, logged for consideration

#### Default Order Type Setting
- **Request:** "Can I set default order type based on user group?"
- **Example:** Ticket #13898 - "eCat online"
- **Resolution:** Yes, can set default to "Quote" or create new order type

---

### 7. Configuration Issues (10 tickets - 2.9%)

**What Customers Actually Need:**

#### User Group Permission Setup
- **Request:** "How do I configure user group permissions?"
- **Example:** Ticket #13645 - "Jamie Young Enrollment Field - Add Customer Type Option"
- **Resolution:** Admin console configuration guidance
- **Time:** 2-3 days

#### Email Notification Settings
- **Request:** "Configure email notification settings"
- **Example:** Ticket #13829 - "ET2 ECat email notification"
- **Resolution:** KB article, configuration steps
- **Time:** 1 day

---

### 8. Orders / Invoices (6 tickets - 1.7%)

**What Customers Actually Need:**

#### Order Integration Questions
- **Request:** "How do orders flow into our ERP?"
- **Example:** Ticket #13635 - "Ecat Orders not flowing into SAP" (13-message thread)
- **Resolution:** Troubleshooting order integration, verification
- **Time:** 3-5 days

#### Order Email Issues
- **Request:** "Order confirmation emails not sending"
- **Example:** Ticket #13810 - "Possible Order Email Issue" (11-message thread)
- **Resolution:** Email settings verification
- **Time:** 2-4 days

---

### 9. Password Reset Specific Tag (10 tickets - 2.9%)

**What Customers Actually Need:**

#### Password Reset Email Not Received
- **Request:** "Didn't get password reset email"
- **Example:** Ticket #13520 - "Capital Lighting FW: Ecat login trouble"
- **Example:** Ticket #13518 - "Issues logging in to Various Vendors"
- **Example:** Ticket #13361 - "Not Receiving Password Reset Emails" (8-message thread)
- **Resolution:** Resend password reset, check spam, verify email address
- **Time:** Same day to 2 days

---

### 10. Sales/Finance - eCat Online Pricing (5 tickets - 1.4%)

**What Customers Actually Need:**

#### eCat Online Pricing Questions
- **Request:** "How much does eCat Online cost?"
- **Example:** Ticket #13828 - "eCat Online Pricing Request"
- **Resolution:** Overview of add-on services and pricing structure
- **Time:** Same day

---

## Common Patterns & Insights

### Pattern 1: Voice Messages = Urgent Password Resets
- **11 voice message tickets**, all for password resets
- Indicates users need immediate access
- Often have meetings or time-sensitive needs
- Example: "He is over 70 years old and has a meeting at 10"

**Recommendation:** Self-service password reset would eliminate these urgent calls

---

### Pattern 2: iPad Email Configuration Confusion
- **Multiple tickets** about emails sending from wrong address
- **Root cause:** iPad has multiple email accounts (personal + business)
- **Common issue:** Using Gmail app or Outlook app instead of Apple Mail
- **Resolution:** Always same guidance:
  1. Use Apple Mail (not third-party apps)
  2. Set business email as default in iPad Settings → Mail
  3. Can tap email address in draft to change per-message

**Recommendation:** Create visual guide for iPad email setup, add to onboarding

---

### Pattern 3: Rep Enrollment Process Confusion
- **Multiple tickets** from reps who didn't receive enrollment links
- **Issue:** Reps think SuperCat can grant vendor access
- **Reality:** Vendors must grant access, SuperCat can only create account shell
- **Resolution:** Explain vendor must add them, provide username to give to vendor

**Recommendation:** Clarify enrollment process in rep communications

---

### Pattern 4: Account Merging Not Possible
- **9+ tickets** requesting account merges
- **Issue:** Users have multiple accounts across vendors
- **Reality:** Can't merge accounts without losing data
- **Workarounds:**
  1. Update primary account email, delete secondary (loses data)
  2. Keep both accounts separate
  3. Contact each vendor individually

**Recommendation:** Build account merging capability or improve multi-account management

---

### Pattern 5: Pricing Configuration Confusion
- **6 tickets** about price level setup
- **Common confusion:**
  - User group vs customer contract pricing
  - Multiple price levels per user group
  - Currency settings
  - Base price level vs actual price levels
- **Resolution:** Admin console screenshots, detailed explanations

**Recommendation:** Simplify pricing configuration UI, add pricing wizard

---

### Pattern 6: "How To" Questions Indicate Documentation Gaps
- **30 general "question" tickets**
- **Topics:**
  - How to configure features
  - How to generate reports
  - How to set up scanning
  - How to display inventory
  - How to create smart lists
  - How to upload logos

**Recommendation:** Expand KB with top 20 how-to articles, add contextual help in UI

---

### Pattern 7: Loom Videos Highly Effective
- **Multiple tickets** resolved with Loom videos
- **Used for:**
  - Barcode scanning (step-by-step)
  - Missing images troubleshooting
  - Admin console navigation
  - Feature configuration
- **Result:** Reduces back-and-forth, visual learners benefit

**Recommendation:** Create Loom library for top 20 tasks

---

### Pattern 8: Trade Account Registration Issues
- **Multiple tickets** about "Apply for Trade Account" button
- **Issue:** Links pointing to customer's WordPress sites, not SuperCat pages
- **Resolution:** Update URL configuration
- **Time:** Same day

**Recommendation:** Standardize trade account registration flow

---

### Pattern 9: Frequent Password Resets
- **Multiple tickets** about users having to reset password frequently
- **Root causes:**
  1. Two users sharing same login, resetting back and forth
  2. User thinks each vendor has different password, keeps resetting
  3. IT policy or password manager forcing resets
- **Reality:** eCat never prompts for password changes

**Recommendation:** Add password education, show which vendors share same login

---

### Pattern 10: Multiple Accounts Across Vendors
- **Common issue:** Users have different accounts for different vendors
- **Causes confusion** when trying to log in
- **Can't merge** without losing data

**Recommendation:** Unified account management, show all vendor access in one place

---

## Request Type Breakdown

### By Complexity

#### Single-Touch (Quick)
- Password resets via email: 20 tickets
- FTP credentials: 2 tickets
- Simple configuration updates: 15 tickets
- **Total:** ~37 tickets (10.6%)

#### 2-4 Messages (Standard)
- User account setup: 13 tickets
- Email configuration: 10 tickets
- Simple how-to questions: 25 tickets
- **Total:** ~48 tickets (13.8%)

#### 5-9 Messages (Moderate)
- Email/username changes: 15 tickets
- Price level configuration: 6 tickets
- Account merging attempts: 9 tickets
- **Total:** ~30 tickets (8.6%)

#### 10+ Messages (Complex but still L1)
- Multi-step troubleshooting: 10 tickets
- Complex configuration: 8 tickets
- **Total:** ~18 tickets (5.2%)

---

## Top 15 Specific Request Types (By Frequency)

1. **Password Reset / Forgot Login** - 37 tickets
   - Voice messages, email requests, expired reset links
   
2. **General How-To Questions** - 30 tickets
   - "How do I configure X?"
   - "Where do I find Y?"
   
3. **Email/Username Updates** - 25 tickets
   - Change email address
   - Update username
   - Account ownership changes
   
4. **Order-Related Questions** - 23 tickets
   - How orders work
   - Order email issues
   - Order status
   
5. **Account Enrollment Issues** - 21 tickets
   - New rep setup
   - Vendor access requests
   - Registration problems
   
6. **New User Setup** - 13 tickets
   - Create new accounts
   - Provide credentials
   
7. **Image/Logo Updates** - 11 tickets
   - Missing images
   - Logo uploads
   - Image format issues
   
8. **File Import Questions** - 10 tickets
   - Import errors
   - File format questions
   - FTP access
   
9. **Pricing Configuration** - 7 tickets
   - Price level setup
   - Currency settings
   - Price display
   
10. **Report Generation** - 6 tickets
    - What reports available?
    - How to export data?
    
11. **Catalog Link Requests** - 5 tickets
    - Catalog URL requests
    - Link configuration
    
12. **Account Enrollment/Registration** - 4 tickets
    - Registration flow issues
    - Trade account setup
    
13. **Scanning/Barcode** - 2 tickets
    - How to set up scanning
    - Barcode configuration
    
14. **Company Info Verification** - 2 tickets
    - Third-party verification requests
    
15. **Remove Vendor Access** - 3 tickets
    - Remove factories from account

---

## Resolution Methods

### Email-Only (70%)
- Password resets
- Simple configuration updates
- FTP credentials
- Quick how-to answers

### Email + Screenshots (15%)
- Admin console navigation
- Configuration guidance
- Error message explanation

### Email + Loom Video (10%)
- Barcode scanning
- Missing images
- Feature walkthroughs
- Complex configurations

### Email + KB Article (5%)
- Standard procedures
- Feature documentation
- Setup guides

---

## Key Recommendations

### Immediate Impact (High Volume, Low Complexity)

#### 1. Self-Service Password Reset (37 tickets)
- **Current:** Users call/email, support sends reset link
- **Proposed:** "Forgot Password" link on login page
- **Impact:** Eliminate 10.6% of L1 tickets, reduce voice messages
- **Urgency:** High - users have time-sensitive needs

#### 2. iPad Email Configuration Guide (10+ tickets)
- **Current:** Repeated explanations of Apple Mail setup
- **Proposed:** Visual guide with screenshots/GIF
- **Content:**
  - Use Apple Mail (not Gmail/Outlook apps)
  - Set default email in iPad Settings
  - How to change per-message
- **Impact:** Reduce repetitive email configuration tickets
- **Location:** KB article + onboarding checklist

#### 3. Rep Enrollment Process Clarification (21 tickets)
- **Current:** Reps confused about enrollment process
- **Proposed:** Clear enrollment flow documentation
- **Content:**
  - SuperCat creates account shell
  - Vendor must grant access
  - What to provide to vendor (username, email)
- **Impact:** Reduce enrollment confusion tickets

#### 4. Account Management Improvements (25 tickets)
- **Current:** Can't merge accounts, manual email changes
- **Proposed:** 
  - Account merging capability
  - Self-service email updates
  - Unified vendor access view
- **Impact:** Reduce account management tickets by 50%

#### 5. Pricing Configuration Wizard (7 tickets)
- **Current:** Complex admin console settings, long threads
- **Proposed:** Step-by-step pricing setup wizard
- **Content:**
  - User group vs customer contract pricing
  - Currency settings
  - Price level hierarchy
- **Impact:** Reduce pricing configuration confusion

---

### Medium-Term (Documentation & Training)

#### 6. Expand Knowledge Base (30 how-to tickets)
- **Top articles needed:**
  - How to set up barcode scanning (both methods)
  - How to configure price levels
  - How to create smart lists
  - How to display inventory
  - How to generate reports
  - How to upload logos/branding
  - How to configure email notifications
  - How to set up QR codes
  - How to review orders
  - How to assign territory codes

#### 7. Loom Video Library (Current: Ad-hoc)
- **Create videos for:**
  - Barcode scanning (2 methods)
  - Missing images troubleshooting
  - Admin console navigation
  - Price level configuration
  - User group setup
  - iPad email configuration
  - Smart list creation
  - Report generation

#### 8. In-App Contextual Help
- **Add help links** in key areas:
  - Price level configuration page
  - User group settings
  - Import pages
  - Report generation

---

### Long-Term (Product Improvements)

#### 9. Account Merging Capability
- **Current:** Can't merge accounts without losing data
- **Proposed:** Safe account merging that preserves data
- **Impact:** Eliminate 9+ tickets per 180 days

#### 10. Unified Vendor Access Dashboard
- **Current:** Users don't know which vendors they have access to
- **Proposed:** Dashboard showing all vendor access in one place
- **Impact:** Reduce confusion, improve user experience

---

## Success Metrics

### Ticket Volume Reduction Targets

#### Password Resets (37 tickets → 5 tickets)
- **Target:** 85% reduction via self-service
- **Measure:** Voice messages eliminated
- **Timeline:** 30 days to implement

#### Email Configuration (10 tickets → 2 tickets)
- **Target:** 80% reduction via visual guide
- **Measure:** Repeat questions eliminated
- **Timeline:** 30 days to create guide

#### How-To Questions (30 tickets → 15 tickets)
- **Target:** 50% reduction via expanded KB
- **Measure:** KB article views increase
- **Timeline:** 90 days to create top 20 articles

#### Account Management (25 tickets → 10 tickets)
- **Target:** 60% reduction via self-service + merging
- **Measure:** Email change requests reduced
- **Timeline:** 180 days for full implementation

### Overall L1 Ticket Reduction
- **Current:** 349 tickets per 180 days
- **Target:** 250 tickets per 180 days (28% reduction)
- **Focus:** Automate top 4 categories (password, email config, enrollment, account management)

---

## Conclusion

The L1/first-touch support analysis reveals that **35.5% of straightforward support requests are user management tasks** (passwords, account setup, email changes), and **20.1% are training/how-to questions**. Together, these represent **55.6% of all L1 tickets**.

### Key Findings:

1. **Password resets are urgent** (voice messages indicate time-sensitivity)
2. **iPad email configuration is repeatedly misunderstood** (Apple Mail vs third-party apps)
3. **Rep enrollment process causes confusion** (who grants access)
4. **Account merging is frequently requested but impossible**
5. **Pricing configuration requires extensive explanation**
6. **How-to questions indicate documentation gaps**

### Highest ROI Opportunities:

1. **Self-service password reset** - Eliminate 37 tickets (10.6%)
2. **iPad email setup guide** - Eliminate 10 tickets (2.9%)
3. **Rep enrollment clarification** - Eliminate 21 tickets (6.0%)
4. **Expanded KB articles** - Eliminate 15 tickets (4.3%)

**Total potential reduction: 83 tickets (23.8%) with relatively simple improvements.**

---

## Appendix: Methodology

### Data Collection
- **Source:** BigQuery - Hevo Dataset
- **Date Range:** August 1, 2025 - January 29, 2026 (180 days)
- **Filters:**
  - Mailbox: `support@supercatsolutions.com` only
  - Tags: `l1 - handled by frontline support` OR `first-touch resolved`
  - Excluded: Engineering issues, bugs, complex integrations

### Analysis Approach
1. Extracted 349 L1/first-touch tickets
2. Analyzed tags to categorize by type
3. Read thread bodies to understand actual customer requests
4. Identified specific examples with ticket numbers
5. Documented resolution patterns and time to resolution

---

**Report Generated:** January 29, 2026  
**Focus:** Common, straightforward support requests only  
**Next Review:** July 29, 2026 (180 days)
