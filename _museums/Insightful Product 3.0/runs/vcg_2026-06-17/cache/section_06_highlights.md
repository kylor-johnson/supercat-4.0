# Section 06 Highlights — Platform Context (vcg, 2026-06-17)

## Candidate Highlights

1. **Pricing and option data is 10 months stale — quotes may be wrong**
   Price levels, contract prices, options, and matrix configurations haven't imported since August 7, 2025 (313 days), so any rep quoting a configured fixture or contract price is working from outdated reference data. A single FTP re-import restores quote accuracy across the catalog.
   - Dollar figure: N/A (operational reliability — affects accuracy of all quoting, no isolated $ figure)
   - `surprise_score`: 2.0
   - `signal_id`: SIG-STALE-CONFIG (Q-08 / Q-11)
   - `[→ §platform]`
   - **PRIORITY ACTION candidate** — urgency: HIGH (core pricing/config data >180d stale undermines quote accuracy across the report)

2. **SmartPicks is barely touched while reps search 52,000+ times a year (positive opportunity)**
   Product search ran 52,034 times (LTM) but SmartPicks opened only 269 times — reps are browsing manually for recommendations the app can generate from purchase history. Coaching the heaviest searchers onto SmartPicks would cut browsing time and lift presentation relevance.
   - Dollar figure: N/A (engagement/coaching opportunity — no direct $ estimate available)
   - `surprise_score`: 1.5
   - `signal_id`: SIG-FEATURE-GAP (Q-22)
   - `[→ §platform]`
   - POSITIVE / OPPORTUNITY highlight

## Priority Action Candidates
- Re-import pricing and option-configuration tables (313 days stale) — HIGH urgency.

## Notes
- Catalog Remediation NOT rendered (Q-07 not present).
- Peer benchmarking permanently excluded — not referenced.
- Import pipeline healthy (~263/mo) — Import Pipeline Detail not rendered.
