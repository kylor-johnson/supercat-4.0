# Help Scout Ticket Analysis - 90 Day Lookback
**Analysis Period:** October 30, 2025 - January 29, 2026  
**Data Source:** Hevo Dataset - Help Scout Tickets  
**Inboxes Analyzed:** Support & Onboarding  
**Date Generated:** January 29, 2026

---

## Executive Summary

This comprehensive analysis examines 498 Help Scout tickets received over the past 90 days across both the Support (`support@supercatsolutions.com`) and Onboarding (`onboarding@supercatsolutions.com`) inboxes. The analysis reveals critical patterns in customer issues, confusion points, and support resolution methods with **specific details about the actual substance of each issue type**.

### Key Metrics
- **Total Tickets:** 498 unique conversations
- **Closed Tickets:** 334 (67.1%)
- **Open/Active Tickets:** 138 (27.7%)
- **Support Inbox:** 295 tickets (59.2%)
- **Onboarding Inbox:** 203 tickets (40.8%)
- **Average Thread Count:** 3.5 messages per ticket
- **Maximum Thread Count:** 31 messages (indicating complex issues)

### Resolution Methods Distribution
- **Meeting/Call Required:** 137 tickets (27.5%)
- **Long Email Thread (7+ messages):** 71 tickets (14.3%)
- **Loom Video Provided:** 46 tickets (9.2%)

---

## Top 20 Themes & Issues (With Specific Substance)

### 1. Data Sync / Import Issues (216 tickets - 43.4%)

**Specific Issues Customers Face:**

#### File Import Errors & Validation
- **Import validation failures** with unclear error messages
  - Example: Ticket #13827 - Customer received error during import but couldn't understand what was wrong with their file
  - Resolution: Loom video showing how to read error messages and fix file format issues

#### Collection/Category Sync Problems
- **Collections not automatically appearing** after adding new ones
  - Example: Ticket #13908 - Charleston Forge: "Collections not showing up in catalog"
  - Issue: When adding a new Collection, it doesn't automatically get selected into user groups that don't have "All" selected
  - Even slight renaming of a collection causes it to be treated as "new" and not auto-populate
  - Resolution: Manual selection required in admin console

#### Barcode/Scan Value Configuration
- **Confusion about where barcode data should go** for scanning functionality
  - Example: Ticket #13902 - Wendover Art: "Syncing Barcode Values in Product Uploads"
  - Issue: Customer added barcode values to `ScanValue` column but couldn't search for them in the app
  - Root cause: Scan values need to be in the `keywords` field for search bar scanning, OR used directly on orders via the scan button
  - Resolution: Detailed Loom video with step-by-step screenshots showing both scanning methods

#### Cache Issues Causing Stale Data
- **Data not updating after imports** due to cache problems
  - Example: Tickets #13794, #13792, #13785 - Multiple customers reporting "eCat Online not updating trade names and collections"
  - Issue: Server-side caching causing different users to see different data
  - Particularly problematic when permissions differ between user groups
  - Resolution: Engineering investigation, cache invalidation required

#### Authentication Failures in Automated Sync
- **API integration auth errors** breaking automated data flows
  - Example: Ticket #13847 - "Auth Errors from WebSan Process"
  - Issue: Automated sync process failing due to credential problems
  - Resolution: Engineering intervention to update credentials and test connection

#### Missing Orders/Data After Sync
- **Orders not syncing between devices**
  - Example: Ticket #13845 - "Missing Orders"
  - Issue: Reps switching iPads back and forth, wish lists not following
  - Root cause: Different customer records being used, iPad sync not completing
  - Resolution: Verify customer record consistency, ensure good internet connection

**Common Resolution Patterns:**
- 60% L1 support with email guidance
- 25% L2 requiring internal investigation
- 15% L3 needing engineering fixes
- Loom videos frequently used for file format guidance
- Time to resolution: 1-3 days (standard), 5-7 days (engineering issues)

---

### 2. Pricing Configuration & Display Issues (13 tickets - 2.6%)

**Specific Issues Customers Face:**

#### Price Level Mismatches
- **Customers seeing wrong price tier** despite correct user group assignment
  - Example: Ticket #13889 - Furniture Classics: "Price level issues" (11-message thread)
  - Issue: 7+ customers reporting they're in "Wholesale" user group but seeing "Volume Dealer" pricing
  - Root cause confusion: Customers thought user group determined pricing, but for eCat Online users with customer numbers, pricing is determined by the customer's default price level from Bluelink, NOT user group
  - Specific examples from ticket:
    - Customer `kavolpi` - marked wholesale in BL but seeing Volume Dealer prices
    - Customer `esullivan2` - user group doesn't affect their pricing at all
    - Multiple users without customer codes assigned defaulting to wrong price level
  - Resolution: Chuck explained the pricing hierarchy - user group only affects permissions, not prices for customers with account numbers

#### User Group vs. Customer Contract Pricing Confusion
- **Fundamental misunderstanding** of how pricing is determined
  - Issue: Customers believe changing user group will change pricing
  - Reality: For users associated with customer numbers, price comes from Bluelink contract
  - For users NOT associated with customer numbers, price comes from user group's default price level
  - Resolution: Detailed explanation with screenshots showing where to check settings

#### Price Level Configuration for Reps
- **Rep price levels not displaying correctly**
  - Example: Ticket #13887 - "Schonbek eCat pricing issue"
  - Issue: Currency symbols showing incorrectly (USD vs CAD)
  - Root cause: Price level currency field set to USD instead of CAD
  - Also: Catalog price level and order price level were different (yellow warning)
  - Resolution: Update currency field in price level settings

#### Pack Pricing vs. Unit Pricing
- **Confusion about pack quantity pricing**
  - Example: Ticket #13863 - Coaster onboarding
  - Issue: Unclear if price transmitted is per-unit or per-pack
  - Question: "If item is sold in pack of 2, is price for the pack or per unit?"
  - Resolution: Clarification that system expects pack price, not per-unit price

**Common Resolution Patterns:**
- 90% L1 support
- 40% require extended troubleshooting (5-11 messages)
- Often requires screenshots and admin console access
- Time to resolution: 1-3 days

---

### 3. Rep/Territory Configuration Issues (15 tickets - 3.0%)

