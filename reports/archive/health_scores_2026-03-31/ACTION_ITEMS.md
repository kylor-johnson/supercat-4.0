# Health Intelligence v3 — Action Items
## Immediate Priorities from March 31, 2026 Analysis

---

## 🚨 IMMEDIATE ACTIONS (Next 48 Hours)

### 1. Critical Churn Risk — Immediate Severity

**Client:** Butler FurnishWEB Test (sic)
- **Score:** 0.236 (Critical)
- **ARR:** $6,960
- **Issue:** Paying customer with ZERO engagement
- **Action:** 
  - Contact immediately
  - Understand why no logins despite active subscription
  - Determine if this is a test account that should be deactivated
  - If legitimate, schedule onboarding/training

### 2. High-Value Churn Risk

**Client:** Jonathan Charles at The Gallery (jcsa)
- **Score:** 0.271 (Critical)
- **ARR:** $9,660
- **Issue:** Minimal engagement (5/100), very low logins
- **Action:**
  - Reach out within 48 hours
  - Identify barriers to adoption
  - Offer training or support
  - Consider intervention playbook

**Total ARR at Immediate Risk:** $16,620

---

## ⚠️ HIGH PRIORITY (Next 2 Weeks)

### 3. Data Quality — Missing Segments

**Issue:** 63 clients have missing or null segment classification

**Impact:**
- Cannot apply proper benchmarks
- Many defaulting to Critical scores (0.281)
- False churn risk flags

**Clients Affected (sample):**
- ahc (Coe Limited)
- al (Abbyson Living)
- art (ART Furniture, Inc.)
- bde (Bad Dog Editions)
- bi (Winslow Home Furniture)
- ... and 58 more

**Action:**
1. Review org_summary table segment field
2. Classify all clients with `segment = None`
3. Re-run scoring after classification
4. Expected outcome: Many will move from Critical to Fair/Good

### 4. Template/Test Account Cleanup

**Issue:** Multiple template and test accounts in production

**Accounts to Review:**
- tmpl (Template_Lighting Company)
- tmpo (Template_not lighting)
- temp (For Jimmy, to Delete)
- tech (Tech Lighting Demo)
- tle (Tech Lighting Demo)
- tll (Lighting Lab)
- vc (Lighting Demo)

**Action:**
1. Verify if these should exist in production
2. Archive or delete test accounts
3. Remove from future scoring runs
4. Document which are legitimate demo environments

---

## 💰 EXPANSION OPPORTUNITIES (Next 30 Days)

### 5. Top 10 Expansion-Ready Clients

Schedule QBRs and present expansion opportunities:

| Priority | Client | Org | Score | ARR | Opportunity |
|----------|--------|-----|-------|-----|-------------|
| 1 | Gabby | gh | 0.659 | N/A | CPQ, advanced features (13K orders) |
| 2 | Summer Classics | scw | 0.650 | N/A | CPQ, advanced features (11K+ orders) |
| 3 | Gabriella White | sc | 0.642 | $30,904 | Additional features, services |
| 4 | RENWIL | rw | 0.625 | $28,249 | CPQ, advanced features |
| 5 | Hubbardton Forge | hfg | 0.610 | $35,540 | Highest ARR, strong engagement |
| 6 | Braxton Culler | bcf | 0.595 | $26,620 | Platform optimization |
| 7 | Somerset Bay | sbmh | 0.593 | N/A | CPQ opportunity |
| 8 | Palecek | pf | 0.588 | $39,660 | Highest ARR in pipeline |
| 9 | Uniware | uhc | 0.584 | $8,740 | Feature expansion |
| 10 | Interlude Furniture | ihw | 0.578 | $4,915 | Feature expansion |

**Total Opportunity:** $174,078 ARR (tracked) + additional untracked

**Recommended Upsells:**
- **CPQ/Configuration:** For clients with 100+ configured items
- **Advanced Features:** Portal enhancements, library, kits
- **Services:** Training, optimization, custom integrations

---

## 📊 PORTFOLIO OPTIMIZATION (Next 60 Days)

### 6. Engagement Improvement Initiative

**Finding:** Average engagement score is only 41.9/100

**Opportunity:** Boost engagement across Fair-band clients (108 total)

**Target Cohort:** Clients scoring 0.40-0.59 with low engagement (<50)

**Actions:**
1. Identify common engagement barriers
2. Create engagement playbook
3. Pilot with 10 clients
4. Measure impact on scores

**Expected Impact:** Move 20-30 clients from Fair to Good band

### 7. Feature Adoption Campaign

**Finding:** Many clients use only 1-3 features

**Opportunity:** Increase feature adoption to boost scores

**Target Features:**
- Sales Portal (for Catalog-Focused clients)
- CPQ/Configuration (for high-order clients)
- Library (for all segments)
- PDF Catalog Export (for all segments)

**Actions:**
1. Segment clients by current feature usage
2. Identify next-best feature for each segment
3. Create feature adoption campaigns
4. Track adoption impact on health scores

---

## 🔧 INFRASTRUCTURE IMPROVEMENTS (Next 90 Days)

### 8. Historical Data Collection

**Issue:** Layer 3 (Trend Momentum) uses neutral scores for all clients

