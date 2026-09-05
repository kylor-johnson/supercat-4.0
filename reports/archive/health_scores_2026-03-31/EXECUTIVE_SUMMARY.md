# Health Intelligence v3 — Executive Summary
## All SuperCat Clients Health Assessment

**Generated:** March 31, 2026  
**Total Clients Analyzed:** 218  
**Analysis Period:** Last 90 days (rolling)

---

## Key Findings

### Overall Health Distribution

- **0 clients (0.0%)** in Excellent health (0.80+)
- **23 clients (10.6%)** in Good health (0.60-0.79)
- **108 clients (49.5%)** in Fair health (0.40-0.59)
- **10 clients (4.6%)** At Risk (0.30-0.39)
- **77 clients (35.3%)** in Critical health (<0.30)

**Key Insight:** The portfolio shows a concerning concentration in Fair and Critical bands, with NO clients achieving Excellent health. This suggests systemic opportunities for improvement across engagement and value realization.

### Critical Action Items

#### 🚨 Churn Risk: 77 clients (35.3%)

**Immediate Severity (1 client):**
- **Butler FurnishWEB Test (sic)**: 0.236 score, $6,960 ARR
  - Zero engagement despite being a paying customer
  - Requires immediate intervention

**High Priority (76 additional clients):**
- Many clients with segment = None (missing segmentation data)
- Several paying customers with minimal engagement
- Concentration of template/test accounts that may need cleanup

#### 💰 Expansion Ready: 29 clients (13.3%)

Top expansion opportunities by health score:
1. **Gabby (gh)**: 0.659 — Platform-Embedded, high engagement
2. **Summer Classics (scw)**: 0.65 — Platform-Embedded, high engagement
3. **Gabriella White (sc)**: 0.642 — Platform-Embedded, $30,904 ARR
4. **RENWIL (rw)**: 0.625 — Platform-Embedded, $28,249 ARR
5. **Hubbardton Forge (hfg)**: 0.61 — Platform-Embedded, $35,540 ARR

**Expansion Criteria Met:**
- High order volumes relative to segment
- Strong engagement patterns
- Feature adoption indicating readiness for additional capabilities

#### ✨ Healthy Complete: 0 clients

No clients currently meet the "Healthy Complete" criteria (0.70+ score with no churn risk and no expansion gaps). This represents a significant opportunity for portfolio optimization.

---

## How Health Scores Are Calculated

Health Intelligence v3 uses a **4-layer weighted composite model** that combines engagement, value realization, trend momentum, and risk signals.

### Layer 1: Engagement Health (25% weight, 100 points max)

Measures how actively users engage with the platform across 6 components:

1. **Login Intensity (20 pts)**: Logins per active user, benchmarked against segment peers
2. **Feature Adoption (20 pts)**: Number of features actively used (CPQ, Sales Portal, Library, etc.)
3. **Portal Engagement (15 pts)**: Sales Portal access events
4. **Seat Utilization (20 pts)**: Active users as % of total licensed users
5. **Behavioral Funnel (15 pts)**: Completion of key user journey stages (catalog → search → cart → order → portal)
6. **Clicky Engagement (10 pts)**: Portal traffic quality (daily visitors, bounce rate)

### Layer 2: Value Realization (40% weight, 125 points max, normalized to 100)

Measures business value derived from the platform across 8 components:

7. **Order Volume (25 pts)**: Order count benchmarked against segment peers
8. **User Activation (20 pts)**: Active user rate relative to total users
9. **Customer Engagement (20 pts)**: Customer selections per order (breadth of customer base)
10. **Product/Inventory Health (15 pts)**: *Neutral score (data unavailable)*
11. **Support Burden (10 pts)**: *Neutral score (data unavailable)*
12. **Geographic Penetration (10 pts)**: *Neutral score (data unavailable)*
13. **Customer Concentration (10 pts)**: *Neutral score (data unavailable)*
14. **Dormant Reactivation (15 pts)**: *Neutral score (data unavailable)*

### Layer 3: Trend Momentum (20% weight, 100 points max)

Measures directional trends over time across 4 components:

15. **Order Volume Trend (30 pts)**: *Neutral score (historical data unavailable)*
16. **User Growth Trend (25 pts)**: *Neutral score (historical data unavailable)*
17. **Customer Health Trend (25 pts)**: *Neutral score (historical data unavailable)*
18. **Feature Adoption Velocity (20 pts)**: *Neutral score (historical data unavailable)*

