# Insightful Product — Source Pointer

Do not copy query library files or templates into this folder. Reference source paths below.

## What We Borrow (Read-Only)

| Asset | Path | What It Provides |
|-------|------|-----------------|
| Query library | `Insightful Product/report-system/query_library.md` | MCP SQL for orders, customers, products, channel mix, dormancy |
| External report template | `Insightful Product/report-system/external_report_template.md` | Editorial standards, section structure, framing conventions |
| Editorial standards | `Insightful Product/report-system/editorial_standards.md` | Tone, data labeling, time-qualifier rules |
| Cross-instance benchmarks | BigQuery `supercat-data-pipeline.insightful_product.*` | Peer comparison data (segment_peer_comparison, segment_benchmarks_monthly) |
| Strategy doc | `Insightful Product/strategy/strategy_and_game_plan.md` | Value moment definitions, audience framing |

## Key Queries Needed for Upgrade Briefs

From the query library, the upgrade brief operator will use:

**T1→T2 brief:**
- Customer activation rate (ordering vs. dormant buyer count)
- Dormant buyer GMV math (dormant count × historical AOV)
- iPad order volume and rep load
- Cross-instance benchmark: eOL channel share at comparable catalog size

**T2→T3 brief:**
- Peer benchmark standing (order volume, login percentile, feature depth)
- Revenue leakage analysis (dormant buyers × AOV)
- Rep behavioral scorecard summary
- Portal traffic (if Clicky enabled)
- Cross-instance benchmark: segment classification + percentile position

## What Stays Separate

The upgrade brief templates in `02_briefs/templates/` are **new files** distinct from the Insightful Product templates. They share editorial standards and framing conventions but are structured differently (2-page opportunity brief vs. 10-section comprehensive report). Do not merge them.
