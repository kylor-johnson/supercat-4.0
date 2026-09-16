# Section 06 Highlights — Platform Context (DALS Lighting)
- Run date: 2026-06-17

## Candidate Highlights

1. **Strong daily app adoption — 35 users, 7,539 actions in 12 months** (POSITIVE/MOMENTUM)
   Context: 10 of 11 tracked features are in active use, led by 3,193 product searches; the team's engagement is real and consistent. [→ §platform]
   - Dollar figure: n/a (engagement signal)
   - surprise_score: 2.0
   - signal_id: SIG-FEATURE-USAGE
   - tone: POSITIVE

2. **Import pipeline stalled — only 1 import in 12 months, none since February** (RISK)
   Context: The feed that updates the app has effectively stopped, freezing 18 data sources and leaving customer, pricing, and inventory data up to 313 days old. [→ §platform]
   - Dollar figure: n/a (operational)
   - surprise_score: 3.5
   - signal_id: SIG-RISK-03
   - tone: RISK

3. **Customer & pricing data 313 days stale; inventory 244 days stale** (RISK)
   Context: Reps may be quoting 10-month-old prices and stock — every customer-, pricing-, and availability-related finding in this report rests on data that predates the last 10 months. [→ §platform]
   - Dollar figure: n/a (data integrity)
   - surprise_score: 3.5
   - signal_id: SIG-RISK-03
   - tone: RISK

## Priority Action Candidate

- **Restart the FTP import job to refresh Customer Master, Price Levels, and Inventory** — urgency: HIGH.
  Core entities are >180 days stale (customers/pricing 313d, inventory 244d), which undermines every other section of this report. A single import cycle clears all 18 freshness alerts.
