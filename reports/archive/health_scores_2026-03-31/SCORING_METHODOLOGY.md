# Health Intelligence v3 — Scoring Methodology

## Quick Reference

### Composite Score Formula

```
Composite Score = (
  (Layer 1 × 0.25) +
  (Layer 2 × 0.40) +
  (Layer 3 × 0.20) +
  (Layer 4 × 0.15)
) / 100
```

### Layer Composition

| Layer | Weight | Max Points | Components |
|-------|--------|------------|------------|
| Layer 1: Engagement Health | 25% | 100 | 6 components |
| Layer 2: Value Realization | 40% | 125 → 100 | 8 components (normalized) |
| Layer 3: Trend Momentum | 20% | 100 | 4 components |
| Layer 4: Risk Signals | 15% | -100 to 0 | 4 components (penalties) |

---

## Layer 1: Engagement Health (100 points max)

### Component 1: Login Intensity (20 points max)

**Calculation:** `logins_90d / active_users_90d`

**Scoring Logic:**
- Small orgs (≤10 users): Based on login intensity vs segment benchmarks
- Standard orgs (>10 users): Login intensity + active user % thresholds

**Thresholds (Standard Orgs):**
- 20 pts: ≥P75 login intensity AND ≥15% active user rate
- 17 pts: ≥Median login intensity AND ≥10% active user rate
- 14 pts: ≥P25 login intensity AND ≥5% active user rate
- 10 pts: Any logins
- 0 pts: No logins

### Component 2: Feature Adoption (20 points max)

**Calculation:** Count of features actively used

**Features Tracked:**
- Sales Portal
- CPQ/Configuration
- B2B Cart
- Library
- Kits
- PDF Catalog Export
- Clicky Analytics

**Scoring Logic:**
- **Catalog-Focused:** 15 pts (3+ features), 10 pts (2), 5 pts (1), 0 pts (0)
- **Commerce-Active/Platform-Embedded:** 20 pts (4+), 15 pts (3), 10 pts (2), 5 pts (1), 0 pts (0)

### Component 3: Portal Engagement (15 points max)

**Calculation:** Sales Portal access events in last 90 days

**Scoring:**
- 15 pts: ≥500 access events
- 12 pts: ≥200 access events
- 8 pts: >0 access events
- 0 pts: No portal access

### Component 4: Seat Utilization (20 points max)

**Calculation:** `active_users / total_users`

**Scoring:**
- 20 pts: ≥60% utilization
- 17 pts: ≥40% utilization
- 14 pts: ≥20% utilization
- 10 pts: >0% utilization
- 0 pts: No users

### Component 5: Behavioral Funnel (15 points max)

**Stages Tracked:**
1. Catalog access (logins)
2. Product search
3. Customer selection (cart)
4. Order submission
5. Portal access

**Scoring Logic:**
- **Catalog-Focused:** 10 pts (catalog + search), 5 pts (catalog only), 0 pts (none)
- **Commerce-Active:** 15 pts (3+ stages), 10 pts (2), 5 pts (1), 0 pts (0)
- **Platform-Embedded:** 15 pts (4+ stages), 12 pts (3), 8 pts (2), 4 pts (1), 0 pts (0)

### Component 6: Clicky Engagement (10 points max)

**Calculation:** Portal traffic quality (daily visitors + bounce rate)

**Scoring:**
- 10 pts: ≥100 daily visitors AND <50% bounce rate
- 8 pts: ≥100 daily visitors
- 6 pts: ≥50 daily visitors
- 3 pts: >0 daily visitors
- 0 pts: No Clicky Analytics

---

## Layer 2: Value Realization (125 points max, normalized to 100)

### Component 7: Order Volume (25 points max)

**Calculation:** Order count in last 90 days vs segment benchmarks

**Scoring:**
- 25 pts: ≥P75 benchmark
- 20 pts: ≥Median benchmark
- 15 pts: ≥P25 benchmark
- 10 pts: >0 orders
- 0 pts: No orders

### Component 8: User Activation (20 points max)

**Calculation:** `active_users / total_users`

**Scoring:**
- 20 pts: ≥60% activation
- 17 pts: ≥40% activation
- 14 pts: ≥20% activation
- 10 pts: >0% activation
- 0 pts: No users

### Component 9: Customer Engagement (20 points max)

**Calculation:** `customer_selections / orders` (customer breadth per order)

