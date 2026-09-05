# FRD: Multi-Product Stage-Gated Onboarding Readiness Scoring

**Author:** Kylor Johnson  
**Date:** January 14, 2026  
**Version:** 3.1 (Multi-Product + Validation Layer + Lessons Learned)  
**Status:** Draft  
**Related JIRA:** [Link to your JIRA ticket]

---

## Document Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 2.0 | Jan 5, 2026 | Initial production version (7-stage iPad framework) | Kylor Johnson |
| 2.1 | Jan 6, 2026 | Distinguished iPad app access from web mobile sites | Kylor Johnson |
| 3.0 | Jan 13, 2026 | **Multi-Product Support:** Extended to 12 stages covering eCat iPad, eCat Online, and Sales Portal. **Validation Layer:** Added Fathom + Help Scout cross-reference for contradiction detection. **Confidence Scoring:** Added numeric confidence based on Layer 1 + Layer 2 validation. **BigQuery Integration:** Stage 7 iPad validation via Mixpanel. | Kylor Johnson |
| 3.1 | Jan 14, 2026 | **Lessons Learned (V9 Assessment):** Added "[Hold]" meeting pattern detection for stalled implementations. Clarified Sales Portal is web-based (not iPad native). Added real-world examples from TCD, CST, KLL assessments. Added "Stalled Implementation" and "Unfulfilled Commitment" flag patterns. Enhanced Help Scout evidence requirements. | Kylor Johnson |

---

## Executive Summary

Extend SuperCat's 7-stage onboarding framework to a **12-stage multi-product framework** supporting eCat iPad, eCat Online, and Sales Portal implementations. Add a **two-layer validation approach** that combines quantitative system data (MCP/BigQuery) with qualitative sources (Fathom calls, Help Scout tickets) to detect false positives where system state doesn't reflect implementation reality.

**Key Innovations:**
1. **Multi-Product Support:** Single framework covers all three products with conditional stage logic
2. **Product Dependencies:** Sales Portal requires eCat Online foundation (Stages 8-9)
3. **Validation Layer:** Fathom + Help Scout cross-reference flags contradictions
4. **Confidence Scoring:** Numeric confidence (0-95%) based on Layer 1 + Layer 2 results
5. **BigQuery Integration:** iPad activity validation via Mixpanel data

---

## Problem Statement

### Current Issues (V2.1)
- Framework only covers eCat iPad (7 stages)
- No structured approach for eCat Online or Sales Portal implementations
- System data can produce **false positives** - e.g., products exist but are test data
- No mechanism to validate system state against client communications
- CS team may declare readiness based on system data that doesn't reflect reality

### Business Impact
- Incorrect readiness assessments leading to failed launches
- CS time spent troubleshooting post-launch issues that could have been caught earlier
- Client frustration when "ready" systems don't work as expected
- Tribal knowledge in Fathom calls and Help Scout tickets not leveraged for validation

---

## Proposed Solution

### A. Multi-Product Stage Framework

A **12-stage progressive framework** supporting three products:

| Stage | Name | eCat iPad | eCat Online | Sales Portal |
|-------|------|-----------|-------------|--------------|
| 1 | Account Foundation | ✅ Required | ✅ Required | ✅ Required |
| 2 | Catalog Setup | ✅ Required | ✅ Required | ✅ Required |
| 3 | Pricing Configuration | ✅ Required | ✅ Required | ✅ Required |
| 4 | Option Configuration | ⚪ Conditional | ⚪ Conditional | ⚪ Conditional |
| 5 | Customer & User Setup | ✅ Required | ✅ Required | ✅ Required |
| 6 | Operational Data | ✅ Required | ✅ Required | ✅ Required |
| 7 | iPad Order-Ready | ✅ Required | ⚪ N/A | ⚪ N/A |
| 8 | eCat Online Site Configuration | ⚪ N/A | ✅ Required | ✅ Required |
| 9 | eCat Online User Access | ⚪ N/A | ✅ Required | ✅ Required |
| 10 | eCat Online Ordering | ⚪ N/A | ⚪ Conditional | ⚪ N/A |
| 11 | Sales Portal Data | ⚪ N/A | ⚪ N/A | ✅ Required |
| 12 | Sales Portal User Access | ⚪ N/A | ⚪ N/A | ✅ Required |

### B. Product Dependency Chain

```
eCat iPad ─────────────────────────► [Complete at Stage 7]
     │
     └──► eCat Online ─────────────► [Complete at Stage 10]
               │
               └──► Sales Portal ──► [Complete at Stage 12]
```

**Important:** Sales Portal REQUIRES eCat Online Stages 8-9 to be complete. You cannot implement Sales Portal without first configuring eCat Online site and user access.

### C. Two-Layer Validation Architecture

| Layer | Source | Type | Purpose |
|-------|--------|------|---------|
| **Layer 1** | MCP + BigQuery | Quantitative | System state - data-driven assessment |
| **Layer 2** | Fathom + Help Scout | Qualitative | Contradiction detection - surfaces implementation reality |

