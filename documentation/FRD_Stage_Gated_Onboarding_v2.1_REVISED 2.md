# FRD: Stage-Gated Onboarding Readiness Scoring

**Author:** Kylor Johnson  
**Date:** January 6, 2026  
**Version:** 2.1 (Revised)  
**Status:** Production Ready  
**Related JIRA:** [Link to your JIRA ticket]

---

## Document Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 2.0 | Jan 5, 2026 | Initial production version | Kylor Johnson |
| 2.1 | Jan 6, 2026 | **Revised Stage 7.1:** Distinguished iPad app access from web mobile sites. Either is sufficient for launch. Added user device validation method. | Kylor Johnson |

---

## Executive Summary

Replace SuperCat's existing 100-point onboarding scoring system with a **7-stage progressive framework** that provides clear, actionable readiness indicators for each phase of customer onboarding. This framework identifies launch blockers early and gives CS/implementation teams a structured path to guide clients from kickoff to go-live.

**Key Innovation:** Adaptive logic that automatically handles conditional features (options, territories, inventory) to avoid false negatives and provide accurate readiness scoring regardless of client configuration.

**Version 2.1 Update:** Clarified Stage 7.1 to distinguish between iPad app access and web-based mobile portals. Either method provides sufficient mobile access for launch.

---

## Problem Statement

### Current Issues
- 100-point scoring system is opaque and doesn't map to actual implementation workflow  
- No clear visibility into what's blocking a launch vs. what's "nice to have"  
- CS team lacks structured framework to guide clients through onboarding  
- Implementation delays occur because critical dependencies aren't surfaced early  

### Business Impact
- Extended time-to-value for new clients  
- Higher support burden during onboarding  
- Risk of client churn when launches miss deadlines  
- CS time spent diagnosing problems instead of advancing stages  

---

## Proposed Solution

A **7-stage progressive framework** mirroring real implementation workflow.

| Stage | Name | Core Focus | Typical Timeline |
|------|------|------------|------------------|
| 1 | Account Foundation | Basic org setup complete | Day 1 |
| 2 | Catalog Setup | Products imported and browsable | Week 1–2 |
| 3 | Pricing Configuration | Products can be priced | Week 2–3 |
| 4 | Option Configuration | CPQ/options configured | Week 3–4 |
| 5 | Customer & User Setup | Buyer/seller relationships | Week 4–5 |
| 6 | Operational Data | Real-time data flowing | Week 5–6 |
| 7 | Order-Ready | System can process orders | Week 6–8 |

Each stage includes:
- Always Required checks  
- Conditional checks (when applicable)
- Yellow (🟡) and Green (🟢) thresholds  
- Binary pass/fail requirements  

---

## Success Criteria

### CS / Implementation Team
- Clear stage visibility into client progress
- Actionable next steps at each stage
- Automatic launch blocker detection
- Faster issue triage and resolution

### Clients
- Transparent progress tracking
- Clear expectations at each milestone
- Reduced back-and-forth communication
- Confidence in launch readiness

### Leadership
- Pipeline visibility across all onboarding clients
- Bottleneck identification by stage
- Time-to-launch metrics
- Resource planning insights

---

## Critical Launch Blockers

### Absolute Blockers 🔴
**System cannot launch without these:**
- No price levels configured  
- No customers imported  
- **No mobile access configured** (iPad app OR web portal)
- No presentation formats configured  
- No test order processed

### High-Priority Risks 🟡
**Launch possible but requires CS attention:**
- Missing product images  
- Stale imports (>30 days)
- High import error rates  
- Order notification email not configured
- No recent order activity (post-launch)

### Medium-Priority ⚠️
**Monitor but not blockers:**
- Incomplete taxonomy  
- Limited custom fields  
- Only one price level  
- No inventory data (if tracking disabled)
- Export type not configured (if no ERP)

---

## Conditional Logic Framework

