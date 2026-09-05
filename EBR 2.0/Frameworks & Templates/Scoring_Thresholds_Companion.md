# Scoring Thresholds Companion

**Version:** 1.1 | **Date:** February 26, 2026
**v1.1 changelog:** Fathom absence is no longer a scoring penalty. Fathom inputs score as N/A (weight redistributes) when no data exists — not as zero. Removed 60-point ceiling cap on Relationship Strength. Relationship Cooling Fathom inputs also N/A when no data exists (only scores as risk when meetings were previously happening and stopped). HelpScout silence reframed: only a risk signal when it represents a change from the account's established historical pattern, not an absolute threshold. Updated Crystorama worked example (Expansion: 67→73, Risk: 8→3).

> Defines explicit 0/25/50/75/100 thresholds for every scoring component input. Without these, two operators will produce different scores from the same data. These thresholds are starting assumptions based on the Crystorama test run and general SaaS benchmarks. They should be recalibrated after running the model across all 129 accounts.

---

## How to Use This Document

For each component input, look up the metric value and find the corresponding score band. Interpolate linearly within bands (e.g., Active User Ratio of 55% falls between 50-band and 75-band → score ~62).

When multiple inputs feed a single component, score each input individually, then average the input scores to produce the component score. Apply the component weight from the Account Scoring Framework to compute the weighted contribution.

---

## Expansion Readiness — Component Thresholds

### Adoption Depth (30% weight)

| Input | 0 | 25 | 50 | 75 | 100 | Source |
|---|---|---|---|---|---|---|
| **Active User Ratio** (Mixpanel active / billable) | <10% | 10–30% | 30–55% | 55–80% | >80% | Mixpanel + PostgreSQL/HubSpot |
| **Activity Ladder Levels Active** (out of 6) | 0–1 | 2 | 3 | 4–5 | 6 | Mixpanel |
| **Feature Breadth Score** (avg distinct features per active user) | <3 | 3–6 | 7–12 | 13–18 | >18 | Mixpanel |
| **Subscription Completeness** (products active / total suite) | 1/4 (25%) | 2/4 (50%) | 3/4 (75%) | 4/4 (100%) | 4/4 + add-ons | Stripe / PostgreSQL |

**Notes:**
- Total product suite = eCat iPad, eCat Online, Sales Portal, Admin Console. Adjust denominator if product suite changes.
- Feature Breadth Score counts distinct event types (not event volume) per user, averaged across all active users.
- Active User Ratio uses the canonical Mixpanel definition (see Metrics Framework v5 Design Notes).

### Business Impact (25% weight)

**Ordering Clients:**

| Input | 0 | 25 | 50 | 75 | 100 | Source |
|---|---|---|---|---|---|---|
| **Order Volume Trend** (MoM, 3-month) | Declining 3+ months | Declining 1–2 months | Flat (±5%) | Growing 1–2 months | Growing 3+ months | PostgreSQL / Mixpanel |
| **AOV vs. Segment Median** | <25% of median | 25–50% | 50–100% | 100–150% | >150% | Admin Orders Report |
| **Customer Activation Rate** (customers ordering / total) | <5% | 5–15% | 15–30% | 30–50% | >50% | PostgreSQL |
| **Digital Self-Service Rate** (online orders / total) | 0% | 1–10% | 10–25% | 25–50% | >50% | Mixpanel |

**Non-Ordering Clients:**

| Input | 0 | 25 | 50 | 75 | 100 | Source |
|---|---|---|---|---|---|---|
| **Buyer-Facing Actions per Active User (90d)** | 0 | 1–3 | 4–8 | 9–15 | >15 | Mixpanel |
| **Buyer-Facing Action Trend** (MoM, 3-month) | Declining 3+ months | Declining 1–2 months | Flat (±10%) | Growing 1–2 months | Growing 3+ months | Mixpanel |
| **PDF Catalogs Created (90d)** | 0 | 1–20 | 21–75 | 76–150 | >150 | Mixpanel |
| **Library Share Rate** (emails sent / documents viewed) | 0% | 1–5% | 5–15% | 15–30% | >30% | Mixpanel |

**Non-Ordering + Pushed Data Clients (additional inputs at 50% weight):**

