# Section 06 Highlights — Platform Context (Savoy House Lighting, shl)
- Run date: 2026-06-17

## Candidate Highlights

1. **Pricing configuration is 301 days stale** — Price levels, contract prices, options, and sales quotas haven't been refreshed since Aug 20, 2025, so reps may quote outdated terms on the iPad. A single re-import clears it. `surprise_score: 3.0` `signal_id: SIG-PLATFORM-STALE` `[→ §platform]`

2. **[POSITIVE] Platform foundation is healthy** — Import pipeline runs at ~126/month, catalog is 98.9% complete across 4,984 products, and 10 of 11 tracked features are in active use. `surprise_score: 1.5` `signal_id: SIG-PLATFORM-HEALTH` `[→ §platform]`

3. **SmartPicks adoption gap** — Reps run 40,000+ product searches a year but open SmartPicks only 92 times; activating personalized recommendations would cut browsing time during presentations. `surprise_score: 4.0` `signal_id: SIG-PLATFORM-FEATURE` `[→ §platform]`

## Priority Action Candidates

None. Core entities (products, inventory, customers) are all fresh (≤7 days); the 301-day staleness is limited to configuration tables, which is fixable but not top-level priority-action-worthy per the §6 guide threshold (>180d on core entities only).
