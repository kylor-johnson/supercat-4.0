# Sales Week-Ahead Analyst - Quick Start Guide

**Time to first report: 30 seconds**

---

## What You'll Get

A tactical weekly sales intelligence report that tells you:

1. **What discovery calls to prep** (with specific questions to ask)
2. **Which deals are stalled** (and how to unblock them)
3. **Which deals are moving** (and how to accelerate them)
4. **What prospects are actually saying** (pain themes, objections, competitor mentions)
5. **Your top 5 actions for the week** (ranked by impact)

---

## Quick Start

### Step 1: Run the Script

```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
python3 scripts/sales_week_ahead_analyst.py --ae-name "Kylor Johnson"
```

### Step 2: Open Your Report

The script will save your report to:
```
reports/sales_week_ahead_YYYY-MM-DD_your_name.md
```

### Step 3: Review and Act

Open the report and:
- ✅ Prep your discovery calls (Section 2)
- ✅ Identify stalled deals to unblock (Section 3A)
- ✅ Plan acceleration moves for moving deals (Section 3B)
- ✅ Review VoC intelligence (Section 4)
- ✅ Execute your top 5 actions (Section 5)

---

## Using with Cursor

Just ask Cursor:

```
Generate my Sales Week-Ahead report
```

Cursor will:
1. Run the script for you
2. Show you a preview
3. Open the full report

---

## Weekly Routine

### Monday Morning (15 minutes)
1. Generate your week-ahead report
2. Read all 5 sections
3. Block calendar time for top 5 actions
4. Prep discovery calls

### Mid-Week Check (5 minutes)
1. Review progress on top 5 actions
2. Update HubSpot with new activity
3. Log all call notes

### Friday Afternoon (10 minutes)
1. Review what you accomplished
2. Update stalled deals
3. Note learnings for next week

---

## What It Analyzes

### HubSpot Data
- ✅ Your open pipeline deals
- ✅ Deal stages and values
- ✅ Last activity dates
- ✅ Discovery opportunities

### Fathom Data
- ✅ Last 30 days of recorded calls
- ✅ Pain themes mentioned
- ✅ Objections raised
- ✅ Competitor mentions

### Intelligence Generated
- ✅ Stalled vs moving deal segmentation
- ✅ SPICED gap analysis
- ✅ Discovery question recommendations
- ✅ VoC-based talk tracks
- ✅ Prioritized action plan

---

## Command Options

```bash
# Basic usage
python3 scripts/sales_week_ahead_analyst.py --ae-name "Your Name"

# Look ahead 10 days instead of 7
python3 scripts/sales_week_ahead_analyst.py --ae-name "Your Name" --days 10

# Save to custom location
python3 scripts/sales_week_ahead_analyst.py --ae-name "Your Name" --output ~/Desktop/report.md

# Get help
python3 scripts/sales_week_ahead_analyst.py --help
```

---

## Troubleshooting

### "Could not find owner matching 'Your Name'"

Your name in HubSpot doesn't match. Check your exact name:

```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from integrations.hubspot.client import HubSpotClient
client = HubSpotClient()
result = client.get('/crm/v3/owners')
for owner in result.get('results', []):
    print(f'{owner.get(\"firstName\")} {owner.get(\"lastName\")}')
"
```

Then use the exact name shown.

### "No discovery calls scheduled"

Make sure your upcoming calls are:
1. Logged as deals in HubSpot
2. In a discovery stage
3. Assigned to you

### Script won't run

Test the integrations:

```bash
# Test HubSpot
python3 -c "
import sys
sys.path.insert(0, '.')
from integrations.hubspot.client import HubSpotClient
client = HubSpotClient()
client.test_connection()
"

# Test Fathom
python3 integrations/fathom/fathom_api.py
```

---

## Tips for Better Reports

### 1. Keep HubSpot Updated
- Log all deals and activities
- Update deal stages after every call
- Add notes with SPICED elements

### 2. Record All Calls
- More Fathom recordings = better VoC data
- Use descriptive meeting titles
- Include pain/objection keywords

### 3. Use the Report Actively
- Don't just read it - act on it
- Complete your top 5 actions
- Track which VoC themes resonate

### 4. Run It Weekly
- Monday morning is ideal
- Consistency builds better habits
- Week-over-week comparison shows progress

---

## Next Steps

1. **Generate your first report** (takes 30 seconds)
2. **Review all 5 sections** (takes 10 minutes)
3. **Execute your top 5 actions** (takes all week)
4. **Win more deals** (priceless)

---

## Full Documentation

For detailed information, see:
- `documentation/SALES_WEEK_AHEAD_ANALYST.md` - Complete documentation
- `integrations/hubspot/HUBSPOT_INTEGRATION.md` - HubSpot setup
- `integrations/fathom/README.md` - Fathom setup

---

**Ready to win this week? Generate your report now.**

```bash
python3 scripts/sales_week_ahead_analyst.py --ae-name "Kylor Johnson"
```