| Feature | Detection Method | If Enabled | If Disabled |
|---------|------------------|------------|-------------|
| **Options** | `get_options` returns count | Validate Stage 4 criteria | Skip Stage 4 (N/A) |
| **Territories** | `get_user_territories` returns count | Validate territory assignments | Validate direct customer assignment |
| **Inventory** | `inventory_tracking` flag in settings | Validate inventory imports | Skip inventory checks |
| **Smart Stacks** | `get_smart_stacks` returns count | Validate stack configuration | Skip (N/A) |

**Key Principle:** Features that are disabled should not block launch. Conditional logic ensures clients are only validated on features they actually use.

---

## Color Threshold System

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| 🟢 Green | Production-ready | None - proceed to next stage |
| 🟡 Yellow | Launchable with minor issues | CS follow-up recommended |
| 🔴 Red | Blocker | Halt launch until resolved |
| N/A | Not applicable | Feature disabled or conditional |
| ❓ | Unknown | Investigate data source |

---

## Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 1.1 | Organization exists | `get_organization_info` | `status: "active"` |
| 1.2 | Company information complete | `company_information` | Name, address, email not null |
| 1.3 | Admin user exists | `get_org_users` | At least 1 user with `is_admin: true` |
| 1.4 | Settings initialized | `preferences` | Object exists with defaults |

### Thresholds
- 🔴 **Red:** Any required criterion fails
- 🟢 **Green:** All criteria pass

### Typical Issues
- Organization created but company info not completed
- No admin user assigned
- Settings not initialized

---

## Stage 2: Catalog Setup

**Goal:** Products imported and browsable by users

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 2.1 | Products imported | `get_data_summary` | `products.count >= 10` |
| 2.2 | Product images uploaded | Visual validation | At least 50% of products have images |
| 2.3 | Categories configured | `get_categories` | `categories.count >= 1` |
| 2.4 | Collections exist | `get_collections` | `collections.count >= 1` |
| 2.5 | Recent product update | `last_product_update` | Within 30 days |

### Thresholds
- 🔴 **Red:** Products < 10
- 🟡 **Yellow:** Products 10-100 OR no update in 30+ days
- 🟢 **Green:** Products > 100 AND recent update

### Typical Issues
- Initial product import incomplete
- Missing product images
- Taxonomy (categories/collections) not configured
- Stale data from initial import

---

## Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 3.1 | Price levels configured | `get_price_levels` | `price_levels.count >= 1` |
| 3.2 | Multiple price levels | `get_price_levels` | `price_levels.count >= 2` (recommended) |
| 3.3 | Pricing data populated | Sample products | At least 80% have prices |

### Thresholds
- 🔴 **Red:** No price levels configured
- 🟡 **Yellow:** Only 1 price level configured
- 🟢 **Green:** 2+ price levels with complete data

### Typical Issues
- Price levels created but no pricing data
- Only default price level configured
- Pricing data incomplete across product catalog

---

## Stage 4: Option Configuration

**Goal:** If options enabled, CPQ/configurators are functional

### Conditional Logic

**Check if options are enabled:**
```
options = get_options(org_shortname)
if options.count == 0:
    stage_4_status = "N/A"  # Skip - not applicable
else:
    validate_stage_4_criteria()
```

### Required Criteria (If Options Enabled)

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 4.1 | Options configured | `get_options` | `options.count >= 1` |
| 4.2 | Options have values | Sample validation | At least 80% have choice values |
| 4.3 | Option validation enabled | Settings check | `require_valid_options_to_submit_orders` (if CPQ-critical) |

### Thresholds
- 🔴 **Red:** Options enabled but count = 0
- 🟡 **Yellow:** Options < 5 or incomplete data
- 🟢 **Green:** Options >= 5 with complete configuration
- **N/A:** Options disabled (skip stage)

### Typical Issues
- Options feature enabled but not configured
- Option values missing or incomplete
- Required options not enforced in settings

---

## Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 5.1 | Customers imported | `get_data_summary` | `customers.count >= 10` |
| 5.2 | Users configured | `get_org_users` | `org_users.count >= 2` |
| 5.3 | User types configured | `get_org_users` | Multiple user types exist |
| 5.4 | Recent customer update | `last_customer_update` | Within 30 days |
| 5.5 | Assignment logic configured | **See conditional logic below** | Validated based on model |

### Conditional Logic: Territory vs Direct Assignment

**Check assignment model:**
```
territories = get_user_territories(org_shortname)
if territories.count > 0:
    # Territory-based model
    validate_territory_assignments()
else:
    # Direct assignment model
    validate_direct_customer_user_relationships()
```

**If Territories Enabled:**
- Users must be assigned to territories via `territory_codes`
- Territory structure must exist with at least 1 territory
- Customers assigned to territories or users within territories

**If Territories Disabled:**
- Direct customer-to-user assignments
- No territory structure required

### Thresholds
- 🔴 **Red:** Customers < 10 OR no users configured
- 🟡 **Yellow:** Customers 10-100 OR no recent update
- 🟢 **Green:** Customers > 100 AND recent update AND proper assignment

### Typical Issues
- Customers imported but no user assignments
- Territory structure created but users not assigned
- Missing recent customer data sync

---

## Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 6.1 | Inventory tracking configured | `get_data_summary` | `inventories.count > 0` OR tracking disabled |
| 6.2 | Recent inventory update | `last_inventory_update` | Within 7 days (if enabled) |
| 6.3 | Smart stacks configured | `get_smart_stacks` | At least 1 OR feature disabled |
| 6.4 | Data import health | `get_import_events` | No critical errors in last 30 days |

### Conditional: Inventory Tracking

```
if inventory_tracking_enabled:
    validate_inventory_data_exists()
    validate_recent_inventory_update()
else:
    stage_6_inventory_status = "N/A"
```

### Thresholds
- 🔴 **Red:** Inventory enabled but no data OR critical import errors
- 🟡 **Yellow:** Stale inventory (7+ days) OR minor import warnings
- 🟢 **Green:** Fresh data AND no import errors

### Typical Issues
- Inventory tracking enabled but no data
- Import errors blocking data sync
- Stale data (no recent updates)
- Smart stacks misconfigured

---

## Stage 7: Order-Ready

**Goal:** System can receive, process, and fulfill orders end-to-end

### Required Criteria

| # | Criterion | Validation Method | Pass Condition | Blocker Status |
|---|-----------|-------------------|----------------|----------------|
| **7.1a** | **iPad app access available** | **Admin UI: Check user device registrations** | **At least 1 user with iPad device registered** | **🔴 BLOCKER** ⭐ |
| **7.1b** | **Mobile web portal configured** | **`get_mobile_sites`** | **`mobile_sites.count >= 1 AND enabled: true`** | **🔴 BLOCKER** ⭐ |
| 7.2 | Presentation formats configured | `get_reports_config` | `report_configurations.count >= 3` | 🔴 **BLOCKER** |
| 7.3 | Test order processed | `get_orders` | `orders.count >= 1` | 🔴 **BLOCKER** |
| 7.4 | Order notification email | `order_email_recipient` | Not empty | 🟡 **Recommended** |
| 7.5 | Export type configured | `export_type` | Not empty (if ERP integration) | 🟡 **Conditional** |
| 7.6 | Recent order activity | `orders_last_30_days` | `count > 0` (health check) | 🟡 **Post-Launch** |

---

### ⭐ NEW IN v2.1: Stage 7.1 Mobile Access - iPad OR Web Portal

**IMPORTANT CHANGE:** Stage 7.1 has been split into two alternative validation methods. **Either 7.1a OR 7.1b must pass** - not both required.

#### Understanding Mobile Access Models

SuperCat supports two mobile access methods:

**7.1a: iPad App Access (Most Common)**
- Native iOS app for sales reps
- Users download SuperCat iPad app from App Store
- Register device with their org credentials
- Access full product catalog, ordering, and reporting

