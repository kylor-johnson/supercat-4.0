# Report Delivery Checklist — Insightful Product 2.0

**Use this before sending any external intelligence report to a client.**

This is the final sign-off check. If you cannot check every item below, the report is not ready to deliver. Resolve the open item or escalate.

> **Profiles retired.** There is a single report form; every check below applies to it. (Earlier versions supported `deep_intelligence` / `executive_intelligence` profiles — that branch has been removed.)

---

## Step 1 — Validate before you open the report

- [ ] The validation log for this run is filled out and filed in `qa/validation-logs/`
- [ ] The run status in the log is `COMPLETED` (not BLOCKED or PREFLIGHT-ABORT)
- [ ] The severity assessment in the log is one of:
  - Clean run
  - Log disclosures only (validation-log findings — none affect the delivered report)
  - Section caveats (specific sections degraded or omitted, rest of report is sound)
  - *If the log says "Run caveat" or "Blocked" — stop here. Resolve before delivering.*

---

## Step 2 — Open the HTML report and confirm structure

- [ ] Report opens cleanly in a browser (no broken layout, no missing CSS)
- [ ] Section order is correct for the report mode:
  - **Standard (Mode 1)**: Executive Summary → [Sales Team] → Customer & Buyer → [Product & Inventory] → Commerce → [Portal Engagement] → [Peer Benchmarking] → Platform & Feature → Appendix
  - **Activation (Mode 2)**: Activation Summary → Platform Readiness → [Peer Benchmarking if eligible] → Appendix
  - **Reactivation (Mode 3)**: Reactivation Summary → Historical Commerce → Platform Status → [Peer Benchmarking if eligible] → Appendix
- [ ] §1 Executive Summary (or Activation/Reactivation Summary) opens by default (not collapsed)
- [ ] Report header badge matches the correct mode (e.g., "Activation Stage · No eCat Commerce History")
- [ ] All other sections are present and labeled correctly
- [ ] No section is partially rendered (if a section was omitted, it is entirely absent — not empty or half-shown)

---

## Step 3 — Check the Executive / Activation / Reactivation Summary

- [ ] The summary reflects the actual findings in the body sections
- [ ] Priority Actions are present and specific (not generic advice)
- [ ] No health score, churn risk, or expansion flag language appears anywhere
- [ ] No segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) appear anywhere — these are internal-only terms that must not appear even in §7 Peer Benchmarking. Peer Benchmarking cohort is described in plain language derived from `peer_group_id_effective` — not the raw label.
- [ ] `portal_orders` is not described as buyer activity or portal ordering
- [ ] **Mode 1**: The date range is stated (e.g., "trailing 12 months: April 2025 – April 2026")
- [ ] **Mode 2**: Period label reads "Platform Configuration as of [DATE]" — no commerce date range
- [ ] **Mode 3**: Period label reads "Platform Status as of [DATE] · Last active: [DATE]" — last-active date is present
- [ ] **Executive Summary**: contains 5–6 highlights; no `<p class="prose">` before the list; Priority Actions contain 2–4 items

---

## Step 4 — Direct HTML source inspection (required — not optional)

**Before checking rendered sections, open the HTML file in a text editor or View Source in the browser and confirm zero hits on the following forbidden strings.** These are the confirmed regression leakage points. Any hit is a blocker.

| Search term | Pass condition |
|---|---|
| `<!--` | **Zero hits — no HTML comment nodes may remain in the delivered HTML.** The template contains authoring comments (`<!-- Operator: ... -->`, `<!-- BEGIN/END ... GATE -->`, `<!-- HAS_* -->`, `<!-- EXAMPLE ROW -->`, section banners) that must be stripped before delivery. A clean delivered HTML has zero comment nodes. |
| `HAS_CLICKY` | Zero hits — gating flag must not appear in delivered HTML source |
| `HAS_CART` | Zero hits |
| `HAS_INVENTORY` | Zero hits |
| `HAS_SALES_SECTION` | Zero hits |
| `HAS_PORTAL_ORDERS` | Zero hits |
| `HAS_PEER_DATA` | Zero hits |
| `ERP` | Zero hits in §1–§8 and any metric labels / notes. One hit allowed in Appendix data attribution row only (if `HAS_PORTAL_ORDERS = true`). |
| `Operational Health Score` | Zero hits — use "Data & Operational Health" for this peer benchmark row |
| `operational_health_score` | Zero hits — internal metric key, must not appear in delivered HTML |
| `health score` | Zero hits — covers sentence-level leakage in the benchmark row ("import health score at X") and top-performer prose ("lower operational health scores") |
| `health scores` | Zero hits — plural form of same prohibition |
| `Health Score` | Zero hits |
| `Health Scores` | Zero hits |
| `health_score` | Zero hits |
| `Platform-Embedded` | Zero hits |
| `Commerce-Active` | Zero hits |
| `Catalog-Focused` | Zero hits |
| `benchmark_confidence` | Zero hits |
| `peer_group_level` | Zero hits |
| `Mixpanel` | Zero hits |
| `Clicky` | Zero hits (if `HAS_CLICKY = false`); if `HAS_CLICKY = true`, may appear in Appendix attribution row only — not in report body |

