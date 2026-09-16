# Section 06 Highlights — Platform Context (kll, 2026-06-17)

## Candidate Highlights

1. **SmartPicks sits dormant while reps run 30,630 product searches a year** — Personalized recommendation feature logged just 2 events all year despite all 118 users having access; activating it would guide reps to the right product per account instead of manual browsing. `[→ §platform]`
   - surprise_score: 7.5
   - signal_id: SIG-PLATFORM-FEATURE-01
   - tone: POSITIVE / OPPORTUNITY

2. **11 supporting data types have been frozen for 313 days** — Options, contract and riser pricing, kit items, and report tables stopped importing in August 2025; core data (products, inventory, customers) stays fresh daily, so impact is limited to multi-option and kit configuration accuracy. `[→ §platform]`
   - surprise_score: 5.0
   - signal_id: SIG-PLATFORM-STALE-01
   - tone: RISK (moderate)

## Priority Action Candidates

- None. Staleness is confined to non-core supporting entities (core products/inventory/customers are current), so it does not rise to top-level priority-action urgency. A single coordinated re-import of six files resolves it.
