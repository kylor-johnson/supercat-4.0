# Section 06 Highlights — Platform Context

## Candidate Highlights

1. **Pricing data is 183 days stale — quotes may rest on 6-month-old list prices**
   Price Levels last refreshed Dec 16, 2025; reps quoting from the app may be using outdated pricing across the entire catalog. A single price-level import would restore quoting accuracy.
   - dollar_impact: $1 (operational, not directly monetized)
   - surprise_score: 2.0
   - signal_id: SIG-RISK-03
   - deep-link: [→ §platform]

2. **Import pipeline collapsed from 125/month to single digits — the root cause of stale data**
   December 2025 saw 125 imports; every month since has been under 12 (5 in Jun 2026). This pipeline slowdown is what drives the freshness alerts across products, categories, and price levels.
   - dollar_impact: $1 (operational)
   - surprise_score: 1.6
   - signal_id: SIG-RISK-03
   - deep-link: [→ §platform]

3. **[POSITIVE] Catalog is 98.6% complete and the app is actively used**
   4,252 products are 98.6% complete (only 58 missing images, zero price gaps), and reps logged 5,300+ feature events over the trailing 12 months led by product search — the platform itself is healthy; only the data feeding it has lapsed.
   - dollar_impact: n/a (momentum)
   - surprise_score: 1.2
   - signal_id: SIG-MOMENTUM-platform
   - deep-link: [→ §platform]

## Priority Action Candidate

- **Restart the import pipeline** — urgency: HIGH. Core pricing/product data is now 126–183 days stale (Price Levels >180d threshold), undermining every section that depends on current pricing or SKU availability. A scheduled monthly import feed clears the backlog and keeps downstream intelligence accurate.
