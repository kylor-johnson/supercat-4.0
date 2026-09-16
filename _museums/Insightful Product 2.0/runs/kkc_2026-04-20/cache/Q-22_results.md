# Q-22: Feature Usage Depth — Kindel Furniture (kkc, org_id=99)
- **Maps to**: VM-22
- **Source**: BigQuery (`user-bigquery-vpn`) — `mixpanel.org_feature_usage_report`
- **Run date**: 2026-04-20
- **Period**: All-time cumulative
- **Rows**: 1

## Results

| Feature | Event Count (All-Time) |
|---------|----------------------|
| Product Search | 607 |
| Product Filter | 15 |
| Library / Document Viewing | 834 |
| PDF Catalog Creation | 251 |
| Email Item Info | 22 |
| Email Library Entry (single) | 12 |
| Email Library Entry (multiple) | 17 |
| Customer Selection | 10 |
| Customer Search | 31 |
| View My List | 120 |
| Edit My List | 7 |
| Search Collections | 19 |
| Configured Item Ordering (CPQ) | 20 |
| View iPad Orders | 2 |
| Order Submission | 0 |
| Smart Picks (Smart Stacks) Viewed | 0 |
| Sales Portal Access | 0 |
| View Customer Favorites | 0 |
| Create My List | 0 |
| View Kit | 0 |
| Order Kit | 0 |
| Export to CSV | 0 |
| Export to Excel | 0 |
| Share My List | 1 |

## Summary Stats

| Metric | Value |
|--------|-------|
| Total users (all-time) | 42 |
| Total events (all-time) | 4,554 |

**Feature intensity notes** (for Stage 2 use):
- **High activity**: Library/Document Viewing (834), Product Search (607), PDF Catalog Creation (251), View My List (120)
- **Medium activity**: Email/Library sharing (51 combined), Customer Search (31), Search Collections (19), CPQ usage (20)
- **Zero activity**: Order Submission, Sales Portal Access, Smart Picks, View Kit, Order Kit, Export features
- CPQ (Configured Item Ordering) shows 20 all-time events despite 0 order submissions — users engaged with configuration workflow but did not submit
- The platform is used primarily as a presentation and content library tool, not as an order capture channel