**Key Principle:** Layer 2 does NOT replace Layer 1. It only flags contradictions that prompt human review.

---

## Success Criteria

### CS / Implementation Team
- Clear stage visibility across all three products
- Actionable next steps at each stage
- **NEW:** Contradiction flags when system data may not reflect reality
- **NEW:** Confidence scores to guide decision-making
- Reduced post-launch issues due to better pre-launch validation

### Clients
- Transparent progress tracking across all products
- Reduced launches followed by immediate support tickets
- Higher confidence in launch readiness

### Leadership
- Pipeline visibility across all products
- Bottleneck identification by stage AND by product
- Validation layer reduces false-positive readiness reports

---

## Critical Launch Blockers

### Absolute Blockers 🔴
**System cannot launch without these:**

**Foundation (All Products):**
- No price levels configured (Stage 3)
- No customers imported (Stage 5)

**eCat iPad:**
- No iPad order activity (Stage 7)
- No presentation formats configured (Stage 7)
- No test order processed (Stage 7)

**eCat Online:**
- No eCat Online site configured (Stage 8)
- No enrollment workflow for closed sites (Stage 9)
- No test order via web - if B2B enabled (Stage 10)

**Sales Portal:**
- No portal data imported (Stage 11)
- No users can access portal data (Stage 12)

### High-Priority Risks 🟡
**Launch possible but requires CS attention:**
- Missing product images
- Stale imports (>30 days)
- High import error rates
- Order notification email not configured
- Default email templates not customized
- SSO not configured (Sales Portal)

### Validation Layer Risks
**Contradiction flags that override system status:**
- 🔴 CONTRADICT flag on any stage = investigate before launch
- ⚠️ SENTIMENT flag detected = escalate to leadership
- ⚠️ ACTIVITY flag (90+ days no engagement) = potential abandonment

---

## Conditional Logic Framework

| Feature | Detection Method | If Enabled | If Disabled |
|---------|------------------|------------|-------------|
| **Options** | `get_options` returns count | Validate Stage 4 | Skip Stage 4 (N/A) |
| **Territories** | `get_user_territories` returns count | Validate territory assignments | Validate direct assignment |
| **Inventory** | `inventory_tracking` flag | Validate inventory imports | Skip inventory checks |
| **Smart Stacks** | `get_smart_stacks` returns count | Validate stack configuration | Skip (N/A) |
| **eCat Online** | Product implementation scope | Include Stages 8-10 | Skip Stages 8-10 (N/A) |
| **Sales Portal** | Product implementation scope | Include Stages 11-12 | Skip Stages 11-12 (N/A) |
| **B2B Ordering** | Feature flag for eOL cart | Validate Stage 10 | Skip Stage 10 (N/A) |

**Key Principle:** Features that are disabled should not block launch. Conditional logic ensures clients are only validated on features they actually use.

---

## Color Threshold System

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| 🟢 Green | Production-ready | None - proceed to next stage |
| 🟡 Yellow | Launchable with minor issues | CS follow-up recommended |
| 🔴 Red | Blocker | Halt launch until resolved |
| ⚪ N/A | Not applicable | Feature/product disabled or conditional |
| ❓ Unknown | Cannot validate | Investigate data source |

---

## Confidence Scoring System

Final stage confidence is calculated by combining Layer 1 status with Layer 2 validation results:

| Layer 1 Status | Layer 2 Result | Confidence Score | Interpretation |
|----------------|----------------|------------------|----------------|
| 🟢 GREEN | ✅ CONFIRMED | **95%+** | High confidence - proceed |
| 🟢 GREEN | No flags | **80%** | Good confidence - can proceed |
| 🟢 GREEN | ⚠️ REVIEW | **60%** | Needs investigation before proceeding |
| 🟢 GREEN | 🔴 CONTRADICT | **30%** | Do NOT trust Layer 1 - investigate |
| 🟡 YELLOW | ✅ CONFIRMED | **70%** | Known limitations, validated |
| 🟡 YELLOW | No flags | **60%** | Acceptable with monitoring |
| 🟡 YELLOW | ⚠️ REVIEW | **40%** | Address before go-live |
| 🟡 YELLOW | 🔴 CONTRADICT | **20%** | Major concerns - halt |
| 🔴 RED | Any | **0-10%** | Blocker - must resolve |

---

## Validation Flag Types

| Flag | Meaning | Action |
|------|---------|--------|
| 🔴 CONTRADICT | Evidence directly contradicts system data | Investigate immediately - system data may be wrong |
| 🔴 STALLED | Implementation on hold or paused | Clarify blocker and reactivation timeline |
| ⚠️ REVIEW | Needs clarification or follow-up | Review before marking stage complete |
| ⚠️ SENTIMENT | Negative sentiment or churn risk detected | Escalate to leadership |
| ⚠️ ACTIVITY | Zero engagement signals | Check for abandonment/stall |
| ⚠️ UNFULFILLED | Client commitment not delivered | Follow up on promised deliverables |
| ✅ CONFIRMED | Layer 1 validated by qualitative sources | High confidence in stage status |

### Real-World Examples (V9 Assessment - Jan 2026)

