# Section 06 Highlights — Platform Context (Currey & Company)
- Run date: 2026-06-17

## Candidate Highlights

1. **[POSITIVE] Platform core data is fully fresh and feature adoption is broad.**
   Products, inventory, customers, and orders all refresh daily, with 10+ features in active use across 76 users LTM — the account and product intelligence in this report runs on current data.
   - Dollar figure: n/a (operational reliability)
   - surprise_score: 1.0
   - signal_id: SIG-PLATFORM-HEALTH
   - [→ §platform]

2. **[RISK] 11 pricing & configuration entities haven't synced in 301 days.**
   Price levels, contract prices, options, and collections last updated Aug 20, 2025 — reps may quote outdated pricing and miss 2026 finishes/collections at order entry. Isolated to config data; a single re-import closes it.
   - Dollar figure: n/a (pricing-accuracy risk)
   - surprise_score: 2.5
   - signal_id: SIG-STALE-CONFIG
   - [→ §platform]

## Priority Action Candidates
- 0 priority actions. Staleness is 301 days but confined to pricing/configuration entities, not core products/inventory/customers (all fresh). Not severe enough for the top-level priority list; surfaced as an in-section Action Required table instead.