**Do not proceed to Step 5 until this search is complete and all entries pass.**

## Step 4b — Check each rendered section

For every section that rendered, confirm:

- [ ] At least one time qualifier appears on key metrics ("in the trailing 12 months," "as of [date]")
- [ ] No projections or extrapolations appear without `[HYPOTHETICAL]` or `[ESTIMATED]` labels
- [ ] No Clicky references appear anywhere if §6 was absent
- [ ] Peer Benchmarking (§7), if rendered: uses plain-language cohort framing only — no confidence labels (`high`/`medium`/`low`), no tier labels (`tier1`/`tier2`/`tier3`), and no raw peer counts appear anywhere in the client-facing output; `operational_health_score` metric row uses title "Data & Operational Health" (not "Operational Health Score"); Appendix benchmark note uses plain-language description per `authority/peer_benchmark.md §7`
- [ ] VM-45 (eCat Capture Rate), if rendered: denominator validity confirmed (gate result recorded in validation log — not in Appendix)
- [ ] Sales Team (§2), if rendered: any account excluded from the rep leaderboard had stronger evidence than a name pattern alone; exclusion reason is recorded in the validation log (not in the delivered Appendix)

---

## Step 5 — Check the Appendix

The delivered Appendix contains **data source attribution only**. Every item below is a blocker if present — it belongs in the validation log, not in the delivered Appendix.

- [ ] One attribution row per data source used — plain-language name, time period or "as of [date]"
- [ ] **No report mode stated** (standard / activation / reactivation) — mode is not a client-facing disclosure
- [ ] **No run parameters, generation metadata, or platform bundle metadata**
- [ ] **No omitted-sections table or rationale** — absent sections are omitted silently; no explanation in the Appendix
- [ ] **No gating explanations** (e.g., "HAS_CLICKY = false — Portal Engagement omitted," "VM-45 skipped — Gate 2 failed")
- [ ] **No partial-sync disclosure blocks** or ERP-sync caveats
- [ ] **No standing caveat blocks** or data-quality disclaimers
- [ ] **No [ESTIMATED] explanation rows** — the inline tag in the section body is the complete disclosure
- [ ] No methodology notes, VM-45 rationale, gate flag results, or deduplication notes
- [ ] No internal identifiers: no org IDs, table names, VM codes, query IDs, row counts, dataset paths
- [ ] No Clicky deduplication disclosure, no pipeline outage notes, no validation commentary
- [ ] No operator/debug language ("package defect," "pending engineering," "Gate 2 failed," "rows confirmed," etc.)
- [ ] Peer benchmark row (if section included): "Anonymized median and percentile data from [PEER_GROUP_LABEL] accounts. No individual account data is disclosed." — plain-language description per `authority/peer_benchmark.md §7`; no confidence label, no raw peer count

> **What goes in the validation log (not the Appendix):** omitted-section reasons, VM-45 gate result and denominator ratio, `sales_quotas` staleness disclosure, showroom/operational exclusion notes, duplicate cluster flags, NULL customer_number flags, Clicky deduplication details, benchmark confidence and peer_group_n values, report mode used, gating explanations, partial-sync findings.

---

## Step 6 — Final output check

- [ ] File is named correctly: `{shortname}_{YYYY-MM-DD}_intelligence_report.html`
- [ ] File is in `runs/{shortname}_{YYYY-MM-DD}/output/` (published copy in `hosted/`)
- [ ] The report is for the correct client (shortname in filename matches content)
- [ ] The report date matches the actual run date

---

## Delivery — go / no-go

| Condition | Go / No-Go |
|-----------|-----------|
| All checklist items above are checked | ✅ Go |
| One or more items unchecked, but all are validation-log findings (not client-facing) | ✅ Go — note in delivery note to CSM |
| A section caveat exists that the CSM should be aware of | ✅ Go — brief CSM before client delivery |
| Run caveat flagged in the validation log | ⚠️ Hold — get CSM sign-off before delivering |
| Run is BLOCKED or PREFLIGHT-ABORT | 🚫 No-go — escalate, do not deliver |

---

*This checklist does not replace the full `qa/validation_runbook.md` — it is the final delivery gate only.*
*If something feels off and isn't covered here, go back to the runbook or escalate.*
