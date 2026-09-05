# TTFV Analysis - README

## What is TTFV?

**Time to First Value (TTFV)** measures how quickly a new client's sales team starts actively using SuperCat's core selling tools after their deal closes. It answers: *How long does it take before a real sales rep does something meaningful in the platform?*

### What Counts as "First Value"

| Action | Description |
|--------|-------------|
| **Presentation/Stack** | Rep adds a product to a curated selection for a customer |
| **Email Draft** | Rep drafts an email to a customer with product information |

These represent intentional selling activity, not just logging in or browsing.

### Why Admins Are Excluded

TTFV only counts activity from non-admin users because admin activity during onboarding (testing, configuring, training) doesn't represent real sales adoption.

---

## How to Run TTFV Analysis

### Standard Analysis (All Active Clients)

```
Calculate the TTFV for all active clients using @ttfv/TTFV_Analysis_Prompt.md
```

### Specific Client Cohort (e.g., 2025 Clients)

```
Calculate the TTFV for all clients in @ttfv/2025_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Also provide a monthly averages CSV with months as columns and average TTFV days as the data row.
```

### For Specific Clients by Name

```
Calculate the TTFV for [Client Name 1], [Client Name 2] using @ttfv/TTFV_Analysis_Prompt.md
```

---

## Files in This Folder

### Core Files (Always Keep)
| File | Purpose |
|------|---------|
| `README.md` | This file - start here |
| `TTFV_Analysis_Prompt.md` | The calculation logic and steps (reference this in Cursor prompts) |
| `TTFV_Report_Format_Template.md` | Output formatting guide for reports |
| `TTFV_Methodology_Overview.md` | Detailed explanation of the metric |

### Client Lists
| File | Purpose |
|------|---------|
| `active_orgs.csv` | **Legacy static snapshot — do not rely on for current data.** The authoritative active client list is derived live from Postgres `subscriptions` (see `TTFV_Analysis_Prompt.md` Step 1). |
| `2025_clients.csv` | 2025 new client cohort. As of April 2026, contains 9 verified active orgs with `start_date` sourced from `subscriptions.start_date`. Regenerated from Postgres — do not edit manually. |

### Generated Outputs (Examples)
| File | Purpose |
|------|---------|
| `2025_clients_monthly_averages.csv` | Monthly TTFV averages for 2025 cohort |
| `TTFV_Analysis_Report_*.md` | Detailed analysis reports (dated) |

---

## Quick Reference: Common Use Cases

### 1. Monthly TTFV Review for New Clients
**Goal:** Track TTFV for clients that closed in the current year

**Steps:**
1. Update the client CSV (e.g., `2026_clients.csv`) with new clients and close dates
2. Run: `Calculate TTFV for all clients in @ttfv/2026_clients.csv using @ttfv/TTFV_Analysis_Prompt.md`
3. Request monthly averages CSV output

**Output:** Monthly breakdown showing average TTFV by cohort

---

### 2. Full Active Client TTFV Report
**Goal:** Comprehensive TTFV analysis across all active clients

**Steps:**
1. Run: `Calculate TTFV for all active clients using @ttfv/TTFV_Analysis_Prompt.md`

**Output:** Full report with statistics, insights, and clients needing attention

---

### 3. Specific Client Deep Dive
**Goal:** Investigate TTFV for specific clients

**Steps:**
1. Run: `Calculate TTFV for [Client Name] using @ttfv/TTFV_Analysis_Prompt.md`

**Output:** Detailed TTFV breakdown for named clients

---

## Understanding the Results

| TTFV Result | What It Means |
|-------------|---------------|
| **Low TTFV (fast)** | Smooth onboarding, engaged sales team |
| **High TTFV (slow)** | Potential onboarding friction or adoption challenges |
| **No Valid TTFV** | Only admin activity recorded - sales reps not yet engaged |
| **No TTFV Events** | No qualifying events at all - may need enablement focus |

### Start Date Reference

| Value | Meaning |
|-------|---------|
| `subscriptions.start_date` | The date the org's subscription became active in Postgres — authoritative TTFV clock start |

> **Legacy values (no longer used):** `HubSpot` (deal close date) and `created_at` (org creation date) were previously used as start dates but have been replaced by `subscriptions.start_date` as the single source of truth.

---

## Data Sources

The analysis pulls from:

- **SuperCat Postgres** - Active client list, subscription start dates (`subscriptions.start_date`), admin status
- **Mixpanel** (via BigQuery) - User activity events

> **Note:** HubSpot deal close dates and `organizations.created_at` are no longer used as TTFV start dates. `subscriptions.start_date` is the authoritative clock start.

---

## Tips

- **Run monthly** to track TTFV for new clients
- **Focus on cohorts with subscription start dates** (like 2025_clients.csv) for accurate TTFV benchmarking
- **New clients are automatic** — any org with a new `subscriptions.start_date` in the target year will appear in the Step 1 Postgres query without manual CSV updates
- **Negative TTFV** means sales activity occurred before the subscription was formally activated
- **Client not showing up?** Check that they have a `subscriptions` row with `status = 'active'` in Postgres

---

## Questions?

For methodology details, see `TTFV_Methodology_Overview.md`

For calculation steps, see `TTFV_Analysis_Prompt.md`
