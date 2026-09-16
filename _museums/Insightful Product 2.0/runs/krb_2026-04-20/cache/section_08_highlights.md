# §8 Platform & Feature Utilization — Highlight Candidates

1. **Zero fresh data entities — all 22 tracked types are beyond the 30-day threshold** — the newest data (All-Channel Orders, Portal Invoices) is 38 days old; the oldest (kit items, inventory, options) is 255 days stale. No imports have occurred since December 2025. [→ §platform]
2. **Only 2 of 8 users are active, with 57 total logins all-time** — platform engagement is minimal; 0 users have ordered in the last 90 days. Feature usage is concentrated in browsing (filtering, searching, library) with near-zero transactional or presentation activity. [→ §platform]
3. **Import pipeline dormant for 4+ months** — the last imports were 4 events on December 3, 2025, with 2 containing errors (invalid trade name codes, missing parent reference). No imports attempted since. [→ §platform]
4. **Customer records 223 days stale, inventory 255 days stale** — the two most critical selling data types are 7–8 months old, meaning reps may see outdated accounts and unreliable stock levels. [→ §platform]

## Priority Action Candidate
- **CRITICAL**: Resume regular data imports immediately — customer records, inventory, and price levels are the highest-priority entities to refresh. The import infrastructure is functional (345 lifetime imports); the pipeline just needs to be restarted with corrected source files to address the December 2025 errors. [→ §platform]
