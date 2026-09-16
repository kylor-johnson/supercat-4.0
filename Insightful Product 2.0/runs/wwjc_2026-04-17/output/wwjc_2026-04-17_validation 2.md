# Validation Report — Wildwood/Chelsea House
*2026-04-20 · Internal Brief QA*

## Summary
- **Overall**: PASS
- **Checks run**: 24 / 24
- **Failures**: 0

---

## V1: Health Data Integrity
- [x] Re-read Health V2 CSV row for `wwjc` — confirmed present at line 65
- [x] health_score: CSV=76, Brief=76 ✓
- [x] engagement_score: CSV=40, Brief=40 ✓
- [x] adoption_score: CSV=90, Brief=90 ✓
- [x] value_delivery_score: CSV=85, Brief=85 ✓
- [x] operational_health_score: CSV=100, Brief=100 ✓
- [x] trajectory_score: CSV=80, Brief=80 ✓
- [x] classification: CSV=Maintain, Brief=Maintain ✓
- [x] health_band: CSV=Healthy, Brief=Healthy ✓
- [x] churn_risk: CSV=False, Brief="None" ✓
- [x] expansion_ready: CSV=False, Brief="No" ✓
- [x] risk_modifier_applied: CSV=(empty), Brief="None applied" ✓

**Note**: `score_explanation` was adapted to remove growth score reference per user instruction (growth components excluded from brief). Original CSV: "76 Health / 50 Growth → Maintain". Brief: "76 Health → Maintain". This is an intentional adaptation, not a data error.

---

## V2: Support Data Integrity
- [x] Re-ran Q-IB-HELP-AGG: total_conversations=8. Brief summary says "8 conversations in 90 days" ✓
- [x] Open tickets: Q-IB-HELP-AGING returned 0 active tickets. Brief table shows 0 active, 1 pending ✓ (pending is a distinct HelpScout status, not "active")
- [x] Theme ticket counts: User Management (4) + Data & Integration (2) + Product & Feature Requests (2) = 8. Sum equals total ✓
- [x] Escalation profile: L1=6, L3=2. Total=8 conversations with escalation tags. Brief says "6 L1, 2 L3" ✓. Consistent with Q-IB-HELP-THEMES data: `l1 - handled by frontline support` (6), `l3 - engineering intervention` (2).

