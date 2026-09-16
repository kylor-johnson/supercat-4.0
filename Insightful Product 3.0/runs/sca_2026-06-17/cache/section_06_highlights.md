# Section 06 Highlights — Platform Context (Shadow Catchers, sca)
- **Run date**: 2026-06-17

## Candidate Highlights

1. **Inventory and pricing data are over 10 months stale** — 18 data sources, including inventory, price levels, and contract prices, have not refreshed since August 2025 (313 days), so every stock and price figure reps quote is from last summer. `surprise_score: 3.5` · `signal_id: SIG-RISK-03` · `[→ §platform]`
   - Priority action candidate: **urgency HIGH** — core entities (inventory, pricing, customers) are >180 days stale, which undermines the reorder-decay and revenue-concentration findings in every other section. A single import round fixes it.

2. **(Positive) Reps are actively using the app — 12,484 product searches in the trailing year** — product search alone accounts for 50.8% of all 24,591 tracked events, confirming the team relies on eCat daily despite the stale data feed. `surprise_score: 2.0` · `signal_id: SIG-RISK-03` · `[→ §platform]`

3. **SmartPicks ran 3 times against 12,484 manual searches** — reps are doing the recommendation engine's work by hand; activating SmartPicks with top searchers is a low-cost coaching win. `surprise_score: 2.5` · `signal_id: SIG-RISK-03` · `[→ §platform]`
