# Q-11 — Configuration Completeness
- **Query**: Q-11 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `data_versions` (>30d stale) | **Run date**: 2026-06-12
- **Row count**: 11

| entity_type | last_updated | days_stale | related_record_count |
|---|---|---|---|
| sales_quotas | 2025-08-20 | 296 | 0 |
| customer_payment_informations | 2025-08-20 | 296 | — |
| riser_prices | 2025-08-20 | 296 | — |
| commitment_reports | 2025-08-20 | 296 | — |
| kit_items | 2025-08-20 | 296 | 0 |
| contract_prices | 2025-08-20 | 296 | 0 |
| matrix_options | 2025-08-20 | 296 | — |
| option_groups | 2025-08-20 | 296 | — |
| options | 2025-08-20 | 296 | — |
| price_levels | 2025-11-10 | 214 | — |
| placement_reports | 2026-05-05 | 38 | — |

**Note**: Stale config entities all carry 0 related records (kit_items, contract_prices, sales_quotas) — unused features, not data-quality gaps. Core commerce entities are Fresh (excluded by the >30d filter).