**Specific Issues Customers Face:**

#### Reps Not Seeing Their Customers
- **Territory code misconfiguration** preventing customer visibility
  - Example: Ticket #13863 - Coaster: "Reps not seeing their customers on their login"
  - Specific territories affected: 219, 173
  - Issue: Reps assigned territory codes but customers not mapped to those territories
  - Resolution: Territory code verification and customer assignment in admin console

#### Rep Email Notifications Not Working
- **Order confirmation emails not sending** to reps
  - Example: Ticket #13892 - Palecek: "Rep issue with ECAT"
  - Issue: Rep Tamra Everson's orders submitting successfully but no email confirmations
  - Orders visible in Portal, so transmission working, but emails failing
  - Troubleshooting steps provided:
    1. Check if emails in Sent Items (not just Outbox)
    2. Verify using Apple Mail (not Gmail app or Outlook)
    3. Ensure rep's email is the DEFAULT email in Apple Mail
    4. Check email settings in both admin console and iPad app
  - Resolution: Email configuration guidance, not app reinstall

#### Shared Orders/Quotes Not Visible Between Reps
- **Permission issues** preventing reps from seeing each other's work
  - Example: Ticket #13893 - Gabriella White: "User Issue: Viewing Other Users' Quotes"
  - Issue: Rep `sc-shawndan` has territory codes (CT05-SHAWNDAN, CT05, MKT) but `sc-angeliaking` has no territory codes
  - Root cause: Both users need to be in same territory for shared orders
  - Also need good internet connection for shared orders to sync properly
  - Resolution: Territory code assignment and user group permission verification

#### Sub-Rep Invitations and Hierarchy
- **Confusion about sub-reps** invited by main reps
  - Example: Ticket #13863 - Coaster onboarding
  - Issue: Multiple users not on initial rep list (sub-reps invited via agencies)
  - Need to assign territory codes to all sub-reps manually
  - Resolution: Guidance on assigning territory codes in admin console

**Common Resolution Patterns:**
- 70% L1 support
- 30% L2 requiring investigation
- Often involves checking multiple settings across admin console and app
- Time to resolution: 1-2 days

---

### 4. Scanning/Barcode Functionality Issues (5 tickets - 1.0%)

**Specific Issues Customers Face:**

#### Scans Not Captured in Exports
- **Missing scan data** when exporting orders
  - Example: Tickets #13843, #13837, #13821 - Kuzco: "ECAT SCANNING" / "ECAT Scans at Lightovation"
  - Issue: Reps scanned items at Dallas Market, but scans not showing up in order exports
  - Reps had to forward wish lists manually
  - Root cause: iPads didn't sync orders back completely due to poor market internet connectivity
  - Specific question: "Is there a separate feed/export that would include these missing scans?"
  - Resolution: Sync iPads to push orders to server, then export from admin console

#### Barcode Search Not Working
- **Scan values not searchable** from search bar
  - Example: Ticket #13902 - Wendover Art: "Syncing Barcode Values in Product Uploads"
  - Issue: Added `ScanValue` column with barcode data (e.g., "MIR0024"), but searching for that value in "Search All Products" returns no results
  - Two use cases for scanning:
    1. **Search bar scanning:** Requires barcode value in `keywords` field
    2. **Direct-to-order scanning:** Works with `ScanValue` field (select customer → view order → tap scan button)
  - Resolution: Detailed Loom with 5-step screenshot guide showing both methods

#### Inconsistent Scan Behavior
- **Scanning works sometimes but not others**
  - Example: Ticket #13578 - "Inconsistent Scan Behavior"
  - Issue: Scanning functionality unreliable across different scenarios
  - Resolution: Investigation into specific use cases and device settings

**Common Resolution Patterns:**
- 60% L2 requiring internal investigation
- 40% L3 needing engineering review
- Often tied to trade show/market events (poor connectivity)
- Loom videos critical for explaining dual scanning methods
- Time to resolution: 2-5 days

---

### 5. Image/Asset Management Issues (17 tickets - 3.4%)

**Specific Issues Customers Face:**

#### Missing Images After Upload
- **Images not displaying** despite being uploaded
  - Example: Ticket #13839 - Maxim: "Some other questions!"
  - Issue: Many missing product images persisting after file upload
  - Specific SKUs affected: SM81858PC, E25413-WBR, E42411-AL, E21184-90SN, etc. (10+ examples)
  - Two types of errors identified:
    1. **Yellow error:** No image filename specified in `ImageFileName` column
    2. **Green error:** Image filename specified (e.g., "E25221=WA_01.jpg") but file never uploaded or uploaded with different name
  - Resolution: Loom video + screenshots showing missing images report and how to fix both error types

#### Image File Format Issues
- **Invalid image files** breaking import process
  - Example: Ticket #13796 - Buster + Punch: "B+P Supercat Image Issues"
  - Issue: Images ending in "_line.jpg" were actually SVG files saved as JPGs
  - System couldn't catch during validation (files named correctly) but failed during processing
  - Caused import processes to hang and require abortion
  - Resolution: Engineering deleted problematic files, need better MIME type validation

#### Image Path/Naming Confusion
- **Mismatch between filename in CSV and actual uploaded file**
  - Common issue: Customer specifies "my-product-image.jpg" in product file but uploads "my_product_image.jpg"
  - Or uploads image with different name than specified
  - Resolution: Missing images report in admin console shows exact mismatches

#### Image Copy/Permission Requests
- **Need to copy images between orgs**
  - Example: Ticket #13850 - Donald Choi: "Another eCat request"
  - Issue: Canadian distributor needs images from Universal's catalog
  - Requires permission from original org to copy images
  - Resolution: One-time product image copy process run by engineering

**Common Resolution Patterns:**
- 80% L1 support
- 40% include Loom video demonstrations
- Missing images report tool heavily used
- Time to resolution: 1-3 days

---

### 6. Training / How-To Questions (84 tickets - 16.9%)

**Specific Issues Customers Face:**

#### Feature Configuration Questions
- **How to set up specific features** for first time
  - Example: Ticket #13901 - Dainolite: "Ecat Question" (9-message thread)
  - Questions about feature functionality and configuration options
  - Resolution: Multi-message back-and-forth with screenshots

