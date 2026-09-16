# Section 06 Highlights — Vaxcel International Corporation (vic)
- Run date: 2026-06-17
- Note: §6 surfaces highlights only when staleness/config gaps are severe. Two candidates below; neither rises to top-level priority-action (no core entity >180d — products/inventory/customers are all fresh).

## Candidate Highlights

1. **[POSITIVE / OPPORTUNITY] SmartPicks is live but barely used — guided selling upside.**
   Reps run Product Search 1,931 times (LTM) but open SmartPicks only 19 times; activating it converts manual browsing into customer-specific recommendations that feed the companion-product patterns in §2/§3. No direct dollar figure (utilization gap). `surprise_score: 3.0` · `signal_id: SIG-OPP-04` (feature adoption framing) · `[→ §platform]`

2. **[RISK] 12 reference-data sources are 301 days stale (last synced Aug 2025).**
   Pricing, product options, and sales-planning feeds have not refreshed in 10 months, so every pricing- or option-dependent figure in this report carries that caveat; one configuration re-import clears all 12. Dollar impact nominal ($1 placeholder per signal). `surprise_score: 3.3` · `signal_id: SIG-RISK-03` · `[→ §platform]`

3. **[RISK] Inventory imports silently drop ~80 lines every run.**
   Each inventory sync rejects roughly 80 "product not found" lines (e.g., C0358–C0381, W0566–W0593) that exist in the stock feed but not the product catalog — stock counts for those items never update. `surprise_score: 3.3` · `signal_id: SIG-RISK-03` · `[→ §platform]`

## Priority Action Candidates
- None. Core entities (products, inventory, customers) are all fresh (≤7d); staleness is confined to configuration/reference data, which does not meet the >180d core-entity bar for the top-level priority list.
