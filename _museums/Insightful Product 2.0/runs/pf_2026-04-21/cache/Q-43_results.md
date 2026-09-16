# Q-43 — Territory Coverage & Dormancy — Palecek (pf, org_id=32)
- **Run date**: 2026-04-21
- **Source**: Postgres customers (territory_codes JSON format) + orders
- **Note**: territories table has 0 rows — no territory name lookup available. Territory codes are numeric IDs only.
- **Format detected**: JSON array (e.g., ["90156"])

## Step 1 — Customer Base by Territory (top 20)

| territory_code | territory_name | total_assigned_customers |
|---------------|---------------|------------------------|
| 90350 | — | 1,519 |
| 90200 | — | 944 |
| 90170 | — | 938 |
| 90718 | — | 768 |
| 90902 | — | 738 |
| 90110 | — | 736 |
| 90175 | — | 694 |
| 90156 | — | 634 |
| 90210 | — | 607 |
| 90280 | — | 569 |
| 90174 | — | 559 |
| 90145 | — | 521 |
| 90178 | — | 449 |
| 90217 | — | 439 |
| 90146 | — | 413 |
| 90651 | — | 407 |
| 90561 | — | 387 |
| 90199 | — | 374 |
| 90544 | — | 327 |
| 90541 | — | 313 |

## Step 3 — Territory Gap Summary (top 20 by dormancy)

| territory_code | assigned_customers | ecat_active_customers | never_or_lapsed_via_ecat |
|---------------|-------------------|----------------------|------------------------|
| 90350 | 1,519 | 5 | 1,514 |
| 90200 | 944 | 4 | 940 |
| 90170 | 938 | 1 | 937 |
| 90110 | 736 | 4 | 732 |
| 90902 | 738 | 7 | 731 |
| 90718 | 768 | 71 | 697 |
| 90175 | 694 | 67 | 627 |
| 90210 | 607 | 9 | 598 |
| 90156 | 634 | 70 | 564 |
| 90174 | 559 | 75 | 484 |
| 90280 | 569 | 92 | 477 |
| 90217 | 439 | 9 | 430 |
| 90145 | 521 | 97 | 424 |
| 90178 | 449 | 26 | 423 |
| 90651 | 407 | 11 | 396 |
| 90146 | 413 | 42 | 371 |
| 90561 | 387 | 41 | 346 |
| 90199 | 374 | 49 | 325 |
| 90541 | 313 | 30 | 283 |
| 90148 | 268 | 0 | 268 |
