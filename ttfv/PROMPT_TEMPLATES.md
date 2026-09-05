# TTFV Analysis - Prompt Templates

Copy and paste these prompts directly into Cursor for quick analysis.

---

## Template 1: Monthly TTFV Report with CSV Export

**Use Case:** Monthly review of a specific client cohort with exportable data

```
Calculate the TTFV for all clients in @ttfv/2025_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Provide:
1. A comprehensive markdown report with monthly breakdown
2. A CSV file with months as columns and average TTFV days as the data row
3. Highlight any clients with TTFV > 60 days or no TTFV events
```

**Outputs:**
- Detailed markdown report
- `[cohort]_monthly_averages.csv`

---

## Template 2: All Active Clients Analysis

**Use Case:** Quarterly or annual review of all active clients

```
Calculate the TTFV for all active clients using @ttfv/TTFV_Analysis_Prompt.md

Include:
1. Summary statistics
2. Clients with valid TTFV vs clients without
3. Top 10 best performers
4. Clients needing immediate attention (no TTFV events)
```

**Outputs:**
- Comprehensive markdown report
- Insights and recommendations

---

## Template 3: Specific Client Deep Dive

**Use Case:** Investigating adoption for a specific client

```
Calculate the TTFV for [Client Name] using @ttfv/TTFV_Analysis_Prompt.md

Provide detailed information:
1. Close date or org creation date
2. First value action date and type
3. TTFV in days
4. Username who performed first value action
5. All subsequent value actions in the first 30 days
```

**Outputs:**
- Detailed client-specific report

---

## Template 4: Quarterly Cohort Comparison

**Use Case:** Compare TTFV across different time periods

```
Calculate the TTFV for clients in @ttfv/2025_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Group results by quarter:
- Q1 2025 (Jan-Mar close dates)
- Q2 2025 (Apr-Jun close dates)
- Q3 2025 (Jul-Sep close dates)
- Q4 2025 (Oct-Dec close dates)

For each quarter, show:
1. Average TTFV
2. Number of clients
3. Best and worst performers
4. Clients without TTFV events
```

**Outputs:**
- Quarterly comparison report
- Trend analysis

---

## Template 5: New Client CSV Setup

**Use Case:** Creating a new annual cohort file

```
I need to create a new client cohort CSV for 2026.

1. Create a file called @ttfv/2026_clients.csv
2. Use the same format as @ttfv/2025_clients.csv
3. Include these clients: [list client names or provide data]

Format:
- Org: shortname from SuperCat
- OrgName: full company name
- Domain: company website
- CloseDate: YYYY-MM-DD format
```

**Outputs:**
- New `2026_clients.csv` file ready for analysis

---

## Template 6: Enablement Priority List

**Use Case:** Identify clients needing immediate support

```
Calculate the TTFV for all clients in @ttfv/2025_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Create a priority list for enablement:

HIGH PRIORITY (immediate action):
- Clients with no TTFV events and >90 days since close
- Clients with TTFV >120 days

MEDIUM PRIORITY (follow up needed):
- Clients with no TTFV events and 60-90 days since close
- Clients with TTFV 90-120 days

For each client, include:
- Days since close
- Current status (browsing only, admin only, or no activity)
- Recommended action
```

**Outputs:**
- Prioritized enablement list
- Action recommendations

---

## Template 7: Update Existing Report

**Use Case:** Refresh an existing analysis with new data

```
Re-run the TTFV analysis for @ttfv/2025_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Compare to the previous report from [date]:
1. Which clients achieved first value since last report?
2. How has the average TTFV changed?
3. Are there any new clients without TTFV events?

Update the monthly averages CSV file.
```

**Outputs:**
- Updated report with changes highlighted
- Refreshed CSV

---

## Customization Tips

### Add Filters
```
Calculate TTFV for clients in @ttfv/2025_clients.csv that closed after June 1, 2025
```

### Specify Output Format
```
Provide results in a simple table format suitable for pasting into Slack
```

### Request Specific Insights
```
Focus on identifying patterns in clients with fast TTFV (<30 days) vs slow TTFV (>90 days)
```

### Export for Presentations
```
Create an executive summary suitable for a QBR presentation
```

---

## Variables to Replace

When using these templates, replace:
- `[Client Name]` - Specific client company name
- `[cohort]` - Year or group identifier (e.g., "2025", "Q1_2026")
- `[date]` - Previous report date for comparisons
- `[list client names or provide data]` - Actual client information

---

## Pro Tips

1. **Be specific about outputs** - Request CSV, markdown, or both
2. **Set context** - Mention if this is for a QBR, monthly review, or investigation
3. **Request comparisons** - Ask for trends over time or cohort comparisons
4. **Specify thresholds** - Define what "good" vs "needs attention" means for your use case
5. **Ask for actions** - Request recommendations, not just data

---

## Example: Full Monthly Workflow

**Step 1: Update client CSV** (if new clients closed)
```
Add these new clients to @ttfv/2026_clients.csv:
- Company ABC (org: abc, closed: 2026-01-15)
- Company XYZ (org: xyz, closed: 2026-01-28)
```

**Step 2: Run analysis**
```
Calculate TTFV for all clients in @ttfv/2026_clients.csv using @ttfv/TTFV_Analysis_Prompt.md

Provide monthly averages CSV and highlight any changes from last month.
```

**Step 3: Share results**
- Export CSV to Google Sheets
- Share markdown report with Customer Success team
- Create action items for clients needing attention
