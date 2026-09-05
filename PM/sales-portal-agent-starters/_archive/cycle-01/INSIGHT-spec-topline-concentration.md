# INSIGHT / Lane 2 — Computational Intelligence Report v1 Spec (Bet C)

**Date:** 2026-07-16
**Lane:** 2 (Smart / Computational)
**Bet:** C — Computational Intelligence Report surface v1
**Scope this doc:** Hero 1 **True Topline** + Hero 3 **Concentration / single-account risk**. (Hero 4 Fill Leakage noted as next.)
**Isolation:** ON — spec/AC/markdown + read-only Postgres prototype only. No Insightful pipeline code changes, no Rails.
**Computational only.** No LLM / NL query / EBR-772 agentic layer in this bet.

## Metric law (inherited from the Provenance Spine — do not restate/fork)
- **Revenue spine = invoiced net:** `SUM(portal_invoices.net_amount)` over a clamped window. `net_amount` is client-facing invoiced total, **negative for credit memos** (returns net out). `portal_invoices.total_amount` is **not** the sales figure. (provenance_spine §1)
- **Confidence + completeness on every number.** Economics ceiling is **STRONG** on a single invoice feed — `FULL` is unreachable without `FEED_COMPLETENESS = CORROBORATED`. Every total carries the single-feed caveat. (§5, §6.3, §6.8)
- **Date clamp (R1):** `report_through_date = MAX(invoice_date) WHERE invoice_date <= CURRENT_DATE`. LTM = trailing 12 months ending at `report_through_date`, never `CURRENT_DATE`. (§6.4, §6.8 R1) Live hazard: `clm` had an invoice dated 4107, `jyc` 2032.
- **`$5M` single-row cap:** exclude any single invoice/line > $5,000,000 as a likely data-entry artifact unless the org is known to transact at that scale. (§6.6)
- **Customer grain = billing entity** (`customer_bill_to_number`). No native parent/corporate key (`mapped_code` ~0% populated) → concentration is reported at billing-entity grain; parent roll-up is a gated/suppressed derived artifact. (§7.2)
- **Preflight first:** run `Q-ECON-00` to resolve `TOTAL_BUSINESS_SOURCE` + `COMMERCE_CONFIDENCE` before emitting any number; stamp them on output.

## 1. Where this lives (recommendation — no waffle)
**Both surfaces, one computation authority.** The two heroes are computed **once** by the Insightful invoiced-spine SQL (the same `SUM(portal_invoices.net_amount)` law above) and exposed as a small read model. The **Sales Portal** presents them (Lane 1 wireframe); **Insightful 4.0** consumes the same read model for the CEO report. 

Rationale: the spine explicitly warns the **portal dashboard warehouse rollup is not validation ground truth and can disagree** with the invoiced spine. If the portal computes its own topline off the warehouse and Insightful computes off `portal_invoices`, the client sees two different "totals" — the exact ACL failure the program is trying to avoid. One spine, two presentations. The portal surface must **label which spine it is showing** ("invoiced ledger", not "warehouse dashboard").

## 2. Acceptance criteria (computational, testable, org-reproducible)

### Hero 1 — True Topline
- Emits `topline_invoiced_net = SUM(net_amount)` over the clamped LTM window for the selected org, at STRONG confidence with the single-feed completeness caveat string attached.
- Window is clamped to `report_through_date`; a future-dated invoice never extends the window (regression guard: `clm`/`jyc` bad dates).
- Excludes any single row > $5M unless org is whitelisted; credit memos remain negative (returns net out).
- Reconciles to the portal Customers-page invoiced total for the same org + range (ties the FIX/SERV-2395 work to the same number).
- Reproducible: running the reference SQL below on `sarreid` returns **$16.03M** (LTM ending 2026-07-15); on `cci` returns **$71.14M**.

### Hero 3 — Concentration / single-account risk
- Emits `top1_share`, `top10_share` of LTM invoiced net at billing-entity grain, plus a masked/real top-5 cumulative list.
- Emits a `single_account_risk` boolean = `top1_share >= 0.20` (proposed threshold; owner-tunable) with the dollar exposure of the top account.
- Parent/corporate roll-up is **not** presented (billing-entity grain only) unless a gated fuzzy-match artifact is explicitly requested.
- Reproducible: `sarreid` returns top1 **30.0%** ($4.80M), top10 **46.3%**, `single_account_risk = true`; `cci` returns top1 **6.1%**, top10 **16.8%**, `single_account_risk = false`. (This opposite-shape pair is the required test that the report reads real org shape, not a template.)