**Note**: Q-IB-HELP-AGG counted `open_conversations=0` (status='active' only). One conversation (#3291979476 "Sales Order Data") has status='pending', which is a distinct HelpScout state meaning "awaiting client response." The brief correctly distinguishes "0 active, 1 pending." The validation re-run confirmed: total=8, closed=7, pending=1, active=0.

---

## V3: Jira Data Integrity
- [x] CSP-36: URL `https://supercatsolutions.atlassian.net/browse/CSP-36` ✓, Summary "Purge and rebuild sales_data" matches Jira ✓, Status "To Do" ✓, Priority "Medium" ✓
- [x] EBR-728: URL `https://supercatsolutions.atlassian.net/browse/EBR-728` ✓, Summary "Sales rep activity logging (visits)" matches ✓, Status "Submitted" ✓, Priority "Unprioritized" ✓
- [x] SERV-1637: URL ✓, Summary "Sales Totals filter" matches ✓, Status "To Do" ✓, Priority "High" ✓
- [x] EBR-542: URL ✓, Summary "Brandwise integration" matches ✓, Status "Triaging" ✓, Priority "High" ✓
- [x] EBR-450: URL ✓, Summary matches (abbreviated in brief as "Credit card capture at eOL checkout") ✓, Status "Triaging" ✓, Priority "Medium" ✓
- [x] SERV-278: URL ✓, Summary matches (abbreviated in brief) ✓, Status "To Do" ✓, Priority "Unprioritized" ✓

All 6 Jira keys verified against API response. URLs follow correct pattern.

---

## V4: Cross-Contamination Check
- [x] Searched entire brief text for org_shortnames/org_names that are NOT `wwjc` or `Wildwood/Chelsea House`. None found. Names referenced (Lyteworks, Brubaker's Design, Tammy Preusse, Mike Studley, Daniel Ratchford, Whit Barnes, Savoy House) are all people/entities associated with the Wildwood account or co-mentioned in Jira tickets originating from this client's context.
- [x] Header: "Wildwood/Chelsea House" ✓
- [x] Footer: "Wildwood/Chelsea House" ✓
- [x] File names: `wwjc_2026-04-17_internal_brief.md`, `wwjc_2026-04-17_internal_brief.html` ✓

**Note**: EBR-450 mentions "Savoy House" (another client co-requesting the same feature). This is a genuine Jira artifact, not cross-contamination — the ticket was created for a feature requested by multiple clients. The brief does not attribute Savoy House data to Wildwood.

---

## V5: Internal Consistency
- [x] Verdict references data that appears in Sections 2–5:
  - "Health scores 76 (Healthy)" → Section 2 ✓
  - "Engagement at 40 (Watch)" → Section 2 dimension table ✓
  - "80% of orders flow through buyer self-service" → Section 2 Value Delivery explanation ✓
  - "CSP-36 is logged" → Section 4 Jira table ✓
  - "7,044 lapsed accounts" → Section 5 (from external report) ✓
- [x] "Three Things That Matter" items each trace to a specific section finding:
  1. "7,044 lapsed accounts" → External report finding referenced in Section 5 Talking Points ✓
  2. "Sales data purge request" → Section 3 (Support theme #2) + Section 4 (CSP-36) ✓
  3. "Engagement score masks strong health" → Section 2 (Engagement dimension at 40) ✓
- [x] "Not in the External Report" items are genuinely absent from the external report (spot-checked against `wwjc_2026-04-17_intelligence_report.html`):
  - Health score (76) — not in external report ✓
  - Support history — not in external report ✓
  - CSP-36 status — not in external report ✓
  - Clicky Analytics status — not in external report ✓
  - Jira backlog — not in external report ✓
- [x] SuperCat Action Items are supported by findings:
  - "Enable Clicky Analytics" → org_summary `has_clicky_portal=false` ✓
  - "Close the sales data purge loop" → CSP-36 in Jira + HelpScout #3291979476 ✓
  - "Offer 12-entity config data refresh" → External report finding (12 stale entities, 240 days) ✓
  - "Triage stale Jira backlog" → EBR-728 (62d stale), 4 older tickets (800+d) ✓

---

## V6: HTML Parity
- [x] HTML file exists at `wwjc_2026-04-17_internal_brief.html` alongside markdown ✓
- [x] Spot-check: Health score — MD=76, HTML=76 ✓
- [x] Spot-check: Open ticket count — MD="0 active, 1 pending", HTML="0 active, 1 pending" ✓
- [x] Spot-check: Jira ticket count — MD=6 tickets (2 recent + 4 backlog), HTML=6 tickets (2 recent + 4 backlog) ✓
- [x] HTML header shows correct client name ("Wildwood/Chelsea House"), date ("2026-04-20"), and bundle ("Full") ✓

---

## Notes

1. **Growth components intentionally excluded**: Per user instruction, Growth Score, Growth Band, and Growth Components section were removed from both MD and HTML briefs. Classification (Maintain) is still shown as it's a derived field. The score_explanation was adapted to remove the "50 Growth" reference.

2. **HelpScout domain coverage**: Attribution used 4 core company domains (`wildwood.com`, `wildwoodhome.com`, `wildwoodlamps.com`, `chelseahouseinc.com`). The full `pg_domain_map.csv` contains 487+ domains for wwjc (including all dealer/customer email domains), but the core company domains captured 8 conversations in 90 days — sufficient for theme analysis.

3. **Pending vs Active HelpScout status**: The Q-IB-HELP-AGING query (which filters `status = 'active'`) returned 0 rows, but one conversation (#3291979476 "Sales Order Data") has status='pending'. This is a recognized HelpScout status meaning "awaiting client response" and is correctly noted in the brief as a distinct state.

4. **Jira backlog age**: Four Wildwood tickets are 800+ days old with no recent activity. These are historical feature requests / enhancements that have likely been deprioritized or superseded. The brief recommends triaging them for closure.

5. **External report cross-reference**: The external report (`wwjc_2026-04-17_intelligence_report.html`) was successfully used for Meeting Playbook cross-references. Key findings incorporated: 7,044 lapsed accounts, 50.2% capture rate, 12 stale data entities, Daniel Ratchford territory analysis, and 80% eCat Online order share.
