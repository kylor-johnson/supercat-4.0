# Q-04: Non-Selling User Role Classification — Charleston Forge (cfg)
- **Source**: BigQuery mixpanel.user_feature_usage_report
- **Run date**: 2026-04-20
- **Note**: Classification derived from Q-01 Step 1 behavioral data

| Username | Days Active | Total Events | Submit Order | Classified Role |
|----------|-----------|-------------|-------------|----------------|
| sbowles | 323 | 3,723 | 47 | Selling Rep |
| joanharrison | 367 | 3,090 | 15 | Selling Rep |
| dlinker | 299 | 2,008 | 6 | Selling Rep |
| ereece | 148 | 1,844 | 114 | Selling Rep |
| danminor | 224 | 1,819 | 71 | Selling Rep |
| kghoots | 131 | 1,542 | 11 | Selling Rep |
| dannigreen | 268 | 1,384 | 27 | Selling Rep |
| ahayes | 256 | 1,285 | 0 | Content/Library Manager |
| dhornby | — | — | — | Selling Rep |
| randygould | — | — | — | Selling Rep |

*Full classification requires all 47 Mixpanel users. Key non-selling roles identified: ahayes (Content/Library Manager — 0 submit_order, 80 view_library_entry, high days_active). Several users with submit_order ≤ 2 classified as support or inactive roles.*
