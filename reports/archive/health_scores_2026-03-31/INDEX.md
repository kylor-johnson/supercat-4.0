# Health Intelligence v3 — Complete Report Index
## All 218 SuperCat Clients — March 31, 2026

---

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| **Total Clients Scored** | 218 |
| **Mean Health Score** | 0.439 |
| **Median Health Score** | 0.476 |
| **Total ARR (tracked)** | $1,508,639.54 |
| **Clients with ARR Data** | 99 (45%) |

---

## 🎯 Health Band Distribution

```
Excellent (0.80+)    ▏ 0 clients (0.0%)
Good (0.60-0.79)     ████████████ 23 clients (10.6%)
Fair (0.40-0.59)     ████████████████████████████████████████████████ 108 clients (49.5%)
At Risk (0.30-0.39)  ████ 10 clients (4.6%)
Critical (<0.30)     ████████████████████████████████████ 77 clients (35.3%)
```

---

## 🚨 Risk & Opportunity Flags

| Flag | Count | % of Portfolio | ARR Impact |
|------|-------|----------------|------------|
| **Churn Risk** | 77 | 35.3% | $16,620 at risk |
| **Expansion Ready** | 29 | 13.3% | $411,498 opportunity |
| **Healthy Complete** | 0 | 0.0% | N/A |

---

## 📁 Files in This Report

### Start Here

1. **README.md** — Overview and quick start guide
2. **ACTION_ITEMS.md** — Prioritized action list with specific next steps

### Strategic Analysis

3. **EXECUTIVE_SUMMARY.md** — Strategic insights, recommendations, portfolio analysis
4. **SUMMARY_REPORT.md** — Complete summary with all clients listed by category

### Technical Documentation

5. **SCORING_METHODOLOGY.md** — Complete scoring formula, components, examples
6. **client_health_scores_2026-03-31.csv** — Main data file (218 rows)
7. **client_breakdowns/** — 218 individual client breakdown files

---

## 🎯 Recommended Reading Path

### For Executives
1. Start with **EXECUTIVE_SUMMARY.md**
2. Review **ACTION_ITEMS.md** for priorities
3. Reference **SUMMARY_REPORT.md** for complete lists

### For Account Managers
1. Start with **README.md** for context
2. Open **client_health_scores_2026-03-31.csv** in Excel
3. Filter for your clients
4. Review individual breakdowns in **client_breakdowns/** folder

### For Product/CS Teams
1. Read **SCORING_METHODOLOGY.md** to understand calculations
2. Analyze **client_health_scores_2026-03-31.csv** for patterns
3. Review **EXECUTIVE_SUMMARY.md** for systemic insights
4. Use **ACTION_ITEMS.md** to prioritize initiatives

---

## 🔍 How to Find Specific Information

### "Which clients are at churn risk?"
→ Open `client_health_scores_2026-03-31.csv`, filter `churn_risk = True`

### "Who should I contact first?"
→ See **ACTION_ITEMS.md**, Section 1 (Immediate Actions)

### "Which clients are ready for upsell?"
→ Open `client_health_scores_2026-03-31.csv`, filter `expansion_ready = True`, sort by ARR

### "How is [specific client] doing?"
→ Open `client_breakdowns/{org}_health_breakdown.md`

### "How are scores calculated?"
→ Read **SCORING_METHODOLOGY.md**

### "What should we do strategically?"
→ Read **EXECUTIVE_SUMMARY.md**, Section: Strategic Recommendations

### "What's the overall portfolio health?"
→ See **SUMMARY_REPORT.md**, Section: Distribution by Health Band

---

## 📈 Key Insights

### 1. No Excellent Performers
- Zero clients scored 0.80 or higher
- Top score: 0.659 (Gabby)
- Opportunity for portfolio-wide optimization

### 2. Large Critical Cohort
- 77 clients (35%) in Critical band
- Many due to missing segment data
- Segment classification will reclassify many

### 3. Strong Expansion Pipeline
- 29 clients ready for expansion
- $411K ARR in pipeline
- Top candidates have 0.60+ scores

### 4. Engagement Gap
- Average engagement: 41.9/100
- Average value realization: 58.4/100
- Clients deriving value despite moderate engagement

### 5. Data Quality Issues
- 63 clients missing segments
- Template/test accounts in production
- Historical and MCP data unavailable

---

## 🎬 Next Steps

### This Week
1. ✅ Health scores calculated (COMPLETE)
2. ⏳ Fix segment classification
3. ⏳ Contact immediate churn risk clients
4. ⏳ Review template accounts

### Next 30 Days
1. ⏳ Re-run scoring after data fixes
2. ⏳ Schedule 5 expansion QBRs
3. ⏳ Create intervention playbooks
4. ⏳ Launch engagement pilot

### Next 90 Days
1. ⏳ Implement historical data collection
2. ⏳ Integrate MCP data sources
3. ⏳ Establish monthly scoring cadence
4. ⏳ Achieve 5+ Excellent-band clients

---

## 📞 Questions or Issues?

**Scoring Questions:** See `SCORING_METHODOLOGY.md`  
**Strategic Questions:** See `EXECUTIVE_SUMMARY.md`  
**Technical Issues:** Contact Insightful Product team  
**Data Quality:** Review `ACTION_ITEMS.md` Section 3

---

## 🔄 Reproducibility

To regenerate this report:

```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
export GOOGLE_APPLICATION_CREDENTIALS="integrations/bigquery/service-account/supercat-data-pipeline-ac0671b8d44a.json"
source "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/Insightful Product/health-scoring/scripts/venv/bin/activate"
python scripts/health_score_batch_calculator_v3.py --batch-size 5 --output-dir reports/health_scores_YYYY-MM-DD
```

**Runtime:** ~20 minutes for 218 clients  
**Requirements:** BigQuery credentials, Python 3.8+, pandas, google-cloud-bigquery

---

**Report Generated:** March 31, 2026 21:55:33  
**Script Version:** health_score_batch_calculator_v3.py  
**Data Source:** BigQuery `insightful_product.org_summary` (updated April 1, 2026 03:27 UTC)  
**Benchmarks:** `segment_benchmarks_monthly` (March 2026)
