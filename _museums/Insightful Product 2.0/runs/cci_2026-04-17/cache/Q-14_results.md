# Q-14: Customer Reorder Frequency & Velocity
- **Org**: Currey & Company (cci), org_id=161
- **Period**: LTM (trailing 12 months), customers with ≥3 orders
- **Source**: Postgres MCP (orders)
- **Row count**: 20
- **Run date**: 2026-04-17

| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
|-------------|---------------------|-----------------|----------|-----------------|----------------|----------------------------|
| BAER 2 | BAER'S FURNITURE COMPANY | 147 | $275,016.24 | 2025-06-02 | 2026-02-27 | 1.8 |
| CLIVE D | CLIVE DANIEL HOME | 60 | $96,431.00 | 2025-05-01 | 2026-04-17 | 5.9 |
| RS INTL | ROBB & STUCKY INTERNATIONAL | 48 | $93,836.40 | 2025-04-24 | 2026-04-09 | 7.5 |
| LIBUMC | LIGHTING IN STYLE | 47 | $38,916.00 | 2025-04-21 | 2026-03-31 | 7.5 |
| 0003564 | TRIBUS DESIGN STUDIO | 43 | $100,198.20 | 2025-04-22 | 2026-04-15 | 8.5 |
| AWELL | A WELL DRESSED HOME | 42 | $57,275.60 | 2025-04-28 | 2026-04-15 | 8.6 |
| VITOCH | VITOCH INTERIORS | 34 | $32,814.00 | 2025-04-22 | 2026-04-03 | 10.5 |
| ST LGT | METRO LIGHTING, ST LOUIS | 31 | $34,504.20 | 2025-04-21 | 2026-04-16 | 12.0 |
| DEC UNL | THE DECORATORS UNLIMITED | 29 | $48,946.60 | 2025-05-03 | 2026-03-31 | 11.9 |
| NTDTX | NORTH TEXAS DESIGN GROUP | 28 | $40,392.00 | 2025-05-01 | 2026-04-17 | 13.0 |
| LYTE | LYTEWORKS | 28 | $38,184.00 | 2025-04-24 | 2026-03-10 | 11.9 |
| FORD | VERVE INTERIORS LTD | 26 | $33,344.00 | 2025-04-18 | 2026-03-13 | 13.2 |
| MEDER | BLACK SHEEP INTERIORS | 24 | $29,544.16 | 2025-06-02 | 2026-04-17 | 13.9 |
| KCID | KELLY CARON DESIGNS | 24 | $28,412.98 | 2025-04-18 | 2026-03-12 | 14.3 |
| 0003330 | BUNNY WILLIAMS HOME | 24 | $36,168.00 | 2025-05-21 | 2026-04-13 | 14.2 |
| DWS | DESIGN WORKS STUDIO, INC. NC | 22 | $20,377.60 | 2025-07-02 | 2026-03-31 | 12.9 |
| 0014980 | NAPLES LIGHTING & FAN DEPOT | 21 | $18,500.00 | 2025-04-24 | 2026-03-30 | 17.0 |
| CHD 3 | CUSTOM HOME DECORATING | 20 | $18,220.00 | 2025-05-16 | 2026-03-31 | 16.8 |
| 0015859 | FIRST COAST LIGHTING AND FANS | 20 | $37,124.00 | 2025-04-22 | 2026-03-05 | 16.7 |
| PULTE | PULTE INTERIORS | 19 | $26,286.00 | 2025-05-22 | 2026-03-27 | 17.2 |