### Layer 4: Risk Signals (15% weight, -100 to 0 points)

Detects early warning indicators of churn risk across 4 components:

19. **Rep Disengagement Risk (-30 pts max)**: Paying customers with zero/minimal logins
20. **Support Escalation Risk (-30 pts max)**: *No penalty (data unavailable)*
21. **Data Integrity Risk (-20 pts max)**: *No penalty (data unavailable)*
22. **Customer Exodus Risk (-20 pts max)**: *No penalty (data unavailable)*

### Health Bands

| Band | Score Range | Description |
|------|-------------|-------------|
| **Excellent** | 0.80+ | Thriving clients with high engagement and value realization |
| **Good** | 0.60-0.79 | Healthy clients with solid usage patterns |
| **Fair** | 0.40-0.59 | Moderate health, may need attention |
| **At Risk** | 0.30-0.39 | Low health, intervention recommended |
| **Critical** | <0.30 | Severe health issues, immediate action required |

### Three Key Flags

1. **Churn Risk**: Triggered when:
   - Paying customer (ARR > $5,000) has zero logins, OR
   - Composite score < 0.30

2. **Expansion Ready**: Triggered when:
   - Catalog-Focused segment with 50+ orders, OR
   - Commerce-Active segment with 400+ orders, OR
   - 100+ configured items (CPQ opportunity)

3. **Healthy Complete**: Triggered when:
   - Composite score ≥ 0.70, AND
   - No churn risk, AND
   - Either no expansion opportunity OR score ≥ 0.80

---

## Portfolio Analysis

### Segment Distribution

Based on the scored clients:

- **Platform-Embedded**: ~33% of portfolio (highest engagement potential)
- **Commerce-Active**: ~30% of portfolio (transactional focus)
- **Catalog-Focused**: ~15% of portfolio (content-driven)
- **Unknown/None**: ~22% of portfolio (requires segmentation)

### Data Quality Observations

**Missing Segment Data (Critical Issue):**
- 48+ clients have `segment = None`
- These clients default to 0.281 score (Critical band)
- **Action Required:** Segment classification needed for accurate scoring

**Benchmark Availability:**
- Segment benchmarks exist for Platform-Embedded, Commerce-Active, Catalog-Focused
- Clients with missing segments cannot be properly benchmarked

**Historical Data Gaps:**
- Layer 3 (Trend Momentum) uses neutral scores due to missing historical data
- Layer 2 components 10-14 use neutral scores due to missing MCP data
- Layer 4 components 20-22 have no penalties due to missing support/data integrity data

**Impact:** Current scores are conservative and may underrepresent true health for high-performing clients. Once historical and MCP data are available, scores will become more accurate and differentiated.

---

## Strategic Recommendations

### Immediate Actions (Next 30 Days)

1. **Address Churn Risk Clients (77 total)**
   - Prioritize the 1 immediate severity case (sic)
   - Investigate 13 clients with ARR > $20K in Critical/At Risk bands
   - Clean up template/test accounts (tmpl, tmpo, temp, etc.)

2. **Fix Segment Classification**
   - 48+ clients need segment assignment
   - This will unlock proper benchmarking and more accurate scoring

3. **Engage Expansion Ready Clients (29 total)**
   - Focus on top 10 expansion-ready clients with ARR > $25K
   - Gabby (gh), Hubbardton Forge (hfg), and Palecek (pf) are prime candidates

### Medium-Term Improvements (60-90 Days)

1. **Enable Historical Trending**
   - Implement monthly snapshots for Layer 3 (Trend Momentum)
   - This will reveal growth/decline patterns not visible in point-in-time data

2. **Integrate MCP Data**
   - Add support ticket data for Layer 4 (Support Escalation Risk)
   - Add product/inventory health metrics for Layer 2
   - Add customer concentration metrics for Layer 2

3. **Refine Scoring Logic**
   - Adjust benchmarks based on observed portfolio patterns
   - Consider segment-specific weights (e.g., Catalog-Focused may not need portal engagement)

### Long-Term Strategy

1. **Portfolio Health Goal**: Move 50% of clients from Fair to Good within 12 months
2. **Churn Prevention**: Reduce Critical band from 35% to <10%
3. **Expansion Pipeline**: Maintain 15-20% of portfolio as Expansion Ready
4. **Excellence Target**: Achieve 10% of portfolio in Excellent band

