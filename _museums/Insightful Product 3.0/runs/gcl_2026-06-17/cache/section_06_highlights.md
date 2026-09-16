# Section 06 Highlights — Geo Contemporary (gcl)
- Run date: 2026-06-17
- Section: §6 Platform Context

## Candidate Highlights

1. **10 operational data sources have gone stale — inventory, contract pricing, and customer favorites are 313 days old**
   Context: Inventory, contract prices, favorites, quotas, and seven other sources last refreshed Aug 7, 2025; every stock and pricing finding downstream is working from year-old data. Dollar impact: n/a (operational, no GMV attribution). surprise_score: 3.5 · signal_id: SIG-RISK-03 · [→ §platform]

2. **A single coordinated import would restore reliability across the whole report**
   Context: The import pipeline is active (~13 files/month) and the catalog itself is fresh (13 days) — the stale sources are an easy fix, not a broken pipeline. surprise_score: 2.0 · signal_id: SIG-RISK-03 · [→ §platform]  *(POSITIVE framing — fixable, system is live)*

3. **Reps actively use 14 of 17 tracked app features — strong, broad adoption**
   Context: Product Search (2,445 events) and configured-item ordering (1,553) lead a healthy usage profile across the team in the last 12 months. surprise_score: 1.4 · signal_id: SIG-FEATURE-USE · [→ §platform]  *(POSITIVE)*

## Priority Action Candidates
- 1 candidate (MEDIUM urgency): Re-import the nine 281–313 day operational sources (inventory, contract prices, favorites, options, quotas). Core entities are >180 days stale, which the guide flags as priority-worthy. Not P0 — catalog and customers remain fresh, so the report's core findings still hold.
