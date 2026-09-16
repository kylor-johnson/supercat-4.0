# §8 Platform & Feature Utilization — Highlights

## Key Stats
- 7,641 total products (6,202 visible, 96.7% complete)
- 29 of 35 features actively used (83% adoption rate)
- 118,286 total feature events across 70 active users, 11,142 logins (all-time)
- 11 entities Fresh, 3 Monitor, 8 Stale (all 8 stale since Aug 7, 2025)
- 14 smart stacks — all published, zero dormant, all updated today
- Import pipeline: 936 imports over 7 months, 134 avg/month, no gaps

## Notable Findings
1. **Product Search** (37,097 events) and **Library Browsing** (15,717) dominate feature usage by a wide margin
2. 8 data entities share the exact same stale date (Aug 7, 2025) — indicates a secondary import pipeline was discontinued
3. Inventory, options, and riser prices are drifting from daily-updated products and pricing — highest-priority restoration targets
4. Sales Quotas entity is enabled but contains 0 records — non-functional
5. Smart stack management is exemplary: 14/14 published, 0 dormant, all updated today
6. All-Channel Orders and Invoices are in Monitor status (38 days) — not yet stale but watch-listed
7. Selling workflow shows depth: 7,055 customer targeting → 38,242 product discovery → 2,941 presentation events; 56 iPad orders submitted in the last 90 days

## Subsections Rendered
1. Catalog Health (always visible)
2. Feature Usage Intensity (always visible)
3. Data Health Report (always visible)
4. Data Pipeline Health (collapsed)
5. Platform Configuration Alerts (collapsed)
6. Smart Stack Performance (collapsed)

## Decisions
- `portal_orders` labeled as "All-Channel Orders" per semantic guardrail
- 6 zero-usage features acknowledged but NOT flagged as gaps — 2 are outside iPad-only bundle scope (Sales Portal, configured item ordering), 4 are adoption opportunities (camera scanning, flipbook, list creation)
- Feature intensity tiers: High (≥5,000 events), Moderate (500–4,999), Low (<500)
- Data freshness uses strict 3-label system: Fresh (≤30 days), Monitor (31–180 days), Stale (>180 days)
- Configuration alerts use Drift / Stale / Not Established badges per Q-11 specification
- `MIXPANEL_ORDER_TRACKING_GAP = false` — submit_order events included normally
- `HAS_CART = false` — no cart-related features referenced
- No prohibited terms used: no ERP, Mixpanel, Clicky, or health score in delivered HTML
- Q-50 library data (19 directories, 17 stale >90 days) folded into Catalog Health prose and Feature Usage context
- Q-46 selling workflow maturity data integrated into Feature Usage narrative