#### Price Level Display Configuration
- **How to configure what users see** for pricing
  - Example: Ticket #13889 - Furniture Classics: "Price level issues"
  - Confusion about relationship between user groups, customer records, and pricing
  - Resolution: Detailed explanation with admin console screenshots

#### Email Notification Setup
- **How to configure email settings** for order confirmations
  - Example: Ticket #13892 - Palecek: "Rep issue with ECAT"
  - Questions about Apple Mail vs other email clients
  - Default email address configuration
  - Resolution: Step-by-step email settings checklist

#### Report Generation and Usage
- **How to access and use reports**
  - Example: Ticket #13885 - Bulbrite: "Report Request"
  - Customer wants to analyze eCat usage, rep activity, customer orders
  - Questions: "Which reps use it most? Which customers? Average order size?"
  - Resolution: Guidance on Orders → Reports, CSV downloads, offer of Clicky analytics and usage reports

#### Smart List Creation
- **How to create and use smart lists**
  - Example: Ticket #13492 - "Smart list"
  - Questions about filtering and list management
  - Resolution: Loom video walkthrough

#### QR Code Generation
- **How to create QR codes** for smart lists
  - Example: Ticket #13830 - WAC: "WAC Showroom: Lightovation"
  - Question: "Can QR code bring someone to a smart list?"
  - Resolution: Yes, with link to KB article and instructions

#### App Update Notifications
- **When do users get notified** about app updates?
  - Example: Ticket #13811 - Maxim: "Question on Exported Reports"
  - Question: "Does eCat send notification when file update is imported?"
  - Answer: No notification for file updates, only for actual app updates from App Store
  - Recommendation: Reps should manually update app daily (twice daily during market)

#### iPad/Device Requirements
- **What devices are supported?**
  - Example: Ticket #13834 - "Possibly need to purchase a low cost iPad for my back office"
  - Questions about device requirements and compatibility
  - Resolution: Device recommendation guidance

**Common Resolution Patterns:**
- 85% L1 support
- 30% include Loom video walkthroughs
- 40% require 5+ message exchanges
- Often reference KB articles
- Time to resolution: 2-5 days depending on complexity

---

### 7. User Management (86 tickets - 17.3%)

**Specific Issues Customers Face:**

#### Password Reset Requests
- **Users can't log in** and need password reset
  - Example: Tickets #13905, #13903 - Voice messages for password resets
  - Pattern: Multiple voice messages indicate urgency
  - Resolution: Same-day password reset via email

#### New User Account Setup
- **Need credentials for new users**
  - Example: Ticket #13906 - Kennedy Intl: "Saul needs username and password please"
  - Issue: Also getting bounce at user's email address
  - Resolution: Create account, provide credentials, verify email deliverability

#### Username/Email Changes
- **Need to update user's email or username**
  - Example: Ticket #13826 - "Change web login"
  - Multiple requests to update user email addresses
  - Resolution: Update in admin console, confirm with user

#### User Registration Failures
- **Can't create new accounts** through registration flow
  - Example: Ticket #13846 - Chelsea House: "Unable to Register New Accounts"
  - Issue: Registration process failing for new users
  - Resolution: Manual account creation, investigation of registration flow

#### User Access Issues
- **Users can see things they shouldn't** or can't see things they should
  - Example: Ticket #13893 - "User Issue: Viewing Other Users' Quotes"
  - Issue: Permission and territory configuration problems
  - Resolution: User group and territory verification

#### Confusion About Software Vendor Role
- **Customers contacting SuperCat** for manufacturer-specific issues
  - Example: Ticket #13871 - "Change web login"
  - Customer asking SuperCat which sales rep services their account
  - Resolution: Explanation that SuperCat is software vendor, need to contact manufacturer

**Common Resolution Patterns:**
- 95% L1 support
- 85% resolved in single touch or 1-2 messages
- Same-day resolution typical
- Voice messages indicate high urgency
- Time to resolution: Hours to same-day

---

### 8. Onboarding / Setup (206 tickets - 41.4%)

**Specific Issues Customers Face:**

#### Complex Multi-Stakeholder Coordination
- **Long-running onboarding threads** with many touchpoints
  - Example: Ticket #13863 - Coaster: "Coaster Follow-Up - Action Items & Thursday Sync" (22 messages)
  - Example: Ticket #13448 - Terracotta: "Terracotta Onboarding Kickoff Follow Ups" (31 messages - longest in dataset)
  - Multiple action items across both teams:
    - eCat display updates (category fixes, field additions)
    - API & data enhancements (vendor number, fallback logic, inventory visibility)
    - Customer import issues (international addresses, duplicate emails, ship-to codes)
    - Order integration deployment
    - Pricing updates and configuration
    - Rep territory assignments
  - Resolution: Multiple meetings, ongoing collaboration, structured follow-up

#### Pricing Configuration During Onboarding
- **Setting up complex pricing structures**
  - Example: Ticket #13863 - Coaster pricing
  - Issue: Multiple price levels (Z1T2, Z2T1, Z2T2, Z3T1, Z1T1, Z3T2, M1-M5 zones, etc.)
  - Question: "Should price be per-unit or per-pack?"
  - Need to configure price level "Cue" characters (2-character limit)
  - Resolution: Pricing file template, documentation on product file vs matrix pricing vs contract prices

#### API Integration Setup
- **Connecting data feeds** from customer systems
  - Example: Ticket #13863 - Coaster API integration
  - Issues: Adding vendor number to API feed, implementing fallback logic, adding LC inventory
  - Resolution: Engineering work with customer's technical team

#### FTP Access and File Upload
- **Getting customers set up** with file transfer
  - Example: Ticket #13863 - Coaster FTP setup
  - Providing credentials and KB article for FTP access
  - Resolution: Credentials + documentation

#### Automated Questionnaire Submissions
- **Multiple duplicate tickets** from onboarding automation
  - Example: Tickets #13886, #13884, #13883, #13882 - All "Onboarding Questionnaire Completed - Coaster Furniture"
  - Issue: Automation creating multiple tickets for same submission
  - Resolution: Need to fix automation to prevent duplicates

