# TTFV Analysis - File Index

Quick reference guide to all files in this folder.

---

## 📚 Documentation Files

### Start Here
| File | Purpose | When to Use |
|------|---------|-------------|
| **README.md** | Main documentation and overview | First time setup, understanding TTFV |
| **QUICKSTART.md** | Step-by-step guide for new users | Running your first analysis |
| **PROMPT_TEMPLATES.md** | Copy-paste prompts for common tasks | Monthly reviews, specific analyses |

### Reference
| File | Purpose | When to Use |
|------|---------|-------------|
| **TTFV_Methodology_Overview.md** | Detailed explanation of TTFV metric | Understanding why/how TTFV works |
| **TTFV_Analysis_Prompt.md** | Core calculation logic (reference in Cursor) | Every analysis - this is the engine |
| **TTFV_Report_Format_Template.md** | Report formatting guidelines | Customizing output format |

---

## 📊 Data Files

### Client Lists
| File | Description | Clients | Last Updated |
|------|-------------|---------|--------------|
| **active_orgs.csv** | All active SuperCat clients | 127 | Feb 15, 2026 |
| **2025_clients.csv** | 2025 new client cohort with close dates | 11 | Feb 17, 2026 |

**Note:** Create new files like `2026_clients.csv` for future cohorts

---

## 📈 Generated Outputs

### Reports
| File | Description | Date |
|------|-------------|------|
| **TTFV_Analysis_Report_Feb_2026.md** | Full active clients analysis | Feb 16, 2026 |

### Data Exports
| File | Description | Date |
|------|-------------|------|
| **2025_clients_monthly_averages.csv** | Monthly TTFV averages for 2025 cohort | Feb 17, 2026 |

**Note:** Generated files can be archived or deleted after review

---

## 🚀 Quick Navigation

### I want to...

**Run my first TTFV analysis**
→ Read `QUICKSTART.md`

**Understand what TTFV means**
→ Read `TTFV_Methodology_Overview.md`

**Run a monthly review**
→ Copy prompt from `PROMPT_TEMPLATES.md` (Template 1)

**Create a new client cohort**
→ Copy `2025_clients.csv` format, update with new clients

**Investigate a specific client**
→ Use `PROMPT_TEMPLATES.md` (Template 3)

**Share results with team**
→ Use generated markdown reports and CSV exports

**Troubleshoot an issue**
→ Check `QUICKSTART.md` Troubleshooting section

---

## 📁 Recommended Folder Structure

```
ttfv/
├── README.md                          # Main documentation
├── QUICKSTART.md                      # New user guide
├── PROMPT_TEMPLATES.md                # Copy-paste prompts
├── INDEX.md                           # This file
├── TTFV_Methodology_Overview.md       # Detailed methodology
├── TTFV_Analysis_Prompt.md            # Core logic (DO NOT EDIT)
├── TTFV_Report_Format_Template.md     # Formatting guide
├── active_orgs.csv                    # Master client list
├── 2025_clients.csv                   # 2025 cohort
├── 2026_clients.csv                   # 2026 cohort (create as needed)
├── reports/                           # Optional: archive folder
│   ├── 2025_clients_monthly_averages.csv
│   └── TTFV_Analysis_Report_*.md
```

---

## 🔄 Monthly Workflow

1. **Update client CSV** - Add new clients with close dates
2. **Run analysis** - Use Template 1 from `PROMPT_TEMPLATES.md`
3. **Review outputs** - Check markdown report and CSV
4. **Take action** - Follow up with clients needing attention
5. **Archive** - Move old reports to `reports/` subfolder (optional)

---

## ⚙️ System Requirements

- **Cursor IDE** with workspace access
- **MCP Connections:**
  - BigQuery (HubSpot and Mixpanel data)
  - Postgres (SuperCat database)
- **Permissions:** Read access to all data sources

---

## 📞 Support

**Questions about methodology?**
→ See `TTFV_Methodology_Overview.md`

**Questions about running analysis?**
→ See `QUICKSTART.md`

**Need a specific analysis?**
→ Check `PROMPT_TEMPLATES.md` or create custom prompt

**Technical issues?**
→ Check Troubleshooting in `QUICKSTART.md`

---

## 🎯 Key Metrics Reference

| Metric | Value | Source |
|--------|-------|--------|
| **2025 Average TTFV** | 72.0 days | 2025 new clients cohort |
| **2025 Best TTFV** | 26 days | Oly Studio |
| **Target TTFV** | <45 days | Based on best performers |
| **Active Clients** | 127 | active_orgs.csv |
| **Clients with TTFV (2025)** | 8/11 (73%) | 2025 cohort analysis |

---

Last updated: February 17, 2026
