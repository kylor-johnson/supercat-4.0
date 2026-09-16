# Q-43: Territory Coverage Analysis — Visual Comfort - Studio /Fans (fms, org_id=108)
- **Run date**: 2026-04-30
- **Source**: Postgres (customers × orders)

## Step 1: Customer Base by Territory
- **Status**: SQL syntax error in initial query — skipped
- **Fallback**: Territory customer counts derived from Step 3 gap summary

## Step 2: eCat Order Activity by Territory
- **Status**: Large output — see raw query logs for full detail

## Step 3: Territory Gap Summary (Assigned vs Active Customers)

| Territory Code | Customers Assigned | Customers Active (eCat orders) | Coverage Gap |
|---------------|-------------------|-------------------------------|-------------|
| 314042 | 476 | 29 | 447 |
| 269729 | 339 | 44 | 295 |
| 20943 | 322 | 56 | 266 |
| 21919 | 260 | 3 | 257 |