### Cross-cutting
- Every emitted number carries `{confidence, feed_completeness, total_business_source, report_through_date}`.
- No number is emitted if `Q-ECON-00` returns `NONE` (suppress + offer behavior-only).

## 3. Prototype / demo plan (using sarreid + cci)
- **Prototype exists:** the read-only Postgres queries below already produced the live figures cited above (run 2026-07-16). The Lane 1 wireframe [`design-system/app/sales-portal-cycle01-mockup.html`](../../design-system/app/sales-portal-cycle01-mockup.html) renders them (masked).
- **Demo slice:** wrap the two queries as a parameterized read model (org_id → JSON with the four provenance stamps) and render into the wireframe for `sarreid` (concentrated) and `cci` (diversified). No pipeline code change; this is a spec + query pair, and the existing Insightful operators own the eventual runtime.
- **Refinement before build:** the prototype queries below use a fixed `CURRENT_DATE`-anchored window; the shipped version must switch to the `report_through_date` clamp (subquery already sketched).

### Reference SQL (read-only; clamp-ready)
```sql
-- report_through_date clamp (per org)
WITH rtd AS (
  SELECT MAX(invoice_date) AS report_through_date
  FROM portal_invoices
  WHERE organization_id = :org_id AND invoice_date <= CURRENT_DATE
),
inv AS (
  SELECT customer_bill_to_number, net_amount
  FROM portal_invoices, rtd
  WHERE organization_id = :org_id
    AND invoice_date >  (rtd.report_through_date - INTERVAL '12 months')
    AND invoice_date <= rtd.report_through_date
    AND net_amount <= 5000000           -- $5M row cap
),
by_cust AS (
  SELECT customer_bill_to_number, SUM(net_amount) AS amt
  FROM inv GROUP BY customer_bill_to_number
),
ranked AS (
  SELECT amt, ROW_NUMBER() OVER (ORDER BY amt DESC) AS rn,
         SUM(amt) OVER () AS topline
  FROM by_cust
)
SELECT
  MAX(topline)                                        AS topline_invoiced_net,   -- Hero 1
  SUM(amt) FILTER (WHERE rn = 1)  / MAX(topline)      AS top1_share,             -- Hero 3
  SUM(amt) FILTER (WHERE rn <= 10) / MAX(topline)     AS top10_share
FROM ranked;
```

## 4. SERV feature-ticket mapping (absorb vs defer)
- **SERV-2382 (Prior-year YTD on Customers)** → **ABSORB.** Same invoiced-spine math over a prior-year window; becomes the period-comparison on Hero 1 (per-customer topline). No new math.
- **SERV-2388 (Per-rep MoM/YoY)** → **ABSORB (gated), phase 2.** Requires rep-identity **Tier 2** (name bridge >= 82%, §7.1). `sarreid` and `cci` are both Tier 2 (100%), so demoable there, but many orgs are Tier 0/1 → must gate and ship `rep_number`-grain fallback. Do not ship per-rep names org-wide in v1.
- **SERV-2425 (Product details xlsx + thumbnails)** → **DEFER.** Export/catalog feature, not a hero answer.
- **SERV-2403 (Scheduled production date on orders)** → **DEFER.** Orders feed, not invoiced spine.
- **EBR-7 (sales totals reflect discounts)** → **CLARIFY/ABSORB.** `net_amount` is already net of discounts; but true margin needs COGS which is a **hard gap** (§6.9) → cannot compute margin, only net revenue. Answer the ticket by confirming net semantics, not by inventing margin.
- **EBR-629 (Trade Name filter on Sales Reports)** → **DEFER.** Useful dimension, but product grouping is org-opaque (§7.4); not a v1 hero.

## 5. Explicit no-gos (Lane 3 / EBR-772 and hard gaps)
- No NL query / talk-to-data / agentic anomaly layer (EBR-772 — parked until Bet C is trusted).
- No capture-rate / attribution presented as a **% of total business** unless `FEED_COMPLETENESS = CORROBORATED` — a single invoice feed caps at STRONG, so present capture in absolute dollars only. (§4)
- No **margin / gross / COGS** (no cost column anywhere — hard gap §6.9). No AR / DSO / collections ("invoiced != collected", §6.7).
- No **"% off list" leakage** (list semantics vary per org; prohibited client-facing — §6.10). Fill/leakage is a later hero and must use tier-aware dispersion.
- No parent/corporate roll-up presented as exact (no native key — §7.2).
- No FULL confidence label on any economics number.

## 6. Handoff
Paste to `05-ORCHESTRATOR` for the Review Card (done in `ORCHESTRATOR-review-cards.md`). Shared heroes with Lane 1 (UX) and dependent on Lane 0 (FIX) for trustworthy territory/date scoping.
