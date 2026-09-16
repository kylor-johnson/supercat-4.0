# Section 06 Highlights — Platform Context

## Candidate Highlights

1. **[POSITIVE] Healthy Daily Import Pipeline — ~118 Imports/Month** — Products, inventory, and customers refresh every day, generating ~118 imports/month over the trailing 12 months; the data backbone every other section depends on is operating well. Dollar figure: N/A (operational health). `surprise_score`: 2.5 · `signal_id`: SIG-PLATFORM-PIPELINE-01 · [→ §platform]

2. **15 Configuration Entities Stale Since August 2025** — Options, taxonomy, price levels, and kit data haven't been refreshed in 7–10 months while the core product/inventory pipeline runs daily; one coordinated import cycle would clear all flags. Dollar figure: Price levels govern pricing on $2.6M in eCat orders (LTM). `surprise_score`: 4.2 · `signal_id`: SIG-PLATFORM-STALE-01 · [→ §platform]

3. **SmartPicks at 46 Events vs 14,496 Product Searches** — 65 active users hand-browse a 5,800-item catalog ~315x more often than they use algorithmic recommendations; a short coaching push could shift browsing time toward personalized, higher-yield product discovery. Dollar figure: N/A (efficiency gain). `surprise_score`: 3.8 · `signal_id`: SIG-PLATFORM-FEATURE-01 · [→ §platform]

## Priority Action Candidates

None — core entities (products, inventory, customers) are fresh and refresh daily. Configuration staleness is operationally important but not urgent enough for the top-level priority list (no core entity exceeds 180 days).
