# Sales Week-Ahead Analyst

**Purpose:** Prepare AEs to win each week by sharpening discovery, unblocking stalled pipeline, accelerating moving deals, and grounding conversations in real Voice of Customer intelligence.

This is not a dashboard. This is a **tactical plan for THIS WEEK**.

---

## What It Does

The Sales Week-Ahead Analyst generates a comprehensive weekly intelligence report that combines:

1. **HubSpot Pipeline Data** - Your deals, activities, and account information
2. **Fathom VoC Intelligence** - Real buyer language, pain themes, and objections from recent calls
3. **Tactical Recommendations** - Specific actions to take this week

### Report Sections

#### 1. Week at a Glance (5-bullet snapshot)
- Number of discovery calls scheduled
- Pipeline deals to focus on
- Biggest revenue at risk
- Biggest upside if you execute well
- One sentence: "If I do only one thing well this week, it is ___"

#### 2. Discovery Call Prep
For EACH discovery call scheduled in the next 7 days:
- **Account & Fit Snapshot** - Segment, fit score, lookalike customers
- **Historical Context** - Prior interactions, what they've seen/heard
- **Hypothesized SPICED** - Likely situation, pain, impact, critical event, decision
- **Discovery Strategy** - Must-ask questions, urgency questions, qualify-out questions

#### 3. Pipeline Reality
**A) Stalled Deals (no activity in 14+ days)**
- Why it's stalled
- SPICED gap
- Best next action THIS WEEK
- Risk if you do nothing

**B) Moving Deals (recent activity)**
- What's working
- What could accelerate it
- One action to progress stage, increase deal size, or reduce close risk

#### 4. Voice of Customer Intelligence
Based on last 30 days of Fathom calls:
- Top 3 pain themes you should expect to hear
- Top 3 objections to be ready for
- Competitor mentions and "do nothing" alternatives
- Talk track recommendations (what to lean into, what to stop saying)

#### 5. Weekly Game Plan
- **Top 5 Actions** (ranked, with who/what/by when)
- **Deals to CLOSE or DISQUALIFY** this week
- **Personal focus improvement** (e.g., "Slow down discovery and quantify impact before demo")

---

## How to Use

### Basic Usage

```bash
python3 scripts/sales_week_ahead_analyst.py --ae-name "Kylor Johnson"
```

This will:
1. Connect to HubSpot and Fathom
2. Pull your pipeline data and recent calls
3. Generate a tactical weekly report
4. Save it to `reports/sales_week_ahead_YYYY-MM-DD_ae_name.md`

### Advanced Options

```bash
# Look ahead 10 days instead of 7
python3 scripts/sales_week_ahead_analyst.py --ae-name "Kylor Johnson" --days 10

# Specify custom output location
python3 scripts/sales_week_ahead_analyst.py --ae-name "Kylor Johnson" --output ~/Desktop/my_week_ahead.md
```

### Using with Cursor

You can also ask Cursor to generate the report:

```
Generate my Sales Week-Ahead report for Kylor Johnson
```

Cursor will:
1. Run the script
2. Show you a preview
3. Open the full report for you

---

## Setup Requirements

### Prerequisites

1. **HubSpot Integration** - Already configured (see `integrations/hubspot/`)
2. **Fathom Integration** - Already configured (see `integrations/fathom/`)
3. **Python 3.8+** - Required

### First-Time Setup

The script uses existing integrations, so no additional setup is needed. Just run it!

If you encounter issues:

```bash
# Test HubSpot connection
python3 -c "
import sys
sys.path.insert(0, '.')
from integrations.hubspot.client import HubSpotClient
client = HubSpotClient()
client.test_connection()
"

# Test Fathom connection
python3 integrations/fathom/fathom_api.py
```

---

## Data Sources

### HubSpot Data Pulled

- **Owners** - To find your owner ID
- **Deals** - All open pipeline deals assigned to you
- **Deal Properties:**
  - `dealname` - Deal name
  - `dealstage` - Current stage
  - `amount` - Deal value
  - `closedate` - Expected close date
  - `hubspot_owner_id` - Owner assignment
  - `createdate` - When deal was created
  - `hs_lastmodifieddate` - Last activity date
  - `notes_last_updated` - Last note added
  - `num_associated_contacts` - Number of contacts

### Fathom Data Pulled