**🔴 STALLED Flag Example (Coaster Furniture):**
> Fathom meetings titled `[Hold] eCat x Coaster Standup` indicate implementation paused. Despite 6,420 customers loaded, 0 iPad orders exist. The "[Hold]" prefix signals waiting on client action.

**⚠️ UNFULFILLED Flag Example (Terracotta Designs):**
> Help Scout thread (Nov 2025): *"For now, we don't have a customer list file, but we will get it ready by the end of this week."* — 2 months later, still 0 customers imported. Promised deliverable never received.

**🔴 SENTIMENT Flag Example (Terracotta Designs):**
> Help Scout (Dec 2025): *"The tool feels less like a mature commercial product and more like an early-stage amateur implementation. Had I known this earlier, I likely would not have signed up."* — Immediate escalation required.

---

# FOUNDATION STAGES (1-6)

## Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

**Applies to:** All Products

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 1.1 | Organization exists | `get_organization_info` | `status: "active"` |
| 1.2 | Company information complete | `company_information` | Name, address, email not null |
| 1.3 | Admin user exists | `get_org_users` | At least 1 user with `is_admin: true` (excluding Kylor_Johnson, brentsanders, cwiebe) |
| 1.4 | Settings initialized | `preferences` | Object exists with defaults |

### Thresholds
- 🔴 **Red:** Any required criterion fails
- 🟢 **Green:** All criteria pass

### Validation Layer Keywords

**Fathom Search:**
- "admin", "administrator", "admin access", "account setup"

**Help Scout Search:**
- "login", "credentials", "can't log in", "no access"

**Contradiction Triggers:**
- "no admin access" while system shows admin exists
- "still setting up account" while Stage 1 shows green

---

## Stage 2: Catalog Setup

**Goal:** Products imported and browsable by users

**Applies to:** All Products

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 2.1 | Products imported | `get_data_summary` | `products.count >= 10` |
| 2.2 | Product images uploaded | `get_data_summary` | At least 10 products have images |
| 2.3 | Categories configured | `get_categories` | `categories.count >= 1` |
| 2.4 | Collections exist | `get_collections` | `collections.count >= 1` |
| 2.5 | Recent product update | `last_product_update` | Within 30 days |

### Thresholds
- 🔴 **Red:** Products < 10
- 🟡 **Yellow:** Products 10-100 OR no update in 60+ days OR < 10 products with images
- 🟢 **Green:** Products > 100 AND recent update

### Validation Layer Keywords

**Fathom Search:**
- "product import", "catalog", "images", "test data", "sample products", "placeholder"

**Help Scout Search:**
- "import error", "missing products", "images not showing"

**Contradiction Triggers:**
- 🔴 "Using test/sample data" while system shows 100+ products
- 🔴 "Haven't imported real products yet" while Stage 2 shows green
- ⚠️ "Need to re-import products" indicates data may be stale

---

## Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

**Applies to:** All Products

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 3.1 | Price levels configured | `get_price_levels` | `price_levels.count >= 1` |
| 3.2 | Multiple price levels | `get_price_levels` | `price_levels.count >= 2` (recommended) |
| 3.3 | Descriptive names | `get_price_levels` | Names not generic like "Price Level 1" |
| 3.4 | Unique codes assigned | `get_price_levels` | All price levels have unique codes |

### Thresholds
- 🔴 **Red:** No price levels configured
- 🟡 **Yellow:** Only 1 price level OR generic names OR missing/duplicate codes
- 🟢 **Green:** 2+ price levels with descriptive names AND unique codes

### Validation Layer Keywords

**Fathom Search:**
- "price levels", "pricing", "contract pricing", "test pricing", "placeholder pricing"

**Contradiction Triggers:**
- 🔴 "Pricing is test data" while system shows price levels configured
- 🔴 "Using placeholder pricing" while Stage 3 shows green
- ⚠️ "Need to set up contract pricing" indicates complex pricing not captured

---

## Stage 4: Option Configuration

**Goal:** If options enabled, CPQ/configurators are functional

**Applies to:** All Products (Conditional)

### Conditional Logic

```python
options = get_options(org_shortname)
if options["count"] == 0:
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
- ⚪ **N/A:** Options disabled (skip stage)
- 🔴 **Red:** Options enabled but count = 0
- 🟡 **Yellow:** Options < 5 or incomplete data
- 🟢 **Green:** Options >= 5 with complete configuration

### Validation Layer Keywords

**Fathom Search:**
- "options", "configurator", "CPQ", "fabric", "finish", "restructuring options"

**Contradiction Triggers:**
- 🔴 "Options not set up yet" while system shows options configured
- ⚠️ "Restructuring options" indicates pending changes

---

## Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

**Applies to:** All Products

### Conditional Logic: Territory vs Direct Assignment

```python
territories = get_user_territories(org_shortname)
if territories["count"] > 0:
    # Territory-based model
    validate_territory_assignments()
else:
    # Direct assignment model
    validate_direct_customer_user_relationships()
