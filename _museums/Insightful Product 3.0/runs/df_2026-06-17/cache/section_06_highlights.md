# Section 06 Highlights — Platform Context (Designer's Fountain, df)
- **Run date**: 2026-06-17

## Candidate Highlights

1. **12 pricing and configuration data sources are frozen at 313 days old**
   Price levels, contract prices, options, and quotas haven't refreshed since Aug 7, 2025 — quotes and configured products throughout the report may be nearly a year out of date. A single FTP re-import clears it. `[→ §platform]`
   surprise_score: 3.5 | signal_id: SIG-RISK-03 | dollar_impact: n/a (operational)

2. **Your team is actively using the app — 11 features in regular rotation across 46 users**
   Product search alone fired 2,741 times in the trailing 12 months, the dominant feature at ~28% of all activity. Adoption is a strength, not a gap. `[→ §platform]`
   surprise_score: 2.1 | signal_id: SIG-FEATURE-USE | tone: POSITIVE

3. **SmartPicks used twice all year against 2,741 product searches**
   Reps browse manually instead of using personalized, history-based recommendations — a coaching opportunity with no cost to enable. `[→ §platform]`
   surprise_score: 2.4 | signal_id: SIG-RISK-03 | tone: OPPORTUNITY

## Priority Action Candidates

- **Re-import pricing and product-option files** — urgency: HIGH. 12 core data sources sit at 313 days stale (>180d threshold), undermining pricing and configuration accuracy across every section. One import round resolves it.
