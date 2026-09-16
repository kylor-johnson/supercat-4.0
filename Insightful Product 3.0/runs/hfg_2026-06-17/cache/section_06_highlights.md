# Section 06 Highlights — Platform Context

## Candidate Highlights

1. **9 core data sources are 300 days stale, including inventory and pricing** — Inventory, price levels, and contract prices were last refreshed Aug 20, 2025, so every stock-availability and pricing finding downstream is working from 10-month-old data. A single import round restores reliability. `surprise_score: 2.0` · `signal_id: SIG-PLATFORM-STALE` · [→ §platform]

2. **[POSITIVE] 15 of 15 tracked app features show active usage** — Customer Search (38,554 events LTM), Product Search (31,631), and Catalog Browsing (31,094) lead a broadly-adopted toolset, with 7 Smart Stacks published and guiding reps. `surprise_score: 1.5` · `signal_id: SIG-PLATFORM-ADOPT` · [→ §platform]

3. **SmartPicks adoption gap: 226 uses vs 31,600+ product searches** — Reps browse manually instead of using the recommendation engine that surfaces products from each customer's purchase history; activating it for top searchers is low-effort upside. `surprise_score: 1.8` · `signal_id: SIG-PLATFORM-SMARTPICKS` · [→ §platform]

## Priority Action Candidates

- **[HIGH urgency] Refresh 9 stale reference data sources (inventory, pricing, quotas)** — At 300 days stale (>180d threshold), this undermines product and commerce intelligence across the report; a single import round fixes it. `signal_id: SIG-PLATFORM-STALE` · [→ §platform]
