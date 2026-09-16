# Section 06 Highlights — Platform Context

## Highlight Candidates

1. **Configuration catalog frozen since August 2025** — 11 data sources (options, kits, contract prices, quotas, customer favorites) all stuck at 313 days stale from a single import that never repeated; configurable products and contract-priced accounts may show outdated choices and pricing. `surprise_score: 3.5` · `signal_id: SIG-RISK-03` · `[→ §platform]`

2. **Reps lean hard on Product Search — 31,742 uses in 12 months** *(positive / intelligence)* — Product Search alone drives nearly 40% of all app activity, anchoring a healthy 12-of-17 active feature mix and a current product/inventory/Smart Stack feed. `surprise_score: 1.2` · `signal_id: SIG-FEATURE-USE` · `[→ §platform]`

3. **SmartPicks effectively unused — 9 opens vs 31,742 product searches** *(opportunity)* — Reps hand-search for items the app could surface automatically from each customer's purchase history; activating SmartPicks with top searchers would cut browsing time in presentations. `surprise_score: 1.4` · `signal_id: SIG-FEATURE-GAP` · `[→ §platform]`

## Priority Action Candidates
- **One re-import clears the entire Critical staleness cluster** — urgency: MEDIUM. The 11 sources at 313 days share a single stale August 2025 import; a single re-import session (starting with contract prices and options) restores configurable-product and contract-pricing accuracy. Borderline priority-worthy because the affected tables sit behind a current, actively-used catalog rather than the live product feed itself.
