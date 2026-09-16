# Validation Report — Hubbardton Forge
*April 20, 2026 · Internal Brief QA*

## Summary
- **Overall**: PASS
- **Checks run**: 24 / 24
- **Failures**: 0

---

## V1: Health Data Integrity

Source: `Health V2/runs/2026-04-14_v2.5.1/client_health_scores_2026-04-14.csv`, row 68 (`org_shortname = 'hfg'`)

- [x] health_score: CSV=82, Brief=82 ✓
- [x] health_band: CSV=Thriving, Brief=Thriving ✓
- [x] engagement_score: CSV=60, Brief=60 ✓
- [x] adoption_score: CSV=100, Brief=100 ✓
- [x] value_delivery_score: CSV=90, Brief=90 ✓
- [x] operational_health_score: CSV=70, Brief=70 ✓
- [x] trajectory_score: CSV=90, Brief=90 ✓
- [x] classification: CSV=Maintain, Brief=Maintain ✓
- [x] churn_risk: CSV=False, Brief="No churn risk" ✓
- [x] expansion_ready: CSV=False, Brief="No expansion-ready flag" ✓
- [x] risk_modifier_applied: CSV=(empty), Brief="No risk modifiers fired" ✓
- [x] hs_lifecycle_stale: CSV=False, Brief=false ✓
- [x] hs_join_missing: CSV=False, Brief=false ✓
- [x] arr_data_gap: CSV=False, Brief=false ✓

**Note**: Growth components (growth_score=52, growth_band=Developing, bundle_upgrade_signal=75, feature_gap_score=50, customer_headroom_score=0, peer_benchmark_gap=20) intentionally omitted per operator instruction. Confirmed absent from both markdown and HTML.

---

## V2: Support Data Integrity

Source: Re-run of Q-IB-HELP-AGG (180-day window) on 2026-04-20.

- [x] Total conversations: Query=3 (180-day), Brief="3 total" ✓
- [x] 90-day count noted as 2 with extension: Query=2 (90d), Brief="2 conversations in 90 days (extended to 180 days)" ✓
- [x] Open tickets: Query=0 active, Brief="Open Tickets (0)" ✓
- [x] Theme ticket counts: 3 tickets in 1 theme ≤ 3 total ✓
- [x] Escalation profile: Query=1 L3 (escalations_l2_plus=1), theme data=2 L1 + 1 L3, Brief="2 L1, 1 L3" ✓ (counts are consistent: 2 L1 + 1 L3 = 3 tagged conversations)

**Note**: 1 ticket has status "pending" (not "active" or "closed") — "Re: Help with Option $ add-ons". Brief correctly notes this as "1 ticket in 'pending' status" separate from the open ticket table. This is a HelpScout-specific status meaning customer-response awaited.

---

## V3: Jira Data Integrity

Source: Jira MCP `searchJiraIssuesUsingJql` results from 2026-04-20.

- [x] ECAT-436: URL=`https://supercatsolutions.atlassian.net/browse/ECAT-436` — correct domain and key format ✓
- [x] ECAT-436 summary: Jira="Include Smart String in Order", Brief="Include Smart String in Order" ✓
- [x] ECAT-436 status/priority: Jira=To Do/High, Brief=To Do/High ✓
- [x] ECAT-259: URL=`https://supercatsolutions.atlassian.net/browse/ECAT-259` — correct ✓
- [x] ECAT-259 summary: Jira="Provide an easy way to print barcode tags - iPad", Brief="Provide an easy way to print barcode tags — iPad" ✓ (dash vs em-dash is HTML rendering)
- [x] ECAT-259 status/priority: Jira=To Do/High, Brief=To Do/High ✓
- [x] ECAT-475: URL=`https://supercatsolutions.atlassian.net/browse/ECAT-475` — correct ✓
- [x] ECAT-475 summary: Jira="eCat: Reimplement matrix option item codes in terms of smart strings", Brief="Reimplement matrix option item codes in terms of smart strings" ✓ (prefix "eCat:" dropped for conciseness — acceptable)
- [x] ECAT-475 status/priority: Jira=To Do/Low, Brief=To Do/Low ✓

