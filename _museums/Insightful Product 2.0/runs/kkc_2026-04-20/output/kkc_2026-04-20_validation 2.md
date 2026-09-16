# Validation Report — Kindel Karges Furniture
*April 20, 2026 · Internal Brief QA*

## Summary
- **Overall**: PASS
- **Checks run**: 23 / 23
- **Failures**: 0
- **Degradation notes**: Support data (V2) and Jira data (V3) are structurally unavailable — validated as correctly handled degradation, not failures.

## V1: Health Data Integrity
- [x] health_score: CSV=56, Brief=56 ✓
- [x] health_band: CSV=Watch, Brief=Watch ✓
- [x] engagement_score: CSV=50, Brief=50 ✓
- [x] adoption_score: CSV=57, Brief=57 ✓
- [x] value_delivery_score: CSV=40, Brief=40 ✓
- [x] operational_health_score: CSV=100, Brief=100 ✓
- [x] trajectory_score: CSV=50, Brief=50 ✓
- [x] classification: CSV=Intervene, Brief=Intervene ✓
- [x] churn_risk: CSV=False, Brief=False (correctly reported as "No churn risk flag set") ✓
- [x] expansion_ready: CSV=False, Brief=False (correctly reported as "Not expansion ready") ✓
- [x] risk_modifier_applied: CSV=(empty), Brief="No risk modifiers fired" ✓
- [x] hs_lifecycle_stale: CSV=True, Brief=True (prominently flagged in Flags section and Verdict) ✓
- [x] hs_join_missing: CSV=False, Brief=False ✓
- [x] arr_data_gap: CSV=False, Brief=False ✓
- [x] bundle: CSV=iPad-only, Brief=iPad-only ✓

## V2: Support Data Integrity
- [x] HelpScout data unavailable: correctly identified — no email domain mapping for `kkc` in `pg_domain_map.csv` ✓
- [x] Brief Section 3 correctly notes degradation: "Support data unavailable — no email domain mapping" ✓
- [x] Verdict correctly notes support gap: "no support history is attributable" ✓

**Note**: No Q-IB-HELP-AGG re-run was possible because the prerequisite email domain resolution returned zero domains. This is the expected degradation path per the operator spec.

## V3: Jira Data Integrity
- [x] Jira search performed with correct cloud ID (`3aea3e61-c30d-422a-9b0e-b5bab9b4c92a`) ✓
- [x] Search by client name: `text ~ "Kindel" AND statusCategory != Done` → 0 results. Correctly reported. ✓
- [x] Search by shortname: `text ~ "kkc" AND statusCategory != Done` → 0 results. Correctly reported. ✓
- [x] Brief Section 4 correctly notes "No Jira tickets found" with search strategies documented ✓

## V4: Cross-Contamination Check
- [x] Searched brief text for foreign org_shortnames — none found. All references are to `kkc`, "Kindel Karges Furniture", or "Kindel" ✓
- [x] Header references correct client: "Kindel Karges Furniture" ✓
- [x] Footer references correct client: "Kindel Karges Furniture" ✓
- [x] File names: `kkc_2026-04-20_internal_brief.md`, `kkc_2026-04-20_internal_brief.html` — correct ✓

## V5: Internal Consistency
- [x] Verdict references health score (56), classification (Intervene), HubSpot stale flag — all appear in Section 2 ✓
- [x] "Three Things That Matter" trace to specific findings:
  - Item 1 (HubSpot stale) → Section 2 Flags ✓
  - Item 2 (Value Delivery 40) → Section 2 Dimensions table ✓
  - Item 3 (13 stale config entities) → Section 5 Meeting Playbook + external report cross-reference ✓
- [x] "Not in the External Report" items verified against external report (`kkc_2026-04-20_intelligence_report.html`):
  - Health score: not present in external report ✓
  - HubSpot stale flag: not present in external report ✓
  - Support history: not present in external report ✓
  - Jira work: not present in external report ✓
  - Parent entity: not present in external report ✓
- [x] SuperCat Action Items supported by findings:
  - "Establish email domain mapping" → Section 3 documents missing domain map ✓
  - "Enable Clicky Analytics" → org_summary confirms `has_clicky_portal = false` ✓
  - "Update HubSpot lifecycle status" → Section 2 Flags documents `hs_lifecycle_stale = True` ✓
  - "Refresh stale configuration data" → External report documents 13 stale entities ✓
  - "Confirm bundle classification" → External report header says "iPad + Catalog + Portal", Health V2 says "iPad-only" ✓

## V6: HTML Parity
- [x] HTML file exists alongside markdown: `kkc_2026-04-20_internal_brief.html` ✓
- [x] Spot-check 1 — Health score: Markdown="56", HTML="56" ✓
- [x] Spot-check 2 — Open ticket count: Markdown="0" (no data), HTML="0" (empty table) ✓
- [x] Spot-check 3 — Jira ticket count: Markdown="0" (no tickets found), HTML="0" (empty table with search strategies) ✓
- [x] HTML header shows correct client name: "Kindel Karges Furniture" ✓
- [x] HTML header shows correct date: "April 20, 2026" ✓
- [x] HTML header shows correct bundle: "iPad-only" ✓

## Notes

1. **Growth components intentionally omitted**: Per user directive, growth score, growth band, and growth components section were excluded from the brief. Classification (Intervene) is retained as it reflects the Health × Growth quadrant — the Intervene classification is accurate (Health 56 < 60, Growth 43 < 60).

2. **Bundle discrepancy flagged**: The external Customer Intelligence Report identifies Kindel's bundle as "iPad + Catalog + Portal" in its header, but the Health V2 CSV (authoritative source) and Master Account List both classify it as "iPad-only." This is flagged as a SuperCat action item. If the MAL is incorrect, updating it would change which features count toward Adoption and how Value Delivery is calculated — potentially shifting the health score.

3. **Support and Jira both unavailable**: This is the most degraded brief possible while still being generatable (Health V2 data is present, which is the only blocking requirement). The brief correctly handles both degradation paths per the operator spec — noting unavailability in the relevant sections and in the Verdict.

4. **hs_lifecycle_stale concern**: This flag is prominently surfaced across the Verdict, Flags section, Meeting Playbook, and action items. For an Intervene-classified account, the combination of stale HubSpot lifecycle and no support/Jira visibility is a significant organizational risk — the account may be genuinely disengaging with no internal detection mechanism in place.

5. **Operational Health score of 100 is somewhat misleading**: The Health V2 model scores import success, catalog completeness, and data freshness at the product/customer/inventory level. Kindel scores 100 because the product catalog is complete and imports are clean. However, the external report identifies 13 stale configuration entities (options, finishes, price levels) that the health model does not capture. This is noted in the Dimensions table explanation.
