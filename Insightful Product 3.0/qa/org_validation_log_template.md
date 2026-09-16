# Org Validation Log

**System**: Insightful Product 2.0 / External Report
**Instructions**: Copy this file, rename it `org_validation_log_{shortname}_{YYYY-MM-DD}.md`, and file it in `qa/validation-logs/` when done.

---

## 1. Org Identity

| Field | Value |
|-------|-------|
| Org name | |
| Shortname | |
| Org ID | |
| Run date | |
| Validator | |

---

## 2. Minimum-Commerce Gate

| Check | Result | Notes |
|-------|--------|-------|
| LTM eCat order count | | |
| LTM `portal_orders` count | | |
| **Gate result** | PASS → standard report / FAIL → see below | |
| If failed — report mode | Activation Summary / Reactivation Summary / N/A | |

---

## 3. Preflight Gates

| Gate | Result | Detail |
|------|--------|--------|
| `HAS_CLICKY` | true / false | Prefix: |
| `HAS_CART` | true / false | Server orders confirmed: |
| `HAS_PORTAL_ORDERS` | true / false | ERP orders: &nbsp; ERP GMV: |
| `HAS_INVENTORY` | true / false | Row count: |
| `HAS_SALES_DATA` | true / false | Row count: |
| `HAS_SALES_SECTION` | true / false | Qualifying iPad reps (≥ 10 orders): |
| `HAS_PEER_DATA` | true / false | Confidence: &nbsp; Peer count: |
| Core data staleness | OK / WARN / SEVERE | Stale entities and age: |

---

## 4. VM-45 Denominator Check

*(Skip if `HAS_PORTAL_ORDERS = false`)*

| Check | Value |
|-------|-------|
| LTM eCat GMV | |
| LTM `portal_orders` GMV | |
| Gate 1: `portal_orders_gmv > ecat_gmv` | PASS / FAIL |
| Gate 2: `ecat_gmv ≥ 5%` of `portal_orders_gmv` | PASS / FAIL |
| **VM-45 result** | RENDERS (capture rate: %) / SKIPPED — reason: |

---

## 5. Anomaly Scan

| Anomaly | Observed? | Details |
|---------|-----------|---------|
| Partial ERP sync (VM-45 denominator invalid) | Yes / No | |
| Zero-commerce or deeply lapsed account | Yes / No | Last order date: |
| Duplicate quote clusters | Yes / No | Clusters found: |
| Rapid resubmission (4+ orders < 10 min) | Yes / No | |
| Zero-dollar orders | Yes / No | Count and % of total: |
| Showroom / internal account submitters | Yes / No | Accounts and GMV flagged: |
| Numeric buyer-ID server orders | Yes / No (expected for B2B Cart) | |
| NULL `customer_number` on high-value orders | Yes / No | |
| OOS items with NULL ERP sales history | Yes / No | |
| Monthly GMV spike (single month > 50% LTM) | Yes / No | Month and context: |
| Catalog visibility gap (`hideable = NULL` pattern) | Yes / No | Null count vs. total active: |
| `sales_quotas` stale | Yes — standing disclosure | Age in days: |
| Additional stale entities | Yes / No | Entities and age: |
| Clicky row-duplication | Yes / No / N/A | Max rows per date: |
| Clicky cross-account gap window | Yes / No / N/A | Window and orgs affected: |
| **New anomaly class observed?** | Yes / No | If yes — describe: |

---

## 6. Sections Rendered

| Section | Status | Notes / Reason if omitted |
|---------|--------|--------------------------|
| §1 Executive Summary | Rendered / Activation summary / Reactivation summary | |
| §2 Sales Team Performance | Rendered / Omitted | |
| §3 Customer & Buyer Intelligence | Rendered / Omitted | |
| §4 Product & Inventory Intelligence | Rendered / Omitted | |
| §5 Commerce Analytics | Rendered / Omitted | |
| §5 VM-45 (eCat Capture Rate) | Rendered / Skipped | |
| §5 VM-19 (Channel Mix) | Rendered / Skipped | |
| §6 Portal Engagement | Rendered / Absent (HAS_CLICKY = false) | |
| §7 Peer Benchmarking | Rendered / Omitted | Confidence: |
| §8 Platform & Feature Utilization | Rendered / Omitted | |
| §9 Appendix | Rendered | |

---

## 7. Report Output

| Field | Value |
|-------|-------|
| HTML report path | `runs/{shortname}_{date}/output/{shortname}_{date}_intelligence_report.html` |
| Markdown artifact | Path / Not generated |
| **Run status** | COMPLETED / PREFLIGHT-ABORT / BLOCKED |
| System fixes applied during run? | Yes / No — if yes, describe: |

---

## 8. Severity Assessment

*(Choose one — use the caveat/blocker guide in the runbook if unsure)*

| Assessment | Check if applies |
|------------|-----------------|
| Clean run — no significant issues | ☐ |
| Log disclosures only — validation-log findings only; none affect the delivered report | ☐ |
| Section caveats — one or more sections degraded or omitted; rest of report is sound | ☐ |
| Run caveat — a data issue affects overall reliability; CSM review recommended before delivery | ☐ |
| Blocked — run aborted or report cannot be delivered without escalation | ☐ |

---

## 9. Follow-Up

*(What needs to happen before this report is delivered or the next run for this org?)*

- 
- 

---

*File this log in: `Insightful Product 2.0/qa/validation-logs/`*