```

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 5.1 | Customers imported | `get_data_summary` | `customers.count >= 10` |
| 5.2 | Users configured | `get_org_users` | `org_users.count >= 2` |
| 5.3 | User types configured | `get_org_users` | Multiple user types exist |
| 5.4 | Recent customer update | `last_customer_update` | Within 30 days |
| 5.5 | Assignment logic configured | Territory OR Direct | Validated based on model |

### Thresholds
- 🔴 **Red:** Customers < 10 OR no users configured
- 🟡 **Yellow:** Customers 10-100 OR no recent update
- 🟢 **Green:** Customers > 100 AND recent update AND proper assignment

### Validation Layer Keywords

**Fathom Search:**
- "customer import", "territory", "rep assignment", "test customers"

**Contradiction Triggers:**
- 🔴 "Customer data needs re-import" while system shows customers exist
- 🔴 "Territories not set up" while system shows territory assignments
- 🔴 "Using test customers" while Stage 5 shows green
- ⚠️ "Price levels clobbered" indicates customer-specific pricing broken

---

## Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

**Applies to:** All Products

### Conditional Logic: Inventory Tracking

```python
if inventory_tracking_enabled:
    validate_inventory_data_exists()
    validate_recent_inventory_update()
else:
    stage_6_inventory_status = "N/A"
```

### Required Criteria

| # | Criterion | MCP Query | Pass Condition |
|---|-----------|-----------|----------------|
| 6.1 | Import health | `get_import_events` | No critical errors in last 30 days |
| 6.2 | Smart stacks | `get_smart_stacks` | At least 1 OR feature disabled |
| 6.3 | Inventory exists (if enabled) | `get_data_summary` | `inventories.count > 0` |
| 6.4 | Inventory fresh (if enabled) | `last_inventory_update` | Within 7 days |

### Thresholds
- 🔴 **Red:** Inventory enabled but no data OR critical import errors
- 🟡 **Yellow:** Stale inventory (7+ days) OR minor import warnings
- 🟢 **Green:** Fresh data AND no import errors

### Validation Layer Keywords

**Fathom Search:**
- "inventory", "import", "FTP", "imports failing", "manual import"

**Contradiction Triggers:**
- 🔴 "Inventory not connected" while system shows inventory data
- 🔴 "Imports failing" while system shows clean imports
- ⚠️ "Import schedule not set up" indicates manual process

---

# eCAT iPAD STAGE (7)

## Stage 7: iPad Order-Ready

**Goal:** iPad app can receive, process, and fulfill orders end-to-end

**Applies to:** eCat iPad Only

### Required Criteria

| # | Criterion | Validation Method | Pass Condition | Blocker Status |
|---|-----------|-------------------|----------------|----------------|
| 7.1 | iPad app activity | **BigQuery Mixpanel** | At least 1 order with `mp_lib='iphone'` | 🔴 **BLOCKER** |
| 7.2 | Presentation formats | `get_reports_config` | `count >= 3` | 🔴 **BLOCKER** |
| 7.3 | Test order processed | `get_orders` | `orders.count >= 1` | 🔴 **BLOCKER** |
| 7.4 | Order notification email | `order_email_recipient` | Not empty | 🟡 **Recommended** |
| 7.5 | Export type configured | `export_type` | Not empty (if ERP integration) | 🟡 **Conditional** |

### BigQuery Validation: iPad Activity

```sql
SELECT 
  COUNT(*) as ipad_order_count,
  COUNT(DISTINCT distinct_id) as unique_ipad_users,
  MIN(TIMESTAMP_SECONDS(CAST(time AS INT64))) as first_ipad_order,
  MAX(TIMESTAMP_SECONDS(CAST(time AS INT64))) as last_ipad_order
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.mixpanel_order_submitted`
WHERE currentorganizationshortname = '[ORG_SHORTNAME]'
  AND mp_lib = 'iphone'
```

**Pass Condition:** `ipad_order_count >= 1`

### Thresholds
- ⚪ **N/A:** eCat iPad not being implemented
- 🔴 **Red:** iPad activity OR reports OR test order missing
- 🟡 **Yellow:** Order email missing
- 🟢 **Green:** All critical criteria pass

### Validation Layer Keywords

**Fathom Search:**
- "iPad", "mobile app", "test order", "order export not configured"

**Contradiction Triggers:**
- 🔴 "Haven't tested orders yet" while system shows orders exist
- 🔴 "Orders are test orders" while Stage 7 shows green

---

# eCAT ONLINE STAGES (8-10)

## Stage 8: eCat Online Site Configuration

**Goal:** Web catalog is accessible and properly branded

**Applies to:** eCat Online, Sales Portal

**Prerequisites:** Stages 1-6 complete

### Required Criteria

