# Section 06 Build Plan — Platform Context

**Client:** Bulbrite (bri, org_id=222) · **Run date:** 2026-06-17
**Render mode:** Collapsed `<details class="section-collapse" id="platform">`
**Confidence header:** NONE — §6 (Platform Context) does not use a data confidence header (per shared contract §2).
**Section-level what-this-means:** NONE — not required for Platform Context (each subsection closes its own).

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY (when any data) | MET — Q-08, Q-09, Q-10, Q-22 all present | YES |
| Action Required | CONDITIONAL | MET — 8 entities >90d stale (matrix_options/option_groups/options/riser_prices/sales_quotas/etc. at 300d; price_levels at 82d > 30d override) | YES |
| Feature Utilization | CONDITIONAL | MET — Q-22 has 17 tracked features, 14 active | YES |
| Catalog Remediation | CONDITIONAL | NOT MET — Q-07 not present in bundle; cannot evaluate completeness | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED — peer data unreliable | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED — peer data unreliable | NO |
| Import Pipeline | CONDITIONAL | MET — cadence notably irregular (7,669 in Apr 2026 vs ~150/mo baseline) | YES |

## Rendered subsections (in guide order)
1. Platform Health Status — `.metrics-grid` (4 cards: Import Pipeline, Data Freshness, Feature Adoption, Smart Stacks) + prose + what-this-means
2. Action Required — `.callout.alert` + stale-entity table (thead/tbody, row-warn/row-danger) + what-this-means
3. Feature Utilization — `.callout.insight` + feature table + `.callout.opportunity` (SmartPicks) + what-this-means
4. Import Pipeline — month/imports table + what-this-means

## Notes
- MIXPANEL_ORDER_TRACKING_GAP = False → keep "Order Submission" in Feature Utilization table.
- Core entities (products, inventory, customers) are all Fresh (0d) → NOT priority-action-worthy. 0 priority actions in highlights.
- Stale entities are config tables (options, riser prices, sales quotas) at 300d → eligible for 1 highlight (>180d) but not a top-level priority action.
- No confidence header, no section-level what-this-means, no peer benchmark references.
- `section-contents` middot list = only the 4 rendered subsections.