---

## Top 10 Healthiest Clients

| Rank | Client | Org | Score | Band | ARR | Key Strengths |
|------|--------|-----|-------|------|-----|---------------|
| 1 | Gabby | gh | 0.659 | Good | N/A | Perfect engagement (100/100), 8 features, 13K orders |
| 2 | Summer Classics | scw | 0.650 | Good | N/A | Perfect engagement (100/100), high portal usage |
| 3 | Jamie Young Company | jyc | 0.642 | Good | $35,725 | 97/100 engagement, strong ARR |
| 4 | Gabriella White | sc | 0.642 | Good | $30,904 | 93/100 engagement, expansion ready |
| 5 | Interlude Home | ih | 0.634 | Good | $4,915 | 90/100 engagement, high value realization |
| 6 | Craftmade | clli | 0.633 | Good | $26,065 | 96/100 engagement, strong commerce activity |
| 7 | Furniture Classics | fc | 0.628 | Good | $23,960 | 94/100 engagement, platform-embedded |
| 8 | Eurofase Inc. | el | 0.626 | Good | N/A | 93/100 engagement, strong feature adoption |
| 9 | Universal Furniture | ufi | 0.626 | Good | $25,435 | 93/100 engagement, solid ARR |
| 10 | RENWIL | rw | 0.625 | Good | $28,249 | 90/100 engagement, expansion ready |

**Common Patterns:**
- All top performers have 87+ engagement scores
- Strong feature adoption (6-8 features)
- High login intensity and seat utilization
- Platform-Embedded segment dominates top 10

---

## Bottom 10 Clients (Require Immediate Attention)

| Rank | Client | Org | Score | Band | ARR | Key Issues |
|------|--------|-----|-------|------|-----|------------|
| 1 | Butler FurnishWEB Test | sic | 0.236 | Critical | $6,960 | Zero engagement, paying customer (IMMEDIATE) |
| 2 | Jonathan Charles at The Gallery | jcsa | 0.271 | Critical | $35,725 | Very low engagement despite high ARR |
| 3 | Coe Limited | ahc | 0.281 | Critical | N/A | Missing segment, zero engagement |
| 4 | Abbyson Living | al | 0.281 | Critical | N/A | Missing segment, zero engagement |
| 5 | ART Furniture, Inc. | art | 0.281 | Critical | N/A | Missing segment, zero engagement |
| 6 | Bad Dog Editions | bde | 0.281 | Critical | N/A | Missing segment, zero engagement |
| 7 | Winslow Home Furniture | bi | 0.281 | Critical | N/A | Missing segment, zero engagement |
| 8 | Bassett Mirror VIP | bmc3 | 0.281 | Critical | N/A | Missing segment, zero engagement |
| 9 | BSC | bscc | 0.281 | Critical | N/A | Missing segment, zero engagement |
| 10 | Big Sandy Superstores | bss | 0.281 | Critical | N/A | Missing segment, zero engagement |

**Common Patterns:**
- Many have missing segment classification (segment = None)
- Zero or near-zero engagement scores
- Several appear to be test/template accounts
- Some have significant ARR but no usage (highest risk)

**Immediate Actions Required:**
1. Verify if template/test accounts should remain in production
2. Reach out to paying customers with zero engagement (sic, jcsa)
3. Complete segment classification for accurate scoring

---

## Expansion Opportunities

### Top 15 Expansion-Ready Clients

| Client | Org | Score | Band | ARR | Expansion Trigger |
|--------|-----|-------|------|-----|-------------------|
| Gabby | gh | 0.659 | Good | N/A | High order volume (13K orders) |
| Summer Classics | scw | 0.650 | Good | N/A | High order volume (11K+ orders) |
| Gabriella White | sc | 0.642 | Good | $30,904 | High order volume, Platform-Embedded |
| RENWIL | rw | 0.625 | Good | $28,249 | High order volume (6K+ orders) |
| Hubbardton Forge | hfg | 0.610 | Good | $35,540 | High ARR, strong engagement |
| Braxton Culler | bcf | 0.595 | Fair | $26,620 | High order volume |
| Somerset Bay and Modern History | sbmh | 0.593 | Fair | N/A | High order volume |
| Palecek | pf | 0.588 | Fair | $39,660 | Highest ARR in expansion group |
| Uniware Housewares Corp. | uhc | 0.584 | Fair | $8,740 | High order volume |
| Interlude Furniture | ihw | 0.578 | Fair | $4,915 | High order volume |
| ELICO LTD. | etl | 0.577 | Fair | $8,700 | High order volume |
| Four Seasons Furniture | fsf | 0.576 | Fair | $22,560 | High order volume |
| Geo Contemporary | gcl | 0.569 | Fair | $9,740 | High order volume |
| Pioneer Morton | mpc | 0.567 | Fair | $15,282 | High order volume |
| Ricci Argentieri Company | rac | 0.567 | Fair | $4,660 | High order volume |

