# Q-47: Smart Stack Effectiveness — Buster & Punch (bp, org_id=250)
- **Query**: Q-47 (VM-47) — Postgres metadata only
- **Period**: Current snapshot
- **Run date**: 2026-04-21
- **Rows returned**: 6

| stack_id | stack_name | published | is_dormant | created_at | updated_at | days_since_update |
|----------|-----------|-----------|------------|------------|------------|------------------|
| 10006 | UK Products | true | false | 2025-04-25 | 2026-01-08 | 102 |
| 9676 | Qty Available | true | false | 2025-02-13 | 2026-01-08 | 102 |
| 10276 | Grohe Spa | true | false | 2025-09-18 | 2026-01-08 | 102 |
| 9855 | AUD Products | true | false | 2025-03-10 | 2026-01-08 | 102 |
| 9856 | US Products | true | false | 2025-03-10 | 2026-01-08 | 102 |
| 10273 | EU Products | true | — | 2025-09-18 | 2026-01-08 | 102 |

**Notes**:
- 6 Smart Stacks, all published
- All last updated 2026-01-08 (102 days ago) — likely a batch product sync updated timestamps
- Stack names suggest regional product segmentation (US, UK, EU, AUD) plus one functional (Qty Available) and one brand (Grohe Spa)
- No stale stacks (>90 days) by the strict definition, though all are 102 days since last update
- Per-stack Mixpanel view data not available (pending_query)
