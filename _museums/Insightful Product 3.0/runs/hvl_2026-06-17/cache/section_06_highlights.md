# Section 06 Highlights — Platform Context (hvl, 2026-06-17)

## Candidate Highlights

1. **[POSITIVE] Reps are highly engaged — 18,678 app events across 91 users in 12 months**
   - Despite stale back-end data, the sales team actively uses the app, with Product Search alone driving 7,292 events. Strong adoption foundation to build on. [→ §platform]
   - dollar_figure: n/a (engagement signal)
   - surprise_score: 2.0
   - signal_id: SIG-PLAT-ENGAGE
   - tone: POSITIVE

2. **[RISK] Import pipeline stalled since January 2026 — 14 core data sources frozen at 313 days**
   - Customers, inventory, and price levels were last synced August 2025; every product and account finding in this report is working from ~10-month-old data. [→ §platform]
   - dollar_figure: n/a (operational reliability)
   - surprise_score: 3.5
   - signal_id: SIG-RISK-03
   - tone: RISK

3. **[OPPORTUNITY] SmartPicks viewed only 8 times against 7,292 product searches**
   - Reps do heavy manual catalog browsing the recommendation engine could automate; coaching active searchers on SmartPicks reduces browse time and sharpens in-visit suggestions. [→ §platform]
   - dollar_figure: n/a (coaching upside)
   - surprise_score: 2.5
   - signal_id: SIG-PLAT-SMARTPICKS
   - tone: OPPORTUNITY

## Priority Action Candidates

1. **Restart the import pipeline — re-sync customers, inventory, and price levels** (urgency: HIGH)
   - Core entities (customers, inventory, pricing) are 313 days stale — beyond the 180-day threshold, data staleness at this level undermines every other section. A single import round restores reliability across all 20 stale data sources.
   - signal_id: SIG-RISK-03
