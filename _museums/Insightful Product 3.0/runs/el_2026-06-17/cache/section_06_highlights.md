# Section 06 Highlights — Platform Context (Eurofase Inc., el)
Run date: 2026-06-17

## Candidate Highlights

1. **[POSITIVE] Product search powers 90,584 app events with 11 capabilities in active use**
   Eurofase's reps lean hard on the digital catalog — product search alone drove 27,031 events (30% of all activity) over the trailing 12 months, with the catalog library a strong second. Adoption breadth is a credibility win for the platform.
   - Dollar figure: n/a (engagement signal)
   - surprise_score: 1.2
   - signal_id: SIG-FEATURE-USE (Q-22)
   - [→ §platform]

2. **[POSITIVE/OPPORTUNITY] SmartPicks used just 67 times against 27,031 product searches — guided-selling upside**
   Reps do manual product discovery 400x more often than they let SmartPicks recommend — activating it across the team (starting with the proven 46818-034 / 46819-031 companion pattern) converts heavy search effort into guided suggestions.
   - Dollar figure: ties to $1.4M co-purchase opportunity (SIG-OPP-01)
   - surprise_score: 2.0
   - signal_id: SIG-OPP-01 (companion-product link)
   - [→ §platform]

3. **[RISK] 10 configuration data sources stale 301 days — configurable-product layer running on year-old definitions**
   Options, option groups, riser pricing, kit items, and quota/commitment reports all stopped syncing on Aug 20, 2025. Core daily data (products, inventory, customers) is fresh, so the impact is contained to configurable SKUs — but a single batch re-import would close it.
   - Dollar figure: n/a (operational data integrity)
   - surprise_score: 3.3
   - signal_id: SIG-RISK-03 (Q-08 / Q-11)
   - [→ §platform]

## Priority Action Candidate

- **Re-import the 10 stale configuration sources (URGENCY: MEDIUM).** All stopped on the same date (Aug 20, 2025), pointing to one paused feed; one batch FTP upload restores option pricing, kit definitions, and quota tracking. Not top-of-report urgent because core catalog/inventory/customer data is fresh — the staleness is confined to the configurable-product and quota layer.