| Input | 0 | 25 | 50 | 75 | 100 | Source |
|---|---|---|---|---|---|---|
| **Pushed Order Volume Trend** (MoM, 3-month) | Declining 3+ months | Declining 1–2 months | Flat (±5%) | Growing 1–2 months | Growing 3+ months | PostgreSQL `orders` |
| **Pushed Revenue (12-month)** | <$10K | $10–50K | $50–150K | $150–500K | >$500K | PostgreSQL `orders` |
| **Import Cadence** (data pushes per month) | 0 | 1–5 | 6–15 | 16–50 | >50 (daily+) | PostgreSQL `import_events` |

**Pushed data scoring:** Score each pushed input on the 0–100 scale above, average them, then multiply by 0.5 (50% weight). Add to the non-ordering inputs score (at full weight). Example: Non-ordering inputs average = 60, pushed data inputs average = 80. Component score = (60 × 0.67) + (80 × 0.5 × 0.33) = 40.2 + 13.2 = 53.4. (Weights normalize so non-ordering inputs get ~67% and pushed gets ~33% of the component.)

### Growth Signals (25% weight)

| Input | 0 | 25 | 50 | 75 | 100 | Source |
|---|---|---|---|---|---|---|
| **MAU Trend** (MoM, 3-month) | Declining 3+ months | Declining 1–2 months | Flat (±5%) | Growing 1–2 months | Growing 3+ months | Mixpanel |
| **User Growth** (net new users, 90d) | Net loss | 0 (flat) | 1–5 new | 6–15 new | >15 new | PostgreSQL `org_users` |
| **Expansion Signals Triggered** (from §14) | 0 | 1 | 2–3 | 4–5 | >5 | Cross-source |
| **Fathom Pain → Unused Feature Matches** | N/A (no Fathom) | 0 matches | 1 match | 2 matches | >2 matches | Fathom + feature usage |
| **Open HubSpot Expansion Deals** | 0 | — | 1 (early stage) | 1 (late stage) | >1 deal | HubSpot |

**Notes:**
- If Fathom data is absent, this input scores as N/A and weight redistributes to remaining inputs.
- Expansion Signals from §14 of the Metrics Framework: count how many are currently active for the account.

### Relationship Strength (20% weight)

| Input | 0 | 25 | 50 | 75 | 100 | Source |
|---|---|---|---|---|---|---|
| **Fathom Meeting Cadence** (meetings in last 90d) | *If no Fathom data: N/A — skip this input, redistribute weight to remaining inputs* | 1 | 2 | 3–4 | >4 (monthly+) | Fathom |
| **Days Since Last Interaction** (any channel) | >90 days | 61–90 | 31–60 | 15–30 | <15 | Fathom + HelpScout + HubSpot |
| **Stakeholder Breadth** (distinct contacts across all sources) | 1 | 2–3 | 4–6 | 7–10 | >10 | HubSpot + Fathom + HelpScout |
| **HelpScout Responsiveness** (all tickets resolved, low wait time) | Multiple unresolved, high wait | Some unresolved | All resolved, moderate pace | All resolved, responsive | All resolved quickly + proactive engagement | HelpScout |

**Notes:**
- **Fathom absence is NOT a penalty.** If Fathom = zero meetings, the Meeting Cadence input is N/A and its weight redistributes to the remaining three inputs. A self-sufficient, well-implemented client should not score lower because we haven't scheduled calls with them. No ceiling cap applies.
- Fathom absence IS surfaced as an operational callout in the Snapshot (A3/A5) and Intelligence Brief (B5) — "No proactive meeting history on record. Consider establishing a structured engagement cadence." This is a recommendation to the team, not a judgment on the account.
- If Fathom data exists, use it — meeting cadence, pain themes, and competitor mentions are all valuable signal. The input only becomes N/A when no data exists at all.

---

## Retention Risk — Component Thresholds

**Reminder:** Retention Risk scores are inverted from Expansion Readiness. A HIGH score = HIGH risk = BAD. The thresholds below produce higher scores for worse conditions.

### Engagement Decline (30% weight)

