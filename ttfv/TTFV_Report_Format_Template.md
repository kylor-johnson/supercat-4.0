# TTFV Report Format Template

Use this template to format all TTFV Analysis reports for consistency.

---

## Report Structure

### 1. Header

```markdown
# TTFV Analysis Report - [REPORT SCOPE]
**Generated:** [DATE]

---
```

### 2. Executive Summary

```markdown
## Executive Summary

This report calculates the **Time to First Value (TTFV)** for all active SuperCat clients. TTFV measures the number of days from a baseline date to the first time a **non-admin sales rep** performed a value-generating action:
- **Presentation/Stack**: Added a product via magic button
- **Email Draft**: Drafted an email from the platform

### Start Date Methodology (Hybrid Approach)
- **Primary**: HubSpot deal close date (when available)
- **Fallback**: Organization `created_at` date from Postgres (for legacy clients without HubSpot data)

**Note:** TTFV is only valid when performed by a non-admin user, as admin activity during implementation doesn't represent true sales adoption.

---
```

### 3. Summary Statistics

```markdown
## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Active Orgs** | [COUNT] |
| **Orgs with Valid TTFV** | [COUNT] |
| **Orgs with No Valid TTFV** | [COUNT] |
| **Orgs Using HubSpot (Start Date)** | [COUNT] |
| **Orgs Using Created_At (Start Date)** | [COUNT] |

---
```

### 4. Complete TTFV Results Table

```markdown
## Complete TTFV Results

| Organization Name | TTFV (Days) | Action Type | Start Date | First Action Date | Start Date Reference |
|-------------------|-------------|-------------|------------|-------------------|----------------------|
| [Org Name] | [Days] | [Email Draft or Presentation (Stack)] | [YYYY-MM-DD] | [YYYY-MM-DD] | [HubSpot or created_at] |
```

**Column Definitions:**
- **Organization Name**: Full client name
- **TTFV (Days)**: Number of days from Start Date to First Action Date
- **Action Type**: Either "Email Draft" or "Presentation (Stack)"
- **Start Date**: The baseline date (HubSpot close or created_at)
- **First Action Date**: Date of first valid non-admin TTFV event
- **Start Date Reference**: Source of the Start Date ("HubSpot" or "created_at")

**For orgs without valid TTFV:**
```markdown
| [Org Name] | - | - | - | - | No Valid TTFV |
| [Org Name] | - | - | - | - | No TTFV Events |
```

### 5. TTFV Analysis by Start Date Source

```markdown
---

## TTFV Analysis by Baseline Source

### HubSpot Close Date (Most Accurate - Recent Deals)

| Organization | Close Date | First Value Date | TTFV (Days) | Action Type |
|--------------|------------|------------------|-------------|-------------|
| [Org Name] | [YYYY-MM-DD] | [YYYY-MM-DD] | **[Days]** | [Action Type] |

#### HubSpot TTFV Statistics
- **Best TTFV:** [X] days ([Org Name])
- **Average TTFV:** [X] days
- **Median TTFV:** [X] days

---

### Created_At as Start Date (Legacy Clients)

For legacy clients, TTFV from `created_at` reflects time since initial platform setup. These numbers are large because many clients were set up years ago but the Mixpanel tracking of value events started more recently (around Nov 2024).

#### Recent Implementations (created_at within last 2 years)

| Organization | Created | First Value | TTFV (Days) |
|--------------|---------|-------------|-------------|
| [Org Name] | [YYYY-MM-DD] | [YYYY-MM-DD] | **[Days]** |

#### Recent Implementation Statistics (created_at in [YEAR])
- **Best TTFV:** [X] days ([Org Name])
- **Average TTFV:** [X] days
- **Median TTFV:** [X] days

---
```

### 6. Orgs Without Valid TTFV

```markdown
## Orgs Without Valid TTFV

| Organization Name | Reason |
|-------------------|--------|
| [Org Name] | Admin-only TTFV activity |
| [Org Name] | No TTFV events recorded |

---
```

### 7. Key Insights

```markdown
## Key Insights

### 1. HubSpot-Tracked Deals (Most Reliable)
For the [X] recent deals with HubSpot close dates:
- **Average TTFV: [X] days**
- **Best performers:** [Org] ([X] days), [Org] ([X] days), [Org] ([X] days)
- **Slowest:** [Org] ([X] days)

### 2. Recent Implementations ([YEAR] created_at)
For clients created in [YEAR] (using created_at as baseline):
- **Average TTFV: [X] days**
- **Best performers:** [Org] ([X] days), [Org] ([X] days), [Org] ([X] days)

### 3. Anomalies
- [Note any negative TTFV values or other anomalies]

### 4. Clients Needing Attention
[X] orgs have no valid non-admin TTFV:
- [X] have admin-only activity (sales reps not yet engaged)
- [X] have no TTFV events at all (may need enablement focus)

---
```

### 8. Methodology Notes

```markdown
## Methodology Notes

1. **Start Date Priority:**
   - Primary: HubSpot deal close date (stage `53599608` = Closed-Won)
   - Fallback: Postgres `organizations.created_at`

2. **Admin Exclusion:** Users with `is_admin = TRUE` in Postgres `org_users` table are excluded from TTFV calculations.

3. **Value Actions Tracked:**
   - `item_added_via_magic_button` (Presentation/Stack)
   - `document_email_drafted` (Email Draft)
   - `item_email_drafted` (Email Draft)

4. **Data Sources:**
   - Deal close dates: BigQuery `hubspot__deal` table
   - TTFV events: BigQuery `mixpanel__events` table
   - Admin status: Postgres `org_users` table
   - Org created dates: Postgres `organizations` table

---

*Report generated using SuperCat TTFV Analysis methodology (Hybrid Approach).*
```

---

## Date Formats

- All dates should use **YYYY-MM-DD** format in tables
- Generated date in header can use full format (e.g., "February 14, 2026")

## Number Formats

- TTFV days should be whole numbers
- Large numbers (1,000+) should include commas for readability
- Bold (**) the TTFV days in summary/highlight tables

## Action Types

Use exactly these values:
- `Email Draft` - for document_email_drafted or item_email_drafted events
- `Presentation (Stack)` - for item_added_via_magic_button events

## Start Date Reference Values

Use exactly these values:
- `HubSpot` - when using deal close date
- `created_at` - when using organization creation date
- `No Valid TTFV` - when org has only admin TTFV activity
- `No TTFV Events` - when org has no TTFV events at all