**7.1b: Mobile Web Portal**
- Browser-based mobile-responsive interface
- Accessed via URL (e.g., `orgname.supercat.com`)
- No app installation required
- Works on any device with web browser

---

### Criterion 7.1a: iPad App Access (ALTERNATIVE METHOD)

**Goal:** Verify at least one user has iPad app registered and functional

**Validation Method:**
```
MANUAL VALIDATION REQUIRED (Admin UI)
1. Log into SuperCat Admin for organization
2. Navigate to Users section
3. Check user list for device information columns:
   - "eCat" column shows app build version
   - "iOS" column shows iOS version
   - "iPad" column shows device model
4. Verify at least 1 user has values in these columns
5. Check "Last login" is recent (within 30 days recommended)
```

**Pass Condition:**
- ✅ At least 1 user has iPad device information populated
- ✅ Last login within 30 days (indicates active usage)

**Example (TCD organization):**
| User | eCat Build | iOS Version | iPad Model | Last Login |
|------|------------|-------------|------------|------------|
| TerraCat | 20251107 | 18.6 | iPad15,5 | 2025-12-20 ✅ |
| Kylor_Johnson | 20251107 | 18.6.2 | iPad15,3 | 2026-01-06 ✅ |

**Typical Issues:**
- Users created but haven't downloaded iPad app yet
- iPad app downloaded but user hasn't logged in
- Old app version (outdated eCat build number)

**How to Resolve:**
1. Send iPad app download link to users
2. Provide login credentials
3. Walk user through first-time setup
4. Verify successful login in Admin UI

---

### Criterion 7.1b: Mobile Web Portal (ALTERNATIVE METHOD)

**Goal:** Web-based mobile portal configured and accessible

**Validation Method:**
```
MCP ENDPOINT: get_mobile_sites(org_shortname)
```

**Pass Condition:**
- ✅ `mobile_sites.count >= 1`
- ✅ `enabled: true` on at least one site
- ✅ Site URL is accessible (optional validation)

**Example Response:**
```json
{
  "mobile_sites": [
    {
      "id": 123,
      "name": "Main Mobile Portal",
      "url": "tcd.supercat.com",
      "enabled": true,
      "theme": "custom"
    }
  ],
  "total_count": 1,
  "has_mobile_sites": true,
  "configuration_summary": {
    "active_sites": 1
  }
}
```

**Typical Issues:**
- Mobile site created but not enabled
- DNS/domain not configured
- SSL certificate issues
- Site configuration incomplete

**How to Resolve:**
1. Create mobile site record in admin
2. Configure site URL and domain
3. Enable site (toggle to active)
4. Test URL accessibility
5. Configure theming/branding

---

### Stage 7.1 Decision Matrix

**Which mobile access method do you need?**

| Client Profile | Recommended | Reason |
|----------------|-------------|--------|
| **Field sales reps** | 🎯 7.1a iPad App | Offline access, camera integration, better performance |
| **Office buyers only** | 🌐 7.1b Web Portal | No app installation, works on any device |
| **Mixed users** | ✅ Both | Flexibility for different user types |
| **Quick launch needed** | 🎯 7.1a iPad App | Faster to set up (just send credentials) |
| **Enterprise/IT controlled** | 🌐 7.1b Web Portal | Easier for IT to manage, no app store approval |

**For launch readiness validation:**
- ✅ **PASS:** Either 7.1a OR 7.1b satisfied
- ❌ **FAIL:** Neither 7.1a nor 7.1b satisfied

---

### MCP Endpoint Limitation (v2.1 Note)

**Current Gap:** The `get_org_users` MCP endpoint does NOT return iPad device information visible in the Admin UI.

**Workaround:** Manual validation via Admin UI for Stage 7.1a

