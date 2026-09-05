# Health Intelligence v3 — All Clients Report
## March 31, 2026

This directory contains complete Health Intelligence v3 scores for all 218 SuperCat clients.

---

## Quick Summary

**Total Clients Scored:** 218  
**Analysis Period:** Last 90 days (rolling)  
**Generated:** March 31, 2026

### Health Distribution

- **Excellent (0.80+):** 0 clients (0.0%)
- **Good (0.60-0.79):** 23 clients (10.6%)
- **Fair (0.40-0.59):** 108 clients (49.5%)
- **At Risk (0.30-0.39):** 10 clients (4.6%)
- **Critical (<0.30):** 77 clients (35.3%)

### Key Metrics

- **Mean Score:** 0.439
- **Median Score:** 0.476
- **Score Range:** 0.236 - 0.659

### Portfolio Flags

- 🚨 **Churn Risk:** 77 clients (1 immediate severity)
- 💰 **Expansion Ready:** 29 clients
- ✨ **Healthy Complete:** 0 clients

### ARR Analysis

- **Total ARR (tracked):** $1,508,639.54 across 99 clients
- **ARR at Risk:** $16,620.00 (2 clients)
- **Expansion Pipeline ARR:** $411,498.54 (23 clients)

---

## Files in This Directory

### 1. Main CSV: `client_health_scores_2026-03-31.csv`

**Contains:** All 218 clients with scores, bands, flags, and layer breakdowns

**Columns:**
- `org_shortname` — Client identifier
- `org_name` — Client full name
- `segment` — Client segment (Platform-Embedded, Commerce-Active, Catalog-Focused)
- `arr` — Annual Recurring Revenue
- `composite_score_final` — Final health score (0-1 scale)
- `health_band` — Health category (Excellent/Good/Fair/At Risk/Critical)
- `churn_risk` — Boolean churn risk flag
- `churn_severity` — Severity level (immediate or blank)
- `expansion_ready` — Boolean expansion opportunity flag
- `healthy_complete` — Boolean healthy & complete flag
- `layer_1_engagement` — Engagement Health score (0-100)
- `layer_2_value_realization` — Value Realization score (0-100)
- `layer_3_trend_momentum` — Trend Momentum score (0-100)
- `layer_4_risk_signals` — Risk Signals score (-100 to 0)

**Sorting:** Sorted by `composite_score_final` descending (best to worst)

**Use Cases:**
- Filter by health band for targeted outreach
- Sort by ARR to prioritize high-value clients
- Filter by flags (churn_risk, expansion_ready) for action lists
- Analyze layer scores to identify systemic issues

### 2. Summary Report: `SUMMARY_REPORT.md`

**Contains:**
- Scoring methodology overview
- Complete health band distribution
- All 77 churn risk clients listed
- Top 20 expansion-ready clients
- Top/bottom 10 clients by score

**Best For:** Quick reference and executive briefings

### 3. Executive Summary: `EXECUTIVE_SUMMARY.md`

**Contains:**
- Strategic analysis and insights
- Portfolio health assessment
- Data quality observations
- Actionable recommendations (immediate, medium-term, long-term)
- Segment performance analysis
- ARR risk/opportunity analysis

**Best For:** Leadership presentations and strategic planning

### 4. Scoring Methodology: `SCORING_METHODOLOGY.md`

**Contains:**
- Complete scoring formula documentation
- Component-by-component breakdown
- Worked examples with real clients
- Benchmark data sources
- Scoring philosophy and design principles
- Common scoring scenarios
- Technical implementation details

**Best For:** Understanding how scores are calculated, training, and methodology questions

### 5. Client Breakdowns: `client_breakdowns/` (218 files)

**Contains:** Individual markdown file for each client with:
- Composite score and health band
- All 4 layer scores
- All 22 component scores with details
- Three flags (churn_risk, expansion_ready, healthy_complete)
- Raw metrics used in calculations

**File Naming:** `{org_shortname}_health_breakdown.md`

**Best For:** Deep-dive analysis of individual clients, QBR prep, intervention planning

---

## How to Use This Data

### For Account Managers

1. **Identify Your Clients:** Filter CSV by your territory/portfolio
2. **Prioritize Actions:**
   - Critical/At Risk: Review breakdown, schedule intervention
   - Fair: Monitor and optimize
   - Good: Maintain and explore expansion
3. **Prepare for QBRs:** Use individual breakdowns for talking points

### For Executive Leadership

1. **Read:** `EXECUTIVE_SUMMARY.md` for strategic overview
2. **Review:** Portfolio health distribution and trends
3. **Focus On:**
   - Churn risk exposure ($16,620 ARR at immediate risk)
   - Expansion pipeline ($411,498 ARR opportunity)
   - Systemic issues (35% in Critical band)

