# §8 Platform & Feature Utilization — Highlights

## Key Stats
- 2,297 active products across iPad + Online Catalog channels (online ordering configured but inactive — 0 server orders)
- 12,041 total platform events across 48 active users, 2,411 logins (all-time)
- 14 features actively used; Product Search (2,244) and Customer Search (1,586) dominate
- 2 entities Fresh (customers, inventories — daily imports), 9 Monitor, 11 Stale (all 256 days, Aug 2025)
- 6 smart stacks — all published, all 102 days since update, organized by region (UK/US/EU/AUD)
- Import pipeline: 414 imports over 7 months, 59 avg/month, daily automated cadence active

## Notable Findings
1. **Daily imports keep customers and inventory fresh (0 days)** — this is the strongest data health signal; the daily AM inventory / PM customer cadence is working as designed
2. **Product catalog at 102 days is the most impactful Monitor entity** — categories, collections, groups, trade names, and smart stacks all share this age and will become stale in 78 days without a refresh
3. **11 entities frozen since Aug 2025 (256 days)** — a secondary import pipeline was discontinued; 3 of those entities (contract_prices, kit_items, sales_quotas) contain 0 records and were never populated
4. **Online ordering is configured but has 0 server orders** — all 19 lifetime orders came through iPad; the B2B channel exists but has never been activated by buyers
5. **Browse-to-transact drop-off** — thousands of search/browse events vs. 66 all-time order submissions; only 3 of 81 users (3.7%) have ordered in the last 90 days
6. **Recurring import issues** — inventory imports warn on "product not found" (catalog mismatch); customer imports error on missing shipping address fields (records silently skipped)
7. **Regional smart stack structure** — 4 of 6 stacks serve as region-filtered catalog views (UK/US/EU/AUD), well-suited for an international sales operation

## Subsections Rendered
1. Catalog Health (always visible)
2. Feature Usage Intensity (always visible)
3. Data Health Report (always visible)
4. Data Pipeline Health (collapsed)
5. Platform Configuration Alerts (collapsed)
6. Smart Stack Performance (collapsed)

## Decisions
- `portal_orders` labeled as "All-Channel Orders" per semantic guardrail
- Online ordering NOT flagged as a gap — it is configured, just inactive (0 server orders)
- Sales Portal correctly shown as "Not in Bundle" (enable_sales_portal=false)
- Zero-usage features (CSV/Excel export, camera scan, flipbook) mentioned as adoption opportunities, not gaps
- CPQ features not flagged as gaps per instruction
- Feature intensity tiers: High (≥1,000 events), Moderate (500–999), Low (<500) — adjusted for this org's volume
- Data freshness uses strict 3-label system: Fresh (≤30 days), Monitor (31–180 days), Stale (>180 days)
- `USER_GROUP_SPLIT_AVAILABLE = false` — platform activity composition skipped
- `MIXPANEL_ORDER_TRACKING_GAP = N/A` — not applicable
- `HAS_CART = false` — online ordering referenced but not treated as active channel
- No prohibited terms used: no ERP, Mixpanel, Clicky, or health score in delivered HTML
- No HTML comments or [HYPOTHETICAL] tags in fragment