| # | Criterion | MCP Query | Pass Condition | Blocker Status |
|---|-----------|-----------|----------------|----------------|
| 8.1 | Site exists and enabled | `get_mobile_sites` | `enabled: true` | 🔴 **BLOCKER** |
| 8.2 | Site name configured | `get_mobile_sites` | Not default name | 🔴 **BLOCKER** |
| 8.3 | Public user group exists | `get_permissions_summary` | Public group configured | 🔴 **BLOCKER** |
| 8.4 | Logos uploaded | `get_organization_info` | Logo URLs not empty | 🟡 **Recommended** |
| 8.5 | Custom domain | Site configuration | CNAME configured | 🟡 **Recommended** |
| 8.6 | Analytics enabled | Site configuration | Clicky enabled | 🟡 **Recommended** |

### Thresholds
- ⚪ **N/A:** eCat Online not being implemented
- 🔴 **Red:** No site OR disabled OR no public user group
- 🟡 **Yellow:** Missing logos OR default URL OR no analytics
- 🟢 **Green:** Site enabled with custom branding AND custom domain

### Validation Layer Keywords

**Fathom Search:**
- "eCat Online", "eOL", "web catalog", "site not ready", "test site"

**Contradiction Triggers:**
- 🔴 "Site not set up yet" while system shows site enabled
- 🔴 "Using temporary/test site" while Stage 8 shows green

---

## Stage 9: eCat Online User Access & Enrollment

**Goal:** Users can access the catalog via enrollment or direct invitation

**Applies to:** eCat Online, Sales Portal

**Prerequisites:** Stage 8 complete

### Conditional Logic: Public vs Closed Site

```python
if public_site:
    validate_public_user_group()
    validate_pricing_visibility()
else:
    validate_enrollment_workflow()
    validate_email_templates()
    validate_approval_admin()
```

### Required Criteria (Closed Site)

| # | Criterion | MCP Query | Pass Condition | Blocker Status |
|---|-----------|-----------|----------------|----------------|
| 9.1 | Enrollment form configured | `get_organization_info` | Enrollment templates exist | 🔴 **BLOCKER** |
| 9.2 | Approval workflow defined | Settings | Auto-approve or admin designated | 🔴 **BLOCKER** |
| 9.3 | Welcome email customized | `enrollment_welcome_template` | Not default template | 🟡 **Recommended** |
| 9.4 | Rejection email customized | `enrollment_denied_template` | Not default template | 🟡 **Recommended** |
| 9.5 | eCat Online user type exists | `get_org_users` | At least 1 eOL user type | 🟡 **Recommended** |

### Thresholds
- ⚪ **N/A:** eCat Online not being implemented
- 🔴 **Red:** Closed site with no enrollment workflow OR no approval admin
- 🟡 **Yellow:** Default email templates OR only 1 user type
- 🟢 **Green:** Enrollment workflow functional with customized templates

### Validation Layer Keywords

**Fathom Search:**
- "enrollment", "user access", "sign up", "email not customized"

**Contradiction Triggers:**
- 🔴 "Enrollment not configured" while system shows enrollment templates
- 🔴 "No users set up for online" while system shows eCat Online users

---

## Stage 10: eCat Online Ordering (B2B Cart)

**Goal:** If B2B ordering enabled, customers can place orders through web

**Applies to:** eCat Online (Conditional)

**Prerequisites:** Stage 9 complete

### Conditional Logic

```python
if b2b_ordering_enabled:
    validate_cart_functionality()
    validate_order_workflow()
    validate_test_order()
else:
    stage_10_status = "N/A"  # Catalog-only implementation
```

### Required Criteria (If B2B Enabled)

| # | Criterion | MCP Query | Pass Condition | Blocker Status |
|---|-----------|-----------|----------------|----------------|
| 10.1 | Cart functionality enabled | `get_organization_info` | Cart settings configured | 🔴 **BLOCKER** |
| 10.2 | Order email configured | `send_order_email_on_submit` | `true` | 🔴 **BLOCKER** |
| 10.3 | Order recipient configured | `order_email_recipient` | Not empty | 🔴 **BLOCKER** |
| 10.4 | Test web order exists | `get_orders` | At least 1 web order | 🔴 **BLOCKER** |
| 10.5 | PDF attachment enabled | `attach_pdf_to_order_email` | `true` | 🟡 **Recommended** |

### Thresholds
- ⚪ **N/A:** B2B ordering not enabled (catalog-only)
- 🔴 **Red:** Ordering enabled but no test order OR email not configured
- 🟡 **Yellow:** PDF attachment disabled
- 🟢 **Green:** Test orders submitted via web AND email verified

### Validation Layer Keywords

**Fathom Search:**
- "online order", "web order", "B2B", "cart not working"

**Contradiction Triggers:**
- 🔴 "Haven't tested web orders" while system shows orders exist
- 🔴 "Online ordering not enabled" while Stage 10 shows green

---

# SALES PORTAL STAGES (11-12)

## Stage 11: Sales Portal Data Configuration

**Goal:** Sales data imported and displaying accurately

**Applies to:** Sales Portal Only

**Prerequisites:** Stages 8-9 complete (eCat Online foundation required)

### Required Criteria