**Recommended Enhancement:** Add new MCP endpoint:
```python
get_user_devices(org_shortname)
# Returns: user_id, username, device_model, ios_version, 
#          ecat_build, last_login, first_registration
```

This would enable programmatic iPad app validation.

---

### Criterion 7.2: Presentation Formats (BLOCKER)

**Goal:** Minimum 3 report formats configured for product presentations, quotes, orders

**Validation Method:**
```
MCP ENDPOINT: get_reports_config(org_shortname)
```

**Pass Condition:**
- ✅ `report_configurations.count >= 3`

**Required Report Types:**
1. Product Presentation (with images, pricing, options)
2. Quote/Proposal Template
3. Order Confirmation Template

**Typical Issues:**
- Report configurations not created
- Templates not customized for client
- Missing required fields in templates

**How to Resolve:**
1. Deploy standard report format library
2. Customize templates with client branding
3. Test each format with sample data
4. Validate option rendering (if CPQ enabled)

---

### Criterion 7.3: Test Order Processed (BLOCKER)

**Goal:** At least one end-to-end test order successfully processed

**Validation Method:**
```
MCP ENDPOINT: get_orders(org_shortname, limit=1)
```

**Pass Condition:**
- ✅ `orders.count >= 1`

**Test Order Requirements:**
1. Login as sales rep (not admin)
2. Select customer
3. Add products (including option-configured products if applicable)
4. Enter shipping address
5. Submit order
6. Verify order confirmation email received
7. Verify order appears in admin panel
8. Verify order PDF renders correctly

**Critical Validation Points:**
- Pricing calculations correct
- Territory-based pricing applied (if applicable)
- Options render in order confirmation
- Email notifications sent
- Order export generated (if ERP integration)

**How to Resolve:**
1. Schedule test order session with client
2. Walk through order process step-by-step
3. Document any issues encountered
4. Fix issues and re-test
5. Don't launch until test order succeeds

---

### Criterion 7.4: Order Notification Email (RECOMMENDED)

**Goal:** Email address configured for order notifications

**Validation Method:**
```
get_organization_info → preferences.administrative.order_email_recipient
```

**Pass Condition:**
- ✅ Email address not empty

**Typical Issues:**
- Email not configured
- Wrong email address (typo)
- Email goes to spam folder

**How to Resolve:**
1. Set `order_email_recipient` in preferences
2. Use client's order processing team email
3. Test with dummy order
4. Add to safe sender list

---

### Criterion 7.5: Export Type (CONDITIONAL)

**Goal:** Order export type configured (only if ERP integration needed)

**Validation Method:**
```
get_organization_info → preferences.ordering.export_type
```

**Pass Condition:**
- ✅ Export type not empty (if ERP integration)
- ✅ N/A if no ERP integration (manual order processing)

**Export Types:**
- CSV
- XML
- EDI
- Custom API

**How to Resolve:**
1. Determine if ERP integration needed
2. If yes: Configure export type and destination
3. If no: Mark as N/A
4. Test export generation with test order

---

### Criterion 7.6: Recent Order Activity (HEALTH CHECK)

**Goal:** Post-launch health indicator - orders being placed

**Validation Method:**
```
get_data_summary → counts.orders_last_30_days
```

**Pass Condition:**
- ✅ Count > 0 (indicates active usage)
- ⚠️ Count = 0 post-launch (potential dormant client)

**Note:** This is NOT a launch blocker - only relevant after launch for health monitoring.

---

### Stage 7 Thresholds

- 🔴 **Red:** Mobile access (7.1a OR 7.1b) OR reports (7.2) OR test order (7.3) missing
- 🟡 **Yellow:** Order email (7.4) missing OR no recent activity (7.6)
- 🟢 **Green:** All critical criteria pass + recent order activity

---

## Implementation Guidance

### MCP Endpoints Required

