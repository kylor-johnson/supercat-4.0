# INSIGHT — Intelligence Report v1 Acceptance Criteria (Bet C)

**Date:** 2026-07-17 · **Epic:** [EBR-775](https://supercatsolutions.atlassian.net/browse/EBR-775)  
**Lane:** 2 Computational · **Isolation:** ON (spec only until GO)  
**Supersedes cycle-01** topline+concentration-only scope for program bets.

> **Bet F persona note (footnote — no AC change).** Intelligence (C1 + S1 + team strip) is the **owner-leaning surface**; persona priority for who leads on it is shaped in Bet F (`IA-PRIORITY-MATRIX.md`, rules R2/R5). Bet F adds **no new metric law**: RS-01 named invoiced-rep revenue stays gated (never a v1 default lead; suppressed below Tier 2 per AC-3), and the STRONG-not-FULL ceiling holds. This AC body is unchanged.

---

## Metric law (locked)

- Revenue = `SUM(portal_invoices.net_amount)` over RTD-clamped window; $5M single-row cap.  
- Confidence ceiling **STRONG** (single feed); never claim FULL completeness.  
- Quotes never in sales ([EBR-87](https://supercatsolutions.atlassian.net/browse/EBR-87)).  
- UI total and export for same scope must reconcile ([EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91)).  
- [EBR-7](https://supercatsolutions.atlassian.net/browse/EBR-7) answered by `net_amount` — no separate discount build.  
- Preflight: `Q-ECON-00` → `COMMERCE_CONFIDENCE` + `report_through_date`.

---

## v1 heroes

### AC-1 — True Topline (C1)
- Given org with live invoice feed, emit LTM invoiced net at STRONG with single-feed caveat.  
- Window ends at `report_through_date`, not `CURRENT_DATE`.  
- Reproducible on `sarreid` / `cci` within rounding of cycle-02 LTM figures (~$15.98M / ~$71.23M).  
- Suppress when `COMMERCE_CONFIDENCE = NONE`.

### AC-2 — Quietly dying accounts (S1 / [EBR-198](https://supercatsolutions.atlassian.net/browse/EBR-198))
- Equal 6mo vs prior-6mo decay + cadence gap; $-at-risk = account LTM.  
- Who-to-call uses named rep only at Tier 2; else `rep_number` or omit name.  
- Must not use 6-vs-18 false-flag form.  
- Canonical: `selling_customer_exception_layer` / CAPABILITY #5.

### AC-3 — Team strip (behavior floor)
- Always: Q-R1 active seats / login cadence / quiet reps.  
- Leaderboard: Q-18 (eCat GMV) when orders exist; else Q-01 engagement fallback.  
- Mixpanel depth (Q-63/64/65) only when Mixpanel CORROBORATED; else degrade.  
- **Forbidden in v1 default:** RS-01 named invoiced-rep revenue leaderboard.

### AC-4 — Concentration (optional / degrade)
- If shown: top1/top10 + “healthy diversification” when `top1_share < 0.20`.  
- Billing-entity grain only. Not required if S1 ships as hero 2.

### AC-5 — Provenance stamps
Every number carries `{confidence, feed_completeness, total_business_source, report_through_date}`.

---

## Grade / demo orgs

| Role | Org |
|---|---|
| Grade | `cci` + `kll` (Tier-0) |
| Demo | `sarreid` + `ufi` |

---

## No-gos

- [EBR-772](https://supercatsolutions.atlassian.net/browse/EBR-772) / [EBR-776](https://supercatsolutions.atlassian.net/browse/EBR-776)  
- Peer benchmarks, margin/COGS, FULL completeness claims  
- "$0 returns" on gross-only feeds  
- Leading with Universe E (invoiced named-rep revenue)  
- Absorbing deferred EBRs (213, 629, 197, 278) into v1 without reshaping  

---

## Absorb later (not v1)

EBR-197 (items) · EBR-278 (territory analytics) · EBR-213 (quota, sarreid-only) · EBR-629 · EBR-687 (drill-down UX pattern) · fill leakage C4

---

## Done

Spec + AC + reproducible SQL/read-model demo that reconciles to portal invoice math on a live org. Build only after UX feedback updates AC and Kylor issues `ISOLATION OFF — GO on EBR-775` (or named surface).

**Companion:** `TECHNICAL-PLAN.md` · `IR-v1-QUERIES.md` (live-stamped SQL) · `UX-brief-c1-s1-team-strip.md` · Bet A gate: `FILTER-TRUTH-AC.md`