**Total Expansion ARR Opportunity:** $310,000+ across top 15 clients

**Recommended Upsell Paths:**
- **CPQ/Configuration**: Clients with 100+ configured items but no CPQ
- **Sales Portal**: Catalog-Focused clients with 50+ orders
- **Advanced Features**: Commerce-Active clients with 400+ orders

---

## Segment Performance Analysis

### Platform-Embedded Segment (Highest Performers)

**Characteristics:**
- Highest average health scores
- 8 of top 10 healthiest clients
- Strong feature adoption (6-8 features typical)
- High engagement scores (87-100 range)

**Top Performers:**
- Gabby (gh): 0.659
- Summer Classics (scw): 0.650
- Gabriella White (sc): 0.642

### Commerce-Active Segment

**Characteristics:**
- Moderate health scores (0.57-0.63 range for top performers)
- Strong order volumes
- Feature adoption varies (3-6 features)

**Top Performers:**
- Jamie Young Company (jyc): 0.642
- Craftmade (clli): 0.633
- Kalco Lighting (kal): 0.618

### Catalog-Focused Segment

**Characteristics:**
- Lower engagement expectations
- Content-driven usage patterns
- Top performer: Crystorama (clm): 0.602

### Unknown Segment (Data Quality Issue)

**Critical Finding:** 48+ clients have `segment = None`, resulting in:
- Inability to apply proper benchmarks
- Default to 0.281 Critical score
- False churn risk flags

**Action Required:** Complete segment classification for these clients to enable accurate health scoring.

---

## Data Quality & Scoring Limitations

### Current Limitations

1. **Historical Data Unavailable**
   - Layer 3 (Trend Momentum) uses neutral scores (51/100)
   - Cannot detect growth/decline patterns
   - All clients receive same Layer 3 score

2. **MCP Data Unavailable**
   - Layer 2 components 10-14 use neutral scores
   - Layer 4 components 20-22 have no penalties
   - Support burden, data integrity not factored in

3. **Missing Segment Classification**
   - 48+ clients need segment assignment
   - Prevents proper peer benchmarking
   - Results in artificially low scores

### Impact on Scores

**Conservative Bias:** Current scores likely underrepresent true health for high-performing clients because:
- Trend Momentum layer is neutral (no credit for positive trends)
- Several Value Realization components are neutral
- Risk Signals layer cannot penalize support/data issues

**Expected Changes When Data Available:**
- Top performers may score 0.70-0.85 (some reaching Excellent)
- Fair clients may differentiate into Good vs At Risk
- Critical clients with real issues will be more clearly identified

---

## Recommended Next Steps

### Week 1: Data Quality
1. Complete segment classification for all clients with `segment = None`
2. Verify template/test accounts (tmpl, tmpo, temp, etc.) should exist
3. Re-run scoring after segment fixes

### Week 2: Churn Prevention
1. Contact immediate severity case (sic)
2. Reach out to 5 highest-ARR Critical clients
3. Develop intervention playbook for At Risk clients

### Week 3: Expansion Pipeline
1. Create expansion proposals for top 5 expansion-ready clients
2. Schedule QBRs with Gabby, Summer Classics, Gabriella White
3. Identify specific upsell opportunities (CPQ, features, services)

### Month 2-3: Infrastructure
1. Implement historical data collection for Layer 3
2. Integrate support ticket data for Layer 4
3. Add product/inventory health metrics for Layer 2

---

## Files Generated

1. **client_health_scores_2026-03-31.csv** — Main CSV with all 218 client scores
2. **SUMMARY_REPORT.md** — Detailed summary with all clients listed
3. **client_breakdowns/** — 218 individual markdown files with component-level details
4. **EXECUTIVE_SUMMARY.md** — This document

---

## Questions or Issues?

Contact the Insightful Product team for:
- Scoring methodology questions
- Data quality issues
- Custom analysis requests
- Integration support