| Input | 0 (no risk) | 25 | 50 | 75 | 100 (critical) | Source |
|---|---|---|---|---|---|---|
| **MAU Trend** (MoM, 3-month) | Growing 3+ months | Growing 1–2 | Flat | Declining 1–2 months | Declining 3+ months | Mixpanel |
| **Active User Ratio Change** (vs. 3 months ago) | Increased >10pts | Increased 1–10pts | Flat (±2pts) | Decreased 3–10pts | Decreased >10pts | Mixpanel + PostgreSQL |
| **Login Frequency Trend** | Increasing | Stable-high | Stable-moderate | Declining | Declining + low absolute | Mixpanel (`selected_org`) |
| **User Count Change** (net, 90d) | Net gain >5 | Net gain 1–5 | Flat | Net loss 1–5 | Net loss >5 | PostgreSQL `org_users` |

### Relationship Cooling (25% weight)

| Input | 0 (no risk) | 25 | 50 | 75 | 100 (critical) | Source |
|---|---|---|---|---|---|---|
| **Days Since Last Fathom Meeting** | *If no Fathom data: N/A — skip this input, redistribute weight. If Fathom exists:* <30 days | 30–60 | 60–90 | 90–180 | >180 (meetings were happening, then stopped) | Fathom |
| **Competitor Mentions** (last 90d calls) | *If no Fathom data: N/A — skip.* 0 | — | 1 mention | 2 mentions | >2 mentions | Fathom |
| **HelpScout Ticket Pattern Change** (vs. established cadence) | Normal cadence maintained | Slight decrease from norm | 50%+ decrease from established cadence | Near-silence after regular cadence | Complete silence after regular cadence (>90d gap) | HelpScout |
| **Unresolved Ticket Age** (oldest open ticket) | No open tickets | <7 days | 7–14 days | 14–30 days | >30 days open | HelpScout |
| **Billing/Cancellation Tags** (in recent tickets) | 0 | — | 1 tag | 2 tags | >2 tags | HelpScout |

**Notes:**
- **Fathom absence is NOT a risk signal.** If Fathom = zero data for an account, both Fathom inputs (Days Since Last Meeting and Competitor Mentions) are N/A and weight redistributes to HelpScout inputs. Absence of Fathom data means we can't observe proactive relationship signals — it does not mean the relationship is cooling. Surfaced as an operational callout, not a score penalty.
- **Fathom cessation IS a risk signal.** If an account previously had regular Fathom meetings and they stopped (e.g., monthly meetings for 6 months, then nothing for 90+ days), that IS a cooling indicator and should score high on Days Since Last Meeting.
- **HelpScout silence is only a risk signal when it represents a CHANGE from established patterns.** A client that averages 1 ticket/quarter and hasn't filed one in 60 days is behaving normally. A client that averaged 3 tickets/month and suddenly went silent for 90 days is flagging. The input measures deviation from the account's own historical norm, not an absolute threshold.
- Zero HelpScout tickets from a high-engagement, well-implemented account = self-sufficient. Not a risk signal. Score as 0 (no risk).

### Financial Distress (25% weight)

| Input | 0 (no risk) | 25 | 50 | 75 | 100 (critical) | Source |
|---|---|---|---|---|---|---|
| **Payment Status** | Current, $0 outstanding | 1–15 days overdue | 16–30 days overdue | 31–60 days overdue | >60 days overdue | Stripe / QuickBooks |
| **Invoice Aging** (oldest unpaid) | All paid | <30 days | 30–45 days | 45–60 days | >60 days | QuickBooks |
| **MRR Trend** (6-month) | Growing | Flat | Contracted <10% | Contracted 10–25% | Contracted >25% | Stripe / QuickBooks |
| **Order Revenue Trend** (ordering/pushed clients only) | Growing | Flat | Declined <15% | Declined 15–30% | Declined >30% | PostgreSQL / Admin |

### Operational Deterioration (20% weight)

