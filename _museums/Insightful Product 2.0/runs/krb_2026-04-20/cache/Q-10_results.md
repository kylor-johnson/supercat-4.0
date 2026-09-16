# Q-10: Feature Enablement Gap Analysis
- **Org**: Kaleen Rugs & Broadloom (krb, org_id=244)
- **Period**: Current snapshot
- **Rows returned**: 0
- **Run date**: 2026-04-20

No mobile_sites row exists for org_id 244. Feature enablement flags (enable_sales_portal, enable_online_catalog, enable_online_ordering) cannot be derived from this table.

Supplemental context from org_summary (BigQuery):
- recurring_services: "eCat (iPad) Service"
- feature_depth: 2
- Bundle: iPad-only

| feature | status |
|---------|--------|
| iPad App | Active (bundle includes) |
| Online Catalog | Not in bundle |
| B2B Cart (Online Ordering) | Not in bundle |
| Sales Portal | Not in bundle |
| CPQ | Not in bundle |
| Kit items | 830 records (stale — 255 days) |
| Contract prices | 0 records |
| Smart Stacks | 1 |
| Shared resources (Library) | 57 |
| Portal orders | 0 |
