# Section 08 Highlights — Platform & Feature Utilization
- **Client**: Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-15
- **Period**: Trailing 12 months (2025-06-15 to 2026-06-15)

## Key Metrics

| Metric | Value | Context |
|--------|-------|---------|
| Total Platform Events | 175,324 | LTM across 76 active users |
| Active Features | 12 of 17 | 5 features at zero usage |
| Visible Products | 3,389 | 95.8% completeness |
| Total Products | 6,130 | Including 2,741 hidden |
| Smart Stacks | 5 (4 published) | No dormant stacks |
| Monthly Import Volume | ~430/mo | Highly active automated pipeline |
| Data Freshness | 8 Fresh / 3 Monitor / 11 Stale | Core data daily; config stale since Aug 2025 |

## Headline Findings

1. **Strong daily data pipeline**: Products, inventory, customers, and all-channel orders refresh daily with ~430 imports/month — operationally mature.
2. **Feature usage dominated by search & ordering**: Product search (46K events) and customer search (46K events) drive the majority of platform activity, followed by order submission (6,565 events).
3. **Options drift risk**: Options and option groups last imported 299 days ago while the product catalog updates daily — the longest-standing configuration gap.
4. **Active smart stack curation**: Seasonal stack (Spring 2026) created in May 2026 alongside evergreen category stacks shows ongoing merchandising effort.
5. **11 stale configuration entities**: All trace to the same Aug 20, 2025 import; no subsequent refresh of options, price levels, taxonomy definitions, or reporting configuration.

## Positive Signals

- Daily automated imports for core data (products, inventory, customers, orders)
- 95.8% catalog completeness for visible products
- 12 of 17 features actively used — broad adoption
- Smart stacks actively managed with recent seasonal additions
- Import pipeline error-free for inventory and customer payment data
- All published smart stacks are active (zero dormant)

## Areas to Watch

- Options/option groups stale 299 days — drift risk if codes have changed
- Price level definitions stale 299 days — verify still aligned with current structure
- Sales quotas not established (0 rows) — not a problem if not desired
- Recurring product import error (tab character in category code, line 3711)
- 5 features at zero adoption: configured item ordering, kits, data exports

## Narrative Posture

Platform is operationally active with healthy daily data pipelines and broad feature adoption. The primary gap is configuration maintenance — options, pricing config, and taxonomy definitions last touched in Aug 2025. This is a maintenance cadence issue, not a platform adoption concern.
