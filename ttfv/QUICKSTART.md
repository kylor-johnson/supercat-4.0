# TTFV Analysis - Quick Start Guide

## For New Users

If you're new to TTFV analysis, start here.

---

## What You Need

1. **Cursor IDE** with access to this workspace
2. **MCP Connections** configured:
   - BigQuery (for HubSpot and Mixpanel data)
   - Postgres (for admin status and org data)

---

## Running Your First Analysis

### Step 1: Choose Your Cohort

**Option A: All Active Clients** (127 clients)
- Use: `active_orgs.csv`
- Best for: Overall platform usage analysis

**Option B: Specific Year Cohort** (e.g., 2025 clients)
- Use: `2025_clients.csv` (or create `2026_clients.csv`)
- Best for: TTFV benchmarking with accurate close dates

### Step 2: Open Cursor and Paste This Prompt

**For a specific cohort with monthly averages:**
```
Calculate the TTFV for all clients in @ttfv/2025_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Also provide:
1. A comprehensive analysis report
2. A monthly averages CSV with months as columns and average TTFV days as the data row
```

**For all active clients:**
```
Calculate the TTFV for all active clients using @ttfv/TTFV_Analysis_Prompt.md
```

### Step 3: Review the Output

Cursor will generate:
- **Markdown report** with detailed analysis, insights, and recommendations
- **CSV file** with monthly averages (if requested)

---

## Creating a New Client Cohort CSV

To track TTFV for a new year (e.g., 2026), create a CSV like this:

**File:** `2026_clients.csv`

```csv
Org,OrgName,Domain,CloseDate,,,
abc,ABC Company,abccompany.com,2026-01-15,,,
xyz,XYZ Corp,xyzcorp.com,2026-02-20,,,
```

**Required columns:**
- `Org` - Organization shortname (from SuperCat)
- `OrgName` - Full company name
- `CloseDate` - Deal close date (YYYY-MM-DD format)

**Optional columns:**
- `Domain` - Company website

---

## Common Prompts

### Monthly Review (End of Month)
```
Calculate TTFV for all clients in @ttfv/2026_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Provide a monthly averages CSV and highlight:
1. Clients with TTFV > 60 days
2. Clients without any TTFV events yet
3. Best performers this month
```

### Quarterly Business Review
```
Calculate TTFV for all clients in @ttfv/2026_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Focus the analysis on:
1. Q1 2026 clients (Jan-Mar close dates)
2. Average TTFV by month
3. Clients needing enablement support
```

### Specific Client Investigation
```
Calculate TTFV for [Client Name] using @ttfv/TTFV_Analysis_Prompt.md

Include:
1. First value date and action type
2. All users who have performed value actions
3. Timeline of adoption
```

---

## Understanding Your Results

### Good TTFV (Target: <45 days)
- **26-45 days:** Excellent onboarding
- **Example:** Oly Studio (26 days), Wendover Art Group (27 days)

### Needs Attention (>60 days)
- **60-90 days:** Potential friction, follow up needed
- **90+ days:** Significant adoption challenge, immediate action required

### No TTFV Events
- Client is browsing but not using high-value features
- **Action:** Schedule enablement call, provide training resources

---

## File Management

### Keep These Files
- `README.md` - Main documentation
- `QUICKSTART.md` - This file
- `TTFV_Analysis_Prompt.md` - Core calculation logic
- `TTFV_Report_Format_Template.md` - Report formatting
- `TTFV_Methodology_Overview.md` - Detailed methodology
- `active_orgs.csv` - Master client list
- `[YEAR]_clients.csv` - Annual cohort lists

### Clean Up After Analysis
Generated reports and CSVs can be:
- Moved to a `reports/` subfolder
- Archived after review
- Deleted if no longer needed

---

## Troubleshooting

### "No data found for client"
- Check org shortname spelling in CSV
- Verify client exists in SuperCat Postgres
- Confirm Mixpanel tracking is active

### "Postgres timeout"
- This is expected for large queries
- The analysis will continue with available data
- Admin filtering may be limited

### "All TTFV events are admin-only"
- Sales reps haven't used the platform yet
- Schedule enablement/training session
- Check if users have correct permissions

---

## Need Help?

1. Read `TTFV_Methodology_Overview.md` for detailed explanation
2. Review `TTFV_Analysis_Prompt.md` for calculation steps
3. Check previous reports in the folder for examples

---

## Next Steps

After your first analysis:
1. **Set a monthly reminder** to run TTFV for new clients
2. **Create a 2026 client CSV** and start tracking
3. **Share results** with Customer Success and Onboarding teams
4. **Set TTFV targets** based on your 2025 benchmarks (avg: 72 days, best: 26 days)