| Input | 0 (no risk) | 25 | 50 | 75 | 100 (critical) | Source |
|---|---|---|---|---|---|---|
| **Data Freshness** (days since last import) | Today | 1–3 days | 4–7 days | 8–14 days | >14 days | PostgreSQL `import_events` |
| **Import Error Rate** (errors / total imports, 30d) | 0% | 1–5% | 5–15% | 15–30% | >30% | PostgreSQL `import_events` |
| **Repeated Support Issues** (same-topic tickets in 90d) | 0 repeats | 1 repeat | 2 repeats | 3 repeats | >3 repeats | HelpScout |
| **Inventory Staleness** (days since inventory update) | Today | 1–3 days | 4–7 days | 8–14 days | >14 days | PostgreSQL `inventories` |

---

## Scoring Calculation Example

**Account: Crystorama (Non-Ordering + Pushed Data)**

### Expansion Readiness

| Component | Weight | Input Scores | Component Score | Weighted |
|---|---|---|---|---|
| Adoption Depth | 30% | Active User Ratio: 75% → 75, Ladder Levels: 5/6 → 83, Feature Breadth: ~20 → 83, Sub Completeness: 4/4 → 75. Avg: 79 | **79** | 23.7 |
| Business Impact | 25% | Non-ordering: Actions/user 4.5 → 52, Trend: growing → 75, PDFs: 185 → 75, Share Rate: 6.6% → 52. Avg: 63.5. Pushed: Volume trend: breakout → 100, Revenue $536K → 100, Import cadence: daily → 100. Avg: 100 × 0.5 = 50. Combined: ~70 | **70** | 17.5 |
| Growth Signals | 25% | MAU: growing → 75, User growth: new users → 75, Expansion signals: 7 → 100, Fathom: N/A, HubSpot deals: 0 → 0. Avg (excl N/A): 62.5 | **63** | 15.8 |
| Relationship Strength | 20% | Fathom: N/A (no data — skip, redistribute). Days since: 23 → 60, Stakeholder breadth: 12+ → 100, HelpScout: all resolved → 75. Avg of 3 scored inputs: 78 | **78** | 15.6 |
| | | | **Total** | **72.6 → 73** |

vs. original Cursor output: **67** (which applied a Fathom penalty). With the corrected approach (no penalty for self-sufficient client), Crystorama moves from Nurture (67) to the low end of Active Expansion Target range — which better reflects the reality of a 12-year, deeply embedded, high-engagement account.

### Retention Risk

| Component | Weight | Input Scores | Component Score | Weighted |
|---|---|---|---|---|
| Engagement Decline | 30% | MAU: growing → 0, Ratio: increased → 0, Login: stable → 15, Users: net gain → 0. Avg: 4 | **4** | 1.2 |
| Relationship Cooling | 25% | Fathom: N/A (no data — skip both inputs, redistribute). Ticket pattern: normal cadence → 0, Unresolved: none → 0, Billing tags: 0 → 0. Avg of 3 scored inputs: 0 | **0** | 0 |
| Financial Distress | 25% | Payment: current → 0, Aging: all paid → 0, MRR: flat → 10, Revenue: growing → 0. Avg: 2.5 | **3** | 0.8 |
| Operational Deterioration | 20% | Freshness: today → 0, Errors: low → 10, Repeats: 0 → 0, Inventory: today → 0. Avg: 2.5 | **3** | 0.6 |
| | | | **Total** | **2.6 → 3** |

vs. original Cursor output: **8** (which scored Fathom absence as a risk signal). With the corrected approach, Crystorama's risk score drops further — confirming this is a healthy, stable account with no cooling signals.

---

## Calibration Notes

These thresholds are derived from:
- The Crystorama test run (a large, healthy, long-tenured non-ordering + pushed data account)
- General B2B SaaS benchmarks for engagement and retention metrics
- Reasonable assumptions about SuperCat's 129-account portfolio

**They have NOT been validated against:**
- The full portfolio (running all 129 accounts would reveal threshold outliers)
- Actual churn or expansion events (no backtesting data yet)
- Segment-specific norms (lighting vs. furniture vs. outdoor may have different baselines)

**Recalibration process:**
1. Run the model across 10–15 accounts spanning all quadrants
2. Compare computed scores against team intuition — flag any accounts where the score feels wrong
3. Identify which thresholds drove the mismatch
4. Adjust thresholds and re-run
5. After 6–12 months of tracking, backtest against actual churn/expansion outcomes to derive empirical thresholds
