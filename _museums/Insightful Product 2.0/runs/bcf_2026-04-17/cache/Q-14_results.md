# Q-14 — Reorder Velocity (Top 20, >= 3 orders)

- **Org:** Braxton Culler (bcf, org_id=171)
- **Period:** Last 12 months
- **Guardrails:** `is_marked_deleted = false OR IS NULL`
- **Rows returned:** 20
- **Run date:** 2026-04-17

| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
|---|---|---|---|---|---|---|
| 00982 | Outer Banks Furniture | 97 | $183,453 | 2025-04-19 | 2026-04-14 | 3.7 |
| 00523 | W.F. Booth & Son, Inc. | 76 | $118,817 | 2025-04-18 | 2026-04-14 | 4.8 |
| 02524 | Guthrie Interiors | 64 | $106,310 | 2025-04-29 | 2026-04-08 | 5.5 |
| 03402 | Trident Furnishings Inc | 61 | $130,900 | 2025-04-25 | 2026-04-16 | 5.9 |
| 01196 | Furniture & More | 56 | $91,723 | 2025-04-25 | 2026-04-17 | 6.5 |
| 25355 | Platt's Furniture | 35 | $79,549 | 2025-04-28 | 2026-04-14 | 10.3 |
| 01453 | Osborne's Furniture | 33 | $89,864 | 2025-04-25 | 2026-04-14 | 11.1 |
| 03785 | COASTAL FURNITURE | 30 | $43,751 | 2025-05-09 | 2026-04-03 | 11.3 |
| 03808 | Thrifty Nikki's Inc | 28 | $31,168 | 2025-04-21 | 2026-04-12 | 13.2 |
| 14361 | Donna Grimes Custom Designs | 26 | $46,173 | 2025-04-23 | 2026-04-17 | 14.4 |
| 04026 | Styled By Sean | 25 | $87,593 | 2025-05-01 | 2026-04-07 | 14.2 |
| 02582 | Izzy's Inc | 25 | $35,405 | 2025-05-02 | 2026-04-14 | 14.5 |
| 03461 | Steven Shell Living | 24 | $84,240 | 2025-05-08 | 2026-04-17 | 15.0 |
| 01483 | Exotic Imports, Inc. | 24 | $79,643 | 2025-04-18 | 2026-04-01 | 15.1 |
| 22910 | Philip & Sharyn R Moss | 23 | $70,838 | 2025-04-30 | 2026-04-15 | 15.9 |
| 03461 | Steven Shell LLC | 21 | $127,260 | 2025-08-12 | 2026-03-17 | 10.8 |
| 02235 | D.Marie Interiors | 21 | $55,790 | 2025-05-01 | 2026-03-25 | 16.4 |
| 04060 | Marathon Furnishings | 21 | $37,005 | 2025-06-18 | 2026-03-23 | 13.9 |
| 02347 | Casual Designs Furniture Inc | 21 | $85,529 | 2025-04-28 | 2026-04-15 | 17.6 |
| 03948 | Fazzio Interiors Inc | 20 | $25,415 | 2025-04-21 | 2026-04-06 | 18.4 |
