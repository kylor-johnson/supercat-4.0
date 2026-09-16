# §8 Platform & Feature Utilization — Highlight Candidates

1. **99.9% catalog completeness** — 1,731 active products with only 2 missing images and zero pricing gaps as of June 2026. [→ §platform]
2. **15 of 17 tracked features active with 173K events** — broad platform adoption across 90 users in the trailing 12 months, led by product search (45,235 events) and configured item ordering (16,443 events). [→ §platform]
3. **14 data entities stale (7–10 months)** — Options, pricing configuration, and taxonomy data have not been refreshed since August–November 2025, creating drift against the product catalog refreshed 5 days ago. [→ §platform]
4. **Import pipeline healthy at ~49 imports/month** — consistent data maintenance cadence over the trailing 5 full months (January–May 2026) with no fatal processing errors. [→ §platform]

## Priority Action Candidate
- **MEDIUM**: Re-import options.csv and option_groups.csv to resolve 220-day drift against product catalog, then refresh pricing and taxonomy data to eliminate the remaining 299-day staleness across 14 configuration entities [HYPOTHETICAL]. [→ §platform]
