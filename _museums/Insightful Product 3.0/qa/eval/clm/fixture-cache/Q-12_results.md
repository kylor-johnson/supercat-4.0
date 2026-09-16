# Q-12 — Customer Activation & ERP Penetration
- **Query**: Q-12 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres | **Run date**: 2026-06-12
- **Row count**: 1

| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
|---|---|---|---|---|
| 4,812 | 611 | 115 | 91 | 18 |

**Derived metrics**:
- `lapsed_ecat` = 611 − 115 = **496** (ordered via eCat before, not in last 12 months)
- `never_activated` = 4,812 − 611 = **4,201** (ERP records with no eCat history)
- `ecat_retention_rate` = 115 / 611 = **18.8%** (primary metric — active 12mo of all-time eCat buyers)

**Framing**: ecat_retention_rate is primary. ERP total (4,812) is secondary context only — never frame as "X% dormant."
