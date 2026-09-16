# Section 06 Highlights — Platform Context (Buster & Punch, bp)
Run date: 2026-06-17

## Candidate Highlights

1. **11 core reference data sources have not refreshed in 313 days**
   Options, contract prices, kit items, and customer favorites all last synced August 2025 — every quote and product view in the app is working from year-old configuration data. No direct dollar figure (reference-data staleness). surprise_score: 3.5 | signal_id: SIG-RISK-03 | [→ §platform]

2. **Catalog is only 43.8% complete — 495 visible products have no image, 1,237 carry no price**
   Nearly 1,500 visible products are missing the assets reps need to present or quote them on the iPad. No direct dollar figure (operational gap). surprise_score: 2.4 | signal_id: SIG-RISK-01 (catalog) | [→ §platform]

3. **[POSITIVE] Import pipeline is healthy and the app is in daily use**
   ~60 imports/month sustained over 7 months, 8 core features actively used (2,800 product searches LTM), and 6 Smart Stacks live — the platform foundation is solid, which is why a single refresh would pay off immediately. surprise_score: 1.0 | signal_id: SIG-PLATFORM-HEALTH | [→ §platform]

## Priority Action Candidates

1. **Coordinated re-import of 11 stale reference sources** — urgency: HIGH
   Core entities (options, contract prices, kit items) are >180 days stale (313d), which the guide flags as priority-action-worthy because staleness at this level undermines every other section. signal_id: SIG-RISK-03