| # | Criterion | MCP Query | Pass Condition | Blocker Status |
|---|-----------|-----------|----------------|----------------|
| 11.1 | Portal enabled | `enable_portal_dashboard` | `true` | 🔴 **BLOCKER** |
| 11.2 | Invoice data imported | `get_import_events` | Portal Invoice import exists | 🔴 **BLOCKER** |
| 11.3 | Order data imported | `get_import_events` | Portal Orders import exists | 🔴 **BLOCKER** |
| 11.4 | No critical import errors | `get_import_events` | `total_errors: 0` | 🔴 **BLOCKER** |
| 11.5 | Data verified against ERP | Manual validation | Numbers match | 🔴 **BLOCKER** |
| 11.6 | Historical data (12+ months) | Import date range | Spans 12 months | 🟡 **Recommended** |
| 11.7 | Tracking data imported | `get_import_events` | Invoice tracking exists | 🟡 **Recommended** |

### Thresholds
- ⚪ **N/A:** Sales Portal not being implemented
- 🔴 **Red:** Portal enabled but no data OR critical import errors
- 🟡 **Yellow:** Less than 12 months history OR minor warnings
- 🟢 **Green:** Clean import with 12+ months AND verified against ERP

### Validation Layer Keywords

**Fathom Search:**
- "sales portal", "portal data", "invoice data", "numbers don't match"

**Contradiction Triggers:**
- 🔴 "Portal data not imported" while system shows portal imports
- 🔴 "Data doesn't match ERP" indicates validation failure

---

## Stage 12: Sales Portal User Access

**Goal:** Reps and customers can access sales data appropriate to their role

**Applies to:** Sales Portal Only

**Prerequisites:** Stage 11 complete

### ⚠️ CRITICAL: Sales Portal is Web-Based, NOT iPad Native

**Lesson Learned (V9 Assessment - KLL):** A common misconception is that Sales Portal appears in the iPad app. It does NOT.

**Sales Portal Access:**
- **URL Pattern:** `https://catalog.[domain].com/[org]/e/1/portal`
- **Example:** `https://catalog.kuzcolighting.com/kll/e/1/portal`
- **Access Method:** Web browser (desktop, tablet, mobile)
- **NOT in:** iPad app native interface

**Common Issue:** Users (like reps at trade shows) may report "can't see Sales Portal on iPad" when they're actually looking in the wrong place. The iPad app handles orders; the Sales Portal is a separate web experience.

**Permission Requirement:** User type must have `Enable sales portal` checkbox enabled in Admin Console → User Types.

### Required Criteria

| # | Criterion | MCP Query | Pass Condition | Blocker Status |
|---|-----------|-----------|----------------|----------------|
| 12.1 | Portal permissions configured | `get_permissions_summary` | Portal access in user types | 🔴 **BLOCKER** |
| 12.2 | Territory assignments correct | `analyze_user_permissions` | Reps see correct customers | 🔴 **BLOCKER** |
| 12.3 | Rep verification | Manual test | At least 1 rep sees correct data | 🔴 **BLOCKER** |
| 12.4 | SSO configured | `external_auth_provider` | Configured (if required) | 🟡 **Recommended** |
| 12.5 | Customer self-service | Manual test | Customers see own data | 🟡 **Conditional** |

### Thresholds
- ⚪ **N/A:** Sales Portal not being implemented
- 🔴 **Red:** No users can access portal OR territory assignments broken
- 🟡 **Yellow:** Only admin can see data OR SSO not configured
- 🟢 **Green:** Reps see their territory data correctly AND SSO functional

### Validation Layer Keywords

**Fathom Search:**
- "portal access", "rep access", "SSO", "wrong customers showing"

**Contradiction Triggers:**
- 🔴 "Reps can't access portal" while system shows permissions configured
- 🔴 "Seeing wrong customers" indicates territory misconfiguration

---

# VALIDATION LAYER IMPLEMENTATION

## ⚠️ CRITICAL: Evidence-Based Validation

**Every validation flag MUST include the actual quote/sentiment from the source.**

DO NOT simply say "flagged" or "issue detected." ALWAYS include:
- The **exact quote** from Fathom transcript/summary
- The **ticket excerpt** from Help Scout
- The **date** the evidence was captured
- The **source** (which call or ticket)

### ❌ BAD Example (Do Not Do This)
```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | 🔴 CONTRADICT | Help Scout | Customer data issue flagged |
```

### ✅ GOOD Example (Required Format)
```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | 🔴 CONTRADICT | Help Scout #12345 (Jan 10) | *"Customer data requires re-import. A script clobbered customer-specific price levels (e.g., DSFOB C6) with default (Z3T1)."* |
```

---

## Fathom API Integration

### Configuration

```python
# File: /fathom/fathom_api.py
FATHOM_API_KEY = "[stored in fathom_api.py]"
FATHOM_BASE_URL = "https://fathom.video/external/v1"
```

### Query Strategy

**CRITICAL:** When searching for client calls, you MUST be extremely diligent:

1. **Search Call Titles** - Search for:
   - Full company name (e.g., "Craftmade")
   - Company shortname (e.g., "clli")
   - Variations of name
   - Key contact names if known

2. **Search Call Summaries** - The AI summary often contains:
   - Company name mentions not in title
   - Implementation status discussions
   - Issue/blocker mentions

