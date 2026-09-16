# Section 06 Build Plan — Platform Context

Confidence tier: §6 does NOT use a data-confidence header (per shared contract §2).
Render mode: collapsed `<details class="section-collapse" id="platform">`.

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| Platform Health Status | MANDATORY | MET (Q-08, Q-09, Q-22, Q-10 all have data) | YES |
| Action Required (Operational Alerts) | CONDITIONAL | MET (12 entities stale 313d / Critical) | YES |
| Feature Utilization | CONDITIONAL | MET (Q-22 has 13+ tracked features with events) | YES |
| Catalog Remediation | CONDITIONAL | NOT MET (Q-07 not present in bundle — no catalog completeness data) | NO |
| Feature Adoption vs Peers | EXCLUDED | Permanently excluded | NO |
| Peer Benchmarking Summary | EXCLUDED | Permanently excluded | NO |
| Import Pipeline Detail | CONDITIONAL | NOT MET (avg 30/mo, consistent 31–45 range, recent month 23 — not stalled, not notably irregular) | NO |

## Health dashboard badge computation
- Core Pipeline: Q-09 avg = (23+32+45+31+33+32+14)/7 = 30/mo → `badge warn` "Low Volume" (<50/mo, recent month not 0).
- Data Freshness: 12 entities >90d stale (all 313d) → `badge danger` (>3 Stale).
- Catalog: Q-07 not present → card OMITTED (no data).
- Feature Adoption: Q-22 has 13 features with >0 events → `badge ok` "Active" (≥5 active).
- Smart Stacks: Q-10 smart_stack_count=58 → `badge ok` "58 published".

## Feature Utilization %
Denominator = sum of tracked feature events = 36,594 (LTM).
search_products 30,897 = 84.4% (Heavy). create_pdf_catalog 1,153 = 3.2% (Moderate).
view_library_entry 1,108 = 3.0% (Moderate). filter_products 1,121 = 3.1% (Moderate).
select_a_customer 854 = 2.3% (Moderate). search_for_customer 825 = 2.3% (Moderate).
search_collections 334 = 0.9% (Light). email_item_info 130 = 0.4% (Light).
submit_order 86 = 0.2% (kept; MIXPANEL_ORDER_TRACKING_GAP=False). view_smartpicks 3 = <0.1% (Light) → coaching opportunity.
Suppressed: access_sales_portal (Clicky-related term, 0 events); zero-only order_configured_item/view_kit/order_kit.

## Highlights
1–2 RISK highlights (12 entities >180d stale = priority-action-worthy per guide §Highlight). 1 positive (SmartPicks coaching opportunity).