- **Meetings** - Last 30 days of recorded calls
- **Meeting Properties:**
  - `meeting_title` - Call title
  - `recording_id` - Fathom recording ID
  - `recording_start_time` - When the call happened
  - `recorded_by` - Who recorded it
  - `share_url` - Link to recording

### Voice of Customer Extraction

The script analyzes meeting titles and summaries to extract:

**Pain Keywords:**
- problem, issue, challenge, struggle, difficult
- frustrated, manual, time-consuming, inefficient

**Objection Keywords:**
- expensive, cost, price, budget, timing
- not sure, concerned, worried, risk

**Competitor Names:**
- coaster, amp, salesforce, hubspot, pipedrive

---

## Report Output Format

Reports are saved as Markdown files in the `reports/` directory with this naming convention:

```
sales_week_ahead_YYYY-MM-DD_ae_name.md
```

Example: `sales_week_ahead_2026-02-03_kylor_johnson.md`

### Report Structure

```markdown
# Sales Week-Ahead Report
**AE:** Kylor Johnson
**Week:** February 3, 2026 - February 10, 2026
**Generated:** 2026-02-03 14:30

---

## 1. WEEK AT A GLANCE
- Discovery calls scheduled: 3
- Pipeline deals to focus on: 5 moving, 2 stalled
- Biggest revenue at risk: $50,000 (Acme Corp)
- Total pipeline value: $250,000
- One thing to do well: Unblock the 2 stalled deals and get them moving

---

## 2. DISCOVERY CALL PREP
[Detailed prep for each call...]

---

## 3. PIPELINE REALITY
[Stalled and moving deals analysis...]

---

## 4. VOICE OF CUSTOMER INTELLIGENCE
[Pain themes, objections, competitor intel...]

---

## 5. MY WEEKLY GAME PLAN
[Top 5 actions, deals to close/disqualify, personal focus...]
```

---

## Customization

### Adjusting Stalled Deal Threshold

By default, deals with no activity in 14+ days are considered "stalled". To change this:

Edit `scripts/sales_week_ahead_analyst.py`:

```python
# Line ~275
cutoff_date = self.today - timedelta(days=14)  # Change 14 to your preferred days
```

### Adding More VoC Keywords

To track additional pain themes, objections, or competitors:

Edit `scripts/sales_week_ahead_analyst.py`:

```python
# Line ~236 - Add pain keywords
pain_keywords = [
    'problem', 'issue', 'challenge', 'struggle', 'difficult',
    'frustrated', 'manual', 'time-consuming', 'inefficient',
    'your-new-keyword-here'  # Add here
]

# Line ~242 - Add objection keywords
objection_keywords = [
    'expensive', 'cost', 'price', 'budget', 'timing',
    'not sure', 'concerned', 'worried', 'risk',
    'your-new-keyword-here'  # Add here
]

# Line ~249 - Add competitors
competitors = [
    'coaster', 'amp', 'salesforce', 'hubspot', 'pipedrive',
    'your-competitor-here'  # Add here
]
```

### Changing Report Sections

The report structure is modular. Each section is generated by a separate method:

- `_build_report()` - Main report builder
- `_format_discovery_brief()` - Discovery call prep
- `_format_stalled_deal()` - Stalled deal analysis
- `_format_moving_deal()` - Moving deal analysis
- `_format_voc_intelligence()` - VoC intelligence
- `_build_game_plan()` - Weekly game plan

Edit these methods to customize the output.

---

## Troubleshooting

### "Could not find owner matching 'Your Name'"

**Cause:** Your name in HubSpot doesn't match the `--ae-name` parameter.

**Solution:** Check your exact name in HubSpot:

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

**Cause:** No deals in discovery stages in HubSpot.

**Solution:** Ensure your upcoming discovery calls are:
1. Logged as deals in HubSpot
2. In a discovery-related stage (e.g., "Appointment Scheduled", "Qualified to Buy")
3. Assigned to you as the owner

### "Error pulling Fathom data"

**Cause:** Fathom API connection issue.

**Solution:** Test the Fathom connection:

```bash
python3 integrations/fathom/fathom_api.py
```

If it fails, check that the API key is still valid in `integrations/fathom/fathom_api.py`.

### "No VoC themes extracted"

**Cause:** Meeting titles don't contain tracked keywords.