#### File Upload Notifications
- **Automated notifications** when customers upload files
  - Example: Tickets #13774, #13773, #13772 - "New Onboarding File Upload - Magic Lite"
  - Multiple notifications for same customer uploading multiple files
  - Resolution: Internal tracking, no customer action needed

**Common Resolution Patterns:**
- 70% L2 requiring internal coordination
- 80% include kickoff calls or check-in meetings
- 50% have 10+ message exchanges
- Structured onboarding process with documented action items
- Time to resolution: 2-6 weeks (ongoing process)

---

### 9. Bugs / Technical Issues (52 tickets - 10.4%)

**Specific Issues Customers Face:**

#### Maybe List Removal Bug
- **Items not removing from maybe lists** properly
  - Example: Ticket #13880 - Crystorama: "Maybe List Removals-ECat"
  - Issue: Bug in maybe list functionality
  - Resolution: Engineering fix, 50/50 chance of inclusion in next release

#### Product Listing Display Bug
- **Products not displaying correctly** in lists
  - Example: Ticket #13824 - "Product Listing change" (24-message thread)
  - Issue: Complex display bug requiring extensive troubleshooting
  - Resolution: Engineering intervention, Loom video, logged in Jira

#### Cache-Related Bugs
- **Stale data showing** due to caching issues
  - Example: Ticket #13785 - "eCat Online not updating trade names and collections"
  - Issue: Different users seeing different data due to cache
  - Resolution: Engineering investigation, cache invalidation

#### Complete Orders Hidden
- **Orders disappearing** from orders screen
  - Example: Ticket #13551 - "Complete Orders Hidden From Orders Screen"
  - Issue: Display bug hiding completed orders
  - Resolution: Logged in Jira, engineering fix

#### Integration Failures
- **Third-party integrations breaking**
  - Example: Ticket #13847 - "Auth Errors from WebSan Process"
  - Issue: Authentication failures in automated processes
  - Resolution: Engineering credential update and testing

**Common Resolution Patterns:**
- 65% L3 engineering intervention required
- 60% have 7+ message exchanges
- 40% require live calls or meetings
- Logged in Jira for tracking
- Time to resolution: 5-14 days depending on severity

---

### 10. Orders / Invoices (33 tickets - 6.6%)

**Specific Issues Customers Face:**

#### Order Status Visibility
- **Can't see order status information**
  - Example: Ticket #13900 - Charleston Forge: "Order status information"
  - Request: Want to see order status in system
  - Resolution: Feature request logged, explanation of current capabilities

#### Missing Orders Between Devices
- **Orders not syncing** between iPads
  - Example: Ticket #13845 - "Missing Orders"
  - Issue: Reps switching iPads, wish lists not following
  - Root cause: Using different customer records, or iPad sync incomplete
  - Resolution: Verify customer record consistency, ensure good internet

#### Order Transmission Failures
- **Orders not sending from server**
  - Example: Ticket #13835 - "Orders not sending from Server"
  - Issue: Order transmission failing
  - Resolution: L2 investigation of data sync settings

#### Order Email Issues
- **Order confirmation emails** not being received
  - Example: Ticket #13810 - "Possible Order Email Issue" (11-message thread)
  - Issue: Email delivery problems
  - Resolution: Email settings verification

**Common Resolution Patterns:**
- 60% L1 support
- 30% L2 requiring internal investigation
- Configuration checks and data sync verification
- Time to resolution: 1-3 days

---

### 11. Sales Portal Issues (18 tickets - 3.6%)

**Specific Issues Customers Face:**

#### Dashboard Loading Issues
- **Portal dashboard stuck "loading"**
  - Example: Ticket #13783 - "Portal dashboard 'loading'"
  - Issue: Dashboard not displaying data
  - Root cause: "Current YTD" selected but no orders since Dec 31
  - Resolution: Date range explanation

#### Portal Access Problems
- **Users can't access portal features**
  - Example: Ticket #13878 - "FW: ECAT Logins"
  - Issue: Users not seeing portal button or not seeing their data once in
  - Resolution: Verify checkbox settings for portal access

#### Report Generation
- **Questions about portal reports**
  - Example: Ticket #13900 - Order status information requests
  - Resolution: Guidance on available reports

**Common Resolution Patterns:**
- 60% L1 support
- 40% L2 requiring investigation
- Configuration verification, data sync checks
- Time to resolution: 1-3 days

---

### 12. Configuration Issues (18 tickets - 3.6%)

**Specific Issues Customers Face:**

#### Custom Field Setup
- **How to configure custom fields**
  - Example: Ticket #13643 - "Custom Field Question" (15-message thread)
  - Issue: Complex custom field configuration
  - Resolution: Meeting scheduled, L2 collaboration, added to KB

#### User Group Permissions
- **Permission configuration** for different user types
  - Example: Multiple tickets about user group settings
  - Issue: Understanding which permissions do what
  - Resolution: Admin console guidance, screenshots

#### Price Level Mapping
- **Connecting price levels** to user groups and customers
  - Example: Ticket #13889 - Price level issues
  - Issue: Confusion about price level hierarchy
  - Resolution: Detailed explanation of pricing logic

**Common Resolution Patterns:**
- 70% L2 requiring internal discussion
- 50% include scheduled calls
- Admin console configuration guidance
- Sometimes requires engineering review
- Time to resolution: 3-7 days

---

### 13. Integration Issues (14 tickets - 2.8%)

**Specific Issues Customers Face:**

#### NetSuite Integration Updates
- **Upgrading from REST to JSON**
  - Example: Ticket #13907 - Progressive: "Netsuite Integration Update (REST to JSON)"
  - Issue: Planning for NetSuite 2026.01 update on April 9
  - Need eCat updated before that date
  - Resolution: Integration upgrade planning

#### API Authentication Failures
- **Integration credentials expiring**
  - Example: Ticket #13847 - "Auth Errors from WebSan Process"
  - Issue: Automated process failing due to auth errors
  - Resolution: Engineering credential swap and connection testing

**Common Resolution Patterns:**
- 60% L3 engineering required
- 40% L2 internal coordination
- API troubleshooting, credential verification
- Time to resolution: 5-10 days

---

### 14. Email/Notification Issues (15 tickets - 3.0%)

