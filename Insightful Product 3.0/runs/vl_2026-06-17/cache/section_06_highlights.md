# Section 06 Highlights — Platform Context (vl, 2026-06-17)

## Candidate Highlights

1. **[RISK] Ten configuration data sources frozen since August 2025**
   Options, Option Groups, Matrix Options, Contract Prices and 6 related tables
   were last refreshed 301 days ago, so any configured-item or contract-pricing
   logic the app applies reflects setup from 10 months ago. A single re-import
   closes the gap.
   - Dollar figure: not directly monetized (operational reliability impact)
   - surprise_score: 3.3
   - signal_id: SIG-RISK-03
   - [→ §platform]

2. **[POSITIVE] Core selling data is fully fresh — products, inventory, customers all under 1 day old**
   The feeds reps depend on daily are current, the import pipeline runs a steady
   ~86 imports/month, and 4 Smart Stacks are live. The staleness is confined to
   back-office configuration tables, not the day-to-day catalog.
   - Dollar figure: n/a (reliability foundation)
   - surprise_score: 1.0
   - signal_id: SIG-RISK-03 (inverse / freshness baseline)
   - [→ §platform]

3. **[OPPORTUNITY] SmartPicks unused despite 5,000+ annual product searches**
   Reps search the catalog 5,010 times a year but have used SmartPicks zero
   times; activating it would surface personalized reorder candidates
   automatically and complements the companion-buying patterns in product
   intelligence.
   - Dollar figure: not directly monetized
   - surprise_score: 2.0
   - signal_id: SIG-OPP (feature adoption)
   - [→ §platform]

## Priority Action Candidates
- None. Configuration staleness is at 301 days but is confined to back-office
  tables (options, contract prices); core selling data (products, inventory,
  customers) is fresh, so this does not undermine every other section and stays
  below the priority-action bar. Surface as a §6 operational item only.