**Scoring:**
- 20 pts: ≥2.0 ratio (high customer variety)
- 17 pts: ≥1.5 ratio
- 14 pts: ≥1.0 ratio
- 10 pts: >0 ratio
- 0 pts: No orders

### Components 10-14 (Neutral Scores in Current Implementation)

- **Component 10:** Product/Inventory Health (15 pts max) — *8 pts neutral*
- **Component 11:** Support Burden (10 pts max) — *5 pts neutral*
- **Component 12:** Geographic Penetration (10 pts max) — *5 pts neutral*
- **Component 13:** Customer Concentration (10 pts max) — *5 pts neutral*
- **Component 14:** Dormant Reactivation (15 pts max) — *8 pts neutral*

**Note:** These components use neutral scores due to missing MCP/additional data. Once available, they will provide more nuanced value realization assessment.

**Normalization:** Total raw score (max 125) is normalized to 100 for consistency with other layers.

---

## Layer 3: Trend Momentum (100 points max)

### Components 15-18 (Neutral Scores in Current Implementation)

- **Component 15:** Order Volume Trend (30 pts max) — *15 pts neutral*
- **Component 16:** User Growth Trend (25 pts max) — *13 pts neutral*
- **Component 17:** Customer Health Trend (25 pts max) — *13 pts neutral*
- **Component 18:** Feature Adoption Velocity (20 pts max) — *10 pts neutral*

**Note:** These components require historical snapshots (monthly data over 6-12 months). Current implementation uses neutral scores (51/100 total) for all clients.

**Future Implementation:** Once historical data is available:
- Positive trends (growth) will add points
- Negative trends (decline) will subtract points
- Flat trends will remain neutral

---

## Layer 4: Risk Signals (-100 to 0 points)

### Component 19: Rep Disengagement Risk (-30 points max)

**Calculation:** Paying customers with zero/minimal logins

**Scoring:**
- -30 pts: ARR > $5,000 AND zero logins (CRITICAL)
- -15 pts: ARR > $5,000 AND <100 logins
- 0 pts: No disengagement detected

**Auto-Cap:** If this risk is triggered, composite score is capped at 0.30 (Critical band)

### Components 20-22 (No Penalties in Current Implementation)

- **Component 20:** Support Escalation Risk (-30 pts max) — *0 pts (no penalty)*
- **Component 21:** Data Integrity Risk (-20 pts max) — *0 pts (no penalty)*
- **Component 22:** Customer Exodus Risk (-20 pts max) — *0 pts (no penalty)*

**Note:** These components require support ticket data and customer activity tracking. Current implementation applies no penalties due to missing data.

---

## Health Bands & Thresholds

| Band | Score Range | Description | Typical Characteristics |
|------|-------------|-------------|------------------------|
| **Excellent** | 0.80 - 1.00 | Thriving clients | 90+ engagement, 80+ value realization, positive trends |
| **Good** | 0.60 - 0.79 | Healthy clients | 70+ engagement, 65+ value realization, stable/growing |
| **Fair** | 0.40 - 0.59 | Moderate health | 50+ engagement, 50+ value realization, stable |
| **At Risk** | 0.30 - 0.39 | Low health | <50 engagement OR <50 value realization |
| **Critical** | 0.00 - 0.29 | Severe issues | Near-zero engagement OR disqualifying risk |

---

## Three Key Flags

### 🚨 Churn Risk Flag

**Triggered When:**
1. Paying customer (ARR > $5,000) has zero logins, OR
2. Composite score < 0.30

**Severity Levels:**
- **Immediate:** Paying customer with zero logins (auto-caps score to 0.30)
- **Standard:** Score < 0.30 due to low engagement/value

**Action Required:**
- Immediate: Outreach within 48 hours
- Standard: Intervention plan within 2 weeks

### 💰 Expansion Ready Flag

**Triggered When:**
1. Catalog-Focused segment with 50+ orders, OR
2. Commerce-Active segment with 400+ orders, OR
3. 100+ configured items (indicates CPQ opportunity)

**Recommended Actions:**
- Schedule QBR/EBR
- Present upsell opportunities
- Identify feature gaps
- Propose expansion roadmap

### ✨ Healthy Complete Flag

**Triggered When:**
1. Composite score ≥ 0.70, AND
2. No churn risk, AND
3. Either no expansion opportunity OR score ≥ 0.80

**Interpretation:**
- Client is healthy and fully utilizing available features
- Maintenance mode (monitor for changes)
- Low touch required unless trends decline

