# Section 06 Build Plan — Platform Context

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08/Q-09/Q-07/Q-22 all present) | YES |
| Action Required | CONDITIONAL | MET (Q-08 shows 10 entities at 301d stale; Q-11 config drift) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has data, >3 distinct features tracked; MIXPANEL_ORDER_TRACKING_GAP=False so submit_order retained) | YES |
| Catalog Remediation | CONDITIONAL | MET (Q-07 completeness=56.30% < 95%) | YES |
| Feature Adoption vs Peers | — | PERMANENTLY EXCLUDED | NO |
| Peer Benchmarking Summary | — | PERMANENTLY EXCLUDED | NO |
| Import Pipeline | CONDITIONAL | NOT MET (Q-09 avg ~86/mo, consistent, no stalled/zero month — no story) | NO |

## Notes
- §6 uses NO confidence header (per shared contract §2).
- §6 renders as collapsed `<details>`.
- No section-level what-this-means (per guide).
- Catalog: missing_price=356 is price-level pricing configuration (Q-10 contract_price_count=0, price_levels entity present), not a true gap. Only 2 items missing images is the real remediation item. Frame accordingly.
- Health badge computations:
  - Core Pipeline: avg (38+62+110+66+98+148+81)/7 ≈ 86/mo → ok "Healthy"
  - Data Freshness: 10 entities >90d → danger
  - Catalog: 56.30% → danger (but price-level config caveat in note)
  - Feature Adoption: many active features (>5) → ok
  - Smart Stacks: 4 published → ok
- Forbidden terms: no ERP/Mixpanel/Clicky/portal orders/standalone "platform"/peer benchmark references. Entity names humanized.
