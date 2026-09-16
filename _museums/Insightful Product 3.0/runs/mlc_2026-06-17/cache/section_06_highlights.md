# Section 06 Highlights — Platform Context (mlc, 2026-06-17)

## Candidate Highlights

1. **Pricing and options data is 313 days stale across 12 tables** — Price levels, contract prices, and configurable-product options haven't refreshed since August 2025, so reps may be quoting from 10-month-old prices on every configured order. `surprise_score: 3.5` · `signal_id: SIG-RISK-03` · [→ §platform]

2. **(POSITIVE) Catalog and inventory feeds are current within 2 days** — Products and inventory import nightly, so reps see accurate stock and the latest SKUs even while supporting tables lag — the core selling surface is healthy. `surprise_score: 1.1` · `signal_id: SIG-RISK-03` · [→ §platform]

3. **SmartPicks effectively unused: 1 event vs 8,408 product searches (LTM)** — Reps do high-volume manual search while a guided-recommendation feature that draws on customer purchase history sits idle — a low-cost coaching win. `surprise_score: 1.6` · `signal_id: SIG-RISK-03` · [→ §platform]

## Priority Action Candidates

1. **Refresh stale pricing/options data (urgency: HIGH)** — 12 core configuration tables at 313 days stale undermine quote accuracy in every section that touches pricing; a single import pass resolves it. `signal_id: SIG-RISK-03`
