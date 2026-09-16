# Q-43: Territory Coverage & Dormancy — Visual Comfort Signature (vcg, org_id=141)
- **Source**: Postgres MCP (customers + orders)
- **Run date**: 2026-04-30

## Territory Code Lookup
- **Format**: JSON (territory_codes column on customers table)
- **Territories table row count**: 0 (no code-to-name lookup available)

## Step 1: Territory Distribution
- **Total territory codes**: 99
- **Largest territory**: Code "19" with 2,284 assigned customers

## Step 3: Territory Gap Summary
Most territories have very low eCat activation rates.

| Territory Code | Assigned Customers | eCat Active (ordered LTM) | Activation Rate |
|---------------|-------------------|--------------------------|----------------|
| 40 | 112 | 52 | 46.4% |
| 19 | 2,284 | 87 | 3.8% |
| 12 | 1,043 | 41 | 3.9% |
| 25 | 876 | 34 | 3.9% |
| 31 | 654 | 28 | 4.3% |
| 08 | 982 | 31 | 3.2% |
| 15 | 743 | 22 | 3.0% |
| 22 | 891 | 19 | 2.1% |
| 33 | 567 | 16 | 2.8% |
| 44 | 423 | 14 | 3.3% |

Note: Territory code "40" has the best activation rate at 46.4% (52 of 112 customers). Most other territories are below 5% activation, indicating significant eCat adoption opportunity across the territory map.
