# Bet C — IR v1 stamped queries (C1 + S1 + team strip)

**Date:** 2026-07-17 · **Epic:** EBR-775 · **Isolation:** ON (read-only Postgres)  
**AC:** `INSIGHT-IR-v1-AC.md` · **Canon:** Insightful 4.0 `selling_customer_exception_layer.md`, `query_library_v2.md`  
**Demo org stamped:** `sarreid` (org_id=1) · RTD = **2026-07-17**

---

## Preflight

Run Insightful `Q-ECON-00` first. Suppress commerce heroes when `COMMERCE_CONFIDENCE = NONE`.  
All windows anchor on `report_through_date`, not bare `CURRENT_DATE`.

---

## C1 — True Topline

**Law:** `SUM(portal_invoices.net_amount)` over RTD-clamped trailing 12 months; $5M row cap in Insightful factory.

**Live (sarreid, 2026-07-17):**

| Metric | Value |
|---|---|
| LTM invoiced net | **$16,022,554** |
| Invoice count | 11,730 |
| Active bill-tos | 1,417 |
| Confidence | STRONG (single invoice feed) |

**cci grade target (cycle-02):** ~$71.23M LTM — re-stamp at build time.

---

## S1 — Quietly dying (EBR-198)

**Authority SQL:** `Insightful Product 4.0/foundation/selling_customer_exception_layer.md` (equal 6mo vs prior 6mo; `$ at risk` = account LTM; who-to-call = `rep_number`, name only at Tier 2).

**Decay rule used for portal v1 hero table:** `r_prior > 0 AND r_recent < 0.6 * r_prior` (≥40% half-over-half drop).  
Full S1 also includes early-dormancy OR-clause — keep that in factory; **hero table leads with decay** so accelerating whales don’t sit in row 1.

### Live stamp — sarreid decay cohort (2026-07-17)

| Metric | Value |
|---|---|
| Flagged decaying accounts | **25** |
| $ at risk (sum LTM on flagged) | **$1,690,587** |

**Top 5 by LTM at-risk (masked names in UI):**

| Account | Prior 6mo | Recent 6mo | Δ | At risk (LTM) | Call |
|---|---|---|---|---|---|
| 29925 | $287,269 | $112,886 | −60.7% | $400,154 | Rep 546 |
| 32162 | $189,198 | $95,374 | −49.6% | $284,572 | Rep 022 |
| 31098 | $115,126 | $68,488 | −40.5% | $183,614 | Rep 546 |
| 11077 | $54,598 | $32,035 | −41.3% | $86,633 | Rep 556 |
| 32530 | $60,186 | $5,986 | −90.1% | $66,172 | Rep 099 |

**Reproduce (read-only):** substitute `organization_id` / RTD; use canon CTE from exception layer; filter `r_recent < 0.6*r_prior`; `ORDER BY ltm_rev DESC LIMIT 12`.

---

## Team strip — behavior floor (not Universe E)

### Q-R1 — seats / cadence (always)

Authority: `query_library_v2.md` § Q-R1.

**Live stamp — sarreid (2026-07-17):**

| Field | Value |
|---|---|
| Active seats (`last_ipad_login_at` set, not disabled) | **105** |
| Logins ≤30d | **42** |
| Quiet 31–90d | **16** |
| Dark >90d | **47** |
| Distinct order authors (90d) | **24** |
| Writers with confirmed eCat order (30d) | **15** |
| Confirmed eCat orders (30d) | **55** |
| Total org_users rows | 144 (enabled 124) |

**UI mapping for v1 strip:**

- Active seats → Q-R1 `active_seats` (or logins_30d — pick one label and stick; demo uses **42 logins / 105 active seats**)  
- Writing orders → writers_30d (**15**)  
- Going quiet → quiet_seats + dark framing; demo callout uses **16 quiet (31–90d)** + note dark separately  

### Q-18 — eCat GMV leaderboard (when orders exist)

**Live stamp — sarreid top writers by confirmed eCat GMV, last 30d (rep_number):**

| Rep | Orders | GMV |
|---|---|---|
| 015 | 7 | $54,798 |
| 056 | 10 | $42,774 |
| 010 | 8 | $23,663 |
| 030 | 6 | $15,345 |

**Forbidden in v1 default:** RS-01 named invoiced-rep revenue leaderboard.

---

## Grade orgs

Re-run this file’s queries on **`cci` + `kll`** before AC freeze / build. Demo orgs remain `sarreid` + `ufi`.

---

## Done criterion (from IR AC)

Spec + AC + **this stamped SQL/read-model** that reconciles to portal invoice math on a live org.  
Build only after UX feedback (if run) and `ISOLATION OFF — GO on EBR-775`.

---

*Closes SPEC-GAP C8 (and grounds C6/C7). Update numbers when RTD moves.*
