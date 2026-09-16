# §8 Platform & Feature Utilization — Highlight Candidates

1. **175,771 platform events across 76 users in the trailing 12 months** — product search and customer lookup dominate activity, confirming the platform's role as a primary selling tool rather than just a catalog browser. [→ §platform]
2. **11 configuration entities stale since August 2025** — options, price levels, and taxonomy definitions have not been refreshed in 299 days while products update daily, creating drift between the catalog and its supporting configuration. [→ §platform]
3. **Import pipeline averaging ~425 imports/month** — automated data integration is healthy and consistent with no processing failures, though individual row-level errors persist in sales data and product imports. [→ §platform]

## Priority Action Candidate
- **HIGH**: Refresh options.csv and option_groups.csv to resolve 299-day drift against the daily-updating product catalog — could affect option accuracy for reps building orders on products modified since August 2025 [HYPOTHETICAL]. [→ §platform]