### For Product Team

1. **Analyze:** Layer 1 (Engagement) scores to identify friction points
2. **Review:** Feature adoption patterns across segments
3. **Investigate:** Why no clients reach Excellent band
4. **Plan:** Features/improvements to boost engagement

### For Customer Success

1. **Churn Prevention:**
   - Filter CSV for `churn_risk = True`
   - Sort by ARR (prioritize high-value)
   - Review individual breakdowns for root causes
   - Execute intervention playbooks

2. **Expansion Pipeline:**
   - Filter CSV for `expansion_ready = True`
   - Sort by score (highest = best candidates)
   - Identify specific upsell opportunities
   - Schedule expansion conversations

---

## Key Insights from This Analysis

### 1. No Excellent Performers

**Finding:** Zero clients scored 0.80 or higher

**Root Causes:**
- Layer 3 (Trend Momentum) uses neutral scores (51/100) due to missing historical data
- Even top performers have room for improvement in value realization
- Portfolio-wide opportunity for optimization

**Implication:** Once historical data is available, top performers (Gabby, Summer Classics, etc.) may reach Excellent band.

### 2. Large Critical Cohort (35%)

**Finding:** 77 clients (35.3%) in Critical band

**Root Causes:**
- 48+ clients missing segment classification → default to 0.281 score
- Several template/test accounts in production
- Some paying customers with zero engagement

**Action Required:**
- Complete segment classification (will reclassify many)
- Clean up template/test accounts
- Intervene with paying-but-disengaged clients

### 3. Strong Expansion Pipeline

**Finding:** 29 clients (13.3%) flagged as expansion-ready

**Opportunity:**
- $411,498 ARR in expansion pipeline
- Top candidates have 0.60+ health scores
- High engagement + high order volumes = upsell readiness

**Recommended Actions:**
- Focus on top 10 (Gabby, Summer Classics, Gabriella White, etc.)
- Identify specific expansion paths (CPQ, features, services)
- Schedule QBRs to present opportunities

### 4. Engagement vs Value Realization Gap

**Finding:**
- Average Layer 1 (Engagement): 41.9/100
- Average Layer 2 (Value Realization): 58.4/100

**Interpretation:**
- Clients are deriving value (orders, customers) even with moderate engagement
- Opportunity to boost engagement to unlock more value
- Engagement improvements could lift scores significantly

### 5. Segment Distribution Surprise

**Finding:**
- Catalog-Focused: 81 clients (37%)
- Platform-Embedded: 41 clients (19%)
- Commerce-Active: 33 clients (15%)
- Unknown: 63 clients (29%)

**Note:** This differs from expected distribution. Many clients may be misclassified or missing segments.

---

## Action Plan Summary

### Immediate (This Week)

1. ✅ **Complete:** Health scores calculated for all 218 clients
2. ⏳ **Next:** Fix segment classification for 63 unknown clients
3. ⏳ **Next:** Contact immediate churn risk client (sic)
4. ⏳ **Next:** Review template/test accounts for cleanup

### Week 2-4

1. Re-run scoring after segment fixes
2. Create intervention plans for top 10 churn risk clients
3. Schedule QBRs with top 5 expansion-ready clients
4. Develop playbooks for each health band

### Month 2-3

1. Implement historical data collection for Layer 3
2. Integrate support ticket data for Layer 4
3. Add MCP data for Layer 2 components
4. Establish monthly scoring cadence

---

## Questions?

For questions about:
- **Scoring methodology:** See `SCORING_METHODOLOGY.md`
- **Strategic recommendations:** See `EXECUTIVE_SUMMARY.md`
- **Individual clients:** See `client_breakdowns/{org}_health_breakdown.md`
- **Raw data:** See `client_health_scores_2026-03-31.csv`

---

## Technical Details

**Script Used:** `scripts/health_score_batch_calculator_v3.py`  
**Data Source:** BigQuery `insightful_product.org_summary` table  
**Benchmarks:** BigQuery `insightful_product.segment_benchmarks_monthly` table  
**Runtime:** ~20 minutes for 218 clients  
**Batch Size:** 5 clients per batch  

**BigQuery Credentials:** `integrations/bigquery/service-account/supercat-data-pipeline-ac0671b8d44a.json`

**To Reproduce:**

```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
export GOOGLE_APPLICATION_CREDENTIALS="integrations/bigquery/service-account/supercat-data-pipeline-ac0671b8d44a.json"
source "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/Insightful Product/health-scoring/scripts/venv/bin/activate"
python scripts/health_score_batch_calculator_v3.py --batch-size 5 --output-dir reports/health_scores_YYYY-MM-DD
```

---

**Generated:** March 31, 2026  
**Version:** Health Intelligence v3  
**Status:** Complete