3. **Search Call Transcripts** - For deep validation:
   - Search for company name within transcript text
   - Search for product names mentioned ("eCat Online", "Sales Portal")
   - Search for stage-relevant keywords

### API Functions

```python
# Get ALL meetings (with pagination - ALWAYS use paginate=True)
meetings = get_meetings(paginate=True)

# Get summary for specific meeting
summary = get_summary(recording_id)

# Get full transcript for specific meeting
transcript = get_transcript(recording_id)
```

### ⚠️ Troubleshooting: Meetings Without IDs

**Known Issue:** The Fathom API may return meetings with `id: None`. This happens when:
- The meeting was recently recorded and hasn't fully processed
- The meeting is a calendar hold without a recording
- API sync delays (especially for same-day calls)

**When this happens:**

1. **Document the gap** - Note that Fathom calls exist but transcripts unavailable
2. **Flag for manual review** - Add `⚠️ PENDING` flag indicating validation incomplete
3. **Retry later** - Same-day calls may take 1-24 hours to process with IDs
4. **Use title/date as context** - Even without transcript, note the meeting occurred

```markdown
### Validation Flags

| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 7 | ⚠️ PENDING | Fathom | Meeting found: "eCat x Coaster Standup" (Jan 14) - transcript unavailable, retry in 24 hours |
```

### 🔴 CRITICAL: "[Hold]" Meeting Pattern Detection

**Lesson Learned (V9 Assessment - CST):** Meetings with `[Hold]` prefix in the title indicate **stalled implementations**.

**Detection Pattern:**
```python
for meeting in meetings:
    title = meeting.get('title', '')
    if '[Hold]' in title or '[HOLD]' in title:
        # Flag as stalled implementation
        flag_type = "🔴 STALLED"
        evidence = f"Meeting '{title}' indicates implementation paused"
```

**Example from Real Assessment:**
```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 7 | 🔴 STALLED | Fathom | Multiple meetings titled "[Hold] eCat x Coaster Standup" - implementation paused. 0 iPad orders despite 6,420 customers loaded. |
```

**Action Required:** When `[Hold]` pattern detected:
1. Flag all related stages as `🔴 STALLED`
2. Identify what's blocking (usually customer data or client action)
3. Determine reactivation timeline
4. Do NOT count as "in progress" - this is a pause state

### Required: Include Actual Quotes

**When Fathom data IS available, you MUST quote directly:**

```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 3 | ⚠️ REVIEW | Fathom (Dec 3 call) | *"Use eCat's Contract Pricing feature for all pricing."* - May not align with 19 standard price levels in system |
| 7 | 🔴 CONTRADICT | Fathom (Jan 6 call) | *"Customer data requires re-import. A script clobbered customer-specific price levels."* |
```

---

## Help Scout BigQuery Integration

### Configuration

```
Project: supercat-data-pipeline
Dataset: hevo_dataset_supercat_data_pipeline_Slhk
Table: help_scout_tickets (VIEW)
```

### Mailboxes to Query

**CRITICAL:** You MUST query BOTH mailboxes:

| Mailbox ID | Mailbox Name | Email |
|------------|--------------|-------|
| 312855 | SuperCat Onboarding | onboarding@supercatsolutions.com |
| 65829 | SuperCat Support | support@supercatsolutions.com |

### Ticket Statuses to Include

**CRITICAL:** You MUST query ALL ticket statuses:
- `active` - Currently open (MOST IMPORTANT - indicates ongoing issues)
- `pending` - Awaiting response
- `closed` - Resolved (still useful for historical context)

### Query Template

```sql
SELECT DISTINCT
    ticket_number,
    ticket_subject,
    ticket_status,
    ticket_created_at,
    mailbox_name,
    conv_customer_organization,
    ticket_preview,  -- Include preview for quick context
    LEFT(thread_body, 500) as thread_excerpt  -- MUST include excerpt
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
    (LOWER(conv_customer_organization) LIKE LOWER('%[CLIENT_NAME]%')
    OR LOWER(conv_customer_email) LIKE LOWER('%@[CLIENT_DOMAIN]%')
    OR LOWER(ticket_subject) LIKE LOWER('%[CLIENT_NAME]%')
    OR LOWER(thread_body) LIKE LOWER('%[CLIENT_NAME]%'))
    AND mailbox_id IN (312855, 65829)
    AND ticket_status IN ('active', 'pending', 'closed')
ORDER BY ticket_created_at DESC
```

### ⚠️ CRITICAL: Active Tickets Require Special Attention

**If ANY active or pending tickets exist for a client, they MUST be:**

1. **Included in the assessment** - Never skip active tickets
2. **Quoted with context** - Include the relevant excerpt
3. **Flagged appropriately** - Active tickets often indicate blockers

### 🔴 CRITICAL: Unfulfilled Commitment Detection

**Lesson Learned (V9 Assessment - TCD):** Track client promises that haven't been delivered.

**Pattern to Detect:**
Look for phrases like:
- "will get it ready by the end of this week"
- "will send the file tomorrow"
- "should have this done by [date]"

