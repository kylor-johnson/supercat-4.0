# Section 06 Highlights — Platform Context (Bulbrite, bri)
- Run date: 2026-06-17
- Section: §6 Platform Context (`[→ §platform]`)
- Note: §6 produces highlights only when issues are severe (>180d staleness) or a clear capability opportunity exists. Core entities (products/inventory/customers) are all Fresh — so 0 priority-action candidates.

## Candidate Highlights

1. **SmartPicks is sitting idle while reps search 11,000+ times a month** — Product Search drove 11,079 events (LTM) but SmartPicks was opened only 29 times; activating the recommendation engine turns manual browsing into guided selling.
   - dollar_figure: n/a (capability/coaching opportunity — no direct dollar attribution)
   - surprise_score: 6.5
   - signal_id: SIG-FEAT-01
   - tone: POSITIVE / OPPORTUNITY
   - deep-link: `[→ §platform]`

2. **Eight configuration tables haven't refreshed since August 2025** — Options, Option Groups, Matrix Options, Riser Prices, and Sales Quotas are all ~300 days stale, so configurable-product setups and quota tracking are running on last summer's data.
   - dollar_figure: n/a (operational risk — no direct dollar attribution)
   - surprise_score: 5.0
   - signal_id: SIG-STALE-01
   - tone: RISK / OPERATIONAL
   - deep-link: `[→ §platform]`

3. **Price levels are 82 days stale — reps may be quoting old pricing** — The price_levels table last imported March 26, 2026, past the 30-day freshness window for pricing data; a single price-level re-import removes the risk of an outdated quote on the iPad.
   - dollar_figure: n/a (pricing-accuracy risk)
   - surprise_score: 4.0
   - signal_id: SIG-STALE-02
   - tone: RISK / OPERATIONAL
   - deep-link: `[→ §platform]`

## Priority Action Candidates
- None. Stale entities are peripheral config tables, not core data (products, inventory, customers are all Fresh / 0 days). Per the section guide, platform context reaches priority-action urgency only when core entities exceed 180 days stale.
