# Q-22: Feature Usage Depth — Kindel Karges Furniture (kkc, org_id=99)
- **Query ID**: Q-22
- **VM**: VM-22
- **Run date**: 2026-04-23
- **Period**: All-time cumulative (Mixpanel)
- **Rows returned**: 1
- **Source**: BigQuery mixpanel.org_feature_usage_report

| Feature | Event Count (All-Time) |
|---------|----------------------|
| Total Events | 4,601 |
| Total Users | 42 |
| Active Users | 24 |
| Total Logins | 1,266 |
| View Library Entry | 846 |
| Search Products | 609 |
| Create PDF Catalog | 253 |
| View My List | 120 |
| PDF Searches | 115 |
| Search for Customer | 31 |
| Order Configured Item | 20 |
| Search Collections | 19 |
| Email Multiple Library Entries | 17 |
| Filter Products | 15 |
| Change Catalog Sort | 12 |
| Email Single Library Entry | 12 |
| Select a Customer | 10 |
| Edit My List | 7 |
| Email Item Info | 22 |
| View iPad Orders | 2 |
| Share My List | 1 |
| Submit Order | 0 |
| Access Sales Portal | 0 |
| View Kit | 0 |
| Order Kit | 0 |
| Export Data to CSV | 0 |
| Export Data to Excel | 0 |
| Scan Item with Camera | 0 |
| View Customer Favorites | 0 |
| Show Sales in Catalog | 0 |
| View Smart Picks | 0 |
| Create My List | 0 |
| Create Customer Product List | 0 |
| View Customer Product List | 0 |
| Create Maybe List | 0 |
| Order from Maybe List | 0 |
| View Placements | 0 |
| View Commitments | 0 |
| View Flipbook | 0 |
| Add to List from Flipbook | 0 |
| Order from Flipbook | 0 |

**MIXPANEL_ORDER_TRACKING_GAP applied**: Submit Order shows 0 in Mixpanel but Postgres records 41 all-time eCat orders. Mixpanel is not tracking iPad order submissions for this org. The Order Submission row should be removed from external display per Mode 3 gap handling rules.

**Top activity clusters**:
1. **Library/Content** (846 views + 29 email shares) — dominant usage pattern
2. **Product Discovery** (609 searches + 15 filters + 19 collection searches)
3. **Presentation** (253 PDF catalogs + 22 email item info + 1 share my list)
4. **Configuration** (20 configured item events)
5. **Customer Targeting** (31 customer searches + 10 customer selections)