Then check if the promised deliverable ever arrived (compare system state to promise).

**Example from Real Assessment:**
```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | ⚠️ UNFULFILLED | Help Scout (Nov 2025) | *"For now, we don't have a customer list file, but we will get it ready by the end of this week."* — 2 months later: still 0 customers in system |
```

**Action Required:** When unfulfilled commitment detected:
1. Note the original promise date
2. Calculate days since promise
3. Check if deliverable arrived (verify in MCP)
4. If not delivered: Flag and schedule follow-up

### Required: Include Ticket Excerpts

**Every Help Scout validation flag MUST include actual ticket content:**

```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | 🔴 ACTIVE | Help Scout (Nov 17) | Subject: "Re: Terracotta Onboarding Kickoff Follow Ups" - *"I'd love the opportunity to meet and speak with you in person at Dallas Market, showroom #3751..."* - Indicates ongoing coordination needed |
```

**DO NOT do this:**
```markdown
| Stage | Flag | Source | Evidence |
|-------|------|--------|----------|
| 5 | ⚠️ REVIEW | Help Scout | Active ticket exists |
```

---

## Global Sentiment & Activity Flags

### Sentiment Keywords

| Keyword/Phrase | Flag Type | Action |
|----------------|-----------|--------|
| "disappointed" | ⚠️ SENTIMENT | Review context |
| "frustrated" | ⚠️ SENTIMENT | Escalate |
| "amateur" | 🔴 SENTIMENT | Urgent escalation |
| "early-stage" (negative context) | 🔴 SENTIMENT | Urgent escalation |
| "not mature" / "immature" | 🔴 SENTIMENT | Urgent escalation |
| "would not have signed up" | 🔴 CHURN RISK | Immediate notification |
| "had I known" | 🔴 CHURN RISK | Immediate notification |
| "cancel" OR "cancellation" | 🔴 CHURN RISK | Immediate notification |
| "refund" | 🔴 CHURN RISK | Immediate notification |

**Real-World Example (TCD - Dec 2025):**
> *"The tool feels less like a mature commercial product and more like an early-stage amateur implementation. Had I known this earlier, I likely would not have signed up."*
> 
> This single message contains **4 sentiment triggers**: "amateur", "early-stage", "Had I known", "would not have signed up" — triggering both `🔴 SENTIMENT` and `🔴 CHURN RISK`.

### Activity Thresholds

| Condition | Flag | Action |
|-----------|------|--------|
| 0 Fathom calls in 60 days | ⚠️ ACTIVITY | Check engagement |
| 0 Help Scout tickets in 60 days | ⚠️ ACTIVITY | Proactive outreach |
| 0 Fathom AND 0 Help Scout in 90 days | 🔴 ACTIVITY | Potential abandonment |
| No MCP data updates in 30 days | ⚠️ ACTIVITY | Check import status |
| "[Hold]" prefix on recurring meetings | 🔴 STALLED | Implementation paused - clarify timeline |
| Client promise 30+ days unfulfilled | ⚠️ UNFULFILLED | Follow up on commitment |
| Active ticket 60+ days old | ⚠️ STALLED | Resolution needed |

---

## MCP Endpoints Required

| Endpoint | Purpose | Stages |
|----------|---------|--------|
| `get_organization_info` | Org status and settings | 1, 7, 8, 9, 10, 11, 12 |
| `get_data_summary` | Counts | 2, 5, 6 |
| `get_org_users` | User configuration | 1, 5, 9 |
| `get_price_levels` | Pricing setup | 3 |
| `get_options` | Options validation (conditional) | 4 |
| `get_user_territories` | Territory validation (conditional) | 5, 12 |
| `get_categories` | Taxonomy | 2 |
| `get_collections` | Product organization | 2 |
| `get_mobile_sites` | eCat Online site config | 8 |
| `get_reports_config` | Report formats | 7 |
| `get_orders` | Order validation | 7, 10 |
| `get_import_events` | Data health | 6, 11 |
| `get_smart_stacks` | Smart list config (conditional) | 6 |
| `get_permissions_summary` | User permissions | 8, 9, 12 |
| `analyze_user_permissions` | Deep permission check | 12 |

---

## BigQuery Endpoints Required

| Query | Purpose | Stage |
|-------|---------|-------|
| Mixpanel `order_submitted` with `mp_lib='iphone'` | iPad activity validation | 7 |
| Help Scout `help_scout_tickets` | Validation layer | All |

---

## Approvals

| Role | Name | Date | Status |
|------|------|------|--------|
| **Author** | Kylor Johnson | Jan 14, 2026 | ✅ Complete (v3.1) |
| **CS Lead** | [Name] | [Date] | ⏳ Pending |
| **Engineering Lead** | [Name] | [Date] | ⏳ Pending |
| **Product Manager** | [Name] | [Date] | ⏳ Pending |

---

**Document Status:** Draft - Ready for Review  
**Version:** 3.1 (Multi-Product + Validation Layer + Lessons Learned)  
**Last Updated:** January 14, 2026  
**Contact:** Kylor Johnson
