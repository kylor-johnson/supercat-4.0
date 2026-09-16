# Q-17 — Dormant Customers

- **Org:** Braxton Culler (bcf, org_id=171)
- **Period:** Last 12 months (lapsed = ordered 3–12mo ago, not in last 3mo; at-risk = last order > 90 days ago)
- **Guardrails:** `is_marked_deleted = false OR IS NULL`
- **Run date:** 2026-04-17

## Recently Lapsed (25 rows)

| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
|---|---|---|---|---|---|
| 03773 | Halo Home | NC | 2025-12-02 | 15 | $48,968 |
| 00305 | Kalin Home Furnishings | FL | 2025-12-15 | 3 | $42,575 |
| 03851 | Closter Sales/Richard Goodman | NJ | 2025-12-29 | 4 | $33,812 |
| 01419 | Sweat's Furniture, Inc. | GA | 2025-12-11 | 7 | $32,570 |
| 03753 | B & B Family Ventures Inc | NC | 2025-09-29 | 2 | $26,755 |
| 03875 | Esther Ashe Designs | GA | 2025-04-27 | 1 | $24,631 |
| 02093 | Custom Home Furnishings | NC | 2025-11-02 | 5 | $23,500 |
| 03286 | Home Accents II | SC | 2025-11-03 | 3 | $23,210 |
| 02414 | Rising Sun Partners LLC | PA | 2025-09-10 | 4 | $23,034 |
| 22036 | Matter Bros. Furn. | FL | 2025-09-25 | 1 | $22,540 |
| 03679 | Wicker and More of Shallotte | NC | 2026-01-16 | 2 | $21,220 |
| 02020 | Preferred Designs, Inc. | DE | 2026-01-09 | 4 | $21,048 |
| 04046 | Door County Int & Design | WI | 2025-12-12 | 12 | $20,800 |
| 03843 | Tuskers Home Store Inc | FL | 2026-01-07 | 7 | $20,090 |
| 02163 | Phillips-Wright Furniture Co | NC | 2025-10-28 | 6 | $16,973 |
| 01683 | The Pamaro Shop Co. | FL | 2025-10-28 | 1 | $14,205 |
| 02290 | Decorating Den Ints #2290 | PA | 2025-11-14 | 4 | $13,829 |
| 03553 | Brooke Chamblee Interiors | AL | 2025-10-04 | 4 | $13,566 |
| 03877 | Revisioned Interiors | GA | 2025-08-18 | 7 | $13,405 |
| 03211 | Interiors By Mary Susan | IL | 2026-01-05 | 6 | $11,715 |
| 04650 | Castner & Castner | FL | 2026-01-09 | 1 | $10,630 |
| 03568 | Outside Interiors LLC | NJ | 2025-05-31 | 1 | $10,610 |
| 03304 | Waterside Interiors | FL | 2025-07-15 | 2 | $10,308 |
| 21582 | Manteo Furniture | NC | 2025-12-17 | 2 | $10,278 |
| 02345 | Cynthia Huffines Int Design | NC | 2025-11-03 | 2 | $10,220 |

## At-Risk High-Value (20 rows)

| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
|---|---|---|---|---|---|
| 03773 | Halo Home | NC | $48,968 | 2025-12-02 | 136 |
| 00305 | Kalin Home Furnishings | FL | $42,575 | 2025-12-15 | 123 |
| 03851 | Closter Sales/Richard Goodman | NJ | $33,812 | 2025-12-29 | 109 |
| 01419 | Sweat's Furniture, Inc. | GA | $32,570 | 2025-12-11 | 127 |
| 03753 | B & B Family Ventures Inc | NC | $26,755 | 2025-09-29 | 200 |
| 03875 | Esther Ashe Designs | GA | $24,631 | 2025-04-27 | 355 |
| 02093 | Custom Home Furnishings | NC | $23,500 | 2025-11-02 | 166 |
| 03286 | Home Accents II | SC | $23,210 | 2025-11-03 | 165 |
| 02414 | Rising Sun Partners LLC | PA | $23,034 | 2025-09-10 | 219 |
| 22036 | Matter Bros. Furn. | FL | $22,540 | 2025-09-25 | 204 |
| 03679 | Wicker and More of Shallotte | NC | $21,220 | 2026-01-16 | 90 |
| 02020 | Preferred Designs, Inc. | DE | $21,048 | 2026-01-09 | 98 |
| 04046 | Door County Int & Design | WI | $20,800 | 2025-12-12 | 126 |
| 03843 | Tuskers Home Store Inc | FL | $20,090 | 2026-01-07 | 100 |
| 02163 | Phillips-Wright Furniture Co | NC | $16,973 | 2025-10-28 | 171 |
| 01683 | The Pamaro Shop Co. | FL | $14,205 | 2025-10-28 | 171 |
| 02290 | Decorating Den Ints #2290 | PA | $13,829 | 2025-11-14 | 154 |
| 03553 | Brooke Chamblee Interiors | AL | $13,566 | 2025-10-04 | 195 |
| 03877 | Revisioned Interiors | GA | $13,405 | 2025-08-18 | 242 |
| 03211 | Interiors By Mary Susan | IL | $11,715 | 2026-01-05 | 102 |