---

## V4: Cross-Contamination Check

- [x] Searched brief text for all org_shortnames that are NOT "hfg" — none found ✓
- [x] Client names mentioned (CED, ILC Studios, IDC, Hotel Design Group, One Source Distributors, Beyer Brown, Gannon Sales Agency) are all HFG *customers* referenced from the external report — not other scored entities ✓
- [x] Header: "Hubbardton Forge" ✓
- [x] Footer: "Hubbardton Forge" ✓
- [x] File names: `hfg_2026-04-20_internal_brief.md`, `hfg_2026-04-20_internal_brief.html` ✓

---

## V5: Internal Consistency

- [x] Verdict references health=82, adoption=100, VD=90, trajectory=90 — all appear in Section 2 (Health at a Glance) ✓
- [x] "Three Things That Matter" item 1 ($869K dormant accounts) traces to Section 5 (Meeting Playbook talking point 1, sourced from external report) ✓
- [x] "Three Things That Matter" item 2 (3 Jira tickets) traces to Section 4 (Active Engineering & Projects) — all 3 tickets listed ✓
- [x] "Three Things That Matter" item 3 (stale config data, OpHealth=70) traces to Section 2 (Operational Health dimension "Why") ✓
- [x] "Not in the External Report" items verified against external report: health score, classification, support history, Jira tickets, ARR — all confirmed absent from `hfg_2026-04-20_intelligence_report.html` ✓
- [x] SuperCat Action Items are supported by findings:
  - "Refresh stale configuration data" → Operational Health=70, stale data referenced in Section 2 ✓
  - "Decide on dormant Jira tickets" → 3 stale tickets in Section 4 ✓
  - "Prepare dormant account reactivation talking points" → external report priority action referenced in Section 5 ✓

---

## V6: HTML Parity

- [x] HTML file exists: `hfg_2026-04-20_internal_brief.html` confirmed ✓
- [x] Health score: Markdown=82, HTML=82 ✓
- [x] Open ticket count: Markdown=0, HTML=0 ✓
- [x] Jira ticket count: Markdown=3, HTML=3 ✓
- [x] HTML header: client name="Hubbardton Forge" ✓, date="April 20, 2026" ✓, bundle="iPad+Catalog+Portal" ✓
- [x] HTML uses blue-steel accent (`--accent: #4A6A8C`) — visually distinct from external report ✓
- [x] HTML includes "INTERNAL USE ONLY" banner ✓

---

## Notes

1. **Growth components removed by design**: Per operator instruction, growth_score, growth_band, and the Growth Components section were intentionally excluded from the brief. The CSV values (growth_score=52, growth_band=Developing) were not included. Classification (Maintain) was retained as it is derived from both health and growth but is a classification label, not a growth metric itself.

2. **HelpScout window extension**: The 90-day window yielded only 2 conversations (below the 3-conversation threshold in the operator spec). The brief correctly extended to 180 days and notes this in the summary one-liner. The 180-day window yielded 3 conversations — still a thin sample, but sufficient for theme analysis.

3. **Jira ticket age**: All 3 tickets are 3–4+ years old with no updates in 1,100–1,459 days. These are legacy feature requests, not active engineering work. The brief correctly characterizes them as "dormant feature requests" and flags the stale status prominently.

4. **Pending vs. Active HelpScout status**: 1 conversation has HelpScout status "pending" (not "active"), meaning the ball is in the customer's court. The aging query (`status = 'active'`) correctly returns 0, and the brief correctly notes the pending ticket separately. This is accurate behavior.

5. **Classification note**: The Maintain classification depends on Health ≥ 60 and Growth < 60 (CSV: health=82, growth=52). While growth components are removed from the brief, the classification label "Maintain" is retained as it describes the operational action mode, not growth potential itself.