**Solution:** This is normal if your recent calls don't mention specific pain/objection keywords in the title. The VoC extraction is basic and can be enhanced by pulling full transcripts (see Enhancements below).

---

## Enhancements

### Future Improvements

1. **Full Transcript Analysis**
   - Currently only analyzes meeting titles
   - Could pull full transcripts and use NLP to extract themes
   - Would require more API calls and processing time

2. **SPICED Scoring**
   - Auto-score deals based on SPICED completeness
   - Flag deals missing key SPICED elements

3. **Lookalike Account Matching**
   - Match discovery accounts to existing customers
   - Suggest relevant case studies and references

4. **Automated Email Drafts**
   - Generate re-engagement emails for stalled deals
   - Create follow-up emails based on VoC themes

5. **Calendar Integration**
   - Pull actual calendar events for discovery calls
   - Show exact meeting times and attendees

6. **Team Intelligence**
   - Aggregate VoC across the entire team
   - Show what's working for top performers

### Contributing

To add enhancements:

1. Fork the script
2. Add your feature
3. Test thoroughly
4. Document your changes
5. Share with the team

---

## Best Practices

### Weekly Routine

**Monday Morning:**
1. Generate your week-ahead report
2. Review all sections
3. Block time for top 5 actions
4. Prep discovery calls

**Mid-Week Check:**
1. Review progress on top 5 actions
2. Update deal stages in HubSpot
3. Log all call notes

**Friday Afternoon:**
1. Review what you accomplished
2. Update any stalled deals
3. Prep for next week

### Using the Report Effectively

**DO:**
- ✅ Review the entire report before your week starts
- ✅ Use discovery briefs to prepare specific questions
- ✅ Take action on stalled deals within 48 hours
- ✅ Update HubSpot after every interaction
- ✅ Track which VoC themes resonate with prospects

**DON'T:**
- ❌ Treat this as a static dashboard
- ❌ Ignore stalled deals
- ❌ Skip discovery prep
- ❌ Forget to update HubSpot
- ❌ Use generic talk tracks instead of VoC language

### Maximizing VoC Intelligence

1. **Record all calls** - More Fathom recordings = better VoC data
2. **Use descriptive titles** - Help the extraction pick up themes
3. **Add SPICED notes** - Include pain, impact, critical event in notes
4. **Tag competitors** - Mention competitors in call notes
5. **Share learnings** - Discuss VoC themes with the team

---

## FAQ

**Q: How often should I run this?**
A: Once per week, typically Monday morning.

**Q: Can I run this for my entire team?**
A: Yes, but you'll need to run it separately for each AE:
```bash
for ae in "Kylor Johnson" "Jane Smith" "John Doe"; do
    python3 scripts/sales_week_ahead_analyst.py --ae-name "$ae"
done
```

**Q: Does this update HubSpot?**
A: No, this is read-only. It pulls data but doesn't modify anything.

**Q: Can I customize the report format?**
A: Yes, edit the `_build_report()` method in the script.

**Q: What if I don't have any Fathom calls?**
A: The report will still generate with HubSpot data only. VoC section will show "No data available".

**Q: Can I export this to PDF?**
A: Yes, use a Markdown-to-PDF converter:
```bash
# Using pandoc (if installed)
pandoc reports/sales_week_ahead_2026-02-03_kylor_johnson.md -o report.pdf
```

**Q: How long does it take to run?**
A: Typically 10-30 seconds depending on:
- Number of deals in your pipeline
- Number of recent Fathom calls
- HubSpot API response time

**Q: Can I schedule this to run automatically?**
A: Yes, using cron (macOS/Linux):
```bash
# Run every Monday at 8am
0 8 * * 1 cd /path/to/supercat && python3 scripts/sales_week_ahead_analyst.py --ae-name "Your Name"
```

---

## Support

For issues or questions:

1. Check the Troubleshooting section above
2. Review the integration docs:
   - `integrations/hubspot/HUBSPOT_INTEGRATION.md`
   - `integrations/fathom/README.md`
3. Test individual integrations separately
4. Ask Cursor for help debugging

---

## Version History

**v1.0** (2026-02-03)
- Initial release
- HubSpot pipeline integration
- Fathom VoC intelligence
- 5-section report format
- Discovery call prep
- Stalled vs moving deal segmentation
- Weekly game plan generation

---

*Built for AEs who want to win by being prepared, not just busy.*