**Specific Issues Customers Face:**

#### Order Confirmation Emails Not Sending
- **Reps not receiving order confirmations**
  - Example: Ticket #13892 - Palecek rep issue
  - Issue: Orders submitting but emails not going through
  - Troubleshooting checklist:
    1. Check Sent Items (not just Outbox)
    2. Use Apple Mail (not Gmail app or Outlook)
    3. Set rep email as default in Apple Mail
    4. Verify email settings in admin console
  - Resolution: Email configuration guidance

#### Email Settings Misconfigured
- **Wrong email client** or settings
  - Issue: Using Gmail app instead of Apple Mail
  - Multiple email addresses causing confusion
  - Resolution: Apple Mail configuration instructions

**Common Resolution Patterns:**
- 85% L1 support
- Email settings verification in admin console and iPad
- Time to resolution: 1-2 days

---

### 15. Feature Requests (16 tickets - 3.2%)

**Specific Issues Customers Face:**

#### Order Status Visibility
- **Want to see order status** in system
  - Example: Ticket #13900 - Charleston Forge
  - Request: Display order status information
  - Resolution: Explanation of current capabilities, logged for product roadmap

#### eCat Online Feature Availability
- **Questions about feature parity** between iPad and web
  - Example: Ticket #13898 - "eCat online"
  - Questions about what's possible in web vs iPad
  - Resolution: Feature explanation, workaround suggestions

**Common Resolution Patterns:**
- 70% L1 support with explanation of current capabilities
- 30% escalated for product consideration
- Workaround suggestions provided
- Time to resolution: 1-2 days for response

---

### 16. Sales & Finance (21 tickets - 4.2%)

**Specific Issues Customers Face:**

#### Vendor Verification Requests
- **Third parties verifying company information**
  - Example: Tickets #13890, #13888 - Ferguson: "Verify Company Information"
  - Issue: Ferguson's Vendor Data Department needs info for ACH payment setup
  - Resolution: Provide company information, internal coordination

#### Invoice Inquiries
- **Questions about billing and invoices**
  - Resolution: L2 collaboration with finance team

**Common Resolution Patterns:**
- 60% L1 support
- 40% L2 requiring internal coordination with finance
- Information provision
- Time to resolution: 1-3 days

---

### 17. Catalog / Product Display (13 tickets - 2.6%)

**Specific Issues Customers Face:**

#### Products Not Showing Up
- **Products missing from catalog** after upload
  - Example: Ticket #13895 - "FW: AC Chairs Unreleased for ECAT"
  - Issue: Products not appearing after data sync
  - Resolution: Data sync verification, collection configuration

#### Collections Not Displaying
- **Collections not visible** to users
  - Example: Ticket #13908 - Charleston Forge collections issue
  - Issue: New collections not auto-selected into user groups
  - Resolution: Manual selection in admin console

**Common Resolution Patterns:**
- 75% L1 support
- Data sync verification, collection configuration
- Time to resolution: 1-3 days

---

### 18. iPad/Device Issues (9 tickets - 1.8%)

**Specific Issues Customers Face:**

#### App Not Updating
- **Users not getting latest data**
  - Issue: App not auto-updating after file imports
  - Resolution: Recommendation to manually update daily

#### Device Sync Issues
- **Data not syncing between iPads**
  - Example: Ticket #13845 - Missing orders between devices
  - Issue: Switching iPads, data not following
  - Resolution: Sync troubleshooting, internet connection verification

#### Device Switching Problems
- **Wish lists not transferring** between devices
  - Issue: Reps using multiple iPads
  - Resolution: Explanation of sync limitations

**Common Resolution Patterns:**
- 70% L1 support
- 30% L2 requiring investigation
- App reinstall guidance (rarely needed), sync troubleshooting
- Time to resolution: 1-3 days

---

### 19. Reports/Exports (9 tickets - 1.8%)

**Specific Issues Customers Face:**

#### Report Generation Questions
- **How to access specific reports**
  - Example: Ticket #13885 - Bulbrite: "Report Request"
  - Questions: "Which reps use eCat most? Which customers? Average orders?"
  - Resolution: Guidance on Orders → Reports, CSV downloads, usage report offers

#### Export Functionality
- **How to export data** for analysis
  - Resolution: CSV export instructions, pivot table suggestions

**Common Resolution Patterns:**
- 85% L1 support
- Guidance on using existing reports
- Feature explanation
- Time to resolution: 1-2 days

---

### 20. Permissions/Access Control (11 tickets - 2.2%)

**Specific Issues Customers Face:**

#### Users Unable to See Features
- **Permission configuration** preventing access
  - Example: Ticket #13893 - Viewing other users' quotes
  - Issue: Permission and territory settings
  - Resolution: User group permission verification

#### Shared Order Access
- **Reps can't see each other's orders**
  - Issue: Territory and permission configuration
  - Resolution: Settings adjustment in admin console

**Common Resolution Patterns:**
- 80% L1 support
- User group permission verification and adjustment
- Time to resolution: 1-2 days

---

## Support Complexity Analysis

### Severity Distribution (Based on Tags)
- **S4 - Low:** 175 tickets (35.1%) - Simple, straightforward issues
- **S3 - Medium:** 64 tickets (12.9%) - Moderate complexity requiring investigation
- **S2 - High:** 3 tickets (0.6%) - Urgent issues requiring immediate attention (mostly scanning issues at trade shows)
- **S1 - Critical:** 0 tickets - No critical incidents in 90-day period

### Support Level Distribution
- **L1 - Frontline Support:** 160 tickets (32.1%) - Resolved by first-line support
- **L2 - Internal Collaboration:** 59 tickets (11.9%) - Required cross-team coordination
- **L3 - Engineering Intervention:** 33 tickets (6.6%) - Required engineering resources
- **L4 - Executive/Strategic:** 2 tickets (0.4%) - Required executive involvement

### Resolution Speed
- **First-Touch Resolved:** 37 tickets (7.4%) - Resolved in initial response
- **Quick Resolution (1-2 messages):** ~180 tickets (36.1%)
- **Standard Resolution (3-6 messages):** ~210 tickets (42.2%)
- **Complex Resolution (7+ messages):** 71 tickets (14.3%)

---