**Impact:** Cannot detect growth/decline patterns

**Action:**
1. Implement monthly snapshots of org_summary
2. Store 12 months of historical data
3. Calculate month-over-month trends
4. Update scoring logic to use real trends

**Expected Impact:**
- Top performers may reach Excellent band (0.80+)
- Declining clients will be identified earlier
- More differentiated scores

### 9. MCP Data Integration

**Issue:** Layer 2 components 10-14 and Layer 4 components 20-22 use neutral/no-penalty scores

**Action:**
1. Integrate support ticket data (HelpScout)
2. Add product/inventory health metrics
3. Track customer concentration
4. Monitor data integrity issues

**Expected Impact:**
- More accurate value realization scores
- Better risk signal detection
- Earlier churn prediction

---

## 📈 SUCCESS METRICS

### 30-Day Goals

- ✅ Complete health scoring for all clients (DONE)
- ⏳ Fix segment classification for 63 clients
- ⏳ Contact 2 immediate churn risk clients
- ⏳ Schedule 5 expansion QBRs
- ⏳ Clean up template/test accounts

### 60-Day Goals

- ⏳ Reduce Critical band from 35% to <25%
- ⏳ Move 20+ clients from Fair to Good
- ⏳ Launch engagement improvement pilot
- ⏳ Close 3 expansion deals

### 90-Day Goals

- ⏳ Implement historical data collection
- ⏳ Integrate MCP data sources
- ⏳ Achieve 5+ clients in Excellent band
- ⏳ Reduce churn risk count by 50%

---

## 📋 QUICK REFERENCE: Who Needs What

### Immediate Intervention (Critical + Paying)

1. **sic** (Butler FurnishWEB Test): $6,960 ARR, 0.236 score
2. **jcsa** (Jonathan Charles at The Gallery): $9,660 ARR, 0.271 score

### High-Priority Outreach (At Risk + ARR > $10K)

- None currently (most At Risk clients have no ARR data)

### Expansion Conversations (Top 5 by ARR)

1. **pf** (Palecek): $39,660 ARR, 0.588 score
2. **hfg** (Hubbardton Forge): $35,540 ARR, 0.610 score
3. **sc** (Gabriella White): $30,904 ARR, 0.642 score
4. **rw** (RENWIL): $28,249 ARR, 0.625 score
5. **bcf** (Braxton Culler): $26,620 ARR, 0.595 score

### Monitor Closely (Good Band, Watch for Decline)

- **gh** (Gabby): 0.659 score, expansion ready
- **scw** (Summer Classics): 0.650 score, expansion ready
- **jyc** (Jamie Young Company): 0.642 score, $35,725 ARR
- **ih** (Interlude Home): 0.634 score, $4,915 ARR
- **clli** (Craftmade): 0.633 score, $26,065 ARR

### Maintain & Optimize (Fair Band, Stable)

- 108 clients in Fair band
- Focus on top 20 by ARR
- Identify quick wins for engagement/value boosts

---

## 📞 Contact Templates

### For Churn Risk Clients

**Subject:** Checking in on your SuperCat experience

**Body:**
> Hi [Contact],
>
> I noticed it's been a while since we've seen activity in your SuperCat account. I wanted to reach out to:
>
> 1. Make sure everything is working as expected
> 2. See if there are any barriers we can help remove
> 3. Ensure you're getting value from your investment
>
> Would you have 15 minutes this week for a quick check-in call?
>
> Best,
> [Your Name]

### For Expansion-Ready Clients

**Subject:** Exciting new opportunities for [Client Name]

**Body:**
> Hi [Contact],
>
> I've been reviewing your SuperCat usage, and I'm impressed with your results:
> - [X] orders in the last 90 days
> - [X] active users
> - Strong adoption of [features]
>
> Based on your success, I see some opportunities to unlock even more value:
> - [Specific feature/capability]
> - [Specific feature/capability]
> - [Specific feature/capability]
>
> Would you be interested in a brief call to explore these options?
>
> Best,
> [Your Name]

---

## 🎯 Success Criteria

### How to Know This Initiative Is Working

**Month 1:**
- Segment classification complete (63 clients)
- 2 churn risk clients contacted
- 5 expansion QBRs scheduled

**Month 2:**
- Critical band reduced to <30%
- 10+ clients moved from Fair to Good
- 2+ expansion deals closed

**Month 3:**
- Historical data collection live
- First clients reaching Excellent band
- Churn risk count reduced by 25%

**Month 6:**
- Portfolio distribution: 10% Excellent, 30% Good, 50% Fair, <10% At Risk/Critical
- Churn risk ARR reduced by 50%
- $200K+ in expansion deals closed

---

## 📚 Resources

- **Main CSV:** `client_health_scores_2026-03-31.csv`
- **Individual Breakdowns:** `client_breakdowns/` folder
- **Methodology:** `SCORING_METHODOLOGY.md`
- **Strategic Analysis:** `EXECUTIVE_SUMMARY.md`
- **Full Summary:** `SUMMARY_REPORT.md`

---

**Last Updated:** March 31, 2026  
**Next Review:** April 30, 2026 (monthly cadence recommended)
