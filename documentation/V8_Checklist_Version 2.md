# V8 Multi-Product Stage-Gated Onboarding Checklist

**Version:** 8.0  
**Last Updated:** January 2026

---

## Quick Reference: Which Stages to Run

| Products Purchased | Stages to Run |
|-------------------|---------------|
| eCat iPad only | 1-7 |
| eCat iPad + eCat Online | 1-8 |
| eCat iPad + Sales Portal | 1-7, 9 |
| All three products | 1-9 |
| eCat Online only | 1-6, 8 |
| Sales Portal only | 1-6, 9 |

**Check HubSpot "Associated Product(s)" field before running assessment.**

---

## Stage 1: Account Foundation

**Goal:** Organization exists with basic configuration complete

### Checklist

- [ ] Company name filled in
- [ ] At least 1 admin user exists (excluding internal: Kylor_Johnson, brentsanders, cwiebe)
- [ ] Settings initialized with defaults

### Pass Criteria

- 🔴 **RED (BLOCKER):** Any item above unchecked
- 🟢 **GREEN (READY):** All items checked

### How to Validate

- Run: `get_organization_info` (check `company_information.name`)
- Run: `get_org_users` (verify `is_admin: true` exists)

---

## Stage 2: Catalog Setup

**Goal:** Products imported and browsable by users

### Checklist

- [ ] At least 10 products imported
- [ ] At least 10 products have images
- [ ] At least 1 category configured
- [ ] At least 1 collection exists
- [ ] Products updated within last 30 days

### Pass Criteria

- 🔴 **RED (BLOCKER):** Less than 10 products imported
- 🟡 **YELLOW (WARNING):** 10-100 products OR no updates in 60+ days OR less than 10 products with images
- 🟢 **GREEN (READY):** 100+ products AND updated within last 30 days

### How to Validate

- Run: `get_data_summary` (check `products.count`)
- Run: `get_categories`
- Run: `get_collections`
- Check: `last_product_update` date

---

## Stage 3: Pricing Configuration

**Goal:** Products can be priced and purchased

### Checklist

- [ ] Price levels configured
- [ ] At least 2 price levels configured (recommended)
- [ ] Price levels have descriptive names (not "Price Level 1")
- [ ] Price level codes assigned (recommended)

### Pass Criteria

- 🔴 **RED (BLOCKER):** No price levels configured
- 🟡 **YELLOW (WARNING):** Only 1 price level OR generic names OR missing codes
- 🟢 **GREEN (READY):** 2+ price levels with descriptive names AND unique codes

### How to Validate

- Run: `get_price_levels`
- Sample products to verify pricing data completeness

---

## Stage 4: Option Configuration

**Goal:** If options enabled, CPQ/configurators are functional

### Check if Stage Applies

- [ ] Run `get_options` - does it return any options?
    - **YES** → Continue with checklist below
    - **NO** → Mark stage as **⚪ N/A** and skip to Stage 5

### Checklist (If Options Enabled)

- [ ] At least 1 option configured

### Pass Criteria

- ⚪ **N/A:** Options disabled - skip this stage
- 🔴 **RED (BLOCKER):** Options enabled but none configured
- 🟡 **YELLOW (WARNING):** Less than 5 options configured
- 🟢 **GREEN (READY):** 5+ options configured

### How to Validate

- Run: `get_options`
- Check: `require_valid_options_to_submit_orders` setting

---

## Stage 5: Customer & User Setup

**Goal:** Buyer/seller relationships properly configured

### Check Assignment Model

- [ ] Run `get_user_territories` - are territories configured?
    - **YES** → Use Territory Model checklist
    - **NO** → Use Direct Assignment checklist

### Checklist (Both Models)

- [ ] At least 10 customers imported
- [ ] At least 2 users configured
- [ ] Multiple user types exist
- [ ] Customers updated within last 30 days

### Additional: Territory Model

- [ ] At least 1 territory exists
- [ ] Users assigned to territories (via `territory_codes`)