| Endpoint | Purpose | Stages |
|----------|---------|--------|
| `get_organization_info` | Org status and settings | 1, 7 |
| `get_data_summary` | Product/customer/order counts | 2, 3, 5, 6, 7 |
| `get_org_users` | User configuration | 1, 5 |
| `get_price_levels` | Pricing setup | 3 |
| `get_options` | **Conditional** - Options validation | 4 |
| `get_user_territories` | **Conditional** - Territory validation | 5 |
| `get_categories` | Taxonomy configuration | 2 |
| `get_collections` | Product organization | 2 |
| `get_mobile_sites` | Mobile web portal config | 7 (7.1b) |
| `get_reports_config` | Report formats | 7 (7.2) |
| `get_orders` | Test order validation | 7 (7.3) |
| `get_import_events` | Data health monitoring | 6 |
| `get_smart_stacks` | **Conditional** - Smart list config | 6 |
| ⭐ **`get_user_devices`** | **NEW - iPad app validation** | **7 (7.1a)** |

**⭐ Note:** `get_user_devices` endpoint does not currently exist - requires manual Admin UI validation for Stage 7.1a.

---

### Validation Flow (Updated for v2.1)

```python
def validate_onboarding_stage(org_shortname):
    """
    Validates current onboarding stage for an organization.
    Returns stage number (1-7) and status details.
    """
    
    # Stage 1: Account Foundation
    stage_1 = validate_stage_1(org_shortname)
    if stage_1.status == "red":
        return {"current_stage": 1, "status": "red", "blockers": stage_1.blockers}
    
    # Stage 2: Catalog Setup
    stage_2 = validate_stage_2(org_shortname)
    if stage_2.status == "red":
        return {"current_stage": 2, "status": "red", "blockers": stage_2.blockers}
    
    # Stage 3: Pricing Configuration
    stage_3 = validate_stage_3(org_shortname)
    if stage_3.status == "red":
        return {"current_stage": 3, "status": "red", "blockers": stage_3.blockers}
    
    # Stage 4: Option Configuration (CONDITIONAL)
    options = get_options(org_shortname)
    if options["count"] > 0:
        stage_4 = validate_stage_4(org_shortname)
        if stage_4.status == "red":
            return {"current_stage": 4, "status": "red", "blockers": stage_4.blockers}
    else:
        stage_4 = {"status": "n/a", "reason": "options_disabled"}
    
    # Stage 5: Customer & User Setup
    stage_5 = validate_stage_5(org_shortname)
    if stage_5.status == "red":
        return {"current_stage": 5, "status": "red", "blockers": stage_5.blockers}
    
    # Stage 6: Operational Data
    stage_6 = validate_stage_6(org_shortname)
    if stage_6.status == "red":
        return {"current_stage": 6, "status": "red", "blockers": stage_6.blockers}
    
    # Stage 7: Order-Ready (NEW v2.1 logic)
    stage_7 = validate_stage_7(org_shortname)
    
    return {
        "current_stage": 7,
        "status": stage_7.status,
        "launch_ready": stage_7.status in ["green", "yellow"],
        "blockers": stage_7.blockers,
        "warnings": stage_7.warnings,
        "all_stages": {
            "1": stage_1,
            "2": stage_2,
            "3": stage_3,
            "4": stage_4,
            "5": stage_5,
            "6": stage_6,
            "7": stage_7
        }
    }
```

---

### Stage 7 Validation Example (Updated for v2.1)

