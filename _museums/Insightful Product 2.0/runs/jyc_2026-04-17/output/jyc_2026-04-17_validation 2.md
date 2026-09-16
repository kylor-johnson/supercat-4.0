# Validation Report — Jamie Young Company
*2026-04-17 · Internal Brief QA*

## Summary
- **Overall**: PASS
- **Checks run**: 26 / 26
- **Failures**: 0

---

## V1: Health Data Integrity
- [x] Re-read Health V2 CSV row for `jyc` — confirmed present (row 30)
- [x] health_score: CSV=66, Brief=66 ✓
- [x] engagement_score: CSV=30, Brief=30 ✓
- [x] adoption_score: CSV=100, Brief=100 ✓
- [x] value_delivery_score: CSV=75, Brief=75 ✓
- [x] operational_health_score: CSV=60, Brief=60 ✓
- [x] trajectory_score: CSV=70, Brief=70 ✓
- [x] classification: CSV=Maintain, Brief=Maintain ✓
- [x] health_band: CSV=Healthy, Brief=Healthy ✓
- [x] churn_risk: CSV=False, Brief="No churn risk" ✓
- [x] expansion_ready: CSV=False, Brief="Not expansion ready" ✓
- [x] risk_modifier_applied: CSV=(empty), Brief="No risk modifiers fired" ✓
- [x] Warning flags: CSV hs_lifecycle_stale=False, hs_join_missing=False, arr_data_gap=False — Brief="All warning flags clear" ✓

**Note**: Growth components (growth_score=47, growth_band=Developing, bundle_upgrade_signal=0, feature_gap_score=50, customer_headroom_score=73, peer_benchmark_gap=10) intentionally omitted per user instruction. Not a validation failure.

## V2: Support Data Integrity
- [x] Re-ran Q-IB-HELP-AGG — total_conversations=10. Brief summary one-liner says "10 conversations in 90 days" ✓
- [x] Open tickets: Q-IB-HELP-AGING returned 0 rows. Brief says "Open Tickets (0)" ✓
- [x] Theme ticket counts: data-sync=2, training=2, sales&finance=2 (+ config=1, orders=1, user_mgmt=1). Sum of theme counts (6) ≤ total (10) ✓. Remaining 4 conversations have types counted in sub-themes or are untagged.
- [x] Escalation profile: Q-IB-HELP-THEMES shows L1=9. Brief says "9 of 10 conversations tagged L1...Zero L2+". Q-IB-HELP-AGG shows escalations_l2_plus=0. ✓

## V3: Jira Data Integrity
- [x] EBR-730: URL=`https://supercatsolutions.atlassian.net/browse/EBR-730` — correct format ✓. Summary "Remove Payment Banner from enrollment pages" matches Jira "FEA: Remove Payment Banner from enrollment pages" ✓. Status: Triaging ✓. Priority: Unprioritized ✓.
- [x] SERV-2056: URL correct ✓. Summary "Resale number field (Jamie Young)" matches ✓. Status: In Progress ✓. Priority: Unprioritized ✓.
- [x] EBR-502: URL correct ✓. Summary matches ✓. Status: Triaging ✓. Priority: High ✓.
- [x] EBR-422: URL correct ✓. Summary matches ✓.
- [x] EBR-420: URL correct ✓. Summary matches ✓.
- [x] EBR-417: URL correct ✓. Summary matches ✓.
- [x] EBR-384: URL correct ✓. Summary matches ✓.

## V4: Cross-Contamination Check
- [x] Searched brief text for other org_shortnames/org_names — none found that aren't intentional cross-references. ✓
  - **Note**: "Braxton Culler" appears in the EBR-726 note, which is correctly identified as a different client's request that references JYC. This is intentional context, not contamination.
  - **Note**: "Charlee Lowery" is a JYC employee/rep referenced in the external report highlights. Not cross-contamination.
- [x] Header: "Jamie Young Company" ✓. Footer: "Jamie Young Company" ✓. File names: `jyc_2026-04-17_internal_brief.md`, `jyc_2026-04-17_internal_brief.html` ✓.

## V5: Internal Consistency
- [x] Verdict references Engagement at 30 — confirmed in Section 2 dimension table ✓
- [x] "Three Things" #1 (Engagement drag) traces to Section 2 Engagement row (30, At Risk) ✓
- [x] "Three Things" #2 (3,654 lapsed accounts) traces to external report §3 highlights and Section 5 talking points ✓
- [x] "Three Things" #3 (240-day stale config) traces to Section 2 Operational Health (60) and external report §8 highlights ✓
- [x] "Not in the External Report" items: health score, engagement detail, support cleanliness, Jira backlog — spot-checked against external report HTML; these data points are absent from the client-facing report ✓
- [x] SuperCat Action Items supported by findings: "Refresh stale config" → Section 2 Operational Health ✓; "Triage Jira tickets" → Section 4 (7 stale tickets) ✓; "Charlee Lowery talking points" → Section 1 verdict + external report §2 highlights ✓

## V6: HTML Parity
- [x] HTML file exists at `jyc_2026-04-17_internal_brief.html` alongside markdown ✓
- [x] Spot-check #1 — Health score: MD=66, HTML=66 ✓
- [x] Spot-check #2 — Open ticket count: MD=0, HTML=0 ✓
- [x] Spot-check #3 — Jira ticket count: MD=7, HTML=7 (2 recent + 5 backlog) ✓
- [x] HTML header: client name "Jamie Young Company" ✓, date "2026-04-17" ✓, bundle "Full" ✓

---

## Notes

1. **Growth components intentionally removed**: Per user instruction, Growth Score, Growth Band, and Growth Components section are omitted from the brief. The underlying data exists in the CSV (growth_score=47, growth_band=Developing) but is not surfaced. Classification (Maintain) is retained as it's derived from the Health × Growth quadrant.

2. **HelpScout domain coverage**: Attribution used only `jamieyoung.com` (the corporate domain). The full domain map contains 500+ dealer/designer domains for JYC. If JYC dealers contact support using their own email domains (not @jamieyoung.com), those conversations would not be captured. The 10-conversation count may undercount total JYC-related support volume. For a more comprehensive view, a broader domain set could be used in future runs.

3. **Jira ticket ages**: Calculated from today (2026-04-20) to creation/update dates. The brief uses 2026-04-17 as the report date. Age differences of 3 days between report date and calculation date are immaterial.

4. **EBR-726 classification**: Included as a cross-reference note, not as a JYC ticket. The request originated from Braxton Culler but mentions JYC in internal notes. This is correctly flagged as relevant context rather than a JYC-originated issue.

5. **Accent color differentiation**: HTML uses blue-steel (`--accent: #4A6A8C`) as specified in the template design system, visually distinct from the external report's warm copper (`--accent: #C47A4A`). Confirmed by inspecting the CSS custom properties.
