# §7 Peer Benchmarking — Highlights

## Summary
- **Subsections rendered:** 5 of 6
- **Subsection skipped:** 1 (Growth Trajectory → requires 2+ monthly snapshots, not available until May 2026)
- **Period:** Apr 2025–Apr 2026
- **Peer group:** iPad-only (tier3, n=54, low confidence — all internal-only labels)

## Key Stats
- **Engagement score: 80** — Top 5% of peers (Q4), +20 above median of 60
- **Adoption score: 100** — Top 5% of peers (Q4), +29 above median of 71, highest in cohort
- **Value delivery score: 80** — Top 15% of peers (Q4), +20 above median of 60
- **Data & Operational Health: 30** — Bottom 10% (Q1), −39 below median of 69
- **Trajectory score: 20** — Bottom 20% (Q1), −55 below median of 75
- **3 of 5 benchmarked metrics above peer median** (engagement, adoption, value delivery)
- **Feature depth:** 4 — 3 features active and aligned with peers, 1 gap (Sales Portal)

## Hero Stat
- **Chosen:** Engagement score (80, Top 5%, Q4)
- **Reason:** First applicable metric in priority order — orders_per_user skipped (HAS_CART=false); engagement is a strong outlier at Q4 / pctile=0.981
- **Display:** "80" with "Top 5%" badge (pctile 0.981 → raw 2% → rounded to 5%)

## Notable Decisions
1. **Hero selected: engagement_score** over adoption_score — engagement is higher in priority order (#2 vs #3) and both are Q4. Engagement at pctile=0.981 qualifies as a strong outlier.
2. **catalog_completeness not rendered** — no catalog_completeness data present in peer_benchmark_extract.md for this org.
3. **orders_90d and orders_per_user skipped** — HAS_CART=false, iPad-only bundle per gate_flags.md.
4. **health_score suppressed entirely** — internal metric, not surfaced per operator and dependency rules.
5. **Tier 3 framing applied** — "other accounts on the iPad plan" with directional context note per PEER_BENCHMARK.md §7. Tier 3 not framed as limitation.
6. **operational_health_score titled "Data & Operational Health"** — sentence uses "Data freshness and configuration reliability" framing. No instance of "health score" or "health scores" anywhere in the fragment.
7. **Range bar markers** — Q4 metrics (value delivery, adoption) positioned at left:100% (above p75). Q1 metrics (operational health, trajectory) positioned at left:0% (below p25). Exact p25/p75 values not in extract; quartile-based clamped positioning is correct by definition since Q4 ≥ p75 and Q1 ≤ p25.
8. **Feature Adoption table: 4 rows** — Document Library (Active, 100%), PDF Catalog (Active, 100%), Kit Items (Active, 27.7%), Sales Portal (Not Active, 66%). CPQ excluded per rule (client doesn't have CPQ). Portal Orders excluded as redundant with Sales Portal for iPad-only bundle.
9. **Growth Trajectory (§7.6) skipped** — requires 2+ monthly snapshots, first available May 2026.
10. **Top Performer patterns** derived from Q-CI-05 data (feature depth 7-8 at top, login frequency 3-5× median, 80%+ session conversion). No company names exposed. No "health score" vocabulary used.
11. **Percentile rounding** — engagement 0.981 → raw "Top 1.9%" → rounded to "Top 5%" (nearest 5%, minimum 5%). Adoption 1.0 → would be "Top 0%" → capped at "Top 5%". These only appear in hero badge; narrative rows use quartile pills instead.
