# Section 06 Highlights — Platform Context (eglo_can, 2026-06-17)

## Candidate Highlights

1. **Import pipeline is healthy and consistent** — EGLO Canada runs ~105 imports/month with no missed cycles over the last 7 months (87–166/mo), so the core data plumbing is reliable. `surprise_score: 1.0` · `signal_id: (operational)` · `[→ §platform]`
   - Tone: POSITIVE

2. **10 configuration data sources are 313 days stale** — Options, Matrix Options, Kit Items, Contract Prices and 6 other feeds last synced Aug 7, 2025; reps configure and quote products directly from these. `surprise_score: 3.5` · `signal_id: SIG-RISK-03` · `[→ §platform]`
   - Tone: RISK

3. **SmartPicks used only 14 times all year against 14,443 product searches** — Reps do the manual browsing work the recommendation engine could do for them; activating it across active searchers is a low-cost coaching win. `surprise_score: 2.0` · `signal_id: SIG-OPP (feature gap)` · `[→ §platform]`
   - Tone: OPPORTUNITY

## Priority Action Candidate

- **Re-sync 10 stale configuration feeds (313 days old)** — Urgency: MEDIUM. Core configuration/pricing entities exceed 180 days stale, undermining product-configuration and pricing accuracy across the report. One coordinated FTP re-import clears all Critical flags. `signal_id: SIG-RISK-03`