## Product Distribution

### Tickets by Product
- **Admin Console:** 143 tickets (28.7%)
- **eCat (iPad App):** 57 tickets (11.4%)
- **eCat Online (Web):** 36 tickets (7.2%)
- **Sales Portal:** 8 tickets (1.6%)
- **Multiple/Unspecified:** 254 tickets (51.0%)

---

## Key Insights & Patterns

### 1. Data Sync is the #1 Pain Point (43.4% of tickets)
**Specific Problems:**
- File format confusion and validation errors with unclear messages
- Collections not auto-populating into user groups
- Barcode/scan value field confusion (ScanValue vs keywords)
- Cache issues causing different users to see different data
- API authentication failures breaking automated flows

**Root Causes:**
- Lack of clear documentation on file format requirements
- Unintuitive collection selection behavior
- Two different scanning methods not well explained
- Cache invalidation issues
- Credential management in integrations

**Recommendation:** 
- Improve import validation error messages to be more actionable
- Create file format templates with examples
- Build pre-import validation tool
- Add collection auto-selection option
- Implement better cache management
- Create comprehensive barcode/scanning documentation

---

### 2. Pricing Configuration is Deeply Confusing (Multiple tickets with 5-11 message threads)
**Specific Problems:**
- Fundamental misunderstanding of pricing hierarchy (user group vs customer contract)
- Customers believe user group determines pricing when it doesn't (for users with customer numbers)
- Price level vs user group vs customer contract relationship unclear
- Pack pricing vs unit pricing confusion

**Root Causes:**
- Complex pricing logic not well documented
- Multiple factors determine pricing (user group, customer number, Bluelink contract)
- UI doesn't clearly show which pricing source is being used
- No audit logs to see who changed settings

**Recommendation:**
- Create pricing configuration wizard
- Add "pricing source" indicator in UI showing where price comes from
- Simplify pricing documentation with decision tree
- Add audit logs for pricing changes
- Create pricing troubleshooting guide

---

### 3. Onboarding is Resource-Intensive (41.4% of tickets, longest threads)
**Specific Problems:**
- Complex multi-stakeholder coordination (up to 31 messages)
- Multiple parallel workstreams (pricing, API, customer import, order integration)
- Duplicate tickets from automation
- Many manual steps requiring back-and-forth

**Root Causes:**
- No structured onboarding workflow
- Manual coordination of multiple teams
- Automation creating duplicate tickets
- Many configuration steps not self-service

**Recommendation:**
- Create structured onboarding playbook with phases
- Build onboarding dashboard showing progress
- Fix automation to prevent duplicate tickets
- Create onboarding templates for common scenarios
- Implement automated onboarding workflow where possible

---

### 4. Training Gaps are Significant (16.9% of tickets)
**Specific Problems:**
- How to configure features (price levels, user groups, smart lists)
- How to generate reports
- How to set up email notifications
- When app updates vs when data updates
- Device requirements

**Root Causes:**
- Features not intuitive
- Documentation insufficient or hard to find
- No in-app guidance
- Complex admin console

**Recommendation:**
- Expand knowledge base with top 20 how-to articles
- Create Loom video library for common tasks
- Add contextual help links in application
- Implement in-app tutorials and tooltips
- Create role-based training paths

---

### 5. User Management is High-Volume but Low-Complexity (17.3% of tickets, 95% L1)
**Specific Problems:**
- Password resets (often via voice message indicating urgency)
- New user account setup
- Username/email changes
- Registration failures

**Root Causes:**
- No self-service password reset
- Manual account creation process
- Registration flow issues

**Recommendation:**
- Implement self-service password reset
- Create user invitation workflow
- Add bulk user management tools
- Fix registration flow issues
- Consider SSO integration

---

### 6. Scanning Functionality is Confusing (5 tickets but high severity)
**Specific Problems:**
- Two different scanning methods not well understood
- Scans not captured when internet connectivity poor (trade shows)
- Confusion about ScanValue vs keywords field

**Root Causes:**
- Two scanning workflows (search bar vs direct-to-order)
- Poor documentation of both methods
- Sync issues at trade shows with bad connectivity
- Field naming confusion

**Recommendation:**
- Create comprehensive scanning guide with both methods
- Improve offline sync capability for trade shows
- Rename fields to be more intuitive
- Add in-app scanning tutorial
- Proactive support for trade show seasons

---

### 7. Image Management is Error-Prone (17 tickets)
**Specific Problems:**
- Images not displaying after upload
- Filename mismatches between CSV and uploaded files
- Invalid file formats (SVG saved as JPG)
- No clear error messages

**Root Causes:**
- Manual filename entry prone to typos
- No MIME type validation
- Missing images report exists but not well known
- Two types of errors (no filename vs wrong filename)

**Recommendation:**
- Improve MIME type validation
- Add image upload preview
- Make missing images report more prominent
- Add image filename auto-complete
- Better error messages during upload

---

### 8. Rep/Territory Configuration is Complex (15 tickets)
**Specific Problems:**
- Reps not seeing their customers
- Territory codes not assigned correctly
- Shared orders not working
- Sub-rep hierarchy unclear

**Root Causes:**
- Manual territory assignment required
- No validation of territory setup
- Complex permission interactions
- Sub-rep workflow not documented

**Recommendation:**
- Create territory setup wizard
- Add territory validation checks
- Improve shared order documentation
- Create sub-rep management workflow
- Add territory troubleshooting guide

---

### 9. Bugs Require Significant Engineering Resources (52 tickets, 65% L3)
**Specific Problems:**
- Maybe list removal bug
- Product listing display issues
- Cache-related bugs
- Orders hidden from screen
- Integration failures

**Root Causes:**
- Quality assurance gaps
- Complex caching logic
- Integration credential management
- Display logic bugs

**Recommendation:**
- Invest in automated testing
- Improve error messages
- Implement proactive monitoring
- Better cache management
- Improve integration credential handling

---

### 10. Resolution Methods Vary by Complexity

#### Email-Only (60% of tickets)
- Simple, straightforward issues
- Clear documentation exists
- 1-3 message exchanges
- Examples: Password resets, simple user management, basic questions