---

## Worked Examples

### Example 1: Gabby (gh) — Top Performer

**Final Score:** 0.659 (Good)

**Layer Breakdown:**
- Layer 1 (Engagement): 100/100 × 0.25 = 25.0
- Layer 2 (Value): 76.8/100 × 0.40 = 30.7
- Layer 3 (Trend): 51/100 × 0.20 = 10.2
- Layer 4 (Risk): 0/0 × 0.15 = 0.0
- **Total:** (25.0 + 30.7 + 10.2 + 0.0) / 100 = **0.659**

**Why This Score:**
- Perfect engagement (100/100): All 6 components maxed out
- Strong value realization (76.8/100): High order volume, good activation
- Neutral trend momentum (51/100): Historical data unavailable
- No risk signals (0): No disengagement detected

**Flags:**
- Expansion Ready: YES (13,226 orders far exceeds thresholds)
- Churn Risk: NO
- Healthy Complete: NO (expansion opportunity exists)

### Example 2: Butler FurnishWEB Test (sic) — Critical Case

**Final Score:** 0.236 (Critical)

**Layer Breakdown:**
- Layer 1 (Engagement): 0/100 × 0.25 = 0.0
- Layer 2 (Value): 44.8/100 × 0.40 = 17.9
- Layer 3 (Trend): 51/100 × 0.20 = 10.2
- Layer 4 (Risk): -30/0 × 0.15 = -4.5
- **Total:** (0.0 + 17.9 + 10.2 - 4.5) / 100 = **0.236**

**Why This Score:**
- Zero engagement (0/100): No logins, no features, no activity
- Moderate value (44.8/100): Only from neutral scores (no actual value)
- Neutral trend momentum (51/100): Historical data unavailable
- Severe risk penalty (-30): Paying customer ($6,960 ARR) with zero logins

**Flags:**
- Churn Risk: YES (Immediate severity)
- Expansion Ready: NO
- Healthy Complete: NO

**Auto-Cap Applied:** Score capped at 0.30 due to disqualifying risk (actual raw score would be similar)

### Example 3: Craftmade (clli) — Strong Commerce Client

**Final Score:** 0.633 (Good)

**Layer Breakdown:**
- Layer 1 (Engagement): 96/100 × 0.25 = 24.0
- Layer 2 (Value): 72.8/100 × 0.40 = 29.1
- Layer 3 (Trend): 51/100 × 0.20 = 10.2
- Layer 4 (Risk): 0/0 × 0.15 = 0.0
- **Total:** (24.0 + 29.1 + 10.2 + 0.0) / 100 = **0.633**

**Why This Score:**
- Near-perfect engagement (96/100): Strong across all components
- Good value realization (72.8/100): Solid order volume and activation
- Neutral trend momentum (51/100): Historical data unavailable
- No risk signals (0): No disengagement detected

**Flags:**
- Expansion Ready: NO (below thresholds for Commerce-Active)
- Churn Risk: NO
- Healthy Complete: NO (score < 0.70)

---

## Component Scoring Details

### Login Intensity Calculation

**Example: Gabby (gh)**
- Total logins (90d): 11,002
- Active users: 56
- Login intensity: 11,002 / 56 = **196.46 logins per active user**
- Active user %: 56 / 91 = **62%**
- Org size: Standard (>10 users)

**Benchmark Comparison (Platform-Embedded):**
- P75 login intensity: ~150 logins per user
- Gabby's 196.46 exceeds P75 ✓
- Active user % 62% exceeds 15% threshold ✓
- **Score: 20/20**

### Feature Adoption Calculation

**Example: Gabby (gh)**
- Feature depth: 8 features
- Segment: Platform-Embedded
- Threshold: 4+ features for max score
- **Score: 20/20**

### Order Volume Calculation

**Example: Gabby (gh)**
- Orders (90d): 13,226
- Segment: Platform-Embedded
- P75 benchmark: 6,109
- Median benchmark: 2,986
- Gabby's 13,226 exceeds P75 ✓
- **Score: 25/25**

### Seat Utilization Calculation

**Example: Gabby (gh)**
- Active users: 56
- Total users: 91
- Utilization: 56 / 91 = **62%**
- Threshold: ≥60% for max score
- **Score: 20/20**

---

## Benchmark Data Sources

### Segment Benchmarks (Monthly)