```python
def validate_stage_7(org_shortname):
    """Validates Stage 7: Order-Ready criteria (v2.1)"""
    blockers = []
    warnings = []
    
    # 7.1: Mobile Access - CHECK BOTH METHODS (only one needs to pass)
    mobile_access_available = False
    
    # 7.1a: Check iPad app access (requires manual validation or new endpoint)
    # NOTE: get_org_users does NOT include device info in current implementation
    # Recommendation: Check Admin UI or use new get_user_devices endpoint
    
    # For now, mark as "NEEDS MANUAL VERIFICATION" 
    ipad_access_status = "UNKNOWN - Manual Admin UI verification required"
    
    # 7.1b: Check mobile web portal
    mobile_sites = mcp_get_mobile_sites(org_shortname)
    web_portal_available = (
        mobile_sites.get("has_mobile_sites") and 
        mobile_sites["configuration_summary"]["active_sites"] > 0
    )
    
    # Either method satisfies mobile access requirement
    if not web_portal_available and ipad_access_status == "UNKNOWN":
        blockers.append(
            "Mobile access not verified - Need to check EITHER:\n" +
            "  (a) iPad app: Manually verify users have iPad devices registered in Admin UI, OR\n" +
            "  (b) Web portal: No mobile sites configured"
        )
    elif web_portal_available:
        mobile_access_available = True
        # Details logged below
    
    # 7.2: Report formats (BLOCKER)
    reports = mcp_get_reports_config(org_shortname)
    if reports["total_count"] < 3:
        blockers.append(
            f"Only {reports['total_count']} report formats configured (minimum 3 required)"
        )
    
    # 7.3: Test order processed (BLOCKER)
    orders = mcp_get_orders(org_shortname)
    if orders["total_count"] == 0:
        blockers.append(
            "No test order processed - must validate end-to-end order flow"
        )
    
    # 7.4: Order email (RECOMMENDED)
    org_info = mcp_get_organization_info(org_shortname)
    if not org_info["preferences"]["administrative"]["order_email_recipient"]:
        warnings.append("Order notification email not configured (recommended)")
    
    # 7.5: Export type (CONDITIONAL)
    export_type = org_info["preferences"]["ordering"]["export_type"]
    if not export_type or export_type == "":
        warnings.append("Export type not configured (required only if ERP integration)")
    
    # 7.6: Recent order activity (HEALTH CHECK)
    data_summary = mcp_get_data_summary(org_shortname)
    if data_summary["counts"]["orders_last_30_days"] == 0:
        warnings.append("No orders in last 30 days (potential dormant client)")
    
    # Determine status
    if len(blockers) > 0:
        status = "red"
    elif len(warnings) > 0:
        status = "yellow"
    else:
        status = "green"
    
    return {
        "status": status,
        "blockers": blockers,
        "warnings": warnings,
        "mobile_access_method": "web_portal" if web_portal_available else "needs_verification",
        "criteria_passed": 6 - len(blockers) - len(warnings),
        "criteria_total": 6
    }
```

---

## CS Team Workflow

### Pre-Kickoff (Day 0)
- Verify Stage 1 passes before scheduling kickoff
- Confirm admin user access
- Validate company information

### Week 1-2: Catalog Import
- Monitor Stage 2 progression
- Flag missing product images
- Validate taxonomy setup

### Week 2-3: Pricing Setup
- Ensure Stage 3 passes before proceeding
- Verify multiple price levels configured
- Validate pricing data completeness

### Week 3-4: Options (If Applicable)
- Check if options required
- If yes, validate Stage 4
- If no, mark N/A and proceed

### Week 4-5: Users & Customers
- Validate Stage 5 criteria
- Confirm territory or direct assignment
- Check recent customer data sync

### Week 5-6: Operational Data
- Monitor import health
- Validate inventory tracking (if enabled)
- Check smart stacks configuration

### Week 6-8: Launch Preparation
- **CRITICAL:** Ensure all Stage 7 blockers resolved
- **NEW in v2.1:** Verify mobile access (iPad app OR web portal)
  - **Option A:** Verify iPad users in Admin UI (at least 1 user with device)
  - **Option B:** Verify mobile web portal configured
  - **Either method is sufficient for launch**
- Process test order with client
- Verify report formats functional
- Validate order email notifications (recommended)

### Launch Day
- All stages Green or Yellow
- Mobile access confirmed (iPad OR web)
- Test order successfully processed
- Client trained and confident
- Support team on standby

---

## Launch Readiness Checklist

### Pre-Launch Requirements

