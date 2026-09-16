# Q-CI-05: Top-Performer Patterns (Anonymized)
- **Query ID**: Q-CI-05 (VM-26)
- **Org**: Wildwood/Chelsea House (wwjc, org_id=8)
- **Period**: Current snapshot
- **Row count**: 10 (top performers in Platform-Embedded segment)
- **Run date**: 2026-04-16
- **Source**: BigQuery insightful_product.top_performers_by_segment
- **Note**: Org names shown for internal reference only. External report must anonymize all peer data — never name specific clients.

## Top Performers by Order Volume (Platform-Embedded Segment)

| Rank (Orders) | Rank (Logins) | Org | ARR | Submit Orders | Total Logins | Feature Depth |
|--------------|--------------|-----|-----|--------------|-------------|--------------|
| 1 | 1 | Org A | $30,904 | 39,788 | 34,154 | 8 |
| 2 | 7 | Org B | — | 14,265 | 11,401 | 8 |
| 3 | 8 | Org C | — | 13,628 | 11,366 | 8 |
| 4 | 17 | Org D | $28,249 | 8,377 | 7,782 | 7 |
| 5 | 43 | Org E | — | 7,285 | 3,090 | 4 |
| 6 | 13 | Org F | $35,725 | 6,558 | 8,570 | 6 |
| 7 | 22 | Org G | $4,915 | 6,289 | 6,653 | 6 |
| 8 | 23 | Org G | $25,555 | 6,289 | 6,653 | 6 |
| 9 | 24 | Org G | $4,915 | 6,289 | 6,653 | 6 |
| 10 | 25 | Org G | $25,555 | 6,289 | 6,653 | 6 |

## wwjc Position

| Metric | wwjc | Top Performer | wwjc as % of Top |
|--------|------|--------------|-----------------|
| Submit Orders | 1,758 | 39,788 | 4.4% |
| Total Logins | 9,557 | 34,154 | 28.0% |
| Feature Depth | 5 | 8 | 62.5% |
| ARR | $40,220 | $30,904 | 130.1% |

## Behavioral Patterns of Top Performers

- Top 3 performers all have feature_depth = 8 (maximum observed), vs. wwjc at 5
- Top performer has 39,788 submit_order events — 22.6× wwjc's 1,758
- Top 3 by orders also rank in top 10 by logins — engagement and ordering are correlated
- Note: Org G appears multiple times (likely duplicate rows from pipeline) — deduplicate before analysis