**Source:** `segment_benchmarks_monthly` table in BigQuery

**Benchmarks Available:**
- Login intensity (P25, Median, P75)
- Order volume (P25, Median, P75)
- Feature adoption rates
- ARR/MRR percentiles

**Segments:**
- Platform-Embedded (33 clients)
- Commerce-Active (~60 clients)
- Catalog-Focused (~30 clients)

**Update Frequency:** Monthly (latest: March 2026)

---

## Scoring Philosophy

### Design Principles

1. **Segment-Aware:** Different expectations for different client types
2. **Benchmark-Driven:** Scores relative to peer performance, not absolute
3. **Weighted Layers:** Value realization (40%) weighted highest
4. **Risk-Adjusted:** Disqualifying risks auto-cap scores
5. **Graceful Degradation:** Missing data uses neutral scores (not penalties)

### Why Neutral Scores?

**Problem:** If we scored missing data as 0, clients would be unfairly penalized for data gaps.

**Solution:** Use neutral scores (midpoint of range) when data unavailable:
- Layer 3 components: 51/100 total (neutral momentum)
- Layer 2 components 10-14: Neutral values that sum to ~40/125
- Layer 4 components 20-22: 0 penalty (no data = no penalty)

**Impact:** Scores are conservative but fair. Once data is available, scores will become more differentiated.

---

## Common Scoring Scenarios

### Scenario 1: High Engagement, Low Orders

**Profile:**
- 90+ engagement score
- <P25 order volume
- Result: Fair band (0.40-0.59)

**Example:** Client with many logins, feature usage, but few orders
**Interpretation:** Users are engaged but not transacting (may indicate pricing, inventory, or workflow issues)

### Scenario 2: High Orders, Low Engagement

**Profile:**
- <50 engagement score
- ≥P75 order volume
- Result: Fair band (0.40-0.59)

**Example:** Client with many orders but few logins
**Interpretation:** Possible API integration or rep-driven ordering (not self-service)

### Scenario 3: Balanced Performance

**Profile:**
- 70-90 engagement score
- Median-P75 order volume
- Result: Good band (0.60-0.79)

**Example:** Solid performance across all dimensions
**Interpretation:** Healthy client with room for optimization

### Scenario 4: Paying But Disengaged

**Profile:**
- ARR > $5,000
- Zero logins
- Result: Critical band (auto-capped at 0.30)

**Example:** Client paying but not using platform
**Interpretation:** Immediate churn risk, requires urgent intervention

---

## Data Sources

### BigQuery Tables Used

1. **org_summary** — Primary client metrics
   - Engagement data (logins, orders, users)
   - Feature adoption flags
   - Portal traffic (Clicky)
   - Segment classification

2. **segment_benchmarks_monthly** — Peer comparison data
   - Login intensity percentiles
   - Order volume percentiles
   - Feature adoption rates
   - Updated monthly

### Data Freshness

- **org_summary:** Updated daily (last update: April 1, 2026 03:27 UTC)
- **segment_benchmarks_monthly:** Updated monthly (latest: March 2026)

### Missing Data Sources (Future)

- **Historical snapshots:** For Layer 3 trend calculations
- **Support tickets:** For Layer 4 support escalation risk
- **MCP data:** For Layer 2 components 10-14
- **Customer activity:** For Layer 4 customer exodus risk

---

## Validation & Quality Checks

### Known Issues in Current Run

1. **Missing Segments:** 48+ clients have `segment = None`
   - Cannot apply proper benchmarks
   - Default to 0.281 score (Critical)
   - **Fix:** Complete segment classification

2. **Template Accounts:** Several template/test accounts scored
   - tmpl, tmpo, temp, tech (demo), etc.
   - **Fix:** Remove from production or flag as test accounts

3. **Order Volume Scoring:** Component 7 may give 25 pts even with 0 orders if benchmarks are also 0
   - Affects clients in segments with no order data
   - **Fix:** Add validation to prevent false positives

### Validation Recommendations

1. **Spot Check Top 10:** Verify scores match expected performance
2. **Review Critical Clients:** Confirm low scores are accurate
3. **Check Expansion Flags:** Validate expansion-ready clients meet criteria
4. **Segment Validation:** Ensure segment classifications are correct

---

## Interpreting Scores

### What Makes a Good Score?