**Must Have (Red Blockers):**
- [ ] Stage 1: Organization active with admin user
- [ ] Stage 2: Products imported (100+ recommended)
- [ ] Stage 3: Price levels configured (2+ recommended)
- [ ] Stage 4: Options configured (if feature enabled)
- [ ] Stage 5: Customers imported (100+ recommended)
- [ ] Stage 6: Real-time data flowing
- [ ] **Stage 7.1: Mobile access available** ⭐
  - **EITHER** [ ] iPad app: At least 1 user with registered device
  - **OR** [ ] Web portal: Mobile site configured and enabled
- [ ] Stage 7.2: Report formats configured (3+ minimum)
- [ ] Stage 7.3: Test order successfully processed

**Should Have (Yellow Warnings):**
- [ ] Product images uploaded (50%+ coverage)
- [ ] Recent data imports (within 30 days)
- [ ] Order notification email configured
- [ ] Export type configured (if ERP integration)

**Post-Launch Monitoring:**
- [ ] Order activity within 7 days of launch
- [ ] No critical import errors
- [ ] Client support tickets triaged

---

## Success Metrics

### CS Team Efficiency
- **Target:** 40% reduction in onboarding triage time
- **Measure:** Time from client question to action plan

### Client Time-to-Value
- **Target:** Average onboarding timeline: 6 weeks
- **Measure:** Days from kickoff to first production order

### Launch Success Rate
- **Target:** 95% of launches succeed on first attempt
- **Measure:** Launches without critical post-launch issues (7-day window)

### Pipeline Visibility
- **Target:** 100% of onboarding clients have visible stage status
- **Measure:** Dashboard adoption by CS team

---

## Out of Scope

**The following are explicitly OUT of scope:**
- Post-launch health monitoring (separate system)
- Adoption metrics (DAU/MAU)
- CSAT/NPS scores
- Sales qualification
- Contract/payment status
- Client-facing reporting
- Order volume targets

---

## Appendix: Validation Queries

### Stage 1 Example
```python
org_info = mcp_get_organization_info(org_shortname="client")
assert org_info["basic_info"]["status"] == "active"
assert org_info["company_information"]["name"] is not None
admin_users = [u for u in mcp_get_org_users(org_shortname="client")["org_users"] if u["is_admin"]]
assert len(admin_users) >= 1
```

### Stage 4 Conditional Example
```python
options = mcp_get_options(org_shortname="client")
if options["total_count"] == 0:
    stage_4_status = "n/a"  # Skip - not applicable
else:
    assert options["total_count"] >= 5  # Green threshold
    stage_4_status = "green"
```

### Stage 7 Mobile Access Example (v2.1)
```python
# Method 1: Check iPad app access (requires manual Admin UI check)
# Log into Admin UI → Users → Check for iPad/eCat/iOS columns populated

# Method 2: Check mobile web portal
mobile_sites = mcp_get_mobile_sites(org_shortname="client")
if mobile_sites["has_mobile_sites"] and mobile_sites["configuration_summary"]["active_sites"] > 0:
    stage_7_1_status = "green"  # Web portal available
else:
    # Need to manually verify iPad app access
    stage_7_1_status = "needs_verification"
```

### Stage 7 Test Order Example
```python
orders = mcp_get_orders(org_shortname="client")
if orders["total_count"] == 0:
    blockers.append("No test order processed")
    stage_7_status = "red"
```

---

## Approvals

| Role | Name | Date | Status |
|------|------|------|--------|
| **Author** | Kylor Johnson | Jan 6, 2026 | ✅ Complete (v2.1) |
| **CS Lead** | [Name] | [Date] | ⏳ Pending |
| **Engineering Lead** | [Name] | [Date] | ⏳ Pending |
| **Product Manager** | [Name] | [Date] | ⏳ Pending |

---

**Document Status:** Ready for Review  
**Version:** 2.1 (Revised)  
**Last Updated:** January 6, 2026  
**Contact:** Kylor Johnson



