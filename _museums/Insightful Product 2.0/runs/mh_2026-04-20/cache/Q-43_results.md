# Q-43: Territory Coverage & Dormancy

- **Query ID:** Q-43
- **Org:** Magnussen Home (mh, org_id=184)
- **Source:** Postgres
- **Period:** LTM
- **Row count:** 37 territories
- **Run date:** 2026-04-20
- **Exclusions:** None
- **Note:** Territory codes stored as JSON array

## Step 1 — Customer base by territory

| territory_code | territory_name | total_assigned_customers |
|---|---|---|
| 230 | 230 - Kentucky, Tennessee, Alabama | 125 |
| 201 | 201 - North Carolina, South Carolina | 110 |
| 262 | 262 - Metro NY, Connecticut | 83 |
| 310 | 310 - N California, N Nevada, Hawaii | 83 |
| 115 | — | 80 |
| 205 | 205 - Ohio, Western PA, Maryland | 79 |
| 345 | 345 - Georgia | 79 |
| 320 | 320 - Wisconsin, Illinois, Indiana | 74 |
| 250 | 250 - Southern California | 66 |
| 335 | 335 - North Texas | 65 |
| 235 | 235 - Florida (Excl. Panhandle) | 58 |
| 125 | — | 58 |
| 110 | — | 46 |
| 225 | 225 - E. Pennsylvania, S. New Jersey, Delaware | 40 |
| 290 | 290 - Vermont, Massachusetts, New Hampshire, Maine, R | 39 |
| 130 | — | 37 |
| 355 | 355 - Mississippi, Louisiana, Tennessee (Memphis Trading Area) | 34 |
| 220 | 220 - Washington, Oregon, Idaho, Alaska | 34 |
| 100 | — | 33 |
| 330 | 330 - Iowa, Nebraska, Kansas | 33 |
| 295 | 295 - Michigan | 30 |
| 120 | — | 28 |
| 135 | — | 25 |
| 260 | 260 - New York (Excl. NYC) | 24 |
| 240 | 240 - Internet Business | 24 |
| 245 | 245 - N W and S Dakota, Montana, N Wyoming, E Washington, E | 23 |
| 285 | 285 - Mexico | 23 |
| 315 | 315 - South Texas (Excl. El Paso) | 19 |
| 200 | 200 - Minnesota, South Dakota, North Dakota | 17 |
| 340 | 340 - Colorado, Utah, Wyoming | 16 |
| 360 | 360 - House Account - US | 14 |
| 145 | — | 7 |
| 505 | — | 5 |
| 203 | 203 - ON USA | 2 |
| 202 | 202 - BC USA | 1 |
| 505.1 | — | 1 |
| 520 | — | 1 |

## Step 3 — Territory gap summary

| territory_code | assigned_customers | ecat_active_customers | never_or_lapsed_via_ecat |
|---|---|---|---|
| 201 | 110 | 0 | 110 |
| 230 | 125 | 27 | 98 |
| 310 | 83 | 0 | 83 |
| 262 | 83 | 1 | 82 |
| 205 | 79 | 0 | 79 |
| 345 | 79 | 0 | 79 |
| 115 | 80 | 2 | 78 |
| 320 | 74 | 0 | 74 |
| 335 | 65 | 1 | 64 |
| 235 | 58 | 0 | 58 |
| 125 | 58 | 0 | 58 |
| 250 | 66 | 20 | 46 |
| 110 | 46 | 0 | 46 |
| 225 | 40 | 0 | 40 |
| 290 | 39 | 0 | 39 |
| 130 | 37 | 0 | 37 |
| 220 | 34 | 0 | 34 |
| 355 | 34 | 2 | 32 |
| 295 | 30 | 1 | 29 |
| 330 | 33 | 7 | 26 |
| 240 | 24 | 0 | 24 |
| 260 | 24 | 0 | 24 |
| 245 | 23 | 0 | 23 |
| 100 | 33 | 12 | 21 |
| 120 | 28 | 8 | 20 |
| 285 | 23 | 6 | 17 |
| 315 | 19 | 2 | 17 |
| 135 | 25 | 8 | 17 |
| 340 | 16 | 0 | 16 |
| 200 | 17 | 1 | 16 |
| 360 | 14 | 0 | 14 |
| 145 | 7 | 1 | 6 |
| 505 | 5 | 1 | 4 |
| 203 | 2 | 0 | 2 |
| 202 | 1 | 0 | 1 |
| 505.1 | 1 | 0 | 1 |
| 520 | 1 | 0 | 1 |
