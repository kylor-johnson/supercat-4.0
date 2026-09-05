# PITCH: Sales Portal filter truth + metric law (Phase 1 / Bet A)

**Date:** 2026-07-17 · **Program:** Sales Analytics (EBR-only)  
**Appetite:** Small batch (1–2 weeks shaping + AC; eng build only after `ISOLATION OFF`)  
**EBR in:** [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40), [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212), [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91), [EBR-87](https://supercatsolutions.atlassian.net/browse/EBR-87)  
**Shelf:** [EBR-180](https://supercatsolutions.atlassian.net/browse/EBR-180) (XL) · **Close:** [EBR-7](https://supercatsolutions.atlassian.net/browse/EBR-7)

---

## 1. Problem

**Baseline:** A rep or CSM opens Sales Portal, picks a territory on the invoice list (EBR-40) or dashboard (EBR-212), and the book is wrong — too many customers, too few, or no change. They export to Excel. Separately, exported customer sales don’t match on-screen totals (EBR-91), and quote/pipeline rows can pollute “sales” (EBR-87 / FAL trap).

**Who:** Portal users on manufacturer orgs with territory-scoped access.  
**Why now:** Computational IR under EBR-775 is worthless if filters and “sales” mean different things in UI vs export vs Insightful.

## 2. Appetite

- [x] Small batch (1–2 weeks) for **shape + AC + diagnosis handoff**  
- [ ] Big batch — only if betting table expands to XL EBR-180  

Fixed time, variable scope: ship correct filter + locked metric definition stubs — not a territory data-model rewrite.

## 3. Solution (elements)

| Element | Detail |
|---|---|
| **Places** | Sales Portal invoice list · Sales Portal dashboard (territory control) |
| **Affordance** | Territory filter that scopes the visible book and every total on that surface |
| **Metric law stubs** | “Sales” = `SUM(portal_invoices.net_amount)` RTD-clamped + $5M cap; exports must reconcile (EBR-91); quotes excluded from sales (EBR-87) |
| **EBR-7 disposition** | Document close — discounts already reflected in `net_amount` (Prod-Council denied 2022) |
| **Breadboard** | Select territory → list + summary recompute → export matches UI for same scope |

## 4. Rabbit holes (patched)

| Risk | Patch |
|---|---|
| Multi-territory comma RepNumber (EBR-180) | **Out of this pitch** — XL shelf; downstream SERV-2178/2180 |
| Empty `territories` master (32/55 orgs) | Filter truth ≠ inventing a territory master; don’t promise named rollups where master is empty |
| Warehouse dashboard ≠ invoiced spine | Label which spine; IR AC uses invoiced only |
| iPad / eOL-only date bugs | Out of program — do not pull SERV-2395 into this pitch |

## 5. No-gos

- Starting EBR-180 / schema+ETL without separate appetite GO  
- New Intelligence Report heroes in this bet  
- LLM / EBR-772  
- iPad tickets (EBR-36, 655, 743)  
- Rails implementation while isolation ON  

## Done means

1. ~~One written diagnosis + AC~~ → **`FILTER-TRUTH-AC.md`** (AC-A1…A4).  
2. Metric-law AC stubs from EBR-91 / EBR-87 in FILTER-TRUTH-AC + IR v1.  
3. EBR-7 close recommendation in `JIRA-HYGIENE-COMMENTS.md`; **Kylor** applies in Jira.  
4. Eng work only after Kylor: `ISOLATION OFF — GO on <EBR-40|EBR-212>`.

## DDD lock

| Term | Means | Not |
|---|---|---|
| Sales / topline | Invoiced `net_amount` | Booked `portal_orders.total_amount`, quotes |
| Territory filter | Scopes portal reporting book | iPad shared drafts / order email CC |
| Export total | Same spine + same scope as UI | A second warehouse definition |

**Bounded context:** Portal Reporting. **ACL:** ERP `invoice_data.csv` / `order_data.csv` → `portal_invoices` / `portal_orders`.

---

*Pitch ready for betting table. Next: UX brief (parallel) → IR v1 AC under EBR-775.*
