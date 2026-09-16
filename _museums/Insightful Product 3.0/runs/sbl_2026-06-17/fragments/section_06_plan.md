# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-22 all have data) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (Q-08: 10 entities at 313d Critical; products 57d > 30d override = Stale) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 11 distinct active features, ≥3 tracked) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 cadence is consistent 18–91/mo, no stall, recent month=18 ≠ 0) | NO |

## Gate computation notes

- **Core Pipeline badge**: avg monthly imports ≈ 42/mo (18+33+45+38+30+91+42)/7 → <50 = `.badge.warn` "Low Volume". Recent month (June) = 18, not 0 and not <10, so not Stalled.
- **Data Freshness badge**: >3 Stale entities (10 at 313d Critical, plus products at 57d via 30d product override) → `.badge.danger`.
- **Feature Adoption badge**: 11 features with >0 events (≥5) → `.badge.ok` "Healthy".
- **Catalog badge**: Q-07 not present → omit Catalog card (no completeness data to assess).
- **Smart Stacks card**: Q-10 returned 0 rows but Q-08 shows smart_stacks entity has a sync timestamp (configured). Ambiguous; omit card to keep 4 clean indicators rather than show a misleading "Not configured".
- **Operational Alerts**: render only entities that are Stale per labels. Monitor-band entities (price_levels 145d, portal_orders/invoices 96d, products family 57d at general threshold) are NOT rendered EXCEPT products, which is Stale via the 30d product-specific override. Grouped 313d entities into logical rows.
- **MIXPANEL_ORDER_TRACKING_GAP = False** → no Order Submission suppression needed; submit_order shown as a normal feature.
- **Confidence header**: §6 does NOT use a confidence header (per shared contract).
- **Section-level what-this-means**: NOT required for §6.
- Peer benchmark cache files (Q-CI-02/03/05, peer_benchmark_extract) NOT used.
