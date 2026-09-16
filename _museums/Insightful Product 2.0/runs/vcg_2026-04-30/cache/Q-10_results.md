# Q-10: Feature Enablement Gap Analysis — Visual Comfort Signature (vcg, org_id=141)
- **Source**: Postgres MCP (mobile_sites) + org_summary
- **Run date**: 2026-04-30

mobile_sites table returned 0 rows for this org. Feature flags derived from org_summary:

| Feature | Status | Evidence |
|---------|--------|----------|
| Sales Portal | Active (low usage) | access_sales_portal = 229 events |
| Online Catalog | Listed in recurring_services | "eCat Online service" |
| B2B Cart / Online Ordering | Not active | No "B2B Cart" in services; server_order_count = 0 |
| CPQ / Configured Items | Not active | order_configured_item = 0 |
| Kit Items | 0 records | — |
| Contract Prices | 0 records | — |
| Smart Stacks | 4 stacks | Active, all updated today |
| Shared Resources | 9 top-level directories | 8 stale (>90 days) |
| Portal Orders | Present but not LTM-active | Total count exists but 0 in trailing 12 months |