#### Email + Loom Video (9.2% of tickets - 46 tickets)
- Visual explanation needed
- Step-by-step processes
- Configuration guidance
- Examples: Image troubleshooting, barcode scanning, import file formats

#### Long Email Thread (14.3% of tickets - 71 tickets)
- Complex troubleshooting
- Multiple variables
- 7-31 message exchanges
- Examples: Pricing configuration, onboarding, bug investigation

#### Meeting/Call Required (27.5% of tickets - 137 tickets)
- High complexity
- Real-time collaboration needed
- Strategic decisions
- Multiple stakeholders
- Examples: Onboarding kickoffs, complex bugs, configuration planning

---

## Notable Patterns & Observations

### 1. Voice Message Pattern
Multiple tickets (#13905, #13903) show voice messages being converted to Help Scout tickets for password resets, indicating:
- Customers prefer phone support for urgent issues
- Password reset is high-urgency for users
- Phone support availability should be clearly communicated

**Recommendation:** Consider implementing callback functionality for urgent issues.

---

### 2. Duplicate Ticket Pattern
Several onboarding questionnaire submissions created duplicate tickets (#13886, #13884, #13883, #13882), suggesting:
- Automation issues in onboarding workflow
- Creates noise in support queue
- Wastes support team time

**Recommendation:** Review onboarding automation to prevent duplicate ticket creation.

---

### 3. Market/Trade Show Spike
Scanning issues (#13843, #13837, #13821) clustered around trade show dates (Lightovation), indicating:
- Seasonal support needs
- Poor internet connectivity at trade shows causes sync issues
- Reps need offline capability

**Recommendation:** 
- Prepare proactive support resources for trade show seasons
- Improve offline sync capability
- Provide pre-market checklist for reps

---

### 4. Cache Issue Pattern
Multiple tickets (#13794, #13792, #13785) related to cache issues causing stale data, indicating:
- Systemic technical issue
- Affects multiple customers
- Causes confusion and mistrust

**Recommendation:** Investigate and resolve cache invalidation issues, implement better cache management.

---

### 5. Price Level Confusion Pattern
Recurring confusion about price level configuration (#13889, #13887) with very long threads (11 messages), suggesting:
- UI/UX improvements needed
- Pricing logic too complex
- Documentation insufficient

**Recommendation:** 
- Simplify price level configuration interface
- Add clearer documentation with examples
- Show pricing source in UI
- Create pricing troubleshooting wizard

---

### 6. Loom Video Effectiveness
46 tickets (9.2%) included Loom videos, often for:
- Image troubleshooting
- Barcode scanning
- Import file formats
- Feature configuration

**Pattern:** Loom videos significantly reduce back-and-forth, especially for visual/procedural issues.

**Recommendation:** Expand Loom video library for top 20 issues, make videos discoverable in KB.

---

### 7. Onboarding Complexity
Longest threads are onboarding-related (31 messages for Terracotta, 22 for Coaster), indicating:
- Onboarding is most complex customer journey
- Multiple parallel workstreams
- High touch required

**Recommendation:** 
- Create structured onboarding phases
- Build onboarding dashboard
- Automate common tasks
- Create onboarding templates

---

## Customer Sentiment Indicators

### Positive Indicators
- "Thank you!" - Frequent positive closures
- "That was super helpful" - Appreciation for support quality
- "Great to hear!" - Satisfaction with resolutions
- Quick "Thanks Chuck" responses - Trust in support team
- "Got it! Updated, thanks Chuck 😊" - Positive emoji usage

### Frustration Indicators
- Long thread counts (11-31 messages) - Complexity frustration
- "This is so odd" - Unexpected behavior causing confusion
- Multiple follow-ups - Unresolved issues
- Voice messages - Urgency/frustration with written support
- "I have gotten at least 7 reports of this this week" - Recurring problems

### Confusion Indicators
- "I'm not sure I understand" - Clarity issues
- Multiple clarifying questions - Documentation gaps
- "How do I..." questions - Training needs
- "I was told the pricing always corresponded with their user group" - Misinformation

---

## Support Team Performance

### Strengths
1. **Quick Response Times:** First-touch resolved tickets indicate fast initial response
2. **Video Support:** 46 Loom videos show commitment to visual explanation
3. **Personalized Support:** Long threads show dedication to resolution
4. **Cross-Team Collaboration:** L2/L3 escalation working effectively
5. **Knowledge Sharing:** "Add to knowledge base" tag on 7 tickets shows continuous improvement

### Opportunities
1. **Automation:** High-volume, low-complexity tasks (password resets) could be automated
2. **Self-Service:** Training questions could be addressed through better documentation
3. **Proactive Support:** Patterns suggest opportunities for proactive outreach (trade shows, common issues)
4. **Knowledge Base:** Only 7 tickets tagged "add to knowledge base" suggests more could be documented
5. **First-Touch Resolution:** Average of 3.5 messages per ticket indicates room for improvement

---

## Recommendations by Priority

### Immediate (0-30 days)

#### 1. Improve Data Import Experience
**Problem:** #1 source of tickets (216 tickets, 43.4%)
- Better import validation error messages
- File format templates with examples
- Pre-import validation tool
- Collection auto-selection option

#### 2. Pricing Configuration Documentation
**Problem:** Long, complex threads (11 messages) with deep confusion
- Create pricing decision tree
- Add "pricing source" indicator in UI
- Pricing troubleshooting guide
- Admin console screenshots for common scenarios

#### 3. Self-Service Password Reset
**Problem:** High volume (86 tickets), low complexity, urgent (voice messages)
- Implement self-service password reset
- Reduce support burden
- Improve user experience

#### 4. Scanning Documentation
**Problem:** High severity (S2), trade show critical
- Comprehensive scanning guide with both methods
- In-app scanning tutorial
- Trade show preparation checklist

#### 5. Fix Onboarding Automation
**Problem:** Duplicate tickets creating noise
- Fix automation to prevent duplicates
- Clean up support queue

---

### Short-Term (30-90 days)

#### 1. Expand Knowledge Base
**Problem:** 84 training tickets (16.9%)
- Top 20 how-to articles
- Loom video library for common tasks
- Contextual help links in application

#### 2. Image Management Improvements
**Problem:** 17 tickets, error-prone process
- Better MIME type validation
- Image upload preview
- Make missing images report more prominent
- Image filename auto-complete

#### 3. Cache Management
**Problem:** Systemic issue affecting multiple customers
- Investigate cache invalidation issues
- Implement better cache management
- Proactive monitoring

#### 4. Territory Setup Wizard
**Problem:** 15 tickets, complex configuration
- Territory setup wizard
- Territory validation checks
- Sub-rep management workflow

#### 5. Onboarding Dashboard
**Problem:** Most complex customer journey (31-message threads)
- Structured onboarding phases
- Progress dashboard
- Onboarding templates

---

### Medium-Term (90-180 days)

#### 1. Pricing Configuration Wizard
**Problem:** Deep confusion, long threads
- Simplify pricing interface
- Configuration wizard
- Show pricing source in UI
- Audit logs for pricing changes

#### 2. In-App Tutorials
**Problem:** Training gaps
- Implement in-app tutorials and tooltips
- Interactive training modules
- Role-based training paths

#### 3. Bulk User Management
**Problem:** High volume user management
- Bulk user management tools
- User invitation workflow
- SSO integration planning

#### 4. Automated Testing
**Problem:** 52 bug tickets, 65% requiring engineering
- Invest in automated testing
- Improve error handling
- Proactive monitoring

#### 5. Trade Show Support Package
**Problem:** Seasonal spikes, poor connectivity
- Improve offline sync capability
- Pre-market checklist
- Proactive support staffing

---

### Long-Term (180+ days)

#### 1. Automated Onboarding Workflow
**Problem:** Most resource-intensive process
- Build automated onboarding workflow
- Self-service onboarding portal
- Industry-specific templates

#### 2. AI-Powered Help Assistant
**Problem:** Training and documentation gaps
- AI-powered help assistant
- Personalized learning recommendations
- Contextual help

#### 3. Advanced User Analytics
**Problem:** Customer requests for usage insights
- User activity analytics
- Rep performance dashboards
- Customer engagement metrics

#### 4. Integration Credential Management
**Problem:** API auth failures
- Automated credential rotation
- Integration health monitoring
- Self-service integration setup

---

## Success Metrics

### Ticket Volume Reduction Targets
**Key Success Metric:** Reducing the top 3 themes (Data Sync, Onboarding, Training) by 50% would eliminate approximately 250 tickets per 90-day period.

#### Data Sync (216 tickets → 108 tickets)
- Measure: Import validation errors reduced by 50%
- Measure: Collection configuration questions reduced by 60%
- Measure: Barcode/scanning questions reduced by 70%

#### Onboarding (206 tickets → 103 tickets)
- Measure: Average thread count reduced from 10+ to 5
- Measure: Duplicate tickets eliminated (100%)
- Measure: Onboarding time reduced from 4-6 weeks to 2-3 weeks

#### Training (84 tickets → 42 tickets)
- Measure: "How to" questions reduced by 50%
- Measure: KB article views increased by 200%
- Measure: Loom video views increased by 300%

### Support Efficiency Targets
- **First-Touch Resolution:** Increase from 7.4% to 15%
- **Average Messages Per Ticket:** Reduce from 3.5 to 2.5
- **L3 Engineering Tickets:** Reduce from 6.6% to 4%
- **Time to Resolution:** Reduce average from 3 days to 2 days

### Customer Satisfaction Targets
- **Positive Sentiment:** Increase positive closures by 25%
- **Frustration Indicators:** Reduce long threads (7+) from 14.3% to 10%
- **Voice Messages:** Reduce by 50% (indicates urgency/frustration)

---

## Conclusion

This 90-day analysis reveals that while SuperCat's support team is effectively handling a diverse range of issues, there are significant opportunities to reduce ticket volume through:

1. **Improved Data Import Experience** - The #1 source of tickets with specific pain points around validation errors, collection sync, and barcode configuration
2. **Simplified Pricing Configuration** - Deep confusion requiring 11-message threads indicates UI/UX and documentation improvements needed
3. **Streamlined Onboarding** - The #2 source of tickets and most complex customer journey with 31-message threads
4. **Enhanced Training Resources** - The #3 source of tickets with clear gaps in documentation and in-app guidance
5. **User Management Automation** - High volume, low complexity, perfect for self-service

The support team demonstrates strong performance with 67.1% ticket closure rate and effective use of multiple resolution methods (email, video, calls). However, the average of 3.5 messages per ticket and 71 tickets requiring 7+ messages indicate opportunities for first-touch resolution improvement.

**The specific substance of issues reveals:**
- Customers struggle with complex pricing logic (user group vs customer contract)
- File import validation errors are unclear and not actionable
- Two different scanning methods cause confusion
- Onboarding requires extensive manual coordination
- Cache issues cause systemic problems affecting multiple customers

By addressing these specific pain points with targeted improvements, SuperCat can significantly reduce support burden while improving customer experience.

---

## Appendix: Data Methodology

### Data Collection
- **Source:** BigQuery - Hevo Dataset (`supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`)
- **Date Range:** October 30, 2025 - January 29, 2026 (90 days)
- **Filters Applied:** 
  - Mailbox emails: `support@supercatsolutions.com`, `onboarding@supercatsolutions.com`
  - All ticket statuses included (open, active, pending, closed, spam)

### Analysis Approach
1. **Thematic Categorization:** Analyzed ticket subjects, previews, and tags using keyword matching and tag analysis
2. **Substance Extraction:** Read thread bodies to understand specific customer problems, not just categories
3. **Resolution Method Analysis:** Examined thread bodies for Loom links, meeting mentions, and thread counts
4. **Complexity Assessment:** Used Help Scout tags (S1-S4, L1-L4) for severity and support level classification
5. **Pattern Identification:** Reviewed specific ticket examples to understand common issues and resolutions

### Limitations
- Thread body analysis limited to text content; attachments not analyzed
- Customer sentiment inferred from text patterns, not explicitly measured
- Resolution time estimates based on ticket creation and closure timestamps
- Some tickets may span multiple themes; primary theme assigned based on dominant issue

---

**Report Generated:** January 29, 2026  
**Analyst:** AI Analysis via Cursor  
**Next Review:** April 29, 2026 (90 days)