### Additional: Direct Assignment Model

- [ ] Customers directly assigned to users

### Pass Criteria

- 🔴 **RED (BLOCKER):** Less than 10 customers OR no users configured
- 🟡 **YELLOW (WARNING):** 10-100 customers OR no updates in 30+ days
- 🟢 **GREEN (READY):** 100+ customers AND updated within last 30 days AND proper assignments

### How to Validate

- Run: `get_data_summary` (check `customers.count`)
- Run: `get_org_users`
- Run: `get_user_territories`
- Check: `last_customer_update` date

---

## Stage 6: Operational Data

**Goal:** Real-time data flowing (inventory, imports)

### Check if Inventory Tracking Applies

- [ ] Is inventory tracking enabled?
    - **YES** → Include inventory checks
    - **NO** → Skip inventory checks (mark **⚪ N/A**)

### Checklist (Always Required)

- [ ] No critical import errors in last 30 days
- [ ] Smart stacks configured OR feature disabled

### Additional: If Inventory Enabled

- [ ] Inventory data exists (`inventories.count > 0`)
- [ ] Inventory updated within last 7 days

### Pass Criteria

- 🔴 **RED (BLOCKER):** Inventory enabled but no data OR critical import errors
- 🟡 **YELLOW (WARNING):** Stale inventory (7+ days) OR minor import warnings
- 🟢 **GREEN (READY):** Fresh data AND no import errors

### How to Validate

- Run: `get_data_summary` (check `inventories.count`)
- Run: `get_import_events` (review last 30 days)
- Run: `get_smart_stacks`

---

## Stage 7: eCat iPad Order-Ready

**Goal:** iPad app can receive, process, and fulfill orders end-to-end

### ⚠️ Only Run If: HubSpot includes "eCat iPad"

### Checklist

- [ ] 1+ user types exist (more than Default User Group)
- [ ] At least 1 user has logged into eCat iPad app
- [ ] Report formats configured (minimum 3)
- [ ] Test order processed (at least 1 order exists)
- [ ] Order notification email configured (recommended)
- [ ] Export type configured if ERP integration needed (recommended)

### Pass Criteria

- 🔴 **RED (BLOCKER):** No iPad logins OR no report formats OR no test order
- 🟡 **YELLOW (WARNING):** All blockers pass but email not configured OR no recent activity
- 🟢 **GREEN (READY):** All criteria pass AND recent iPad activity

### How to Validate

- Run: `get_org_users` (check user types)
- Run: `get_reports_config` (verify count >= 3)
- Run: `get_orders` (verify count >= 1)
- BigQuery: Query `mixpanel_selected_org` for iPad logins (see FRD for SQL)

---

## Stage 8: eCat Online (B2B Web Portal)

**Goal:** Web-based B2B catalog is accessible and customers can browse/order online

### ⚠️ Only Run If: HubSpot includes "eCat Online"

### Prerequisites

- [ ] Stages 1-6 must be GREEN

### Checklist

- [ ] Mobile site enabled (at least 1 with `enabled: true`)
- [ ] More than 1 user group exists
- [ ] At least 1 customer/online user created
- [ ] Enrollment email recipients configured (recommended)

### Pass Criteria

- 🔴 **RED (BLOCKER):** Mobile site disabled OR only 1 user group OR no online users
- 🟡 **YELLOW (WARNING):** All blockers pass but enrollment not configured
- 🟢 **GREEN (READY):** All critical + recommended criteria pass

### How to Validate

- Run: `get_mobile_sites` (check `enabled: true`)
- Run: `get_org_users` (check distinct `user_type` count > 1)
- Run: `get_organization_settings` (check `enrollment_email_recipients`)

---

## Stage 9: Sales Portal (Analytics Dashboard)

**Goal:** Sales analytics portal is configured with data and accessible to authorized users

### ⚠️ Only Run If: HubSpot includes "eCat Sales Portal"

### Prerequisites