**Good Band (0.60-0.79):**
- Engagement: 70-90 points (active users, features, logins)
- Value Realization: 65-80 points (orders, activation, customer breadth)
- Trend Momentum: 51 points (neutral, will vary when data available)
- Risk Signals: 0 to -10 points (minimal risk)

### What Causes Low Scores?

**Critical Band (<0.30):**
- Zero engagement (0 logins, 0 features, 0 orders)
- Disqualifying risk (paying but disengaged)
- Missing segment classification

**At Risk Band (0.30-0.39):**
- Low engagement (10-30 points)
- Low value realization (30-50 points)
- May have minor risk penalties

### Why No Excellent Scores?

**Current Portfolio Reality:**
- No clients have 80+ engagement AND 80+ value realization
- Layer 3 neutral scores (51/100) prevent reaching 0.80+
- Once historical data available, top performers may reach Excellent

**To Reach Excellent (0.80+):**
- Need 90+ engagement
- Need 85+ value realization
- Need positive trend momentum (60+ when available)
- Need zero risk signals

---

## Using These Scores

### For Account Management

1. **Prioritize by Band:**
   - Critical: Immediate intervention
   - At Risk: Proactive outreach
   - Fair: Monitor and optimize
   - Good: Maintain and expand
   - Excellent: Showcase and replicate

2. **Use Flags for Action:**
   - Churn Risk: Retention playbook
   - Expansion Ready: Upsell pipeline
   - Healthy Complete: Low-touch monitoring

### For Executive Reporting

- **Portfolio Health:** Distribution by band
- **Risk Exposure:** Count and ARR of churn risk clients
- **Growth Pipeline:** Count and ARR of expansion-ready clients
- **Trends:** Month-over-month changes (once historical data available)

### For Product Strategy

- **Feature Adoption Gaps:** Which features are underutilized?
- **Engagement Patterns:** What drives high engagement scores?
- **Value Realization:** What separates Good from Fair clients?
- **Risk Indicators:** What early signals predict churn?

---

## Scoring Roadmap

### Phase 1: Current State (Complete)
- ✅ 4-layer composite model
- ✅ Segment-aware benchmarking
- ✅ 22 component framework
- ✅ 3 key flags
- ✅ Graceful degradation for missing data

### Phase 2: Historical Trending (Next 60 days)
- ⏳ Monthly snapshots for Layer 3
- ⏳ Growth/decline detection
- ⏳ Trend-based scoring adjustments

### Phase 3: MCP Integration (Next 90 days)
- ⏳ Support ticket data for Layer 4
- ⏳ Product/inventory health for Layer 2
- ⏳ Customer concentration metrics

### Phase 4: Advanced Analytics (Future)
- ⏳ Predictive churn modeling
- ⏳ Expansion propensity scoring
- ⏳ Automated intervention triggers
- ⏳ Real-time score updates

---

## Technical Notes

### Performance

- **Batch Size:** 5 clients per batch
- **Total Runtime:** ~20 minutes for 218 clients
- **BigQuery Queries:** 2 per client (org_summary + segment_benchmarks)
- **Rate Limiting:** None applied (BigQuery handles concurrency)

### Output Files

1. **CSV:** Sortable, filterable, Excel-compatible
2. **Summary Report:** High-level overview with all clients listed
3. **Client Breakdowns:** 218 individual markdown files with full component details
4. **Executive Summary:** Strategic analysis and recommendations

### Reproducibility

To re-run scoring:

```bash
cd "/path/to/SuperCat 4.0"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
source "/path/to/venv/bin/activate"
python scripts/health_score_batch_calculator_v3.py --batch-size 5 --output-dir reports/health_scores_YYYY-MM-DD
```

---

## Appendix: Segment Benchmark Values (March 2026)

### Platform-Embedded (33 clients)

- **Login Intensity:**
  - P25: 4,640 total logins
  - Median: 6,368 total logins
  - P75: 8,568 total logins

- **Order Volume:**
  - P25: 1,205 orders
  - Median: 2,986 orders
  - P75: 6,109 orders

### Commerce-Active (~60 clients)

- **Order Volume:**
  - P25: ~800 orders (estimated)
  - Median: ~1,500 orders (estimated)
  - P75: ~3,000 orders (estimated)

### Catalog-Focused (~30 clients)

- **Order Volume:**
  - P25: ~50 orders (estimated)
  - Median: ~150 orders (estimated)
  - P75: ~400 orders (estimated)

**Note:** Exact benchmarks vary by segment and are updated monthly based on actual portfolio performance.
