# Section 06 Build Plan — Platform Context

**Section:** 6 · id=`platform` · title "Platform Context"
**Confidence:** §6 does NOT use a confidence header (per shared contract).
**Wrapper:** collapsed `<details class="section-collapse" id="platform">`.

## Gate Check

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status Dashboard | MANDATORY | MET (Q-08, Q-09, Q-22 all present) | YES |
| Operational Alerts | CONDITIONAL | MET (10 config entities >90d stale per Q-08; options/option_groups/matrix_options 301d) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 12 active features of 17 tracked) | YES |
| Catalog Operational Recommendations | CONDITIONAL | NOT MET (Q-07 not present in cache — completeness not computable) | NO |
| Feature Adoption vs Peers | EXCLUDED | PERMANENTLY EXCLUDED (peer data unreliable) | NO |
| Peer Benchmarking Summary | EXCLUDED | PERMANENTLY EXCLUDED (peer data unreliable) | NO |
| Import Pipeline Detail | CONDITIONAL | NOT MET (Q-09 consistent 25–57/mo, no zero months, not stalled) | NO |

## Render Notes

- **Confidence header:** none (§6 exempt).
- **Section-level what-this-means:** none (§6 exempt; each subsection closes its own).
- **MIXPANEL_ORDER_TRACKING_GAP = False** → keep "Order Submission" in Feature Utilization table; do NOT remove it.
- **Health dashboard cards (4):** Core Pipeline (warn — ~38 imports/mo LTM avg), Data Freshness (danger — 10 stale config sources), Feature Adoption (ok — 12 active), Smart Stacks (ok — 20 published). Catalog card omitted (Q-07 absent).
- **Operational Alerts** surfaces only the genuinely in-use stale config: Options & Option Groups, Matrix Option Pricing (both 301d, Critical/danger). Entities with 0 related records (contract_prices, kit_items, sales_quotas, commitment_reports) are NOT surfaced — not in use.
- **% of activity** denominator = sum of tracked feature events (40,816 LTM).
- **[COLLAPSE]** applied to Feature Utilization table via inner `<details>`.
- **Freshness labels:** only Stale (91–180d, warn) / Critical (181+, danger) rendered; Fresh/Monitor entities suppressed.