- [ ] Stages 1-6 must be GREEN
- [ ] eCat Online (Stage 8) recommended but not required

### Checklist

- [ ] Portal dashboard feature enabled (`enable_portal_dashboard: true`)
- [ ] Order data file uploaded (CSV)
- [ ] Invoice data file uploaded (CSV)
- [ ] Data verified against ERP source (recommended)
- [ ] Territory/user permissions configured (recommended)

### Pass Criteria

- 🔴 **RED (BLOCKER):** Portal disabled OR no order data OR no invoice data
- 🟡 **YELLOW (WARNING):** All blockers pass but ERP not verified OR no permissions
- 🟢 **GREEN (READY):** All criteria pass AND data verified accurate

### How to Validate

- Run: `get_organization_settings` (check `flags.enable_portal_dashboard`)
- Manual check: Order/invoice data visible in portal admin
- Run: `get_user_territories` OR `get_org_users` (check permissions)

---

## Quick Reference: Status Colors

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| 🔴 RED | Launch Blocker | Stop - must resolve before proceeding |
| 🟡 YELLOW | Warning | Can launch but requires CS follow-up |
| 🟢 GREEN | Ready | Proceed to next stage |
| ⚪ N/A | Not Applicable | Feature disabled - skip validation |

---

## Critical Launch Blockers Summary

### eCat iPad (Stages 1-7)

| # | Blocker | Stage |
|---|---------|-------|
| 1 | Price levels configured | 3 |
| 2 | Customers imported | 5 |
| 3 | iPad app logins | 7 |
| 4 | Report formats configured | 7 |
| 5 | Test order processed | 7 |

### eCat Online (Stages 1-6 + 8)

| # | Blocker | Stage |
|---|---------|-------|
| 1 | Price levels configured | 3 |
| 2 | Customers imported | 5 |
| 3 | Mobile site enabled | 8 |
| 4 | Multiple user groups | 8 |
| 5 | Online user created | 8 |

### Sales Portal (Stages 1-6 + 9)

| # | Blocker | Stage |
|---|---------|-------|
| 1 | Portal dashboard enabled | 9 |
| 2 | Order data uploaded | 9 |
| 3 | Invoice data uploaded | 9 |

---

## Validation Overlay: Fathom + Help Scout

After completing the data-driven assessment, apply the **Validation Overlay** to catch contradictions:

1. **Query Fathom API** for implementation/onboarding calls (last 90 days)
2. **Query Help Scout** (BigQuery) for support tickets (BOTH inboxes, ALL statuses)
3. **Flag any contradictions** between system data and conversations

### ⚠️ CRITICAL: Include Actual Quotes

**Every flag MUST include:**
- The **exact quote** from the call/ticket
- The **date** of the evidence
- The **source** (call title or ticket number)

### ❌ Wrong Way
```markdown
| Stage | Flag | Evidence |
|-------|------|----------|
| 5 | 🔴 CONTRADICT | Customer data issue flagged |
```

### ✅ Right Way
```markdown
| Stage | Flag | Evidence |
|-------|------|----------|
| 5 | 🔴 CONTRADICT | Fathom (Jan 14): *"Customer data requires re-import. Script clobbered price levels."* |
```

### Flag Types

| Flag | Icon | Meaning |
|------|------|---------|
| CONTRADICT | 🔴 | Evidence directly contradicts system data |
| REVIEW | ⚠️ | Needs clarification from CSM |
| TIMELINE | ⏰ | Date/target has changed |
| ACTIVITY | 📭 | Zero engagement signals |
| PENDING | ⏳ | Fathom call found, transcript unavailable (retry in 24h) |
| CONFIRMED | ✅ | Qualitative sources validate data |

### Fathom: What If IDs Are Null?

If Fathom returns meetings without IDs (common for same-day calls):
- Note the meeting title and date
- Add ⏳ PENDING flag
- Retry in 24 hours for full transcript

---

**For detailed validation queries and technical implementation, see FRD V8 3.0**
