# Admin Console — Option Mapping update (Pebl)

Apply **after** options, option_groups, and products imports succeed.

**Path:** Products → Option Mappings → **OptionSet1: Frame Color** → Edit

Replace/add mapping connections using `option_mappings_spec.json`. Summary:

| Frame group selected | Updates OptionSet2 (Material) | Updates OptionSet3 (Cushion) |
|---------------------|------------------------------|------------------------------|
| **Mocha Frame** | Neo/Teak/Alu/Haven/Wave ceramics + new collection sand ceramics | Neo/Teak/Alu/Wave/Orbit cushions |
| **Dark Brown Frame** | Neo dark brown + Tube offwhite ceramic | Neo dark brown cushion |
| **Charcoal Frame** | Teak/Alu/Wave + new collection graphite ceramics | Teak/Alu/Wave + Alu sunlounger Jalousie (+$10) |
| **Olive Green Frame** | Horizon Roman Sand ceramic | — |
| **Teak Frame** | Orbit travertine + Levl/Newport glazed ceramics | Newport UV931609 + Lajolla 185 |

**Note:** Product OptionSet columns on each SKU narrow which groups appear. Mapping controls the frame → material/cushion cascade.

Postgres MCP is read-only — this step must be done in Admin Console (or Rails console on server).
